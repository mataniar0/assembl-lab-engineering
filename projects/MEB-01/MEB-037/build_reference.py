#!/usr/bin/env python3
"""Reconstruct and audit a nominal MEB-033 assembly hypothesis in mm."""
import argparse
import csv
import hashlib
from importlib.metadata import version
from itertools import combinations
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

import cadquery as cq
import numpy as np
from shapely.geometry import LineString, Polygon

HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
SOURCE = PRODUCT / "MEB-033" / "cutting"
BASELINE = PRODUCT / "MEB-036"
SKIN = "LID_SKIN_RADIAL_4MM"
T = 4.0
LENGTH = 324.0
WIDTH = 77.0
BORE_HEIGHT = 75.0
BORE_DEPTH = 75.0
LIP_HEIGHT = BORE_HEIGHT - 2.5
VOLUME_EPS = 1e-4  # mm³, detection threshold for this run
DISTANCE_EPS = 1e-5  # mm, boundary-contact resolution
BOOLEAN_EPS = 1e-7  # mm, OCC fuzzy Boolean parameter


def read_source():
    audit = json.loads((BASELINE / "MEB036_BASELINE_AUDIT.json").read_text())
    path = SOURCE / Path(audit["source"]["svg"]).name
    data = path.read_bytes()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if blob != audit["source"]["svg_blob"]:
        raise ValueError(f"Unexpected MEB-033 SVG blob {blob}")
    profiles = {}
    for group in ET.fromstring(data).findall(".//{*}g"):
        loops = [
            [tuple(map(float, point.split(","))) for point in line.get("points").split()]
            for line in group.findall("{*}polyline")
        ]
        if not loops:
            continue
        origin = np.min(loops[0], axis=0)
        local = []
        for loop in loops:
            points = np.round(np.asarray(loop) - origin, 8)
            if np.linalg.norm(points[0] - points[-1]) < BOOLEAN_EPS:
                points = points[:-1]
            local.append(points)
        profiles[group.get("id")] = local
    return profiles, blob


def outer(profile):
    return Polygon(profile[0], profile[1:])


def opening_bounds(profile):
    return sorted([Polygon(loop).bounds for loop in profile[1:]])


def fit_contact(profiles):
    """Use two independent end curves and the common tangent reference at u=0."""
    fit = []
    for name in ("LID_END_L", "LID_END_R"):
        outline = profiles[name][0]
        x, z = outline[(outline[:, 0] < 68.87) & (outline[:, 1] > 20)].T
        cx, cz, constant = np.linalg.lstsq(
            np.column_stack((2*x, 2*z, np.ones_like(x))), x*x + z*z, rcond=None
        )[0]
        radius = math.sqrt(constant + cx*cx + cz*cz)
        residual = max(abs(np.hypot(x-cx, z-cz)-radius))
        if residual >= DISTANCE_EPS or abs(cx - WIDTH/2) >= DISTANCE_EPS:
            raise ValueError(f"End profile {name} does not match the radial contact hypothesis")
        fit.append((radius, float(cz-8), float(residual)))
    radius, center, residual = fit[0]
    half_angle = math.asin(WIDTH / (2*radius))
    neutral = radius + T/2
    developed = 2 * half_angle * neutral
    measured = max(profiles[SKIN][0][:, 0])
    if abs(developed - measured) >= DISTANCE_EPS:
        raise ValueError("Skin width disagrees with the end-curve neutral length")
    if abs(fit[1][0] - radius) >= DISTANCE_EPS or abs(fit[1][1] - center) >= DISTANCE_EPS:
        raise ValueError("End-curve fits disagree")
    return {
        "radius_inner_mm": radius,
        "center_depth_mm": WIDTH/2,
        "center_height_mm": LIP_HEIGHT + center,
        "half_angle_rad": half_angle,
        "radius_neutral_mm": neutral,
        "developed_mm": developed,
        "inner_arc_mm": 2 * half_angle * radius,
        "outer_arc_mm": 2 * half_angle * (radius+T),
        "max_radial_fit_residual_mm": max(row[2] for row in fit),
    }


def from_profile(profile, placement, direction):
    wires = [
        cq.Wire.makePolygon([cq.Vector(*placement(*point)) for point in loop], close=True)
        for loop in profile
    ]
    return cq.Solid.extrudeLinear(wires[0], wires[1:], cq.Vector(*direction))


def bend_point(contact, station, radius, axial):
    angle = station / contact["radius_neutral_mm"] - contact["half_angle_rad"]
    return cq.Vector(axial, contact["center_depth_mm"] + radius*math.sin(angle),
                     contact["center_height_mm"] + radius*math.cos(angle))


