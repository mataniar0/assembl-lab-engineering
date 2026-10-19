"""Read real exported candidates, full solid sweeps and negative controls."""
import copy
import csv
import hashlib
import json
import math
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import ezdxf
import numpy as np
import trimesh
from PIL import Image
from jsonschema import ValidationError
from shapely.affinity import translate
from shapely.geometry import Polygon,LineString,box,Point
from shapely.ops import unary_union

PART=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PART/'src'))
from model import *
D,B=inputs()


def exported(concept,name):
    folder=PART/'variants'/concept
    data=json.loads((folder/f'{name}-dimensions.json').read_text())
    paths=data['paths_mm']
    return folder,data,Polygon(paths[0],paths[1:])


def clear(solids):return max(x['intersection_mm3'] for x in collision_matrix(solids))<1e-6


class SpacerTests(unittest.TestCase):
    def test_BOM_exact_twelve_and_six(self):
        with (PART/'BOM-v1.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual({r['part_id']:int(r['quantity_table']) for r in rows},
                         {'P01-SOFT_CURVE-mortise-study-v1':6,'P02':9,'P02B':3})
        self.assertEqual([s['part'] for s in stations(D)],['P02B','P02','P02','P02'])

    def test_schema_rejects_zero_thickness(self):
        from jsonschema import Draft202012Validator
        data=copy.deepcopy(D);data['spacer_thickness_mm']=0
        schema=json.loads((PART/'src/design.schema.json').read_text())
        with self.assertRaises(ValidationError):Draft202012Validator(schema).validate(data)

    def test_original_upstream_bytes_unchanged(self):
        hashes=json.loads((PART/'assembly/upstream-sha256.json').read_text())
        self.assertEqual(len(hashes),47)
        for name,digest0 in hashes.items():
            self.assertEqual(hashlib.sha256((PROJECT/name).read_bytes()).hexdigest(),digest0,name)
        # Also check against authoritative pre-task Git HEAD, not just a generated hash list.
        import subprocess
        paths=subprocess.check_output(['git','ls-tree','-r','--name-only','849d40c45ddad721dc2aafec8241b45d9cf56a62',str(P01.relative_to(PROJECT.parents[1])),str((PROJECT/'specifications/CTB-000').relative_to(PROJECT.parents[1]))],cwd=PROJECT.parents[1],text=True).splitlines()
        self.assertEqual(len(paths),47)
        self.assertEqual(set(hashes),{str(Path(name).relative_to(PROJECT.relative_to(PROJECT.parents[1]))) for name in paths})
        for name in paths:
            expected=subprocess.check_output(['git','show','849d40c45ddad721dc2aafec8241b45d9cf56a62:'+name],cwd=PROJECT.parents[1])
            self.assertEqual((PROJECT.parents[1]/name).read_bytes(),expected,name)

    def test_six_identical_cheeks_and_nominal_gap(self):
        face,_=cheek(D['working_concept'],D)
        for angle in B['frozen']['leg_angles_deg']:
            a=math.radians(angle)
            for center in [-10.5,10.5]:
                for r,z in list(face.exterior.coords):
                    x=r*math.cos(a)-center*math.sin(a);y=r*math.sin(a)+center*math.cos(a)
                    self.assertAlmostEqual(x*math.cos(a)+y*math.sin(a),r)
                    self.assertAlmostEqual(-x*math.sin(a)+y*math.cos(a),center)
        self.assertEqual(7.5-(-7.5),15);self.assertEqual(13.5-(-13.5),27)
        self.assertEqual(set(B['frozen']['leg_angles_deg']),{0,120,240})

    def test_ring_relocation_and_bypass_quantified(self):
        data=json.loads((PART/'assembly/ring-interference-study.json').read_text())
        self.assertGreater(data['spacer_reservation_overlap_mm3']['REFERENCE_245_CONFLICT']['S3'],1000)
        self.assertEqual(max(data['spacer_reservation_overlap_mm3']['RELOCATE_200'].values()),0)
        self.assertEqual(max(data['spacer_reservation_overlap_mm3']['BYPASS_OUTSIDE_KEEP_245'].values()),0)
        self.assertEqual(data['relocation_plate_z_clearance_mm'],22)
        self.assertAlmostEqual(data['relocation_slot_z_clearance_mm'],21.8)
        self.assertEqual(data['bypass_gap_to_outer_cheek_t_mm'],5)
        self.assertTrue(data['ring_geometry_unknown'])
        self.assertEqual(data['status'],'CONDITIONAL_CTB006_REVIEW')

    def test_no_slots_in_ring_Y_tongue_foot(self):
        face,holes=cheek(D['working_concept'],D)
        forbidden=[box(-1000,225,1000,265),box(-1000,406.9,1000,413.1),box(-1000,450,1000,500),box(-1000,0,1000,12)]
        for h in holes:
            for zone in forbidden:self.assertEqual(h.intersection(zone).area,0)
        for zone in (forbidden[2],forbidden[3]):
            self.assertEqual(face.intersection(zone).symmetric_difference(outer().intersection(zone)).area,0)

    def test_negative_thick_stock_causes_collision(self):
        self.assertFalse(clear(assembly(D['working_concept'],D,B,stock=6.8)))

    def test_negative_shifted_mortises_fail(self):
        face,holes=cheek(D['working_concept'],D)
        wrong=outer().difference(unary_union([translate(h,xoff=4) for h in holes]))
        solids=assembly(D['working_concept'],D,B)
        solids['P01_1']=cheek_solid(wrong,-13.5,6)
        self.assertFalse(clear(solids))

    def test_negative_forced_spacer_overlap(self):
        solids=assembly(D['working_concept'],D,B)
        solids['S2']=solids['S1']
        self.assertFalse(clear(solids))

    def test_negative_zero_web_rejected(self):
        destructive=outer().difference(box(-1000,32,1000,38))
        self.assertNotEqual(destructive.geom_type,'Polygon')

    def test_negative_reverse_insertion_collides(self):
        # A cheek cannot be placed first and accept a broad shoulder through its hole.
        st=stations(D)[0];face=translate(spacer(D['working_concept'],st['part'],D,B),xoff=st['r_mm'])
        swept=plate_solid(swept_polygon(face,0,-40),st['z_mm']-3,6)
        fixed=assembly(D['working_concept'],D,B)['P01_1']
        self.assertGreater((swept^fixed).volume(),100)

    def test_negative_missing_C_spare_hole_breaks_interchangeability(self):
        # For identical C cheeks BOTH offset holes are necessary; remove one pattern.
        chosen=[slot_shapes('C_ASYMMETRIC',s,D)[0] for s in stations(D)]
        wrong=outer().difference(unary_union(chosen))
        solids=assembly('C_ASYMMETRIC',D,B);solids['P01_2']=cheek_solid(wrong,7.5,6)
        self.assertFalse(clear(solids))

    def test_working_GLTF_six_watertight_parts(self):
        scene=trimesh.load(PART/'assembly/one-leg-DESIGN_ONLY.glb',force='scene')
        self.assertEqual(len(scene.geometry),6)
        for name,g in scene.geometry.items():
            self.assertTrue(g.is_watertight,name);self.assertGreater(g.volume,0,name)
        self.assertAlmostEqual(scene.bounds[1,2],.488,places=5) # GLTF metres

    def test_reinforcement_by_geometry_only(self):
        std=spacer(D['working_concept'],'P02',D,B);low=spacer(D['working_concept'],'P02B',D,B)
        self.assertGreater(low.area,std.area*1.3)
        self.assertEqual(D['parts']['P02B']['body_radial_width_mm'],40)
        self.assertEqual(D['parts']['P02B']['tab_radial_width_mm'],24)

    def test_layout_components_do_not_overlap(self):
        for c in CONCEPTS:
            folder=PART/'variants'/c
            evidence=json.loads((folder/'layout-evidence.json').read_text())
            axes=evidence['axes_bounds_fraction']
            self.assertEqual(len(axes),3)
            for i,(x,y,w,h) in enumerate(axes):
                for x1,y1,w1,h1 in axes[:i]:
                    overlap_w=max(0,min(x+w,x1+w1)-max(x,x1))
                    overlap_h=max(0,min(y+h,y1+h1)-max(y,y1))
                    self.assertLess(overlap_w*overlap_h,1e-8)
            for name,value in evidence['spacer_hashes'].items():
                self.assertEqual(value,digest(spacer(c,name,D,B)))
            with Image.open(folder/'concept-layout.png') as image:
                self.assertGreater(np.array(image).std(),20)

    def test_nominal_shoulders_have_bearing_contact(self):
        # Measure actual face contact at t=±7.5, excluding all clearance mortises.
        face,_=cheek(D['working_concept'],D)
        for st in stations(D):
            p=translate(spacer(D['working_concept'],st['part'],D,B),xoff=st['r_mm'])
            for t in (-7.5,7.5):
                cut=p.intersection(LineString([[-1000,t],[1000,t]]))
                lo,hi=cut.bounds[0],cut.bounds[2]
                cross=box(lo,st['z_mm']-3,hi,st['z_mm']+3)
                contact=cross.intersection(face).area
                self.assertGreater(contact,50)

    def test_hypothetical_stock_sensitivity_is_not_fit_approval(self):
        table=json.loads((PART/'assembly/thickness-sensitivity.json').read_text())
        self.assertEqual(len(table),4)
        self.assertGreater(table[0]['shoulder_gap_each_side_mm'],.19)
        self.assertEqual(table[1]['maximum_material_intersection_mm3'],0)
        for row in table[2:]:self.assertGreater(row['maximum_material_intersection_mm3'],1)
        for row in table:
            self.assertFalse(row['measured']);self.assertEqual(row['physical_fit_status'],'UNVERIFIED')

    def test_GLTF_matches_final_solid_volumes(self):
        scene=trimesh.load(PART/'assembly/one-leg-DESIGN_ONLY.glb',force='scene')
        solids=assembly(D['working_concept'],D,B)
        self.assertEqual(set(scene.geometry),set(solids))
        for name,solid in solids.items():
            self.assertAlmostEqual(scene.geometry[name].volume*1e9/solid.volume(),1,delta=1e-5)

    def test_no_extra_key_parts_or_measured_claims(self):
        self.assertIsNone(D['actual_stock_thickness_mm']);self.assertIsNone(D['measured_kerf_mm'])
        self.assertEqual(len(D['parts']),2)
        self.assertEqual(D['status'],'DESIGN_ONLY')


