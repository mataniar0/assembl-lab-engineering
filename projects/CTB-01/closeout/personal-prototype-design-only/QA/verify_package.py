"""CTB-010 file QA: re-import exported files, without importing the exporter.

SVG is parsed by minidom; DXF by ezdxf. No B1/B2/OCC execution is performed.
This is implementer-run computational file QA, not independent reviewer signoff.
"""
from collections import Counter
import copy
import csv
import hashlib
import importlib.metadata
import itertools
import json
from pathlib import Path
import subprocess
import tempfile
import traceback
from xml.dom import minidom

import ezdxf
from shapely.affinity import translate
from shapely.geometry import LineString, Polygon, box

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = next(p for p in PACKAGE.parents if (p/"projects/CTB-01/parts").is_dir())
PROJECT = ROOT/"projects/CTB-01"
EPS = 1e-7


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polygons_from_source(path):
    dom = minidom.parse(str(path))
    cuts = [g for g in dom.getElementsByTagName("g") if g.getAttribute("id") == "CUT"]
    parent = cuts[0] if cuts else dom
    rings = [[tuple(map(float,token.split(","))) for token in el.getAttribute("points").split()]
             for el in parent.getElementsByTagName("polygon")]
    p = Polygon(rings[0], rings[1:])
    assert p.is_valid and p.geom_type == "Polygon" and p.area > 0, (path,"source topology")
    return p


def topology(contours):
    outers, inners, seen = [], [], set()
    for layer, coords in contours:
        assert len(coords) >= 3 and len(coords) == len(set(coords)), "duplicate/degenerate contour vertices"
        line = LineString([*coords,coords[0]])
        assert line.is_simple, "self-crossing cut loop"
        p = Polygon(coords)
        assert p.is_valid and p.area > 0, "invalid cut contour"
        key = p.normalize().wkb
        assert key not in seen, "duplicate cut contour"
        seen.add(key)
        (outers if layer == "CUT_OUTER" else inners).append(p)
    assert outers, "no cut material"
    holes = [[] for _ in outers]
    for p in inners:
        parents = [i for i,o in enumerate(outers) if o.contains(p)]
        assert len(parents) == 1, "orphan/ambiguous aperture"
        holes[parents[0]].append(list(p.exterior.coords))
    for a,b in itertools.combinations([*outers,*inners],2):
        assert a.boundary.intersection(b.boundary).is_empty, "crossed/common-line cut paths"
    polys = [Polygon(o.exterior,hs) for o,hs in zip(outers,holes)]
    assert all(p.is_valid and p.geom_type=="Polygon" for p in polys), "invalid material topology"
    return polys


def parse_file(path, sheet):
    contours = []
    if path.suffix == ".dxf":
        d = ezdxf.readfile(path)
        assert d.units == 4 and d.header["$MEASUREMENT"] == 1, "DXF must be 1:1 mm"
        assert not d.audit().errors, "DXF audit errors"
        reference = []
        for e in d.modelspace():
            layer = e.dxf.layer
            assert layer in {"CUT_OUTER","CUT_INNER","REFERENCE_SHEET_NOT_CUT","ANNOTATION_NOT_CUT"}, "unknown vector layer"
            if layer.startswith("CUT_"):
                assert e.dxftype()=="LWPOLYLINE" and e.closed, "open/non-polyline cut"
                assert all(v[2]==v[3]==v[4]==0 for v in e.get_points()), "unexpected widths/bulges"
                contours.append((layer,[(float(v[0]),float(v[1])) for v in e.get_points()]))
            elif layer=="REFERENCE_SHEET_NOT_CUT":
                assert e.dxftype()=="LWPOLYLINE" and e.closed
                reference.append(Polygon([(v[0],v[1]) for v in e.get_points()]))
            else:
                assert e.dxftype()=="TEXT", "annotation contains unexpected vector"
        if sheet:
            assert len(reference)==1 and reference[0].equals(box(0,0,440,800)), "wrong sheet outline"
        else:
            assert not reference
    else:
        dom = minidom.parse(str(path))
        svg = dom.documentElement
        assert svg.getAttribute("xmlns")=="http://www.w3.org/2000/svg"
        w,h = svg.getAttribute("width"),svg.getAttribute("height")
        assert w.endswith("mm") and h.endswith("mm"), "SVG must use mm"
        width,height = float(w[:-2]),float(h[:-2])
        assert width>0 and height>0
        assert list(map(float,svg.getAttribute("viewBox").split()))==[0,0,width,height], "SVG physical scale mismatch"
        cart = [g for g in dom.getElementsByTagName("g") if g.getAttribute("id")=="CARTESIAN_MM"]
        assert len(cart)==1
        assert cart[0].getAttribute("transform")==f"translate(0 {height:.12g}) scale(1 -1)", "SVG coordinate transform mismatch"
        for layer in ["CUT_OUTER","CUT_INNER"]:
            gs = [g for g in cart[0].getElementsByTagName("g") if g.getAttribute("id")==layer]
            assert len(gs)==1 and not gs[0].hasAttribute("transform")
            for e in gs[0].childNodes:
                if e.nodeType != e.ELEMENT_NODE:
                    continue
                assert e.tagName=="polygon" and not e.hasAttribute("transform"), "unexpected cut element/transform"
                coords = [tuple(map(float,token.split(","))) for token in e.getAttribute("points").split()]
                # Explicitly evaluate the only allowed display transform and
                # invert screen Y to Cartesian mm used by the DXF reader.
                contours.append((layer,[(x,height-(height-y)) for x,y in coords]))
        if sheet:
            assert width==440 and height==800, "SVG portrait sheet dimensions"
    return topology(contours), len(contours)


