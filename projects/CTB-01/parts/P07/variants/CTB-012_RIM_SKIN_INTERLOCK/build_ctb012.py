"""CTB-012 rim/skin positive-location concept — DESIGN_ONLY, no physical approval.

Run from repository checkout: python3 build_ctb012.py --out /tmp/ctb012-vectors
Uses only Python standard library. Source contour polygons are the CTB-010 P07
variant A files; source holes remain unchanged. No kerf compensation is applied.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

PREFIX = Path("projects/CTB-01/parts/P07/variants/A")
CENTERS_MM = (45, 135, 225, 315, 405, 495)
PHASES_DEG = (15, 195)
NEUTRAL_R_MM = 173.0
SKIN_BASE_R_MM = 171.0
SKIN_TAB_R_MM = 174.8
NOTCH_Y_HALF_MM = 6.0
TAB_ARC_HALF_MM = 5.75
RIM_MIN_Y_MM, RIM_MAX_Y_MM = 0.2, 543.295529
SHORTENED_KERF_REGION_HALF_MM = 12.0
NS = "{http://www.w3.org/2000/svg}"

def read_loops(path):
    tree = ET.parse(path)
    loops = []
    for node in tree.iter():
        if node.tag == NS + "polygon":
            loops.append([[float(q) for q in pair.split(",")]
                          for pair in node.attrib["points"].split()])
    if not loops:
        raise ValueError(f"No polygons in {path}")
    return loops

def rounded(x):
    return round(x, 6)

def mod_angle(a):
    return a % (2 * math.pi)

def signed_angle(a):
    return (a + math.pi) % (2 * math.pi) - math.pi

def skin_outline():
    centers = [mod_angle(math.radians(phase) + (y - RIM_MIN_Y_MM) / NEUTRAL_R_MM)
               for phase in PHASES_DEG for y in CENTERS_MM]
    half = TAB_ARC_HALF_MM / NEUTRAL_R_MM
    events = [(math.radians(deg), "base") for deg in range(360)]
    for mid in centers:
        events.extend(((mod_angle(mid - half), "start"), (mod_angle(mid + half), "end")))
    outline = []
    for angle, kind in sorted(events):
        if kind == "start":
            radii = (SKIN_BASE_R_MM, SKIN_TAB_R_MM)
        elif kind == "end":
            radii = (SKIN_TAB_R_MM, SKIN_BASE_R_MM)
        else:
            radii = (SKIN_TAB_R_MM if any(abs(signed_angle(angle - c)) < half for c in centers)
                     else SKIN_BASE_R_MM,)
        outline.extend([[rounded(radius * math.cos(angle)),
                         rounded(radius * math.sin(angle))] for radius in radii])
    assert len(outline) == 408
    return outline

def rim_outline():
    ext = [[0, RIM_MIN_Y_MM], [50, RIM_MIN_Y_MM]]
    for y in CENTERS_MM:
        ext += [[50, y - NOTCH_Y_HALF_MM], [44, y - NOTCH_Y_HALF_MM],
                [44, y + NOTCH_Y_HALF_MM], [50, y + NOTCH_Y_HALF_MM]]
    ext += [[50, RIM_MAX_Y_MM], [0, RIM_MAX_Y_MM]]
    for y in reversed(CENTERS_MM):
        ext += [[0, y + NOTCH_Y_HALF_MM], [6, y + NOTCH_Y_HALF_MM],
                [6, y - NOTCH_Y_HALF_MM], [0, y - NOTCH_Y_HALF_MM]]
    assert len(ext) == 52
    return ext

def rim_loops(source, reinforced):
    assert len(source) == 64, "Expected outer contour and 63 kerf slots"
    slots = []
    for old in source[1:]:
        cy = sum(p[1] for p in old) / len(old)
        shorten = reinforced and any(abs(cy-y) <= SHORTENED_KERF_REGION_HALF_MM
                                     for y in CENTERS_MM)
        slots.append([[12 if x == 8 else 38 if x == 42 else x, y]
                      for x,y in old] if shorten else old)
    return [rim_outline()] + slots

def write_svg(path, loops, title):
    text = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" width="{}mm" height="{}mm" viewBox="{}">'.format(
                380 if title.startswith("P07T") or title.startswith("P07B") else 90,
                380 if title.startswith("P07T") or title.startswith("P07B") else 584,
                "-190 -190 380 380" if title.startswith("P07T") or title.startswith("P07B")
                else "-20 -564 90 584"),
            '<title>{} — CTB-012 DESIGN_ONLY</title>'.format(title),
            '<desc>Conceptual uncalibrated laser vectors; not production approved.</desc>',
            '<g id="CUT" transform="scale(1,-1)" fill="none" stroke="black" stroke-width="0.2">']
    for index, loop in enumerate(loops):
        text.append('<polygon class="{}" points="{}"/>'.format(
            "CUT_INNER" if index else "CUT_OUTER",
            " ".join(f"{rounded(x)},{rounded(y)}" for x,y in loop)))
    text += ["</g>", "</svg>"]
    path.write_text("\n".join(text)+"\n", encoding="utf-8")

def write_dxf(path, loops):
    lines = ["0","SECTION","2","HEADER","9","$ACADVER","1","AC1015",
             "9","$INSUNITS","70","4","0","ENDSEC",
             "0","SECTION","2","TABLES","0","TABLE","2","LAYER","70","2"]
    for name in ("CUT_OUTER", "CUT_INNER"):
        lines += ["0","LAYER","2",name,"70","0","62","7","6","CONTINUOUS"]
    lines += ["0","ENDTAB","0","ENDSEC","0","SECTION","2","ENTITIES"]
    for index, loop in enumerate(loops):
        lines += ["0","LWPOLYLINE","8","CUT_INNER" if index else "CUT_OUTER",
                  "90",str(len(loop)),"70","1"]
        for x,y in loop:
            lines += ["10",str(rounded(x)),"20",str(rounded(y))]
    lines += ["0","ENDSEC","0","EOF"]
    path.write_text("\n".join(lines)+"\n", encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    script_dir = Path(__file__).resolve().parent
    root = Path(args.repo_root).resolve() if args.repo_root else script_dir.parents[4]
    src = root / PREFIX
    dest = Path(args.out).resolve() if args.out else script_dir
    dest.mkdir(parents=True, exist_ok=True)
    report = {"status": "DESIGN_ONLY", "parameters": {"skin_tab_radius_mm": SKIN_TAB_R_MM,
               "rim_notch_width_mm": 12, "kerf_compensation_mm": 0}, "sources": {}, "outputs": []}
    outline = skin_outline()
    for name in ("P07T", "P07B"):
        source_path = src / (name+".svg")
        original = read_loops(source_path)
        assert len(original) == (1 if name == "P07T" else 7)
        modified = [outline]+original[1:]
        report["sources"][name] = hashlib.sha256(source_path.read_bytes()).hexdigest()
        for extension, writer in (("svg", write_svg), ("dxf", write_dxf)):
            path = dest / f"{name}_TABBED_DESIGN_ONLY.{extension}"
            writer(path, modified, name) if extension == "svg" else writer(path, modified)
            report["outputs"].append(path.name)
    for name in ("P07R1", "P07R2"):
        source_path = src / (name+".svg")
        original = read_loops(source_path)
        report["sources"][name] = hashlib.sha256(source_path.read_bytes()).hexdigest()
        for reinforced in (False, True):
            modified = rim_loops(original, reinforced)
            assert len(modified) == 64
            suffix = "REINFORCED" if reinforced else "NOTCHED"
            for extension, writer in (("svg", write_svg), ("dxf", write_dxf)):
                path = dest / f"{name}_{suffix}_DESIGN_ONLY.{extension}"
                writer(path, modified, name) if extension == "svg" else writer(path, modified)
                report["outputs"].append(path.name)
    (dest / "BUILD_REPORT.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print("Generated", len(report["outputs"]), "vector files (DESIGN_ONLY)")

if __name__ == "__main__":
    main()
