"""Actual finite P05 materials, exports, baseline/proposal distinctions and continuous paths."""
import copy,csv,hashlib,itertools,json,math,subprocess,sys,unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import ezdxf,numpy as np,trimesh
from PIL import Image
from jsonschema import ValidationError
from shapely.geometry import Polygon,Point,LineString,box
from shapely.affinity import rotate
PART=Path(__file__).resolve().parents[1];sys.path.insert(0,str(PART/'src'))
from model import *
D,D4,D3,U,B=inputs()
PROOFS=json.loads((PART/'assembly/proofs.json').read_text())


def data(name):return json.loads((PART/'variants'/name/'P05-dimensions.json').read_text())
def svg(path):
    root=ET.parse(path).getroot();cut=root.find('.//{http://www.w3.org/2000/svg}g[@id="CUT"]')
    loops=[[[float(x) for x in s.split(',')] for s in e.attrib['points'].split()] for e in cut.iter() if e.tag.endswith('polygon')]
    return root,loops,Polygon(loops[0],loops[1:])


class GlobalTests(unittest.TestCase):
    def test_schema_rejects_unapproved_dimensions_measurements_and_count(self):
        schema=json.loads((PART/'src/design.schema.json').read_text())
        for key,value in [('rib_thickness_mm',0),('angles_deg',[0,120,240]),('measured_kerf_mm',.1),('core_z_mm',[456,500])]:
            wrong=copy.deepcopy(D);wrong[key]=value
            with self.assertRaises(ValidationError):Draft202012Validator(schema).validate(wrong)

    def test_protected_bytes_all_259_equal_approved_base(self):
        refs=json.loads((PART/'src/upstream-sha256.json').read_text());self.assertEqual(len(refs),259)
        for name,sha in refs.items():
            actual=(ROOT/name).read_bytes();self.assertEqual(hashlib.sha256(actual).hexdigest(),sha)
            self.assertEqual(actual,subprocess.check_output(['git','show',D['source_commit']+':'+name],cwd=ROOT),name)

    def test_twentyone_actual_base_solids_match_reviewed_glb(self):
        solids=existing(D4,D3,U,B);self.assertEqual(len(solids),21)
        scene=trimesh.load(PROJECT/'parts/P04/variants/A/actual-21-body-DESIGN_ONLY.glb',force='scene')
        self.assertEqual(set(solids),set(scene.graph.nodes_geometry))
        for node in scene.graph.nodes_geometry:
            transform,g=scene.graph[node];mesh=scene.geometry[g].copy();mesh.apply_transform(transform)
            self.assertAlmostEqual(mesh.volume*1e9/solids[node].volume(),1,delta=1e-5)

    def test_selected_source_authorities_and_no_center_hole(self):
        self.assertEqual(D['selected_sources'],['SOFT_CURVE','B_THROUGH_ADHESIVE','A_COMPACT_CLOSED','Y_FIRST','A_RIM_OPEN','NO_HOLE'])
        selection=(PROJECT/'parts/P04/CTB-004-SELECTION.md').read_text();self.assertIn('A_RIM_OPEN / NO_HOLE',selection)
        for layer in ('P04L','P04U'):self.assertTrue(disk('A',layer,D,D4,D3,U,B).contains(Point(0,0)))

    def test_exact_six_added_ribs_no_hidden_hardware(self):
        with (PART/'BOM-v1.csv').open() as file:rows=list(csv.DictReader(file))
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['part_id'],'P05');self.assertEqual(rows[0]['quantity'],'6')
        self.assertEqual(rows[0]['thickness_mm'],'6');self.assertEqual(rows[0]['release'],'DESIGN_ONLY')
        for name in CONCEPTS:self.assertEqual(len(assembly(name,D,D4,D3,U,B)),27)

    def test_core_and_top_budget_and_null_physical_measurements(self):
        self.assertEqual(D['core_z_mm'],[456,494]);self.assertEqual(494-456,38)
        self.assertEqual(D4['layers_z_mm'],{'P04L':[456,462],'P04U':[480,486]})
        self.assertEqual(480-462,18);self.assertEqual(480-456,24);self.assertEqual(500-450,50)
        self.assertEqual(488-486,2)
        for key in ('measured_thickness_mm','measured_kerf_mm','adhesive_specification'):self.assertIsNone(D[key])

    def test_complete_upstream_y_first_recheck_171_continuous_checks(self):
        evidence=p03.y_first('A_COMPACT_CLOSED',D3,U,B)
        self.assertEqual(evidence['moving_stages'],18);self.assertEqual(evidence['checks'],171)
        self.assertLess(evidence['maximum_intersection_mm3'],1e-6)
        saved=json.loads((PART/'assembly/upstream-y-first-recheck.json').read_text())
        self.assertEqual(saved['checks'],171);self.assertEqual(saved['status'],'PASS_CAD_LOCAL_BASE_PATH')

    def test_handoff_preserves_dependent_claims_and_two_rim_options(self):
        text=(PART/'CTB-007-008-HANDOFF.md').read_text()
        for token in ('IF-06','IF-07','IF-08','IF-12','B01','B02','B06','B10','B11','OPTION-1','OPTION-2','NOT_RUN','NO_HOLE'):self.assertIn(token,text)