def same(actual, expected):
    assert len(actual.interiors)==len(expected.interiors), "aperture count mismatch"
    assert max(abs(a-b) for a,b in zip(actual.bounds,expected.bounds))<EPS, "1:1 bounds mismatch"
    assert actual.hausdorff_distance(expected)<EPS, "source boundary mismatch"
    assert actual.symmetric_difference(expected).area<1e-5, "source material area mismatch"


def match(polys, expected):
    matches = [p for p in polys if max(abs(a-b) for a,b in zip(p.bounds,expected.bounds))<EPS]
    assert len(matches)==1, "missing/duplicate placement"
    same(matches[0],expected)
    return matches[0]


def sheet_rules(polys, row, manifest):
    assert len(polys)==len(row["placements"]), "sheet instance quantity mismatch"
    spec = manifest["sheet"]
    bed = box(spec["edge_margin_mm"],spec["edge_margin_mm"],440-spec["edge_margin_mm"],800-spec["edge_margin_mm"])
    for p in polys:
        assert bed.buffer(EPS).covers(Polygon(p.exterior)), "part outside bed/margin"
    minimum = None
    for a,b in itertools.combinations(polys,2):
        # Outer envelopes keep holes/waste free; do not count material cutouts as room for another part.
        pa,pb = Polygon(a.exterior),Polygon(b.exterior)
        distance = pa.distance(pb)
        assert distance >= spec["inter_part_gap_mm"]-EPS, "part overlap/insufficient gap"
        minimum = distance if minimum is None else min(minimum,distance)
    return minimum


def inventory(m):
    assert m["wood_body_count"]==32 and m["P08_keys"]==0
    roles, instances = m["roles"],m["instances"]
    assert len(instances)==32 and len({x["body"] for x in instances})==32
    assert Counter(x["role"] for x in instances)=={k:v["quantity"] for k,v in roles.items()}
    assert {k:v["quantity"] for k,v in roles.items()}=={
        "P01":6,"P02":9,"P02B":3,"P03":1,"P04L":1,"P04U":1,"P05":6,"P06":1,"P07B":1,"P07T":1,"P07R1":1,"P07R2":1}
    flat = [p for s in m["sheets"] for p in s["placements"]]
    assert Counter(p["body"] for p in flat)==Counter(p["body"] for p in instances), "nesting/BOM quantity mismatch"
    for s in m["sheets"]:
        for p in s["placements"]:
            assert p["thickness_mm"]==s["thickness_mm"]==roles[p["role"]]["thickness_mm"], "stock thickness mixed"
            assert p["rotation_deg"]==0 and p["reflected"] is False, "grain/flex source orientation changed"
            assert p["master"]==roles[p["role"]]["master"]
    assert len(m["masters"])==11 and m["masters"]["P07R_MASTER"]["quantity"]==2
    assert roles["P07R1"]["master"]==roles["P07R2"]["master"]=="P07R_MASTER"


