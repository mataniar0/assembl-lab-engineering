"""P03 artifacts, explicit solid/sweep assertions and deliberate counterexamples."""
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
from jsonschema import ValidationError,Draft202012Validator
from shapely.affinity import rotate,translate
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union

PART=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PART/'src'))
from model import *
D,U,B=inputs()


def exported(name,label):
    directory=PART/'variants'/name
    data=json.loads((directory/f'{label}-dimensions.json').read_text())
    return directory,data,Polygon(data['paths_mm'][0],data['paths_mm'][1:])


def evidence(name):return json.loads((PART/'variants'/name/'mechanical-dimensions.json').read_text())


class ConnectorTests(unittest.TestCase):
    def test_upstream_full_byte_preservation(self):
        hashes=json.loads((PART/'src/upstream-sha256.json').read_text())
        self.assertGreater(len(hashes),100)
        for name,expected in hashes.items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),expected,name)
            source=subprocess.check_output(['git','show',D['source_commit']+':'+name],cwd=ROOT)
            self.assertEqual((ROOT/name).read_bytes(),source,name)

    def test_actual_source_selections_and_frozen_inputs(self):
        self.assertIn('SOFT_CURVE',(PROJECT/'parts/P01/P01-SELECTION.md').read_text())
        self.assertIn('B_THROUGH_ADHESIVE',(PROJECT/'parts/P02/CTB-002-SELECTION.md').read_text())
        self.assertEqual(U['station_z_mm'],[35,90,200,390])
        self.assertEqual(B['frozen']['stock_sheet_mm'],[800,440])
        self.assertEqual((B['frozen']['table_outer_diameter_mm'],B['frozen']['table_height_mm'],B['frozen']['top_total_thickness_mm']),(350,500,50))
        self.assertEqual(len(json.loads((PROJECT/'specifications/CTB-000/CTB-000_interfaces.json').read_text())['interfaces']),14)
        with (PROJECT/'specifications/CTB-000/CTB-000_open_issues.csv').open(encoding='utf-8-sig') as f:self.assertEqual(len(list(csv.DictReader(f))),13)

    def test_negative_zero_thickness(self):
        bad=copy.deepcopy(D);bad['thickness_mm']=0
        validator=Draft202012Validator(json.loads((PART/'src/design.schema.json').read_text()))
        with self.assertRaises(ValidationError):validator.validate(bad)

    def test_negative_94_tip_fails_envelope(self):
        bad=copy.deepcopy(D);bad['variants']['A_COMPACT_CLOSED']['arm_tip_local_r_mm']=94
        p=y_profile('A_COMPACT_CLOSED',bad)
        self.assertGreater(max(math.hypot(x,y) for x,y in p.exterior.coords),90)

    def test_negative_lost_arm_web(self):
        p=y_profile('A_COMPACT_CLOSED',D)
        broken=p.difference(box(38,-30,42,30))
        self.assertNotEqual(broken.geom_type,'Polygon')

    def test_negative_shifted_Y_holes_collides(self):
        face,holes=cheek('A_COMPACT_CLOSED',D,U)
        original,_=p02.cheek('B_THROUGH_ADHESIVE',U)
        bad=original.difference(unary_union([translate(h,xoff=5) for h in holes]))
        solid=p02.cheek_solid(bad,-13.5,6)
        connector=assembly('A_COMPACT_CLOSED',D,U,B)['P03']
        self.assertGreater((solid^connector).volume(),10)

    def test_negative_wrong_cheek_sweep_direction_collides(self):
        face,_=cheek('A_COMPACT_CLOSED',D,U)
        # Wrong entry crosses Y core material outside the closed tab aperture.
        sweep=p02.cheek_solid(face,-13.5,46)
        self.assertGreater((sweep^assembly('A_COMPACT_CLOSED',D,U,B)['P03']).volume(),100)

    def test_negative_thick_Y_plate(self):
        nominal=assembly('A_COMPACT_CLOSED',D,U,B)
        thick=p02.plate_solid(y_profile('A_COMPACT_CLOSED',D),406.6,6.8)
        self.assertGreater((thick^nominal['L1_P01_1']).volume(),1)

    def test_BOM_nineteen_no_hidden_parts(self):
        with (PART/'BOM-v1.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual({r['part_id']:int(r['quantity']) for r in rows},{'P03':1,'P01-Y-mortise-study-v1':6,'P02':9,'P02B':3})
        self.assertEqual(sum(int(r['quantity']) for r in rows),19)

    def test_full_GLTF_nineteen_watertight(self):
        scene=trimesh.load(PART/'assembly/three-leg-base-DESIGN_ONLY.glb',force='scene')
        solids=assembly(D['working_concept'],D,U,B)
        self.assertEqual(set(scene.geometry),set(solids))
        self.assertEqual(len(scene.geometry),19)
        for name,p in scene.geometry.items():
            self.assertTrue(p.is_watertight,name);self.assertGreater(p.volume,0)
            self.assertAlmostEqual(p.volume*1e9/solids[name].volume(),1,delta=1e-5)
        self.assertAlmostEqual(scene.bounds[1,2],.488,places=5)

    def test_all_three_joinery_geometries_differ(self):
        ps=[y_profile(n,D) for n in CONCEPTS]
        for i,p in enumerate(ps):
            for q in ps[:i]:self.assertGreater(p.symmetric_difference(q).area,100)

    def test_no_physical_measurements_invented(self):
        self.assertIsNone(D['actual_stock_mm']);self.assertIsNone(D['measured_kerf_mm'])
        self.assertEqual(D['status'],'DESIGN_ONLY')


def add_cases(name):
    def valid_unique_contours(self):
        for label in ['P03','P01-Y-mortise-study-v1']:
            folder,data,p=exported(name,label)
            self.assertTrue(p.is_valid);self.assertEqual(p.geom_type,'Polygon')
            self.assertTrue(p.buffer(-.01).geom_type=='Polygon')
            for ring in [p.exterior,*p.interiors]:
                self.assertTrue(ring.is_simple);self.assertTrue(ring.is_ring)
                pts=list(ring.coords)
                self.assertEqual(len(set(pts[:-1])),len(pts)-1)
                self.assertGreater(min(math.dist(a,b) for a,b in zip(pts,pts[1:])),.001)

    def Y_one_piece_and_residual_necks(self):
        _,_,p=exported(name,'P03')
        self.assertEqual(len(p.interiors),0)
        self.assertEqual(p.buffer(-3).geom_type,'Polygon')
        for angle in (0,120,240):
            local=rotate(p,-angle,origin=(0,0))
            width=local.intersection(LineString([[40,-100],[40,100]])).length
            self.assertAlmostEqual(width,14.6,places=5)
            self.assertGreaterEqual(width,D['minimum_arm_width_hypothesis_mm'])
        self.assertAlmostEqual(D['arm_core_width_mm']*D['thickness_mm'],87.6)

    def three_identical_arms_and_six_cheeks(self):
        p=y_profile(name,D)
        self.assertLess(p.symmetric_difference(rotate(p,120,origin=(0,0))).area,1e-3)
        parts=assembly(name,D,U,B)
        self.assertEqual(len(parts),19)
        face,_=cheek(name,D,U)
        v=face.area*6
        for leg in (1,2,3):
            for side in (1,2):self.assertAlmostEqual(parts[f'L{leg}_P01_{side}'].volume(),v,places=4)
        self.assertEqual(B['frozen']['leg_angles_deg'],[0,120,240])
        self.assertEqual(B['coordinate_frame']['cheek_center_t_offsets_mm'],[-10.5,10.5])
        self.assertEqual(21-6,15);self.assertEqual(21+6,27)

    def B04_envelope_and_engagement(self):
        result=evidence(name)['metrics']
        self.assertLessEqual(result['maximum_global_radius_mm'],86)
        self.assertGreaterEqual(result['local_end_land_to_r90_mm'],4)
        self.assertEqual(result['tab_through_cheek_depth_mm'],6)
        self.assertAlmostEqual(result['core_gap_each_side_mm'],.2)
        self.assertEqual(result['slot_radial_and_Z_allowance_each_side_mm'],.2)
        self.assertEqual(result['old_overhang_mm'],4)

    def all_final_solid_intersections(self):
        matrix=final_matrix(assembly(name,D,U,B))
        self.assertEqual(len(matrix),171)
        self.assertLess(max(x['intersection_mm3'] for x in matrix),EPS)

    def Y_first_continuous_all_eighteen_stages(self):
        result=y_first(name,D,U,B)
        self.assertEqual(result['status'],'PASS_CAD_LOCAL_BASE_PATH')
        self.assertEqual(result['moving_stages'],18);self.assertEqual(result['checks'],171)
        self.assertLess(result['maximum_intersection_mm3'],EPS)
        moving=[s['moving'] for s in result['steps']]
        self.assertEqual(len(set(moving)),18)
        self.assertEqual(moving[0],'L1_P01_1');self.assertEqual(moving[-1],'L3_P01_2')

    def prebuilt_paths_have_real_obstruction_or_C_pass(self):
        for axis in ['radial','tangential','vertical']:
            result=prebuilt(name,D,U,B,axis)
            self.assertEqual(result['checks'],126)
            if name=='C_OPEN_REMOVABLE' and axis=='radial':
                self.assertEqual(result['status'],'PASS_CAD_REMOVABLE_PATH');self.assertLess(result['maximum_intersection_mm3'],EPS)
            else:
                self.assertEqual(result['status'],'BLOCKED');self.assertGreater(result['maximum_intersection_mm3'],100)

    def simultaneous_central_Y_paths_blocked(self):
        for axis in ['vertical','global_X']:
            result=central_insertion(name,D,U,B,axis)
            self.assertEqual(result['checks'],18);self.assertEqual(result['status'],'BLOCKED')
            self.assertGreater(result['maximum_intersection_mm3'],100)

    def land_web_S4_and_upper_envelopes(self):
        met=metrics(name,D,U,B)
        if name=='C_OPEN_REMOVABLE':
            self.assertFalse(met['cheek_original_outer_preserved'])
            self.assertEqual(met['new_hole_to_outer_land_mm'],[0])
            # Open mouth intentional; remaining outer bridge, not mouth land, is19.8.
            self.assertAlmostEqual(90-max(b for a,b in D['variants'][name]['tabs_r_mm'])-.2,19.8)
        else:
            self.assertTrue(met['cheek_original_outer_preserved'])
            self.assertGreaterEqual(min(met['new_hole_to_outer_land_mm']),6)
        if name=='B_DUAL_CLOSED':self.assertAlmostEqual(met['new_hole_between_web_mm'],9.6)
        self.assertAlmostEqual(min(met['new_hole_to_S4_hole_mm']),13.6)
        self.assertEqual(met['Y_z_mm'],[407,413]);self.assertEqual(met['Y_hole_z_mm'],[406.8,413.2])
        self.assertEqual(met['Y_to_spacer_S4_Z_gap_mm'],14)
        self.assertEqual(met['Y_to_underside_Z_gap_mm'],37)
        self.assertEqual(met['disc_lower_Z_gap_mm'],43);self.assertEqual(met['disc_upper_Z_gap_mm'],67)

    def old_B_mortises_and_tongues_unchanged(self):
        face,_=cheek(name,D,U);old,holes=p02.cheek('B_THROUGH_ADHESIVE',U)
        for h in holes:self.assertEqual(face.intersection(h).area,0)
        for zone in [box(-1000,0,1000,380),box(-1000,440,1000,500)]:
            self.assertEqual(face.intersection(zone).symmetric_difference(old.intersection(zone)).area,0)
        self.assertEqual(face.intersection(box(-1000,225,1000,265)).symmetric_difference(old.intersection(box(-1000,225,1000,265))).area,0)

    def real_DXF_SVG_path_equality(self):
        for label in ['P03','P01-Y-mortise-study-v1']:
            folder,data,p=exported(name,label)
            doc=ezdxf.readfile(folder/f'{label}.dxf');self.assertEqual(doc.units,4)
            audit=doc.audit();self.assertFalse(audit.has_errors);self.assertFalse(audit.has_fixes)
            curves=list(doc.modelspace());nodes=ET.parse(folder/f'{label}.svg').getroot().findall('.//{http://www.w3.org/2000/svg}polygon')
            self.assertEqual(len(curves),len(nodes));self.assertEqual(len(curves),len(data['paths_mm']))
            for c,n,points in zip(curves,nodes,data['paths_mm']):
                self.assertTrue(c.closed);self.assertEqual(c.dxf.elevation,0)
                actual=[[float(x),float(y)] for x,y in c.get_points('xy')]
                svg=[[float(x) for x in pair.split(',')] for pair in n.attrib['points'].split()]
                self.assertEqual(actual,points);self.assertEqual(svg,points)

    def PNG_ink_geometry_units_and_sheet(self):
        for label in ['P03','P01-Y-mortise-study-v1']:
            folder,data,p=exported(name,label)
            w,h=data['padded_wh_mm'];x0,y0,x1,y1=p.bounds;m=data['margin_mm']
            self.assertLessEqual(w,440);self.assertLessEqual(h,800);self.assertEqual(m,10)
            with Image.open(folder/f'{label}.png') as im:
                self.assertIn(data['sha256'],im.info['Description'])
                self.assertAlmostEqual(im.info['dpi'][0],96,delta=.03)
                self.assertAlmostEqual(im.width,w*96/25.4,delta=1.1);self.assertAlmostEqual(im.height,h*96/25.4,delta=1.1)
                ink=np.min(np.asarray(im.convert('RGB')),axis=2)<220
                for ring in data['paths_mm']:
                    for x,y in ring:
                        ix=round((x-x0+m)/w*im.width);iy=round((y1+m-y)/h*im.height)
                        self.assertTrue(ink[max(0,iy-2):iy+3,max(0,ix-2):ix+3].any())

    def source_rebuild_and_layout_consistency(self):
        folder,yd,y=exported(name,'P03');_,cd,c=exported(name,'P01-Y-mortise-study-v1')
        self.assertLess(y.symmetric_difference(y_profile(name,D)).area,1e-4)
        self.assertLess(c.symmetric_difference(cheek(name,D,U)[0]).area,1e-4)
        data=json.loads((folder/'layout-evidence.json').read_text())
        self.assertEqual(data['P03_hash'],digest(y_profile(name,D)))
        self.assertEqual(data['cheek_hash'],digest(cheek(name,D,U)[0]))
        axes=data['axes_bounds']
        for i,(x,y,w,h) in enumerate(axes):
            for x1,y1,w1,h1 in axes[:i]:
                self.assertLess(max(0,min(x+w,x1+w1)-max(x,x1))*max(0,min(y+h,y1+h1)-max(y,y1)),1e-8)

    for label,fn in list(locals().items()):
        if callable(fn):setattr(ConnectorTests,'test_'+name+'_'+label,fn)


for name in CONCEPTS:add_cases(name)
if __name__=='__main__':unittest.main(verbosity=2)
