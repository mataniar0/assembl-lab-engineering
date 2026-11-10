#!/usr/bin/env python3
"""PST-230 plant stand parametric CAD derived from PST-310 V8 geometry.
Fixed material 6/4 mm, fixed 550 mm height, horizontal geometry scaled 230/310;
joinery tangential clearances and material thickness preserved. DESIGN_ONLY.
"""
from __future__ import annotations
import itertools, pathlib, json, math, os, time
import numpy as np
import cadquery as cq
import trimesh
from shapely.geometry import Polygon, box, LineString
from shapely.affinity import scale as shp_scale
ROOT=pathlib.Path(__file__).resolve().parent
LEGACY=ROOT/'source'/'build_pst_310_v4.py'
# Reuse tested legacy V4 silhouette and bend-sector CAD primitives without executing final V4 export.
NS={'__file__':str(LEGACY),'__name__':'legacy_parametric'}
exec(LEGACY.read_text(encoding='utf8').split('parts={}')[0],NS)
Q=230.0/310
R=115.; RNEUTRAL=113.; OUTER_R=115.; INNER_R=111.
HEIGHT=550.; BOX_HEIGHT=60.; PLATE_T=6.; RIM_T=4.; MIN_CUT_GAP=1.0
P=NS['PARAM']; sector=NS['sector']; polar_box=NS['polar_box']
assert len(NS['new_outline'])>=20

# Preserve structure height, taper radius and material cross sections.
leg_outline=[(x*Q,490 if z==484 and i<12 else z) for i,(x,z) in enumerate(NS['new_outline'])]
leg_holes=[shp_scale(h,xfact=Q,yfact=1,origin=(0,0)) for h in NS['new_holes']]

def leg_blank():
    w=cq.Workplane('XZ').polyline(leg_outline).close().extrude(6).translate((0,3,0))
    for h in leg_holes:
        w=w.cut(cq.Workplane('XZ').polyline(list(h.exterior.coords)[:-1]).close().extrude(12).translate((0,6,0)))
    s=w.val();assert s.isValid() and len(s.Solids())==1
    return s

def disk(upper):
    z=544 if upper else 490
    w=cq.Workplane('XY').circle(R).extrude(6).translate((0,0,z))
    if not upper:
        for angle in P['rib_angles']:
            for a,b in P['rib_tab_spans']:
                # radial length scales, but 6mm tangential thickness and slot allowance DO NOT
                clearance=P['slot_side_allowance_mm']
                w=w.cut(polar_box((a+b)*Q/2,(b-a)*Q+2*clearance,6+2*clearance,angle,z-.8,7.6))
    # 2 perimeter rim finger mortises per each of 6 curved sectors.
    for idx in range(6):
        for local in P['rim_tab_centers_deg']:
            mid=idx*60+local
            half=(6+P['rim_slot_angular_clearance_arclength_mm'])/RNEUTRAL/(math.pi/180)
            w=w.cut(sector(INNER_R-.5,R+2,mid-half,mid+half,z-.8,7.6,n=10))
    if not upper:
        for angle in P['leg_angles']:
            for a,b in P['leg_tab_spans']:
                clearance=P['leg_slot_side_allowance_mm']
                w=w.cut(polar_box((a+b)*Q/2,(b-a)*Q+2*clearance,12+2*clearance,angle,z-.8,7.6))
    s=w.val();assert s.isValid() and len(s.Solids())==1
    return s

def rib_blank(angle):
    poly=box(44*Q,496,148.5*Q,544)
    for a,b in P['rib_tab_spans']:
        poly=poly.union(box(a*Q,490,b*Q,496))
    poly=poly.difference(box(43.5*Q,522,57.6*Q,552))
    assert poly.is_valid and poly.geom_type=='Polygon'
    s=cq.Workplane('XZ').polyline(list(poly.exterior.coords)[:-1]).close().extrude(6).translate((0,3,0)).val().rotate((0,0,0),(0,0,1),angle)
    assert s.isValid() and len(s.Solids())==1
    return s

def flat_core():
    w=cq.Workplane('XY').circle(71*Q).extrude(6).translate((0,0,522))
    for theta in P['rib_angles']:
        cutter=polar_box(58.5*Q,33*Q,6+2*P['slot_side_allowance_mm'],theta,521,8)
        w=w.cut(cutter)
    s=w.val();assert s.isValid() and len(s.Solids())==1
    return s

def triangle(R):
    return [(R*math.cos(a*math.pi/180),R*math.sin(a*math.pi/180)) for a in (0,120,240)]

def triangular_ring():
    w=cq.Workplane('XY').polyline(triangle(218*Q)).close().polyline(list(reversed(triangle(160*Q)))).close().extrude(6)
    for theta in P['leg_angles']:
        w=w.cut(polar_box(222.5*Q,93*Q,12.36,theta,-2,10))
    s=w.val().translate(cq.Vector(0,0,155))
    assert s.isValid() and len(s.Solids())==1
    return s

