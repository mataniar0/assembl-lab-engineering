"""Tier1 new skin/experimental rim profiles, actual exports, material mapping and routes."""
import copy,csv,json,math,sys,unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import ezdxf,numpy as np,trimesh
from PIL import Image
from jsonschema import ValidationError
PART=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PART/'src'))
from model import *
D,D5,D4,D3,U,B=inputs();PROOFS=json.loads((PART/'assembly/proofs.json').read_text())
def meta(n):return json.loads((PART/'variants'/n/'dimensions-and-bom.json').read_text())
def cut_parts(n):return {**{k:skin(n,k,D,D4,D3,U,B) for k in ('P07B','P07T')},**{f'P07R{i+1}':sheet_profile(flat_profile(n,i,D)) for i in range(D[n]['segments'])}}
def svg(path):
 root=ET.parse(path).getroot();cut=root.find('.//{http://www.w3.org/2000/svg}g[@id="CUT"]');loops=[[[float(x) for x in v.split(',')] for v in e.attrib['points'].split()] for e in cut if e.tag.endswith('polygon')]
 return root,Polygon(loops[0],loops[1:])
class GlobalTests(unittest.TestCase):
 def test_schema_rejects_wrong_stock_dimensions_radius_pattern_and_fake_measurements(self):
  schema=json.loads((PART/'src/design.schema.json').read_text())
  for key,value in [('outer_radius_mm',171),('skin_radius_mm',175),('skin_thickness_mm',4),('rim_thickness_mm',6),('sheet_hw_mm',[440,800]),('measured_kerf_mm',.1),('kerf_width_hypothesis_mm',8),('kerf_status','BEND_VERIFIED')]:
   wrong=copy.deepcopy(D);wrong[key]=value
   with self.assertRaises(ValidationError):Draft202012Validator(schema).validate(wrong)
 def test_unsegmented_strip_cannot_fit_portrait_stock(self):
  self.assertAlmostEqual(circumference(D),1086.991058142,places=8)
  self.assertGreater(circumference(D)+20,800);self.assertGreater(circumference(D)+20,440)
  self.assertEqual((500-450,494-456),(50,38))
 def test_inner_outer_radius_confusion_causes_skin_collision(self):
  bad=extrude_multi(circle(171,D).difference(circle(167,D)),450,50)
  bottom=p02.plate_solid(skin('A','P07B',D,D4,D3,U,B),450,6)
  self.assertGreater((bad^bottom).volume(),1000)
 def test_invalid_full_height_kerfs_disconnect_material(self):
  bad=box(0,0,100,50).difference(box(40,0,41,50));self.assertEqual(bad.geom_type,'MultiPolygon')
  for n in CONCEPTS:
   for i in range(D[n]['segments']):self.assertEqual(flat_profile(n,i,D).geom_type,'Polygon')
 def test_missing_segment_is_detectable_in_bom_and_coverage(self):
  for n in CONCEPTS:
   full=meta(n);self.assertEqual(len(full['segments']),D[n]['segments']);self.assertNotEqual(D[n]['segments']-1,full['bom']['rim_segments'])
   face=flat_profile(n,0,D);self.assertGreater(face.area,5000)
 def test_periodic_step_seams_preserve_gap_without_positive_overlap(self):
  for n in CONCEPTS:
   length=circumference(D)/D[n]['segments'];p=flat_profile(n,0,D,kerfs=False)
   self.assertLess(p.intersection(translate(p,xoff=length)).area,1e-7)
   for z in [1,17,19,31,33,49]:
    a,c=horizontal_intervals(p,z)[0][0],horizontal_intervals(p,z)[-1][1]
    self.assertAlmostEqual((a+length)-c,.4,places=8)
 def test_no_measured_kerf_or_physical_release_and_p06_open(self):
  self.assertEqual(D['kerf_status'],'KERF_COUPON_PENDING');self.assertEqual(D['physical_tests'],'NOT_RUN')
  for key in ('measured_thickness_mm','measured_kerf_mm','neutral_axis_measured_mm'):self.assertIsNone(D[key])
  decision=(PROJECT/'parts/P06/CTB-006-LEAD-DECISION.md').read_text();self.assertIn('IF-09_OPEN',decision)
  for n in CONCEPTS:self.assertIn('ISSUE23_OPEN',PROOFS[n]['P06']);self.assertIn('NOT_MODELED',PROOFS[n]['P08'])
class VariantTests(unittest.TestCase):pass

def contours(self,n):
 for k,p in cut_parts(n).items():
  self.assertTrue(p.is_valid,k);self.assertEqual(p.geom_type,'Polygon');self.assertGreater(p.area,0)
  for loop in paths(p):
   self.assertEqual(len(loop),len(set(tuple(v) for v in loop)));self.assertTrue(LineString(loop+[loop[0]]).is_simple)
 if n=='C':self.assertEqual(len(flat_profile(n,0,D).interiors),0)

