"""Parametric FreeCAD/OCCT B-reps for ST-001 digital review only."""
from dataclasses import dataclass
import math

import FreeCAD as App
import Part

V = App.Vector
TOL = 1e-6
VOLUME_TOL = 1e-5
REVIEW_SCOPE = "DESIGN_ONLY / NO_CUT / NO_OCCUPANT_USE"
FAMILIES = {"A01": (8, 16), "A02": (8, 16), "A03": (12, 12),
            "A04": (4, 8), "B01": (4, 4), "C01": (8, 16),
            "E01": (8, 16), "F01": (8, 16)}
COLORS = {"A01": "#deb784", "A02": "#deb784", "A03": "#e28c42",
          "A04": "#9b734a", "B01": "#308f99", "C01": "#bf935d",
          "E01": "#a66b4e", "F01": "#ae62c5"}


@dataclass
class Layer:
    component: str
    family: str
    index: int
    shape: Part.Shape
    normal: tuple
    leg: int | None = None
    provisional: bool = False

    @property
    def id(self):
        return f"{self.component}_P{self.index}"

    @property
    def proxy(self):
        return self.family == "F01"


def polygon(points):
    vectors = [V(*point) for point in points]
    return Part.Face(Part.makePolygon(vectors + [vectors[0]]))


def rotate_uv(point, quarter_turns):
    u, v, z = point
    for _ in range(quarter_turns % 4):
        u, v = -v, u
    return u, v, z


def world(point, quarter_turns=0):
    u, v, z = rotate_uv(point, quarter_turns)
    root = math.sqrt(2)
    return (u - v) / root, (u + v) / root, z


def slab(points, delta, turn=0):
    face = polygon([world(point, turn) for point in points])
    return face.extrude(V(*world(delta, turn)))


def profile(points, v, width, turn):
    return slab([(u, v, z) for u, z in points], (0, width, 0), turn)


def leg_prism(u0, u1, v0, v1, z0, z1, p, turn):
    slope = p["leg_inward_slope_per_uv_axis"]
    center = -p["leg_center_at_floor_mm_in_uv"] + z0 * slope
    return slab([(center + u, center + v, z0)
                 for u, v in [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]],
                ((z1 - z0) * slope, (z1 - z0) * slope, z1 - z0), turn)


def inner_edge(z, p):
    return (-p["leg_center_at_floor_mm_in_uv"] +
            z * p["leg_inward_slope_per_uv_axis"] +
            p["horizontal_leg_section_mm"] / 2)


