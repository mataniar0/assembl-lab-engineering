"""CAD Boolean, interface, assembly-approach and native-file checks."""
from collections import Counter, defaultdict
from itertools import combinations
import math

import FreeCAD as App
import Part
import numpy as np
from scipy.spatial import ConvexHull

from model import FAMILIES, TOL, VOLUME_TOL, V, leg_prism, world


def intersects(a, b):
    return all(getattr(a, axis + "Min") <= getattr(b, axis + "Max") + TOL
               and getattr(b, axis + "Min") <= getattr(a, axis + "Max") + TOL
               for axis in "XYZ")


def volume(a, b):
    return a.common(b).Volume if intersects(a.BoundBox, b.BoundBox) else 0.0


def face_area(a, b):
    return sum(fa.common(fb).Area
               for fa in a.Faces for fb in b.Faces
               if intersects(fa.BoundBox, fb.BoundBox))


class Register:
    def __init__(self, previous=None):
        self.rows = {}
        self.previous = {row["id"]: row for row in previous or []}

    def add(self, key, suite, result, evidence):
        if key in self.rows:
            raise ValueError(f"Duplicate QA case {key}")
        status = ("PASS" if result else "FAIL") if isinstance(result, bool) else result
        self.rows[key] = dict(id=key, suite=suite, status=status, evidence=evidence)

    def reuse(self, key, affected):
        if not affected and key in self.previous:
            self.rows[key] = self.previous[key]
            return True
        return False


def check_model(layers, parameters, register):
    groups = defaultdict(list)
    by_family = defaultdict(list)
    for layer in layers:
        groups[layer.component].append(layer)
        by_family[layer.family].append(layer)
        shape = layer.shape
        if register.reuse(f"SOLID:{layer.id}", layer.family in {"A03", "E01"}):
            continue
        projected = [vertex.Point.dot(V(*layer.normal)) for vertex in shape.Vertexes]
        thickness = max(projected) - min(projected)
        closed = len(shape.Solids) == 1 and shape.isClosed() and shape.isValid()
        register.add(f"SOLID:{layer.id}", "solid", closed,
                     f"valid closed single solid={closed}, volume={shape.Volume:.6f} mm3")
        register.add(f"PLY:{layer.id}", "ply",
                     abs(thickness - parameters["ply_thickness_mm"]) <= TOL,
                     f"normal thickness={thickness:.8f} mm")
    # Carry forward the unchanged thickness cases alongside the identical solids.
    for layer in layers:
        if f"PLY:{layer.id}" not in register.rows:
            register.reuse(f"PLY:{layer.id}", False)

    ids = {layer.id for layer in layers}
    if not register.reuse("IDS", False):
        register.add("IDS", "counts", len(ids) == len(layers) == 104 and len(groups) == 60,
                     f"{len(ids)} unique layer IDs / {len(groups)} component IDs")
    bom = []
    for family, (expected_parts, expected_layers) in FAMILIES.items():
        items = by_family[family]
        parts = len({layer.component for layer in items})
        if not register.reuse(f"BOM:{family}", False):
            register.add(f"BOM:{family}", "counts",
                         (parts, len(items)) == (expected_parts, expected_layers),
                         f"{parts}/{expected_parts} components, {len(items)}/{expected_layers} layers")
        bom.append(dict(family=family, expected_components=expected_parts,
                        expected_layers=expected_layers, represented_components=parts,
                        represented_layers=len(items), defined_review_components=0 if family == "F01" else parts,
                        defined_review_layers=0 if family == "F01" else len(items),
                        status="PROXY_ONLY" if family == "F01" else "REVIEW_GEOMETRY"))

    body = [layer for layer in layers if not layer.proxy]
    if not register.reuse("DIM:height", False):
        zmin = min(layer.shape.BoundBox.ZMin for layer in body)
        zmax = max(layer.shape.BoundBox.ZMax for layer in body)
        register.add("DIM:height", "dimensions", abs(zmin) < TOL and
                     abs(zmax - parameters["height_mm"]) < TOL, f"Z={zmin:.6f} to {zmax:.6f} mm")
    for leg in range(1, 5):
        walls = [layer for layer in body if layer.leg == leg and layer.family in {"A01", "A02"}]
        for z in (20, 180, 380):
            key = f"DIM:LEG{leg}:Z{z}"
            if register.reuse(key, False):
                continue
            face = Part.makePlane(700, 700, V(-350, -350, z))
            points = [vertex.Point for layer in walls
                      for vertex in layer.shape.section(face).Vertexes]
            axes = [V(*world(axis, leg - 1)) for axis in [(1, 0, 0), (0, 1, 0)]]
            spans = [max(v.dot(ax) for v in points) - min(v.dot(ax) for v in points)
                     for ax in axes]
            register.add(key, "dimensions",
                         all(abs(span - parameters["horizontal_leg_section_mm"]) < TOL for span in spans),
                         f"horizontal U/V extent={spans[0]:.6f}/{spans[1]:.6f} mm")
        key = f"FLOOR:LEG{leg}"
        if not register.reuse(key, False):
            caps = sorted((layer for layer in body if layer.leg == leg and layer.family == "A04"),
                          key=lambda layer: layer.index)
            floor = [layer.shape.BoundBox.ZMin for layer in walls + caps[:1]]
            register.add(key, "dimensions", all(abs(z) < TOL for z in floor) and
                         abs(caps[1].shape.BoundBox.ZMin - parameters["ply_thickness_mm"]) < TOL,
                         f"{len(floor)} lower faces at Z=0; second cap ply at Z={caps[1].shape.BoundBox.ZMin:.6f}")

    pair_rows = []
    links = defaultdict(set)
    for a, b in combinations(layers, 2):
        key = f"PAIR:{a.id}|{b.id}"
        if register.reuse(key, {a.family, b.family} & {"A03", "E01"}):
            detail = register.rows[key]["evidence"]
        else:
            candidate = intersects(a.shape.BoundBox, b.shape.BoundBox)
            overlap = volume(a.shape, b.shape) if candidate else 0.0
            gap = a.shape.distToShape(b.shape)[0] if candidate and a.component != b.component else None
            contact = gap is not None and gap <= TOL and overlap <= VOLUME_TOL
            detail = dict(a=a.id, b=b.id, aabb_candidate=candidate,
                          overlap_mm3=round(overlap, 9), touching=contact)
            register.add(key, "overlap", overlap <= VOLUME_TOL, detail)
        pair_rows.append(detail)
        if detail["touching"]:
            links[a.component].add(b.component)
            links[b.component].add(a.component)

    for component, members in sorted(groups.items()):
        mates = links[component]
        is_proxy = members[0].proxy
        register.add(f"ISO:{component}", "isolation",
                     ("BLOCKED" if not mates else "FAIL") if is_proxy else bool(mates),
                     f"{'off-body placeholder; ' if is_proxy else ''}touching components: "
                     + (", ".join(sorted(mates)) or "none"))
    return groups, bom, pair_rows


