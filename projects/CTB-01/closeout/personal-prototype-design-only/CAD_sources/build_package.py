"""CTB-010 stages 3/4 only: source-faithful, uncompensated prototype vectors.

Run with the existing ctb-001 Python environment. No CAD kernel is imported.
--seal only refreshes the SHA inventory and deterministic ZIP after file QA.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import zipfile

import ezdxf
from shapely.geometry import Polygon

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = next(p for p in PACKAGE.parents if (p / "projects/CTB-01/parts").is_dir())
PROJECT = ROOT / "projects/CTB-01"
BASE = "9caa69445d3f9816bdf23a934d8824b86e1ad913"
STATUS = "DESIGN_ONLY / PERSONAL_PROTOTYPE / FIT_STRENGTH_UNVERIFIED"
WIDTH, HEIGHT, MARGIN, GAP = 440., 800., 10., 5.
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ROLES = {
    "P01": (6, 6, "P06/adhesive-study/candidate-v1/P01_BONDED_UNIFIED_V1_DESIGN_ONLY.svg"),
    "P02": (9, 6, "P02/variants/B_THROUGH_ADHESIVE/P02.svg"),
    "P02B": (3, 6, "P02/variants/B_THROUGH_ADHESIVE/P02B.svg"),
    "P03": (1, 6, "P03/variants/A_COMPACT_CLOSED/P03.svg"),
    "P04L": (1, 6, "P04/variants/A/P04L.svg"),
    "P04U": (1, 6, "P04/variants/A/P04U.svg"),
    "P05": (6, 6, "P05/variants/A/P05.svg"),
    "P06": (1, 6, "P06/adhesive-study/candidate-v1/P06C_BONDED_V1_DESIGN_ONLY.svg"),
    "P07B": (1, 6, "P07/variants/A/P07B.svg"),
    "P07T": (1, 6, "P07/variants/A/P07T.svg"),
    "P07R1": (1, 4, "P07/variants/A/P07R1.svg"),
    "P07R2": (1, 4, "P07/variants/A/P07R2.svg"),
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save_json(name, data):
    p = PACKAGE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def read_profile(p):
    root = ET.parse(p).getroot()
    group = root.find(f".//{{{NS}}}g[@id='CUT']")
    if group is None:
        group = root  # Historical native-coordinate polygons; presentation transforms ignored.
    loops = [[[float(q) for q in xy.split(",")] for xy in e.attrib["points"].split()]
             for e in group.findall(f".//{{{NS}}}polygon")]
    poly = Polygon(loops[0], loops[1:])
    assert poly.is_valid and poly.geom_type == "Polygon" and poly.area > 0, p
    return poly


def loops(poly):
    return [list(r.coords)[:-1] for r in [poly.exterior, *poly.interiors]]


def body_role(key):
    if "_P01_" in key:
        return "P01"
    if "_S" in key:
        return "P02B" if key.endswith("_S1") else "P02"
    if key.startswith("P05_"):
        return "P05"
    return "P06" if key == "P06_BONDED" else key


def emit(stem, width, height, items, profiles, sheet=False):
    """Both formats derive from exactly the same unrounded native vertices."""
    doc = ezdxf.new("R2010")
    doc.units = 4
    doc.header["$MEASUREMENT"] = 1
    for layer, color in (("CUT_OUTER", 1), ("CUT_INNER", 3), ("ANNOTATION_NOT_CUT", 7), ("REFERENCE_SHEET_NOT_CUT", 8)):
        doc.layers.new(layer, dxfattribs={"color": color})
    ms = doc.modelspace()
    svg = ET.Element(f"{{{NS}}}svg", {"width": f"{width:.12g}mm", "height": f"{height:.12g}mm",
                                         "viewBox": f"0 0 {width:.12g} {height:.12g}"})
    ET.SubElement(svg, f"{{{NS}}}title").text = STATUS
    ET.SubElement(svg, f"{{{NS}}}metadata").text = "mm; no kerf compensation; Cartesian y-up; only CUT_* groups are cut vectors"
    cart = ET.SubElement(svg, f"{{{NS}}}g", {"id": "CARTESIAN_MM", "transform": f"translate(0 {height:.12g}) scale(1 -1)"})
    groups = {layer: ET.SubElement(cart, f"{{{NS}}}g", {"id": layer, "fill": "none", "stroke": color,
                                                       "stroke-width": "0.1"})
              for layer, color in (("CUT_OUTER", "red"), ("CUT_INNER", "green"), ("REFERENCE_SHEET_NOT_CUT", "gray"))}
    labels = ET.SubElement(svg, f"{{{NS}}}g", {"id": "ANNOTATION_NOT_CUT", "font-size": "2.5", "fill": "black"})
    for row in items:
        master = row["master"]
        for index, ring in enumerate(loops(profiles[master])):
            points = [(x + row["dx_mm"], y + row["dy_mm"]) for x, y in ring]
            layer = "CUT_OUTER" if index == 0 else "CUT_INNER"
            ms.add_lwpolyline(points, close=True, dxfattribs={"layer": layer})
            ET.SubElement(groups[layer], f"{{{NS}}}polygon", {"data-instance": row["body"],
                           "points": " ".join(f"{x:.15g},{y:.15g}" for x, y in points)})
        x, y = row["x_mm"] + 2, row["y_mm"] + 2
        label = row["body"] + " | " + master
        ms.add_text(label, dxfattribs={"layer": "ANNOTATION_NOT_CUT", "height": 2.5, "insert": (x, y)})
        ET.SubElement(labels, f"{{{NS}}}text", {"x": f"{x:.12g}", "y": f"{height-y:.12g}"}).text = label
    if sheet:
        outline = [(0, 0), (width, 0), (width, height), (0, height)]
        ms.add_lwpolyline(outline, close=True, dxfattribs={"layer": "REFERENCE_SHEET_NOT_CUT"})
        ET.SubElement(groups["REFERENCE_SHEET_NOT_CUT"], f"{{{NS}}}polygon",
                      {"points": " ".join(f"{x},{y}" for x, y in outline)})
    ms.add_text(STATUS, dxfattribs={"layer": "ANNOTATION_NOT_CUT", "height": 2.0, "insert": (2, height-4)})
    ET.SubElement(labels, f"{{{NS}}}text", {"x": "2", "y": "4", "font-size": "2"}).text = STATUS
    dxf, svgpath = PACKAGE / (stem + ".dxf"), PACKAGE / (stem + ".svg")
    dxf.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(dxf)
    ET.ElementTree(svg).write(svgpath, encoding="utf-8", xml_declaration=True)


def nesting(instances, profiles):
    sheets = []
    def size(row):
        a,b,c,d = profiles[row["master"]].bounds
        return c-a, d-b
    # Deterministic first-fit bottom-left, conservative bounding envelopes.
    # No rotation, reflection, use of hole waste or optimal packing claim.
    for row in sorted(instances, key=lambda r: (-r["thickness_mm"], -size(r)[0]*size(r)[1], r["body"])):
        w, h = size(row)
        assert w <= WIDTH-2*MARGIN and h <= HEIGHT-2*MARGIN, (row, "single-part sheet fit")
        chosen = None
        for s in sheets:
            if s["thickness_mm"] != row["thickness_mm"]:
                continue
            xs = {MARGIN, *[p["x_mm"]+p["width_mm"]+GAP for p in s["placements"]]}
            ys = {MARGIN, *[p["y_mm"]+p["height_mm"]+GAP for p in s["placements"]]}
            for y,x in sorted((y,x) for y in ys for x in xs):
                if x+w > WIDTH-MARGIN+1e-8 or y+h > HEIGHT-MARGIN+1e-8:
                    continue
                if all(x+w+GAP <= p["x_mm"]+1e-8 or p["x_mm"]+p["width_mm"]+GAP <= x+1e-8 or
                       y+h+GAP <= p["y_mm"]+1e-8 or p["y_mm"]+p["height_mm"]+GAP <= y+1e-8
                       for p in s["placements"]):
                    chosen = (s,x,y)
                    break
            if chosen:
                break
        if chosen is None:
            s = {"id": f"BIRCH{row['thickness_mm']}_S{1+sum(s['thickness_mm']==row['thickness_mm'] for s in sheets):02}",
                 "thickness_mm": row["thickness_mm"], "width_mm": WIDTH, "height_mm": HEIGHT, "placements": []}
            sheets.append(s)
            chosen = (s,MARGIN,MARGIN)
        s,x,y = chosen
        a,b,_,_ = profiles[row["master"]].bounds
        s["placements"].append({**row, "x_mm": x, "y_mm": y, "width_mm": w, "height_mm": h,
                                "dx_mm": x-a, "dy_mm": y-b, "rotation_deg": 0, "reflected": False})
    for s in sheets:
        area = sum(profiles[p["master"]].area for p in s["placements"])
        envelope = sum(p["width_mm"]*p["height_mm"] for p in s["placements"])
        s.update({"net_material_area_mm2": area, "net_material_utilization": area/(WIDTH*HEIGHT),
                  "envelope_utilization": envelope/(WIDTH*HEIGHT)})
    return sheets


def write_csv(name, fields, rows):
    p = PACKAGE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        w.writeheader(); w.writerows(rows)


def build():
    out = {}
    b2 = PROJECT / "assemblies/bonded-b2/evidence.json"
    secondary = PROJECT / "assemblies/bonded-secondary/evidence.json"
    primary = json.loads(b2.read_text())
    independent = json.loads(secondary.read_text())
    assert independent["decision"] == "SECONDARY_KERNEL_GEOMETRY_CONFIRMED / LEAD_REVIEW_PENDING"
    # Verify archived byte provenance only; no old geometric checks are rerun.
    for name, digest in independent["source_sha256"].items():
        assert sha(ROOT/name) == digest, (name, "upstream drift; stop")
    for folder in ["DXF", "SVG", "nesting", "BOM", "assembly", "QA", "manifest", "CAD_sources/authoritative"]:
        (PACKAGE/folder).mkdir(parents=True, exist_ok=True)
    source_hashes = {}
    profiles, roles = {}, {}
    for role, (quantity, thickness, source) in ROLES.items():
        p = PROJECT / "parts" / source
        poly = read_profile(p)
        master = "P07R_MASTER" if role.startswith("P07R") else role
        if master in profiles:
            assert poly.equals_exact(profiles[master], 0), "rim alias contours differ"
        else:
            profiles[master] = poly
        source_hashes[str(p.relative_to(ROOT))] = sha(p)
        shutil.copyfile(p, PACKAGE/f"CAD_sources/authoritative/{role}.svg")
        roles[role] = {"master": master, "quantity": quantity, "thickness_mm": thickness,
                       "source": str(p.relative_to(ROOT)), "source_sha256": sha(p)}
    instances = [{"body": body, "role": body_role(body), "master": roles[body_role(body)]["master"],
                  "thickness_mm": roles[body_role(body)]["thickness_mm"]}
                 for body in primary["body_manifest"]]
    assert len(instances) == sum(r["quantity"] for r in roles.values()) == 32
    assert len(profiles) == 11
    sheets = nesting(instances, profiles)
    masters = {}
    for name, poly in profiles.items():
        a,b,c,d = poly.bounds
        row = {"body": name+"_MASTER_ONLY", "master": name, "x_mm": MARGIN, "y_mm": MARGIN,
               "dx_mm": MARGIN-a, "dy_mm": MARGIN-b}
        emit("DXF/"+name, c-a+2*MARGIN, d-b+2*MARGIN, [row], profiles)
        # emit writes both; separate the final per-master format families.
        (PACKAGE/f"DXF/{name}.svg").replace(PACKAGE/f"SVG/{name}.svg")
        masters[name] = {"native_bounds_mm": list(poly.bounds), "native_area_mm2": poly.area,
                         "cut_holes": len(poly.interiors), "contours": len(poly.interiors)+1,
                         "master_translation_mm": [MARGIN-a,MARGIN-b],
                         "roles": [k for k,v in roles.items() if v["master"]==name],
                         "quantity": sum(r["quantity"] for r in roles.values() if r["master"]==name)}
    for s in sheets:
        emit("nesting/"+s["id"], WIDTH, HEIGHT, s["placements"], profiles, sheet=True)
    save_json("CAD_sources/native-profiles.json", {name: loops(p) for name,p in profiles.items()})
    save_json("manifest/CUT_PARTS_MANIFEST.json", {
        "task": "CTB-010 stages 3/4", "issues": [50,51,52], "baseline_commit": BASE, "status": STATUS,
        "routing": {"priority": "P1", "executor": "Codex export/file QA only", "lead": "ChatGPT",
                    "minimal_action": "1:1 source-derived vectors, conservative sheet plan, file QA and ZIP; no kernel reruns"},
        "units": "mm", "sheet": {"width_mm": WIDTH, "height_mm": HEIGHT, "edge_margin_mm": MARGIN, "inter_part_gap_mm": GAP,
            "orientation": "portrait", "rotation_policy": "0 degrees only; original native sheet axes retained; no reflection",
            "packing": "first-fit bottom-left bounding envelopes, NOT optimized nesting"},
        "materials": {"6": "nominal 6mm birch structural", "4": "nominal 4mm kerf-flex birch rim"},
        "measured_thickness_mm": None, "measured_machine_kerf_mm": None, "kerf_compensation_mm": 0,
        "kerf_compensation_status": "UNCOMPENSATED_EXPERIMENTAL_UNKNOWN_KERF",
        "grain_flex_axis_status": "UNMEASURED; preserve source axes; verify sheet grain/flex before any physical trial",
        "rim_pattern": {"slot_width_nominal_mm": .8, "pitch_nominal_mm": 8, "slots_per_strip": 63,
                        "neutral_radius_hypothesis_mm": 173, "bend_status": "NOT_PHYSICALLY_VALIDATED"},
        "layer_semantics": {"CUT_OUTER": "closed material outer boundaries", "CUT_INNER": "closed apertures including kerf slots",
            "ANNOTATION_NOT_CUT": "display/identification only, NOT engraving or cutting",
            "REFERENCE_SHEET_NOT_CUT": "stock boundary display only, NOT cutting", "engrave": "NONE; no engraving operation prescribed"},
        "source_sha256": source_hashes, "roles": roles, "masters": masters, "instances": instances, "sheets": sheets,
        "wood_body_count": 32, "unique_cut_master_count": 11, "P08_keys": 0,
        "inherited_gates": {"secondary": "CONFIRMED; PR53 merged after ChatGPT lead QA96/100; NOT rerun",
             "G2b": "CAD_EVIDENCE_ACCEPTED_FOR_CONTINUATION; final closeout lead review pending",
             "B1_B2_OCC_executions_this_task": 0, "G3": "NOT_PERFORMED_OWNER_DEFERRED", "G4": "BLOCKED"},
        "affected_interfaces": ["IF-01","IF-02","IF-03","IF-04","IF-05","IF-06","IF-07","IF-08","IF-09","IF-10","IF-11","IF-12","IF-13","IF-14"],
    })
    write_csv("BOM/BOM.csv", ["role","master","quantity","thickness_mm","source","source_sha256"],
              [{"role":k,**v} for k,v in roles.items()])
    write_csv("BOM/instances.csv", ["body","role","master","thickness_mm","sheet","x_mm","y_mm","rotation_deg"],
              [{**p,"sheet":s["id"]} for s in sheets for p in s["placements"]])
    write_csv("nesting/SHEETS.csv", ["id","thickness_mm","width_mm","height_mm","net_material_area_mm2","net_material_utilization","envelope_utilization"], sheets)
    save_json("assembly/sequence.json", [{"step": 0,"body": "P06_BONDED", "action": "pre-position ring at Z242..248; temporary support UNPROVED"},
        *[{"step":i,"body":s["moving"],"start_offset_xyz_mm":s["start_offset_xyz_mm"],"end_offset_xyz_mm":s["end_offset_xyz_mm"]}
          for i,s in enumerate(primary["assembly_steps"],1)]])
    text = ["# Conceptual assembly — DESIGN_ONLY", "", "Coordinates: right-handed XYZ mm, floor Z0; legs L1/L2/L3 at 0/120/240 degrees. Local t positive CCW. Sheet labels are exact body IDs; map each ID through BOM/instances.csv. No parts are rotated in sheet plans.",
            "", "Initial ring pre-position +31 CAD translations are inherited from B2, NOT rerun. Offsets are relative to final assembly position, in global XYZ. This is not a validated physical glue/cure/fixture procedure.", "", "| Step | Body / sheet label | Start offset XYZ mm → final (0,0,0) |", "|---:|---|---|"]
    text.append("| 0 | P06_BONDED | Pre-position Z242..248; temporary support/access UNPROVED |")
    for i,s in enumerate(primary["assembly_steps"],1):
        text.append(f"| {i} | {s['moving']} | {s['start_offset_xyz_mm']} |")
    text += ["", "P01_1 centers t=-10.5 and P01_2 t=+10.5, 6mm thick, gap15mm. S1=reinforced P02B Z35, S2 Z90, S3 Z200, S4 Z390. All P01 use one identical master. Place ring, then Y_FIRST, cheek/spacers per leg, bottom skin BEFORE disks, six radial ribs BEFORE rim, solid top last. P07R1/2 are identical flat profiles but distinct assembly phases15/195 degrees; use verified B2 scene for spatial orientation. No P08 keys.",
             "", "P04U↔P05 ~0.2mm AIR; P04U→top 8mm AIR; ribs↔rim ~1.97287mm AIR. No adhesive bridge, continuous structural load path or strength proven. Rim is ideal pre-bent geometry only; bend length/neutral axis uncalibrated. Glue application/cure/access/fixtures, actual fit/kerf, loads/stability NOT_RUN. G3_NOT_PERFORMED_OWNER_DEFERRED; G4_BLOCKED."]
    (PACKAGE/"assembly/ASSEMBLY_SEQUENCE.md").write_text("\n".join(text)+"\n")
    for src,dest in [(b2,"QA/inherited-B2-evidence.json"),(secondary,"QA/inherited-secondary-evidence.json"),
                     (PROJECT/"assemblies/bonded-b2/assembly-DESIGN_ONLY.glb","assembly/validated-candidate-DESIGN_ONLY.glb"),
                     (PROJECT/"specifications/CTB-000/CTB-000_parameters.json","CAD_sources/frozen-parameters.json"),
                     (PROJECT/"specifications/CTB-000/CTB-000_interfaces.json","CAD_sources/interfaces.json")]:
        shutil.copyfile(src,PACKAGE/dest)
    (PACKAGE/"README.md").write_text(f"""# CTB-010 — experimental personal prototype digital package

