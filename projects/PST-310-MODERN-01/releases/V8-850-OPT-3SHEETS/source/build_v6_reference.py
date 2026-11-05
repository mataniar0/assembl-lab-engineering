#!/usr/bin/env python3
"""PST-310 V6 single-triangle laser-cut candidate; same approved 310/60/550 envelope.
Only physical kerf, bending, glue and load remain unverified; no human load test.
"""
import math,pathlib,itertools,json,time
import numpy as np
import cadquery as cq
import trimesh
ROOT=pathlib.Path(__file__).resolve().parent
NS={'__name__':'pst_v4_source_without_side_effects'}
exec((ROOT/'build_pst_310_v4.py').read_text().split('parts={}')[0],NS)
PARAM=NS['PARAM'];polyline=NS['new_outline'];holes=NS['new_holes']
# The old 6mm underside spider is REMOVED. Raising the leg bearing shoulder from Z484 to
# Z490 allows the wide top shoulder to bear immediately against underside of Z490..496 disc.
# Crucial: the two top fingers still project to Z496, so they enter ONLY one 6mm bottom plate.
V6_LEG_OUTLINE=[(x,490 if z==484 and i<12 else z) for i,(x,z) in enumerate(polyline)]

def leg_v6():
    w=cq.Workplane('XZ').polyline(V6_LEG_OUTLINE).close().extrude(6).translate((0,3,0))
    for hole in holes:
        w=w.cut(cq.Workplane('XZ').polyline(list(hole.exterior.coords)[:-1]).close().extrude(12).translate((0,6,0)))
    result=w.val(); assert result.isValid() and len(result.Solids())==1
    return result

def flat_core():
    w=cq.Workplane('XY').circle(71).extrude(6).translate((0,0,522))
    for theta in PARAM['rib_angles']:
        hole=cq.Workplane('XY').box(33,6.32,8,centered=(True,True,False)).translate((58.5,0,521)).rotate((0,0,0),(0,0,1),theta)
        w=w.cut(hole)
    result=w.val();assert result.isValid() and len(result.Solids())==1
    return result
parts={
 'TOP_DISC_D310_6MM':NS['disk'](True),
 'BOTTOM_DISC_D310_6MM':NS['disk'](False),
}
for i in range(6):parts[f'RIM_{i+1:02d}_4MM_CURVED_REFERENCE']=NS['rim_segment'](i)
for i,theta in enumerate(PARAM['rib_angles'],1):parts[f'CORE_RIB_{i:02d}_6MM']=NS['rib'](theta)
parts['CENTRAL_FLAT_6MM_SPIDER']=flat_core()
leg=leg_v6()
for i,theta in enumerate(PARAM['leg_angles'],1):
    for suffix,dy in [('A',-3),('B',3)]:
        parts[f'LEG_{i}_{suffix}_6MM']=leg.translate((0,dy,0)).rotate((0,0,0),(0,0,1),theta)
parts['LOWER_TRIANGLE_ONE_PIECE_6MM']=NS['lower_triangle']()
assert len(parts)==22,len(parts)
assert all(shape.isValid() and len(shape.Solids())==1 for shape in parts.values())