def sweep(layer, dz):
    vertices = np.array([tuple(vertex.Point) for vertex in layer.shape.Vertexes])
    points = np.vstack((vertices, vertices + [0, 0, dz]))
    hull = ConvexHull(points)
    faces = []
    for simplex, equation in zip(hull.simplices, hull.equations):
        a, b, c = points[simplex]
        if np.dot(np.cross(b - a, c - a), equation[:3]) < 0:
            b, c = c, b
        wire = Part.makePolygon([V(*p) for p in (a, b, c, a)])
        faces.append(Part.Face(wire))
    solid = Part.makeSolid(Part.makeShell(faces))
    if not solid.isValid() or not solid.isClosed() or not math.isclose(
            solid.Volume, hull.volume, rel_tol=1e-8):
        raise ValueError(f"Invalid swept hull for {layer.id}")
    return solid


def path_obstacles(moving, others, dz):
    obstacles = {}
    for layer in moving:
        swept = sweep(layer, dz)
        for other in others:
            overlap = volume(swept, other.shape)
            if overlap > VOLUME_TOL:
                # Upper bound per obstacle ply; avoid double counting overlapping sweeps.
                obstacles[other.id] = round(max(overlap, obstacles.get(other.id, 0)), 6)
    return obstacles


def interface_register(layers, p, register):
    interfaces = []
    for side in range(1, 5):
        for family, level in (("B01", "upper"), ("C01", "lower")):
            moving = [l for l in layers if l.component.startswith(f"{family}_SIDE{side}_")]
            moving_ids = {l.id for l in moving}
            others = [l for l in layers if l.id not in moving_ids and not l.proxy]
            range_ = p[f"{level}_z_range_mm"]
            # Test both directions near the node and from beyond the final rail span.
            displacements = {"below_local": -12, "above_local": 12,
                             "below_extended": -(range_[0] - 1),
                             "above_extended": p["height_mm"] - range_[0] + 1}
            observations = {}
            for name, dz in displacements.items():
                key = f"PATH:{level}-{side}:{name}"
                affected = any(intersects(
                    moving_layer.shape.BoundBox.united(
                        moving_layer.shape.translated(V(0, 0, dz)).BoundBox),
                    other.shape.BoundBox)
                    for moving_layer in moving for other in others
                    if other.family in {"A03", "E01"})
                # The larger legacy diaphragm also reaches into the side envelope.
                affected = affected or family == "C01" or name == "below_extended"
                if not register.reuse(key, affected):
                    obstacles = path_obstacles(moving, others, dz)
                    register.add(key, "approach", not bool(obstacles),
                                 dict(offset_mm=dz, blocking_layer_overlap_mm3=obstacles))
                row = register.rows[key]
                observations[name] = row["status"]
            for leg in (side, 1 + side % 4):
                key = f"{level}-{side}-leg-{leg}"
                walls = [l for l in others if l.leg == leg and l.family in {"A01", "A02"}]
                case = f"NODE:{key}"
                if not register.reuse(case, False):
                    gap = min(a.shape.distToShape(b.shape)[0] for a in moving for b in walls)
                    contacts = {f"{a.id}/{b.id}": round(face_area(a.shape, b.shape), 6)
                                for a in moving for b in walls
                                if intersects(a.shape.BoundBox, b.shape.BoundBox)}
                    contacts = {pair: area for pair, area in contacts.items() if area > TOL}
                    area = sum(contacts.values())
                    overlap = sum(volume(a.shape, b.shape) for a in moving for b in walls)
                    register.add(case, "nominal_node", gap <= TOL and area > TOL and overlap <= VOLUME_TOL,
                                 dict(gap_mm=round(gap, 8), shared_face_mm2=round(area, 6),
                                      overlap_mm3=round(overlap, 9), shared_layer_faces_mm2=contacts))
                interfaces.append(dict(id=key, family="FJ-NODE", members="/".join(sorted({l.component for l in moving})),
                                       counterpart=f"LEG{leg}",
                                       nominal_status=register.rows[case]["status"],
                                       **register.rows[case]["evidence"], **observations,
                                       design_status="BLOCKED", limit="End-face contact surrogate. Mating, fixation, retention and whole assembly sequence open."))
    return interfaces


