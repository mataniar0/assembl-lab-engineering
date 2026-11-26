#!/usr/bin/env python3
"""Build a native B-rep review candidate from the R18 solids and R21 scene."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import struct
import subprocess

import FreeCAD as App
import Import
import Part

R18 = "f6d732ecf589eda71853d0c3f54d7ae65bcdbed2"
R21 = "b8bfe123f2a77c628f2730af3a9a1c08ed2e6843"
R18_PATH = "engineering-reviews/ST001/R18A_FIX/evidence"
R21_PATH = "engineering-reviews/ST001/R21_VISUAL/R21_DISPLAY_CONCEPT.glb"
R18_FCSTD_SHA = "2693fd695f0ee91bf0fbc8b17c9fca725b6e93019bc80025feb2f7fc3364b8a9"
R21_GLB_SHA = "f0a7d3815887ef86ba9af7ac6d9337547fe67c7e7352b96109caeb9c4779c5fa"
SCOPE = "DESIGN_ONLY / NO_CUT / NO_OCCUPANT_USE"
VOLUME_EPS = 1e-5
CONTACT_EPS = 1e-6


def git_blob(commit, path):
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"], cwd=Path(__file__).parent
    )


def parse_glb(data):
    magic, version, size, length, tag = struct.unpack_from("<5I", data)
    if (magic, version, size, tag) != (0x46546C67, 2, len(data), 0x4E4F534A):
        raise ValueError("Unexpected GLB header")
    end = 20 + length
    payload_size, binary_tag = struct.unpack_from("<2I", data, end)
    if binary_tag != 0x004E4942 or end + 8 + payload_size != size:
        raise ValueError("Unexpected GLB payload")
    return json.loads(data[20:end]), data[end + 8:]


def validate_scene(old_scene, scene, old_buffer, buffer):
    for key in ("meshes", "accessors", "bufferViews"):
        if old_scene[key] != scene[key]:
            raise ValueError(f"R21 scene modified source {key}")
    if old_buffer != buffer:
        raise ValueError("R21 scene modified source GLB binary buffer")


def validate_transform(node, group=False):
    if any(key in node for key in ("rotation", "scale", "matrix")):
        raise ValueError(f"Unsupported node transform {node['name']}")
    gltf = node.get("translation", [0, 0, 0])
    if group and gltf != [0, 0, 0]:
        raise ValueError(f"Unexpected group translation {node['name']}")
    # glTF stores (X, Z, -Y) in metres. FreeCAD uses (X, Y, Z) in mm.
    return 1000*gltf[0], -1000*gltf[2], 1000*gltf[1]


def make_candidate(source, scene):
    old = {obj.Label: obj for obj in source.Objects if obj.TypeId == "Part::Feature"}
    doc = App.newDocument("ST001_Native_CAD_Review_Candidate")
    doc.Label = f"ST-001 CAD candidate | {SCOPE}"
    nodes = scene["nodes"]
    roots = scene["scenes"][scene.get("scene", 0)]["nodes"]
    members = {}
    features = []
    for node_index in roots:
        node = nodes[node_index]
        compound = "children" in node
        if compound:
            validate_transform(node, group=True)
        children = [nodes[index] for index in node["children"]] if compound else [node]
        shapes = []
        for child in children:
            name = child["name"]
            if name in members or child.get("extras", {}).get("proxy_only"):
                raise ValueError(f"Unexpected active member {name}")
            if child["mesh"] >= len(scene["meshes"]) or scene["meshes"][child["mesh"]]["name"] != name:
                raise ValueError(f"Mesh/member mapping mismatch for {name}")
            delta = validate_transform(child)
            shape = old[name].Shape.copy()
            if any(delta):
                shape.translate(App.Vector(*delta))
            if not shape.isValid() or not shape.isClosed() or shape.Volume <= 0 or len(shape.Solids) != 1:
                raise ValueError(f"Invalid source solid {name}")
            members[name] = {"feature": node["name"], "translation_xyz_mm": list(delta),
                             "shape": shape}
            shapes.append(shape)
        name = node["name"]
        part = doc.addObject("Part::Feature", name)
        part.Label = name
        part.Shape = Part.Compound(shapes) if compound else shapes[0]
        part.addProperty("App::PropertyStringList", "SourceMembers", "Provenance")
        part.SourceMembers = [child["name"] for child in children]
        part.addProperty("App::PropertyString", "SourceRevision", "Provenance")
        part.SourceRevision = R18
        part.addProperty("App::PropertyString", "ReviewScope", "Provenance")
        part.ReviewScope = SCOPE
        features.append(part)
    if len(features) != 72 or len(members) != 80 or sum(len(p.SourceMembers) > 1 for p in features) != 4:
        raise ValueError("Unexpected scene inventory")
    doc.recompute()
    return doc, features, members, sorted(old.keys() - members.keys())


def bounds(shape):
    box = shape.BoundBox
    return box.XMin, box.YMin, box.ZMin, box.XMax, box.YMax, box.ZMax


def candidates(a, b):
    return all(min(a[i + 3], b[i + 3]) >= max(a[i], b[i]) - CONTACT_EPS for i in range(3))


def static_checks(members):
    boxes = {name: bounds(entry["shape"]) for name, entry in members.items()}
    positive = []
    tested = 0
    for a, b in combinations(members, 2):
        if not candidates(boxes[a], boxes[b]):
            continue
        tested += 1
        volume = members[a]["shape"].common(members[b]["shape"]).Volume
        if volume > VOLUME_EPS:
            positive.append({"members": [a, b], "overlap_mm3": volume})
    return {"pairs_total": len(members)*(len(members)-1)//2,
            "pairs_boolean": tested, "tolerance_mm3": VOLUME_EPS,
            "positive_overlaps": positive, "status": "FAIL" if positive else "PASS"}


def interface_checks(members):
    result = []
    for side in range(1, 5):
        for leg in (side, side % 4 + 1):
            walls = [n for n in members if n.startswith((f"A01_LEG{leg}_", f"A02_LEG{leg}_"))]
            upper = [n for n, attrs in members.items() if attrs["feature"] == f"R21_Upper_Visual_Group_{side}"]
            lower = [n for n in members if n.startswith(f"C01_SIDE{side}_")]
            for label, rail in (("upper", upper), ("lower", lower)):
                distances = [(members[r]["shape"].distToShape(members[w]["shape"])[0], r, w)
                             for r in rail for w in walls]
                nearest, rail_witness, wall_witness = min(distances)
                contacts = []
                for gap, r, w in distances:
                    if gap > CONTACT_EPS:
                        continue
                    faces_a = members[r]["shape"].Faces
                    faces_b = members[w]["shape"].Faces
                    area = sum(a.common(b).Area for a in faces_a for b in faces_b
                               if candidates(bounds(a), bounds(b)))
                    contacts.append({"rail": r, "wall": w, "shared_face_area_mm2": area})
                result.append({"candidate_interface_id": f"{label}-{side}-leg-{leg}",
                               "members": rail, "leg": leg, "nominal_min_gap_mm": nearest,
                               "nearest_members": [rail_witness, wall_witness],
                               "touching_pairs": contacts,
                               "status": "NOMINAL_FACE_CONTACT" if any(
                                   c["shared_face_area_mm2"] > CONTACT_EPS for c in contacts
                               ) else ("BOUNDARY_CONTACT_ONLY" if contacts else "GAP"),
                               "mapping_to_R30": "UNVERIFIED"})
    return result


def fingerprint(shape):
    return sorted((round(s.Volume, 3), *(round(v, 5) for v in bounds(s))) for s in shape.Solids)


def verify_exports(assembly_name, step, features, members):
    expected = {part.Label: (fingerprint(part.Shape), list(part.SourceMembers)) for part in features}
    App.closeDocument(features[0].Document.Name)
    doc = App.openDocument(str(assembly_name))
    actual = {part.Label: (fingerprint(part.Shape), list(part.SourceMembers))
              for part in doc.Objects if part.TypeId == "Part::Feature"}
    if actual != expected:
        raise ValueError("FreeCAD reimport changed geometry or source member IDs")
    App.closeDocument(doc.Name)
    imported = Part.read(str(step))
    if fingerprint(imported) != sorted(fingerprint(entry["shape"])[0] for entry in members.values()):
        raise ValueError("STEP reimport changed solid inventory, volumes or bounds")
    if not all(s.isValid() and s.isClosed() for s in imported.Solids):
        raise ValueError("STEP reimport contains invalid or open solids")
    return {"native_features": len(actual), "step_solids": len(imported.Solids)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    native = git_blob(R18, f"{R18_PATH}/R18A_FIX_REVIEW.FCStd")
    new_glb = git_blob(R21, R21_PATH)
    if hashlib.sha256(native).hexdigest() != R18_FCSTD_SHA or hashlib.sha256(new_glb).hexdigest() != R21_GLB_SHA:
        raise ValueError("Pinned source hash mismatch")
    source_path = out / "input_R18.FCStd"
    source_path.write_bytes(native)
    old, old_buffer = parse_glb(git_blob(R18, f"{R18_PATH}/R18A_FIX_ASSEMBLED.glb"))
    scene, buffer = parse_glb(new_glb)
    validate_scene(old, scene, old_buffer, buffer)
    source = App.openDocument(str(source_path))
    doc, features, members, omitted = make_candidate(source, scene)
    assembly_name = out / "ST001_NATIVE_CAD_CANDIDATE_DESIGN_ONLY.FCStd"
    step = out / "ST001_NATIVE_CAD_CANDIDATE_DESIGN_ONLY.step"
    doc.saveAs(str(assembly_name))
    Import.export(features, str(step))
    static = static_checks(members)
    interfaces = interface_checks(members)
    export_qa = verify_exports(assembly_name, step, features, members)
    (out / "QA.json").write_text(json.dumps({
        "scope": SCOPE, "model": "New native CAD candidate for digital review",
        "r30_equivalence": "UNVERIFIED", "freecad_version": ".".join(App.Version()[:3]),
        "occt_version": Part.OCC_VERSION, "source_commits": {"R18": R18, "R21": R21},
        "source_sha256": {"R18_FCStd": R18_FCSTD_SHA, "R21_GLB": R21_GLB_SHA},
        "display_buffer_reuse": "PASS", "exports": export_qa,
        "static_checks": static, "candidate_interfaces": interfaces,
        "omitted_in_R21_scene": omitted,
        "members": {name: {k: v for k, v in entry.items() if k != "shape"}
                    for name, entry in members.items()},
        "motion_and_assembly_sequence": "NOT_RUN", "physical_validation": "NOT_RUN",
    }, indent=2) + "\n")
    print(json.dumps({"exports": export_qa,
                      "static": {**static, "positive_overlaps": len(static["positive_overlaps"])},
                      "interface_gaps": sum(i["status"] == "GAP" for i in interfaces)}, indent=2))


if __name__ == "__main__":
    main()