**{STATUS}. G3_NOT_PERFORMED_OWNER_DEFERRED / G4_BLOCKED.**
Stage3/4 only, branch codex/ctb-010-final-digital-closeout; baseline {BASE}.
Geometry evidence inherited from merged PR49 and secondary PR53 (lead QA96/100),
not rerun. Separate final file review: QA/INDEPENDENT_QA.md. ChatGPT lead review
and final digital-closeout decision remain pending.
Personal noncommercial one-off; no safe-use/load rating or cutting authorization.

32 wood instances, 12 assembly roles, 11 unique cut masters. P01 master repeated6;
P07R_MASTER repeated2 maps to distinct P07R1/P07R2 assembly bodies. P04L/U remain
different contours. P08 keys0. CAD_sources/authoritative holds byte-identical
native input SVGs; native-profiles.json records exact numeric contour vertices.
SVG/ and DXF/ contain each unique master once; nesting/ contains numbered sheets
and labels matching BOM/instances.csv. Only CUT_OUTER and CUT_INNER are cut data;
ANNOTATION_NOT_CUT and REFERENCE_SHEET_NOT_CUT are display-only. No engraving.

Units mm, 1:1, portrait bed WIDTH440 × HEIGHT800. Nominal material groups6/4mm
are separate. Planning margin10mm and part gap5mm are provisional, unmeasured
allowances, NOT calibrated cutting tolerances. No common-line cutting or use
of aperture waste. Packing uses conservative bounding envelopes; no optimum
sheet-count claim. Rotation0 only, no mirror; source sheet axes preserved.
Grain/flex axis and actual stock thickness UNMEASURED, physical orientation
must be checked separately; this is no approved grain/bending recipe.