def check_joint_details(layers, parameters, register):
    by_id = {layer.id: layer for layer in layers}
    ply = parameters["ply_thickness_mm"]
    width = ply * math.hypot(1, parameters["leg_inward_slope_per_uv_axis"])
    cavity = parameters["horizontal_leg_section_mm"] / 2 - 2 * width
    depth = parameters["tab_review_depth_mm"]
    half_width = parameters["tab_half_width_mm"]
    relief = parameters["slot_side_relief_mm"]
    for leg in range(1, 5):
        socket = by_id[f"A01_LEG{leg}_POS_P2"]
        for suffix, z in zip(("LOW", "MID", "HIGH"), parameters["diaphragm_center_z_mm"]):
            diaphragm = by_id[f"A03_LEG{leg}_{suffix}_P1"]
            overlap = volume(socket.shape, diaphragm.shape)
            tongue_zone = leg_prism(cavity, cavity + depth, -half_width, half_width,
                                     z - ply / 2, z + ply / 2, parameters, leg - 1)
            pocket_zone = leg_prism(cavity, cavity + depth + relief,
                                     -half_width - relief, half_width + relief,
                                     z - ply / 2 - relief, z + ply / 2 + relief, parameters, leg - 1)
            fill_error = abs(volume(diaphragm.shape, tongue_zone) - tongue_zone.Volume)
            pocket_intrusion = volume(socket.shape, pocket_zone)
            gap = socket.shape.distToShape(diaphragm.shape)[0]
            register.add(f"TAB:LEG{leg}:{suffix}", "joint_details",
                         max(overlap, fill_error, pocket_intrusion) <= VOLUME_TOL and gap <= TOL,
                         dict(interference_mm3=round(overlap, 9), tongue_fill_error_mm3=round(fill_error, 9),
                              pocket_intrusion_mm3=round(pocket_intrusion, 9), nominal_shoulder_gap_mm=round(gap, 9),
                              lateral_z_and_depth_relief_mm=relief,
                              remaining_pocket_backing_normal_mm=round((width-depth-relief) * ply/width, 6)))
        for u in ("NEG", "POS"):
            for v in ("NEG", "POS"):
                key = f"EDGE:LEG{leg}:{u}:{v}"
                if register.reuse(key, False):
                    continue
                wall_u = by_id[f"A01_LEG{leg}_{u}_P1"]
                wall_v = by_id[f"A02_LEG{leg}_{v}_P1"]
                contact = face_area(wall_u.shape, wall_v.shape)
                register.add(key, "joint_details",
                             contact > TOL and volume(wall_u.shape, wall_v.shape) <= VOLUME_TOL,
                             f"review finger bands, shared area={contact:.6f} mm2")
    for side in range(1, 5):
        rail = by_id[f"B01_SIDE{side}_1_P1"]
        for endpoint in (1, 2):
            parts = [by_id[f"E01_SIDE{side}_END{endpoint}_P{ply}"] for ply in (1, 2)]
            leg = side if endpoint == 1 else 1 + side % 4
            walls = [l for l in layers if l.leg == leg and l.family in {"A01", "A02"}]
            leg_area = sum(face_area(a.shape, b.shape) for a in parts for b in walls
                           if intersects(a.shape.BoundBox, b.shape.BoundBox))
            rail_area = sum(face_area(a.shape, rail.shape) for a in parts)
            register.add(f"GUSSET:SIDE{side}:END{endpoint}", "joint_details",
                         leg_area > TOL and rail_area > TOL,
                         f"leg contact={leg_area:.6f}; upper rail contact={rail_area:.6f} mm2")


