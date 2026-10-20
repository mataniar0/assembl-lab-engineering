"""Independent CTB-006 OpenCASCADE audit of actual cut exports.
No P06 or upstream implementation models imported. Risk-based scope only; no broad337-suite rerun.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,subprocess,xml.etree.ElementTree as ET
import cadquery as cq
import ezdxf
import numpy as np
import trimesh
from shapely.geometry import Polygon,Point,LineString,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'projects/CTB-01/parts/P06').is_dir())
PARTS=ROOT/'projects/CTB-01/parts';PART=PARTS/'P06';BASE='c27f722e16668e4ed32cee1c72f5a699b40e504e';EPS=1e-6
SWEEP_NUMERIC_ARTIFACTS=[]


def svg(path):
    root=ET.parse(path).getroot();cut=root.find('.//{http://www.w3.org/2000/svg}g[@id="CUT"]')
    if cut is None:cut=root
    loops=[[(float(x),float(y)) for x,y in (v.split(',') for v in e.attrib['points'].split())] for e in cut.findall('.//{http://www.w3.org/2000/svg}polygon')]
    assert loops,path
    p=Polygon(loops[0],loops[1:]);assert p.is_valid and p.geom_type=='Polygon',(path,'invalid/disconnected material')
    return p


def export_audit(path):
    p=svg(path);root=ET.parse(path).getroot();vb=[float(v) for v in root.attrib['viewBox'].split()]
    assert abs(float(root.attrib['width'].removesuffix('mm'))-vb[2])<1e-5
    assert abs(float(root.attrib['height'].removesuffix('mm'))-vb[3])<1e-5
    doc=ezdxf.readfile(path.with_suffix('.dxf'));assert doc.units==4
    loops=[]
    for e in doc.modelspace():
        if e.dxf.layer.startswith('CUT'):
            assert e.dxftype()=='LWPOLYLINE' and e.closed
            xy=[(v[0],v[1]) for v in e.get_points()];assert len(xy)==len(set(xy))
            loops.append(xy)
    q=Polygon(loops[0],loops[1:]);assert q.is_valid and p.symmetric_difference(q).area<1e-6
    assert p.bounds[2]-p.bounds[0]+20<=440 and p.bounds[3]-p.bounds[1]+20<=800
    assert len(doc.audit().errors)==0
    return p,{'area_mm2':p.area,'bounds_mm':list(p.bounds),'cut_loops':len(loops),'DXF_SVG_area_delta_mm2':p.symmetric_difference(q).area,'single_part_H800_W440_margin10_fit':True}


def extrude(poly,plane,height):
    work=cq.Workplane(plane).polyline(list(poly.exterior.coords)[:-1]).close()
    for h in poly.interiors:work=work.polyline(list(h.coords)[:-1]).close()
    s=work.extrude(height).val();assert s.isValid() and len(s.Solids())==1
    return s


def plate(poly,z,height=6):return extrude(poly,cq.Plane(origin=(0,0,z),xDir=(1,0,0),normal=(0,0,1)),height)
def cheek(poly,t_top,height=6):return extrude(poly,cq.Plane(origin=(0,t_top,0),xDir=(1,0,0),normal=(0,-1,0)),height)
def spin(s,a):return s.rotate((0,0,0),(0,0,1),a)


def overlap(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if any(getattr(aa,c+'max')<=getattr(bb,c+'min')+1e-9 or getattr(bb,c+'max')<=getattr(aa,c+'min')+1e-9 for c in 'xyz'):return 0.
    v=abs(a.intersect(b).Volume());assert math.isfinite(v);return v


def sweep2(poly,dx=0,dy=0):
    pieces=[poly,translate(poly,xoff=dx,yoff=dy)]
    for ring in (poly.exterior,*poly.interiors):
        for p,q in zip(ring.coords,list(ring.coords)[1:]):
            cell=Polygon([p,q,(q[0]+dx,q[1]+dy),(p[0]+dx,p[1]+dy)])
            if cell.area>1e-10:pieces.append(cell)
    out=unary_union(pieces);assert out.is_valid and out.geom_type=='Polygon'
    # Rotated collinear boundary unions can leave zero-area (~1e-28 mm2) rings.
    # Filter only this generated intermediate, never the actual exported cut profiles.
    tiny=[Polygon(h).area for h in out.interiors if Polygon(h).area<1e-14]
    if tiny:
        clean=Polygon(out.exterior,[h.coords for h in out.interiors if Polygon(h).area>=1e-14])
        delta=clean.symmetric_difference(out).area;assert delta<1e-14 and clean.is_valid
        SWEEP_NUMERIC_ARTIFACTS.append({'removed_hole_areas_mm2':tiny,'area_delta_mm2':delta,'threshold_mm2':1e-14})
        out=clean
    return out


def matrix(solids):return {a+'|'+b:overlap(x,y) for (a,x),(b,y) in itertools.combinations(solids.items(),2)}


def stage(label,swept,fixed):
    checks={k:overlap(swept,v) for k,v in fixed.items()}
    return {'moving':label,'checks':len(checks),'maximum_overlap_mm3':max(checks.values(),default=0.),'positive_pairs_mm3':{k:v for k,v in checks.items() if v>EPS}}


def base19(profile=None):
    p03=PARTS/'P03/variants/A_COMPACT_CLOSED'
    face=svg(p03/'P01-Y-mortise-study-v1.svg') if profile is None else profile
    stations=json.loads((p03/'mechanical-dimensions.json').read_text())['stations']
    parts={'P03':plate(svg(p03/'P03.svg'),407)}
    for leg,a in enumerate([0,120,240],1):
        for i,t in enumerate([-7.5,13.5],1):parts[f'L{leg}_P01_{i}']=spin(cheek(face,t),a)
        for s in stations:
            p=translate(svg(PARTS/f"P02/variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
            parts[f"L{leg}_{s['id']}"]=spin(plate(p,s['z_mm']-3),a)
    assert len(parts)==19
    return parts,face,stations


def base27(profile=None):
    parts,face,stations=base19(profile)
    for layer,z in [('P04L',456),('P04U',480)]:parts[layer]=plate(svg(PARTS/f'P04/variants/A/{layer}.svg'),z)
    p05=svg(PARTS/'P05/variants/A/P05.svg')
    parts.update({f'P05_{i+1}':spin(cheek(p05,3),a) for i,a in enumerate(range(0,360,60))})
    assert len(parts)==27
    return parts,face,stations


def y_first(parts,face,stations,extra_fixed=None):
    fixed={**(extra_fixed or {}),'P03':parts['P03']};stages=[]
    for leg,a in enumerate([0,120,240],1):
        seq=[('P01_1',cheek(face,-7.5,46))]
        for s in stations:
            p=translate(svg(PARTS/f"P02/variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
            seq.append((s['id'],plate(sweep2(p,dy=40),s['z_mm']-3)))
        seq.append(('P01_2',cheek(face,53.5,46)))
        for key,s in seq:
            label=f'L{leg}_{key}';record=stage(label,spin(s,a),fixed);stages.append(record);fixed[label]=parts[label]
    assert len(stages)==18
    return {'stages':stages,'checks':sum(s['checks'] for s in stages),'maximum_overlap_mm3':max(s['maximum_overlap_mm3'] for s in stages)},fixed


def physical_reference():
    _,face,stations=base19();sections={}
    for z in [*range(225,266,5),242,248]:
        s=face.intersection(LineString([[-100,z],[400,z]]));sections[str(z)]=[s.bounds[0],s.bounds[2]]
    q=face.intersection(LineString([[-100,0],[400,0]]));a,_,b,_=q.bounds
    feet=[rotate(box(a,t-3,b,t+3),ang,origin=(0,0)) for ang in [0,120,240] for t in [-10.5,10.5]]
    hull=unary_union(feet).convex_hull
    return {'P01_sections_r_mm':sections,'current_spacer_stations':[s['z_mm'] for s in stations],
            'ring_to_S3_vertical_face_gap_mm':39,'foot_r_mm':[a,b],'ground_contact_each_cheek_mm2':(b-a)*6,
            'support_hull_xy_mm':[list(v) for v in hull.exterior.coords],'support_min_center_edge_distance_mm':hull.exterior.distance(Point(0,0)),
            'module_center_triangle_inradius_mm':120,'no_stability_or_load_claim':True}


def protected():
    prefixes=['projects/CTB-01/specifications/CTB-000',*[f'projects/CTB-01/parts/P{i:02}' for i in range(1,6)]]
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,*prefixes],cwd=ROOT,text=True).splitlines()
    for n in names:
        src=subprocess.check_output(['git','show',BASE+':'+n],cwd=ROOT)
        assert (ROOT/n).read_bytes()==src,n
    assert len(names)==336
    return {'baseline':BASE,'files_byte_equal':len(names)}


def bounds(s):
    q=s.BoundingBox();return np.array([[q.xmin,q.ymin,q.zmin],[q.xmax,q.ymax,q.zmax]])


def glb_audit(path,reference):
    scene=trimesh.load(path,force='scene');assert len(scene.geometry)==len(reference)==len(scene.graph.nodes_geometry)
    unmatched=dict(reference);worst_bound=worst_volume=0.
    for node in scene.graph.nodes_geometry:
        tf,g=scene.graph[node];m=scene.geometry[g].copy();m.apply_transform(tf)
        assert m.is_watertight and m.volume>0
        match=[]
        for label,s in unmatched.items():
            db=float(np.max(np.abs(m.bounds*1000-bounds(s))));dv=abs(m.volume*1e9/s.Volume()-1)
            if db<.001 and dv<1e-5:match.append((label,db,dv))
        assert len(match)==1,(path,node,match)
        label,db,dv=match[0];unmatched.pop(label);worst_bound=max(worst_bound,db);worst_volume=max(worst_volume,dv)
    assert not unmatched
    return {'nodes':len(reference),'units':'GLTF_metres','maximum_bounds_delta_mm':worst_bound,'maximum_relative_volume_delta':worst_volume}


def key_c(profile,joint,side,angle):
    return spin(spin(cheek(profile,3),90*side).translate((joint,0,0)),angle)


def ring_first(parts,face,stations,ring,key_profile=None,joint=None):
    """Bounded changed-interface route: ring, Y, 18 original base pieces, then C keys."""
    initial=dict(ring);y=svg(PARTS/'P03/variants/A_COMPACT_CLOSED/P03.svg')
    lead=stage('P03_lower_from520',plate(y,407,119),initial)
    route,fixed=y_first(parts,face,stations,initial)
    route['stages'].insert(0,lead)
    if key_profile is not None:
        for leg,angle in enumerate([0,120,240],1):
            for side in [-1,1]:
                label=f'P06C_K{leg}_{"N" if side<0 else "P"}'
                swept=key_c(sweep2(key_profile,dy=40),joint,side,angle)
                route['stages'].append(stage(label+'_down40',swept,fixed));fixed[label]=parts[label]
    route['checks']=sum(s['checks'] for s in route['stages'])
    route['maximum_overlap_mm3']=max(s['maximum_overlap_mm3'] for s in route['stages'])
    return route


def segmented_late(parts,segments,stop_profile):
    prior={k:v for k,v in parts.items() if not k.startswith('P06')};steps=[]
    for index,(label,p) in enumerate(segments.items()):
        a=math.radians(index*120);dx=-40*math.sin(a);dy=40*math.cos(a)
        steps.append(stage(label+'_entry40',plate(sweep2(p,dx,dy),248.4),prior))
        steps.append(stage(label+'_lower6p4',plate(p,242,12.4),prior));prior[label]=parts[label]
    for leg,angle in enumerate([0,120,240],1):
        for side in [-1,1]:
            label=f'P06B_K{leg}_{"N" if side<0 else "P"}'
            top=(-7.5 if side<0 else 13.5)+(0 if side<0 else 40)
            steps.append(stage(label+'_entry40',spin(cheek(stop_profile,top,46),angle),prior));prior[label]=parts[label]
    return {'stages':steps,'checks':sum(s['checks'] for s in steps),'maximum_overlap_mm3':max(s['maximum_overlap_mm3'] for s in steps)}


def restraint(parts,face,name):
    """Keep ring/keepers fixed while each cheek moves; excludes upstream Y/spacer restraints."""
    ring={k:v for k,v in parts.items() if k.startswith('P06')};without_keys={k:v for k,v in ring.items() if '_K' not in k};rows=[]
    for leg,angle in enumerate([0,120,240],1):
        for side in [-1,1]:
            top=-7.5 if side<0 else 13.5
            outward=spin(cheek(face,top+(4 if side>0 else 0),10),angle)
            radial={f'radial_{"out" if dx>0 else "in"}':spin(cheek(sweep2(face,dx=dx),top),angle) for dx in [-4,4]}
            row={'leg':leg,'side':side,'outward_t_with_keys_mm3':max(overlap(outward,v) for v in ring.values()),
                 'outward_t_without_keys_mm3':max(overlap(outward,v) for v in without_keys.values())}
            row.update({k+'_mm3':max(overlap(s,v) for v in ring.values()) for k,s in radial.items()});rows.append(row)
    assert all(r['radial_in_mm3']>EPS and r['radial_out_mm3']>EPS for r in rows),('radial coupling',name,rows)
    if name=='C':assert all(r['outward_t_with_keys_mm3']>EPS and r['outward_t_without_keys_mm3']<EPS for r in rows)
    else:assert all(r['outward_t_with_keys_mm3']<EPS for r in rows)
    return {'scope':'geometric obstruction only; keepers fixed; no force/6DOF claim','six_cheeks':rows}


def variant_audit(name,ring_paths,overlay_path,key_path,glb_path):
    print(f'Independent OCC {name}: auditing actual exports and paths',flush=True)
    exports={};rings={}
    for label,path in ring_paths.items():rings[label],exports[path.name]=export_audit(path)
    face,exports[overlay_path.name]=export_audit(overlay_path)
    if key_path is not None:key,exports[key_path.name]=export_audit(key_path)
    else:key=None
    parts,_,stations=base27(face);parts.update({k:plate(p,242) for k,p in rings.items()})
    # Derive joint radius from the symmetry of actual exported tab extremes on leg0.
    tab=next(iter(rings.values())).intersection(LineString([[80,10.5],[160,10.5]]));joint=(tab.bounds[0]+tab.bounds[2])/2
    for leg,angle in enumerate([0,120,240],1):
        for side in [-1,1]:
            label=f'P06{name}_K{leg}_{"N" if side<0 else "P"}'
            if name=='B':parts[label]=spin(cheek(key,-7.5 if side<0 else 13.5),angle)
            elif name=='C':parts[label]=key_c(key,joint,side,angle)
    expected={'A':28,'B':36,'C':34}[name];assert len(parts)==expected
    pairs=matrix(parts);assert max(pairs.values())<EPS,(name,'nominal',sorted(pairs.items(),key=lambda a:-a[1])[:10])
    original,_,_=base27();unmodified={k:v for k,v in original.items() if 'P01' in k}
    original_hits={k:max(overlap(v,parts[r]) for r in rings) for k,v in unmodified.items()};assert all(v>EPS for v in original_hits.values())
    if name=='B':route=segmented_late(parts,rings,key)
    else:route=ring_first(parts,face,stations,{k:parts[k] for k in rings},key,joint)
    assert route['maximum_overlap_mm3']<EPS,(name,'claimed route',route)
    late=[]
    if name!='B':
        p=next(iter(rings.values()))
        late=[stage('after_closed_base_from_above',plate(p,242,364),original),stage('after_closed_base_radial60',plate(sweep2(p,dx=60),242),original)]
        assert all(s['maximum_overlap_mm3']>EPS for s in late)
    old=translate(svg(PARTS/'P02/variants/B_THROUGH_ADHESIVE/P02.svg'),xoff=joint)
    old_hit=max(overlap(plate(old,242),v) for k,v in parts.items() if k.startswith('P06'));assert old_hit>EPS
    s3={k:v for k,v in original.items() if k.endswith('_S3')}
    s3hits={k+'|'+r:overlap(s,parts[r]) for k,s in s3.items() for r in parts if r.startswith('P06')};assert max(s3hits.values())<EPS
    ejection=None
    if name in ('B','C'):
        label=f'P06{name}_K1_P'
        swept=cheek(key,53.5,46) if name=='B' else key_c(sweep2(key,dy=40),joint,1,0)
        ejection=stage(label+'_ejection',swept,{k:v for k,v in parts.items() if k!=label});assert ejection['maximum_overlap_mm3']<EPS
    original_face=svg(PARTS/'P03/variants/A_COMPACT_CLOSED/P01-Y-mortise-study-v1.svg')
    delta=original_face.difference(face);outer=original_face.intersection(LineString([[0,248.2],[400,248.2]])).bounds[2]
    p=next(iter(rings.values()));arm=p.intersection(LineString([[90,-40],[90,40]]))
    lands={'arm_width_mm':arm.length,'arm_to_each_inner_cheek_gap_mm':(15-arm.length)/2,
           'minimum_outer_radial_cheek_land_at_expanded_band_mm':outer-delta.bounds[2]}
    if name=='B':
        section=rotate(p,60,origin=(0,0)).intersection(LineString([[0,4],[80,4]]))
        lands['female_splice_radial_lands_mm']=[v.length for v in section.geoms]
        assert min(lands['female_splice_radial_lands_mm'])>6
    if name=='C':
        section=p.intersection(LineString([[joint,-40],[joint,40]]))
        lands['outer_keyslot_lands_mm']=[section.geoms[i].length for i in [0,2]]
        # Actual filleted head's horizontal boundary at Z248, intersected with ring material.
        seat=key.intersection(LineString([[20.3,248],[40,248]])).length
        lands['actual_key_horizontal_bearing_width_mm']=seat;lands['bearing_boundary_area_per_key_mm2']=seat*6
        assert min(lands['outer_keyslot_lands_mm'])>6 and abs(seat-1.3)<1e-5
    result={'exports':exports,'body_count':len(parts),'static_pairs':len(pairs),'maximum_overlap_mm3':max(pairs.values()),
            'original_selected_P01_without_CR_collision_mm3':original_hits,'actual_joint_center_r_mm':joint,
            'claimed_route':route,'blocked_late_routes':late,'hypothetical_Z245_S3_overlap_mm3':old_hit,
            'actual_Z200_S3_maximum_overlap_mm3':max(s3hits.values()),'ring_family_min_Z_mm':min(bounds(v)[0,2] for k,v in parts.items() if k.startswith('P06')),
            'export_derived_geometric_lands':lands,'restraint':restraint(parts,face,name),'keeper_ejection':ejection,'glb':glb_audit(glb_path,parts)}
    return result


def audit(output):
    source,face,stations=base27();baseline_matrix=matrix(source)
    route,_=y_first(source,face,stations)
    assert len(baseline_matrix)==351 and max(baseline_matrix.values())<EPS
    assert route['checks']==171 and route['maximum_overlap_mm3']<EPS
    print('Independent OCC upstream bounded baseline: 351 static +171 exact Y_FIRST checks PASS',flush=True)
    result={'scope':'Risk-based CTB006: actual exported geometry, focused integration; broad337 previous cases deliberately NOT_RUN',
            'method':'Independent OpenCASCADE with exact boundary-prism translational sweeps; no implementation imports',
            'upstream_27_static':{'pairs':351,'maximum_overlap_mm3':max(baseline_matrix.values())},
            'upstream_Y_FIRST':route,'physical_reference':physical_reference(),'protected':protected(),'variants':{}}
    for name,labels in [('A',['P06A']),('B',['P06B1','P06B2','P06B3']),('C',['P06C'])]:
        cut=PART/'variants'/name
        result['variants'][name]=variant_audit(name,{label:cut/(label+'.svg') for label in labels},
            PART/'proposals'/name/'P01-ring-interface-study-v1.svg',
            None if name=='A' else cut/f'P06{name}-KEY.svg',PART/'assembly'/f'{name}-conditional-DESIGN_ONLY.glb')
        output.write_text(json.dumps(result,indent=2)+'\n')
        print(f'Independent OCC {name}: PASS ({result["variants"][name]["body_count"]} bodies)',flush=True)
    result['export_SHA256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PART.rglob('*')) if p.suffix in ('.svg','.dxf','.glb')}
    result['intermediate_sweep_numerical_artifacts']=SWEEP_NUMERIC_ARTIFACTS
    output.write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path('/tmp/ctb006-independent-occ-results.json'))
    audit(parser.parse_args().output)
