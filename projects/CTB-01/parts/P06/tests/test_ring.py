"""Tier1: new P06 material, actual exports, six interfaces, routes and deliberate controls."""
import copy,csv,hashlib,json,math,sys,unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import ezdxf,numpy as np,trimesh
from PIL import Image
from jsonschema import ValidationError
PART=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PART/'src'))
from model import *
D,D5,D4,D3,U,B=inputs();PROOF=json.loads((PART/'assembly/proofs.json').read_text())
def dimensions(name):return json.loads((PART/'variants'/name/'dimensions-and-bom.json').read_text())
def poly_from_svg(path):
 root=ET.parse(path).getroot();cut=root.find('.//{http://www.w3.org/2000/svg}g[@id="CUT"]')
 loops=[[[float(x) for x in p.split(',')] for p in e.attrib['points'].split()] for e in cut if e.tag.endswith('polygon')]
 return root,Polygon(loops[0],loops[1:]),loops

def pieces(name):
 parts=planar_parts(name,D,D3,U)
 if name!='A':parts['P06'+name+'-KEY']=stop_key(D,D3,U) if name=='B' else vertical_key(D)
 return parts

class GlobalTests(unittest.TestCase):
 def test_schema_blocks_wrong_material_dimensions_measurements_neck_and_rotation(self):
  schema=json.loads((PART/'src/design.schema.json').read_text())
  wrongs=[]
  for key,value in [('thickness_mm',6.8),('ring_center_z_mm',257),('leg_angles_deg',[0,120,241]),('measured_kerf_mm',.1),('sheet_hw_mm',[440,800]),('arm_width_mm',16)]:
   bad=copy.deepcopy(D);bad[key]=value;wrongs.append(bad)
  for name in CONCEPTS:
   bad=copy.deepcopy(D);bad[name]['band_width_mm']=2;wrongs.append(bad)
  for bad in wrongs:
   with self.assertRaises(ValidationError):Draft202012Validator(schema).validate(bad)
 def test_sections_derive_joint_from_actual_jointed_cheek(self):
  sec=sections(D,D3,U);lo,hi=sec['joint_common_r_mm'];self.assertAlmostEqual(sec['joint_center_r_mm'],(lo+hi)/2)
  self.assertAlmostEqual(sec['joint_center_r_mm'],112.01764591842917)
  self.assertAlmostEqual(sec['core_outer_radius_mm'],71.38953382956522)
  self.assertEqual(sec['z_mm'],[242,248]);self.assertEqual(len(sec['samples']),13)
  self.assertTrue(all(s['outer_r_mm']>s['inner_r_mm'] for s in sec['samples']))
 def test_b_splice_three_real_finite_connected_pieces(self):
  parts=planar_parts('B',D,D3,U);self.assertEqual(set(parts),{'P06B1','P06B2','P06B3'})
  for i,p in enumerate(parts.values()):
   self.assertEqual(p.geom_type,'Polygon');self.assertTrue(p.is_valid)
   self.assertLess(p.symmetric_difference(rotate(parts['P06B1'],i*120,origin=(0,0))).area,1e-6)
  for a,c in itertools.combinations(parts.values(),2):self.assertLess(a.intersection(c).area,1e-6)
  self.assertGreater(splice(D,D3,U,60).area,0);self.assertTrue(unary_union(list(parts.values())).is_valid);self.assertAlmostEqual(unary_union(list(parts.values())).area,sum(p.area for p in parts.values()),places=6)
 def test_c_filleted_key_repair_retains_gap_and_outer_land(self):
  self.assertEqual(D['C']['key_slot_t_range_mm'],[13.5,20.3]);self.assertEqual(D['C']['tab_abs_t_mm'],26.5)
  self.assertAlmostEqual(26.5-20.3,6.2);self.assertEqual(len(full_ring('C',D,D3,U).interiors),7)
  solids=ring_solids('C',D,D3,U);self.assertLess((solids['P06C']^solids['P06C_K1_P']).volume(),1e-6)
  bad=copy.deepcopy(D);bad['C']['key_slot_t_range_mm'][1]=19.9;bad['C']['tab_abs_t_mm']=26
  broken=ring_solids('C',bad,D3,U);self.assertGreater((broken['P06C']^broken['P06C_K1_P']).volume(),.02)
 def test_no_variant_claims_complete_retention(self):
  for name in CONCEPTS:
   c=PROOF[name]['controls'];self.assertGreater(c['ring_only_restraint']['radial_out']['maximum_intersection_mm3'],1)
   if name=='C':self.assertGreater(c['ring_only_restraint']['cheek_out_t']['maximum_intersection_mm3'],1)
   else:self.assertLess(c['ring_only_restraint']['cheek_out_t']['maximum_intersection_mm3'],1e-6)
   if name!='A':self.assertLess(max(x['volume_mm3'] for x in c['keeper_ejection_intersections']),1e-6)
 def test_c_missing_keeper_detected_as_free_outward_cheek_motion(self):
  solids=ring_solids('C',D,D3,U);solids.pop('P06C_K1_P');face,_=cheek_overlay('C',D,D3,U)
  sweep=p02.cheek_solid(face,7.5,10);self.assertLess(max(x['volume_mm3'] for x in p04.checks(sweep,solids)),1e-6)
  self.assertNotEqual(len(solids),7)

