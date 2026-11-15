#!/usr/bin/env python3
"""PST-310 Modern V4 parametric CAD; design-only mechanical interlocks.
Each wooden cut feature is built once and used to generate its mating feature.
Clearances are *nominal*: physical plywood, kerf, glue, bend and loading require tests.
"""
import math, itertools, json, pathlib, traceback, time
import cadquery as cq
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
import numpy as np
import trimesh
from cadquery import importers
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=pathlib.Path('/mnt/data/PST_310_MODERN_V4_JOINERY')
ROOT.mkdir(parents=True,exist_ok=True)
(ROOT/'parts_STEP').mkdir(exist_ok=True)
(ROOT/'previews').mkdir(exist_ok=True)
PARAM=dict(disk_diameter=310,total_h=550,box_h=60,plate_t=6,
    core_h=48,rim_t=4,leg_lam_t=6,leg_laminations=2,leg_angles=[0,120,240],
    rib_angles=[30,90,150,210,270,330],rim_segments=6,leg_tab_spans=[[91,110],[121,140]],
    rib_tab_spans=[[69,89],[112,132]],rib_t=6,
    rim_tab_centers_deg=[12,48],rim_tab_length_arclength=12,
    slot_side_allowance_mm=.16,leg_slot_side_allowance_mm=.18,
    rim_slot_angular_clearance_arclength_mm=.25,
    top_z=[544,550],bottom_z=[490,496],spider_z=[484,490],
    core_z=[496,544],frame_z=[155,161],actual_kerf='UNMEASURED',
    material_actual_thickness='UNMEASURED',status='DESIGN_ONLY')
DEG=math.pi/180

def sector(r1,r2,ang1,ang2,z,h,n=90):
    a=np.linspace(ang1*DEG,ang2*DEG,n+1)
    polygon=[(r2*math.cos(t),r2*math.sin(t)) for t in a]+[(r1*math.cos(t),r1*math.sin(t)) for t in a[::-1]]
    s=cq.Workplane('XY').polyline(polygon).close().extrude(h).val().translate(cq.Vector(0,0,z))
    assert s.isValid() and len(s.Solids())==1
    return s

# leg design silhouette from approved V2 and recast V3; just extend two fingers +6mm.
outline=[(61,538),(91,538),(91,544),(110,544),(110,538),(121,538),
 (121,544),(140,544),(140,538),(154,538), (155,518),(149,492),
 (163,458),(165,437),(170,389),(186,312),(202,227),(215,154),(234,0),
 (184,0),(190,64),(189,112),(185,141),(157,141),(157,155),(184,155),
 (178,195),(168,248),(156,306),(138,382),(117,435),(93,469),(72,502)]
def zmap(z):
    if z==544:return 496  # NEW leg upper fingers penetrate lower disc, not just spider
    if z<=161:return z
    return 161+(z-161)*(484-161)/(538-161) if z<=538 else z-54
new_outline=[(x,zmap(z)) for x,z in outline]
base_outline=Polygon(outline)
raw_opening=Polygon([(136,407),(144,431),(158,410),(177,332),(197,235),(207,190),
 (194,188),(182,210),(170,261),(153,334),(132,386)])
opening=raw_opening.intersection(base_outline.buffer(-9))
slit1=LineString([(207.8,51),(207.5,83)]).buffer(2.1,cap_style=1,resolution=10)
slit2=LineString([(204.6,112),(204.5,142)]).buffer(2.1,cap_style=1,resolution=10)
def rescale(poly):return Polygon([(x,zmap(z)) for x,z in poly.exterior.coords[:-1]])
new_holes=[rescale(p) for p in [opening,slit1,slit2]]
assert Polygon(new_outline).is_valid

def leg_lam():
    w=cq.Workplane('XZ').polyline(new_outline).close().extrude(6).translate((0,3,0))
    for h in new_holes:
        w=w.cut(cq.Workplane('XZ').polyline(list(h.exterior.coords)[:-1]).close().extrude(12).translate((0,6,0)))
    s=w.val();assert s.isValid() and len(s.Solids())==1
    return s

# Cut the two NEW 310mm disks, including actual through finger slots and rim edge scallops.
# Disk cutter shapes are the same parametric bounds that define matching parts.
def polar_box(center_r,radial_len,tangent_len,angle,z,height):
    return (cq.Workplane('XY').box(radial_len,tangent_len,height,centered=(True,True,False))
      .translate((center_r,0,z)).rotate((0,0,0),(0,0,1),angle).val())

