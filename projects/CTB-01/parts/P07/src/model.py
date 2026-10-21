"""Finite experimental flat/bent P07 material; selected pre-ring27 is never modified."""
import hashlib,importlib.util,itertools,json,math
from functools import lru_cache
from pathlib import Path
import numpy as np
from jsonschema import Draft202012Validator
from shapely.geometry import Point,Polygon,LineString,box
from shapely.geometry.polygon import orient
from shapely.affinity import rotate,translate
from shapely.ops import unary_union,transform
PART=Path(__file__).resolve().parents[1];PROJECT=PART.parents[1];ROOT=PROJECT.parents[1]
spec=importlib.util.spec_from_file_location('p05_reference',PROJECT/'parts/P05/src/model.py');p05=importlib.util.module_from_spec(spec);spec.loader.exec_module(p05)
p04=p05.p04;p03=p05.p03;p02=p05.p02;paths=p05.paths;digest=p05.digest;CONCEPTS=('A','B','C')
def inputs():
 d=json.loads((PART/'src/design.json').read_text());Draft202012Validator(json.loads((PART/'src/design.schema.json').read_text())).validate(d)
 return d,*p05.inputs()
def circle(r,d):return p04.circle(r,d)
def skin(name,layer,d,d4,d3,u,b):
 face=circle(d['skin_radius_mm'],d)
 if name=='C':
  tabs=[rotate(box(d['C']['tab_inner_r_mm'],-4,175,4),a,origin=(0,0)) for a in d['C']['tab_angles_deg']]
  face=unary_union([face,*tabs]).intersection(circle(d['outer_radius_mm'],d))
 if layer=='P07B':face=face.difference(unary_union(p04.tongue_slots(d4,d3,u,b)))
 if name=='C':face=face.simplify(1e-9,preserve_topology=True)
 return orient(face,1)
def circumference(d):return 2*math.pi*d['neutral_radius_hypothesis_mm']
def tab_centres(name,i,d):
 if name!='C':return []
 origin=math.radians(d['seam_phase_deg']+i*360/d[name]['segments']);r=d['neutral_radius_hypothesis_mm'];length=circumference(d)/d[name]['segments']
 return sorted(s for a in d['C']['tab_angles_deg'] for s in [((math.radians(a)-origin)%(2*math.pi))*r] if -.01<=s<=length+.01)
def flat_profile(name,i,d,kerfs=True):
 length=circumference(d)/d[name]['segments'];gap=d['seam_gap_mm']/2
 if name=='B':
  boundaries=[0,*d['B']['seam_steps_z_mm'],50]
  face=unary_union([box(off+gap,a,length+off-gap,c) for off,a,c in zip(d['B']['seam_offsets_mm'],boundaries,boundaries[1:])])
 else:face=box(gap,0,length-gap,50)
 cuts=[];tabcentres=tab_centres(name,i,d);tabhalf=d['neutral_radius_hypothesis_mm']*math.asin((4+.2)/171)
 if name=='C':
  for s in tabcentres:
   cuts.extend([box(s-tabhalf,0,s+tabhalf,6.2),box(s-tabhalf,43.8,s+tabhalf,50)])
 if kerfs:
  for k,s in enumerate(np.arange(d['seam_keepout_mm']+8,length-d['seam_keepout_mm']-8,d['kerf_pitch_hypothesis_mm'])):
   if any(abs(s-c)<tabhalf+d['C']['kerf_to_tab_keepout_mm']+.4 for c in tabcentres):continue
   if name=='A':lo,hi=d['A']['kerf_z_ranges_mm'][0]
   else:lo,hi=d[name]['kerf_z_ranges_mm'][k%2]
   cuts.append(box(s-.4,lo,s+.4,hi))
 return orient(face.difference(unary_union(cuts)),1)
def sheet_profile(face):
 # Flat axes are (s,height); laser portrait axes are (height,s), still true mm.
 return orient(transform(lambda s,h:(h,s),face),1)