class VariantTests(unittest.TestCase):pass

def contours(self,name):
 for label,p in pieces(name).items():
  self.assertTrue(p.is_valid);self.assertEqual(p.geom_type,'Polygon');self.assertGreater(p.area,0)
  for loop in paths(p):
   self.assertEqual(len(loop),len(set(tuple(v) for v in loop)))
   self.assertTrue(LineString(loop+[loop[0]]).is_simple)
   self.assertTrue(all(math.dist(a,c)>1e-7 for a,c in zip(loop,loop[1:]+loop[:1])))

def exports(self,name):
 for label,p in pieces(name).items():
  folder=PART/'variants'/name;root,svg,loops=poly_from_svg(folder/f'{label}.svg');doc=ezdxf.readfile(folder/f'{label}.dxf')
  self.assertEqual(doc.units,4);lines=[x for x in doc.modelspace().query('LWPOLYLINE') if x.dxf.layer=='CUT_DESIGN_ONLY']
  self.assertTrue(all(x.closed for x in lines));self.assertEqual(len(lines),len(loops))
  dxfloops=[[[v[0],v[1]] for v in x.get_points()] for x in lines];dxf=Polygon(dxfloops[0],dxfloops[1:])
  self.assertLess(svg.hausdorff_distance(p),1e-6);self.assertLess(dxf.hausdorff_distance(p),1e-6)
  self.assertEqual(doc.modelspace().query('TEXT')[0].dxf.layer,'NOT_CUT_DIMENSIONS')
  self.assertIn('DESIGN_ONLY',root.find('{http://www.w3.org/2000/svg}title').text)
  self.assertIn('sha256='+digest(p),root.find('{http://www.w3.org/2000/svg}metadata').text)

def physical_scale(self,name):
 met=dimensions(name)
 for label,p in pieces(name).items():
  folder=PART/'variants'/name;root,_,_=poly_from_svg(folder/f'{label}.svg');ex=met['cut_parts'][label];w,h=ex['artboard_wh_mm']
  self.assertAlmostEqual(float(root.attrib['width'][:-2]),w);self.assertAlmostEqual(float(root.attrib['height'][:-2]),h)
  self.assertEqual(root.attrib['viewBox'].split()[2:],[str(w),str(h)])
  with Image.open(folder/f'{label}.png') as im:
   self.assertLess(abs(im.width-w/25.4*96),1.01);self.assertLess(abs(im.height-h/25.4*96),1.01)
   self.assertIn('1:1mm',im.info['Description'])
  np.testing.assert_allclose(ex['bounds_mm'],p.bounds,atol=1e-6)

def stock_and_necks(self,name):
 met=dimensions(name)
 self.assertGreaterEqual(met['screened_specific_neck_mm'],D['geometric_neck_screen_mm'])
 self.assertGreaterEqual(met['ring_band_width_mm'],6);self.assertGreaterEqual(met['cheek_outer_land_at_expanded_ring_band_mm'],8)
 for p in pieces(name).values():
  x0,y0,x1,y1=p.bounds;self.assertLessEqual(x1-x0+20,440);self.assertLessEqual(y1-y0+20,800)
 self.assertEqual(met['arm_gap_each_side_mm'],.20000000000000018)

def overlays(self,name):
 poly,_=cheek_overlay(name,D,D3,U);original=active_cheek(D3,U)
 self.assertEqual(poly.geom_type,'Polygon');self.assertTrue(poly.is_valid);self.assertLess(poly.difference(original).area,1e-6)
 self.assertLess(poly.area,original.area);self.assertEqual(poly.bounds,original.bounds)
 _,export,_=poly_from_svg(PART/'proposals'/name/'P01-ring-interface-study-v1.svg');self.assertLess(poly.hausdorff_distance(export),1e-6)
 # Each of all four old spacer mortises and Y remains removed, never refilled.
 for hole in original.interiors:self.assertLess(poly.intersection(Polygon(hole)).area,1e-6)