def controls(register):
    if register.reuse("CTRL:overlap", False):
        for key in ("CTRL:gap", "CTRL:sweep", "CTRL:open"):
            register.reuse(key, False)
        return
    box = Part.makeBox(4, 4, 4)
    overlap = volume(box, Part.makeBox(4, 4, 4, V(3, 0, 0)))
    register.add("CTRL:overlap", "negative_control", abs(overlap - 16) < TOL,
                 f"planted interference detected: {overlap} mm3")
    gap = box.distToShape(Part.makeBox(4, 4, 4, V(5, 0, 0)))[0]
    register.add("CTRL:gap", "negative_control", abs(gap - 1) < TOL,
                 f"planted separation detected: {gap} mm")
    from model import Layer
    moving = Layer("CONTROL", "B01", 1, box, (0, 0, 1))
    barrier = Layer("BARRIER", "B01", 1, Part.makeBox(4, 4, 1, V(0, 0, 9)), (0, 0, 1))
    hit = path_obstacles([moving], [barrier], 20)
    register.add("CTRL:sweep", "negative_control", hit == {barrier.id: 16},
                 f"intermediate-only obstruction detected: {hit}")
    register.add("CTRL:open", "negative_control", not box.Faces[0].isClosed(),
                 "single face rejected by closed-solid criterion")


def open_cases(register):
    for key, reason in {
        "F01": "8 positions / 16 proxy plies; shape, retention and installation open",
        "A03": "12 positions for the review; four interpolated mid positions remain unverified",
        "FJ": "Complementary load-bearing EB/FJ, fixing, material tolerances and sequence undefined",
        "G2b": "Whole-model assembly order, leg closure and access remain unresolved",
        "G3": "Professional and physical assessment outside the issue scope",
        "G4": "Production release outside the issue scope",
    }.items():
        register.add(f"OPEN:{key}", "remaining", "BLOCKED", reason)
    for key, reason in {
        "physical": "Measured fit, thickness, kerf, bond, strength, and stability",
        "independent": "ChatGPT R18-B independent review pending",
        "sequence": "Unmodeled retention and final assembly sequence",
    }.items():
        register.add(f"NOT_RUN:{key}", "remaining", "NOT_RUN", reason)


def check_fcstd(layers, path, register):
    document = App.openDocument(str(path))
    try:
        features = [obj for obj in document.Objects if obj.TypeId == "Part::Feature"]
        expected = {layer.id: layer for layer in layers}
        actual = {obj.Name: obj for obj in features}
        register.add("FCSTD:ids", "native_readback", actual.keys() == expected.keys(),
                     f"{len(actual)} reopened FreeCAD solid objects")
        for key in sorted(expected.keys() & actual.keys()):
            obj, layer = actual[key], expected[key]
            shape = obj.Shape
            ok = (shape.isValid() and shape.isClosed() and len(shape.Solids) == 1
                  and abs(shape.Volume - layer.shape.Volume) <= VOLUME_TOL
                  and obj.ComponentID == layer.component and
                  obj.GeometryStatus == ("PROXY_ONLY" if layer.proxy else "REVIEW_GEOMETRY"))
            register.add(f"FCSTD:{key}", "native_readback", ok,
                         f"volume={shape.Volume:.6f} mm3; {obj.GeometryStatus}")
    finally:
        App.closeDocument(document.Name)


def totals(rows):
    counts = Counter(row["status"] for row in rows)
    return {status: counts[status] for status in ("PASS", "FAIL", "BLOCKED", "NOT_RUN")}
