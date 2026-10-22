"""CTB-015 focused B1: corrected sources, curved seams, actual route witness.

No source changes, fit/kerf allowance, nesting, full table or B2.
The local joint domain contains ALL possible mutual seam interference.
"""
import argparse
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import cadquery as cq
import ezdxf
from shapely.affinity import translate
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union
from OCP.Geom import Geom_CylindricalSurface
from OCP.gp import gp_Ax3, gp_Pnt, gp_Dir, gp_Pnt2d
from OCP.GCE2d import GCE2d_MakeSegment
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing)
from OCP.BRepLib import BRepLib
from OCP.BRepFill import BRepFill
from OCP.TopoDS import TopoDS
from OCP.ShapeFix import ShapeFix_Solid

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/"projects/CTB-01/parts").is_dir())
PROJECT=ROOT/"projects/CTB-01"
INPUT=PROJECT/"studies/CTB-015-CHATGPT"
C12=PROJECT/"parts/P07/variants/CTB-012_RIM_SKIN_INTERLOCK"
C13=PROJECT/"parts/P07/variants/CTB-013_RIM_SEAM_PUZZLE"
BASE="3ca8e38cc084e82f237b427903249282ebe4d1e2"
OLD_EVIDENCE_SHA="3fc8ac39c9f045b1ebeb342a5c4b8085a47ba11b20af052d9a260cf9f1461058"
EPS=1e-4


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def profile(p):
    root=ET.parse(p).getroot()
    assert root.attrib["width"].endswith("mm") and root.attrib["height"].endswith("mm")
    vb=list(map(float,root.attrib["viewBox"].split()))
    assert float(root.attrib["width"][:-2])==vb[2] and float(root.attrib["height"][:-2])==vb[3]
    loops=[[(float(x),float(y)) for x,y in (v.split(",") for v in e.attrib["points"].split())]
           for e in root.findall(".//{*}polygon")]
    p=Polygon(loops[0],loops[1:])
    assert p.is_valid and p.geom_type=="Polygon" and p.area>0
    assert len({Polygon(h).normalize().wkb for h in loops})==len(loops)
    assert all(LineString([*h,h[0]]).is_simple for h in loops)
    return p,loops


def wrap(poly,phase):
    """Actual cylindrical BRep faces with native straight (s,h) UV edges.

    Non-orthogonal head edges map to helices. Do not replace them with boxes
    or polygonal chords: BuildCurves3d at1e-9mm creates their3D edge curves;
    ruled radial faces connect the two cylinders. Sewing tolerance1e-6mm.
    """
    assert not poly.interiors and poly.geom_type=="Polygon"
    coords=list(poly.exterior.coords);edges=[];faces=[]
    for radius in [171,175]:
        surface=Geom_CylindricalSurface(gp_Ax3(gp_Pnt(0,0,450),gp_Dir(0,0,1)),radius)
        boundary=[];wire=BRepBuilderAPI_MakeWire()
        for (h0,s0),(h1,s1) in zip(coords,coords[1:]):
            a=gp_Pnt2d(math.radians(phase)+(s0-.2)/173,h0)
            b=gp_Pnt2d(math.radians(phase)+(s1-.2)/173,h1)
            curve=GCE2d_MakeSegment(a,b).Value()
            edge=BRepBuilderAPI_MakeEdge(curve,surface).Edge()
            assert BRepLib.BuildCurves3d_s(edge,1e-9)
            boundary.append(edge);wire.Add(edge)
        assert wire.IsDone()
        face=BRepBuilderAPI_MakeFace(surface,wire.Wire(),True).Face()
        if radius==171:face=TopoDS.Face_s(face.Reversed())
        faces.append(face);edges.append(boundary)
    for a,b in zip(*edges):faces.append(BRepFill.Face_s(a,b))
    sewing=BRepBuilderAPI_Sewing(1e-6)
    for face in faces:sewing.Add(face)
    sewing.Perform()
    raw=cq.Solid.makeSolid(cq.Shell(TopoDS.Shell_s(sewing.SewedShape())))
    orient=ShapeFix_Solid(raw.wrapped);orient.Perform()
    solid=cq.Solid(orient.Solid())
    # Topological orientation, not input geometry repair or fit compensation.
    assert solid.isValid() and len(solid.Solids())==1
    assert abs(solid.Volume()-4*poly.area)<1e-5
    return solid


def sector(s0,s1,h0,h1,phase):
    a,b=math.radians(phase)+(s0-.2)/173,math.radians(phase)+(s1-.2)/173
    def xy(r,t):return (r*math.cos(t),r*math.sin(t))
    w=(cq.Workplane("XY",origin=(0,0,450+h0)).moveTo(*xy(171,a)).lineTo(*xy(175,a))
       .threePointArc(xy(175,(a+b)/2),xy(175,b)).lineTo(*xy(171,b))
       .threePointArc(xy(171,(a+b)/2),xy(171,a)).close())
    return w.extrude(h1-h0).val()