def exports(self,n):
 for k,p in cut_parts(n).items():
  folder=PART/'variants'/n;root,v=svg(folder/f'{k}.svg');doc=ezdxf.readfile(folder/f'{k}.dxf');self.assertEqual(doc.units,4)
  lines=[e for e in doc.modelspace().query('LWPOLYLINE') if e.dxf.layer=='CUT_DESIGN_ONLY'];self.assertTrue(all(e.closed for e in lines))
  loops=[[[v[0],v[1]] for v in e.get_points()] for e in lines];q=Polygon(loops[0],loops[1:]);self.assertEqual(len(lines),1+len(p.interiors))
  self.assertLess(p.hausdorff_distance(v),1e-6);self.assertLess(p.hausdorff_distance(q),1e-6)
  self.assertTrue(all(e.dxf.layer=='NOT_CUT_DIMENSIONS' for e in doc.modelspace().query('TEXT')))
  self.assertIn('sha256='+digest(p),root.find('{http://www.w3.org/2000/svg}metadata').text)

def raster_mm(self,n):
 for k,p in cut_parts(n).items():
  ex=meta(n)['cut_parts'][k];root,_=svg(PART/'variants'/n/f'{k}.svg');w,h=ex['artboard_wh_mm']
  self.assertAlmostEqual(float(root.attrib['width'][:-2]),w);self.assertAlmostEqual(float(root.attrib['height'][:-2]),h)
  with Image.open(PART/'variants'/n/f'{k}.png') as im:
   self.assertLess(abs(im.width-w/25.4*96),1.01);self.assertLess(abs(im.height-h/25.4*96),1.01)
   self.assertIn('1:1mm',im.info['Description'])
  np.testing.assert_allclose(p.bounds,ex['bounds_mm'],atol=1e-6)

def stock_and_webs(self,n):
 for k,p in cut_parts(n).items():
  x0,y0,x1,y1=p.bounds;self.assertLessEqual(x1-x0+20,440);self.assertLessEqual(y1-y0+20,800)
  if k.startswith('P07R'):self.assertAlmostEqual(x1-x0,50)
 self.assertAlmostEqual(meta(n)['remaining_lateral_web_screen_mm'],7.2)
 self.assertEqual(meta(n)['kerf_compensation_mm'],None)
 # Every experimental slit retains actual material at one or both ends.
 for i in range(D[n]['segments']):
  p=flat_profile(n,i,D);self.assertGreater(p.intersection(box(-10,6.2,800,6.5)).area,0)
  spans=horizontal_intervals(p,25);self.assertTrue(all(c-a>=7.2-1e-6 for a,c in spans))
  self.assertGreaterEqual(spans[0][1]-spans[0][0],12)
  self.assertGreaterEqual(spans[-1][1]-spans[-1][0],12)
  if n in ('A','B'):
   uncut=flat_profile(n,i,D,kerfs=False)
   for hole in p.interiors:
    a,lo,c,hi=hole.bounds
    for z in [lo+1e-5,(lo+hi)/2,hi-1e-5]:
     outer=horizontal_intervals(uncut,z);self.assertGreaterEqual(a-outer[0][0],12);self.assertGreaterEqual(outer[-1][1]-c,12)

def mapping(self,n):
 for i in range(D[n]['segments']):
  face=flat_profile(n,i,D);s=bent_solid(n,i,D);self.assertLess(abs(s.volume()/(4*face.area)-1),.0002)
  self.assertEqual(len(s.decompose()),1);self.assertAlmostEqual(s.bounding_box()[2],450,places=5);self.assertAlmostEqual(s.bounding_box()[5],500,places=5)
  mesh=s.to_mesh();vertices=np.asarray(mesh.vert_properties)[:,:3];r=np.hypot(vertices[:,0],vertices[:,1]);self.assertLessEqual(r.max(),175+2e-5);self.assertGreaterEqual(r.min(),171-.007)

def six_slots(self,n):
 p=skin(n,'P07B',D,D4,D3,U,B);self.assertEqual(len(p.interiors),6);top=skin(n,'P07T',D,D4,D3,U,B);self.assertEqual(len(top.interiors),0)
 s=p02.plate_solid(p,450,6)
 for t in p04.tongues(D3,U,B):self.assertLess((s^t['solid']).volume(),1e-6)
 self.assertTrue(top.contains(Point(0,0)))
 if n=='C':self.assertLess(top.difference(circle(175,D)).area,1e-6);self.assertGreater(top.area,circle(171,D).area)
 else:self.assertAlmostEqual(top.area,circle(171,D).area)

