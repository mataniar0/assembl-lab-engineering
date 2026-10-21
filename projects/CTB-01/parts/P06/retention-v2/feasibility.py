"""Issue #23 B1: unchanged-C early-keeper feasibility preflight, not a new design.

Only the selected assembly-captive hypothesis is screened. A blocked approach is
sufficient for NO_GO; no replacement cut profiles or full regression are built.
"""
import argparse
import hashlib
import importlib.metadata
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = "532f8889ef8ec318908a7f08dcae2d0e3e792e92"
EPS = 1e-6


def upstream_integrity():
    prefixes = ["projects/CTB-01/specifications/CTB-000", "projects/CTB-01/parts"]
    archive = subprocess.run(
        ["git", "archive", BASE, *prefixes], cwd=ROOT, check=True,
        capture_output=True,
    ).stdout
    expected, actual, source_hashes, changed = {}, {}, {}, []
    with tarfile.open(fileobj=io.BytesIO(archive)) as saved:
        for item in saved:
            if not item.isfile():
                continue
            path = item.name
            expected[path] = hashlib.sha256(saved.extractfile(item).read()).hexdigest()
            live = ROOT / path
            actual[path] = hashlib.sha256(live.read_bytes()).hexdigest() if live.is_file() else None
            if actual[path] != expected[path]:
                changed.append(path)
            if "/src/" in path or "/specifications/CTB-000/" in path:
                source_hashes[path] = actual[path]
    def seal(inventory):
        return hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest()
    return {
        "baseline_commit": BASE,
        "protected_files_checked": len(expected),
        "changed_or_missing": sorted(changed),
        "baseline_inventory_sha256": seal(expected),
        "working_inventory_sha256": seal(actual),
        "source_files_sha256": dict(sorted(source_hashes.items())),
    }


