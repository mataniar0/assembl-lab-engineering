"""P01 concepts in local r-z. No dependent slots or approved manufacturing fit."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from shapely.geometry import Polygon, LineString, Point
from jsonschema import Draft202012Validator

PART = Path(__file__).resolve().parents[1]
PROJECT = PART.parents[1]
BASE = PROJECT / 'specifications/CTB-000'


def inputs():
    design = json.loads((PART / 'src/design.json').read_text())
    baseline = json.loads((BASE / 'CTB-000_parameters.json').read_text())
    schema = json.loads((PART / 'src/design.schema.json').read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(design)
    return design, baseline


def digest(points):
    return hashlib.sha256(json.dumps(points, separators=(',', ':')).encode()).hexdigest()


class Outline:
    def __init__(self, tolerance):
        self.points = []
        self.tolerance = tolerance
        self.radii = []
        self.cubics = []

    def line(self, point):
        p = list(map(float, point))
        if not self.points or math.dist(self.points[-1], p) > 1e-8:
            self.points.append(p)

    def arc(self, center, radius, start_deg, sweep_deg):
        # Exact analytic circular arc, flattened to a bounded sagitta tolerance.
        self.radii.append(radius)
        step = 2 * math.acos(1 - self.tolerance / radius)
        count = max(2, math.ceil(abs(math.radians(sweep_deg)) / step))
        for angle in np.linspace(start_deg, start_deg + sweep_deg, count + 1):
            a = math.radians(angle)
            self.line([center[0] + radius * math.cos(a), center[1] + radius * math.sin(a)])

    def cubic(self, controls):
        self.cubics.append(controls)

        def flatten(c):
            a, b, c2, d = np.array(c)
            chord = LineString([a, d])
            # Convex hull containment gives a conservative Bezier/chord bound.
            if max(chord.distance(Point(p)) for p in (b, c2)) <= self.tolerance:
                self.line(d)
                return
            ab, bc, cd = (a+b)/2, (b+c2)/2, (c2+d)/2
            abc, bcd = (ab+bc)/2, (bc+cd)/2
            middle = (abc+bcd)/2
            flatten([a, ab, abc, middle])
            flatten([middle, bcd, cd, d])
        self.line(controls[0])
        flatten(controls)

    def final(self):
        if math.dist(self.points[0], self.points[-1]) < 1e-8:
            self.points.pop()
        return [[round(float(x), 6), round(float(y), 6)] for x, y in self.points]


def rail_controls(z, r):
    z, r = np.array(z, dtype=float), np.array(r, dtype=float)
    h = np.diff(z)
    secant = np.diff(r) / h
    slopes = np.zeros(len(z))  # vertical tangents at the foot and upper stem
    for i in range(1, len(z)-1):
        if secant[i-1] * secant[i] > 0:
            w1, w2 = 2*h[i] + h[i-1], h[i] + 2*h[i-1]
            slopes[i] = (w1+w2)/(w1/secant[i-1] + w2/secant[i])
    return [[[r[i], z[i]], [r[i]+slopes[i]*h[i]/3, z[i]+h[i]/3],
             [r[i+1]-slopes[i+1]*h[i]/3, z[i+1]-h[i]/3], [r[i+1], z[i+1]]]
            for i in range(len(h))]


def rounded_polygon(outline, vertices, radii):
    vertices = np.array(vertices, dtype=float)
    trims = []
    turns = []
    for i, vertex in enumerate(vertices):
        incoming = vertex-vertices[i-1]
        outgoing = vertices[(i+1) % len(vertices)]-vertex
        incoming /= np.linalg.norm(incoming)
        outgoing /= np.linalg.norm(outgoing)
        turn = math.atan2(float(np.linalg.det([incoming, outgoing])), float(np.dot(incoming, outgoing)))
        turns.append((incoming, outgoing, turn))
        trims.append(radii[i] * math.tan(abs(turn)/2))
    for i in range(len(vertices)):
        if trims[i] + trims[(i+1) % len(vertices)] >= np.linalg.norm(vertices[(i+1) % len(vertices)]-vertices[i]):
            raise ValueError('Fillet consumes adjacent edge; reduce radius explicitly in design inputs')
    for i, vertex in enumerate(vertices):
        incoming, outgoing, turn = turns[i]
        if abs(turn) < 1e-8:
            outline.line(vertex)
            continue
        start = vertex-incoming*trims[i]
        center = start + np.array([-incoming[1], incoming[0]]) * math.copysign(radii[i], turn)
        angle = math.degrees(math.atan2(start[1]-center[1], start[0]-center[0]))
        outline.line(start)
        outline.arc(center, radii[i], angle, math.degrees(turn))


def profile(name, design=None, baseline=None):
    if design is None:
        design, baseline = inputs()
    s, v = design['study'], design['variants'][name]
    p = baseline['provisional']
    t0, t1 = p['upper_cheek_tongue_radial_interval_mm']
    top = p['upper_cheek_tongue_z_range_mm'][1]
    a, b = s['foot_radial_limits_mm']
    f, q, k = s['foot_corner_radius_mm'], s['shoulder_radius_mm'], s['tongue_tip_radius_mm']
    shoulder = s['shoulder_z_mm']
    assert shoulder + q == p['upper_cheek_tongue_z_range_mm'][0], 'Root easing must end at tongue start'
    lo, hi = p['Y_cheek_interface_radial_limits_mm']
    out = Outline(s['chord_tolerance_mm'])
    if v['kind'] == 'pchip_rails':
        z = s['rail_z_mm']
        assert v['inner_r_mm'][0] == a and v['outer_r_mm'][0] == b
        assert v['inner_r_mm'][-1] == lo and v['outer_r_mm'][-1] == hi
        out.line([a+f, 0]); out.line([b-f, 0])
        out.arc([b-f, f], f, -90, 90)
        out.line([b, z[0]])
        for c in rail_controls(z, v['outer_r_mm']):
            out.cubic(c)
        out.line([hi, shoulder-q]); out.arc([hi-q, shoulder-q], q, 0, 90)
        out.line([t1+q, shoulder]); out.arc([t1+q, shoulder+q], q, -90, -90)
        out.line([t1, top-k]); out.arc([t1-k, top-k], k, 0, 90)
        out.line([t0+k, top]); out.arc([t0+k, top-k], k, 90, 90)
        out.line([t0, shoulder+q]); out.arc([t0-q, shoulder+q], q, 0, -90)
        out.line([lo+q, shoulder]); out.arc([lo+q, shoulder-q], q, 90, 90)
        out.line([lo, z[-1]])
        for c in reversed(rail_controls(z, v['inner_r_mm'])):
            out.cubic(list(reversed(c)))
        out.line([a, f]); out.arc([a+f, f], f, 180, 90)
    else:
        vertices = v['body_vertices_rz_mm']
        # Geometric control polygon shares the same baseline-derived attachment.
        assert vertices[5:11] == [[hi,shoulder],[t1,shoulder],[t1,top],
                                   [t0,top],[t0,shoulder],[lo,shoulder]]
        radii = [v['body_fillet_radius_mm']] * len(vertices)
        for i in (0, 1): radii[i] = f
        for i in (5, 6, 9, 10): radii[i] = q
        for i in (7, 8): radii[i] = k
        rounded_polygon(out, vertices, radii)
    points = out.final()
    return points, out


def instances(points, baseline):
    thickness = baseline['frozen']['cheek_thickness_mm']
    result = []
    for angle in baseline['frozen']['leg_angles_deg']:
        a = math.radians(angle)
        for t in baseline['coordinate_frame']['cheek_center_t_offsets_mm']:
            surfaces = []
            for side in (-1, 1):
                local_t = t + side*thickness/2
                surfaces.append([[round(r*math.cos(a)-local_t*math.sin(a), 6),
                                  round(r*math.sin(a)+local_t*math.cos(a), 6), z] for r,z in points])
            result.append({'angle_deg': angle, 'center_t_mm': t,
                           'profile_sha256': digest(points), 'surfaces_xyz_mm': surfaces})
    return result


def section(poly, z):
    line = poly.intersection(LineString([[-1000,z], [1000,z]]))
    return float(line.length)
