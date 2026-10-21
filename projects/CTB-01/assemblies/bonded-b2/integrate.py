"""Issue34 B2:32 real wood bodies; changed finite sweeps + pinned P07 inheritance.

No bond polymer, capacity assertion, physical release or alternate design.
"""
import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import subprocess
from xml.etree import ElementTree as ET

import numpy as np
import trimesh
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parents[1]
BASE = "daa8879badb921ca3ca3c6d7c848ada90ffae7e7"
P07_COMMIT = "8f57abc75113ad2f4d37455dfd1905e951cde98a"
EPS = 1e-6


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def profile(path):
    root = ET.parse(path).getroot()
    loops = [p.attrib["points"] for p in root.findall(".//{*}polygon")]
    polygons = [[tuple(map(float, xy.split(","))) for xy in s.split()] for s in loops]
    return Polygon(polygons[0], polygons[1:]), loops, list(map(float, root.attrib["viewBox"].split()))


def run(export):
    spec = importlib.util.spec_from_file_location("p07_bonded_b2", PROJECT / "parts/P07/src/model.py")
    p07 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p07)
    d7, d5, d4, d3, u, b = p07.inputs()
    p02, p03, p04, p05 = p07.p02, p07.p03, p07.p04, p07.p05
    candidates = PROJECT / "parts/P06/adhesive-study/candidate-v1"
    cheek_file = candidates / "P01_BONDED_UNIFIED_V1_DESIGN_ONLY.svg"
    ring_file = candidates / "P06C_BONDED_V1_DESIGN_ONLY.svg"
    cheek_face, cheek_strings, _ = profile(cheek_file)
    ring_face, ring_strings, _ = profile(ring_file)
    source_cheek, source_strings, _ = profile(PROJECT / "parts/P03/variants/A_COMPACT_CLOSED/P01-Y-mortise-study-v1.svg")
    proof_file = PROJECT / "parts/P07/assembly/proofs.json"
    old_route = json.loads(proof_file.read_text())["A"]["routes"]["bottom_disks_ribs_rim_top"]
    pinned_proof = subprocess.run(["git", "show", f"{P07_COMMIT}:{proof_file.relative_to(ROOT)}"], cwd=ROOT, capture_output=True, check=True).stdout
    seal = json.loads((PROJECT / "parts/P07/assembly/independent-final-seal.json").read_text())
    inherited_hashes = {**json.loads((PROJECT / "parts/P07/src/upstream-sha256.json").read_text()), **seal["source_input_sha256"]}
    drift = [p for p, h in inherited_hashes.items() if sha(ROOT / p) != h]
    source_checks = {
        "P07_inherited_sources_hash_match": not drift,
        "P07_proof_matches_original_merged_commit": pinned_proof == proof_file.read_bytes(),
        "P07_primary_route_passes": old_route["status"] == "PASS_CAD_SPECIFIED_PATH" and len(old_route["steps"]) == 12,
        "P01_original_outer_and_five_holes_preserved": (
            [[tuple(map(float, xy.split(","))) for xy in s.split()] for s in cheek_strings[:6]]
            == [[tuple(map(float, xy.split(","))) for xy in s.split()] for s in source_strings]
            and len(cheek_strings) == 7
        ),
        "candidate_profiles_valid_connected": all(p.is_valid and p.geom_type == "Polygon" for p in (cheek_face, ring_face)),
    }
    out = {
        "issue": 34, "phase": "B2_CHANGED_IMPACT_WHOLE_ASSEMBLY", "base_commit": BASE,
        "decision": "G2b_NO_GO", "release": "DESIGN_ONLY / INDEPENDENT_QA_PENDING / SECONDARY_KERNEL_PENDING",
        "physical_gates": "BOND_CAPACITY_NOT_RUN / G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED",
        "source_checks": source_checks, "inherited_source_drift": drift,
        "inheritance": {"proof_sha256": sha(proof_file), "original_P07_commit": P07_COMMIT,
                        "selector": "A.routes.bottom_disks_ribs_rim_top", "pinned_source_files": len(inherited_hashes)},
        "initial_state": "P06 positioned atZ242..248 before any other body. Temporary support/cure/fixture access NOT_PROVED; no invisible fixture solid or bond capacity assumed.",
        "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (
            cheek_file, ring_file, proof_file, PROJECT / "parts/P07/assembly/independent-final-seal.json",
            *[PROJECT / f"parts/P{i:02d}/src/model.py" for i in range(1, 8)],
            *[PROJECT / f"parts/P{i:02d}/src/design.json" for i in range(1, 8)])},
        "assembly_steps": [], "negative_controls": [], "units": "CAD mm, GLB metres; right-handed XYZ",
        "runtime": {n: importlib.metadata.version(n) for n in ("manifold3d", "shapely", "numpy", "trimesh")},
        "execution_history": [{"attempt": 1, "outcome": "SOURCE_CHECKER_FALSE_FAILURE",
                               "detail": "Raw numeric text was compared across original/candidate SVGs; numerical vertices are identical. Corrected comparison, zero source geometry edits. No finite assembly evaluated before this repair."},
                              {"attempt": 2, "outcome": "Full candidate CAD build passed; first archival replay matched."},
                              {"attempt": 3, "outcome": "Per-rib contact measurement refinement; same geometry/cases rebuilt. See current decision/counts."}],
    }
    if not all(source_checks.values()):
        out["stop_reason"] = "SOURCE_OR_INHERITANCE_PRECONDITION"
        return out

    baseline = p07.assembly("A", d7, d5, d4, d3, u, b)
    parts = dict(baseline)
    placements = []
    for leg, angle in enumerate(b["frozen"]["leg_angles_deg"], 1):
        for index, t in enumerate(b["coordinate_frame"]["cheek_center_t_offsets_mm"], 1):
            key = f"L{leg}_P01_{index}"
            parts[key] = p03.rotation(p02.cheek_solid(cheek_face, t - 3, 6), angle)
            placements.append({"id": key, "leg": leg, "angle_deg": angle, "t_center_mm": t, "master_sha256": sha(cheek_file)})
    parts["P06_BONDED"] = p02.plate_solid(ring_face, 242, 6)
    changed = {p["id"] for p in placements} | {"P06_BONDED"}
    out["placements"] = placements
    out["body_manifest"] = {k: {"volume_mm3": round(s.volume(), 6), "bounds_xyz_mm": list(s.bounding_box()),
                                "connected_components": len(s.decompose()),
                                "unchanged_P07_object": k in baseline and s is baseline[k]} for k, s in parts.items()}
    out["BOM"] = {"P01": 6, "P02": 9, "P02B": 3, "P03": 1, "P04": 2, "P05": 6,
                  "P06": 1, "P07_skins": 2, "P07_rim_segments": 2, "P08_keys": 0, "adhesive_solids": 0, "total": len(parts)}
    top_bounds = [parts[k].bounding_box() for k in ("P07B", "P07T", "P07R1", "P07R2")]
    checks = {
        "32_single_connected_positive_volume_bodies": len(baseline) == 31 and len(parts) == 32 and all(v["connected_components"] == 1 and v["volume_mm3"] > 0 for v in out["body_manifest"].values()),
        "25_unchanged_objects_reused": sum(v["unchanged_P07_object"] for v in out["body_manifest"].values()) == 25,
        "height500_floor0": min(s.bounding_box()[2] for s in parts.values()) == 0 and max(s.bounding_box()[5] for s in parts.values()) == 500,
        "tabletop_total50": min(v[2] for v in top_bounds) == 450 and max(v[5] for v in top_bounds) == 500,
        "top_NO_HOLE": len(p07.skin("A", "P07T", d7, d4, d3, u, b).interiors) == 0,
        "unchanged_tongue_tip488": cheek_face.bounds[3] == 488,
        "unchanged_gap15_thickness6_and_four_spacers": b["frozen"]["leg_inner_gap_mm"] == 15 and b["frozen"]["cheek_thickness_mm"] == 6 and len(p02.stations(u)) == 4,
        "tabletop_nominal_diameter350": d7["outer_radius_mm"] * 2 == 350,
    }
    out["invariants"] = checks
    if not all(checks.values()):
        out["stop_reason"] = "BOM_OR_FROZEN_GEOMETRY"
        return out

    def volume(a, c):
        return round(max(0.0, (a ^ c).volume()), 9)

    static_max, static_count = 0, 0
    for i, key in enumerate(parts):
        for other in list(parts)[:i]:
            v = volume(parts[key], parts[other])
            static_count += 1
            static_max = max(static_max, v)
            if v > EPS:
                out["stop_reason"] = {"stage": "FINAL_SOLIDS", "parts": [key, other], "overlap_mm3": v,
                                      "intersection_bbox": list((parts[key] ^ parts[other]).bounding_box())}
                return out
    out["final_static"] = {"fresh_pair_checks": static_count, "max_overlap_mm3": static_max, "epsilon_mm3": EPS}
    prior = {"P06_BONDED": parts["P06_BONDED"]}

    def step(key, swept, offset, inherited=None):
        tested = prior if inherited is None else {k: s for k, s in prior.items() if k in changed}
        hits = {k: volume(swept, s) for k, s in tested.items()}
        inherited_hits = {} if inherited is None else {
            row["fixed"]: row["volume_mm3"] for row in inherited["continuous_intersections"] if row["fixed"] not in changed
        }
        if set(tested) | set(inherited_hits) != set(prior) or set(tested) & set(inherited_hits):
            raise RuntimeError(f"Missing/duplicate assembly predecessor proof for {key}")
        if inherited is not None and (inherited["moving"] != key or inherited["start_offset_xyz_mm"] != offset):
            raise RuntimeError(f"Inherited path differs for {key}")
        worst = max([0, *hits.values(), *inherited_hits.values()])
        out["assembly_steps"].append({"moving": key, "start_offset_xyz_mm": offset, "end_offset_xyz_mm": [0, 0, 0],
                                      "fresh_swept_intersections_mm3": hits, "inherited_P07_intersections_mm3": inherited_hits,
                                      "maximum_overlap_mm3": worst, "swept_volume_mm3": round(swept.volume(), 6),
                                      "method": "EXACT_TRANSLATION_SWEPT_SOLID"})
        if worst > EPS:
            out["stop_reason"] = {"stage": key, "fresh_hits": hits, "inherited_hits": inherited_hits}
            return False
        prior[key] = parts[key]
        return True

    if not step("P03", p02.plate_solid(p03.y_profile("A_COMPACT_CLOSED", d3), 407, 119), [0, 0, 113]):
        return out
    for leg, angle in enumerate(b["frozen"]["leg_angles_deg"], 1):
        for local in ("P01_1", "S1", "S2", "S3", "S4", "P01_2"):
            key = f"L{leg}_{local}"
            if local.startswith("P01"):
                t = (-10.5, 10.5)[int(local[-1]) - 1] - 3
                shift = -40 if local == "P01_1" else 40
                swept = p03.rotation(p02.cheek_solid(cheek_face, min(t, t + shift), 46), angle)
            else:
                station = next(s for s in p02.stations(u) if s["id"] == local)
                xy = translate(p02.spacer("B_THROUGH_ADHESIVE", station["part"], u, b), xoff=station["r_mm"])
                swept = p03.rotation(p02.plate_solid(p02.swept_polygon(xy, 0, 40), station["z_mm"] - 3, 6), angle)
                shift = 40
            radians = math.radians(angle)
            if not step(key, swept, [-shift * math.sin(radians), shift * math.cos(radians), 0]):
                return out
    for old in old_route["steps"]:
        key = old["moving"]
        if key in ("P07B", "P07T"):
            z, start = (450, 520) if key == "P07B" else (494, 540)
            swept = p04.lower_sweep(p07.skin("A", key, d7, d4, d3, u, b), z, start)
        elif key in ("P04L", "P04U"):
            swept = p04.lower_sweep(p04.disk("A", key, d4, d3, u, b), d4["layers_z_mm"][key][0], 520)
        elif key.startswith("P05"):
            swept = p05.sweep_rib("A", d5, dr=100, angle=d5["angles_deg"][int(key[-1]) - 1])
        else:
            swept = p07.bent_solid("A", int(key[-1]) - 1, d7, dz_sweep=70)
        if not step(key, swept, old["start_offset_xyz_mm"], old):
            return out
    if set(prior) != set(parts) or len(out["assembly_steps"]) != 31:
        raise RuntimeError("Incomplete 32-body sequence")

    # Negative controls independently expose both missing mortises and wrong stock
    # in each actual rotated/mirrored joint, without proposing another design.
    thick = p02.plate_solid(ring_face, 241.6, 6.8)
    for p in placements:
        original = p03.rotation(p02.cheek_solid(source_cheek, p["t_center_mm"] - 3, 6), p["angle_deg"])
        for label, v in (("missing_mortise", volume(original, parts["P06_BONDED"])),
                         ("ring_thickness6p8", volume(parts[p["id"]], thick))):
            out["negative_controls"].append({"joint": p["id"], "case": label, "overlap_mm3": v, "verified": v > EPS})
            if v <= EPS:
                out["stop_reason"] = "NEGATIVE_CONTROL_DID_NOT_DISCRIMINATE"
                return out

    slot = Polygon([tuple(map(float, xy.split(","))) for xy in cheek_strings[-1].split()])
    r0 = (slot.bounds[0] + slot.bounds[2]) / 2
    out["six_joint_sections"] = []
    for p in placements:
        local_ring = rotate(ring_face, -p["angle_deg"], origin=(0, 0))
        band = local_ring.intersection(box(slot.bounds[0], p["t_center_mm"] - 3, slot.bounds[2], p["t_center_mm"] + 3))
        section = box(band.bounds[0], 242, band.bounds[2], 248)
        out["six_joint_sections"].append({"joint": p["id"], "minimum_section_envelope_clearance_mm": slot.boundary.distance(section),
                                          "projected_face_mm2": band.area})
    out["affected_lands"] = {
        "mortise_to_outer_min_mm": slot.distance(Polygon([tuple(map(float, xy.split(","))) for xy in cheek_strings[0].split()]).exterior),
        "mortise_to_other_five_min_mm": slot.distance(unary_union([Polygon([tuple(map(float, xy.split(","))) for xy in s.split()]) for s in cheek_strings[1:6]])),
    }
    dl = p04.disk("A", "P04L", d4, d3, u, b)
    du = p04.disk("A", "P04U", d4, d3, u, b)
    rib = p05.rib("A", d5)
    upper_band = rib.intersection(box(0, 480, 200, 486))
    upper_envelope = box(upper_band.bounds[0], -3, upper_band.bounds[2], 3)
    lower_band = rib.intersection(box(0, 456, 200, 462))
    lower_envelope = box(lower_band.bounds[0], -3, lower_band.bounds[2], 3)
    upper_distances = {f"P05_{i+1}": du.distance(rotate(upper_envelope, angle, origin=(0, 0))) for i, angle in enumerate(d5["angles_deg"])}
    lower_distances = {f"P05_{i+1}": dl.distance(rotate(lower_envelope, angle, origin=(0, 0))) for i, angle in enumerate(d5["angles_deg"])}
    wall_at457p5 = unary_union([xy for i in range(2) for (a, c), xy in p07.bent_slabs("A", i, d7) if a <= 7.5 < c])
    rib_footprint457p5 = box(*[p05.section_intervals(rib, 457.5)[0][0], -3, p05.section_intervals(rib, 457.5)[0][1], 3])
    out["geometric_load_path"] = {
        "upper_disk_to_top_direct_gap_mm": 8,
        "P04U_to_P05_whole_band_distance_lower_bound_mm": min(upper_distances.values()),
        "P04U_to_each_P05_whole_band_distance_lower_bounds_mm": upper_distances,
        "P04L_to_each_P05_whole_band_distance_lower_bounds_mm": lower_distances,
        "P04U_slot_side_gap_nominal_mm": .2,
        "P04U_P05_zero_gap_contact": False,
        "P05_to_skins_flat_face_mm2_each": {str(z): sum(c - a for a, c in p05.section_intervals(rib, z)) * 6 for z in (456, 494)},
        "P04L_to_P07B_zero_gap_face_mm2": dl.intersection(p07.skin("A", "P07B", d7, d4, d3, u, b)).area,
        "actual_rib_to_rim_distances_at_Z457p5_mm": [rotate(rib_footprint457p5, a, origin=(0, 0)).distance(wall_at457p5) for a in d5["angles_deg"]],
        "interpretation": "U-to-rib interfaces have AIR requiring qualified bonding; no direct U-to-top bridge. Rib-to-skin and L-to-bottom coincidences are geometry only. No effective bonded area or capacity inferred.",
    }
    out["counts"] = {"final_static_pairs": static_count, "sequence_movements": len(out["assembly_steps"]),
                     "new_continuous_pair_checks": sum(len(s["fresh_swept_intersections_mm3"]) for s in out["assembly_steps"]),
                     "inherited_continuous_pair_checks": sum(len(s["inherited_P07_intersections_mm3"]) for s in out["assembly_steps"]),
                     "unique_negative_cases": len(out["negative_controls"])}
    out["decision"] = "G2b_CAD_CANDIDATE_GO_ONLY"
    if export:
        scene = trimesh.Scene()
        for key, s in parts.items():
            mesh = s.to_mesh()
            tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=False)
            tm.visual.face_colors = [205, 169, 118, 255]
            tm.apply_scale(.001)
            scene.add_geometry(tm, node_name=key, geom_name=key)
        path = HERE / "assembly-DESIGN_ONLY.glb"
        path.write_bytes(scene.export(file_type="glb"))
        loaded = trimesh.load(path, force="scene", process=False)
        out["study_model"] = {"file": path.name, "sha256": sha(path), "units": "metres",
                              "separate_geometry_count": len(loaded.geometry),
                              "all_exported_meshes_watertight": all(s.is_watertight for s in loaded.geometry.values())}
        if len(loaded.geometry) != 32 or not out["study_model"]["all_exported_meshes_watertight"]:
            raise RuntimeError("Study model failed 32-body round-trip")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run(args.write)
    diff = subprocess.run(["git", "diff", BASE, "--", "projects/CTB-01",
                           ":(exclude)projects/CTB-01/assemblies/bonded-b2/**"], cwd=ROOT, capture_output=True, check=True).stdout
    result["protected_project_diff_empty"] = not diff
    if diff:
        raise SystemExit("Protected project source changed")
    if args.write:
        (HERE / "evidence.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        saved = json.loads((HERE / "evidence.json").read_text())
        model = saved.pop("study_model", None)
        if model and sha(HERE / model["file"]) != model["sha256"]:
            raise SystemExit("Archived study model hash changed")
        if saved != result:
            raise SystemExit("Recorded evidence differs from recomputation")
    print(result["decision"])
    print(result.get("counts", result.get("stop_reason", "source precondition failed")))
