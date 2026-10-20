"""Independent CTB005 audit from actual exported cut loops using OpenCASCADE.
No P05/P04/P03/P02/P01 implementation module is imported.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import subprocess
import xml.etree.ElementTree as ET

import cadquery as cq
import ezdxf
import numpy as np
import trimesh
from shapely.affinity import rotate, translate
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import unary_union

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'projects/CTB-01/parts/P05').is_dir())
PARTS=ROOT/'projects/CTB-01/parts';P05=PARTS/'P05'
EPS=1e-6


def svg(path):
    root=ET.parse(path).getroot();group=root.find('.//{http://www.w3.org/2000/svg}g[@id="CUT"]')
    if group is None:group=root
    loops=[]
    for e in group.findall('.//{http://www.w3.org/2000/svg}polygon'):
        loops.append([(float(a),float(b)) for a,b in (p.split(',') for p in e.attrib['points'].split())])
    assert loops,path
    poly=Polygon(loops[0],loops[1:]);assert poly.is_valid and poly.geom_type=='Polygon',(path,poly.is_valid)
    return poly


def export_audit(path,plane):
    poly=svg(path);root=ET.parse(path).getroot();vb=[float(x) for x in root.attrib['viewBox'].split()]
    assert abs(float(root.attrib['width'].removesuffix('mm'))-vb[2])<1e-5
    assert abs(float(root.attrib['height'].removesuffix('mm'))-vb[3])<1e-5
    assert 'DESIGN_ONLY' in ET.tostring(root).decode()
    doc=ezdxf.readfile(path.with_suffix('.dxf'));assert doc.units==4
    loops=[]
    for e in doc.modelspace():
        if e.dxf.layer.startswith('CUT'):
            assert e.dxftype()=='LWPOLYLINE' and e.closed
            points=[(p[0],p[1]) for p in e.get_points()]
            assert len(points)==len(set(points)),(path,'duplicate vertices')
            loops.append(points)
    assert len(loops)==len(poly.interiors)+1
    other=Polygon(loops[0],loops[1:]);assert other.is_valid
    assert poly.symmetric_difference(other).area<1e-7
    w=poly.bounds[2]-poly.bounds[0];h=poly.bounds[3]-poly.bounds[1]
    assert w+20<=440 and h+20<=800
    assert len(doc.audit().errors)==0
    holes=[Polygon(h) for h in poly.interiors]
    return poly,{'plane':plane,'area_mm2':poly.area,'bounds_mm':list(poly.bounds),'closed_cut_loops':len(loops),
                 'DXF_SVG_area_delta_mm2':poly.symmetric_difference(other).area,'single_part_sheet_fit':True,
                 'minimum_hole_to_exterior_mm':min((h.distance(poly.exterior) for h in holes),default=None),
                 'minimum_hole_to_hole_mm':min((a.distance(b) for a,b in itertools.combinations(holes,2)),default=None)}


def extrusion(poly,plane,height):
    work=cq.Workplane(plane).polyline(list(poly.exterior.coords)[:-1]).close()
    for ring in poly.interiors:work=work.polyline(list(ring.coords)[:-1]).close()
    solid=work.extrude(height).val();assert solid.isValid() and len(solid.Solids())==1
    return solid


def plate(poly,z,height=6):return extrusion(poly,cq.Plane(origin=(0,0,z),xDir=(1,0,0),normal=(0,0,1)),height)
def rib(poly,t_top=3,height=6):return extrusion(poly,cq.Plane(origin=(0,t_top,0),xDir=(1,0,0),normal=(0,-1,0)),height)
def spin(solid,angle):return solid.rotate((0,0,0),(0,0,1),angle)


def overlap(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if any(getattr(aa,c+'max')<=getattr(bb,c+'min')+1e-9 or getattr(bb,c+'max')<=getattr(aa,c+'min')+1e-9 for c in 'xyz'):return 0.
    val=abs(a.intersect(b).Volume());assert math.isfinite(val)
    return val


def sweep2(poly,dx=0,dy=0):
    pieces=[poly,translate(poly,xoff=dx,yoff=dy)]
    for ring in (poly.exterior,*poly.interiors):
        for p,q in zip(ring.coords,list(ring.coords)[1:]):
            cell=Polygon([p,q,(q[0]+dx,q[1]+dy),(p[0]+dx,p[1]+dy)])
            if cell.area>1e-10:pieces.append(cell)
    result=unary_union(pieces);assert result.is_valid and result.geom_type=='Polygon'
    return result


def matrix(solids):
    return {a+'|'+b:overlap(x,y) for (a,x),(b,y) in itertools.combinations(solids.items(),2)}


def base():
    p03=PARTS/'P03/variants/A_COMPACT_CLOSED';cheek=svg(p03/'P01-Y-mortise-study-v1.svg');yp=svg(p03/'P03.svg')
    stations=json.loads((p03/'mechanical-dimensions.json').read_text())['stations']
    out={'P03':plate(yp,407)}
    for leg,angle in enumerate((0,120,240),1):
        for n,t in enumerate((-7.5,13.5),1):out[f'L{leg}_P01_{n}']=spin(rib(cheek,t),angle)
        for s in stations:
            profile=translate(svg(PARTS/f"P02/variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
            out[f"L{leg}_{s['id']}"]=spin(plate(profile,s['z_mm']-3),angle)
    assert len(out)==19
    return out,cheek,stations


def y_first(base19,cheek,stations):
    fixed={'P03':base19['P03']};stages=[]
    for leg,angle in enumerate((0,120,240),1):
        seq=[('P01_1',rib(cheek,-7.5,46))]
        for s in stations:
            profile=translate(svg(PARTS/f"P02/variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
            seq.append((s['id'],plate(sweep2(profile,dy=40),s['z_mm']-3)))
        seq.append(('P01_2',rib(cheek,53.5,46)))
        for key,swept in seq:
            vals={n:overlap(spin(swept,angle),v) for n,v in fixed.items()}
            assert max(vals.values())<EPS,(leg,key,max(vals.values()))
            label=f'L{leg}_{key}';stages.append({'moving':label,'checks':len(vals),'max_mm3':max(vals.values())})
            fixed[label]=base19[label]
    assert len(fixed)==19 and sum(x['checks'] for x in stages)==171
    return {'moving_stages':len(stages),'continuous_checks':171,'maximum_overlap_mm3':max(s['max_mm3'] for s in stages)}


def bounds(solid):
    b=solid.BoundingBox();return np.array([[b.xmin,b.ymin,b.zmin],[b.xmax,b.ymax,b.zmax]])


def glb_audit(path,reference,poly):
    scene=trimesh.load(path,force='scene');assert len(scene.geometry)==27 and len(scene.graph.nodes_geometry)==27
    unmatched=dict(reference);maximum_bound=0;maximum_rel=0;rib_nodes=0
    for node in scene.graph.nodes_geometry:
        transform,key=scene.graph[node];m=scene.geometry[key].copy();m.apply_transform(transform)
        assert m.is_watertight and m.volume>0
        candidates=[]
        for name,s in unmatched.items():
            delta=float(np.max(np.abs(m.bounds*1000-bounds(s))))
            rel=abs(m.volume*1e9/s.Volume()-1)
            if delta<.001 and rel<1e-5:candidates.append((name,delta,rel))
        assert len(candidates)==1,(path,node,candidates)
        name,delta,rel=candidates[0];maximum_bound=max(maximum_bound,delta);maximum_rel=max(maximum_rel,rel)
        if name.startswith('P05_'):
            index=int(name.split('_')[1])-1;ang=math.radians(index*60);c,s=math.cos(ang),math.sin(ang)
            vertices=m.vertices*1000;rr=vertices[:,0]*c+vertices[:,1]*s;tt=-vertices[:,0]*s+vertices[:,1]*c
            assert max(abs(tt))<=3.001
            assert all(poly.buffer(.001).covers(Point(r,z)) for r,z in zip(rr,vertices[:,2]))
            rib_nodes+=1
        unmatched.pop(name)
    assert not unmatched and rib_nodes==6
    return {'nodes':27,'identical_master_rib_nodes':6,'units':'GLTF_metre','max_bound_delta_mm':maximum_bound,'max_relative_volume_delta':maximum_rel}


def selected_disks():
    folder=PARTS/'P04/variants/A'
    return {layer:svg(folder/f'{layer}.svg') for layer in ('P04L','P04U')}


def skin_envelope(disks):
    # The six current tongue apertures are real, but the P07B body remains an envelope.
    return Point(0,0).buffer(171,quad_segs=90).difference(unary_union([Polygon(h) for h in disks['P04L'].interiors]))


def actual27(base19,disks,profile):
    result={**base19,'P04L':plate(disks['P04L'],456),'P04U':plate(disks['P04U'],480)}
    result.update({f'P05_{i+1}':spin(rib(profile),angle) for i,angle in enumerate(range(0,360,60))})
    assert len(result)==27
    return result


def stage(name,moving,fixed):
    checks={label:overlap(moving,s) for label,s in fixed.items()}
    return {'moving':name,'continuous_checks':len(checks),'max_overlap_mm3':max(checks.values()),
            'positive_intersections_mm3':{k:v for k,v in checks.items() if v>EPS}}


def route(base19,disks,profile,vertical=False):
    fixed=dict(base19);stages=[];skin=skin_envelope(disks);real=actual27(base19,disks,profile)
    stages.append(stage('P07B_ENVELOPE',plate(skin,450,76),fixed));fixed['P07B_ENVELOPE']=plate(skin,450)
    stages.append(stage('P04L',plate(disks['P04L'],456,70),fixed));fixed['P04L']=real['P04L']
    if not vertical:
        stages.append(stage('P04U',plate(disks['P04U'],480,46),fixed));fixed['P04U']=real['P04U']
    for i,angle in enumerate(range(0,360,60),1):
        shape=spin(rib(sweep2(profile,dy=64) if vertical else sweep2(profile,dx=100)),angle)
        key=f'P05_{i}';stages.append(stage(key,shape,fixed));fixed[key]=real[key]
    if vertical:
        stages.append(stage('P04U',plate(disks['P04U'],480,46),fixed));fixed['P04U']=real['P04U']
    assert len(fixed)==28 and len(stages)==9
    assert sum(s['continuous_checks'] for s in stages)==207
    return {'mode':'VERTICAL_RIBS_BEFORE_U' if vertical else 'RADIAL_RIBS_AFTER_U','stages':stages,
            'continuous_checks':207,'max_overlap_mm3':max(s['max_overlap_mm3'] for s in stages)}


def displacement_controls(disks,profile):
    low,high=plate(disks['P04L'],456),plate(disks['P04U'],480)
    controls={}
    for name,dx,dy in [('outward100',100,0),('inward20',-20,0),('up6p4',0,6.4),('down6p4',0,-6.4)]:
        swept=rib(sweep2(profile,dx=dx,dy=dy))
        controls[name]={'P04L_mm3':overlap(swept,low),'P04U_mm3':overlap(swept,high)}
    return controls


def lock_access(real):
    top=plate(Point(0,0).buffer(171,quad_segs=90),494)
    results=[]
    for a in (0,120,240):
        for t in (-10.5,10.5):
            xy=rotate(Point(57,t),a,origin=(0,0));tool=plate(Point(xy.x,xy.y).buffer(2,quad_segs=32),488.5,31.5)
            values={k:overlap(tool,v) for k,v in real.items()}
            closed=overlap(tool,top)
            assert max(values.values())<EPS and closed>50
            results.append({'angle':a,'t':t,'assumed_tool_diameter_mm':4,'open_top_max_overlap_mm3':max(values.values()),'closed_top_overlap_mm3':closed})
    return results


def proposal_disks(name,selected):
    folder=P05/'proposals'/name;out={};evidence={}
    for layer in ('P04L','P04U'):
        path=folder/f'{layer}-v2-proposal.svg'
        if name=='C' and layer=='P04U':path=folder/'P04U-v1-reference.svg'
        out[layer],evidence[layer]=export_audit(path,'XY')
        assert out[layer].covers(Point(0,0)) and out[layer].geom_type=='Polygon'
        assert max(math.hypot(x,y) for x,y in out[layer].exterior.coords)<95.000001
        assert len(out[layer].interiors)==(6 if name=='C' and layer=='P04U' else 12)
        for tongue in selected[layer].interiors:
            assert any(Polygon(tongue).symmetric_difference(Polygon(h)).area<1e-7 for h in out[layer].interiors)
        if name=='C' and layer=='P04U':assert out[layer].symmetric_difference(selected[layer]).area<1e-7
    return out,evidence


def audit(output):
    result={'method':'Actual exported SVG/DXF -> independent CadQuery/OpenCASCADE material and exact boundary-prism translational sweeps; no implementation imports',
            'scope':'DESIGN_ONLY; proposal disks conditional/unapproved; P07/P08/tool envelope only','variants':{}}
    base19,cheek,stations=base();result['base19_y_first']=y_first(base19,cheek,stations)
    selected=selected_disks()
    for name in ('A','B','C'):
        folder=P05/'variants'/name;profile,entry=export_audit(folder/'P05.svg','r,z')
        assert len(profile.interiors)==0 and profile.area>2500
        assert abs(profile.bounds[0]-(81 if name=='A' else 82))<1e-5
        assert abs(profile.bounds[1]-456)<1e-5 and abs(profile.bounds[2]-169)<1e-5 and abs(profile.bounds[3]-494)<1e-5
        solid=rib(profile);assert abs(solid.Volume()-profile.area*6)<1e-4
        entry['finite_nominal_thickness_mm']=6;entry['identical_instances']=6
        entry['skin_boundary_contact_area_mm2']={str(z):profile.intersection(LineString([(0,z),(200,z)])).length*6 for z in (456,494)}
        chord=math.sqrt(95**2-3.2**2)
        entry['candidate_broadside_bond_reservation_mm2']={layer:2*profile.intersection(box(0,z,chord,z+6)).area for layer,z in (('P04L',456),('P04U',480))}
        if name=='C':
            pts=list(profile.exterior.coords)
            flat=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]) if abs(a[1]-479.6)<1e-7 and abs(b[1]-479.6)<1e-7)
            assert abs(flat-.4)<1e-7
            entry['small_upper_step_geometric_flat_area_mm2']=flat*6
            entry['small_step_strength_status']='NOT_RUN; finite flat is not a load rating'
        entry['nominal_outer_rim_gap_mm']=2
        entry['finite_tangent_min_circular_rim_gap_mm']=171-math.hypot(169,3)
        baseline=actual27(base19,selected,profile);pairs=matrix(baseline)
        assert len(pairs)==351
        entry['baseline27_static']={'body_count':27,'pairs':351,'max_overlap_mm3':max(pairs.values()),'positive_pairs_mm3':{k:v for k,v in pairs.items() if v>EPS}}
        baseline_route=route(base19,selected,profile)
        entry['baseline27_radial_route']=baseline_route
        if name=='B':
            assert max(pairs.values())>20 and baseline_route['max_overlap_mm3']>20
            baseline_glb=P05/'assembly/B-baseline-27-BLOCKED.glb'
            entry['baseline_status']='BLOCKED_WITH_SELECTED_P04_A'
        else:
            assert max(pairs.values())<EPS and baseline_route['max_overlap_mm3']<EPS
            baseline_glb=P05/f'assembly/{name}-baseline-27-DESIGN_ONLY.glb'
            entry['baseline_status']='PASS_CAD_FIT_AND_RADIAL_PATH; NO_POSITIVE_RADIAL_RETENTION'
        entry['baseline_GLB']=glb_audit(baseline_glb,baseline,profile)
        entry['baseline_radial_retention']=displacement_controls(selected,profile)
        working=baseline;work_disks=selected
        if name in ('B','C'):
            changed,cut_evidence=proposal_disks(name,selected);proposed=actual27(base19,changed,profile);pr_pairs=matrix(proposed)
            assert len(pr_pairs)==351 and max(pr_pairs.values())<EPS
            conditional=route(base19,changed,profile,vertical=True);assert conditional['max_overlap_mm3']<EPS
            restraints=displacement_controls(changed,profile)
            assert sum(restraints['outward100'].values())>1
            assert sum(restraints['up6p4'].values())>1 and sum(restraints['down6p4'].values())>1
            late=overlap(rib(sweep2(profile,dy=64)),proposed['P04U']);assert late>1
            entry['proposal_disks']=cut_evidence
            entry['proposal27_static']={'body_count':27,'pairs':351,'max_overlap_mm3':max(pr_pairs.values())}
            entry['proposal27_staged_route']=conditional
            entry['proposal_translation_controls']=restraints
            entry['rib_after_U_vertical_block_mm3']=late
            entry['proposal_GLB']=glb_audit(P05/f'assembly/{name}-proposed-27-CR_REQUIRED.glb',proposed,profile)
            entry['proposal_status']='PASS_CAD_CONDITIONAL; CR_REQUIRED; FIXED_DISK_TRANSLATIONAL_RESTRAINT_ONLY'
            working=proposed;work_disks=changed
        entry['lock_access_envelope']=lock_access(working)
        # Every negative is real material, not a hardcoded failure flag.
        low,high=plate(selected['P04L'],456),plate(selected['P04U'],480)
        fat=rib(profile,t_top=3.4,height=6.8)
        moved=spin(rib(profile),5)
        wall=plate(Point(0,0).buffer(175,quad_segs=90).difference(Point(0,0).buffer(171,quad_segs=90)),450,50)
        neg={'uncut38mm_against_U':overlap(rib(box(81,456,169,494)),high),
             'thickness6p8_against_L':overlap(fat,low),
             'rotated5deg_against_L':overlap(moved,low),
             'shifted_t1mm_against_L':overlap(rib(profile).translate((0,1,0)),low),
             'radial_insertion_after_wall':overlap(rib(sweep2(profile,dx=100)),wall)}
        assert all(v>1 for v in neg.values()),(name,neg)
        if name=='A':
            neg['upper_disk_after_rib_head']=overlap(plate(selected['P04U'],480,46),solid)
            assert neg['upper_disk_after_rib_head']>1
            assert sum(entry['baseline_radial_retention']['outward100'].values())<EPS
        if name=='C':assert sum(entry['baseline_radial_retention']['outward100'].values())<EPS
        entry['genuine_negative_controls_mm3']=neg
        result['variants'][name]=entry
        print(name,'351 baseline pairs /207 exact assembly checks /27-node GLB; conditional proposal and negative controls PASS',flush=True)
    protected_prefixes=['projects/CTB-01/specifications/CTB-000',*[f'projects/CTB-01/parts/P0{i}' for i in range(1,5)]]
    baseline_commit='6292a0e22c9aacade5aa7c7995332494aa8de005'
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',baseline_commit,*protected_prefixes],cwd=ROOT,text=True).splitlines()
    assert len(names)==259
    for name in names:
        source=subprocess.check_output(['git','show',baseline_commit+':'+name],cwd=ROOT)
        assert (ROOT/name).read_bytes()==source,name
    result['protected_upstream_files_unchanged']=len(names);result['protected_baseline_commit']=baseline_commit
    before=Path('/tmp/ctb005-independent-protected-before.json')
    if before.exists():
        recorded=json.loads(before.read_text())
        for name,sha in recorded.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
        result['protected_upstream_files_unchanged']=len(recorded)
    output.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('/tmp/ctb005-independent-occ-results.json'))
    audit(parser.parse_args().output)