def horizontal_intervals(face,z):
 cut=face.intersection(LineString([[-200,z],[1500,z]]));geoms=[cut] if cut.geom_type=='LineString' else list(cut.geoms) if hasattr(cut,'geoms') else []
 return [[g.bounds[0],g.bounds[2]] for g in geoms if g.geom_type=='LineString' and g.length>1e-8]
def slab_intervals(face):
 z=sorted(set(round(float(y),9) for ring in [face.exterior,*face.interiors] for _,y in ring.coords))
 return [{'height_interval_mm':[a,c],'s_intervals_mm':horizontal_intervals(face,(a+c)/2)} for a,c in zip(z,z[1:]) if c-a>1e-8]
def sector(a,c,d):
 if c-a<=1e-10:return Polygon()
 deg0=math.degrees(a);deg1=math.degrees(c);angles=np.linspace(a,c,max(2,math.ceil((deg1-deg0)/20)+1))
 wedge=Polygon([(0,0),*[(1000*math.cos(t),1000*math.sin(t)) for t in angles]])
 return circle(175,d).difference(circle(171,d)).intersection(wedge)
_SLABS={}
def bent_slabs(name,i,d,kerfs=True):
 key=(name,i,json.dumps(d,sort_keys=True),kerfs)
 if key not in _SLABS:_SLABS[key]=_make_bent_slabs(name,i,d,kerfs)
 return _SLABS[key]
def _make_bent_slabs(name,i,d,kerfs=True):
 face=flat_profile(name,i,d,kerfs);r=d['neutral_radius_hypothesis_mm'];phase=math.radians(d['seam_phase_deg']+i*360/d[name]['segments']);out=[]
 for slab in slab_intervals(face):
  xy=unary_union([sector(phase+a/r,phase+c/r,d) for a,c in slab['s_intervals_mm']]);out.append((slab['height_interval_mm'],xy))
 return out
def polygons(face):return [face] if face.geom_type=='Polygon' else [p for p in face.geoms if p.geom_type=='Polygon']
def union_solids(solids):
 solids=list(solids)
 if not solids:return p02.m.Manifold()
 return p02.m.Manifold.batch_boolean(solids,p02.m.OpType.Add)
def extrude_multi(face,z,height):return union_solids(p02.plate_solid(p,z,height) for p in polygons(face) if p.area>1e-10)
_SOLIDS={}
def bent_solid(name,i,d,dz_sweep=0,radial_sweep=0,kerfs=True):
 key=(name,i,json.dumps(d,sort_keys=True),dz_sweep,radial_sweep,kerfs)
 if key not in _SOLIDS:_SOLIDS[key]=_make_bent_solid(name,i,d,dz_sweep,radial_sweep,kerfs)
 return _SOLIDS[key]
def _make_bent_solid(name,i,d,dz_sweep=0,radial_sweep=0,kerfs=True):
 slabs=bent_slabs(name,i,d,kerfs);angle=math.radians(d['seam_phase_deg']+(i+.5)*360/d[name]['segments'])
 pieces=[]
 for (a,c),xy in slabs:
  if radial_sweep:xy=unary_union([p02.swept_polygon(p,radial_sweep*math.cos(angle),radial_sweep*math.sin(angle)) for p in polygons(xy)])
  pieces.append(extrude_multi(xy,450+a,c-a+dz_sweep))
 return union_solids(pieces)
def existing(d5,d4,d3,u,b):return p05.assembly('A',d5,d4,d3,u,b)
def assembly(name,d,d5,d4,d3,u,b):
 out=existing(d5,d4,d3,u,b)
 for layer,z in [('P07B',450),('P07T',494)]:out[layer]=p02.plate_solid(skin(name,layer,d,d4,d3,u,b),z,6)
 for i in range(d[name]['segments']):out[f'P07R{i+1}']=bent_solid(name,i,d)
 return out