def verify():
    m = json.loads((PACKAGE/"manifest/CUT_PARTS_MANIFEST.json").read_text())
    result = {"status":"FAIL", "new_kernel_executions":0, "independent_reviewer_status":"IMPLEMENTER_FILE_QA_ONLY / SEE_INDEPENDENT_QA.md / CHATGPT_LEAD_REVIEW_PENDING",
              "versions":{n:importlib.metadata.version(n) for n in ["ezdxf","shapely"]},"cases":[],"failures":[]}
    current = "initialization"
    def case(name, function):
        nonlocal current
        current=name
        metric=function()
        result["cases"].append({"id":name,"status":"PASS","metrics":metric})
    def rejects(function):
        try:
            function()
        except AssertionError as exc:
            return {"expected_rejection":str(exc)}
        raise AssertionError("corrupted output falsely passed")
    try:
        source = {}
        for role,meta in m["roles"].items():
            def check_source(role=role,meta=meta):
                original=ROOT/meta["source"]
                copied=PACKAGE/f"CAD_sources/authoritative/{role}.svg"
                assert sha(original)==sha(copied)==meta["source_sha256"]
                p=polygons_from_source(copied)
                native=json.loads((PACKAGE/"CAD_sources/native-profiles.json").read_text())[meta["master"]]
                same(Polygon(native[0],native[1:]),p)
                source[role]=p
                return {"holes":len(p.interiors),"area_mm2":p.area,"bounds_mm":p.bounds}
            case("source/"+role,check_source)
        reimports = {}
        for name,meta in m["masters"].items():
            p=source[meta["roles"][0]]
            expected=translate(p,*meta["master_translation_mm"])
            for suffix,folder in [(".dxf","DXF"),(".svg","SVG")]:
                def check_master(name=name,suffix=suffix,folder=folder,expected=expected):
                    pieces,n=parse_file(PACKAGE/f"{folder}/{name}{suffix}",False)
                    assert len(pieces)==1
                    same(pieces[0],expected)
                    return {"contours":n,"holes":len(pieces[0].interiors)}
                case("master/"+name+suffix,check_master)
        for s in m["sheets"]:
            for suffix in [".dxf",".svg"]:
                def check_sheet(s=s,suffix=suffix):
                    pieces,n=parse_file(PACKAGE/f"nesting/{s['id']}{suffix}",True)
                    minimum=sheet_rules(pieces,s,m)
                    reimports[s["id"]+suffix]=pieces
                    return {"instances":len(pieces),"contours":n,"minimum_outer_gap_mm":minimum}
                case("sheet/"+s["id"]+suffix,check_sheet)
        for s in m["sheets"]:
            for row in s["placements"]:
                def check_instance(row=row,s=s):
                    p=source[row["role"]]
                    expected=translate(p,row["dx_mm"],row["dy_mm"])
                    a=match(reimports[s["id"]+".dxf"],expected)
                    b=match(reimports[s["id"]+".svg"],expected)
                    same(a,b)
                    return {"sheet":s["id"],"role":row["role"],"holes":len(a.interiors)}
                case("instance/"+row["body"],check_instance)
        case("BOM/32_instances_stock_and_aliases",lambda:inventory(m))
        def csv_check():
            rows=list(csv.DictReader((PACKAGE/"BOM/BOM.csv").open()))
            assert {r["role"]:int(r["quantity"]) for r in rows}=={k:r["quantity"] for k,r in m["roles"].items()}
            placed=list(csv.DictReader((PACKAGE/"BOM/instances.csv").open()))
            assert len(placed)==32 and {r["body"] for r in placed}=={r["body"] for r in m["instances"]}
            for row in placed:
                target=next((s,p) for s in m["sheets"] for p in s["placements"] if p["body"]==row["body"])
                s,p=target
                assert row["sheet"]==s["id"] and row["master"]==p["master"] and int(row["thickness_mm"])==p["thickness_mm"]
                assert abs(float(row["x_mm"])-p["x_mm"])<EPS and abs(float(row["y_mm"])-p["y_mm"])<EPS
            return {"roles":len(rows),"placed_instances":len(placed)}
        case("BOM/CSV_mapping",csv_check)
        def inherited():
            for name,repo in [("B2","bonded-b2"),("secondary","bonded-secondary")]:
                assert sha(PACKAGE/f"QA/inherited-{name}-evidence.json")==sha(PROJECT/f"assemblies/{repo}/evidence.json")
            d=json.loads((PACKAGE/"QA/inherited-secondary-evidence.json").read_text())
            assert d["decision"].startswith("SECONDARY_KERNEL_GEOMETRY_CONFIRMED")
            for p,h in d["source_sha256"].items():assert sha(ROOT/p)==h
            return {"status":"INHERITED_ONLY","source_hashes":len(d["source_sha256"]),"kernel_runs":0}
        case("provenance/accepted_evidence",inherited)
        def sequence():
            b2=json.loads((PACKAGE/"QA/inherited-B2-evidence.json").read_text())
            seq=json.loads((PACKAGE/"assembly/sequence.json").read_text())
            assert len(seq)==32 and seq[0]["body"]=="P06_BONDED"
            for i,(a,b) in enumerate(zip(seq[1:],b2["assembly_steps"]),1):
                assert a["step"]==i and a["body"]==b["moving"]
                assert a["start_offset_xyz_mm"]==b["start_offset_xyz_mm"] and a["end_offset_xyz_mm"]==b["end_offset_xyz_mm"]
            assert {s["body"] for s in seq}=={i["body"] for i in m["instances"]}
            text=(PACKAGE/"assembly/ASSEMBLY_SEQUENCE.md").read_text()
            for s in seq:assert f"| {s['step']} | {s['body']} |" in text
            return {"preposition":1,"inherited_movements":31,"rerun":False}
        case("assembly/31_moves_plus_ring",sequence)
        def preview():
            assert sha(PACKAGE/"assembly/validated-candidate-DESIGN_ONLY.glb")==sha(PROJECT/"assemblies/bonded-b2/assembly-DESIGN_ONLY.glb")
        case("assembly/unchanged_verified_preview",preview)
        def frozen():
            p=json.loads((PACKAGE/"CAD_sources/frozen-parameters.json").read_text())
            f=p["frozen"]
            assert [f[k] for k in ["table_outer_diameter_mm","table_height_mm","top_total_thickness_mm","cheek_thickness_mm","leg_inner_gap_mm","stock_sheet_height_mm","stock_sheet_width_mm"]]==[350,500,50,6,15,800,440]
            for name in ["frozen-parameters.json","interfaces.json"]:
                original="CTB-000_parameters.json" if name.startswith("frozen") else "CTB-000_interfaces.json"
                assert sha(PACKAGE/"CAD_sources"/name)==sha(PROJECT/"specifications/CTB-000"/original)
            assert m["measured_thickness_mm"] is None and m["measured_machine_kerf_mm"] is None and m["kerf_compensation_mm"]==0
            assert len(source["P07R1"].interiors)==len(source["P07R2"].interiors)==63
            for poly in [source["P07R1"],source["P07R2"]]:
                for h in poly.interiors:
                    a,b,c,d=h.bounds
                    assert abs(c-a-34)<EPS and abs(d-b-.8)<EPS
            return {"frozen":"UNCHANGED","rim_slots":126,"physical":"NOT_RUN"}
        case("contract/frozen_and_kerf_profiles",frozen)
        def protected():
            diff=subprocess.check_output(["git","diff",m["baseline_commit"],"--","projects/CTB-01/parts","projects/CTB-01/specifications","projects/CTB-01/assemblies"],cwd=ROOT,text=True)
            assert not diff,"original sources changed"
        case("provenance/protected_sources",protected)
        # Actual corrupted files, not only fabricated geometry in memory.
        with tempfile.TemporaryDirectory(prefix="ctb010-file-negatives-") as tmp:
            folder=Path(tmp)
            duplicate=folder/"duplicate.dxf"
            d=ezdxf.readfile(PACKAGE/"DXF/P01.dxf")
            e=next(e for e in d.modelspace() if e.dxf.layer=="CUT_OUTER")
            d.modelspace().add_entity(e.copy());d.saveas(duplicate)
            case("negative/duplicate_cut",lambda:rejects(lambda:parse_file(duplicate,False)))
            missing=folder/"missing-slot.dxf"
            d=ezdxf.readfile(PACKAGE/"DXF/P07R_MASTER.dxf")
            d.modelspace().delete_entity(next(e for e in d.modelspace() if e.dxf.layer=="CUT_INNER"));d.saveas(missing)
            def missing_slot():
                actual,_=parse_file(missing,False)
                same(actual[0],translate(source["P07R1"],*m["masters"]["P07R_MASTER"]["master_translation_mm"]))
            case("negative/missing_kerf_slot",lambda:rejects(missing_slot))
            scale=folder/"wrong-scale.svg"
            text=(PACKAGE/"SVG/P01.svg").read_text().replace('width="247mm"','width="494mm"',1)
            assert text!=(PACKAGE/"SVG/P01.svg").read_text()
            scale.write_text(text)
            case("negative/SVG_scale",lambda:rejects(lambda:parse_file(scale,False)))
            sheet=m["sheets"][0]
            bad=folder/"outside.dxf"
            d=ezdxf.readfile(PACKAGE/f"nesting/{sheet['id']}.dxf")
            for e in d.modelspace():
                if e.dxf.layer.startswith("CUT_"):e.translate(440,0,0)
            d.saveas(bad)
            case("negative/outside_stock",lambda:rejects(lambda:sheet_rules(parse_file(bad,True)[0],sheet,m)))
            wrong=copy.deepcopy(m);wrong["sheets"][0]["placements"].pop()
            case("negative/BOM_quantity",lambda:rejects(lambda:inventory(wrong)))
        result["status"]="PASS"
    except Exception as exc:
        result["failures"].append({"case":current,"type":type(exc).__name__,"detail":str(exc),"traceback":traceback.format_exc()})
    result["counts"]={"unique_cases":len(result["cases"])+len(result["failures"]),"pass":len(result["cases"]),"fail":len(result["failures"]),
                      "negative_controls":sum(c["id"].startswith("negative/") for c in result["cases"])}
    result["checked_file_sha256"]={str(p.relative_to(PACKAGE)):sha(p) for p in sorted(PACKAGE.rglob("*")) if p.is_file() and
        p.suffix in [".dxf",".svg",".csv",".glb",".json"] and p.name not in
        ["file-evidence.json","execution-history.json","SHA256SUMS.json"]}
    history_path=PACKAGE/"QA/execution-history.json"
    history=json.loads(history_path.read_text()) if history_path.exists() else []
    history.append({"attempt":len(history)+1,"status":result["status"],"passed":result["counts"]["pass"],"failures":result["failures"],
                    "new_kernel_runs":0})
    history_path.write_text(json.dumps(history,indent=2)+"\n")
    (PACKAGE/"QA/file-evidence.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    sheets=Counter(s["thickness_mm"] for s in m["sheets"])
    report=f"""# CTB-010 — computational final-file QA

**{result['status']} / DESIGN_ONLY / CHATGPT_LEAD_REVIEW_PENDING**.
This is implementer-run file QA with separate parsers, not independent reviewer signoff.
Priority P1; user requested stage3 onward; B1/B2/OpenCASCADE reruns **0**.

{result['counts']['unique_cases']} unique named cases: {result['counts']['pass']} PASS,
{result['counts']['fail']} FAIL, including {result['counts']['negative_controls']} true corrupt-file controls.
Groups: source12; master DXF/SVG22; sheet DXF/SVG{2*len(m['sheets'])}; placement32;
BOM/provenance/sequence/frozen7; negative5. Repeated executions are not new cases.
Execution attempts and all initial failures/corrections belong in execution-history.json
and the delivery review; {len(history)} verifier attempts currently recorded.

32 wood instances, 12 roles, 11 cut masters. Stock sheets: {dict(sheets)}.
Portrait WIDTH440 × HEIGHT800, provisional edge margin10 and inter-part gap5mm.
Every final DXF/SVG is re-imported (ezdxf / minidom, no exporter import), with
units, closed/simple loops, no duplicates/orphan holes/common-line cuts, native
contour fidelity, 1:1 bounds, stock separation, actual outer-envelope spacing
and BOM/source mapping checked. Negative controls corrupt a real duplicate
cut, omit a rim slot, alter SVG scale, move cuts outside bed and remove a BOM
placement; all must be rejected. Detailed metrics and actual checked-file
digests are in file-evidence.json. Hash/ZIP sealing is a subsequent packaging check.

Inherited evidence: PR49 B2 and PR53 secondary CAD, with accepted source hashes.
One initial B2 checker repair and one secondary isolation-checker repair are
historical and are NOT new failures/runs here. Their recorded 782/222 and 569
pair/control cases are NOT added to the new file-QA count. GLB is byte-identical
to the validated candidate; no model rebuild or new renderer ran.

G2b final decision remains for ChatGPT. Material thickness/grain/flex axis/kerf,
physical fit/bending/glue/cure/fixture/access, load and stability NOT_RUN.
G3_NOT_PERFORMED_OWNER_DEFERRED; G4_BLOCKED. No physical cut/use approval,
no certification claim and no self-merge. Inspect README, manifest, BOM,
ASSEMBLY_SEQUENCE and the downloadable ZIP for the complete bounded handoff.
"""
    (PACKAGE/"QA/QA_REPORT.md").write_text(report)
    print(json.dumps({"status":result["status"],"counts":result["counts"],"failures":result["failures"]},indent=2))
    return result["status"]=="PASS"


if __name__=="__main__":
    raise SystemExit(0 if verify() else 1)