def rim_sector(i):
    start=i*60
    w=cq.Workplane('XY').newObject([sector(INNER_R,OUTER_R,start,start+60,496,48,n=100)])
    half=6/RNEUTRAL/(math.pi/180)
    for local in P['rim_tab_centers_deg']:
        mid=start+local
        bottom=sector(INNER_R,OUTER_R,mid-half,mid+half,490,6.1,n=12)
        top=sector(INNER_R,OUTER_R,mid-half,mid+half,543.9,6.1,n=12)
        w=w.union(bottom).union(top)
    s=w.val();assert s.isValid() and len(s.Solids())==1
    return s

parts={'TOP_DISC_D230_RIM_TABS_ONLY_6MM':disk(True),
       'BOTTOM_DISC_D230_6MM':disk(False)}
for i in range(6): parts[f'RIM_{i+1:02d}_BIRCH4_UPPER_LOWER_TABS']=rim_sector(i)
for i,angle in enumerate(P['rib_angles'],1):parts[f'CORE_RIB_{i:02d}_6MM']=rib_blank(angle)
parts['CENTRAL_FLAT_6MM_SPIDER']=flat_core()
leg=leg_blank()
for i,angle in enumerate(P['leg_angles'],1):
    for suffix,dy in [('A',-3),('B',3)]:
        parts[f'LEG_{i}_{suffix}_6MM']=leg.translate((0,dy,0)).rotate((0,0,0),(0,0,1),angle)
parts['LOWER_TRIANGLE_ONE_PIECE_6MM']=triangular_ring()
assert len(parts)==22
assert all(s.isValid() and len(s.Solids())==1 for s in parts.values())

# Static CAD Boolean collision QA at final mounting pose.
clashes=[]; bbox_skip=0; boo=0
for (na,a),(nb,b) in itertools.combinations(parts.items(),2):
    ba=a.BoundingBox();bb=b.BoundingBox()
    if ba.xmax<bb.xmin-1e-5 or bb.xmax<ba.xmin-1e-5 or ba.ymax<bb.ymin-1e-5 or bb.ymax<ba.ymin-1e-5 or ba.zmax<bb.zmin-1e-5 or bb.zmax<ba.zmin-1e-5:
        bbox_skip+=1;continue
    v=a.intersect(b).Volume();boo+=1
    if v>.01:clashes.append([na,nb,round(v,5)])
print('PST230 solids',len(parts),'checks',boo,'skip',bbox_skip,'clashes',len(clashes),clashes[:10],flush=True)
assert not clashes,clashes[:20]

# CAD data: assembly STEP and GLB; mounting coordinates in millimeters, no cutting tools modeled.
(ROOT/'cad').mkdir(parents=True,exist_ok=True)
assy=cq.Assembly(name='PST230_PLANT_STAND_DESIGN_ONLY')
visual=trimesh.Scene()
for name,s in parts.items():
    color=(.78,.57,.34) if ('LEG' in name or 'DISC' in name) else (.56,.38,.25) if name.startswith('RIM') else (.71,.50,.31)
    assy.add(s,name=name,color=cq.Color(*color))
    verts,faces=s.tessellate(0.9,0.16)
    mesh=trimesh.Trimesh(vertices=[v.toTuple() for v in verts],faces=faces,process=False)
    mesh.visual.face_colors=np.array([int(255*x) for x in color]+[255],dtype=np.uint8)
    visual.add_geometry(mesh,geom_name=name,node_name=name)
assyp=ROOT/'cad'/'PST_230_ASSEMBLY_DESIGN_ONLY.step';glbp=ROOT/'cad'/'PST_230_ASSEMBLY_DESIGN_ONLY.glb'
assy.save(str(assyp));visual.export(str(glbp))
assert len(cq.importers.importStep(str(assyp)).solids().vals())==22
assert len(trimesh.load(str(glbp),force='scene').geometry)==22
CAD_QA={'project':'PST-230','inspiration':'PST-310 V8-850 R2', 'status':'DESIGN_ONLY','top_diameter_mm':230,
 'height_mm':550,'top_structure_height_mm':60,'plate_thickness_mm':6,'rim_thickness_mm':4,
 'horizontal_scale_factor':Q,'actual_laser_kerf_mm':None,'actual_material_thickness_mm':None,
 'solids':len(parts),'checked_static_pairs':231,'booleans':boo,'bbox_culled':bbox_skip,
 'collisions_above_0_01_mm3':clashes,'step_reimported_solids':22,'glb_reimported_meshes':22,
 'known_unverified':['real material fit and laser kerf','flex rim seam closure and kerfs',
 'joint pullout / glue peel','tilt resistance of narrowed base at 550mm height','wet pot load',
 'cut instructions require competent supervision']}
(ROOT/'qa').mkdir(exist_ok=True)
(ROOT/'qa'/'CAD_QA.json').write_text(json.dumps(CAD_QA,ensure_ascii=False,indent=2))
print('CAD created',str(glbp),flush=True)