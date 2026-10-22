"""CTB-014 B1: source-preserving nominal rim/puzzle collision feasibility.

No design repair, kerf calibration, physical bending, nesting or B2 execution.
Exact circular BRep witnesses suffice to disprove the proposed final state;
they are conservative material SUBSETS, not a claimed whole-shell model.
"""
import hashlib
import importlib.metadata
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

import cadquery as cq
import ezdxf
from ezdxf.lldxf.tagger import ascii_tags_loader
from shapely.affinity import translate
from shapely.geometry import LineString, Polygon, box

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/"projects/CTB-01/parts").is_dir())
PART = ROOT/"projects/CTB-01/parts/P07"
C12 = PART/"variants/CTB-012_RIM_SKIN_INTERLOCK"
C13 = PART/"variants/CTB-013_RIM_SEAM_PUZZLE"
HEAD = "72595e4cd7164efa44b4ebda8bf48bf7b2c51c11"
R, START, EPS = 173., .2, 1e-4


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def svg(path):
    r = ET.parse(path).getroot()
    assert r.attrib["width"].endswith("mm") and r.attrib["height"].endswith("mm")
    vb = list(map(float,r.attrib["viewBox"].split()))
    assert abs(float(r.attrib["width"][:-2])-vb[2])<1e-7
    assert abs(float(r.attrib["height"][:-2])-vb[3])<1e-7
    group = r.find(".//{*}g[@id='CUT']")
    assert group is not None and group.attrib["transform"]=="scale(1,-1)"
    rings = [[tuple(map(float,p.split(","))) for p in e.attrib["points"].split()]
             for e in group.findall(".//{*}polygon")]
    poly = Polygon(rings[0],rings[1:])
    assert poly.is_valid and poly.area>0 and poly.geom_type=="Polygon"
    assert all(LineString([*a,a[0]]).is_simple for a in rings)
    return poly,rings


def raw_dxf_geometry(path):
    """Read original tags without repairing an invalid DXF document.

    This is coordinate inspection only. A standard DXF importer failure remains
    a FAIL, even when its raw tags agree with the valid SVG geometry.
    """
    tags=list(ascii_tags_loader(io.StringIO(path.read_text())))
    unit=next(int(tags[i+1].value) for i,t in enumerate(tags) if t.code==9 and t.value=="$INSUNITS")
    assert unit==4
    entities=[]
    for i,t in enumerate(tags):
        if t.code==0 and t.value=="LWPOLYLINE":
            end=next(j for j in range(i+1,len(tags)) if tags[j].code==0)
            values=tags[i+1:end]
            assert next(v.value for v in values if v.code==8) in ["CUT_OUTER","CUT_INNER"]
            assert int(next(v.value for v in values if v.code==70))&1
            points=[(float(v.value),float(values[j+1].value)) for j,v in enumerate(values) if v.code==10]
            assert len(points)==int(next(v.value for v in values if v.code==90))
            entities.append(points)
    return entities


def plate(poly,z):
    w = cq.Workplane("XY",origin=(0,0,z)).polyline(list(poly.exterior.coords)[:-1]).close()
    for h in poly.interiors:
        w=w.polyline(list(h.coords)[:-1]).close()
    s=w.extrude(6).val()
    assert s.isValid() and len(s.Solids())==1
    return s


def sector(s0,s1,h0,h1,phase,r0=171.,r1=175.):
    """Exact circular annular-sector prism: source x=h,y=s, Z=450+h."""
    a,b = math.radians(phase)+(s0-START)/R, math.radians(phase)+(s1-START)/R
    assert 0<b-a<math.pi and h1>h0
    def xy(r,t):return (r*math.cos(t),r*math.sin(t))
    w=(cq.Workplane("XY",origin=(0,0,450+h0)).moveTo(*xy(r0,a)).lineTo(*xy(r1,a))
       .threePointArc(xy(r1,(a+b)/2),xy(r1,b)).lineTo(*xy(r0,b))
       .threePointArc(xy(r0,(a+b)/2),xy(r0,a)).close())
    s=w.extrude(h1-h0).val()
    assert s.isValid() and len(s.Solids())==1
    return s


def lines(g):
    if g.geom_type=="LineString":return [g]
    return [x for x in g.geoms if x.geom_type=="LineString"]