class VariantTests(unittest.TestCase):pass
class ProposalTests(unittest.TestCase):pass


def outline(self,name):
    p=rib(name,D);root,loops,out=svg(PART/'variants'/name/'P05.svg')
    self.assertTrue(p.is_valid);self.assertEqual(p.geom_type,'Polygon');self.assertEqual(len(p.interiors),0)
    self.assertEqual(p.bounds,(81 if name=='A' else 82,456,169,494))
    self.assertLess(p.hausdorff_distance(out),1e-6);self.assertLess(p.symmetric_difference(out).area,p.length*math.sqrt(2)*.5e-6+1e-8)
    for a,c in zip(list(p.exterior.coords),list(p.exterior.coords)[1:]):self.assertGreater(math.dist(a,c),1e-7)
    self.assertEqual(len(loops[0]),len(set(tuple(v) for v in loops[0])))


def necks(self,name):
    m=data(name)
    self.assertTrue(all(v>=6 for v in m['neck_screening_dimensions'].values()))
    p=rib(name,D)
    if name=='A':
        self.assertGreater(m['neck_screening_dimensions']['upper_cap_envelope_budget_mm'],7)
        edge=p.intersection(LineString([[81,450],[81,500]]))
        spans=sorted(s.length for s in edge.geoms if s.geom_type=='LineString')
        np.testing.assert_allclose(spans,[6.6,22.6],atol=1e-6)
        self.assertAlmostEqual(m['neck_screening_dimensions']['upper_inner_edge_span_mm'],spans[0])
    if name in ('B','C'):
        self.assertGreaterEqual(sum(c-a for a,c in section_intervals(p,459)),6+72)
    if name=='C':
        flat=[math.dist(a,c) for a,c in zip(list(p.exterior.coords),list(p.exterior.coords)[1:]) if abs(a[1]-479.6)<1e-6 and abs(c[1]-479.6)<1e-6]
        self.assertAlmostEqual(sum(flat),.4,places=6)


def six_instances(self,name):
    solids=rib_solids(name,D);master=solids['P05_1'];self.assertEqual(len(solids),6)
    for (key,s),angle in zip(solids.items(),D['angles_deg']):
        back=p03.rotation(s,-angle);self.assertAlmostEqual((back^master).volume()/master.volume(),1,delta=1e-7)
        self.assertGreater(s.volume(),18000);self.assertEqual(s.bounding_box()[2],456);self.assertEqual(s.bounding_box()[5],494)
    self.assertEqual(data(name)['angles_deg'],[0,60,120,180,240,300]);self.assertEqual(data(name)['instances'],6)


