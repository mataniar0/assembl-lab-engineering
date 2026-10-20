"""CTB004 alternate OpenCASCADE audit of exported SVG/DXF, no P04 source imports."""
from pathlib import Path
import json, math, itertools, xml.etree.ElementTree as ET
import cadquery as cq
import ezdxf
import trimesh
from shapely.geometry import Polygon, box, Point
from shapely.affinity import rotate, translate
from shapely.ops import unary_union
ROOT=next((p for p in Path(__file__).resolve().parents if (p/'projects/CTB-01/parts/P04').is_dir()), Path('/workspace/assembl-lab-engineering'));P=ROOT/'projects/CTB-01/parts';P04=P/'P04'

def svg(path):
    r=ET.parse(path).getroot();loops=[]
    cut=r.find('.//{http://www.w3.org/2000/svg}g[@id="CUT"]')
    if cut is None:cut=r
    for n in cut.findall('.//{http://www.w3.org/2000/svg}polygon'):
        if n.attrib.get('points'):
            loops.append([(float(a),float(b)) for a,b in (p.split(',') for p in n.attrib['points'].split())])
    assert loops, path
    p=Polygon(loops[0],loops[1:]);assert p.is_valid and p.area>0,(path,p.is_valid)
    return p

def planar(poly,plane,h):
    assert poly.geom_type=='Polygon'
    q=cq.Workplane(plane).polyline(list(poly.exterior.coords)[:-1]).close()
    for r in poly.interiors:q=q.polyline(list(r.coords)[:-1]).close()
    s=q.extrude(h).val();assert s.isValid() and len(s.Solids())==1
    return s

def plate(p,z=0,h=6):return planar(p,cq.Plane(origin=(0,0,z),xDir=(1,0,0),normal=(0,0,1)),h)
def cheek(p,top_t=13.5,h=6):return planar(p,cq.Plane(origin=(0,top_t,0),xDir=(1,0,0),normal=(0,-1,0)),h)
def spin(s,a):return s.rotate((0,0,0),(0,0,1),a)
def volume(a,b):
    x=a.BoundingBox();y=b.BoundingBox()
    if any(getattr(x,k+'max')<getattr(y,k+'min')-1e-9 or getattr(y,k+'max')<getattr(x,k+'min')-1e-9 for k in 'xyz'):return 0.
    v=abs(a.intersect(b).Volume());assert math.isfinite(v);return v

def sweep2(p,dx=0,dy=0):
    pieces=[p,translate(p,xoff=dx,yoff=dy)]
    for ring in [p.exterior,*p.interiors]:
        for a,b in zip(ring.coords,list(ring.coords)[1:]):
            q=Polygon([a,b,(b[0]+dx,b[1]+dy),(a[0]+dx,a[1]+dy)])
            if q.area>1e-10:pieces.append(q)
    q=unary_union(pieces);assert q.is_valid
    return q