def pair_volume(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if any([aa.xmax<bb.xmin-.00001,bb.xmax<aa.xmin-.00001,
            aa.ymax<bb.ymin-.00001,bb.ymax<aa.ymin-.00001,
            aa.zmax<bb.zmin-.00001,bb.zmax<aa.zmin-.00001]):return 0.,False
    return a.intersect(b).Volume(),True

static_errors=[];broadphase=0;booleans=0;micro=[]
for (na,a),(nb,b) in itertools.combinations(parts.items(),2):
    v,actual=pair_volume(a,b)
    broadphase+=not actual;booleans+=actual
    if v>.01:static_errors.append([na,nb,round(v,5)])
    elif v>1e-6:micro.append([na,nb,round(v,7)])
if static_errors:raise RuntimeError(f'CAD final collision {static_errors[:20]}')
print('CAD validation:',len(parts),'solids',broadphase,'bounding-box disjoints',booleans,'Booleans',flush=True)

assembly=cq.Assembly(name='PST_310_V6_ONE_PIECE_TRIANGLE_NO_LOWER_SPIDER_DESIGN_ONLY')
visual=trimesh.Scene()
for name,s in parts.items():
    color=(.79,.59,.36) if ('LEG_' in name or 'DISC_' in name) else (.58,.40,.26) if name.startswith('RIM_') else (.71,.50,.31)
    assembly.add(s,name=name,color=cq.Color(*color))
    verts,faces=s.tessellate(.65,.15)
    mesh=trimesh.Trimesh(vertices=[v.toTuple() for v in verts],faces=faces,process=False)
    mesh.visual.face_colors=np.array([int(255*x) for x in color]+[255],dtype=np.uint8)
    visual.add_geometry(mesh,geom_name=name,node_name=name)
    cq.exporters.export(s,str(ROOT/'parts_STEP'/(name+'.step')))
assembly.save(str(ROOT/'cad'/'PST_310_V6_FULL_ONE_TRIANGLE_DESIGN_ONLY.step'))
visual.export(str(ROOT/'cad'/'PST_310_V6_FULL_ONE_TRIANGLE_DESIGN_ONLY.glb'))
top_assy=cq.Assembly(name='PST_310_V6_TOP_ASSEMBLY')
for k,s in parts.items():
    if k.startswith(('TOP_','BOTTOM_','CORE_RIB_','RIM_','CENTRAL_')):top_assy.add(s,name=k)
top_assy.save(str(ROOT/'cad'/'PST_310_V6_TOP_ONLY.step'))
frame_assy=cq.Assembly(name='PST_310_V6_FRAME_ONLY')
for k,s in parts.items():
    if k.startswith(('LEG_','LOWER_TRIANGLE_')):frame_assy.add(s,name=k)
frame_assy.save(str(ROOT/'cad'/'PST_310_V6_FRAME_ONLY.step'))
load=cq.importers.importStep(str(ROOT/'cad'/'PST_310_V6_FULL_ONE_TRIANGLE_DESIGN_ONLY.step')).solids().vals()
loadedglb=trimesh.load(ROOT/'cad'/'PST_310_V6_FULL_ONE_TRIANGLE_DESIGN_ONLY.glb',force='scene')
assert len(load)==22 and all(s.isValid() for s in load)
assert len(loadedglb.geometry)==22
qa={'project':'PST-310','version':'V6','status':'DESIGN_ONLY / CONTINUOUS_BEND_STRENGTH_UNVERIFIED',
    'material':{'structure_mm':6,'flex_wall_mm':4},'body_count':22,'original_v5_count':34,
    'part_reduction':12,'diameter_mm':310,'total_height_mm':550,'top_box_height_mm':60,
    'delta_from_v5':['replace three separate triangle sectors with ONE original unmodified 6mm triangular ring',
      'remove all nine 6mm laminated inter-corner bridge strips',
      'remove redundant circular 6mm underside leg spider',
      'raise three leg pair shoulders by 6mm to contact lower disc directly, while retaining 6mm through-tabs'],
    'solid_validity':22,'step_reimport_valid_solids':len(load),'glb_reimport_meshes':len(loadedglb.geometry),
    'checked_pairs':231,'bbox_disjoint':broadphase,'CAD_boolean_checked':booleans,
    'collisions_above_0_01mm3':static_errors,'micro_overlap_below_threshold':micro,
    'caveats':['No validated load rating or wet-pot test','Measured plywood thickness and laser kerf unavailable',
      'kerf-bent rim sectors are geometric proxies, flex and closure unproved','Physical adhesive/bearing joints unproved']}
(ROOT/'qa'/'V6_CAD_QA.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False))
print('STEP, GLB reimported',len(load),'bodies',flush=True)