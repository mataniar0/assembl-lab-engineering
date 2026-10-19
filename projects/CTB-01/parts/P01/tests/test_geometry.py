"""Read exported artifacts independently; never infer mechanical approval from CAD."""
import copy
import hashlib
import json
import math
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import ezdxf
import numpy as np
from PIL import Image
from jsonschema import Draft202012Validator, ValidationError
from shapely.geometry import Polygon, LineString, MultiPoint, Point
from shapely import line_merge
from shapely.validation import explain_validity

PART=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PART/'src'))
from model import inputs, profile, instances, digest, section

DESIGN, BASELINE=inputs()


def artifact(name):
    directory=PART/'variants'/name
    d=json.loads((directory/'dimensions.json').read_text())
    return directory,d,Polygon(d['contour_rz_mm'])


def assert_contour(test, points):
    polygon=Polygon(points)
    test.assertTrue(polygon.is_valid,explain_validity(polygon))
    test.assertTrue(polygon.exterior.is_simple)
    test.assertTrue(polygon.exterior.is_ring)
    test.assertFalse(polygon.is_empty)
    test.assertEqual(len(polygon.interiors),0)
    test.assertGreater(polygon.area,0)
    test.assertEqual(polygon.geom_type,'Polygon')
    return polygon


class GeometryTests(unittest.TestCase):
    def test_invalid_self_intersection_rejected(self):
        with self.assertRaises(AssertionError):
            assert_contour(self,[[0,0],[10,10],[0,10],[10,0]])

    def test_oversize_fillet_rejected(self):
        d=copy.deepcopy(DESIGN)
        d['variants']['GEOMETRIC']['body_fillet_radius_mm']=1000
        with self.assertRaises(ValueError):
            profile('GEOMETRIC',d,BASELINE)

    def test_alternatives_genuinely_different(self):
        polygons=[artifact(n)[2] for n in DESIGN['variants']]
        for i in range(3):
            for j in range(i):
                self.assertGreater(polygons[i].symmetric_difference(polygons[j]).area,1000)

    def test_no_baseline_byte_changes(self):
        project=PART.parents[1]
        hashes=json.loads((project/'reports/CTB-000-source-sha256.json').read_text())
        for name, expected in hashes.items():
            self.assertEqual(hashlib.sha256((project/'specifications/CTB-000'/name).read_bytes()).hexdigest(),expected)

    def test_status_and_no_dependent_cutouts(self):
        self.assertEqual(DESIGN['status'],'DESIGN_ONLY')
        self.assertEqual(set(DESIGN['variants']),{'SOFT_CURVE','FLARED_CURVE','GEOMETRIC'})
        for name in DESIGN['variants']:
            directory,d,p=artifact(name)
            self.assertEqual(d['status'],'DESIGN_ONLY')
            self.assertEqual(len(p.interiors),0)  # reservation annotations never cut slots

    def test_common_parameter_schema(self):
        schema=json.loads((PART/'src/design.schema.json').read_text())
        validator=Draft202012Validator(schema)
        validator.validate(DESIGN)
        invalid=copy.deepcopy(DESIGN)
        invalid['study']['tongue_tip_radius_mm']=-1
        with self.assertRaises(ValidationError):
            validator.validate(invalid)

    def test_known_Y_mismatch_remains_open(self):
        p=BASELINE['provisional']
        self.assertEqual(p['Y_arm_end_radius_mm']-p['Y_cheek_interface_radial_limits_mm'][1],4)
        matrix=(PART.parents[1]/'reports/CTB-001-INTERFACE-MATRIX.md').read_text()
        self.assertIn('Extend the upper cheek envelope',matrix)
        self.assertIn('Shorten/rework the Y arm',matrix)
        self.assertIn('BLOCKED',matrix)