def bent_segment(contact, x0, x1, s0, s1):
    r = contact["radius_inner_mm"]
    point = lambda s, radius: bend_point(contact, s, radius, x0)
    middle = (s0+s1)/2
    edges = [
        cq.Edge.makeThreePointArc(point(s0, r), point(middle, r), point(s1, r)),
        cq.Edge.makeLine(point(s1, r), point(s1, r+T)),
        cq.Edge.makeThreePointArc(point(s1, r+T), point(middle, r+T), point(s0, r+T)),
        cq.Edge.makeLine(point(s0, r+T), point(s0, r)),
    ]
    return cq.Solid.extrudeLinear(cq.Wire.assembleEdges(edges), [], cq.Vector(x1-x0, 0, 0))


def roof_sections(profile):
    polygon = outer(profile)
    stations = sorted(set(profile[0][:, 0]))
    sections = []
    for start, end in zip(stations, stations[1:]):
        middle = (start+end)/2
        section = polygon.intersection(LineString([(middle, -1), (middle, LENGTH+1)]))
        if section.geom_type != "LineString":
            raise ValueError("Unexpected discontinuity in historical skin")
        _, axial_min, _, axial_max = section.bounds
        sections.append((start, end, axial_min, axial_max))
    return sections


def rail_features(profile):
    """Recover top rib and bottom saddle stations from pocket floors."""
    points = profile[0]
    pockets = {7: [], 4.25: []}
    for (a, z), (b, next_z) in zip(points, np.roll(points, -1, axis=0)):
        if z == next_z and z in pockets:
            pockets[z].append(tuple(sorted((a, b))))
    return {height: sorted(spans) for height, spans in pockets.items()}


def build_solids(profiles, contact):
    solids = {}
    place = {}

    def add(name, placement, direction, evidence):
        solids[name] = from_profile(profiles[name], placement, direction)
        place[name] = evidence

    add("BODY_FLOOR", lambda u, v: (u, v, 0), (0, 0, T),
        "Registered floor teeth to four bottom edges by checking the four axis-preserving orientations.")
    for name, depth in (("BODY_FRONT", 0), ("BODY_BACK", WIDTH-T)):
        add(name, lambda u, v: (u, depth, v), (0, T, 0),
            "Registered bottom and corner fingers, short wall at hinge side.")
    for side, end_x, sign in (("L", 0, 1), ("R", LENGTH, -1)):
        add(f"BODY_END_{side}", lambda u, v: (end_x, u, v), (sign*T, 0, 0),
            "Registered corner and floor fingers, rear recess faces positive Y.")
        add(f"LID_END_{side}", lambda u, v: (end_x, u, LIP_HEIGHT+v-8),
            (sign*T, 0, 0), "Matched bore to body recess; axial slab from rail tenon shoulders.")
        for key, layers in (("FASCIA_HIDDEN_BACKER", 1), ("OUTER_FASCIA", 2)):
            name = f"{key}_{side}"
            height = max(profiles[name][0][:, 0])
            (xmin, ymin, xmax, ymax), = opening_bounds(profiles[name])
            add(name, lambda u, v: (end_x-sign*layers*T, BORE_DEPTH+v-(ymin+ymax)/2,
                                   height-u), (sign*T, 0, 0),
                "Square bottom on Z=0 and bore on hinge axis; outside face stack hypothesized.")
        pin_width = max(profiles[f"CAPTIVE_PIN_{side}"][0][:, 0])
        add(f"CAPTIVE_PIN_{side}", lambda u, v: (end_x+sign*((u if side == "L" else pin_width-u)-2*T),
                                               BORE_DEPTH-T/2, BORE_HEIGHT+v-5),
            (0, T, 0), "4 mm shoulders matched to the 2 fascia layers and narrower tip to bore.")

    slots = opening_bounds(profiles["LID_END_L"])[:2]
    slot_centers = [(a+c)/2 for a, _, c, _ in slots]
    rail_z = LIP_HEIGHT + (slots[0][1]+slots[0][3])/2-8-6
    rail_x = (LENGTH-max(profiles["LID_FRONT_RAIL"][0][:, 0]))/2
    features = rail_features(profiles["LID_FRONT_RAIL"])
    if features != rail_features(profiles["LID_BACK_RAIL"]):
        raise ValueError("Rail notch features differ")
    for name, depth in zip(("LID_FRONT_RAIL", "LID_BACK_RAIL"), slot_centers):
        add(name, lambda u, v: (rail_x+u, depth-T/2, rail_z+v), (0, T, 0),
            "End mortise Y/Z centers; centered original rail length; tenon shoulders at X=4/320.")
    for index, (start, end) in enumerate(features[7], 1):
        x = rail_x + (start+end-T)/2
        add(f"LID_CROSS_RIB_{index}", lambda u, v: (x, u+5, rail_z+7-13.25+v),
            (T, 0, 0), "Rail pockets set the rib X; matching 13 mm notch spacing sets Y; floors set Z.")
    for side, (start, end) in zip(("L", "R"), features[4.25]):
        x = rail_x+(start+end-T)/2
        add(f"INTERNAL_RAIL_SADDLE_{side}", lambda u, v: (x, slot_centers[0]-4.5+u,
                                                          rail_z+4.25-9.95+v), (T, 0, 0),
            "Hypothesis: lower two-slot saddle mates with the end pockets of both rails, moves with lid.")
    sections = roof_sections(profiles[SKIN])
    end = max(profiles[SKIN][0][:, 0])
    bands = [bent_segment(contact, x0, x1, end-s1, end-s0) for s0, s1, x0, x1 in sections]
    solids[SKIN] = bands[0].fuse(*bands[1:], tol=BOOLEAN_EPS).clean()
    place[SKIN] = "Historical 308/324/308 spans; long relief towards rear identified by testing both orientations; rigid uncut material envelope."
    invalid = [name for name, shape in solids.items()
               if not shape.isValid() or len(shape.Solids()) != 1]
    if invalid:
        raise ValueError(f"Invalid or disconnected part solids: {invalid}")
    return solids, place