def build(p, cycle):
    layers = []
    half = p["horizontal_leg_section_mm"] / 2
    ply = p["ply_thickness_mm"]
    height = p["height_mm"]
    slope = p["leg_inward_slope_per_uv_axis"]
    width = ply * math.hypot(1, slope)
    cavity = half - 2 * width
    tab = p["tab_half_width_mm"]
    depth = p["tab_review_depth_mm"]
    relief = p["slot_side_relief_mm"]
    breaks = [0, *p["edge_demonstrator_z_breaks_mm"], height]

    def add(component, family, index, shape, normal, turn, leg=None, provisional=False):
        shape.rotate(V(0, 0, 0), V(0, 0, 1), 90 * turn)
        vector = V(*world(normal, turn))
        vector.normalize()
        layers.append(Layer(component, family, index, shape.removeSplitter(),
                            tuple(vector), leg, provisional))

    for turn in range(4):
        leg = turn + 1
        for direction in ("U", "V"):
            family = "A01" if direction == "U" else "A02"
            for sign, label in ((-1, "NEG"), (1, "POS")):
                for index in (1, 2):
                    thickness = sorted((sign * (half - (index - 1) * width),
                                        sign * (half - index * width)))
                    segments = []
                    for band, (low, high) in enumerate(zip(breaks, breaks[1:])):
                        owns_corner = (direction == "U") == (band % 2 == 0)
                        reach = half if owns_corner else cavity
                        ranges = (*thickness, -reach, reach)
                        if direction == "V":
                            ranges = (-reach, reach, *thickness)
                        segments.append(leg_prism(*ranges, low, high, p, 0))
                    shape = segments[0].multiFuse(segments[1:]).removeSplitter()
                    if direction == "U" and sign == 1 and index == 2:
                        pockets = [leg_prism(cavity - 0.01, cavity + depth + relief,
                                             -tab - relief, tab + relief,
                                             z - ply / 2 - relief, z + ply / 2 + relief,
                                             p, 0) for z in p["diaphragm_center_z_mm"]]
                        for pocket in pockets:
                            shape = shape.cut(pocket)
                    normal = (1, 0, -slope) if direction == "U" else (0, 1, -slope)
                    add(f"{family}_LEG{leg}_{label}", family, index, shape, normal, turn, leg)

        for name, z in zip(("LOW", "MID", "HIGH"), p["diaphragm_center_z_mm"]):
            lo, hi = z - ply / 2, z + ply / 2
            reach = cavity if cycle >= 2 else p["diaphragm_legacy_width_mm"] / 2
            shape = leg_prism(-reach, reach, -reach, reach, lo, hi, p, 0)
            if cycle >= 2:
                tongue = leg_prism(cavity, cavity + depth, -tab, tab, lo, hi, p, 0)
                shape = shape.fuse(tongue).removeSplitter()
            add(f"A03_LEG{leg}_{name}", "A03", 1, shape, (0, 0, 1), turn,
                leg, provisional=True)

        for index in (1, 2):
            add(f"A04_LEG{leg}", "A04", index,
                leg_prism(-cavity, cavity, -cavity, cavity,
                          (index - 1) * ply, index * ply, p, 0),
                (0, 0, 1), turn, leg)

        for family, level, count in (("B01", "upper", 1), ("C01", "lower", 2)):
            bottom, top = p[f"{level}_z_range_mm"]
            center = -p[f"{level}_side_offset_mm"]
            left_bottom, left_top = inner_edge(bottom, p), inner_edge(top, p)
            outline = [(left_bottom, bottom), (-left_bottom, bottom),
                       (-left_top, top), (left_top, top)]
            for member in range(1, count + 1):
                start = center - ply / 2 if count == 1 else center + (member - 2) * 2 * ply
                for index in range(1, count + 1):
                    shape = profile(outline, start + (index - 1) * ply, ply, 0)
                    add(f"{family}_SIDE{leg}_{member}", family, index, shape, (0, 1, 0), turn)

        # One gusset and one reserved lock location at each upper rail endpoint.
        bottom, top = p["gusset_bottom_z_mm"], p["upper_z_range_mm"][0]
        for endpoint, sign in ((1, -1), (2, 1)):
            start = p["gusset_legacy_start_u_mm"]
            gusset = [(sign * -(inner_edge(bottom, p) if cycle >= 2 else start), bottom),
                      (sign * -(inner_edge(top, p) if cycle >= 2 else start), top),
                      (sign * -p["gusset_inner_tip_u_mm"], top)]
            center = -p["upper_side_offset_mm"]
            for index in (1, 2):
                shape = profile(gusset, center + (index - 2) * ply, ply, 0)
                add(f"E01_SIDE{leg}_END{endpoint}", "E01", index, shape, (0, 1, 0), turn)
                # Two visibly offset symbol plies outside the leg. No mating surfaces.
                anchor = sign * -inner_edge(height - 40, p)
                outside = center - half - p["lock_review_offset_mm"]
                symbol = [(anchor + sign * u, height - z)
                          for u, z in [(0, 40), (12, 40), (12, 29), (5, 29), (5, 34), (0, 34)]]
                if index == 2:
                    symbol = [(u + sign * 2, z) for u, z in symbol]
                shape = profile(symbol, outside + (index - 1) * ply, ply, 0)
                add(f"F01_SIDE{leg}_END{endpoint}", "F01", index, shape,
                    (0, 1, 0), turn, provisional=True)

    return sorted(layers, key=lambda layer: layer.id)


def save_document(layers, path):
    document = App.newDocument("ST001_R18A_FIX")
    for family in FAMILIES:
        group = document.addObject("App::DocumentObjectGroup", family)
        group.Label = f"{family} | " + ("LOCK proxies" if family == "F01" else "Review solids")
        for layer in layers:
            if layer.family != family:
                continue
            feature = document.addObject("Part::Feature", layer.id)
            feature.addProperty("App::PropertyString", "ReviewScope")
            feature.ReviewScope = REVIEW_SCOPE
            feature.addProperty("App::PropertyString", "ComponentID")
            feature.ComponentID = layer.component
            feature.addProperty("App::PropertyString", "GeometryStatus")
            feature.GeometryStatus = "PROXY_ONLY" if layer.proxy else "REVIEW_GEOMETRY"
            feature.Shape = layer.shape
            group.addObject(feature)
    document.recompute()
    document.saveAs(str(path))
    App.closeDocument(document.Name)
