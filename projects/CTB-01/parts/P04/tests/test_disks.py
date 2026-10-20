"""Read actual exports, test geometry/sweeps and deliberately break each critical interface."""
import copy
import csv
import hashlib
import json
import math
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import ezdxf
import numpy as np
import trimesh
from PIL import Image
from jsonschema import ValidationError
from shapely.geometry import Polygon, Point, LineString, box
from shapely.affinity import rotate

PART=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PART/'src'))
from model import *
D,D3,U,B=inputs()
PROOF=json.loads((PART/'assembly/proofs.json').read_text())


def read(name,layer):
    folder=PART/'variants'/name
    data=json.loads((folder/f'{layer}-dimensions.json').read_text())
    return folder,data,Polygon(data['paths_mm'][0],data['paths_mm'][1:])


class GlobalTests(unittest.TestCase):
    def test_versioned_input_schema_rejects_wrong_gap_and_radius(self):
        schema=json.loads((PART/'src/design.schema.json').read_text())
        for key,value in [('disk_diameter_mm',380),('layers_z_mm',{'P04L':[456,462],'P04U':[486,492]}),('measured_kerf_mm',0.1)]:
            wrong=copy.deepcopy(D);wrong[key]=value
            with self.assertRaises(ValidationError):Draft202012Validator(schema).validate(wrong)

    def test_all_upstream_bytes_equal_reviewed_commit(self):
        refs=json.loads((PART/'src/upstream-sha256.json').read_text());self.assertEqual(len(refs),174)
        for name,sha in refs.items():
            actual=(ROOT/name).read_bytes()
            self.assertEqual(hashlib.sha256(actual).hexdigest(),sha,name)
            self.assertEqual(actual,subprocess.check_output(['git','show',D['source_commit']+':'+name],cwd=ROOT),name)

    def test_real_tongue_extraction_all_six_rotations_and_nose(self):
        extracted=json.loads((PART/'assembly/six-tongues.json').read_text())['tongues'];self.assertEqual(len(extracted),6)
        current,_=p03.cheek('A_COMPACT_CLOSED',D3,U)
        for entry,item in zip(extracted,tongues(D3,U,B)):
            rz=Polygon(entry['rz_loops_mm'][0],entry['rz_loops_mm'][1:])
            self.assertLess(rz.symmetric_difference(current.intersection(box(-1000,450,1000,488))).area,1e-5)
            self.assertEqual(item['solid'].bounding_box()[2:3],(450.0,))
            self.assertEqual(item['t_center_mm'] in (-10.5,10.5),True)
            self.assertEqual([s['z_mm'] for s in entry['samples']],[450,456,462,480,486,487,487.5,488])
            for sample in entry['samples']:
                a,c=sample['r_interval_mm'];self.assertAlmostEqual(a,46 if sample['z_mm']==488 else 45,delta=1 if sample['z_mm']==487.5 else 1e-6)
                self.assertLessEqual(c,69+1e-6)
            self.assertEqual(entry['samples'][-1]['r_interval_mm'],[46,68])

    def test_fifty_mm_budget_full_upper_engagement(self):
        self.assertEqual(B['frozen']['top_total_thickness_mm'],50)
        self.assertEqual(B['derived']['bottom_skin_z_mm'],[450,456]);self.assertEqual(B['derived']['top_skin_z_mm'],[494,500])
        self.assertEqual(D['layers_z_mm']['P04U'][0]-D['layers_z_mm']['P04L'][1],18)
        self.assertEqual(D['layers_z_mm']['P04U'][0]-D['layers_z_mm']['P04L'][0],24)
        self.assertEqual(494-D['layers_z_mm']['P04U'][1],8)
        self.assertEqual(488-D['layers_z_mm']['P04U'][1],2)
        self.assertEqual(494-488,6)

    def test_bom_two_real_parts_and_no_hidden_hardware(self):
        with (PART/'BOM-v1.csv').open() as stream:rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),2)
        self.assertEqual({r['part_id'] for r in rows},{'P04L','P04U'})
        self.assertTrue(all(r['quantity']=='1' and r['thickness_mm']=='6' and r['diameter_mm']=='190' and r['release']=='DESIGN_ONLY' for r in rows))

    def test_clearance_is_not_measured_material_or_kerf(self):
        self.assertIsNone(D['measured_material_thickness_mm']);self.assertIsNone(D['measured_kerf_mm'])
        self.assertAlmostEqual(D['tongue_allowance_t_each_side_mm']*2+6,6.2)
        self.assertAlmostEqual(D['tongue_allowance_radial_each_side_mm']*2+24,24.4)
        self.assertAlmostEqual(D['web_slot_width_mm']-D['web_thickness_mm'],.4)

    def test_selected_upstream_base_and_nineteen_real_bodies(self):
        self.assertEqual(D['approved_sources'],['SOFT_CURVE','B_THROUGH_ADHESIVE','A_COMPACT_CLOSED','Y_FIRST'])
        self.assertEqual(len(base(D3,U,B)),19)
        for file,term in [('P01/P01-SELECTION.md','SOFT_CURVE'),('P02/CTB-002-SELECTION.md','B_THROUGH_ADHESIVE'),('P03/CTB-003-SELECTION.md','A_COMPACT_CLOSED')]:
            self.assertIn(term,(PROJECT/'parts'/file).read_text())
        self.assertEqual([s['z_mm'] for s in p02.stations(U)],[35,90,200,390])

    def test_prospective_web_handoff_counts_and_open_dependencies(self):
        handoff=(PART/'CTB-005-HANDOFF.md').read_text()
        for term in ('CTB-005','38','18','six','DESIGN_ONLY','B01','B06','B10','CTB-008'):self.assertIn(term,handoff)
        for name in CONCEPTS:
            data=PROOF[name]['witness_profiles'];self.assertEqual(sum(p['quantity'] for p in data.values()),6)
            self.assertTrue(all(p['role']=='INTERFACE_WITNESS_NOT_P05_RELEASE' for p in data.values()))