def step(label,swept,prior,start,role='REAL_MATERIAL'):
 return p04.step(label,swept,prior,start,[0,0,0],role)
def routes(name,d,d5,d4,d3,u,b):
 allparts=assembly(name,d,d5,d4,d3,u,b);base=p04.base(d3,u,b);steps=[];prior=dict(base)
 bottom=skin(name,'P07B',d,d4,d3,u,b)
 steps.append(step('P07B',p04.lower_sweep(bottom,450,520),prior,[0,0,70]));prior['P07B']=allparts['P07B']
 for layer,z in d4['layers_z_mm'].items():
  face=p04.disk('A',layer,d4,d3,u,b);steps.append(step(layer,p04.lower_sweep(face,z[0],520),prior,[0,0,520-z[0]]));prior[layer]=allparts[layer]
 for i,a in enumerate(d5['angles_deg'],1):
  k=f'P05_{i}';r=math.radians(a);steps.append(step(k,p05.sweep_rib('A',d5,dr=100,angle=a),prior,[100*math.cos(r),100*math.sin(r),0]));prior[k]=allparts[k]
 # Access reservation checked here, not an invented P08 part or lock installation claim.
 access=tool_access(prior,d,d4,d3,u,b)
 pre_rim=dict(prior)
 for i in range(d[name]['segments']):
  k=f'P07R{i+1}';steps.append(step(k,bent_solid(name,i,d,dz_sweep=70),prior,[0,0,70],'RIGID_PREBENT_IDEAL_MATERIAL_NOT_BENDING_PROOF'));prior[k]=allparts[k]
 top=skin(name,'P07T',d,d4,d3,u,b);steps.append(step('P07T',p04.lower_sweep(top,494,540),prior,[0,0,46]));prior['P07T']=allparts['P07T']
 primary={'status':'PASS_CAD_SPECIFIED_PATH' if max(s['maximum_intersection_mm3'] for s in steps)<1e-6 else 'BLOCKED',
          'steps':steps,'checks':sum(len(s['continuous_intersections']) for s in steps),'open_access_before_top':access,
          'scope':'pre-bent ideal material; no kerf deformation/fixture/P08/adhesive proof'}
 # Alternate order: skins closed before rim; a legitimate trial even if blocked for edge comb.
 prior={**pre_rim,'P07T':allparts['P07T']};alternate=[]
 for i in range(d[name]['segments']):
  k=f'P07R{i+1}';alternate.append(step(k,bent_solid(name,i,d,dz_sweep=70),prior,[0,0,70]));prior[k]=allparts[k]
 prior=dict(pre_rim);radial=list(steps[:9])
 for i in range(d[name]['segments']):
  k=f'P07R{i+1}';ang=math.radians(d['seam_phase_deg']+(i+.5)*360/d[name]['segments'])
  radial.append(step(k,bent_solid(name,i,d,radial_sweep=60),prior,[60*math.cos(ang),60*math.sin(ang),0]));prior[k]=allparts[k]
 radial.append(step('P07T',p04.lower_sweep(top,494,540),prior,[0,0,46]));prior['P07T']=allparts['P07T']
 return {'radial_rim_before_top':{'steps':radial,'status':'PASS_CAD_SPECIFIED_PATH' if max(s['maximum_intersection_mm3'] for s in radial)<1e-6 else 'BLOCKED'},'bottom_disks_ribs_rim_top':primary,'closed_top_then_rim':{'steps':alternate,'status':'PASS_CAD_SPECIFIED_PATH' if max(s['maximum_intersection_mm3'] for s in alternate)<1e-6 else 'BLOCKED'},
         'closed_top_access':tool_access(allparts,d,d4,d3,u,b)}