def install_variant_cases(name):
    def closed(self):
        _,d,_=artifact(name)
        assert_contour(self,d['contour_rz_mm'])

    def no_degenerates(self):
        _,d,p=artifact(name)
        points=d['contour_rz_mm']
        edges=[(tuple(a),tuple(b)) for a,b in zip(points,points[1:]+points[:1])]
        self.assertGreater(min(math.dist(a,b) for a,b in edges),0.01)
        self.assertEqual(len(set(tuple(sorted(edge)) for edge in edges)),len(edges))
        self.assertTrue(LineString(points+[points[0]]).is_simple)

    def no_microscopic_necks(self):
        _,d,p=artifact(name)
        eroded=p.buffer(-DESIGN['study']['screening_erosion_radius_mm'])
        self.assertFalse(eroded.is_empty)
        self.assertEqual(eroded.geom_type,'Polygon')
        self.assertEqual(len(eroded.interiors),0)
        # Wide continuous body; criterion is a geometric screen, not strength.
        for z in np.linspace(0,448,1200):
            cut=p.intersection(LineString([[-1000,z],[1000,z]]))
            if cut.geom_type == 'MultiLineString':
                cut = line_merge(cut)
            self.assertEqual(cut.geom_type,'LineString')
            self.assertGreaterEqual(cut.length,DESIGN['study']['screening_min_body_width_mm'])

    def geometric_corner_radius_screen(self):
        _,d,_=artifact(name)
        self.assertGreaterEqual(min(d['nominal_arc_radii_mm']),1)
        # Curvature of the actual cubic control curves, not polygon turning angles.
        for controls in d['analytic_bezier_controls_rz_mm']:
            a,b,c,e=np.array(controls)
            for t in np.linspace(0,1,1001):
                velocity=3*((1-t)**2*(b-a)+2*(1-t)*t*(c-b)+t*t*(e-c))
                acceleration=6*((1-t)*(c-2*b+a)+t*(e-2*c+b))
                cross=abs(velocity[0]*acceleration[1]-velocity[1]*acceleration[0])
                if cross>1e-8:
                    radius=np.linalg.norm(velocity)**3/cross
                    self.assertGreaterEqual(radius,1)
        self.assertLessEqual(d['chord_tolerance_mm'],.02)

    def dxf_round_trip(self):
        directory,d,p=artifact(name)
        doc=ezdxf.readfile(directory/'profile.dxf')
        self.assertEqual(doc.units,4)
        auditor=doc.audit()
        self.assertFalse(auditor.has_errors)
        self.assertFalse(auditor.has_fixes)
        entities=list(doc.modelspace())
        self.assertEqual(len(entities),1)
        curve=entities[0]
        self.assertEqual(curve.dxftype(),'LWPOLYLINE')
        self.assertTrue(curve.closed)
        self.assertEqual(curve.dxf.elevation,0)
        self.assertEqual(tuple(curve.dxf.extrusion),(0,0,1))
        self.assertEqual(curve.dxf.layer,'CUT_DESIGN_ONLY')
        points=[[float(x),float(y)] for x,y in curve.get_points('xy')]
        self.assertTrue(np.allclose(points,d['contour_rz_mm'],atol=1e-8,rtol=0))
        assert_contour(self,points)

    def svg_round_trip(self):
        directory,d,p=artifact(name)
        root=ET.parse(directory/'profile.svg').getroot()
        self.assertTrue(root.attrib['width'].endswith('mm'))
        x,y,w,h=map(float,root.attrib['viewBox'].split())
        self.assertAlmostEqual(float(root.attrib['width'][:-2]),w)
        self.assertAlmostEqual(float(root.attrib['height'][:-2]),h)
        poly=root.find('.//{http://www.w3.org/2000/svg}polygon')
        points=[[float(n) for n in pair.split(',')] for pair in poly.attrib['points'].split()]
        self.assertEqual(points,d['contour_rz_mm'])
        self.assertEqual(root.find('.//{http://www.w3.org/2000/svg}g').attrib['transform'],'scale(1,-1)')
        assert_contour(self,points)

    def png_actual_contour_and_scale(self):
        directory,d,p=artifact(name)
        with Image.open(directory/'profile.png') as image:
            self.assertIn(d['profile_sha256'],image.info['Description'])
            dpi=image.info['dpi'][0]
            self.assertAlmostEqual(dpi,DESIGN['study']['raster_dpi'],delta=.03)
            minx,minz,maxx,maxz=p.bounds
            m=DESIGN['study']['sheet_margin_mm']
            width,height=maxx-minx+2*m,maxz-minz+2*m
            self.assertAlmostEqual(image.width,width/25.4*dpi,delta=1.1)
            self.assertAlmostEqual(image.height,height/25.4*dpi,delta=1.1)
            pixels=np.array(image.convert('RGB'))
            ink=np.min(pixels,axis=2)<220  # subpixel antialiasing on a 0.5 pt stroke
            self.assertGreater(np.count_nonzero(ink),500)
            # Actual raster content must trace the exported contour, not just a matching tag.
            for r,z in d['contour_rz_mm']:
                x=round((r-minx+m)/width*image.width)
                y=round((maxz+m-z)/height*image.height)
                self.assertTrue(ink[max(0,y-2):y+3,max(0,x-2):x+3].any(),(r,z))
            yy,xx=np.nonzero(ink)
            samples=zip(xx[::20],yy[::20])
            for x,y in samples:
                r=(x+.5)/image.width*width+minx-m
                z=maxz+m-(y+.5)/image.height*height
                self.assertLess(p.exterior.distance(Point(r,z)),.8)

    def six_identical_transformed_instances(self):
        _,d,p=artifact(name)
        self.assertEqual(len(d['instances']),6)
        self.assertEqual({i['angle_deg'] for i in d['instances']},{0,120,240})
        self.assertEqual(d['instances'],instances(d['contour_rz_mm'],BASELINE))
        for i in d['instances']:
            self.assertEqual(i['profile_sha256'],d['profile_sha256'])
            a=math.radians(i['angle_deg'])
            for side,surface in zip((-1,1),i['surfaces_xyz_mm']):
                for (x,y,z),(r,z0) in zip(surface,d['contour_rz_mm']):
                    self.assertAlmostEqual(x*math.cos(a)+y*math.sin(a),r,places=5)
                    self.assertAlmostEqual(-x*math.sin(a)+y*math.cos(a),i['center_t_mm']+side*3,places=5)
                    self.assertEqual(z,z0)

    def tangential_gap_and_thickness(self):
        _,d,_=artifact(name)
        for a in (0,120,240):
            pair=[i for i in d['instances'] if i['angle_deg']==a]
            theta=math.radians(a)
            intervals=[]
            for i in pair:
                vals=[-x*math.sin(theta)+y*math.cos(theta) for surface in i['surfaces_xyz_mm'] for x,y,z in surface]
                intervals.append([min(vals),max(vals)])
            self.assertAlmostEqual(intervals[1][0]-intervals[0][1],15,places=5)
            self.assertAlmostEqual(intervals[1][1]-intervals[0][0],27,places=5)
            for lower,upper in intervals:self.assertAlmostEqual(upper-lower,6,places=5)

    def bare_cheek_footprints_do_not_intersect(self):
        _,d,_=artifact(name)
        footprints=[MultiPoint([(x,y) for surface in i['surfaces_xyz_mm'] for x,y,z in surface]).convex_hull for i in d['instances']]
        for i in range(6):
            for j in range(i):self.assertFalse(footprints[i].intersects(footprints[j]))

    def tongue_disc_sections_only(self):
        _,d,p=artifact(name)
        for low,high in BASELINE['provisional']['anchor_disc_z_ranges_mm']:
            for z in np.linspace(low,high,13):
                cut=p.intersection(LineString([[-1000,z],[1000,z]]))
                self.assertEqual(cut.geom_type,'LineString')
                self.assertAlmostEqual(cut.bounds[0],45)
                self.assertAlmostEqual(cut.bounds[2],69)
                self.assertAlmostEqual(cut.length,24)
                # Disc circle containment includes tangential offset and half thickness.
                self.assertLess(math.hypot(cut.bounds[2],13.5),95)
        tip=p.intersection(LineString([[-1000,488],[1000,488]]))
        self.assertAlmostEqual(tip.length,22)
        self.assertAlmostEqual(p.bounds[3],488)
        self.assertEqual(494-p.bounds[3],6)
        self.assertEqual(488-486,2)

    def bottom_skin_nominal_allowance_only(self):
        _,d,p=artifact(name)
        for z in np.linspace(450,456,13):
            cut=p.intersection(LineString([[-1000,z],[1000,z]]))
            self.assertAlmostEqual(cut.bounds[0]-44.8,.2)
            self.assertAlmostEqual(69.2-cut.bounds[2],.2)
        self.assertAlmostEqual((6.2-6)/2,.1)

    def upper_envelope_and_Y(self):
        _,d,p=artifact(name)
        for z in np.linspace(390,440,30):
            cut=p.intersection(LineString([[-1000,z],[1000,z]]))
            self.assertAlmostEqual(cut.bounds[0],35)
            self.assertAlmostEqual(cut.bounds[2],90)
        self.assertEqual(d['Y_envelope_overhang_mm'],4)

    def reservations_are_material_not_slots(self):
        _,d,p=artifact(name)
        for low,high in d['spacer_reserved_z_mm']+[d['ring_reserved_z_mm']]:
            for z in np.linspace(low,high,50):
                cut=p.intersection(LineString([[-1000,z],[1000,z]]))
                self.assertEqual(cut.geom_type,'LineString')
                self.assertGreaterEqual(cut.length,24)
        spacer=d['spacer_reserved_z_mm'][2]
        ring=d['ring_reserved_z_mm']
        self.assertGreater(min(spacer[1],ring[1])-max(spacer[0],ring[0]),0)

    def single_part_sheet_margin(self):
        _,d,p=artifact(name)
        s=d['sheet_check']; m=s['margin_each_edge_mm']
        self.assertEqual((s['height_mm'],s['width_mm']),(800,440))
        self.assertEqual(m,10)
        x0,z0,x1,z1=p.bounds
        dx,dy=s['placement_translation_rz_to_sheet_xy_mm']
        self.assertGreaterEqual(x0+dx,m)
        self.assertGreaterEqual(z0+dy,m)
        self.assertLessEqual(x1+dx,440-m)
        self.assertLessEqual(z1+dy,800-m)
        self.assertAlmostEqual(s['padded_width_mm'],x1-x0+2*m)
        self.assertAlmostEqual(s['padded_height_mm'],z1-z0+2*m)

    def ground_and_top_elevations(self):
        _,d,p=artifact(name)
        self.assertEqual(p.bounds[1],0)
        foot=p.intersection(LineString([[-1000,0],[1000,0]]))
        self.assertGreaterEqual(foot.length,30)
        self.assertAlmostEqual((foot.bounds[0]+foot.bounds[2])/2,240)
        self.assertEqual(BASELINE['derived']['tabletop_bottom_z_mm'],450)
        self.assertEqual(450+BASELINE['frozen']['top_total_thickness_mm'],500)
        self.assertEqual(BASELINE['frozen']['table_outer_diameter_mm'],350)
        self.assertLess(240/2,350/2)  # center triangle is not a stability proof

    def actual_ground_support_projection(self):
        _,d,p=artifact(name)
        contacts=[]
        for item in d['instances']:
            contacts.extend((x,y) for surface in item['surfaces_xyz_mm']
                            for x,y,z in surface if abs(z)<1e-8)
        hull=MultiPoint(contacts).convex_hull
        result=d['ground_contact_projection']
        self.assertAlmostEqual(hull.area,result['hull_area_mm2'])
        self.assertAlmostEqual(hull.exterior.distance(Point(0,0)),result['origin_to_support_edge_min_mm'])
        self.assertAlmostEqual(result['origin_to_support_edge_min_mm'],140.691343,places=5)
        self.assertLess(result['origin_to_support_edge_min_mm'],175)
        self.assertEqual(result['foot_center_triangle_inradius_mm'],120)

    def rebuild_source_matches_exports(self):
        _,d,p=artifact(name)
        points,out=profile(name)
        self.assertEqual(points,d['contour_rz_mm'])
        self.assertEqual(digest(points),d['profile_sha256'])
        self.assertEqual(d['source_inputs_sha256'],hashlib.sha256((PART/'src/design.json').read_bytes()).hexdigest())

    cases=locals().copy()
    for label,fn in cases.items():
        if callable(fn) and label not in ('install_variant_cases',):
            setattr(GeometryTests,f'test_{name}_{label}',fn)


for variant in DESIGN['variants']:
    install_variant_cases(variant)


if __name__=='__main__':
    unittest.main(verbosity=2)
