"""Tier2 bounded consumption of unchanged upstream and affected tabletop interfaces."""
import hashlib,json,subprocess,sys,unittest
from pathlib import Path
import numpy as np,trimesh
PART=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PART/'src'))
from model import *
D,D5,D4,D3,U,B=inputs()
class FocusedIntegration(unittest.TestCase):
 def test_439_upstream_files_match_main_baseline_byte_for_byte(self):
  refs=json.loads((PART/'src/upstream-sha256.json').read_text());self.assertEqual(len(refs),439)
  for name,sha in refs.items():
   content=(ROOT/name).read_bytes();self.assertEqual(hashlib.sha256(content).hexdigest(),sha,name)
   self.assertEqual(content,subprocess.check_output(['git','show',D['source_commit']+':'+name],cwd=ROOT),name)
 def test_current_27_bodies_match_reviewed_P05A_export(self):
  current=existing(D5,D4,D3,U,B);self.assertEqual(len(current),27)
  scene=trimesh.load(PROJECT/'parts/P05/assembly/A-baseline-27-DESIGN_ONLY.glb',force='scene')
  self.assertEqual(set(current),set(scene.graph.nodes_geometry))
  for k in scene.graph.nodes_geometry:
   trans,g=scene.graph[k];m=scene.geometry[g].copy();m.apply_transform(trans)
   self.assertAlmostEqual(m.volume*1e9/current[k].volume(),1,delta=1e-5)
 def test_IF03_uses_pre_ring_cheeks_all_spacers_and_six_slots(self):
  face,_=p03.cheek('A_COMPACT_CLOSED',D3,U);pre=existing(D5,D4,D3,U,B)
  self.assertEqual([s['z_mm'] for s in p02.stations(U)],[35,90,200,390])
  self.assertEqual(len([k for k in pre if '_S' in k]),12)
  for n in CONCEPTS:
   allparts=assembly(n,D,D5,D4,D3,U,B)
   for k in pre:
    if 'P01' in k:self.assertAlmostEqual(allparts[k].volume(),pre[k].volume())
   self.assertFalse(any(k.startswith('P06') for k in allparts))
   self.assertEqual(len(skin(n,'P07B',D,D4,D3,U,B).interiors),6)
 def test_IF07_and08_boundaries_use_selected_rib_and_original_disks(self):
  for n in CONCEPTS:
   parts=assembly(n,D,D5,D4,D3,U,B)
   self.assertEqual(len([k for k in parts if k.startswith('P05')]),6)
   for k,z in D4['layers_z_mm'].items():
    self.assertEqual(parts[k].bounding_box()[2::3],tuple(z))
    self.assertAlmostEqual(parts[k].volume(),p02.plate_solid(p04.disk('A',k,D4,D3,U,B),z[0],6).volume())
   for k in ['P07B','P07T']:self.assertEqual(contacts(n,D,D5,D4,D3,U,B)['rib_faces_per_skin'][k]['r_intervals_mm'],[[82,168]])
 def test_IF10_and11_single_part_axis_and_top_budget_are_preserved(self):
  for n in CONCEPTS:
   parts=assembly(n,D,D5,D4,D3,U,B)
   for k in ['P07B','P07T',*[f'P07R{i+1}' for i in range(D[n]['segments'])]]:
    a=parts[k].bounding_box();self.assertGreaterEqual(a[2],450-1e-6);self.assertLessEqual(a[5],500+1e-6)
   for i in range(D[n]['segments']):
    x0,y0,x1,y1=sheet_profile(flat_profile(n,i,D)).bounds;self.assertAlmostEqual(x1-x0,50);self.assertLess(y1-y0+20,800)
 def test_IF12_no_invented_lock_or_access_through_closed_top(self):
  for n in CONCEPTS:
   parts=assembly(n,D,D5,D4,D3,U,B);self.assertFalse(any(k.startswith('P08') for k in parts))
   self.assertEqual(tool_access({k:s for k,s in parts.items() if k!='P07T'},D,D4,D3,U,B)['status'],'PASS_RESERVATION_ONLY')
   self.assertEqual(tool_access(parts,D,D4,D3,U,B)['status'],'BLOCKED')
 def test_source_authorities_and_official_open_states_not_upgraded(self):
  for p,token in [('P01/P01-SELECTION.md','SOFT_CURVE'),('P02/CTB-002-SELECTION.md','B_THROUGH_ADHESIVE'),('P03/CTB-003-SELECTION.md','Y_FIRST'),('P04/CTB-004-SELECTION.md','NO_HOLE'),('P05/CTB-005-SELECTION.md','A_RELIEVED_BOND'),('P06/CTB-006-LEAD-DECISION.md','IF-09_OPEN')]:self.assertIn(token,(PROJECT/'parts'/p).read_text())
  raw=json.loads((PROJECT/'specifications/CTB-000/CTB-000_interfaces.json').read_text())
  status={i['id']:i['status'] for i in raw['interfaces']};self.assertEqual(status['IF-09'],'OPEN');self.assertEqual(status['IF-12'],'OPEN');self.assertEqual(status['IF-10'],'EXPERIMENTAL')
if __name__=='__main__':unittest.main(verbosity=2)