Machine kerf UNKNOWN, compensation0 (uncompensated experimental contours).
Rim retains actual63 closed 0.8mm nominal kerf openings per segment, pitch8mm;
173mm neutral-axis hypothesis and developed length are unvalidated physically.
No cut compensation, sanding allowance or stretch correction was invented.
No physical fit/bend, glue/cure/fixture/access, strength/load/stability test ran.

See manifest/CUT_PARTS_MANIFEST.json for all placements, native source digests,
stock metrics, layers and gates; BOM/ for quantities; assembly/ for numbered
ring+31 movement documentation and a byte-identical verified GLB preview;
QA/ for separate-parser DXF/SVG checks and archived geometry evidence.

Reproduce exports (from the repository baseline, no CAD kernel runs):
```sh
XDG_CACHE_HOME=/tmp/ctb-cache /workspace/.venvs/ctb-001/bin/python projects/CTB-01/closeout/personal-prototype-design-only/CAD_sources/build_package.py
XDG_CACHE_HOME=/tmp/ctb-cache /workspace/.venvs/ctb-001/bin/python projects/CTB-01/closeout/personal-prototype-design-only/QA/verify_package.py
```
Seal only after QA PASS using build_package.py --seal. The sibling ZIP includes
CAD_sources, DXF, SVG, nesting, BOM, assembly, QA, manifest and this README;
manifest/SHA256SUMS.json seals every file except itself. The sibling .sha256
file seals the ZIP (no circular self-hash). ZIP entry timestamps are fixed.
No G2b self-approval, no self-merge; stop for ChatGPT lead review.
""")
    print(f"Generated {len(profiles)} masters, {len(instances)} instances, {len(sheets)} stock sheets; no kernels executed.")


def seal():
    evidence = json.loads((PACKAGE/"QA/file-evidence.json").read_text())
    assert evidence["status"] == "PASS", "file QA must pass before ZIP sealing"
    for name,digest in evidence["checked_file_sha256"].items():
        assert sha(PACKAGE/name)==digest, (name,"changed since final-file QA; stop sealing")
    files = [p for p in sorted(PACKAGE.rglob("*")) if p.is_file() and p.name != "SHA256SUMS.json" and "__pycache__" not in p.parts]
    save_json("manifest/SHA256SUMS.json", {str(p.relative_to(PACKAGE)): sha(p) for p in files})
    archive = PACKAGE.parent/"CTB-010-personal-prototype-DESIGN_ONLY.zip"
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted([*files,PACKAGE/"manifest/SHA256SUMS.json"]):
            info = zipfile.ZipInfo(str(p.relative_to(PACKAGE)), date_time=(2026,10,21,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(archive) as z:
        expected={str(p.relative_to(PACKAGE)):p.read_bytes() for p in [*files,PACKAGE/"manifest/SHA256SUMS.json"]}
        assert len(z.namelist())==len(set(z.namelist()))==len(expected)
        assert set(z.namelist())==set(expected) and z.testzip() is None
        for name,data in expected.items():
            assert z.read(name)==data, (name,"ZIP roundtrip mismatch")
    archive.with_suffix(".zip.sha256").write_text(sha(archive)+"  "+archive.name+"\n")
    print("Sealed",len(files)+1,"files;",archive.name,sha(archive))


if __name__ == "__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--seal",action="store_true")
    if parser.parse_args().seal:
        seal()
    else:
        build()