def cut_export(self,name):
    folder=PART/'variants'/name;m=data(name);root,loops,poly=svg(folder/'P05.svg');doc=ezdxf.readfile(folder/'P05.dxf')
    self.assertEqual(doc.units,4);entities=[e for e in doc.modelspace() if e.dxf.layer.startswith('CUT')]
    self.assertEqual(len(entities),1)
    for e,pts in zip(entities,loops):
        self.assertTrue(e.closed);self.assertEqual(e.dxftype(),'LWPOLYLINE');np.testing.assert_allclose(np.array(e.get_points())[:,:2],pts,atol=1e-6)
    self.assertTrue(any(e.dxf.layer=='NOT_CUT_DIMENSIONS' and e.dxftype()=='TEXT' and 'grain' in e.dxf.text for e in doc.modelspace()))
    self.assertEqual(len(doc.audit().errors),0)


def physical_svg(self,name):
    root,loops,p=svg(PART/'variants'/name/'P05.svg');m=data(name);vb=[float(v) for v in root.attrib['viewBox'].split()]
    self.assertEqual(float(root.attrib['width'][:-2]),vb[2]);self.assertEqual(float(root.attrib['height'][:-2]),vb[3])
    text=ET.tostring(root).decode();self.assertIn('scale(1,-1)',text);self.assertIn(m['sha256'],text);self.assertIn('DESIGN_ONLY',text);self.assertIn('grain',text)
    self.assertLessEqual(p.bounds[2]-p.bounds[0]+20,440);self.assertLessEqual(p.bounds[3]-p.bounds[1]+20,800)