def plate(poly,z):
    w=cq.Workplane("XY",origin=(0,0,z)).polyline(list(poly.exterior.coords)[:-1]).close()
    for h in poly.interiors:w=w.polyline(list(h.coords)[:-1]).close()
    s=w.extrude(6).val();assert s.isValid() and len(s.Solids())==1
    return s


def band(poly,lo,hi,phase):
    # Complete source material within skin Z bands; only orthogonal notch edges
    # occur there, so each prism sector is exact, not a sampled shell.
    levels=sorted({lo,hi,*[x for x,_ in poly.exterior.coords if lo<x<hi]});parts=[]
    for h0,h1 in zip(levels,levels[1:]):
        g=poly.intersection(LineString([((h0+h1)/2,-30),((h0+h1)/2,570)]))
        lines=[g] if g.geom_type=="LineString" else [s for s in g.geoms if s.geom_type=="LineString"]
        for line in lines:
            s0,s1=line.bounds[1],line.bounds[3]
            assert poly.buffer(1e-9).covers(box(h0,s0,h1,s1))
            parts.append(sector(s0,s1,h0,h1,phase))
    return cq.Compound.makeCompound(parts)


def intersect(a,b):
    hit=a.intersect(b);return abs(hit.Volume()),hit


def run(out):
    inputs=[*sorted(INPUT.iterdir()),*[C12/f"P07{k}_TABBED_DESIGN_ONLY.svg" for k in ["B","T"]],
            C13/"P07R1_PUZZLE_DESIGN_ONLY.svg",C13/"P07R2_PUZZLE_DESIGN_ONLY.svg",
            PROJECT/"assemblies/bonded-b2/evidence.json"]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in inputs if p.is_file()}
    # Exact archived input, so a fresh branch-only checkout need not fetch the
    # unrelated CTB-014 branch merely to reproduce this bounded study.
    old_evidence=(HERE/"CTB014-evidence-reference.json").read_bytes()
    assert hashlib.sha256(old_evidence).hexdigest()==OLD_EVIDENCE_SHA
    out.update({"task":"CTB-015","stage":"B1_ONLY","priority":"P1","source_commit":BASE,
        "source_sha256":hashes,"CTB014_evidence_git_commit":"2e28d0138f2c2b20260677aa24fba9fd7eba8c91",
        "CTB014_evidence_sha256":hashlib.sha256(old_evidence).hexdigest(),
        "engine":{n:importlib.metadata.version(n) for n in ["cadquery","cadquery-ocp","ezdxf","shapely"]},
        "units":"mm; native rim x=h,y=s; theta=phase+(s−0.2)/173; rho171..175; Z450+h",
        "numerical_tolerances":{"overlap_mm3":EPS,"source_rounding_mm":1e-6,"curve3D_mm":1e-9,"sewing_mm":1e-6},
        "interfaces":["IF-10","IF-11"],"physical_kerf_allowance":"NONE; source zero compensation, no measured fit",
        "cases":[],"source_repairs":0,"checker_repairs":1,"formal_executions":1,
        "development_history":"One successful local wrapped-face construction prototype preceded the formal run; no failed prototype or old global suite.",
        "release":"DESIGN_ONLY / STOP_AFTER_B1 / NO_CUTTING_APPROVAL / G3_NOT_RUN / G4_BLOCKED"})
    profiles=[];audit_fixes=[]
    for i in [1,2]:
        f=INPUT/f"P07R{i}_LENGTH_CORRECTED_DESIGN_ONLY.svg"
        p,loops=profile(f);assert len(loops)==64
        out["cases"].append({"id":f"P07R{i}/SVG","status":"PASS","contours":64})
        d=ezdxf.readfile(f.with_suffix(".dxf"));assert d.units==4
        actual=[]
        for j,e in enumerate(d.modelspace()):
            assert e.dxftype()=="LWPOLYLINE" and e.closed
            assert e.dxf.layer==("CUT_OUTER" if j==0 else "CUT_INNER")
            assert all(v[2]==v[3]==v[4]==0 for v in e.get_points())
            actual.append([(float(v[0]),float(v[1])) for v in e.get_points()])
        assert loops==actual
        audit=d.audit();assert not audit.errors
        notices=[{"code":int(a.code),"message":a.message} for a in audit.fixes]
        audit_fixes.extend(notices)
        out["cases"].append({"id":f"P07R{i}/DXF","status":"PASS","vertices_equal_SVG":True,
                             "audit_errors":0,"audit_fixes_in_memory_only":notices,"source_file_written":False})
        old,_=profile(C13/f"P07R{i}_PUZZLE_DESIGN_ONLY.svg")
        assert [list(h.coords) for h in old.interiors]==[list(h.coords) for h in p.interiors]
        slots=[Polygon(h) for h in p.interiors]
        lands=[min(LineString([(x,c-6),(x,c+6)]).distance(h) for h in slots)
               for c in [45,135,225,315,405,495] for x in [6,44]]
        assert min(lands)==6 and sum(abs(h.bounds[2]-h.bounds[0]-26)<1e-6 for h in slots)==18
        neck=p.intersection(LineString([(0,-1.800001),(50,-1.800001)])).length
        head=p.intersection(LineString([(0,-4),(50,-4)])).length
        tip=p.intersection(LineString([(0,-7.8),(50,-7.8)])).length
        assert abs(neck-12)<1e-5 and head==14 and tip==6
        out["cases"].append({"id":f"P07R{i}/lands_curvature","status":"PASS","neck_one_sided_section_mm":neck,
            "head_mm":head,"tip_mm":tip,"notch_to_kerf_land_mm":min(lands),"kerfs":63,"shortened_kerfs":18,
            "holes_unchanged":True,"fillet":"none, sharp polygon vertices; not curvature/strength-qualified"})
        profiles.append(p)
    print("4 corrected vector imports and2 local geometry cases PASS;2 metadata audit notices",flush=True)
    out["parser_audit_fixes_in_memory"]=audit_fixes
    skins={"P07B":plate(profile(C12/"P07B_TABBED_DESIGN_ONLY.svg")[0],450),
           "P07T":plate(profile(C12/"P07T_TABBED_DESIGN_ONLY.svg")[0],494)}
    for i,(p,phase) in enumerate(zip(profiles,[15,195]),1):
        for name,h0,h1 in [("P07B",0,6),("P07T",44,50)]:
            v,_=intersect(skins[name],band(p,h0,h1,phase))
            out["cases"].append({"id":f"P07R{i}|{name}/final","status":"PASS" if v<EPS else "FAIL","overlap_mm3":v})
    roi=box(0,-10,50,3);period=math.pi*173
    out["final_seams"]=[];out["path_counterexamples"]=[]
    asm=cq.Assembly(name="CTB015_LOCAL_ROUTE_COUNTEREXAMPLES_ONLY")
    for i,phase in enumerate([15,195]):
        male=profiles[i];female=translate(profiles[1-i],yoff=-period)
        assert roi.buffer(1e-9).covers(male.intersection(female))
        a,b=male.intersection(roi),female.intersection(roi)
        sa,sb=wrap(a,phase),wrap(b,phase)
        v,_=intersect(sa,sb)
        analytic=4*male.intersection(female).area
        assert abs(v-analytic)<EPS
        row={"id":f"seam_phase{phase}/final","status":"PASS" if v<EPS else "FAIL","overlap_mm3":v,
             "analytic_rounding_residual_mm3":analytic,"native_joint_domain_h_s_mm":list(roi.bounds),
             "domain_covers_all_possible_seam_overlap":True,"valid_connected_solids":2,
             "solid_volumes_mm3":[sa.Volume(),sb.Volume()]}
        out["final_seams"].append(row);out["cases"].append(row)
        # Actual inherited rim2 lowering route, not a new invented motion.
        # Phase15: R2 is female; phase195: R2 is male.
        fixed,moving=(sa,sb) if i==0 else (sb,sa)
        pose=moving.translate((0,0,2));collision,hit=intersect(fixed,pose)
        planar=4*(a.intersection(translate(b,xoff=2)).area if i==0 else b.intersection(translate(a,xoff=2)).area)
        assert collision>EPS and abs(collision-planar)<1e-4
        q=hit.BoundingBox()
        row={"id":f"seam_phase{phase}/R2_vertical_route","status":"FAIL","overlap_mm3":collision,
             "moving":"P07R2","fixed":"P07R1","interior_route_pose_xyz_mm":[0,0,2],
             "analytic_pose_overlap_mm3":planar,"collision_bbox_xyz_mm":[q.xmin,q.ymin,q.zmin,q.xmax,q.ymax,q.zmax]}
        out["path_counterexamples"].append(row);out["cases"].append(row)
        for name,s in [("fixed_R1_LOCAL",fixed),("moving_R2_Zplus2_LOCAL",pose),("common_VOLUME",hit)]:
            asm.add(s,name=f"PHASE{phase}_{name}")
        print("Seam",phase,"final",v,"route interior collision",collision,flush=True)
    old=profile(C13/"P07R1_PUZZLE_DESIGN_ONLY.svg")[0]
    v,_=intersect(wrap(old.intersection(roi),15),wrap(translate(old,yoff=-period).intersection(roi),15))
    assert abs(v-2.78109132858)<1e-4
    out["cases"].append({"id":"negative/old_shortened_seam","status":"PASS","detected_overlap_mm3":v})
    wall=cq.Workplane("XY",origin=(0,0,494)).circle(175).circle(171).extrude(6).val()
    v,_=intersect(skins["P07T"],wall);assert v>10
    out["cases"].append({"id":"negative/filled_skin_notches","status":"PASS","detected_overlap_mm3":v})
    routes=json.loads((PROJECT/"assemblies/bonded-b2/evidence.json").read_text())["assembly_steps"]
    inherited=next(r for r in routes if r["moving"]=="P07R2")
    assert inherited["start_offset_xyz_mm"]==[0,0,70] and inherited["end_offset_xyz_mm"]==[0,0,0]
    for p,h in hashes.items():assert sha(ROOT/p)==h,p
    assert not subprocess.check_output(["git","diff",BASE,"--","projects/CTB-01/parts","projects/CTB-01/assemblies",
        "projects/CTB-01/specifications","projects/CTB-01/studies/CTB-015-CHATGPT"],cwd=ROOT)
    out["cases"].append({"id":"source_and_route_provenance","status":"PASS","sources_unchanged":True,"inherited_R2_route_mm":[70,0]})
    f=HERE/"route-collisions-DESIGN_ONLY.step";asm.save(str(f))
    f.write_text("\n".join(x.rstrip() for x in f.read_text().splitlines())+"\n")
    finalize(out)


