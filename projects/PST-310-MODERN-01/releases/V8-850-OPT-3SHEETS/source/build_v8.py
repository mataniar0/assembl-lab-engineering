#!/usr/bin/env python3
"""PST-310 V7 CAD: visually seamless, zero-through-cut 6mm upper disc.

Changes constrained to three upstream source geometries:
 - Upper Ø310 6mm disc full circle: no radial tabs, no rim edge scallops.
 - Each of six 6mm core ribs has its upper finger projections clipped flush at Z544.
 - Each of six 4mm rim segments has only its lower two tabs; upper tabs removed.

Bottom disc/leg/triangle/flat core unchanged from approved V6 CAD.
Top-to-core and top-to-rim joints are **glued butt contacts**, NOT interlocks.
Do not infer structural or wet-potted load strength from CAD validity.
"""
import math,pathlib,itertools,json,time
import numpy as np
import cadquery as cq
import trimesh
ROOT=pathlib.Path(__file__).resolve().parent
NS={'__file__':str(ROOT/'build_v6_reference.py'),'__name__':'pst_v6_definitions'}
exec((ROOT/'build_v6_reference.py').read_text().split('\nparts={')[0],NS)
V4=NS['NS'];PA=V4['PARAM'];

def top_disc_rim_fingers_only():
    # Same original V6 rim-mortise construction, without any of V6's 12 radial through-slots.
    vv=V4
    work=cq.Workplane('XY').circle(155).extrude(6).translate((0,0,544))
    for sector_idx in range(6):
        for local in PA['rim_tab_centers_deg']:
            mid=sector_idx*60+local
            half=(6+PA['rim_slot_angular_clearance_arclength_mm'])/153/(math.pi/180)
            cutter=vv['sector'](150.5,157,mid-half,mid+half,543.2,7.6,n=8)
            work=work.cut(cutter)
    s=work.val()
    assert s.isValid() and len(s.Solids())==1
    return s

def top_trim_tool():
    return cq.Workplane('XY').box(1000,1000,20,centered=(True,True,False)).translate((0,0,544)).val()
TRIM=top_trim_tool()

def rib_bottom_fingers_only(theta):
    r=V4['rib'](theta)
    s=r.cut(TRIM)
    assert s.isValid() and len(s.Solids())==1
    return s

def rim_bottom_fingers_only(i):
    r=V4['rim_segment'](i)
    s=r.cut(TRIM)
    assert s.isValid() and len(s.Solids())==1
    return s

parts={'TOP_DISC_D310_RIM_TABS_ONLY_6MM':top_disc_rim_fingers_only(),
       'BOTTOM_DISC_D310_6MM':V4['disk'](False)}
for i in range(6):parts[f'RIM_{i+1:02d}_BIRCH4_LOWER_TABS_ONLY']=rim_bottom_fingers_only(i)
for i,theta in enumerate(PA['rib_angles'],1):parts[f'CORE_RIB_{i:02d}_6MM']=rib_bottom_fingers_only(theta)
parts['CENTRAL_FLAT_6MM_SPIDER']=NS['flat_core']()
leg=NS['leg_v6']()
for i,angle in enumerate(PA['leg_angles'],1):
    for suffix,dy in [('A',-3),('B',3)]:
        parts[f'LEG_{i}_{suffix}_6MM']=leg.translate((0,dy,0)).rotate((0,0,0),(0,0,1),angle)
parts['LOWER_TRIANGLE_ONE_PIECE_6MM']=V4['lower_triangle']()
assert len(parts)==22
assert all(s.isValid() and len(s.Solids())==1 for s in parts.values())
# Positive contact areas for glue-only top interface (not pull-off force measurement)
top=parts['TOP_DISC_D310_RIM_TABS_ONLY_6MM'];topBottom=top.Faces()[0] # orientation uncertain; use intersect with support at underside
contact=[]
for k,s in parts.items():
    if k.startswith(('CORE_RIB_','RIM_')):
        # flat upper rib & rim face at Z544; each has nonzero end face for adhesive.
        fs=[f for f in s.Faces() if f.Center().z>543.9 and abs(f.normalAt().z)>.99]
        if not fs:raise RuntimeError('No adhesive joint top face for '+k)
        contact.append({'part':k,'top_contact_nominal_area_mm2':round(sum(f.Area() for f in fs),4)})