def raster(self,name):
    m=data(name);ex=m['export'];p=rib(name,D);im=Image.open(PART/'variants'/name/'P05.png');w,h=ex['artboard_wh_mm']
    self.assertLessEqual(abs(im.width-w/25.4*96),1);self.assertLessEqual(abs(im.height-h/25.4*96),1);self.assertLess(abs(im.info['dpi'][0]-96),.02)
    self.assertIn(m['sha256'],im.info['Description']);pix=np.asarray(im.convert('RGB'));self.assertGreater(np.count_nonzero(pix.min(axis=2)<100),500)
    for x,y in paths(p)[0][::max(1,len(paths(p)[0])//60)]:
        px=int((x-(p.bounds[0]-20))/w*im.width);py=int((p.bounds[3]+20-y)/h*im.height)
        self.assertLess(pix[max(0,py-2):py+3,max(0,px-2):px+3].min(),150)


def baseline_static(self,name):
    pairs=p02.collision_matrix(assembly(name,D,D4,D3,U,B));self.assertEqual(len(pairs),351)
    overlaps=[r for r in pairs if r['intersection_mm3']>1e-6]
    if name=='B':
        self.assertEqual(len(overlaps),6);self.assertTrue(all('P04U' in (r['a'],r['b']) for r in overlaps));self.assertAlmostEqual(sum(r['intersection_mm3'] for r in overlaps),172.8,places=4)
    else:self.assertLess(max(r['intersection_mm3'] for r in pairs),1e-6)


def baseline_path(self,name):
    evidence=install(name,D,D4,D3,U,B);self.assertEqual(evidence['continuous_checks'],207)
    self.assertEqual([e['moving'] for e in evidence['steps'][:3]],['P07B_ENVELOPE','P04L','P04U'])
    self.assertEqual(evidence['status'],'BLOCKED' if name=='B' else 'PASS_CAD_SPECIFIED_PATH')
    if name!='B':self.assertLess(evidence['maximum_intersection_mm3'],1e-6)
    else:self.assertGreater(evidence['maximum_intersection_mm3'],20)


def controls(self,name):
    proposed=name!='A';c=access_and_controls(name,D,D4,D3,U,B,proposed)
    for key in ('uncut_38mm_web_mm3','oversize_6p8mm_mm3','rotated_rib_5deg_mm3','radial_insertion_after_wall_mm3','lower_after_upper_mm3','bottom_skin_after_disks_mm3','lift_after_top_closure_mm3'):self.assertGreater(c[key],1,key)
    if name=='A':self.assertGreater(c['upper_after_rib_mm3'],1)
    else:self.assertLess(c['upper_after_rib_mm3'],1e-6)


def lock_access(self,name):
    c=PROOFS[name]['baseline' if name=='A' else 'proposal']['controls_and_access']
    self.assertEqual(len(c['tool_reservations']),6)
    for t in c['tool_reservations']:
        self.assertLess(max(x['volume_mm3'] for x in t['open_top']),1e-6)
        self.assertGreater(t['closed_top'][0]['volume_mm3'],50);self.assertEqual(t['stop_z_mm'],488.5)


def bond_and_skin(self,name):
    m=data(name);p=rib(name,D)
    for layer,z in D4['layers_z_mm'].items():
        area=2*p.intersection(box(0,z[0],math.sqrt(95**2-3.2**2),z[1])).area
        self.assertAlmostEqual(m['disk_bond_reservations'][layer]['broadside_geometric_reservation_area_both_faces_mm2'],area,places=6)
        self.assertEqual(m['disk_bond_reservations'][layer]['actual_bonded_area_mm2'],0)
    for key,z in [('P07B',456),('P07T',494)]:
        span=sum(c-a for a,c in section_intervals(p,z));self.assertGreater(span,70)
        self.assertAlmostEqual(m['skin_reservations'][key]['nominal_boundary_area_mm2'],span*6,places=5)
    self.assertAlmostEqual(m['outer_min_radial_gap_to_cylindrical_rim_mm'],171-math.hypot(169,3));self.assertGreater(m['outer_min_radial_gap_to_cylindrical_rim_mm'],1.97)
    self.assertIn('not tested',m['grain'])


def baseline_retention(self,name):
    r=retention(name,D,D4,D3,U,B,False)
    if name=='B':self.assertFalse(r['valid_start']);self.assertNotIn('radial_out',r)
    else:self.assertTrue(r['valid_start']);self.assertEqual(r['radial_out']['status'],'FREE_TRANSLATION');self.assertLess(r['radial_out']['maximum_intersection_mm3'],1e-6)


def glb_audit(self,name):
    configs=[False,True] if name!='A' else [False]
    for proposal in configs:
        filename=f'{name}-proposed-27-CR_REQUIRED.glb' if proposal else f'{name}-baseline-27-'+('BLOCKED.glb' if name=='B' else 'DESIGN_ONLY.glb')
        scene=trimesh.load(PART/'assembly'/filename,force='scene');solids=assembly(name,D,D4,D3,U,B,proposal)
        self.assertEqual(set(scene.graph.nodes_geometry),set(solids));self.assertEqual(len(scene.geometry),27)
        for node in scene.graph.nodes_geometry:
            transform,g=scene.graph[node];p=scene.geometry[g].copy();p.apply_transform(transform)
            self.assertTrue(p.is_watertight);self.assertGreater(p.volume,0);self.assertAlmostEqual(p.volume*1e9/solids[node].volume(),1,delta=1e-5)
            self.assertLess(np.max(np.abs(p.bounds*1000-np.array(solids[node].bounding_box()).reshape(2,3))),.001)


def source_data(self,name):
    m=data(name);self.assertEqual(m['sha256'],digest(rib(name,D)));self.assertEqual(m['source_commit'],D['source_commit'])
    self.assertEqual(m['nominal_height_mm'],38);self.assertEqual(m['nominal_thickness_mm'],6);self.assertIsNone(m['kerf_mm']);self.assertIsNone(m['load_rating'])
    self.assertEqual(m['status_fit_to_original'],'BLOCKED_UPPER_DISK' if name=='B' else 'PASS_CAD_NO_RADIAL_RETAINER')


def proposal_material(self,name):
    for layer in ('P04L','P04U'):
        p=disk(name,layer,D,D4,D3,U,B,True)
        self.assertTrue(p.is_valid);self.assertEqual(p.geom_type,'Polygon');self.assertTrue(p.contains(Point(0,0)))
        changed=layer in D[name]['proposed_slots_r_mm'];self.assertEqual(len(p.interiors),12 if changed else 6)
        if changed:
            for h in p04.tongue_slots(D4,D3,U,B):self.assertLess(p.intersection(h).area,1e-6)
            self.assertGreater(min(Polygon(h).distance(p.exterior) for h in p.interiors),6)
        else:self.assertLess(p.symmetric_difference(p04.disk('A',layer,D4,D3,U,B)).area,1e-8)


def proposal_exports(self,name):
    for layer in ('P04L','P04U'):
        label=layer+('-v2-proposal' if layer in D[name]['proposed_slots_r_mm'] else '-v1-reference');f=PART/'proposals'/name
        root,loops,p=svg(f/f'{label}.svg');doc=ezdxf.readfile(f/f'{label}.dxf');ent=[e for e in doc.modelspace() if e.dxf.layer.startswith('CUT')]
        self.assertEqual(doc.units,4);self.assertEqual(len(ent),len(loops))
        for e,loop in zip(ent,loops):self.assertTrue(e.closed);np.testing.assert_allclose(np.array(e.get_points())[:,:2],loop,atol=1e-6)
        self.assertLess(p.hausdorff_distance(disk(name,layer,D,D4,D3,U,B,True)),1e-6)
        meta=json.loads((f/f'{label}-dimensions.json').read_text());self.assertEqual(meta['release'],'CR_REQUIRED_NOT_APPROVED')


def proposal_static(self,name):
    pairs=p02.collision_matrix(assembly(name,D,D4,D3,U,B,True));self.assertEqual(len(pairs),351);self.assertLess(max(r['intersection_mm3'] for r in pairs),1e-6)


def proposal_path(self,name):
    evidence=install(name,D,D4,D3,U,B,True);self.assertEqual(evidence['status'],'PASS_CAD_SPECIFIED_PATH');self.assertEqual(evidence['continuous_checks'],207)
    self.assertEqual(evidence['steps'][1]['moving'],'P04L');self.assertEqual(evidence['steps'][-1]['moving'],'P04U')
    self.assertEqual([s['moving'] for s in evidence['steps'][2:-1]],[f'P05_{i+1}' for i in range(6)])
    self.assertLess(evidence['maximum_intersection_mm3'],1e-6)


def proposal_capture(self,name):
    r=retention(name,D,D4,D3,U,B,True);self.assertTrue(r['valid_start'])
    for trial in ('radial_out','radial_in','lift','lower'):self.assertEqual(r[trial]['status'],'BLOCKED_TRANSLATION');self.assertGreater(r[trial]['maximum_intersection_mm3'],1)
    self.assertIn('no 6DOF',r['claim']);self.assertIn('CTB008',r['claim'])


def proposal_cr_is_not_approval(self,name):
    text=(PART/'proposals'/name/'CHANGE-PROPOSAL.md').read_text()
    for token in ('CR_REQUIRED','NOT_APPROVED','P04L','IF-06','IF-08','B01','B06','B10','CTB-008'):self.assertIn(token,text)

for name in CONCEPTS:
    for f in (outline,necks,six_instances,cut_export,physical_svg,raster,baseline_static,baseline_path,controls,lock_access,bond_and_skin,baseline_retention,glb_audit,source_data):
        setattr(VariantTests,f'test_{name}_{f.__name__}',lambda self,n=name,f=f:f(self,n))
for name in ('B','C'):
    for f in (proposal_material,proposal_exports,proposal_static,proposal_path,proposal_capture,proposal_cr_is_not_approval):
        setattr(ProposalTests,f'test_{name}_{f.__name__}',lambda self,n=name,f=f:f(self,n))

if __name__=='__main__':unittest.main(verbosity=2)