def separation(a, b):
    ab, bb = a.BoundingBox(), b.BoundingBox()
    return max(ab.xmin-bb.xmax, bb.xmin-ab.xmax, ab.ymin-bb.ymax, bb.ymin-ab.ymax,
               ab.zmin-bb.zmax, bb.zmin-ab.zmax)


def penetration(a, b):
    if separation(a, b) > DISTANCE_EPS:
        return 0.0
    common = a.intersect(b, tol=BOOLEAN_EPS)
    return sum(abs(solid.Volume()) for solid in common.Solids())


def pair_result(a, b):
    gap = separation(a, b)
    if gap > DISTANCE_EPS:
        return "NO_CONTACT", 0.0, gap, "AABB_GAP_LOWER_BOUND"
    volume = penetration(a, b)
    if volume > VOLUME_EPS:
        return "UNAUTHORIZED_INTERFERENCE", volume, 0.0, "OCC_BOOLEAN"
    distance = a.distance(b)
    state = "CONTACT_UNASSESSED" if distance <= DISTANCE_EPS else "NO_CONTACT"
    return state, volume, distance, "OCC_BOOLEAN_AND_DISTANCE"


def write_model(solids, name, destination):
    assembly = cq.Assembly(name=name)
    for part, shape in solids.items():
        color = cq.Color(0.76, 0.53, 0.31) if is_moving(part) else cq.Color(0.87, 0.68, 0.44)
        assembly.add(shape, name=part, color=color)
    assembly.export(str(destination), tolerance=0.025, angularTolerance=0.1)


def is_moving(name):
    return name.startswith(("LID_", "INTERNAL_RAIL_SADDLE_"))


def moved(solids, angle):
    # Negative rotation about +X lifts the front of the lid (Y < pivot).
    axis = (0, BORE_DEPTH, BORE_HEIGHT)
    return {name: shape.rotate(axis, (1, *axis[1:]), -angle) if is_moving(name) else shape
            for name, shape in solids.items()}


def documented_joints():
    body_edges = [("BODY_FLOOR", part)
                  for part in ("BODY_FRONT", "BODY_BACK", "BODY_END_L", "BODY_END_R")]
    rails = ("LID_FRONT_RAIL", "LID_BACK_RAIL")
    corners = [(wall, end) for wall in ("BODY_FRONT", "BODY_BACK")
               for end in ("BODY_END_L", "BODY_END_R")]
    rail_joints = [(rail, part) for rail in rails for part in
                   ("LID_END_L", "LID_END_R", "LID_CROSS_RIB_1", "LID_CROSS_RIB_2")]
    return {frozenset(pair) for pair in body_edges+corners+rail_joints}


