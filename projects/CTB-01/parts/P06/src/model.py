"""Actual P06 ring pieces, six-cheek CR overlays, and whole-material assembly sweeps."""
import hashlib,importlib.util,itertools,json,math
from pathlib import Path
import numpy as np
from jsonschema import Draft202012Validator
from shapely.geometry import Point,Polygon,LineString,box
from shapely.geometry.polygon import orient
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
PART=Path(__file__).resolve().parents[1];PROJECT=PART.parents[1];ROOT=PROJECT.parents[1]
spec=importlib.util.spec_from_file_location('p05_reference',PROJECT/'parts/P05/src/model.py')
p05=importlib.util.module_from_spec(spec);spec.loader.exec_module(p05)
p04=p05.p04;p03=p05.p03;p02=p05.p02;paths=p05.paths;digest=p05.digest
CONCEPTS=('A','B','C')


def inputs():
 d=json.loads((PART/'src/design.json').read_text());Draft202012Validator(json.loads((PART/'src/design.schema.json').read_text())).validate(d)
 return (d,*p05.inputs())


def active_cheek(d3,u):return p03.cheek('A_COMPACT_CLOSED',d3,u)[0]


def sections(d,d3,u):
 face=active_cheek(d3,u);z0=d['ring_center_z_mm']-3;z1=z0+6
 samples=sorted(set(d['section_samples_z_mm']+[z0-.2,z1+.2]))
 out=[]
 for z in samples:
  s=face.intersection(LineString([[-100,z],[400,z]]));out.append({'z_mm':z,'inner_r_mm':s.bounds[0],'outer_r_mm':s.bounds[2]})
 end=[s for s in out if s['z_mm'] in (z0-.2,z1+.2)]
 lo=max(s['inner_r_mm'] for s in end);hi=min(s['outer_r_mm'] for s in end)
 # The core stays inside the smallest actual inner edge across the complete cutout band.
 return {'samples':out,'joint_common_r_mm':[lo,hi],'joint_center_r_mm':(lo+hi)/2,
         'core_outer_radius_mm':min(s['inner_r_mm'] for s in end)-d['core_clearance_from_cheek_inner_mm'],
         'z_mm':[z0,z1]}


def rounded(poly,r,d):
 coords=np.asarray(list(orient(poly,1).exterior.coords)[:-1]);o=p02.master.Outline(d['fillet_chord_tolerance_mm'])
 p02.master.rounded_polygon(o,coords,[r]*len(coords));return orient(Polygon(o.final()),1)