def disk(upper):
    z=544 if upper else 490
    work=cq.Workplane('XY').circle(155).extrude(6).translate((0,0,z))
    # 6 ribs x 2 fingers per plate; clearance from structural rib finger 6mm thick.
    for angle in PARAM['rib_angles']:
        for a,b in PARAM['rib_tab_spans']:
            clearance=PARAM['slot_side_allowance_mm']
            w=polar_box((a+b)/2,(b-a)+2*clearance,6+2*clearance,angle,z-.8,7.6)
            work=work.cut(w)
    # 6 sectors x 2 matching notched perimeter openings for flexible rim tabs.
    for sector_idx in range(6):
        for local in PARAM['rim_tab_centers_deg']:
            mid=sector_idx*60+local
            half=(6+PARAM['rim_slot_angular_clearance_arclength_mm'])/153/DEG
            cutter=sector(150.5,157,mid-half,mid+half,z-.8,7.6,n=8)
            work=work.cut(cutter)
    # the 6 pre-existing leg tab positions now penetrate through the lower 6mm plate.
    if not upper:
        for angle in PARAM['leg_angles']:
            for a,b in PARAM['leg_tab_spans']:
                clear=PARAM['leg_slot_side_allowance_mm']
                work=work.cut(polar_box((a+b)/2,b-a+2*clear,12+2*clear,angle,z-.8,7.6))
    s=work.val();assert s.isValid() and len(s.Solids())==1
    return s

# The six radial vertical ribs, each with two top and two bottom fingers.
# A mating vertical lap slot at the inner edge connects to the central annulus.
def rib_profile():
    bulk=box(44,496,148.5,544)
    for a,b in PARAM['rib_tab_spans']:
        bulk=bulk.union(box(a,490,b,496)).union(box(a,544,b,550))
    # top-open notch / half lap, ring catches below its upper half.
    bulk=bulk.difference(box(43.5,522,57.6,552))
    assert bulk.is_valid and bulk.geom_type=='Polygon'
    return bulk
rib_poly=rib_profile()
def rib(angle):
    w=cq.Workplane('XZ').polyline(list(rib_poly.exterior.coords)[:-1]).close().extrude(6).translate((0,3,0))
    s=w.val().rotate((0,0,0),(0,0,1),angle)
    assert s.isValid() and len(s.Solids())==1
    return s

# Annular inner frame with matching bottom-open slots. Ring single piece continuous in upper half.
def central_ring():
    work=cq.Workplane('XY').circle(57).circle(44).extrude(48).translate((0,0,496))
    for angle in PARAM['rib_angles']:
        cutter=polar_box(50.5,19,6+2*PARAM['slot_side_allowance_mm'],angle,495.5,27)
        work=work.cut(cutter)
    s=work.val();assert s.isValid() and len(s.Solids())==1
    return s

# Lower spider: existing functional design with 6 slots matching the legs.
def spider():
    w=cq.Workplane('XY').circle(149).circle(129).extrude(6)
    w=w.union(cq.Workplane('XY').circle(27).extrude(6))
    for a in PARAM['leg_angles']:
        w=w.union(cq.Workplane('XY').box(139,32,6,centered=(True,True,False)).translate((78,0,0)).rotate((0,0,0),(0,0,1),a))
    for a in PARAM['leg_angles']:
        for x1,x2 in PARAM['leg_tab_spans']:
            c=.18
            w=w.cut(polar_box((x1+x2)/2,x2-x1+2*c,12+2*c,a,-1,8))
    s=w.val().translate(cq.Vector(0,0,484));assert s.isValid() and len(s.Solids())==1
    return s

def triangle(R):
    return [(R*math.cos(a*DEG),R*math.sin(a*DEG)) for a in (0,120,240)]
def lower_triangle():
    w=cq.Workplane('XY').polyline(triangle(218)).close().polyline(list(reversed(triangle(160)))).close().extrude(6)
    for a in PARAM['leg_angles']:
        w=w.cut(polar_box(222.5,93,12.36,a,-2,10))
    s=w.val().translate(cq.Vector(0,0,155));assert s.isValid() and len(s.Solids())==1
    return s

def edge_beam(i):
    verts=triangle(218);a=verts[i];b=verts[(i+1)%3];dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
    nx=-dy/L;ny=dx/L;t1=.17;t2=.83;off=15
    p1=(a[0]+t1*dx+off*nx,a[1]+t1*dy+off*ny)
    p2=(a[0]+t2*dx+off*nx,a[1]+t2*dy+off*ny)
    poly=[(p1[0]-3*nx,p1[1]-3*ny),(p2[0]-3*nx,p2[1]-3*ny),
          (p2[0]+3*nx,p2[1]+3*ny),(p1[0]+3*nx,p1[1]+3*ny)]
    s=cq.Workplane('XY').polyline(poly).close().extrude(19).val().translate(cq.Vector(0,0,136))
    assert s.isValid() and len(s.Solids())==1
    return s

