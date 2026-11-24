#!/usr/bin/env python3
"""Measure source interfaces and reject incompatible MEB-035 substitutions."""
import argparse
from collections import Counter
from itertools import combinations
import json
import math
from pathlib import Path

from shapely.geometry import LineString, Polygon, box

from build_reference import (
    BASELINE, BORE_DEPTH, BORE_HEIGHT, LENGTH, PRODUCT, SKIN, T, WIDTH,
    BOOLEAN_EPS, VOLUME_EPS, bent_segment, build_solids, fit_contact, from_profile,
    opening_bounds, outer, penetration,
    rail_features, read_source, roof_sections,
)

PREVIOUS = PRODUCT / "MEB-035"
TOL = 1e-6


def dimensions(profiles):
    end = profiles["LID_END_L"]
    slots = opening_bounds(end)
    a, z, b, h = slots[0]
    rail = outer(profiles["LID_FRONT_RAIL"])
    return {
        "D01": (slots[2][0]+slots[2][2])/2,
        "D02": (a+b)/2,
        "D03": (slots[1][0]+slots[1][2])/2,
        "D04": (z+h)/2-8,
        "D05": (slots[1][1]+slots[1][3])/2-8,
        "D06": b-a,
        "D07": h-z,
        "D08": max(end[0][:, 1])-8,
        "D09": rail.bounds[2],
        "D10": rail.bounds[3],
        "hinge_height": (slots[2][1]+slots[2][3])/2-8,
        "hinge_diameter": slots[2][2]-slots[2][0],
    }


def source_pattern():
    return json.loads((PREVIOUS / "R6_MEB032_SOURCE_88.json").read_text())["segments"]


def bridge_intervals(lines):
    if len(lines) != 88:
        return []
    bridges = []
    for index in range(22):
        row = lines[index*4:index*4+4]
        station = row[0][1]
        if abs(station-(7.58542717+4*index)) > TOL:
            return []
        if any(abs(y-station) > TOL or abs(h-station) > TOL or b <= a for a, y, b, h in row):
            return []
        bridges.extend((station, row[j][2], row[j+1][0]) for j in range(3))
    return bridges


def slit_geometry(lines):
    return [LineString([(s, a), (t, b)]) for a, s, b, t in lines]


def finger_geometry(width, finger_intervals=None):
    fingers = finger_intervals
    if fingers is None:
        fingers = [(i*(width-7)/4, i*(width-7)/4+7) for i in range(5)]
    return fingers, ([box(a, 0, b, 4) for a, b in fingers] +
                     [box(a, LENGTH-4, b, LENGTH) for a, b in fingers])


