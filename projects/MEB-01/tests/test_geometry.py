"""Negative controls and profile round-trip tests; no production/physical claims."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import ezdxf
from shapely import affinity
from shapely.geometry import Polygon

PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'tools'))
from audit_geometry import load_geometry, same_shape
from reconstruct_reference import generate, MODEL


def dxf(points=((0,0),(10,0),(10,10),(0,10)),closed=True,units=4,duplicate=False,line=None):
    d=ezdxf.new('R2010');d.units=units
    d.modelspace().add_lwpolyline(points,close=closed)
    if duplicate:d.modelspace().add_lwpolyline(points,close=closed)
    if line is not None:d.modelspace().add_line(*line)
    s=io.StringIO();d.write(s);return s.getvalue().encode()


class GeometryControls(unittest.TestCase):
    def test_valid_closed_mm_profile(self):
        self.assertEqual(load_geometry(dxf())['solids'][0].area,100)

    def test_open_cut_contour_rejected(self):
        with self.assertRaisesRegex(ValueError,'Open contour'):load_geometry(dxf(closed=False))

    def test_wrong_units_rejected(self):
        with self.assertRaisesRegex(ValueError,'millimetres'):load_geometry(dxf(units=1))

    def test_missing_units_rejected(self):
        with self.assertRaisesRegex(ValueError,'millimetres'):load_geometry(dxf(units=0))

    def test_self_intersection_rejected(self):
        with self.assertRaisesRegex(ValueError,'Invalid'):load_geometry(dxf(points=((0,0),(10,10),(0,10),(10,0))))

    def test_zero_area_rejected(self):
        with self.assertRaisesRegex(ValueError,'zero-area'):load_geometry(dxf(points=((0,0),(1,0),(2,0))))

    def test_duplicate_contour_rejected(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'):load_geometry(dxf(duplicate=True))

    def test_zero_length_kerf_rejected(self):
        with self.assertRaisesRegex(ValueError,'Zero-length'):load_geometry(dxf(line=((1,1),(1,1))))

    def test_nonplanar_line_rejected(self):
        with self.assertRaisesRegex(ValueError,'Non-planar'):load_geometry(dxf(line=((1,1,2),(2,2,2))))

    def test_shape_match_rejects_same_bbox_wrong_geometry(self):
        self.assertFalse(same_shape(Polygon(((0,0),(10,0),(10,10),(0,10))),Polygon(((0,0),(10,0),(10,10)))))

    def test_shape_match_handles_rotation_translation(self):
        p=Polygon(((0,0),(30,0),(30,10),(5,10),(5,20),(0,20)))
        self.assertTrue(same_shape(p,affinity.translate(affinity.rotate(p,90,origin=(0,0)),100,200)))

    def test_even_odd_coupon_islands(self):
        d=ezdxf.new('R2010');d.units=4
        for pts in [((0,0),(30,0),(30,30),(0,30)),((5,5),(25,5),(25,25),(5,25)),((10,10),(20,10),(20,20),(10,20))]:
            d.modelspace().add_lwpolyline(pts,close=True)
        s=io.StringIO();d.write(s);g=load_geometry(s.getvalue().encode())
        self.assertEqual(len(g['solids']),2)
        self.assertEqual(sum(p.area for p in g['solids']),600)

    def test_generator_refuses_source_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'.git').mkdir();(root/'.git/HEAD').write_text('ref: refs/heads/main\n')
            model=json.loads(MODEL.read_text())
            with self.assertRaisesRegex(ValueError,'Refusing to write'):
                generate(model,root/'per_part')
            self.assertFalse((root/'per_part').exists())

    def test_measured_profiles_round_trip(self):
        model=json.loads(MODEL.read_text())
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(generate(model,Path(d)),14)
            for name,profile in model['profiles'].items():
                with self.subTest(profile=name):
                    actual=load_geometry((Path(d)/(name+'.dxf')).read_bytes())
                    self.assertEqual(len(actual['contours']),len(profile['contours']))
                    for p,pts in zip(actual['contours'],profile['contours']):
                        self.assertLess(p.symmetric_difference(Polygon(pts)).area,1e-8)
                    self.assertEqual([list(p.coords) for p in actual['lines']],[[tuple(p) for p in line] for line in profile['kerf_lines']])
                    self.assertIn('DESIGN_ONLY',(Path(d)/(name+'.svg')).read_text())


if __name__=='__main__':unittest.main()