def rim_segment(i):
    a=i*60
    base=sector(151,155,a,a+60,496,48,n=100)
    w=cq.Workplane('XY').newObject([base])
    half=6/153/DEG  # 12 mm long finger along perimeter
    for local in PARAM['rim_tab_centers_deg']:
        mid=a+local
        bottom=sector(151,155,mid-half,mid+half,490,6.1,n=10)
        top=sector(151,155,mid-half,mid+half,543.9,6.1,n=10)
        w=w.union(bottom).union(top)
    s=w.val();assert s.isValid() and len(s.Solids())==1
    return s

parts={}
parts['01_UPPER_D310_DISC_FINGER_6MM']=disk(True)
parts['02_LOWER_D310_DISC_FINGER_LEG_6MM']=disk(False)
for j in range(6):parts[f'03_RIM_SECTOR_{j+1:02d}_CURVED_4MM']=rim_segment(j)
for j,a in enumerate(PARAM['rib_angles'],1):parts[f'04_CORE_RIB_{j:02d}_FINGER_6MM']=rib(a)
parts['05_CORE_CROSS_LAP_RING_6MM']=central_ring()
parts['06_LOWER_LEG_SPIDER_6MM']=spider()
leg=leg_lam()
for j,a in enumerate(PARAM['leg_angles'],1):
    for suffix,ty in [('A',-3),('B',3)]:
        parts[f'07_LEG_{j}_{suffix}_EXTENDED_FINGER_6MM']=leg.translate((0,ty,0)).rotate((0,0,0),(0,0,1),a)
parts['08_LOWER_TRIANGLE_BRACE_6MM']=lower_triangle()
for j in range(3):parts[f'09_SIDE_EDGE_BEAM_{j+1}_6MM']=edge_beam(j)
print('V4 solids constructed',len(parts),flush=True)
assert len(parts)==26
for name,s in parts.items():
    if not(s.isValid() and len(s.Solids())==1):raise Exception('invalid '+name)

# Validate all 325 final-state volumes in matching assembly pose.
collisions=[];pairchecks=0;zeroed=0;micro=[];time_start=time.time()
for (na,a),(nb,b) in itertools.combinations(parts.items(),2):
    pairchecks+=1
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if (aa.xmax<bb.xmin-.0001 or bb.xmax<aa.xmin-.0001 or aa.ymax<bb.ymin-.0001 or bb.ymax<aa.ymin-.0001 or aa.zmax<bb.zmin-.0001 or bb.zmax<aa.zmin-.0001):
        zeroed+=1;continue
    overlap=a.intersect(b).Volume()
    if overlap>0.005:collisions.append((na,nb,round(overlap,5)))
    elif overlap>.000001:micro.append((na,nb,round(overlap,6)))
print('pairs',pairchecks,'skipped',zeroed,'collisions',len(collisions),'micro',len(micro),'timing',time.time()-time_start,flush=True)
if collisions:
    (ROOT/'COLLISIONS.json').write_text(json.dumps(collisions,indent=2));raise RuntimeError('Actual collisions found '+str(collisions[:10]))

# Kinematic collision sampling (bounded 1D, not full 6DOF path guarantee).
def pathqa(moving,stationary,offsets):
    results=[]
    for dz in offsets:
        s=moving.translate(cq.Vector(0,0,dz))
        hits=[]
        for n,other in stationary.items():
            a,b=s.BoundingBox(),other.BoundingBox()
            if (a.xmax<b.xmin or b.xmax<a.xmin or a.ymax<b.ymin or b.ymax<a.ymin or a.zmax<b.zmin or b.zmax<a.zmin):continue
            v=s.intersect(other).Volume()
            if v>.005:hits.append([n,round(v,4)])
        results.append({'z_offset_mm':round(dz,3),'collisions':hits})
    return results
# Top plate sliding down onto fixed rib fingers: fixture already includes bottom plate, ring, core ribs.
upper_path=pathqa(parts['01_UPPER_D310_DISC_FINGER_6MM'],
                  {k:v for k,v in parts.items() if k.startswith(('04_','05_'))},np.linspace(30,0,16))
# Central ring lowered into six half-lap rib seats from above.
ring_path=pathqa(parts['05_CORE_CROSS_LAP_RING_6MM'],
                 {k:v for k,v in parts.items() if k.startswith('04_')},np.linspace(60,0,31))
print('Path checks upper',sum(len(r['collisions']) for r in upper_path),'ring',sum(len(r['collisions']) for r in ring_path),flush=True)

# Save actual BREP CAD solids, not just triangulated approximations.
assembly=cq.Assembly(name='PST_310_MODERN_V4_JOINTED_DESIGN_ONLY')
def color(name):
    if 'DISC' in name:return(226,193,142,255)
    if 'RIM' in name:return(183,128,85,255)
    if 'RIB' in name:return(181,115,72,255)
    if 'RING' in name:return(167,103,67,255)
    if 'SPIDER' in name:return(184,136,89,255)
    if 'LEG' in name:return(218,167,103,255)
    return (181,130,87,255)