# Check volumetric interference on all pairs
vbad=[];bboxskipped=0;booleans=0;micro=[]
for (ka,a),(kb,b) in itertools.combinations(parts.items(),2):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if aa.xmax<bb.xmin-1e-5 or bb.xmax<aa.xmin-1e-5 or aa.ymax<bb.ymin-1e-5 or bb.ymax<aa.ymin-1e-5 or aa.zmax<bb.zmin-1e-5 or bb.zmax<aa.zmin-1e-5:
        bboxskipped+=1;continue
    booleans+=1;volume=a.intersect(b).Volume()
    if volume>.01:vbad.append([ka,kb,round(volume,6)])
    elif volume>1e-6:micro.append([ka,kb,round(volume,7)])
if vbad:raise RuntimeError('Nominal final-assembly collisions: '+repr(vbad[:15]))
# Four explicitly preserved V6 groups geometry numerical equality
assert len([k for k in parts if k.startswith('LEG_')])==6
assert top.Volume()<math.pi*155**2*6
upper_cap=cq.Assembly(name='PST_310_V8_RIM_FINGER_ONLY_GLUE_JOINT_DESIGN_ONLY')
scene=trimesh.Scene()
for k,s in parts.items():
    color=(.83,.65,.42) if k.startswith(('TOP_','BOTTOM_','LEG_')) else (.67,.46,.28) if k.startswith('RIM_') else (.70,.51,.31)
    upper_cap.add(s,name=k,color=cq.Color(*color))
    v,f=s.tessellate(.60,.13)
    mesh=trimesh.Trimesh(vertices=[p.toTuple() for p in v],faces=f,process=False)
    mesh.visual.face_colors=np.array([round(a*255) for a in color]+[255],dtype=np.uint8)
    scene.add_geometry(mesh,geom_name=k,node_name=k)
    cq.exporters.export(s,str(ROOT/'parts_STEP'/(k+'.step')))
upper_cap.save(str(ROOT/'cad'/'PST_310_V8_RIM_FINGER_ONLY_ASSEMBLY.step'))
scene.export(str(ROOT/'cad'/'PST_310_V8_RIM_FINGER_ONLY_ASSEMBLY.glb'))
upper_cap=cq.Assembly(name='PST_310_V8_HOLLOW_TOP')
for k,s in parts.items():
    if k.startswith(('TOP_','BOTTOM_','CORE_','RIM_','CENTRAL_')):upper_cap.add(s,name=k)
upper_cap.save(str(ROOT/'cad'/'PST_310_V8_HOLLOW_TOP.step'))
loaded=cq.importers.importStep(str(ROOT/'cad'/'PST_310_V8_RIM_FINGER_ONLY_ASSEMBLY.step')).solids().vals()
reloaded=trimesh.load(ROOT/'cad'/'PST_310_V8_RIM_FINGER_ONLY_ASSEMBLY.glb',force='scene')
assert len(loaded)==22 and all(s.isValid() for s in loaded)
assert len(reloaded.geometry)==22
qa={'project':'PST-310','version':'V7 smooth upper disk','status':'CAD_DESIGN_ONLY / GLUED_UPPER_JOINT_UNVERIFIED',
    'upper_disc_diameter_mm':310,'upper_disc_z_mm':[544,550],
    'upper_disc_face_wires':1,'upper_disc_holes':0,'upper_disc_edge_notches':12,
    'rib_top_fingers_removed':12,'rim_upper_tabs_retained':12,'bottom_mortises_preserved':True,
    'finished_assembly_solids_valid':22,'STEP_reimport_solids':22,'GLB_reimport_meshes':22,
    'pair_count':231,'bbox_skip_count':bboxskipped,'actual_occ_intersections':booleans,
    'collisions_over_0_01mm3':vbad,'micro_intersections':micro,
    'nominal_upper_glue_contacts':contact,
    'caveat':'Upper disc no longer mechanically retained by through mortises. No user-grip pull-off, glue bond/peel, moisture or pot loading proof. Do not lift the stand by the tabletop unless joint is physically qualified.'}
(ROOT/'qa'/'V8_CAD_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print('V8 CAD OK 22 bodies 231 pairs',bboxskipped,'culled',booleans,'OCC Booleans',len(contact),'glue interface pieces',flush=True)