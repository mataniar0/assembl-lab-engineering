"""Tier2 affected IF01/02/09/14 and bounded consumption of unchanged approved solids."""
import hashlib,json,subprocess,sys,unittest
from pathlib import Path
import numpy as np,trimesh
from shapely.geometry import Point,Polygon,LineString
PART=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PART/'src'))
from model import *
D,D5,D4,D3,U,B=inputs()
class FocusedIntegration(unittest.TestCase):
 def test_protected_336_files_byte_equal_to_base(self):
  refs=json.loads((PART/'src/upstream-sha256.json').read_text());self.assertEqual(len(refs),336)
  for name,sha in refs.items():
   actual=(ROOT/name).read_bytes();self.assertEqual(hashlib.sha256(actual).hexdigest(),sha,name)
   self.assertEqual(actual,subprocess.check_output(['git','show',D['source_commit']+':'+name],cwd=ROOT),name)
 def test_selected_27_body_consumption_matches_reviewed_glb(self):
  solids=p05.assembly('A',D5,D4,D3,U,B);self.assertEqual(len(solids),27)
  scene=trimesh.load(PROJECT/'parts/P05/assembly/A-baseline-27-DESIGN_ONLY.glb',force='scene')
  self.assertEqual(set(scene.graph.nodes_geometry),set(solids))
  for k in scene.graph.nodes_geometry:
   transform,g=scene.graph[k];m=scene.geometry[g].copy();m.apply_transform(transform)
   self.assertAlmostEqual(m.volume*1e9/solids[k].volume(),1,delta=1e-5)
 def test_IF01_all_four_spacers_and_mortises_unchanged(self):
  stations=p02.stations(U);self.assertEqual([s['z_mm'] for s in stations],[35,90,200,390])
  self.assertEqual([s['part'] for s in stations],['P02B','P02','P02','P02'])
  original=p05.assembly('A',D5,D4,D3,U,B)
  for name in CONCEPTS:
   current=assembly(name,D,D5,D4,D3,U,B)
   for leg in range(1,4):
    for station in stations:
     key=f'L{leg}_{station["id"]}';self.assertLess((current[key]-original[key]).volume(),1e-6)
     self.assertLess((original[key]-current[key]).volume(),1e-6)
 def test_IF02_y_profile_and_current_mortises_consumed(self):
  y=p03.y_profile('A_COMPACT_CLOSED',D3);self.assertTrue(y.is_valid)
  self.assertLess(max(np.linalg.norm(p) for p in y.exterior.coords),90)
  base=p05.assembly('A',D5,D4,D3,U,B)
  for name in CONCEPTS:
   model=assembly(name,D,D5,D4,D3,U,B);self.assertAlmostEqual(model['P03'].volume(),base['P03'].volume())
   self.assertEqual(model['P03'].bounding_box()[2::3],(407.0,413.0))
 def test_IF09_proposed_cuts_preserve_original_only_in_P06(self):
  original=active_cheek(D3,U)
  for name in CONCEPTS:
   overlay,cut=cheek_overlay(name,D,D3,U)
   self.assertLess(overlay.symmetric_difference(original.difference(cut)).area,1e-6)
   self.assertEqual(overlay.bounds,original.bounds)
   self.assertEqual(json.loads((PART/'proposals'/name/'P01-ring-interface-study-v1-dimensions.json').read_text())['approval'],'NOT_APPROVED')
 def test_IF14_actual_contact_hull_and_original_feet_preserved(self):
  s=support(D3,U);self.assertEqual(s['foot_r_interval_mm'],[222,258]);self.assertAlmostEqual(s['total_area_mm2'],1296,places=6)
  self.assertAlmostEqual(s['minimum_origin_to_hull_edge_mm'],140.691342951,places=6)
  for name in CONCEPTS:
   cheek,_=cheek_overlay(name,D,D3,U)
   self.assertEqual(cheek.intersection(LineString([[-100,0],[400,0]])).bounds,(222,0,258,0))
  self.assertLess(s['minimum_origin_to_hull_edge_mm'],s['top_radius_mm'])
 def test_selected_y_first_18_stages_171_exact_sweeps(self):
  proof=p03.y_first('A_COMPACT_CLOSED',D3,U,B)
  self.assertEqual(proof['moving_stages'],18);self.assertEqual(proof['checks'],171)
  self.assertLess(proof['maximum_intersection_mm3'],1e-6)
 def test_bounded_upper_interfaces_top_budget_and_authorities(self):
  for path,token in [('P01/P01-SELECTION.md','SOFT_CURVE'),('P02/CTB-002-SELECTION.md','B_THROUGH_ADHESIVE'),('P03/CTB-003-SELECTION.md','Y_FIRST'),('P04/CTB-004-SELECTION.md','NO_HOLE'),('P05/CTB-005-SELECTION.md','A_RELIEVED_BOND')]:
   self.assertIn(token,(PROJECT/'parts'/path).read_text())
  self.assertEqual(D4['layers_z_mm'],{'P04L':[456,462],'P04U':[480,486]});self.assertEqual(500-450,50)
  for layer in ('P04L','P04U'):self.assertTrue(p04.disk('A',layer,D4,D3,U,B).contains(Point(0,0)))
if __name__=='__main__':unittest.main(verbosity=2)