def base():
    f=P/'P03/variants/A_COMPACT_CLOSED';face=svg(f/'P01-Y-mortise-study-v1.svg');y=svg(f/'P03.svg')
    stations=json.loads((f/'mechanical-dimensions.json').read_text())['stations'];out={'P03':plate(y,407)}
    for leg,a in enumerate([0,120,240],1):
        for i,t in enumerate([-7.5,13.5],1):out[f'L{leg}_P01_{i}']=spin(cheek(face,t),a)
        for s in stations:
            p=translate(svg(P/f"P02/variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
            out[f"L{leg}_{s['id']}"]=spin(plate(p,s['z_mm']-3),a)
    assert len(out)==19
    return out,face

def export_audit(path,has_center_hole=False):
    p=svg(path);root=ET.parse(path).getroot()
    vb=list(map(float,root.attrib['viewBox'].split()))
    assert abs(float(root.attrib['width'].removesuffix('mm'))-vb[2])<1e-5
    assert abs(float(root.attrib['height'].removesuffix('mm'))-vb[3])<1e-5
    d=ezdxf.readfile(path.with_suffix('.dxf'));assert d.header['$INSUNITS']==4
    rows=[]
    for e in d.modelspace().query('LWPOLYLINE'):
        if not e.dxf.layer.startswith('CUT_'):continue
        assert e.closed
        xy=[(v[0],v[1]) for v in e.get_points()]
        assert len(xy)==len(set(xy)),(path,'duplicate vertex')
        rows.append(xy)
    # Exporter can include dimension polylines on non-CUT layers; only closed polygon loops constitute material.
    rows.sort(key=lambda x:Polygon(x).area,reverse=True)
    q=Polygon(rows[0],rows[1:]);assert q.is_valid and p.symmetric_difference(q).area<1e-5,(path,'DXF-SVG mismatch')
    assert p.bounds[2]-p.bounds[0]+20<=440 and p.bounds[3]-p.bounds[1]+20<=800
    assert len(p.interiors)>=6 and (not p.contains(Point(0,0)))==has_center_hole
    land=min(Polygon(r).distance(p.exterior) for r in p.interiors)
    hh=min(Polygon(a).distance(Polygon(b)) for a,b in itertools.combinations(p.interiors,2))
    return p,{'area_mm2':p.area,'bounds_mm':list(p.bounds),'holes':len(p.interiors),'DXF_closed_loops':len(rows),'minimum_hole_to_exterior_mm':land,'minimum_hole_to_hole_mm':hh,'svg_dxf_area_delta_mm2':p.symmetric_difference(q).area}


def run_variants(output=Path('/tmp/ctb004-independent-occ-results.json')):
    actual,face=base();result={'method':'Independent exported SVG/DXF loops; OpenCASCADE solid kernel and exact boundary-prism sweeps. No P04 implementation imports.','base_actual_bodies':19,'variants':{}}
    tongue_rz=face.intersection(box(-1000,450,1000,488))
    assert tongue_rz.bounds==(45.,450.,69.,488.) and tongue_rz.difference(box(45,450,69,488)).area<1e-6
    result['active_tongue_RZ_area_mm2']=tongue_rz.area
    result['active_tongue_RZ_top_corners']='Exact exported source retained; rounded top, 24mm width across disk slabs, 22mm at Z488'
    footprints=[rotate(box(45,t-3,69,t+3),a,origin=(0,0)) for a in [0,120,240] for t in [-10.5,10.5]]
    for letter in ['A','B','C']:
        folders=sorted((P04/'variants').glob(letter+'*'));assert len(folders)==1,folders
        f=folders[0];entry={};lp,entry['P04L']=export_audit(f/'P04L.svg');up,entry['P04U']=export_audit(f/'P04U.svg',has_center_hole=letter=='C')
        for p in [lp,up]:
            assert max(p.intersection(t).area for t in footprints)<1e-6
            assert all(any(Polygon(h).contains(t) for h in p.interiors) for t in footprints)
        entry['minimum_tongue_edge_clearance_mm']=min(lp.distance(t) for t in footprints)
        l,u=plate(lp,456),plate(up,480);allreal={**actual,'P04L':l,'P04U':u}
        final={a+'|'+b:volume(x,y) for (a,x),(b,y) in itertools.combinations(allreal.items(),2)}
        assert len(allreal)==21 and len(final)==210 and max(final.values())<1e-6
        entry['final_21_real_checks']=len(final);entry['final_max_overlap_mm3']=max(final.values())
        skin=Point(0,0).buffer(171,quad_segs=180)
        for a in [0,120,240]:
            for t in [-10.5,10.5]:skin=skin.difference(rotate(box(44.8,t-3.1,69.2,t+3.1),a,origin=(0,0)))
        sk=plate(skin,450);skin_sweep=plate(skin,450,66)
        pv={n:volume(skin_sweep,x) for n,x in actual.items()};assert max(pv.values())<1e-6
        swl=plate(lp,456,60);swu=plate(up,480,36)
        vl={n:volume(swl,x) for n,x in {**actual,'P07B_ENVELOPE_ONLY':sk}.items()}
        vu={n:volume(swu,x) for n,x in {**actual,'P07B_ENVELOPE_ONLY':sk,'P04L':l}.items()}
        assert len(vl)==20 and len(vu)==21 and max([*vl.values(),*vu.values()])<1e-6
        rev=volume(swl,u);late=volume(skin_sweep,l)
        assert rev>1000 and late>1000
        entry['lowering_continuous_checks']={'P07B_envelope':len(pv),'P04L':len(vl),'P04U':len(vu),'maximum_overlap_mm3':max([*pv.values(),*vl.values(),*vu.values()])}
        entry['negative_order_mm3']={'lower_after_upper_sweep_into_upper':rev,'skin_after_lower_sweep_into_lower':late}
        witnesses=[];webs={};shape_types={};expected_angles={'A':{a:'OPEN' for a in range(0,360,60)},'B':{a:'RAIL' for a in range(0,360,60)},'C':{a:('OPEN' if a%120==0 else 'RAIL') for a in range(0,360,60)}}[letter]
        for typ in sorted(set(expected_angles.values())):
            w=svg(f/f'witness-{typ}.svg');assert w.bounds==(81.0,456.0,169.0,494.0),(letter,typ,w.bounds)
            assert len(cheek(w,3).Solids())==1
            shape_types[typ]=w
        for a,typ in expected_angles.items():
            name=f'WITNESS_{a}_{typ}_NOT_P05_RELEASE';webs[name]=spin(cheek(shape_types[typ],3),a)
        static={n+'|'+m:volume(x,y) for n,x in webs.items() for m,y in allreal.items()}
        static.update({a+'|'+b:volume(x,y) for (a,x),(b,y) in itertools.combinations(webs.items(),2)})
        assert len(static)==141 and max(static.values())<1e-6
        entry['six_nonBOM_witnesses']={'actual_P05_parts':0,'reservation_count':6,'static_checks':141,'max_overlap_mm3':max(static.values())}
        # Prove the topology-specific feasible order: L, RAIL vertically (if any), U, OPEN radially (if any).
        fixed={**actual,'P07B_ENVELOPE_ONLY':sk,'P04L':l};stage=[]
        for a,typ in expected_angles.items():
            if typ!='RAIL':continue
            moving=spin(cheek(sweep2(shape_types[typ],dy=70),3),a)
            vals={n:volume(moving,x) for n,x in fixed.items()};assert max(vals.values())<1e-6
            stage.append({'moving':f'RAIL_{a}','continuous_checks':len(vals),'max_overlap_mm3':max(vals.values())});fixed[f'RAIL_{a}']=webs[f'WITNESS_{a}_{typ}_NOT_P05_RELEASE']
        vals={n:volume(swu,x) for n,x in fixed.items()};assert max(vals.values())<1e-6
        stage.append({'moving':'P04U','continuous_checks':len(vals),'max_overlap_mm3':max(vals.values())});fixed['P04U']=u
        for a,typ in expected_angles.items():
            if typ!='OPEN':continue
            moving=spin(cheek(sweep2(shape_types[typ],dx=90),3),a)
            vals={n:volume(moving,x) for n,x in fixed.items()};assert max(vals.values())<1e-6
            stage.append({'moving':f'OPEN_{a}','continuous_checks':len(vals),'max_overlap_mm3':max(vals.values())});fixed[f'OPEN_{a}']=webs[f'WITNESS_{a}_{typ}_NOT_P05_RELEASE']
        entry['witness_conditional_path']=stage
        neg={}
        if 'OPEN' in shape_types:
            witness=cheek(shape_types['OPEN'],3);neg['U_after_OPEN']=volume(swu,witness);assert neg['U_after_OPEN']>1
            uncut=cheek(box(81,456,169,494),3);neg['uncut38mm_OPEN_web_final_upper']=volume(u,uncut);assert neg['uncut38mm_OPEN_web_final_upper']>1
        if 'RAIL' in shape_types:
            moving=cheek(sweep2(shape_types['RAIL'],dy=70),3)
            # Choose a rail angle in C rather than assuming angle0 is closed.
            a=next(k for k,v in expected_angles.items() if v=='RAIL')
            neg['RAIL_after_U']=volume(spin(moving,a),u);assert neg['RAIL_after_U']>1
            uncut=spin(cheek(box(81,456,169,494),3),a);neg['uncut38mm_RAIL_web_final_lower']=volume(l,uncut);assert neg['uncut38mm_RAIL_web_final_lower']>1
        rot=plate(rotate(lp,10,origin=(0,0)),456)
        neg['rotated10deg_disk_max']=max(volume(rot,x) for x in actual.values());assert neg['rotated10deg_disk_max']>1
        # Fill a real tongue opening chosen independently by containment of a realfootprint.
        hole=next(Polygon(h) for h in lp.interiors if Polygon(h).contains(footprints[0]))
        missing=plate(lp.union(hole),456);neg['missing_tongue_hole']=max(volume(missing,x) for x in actual.values());assert neg['missing_tongue_hole']>1
        thick=cheek(face,13.9,6.8);neg['thickness6.8_against_nominal_slot']=volume(l,thick);assert neg['thickness6.8_against_nominal_slot']>1
        neg['wrong24mm_freegap']={'actual_gap_mm':486-462,'upper_Z_mm':[486,492],'tongue_through_height_mm':488-486,'required_engagement_mm':6,'rejected':True}
        if letter=='B':
            wh=next(Polygon(h) for h in lp.interiors if Polygon(h).contains(Point(85,0)))
            misplaced=lp.union(wh).difference(rotate(wh,5,origin=(0,0)))
            wrong_web=cheek(shape_types['RAIL'],3)
        else:
            misplaced=lp.union(box(79.8,-3.2,94,3.2)).difference(rotate(box(80.8,-3.2,96.5,3.2),5,origin=(0,0)))
            wrong_web=cheek(shape_types['OPEN'],3)
        assert misplaced.is_valid and misplaced.geom_type=='Polygon'
        neg['single_web_interface_rotated5deg']=volume(plate(misplaced,456),wrong_web)
        assert neg['single_web_interface_rotated5deg']>1
        entry['genuine_negative_controls']=neg
        scene=trimesh.load(f/'actual-21-body-DESIGN_ONLY.glb',force='scene');meshrows={}
        assert len(scene.graph.nodes_geometry)==21
        for node in scene.graph.nodes_geometry:
            tf,g=scene.graph[node];m=scene.geometry[g].copy();m.apply_transform(tf);m.apply_scale(1000)
            assert node in allreal and m.is_watertight and m.volume>0
            ref=allreal[node];delta=abs(float(m.volume)-ref.Volume());assert delta/ref.Volume()<5e-6,(letter,node,delta)
            b=ref.BoundingBox();bounds=[[b.xmin,b.ymin,b.zmin],[b.xmax,b.ymax,b.zmax]]
            worst=max(abs(float(m.bounds[i][j])-bounds[i][j]) for i in range(2) for j in range(3))
            assert worst<0.0001,(letter,node,worst)
            meshrows[node]={'volume_mm3':float(m.volume),'OCC_volume_delta_mm3':delta,'bounds_max_error_mm':worst}
        entry['GLB_actual_21_watertight_metre_units']=meshrows
        result['variants'][letter]=entry
        print(letter,'independent21body/210final, continuous60skin+diskchecks, 141witnessstatic, paths and negativecontrols PASS',flush=True)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('/tmp/ctb004-independent-occ-results.json'))
    args=parser.parse_args()
    run_variants(args.output)
