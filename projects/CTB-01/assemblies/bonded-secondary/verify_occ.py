"""Issue 34: bounded secondary BRep verification, never a manufacturing release.

Reuse the existing independent export reader, NOT any primary component model.
No Manifold3D invocation or complete historical route replay.
"""
import hashlib
import importlib.metadata
import importlib.util
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import traceback

import cadquery as cq
import numpy as np
from shapely.affinity import scale
from shapely.geometry import Polygon

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parents[1]
BASE = "6ef432f16b12145bf8821aa540d6bf0e50264d4d"
EPS = 1e-6  # mm3, same acceptance threshold as the archived primary result
HISTORY = [{"attempt": 1, "outcome": "CHECKER_FALSE_FAILURE",
            "detail": "All 32 BReps reconstructed; isolation assertion rejected a transitive optional Manifold import by the GLB/trimesh stack. No primary component model or primary Boolean operation was called. Replaced module-presence assertion with an active constructor tripwire and explicit import disclosure.",
            "geometry_repairs": 0, "completed_pair_checks": 0}]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(out):
    helper = PROJECT / "parts/P07/tests/independent_occ_review.py"
    spec = importlib.util.spec_from_file_location("existing_export_occ", helper)
    occ = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(occ)
    # trimesh optionally imports manifold3d as an available backend. Merely
    # loading a dependency is not engine execution: actively forbid use here.
    manifold_loaded = "manifold3d" in sys.modules
    if manifold_loaded:
        def forbidden_primary_kernel(*args, **kwargs):
            raise RuntimeError("Primary Manifold constructor called during secondary validation")
        sys.modules["manifold3d"].Manifold = forbidden_primary_kernel
    inputs = {helper}
    original_svg = occ.svg

    def svg(p):
        inputs.add(p)
        return original_svg(p)

    occ.svg = svg
    b2dir = PROJECT / "assemblies/bonded-b2"
    proof = b2dir / "evidence.json"
    primary = json.loads(proof.read_text())
    inputs.add(proof)
    for name, digest in primary["source_sha256"].items():
        p = ROOT / name
        assert sha(p) == digest, (name, "primary source drift")
        inputs.add(p)
    out.update({
        "issue": 34, "phase": "FOCUSED_SECONDARY_CAD_KERNEL", "base_commit": BASE,
        "priority": "P0", "executor": "Codex; ChatGPT engineering-lead review pending",
        "units": "millimetres; GLB metres converted to mm",
        "engine": {k: importlib.metadata.version(k) for k in ("cadquery", "cadquery-ocp", "shapely", "numpy", "trimesh")},
        "method": "OpenCASCADE BRep planar wires/extrusions and Boolean common, reconstructed from actual selected SVG exports; no primary model imports",
        "acceptance": {"overlap_epsilon_mm3": EPS, "manifest_bounds_tolerance_mm": 5e-5,
                       "relative_volume_tolerance": 1e-5},
        "independent_reviewer_status": "INDEPENDENT_QA_PENDING / CHATGPT_LEAD_REVIEW_PENDING",
        "release": "DESIGN_ONLY", "G2b": "LEAD_REVIEW_PENDING_NOT_SELF_APPROVED",
        "physical_gates": "BOND_CAPACITY_NOT_RUN / G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED",
        "not_run": ["Full 31-motion route replay", "782 primary + 222 inherited assertions replay",
                    "Physical kerf/bending, material fit, fixture/cure/access, glue/load/stability",
                    "Production nesting, manufacturing files, new visualizations"],
    })
    print("Reconstructing selected exports with OpenCASCADE", flush=True)
    parts, old_face, _, _ = occ.base27()
    inputs.add(PROJECT / "parts/P03/variants/A_COMPACT_CLOSED/mechanical-dimensions.json")
    candidate = PROJECT / "parts/P06/adhesive-study/candidate-v1"
    face = svg(candidate / "P01_BONDED_UNIFIED_V1_DESIGN_ONLY.svg")
    ring = svg(candidate / "P06C_BONDED_V1_DESIGN_ONLY.svg")
    cheeks = []
    for leg, angle in enumerate((0, 120, 240), 1):
        for index, t_top in enumerate((-7.5, 13.5), 1):
            key = f"L{leg}_P01_{index}"
            parts[key] = occ.spin(occ.cheek(face, t_top), angle)
            cheeks.append(key)
    parts["P06_BONDED"] = occ.plate(ring, 242)
    folder = PROJECT / "parts/P07/variants/A"
    for label, z in (("P07B", 450), ("P07T", 494)):
        parts[label] = occ.plate(svg(folder / (label + ".svg")), z)
    inner = Polygon(svg(folder / "P07T.svg").exterior)
    mask = scale(inner, xfact=175/171, yfact=175/171, origin=(0, 0)).difference(inner)
    out["rim_reconstruction"] = {}
    for i in range(2):
        key = f"P07R{i+1}"
        flat = occ.swap_sheet_axes(svg(folder / (key + ".svg")))
        cells = occ.mapped_cells(flat, 15 + 180*i, mask)
        material = [occ.plate(p, 450 + lo, hi - lo) for lo, hi, p in cells]
        # Fuse the mathematical band partitions: one real connected solid per rim,
        # not dozens of Boolean cells miscounted as individual wooden parts.
        print(key, "fusing", len(material), "material cells", flush=True)
        fused = material[0].fuse(*material[1:]).clean()
        assert fused.isValid() and len(fused.Solids()) == 1, (key, "rim union invalid/disconnected")
        assert abs(fused.Volume() - sum(s.Volume() for s in material)) < EPS
        parts[key] = fused
        out["rim_reconstruction"][key] = {"input_cells": len(material), "fused_connected_solids": 1,
                                          "source_planar_polygon_connected": flat.is_valid and flat.geom_type == "Polygon"}
    out["numeric_intermediates"] = occ.NUMERIC_INTERMEDIATES
    assert set(parts) == set(primary["body_manifest"]) and len(parts) == 32
    out["kernel_isolation"] = {"optional_manifold_module_transitively_loaded": manifold_loaded,
                              "Manifold_constructor_disabled": manifold_loaded,
                              "primary_component_model_imports": False,
                              "Boolean_backend": "cadquery.Shape.intersect -> OpenCASCADE BRepAlgoAPI_Common"}
    out["body_parity"] = {}
    for key, s in parts.items():
        assert s.isValid() and len(s.Solids()) == 1 and s.Volume() > 0, key
        b = occ.bounds(s).reshape(6)
        ref = primary["body_manifest"][key]
        db = float(np.max(np.abs(b - ref["bounds_xyz_mm"])))
        dv = abs(s.Volume()/ref["volume_mm3"] - 1)
        assert db < 5e-5 and dv < 1e-5, (key, "manifest parity", db, dv)
        out["body_parity"][key] = {"valid": True, "connected_solids": 1, "volume_mm3": s.Volume(),
                                   "bounds_xyz_mm": b.tolist(), "primary_bounds_delta_mm": db,
                                   "primary_relative_volume_delta": dv}
    model = b2dir / "assembly-DESIGN_ONLY.glb"
    inputs.add(model)
    out["existing_GLB_secondary_parity"] = occ.glb_audit(model, parts, {"P07R1", "P07R2"})
    print("32 valid connected BReps and existing GLB parity PASS", flush=True)

    # Empty/grazing intersections are evaluated by the existing guarded OCC
    # Boolean common; no meshed primary intersection engine is consulted.
    out["final_pairs_mm3"] = {}
    for (a, sa), (b, sb) in itertools.combinations(parts.items(), 2):
        v = occ.overlap(sa, sb)
        out["final_pairs_mm3"][a + "|" + b] = v
        assert v < EPS, ("FINAL_COLLISION", a, b, v)
    out["six_changed_joints"] = {}
    for key in cheeks:
        d = parts[key].distance(parts["P06_BONDED"])
        assert .198 < d < .201, (key, "unexpected nominal clearance", d)
        out["six_changed_joints"][key] = {"minimum_BRep_distance_mm": d,
                                          "overlap_mm3": occ.overlap(parts[key], parts["P06_BONDED"])}
    print("496 final pairs and six changed joint clearances PASS", flush=True)

    # Narrow selection: six changed cheek motions, initial Y motion versus new
    # ring, and lower skin motion versus seven changed bodies. Other routes NOT_RUN.
    prior = {"P06_BONDED": parts["P06_BONDED"]}
    out["selected_continuous_sweeps"] = []
    for record in primary["assembly_steps"]:
        key = record["moving"]
        swept = None
        obstacles = prior
        if key == "P03":
            assert record["start_offset_xyz_mm"] == [0, 0, 113]
            swept = occ.plate(svg(PROJECT / "parts/P03/variants/A_COMPACT_CLOSED/P03.svg"), 407, 119)
        elif key in cheeks:
            leg = int(key[1]); index = int(key[-1]); angle = (leg-1)*120
            shift = -40 if index == 1 else 40
            expected = [-shift*math.sin(math.radians(angle)), shift*math.cos(math.radians(angle)), 0]
            assert np.max(np.abs(np.array(record["start_offset_xyz_mm"]) - expected)) < 1e-10
            # Tangential translation is parallel to extrusion: exact union is
            # the same holed face extruded 46mm, not sampling of intermediate poses.
            swept = occ.spin(occ.cheek(face, -7.5 if index == 1 else 53.5, 46), angle)
        elif key == "P07B":
            assert record["start_offset_xyz_mm"] == [0, 0, 70]
            swept = occ.plate(svg(folder / "P07B.svg"), 450, 76)
            obstacles = {k: prior[k] for k in [*cheeks, "P06_BONDED"]}
        if swept is not None:
            hits = {k: occ.overlap(swept, s) for k, s in obstacles.items()}
            out["selected_continuous_sweeps"].append({"moving": key, "offset_xyz_mm": record["start_offset_xyz_mm"],
                "swept_volume_mm3": swept.Volume(), "obstacle_intersections_mm3": hits,
                "scope": "all actual predecessors" if obstacles is prior else "seven changed predecessor bodies only"})
            assert max(hits.values(), default=0) < EPS, ("SWEPT_COLLISION", key, hits)
            print("Continuous sweep", key, len(hits), "pairs PASS", flush=True)
        assert key not in prior, ("duplicate sequence body", key)
        prior[key] = parts[key]
    assert set(prior) == set(parts)
    # Two representative positive negatives, not a replay of all 12 old controls.
    out["negative_controls_mm3"] = {
        "L1_P01_1_missing_new_mortise": occ.overlap(occ.cheek(old_face, -7.5), parts["P06_BONDED"]),
        "L1_P01_1_ring_thickness_6p8": occ.overlap(parts["L1_P01_1"], occ.plate(ring, 241.6, 6.8)),
    }
    assert abs(out["negative_controls_mm3"]["L1_P01_1_missing_new_mortise"] - 936) < .01
    assert abs(out["negative_controls_mm3"]["L1_P01_1_ring_thickness_6p8"] - 62.4) < .01
    out["source_sha256"] = {str(p.relative_to(ROOT)): sha(p) for p in sorted(inputs)}
    protected = ["projects/CTB-01/parts", "projects/CTB-01/specifications", "projects/CTB-01/assemblies/bonded-b2"]
    diff = subprocess.check_output(["git", "diff", BASE, "--", *protected], cwd=ROOT, text=True)
    assert not diff, "original CAD/source/primary evidence changed"
    out["original_sources_and_primary_evidence_unchanged"] = True
    out["counts"] = {"body_parity": 32, "final_pairs": len(out["final_pairs_mm3"]),
        "changed_joint_clearances": 6, "selected_movements": len(out["selected_continuous_sweeps"]),
        "swept_pairs": sum(len(s["obstacle_intersections_mm3"]) for s in out["selected_continuous_sweeps"]),
        "negative_controls": len(out["negative_controls_mm3"])}
    out["counts"]["unique_geometric_pair_or_control_cases"] = out["counts"]["final_pairs"] + out["counts"]["swept_pairs"] + out["counts"]["negative_controls"]
    out["decision"] = "SECONDARY_KERNEL_GEOMETRY_CONFIRMED / LEAD_REVIEW_PENDING"


if __name__ == "__main__":
    result = {"decision": "SECONDARY_KERNEL_NOT_CONFIRMED", "execution_history": HISTORY}
    try:
        run(result)
        HISTORY.append({"attempt": 2, "outcome": "PASS", "geometry_repairs": 0})
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "detail": str(exc), "traceback": traceback.format_exc()}
        HISTORY.append({"attempt": 2, "outcome": "FAIL", "detail": str(exc)})
        raise
    finally:
        (HERE / "evidence.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