def run():
    provenance = upstream_integrity()
    spec = importlib.util.spec_from_file_location(
        "p06_retention_preflight", HERE.parent / "src/model.py"
    )
    p06 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p06)
    d, d5, d4, d3, u, baseline = p06.inputs()
    p02, p03 = p06.p02, p06.p03
    face, _ = p06.cheek_overlay("C", d, d3, u)
    family = p06.ring_solids("C", d, d3, u)
    prior = p03.assembly("A_COMPACT_CLOSED", d3, u, baseline)
    cheek_ids = []
    for leg, angle in enumerate(d["leg_angles_deg"], 1):
        for index, t0 in enumerate((-13.5, 7.5), 1):
            name = f"L{leg}_P01_{index}"
            cheek_ids.append(name)
            prior[name] = p03.rotation(p02.cheek_solid(face, t0, 6), angle)

    def volume(a, b):
        return round(max(0.0, (a ^ b).volume()), 9)

    static = [volume(a, b) for a in family.values() for b in prior.values()]
    static += [row["intersection_mm3"] for row in p02.collision_matrix(family)]
    all_parts = {**prior, **family}
    probes = []
    joint = p06.sections(d, d3, u)["joint_center_r_mm"]
    key_up = p02.swept_polygon(p06.vertical_key(d), 0, d["key_vertical_stroke_mm"])
    for leg, angle in enumerate(d["leg_angles_deg"], 1):
        for side in (-1, 1):
            index = 1 if side < 0 else 2
            cheek_id = f"L{leg}_P01_{index}"
            key_id = f'P06C_K{leg}_{"N" if side < 0 else "P"}'
            key = family[key_id]
            t0 = side * 10.5 - 3
            distance = side * d["cheek_insertion_t_mm"]
            approach = p03.rotation(
                p02.cheek_solid(face, min(t0, t0 + distance), 6 + abs(distance)), angle
            )
            # A real finite intermediate solid is enough to witness a collision;
            # NO_GO does not rely only on an implementation's swept-volume claim.
            at10 = p03.rotation(p02.cheek_solid(face, t0 + side * 10, 6), angle)
            at4 = p03.rotation(p02.cheek_solid(face, t0 + side * 4, 6), angle)
            at40 = p03.rotation(p02.cheek_solid(face, t0 + distance, 6), angle)
            up = p06.key_transform(p02.cheek_solid(key_up, -3, 6), joint, side, angle)
            other_parts = {k: s for k, s in all_parts.items() if k != key_id}
            probes.append({
                "cheek": cheek_id,
                "key": key_id,
                "leg_angle_deg": angle,
                "local_t_start_offset_mm": distance,
                "start_key_overlap_mm3": volume(at40, key),
                "final_key_overlap_mm3": volume(prior[cheek_id], key),
                "approach_sweep_key_overlap_mm3": volume(approach, key),
                "finite_witness_outward10_key_overlap_mm3": volume(at10, key),
                "upward_key_sweep40_max_overlap_mm3": max(volume(up, s) for s in other_parts.values()),
                "key_at_up40_max_overlap_mm3": max(volume(key.translate([0, 0, 40]), s) for s in other_parts.values()),
                "cheek_outward4_fixed_key_overlap_mm3": volume(at4, key),
                "cheek_outward4_missing_key_other_ring_overlap_mm3": max(
                    volume(at4, s) for k, s in family.items() if k != key_id
                ),
            })

    geometry = {
        "cheek_thickness_mm": baseline["frozen"]["cheek_thickness_mm"],
        "inner_gap_mm": baseline["frozen"]["leg_inner_gap_mm"],
        "spacer_stations_z_mm": [s["z_mm"] for s in p02.stations(u)],
        "ring_z_mm": list(family["P06C"].bounding_box()[2::3]),
        "keeper_z_mm": list(family["P06C_K1_P"].bounding_box()[2::3]),
        "Y_z_mm": list(prior["P03"].bounding_box()[2::3]),
        "family_to_S3_vertical_gap_mm": min(s.bounding_box()[2] for s in family.values()) - prior["L1_S3"].bounding_box()[5],
        "family_to_Y_vertical_gap_mm": prior["P03"].bounding_box()[2] - max(s.bounding_box()[5] for s in family.values()),
        "ring_family_to_base_and_internal_finite_pairs": len(static),
        "maximum_final_interface_overlap_mm3": round(max(static), 9),
    }
    checks = {
        "untouched_upstream_hashes": not provenance["changed_or_missing"],
        "retained_geometry_and_clearance": (
            geometry["cheek_thickness_mm"] == 6 and geometry["inner_gap_mm"] == 15
            and geometry["spacer_stations_z_mm"] == [35, 90, 200, 390]
            and geometry["ring_z_mm"] == [242, 248]
            and geometry["keeper_z_mm"] == [235, 256]
            and geometry["Y_z_mm"] == [407, 413]
            and geometry["family_to_S3_vertical_gap_mm"] == 32
            and geometry["family_to_Y_vertical_gap_mm"] == 151
        ),
        "six_proposed_cheeks_final_interface_clear": len(cheek_ids) == 6 and max(static) < EPS,
        "six_early_keeper_approaches_blocked_with_finite_witness": all(
            x["start_key_overlap_mm3"] < EPS and x["final_key_overlap_mm3"] < EPS
            and x["approach_sweep_key_overlap_mm3"] > EPS
            and x["finite_witness_outward10_key_overlap_mm3"] > EPS for x in probes
        ),
        "six_keepers_remain_free_upward": all(
            x["upward_key_sweep40_max_overlap_mm3"] < EPS
            and x["key_at_up40_max_overlap_mm3"] < EPS for x in probes
        ),
        "six_missing_key_spreading_controls_discriminate": all(
            x["cheek_outward4_fixed_key_overlap_mm3"] > EPS
            and x["cheek_outward4_missing_key_other_ring_overlap_mm3"] < EPS for x in probes
        ),
    }
    return {
        "issue": 23,
        "probe": "retention-v2 / Candidate 1 unchanged-C early-position preflight",
        "release": "DESIGN_ONLY / BLOCKED / CR_REQUIRED",
        "decision": "NO_GO" if all(checks.values()) else "PROBE_ERROR_REVIEW_REQUIRED",
        "scope": "Fixed existing C keepers pre-positioned at their final coordinates; unchanged straight Y_FIRST cheek translations. No redesigned keeper profile was constructed.",
        "design_gates": {
            "early_cheek_insertion": "FAIL",
            "positive_Z_keeper_capture": "FAIL",
            "mutual_key_cheek_retention": "NOT_PROVED",
        },
        "independent_qa": "INDEPENDENT_QA_PENDING / ChatGPT Phase C review requested",
        "epsilon_mm3": EPS,
        "focused_checks": checks,
        "unique_check_count": len(checks),
        "geometry": geometry,
        "six_interface_probes": probes,
        "source_integrity": provenance,
        "runtime_packages": {name: importlib.metadata.version(name) for name in (
            "manifold3d", "shapely", "numpy", "jsonschema"
        )},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write evidence.json; default verifies it")
    args = parser.parse_args()
    result = run()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not all(result["focused_checks"].values()):
        raise SystemExit("Unexpected probe result; inspect focused_checks before publishing")
    if args.write:
        (HERE / "evidence.json").write_text(output)
    else:
        if json.loads((HERE / "evidence.json").read_text()) != result:
            raise SystemExit("Saved evidence differs from recomputation")
    print(f'{result["decision"]}: {sum(result["focused_checks"].values())}/{result["unique_check_count"]} focused evidence checks verified; design gates FAIL, not a retention PASS.')