class LayerTests(unittest.TestCase):pass
class VariantTests(unittest.TestCase):pass


def planar(self,name,layer):
    _,data,poly=read(name,layer);model=disk(name,layer,D,D3,U,B)
    self.assertTrue(poly.is_valid);self.assertEqual(poly.geom_type,'Polygon');self.assertGreater(poly.area,26000)
    # Six-decimal coordinate rounding: <=sqrt(2)/2 micromillimetre per vertex.
    self.assertLess(poly.hausdorff_distance(model),1e-6)
    self.assertLess(poly.symmetric_difference(model).area,model.length*math.sqrt(2)*.5e-6+1e-8)
    self.assertLess(max(math.hypot(x,y) for x,y in poly.exterior.coords)-95,1e-6)
    self.assertEqual(data['tongue_hole_count'],6);self.assertEqual(data['web_interface_count'],6)
    self.assertEqual(len(poly.interiors),6+sum(c['family']=='RAIL' for c in web_cuts(name,layer,D))+(1 if data['center_diameter_mm'] else 0))
    w,h=poly.bounds[2]-poly.bounds[0],poly.bounds[3]-poly.bounds[1]
    self.assertLessEqual(w+20,440);self.assertLessEqual(h+20,800)
    self.assertNotEqual(digest(poly),digest(disk(name,'P04U' if layer=='P04L' else 'P04L',D,D3,U,B)))


def tongue_alignment(self,name,layer):
    _,data,poly=read(name,layer);z=D['layers_z_mm'][layer][0];solid=p02.plate_solid(poly,z,6)
    for t,h in zip(tongues(D3,U,B),tongue_slots(D,D3,U,B)):
        self.assertTrue(h.covers(t['xy']));self.assertLess((solid^t['solid']).volume(),1e-6)
        self.assertLess(poly.intersection(t['xy']).area,1e-6)
        self.assertGreater(h.area-t['xy'].area,6)
    self.assertEqual(sorted(t['angle_deg'] for t in tongues(D3,U,B)),[0,0,120,120,240,240])


def lands(self,name,layer):
    _,data,poly=read(name,layer)
    self.assertGreater(min(data['tongue_to_outer_lands_mm']),6)
    self.assertGreater(data['min_tongue_to_tongue_mm'],14)
    self.assertGreater(data['min_tongue_to_web_cut_mm'],6)
    self.assertTrue(all(x>=6 for x in data['closed_web_outer_lands_mm']))
    for r in poly.interiors:self.assertGreater(Polygon(r).distance(poly.exterior),6)
    for a,c in itertools.combinations([Polygon(r) for r in poly.interiors],2):self.assertGreater(a.distance(c),6)


def dxf(self,name,layer):
    folder,data,poly=read(name,layer);doc=ezdxf.readfile(folder/f'{layer}.dxf');self.assertEqual(doc.units,4)
    ent=[e for e in doc.modelspace() if e.dxf.layer.startswith('CUT_')]
    self.assertTrue(all(e.dxftype()=='LWPOLYLINE' and e.closed for e in ent));self.assertEqual(len(ent),len(data['paths_mm']))
    self.assertEqual([e.dxf.layer for e in ent],data['export']['roles'])
    for e,expected in zip(ent,data['paths_mm']):np.testing.assert_allclose(np.array(e.get_points())[:,:2],expected,atol=1e-6)
    self.assertEqual(sum(e.dxf.layer=='CUT_TONGUE' for e in ent),6)
    self.assertEqual(sum(e.dxf.layer=='CUT_WEB' for e in ent),sum(c['family']=='RAIL' for c in web_cuts(name,layer,D)))
    self.assertTrue(any(e.dxftype()=='TEXT' and '190.000 mm' in e.dxf.text for e in doc.modelspace()))
    self.assertFalse(any(e.dxf.layer.startswith('CUT') and e.dxftype() in ('TEXT','LINE','DIMENSION') for e in doc.modelspace()))
    self.assertEqual(len(doc.audit().errors),0)