def finalize(out):
    f=HERE/"route-collisions-DESIGN_ONLY.step"
    solids=cq.importers.importStep(str(f)).solids().vals()
    # Each Boolean common has TWO disconnected material lobes. Per seam:
    # fixed1 + moving1 + common2 =4 diagnostic solids,8 across the two seams.
    assert len(solids)==8 and all(s.isValid() for s in solids)
    out["diagnostic_STEP"]={"sha256":sha(f),"valid_reimported_solids":8,
        "composition":"2 fixed +2 moved +4 disconnected common lobes",
        "scope":"two local route counterexamples; not whole shell/production parts"}
    out["decision"]="REVISE / CURRENT_VERTICAL_ROUTE_NO_GO / STOP_AFTER_B1 / LEAD_REVIEW_PENDING"
    out["assembly_path"]={"tested":"existing R1 then R2 lower70mm onto lower skin, top afterwards",
        "status":"BLOCKED_BY_INTERIOR_POSE","whole_shell_sweeps":0,"full_six_DOF_impossibility_claimed":False,
        "reason":"positive-volume collisions along the actual continuous R2 route are sufficient to reject it; no feasible alternate closure path is supplied/proved"}
    out["minimum_recommendation"]="Final interference correction is not warranted by the sub-tolerance rounding residual. Revise/prove the closing motion/sequence before nesting. If vertical lowering must be retained, source head/receiver undercut must change under lead-reviewed CR; do not add guessed kerf/clearance or silently edit profiles. Correct LAYER table handle metadata separately."
    out["not_run"]=["alternate radial/elastic/preclosure6DOF routes","whole table/old global suites/B2","nesting/CTB016","measured kerf, physical bend/fit/glue/strength"]
    out["counts"]={"unique_cases":len(out["cases"]),"pass":sum(c["status"]=="PASS" for c in out["cases"]),
        "fail":sum(c["status"]=="FAIL" for c in out["cases"]),"negative_controls":2,
        "parser_metadata_audit_fixes_in_memory_only":len(out["parser_audit_fixes_in_memory"]),"source_repairs":0,"checker_repairs":1}


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--finish-artifact",action="store_true")
    finish=ap.parse_args().finish_artifact
    out={"decision":"B1_INCOMPLETE"}
    try:
        if finish:
            out=json.loads((HERE/"evidence.json").read_text())
            failure=out.pop("execution_failure")
            assert len(out["cases"])==17
            for p,h in out["source_sha256"].items():assert sha(ROOT/p)==h
            assert sha(HERE/"CTB014-evidence-reference.json")==out["CTB014_evidence_sha256"]
            out["checker_repairs"]=1
            out["execution_history"]=[{"attempt":1,"outcome":"ARTIFACT_COUNT_CHECKER_FALSE_FAILURE",
                "detail":"Expected6 STEP solids but each common splits into2 valid lobes,8 total. All17 geometric/file cases already evaluated.","original_failure":failure},
                {"attempt":2,"outcome":"TARGETED_ARTIFACT_FINALIZATION","scope":"STEP re-import and result accounting only; no Boolean/case-suite replay"}]
            finalize(out)
        else:run(out)
    except Exception as exc:
        import traceback
        out["execution_failure"]={"detail":str(exc),"traceback":traceback.format_exc()};raise
    finally:(HERE/"evidence.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"decision":out["decision"],"counts":out["counts"]},indent=2))