def nominal(self,n):
 parts=assembly(n,D,D5,D4,D3,U,B);pairs=p02.collision_matrix(parts)
 self.assertEqual(len(parts),29+D[n]['segments']);self.assertEqual(len(pairs),len(parts)*(len(parts)-1)//2)
 self.assertLess(max(x['intersection_mm3'] for x in pairs),1e-6)

def paths_test(self,n):
 r=routes(n,D,D5,D4,D3,U,B);self.assertEqual(r['bottom_disks_ribs_rim_top']['status'],'BLOCKED' if n=='B' else 'PASS_CAD_SPECIFIED_PATH')
 self.assertEqual(r['closed_top_then_rim']['status'],'PASS_CAD_SPECIFIED_PATH' if n=='A' else 'BLOCKED')
 self.assertEqual(r['radial_rim_before_top']['status'],'BLOCKED' if n=='C' else 'PASS_CAD_SPECIFIED_PATH')
 self.assertEqual(r['bottom_disks_ribs_rim_top']['status'],PROOFS[n]['routes']['bottom_disks_ribs_rim_top']['status'])
 for stage in r['bottom_disks_ribs_rim_top']['steps']:
  if not stage['moving'].startswith('P07R'):self.assertLess(stage['maximum_intersection_mm3'],1e-6)

def contact(self,n):
 c=contacts(n,D,D5,D4,D3,U,B);self.assertAlmostEqual(c['disk_lower_bottom_face_mm2'],26899.470377,places=4)
 self.assertEqual(c['disk_upper_top_gap_mm'],8);self.assertAlmostEqual(c['rib_rim_minimum_air_gap_mm'],1.9733748784)
 for layer in ['P07B','P07T']:
  self.assertEqual(c['rib_faces_per_skin'][layer]['nominal_boundary_area_mm2'],516);self.assertGreater(c['rim_skin_boundaries'][layer]['nominal_boundary_contact_area_mm2'],5000)
 self.assertIsNone(c['bond_actual_mm2'])

def access(self,n):
 r=PROOFS[n]['routes'];self.assertEqual(r['bottom_disks_ribs_rim_top']['open_access_before_top']['status'],'PASS_RESERVATION_ONLY')
 self.assertEqual(r['closed_top_access']['status'],'BLOCKED');self.assertEqual(len(r['closed_top_access']['tools']),6)
 self.assertTrue(all(t['maximum_intersection_mm3']>1 for t in r['closed_top_access']['tools']))

def negative_controls(self,n):
 c=negatives(n,D,D5,D4,D3,U,B)
 for key in ['bottom_without_slots_max_mm3','insufficient_slot_clearance_mm3','bottom_after_disks_max_mm3','rib_after_full_closed_rim_mm3','top_skin_wrong_z487_mm3']:self.assertGreater(c[key],1e-6,key)
 self.assertGreater(c['unsegmented_length_with_margins_mm'],800)

def bom_glb(self,n):
 parts=assembly(n,D,D5,D4,D3,U,B);scene=trimesh.load(PART/'assembly'/f'{n}-actual-DESIGN_ONLY.glb',force='scene');self.assertEqual(set(parts),set(scene.graph.nodes_geometry))
 met=meta(n);self.assertEqual(len(parts),met['bom']['total_real_bodies']);self.assertEqual(met['bom']['P06_P08_fixtures_glue_hardware_actual_bodies'],0)
 with (PART/'BOM-v1.csv').open() as h:rows=[r for r in csv.DictReader(h) if r['concept']==n]
 self.assertEqual({r['part_id']:int(r['quantity']) for r in rows},{k:ex['quantity'] for k,ex in met['cut_parts'].items()})
 for k in scene.graph.nodes_geometry:
  trans,g=scene.graph[k];m=scene.geometry[g].copy();m.apply_transform(trans);self.assertTrue(m.is_watertight);self.assertGreater(m.volume,0)
  self.assertAlmostEqual(m.volume*1e9/parts[k].volume(),1,delta=1e-5);np.testing.assert_allclose(m.bounds*1000,np.asarray(parts[k].bounding_box()).reshape(2,3),atol=4e-5)

def top_withdrawal(self,n):
 parts=assembly(n,D,D5,D4,D3,U,B);top=skin(n,'P07T',D,D4,D3,U,B);sweep=p02.plate_solid(top,494,52)
 self.assertLess(max(x['volume_mm3'] for x in p04.checks(sweep,{k:s for k,s in parts.items() if k!='P07T'})),1e-6)
 if n=='C':
  wrong=p03.rotation(parts['P07T'],3);self.assertGreater(sum((wrong^s).volume() for k,s in parts.items() if k.startswith('P07R')),1)

for n in CONCEPTS:
 for fn in [contours,exports,raster_mm,stock_and_webs,mapping,six_slots,nominal,paths_test,contact,access,negative_controls,bom_glb,top_withdrawal]:setattr(VariantTests,'test_'+n+'_'+fn.__name__,lambda self,name=n,f=fn:f(self,name))
if __name__=='__main__':unittest.main(verbosity=2)