def slab_material(poly,h0,h1,phase):
    """Exact complete rim material in a skin's Z band; head/kerfs outside it.

    Source outer edges within these bands are orthogonal. Vertex levels divide
    h into exact constant-section intervals, including every open notch.
    """
    levels=sorted({h0,h1,*[x for x,_ in poly.exterior.coords if h0<x<h1]})
    pieces=[]
    for lo,hi in zip(levels,levels[1:]):
        cut=poly.intersection(LineString([((lo+hi)/2,-30),((lo+hi)/2,570)]))
        for line in lines(cut):
            s0,s1=line.bounds[1],line.bounds[3]
            if s1>s0:
                assert poly.buffer(1e-9).covers(box(lo,s0,hi,s1))
                pieces.append(sector(s0,s1,lo,hi,phase))
    return cq.Compound.makeCompound(pieces)


def common(a,b):
    s=a.intersect(b)
    return abs(s.Volume()),s


def run(out):
    original = {str(p.relative_to(ROOT)):sha(p) for folder in [C12,C13] for p in sorted(folder.iterdir()) if p.is_file()}
    out.update({"task":"CTB-014","stage":"B1_ONLY","priority":"P1","source_commit":HEAD,
        "sources":{"CTB-012":"3326b49fc49eaa63c6ef2a904a7d3cb69fec2ebd / PR56 OPEN",
                   "CTB-013":HEAD+" / PR57 OPEN"},"source_sha256":original,
        "engine":{n:importlib.metadata.version(n) for n in ["cadquery","cadquery-ocp","shapely","ezdxf"]},
        "units":"mm, right-handed XYZ; native rim x=height,y=developed length",
        "mapping":"rho171..175; Z=450+h; theta=phase+(s-0.2)/173; phases15/195 degrees, per CTB-012 README",
        "mapping_status":"source-defined NOMINAL ideal cylindrical wrap only; no physical bend/kerf/strength assumption",
        "numerical_overlap_epsilon_mm3":EPS,"source_coordinate_quantization_mm":1e-6,
        "release":"DESIGN_ONLY / NO_CUTTING_APPROVAL / G3_NOT_RUN / G4_BLOCKED",
        "interfaces":["IF-10","IF-11"],"open_dependencies":["IF-07","IF-08","IF-12"],
        "cases":[],"geometric_failures":[],"source_geometry_repairs":0,"checker_repairs":1,
        "execution_attempts":3,"checker_adaptations":1,"extra_source_only_diagnostic_rebuilds":1,
        "execution_history":[{"attempt":1,"outcome":"ABORTED_ON_REAL_SOURCE_DXF_FORMAT_ERROR",
            "detail":"ezdxf refused first source: missing AcDbPolyline subclass. No CAD cases ran; no sources repaired."},
            {"attempt":2,"outcome":"CHECKER_FALSE_FAILURE_BEFORE_CAD","detail":"Raw regenerated DXF bytes compared:39 vs39.0 etc. Independent tag comparison confirms same numeric contours. Corrected checker to numeric vertices. Sources unchanged."},
            {"attempt":3,"outcome":"DIAGNOSTIC_RUN","detail":"Retain every importer failure; inspect raw original DXF tags to cross-check SVG and permit bounded nominal CAD analysis. No DXF recovery/repair."}],
        "not_run":[]})
    profiles={}
    for folder in [C12,C13]:
        for p in sorted(folder.glob("*.svg")):
            poly,rings=svg(p)
            import_error=None
            try:
                doc=ezdxf.readfile(p.with_suffix(".dxf"))
                assert doc.units==4
            except ezdxf.DXFStructureError as exc:
                import_error=str(exc)
            raw=raw_dxf_geometry(p.with_suffix(".dxf"))
            assert raw==rings and len({Polygon(r).normalize().wkb for r in raw})==len(raw)
            profiles[p.stem]=poly
            out["cases"].append({"id":p.stem+".svg","status":"PASS","scope":"units, closed/simple contours, topology, independent raw DXF/SVG vertex equality","contours":len(rings)})
            row={"id":p.stem+".dxf","status":"FAIL" if import_error else "PASS",
                 "standard_import_error":import_error,"raw_coordinates_equal_SVG":True,"source_repaired":False}
            out["cases"].append(row)
    print("Source import:8 SVG PASS;8 standard DXF FAIL; raw DXF coordinates agree with SVG",flush=True)
    with tempfile.TemporaryDirectory(prefix="ctb014-rebuild-") as tmp:
        subprocess.run([sys.executable,str(C12/"build_ctb012.py"),"--repo-root",str(ROOT),"--out",tmp],check=True,capture_output=True)
        generated=list(Path(tmp).glob("*.svg"))
        assert len(generated)==6
        for p in generated:
            _,rings=svg(p)
            assert rings==svg(C12/p.name)[1]
            assert raw_dxf_geometry(p.with_suffix(".dxf"))==raw_dxf_geometry(C12/p.with_suffix(".dxf").name)
        out["cases"].append({"id":"CTB012_clean_rebuild","status":"PASS","scope":"12 temporary exports equal source geometry; repo sources not regenerated"})
    centers=[45,135,225,315,405,495]
    out["kerf_lands"]={}
    for name in ["P07R1_NOTCHED_DESIGN_ONLY","P07R1_REINFORCED_DESIGN_ONLY","P07R1_PUZZLE_DESIGN_ONLY","P07R2_PUZZLE_DESIGN_ONLY"]:
        p=profiles[name]
        slots=[Polygon(h) for h in p.interiors]
        assert len(slots)==63
        lands=[]
        for c in centers:
            for x in [6,44]:
                floor=LineString([(x,c-6),(x,c+6)])
                lands.append(min(floor.distance(h) for h in slots))
        short=sum(abs(h.bounds[2]-h.bounds[0]-26)<1e-6 for h in slots)
        expected=2 if "NOTCHED" in name else 6
        assert abs(min(lands)-expected)<1e-6
        assert short==(0 if "NOTCHED" in name else 18)
        out["kerf_lands"][name]={"minimum_notch_floor_to_kerf_mm":min(lands),"slots":63,"shortened_slots":short}
        out["cases"].append({"id":"land/"+name,"status":"PASS","scope":"actual flat notch floors vs every kerf aperture; geometric land only"})
    skins={"P07B":plate(profiles["P07B_TABBED_DESIGN_ONLY"],450),"P07T":plate(profiles["P07T_TABBED_DESIGN_ONLY"],494)}
    out["skin_final_fit"]=[]
    for rim,phase in [("P07R1",15),("P07R2",195)]:
        p=profiles[rim+"_PUZZLE_DESIGN_ONLY"]
        for skin,h0,h1 in [("P07B",0,6),("P07T",44,50)]:
            material=slab_material(p,h0,h1,phase)
            volume,_=common(skins[skin],material)
            row={"id":rim+"|"+skin,"overlap_mm3":volume,"status":"PASS" if volume<EPS else "FAIL",
                 "scope":"complete shell material in skin Z band, exact circular-sector BReps; not a whole-shell solid"}
            out["skin_final_fit"].append(row);out["cases"].append(row)
            if volume>=EPS:out["geometric_failures"].append(row)
    print("Skin final-band intersections",out["skin_final_fit"],flush=True)
    # Two controls of the actual OCC Boolean and coordinate interpretation.
    wall=cq.Workplane("XY",origin=(0,0,494)).circle(175).circle(171).extrude(6).val()
    filled,_=common(skins["P07T"],wall)
    assert filled>10
    out["cases"].append({"id":"negative_filled_rim_notches","status":"PASS","detected_overlap_mm3":filled})

    # A final-state impossibility witness is sufficient: no deformation-free
    # insertion path can end in an overlapping final state. Use independent
    # conservative rectangles inscribed in each source profile, not a guessed
    # whole-shell mesh or a manufactured clearance.
    period=math.pi*R
    out["seams"]=[]
    assembly=cq.Assembly(name="CTB014_B1_SOURCE_MATERIAL_SUBSET_WITNESSES_ONLY")
    for index,phase in enumerate([15,195],1):
        male=profiles[f"P07R{index}_PUZZLE_DESIGN_ONLY"]
        other=profiles[f"P07R{3-index}_PUZZLE_DESIGN_ONLY"]
        female=translate(other,yoff=-period)
        flat=male.intersection(female)
        h0,h1=18.3,18.4
        # All involved source edges are linear on this h interval: endpoint
        # bounds give conservative material rectangles across the entire band.
        a=box(h0,-4.83999,h1,-3.34001)
        b=box(h0,-3.51999,h1,-2.20001)
        assert male.covers(a) and female.covers(b)
        assert a.intersection(b).area>.01
        sa=sector(a.bounds[1],a.bounds[3],h0,h1,phase)
        sb=sector(b.bounds[1],b.bounds[3],h0,h1,phase)
        volume,hit=common(sa,sb)
        assert volume>EPS and hit.isValid(),"source-derived witness unexpectedly failed"
        q=hit.BoundingBox()
        row={"id":f"seam{index}_phase{phase}","status":"FAIL","male_body":f"P07R{index}","female_body":f"P07R{3-index}",
             "OCC_proved_overlap_lower_bound_mm3":volume,"witness_bbox_xyz_mm":[q.xmin,q.ymin,q.zmin,q.xmax,q.ymax,q.zmax],
             "source_male_rectangle_h_s_mm":list(a.bounds),"source_female_wrapped_rectangle_h_s_mm":list(b.bounds),
             "source_subset_containment_proved":True,"developed_intersection_area_mm2":flat.area,
             "ideal_wrap_overlap_volume_analytic_mm3":4*flat.area,
             "analytic_volume_scope":"whole joint under nominal injective cylindrical map; NOT a full-shell Boolean volume",
             "half_circumference_mm":period,"body_length_mm":543.295529-.2,
             "per_seam_registration_shortfall_mm":period-(543.295529-.2)}
        out["seams"].append(row);out["cases"].append(row);out["geometric_failures"].append(row)
        for label,s in [("male_SUBSET",sa),("female_SUBSET",sb),("actual_common_VOLUME",hit)]:
            assembly.add(s,name=f"SEAM{index}_{label}")
    separated,_=common(sa,sb.translate((0,0,1)))
    assert separated<EPS
    out["cases"].append({"id":"negative_separated_witnesses","status":"PASS","overlap_mm3":separated})
    assembly.save(str(HERE/"collision-witnesses-DESIGN_ONLY.step"))
    step=HERE/"collision-witnesses-DESIGN_ONLY.step"
    # OCCT's native STEP writer adds end-of-line blanks. Only normalize this
    # generated diagnostic artifact; source vectors and STEP tokens stay intact.
    step.write_text("\n".join(line.rstrip() for line in step.read_text().splitlines())+"\n")
    out["witness_STEP_sha256"]=sha(HERE/"collision-witnesses-DESIGN_ONLY.step")
    out["puzzle_neck"]={"nominal_neck_one_sided_limit_mm":12,"head_span_at_s_minus4_mm":male.intersection(LineString([(0,-4),(50,-4)])).length,
                        "tip_span_at_s_minus7p8_mm":male.intersection(LineString([(0,-7.8),(50,-7.8)])).length,
                        "source_fillet_radius":"sharp polygon; no specified fillet","strength":"NOT_RUN_NOT_INFERRED"}
    out["assembly_path"]={"status":"BLOCKED_AT_FINAL_STATE","swept_motion_kernel_runs":0,
        "reason":"both seams have positive-volume source-material overlap at the proposed final frame; a collision-free rigid path to that final state is impossible",
        "not_claimed":"elastic snap/flex route, material deformation, physical kerf or strength"}
    out["not_run"]=["whole-shell reconstruction and full insertion sweep: stopped at terminal collision witness",
                    "top/bottom insertion path approval; final-band fit is not path proof","physical snap/bend/kerf/stock/glue/strength","nesting, B2, historical regressions"]
    assert all(sha(ROOT/p)==digest for p,digest in original.items())
    assert not subprocess.check_output(["git","diff",HEAD,"--","projects/CTB-01/parts","projects/CTB-01/specifications","projects/CTB-01/assemblies"],cwd=ROOT)
    out["all_original_sources_unchanged"]=True
    out["decision"]="NO-GO_CURRENT_NOMINAL_GEOMETRY / STOP_AFTER_B1 / LEAD_REVIEW_PENDING"
    out["counts"]={"unique_cases":len(out["cases"]),"pass":sum(c["status"]=="PASS" for c in out["cases"]),
                   "fail":sum(c["status"]=="FAIL" for c in out["cases"]),"negative_controls":2,"source_repairs":0,"checker_repairs":1}


if __name__=="__main__":
    result={"decision":"BLOCKED_CHECKER_INCOMPLETE"}
    try:
        run(result)
    except Exception as e:
        import traceback
        result["checker_failure"]={"detail":str(e),"traceback":traceback.format_exc()}
        raise
    finally:
        (HERE/"evidence.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"decision":result["decision"],"counts":result["counts"]},indent=2))