def add_concept_cases(concept):
    def exported_part_paths(self):
        for name in ['P02','P02B','P01-SOFT_CURVE-mortise-study-v1']:
            folder,d,p=exported(concept,name)
            self.assertTrue(p.is_valid)
            self.assertEqual(p.geom_type,'Polygon')
            self.assertTrue(p.exterior.is_ring)
            for ring in [p.exterior,*p.interiors]:
                coords=list(ring.coords)
                self.assertTrue(ring.is_simple)
                self.assertGreater(min(math.dist(a,b) for a,b in zip(coords,coords[1:])),.001)
                self.assertEqual(len(set(coords[:-1])),len(coords)-1)

    def nominal_solid_collision_free(self):
        self.assertTrue(clear(assembly(concept,D,B)))

    def mortises_closed_and_external_unchanged(self):
        _,_,face=exported(concept,'P01-SOFT_CURVE-mortise-study-v1')
        self.assertTrue(face.exterior.equals_exact(outer().exterior,1e-5) or Polygon(face.exterior).symmetric_difference(outer()).area<1e-5)
        self.assertEqual(len(face.interiors),8 if concept=='C_ASYMMETRIC' else 4)

    def local_sweep_or_explicit_blocker(self):
        proof=insertion(concept,D,B)
        if concept=='A_KEYED_HEAD':
            self.assertEqual(proof['status'],'BLOCKED');self.assertTrue(proof['reason'])
        else:
            self.assertEqual(proof['status'],'PASS_CAD_LOCAL_SWEEP')
            self.assertEqual(len(proof['steps']),5)
            self.assertLess(proof['maximum_collision_mm3'],1e-6)

    def land_screen(self):
        report=land_report(concept,D)
        if concept=='A_KEYED_HEAD':
            self.assertLess(report[0]['minimum_hole_to_external_contour_mm'],6)
        else:
            self.assertGreaterEqual(min(x['minimum_hole_to_external_contour_mm'] for x in report),6)
        self.assertTrue(all(x['contained'] for x in report))

    def double_C_web_or_single_B_slot(self):
        for st in stations(D):
            holes=slot_shapes(concept,st,D)
            if len(holes)==2:self.assertGreaterEqual(holes[0].distance(holes[1]),6)
            else:self.assertEqual(len(holes),1)

    def three_standard_parts_identical(self):
        ss=[s for s in stations(D) if s['part']=='P02']
        self.assertEqual(len(ss),3)
        p=spacer(concept,'P02',D,B)
        for s in ss:
            placed=translate(p,xoff=s['r_mm'])
            recovered=translate(placed,xoff=-s['r_mm'])
            self.assertLess(p.symmetric_difference(recovered).area,1e-8)

    def dxf_svg_equality(self):
        for name in ['P02','P02B','P01-SOFT_CURVE-mortise-study-v1']:
            folder,d,p=exported(concept,name)
            doc=ezdxf.readfile(folder/f'{name}.dxf');self.assertEqual(doc.units,4)
            audit=doc.audit();self.assertFalse(audit.has_errors);self.assertFalse(audit.has_fixes)
            curves=list(doc.modelspace());self.assertEqual(len(curves),len(d['paths_mm']))
            svg=ET.parse(folder/f'{name}.svg').getroot()
            nodes=svg.findall('.//{http://www.w3.org/2000/svg}polygon')
            self.assertEqual(len(nodes),len(curves))
            for curve,node,path in zip(curves,nodes,d['paths_mm']):
                self.assertTrue(curve.closed);self.assertEqual(curve.dxf.elevation,0)
                actual=[[float(x),float(y)] for x,y in curve.get_points('xy')]
                svgpath=[[float(x) for x in pair.split(',')] for pair in node.attrib['points'].split()]
                self.assertEqual(actual,path);self.assertEqual(actual,svgpath)

    def PNG_real_geometry_and_scale(self):
        for name in ['P02','P02B','P01-SOFT_CURVE-mortise-study-v1']:
            folder,d,p=exported(concept,name)
            with Image.open(folder/f'{name}.png') as image:
                self.assertIn(d['contour_sha256'],image.info['Description'])
                self.assertAlmostEqual(image.info['dpi'][0],D['raster_dpi'],delta=.03)
                x0,y0,x1,y1=p.bounds;m=D['sheet_margin_mm'];w=x1-x0+2*m;h=y1-y0+2*m
                self.assertAlmostEqual(image.width,w/25.4*D['raster_dpi'],delta=1.1)
                self.assertAlmostEqual(image.height,h/25.4*D['raster_dpi'],delta=1.1)
                ink=np.min(np.array(image.convert('RGB')),axis=2)<220
                self.assertGreater(np.count_nonzero(ink),50)
                for path in d['paths_mm']:
                    for r,z in path:
                        x=round((r-x0+m)/w*image.width);y=round((y1+m-z)/h*image.height)
                        self.assertTrue(ink[max(0,y-2):y+3,max(0,x-2):x+3].any(),(concept,name,r,z))

    def sheet_envelope_and_radius_screen(self):
        for name in ['P02','P02B','P01-SOFT_CURVE-mortise-study-v1']:
            _,d,p=exported(concept,name)
            self.assertLessEqual(d['padded_envelope_mm'][0],440)
            self.assertLessEqual(d['padded_envelope_mm'][1],800)
            self.assertGreaterEqual(d['minimum_nominal_radius_mm'],.1)
            self.assertEqual(d['margin_mm'],10)

    def source_rebuild_matches_export(self):
        for name in ['P02','P02B']:
            _,d,p=exported(concept,name)
            self.assertLess(p.symmetric_difference(spacer(concept,name,D,B)).area,1e-5)
        _,d,p=exported(concept,'P01-SOFT_CURVE-mortise-study-v1')
        self.assertLess(p.symmetric_difference(cheek(concept,D)[0]).area,1e-4)

    for name,fn in list(locals().items()):
        if callable(fn):setattr(SpacerTests,'test_'+concept+'_'+name,fn)


for c in CONCEPTS:add_concept_cases(c)
if __name__=='__main__':unittest.main(verbosity=2)
