#!/usr/bin/env python3
"""Verify and render DESIGN_ONLY exports and check isolated insertion sweeps."""
import argparse
import json
from pathlib import Path
import struct

import cadquery as cq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh

from build_reference import (
    LENGTH, T, VOLUME_EPS, WIDTH, build_solids, fit_contact, penetration, read_source,
)


def swept_prism(shape, direction):
    """Union of all positions for a face extrusion moving along its normal."""
    vector = cq.Vector(*direction)
    unit = vector.normalized()
    faces = [face for face in shape.Faces() if face.normalAt().dot(unit) > 0.999999]
    if len(faces) != 1:
        raise ValueError("Expected one leading planar face for insertion")
    face = faces[0]
    leading = face.translate(vector)
    return cq.Solid.extrudeLinear(leading.outerWire(), leading.innerWires(),
                                 -vector-unit.multiply(T))


def isolated_insertions(solids):
    # For each candidate, fix the preceding items and translate the moving plate
    # down its extrusion axis from 15 mm outside. Face extrusion yields the
    # exact translational swept material including all openings.
    trials = [
        ("body", "BODY_END_L", (-15, 0, 0), ["BODY_FLOOR"]),
        ("body", "BODY_END_R", (15, 0, 0), ["BODY_FLOOR", "BODY_END_L"]),
        ("body", "BODY_FRONT", (0, -15, 0), ["BODY_FLOOR", "BODY_END_L", "BODY_END_R"]),
        ("body", "BODY_BACK", (0, 15, 0), ["BODY_FLOOR", "BODY_END_L", "BODY_END_R", "BODY_FRONT"]),
        ("bare_lid_frame", "LID_END_L", (-15, 0, 0), ["LID_FRONT_RAIL", "LID_BACK_RAIL"]),
        ("bare_lid_frame", "LID_END_R", (15, 0, 0),
         ["LID_FRONT_RAIL", "LID_BACK_RAIL", "LID_END_L"]),
    ]
    evidence = []
    for scope, name, offset, fixed in trials:
        sweep = swept_prism(solids[name], offset)
        results = {label: penetration(sweep, solids[label]) for label in fixed}
        evidence.append({"scope": scope, "moving": name, "start_offset_xyz_mm": offset,
                         "fixed_sweep_intersection_mm3": results,
                         "status": "FAIL" if max(results.values()) > VOLUME_EPS else "PASS"})
    return evidence


def glb_nodes(path):
    data = path.read_bytes()
    magic, version, size, length, tag = struct.unpack_from("<5I", data)
    if (magic, version, size, tag) != (0x46546C67, 2, len(data), 0x4E4F534A):
        raise ValueError(f"Invalid GLB container {path}")
    header = json.loads(data[20:20+length])
    nodes = {node["name"] for node in header["nodes"] if "mesh" in node}
    if len(header["meshes"]) != len(nodes):
        raise ValueError(f"Unexpected instance/mesh count in {path}")
    return nodes


def render_glb(source, destination, label):
    scene = trimesh.load_scene(source)
    figure = plt.figure(figsize=(10, 5.2), facecolor="#f5f0e8")
    axis = figure.add_subplot(projection="3d", computed_zorder=True)
    axis.set_facecolor(figure.get_facecolor())
    vertices = []
    for node in scene.graph.nodes_geometry:
        transform, name = scene.graph[node]
        mesh = scene.geometry[name].copy()
        mesh.apply_transform(transform)
        # GLTF Y is up. Restore the engineering XYZ orientation for rendering.
        points = np.asarray(mesh.vertices)[:, [0, 2, 1]] * [1, -1, 1]
        vertices.append(points)
        color = "#aa7149" if node.startswith(("LID_", "INTERNAL_RAIL_SADDLE_")) else "#d1a572"
        triangles = Poly3DCollection(points[mesh.faces], facecolors=color,
                                     shade=True, zsort="average")
        axis.add_collection3d(triangles)
    xyz = np.concatenate(vertices)
    lo = xyz.min(axis=0)
    hi = xyz.max(axis=0)
    axis.auto_scale_xyz(*xyz.T)
    axis.set_box_aspect(hi-lo, zoom=1.16)
    axis.view_init(elev=23, azim=-112)
    axis.set_axis_off()
    figure.text(0.045, 0.91, label, fontsize=20, weight="bold", color="#30271f")
    figure.text(0.045, 0.075, "MEB-037 / DESIGN ONLY / NOMINAL 4 mm REFERENCE",
                fontsize=9, color="#51463c")
    figure.savefig(destination, dpi=130, facecolor=figure.get_facecolor())
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out
    profiles, _ = read_source()
    solids, _ = build_solids(profiles, fit_contact(profiles))
    views = {"CLOSED": "Closed reference", "OPEN_110": "110° pose sample",
             "EXPLODED": "Exploded reference"}
    exports = {}
    for key, label in views.items():
        source = out / f"MEB037_{key}_DESIGN_ONLY.glb"
        names = glb_nodes(source)
        if names != set(solids):
            raise ValueError(f"Export misses BOM items in {source}")
        exports[source.name] = {"BOM_nodes": len(names)}
        render_glb(source, source.with_suffix(".png"), label)
    step = out / "MEB037_CLOSED_DESIGN_ONLY.step"
    imported = cq.importers.importStep(str(step)).solids().vals()
    step_volumes = sorted(abs(solid.Volume()) for solid in imported)
    model_volumes = sorted(abs(solid.Volume()) for solid in solids.values())
    if len(step_volumes) != len(model_volumes) or not all(solid.isValid() for solid in imported):
        raise ValueError("STEP import has missing or invalid solid")
    volume_error = max(abs(a-b) for a, b in zip(step_volumes, model_volumes))
    if volume_error > VOLUME_EPS:
        raise ValueError(f"STEP volume drift {volume_error} mm³")
    exports[step.name] = {"valid_imported_solids": len(imported),
                          "max_sorted_solid_volume_error_mm3": volume_error}
    void = cq.Solid.makeBox(LENGTH-2*T, WIDTH-2*T, 68.8-T, cq.Vector(T, T, T))
    intruders = {name: vol for name, solid in solids.items()
                 if (vol := penetration(void, solid)) > VOLUME_EPS}
    report = {
        "exports": exports,
        "partial_insertions_exact_normal_sweep": isolated_insertions(solids),
        "complete_assembly_sequence": "NOT_RUN",
        "body_test_internal_rectangular_prism_mm": [LENGTH-2*T, WIDTH-2*T, 68.8-T],
        "body_test_prism_positive_intersections_mm3": intruders,
        "scope": "Rigid nominal reference. Insertion excludes the main skin and hinge stack.",
    }
    (out / "MEB037_EXPORT_PATH_QA.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