scene=trimesh.Scene();meshes={}
for name,s in parts.items():
    rgba=color(name)
    assembly.add(s,name=name,color=cq.Color(*[k/255 for k in rgba[:3]]))
    vs,fs=s.tessellate(1.0,.16)
    m=trimesh.Trimesh(vertices=np.array([v.toTuple() for v in vs]),faces=np.array(fs),process=False)
    m.visual.face_colors=np.array(rgba,dtype=np.uint8)
    meshes[name]=m;scene.add_geometry(m,geom_name=name,node_name=name)
    cq.exporters.export(s,str(ROOT/'parts_STEP'/(name+'.step')))
step=ROOT/'PST_310_MODERN_V4_FINGER_JOINTED_FULL.step';glb=ROOT/'PST_310_MODERN_V4_FINGER_JOINTED_FULL.glb'
assembly.save(str(step));scene.export(str(glb))
frame=cq.Assembly(name='PST_310_MODERN_V4_FRAME_ONLY')
for name,s in parts.items():
    if name.startswith(('06_','07_','08_','09_')):frame.add(s,name=name)
frame.save(str(ROOT/'PST_310_MODERN_V4_FRAME_ONLY.step'))
inner=cq.Assembly(name='PST_310_MODERN_V4_JOINTED_TOP_ONLY')
for name,s in parts.items():
    if name.startswith(('01_','02_','03_','04_','05_')):inner.add(s,name=name)
inner.save(str(ROOT/'PST_310_MODERN_V4_HOLLOW_TOP_ONLY.step'))
# exploded geometry with top, rim, ring, ribs separated for conceptual inspection
exploded=trimesh.Scene()
for name,m in meshes.items():
    x=m.copy()
    if name.startswith('01_'):x.apply_translation([0,0,130])
    elif name.startswith('02_'):x.apply_translation([0,0,-45])
    elif name.startswith('03_'):x.apply_translation([0,0,53])
    elif name.startswith('04_'):x.apply_translation([0,0,78])
    elif name.startswith('05_'):x.apply_translation([0,0,103])
    elif name.startswith('06_'):x.apply_translation([0,0,-63])
    exploded.add_geometry(x,geom_name=name,node_name=name)
exploded.export(str(ROOT/'PST_310_MODERN_V4_EXPLODED.glb'))
loaded=importers.importStep(str(step)).solids().vals()
glbloaded=trimesh.load(str(glb),force='scene')
assert len(loaded)==len(parts) and all(s.isValid() for s in loaded)
assert len(glbloaded.geometry)==len(parts)
qa={'version':'PST-310 V4 FINGER JOINT ENGINEERING', 'status':'DESIGN_ONLY / NOT PRODUCTION APPROVED',
 'frozen_nominal_parameters':PARAM,
 'part_count':len(parts),'part_ids':list(parts),'STEP_reimport_valid':len(loaded),
 'GLB_reimport_meshes':len(glbloaded.geometry),'solid_pairs_checked':pairchecks,
 'broadphase_disjoint_pairs':zeroed,'intersection_volumes_gt_0_005':collisions,'micro_volumes':micro,
 'ring_sweep_z_test':ring_path,'top_disc_sweep_z_test':upper_path,
 'engineering_connections':{
 'upper_disc_to_radial_ribs':'12 through finger-mortises, nominal +0.16mm per side',
 'lower_disc_to_radial_ribs':'12 through finger-mortises, nominal +0.16mm per side',
 'lower_disc_to_legs':'6 through finger-mortises matching 3 laminated leg top ends, shifted outer tab from r129–148 to r121–140, preserving outer edge ligament',
 'core_ring_to_ribs':'6 complementary vertical half-lap joints with 0.16mm lateral clearance',
 'outer_rim_to_discs':'12 angular edge scallops per plate for 2x6 flexible rim fingers',
 'spider_to_leg':'6 mating through-slots inherited V3, slots 0.18mm per side',
 'lower_triangle_to_leg':'3 radial open slots and leg bearing ledges V3 held unchanged'},
 'rim_nominal_sector_developed_mm':(math.pi*153/3),
 'rim_bending_kerf_open_lines':'NOT YET REPRESENTED IN STEP; 4mm spacing candidate only',
 'unverified':['actual plywood thickness and laser kerf','radial insertion of all six curved rim sectors','unrestrained bending strength and springback','lower leg and brace continuous assembly route','mass of plant + wet soil + water','wood grain, adhesive retention and safety stability','environmental wet sealing'],
 'release_decision':'NO CUTTING / NOT FOR PRODUCTION'}
(ROOT/'QA_REPORT.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False),encoding='utf-8')
print('EXPORTS PASS',step.stat().st_size,'reimport',len(loaded),'full',glb.stat().st_size,flush=True)