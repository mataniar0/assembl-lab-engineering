"""Issue34: one bonded P01/ring terminal, actual SVG coordinates, local B1 only."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
from xml.etree import ElementTree as ET

from shapely.affinity import translate
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
P06 = HERE.parents[1]
ROOT = P06.parents[3]
BASE = "a4f3cf09224736ec24c247e18967b5c2e5b438ee"
EPS = 1e-6


def read_profile(path):
    root = ET.parse(path).getroot()
    loops = [[tuple(map(float, xy.split(","))) for xy in p.attrib["points"].split()]
             for p in root.findall(".//{*}polygon")]
    # Exported polygon coordinates are the documented mechanical mm coordinates.
    # scale(1,-1) is their SVG display transform, not a negative mechanical Z.
    return Polygon(loops[0], loops[1:]), loops, root.attrib.get("viewBox")


def run():
    spec = importlib.util.spec_from_file_location("p06_bonded_local", P06 / "src/model.py")
    p06 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p06)
    d, _, _, d3, u, b = p06.inputs()
    p02, p03 = p06.p02, p06.p03
    folder = P06 / "adhesive-study/candidate-v1"
    cheek_file = folder / "P01_BONDED_UNIFIED_V1_DESIGN_ONLY.svg"
    ring_file = folder / "P06C_BONDED_V1_DESIGN_ONLY.svg"
    old_cheek_file = P06.parent / "P03/variants/A_COMPACT_CLOSED/P01-Y-mortise-study-v1.svg"
    old_ring_file = P06 / "variants/C/P06C.svg"
    cheek_face, cheek_loops, cheek_viewbox = read_profile(cheek_file)
    ring_face, ring_loops, ring_viewbox = read_profile(ring_file)
    old_cheek_face, old_cheek_loops, _ = read_profile(old_cheek_file)
    old_ring_face, old_ring_loops, _ = read_profile(old_ring_file)
    r0 = p06.sections(d, d3, u)["joint_center_r_mm"]
    # Crop at the exported SVG precision; do not truncate its radial edge by
    # mixing an unrounded parametric bound with six-decimal source vertices.
    crop = box(round(r0 - 13, 6), 0, round(r0 + 13, 6), 26.5)
    local, old_local = ring_face.intersection(crop), old_ring_face.intersection(crop)
    out = {
        "issue": 34, "phase": "ONE_CHANGED_INTERFACE_B1", "base_commit": BASE,
        "decision": "LOCAL_NO_GO", "release": "DESIGN_ONLY / INDEPENDENT_QA_PENDING",
        "functional_gates": "BOND_CAPACITY_UNKNOWN / G2b_NOT_PASSED / G3_G4_NOT_APPROVED",
        "units_axes": "mm; one L1 positive-t cheek, r=X,t=Y,z=Z",
        "local_model": {"cheek_t": [7.5, 13.5], "ring_Z": [242, 248],
                        "terminal_crop_xy": list(crop.bounds), "insertion_t_offset": [40, 0],
                        "wooden_P08_or_keeper_bodies": 0},
        "source_fidelity": {
            "candidate_cheek_seven_loops": len(cheek_loops) == 7,
            "original_outer_and_five_mortises_exact": cheek_loops[:6] == old_cheek_loops,
            "candidate_ring_two_loops": len(ring_loops) == 2,
            "original_ring_outer_and_central_hole_exact": ring_loops == old_ring_loops[:2],
            "valid_connected_candidate_polygons": all(p.is_valid and p.geom_type == "Polygon" for p in (cheek_face, ring_face, local)),
        },
        "source_metadata_defect": {
            "candidate_P01_viewBox": cheek_viewbox, "candidate_P06_viewBox": ring_viewbox,
            "finding": "Both viewBox attributes contain labels rather than four numbers; numeric viewport text is in title. Inherited source packaging defect, NOT repaired here. Raw mechanical polygons are used, not SVG rendering. This local CAD result does not validate SVG viewer/export packaging.",
        },
        "cases": [], "epsilon_mm3": EPS,
    }
    if not all(out["source_fidelity"].values()):
        out["stop_reason"] = "Invalid candidate polygon or source fidelity mismatch"
        return out
    ring = p02.plate_solid(local, 242, 6)
    old_ring = p02.plate_solid(old_local, 242, 6)
    added = p02.plate_solid(local.difference(old_local), 242, 6)
    cheek = p02.cheek_solid(cheek_face, 7.5, 6)
    initial = p02.cheek_solid(cheek_face, 47.5, 6)
    swept = p02.cheek_solid(cheek_face, 7.5, 46)  # exact union over straight t40→0
    station = next(s for s in p02.stations(u) if s["id"] == "S3")
    spacer_face = translate(p02.spacer("B_THROUGH_ADHESIVE", station["part"], u, b), xoff=station["r_mm"])
    fixed = {"bonded_ring_terminal": ring,
             "nearest_S3": p02.plate_solid(spacer_face, station["z_mm"] - 3, 6),
             "selected_Y": p02.plate_solid(p03.y_profile("A_COMPACT_CLOSED", d3), 407, 6)}

    def test(name, moving, obstacles, expect_blocked=False):
        hits = {k: round(max(0.0, (moving ^ s).volume()), 9) for k, s in obstacles.items()}
        blocked = max(hits.values(), default=0) > EPS
        row = {"name": name, "overlap_mm3": hits, "expected": "BLOCKED" if expect_blocked else "CLEAR",
               "verified": blocked == expect_blocked, "moving_volume_mm3": round(moving.volume(), 9)}
        if not row["verified"]:
            row["intersection_bbox_xyz"] = {k: list((moving ^ obstacles[k]).bounding_box()) for k, v in hits.items() if v > EPS}
        out["cases"].append(row)
        return row["verified"]

    for name, moving, obstacles, blocked in [
        ("original_unmortised_cheek_old_ring_negative", p02.cheek_solid(old_cheek_face, 7.5, 6), {"old_ring": old_ring}, True),
        ("candidate_initial_t40", initial, fixed, False),
        ("candidate_final_t0", cheek, fixed, False),
        ("real_Y_FIRST_full_continuous_t40_to0", swept, fixed, False),
        ("candidate_final_old_apertured_ring", cheek, {"old_ring": old_ring}, False),
        ("filled_hole_material_full_cheek_sweep", swept, {"added_ring_material": added}, False),
        ("ring_vs_S3_Y", ring, {k: v for k, v in fixed.items() if k != "bonded_ring_terminal"}, False),
        ("thickness6p8_negative_control", p02.plate_solid(local, 241.6, 6.8), {"candidate_cheek": cheek}, True),
    ]:
        if not test(name, moving, obstacles, blocked):
            out["stop_reason"] = name
            return out

    slot = Polygon(cheek_loops[-1])
    band = local.intersection(box(-1000, 7.5, 1000, 13.5))
    rmin, _, rmax, _ = band.bounds
    section = box(rmin, 242, rmax, 248)
    out["gap_material_measurements"] = {
        "slot_rz_bounds": list(slot.bounds), "ring_at_cheek_rz_bounds": list(section.bounds),
        "radial_edge_gaps_mm": [rmin - slot.bounds[0], slot.bounds[2] - rmax],
        "axial_face_gaps_mm": [242 - slot.bounds[1], slot.bounds[3] - 248],
        "minimum_actual_contour_gap_mm": slot.boundary.distance(section),
        "mortise_to_outer_silhouette_min_wood_mm": slot.distance(Polygon(cheek_loops[0]).exterior),
        "mortise_to_other_five_mortises_min_wood_mm": slot.distance(unary_union([Polygon(c) for c in cheek_loops[1:6]])),
        "local_hole_fill_area_mm2": local.difference(old_local).area,
        "potential_single_face_projection_mm2": band.area,
        "ring_to_S3_Z_gap_mm": 242 - 203, "ring_to_Y_Z_gap_mm": 407 - 248,
        "contact": "positive axial gaps; zero nominal face contact; projected area is NOT effective bond area",
    }
    out["decision"] = "LOCAL_CAD_GEOMETRY_GO_ONLY"
    out["not_run"] = "six-cheek/32-body integrated assembly, bond/fixture/cure access or capacity, old unaffected suites, G2b/G3/G4"
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    protected = ["projects/CTB-01/specifications/CTB-000", "projects/CTB-01/parts"]
    diff = subprocess.run(["git", "diff", BASE, "--", *protected,
                           ":(exclude)projects/CTB-01/parts/P06/adhesive-study/local-b1/**"],
                          cwd=ROOT, capture_output=True, check=True).stdout
    result["protected_tracked_diff_empty"] = not diff
    if diff:
        raise SystemExit("Protected source changed")
    files = [*[(ROOT / protected[0]) / "CTB-000_parameters.json"],
             *[p for i in range(1, 7) for p in (P06.parent / f"P{i:02d}/src").glob("*") if p.is_file()],
             *[p for p in (P06 / "adhesive-study/candidate-v1").glob("*.svg")],
             P06 / "variants/C/P06C.svg", P06.parent / "P03/variants/A_COMPACT_CLOSED/P01-Y-mortise-study-v1.svg"]
    result["source_sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    result["unique_3d_case_count"] = len(result["cases"])
    if args.write:
        (HERE / "evidence.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    elif json.loads((HERE / "evidence.json").read_text()) != result:
        raise SystemExit("Saved evidence differs from recomputation")
    print(result["decision"], f'{len(result["cases"])} local 3D cases; BOND_CAPACITY_UNKNOWN / G2b_NOT_PASSED')