def full_ring(name,d,d3,u):
 sec=sections(d,d3,u);outer=sec['core_outer_radius_mm'];w=d[name]['band_width_mm'];joint=sec['joint_center_r_mm']
 if name=='C':raw=Point(0,0).buffer(outer,quad_segs=d['circle_segments']//4).difference(Point(0,0).buffer(outer-w,quad_segs=d['circle_segments']//4))
 else:
  radius=outer-w/2;vertices=[(radius*math.cos(math.radians(a)),radius*math.sin(math.radians(a))) for a in d['leg_angles_deg']]
  raw=LineString(vertices+[vertices[0]]).buffer(w/2,quad_segs=16,join_style=1)
 pieces=[raw];a=joint-d[name]['tab_radial_width_mm']/2;c=joint+d[name]['tab_radial_width_mm']/2
 for angle in d['leg_angles_deg']:
  arm=box(outer-w,-d['arm_width_mm']/2,c,d['arm_width_mm']/2)
  tab=box(a,-d[name]['tab_abs_t_mm'],c,d[name]['tab_abs_t_mm'])
  pieces.append(rotate(unary_union([arm,tab]),angle,origin=(0,0)))
 face=orient(unary_union(pieces),1)
 # Actual exterior convex fillets: opening removes material, preserves straight mating lands.
 radius=d['outer_fillet_radius_mm'];face=face.buffer(-radius,quad_segs=8).buffer(radius,quad_segs=8)
 if name=='C':
  half=d['C']['key_slot_r_width_mm']/2;t0,t1=d['C']['key_slot_t_range_mm'];holes=[]
  for angle in d['leg_angles_deg']:
   for side in (-1,1):
    h=p02.rounded_rect(joint-half,t0,joint+half,t1,.2)
    if side<0:h=rotate(h,180,origin=(joint,0))
    holes.append(rotate(h,angle,origin=(0,0)))
  face=face.difference(unary_union(holes))
 return face


def splice(d,d3,u,angle):
 sec=sections(d,d3,u);q=(sec['core_outer_radius_mm']-d['B']['band_width_mm']/2)/2
 neck=d['B']['joint_neck_width_mm']/2;head=d['B']['joint_head_width_mm']/2;depth=d['B']['joint_depth_mm']
 male=rounded(unary_union([box(q-neck,-.2,q+neck,4),box(q-head,2,q+head,depth)]),.4,d)
 return rotate(male,angle,origin=(0,0))


def stop_key(d,d3,u):
 joint=sections(d,d3,u)['joint_center_r_mm'];cfg=d['B'];a=joint+cfg['stop_head_r_offsets_mm'][0];c=joint+cfg['stop_head_r_offsets_mm'][1]
 z0=d['ring_center_z_mm']-3-.2;z1=d['ring_center_z_mm']+3+cfg['loading_lift_mm']+.2
 end=joint-d['B']['tab_radial_width_mm']/2-.2
 return rounded(unary_union([box(a,cfg['stop_head_z_mm'][0],c,cfg['stop_head_z_mm'][1]),box(joint+cfg['stop_stem_start_r_offset_mm'],z0,end,z1)]),cfg['stop_radius_mm'],d)


def vertical_key(d):
 cfg=d['C'];return rounded(unary_union([box(cfg['key_neck_t_mm'][0],cfg['key_neck_z_mm'][0],cfg['key_neck_t_mm'][1],cfg['key_neck_z_mm'][1]),box(cfg['key_head_t_mm'][0],cfg['key_head_z_mm'][0],cfg['key_head_t_mm'][1],cfg['key_head_z_mm'][1])]),cfg['key_radius_mm'],d)


def planar_parts(name,d,d3,u):
 if name!='B':return {f'P06{name}':full_ring(name,d,d3,u)}
 base=full_ring('B',d,d3,u);sector=Polygon([(0,0),(500,-500*math.sqrt(3)),(500,500*math.sqrt(3))])
 master=base.intersection(sector).union(splice(d,d3,u,60)).difference(splice(d,d3,u,-60).buffer(d['B']['joint_clearance_mm'],quad_segs=8))
 return {f'P06B{i+1}':rotate(master,a,origin=(0,0)) for i,a in enumerate(d['leg_angles_deg'])}


def cheek_overlay(name,d,d3,u):
 original=active_cheek(d3,u);joint=sections(d,d3,u)['joint_center_r_mm'];half=d[name]['tab_radial_width_mm']/2;a=d['slot_allowance_each_side_mm'];z=d['ring_center_z_mm'];h=3+a
 if name=='B':
  cut=unary_union([box(-1000,z-h,joint+half+a,z+3+d['B']['loading_lift_mm']+a),stop_key(d,d3,u).buffer(a,quad_segs=8)])
 else:cut=p02.rounded_rect(joint-half-a,z-h,joint+half+a,z+h,d['slot_corner_radius_mm'])
 return original.difference(cut),cut


def key_transform(solid,joint,side,angle):
 # Intrinsic (t,z) plate, extruded along local normal, becomes a vertical t-z key at r=joint.
 mapped=solid.transform([[0,-side,0,joint],[side,0,0,0],[0,0,1,0]])
 return p03.rotation(mapped,angle)


def ring_solids(name,d,d3,u):
 z=d['ring_center_z_mm']-3;out={k:p02.plate_solid(p,z,6) for k,p in planar_parts(name,d,d3,u).items()}
 joint=sections(d,d3,u)['joint_center_r_mm']
 for leg,angle in enumerate(d['leg_angles_deg'],1):
  for side in (-1,1):
   if name=='B':s=p03.rotation(p02.cheek_solid(stop_key(d,d3,u),side*10.5-3,6),angle)
   elif name=='C':s=key_transform(p02.cheek_solid(vertical_key(d),-3,6),joint,side,angle)
   else:continue
   out[f'P06{name}_K{leg}_{"N" if side<0 else "P"}']=s
 return out


def assembly(name,d,d5,d4,d3,u,b,overlay=True):
 out=p05.assembly('A',d5,d4,d3,u,b)
 if overlay:
  face,_=cheek_overlay(name,d,d3,u)
  for leg,angle in enumerate(d['leg_angles_deg'],1):
   for i,t in enumerate((-10.5,10.5),1):out[f'L{leg}_P01_{i}']=p03.rotation(p02.cheek_solid(face,t-3,6),angle)
 return {**out,**ring_solids(name,d,d3,u)}


def record(label,sweep,prior,start,role,end=None):return p04.step(label,sweep,prior,start,end or [0,0,0],role)


def late_paths(name,d,d5,d4,d3,u,b):
 allparts=assembly(name,d,d5,d4,d3,u,b);existing={k:s for k,s in allparts.items() if not k.startswith('P06')};steps=[];z=d['ring_center_z_mm']-3
 if name=='B':
  prior=dict(existing)
  for i,(key,p) in enumerate(planar_parts(name,d,d3,u).items()):
   angle=d['leg_angles_deg'][i];a=math.radians(angle);stroke=d['cheek_insertion_t_mm'];lift=d['B']['loading_lift_mm']
   raised=p02.plate_solid(p,z+lift,6)
   swept=p02.plate_solid(p02.swept_polygon(p,-stroke*math.sin(a),stroke*math.cos(a)),z+lift,6)
   steps.append(record(key+'_entry',swept,prior,[-stroke*math.sin(a),stroke*math.cos(a),lift],'REAL_SEGMENT',[0,0,lift]))
   swept=p02.plate_solid(p,z,6+lift)
   steps.append(record(key+'_lower',swept,prior,[0,0,lift],'REAL_SEGMENT'))
   prior[key]=allparts[key]
  for leg,angle in enumerate(d['leg_angles_deg'],1):
   for side in (-1,1):
    key=f'P06B_K{leg}_{"N" if side<0 else "P"}';t0=side*10.5-3;distance=side*d['cheek_insertion_t_mm']
    swept=p03.rotation(p02.cheek_solid(stop_key(d,d3,u),min(t0,t0+distance),6+abs(distance)),angle)
    steps.append(record(key,swept,prior,[-distance*math.sin(math.radians(angle)),distance*math.cos(math.radians(angle)),0],'REAL_WOOD_STOP'))
    prior[key]=allparts[key]
 else:
  p=next(iter(planar_parts(name,d,d3,u).values()))
  for axis in ('from_above','radial'):
   swept=p02.plate_solid(p,z,600-z) if axis=='from_above' else p02.plate_solid(p02.swept_polygon(p,60,0),z,6)
   steps.append(record('P06'+name+'_'+axis,swept,existing,[0,0,600-z] if axis=='from_above' else [60,0,0],'COUNTERFACTUAL_TESTED_ROUTE'))
 return {'method':'EXACT_TRANSLATION_SWEPT_SOLID','steps':steps,'maximum_intersection_mm3':max(s['maximum_intersection_mm3'] for s in steps),
         'status':'PASS_CAD_SPECIFIED_PATH' if max(s['maximum_intersection_mm3'] for s in steps)<1e-6 else 'BLOCKED','checks':sum(len(s['continuous_intersections']) for s in steps)}


def early_path(name,d,d5,d4,d3,u,b):
 allparts=assembly(name,d,d5,d4,d3,u,b);ringkey='P06'+name;prior={} if name=='B' else {ringkey:allparts[ringkey]};steps=[]
 y=p03.y_profile('A_COMPACT_CLOSED',d3);ystart=520;yz=407
 steps.append(record('P03',p02.plate_solid(y,yz,ystart+6-yz),prior,[0,0,ystart-yz],'REVIEWED_Y'))
 prior['P03']=allparts['P03'];face,_=cheek_overlay(name,d,d3,u);distance=d['cheek_insertion_t_mm']
 for leg,angle in enumerate(d['leg_angles_deg'],1):
  for key in ['P01_1','S1','S2','S3','S4','P01_2']:
   moving=f'L{leg}_{key}'
   if key.startswith('P01'):
    i=int(key[-1])-1;t=(-10.5,10.5)[i]-3;off=-distance if i==0 else distance
    swept=p03.rotation(p02.cheek_solid(face,min(t,t+off),6+distance),angle)
   else:
    station=next(s for s in p02.stations(u) if s['id']==key);p=translate(p02.spacer('B_THROUGH_ADHESIVE',station['part'],u,b),xoff=station['r_mm'])
    swept=p03.rotation(p02.plate_solid(p02.swept_polygon(p,0,distance),station['z_mm']-3,6),angle);off=distance
   steps.append(record(moving,swept,prior,[-off*math.sin(math.radians(angle)),off*math.cos(math.radians(angle)),0],'REVIEWED_BASE_WITH_CHEEK_CR'))
   prior[moving]=allparts[moving]
 if name=='C':
  joint=sections(d,d3,u)['joint_center_r_mm']
  for leg,angle in enumerate(d['leg_angles_deg'],1):
   for side in (-1,1):
    moving=f'P06C_K{leg}_{"N" if side<0 else "P"}';tz=p02.swept_polygon(vertical_key(d),0,d['key_vertical_stroke_mm'])
    swept=key_transform(p02.cheek_solid(tz,-3,6),joint,side,angle)
    steps.append(record(moving,swept,prior,[0,0,d['key_vertical_stroke_mm']],'REAL_WOOD_KEEPER'));prior[moving]=allparts[moving]
 # Continue the selected upper assembly without pretending skin envelope is an actual part.
 skin=p04.skin(d4,d3,u,b);s=p02.plate_solid(skin,450,6)
 steps.append(record('P07B_ENVELOPE',p04.lower_sweep(skin,450,520),prior,[0,0,70],'RESERVATION_NOT_BOM'));prior['P07B_ENVELOPE']=s
 for layer,z in d4['layers_z_mm'].items():
  p=p04.disk('A',layer,d4,d3,u,b);steps.append(record(layer,p04.lower_sweep(p,z[0],520),prior,[0,0,520-z[0]],'REVIEWED_DISK'));prior[layer]=allparts[layer]
 for i,angle in enumerate(d5['angles_deg'],1):
  key=f'P05_{i}';a=math.radians(angle);sweep=p05.sweep_rib('A',d5,dr=100,angle=angle)
  steps.append(record(key,sweep,prior,[100*math.cos(a),100*math.sin(a),0],'REVIEWED_P05'));prior[key]=allparts[key]
 worst=max(s['maximum_intersection_mm3'] for s in steps)
 return {'initial_state':('Y_FIRST without ring; P06B later' if name=='B' else 'single ring in external fixture at245 before Y; fixtures not modeled/BOM'),
         'steps':steps,'checks':sum(len(s['continuous_intersections']) for s in steps),'maximum_intersection_mm3':worst,
         'status':'PASS_CAD_SPECIFIED_PATH' if worst<1e-6 else 'BLOCKED'}


def support(d3,u):
 p=active_cheek(d3,u);line=p.intersection(LineString([[-100,0],[400,0]]));a,_,c,_=line.bounds
 patches=[rotate(box(a,t-3,c,t+3),angle,origin=(0,0)) for angle in (0,120,240) for t in (-10.5,10.5)]
 hull=unary_union(patches).convex_hull
 return {'foot_r_interval_mm':[a,c],'contact_area_each_cheek_mm2':(c-a)*6,'total_area_mm2':sum(p.area for p in patches),
         'centroid_radius_mm':(a+c)/2,'centroid_triangle_inradius_mm':(a+c)/4,'support_hull_paths_mm':paths(hull),
         'minimum_origin_to_hull_edge_mm':Point(0,0).distance(hull.exterior),'maximum_foot_radius_mm':max(math.hypot(x,y) for p in patches for x,y in p.exterior.coords),
         'top_radius_mm':175,'load_cases':None,'stability':'NOT_RUN_NO_TIP_OR_LOAD_RATING'}


def controls(name,d,d5,d4,d3,u,b):
 allparts=assembly(name,d,d5,d4,d3,u,b);rsolids={k:s for k,s in allparts.items() if k.startswith('P06')};cheeks={k:s for k,s in allparts.items() if 'P01' in k}
 sec=sections(d,d3,u);joint=sec['joint_center_r_mm'];z=sec['z_mm'][0]
 old=translate(p02.spacer('B_THROUGH_ADHESIVE','P02',u,b),xoff=joint);old=p02.plate_solid(old,242,6)
 current={k:s for k,s in allparts.items() if k.endswith('_S3')};s3hits=p04.checks(unary_manifold(rsolids.values()),current)
 primary=next(iter(planar_parts(name,d,d3,u).values()));thick=p02.plate_solid(primary,z,6.8)
 shifted=p02.plate_solid(translate(primary,xoff=2),z,6)
 wrongz=p02.plate_solid(primary,z+12,6)
 tilted=p02.plate_solid(primary,z,6).rotate([5,0,0])
 def hit(s,others):return max([0]+[c['volume_mm3'] for c in p04.checks(s,others)])
 # Isolate the ring/key coupling from Y/P02 so their constraints do not counterfeit a ring restraint.
 footface=cheek_overlay(name,d,d3,u)[0];t=7.5;cheek=p02.cheek_solid(footface,t,6)
 direction={}
 for axis,vector in [('radial_out',[4,0,0]),('cheek_out_t',[0,4,0])]:
  swept=p02.cheek_solid(p02.swept_polygon(footface,4,0),t,6) if axis=='radial_out' else p02.cheek_solid(footface,t,10)
  direction[axis]={'maximum_intersection_mm3':hit(swept,rsolids),'claim':'ring/key-only obstruction, fixtures and keeper ejection not certified'}
 keeper=[]
 if name=='C':
  joint=sec['joint_center_r_mm'];swept=key_transform(p02.cheek_solid(p02.swept_polygon(vertical_key(d),0,40),-3,6),joint,1,0)
  keeper=p04.checks(swept,{k:s for k,s in allparts.items() if k!='P06C_K1_P'})
 if name=='B':
  swept=p02.cheek_solid(stop_key(d,d3,u),7.5,46)
  keeper=p04.checks(swept,{k:s for k,s in allparts.items() if k!='P06B_K1_P'})
 return {'S3_at200_intersections':s3hits,'hypothetical_S3_at245_max_mm3':hit(old,rsolids),
         'thickness6p8_mm3':hit(thick,cheeks),'swapped_tab_displaced2mm_mm3':hit(shifted,cheeks),
         'incorrect_ring_z_mm3':hit(wrongz,cheeks),'out_of_plane5deg_mm3':hit(tilted,cheeks),
         'ring_only_restraint':direction,'keeper_ejection_intersections':keeper,
         'keeper_ejection_status':'FREE_OR_UNVERIFIED_NO_6DOF_LOCK' if keeper else 'NO_SEPARATE_KEEPER',
         'Y_vertical_gap_mm':407-max(s.bounding_box()[5] for s in rsolids.values()),
         'S3_vertical_gap_mm':min(s.bounding_box()[2] for s in rsolids.values())-203,
         'ring_slab_S3_gap_mm':z-203}


def unary_manifold(solids):
 iterator=iter(solids);out=next(iterator)
 for s in iterator:out=out+s
 return out