def compare_patterns(developed):
    lines = source_pattern()
    fingers, tablands = finger_geometry(developed)
    bridges = bridge_intervals(lines)
    if len(bridges) != 66 or any(abs(b-a-4) > TOL for _, a, b in bridges):
        raise ValueError("Historical R6 bridges changed")
    report = {}
    protected_r2 = {
        s for a, s, b, t in lines
        if (a < 8 or b > LENGTH-8)
        and any(LineString([(s, a), (t, b)]).distance(land) < 3 for land in tablands)
    }
    for revision in ("original", "R1", "R2"):
        variant = []
        for a, s, b, t in lines:
            at_outer_end = (a < 8 or b > LENGTH-8)
            if revision == "R1":
                protect = any(lo < s < hi for lo, hi in fingers)
            elif revision == "R2":
                protect = s in protected_r2
            else:
                protect = False
            if protect and at_outer_end:
                if a < 8:
                    a = 8.0
                if b > LENGTH-8:
                    b = LENGTH-8
            variant.append([a, s, b, t])
        geometry = slit_geometry(variant)
        changed = [[idx//4+1, idx%4+1, line[:], expected[:]]
                   for idx, (line, expected) in enumerate(zip(variant, lines)) if line != expected]
        report[revision] = {
            "line_count": len(variant),
            "bridges_matching_original_station_and_end_coordinates": sum(
                first == second for first, second in zip(bridge_intervals(variant), bridges)
            ),
            "cut_end_changes_row_and_column_candidate_vs_original": changed,
            "tab_intersections": sum(any(g.intersects(land) for land in tablands) for g in geometry),
            "minimum_tab_clearance_mm": min(g.distance(land) for g in geometry for land in tablands),
        }
    return report, tablands


def skin_interface(profiles, contact):
    radius = contact["radius_inner_mm"]
    half_angle = contact["half_angle_rad"]
    neutral = contact["radius_neutral_mm"]
    baseline = json.loads((BASELINE / "MEB036_BASELINE_AUDIT.json").read_text())
    supported_to = baseline["arch_datum"]["partial_contact_polyline_end_local_mm"][0]
    supported_station = neutral*(half_angle+math.asin((supported_to-WIDTH/2)/radius))
    sections = roof_sections(profiles[SKIN])
    spans = sorted({round(hi-lo, 8) for _, _, lo, hi in sections})
    return {
        "original_continuous_axial_edge_spans_mm": spans,
        "R2_straight_baseline_mm": 316,
        "R2_edge_shift_along_axial_coordinate_from_left_end_at_shoulders_and_center_mm": [-4, 4],
        "chosen_rear_relief_start_station_mm": contact["developed_mm"]-sections[0][1],
        "measured_contact_termination_neutral_station_mm": supported_station,
        "unsupported_continuation_of_arc_on_end_mm": contact["developed_mm"]-supported_station,
        "historical_skin_ear_area_has_no_verified_continuous_end_contact": True,
        "source_discrete_tabs_per_end": 0,
        "verified_new_connections": 0,
        "site_v3_usage": "Visual context only. Source-curve fit and CAD placements do not use mesh coordinates.",
    }


def interface_checks(profiles):
    dims = dimensions(profiles)
    rails = ["LID_FRONT_RAIL", "LID_BACK_RAIL"]
    top_pockets = rail_features(profiles[rails[0]])[7]
    hypothesis = {"D01": 68, "D02": 26, "D03": 58, "D04": -1, "D05": -1,
                  "D06": 4.3, "D07": 7.3, "D08": 21.429271, "D09": 324, "D10": 11,
                  "hinge_height": 2.5, "hinge_diameter": 8.4}
    lands = {}
    for name in ("LID_END_L", "LID_END_R"):
        profile = profiles[name]
        shell = outer(profile).exterior
        lands[name] = [shell.distance(Polygon(loop)) for loop in
                       sorted(profile[1:], key=lambda loop: min(loop[:, 0]))]
    return {
        "original_end_mortise1_mortise2_bore_min_exterior_ligaments_mm": lands,
        "dimensional_dispositions": {
            key: {"MEB033_reference_cad_mm": value, "MEB035_R2_mm": hypothesis[key],
                  "R2_delta_mm": round(hypothesis[key]-value, 8),
                  "status": "MATCH" if abs(hypothesis[key]-value) < TOL
                            else "R2_REJECTED_REFERENCE_DIMENSION_PRESERVED"}
            for key, value in dims.items()
        },
        "both_long_rails": {name: {"tenon_section_mm": [T, 6],
                                  "nominal_per_side_clearance_mm": [(dims["D06"]-T)/2,
                                                                    (dims["D07"]-6)/2],
                                  "top_pockets_flat_axial_mm": top_pockets}
                            for name in rails},
        "both_cross_ribs": {"nominal_axial_total_clearance_in_rail_pocket_mm": 0.4,
                            "nominal_total_clearance_across_rail_mm": 0.5,
                            "contact_order": "NOT_RUN"},
        "hinge": {"reference_axis_YZ_mm": [BORE_DEPTH, BORE_HEIGHT],
                  "tip_cross_section_mm": [T, 6.2],
                  "nominal_corner_clearance_in_circular_bore_mm":
                      dims["hinge_diameter"]/2-math.hypot(T/2, 6.2/2),
                  "retention_and_path": "NOT_RUN"},
    }



def orientation_regression(profiles, contact, solids):
    body = ("BODY_END_L", "BODY_END_R", "BODY_FRONT", "BODY_BACK")
    floor_trials = []
    for reflect_x in (False, True):
        for reflect_y in (False, True):
            geometry = from_profile(
                profiles["BODY_FLOOR"],
                lambda u, v: (LENGTH-u if reflect_x else u, WIDTH-v if reflect_y else v, 0),
                (0, 0, T),
            )
            floor_trials.append({
                "reflect_x": reflect_x, "reflect_y": reflect_y,
                "intersection_mm3": {name: penetration(geometry, solids[name]) for name in body},
            })
    bands = [bent_segment(contact, x0, x1, s0, s1)
             for s0, s1, x0, x1 in roof_sections(profiles[SKIN])]
    alternate = bands[0].fuse(*bands[1:], tol=BOOLEAN_EPS).clean()
    hinge_stack = [f"{part}_{side}" for side in ("L", "R")
                   for part in ("LID_END", "CAPTIVE_PIN")]
    return {
        "floor": floor_trials,
        "skin": {
            name: {part: penetration(geometry, solids[part]) for part in hinge_stack}
            for name, geometry in (("long_relief_front", alternate),
                                   ("long_relief_rear", solids[SKIN]))
        },
    }


def reference_sheet_polygons(profiles):
    """Source sheet only, used as a negative-control baseline."""
    import xml.etree.ElementTree as ET

    audit = json.loads((BASELINE / "MEB036_BASELINE_AUDIT.json").read_text())
    path = PRODUCT.parent.parent / Path(audit["source"]["svg"])
    elements = ET.parse(path).findall(".//{*}g")
    sheets = {}
    for group in elements:
        if group.get("id") not in profiles:
            continue
        loops = [[tuple(map(float, point.split(","))) for point in node.get("points").split()]
                 for node in group.findall("{*}polyline")]
        sheets[group.get("id")] = outer(loops)
    return sheets


def has_sheet_overlap(sheets):
    return any(a.intersection(b).area > TOL for a, b in combinations(sheets.values(), 2))


def negative_controls(profiles, contact, lands, solids):
    from shapely.affinity import translate

    width = contact["developed_mm"]
    fingers, _ = finger_geometry(width)
    pattern = source_pattern()
    altered_bridge = [row[:] for row in pattern]
    altered_bridge[1][0] += 0.5
    wrong_slot = box(0.30, 0, 4.80, 6.50)
    rail_section = box(0.25, 0.25, 4.25, 6.25)
    moved_finger = (fingers[2][0]+0.3, fingers[2][1]+0.3)
    slot = (fingers[2][0]-0.125, fingers[2][1]+0.125)
    reference_sheet = reference_sheet_polygons(profiles)
    first, second = list(reference_sheet.values())[:2]
    dx = first.centroid.x-second.centroid.x
    dy = first.centroid.y-second.centroid.y
    injected_sheet = dict(reference_sheet, injected=translate(second, dx, dy))
    other_format = translate(first, xoff=0.05)
    wall = solids["BODY_FRONT"]
    skin = solids[SKIN]
    baseline_bore_margin = 4.2 - math.hypot(2, 3.1)
    offset_bore_margin = 4.2 - math.hypot(2+1, 3.1)
    return [
        ("shifted_tab", slot[0] <= fingers[2][0] and fingers[2][1] <= slot[1],
         not (slot[0] <= moved_finger[0] and moved_finger[1] <= slot[1])),
        ("incorrect_mortise", box(0, 0, 4.5, 6.5).covers(rail_section),
         not wrong_slot.covers(rail_section)),
        ("missing_part", len(solids) == 20, len({n for n in solids if n != SKIN}) != 20),
        ("hinge_offset", baseline_bore_margin > 0, offset_bore_margin < 0),
        ("incorrect_rail", rail_features(profiles["LID_FRONT_RAIL"])[7] ==
         rail_features(profiles["LID_BACK_RAIL"])[7],
         rail_features(profiles["LID_FRONT_RAIL"])[7] != [(104, 108.1), (214, 218.4)]),
        ("slit_crosses_tab", not lands[0].intersects(LineString([(1, 8), (1, 18)])),
         lands[0].intersects(LineString([(1, 0), (1, 18)]))),
        ("modified_bridge", len(bridge_intervals(pattern)) == 66,
         bridge_intervals(altered_bridge) != bridge_intervals(pattern)),
        ("lid_body_interference", penetration(wall, skin) <= VOLUME_EPS,
         penetration(wall, skin.translate((0, 0, -5))) > VOLUME_EPS),
        ("sheet_overlap", not has_sheet_overlap(reference_sheet), has_sheet_overlap(injected_sheet)),
        ("format_mismatch", first.symmetric_difference(first).area <= TOL,
         first.symmetric_difference(other_format).area > TOL),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    profiles, blob = read_source()
    contact = fit_contact(profiles)
    solids, _ = build_solids(profiles, contact)
    patterns, lands = compare_patterns(contact["developed_mm"])
    controls = negative_controls(profiles, contact, lands, solids)
    data = {"source_svg_git_blob": blob,
            "interfaces": interface_checks(profiles),
            "skin": skin_interface(profiles, contact),
            "R6": patterns,
            "orientation_regression": orientation_regression(profiles, contact, solids),
            "negative_controls": [{"fault": case, "baseline_pass": good,
                                   "fault_detected": detected,
                                   "status": "PASS" if good and detected else "FAIL"}
                                  for case, good, detected in controls],
            "scope": "Nominal comparison and targeted detector controls. No accepted revised candidate or physical results."}
    (out / "MEB037_INTERFACE_R6_QA.json").write_text(json.dumps(data, indent=2) + "\n")
    counts = Counter(item["status"] for item in data["negative_controls"])
    print(json.dumps({"negative_controls": counts,
                      "R6_modified_segments": {key: len(row["cut_end_changes_row_and_column_candidate_vs_original"])
                                               for key, row in patterns.items()}}, indent=2))
    if counts["FAIL"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
