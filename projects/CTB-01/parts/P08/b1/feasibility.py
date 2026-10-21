"""Issue 33 B1 only: one proposed tongue/wood slide-key, no upstream edits.

The two headed ends obstruct direct t withdrawal after a radial seating slide.
The probe must also test reversal of that seating slide with every real part
present. A key held by the collision test is not an anchored keeper.
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

from shapely.affinity import affine_transform, translate
from shapely.geometry import Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = "98f0132423bb33adc19b14a3188a662d36e50e1a"
EPS = 1e-6
# All dimensions are nominal mm. This is ONE P08-local, NOT_APPROVED CR overlay.
TIP, KEY_Z, THICK, RADIAL_SEAT, ENTRY = 493.8, 486.2, 6, 3, 40
SLOT_RZ = [50, 486, 64, 492.4]


def integrity():
    archive = subprocess.run(
        ["git", "archive", BASE, "projects/CTB-01/specifications/CTB-000", "projects/CTB-01/parts"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    expected, current, sources = {}, {}, {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as saved:
        for item in saved:
            if not item.isfile():
                continue
            expected[item.name] = hashlib.sha256(saved.extractfile(item).read()).hexdigest()
            live = ROOT / item.name
            current[item.name] = hashlib.sha256(live.read_bytes()).hexdigest() if live.is_file() else None
            if "/src/" in item.name or "/specifications/CTB-000/" in item.name:
                sources[item.name] = current[item.name]
    seal = lambda data: hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    return {
        "base_commit": BASE, "protected_files": len(expected),
        "changed_or_missing": [p for p in expected if expected[p] != current[p]],
        "expected_inventory_sha256": seal(expected), "actual_inventory_sha256": seal(current),
        "source_sha256": dict(sorted(sources.items())),
    }


def run():
    provenance = integrity()
    spec = importlib.util.spec_from_file_location("p07_for_p08_b1", HERE.parents[1] / "P07/src/model.py")
    p07 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p07)
    d7, d5, d4, d3, u, b = p07.inputs()
    p02, p03, p04 = p07.p02, p07.p03, p07.p04
    # Reuse exact selected geometry in memory; never regenerate its files.
    selected = p07.assembly("A", d7, d5, d4, d3, u, b)
    original_face = p03.cheek("A_COMPACT_CLOSED", d3, u)[0]
    raised_tip = original_face.difference(box(-1000, 487, 1000, 1000)).union(
        p02.rounded_rect(45, 486, 69, TIP, 1)
    )
    slot = p02.rounded_rect(*SLOT_RZ, .2)
    cheek_face = raised_tip.difference(slot)
    tongue_face = cheek_face.intersection(box(-1000, 450, 1000, 500))
    raw_key = orient(unary_union([
        box(54, -3.2, 60, 3.2),
        box(50.2, -7.2, 63.8, -3.2),
        box(50.2, 3.2, 63.8, 7.2),
    ]), 1)
    outline = p02.master.Outline(.002)
    vertices = p07.np.asarray(list(raw_key.exterior.coords)[:-1])
    p02.master.rounded_polygon(outline, vertices, [.2] * len(vertices))
    profile = orient(Polygon(outline.final()), 1)

    def key_solid(poly, center, side, angle, z=KEY_Z, height=THICK):
        xy = affine_transform(poly, [1, 0, 0, side, 0, center])
        return p03.rotation(p02.plate_solid(xy, z, height), angle)

    def overlap(a, c):
        return round(max(0.0, (a ^ c).volume()), 9)

    def max_hit(solid, fixed):
        hits = [(overlap(solid, other), name) for name, other in fixed.items()]
        vol, name = max(hits, default=(0, None))
        return {"max_overlap_mm3": vol, "witness_part": name if vol > EPS else None}

    parts = dict(selected)
    modified, keys, positions = {}, {}, []
    for leg, angle in enumerate(b["frozen"]["leg_angles_deg"], 1):
        for index, center in enumerate((-10.5, 10.5), 1):
            side = -1 if center < 0 else 1
            cheek_id, key_id = f"L{leg}_P01_{index}", f"P08_K{leg}_{index}"
            modified[cheek_id] = p03.rotation(p02.cheek_solid(cheek_face, center - 3, 6), angle)
            keys[key_id] = key_solid(translate(profile, xoff=RADIAL_SEAT), center, side, angle)
            positions.append((cheek_id, key_id, center, side, angle))
    parts.update(modified)
    parts.update(keys)
    changed = set(modified) | set(keys)
    pairs = [(a, c) for i, a in enumerate(parts) for c in list(parts)[:i] if a in changed or c in changed]
    final_hits = [overlap(parts[a], parts[c]) for a, c in pairs]
    before_top = {k: v for k, v in parts.items() if k != "P07T" and k not in keys}
    install, escape, tongue_trials = [], [], []
    disk = parts["P04U"]
    disk_face = p04.disk("A", "P04U", d4, d3, u, b)
    disk_up1 = p02.plate_solid(disk_face, 480, 7)

    for cheek_id, key_id, center, side, angle in positions:
        aligned = profile
        entry = translate(profile, yoff=ENTRY)
        seated = translate(profile, xoff=RADIAL_SEAT)
        feed_sweep = key_solid(entry, center, side, angle, height=THICK + 520 - KEY_Z)
        through_sweep = key_solid(p02.swept_polygon(aligned, 0, ENTRY), center, side, angle)
        seat_sweep = key_solid(p02.swept_polygon(aligned, RADIAL_SEAT, 0), center, side, angle)
        clear_disk_sweep = key_solid(p02.swept_polygon(entry, 60, 0), center, side, angle)
        install.append({
            "key": key_id,
            "feed_down_from_bottom_Z520_before_top": max_hit(feed_sweep, before_top),
            "slide_local_q40_to0": max_hit(through_sweep, before_top),
            "seat_local_r0_to3": max_hit(seat_sweep, before_top),
            "same_feed_with_top_closed": max_hit(feed_sweep, {"P07T": parts["P07T"]}),
        })
        before_top[key_id] = keys[key_id]
        others = {k: v for k, v in parts.items() if k != key_id}
        # Exact reverse of the two horizontal installation stages. Top stays on.
        escape.append({
            "key": key_id,
            "direct_outward_q1_with_r_seated": max_hit(
                key_solid(p02.swept_polygon(seated, 0, 1), center, side, angle), others
            ),
            "unseat_r3_to0_top_closed": max_hit(seat_sweep, others),
            "withdraw_q0_to40_top_closed": max_hit(through_sweep, others),
            "escaped_endpoint": max_hit(key_solid(entry, center, side, angle), others),
            "clear_disk_radial0_to60_top_closed": max_hit(clear_disk_sweep, others),
            "clear_disk_endpoint": max_hit(key_solid(translate(entry, xoff=60), center, side, angle), others),
        })
        axial = {}
        for sign in (-1, 1):
            swept_rz = p02.swept_polygon(tongue_face, 0, sign)
            swept = p03.rotation(p02.cheek_solid(swept_rz, center - 3, 6), angle)
            axial[str(sign)] = {
                "key_artificially_held_overlap_mm3": overlap(swept, keys[key_id]),
                "missing_key_disk_only_max_overlap_mm3": max(
                    overlap(swept, parts[layer]) for layer in ("P04L", "P04U")
                ),
            }
        tongue_trials.append({"tongue": cheek_id, "local_Z_trial_mm": axial})

    top_sweep = p02.plate_solid(p07.skin("A", "P07T", d7, d4, d3, u, b), 494, 52)
    top_closing = max_hit(top_sweep, before_top)
    disk_trials = {
        "upper_disk_up1_vs_keys": max_hit(disk_up1, keys),
        "upper_disk_up1_vs_other_real_parts": max_hit(
            disk_up1, {k: v for k, v in parts.items() if k != "P04U" and k not in keys}
        ),
        "upper_disk_up1_after_keys_unseated_but_still_over_disk": max_hit(
            disk_up1, {
                **{k: v for k, v in parts.items() if k != "P04U" and k not in keys},
                **{key_id: key_solid(translate(profile, yoff=ENTRY), center, side, angle)
                   for _, key_id, center, side, angle in positions},
            }
        ),
        "upper_disk_up1_after_keys_clear_disk_footprint": max_hit(
            disk_up1, {
                **{k: v for k, v in parts.items() if k != "P04U" and k not in keys},
                **{key_id: key_solid(translate(profile, xoff=60, yoff=ENTRY), center, side, angle)
                   for _, key_id, center, side, angle in positions},
            }
        ),
        "upper_disk_up0p1_vs_non_key_parts": max_hit(
            p02.plate_solid(disk_face, 480, 6.1),
            {k: v for k, v in parts.items() if k != "P04U" and k not in keys},
        ),
        "interpretation": "Held keys obstruct U conditionally. Unseated keys initially still overlie U; a further radial60 clearance path is checked explicitly. Existing P05 contact must not be credited to P08.",
    }
    checks = {
        "upstream_unchanged": not provenance["changed_or_missing"],
        "one_valid_overlay_six_keys_and_31_body_baseline": (
            len(selected) == 31 and len(keys) == 6 and len(parts) == 37
            and cheek_face.is_valid and cheek_face.geom_type == "Polygon"
            and profile.is_valid and profile.geom_type == "Polygon"
            and all(s.volume() > 0 for s in parts.values())
        ),
        "modified_final_interfaces_clear": max(final_hits) < EPS,
        "six_installation_routes_clear_before_top": all(
            route[stage]["max_overlap_mm3"] < EPS for route in install
            for stage in ("feed_down_from_bottom_Z520_before_top", "slide_local_q40_to0", "seat_local_r0_to3")
        ),
        "top_closes_but_blocks_late_feed": top_closing["max_overlap_mm3"] < EPS and all(
            route["same_feed_with_top_closed"]["max_overlap_mm3"] > EPS for route in install
        ),
        "headed_keys_block_direct_pull_but_escape_by_reverse_slide": all(
            route["direct_outward_q1_with_r_seated"]["max_overlap_mm3"] > EPS
            and all(route[s]["max_overlap_mm3"] < EPS for s in (
                "unseat_r3_to0_top_closed", "withdraw_q0_to40_top_closed", "escaped_endpoint",
                "clear_disk_radial0_to60_top_closed", "clear_disk_endpoint"
            )) for route in escape
        ),
        "held_key_axial_restraint_missing_key_negative": all(
            row["key_artificially_held_overlap_mm3"] > EPS
            and row["missing_key_disk_only_max_overlap_mm3"] < EPS
            for trial in tongue_trials for row in trial["local_Z_trial_mm"].values()
        ),
        "disk_axial_contact_measured_separately": disk_trials["upper_disk_up1_vs_keys"]["max_overlap_mm3"] > EPS,
    }
    return {
        "issue": 33, "phase": "B1_ONLY", "decision": "NO_GO",
        "reason": "Own headed shoulders block direct t pull, but reverse radial seating then t withdrawal unlocks every key with the real top closed. A further radial60 motion clears the disk footprint. No key self-retention.",
        "release": "DESIGN_ONLY / CR_REQUIRED / IF-12_B01_OPEN / INDEPENDENT_QA_PENDING",
        "units": "mm; right-handed XYZ; local r,t,z; q is outward from each cheek center",
        "CR": {"id": "CR-CTB008-B1-01", "status": "PROPOSED_NOT_APPROVED",
               "parts": "all six identical P01 upper tongues only; no P04/P05/P07 source edits",
               "old_tip_Z": 488, "proposed_tip_Z": TIP, "tip_radius": 1,
               "slot_rz_bounds": SLOT_RZ, "slot_radius": .2,
               "side_lands_r": [5, 5], "roof_land_Z": round(TIP - SLOT_RZ[3], 6),
               "roof_with_example_tip492": round(492 - SLOT_RZ[3], 6),
               "strength": "NOT_RUN; 1.4mm roof is geometric material only, not qualified strength"},
        "one_key_geometry": {"flat_rq_outer_contour": p02.contour(profile), "extrusion_Z": [KEY_Z, KEY_Z + THICK],
                             "local_radial_seating_shift": RADIAL_SEAT, "entry_q_offset": ENTRY,
                             "final_top_skin_gap": 494 - KEY_Z - THICK, "tip_top_skin_gap": round(494 - TIP, 6),
                             "transforms": [{"tongue": c, "key": k, "t_center": t, "q_sign": s, "angle_deg": a}
                                            for c, k, t, s, a in positions]},
        "unchanged_tongue_screen": {"exposed_height": 2, "key_Z_thickness": 6,
                                    "result": "NO_GO_FOR_THIS_ABOVE_DISK_THROUGH_KEY; not all possible locks"},
        "actual_piece_counts": {"selected_baseline": 31, "replaced_cheeks": 6, "added_keys": 6, "proposed_total": 37},
        "focused_checks": checks, "unique_check_count": len(checks), "epsilon_mm3": EPS,
        "final_changed_pair_count": len(pairs), "final_max_overlap_mm3": round(max(final_hits), 9),
        "insertion": install, "key_escape": escape, "tongue_axial_controls": tongue_trials,
        "actual_upper_disk_movement": disk_trials, "top_closing": top_closing,
        "upstream_integrity": provenance,
        "runtime": {name: importlib.metadata.version(name) for name in ("manifold3d", "shapely", "numpy", "jsonschema")},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    if not all(result["focused_checks"].values()):
        print(json.dumps({"unexpected_checks": result["focused_checks"], "observations": result}, indent=2))
        raise SystemExit("Probe observations require review; no successful lock asserted")
    if args.write:
        (HERE / "evidence.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    elif json.loads((HERE / "evidence.json").read_text()) != result:
        raise SystemExit("Stored evidence does not match recomputation")
    print(f'NO_GO: {sum(result["focused_checks"].values())}/{len(result["focused_checks"])} focused observations verified; key self-retention FAIL. Stop before B2.')