def tool_access(parts,d,d4,d3,u,b):
 out=[]
 for t in p04.tongues(d3,u,b):
  c=t['xy'].centroid;tool=p02.plate_solid(translate(circle(d['tool_diameter_hypothesis_mm']/2,d),xoff=c.x,yoff=c.y),d['tool_tip_z_mm'],d['tool_start_z_mm']-d['tool_tip_z_mm'])
  hits=p04.checks(tool,parts);out.append({'tongue':t['id'],'tip_xyz_mm':[c.x,c.y,d['tool_tip_z_mm']],'checks':hits,'maximum_intersection_mm3':max(x['volume_mm3'] for x in hits)})
 return {'role':'TOOL_CORRIDOR_RESERVATION_NOT_REAL_LOCK','tools':out,'status':'PASS_RESERVATION_ONLY' if max(x['maximum_intersection_mm3'] for x in out)<1e-6 else 'BLOCKED'}
def contacts(name,d,d5,d4,d3,u,b):
 bottom=skin(name,'P07B',d,d4,d3,u,b);top=skin(name,'P07T',d,d4,d3,u,b)
 disk=p04.disk('A','P04L',d4,d3,u,b);ribs=p05.metrics('A',d5,d4,d3,u,b)['skin_reservations']
 # Faceted inner skin boundary is shared exactly by rim; quantify actual uninterrupted edge intervals.
 edge={}
 for layer,span in [('P07B',(0,6)),('P07T',(44,50))]:
  face=bottom if layer=='P07B' else top;area=0
  for i in range(d[name]['segments']):
   for (a,c),xy in bent_slabs(name,i,d):
    height=max(0,min(c,span[1])-max(a,span[0]));area+=face.boundary.intersection(xy.buffer(1e-7,join_style=2)).length*height
  edge[layer]={'coincidence_tolerance_mm':1e-7,'nominal_boundary_contact_area_mm2':area,'claim':'boundary only; no adhesive or full retention proof'}
 return {'disk_lower_bottom_face_mm2':disk.intersection(bottom).area,'disk_upper_top_gap_mm':8,
         'rib_faces_per_skin':ribs,'six_ribs_contact_per_skin_mm2':3096,'rib_rim_minimum_air_gap_mm':171-math.hypot(169,3),
         'rim_skin_boundaries':edge,'bond_actual_mm2':None,'structural_tests':'NOT_RUN'}
def negatives(name,d,d5,d4,d3,u,b):
 allparts=assembly(name,d,d5,d4,d3,u,b);bottom=skin(name,'P07B',d,d4,d3,u,b)
 no_slots=p02.plate_solid(circle(171,d),450,6);tongues={t['id']:t['solid'] for t in p04.tongues(d3,u,b)}
 tight=d4.copy();tight['tongue_allowance_t_each_side_mm']=-.1
 tightplate=p02.plate_solid(circle(171,d).difference(unary_union(p04.tongue_slots(tight,d3,u,b))),450,6)
 late=p04.lower_sweep(bottom,450,520);wall=extrude_multi(circle(175,d).difference(circle(171,d)),450,50)
 return {'bottom_without_slots_max_mm3':max(x['volume_mm3'] for x in p04.checks(no_slots,tongues)),
         'insufficient_slot_clearance_mm3':max(x['volume_mm3'] for x in p04.checks(tightplate,tongues)),
         'bottom_after_disks_max_mm3':max(x['volume_mm3'] for x in p04.checks(late,{k:allparts[k] for k in ['P04L','P04U']})),
         'rib_after_full_closed_rim_mm3':(p05.sweep_rib('A',d5,dr=100)^wall).volume(),
         'top_skin_wrong_z487_mm3':(p02.plate_solid(skin(name,'P07T',d,d4,d3,u,b),488-1,6)^allparts['L1_P01_1']).volume(),
         'unsegmented_length_with_margins_mm':circumference(d)+20,
         'P06_status':'RESERVATION_ONLY_CTB006R_23_OPEN_NOT_IN_MODEL',
         'rim_after_closed_top_is_not_lock_access':'BLOCKED_CORRIDORS_RETAINED'}