def svg(self,name,layer):
    folder,data,_=read(name,layer);root=ET.parse(folder/f'{layer}.svg').getroot()
    points=[[[float(x) for x in p.split(',')] for p in e.attrib['points'].split()] for e in root.iter() if e.tag.endswith('polygon')]
    self.assertEqual(len(points),len(data['paths_mm']))
    for actual,expected in zip(points,data['paths_mm']):np.testing.assert_allclose(actual,expected,atol=1e-6)
    vb=[float(x) for x in root.attrib['viewBox'].split()]
    self.assertEqual(float(root.attrib['width'][:-2]),vb[2]);self.assertEqual(float(root.attrib['height'][:-2]),vb[3])
    self.assertIn('scale(1,-1)',ET.tostring(root).decode());self.assertIn('DESIGN_ONLY',ET.tostring(root).decode())
    self.assertIn(data['hash'],ET.tostring(root).decode());self.assertIn('6 tongue24.4x6.2',ET.tostring(root).decode())


def png(self,name,layer):
    folder,data,poly=read(name,layer);im=Image.open(folder/f'{layer}.png');w,h=data['export']['physical_artboard_wh_mm'];dpi=data['export']['raster_dpi']
    self.assertLessEqual(abs(im.width-w/25.4*dpi),1);self.assertLessEqual(abs(im.height-h/25.4*dpi),1)
    self.assertLess(abs(im.info['dpi'][0]-dpi),.02);self.assertIn(data['hash'],im.info['Description'])
    pix=np.asarray(im.convert('RGB'));self.assertGreater(np.count_nonzero(pix.min(axis=2)<100),1000)
    x0,y0,x1,y1=poly.bounds
    for loop in data['paths_mm']:
        for x,y in loop[::max(1,len(loop)//30)]:
            px=int((x-(x0-20))/w*im.width);py=int(((y1+20)-y)/h*im.height)
            self.assertLess(pix[max(0,py-2):py+3,max(0,px-2):px+3].min(),150,(x,y))


def center(self,name,layer):
    _,data,poly=read(name,layer);studies=data['center_study'];self.assertEqual([x['diameter_mm'] for x in studies],[0,24,36])
    self.assertEqual(studies[0]['mode'],'NO_HOLE');self.assertEqual(studies[0]['removed_area_mm2'],0)
    for item in studies:
        self.assertTrue(item['connected_material']);self.assertGreater(item['min_land_to_tongue_mm'],25)
        self.assertGreater(item['min_land_to_web_cut_mm'],60)
        self.assertAlmostEqual(item['removed_area_mm2'],circle(item['diameter_mm']/2,D).area,places=5)
    self.assertEqual(data['center_diameter_mm'],24 if name=='C' and layer=='P04U' else 0)
    self.assertEqual(poly.covers(Point(0,0)),not(name=='C' and layer=='P04U'))


def final_solids(self,name):
    solids=assembly(name,D,D3,U,B);self.assertEqual(len(solids),21)
    pairs=p02.collision_matrix(solids);self.assertEqual(len(pairs),210)
    self.assertLess(max(x['intersection_mm3'] for x in pairs),1e-6)
    self.assertEqual(len(PROOF[name]['final_real_intersections']),210)
    for solid in solids.values():self.assertGreater(solid.volume(),0);self.assertTrue(trimesh.Trimesh(vertices=np.asarray(solid.to_mesh().vert_properties)[:,:3],faces=np.asarray(solid.to_mesh().tri_verts),process=False).is_watertight)


def mating(self,name):
    actual=assembly(name,D,D3,U,B);ws=witness_solids(name,D);self.assertEqual(len(ws),6)
    pairs=[x for x in p02.collision_matrix({**actual,**ws}) if x['a'].startswith('W') or x['b'].startswith('W')]
    self.assertEqual(len(pairs),141);self.assertLess(max(x['intersection_mm3'] for x in pairs),1e-6)
    for angle in range(0,360,60):
        kind=family(name,angle);p=witness(kind,D);self.assertTrue(p.is_valid);self.assertEqual(p.geom_type,'Polygon')
        self.assertEqual(p.bounds,(81,456,169,494));self.assertEqual(p.bounds[3]-p.bounds[1],38)
        folder=PART/'variants'/name
        root=ET.parse(folder/f'witness-{kind}.svg').getroot()
        loops=[[[float(x) for x in s.split(',')] for s in e.attrib['points'].split()] for e in root.iter() if e.tag.endswith('polygon')]
        self.assertLess(Polygon(loops[0],loops[1:]).symmetric_difference(p).area,1e-5)
    self.assertEqual(sum(family(name,a)=='RAIL' for a in range(0,360,60)),0 if name=='A' else 6 if name=='B' else 3)


def disk_paths(self,name):
    p=assembly_paths(name,D,D3,U,B);self.assertEqual(p['real_body_count'],21)
    self.assertEqual([s['moving'] for s in p['disk_stages']],['P07B_ENVELOPE','P04L','P04U'])
    self.assertEqual([len(s['continuous_intersections']) for s in p['disk_stages']],[19,20,21])
    self.assertLess(p['maximum_disk_path_intersection_mm3'],1e-6)
    for s in p['disk_stages']:self.assertEqual(s['method'],'EXACT_TRANSLATION_SWEPT_SOLID');self.assertEqual(s['status'],'PASS_CAD_PATH')


def witness_paths(self,name):
    p=assembly_paths(name,D,D3,U,B);self.assertLess(p['maximum_witness_path_intersection_mm3'],1e-6)
    seq=[s['moving'] for s in p['witness_stages']];self.assertEqual(len(seq),7)
    upper=seq.index('P04U')
    self.assertTrue(all('RAIL' in x for x in seq[:upper]));self.assertTrue(all('OPEN' in x for x in seq[upper+1:]))
    self.assertEqual(upper,0 if name=='A' else 6 if name=='B' else 3)
    for st in p['witness_stages']:
        self.assertEqual(st['status'],'PASS_CAD_PATH');self.assertGreater(st['start_offset_xyz_mm'][2] if 'RAIL' in st['moving'] or st['moving']=='P04U' else sum(v*v for v in st['start_offset_xyz_mm'][:2]),0)


def rejected_orders(self,name):
    p=PROOF[name]
    for st in [p['reverse_order'],p['late_bottom_skin'],*p['rail_after_upper'],*p['upper_after_open'],*p['radial_web_after_wall']]:
        self.assertEqual(st['status'],'BLOCKED');self.assertGreater(st['maximum_intersection_mm3'],1)
    for access in p['upper_access']:
        self.assertLess(max(x['volume_mm3'] for x in access['open_top']),1e-6)
        self.assertGreater(access['closed_top'][0]['volume_mm3'],50)
    self.assertEqual(len(p['upper_access']),6)


def negatives(self,name):
    controls=negative_controls(name,D,D3,U,B)
    for key in ('rotated_disk_10deg','missing_tongue_slot','oversize_tongue_6p6mm','misplaced_web_5deg','uncut_38mm_web'):
        self.assertGreater(controls[key]['intersection_mm3'],1,key)
    self.assertFalse(controls['incorrect_24mm_free_gap']['fixed_layer_contract_matches'])
    self.assertLess(controls['incorrect_24mm_free_gap']['actual_tongue_full_engagement_mm'],6)
    self.assertNotEqual(controls['radius190_error']['candidate_diameter_mm'],190)


def glb(self,name):
    folder=PART/'variants'/name;scene=trimesh.load(folder/'actual-21-body-DESIGN_ONLY.glb',force='scene')
    self.assertEqual(len(scene.geometry),21);self.assertEqual(len(scene.graph.nodes_geometry),21)
    solids=assembly(name,D,D3,U,B)
    for node in scene.graph.nodes_geometry:
        transform,geom=scene.graph[node];p=scene.geometry[geom].copy();p.apply_transform(transform)
        self.assertIn(node,solids);self.assertTrue(p.is_watertight);self.assertGreater(p.volume,0)
        self.assertAlmostEqual(p.volume*1e9/solids[node].volume(),1,delta=1e-5)
        self.assertLess(np.max(np.abs(p.bounds*1000-np.array(solids[node].bounding_box()).reshape(2,3))),.001)


for name in CONCEPTS:
    for layer in ('P04L','P04U'):
        for function in (planar,tongue_alignment,lands,dxf,svg,png,center):
            setattr(LayerTests,f'test_{name}_{layer}_{function.__name__}',lambda self,n=name,l=layer,f=function:f(self,n,l))
    for function in (final_solids,mating,disk_paths,witness_paths,rejected_orders,negatives,glb):
        setattr(VariantTests,f'test_{name}_{function.__name__}',lambda self,n=name,f=function:f(self,n))

if __name__=='__main__':unittest.main(verbosity=2)
