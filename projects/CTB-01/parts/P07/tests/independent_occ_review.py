"""Independent CTB-007 audit from actual cut exports; no component models imported.
Finite OpenCASCADE skin/upstream reconstruction plus mathematically developed rim checks.
All kerf development/bending and attachments remain DESIGN_ONLY, not physical evidence.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,subprocess,xml.etree.ElementTree as ET
import cadquery as cq
import ezdxf
import numpy as np
import trimesh
from PIL import Image
from shapely.geometry import Polygon,Point,LineString,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'projects/CTB-01/parts/P07').is_dir())
PARTS=ROOT/'projects/CTB-01/parts';PART=PARTS/'P07'
BASE='6db45fa7ba0d9a81ff9bbc6d1a432133ab955214';EPS=1e-6
REVIEWED_CUT_GEOMETRY={}


def svg(path):
 root=ET.parse(path).getroot();cut=root.find('.//{http://www.w3.org/2000/svg}g[@id="CUT"]')
 if cut is None:
  assert PART not in path.parents,(path,'newP07export missing CUT group')
  cut=root # Historical P01/P02/P03 exports predate explicit CUT group IDs.
 loops=[[(float(x),float(y)) for x,y in (v.split(',') for v in e.attrib['points'].split())] for e in cut.findall('.//{http://www.w3.org/2000/svg}polygon')]
 assert loops,path
 p=Polygon(loops[0],loops[1:]);assert p.is_valid and p.geom_type=='Polygon',(path,'invalid/disconnected material')
 return p


def export_audit(path,fit_rotation=False):
 p=svg(path);REVIEWED_CUT_GEOMETRY[str(path.relative_to(ROOT))]=hashlib.sha256(p.normalize().wkb).hexdigest();root=ET.parse(path).getroot();vb=[float(v) for v in root.attrib['viewBox'].split()]
 assert abs(float(root.attrib['width'].removesuffix('mm'))-vb[2])<1e-5
 assert abs(float(root.attrib['height'].removesuffix('mm'))-vb[3])<1e-5
 doc=ezdxf.readfile(path.with_suffix('.dxf'));assert doc.units==4
 loops=[]
 for e in doc.modelspace():
  if e.dxf.layer.startswith('CUT'):
   assert e.dxftype()=='LWPOLYLINE' and e.closed
   xy=[(v[0],v[1]) for v in e.get_points()];assert len(xy)==len(set(xy))
   assert LineString(xy+[xy[0]]).is_simple
   loops.append(xy)
 q=Polygon(loops[0],loops[1:]);assert q.is_valid and p.symmetric_difference(q).area<1e-6
 assert len(doc.audit().errors)==0
 w,h=p.bounds[2]-p.bounds[0],p.bounds[3]-p.bounds[1]
 fit=w+20<=440 and h+20<=800
 if fit_rotation:fit=fit or (h+20<=440 and w+20<=800)
 assert fit,(path,w,h,'portrait H800/W440 with10mm margin')
 with Image.open(path.with_suffix('.png')) as im:
  assert abs(im.width-vb[2]/25.4*96)<1.01 and abs(im.height-vb[3]/25.4*96)<1.01
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
 return out


def stage(label,swept,fixed):
 checks={k:overlap(swept,v) for k,v in fixed.items()}
 return {'moving':label,'checks':len(checks),'maximum_overlap_mm3':max(checks.values(),default=0.),'positive_pairs_mm3':{k:v for k,v in checks.items() if v>EPS}}


def base27():
 p03=PARTS/'P03/variants/A_COMPACT_CLOSED';face=svg(p03/'P01-Y-mortise-study-v1.svg')
 stations=json.loads((p03/'mechanical-dimensions.json').read_text())['stations'];parts={'P03':plate(svg(p03/'P03.svg'),407)}
 for leg,a in enumerate([0,120,240],1):
  for i,t in enumerate([-7.5,13.5],1):parts[f'L{leg}_P01_{i}']=spin(cheek(face,t),a)
  for s in stations:
   p=translate(svg(PARTS/f"P02/variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
   parts[f"L{leg}_{s['id']}"]=spin(plate(p,s['z_mm']-3),a)
 for layer,z in [('P04L',456),('P04U',480)]:parts[layer]=plate(svg(PARTS/f'P04/variants/A/{layer}.svg'),z)
 rib=svg(PARTS/'P05/variants/A/P05.svg');parts.update({f'P05_{i+1}':spin(cheek(rib,3),a) for i,a in enumerate(range(0,360,60))})
 assert len(parts)==27
 return parts,face,stations,rib


def protected():
 prefixes=['projects/CTB-01/specifications/CTB-000',*[f'projects/CTB-01/parts/P{i:02}' for i in range(1,7)]]
 names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,*prefixes],cwd=ROOT,text=True).splitlines()
 for n in names:assert (ROOT/n).read_bytes()==subprocess.check_output(['git','show',BASE+':'+n],cwd=ROOT),n
 assert len(names)==439
 return {'baseline':BASE,'files_byte_equal':len(names)}


def bounds(s):
 q=s.BoundingBox();return np.array([[q.xmin,q.ymin,q.zmin],[q.xmax,q.ymax,q.zmax]])


def contact_land(rib,z):
 line=rib.intersection(LineString([(0,z),(200,z)]))
 return {'r_interval_mm':list(line.bounds[::2]),'per_rib_area_mm2':line.length*6,'all_six_area_mm2':line.length*36}


def swap_sheet_axes(poly):
 from shapely.ops import transform
 return transform(lambda x,y:(y,x),poly)


def vertical_bands(poly):
 # Actual experimental contours are orthogonal. Every slab is exact between vertex levels.
 for ring in [poly.exterior,*poly.interiors]:
  for a,b in zip(ring.coords,list(ring.coords)[1:]):
   assert abs(a[0]-b[0])<1e-7 or abs(a[1]-b[1])<1e-7,('nonorthogonal developed contour',a,b)
 heights=sorted({float(y) for ring in [poly.exterior,*poly.interiors] for _,y in ring.coords})
 out=[]
 for low,high in zip(heights,heights[1:]):
  if high-low<1e-9:continue
  section=poly.intersection(LineString([(-200,(low+high)/2),(1500,(low+high)/2)]))
  lines=[section] if section.geom_type=='LineString' else list(section.geoms)
  intervals=sorted((l.bounds[0],l.bounds[2]) for l in lines if l.geom_type=='LineString' and l.length>1e-9)
  out.append((low,high,intervals))
 return out


def angular_clip(a,b,mask):
 angles=np.linspace(a,b,max(2,math.ceil(math.degrees(b-a)/12)+1))
 wedge=Polygon([(0,0),*[(1000*math.cos(t),1000*math.sin(t)) for t in angles]])
 return mask.intersection(wedge)


def polys(poly):
 if poly.geom_type=='Polygon':return [poly]
 return [p for p in poly.geoms if p.geom_type=='Polygon']


NUMERIC_INTERMEDIATES=[]
def mapped_cells(flat,phase_deg,mask):
 cells=[]
 for lo,hi,spans in vertical_bands(flat):
  for s0,s1 in spans:
   xy=angular_clip(math.radians(phase_deg)+s0/173,math.radians(phase_deg)+s1/173,mask)
   for p in polys(xy):
    if p.area<1e-12:
     NUMERIC_INTERMEDIATES.append({'role':'generated angular clipping only','discarded_area_mm2':p.area,'threshold_mm2':1e-12,'maximum_volume_mm3':p.area*(hi-lo)})
     continue
    cells.append((lo,hi,p))
 return cells


def cells_compound(cells,dz=0,radial=None):
 material=[]
 for lo,hi,p in cells:
  if radial is not None:p=sweep2(p,dx=radial[0],dy=radial[1])
  material.append(plate(p,450+lo,hi-lo+dz))
 return cq.Compound.makeCompound(material)


def periodic_material(flat,segment_index,length):
 shifted=translate(flat,xoff=segment_index*length)
 return unary_union([translate(shifted,xoff=k*2*math.pi*173) for k in [-1,0,1]]).intersection(box(0,0,2*math.pi*173,50))


def upper_route(base,skinB,skinT,rib):
 prior={k:s for k,s in base.items() if k!='P04L' and k!='P04U' and not k.startswith('P05')};steps=[]
 for key,poly,z in [('P07B',skinB,450),('P04L',svg(PARTS/'P04/variants/A/P04L.svg'),456),('P04U',svg(PARTS/'P04/variants/A/P04U.svg'),480)]:
  steps.append(stage(key,plate(poly,z,526-z),prior));prior[key]=plate(skinB,450) if key=='P07B' else base[key]
 for i,a in enumerate(range(0,360,60),1):
  key=f'P05_{i}';steps.append(stage(key,spin(cheek(sweep2(rib,dx=100),3),a),prior));prior[key]=base[key]
 return steps,prior


def tool_corridors(parts,top):
 probes=[]
 for leg,a in enumerate([0,120,240],1):
  for side in [-1,1]:
   xy=rotate(Point(57,side*10.5),a,origin=(0,0))
   tool=cq.Workplane('XY',origin=(xy.x,xy.y,488.5)).circle(2).extrude(31.5).val()
   openhit=max(overlap(tool,p) for p in parts.values());closed=overlap(tool,top)
   assert openhit<EPS and closed>EPS
   probes.append({'leg':leg,'side':side,'hypothetical_probe_diameter_mm':4,'probe_tip_z_mm':488.5,'open_top_maximum_mm3':openhit,'closed_top_overlap_mm3':closed})
 return probes


def glb_audit(path,reference,rim_labels):
 scene=trimesh.load(path,force='scene');assert set(scene.graph.nodes_geometry)==set(reference)
 rows={}
 for label in scene.graph.nodes_geometry:
  tf,g=scene.graph[label];m=scene.geometry[g].copy();m.apply_transform(tf)
  assert m.is_watertight and m.volume>0
  db=float(np.max(np.abs(m.bounds*1000-bounds(reference[label]))));dv=abs(m.volume*1e9/reference[label].Volume()-1)
  assert db<5e-5 and dv<1e-5,(label,db,dv)
  rows[label]={'bounds_delta_mm':db,'relative_volume_delta':dv,'watertight_positive':True}
 return {'nodes':len(rows),'parts':rows,'units':'GLTF metres checked against millimetres'}


def radial_swept_cells(cells,dx,dy):
 grouped={}
 for lo,hi,p in cells:grouped.setdefault((lo,hi),[]).append(sweep2(p,dx,dy))
 out=[]
 for (lo,hi),polygons in grouped.items():
  for p in polys(unary_union(polygons)):
   tiny=[Polygon(h).area for h in p.interiors if Polygon(h).area<1e-14]
   if tiny:
    repaired=Polygon(p.exterior,[h for h in p.interiors if Polygon(h).area>=1e-14]);delta=repaired.symmetric_difference(p).area
    assert repaired.is_valid and delta<1e-14
    NUMERIC_INTERMEDIATES.append({'role':'generated radial sweep hole only, actual exports untouched','hole_areas_mm2':tiny,'area_delta_mm2':delta,'threshold_mm2':1e-14})
    p=repaired
   if p.area>1e-12:out.append((lo,hi,p))
 return out


def boundary_area_all_or_nothing(skin,cells,zband):
 total=0.
 for lo,hi,p in cells:
  height=max(0,min(hi,zband[1])-max(lo,zband[0]))
  if height<=0:continue
  for ring in [p.exterior,*p.interiors]:
   for a,b in zip(ring.coords,list(ring.coords)[1:]):
    middle=((a[0]+b[0])/2,(a[1]+b[1])/2)
    if max(skin.boundary.distance(Point(q)) for q in [a,b,middle])<1e-7:total+=math.dist(a,b)*height
 return total


def boundary_area(skin,cells,zband):
 # Quantized6dp exports can truncate a shared facet, so measure projected collinear
 # overlap rather than reject a whole edge when one endpoint crosses a skin tab.
 #1e-6mm is the export-coordinate uncertainty; the area-agreement threshold is unchanged.
 segments=[(a,b) for ring in [skin.exterior,*skin.interiors] for a,b in zip(ring.coords,list(ring.coords)[1:])];total=0.
 for lo,hi,p in cells:
  height=max(0,min(hi,zband[1])-max(lo,zband[0]))
  if height<=0:continue
  for ring in [p.exterior,*p.interiors]:
   for a,b in zip(ring.coords,list(ring.coords)[1:]):
    length=math.dist(a,b)
    if length<1e-12:continue
    ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length;spans=[]
    for c,d in segments:
     normal=max(abs((v[0]-a[0])*uy-(v[1]-a[1])*ux) for v in [c,d])
     if normal>1e-6:continue
     low,high=sorted((v[0]-a[0])*ux+(v[1]-a[1])*uy for v in [c,d]);low=max(0,low);high=min(length,high)
     if high>low:spans.append((low,high))
    end=-math.inf
    for low,high in sorted(spans):
     if high>end:total+=(high-max(low,end))*height;end=high
 return total


def profile_audit(name,folder,mask):
 n={'A':2,'B':3,'C':4}[name];metadata=json.loads((folder/'dimensions-and-bom.json').read_text());length=2*math.pi*173/n
 profiles={};cells={};solids={};records={}
 for i in range(n):
  label=f'P07R{i+1}';sheet,cut=export_audit(folder/(label+'.svg'));flat=swap_sheet_axes(sheet);phase=15+i*360/n
  meta=metadata['segments'][label];intrinsic=Polygon(meta['intrinsic_paths_s_h_mm'][0],meta['intrinsic_paths_s_h_mm'][1:])
  assert flat.symmetric_difference(intrinsic).area<1e-6
  assert abs(meta['phase_angle_deg']-phase)<1e-8 and abs(meta['nominal_arc_length_mm']-length)<1e-8
  assert meta['kerf_status']=='KERF_COUPON_PENDING' and meta['straight_developed_geometry_only_not_bend_recipe']
  current=mapped_cells(flat,phase,mask);solid=cells_compound(current)
  assert solid.isValid() and abs(solid.Volume()/(4*flat.area)-1)<1e-4
  assert abs(solid.Volume()/meta['actual_faceted_volume_mm3']-1)<1e-6
  # Material connectivity is proved by a single planar polygon and injective development
  # over less than one revolution. The CQ compound partitions that same body by Z only.
  assert flat.geom_type=='Polygon' and flat.is_valid and flat.bounds[3]==50
  profiles[label]=flat;cells[label]=current;solids[label]=solid
  records[label]={'cut_export':cut,'mapped_cells':len(current),'OCC_volume_mm3':solid.Volume(),
    'ideal_development_volume_mm3':4*flat.area,'relative_faceted_mapping_delta':abs(solid.Volume()/(4*flat.area)-1),
    'phase_deg':phase,'intrinsic_slabs':vertical_bands(flat),'no_physical_bending_claim':True}
 wrapped={label:periodic_material(p,i,length) for i,(label,p) in enumerate(profiles.items())}
 contacts={a+'|'+b:pa.intersection(pb).area for (a,pa),(b,pb) in itertools.combinations(wrapped.items(),2)}
 assert max(contacts.values(),default=0)<1e-6,(name,'periodic splice overlap',contacts)
 coverage={str(h):sum(p.intersection(LineString([(0,h),(2*math.pi*173,h)])).length for p in wrapped.values()) for h in [2,10,25,40,48]}
 assert metadata['bom']['total_real_bodies']==29+n
 return profiles,cells,solids,{'pieces':records,'periodic_joint_positive_area_mm2':contacts,'occupied_neutral_length_at_heights_mm':coverage}


def variant_audit(name,base,rib,mask):
 print('Independent CTB007 OCC',name,'actual exports',flush=True)
 folder=PART/'variants'/name;skinB,cutB=export_audit(folder/'P07B.svg');skinT,cutT=export_audit(folder/'P07T.svg')
 assert len(skinB.interiors)==6 and len(skinT.interiors)==0 and skinT.contains(Point(0,0))
 expectedR=175 if name=='C' else 171
 assert max(math.hypot(*v) for v in skinT.exterior.coords)<=expectedR+1e-6
 assert abs(max(math.hypot(*v) for v in skinT.exterior.coords)-expectedR)<1e-6
 B,T=plate(skinB,450),plate(skinT,494)
 profiles,cells,rims,rimdata=profile_audit(name,folder,mask)
 print(name,'finite mapped material constructed',flush=True)
 allparts={**base,'P07B':B,'P07T':T,**rims};assert len(allparts)=={'A':31,'B':32,'C':33}[name]
 newpairs={a+'|'+b:overlap(x,y) for (a,x),(b,y) in itertools.combinations(allparts.items(),2) if a.startswith('P07') or b.startswith('P07')}
 assert max(newpairs.values())<EPS,(name,'new material collision',[(k,v) for k,v in newpairs.items() if v>EPS])
 # Exact alternative operation: union the vertical sweep in developed material first,
 # then map it. This commutes with rigid Z translation and avoids double-counting cells.
 print(name,'new static pairs PASS',flush=True)
 steps,prior=upper_route(base,skinB,skinT,rib);pre_rim=dict(prior)
 for i,(label,flat) in enumerate(profiles.items()):
  swept=cells_compound(mapped_cells(sweep2(flat,dy=70),15+i*360/len(rims),mask))
  steps.append(stage(label+'_vertical_down70',swept,prior));prior[label]=rims[label]
 steps.append(stage('P07T_down46',plate(skinT,494,52),prior))
 route_max=max(s['maximum_overlap_mm3'] for s in steps)
 assert (route_max<EPS)==(name!='B'),(name,'vertical route',steps)
 alternate=[];fixed={**pre_rim,'P07T':T}
 for i,(label,flat) in enumerate(profiles.items()):
  swept=cells_compound(mapped_cells(sweep2(flat,dy=70),15+i*360/len(rims),mask))
  alternate.append(stage(label+'_after_closed_top',swept,fixed));fixed[label]=rims[label]
 assert (max(s['maximum_overlap_mm3'] for s in alternate)<EPS)==(name=='A'),(name,'closed top trial',alternate)
 radial=[];fixed=dict(pre_rim)
 for i,(label,current) in enumerate(cells.items()):
  a=math.radians(15+(i+.5)*360/len(rims));swept=cells_compound(radial_swept_cells(current,60*math.cos(a),60*math.sin(a)))
  radial.append(stage(label+'_radial60',swept,fixed));fixed[label]=rims[label]
 print(name,'three exact rim route trials evaluated',flush=True)
 top_radial=stage('P07T_after_radial_rim',plate(skinT,494,52),fixed)
 radial=[*steps[:9],*radial,top_radial]
 assert (max(s['maximum_overlap_mm3'] for s in radial)<EPS)==(name in ['A','B']),(name,'radial route',radial)
 lift=stage('P07T_upward_WITHDRAWAL_FREE',plate(skinT,494,46),{k:v for k,v in allparts.items() if k!='P07T'});assert lift['maximum_overlap_mm3']<EPS
 late=stage('P07B_after_disks_BLOCKED',plate(skinB,450,76),base);assert late['maximum_overlap_mm3']>EPS
 uncut=plate(Polygon(skinB.exterior),450)
 missingholes={k:overlap(uncut,p) for k,p in base.items() if 'P01' in k};assert all(v>EPS for v in missingholes.values())
 tool=tool_corridors({**base,'P07B':B},T)
 contacts={layer:sum(boundary_area(p,cells[label],span) for label in cells) for layer,p,span in [('P07B',skinB,[0,6]),('P07T',skinT,[44,50])]}
 metadata=json.loads((folder/'dimensions-and-bom.json').read_text())
 for label,area in contacts.items():assert abs(area-metadata['contacts']['rim_skin_boundaries'][label]['nominal_boundary_contact_area_mm2'])<.005,(name,label,area,metadata['contacts'])
 # Real slot matching, retaining the selected upstream pre-ring cheek model.
 for leg,a in enumerate([0,120,240],1):
  for side in [-1,1]:
   tongue=rotate(box(45,side*10.5-3,69,side*10.5+3),a,origin=(0,0))
   assert skinB.intersection(tongue).area<1e-6
 glb=glb_audit(PART/'assembly'/f'{name}-actual-DESIGN_ONLY.glb',allparts,set(rims))
 return {'cut_skins':{'P07B':cutB,'P07T':cutT},'body_count':len(allparts),'new_material_static_pairs':len(newpairs),'new_material_maximum_overlap_mm3':max(newpairs.values()),
   'new_material_pair_matrix':newpairs,'rim_development_and_splices':rimdata,
   'vertical_route':{'stages':steps,'checks':sum(s['checks'] for s in steps),'maximum_overlap_mm3':route_max,'status':'PASS' if route_max<EPS else 'BLOCKED'},
   'closed_top_then_rim':{'stages':alternate,'status':'PASS' if max(s['maximum_overlap_mm3'] for s in alternate)<EPS else 'BLOCKED'},
   'radial_rim_before_top':{'stages':radial,'status':'PASS' if max(s['maximum_overlap_mm3'] for s in radial)<EPS else 'BLOCKED'},
   'negative_late_bottom':late,'negative_uncut_bottom_six_tongues_mm3':missingholes,
   'top_upward_withdrawal_FREE':lift,'P08_access_probes_reservation_only':tool,'independent_rim_skin_boundary_area_mm2':contacts,
   'P05_skin_lands':{str(z):contact_land(rib,z) for z in [456,494]},
   'lower_disk_skin_geometric_contact_mm2':svg(PARTS/'P04/variants/A/P04L.svg').intersection(skinB).area,
   'glb_actual_bodies_parity':glb,'P06_included':False,'P06R23_and_P08_and_physical_all_OPEN':True}


def audit(output,variants=None):
 base,face,stations,rib=base27();A=svg(PART/'variants/A/P07T.svg');inner=Polygon(A.exterior)
 from shapely.affinity import scale
 outer=scale(inner,xfact=175/171,yfact=175/171,origin=(0,0));mask=outer.difference(inner)
 before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PART.rglob('*')) if p.suffix in ['.svg','.dxf','.glb']}
 for path in before:
  if path.endswith('.svg'):REVIEWED_CUT_GEOMETRY[path]=hashlib.sha256(svg(ROOT/path).normalize().wkb).hexdigest()
 result={'scope':'independent regenerated cut exports and finite faceted ideal bent geometry, not physical bending',
   'protected':protected(),'baseline_actual_parts':27,'P06_not_in_active_assembly':True,'variants':{}}
 if variants is not None:
  previous=json.loads(output.read_text());assert previous['protected']==result['protected'];result['variants']=previous['variants']
 for name in (variants or ['A','B','C']):
  result['variants'][name]=variant_audit(name,base,rib,mask)
  output.write_text(json.dumps(result,indent=2)+'\n');print('Independent CTB007 OCC',name,'PASS',flush=True)
 for path,sha in before.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,(path,'export changed during final review')
 assert set(result['variants'])=={'A','B','C'}
 result['reviewed_export_SHA256']=before
 result['partial_contact_method']={'method':'merged projected collinear edge overlap','export_normal_coordinate_tolerance_mm':1e-6,'unchanged_area_agreement_tolerance_mm2':.005}
 result['reviewed_cut_normalized_WKB_SHA256']=REVIEWED_CUT_GEOMETRY
 result['numeric_intermediate_handling']=NUMERIC_INTERMEDIATES
 output.write_text(json.dumps(result,indent=2)+'\n');return result


def flat_screens():
 out={}
 for name,n in [('A',2),('B',3),('C',4)]:
  rows=[]
  for i in range(n):
   p=swap_sheet_axes(svg(PART/'variants'/name/f'P07R{i+1}.svg'))
   holes=polys(box(p.bounds[0],0,p.bounds[2],50).difference(p)) if name=='C' else [Polygon(h) for h in p.interiors]
   kerfs=[];captures=[]
   for h in holes:
    a,lo,b,hi=h.bounds;w=b-a;height=hi-lo
    if abs(w-.8)<1e-6:
     assert abs(h.area-w*height)<1e-6 and abs(height-{'A':34,'B':19,'C':43.5}[name])<1e-6
     kerfs.append([a,lo,b,hi])
    else:
     assert name=='C' and abs(height-6.2)<1e-6
     captures.append([a,lo,b,hi])
   assert kerfs
   mid=p.intersection(LineString([(-10,25),(1000,25)]));ls=[mid] if mid.geom_type=='LineString' else list(mid.geoms)
   spans=[l.length for l in sorted(ls,key=lambda l:l.bounds[0]) if l.geom_type=='LineString'];assert min(spans)>=7.2-1e-6
   minend=math.inf
   if name in ['A','B']:
    uncut=Polygon(p.exterior);levels=sorted(set(y for x,y in uncut.exterior.coords))
    for a,lo,b,hi in kerfs:
     probes=[lo+1e-5,hi-1e-5,(lo+hi)/2,*[z+sign*1e-5 for z in levels for sign in [-1,1] if lo<z+sign*1e-5<hi]]
     for z in probes:
      line=uncut.intersection(LineString([(-10,z),(1000,z)]));minend=min(minend,a-line.bounds[0],line.bounds[2]-b)
   else:minend=min(min(h[0]-p.bounds[0],p.bounds[2]-h[2]) for h in kerfs)
   assert minend>=12-1e-6
   rows.append({'part':f'P07R{i+1}','kerf_slots':len(kerfs),'capture_notches':len(captures),
    'exported_design_slot_width_mm':.8,'exported_design_slot_length_mm':{'A':34,'B':19,'C':43.5}[name],
    'minimum_midheight25_lateral_web_mm':min(spans),'first_midheight_end_land_mm':spans[0],
    'last_midheight_end_land_mm':spans[-1],'minimum_kerf_end_to_actual_seam_mm':minend,
    'scope':'export geometry only; KERF_COUPON_PENDING; no measured physical kerf'})
  out[name]=rows
 return out

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path('/tmp/ctb007-independent-occ-results.json'));parser.add_argument('--flat-screens-only',action='store_true');parser.add_argument('--variants',nargs='+',choices=['A','B','C'])
 args=parser.parse_args()
 if args.flat_screens_only:args.output.write_text(json.dumps(flat_screens(),indent=2)+'\n')
 else:audit(args.output,args.variants)
