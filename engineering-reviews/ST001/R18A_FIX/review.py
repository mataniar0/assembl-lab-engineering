"""Generate R18-A-FIX review evidence. Supports Debian FreeCAD embedded modules."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import zipfile

import FreeCAD as App
import numpy as np

from exports import check_glb, display_offsets, render, render_map, tessellate, write_glb
from model import REVIEW_SCOPE, build, save_document
from qa import (Register, check_fcstd, check_joint_details, check_model, controls,
                interface_register, open_cases, totals)

HERE = Path(__file__).resolve().parent


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, rows):
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False, sort_keys=True)
                             if isinstance(value, (list, dict)) else value
                             for key, value in row.items()})


def audit_baseline(archive, p):
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != p["legacy_glb_archive_sha256"]:
        raise ValueError(f"Unexpected R18-A archive SHA-256: {digest}")
    prefix = "ST001_R18A_DIGITAL_REVIEW/"
    with zipfile.ZipFile(archive) as package:
        results = json.loads(package.read(prefix + "RESULTS.json"))
        ledger = list(csv.DictReader(
            package.read(prefix + "R18A_INTERFACE_SCREEN.csv").decode("utf-8-sig").splitlines()))
    return dict(archive_sha256=digest, represented_components=results["component_count"],
                represented_layers=results["output_layers"], reported_interfaces=ledger)


def run_geometry(layers, p, register):
    groups, bom, pairs = check_model(layers, p, register)
    check_joint_details(layers, p, register)
    interfaces = interface_register(layers, p, register)
    controls(register)
    return groups, bom, pairs, interfaces


def other_interfaces(layers, interfaces, register, p):
    rows = []
    for leg in range(1, 5):
        for u in ("NEG", "POS"):
            for v in ("NEG", "POS"):
                key = f"EDGE:LEG{leg}:{u}:{v}"
                rows.append(dict(id=key, family="FJ-EDGE", members=f"A01_LEG{leg}_{u}",
                                 counterpart=f"A02_LEG{leg}_{v}",
                                 nominal_status=register.rows[key]["status"], design_status="BLOCKED",
                                 limit="Alternating corner ownership with zero nominal edge gap. Physical engagement and build order open."))
        for suffix in ("LOW", "MID", "HIGH"):
            key = f"TAB:LEG{leg}:{suffix}"
            rows.append(dict(id=key, family="FJ-TAB-SLOT", members=f"A03_LEG{leg}_{suffix}",
                             counterpart=f"A01_LEG{leg}_POS_P2",
                             nominal_status=register.rows[key]["status"], design_status="BLOCKED",
                             limit="Single review pocket. Position and assembly access provisional.",
                             **register.rows[key]["evidence"]))
        rows.append(dict(id=f"EB:LEG{leg}", family="EB", members=f"A01/A02 LEG{leg}",
                         counterpart=f"A03/A04 LEG{leg}", nominal_status="PASS", design_status="BLOCKED",
                         limit="Closed perimeter with hollow section, diaphragms and flush lower cap. Bond, cap retention and load behavior open."))
    for side in range(1, 5):
        for end in (1, 2):
            leg = side if end == 1 else 1 + side % 4
            key = f"GUSSET:SIDE{side}:END{end}"
            rows.append(dict(id=key, family="FJ-NODE", members=f"E01_SIDE{side}_END{end}",
                             counterpart=f"LEG{leg}/B01_SIDE{side}_1",
                             nominal_status=register.rows[key]["status"], design_status="BLOCKED",
                             limit="Gusset edge meets leg and upper rail. No fastener or mating feature.",
                             shared_area_evidence=register.rows[key]["evidence"]))
            rows.append(dict(id=f"LOCK:SIDE{side}:END{end}", family="LOCK", members=f"F01_SIDE{side}_END{end}",
                             counterpart=f"upper-{side}-leg-{leg}", nominal_status="BLOCKED",
                             design_status="BLOCKED", limit="Off-body, two-ply proxy. Mating role, geometry, capture and installation open."))
    return interfaces + rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-archive", type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "evidence")
    args = parser.parse_args()
    p = json.loads((HERE / "parameters.json").read_text())
    target = args.output.resolve()
    target.mkdir(parents=True, exist_ok=True)
    baseline = audit_baseline(args.baseline_archive, p) if args.baseline_archive else json.loads(
        (HERE / "evidence" / "BASELINE.json").read_text())
    write_json(target / "BASELINE.json", baseline)

    first = Register()
    run_geometry(build(p, 1), p, first)
    first_rows = list(first.rows.values())
    failed = [row for row in first_rows if row["status"] == "FAIL"]
    write_csv(target / "CYCLE_1_FAILURES.csv", failed)
    print("Cycle 1:", totals(first_rows), flush=True)

    final = Register(first_rows)
    layers = build(p, 2)
    groups, bom, pairs, interfaces = run_geometry(layers, p, final)
    interfaces = other_interfaces(layers, interfaces, final, p)
    open_cases(final)
    core_final = list(final.rows.values())
    reused = sum(row is first.rows.get(row["id"]) for row in core_final)
    fixed = [row["id"] for row in failed if final.rows[row["id"]]["status"] == "PASS"]

    doc_path = target / "R18A_FIX_REVIEW.FCStd"
    save_document(layers, doc_path)
    check_fcstd(layers, doc_path, final)
    meshes = tessellate(layers)
    for exploded in (False, True):
        suffix = "EXPLODED" if exploded else "ASSEMBLED"
        path = target / f"R18A_FIX_{suffix}.glb"
        offsets = display_offsets(layers, meshes, exploded)
        write_glb(path, layers, meshes, offsets, exploded)
        check_glb(path, layers, meshes, offsets, final)
        render(target / f"R18A_FIX_{suffix}.png", layers, meshes, offsets, exploded)
    render_map(target / "INTERFACE_MAP.png")

    rows = list(final.rows.values())
    body = [layer for layer in layers if not layer.proxy]
    body_points = np.concatenate([meshes[layer.id][0] for layer in body])
    write_csv(target / "BOM.csv", bom)
    write_csv(target / "LAYERS.csv",
              [dict(id=l.id, component=l.component, family=l.family, ply=l.index,
                    normal_xyz=l.normal, leg=l.leg or "", geometry_status="PROXY_ONLY" if l.proxy else "REVIEW_GEOMETRY",
                    provisional=l.provisional, volume_mm3=round(l.shape.Volume, 6),
                    z_min_mm=round(l.shape.BoundBox.ZMin, 6), z_max_mm=round(l.shape.BoundBox.ZMax, 6))
               for l in layers])
    write_csv(target / "INTERFACES.csv", interfaces)
    write_csv(target / "QA.csv", rows)
    result = dict(revision=p["revision"], scope=REVIEW_SCOPE, delivery="PARTIAL",
                  tools=dict(freecad=".".join(App.Version()[:3]), numpy=np.__version__),
                  source_parameters_sha256=hashlib.sha256((HERE / "parameters.json").read_bytes()).hexdigest(),
                  represented=dict(components=len(groups), layers=len(layers),
                                   review_solids_components=len({l.component for l in body}),
                                   review_solids_layers=len(body),
                                   proxy_components=len({l.component for l in layers if l.proxy}),
                                   proxy_layers=sum(l.proxy for l in layers)),
                  body_bounds_mm=[body_points.min(0).round(6).tolist(), body_points.max(0).round(6).tolist()],
                  cycle_1=dict(counts=totals(first_rows), failed_by_suite=dict(Counter(
                      row["suite"] for row in failed)), legacy_gap_cases=len(baseline["reported_interfaces"])),
                  cycle_2=dict(carried_forward_cases=reused, failed_cases_resolved=len(fixed),
                               final_overlap_cases_passed=sum(r["suite"] == "overlap" and r["status"] == "PASS"
                                                            for r in rows),
                               final_pairs_considered=len(pairs), aabb_candidates=sum(r["aabb_candidate"] for r in pairs)),
                  unique_cases=len(rows), final_counts=totals(rows),
                  suites={suite: totals(r for r in rows if r["suite"] == suite)
                          for suite in sorted({r["suite"] for r in rows})},
                  remaining=[row for row in rows if row["status"] != "PASS"],
                  independent_qa="INDEPENDENT_QA_PENDING")
    write_json(target / "QA.json", result)
    print("Final:", result["final_counts"], "unique:", result["unique_cases"], flush=True)
    print("Cycle-1 failures resolved:", len(fixed), "unchanged cases reused:", reused, flush=True)
    print("Non-approach failures:", [row["id"] for row in rows
          if row["status"] == "FAIL" and row["suite"] != "approach"])
    return any(row["status"] == "FAIL" and row["suite"] != "approach" for row in rows)


if __name__ == "__main__":
    raise SystemExit(main())
