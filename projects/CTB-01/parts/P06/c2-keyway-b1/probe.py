"""Issue 23: ONE C2 key, ONE proposed cheek, local positive-t terminal only."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

from shapely.affinity import translate
from shapely.geometry import LineString, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = "98f0132423bb33adc19b14a3188a662d36e50e1a"
EPS = 1e-6


def run():
    spec = importlib.util.spec_from_file_location("p06_c2_local", HERE.parent / "src/model.py")
    p06 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p06)
    d, _, _, d3, u, b = p06.inputs()
    p02, p03 = p06.p02, p06.p03
    section = p06.sections(d, d3, u)
    r0 = section["joint_center_r_mm"]
    load, park = r0 - 3.8, r0 + 2.6
    # Only the positive-t terminal is changed. Other source ring contours stay as-is.
    original_ring = p06.full_ring("C", d, d3, u)
    old_port = p02.rounded_rect(r0 - 3.2, 13.5, r0 + 3.2, 20.3, .2)
    new_terminal = p02.rounded_rect(r0 - 13, -35, r0 + 13, 35, .5).intersection(
        box(r0 - 13, 0, r0 + 13, 35)
    )
    portal_raw = unary_union([box(r0 - 7, 13.5, r0 - .6, 24.2),
                              box(r0 - .6, 13.5, r0 + 5.8, 25.3)])
    portal = p06.rounded(portal_raw, .2, d)
    ring_profile = original_ring.union(old_port).union(new_terminal).difference(portal)
    local_profile = ring_profile.intersection(box(r0 - 13, 0, r0 + 13, 35))
    key = p06.rounded(unary_union([
        box(13.7, 235, 24, 241.8), box(13.7, 241.8, 19.7, 248.2),
        box(13.7, 248.2, 24, 255),
    ]), .4, d)
    cheek_face, _ = p06.cheek_overlay("C", d, d3, u)
    ring = p02.plate_solid(local_profile, 242, 6)
    cheek = p02.cheek_solid(cheek_face, 7.5, 6)
    station = next(s for s in p02.stations(u) if s["id"] == "S3")
    spacer_face = translate(p02.spacer("B_THROUGH_ADHESIVE", station["part"], u, b), xoff=station["r_mm"])
    fixed = {"P06_local_terminal": ring, "ONE_P01_C_proposed": cheek,
             "nearest_S3": p02.plate_solid(spacer_face, station["z_mm"] - 3, 6),
             "P03_selected_Y": p02.plate_solid(p03.y_profile("A_COMPACT_CLOSED", d3), 407, 6)}

    def solid(poly=key, rc=load, dr=0, dt=0, dz=0):
        if dt or dz:
            poly = p02.swept_polygon(poly, dt, dz)
        slab = p02.cheek_solid(poly, min(-3, -3 - dr), 6 + abs(dr))
        return p06.key_transform(slab, rc, 1, 0)

    def hits(moving, obstacles):
        return {name: round(max(0.0, (moving ^ part).volume()), 9) for name, part in obstacles.items()}

    parked_poly = translate(key, xoff=5)
    parked = solid(parked_poly, park)
    results = []
    evidence = {
        "issue": 23, "candidate": "C2_DUAL_HEAD_RADIAL_DOGLEG", "phase": "LOCAL_B1_ONLY",
        "base_commit": BASE, "release": "DESIGN_ONLY / CR_REQUIRED / INDEPENDENT_QA_PENDING",
        "coordinate_frame": "one L1 positive-t cheek; r=X,t=Y,z=Z; mm",
        "r0_mm": r0, "one_key_only": True, "one_cheek_only": True,
        "geometry": {"key_loading_tz_contour": p02.contour(key),
                     "key_radial_thickness_mm": 6, "loading_r_center": load, "parked_r_center": park,
                     "portal_xy_contour": p02.contour(portal), "local_ring_xy_paths": p06.paths(local_profile),
                     "fillet_radii_mm": {"key": .4, "portal": .2, "terminal_outer": .5},
                     "ring_Z": [242, 248], "key_Z": [235, 255], "terminal_outer_t": 35,
                     "cheek_proposal": "existing P06 C mortise overlay; upstream P01 NOT modified",
                     "source_clearances_mm": {"cheek_gap_loading": 13.7 - 13.5,
                                              "cheek_gap_parked": 18.7 - 13.5,
                                              "S3_vertical": 235 - 203, "Y_vertical": 407 - 255}},
        "cases": results, "epsilon_mm3": EPS,
        "not_run": "six-cheek/mirrored assembly, rotations/6DOF search, renders, production exports, physical fit/strength, unrelated regressions, G2b/G3/G4",
    }

    def test(label, moving, expected, obstacles=fixed, start=None, end=None):
        collisions = hits(moving, obstacles)
        blocked = max(collisions.values(), default=0) > EPS
        okay = blocked == (expected == "BLOCKED")
        row = {"name": label, "expected": expected, "observed": "BLOCKED" if blocked else "CLEAR",
               "verified": okay, "continuous_swept_overlap_mm3": collisions,
               "swept_volume_mm3": round(moving.volume(), 9),
               "start_r_toffset_zoffset": start, "end_r_toffset_zoffset": end}
        if not okay:
            row["failure_intersection_bbox_xyz"] = {
                name: list((moving ^ obstacles[name]).bounding_box())
                for name, v in collisions.items() if v > EPS
            }
        results.append(row)
        return okay

    evidence["profile_checks"] = {
        "key_valid_connected": key.is_valid and key.geom_type == "Polygon",
        "portal_valid_connected": portal.is_valid and portal.geom_type == "Polygon",
        "local_ring_valid_connected": local_profile.is_valid and local_profile.geom_type == "Polygon",
        "proposed_ring_valid_connected": ring_profile.is_valid and ring_profile.geom_type == "Polygon",
        "cheek_valid_connected": cheek_face.is_valid and cheek_face.geom_type == "Polygon",
        "key_single_sheet_H800_W440_with10margin": key.bounds[2] - key.bounds[0] + 20 < 440 and key.bounds[3] - key.bounds[1] + 20 < 800,
        "one_terminal_updated_ring_envelope_sheet_only": ring_profile.bounds[2] - ring_profile.bounds[0] + 20 < 440 and ring_profile.bounds[3] - ring_profile.bounds[1] + 20 < 800,
    }
    if not all(evidence["profile_checks"].values()):
        evidence["decision"] = "NO_GO_INVALID_PROFILE_OR_ENVELOPE"
        return evidence

    # Stop on the FIRST unexpected collision. Never run later paths after failure.
    stages = [
        ("insert_1_lower_Z40_to0", solid(dz=40), [load, 0, 40], [load, 0, 0]),
        ("insert_2_radial_plus6p4", solid(dr=6.4), [load, 0, 0], [park, 0, 0]),
        ("insert_3_tangential_plus5", solid(rc=park, dt=5), [park, 0, 0], [park, 5, 0]),
    ]
    for name, sweep, start, end in stages:
        if not test(name, sweep, "CLEAR", start=start, end=end):
            evidence["decision"] = "NO_GO_INSERTION_BLOCKED"
            return evidence
    if not test("final_finite_key", parked, "CLEAR"):
        evidence["decision"] = "NO_GO_FINAL_CLASH"
        return evidence
    final_static = hits(ring, {name: s for name, s in fixed.items() if name != "P06_local_terminal"})
    evidence["final_ring_vs_cheek_S3_Y_overlap_mm3"] = final_static
    if max(final_static.values()) > EPS:
        evidence["decision"] = "NO_GO_RING_INTERFACE_CLASH"
        return evidence

    trials = [
        ("direct_plusZ40", solid(parked_poly, park, dz=40), "BLOCKED"),
        ("direct_minusZ40", solid(parked_poly, park, dz=-40), "BLOCKED"),
        ("direct_minusR6p4", solid(parked_poly, park, dr=-6.4), "BLOCKED"),
        ("direct_plusR6p4", solid(parked_poly, park, dr=6.4), "BLOCKED"),
        ("direct_plusT5", solid(parked_poly, park, dt=5), "BLOCKED"),
        ("reverse_1_minusT5_OPEN", solid(parked_poly, park, dt=-5), "CLEAR"),
        ("reverse_2_minusR6p4", solid(key, park, dr=-6.4), "CLEAR"),
        ("reverse_3_plusZ40", solid(key, load, dz=40), "CLEAR"),
        ("shortcut_after_minusT5_plusZ40_at_park_R", solid(key, park, dz=40), "CLEAR"),
    ]
    for name, sweep, expectation in trials:
        if not test(name, sweep, expectation):
            evidence["decision"] = "NO_GO_LOCAL_PATH_EXPECTATION_FAILED"
            return evidence

    spread6 = p02.cheek_solid(cheek_face, 7.5, 12)
    spread4 = p02.cheek_solid(cheek_face, 7.5, 10)
    for name, moving, expected, obstacles in [
        ("cheek_spread6_held_key", spread6, "BLOCKED", {"ring": ring, "key_HELD_ONLY_FOR_CONTROL": parked}),
        ("cheek_spread6_key_absent", spread6, "CLEAR", {"ring": ring}),
        ("cheek_spread4_still_FREE_with_held_key", spread4, "CLEAR", {"ring": ring, "key_HELD_ONLY_FOR_CONTROL": parked}),
    ]:
        if not test(name, moving, expected, obstacles):
            evidence["decision"] = "NO_GO_SPREADING_CONTROL_FAILED"
            return evidence

    # Flat shoulder segments at the real filleted head planes. Project onto ring;
    # this is available planar bearing after closing the 0.2 Z gap, NOT contact/load.
    shoulders = {}
    for z in (241.8, 248.2):
        flat = parked_poly.boundary.intersection(LineString([[-100, z], [100, z]]))
        segments = [flat] if flat.geom_type == "LineString" else list(flat.geoms)
        patches = [box(park - 3, line.bounds[0], park + 3, line.bounds[2])
                   for line in segments if line.geom_type == "LineString" and line.length > EPS]
        shoulders[str(z)] = round(unary_union(patches).intersection(local_profile).area, 9)
    evidence["material_screen"] = {
        "loading_head_projection_to_portal_clearance_mm": portal.boundary.distance(box(load - 3, 13.7, load + 3, 24)),
        "parked_true_neck_projection_to_portal_clearance_mm": portal.boundary.distance(
            box(park - 3, parked_poly.intersection(box(-100, 242, 100, 248)).bounds[0],
                park + 3, parked_poly.intersection(box(-100, 242, 100, 248)).bounds[2])
        ),
        "actual_portal_to_outer_edge_min_mm": portal.distance(local_profile.exterior),
        "radial_end_lands_mm": [6, 7.2], "portal_outer_t_land_mm": 9.7,
        "parked_head_outer_t_land_mm": 6,
        "available_flat_shoulder_area_mm2_at_key_Z_planes": shoulders,
        "bearing": "nominal vertical gap0.2; no contact at nominal pose, no strength/physical claim",
        "existing_cheek_outer_land_mm": section["joint_common_r_mm"][1] - (r0 + 13.2),
    }
    evidence["decision"] = "LOCAL_G1_GEOMETRY_PLAUSIBLE / ANTI_T_RETURN_OPEN"
    evidence["open_release_routes"] = [
        "minusT5 then minusR6.4 then plusZ40 (intentional reverse)",
        "minusT5 then plusZ40 directly from parked radial center (shorter escape)",
        "cheek outward free travel5.2 before held key contact; 4mm spread explicitly clear",
        "rotations/combined6DOF not searched; no self-locking or full table claim",
    ]
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    output = run()
    # Integrity read only, not an old CAD/test replay. Geometry source hashes plus
    # git's complete protected tracked-tree comparison bind the unchanged baseline.
    prefixes = ["projects/CTB-01/specifications/CTB-000", "projects/CTB-01/parts"]
    changed = subprocess.run(["git", "diff", BASE, "--", *prefixes,
                              ":(exclude)projects/CTB-01/parts/P06/c2-keyway-b1/**"],
                             cwd=ROOT, capture_output=True, check=True).stdout
    output["upstream_tracked_diff_empty"] = not changed
    output["geometry_source_sha256"] = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for directory in [ROOT / prefixes[0], *[(HERE.parents[1] / f"P{i:02d}/src") for i in range(1, 7)]]
        for path in sorted(directory.glob("*")) if path.is_file()
    }
    if changed:
        raise SystemExit("Protected upstream tracked files changed")
    output["path_case_count"] = len(output["cases"])
    if args.write:
        (HERE / "evidence.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    elif json.loads((HERE / "evidence.json").read_text()) != output:
        raise SystemExit("Saved evidence differs from recomputation")
    print(output["decision"])
    print(f'{len(output["cases"])} local path/pose cases; no six-cheek expansion or production exports.')