def nominal(self,name):
 solids=assembly(name,D,D5,D4,D3,U,B);pairs=p02.collision_matrix(solids)
 self.assertEqual(len(solids),{'A':28,'B':36,'C':34}[name]);self.assertLess(max(x['intersection_mm3'] for x in pairs),1e-6)
 self.assertEqual(len(pairs),len(solids)*(len(solids)-1)//2)
 self.assertLess(PROOF[name]['maximum_final_intersection_mm3'],1e-6)

def all_six(self,name):
 solids=assembly(name,D,D5,D4,D3,U,B);rings=ring_solids(name,D,D3,U)
 original=assembly(name,D,D5,D4,D3,U,B,False)
 for leg in range(1,4):
  for i in (1,2):
   k=f'L{leg}_P01_{i}';self.assertGreater(sum((original[k]^s).volume() for s in rings.values()),1)
   self.assertLess(sum((solids[k]^s).volume() for s in rings.values()),1e-6)

def motions(self,name):
 early=early_path(name,D,D5,D4,D3,U,B);late=late_paths(name,D,D5,D4,D3,U,B)
 self.assertEqual(early['status'],'PASS_CAD_SPECIFIED_PATH');self.assertGreaterEqual(len(early['steps']),28)
 self.assertEqual(late['status'],'PASS_CAD_SPECIFIED_PATH' if name=='B' else 'BLOCKED')
 self.assertGreater(early['checks'],171)
 if name=='B':
  self.assertEqual(len(late['steps']),12)
  self.assertEqual(late['steps'][0]['end_offset_xyz_mm'],[0,0,6.4]);self.assertEqual(late['steps'][1]['end_offset_xyz_mm'],[0,0,0])
 else:self.assertTrue(all(s['status']=='BLOCKED' for s in late['steps']))
 self.assertAlmostEqual(early['maximum_intersection_mm3'],PROOF[name]['early_path']['maximum_intersection_mm3'],delta=1e-6)

def negatives(self,name):
 c=controls(name,D,D5,D4,D3,U,B)
 self.assertLess(max(x['volume_mm3'] for x in c['S3_at200_intersections']),1e-6)
 for key in ('hypothetical_S3_at245_max_mm3','swapped_tab_displaced2mm_mm3','incorrect_ring_z_mm3','out_of_plane5deg_mm3'):self.assertGreater(c[key],1e-6)
 # B loading window deliberately admits 6.8 geometrically; schema must reject the wrong stock.
 if name!='B':self.assertGreater(c['thickness6p8_mm3'],1e-6)
 else:self.assertLess(c['thickness6p8_mm3'],1e-6)
 self.assertGreater(PROOF[name]['original_cheek_maximum_mm3'],1)
 # Explicitly under-sized proposed cut: remove0.3 from each cut edge, proving no-clearance rejection.
 face,cut=cheek_overlay(name,D,D3,U);tight=active_cheek(D3,U).difference(cut.buffer(-.3))
 tight_solid=p02.cheek_solid(tight,7.5,6)
 self.assertGreater(sum((tight_solid^s).volume() for s in ring_solids(name,D,D3,U).values()),1e-6)

def missing_tab(self,name):
 p=full_ring(name,D,D3,U);j=sections(D,D3,U)['joint_center_r_mm'];broken=p.difference(box(j-20,7.5,j+20,40))
 self.assertGreater(p.area-broken.area,1);self.assertNotEqual(digest(p),digest(broken))
 # Exact same source digest is enforced by export/metadata tests, so the deficient tongue cannot substitute.
 self.assertGreater(p.intersection(box(j-3,8,j+3,13)).area,20);self.assertEqual(broken.intersection(box(j-3,8,j+3,13)).area,0)

def bom_glb(self,name):
 met=dimensions(name);solids=assembly(name,D,D5,D4,D3,U,B)
 scene=trimesh.load(PART/'assembly'/f'{name}-conditional-DESIGN_ONLY.glb',force='scene')
 self.assertEqual(set(scene.graph.nodes_geometry),set(solids));self.assertEqual(len(solids),met['bom']['total_real_bodies'])
 self.assertEqual(sum(ex['quantity'] for ex in met['cut_parts'].values()),met['bom']['added_p06_count'])
 with (PART/'BOM-v1.csv').open() as handle:rows=[r for r in csv.DictReader(handle) if r['concept']==name]
 self.assertEqual({r['part_id']:int(r['quantity']) for r in rows},{k:ex['quantity'] for k,ex in met['cut_parts'].items()})
 self.assertTrue(all(r['release']=='DESIGN_ONLY' and r['nominal_thickness_mm']=='6' for r in rows))
 for k in scene.graph.nodes_geometry:
  transform,g=scene.graph[k];m=scene.geometry[g].copy();m.apply_transform(transform);self.assertTrue(m.is_watertight)
  self.assertGreater(m.volume,0);self.assertAlmostEqual(m.volume*1e9/solids[k].volume(),1,delta=1e-5)
  np.testing.assert_allclose(m.bounds*1000,np.asarray(solids[k].bounding_box()).reshape(2,3),atol=4e-5)

def vertical(self,name):
 c=PROOF[name]['controls'];self.assertEqual(c['ring_slab_S3_gap_mm'],39)
 self.assertAlmostEqual(c['S3_vertical_gap_mm'],{'A':39,'B':35.8,'C':32}[name],delta=1e-6)
 solids=ring_solids(name,D,D3,U)
 for s in solids.values():self.assertGreaterEqual(s.bounding_box()[2],225-1e-6);self.assertLessEqual(s.bounding_box()[5],265+1e-6)
 self.assertGreater(c['Y_vertical_gap_mm'],140)

for name in CONCEPTS:
 for fn in (contours,exports,physical_scale,stock_and_necks,overlays,nominal,all_six,motions,negatives,missing_tab,bom_glb,vertical):
  setattr(VariantTests,'test_'+name+'_'+fn.__name__,lambda self,n=name,f=fn:f(self,n))
if __name__=='__main__':unittest.main(verbosity=2)