def overlap_bounds(a, b):
    common = a.intersect(b, tol=BOOLEAN_EPS)
    return [tuple(getattr(solid.BoundingBox(), name) for name in
                  ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax"))
            for solid in common.Solids() if abs(solid.Volume()) > VOLUME_EPS]


def assemble(out, solids, pose, profiles, contact, blob):
    rows = []
    joints = documented_joints()
    for part_a, part_b in combinations(solids, 2):
        state, volume, gap, method = pair_result(solids[part_a], solids[part_b])
        if state == "CONTACT_UNASSESSED" and frozenset((part_a, part_b)) in joints:
            state = "INTENDED_NOMINAL_JOINT"
        rows.append([part_a, part_b, state, volume, gap, method])
    with (out / "MEB037_PAIR_REGISTER.csv").open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["part_a", "part_b", "reference_static_class", "intersection_mm3",
                         "distance_or_bound_mm", "method"])
        writer.writerows(rows)
    failures = sorted((r[:4] for r in rows if r[2] == "UNAUTHORIZED_INTERFERENCE"),
                      key=lambda row: -row[3])

    # Positive-volume interference in any required state is sufficient to reject
    # that hypothesis. Passing samples alone never establish continuous motion.
    motion = []
    for angle in (0, 5, 15, 30, 60, 90, 110):
        if angle == 0:
            collisions = [r for r in failures if is_moving(r[0]) != is_moving(r[1])]
        else:
            trial = moved(solids, angle)
            collisions = []
            for a, b in combinations(trial, 2):
                if is_moving(a) == is_moving(b):
                    continue
                volume = penetration(trial[a], trial[b])
                if volume > VOLUME_EPS:
                    collisions.append([a, b, "UNAUTHORIZED_INTERFERENCE", volume])
        motion.append({"deg": angle, "body_lid_collisions": collisions})
    data = {
        "status": "DESIGN_ONLY_SOURCE_RECONSTRUCTION",
        "source_svg_git_blob": blob,
        "units": "mm",
        "kernel": {"CadQuery": version("cadquery"), "OCP": version("cadquery-ocp"),
                   "fuzzy_boolean_mm": BOOLEAN_EPS, "volume_threshold_mm3": VOLUME_EPS,
                   "contact_threshold_mm": DISTANCE_EPS},
        "pose_evidence": pose,
        "contact_curve": contact,
        "skin_sections_station_to_axial_mm": roof_sections(profiles[SKIN]),
        "parts": len(solids),
        "pairs": len(rows),
        "pair_states": {key: sum(row[2] == key for row in rows) for key in
                        ("NO_CONTACT", "INTENDED_NOMINAL_JOINT", "CONTACT_UNASSESSED",
                         "UNAUTHORIZED_INTERFERENCE")},
        "closed_pose_interferences": failures,
        "closed_positive_intersection_bounds_xyz_mm": {
            f"{a}/{b}": overlap_bounds(solids[a], solids[b]) for a, b, _, _ in failures
        },
        "motion_samples": motion,
        "continuous_range": "FAIL_REFERENCE" if any(r["body_lid_collisions"] for r in motion)
                            else "NOT_RUN",
        "insertion_paths": "NOT_RUN",
        "independent_QA": "INDEPENDENT_QA_PENDING",
    }
    (out / "MEB037_REFERENCE_QA.json").write_text(json.dumps(data, indent=2) + "\n")
    write_model(solids, "meb037_closed_reference", out / "MEB037_CLOSED_DESIGN_ONLY.step")
    write_model(solids, "meb037_closed_reference", out / "MEB037_CLOSED_DESIGN_ONLY.glb")
    write_model(moved(solids, 110), "meb037_open_reference_110",
                out / "MEB037_OPEN_110_DESIGN_ONLY.glb")
    center = cq.Vector(LENGTH/2, WIDTH/2, 50)
    exploded = {name: shape.translate((shape.Center()-center).multiply(0.6))
                for name, shape in solids.items()}
    write_model(exploded, "meb037_exploded_reference", out / "MEB037_EXPLODED_DESIGN_ONLY.glb")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    profiles, blob = read_source()
    contact = fit_contact(profiles)
    solids, pose = build_solids(profiles, contact)
    bom = list(csv.DictReader((BASELINE / "MEB036_BOM.csv").open()))
    if len(solids) != 20 or set(solids) != {row["part_id"] for row in bom if row["role"] == "product"}:
        raise ValueError("Mismatch against 20-part source BOM")
    with (out / "MEB037_BOM.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=[*bom[0], "pose_basis"], lineterminator="\n")
        writer.writeheader()
        for row in bom:
            basis = pose.get(row["part_id"], "Separate bending jig outside the product assembly.")
            status = "REFERENCE_HYPOTHESIS" if row["part_id"] in solids else "OUTSIDE_PRODUCT"
            writer.writerow(dict(row, assembly_pose=status, pose_basis=basis))
    data = assemble(out, solids, pose, profiles, contact, blob)
    print(json.dumps({key: data[key] for key in
                      ("parts", "pair_states", "continuous_range")}, indent=2))


if __name__ == "__main__":
    main()
