"""GLB and technical images derived from the same CAD solids."""
from collections import Counter
import json
import struct

import numpy as np

from model import COLORS, REVIEW_SCOPE


def tessellate(layers):
    result = {}
    for layer in layers:
        points, faces = layer.shape.tessellate(0.04)
        points = np.array([tuple(point) for point in points])
        _, indices, inverse = np.unique(points.round(7), axis=0, return_index=True,
                                        return_inverse=True)
        vertices = points[indices]
        triangles = inverse[np.asarray(faces)]
        result[layer.id] = vertices, triangles
    return result


def display_offsets(layers, meshes, exploded):
    offsets = {}
    for layer in layers:
        points, _ = meshes[layer.id]
        center = (points.min(0) + points.max(0)) / 2
        displacement = np.zeros(3)
        if exploded:
            displacement = np.array([center[0] * .50, center[1] * .50, (center[2] - 200) * .24])
            displacement += np.array(layer.normal) * (layer.index - 1) * 11
            if layer.family == "A03":
                displacement[:2] += center[:2] * .35
            if layer.family in {"A01", "A02"}:
                wall_sign = -1 if "_NEG_" in layer.id else 1
                displacement += np.array(layer.normal) * wall_sign * 29
        offsets[layer.id] = displacement
    return offsets


def gltf_axes(values):
    # Proper rotation only. CAD Z up in mm becomes glTF Y up in meters.
    return values[..., [0, 2, 1]] * [1, 1, -1] / 1000


def write_glb(path, layers, meshes, offsets, exploded):
    data = bytearray()
    gltf = {"asset": {"version": "2.0", "generator": "ST-001 FreeCAD solid review",
                      "extras": {"scope": REVIEW_SCOPE, "view": "EXPLODED" if exploded else "ASSEMBLED"}},
            "scene": 0, "scenes": [{"nodes": list(range(len(layers)))}],
            "nodes": [], "meshes": [], "materials": [], "bufferViews": [], "accessors": []}
    material_index = {}
    for family, color in COLORS.items():
        material_index[family] = len(gltf["materials"])
        rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
        gltf["materials"].append({"name": "F01 / proxy only" if family == "F01" else family,
                                  "pbrMetallicRoughness": {"baseColorFactor": rgb + [1],
                                                           "metallicFactor": 0, "roughnessFactor": .82},
                                  "doubleSided": True})

    def accessor(values, gl_type, kind, target):
        raw = values.tobytes()
        data.extend(b"\x00" * (-len(data) % 4))
        index = len(gltf["bufferViews"])
        gltf["bufferViews"].append({"buffer": 0, "byteOffset": len(data),
                                    "byteLength": len(raw), "target": target})
        data.extend(raw)
        values = values.reshape(-1, 3) if kind == "VEC3" else values.ravel()
        gltf["accessors"].append({"bufferView": index, "componentType": gl_type, "type": kind,
                                  "count": len(values), "min": values.min(0).tolist() if kind == "VEC3" else [int(values.min())],
                                  "max": values.max(0).tolist() if kind == "VEC3" else [int(values.max())]})
        return len(gltf["accessors"]) - 1

    for layer in layers:
        vertices, faces = meshes[layer.id]
        pos = accessor(gltf_axes(vertices).astype("<f4"), 5126, "VEC3", 34962)
        indices = accessor(faces.astype("<u4"), 5125, "SCALAR", 34963)
        gltf["nodes"].append({"name": layer.id, "mesh": len(gltf["meshes"]),
                              "translation": gltf_axes(offsets[layer.id]).tolist(),
                              "extras": {"component": layer.component, "family": layer.family,
                                         "proxy_only": layer.proxy}})
        gltf["meshes"].append({"name": layer.id, "primitives": [
            {"attributes": {"POSITION": pos}, "indices": indices,
             "material": material_index[layer.family], "mode": 4}]})
    data.extend(b"\x00" * (-len(data) % 4))
    gltf["buffers"] = [{"byteLength": len(data)}]
    header = json.dumps(gltf, separators=(",", ":")).encode()
    header += b" " * (-len(header) % 4)
    size = 12 + 8 + len(header) + 8 + len(data)
    path.write_bytes(struct.pack("<4sII", b"glTF", 2, size) +
                     struct.pack("<I4s", len(header), b"JSON") + header +
                     struct.pack("<I4s", len(data), b"BIN\x00") + data)


def read_glb(path):
    data = path.read_bytes()
    magic, version, length, json_length, kind = struct.unpack_from("<4sIII4s", data)
    if (magic, version, length, kind) != (b"glTF", 2, len(data), b"JSON"):
        raise ValueError(f"Invalid GLB container {path}")
    meta = json.loads(data[20:20 + json_length])
    bin_start = 20 + json_length
    bin_length, kind = struct.unpack_from("<I4s", data, bin_start)
    if kind != b"BIN\x00" or bin_start + 8 + bin_length != len(data):
        raise ValueError(f"Invalid GLB binary chunk {path}")

    def values(index, dtype, width):
        a = meta["accessors"][index]
        view = meta["bufferViews"][a["bufferView"]]
        offset = bin_start + 8 + view["byteOffset"] + a.get("byteOffset", 0)
        return np.frombuffer(data, dtype, a["count"] * width, offset)

    output = {}
    for node_index in meta["scenes"][meta["scene"]]["nodes"]:
        node = meta["nodes"][node_index]
        primitive, = meta["meshes"][node["mesh"]]["primitives"]
        coords = values(primitive["attributes"]["POSITION"], "<f4", 3).reshape(-1, 3)
        coords = coords[:, [0, 2, 1]] * [1000, -1000, 1000]
        offset = np.array(node.get("translation", [0, 0, 0]))[[0, 2, 1]] * [1000, -1000, 1000]
        faces = values(primitive["indices"], "<u4", 1).reshape(-1, 3)
        if node["name"] in output:
            raise ValueError(f"Duplicate node: {node['name']}")
        output[node["name"]] = (coords, faces, offset, node["extras"])
    return output


def check_glb(path, layers, meshes, offsets, register):
    restored = read_glb(path)
    expected = {layer.id: layer for layer in layers}
    register.add(f"{path.stem}:ids", "glb_readback", restored.keys() == expected.keys(),
                 f"{len(restored)} distinct nodes")
    for key, (points, faces, offset, meta) in restored.items():
        if key not in expected:
            continue
        layer = expected[key]
        edges = Counter(tuple(sorted((a, b))) for x, y, z in faces
                        for a, b in ((x, y), (y, z), (z, x)))
        manifold = bool(edges) and set(edges.values()) == {2}
        winding = Counter((int(a), int(b)) for x, y, z in faces
                          for a, b in ((x, y), (y, z), (z, x)))
        oriented = all(winding[(b, a)] == count for (a, b), count in winding.items())
        x, y, z = points[faces].transpose(1, 0, 2)
        mesh_volume = abs(np.einsum("ij,ij->i", x, np.cross(y, z)).sum() / 6)
        vertices, triangles = meshes[key]
        point_error = abs(points - vertices).max()
        rigid = abs(offset - offsets[key]).max() <= 0.0001 and point_error <= .0001
        bounds = np.ptp(points @ np.asarray(layer.normal))
        metadata = meta == {"family": layer.family, "component": layer.component, "proxy_only": layer.proxy}
        consistent = (manifold and oriented and rigid and metadata
                      and np.array_equal(faces, triangles)
                      and abs(mesh_volume - layer.shape.Volume) <= max(0.05, layer.shape.Volume * 2e-5))
        register.add(f"{path.stem}:{key}", "glb_readback", bool(consistent),
                     f"manifold={manifold}, oriented={oriented}, extent={bounds:.6f} mm, "
                     f"vertex delta={point_error:.8f} mm, volume={mesh_volume:.6f} mm3")


def render_triangles(triangles, background):
    """Rasterize orthographic triangles against a per-pixel depth buffer."""
    all_points = np.concatenate([triangle[:, :2] for triangle, _ in triangles])
    low = all_points.min(0)
    span = np.ptp(all_points, axis=0)
    padding = 24
    scale = 1050 / span.max()
    width, height = np.ceil(span * scale).astype(int) + 2 * padding + 1
    pixels = np.broadcast_to(np.asarray(background), (height, width, 3)).copy()
    depths = np.full((height, width), -np.inf)
    for triangle, rgb in triangles:
        xy = (triangle[:, :2] - low) * scale + padding
        x0, y0 = xy[0]
        u, v = xy[1] - xy[0], xy[2] - xy[0]
        determinant = u[0] * v[1] - u[1] * v[0]
        if determinant <= 1e-9:
            continue
        left, bottom = np.floor(xy.min(0)).astype(int)
        right, top = np.ceil(xy.max(0)).astype(int) + 1
        grid_y, grid_x = np.ogrid[bottom:top, left:right]
        dx, dy = grid_x - x0, grid_y - y0
        wu = (dx * v[1] - dy * v[0]) / determinant
        wv = (dy * u[0] - dx * u[1]) / determinant
        z0, z1, z2 = triangle[:, 2]
        depth = z0 + wu * (z1 - z0) + wv * (z2 - z0)
        tile = depths[bottom:top, left:right]
        visible = (wu >= -1e-8) & (wv >= -1e-8) & (wu + wv <= 1 + 1e-8) & (depth > tile)
        tile[visible] = depth[visible]
        pixels[bottom:top, left:right][visible] = rgb
    return pixels


def render(path, layers, meshes, offsets, exploded):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgb
    from matplotlib.patches import Patch

    eye = np.array([.91, -1.39, .89])
    eye /= np.linalg.norm(eye)
    right = np.cross([0, 0, 1], eye)
    right /= np.linalg.norm(right)
    up = np.cross(eye, right)
    projection = np.vstack([right, up, eye]).T
    items = []
    for layer in layers:
        points, faces = meshes[layer.id]
        xyz = (points + offsets[layer.id]) @ projection
        rgb = np.array(to_rgb(COLORS[layer.family]))
        if layer.index == 2:
            rgb = rgb * .73 + .24
        for triangle in xyz[faces]:
            normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
            if normal[2] <= 1e-8:
                continue
            light = .64 + .36 * max(0, np.dot(normal / np.linalg.norm(normal), [-.19, .55, .81]))
            items.append((triangle, np.minimum(rgb * light, 1)))
    fig, ax = plt.subplots(figsize=(8, 7.5), facecolor="#f0ede6")
    ax.set_facecolor("#f0ede6")
    ax.imshow(render_triangles(items, to_rgb("#f0ede6")), origin="lower", interpolation="antialiased")
    ax.set_aspect("equal")
    ax.set_axis_off()
    fig.suptitle("ST-001 | R18-A-FIX", fontsize=19, color="#20292d", x=.06, y=.965, ha="left")
    fig.text(.06, .914, ("Exploded CAD review" if exploded else "Assembled CAD review") +
             "   /   DESIGN_ONLY · NO_CUT · NO_OCCUPANT_USE", fontsize=9, color="#526065")
    legend = [Patch(color=COLORS[k], label=label) for k, label in
              [("A01", "A01/A02 walls"), ("A03", "A03 diaphragms"), ("A04", "A04 caps"),
               ("B01", "B01 upper rails"), ("C01", "C01 lower rails"), ("E01", "E01 gussets"),
               ("F01", "F01 lock proxies")]]
    fig.legend(handles=legend, loc="lower center", ncols=4, frameon=False, fontsize=8,
               bbox_to_anchor=(.5, .03))
    fig.subplots_adjust(left=.04, right=.96, top=.885, bottom=.11)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def render_map(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, axes = plt.subplots(1, 2, figsize=(11, 6), facecolor="#f0ede6")
    corners = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
    for ax, level in zip(axes, ("upper", "lower")):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{level.title()} FJ-NODE", color="#18272c", fontsize=15)
        col = COLORS["B01" if level == "upper" else "C01"]
        for i, point in enumerate(corners):
            following = corners[(i + 1) % 4]
            tangent = (following - point) / 2
            first, second = point + .19 * tangent, following - .19 * tangent
            ax.plot(*np.array([first, second]).T, color=col, lw=5, zorder=1)
            ax.scatter(*np.array([first, second]).T, color=col, s=50, zorder=4,
                       edgecolors="#ffffff", linewidths=.8)
            for endpoint, leg in ((first, i + 1), (second, (i + 1) % 4 + 1)):
                from_center = endpoint - (point + following) / 2
                label = endpoint + .22 * endpoint - .34 * from_center
                ax.text(*label, f"{i + 1}→L{leg}", ha="center", va="center", fontsize=8,
                        color="#304047")
                if level == "upper":
                    marker = endpoint + .19 * (point + following) / 2
                    ax.scatter(*marker, color=COLORS["F01"], marker="D", s=18)
            ax.add_patch(Rectangle(point - .19, .38, .38, facecolor=COLORS["A01"], zorder=2))
            ax.text(*point, f"L{i+1}", ha="center", va="center", fontsize=9, zorder=5)
        ax.set(xlim=(-1.45, 1.45), ylim=(-1.45, 1.45))
    fig.text(.05, .93, "ST-001 | Interface map", fontsize=20, color="#18272c")
    fig.text(.05, .87, "Each dot identifies a rail end and its leg.  Purple diamonds locate F01 proxies.",
             fontsize=10, color="#485a60")
    fig.text(.05, .105, "Each leg contains one EB shell, four FJ-EDGE corners and three FJ-TAB-SLOT demonstrations.",
             fontsize=10, color="#27383d")
    fig.text(.05, .06, REVIEW_SCOPE, fontsize=9, color="#485a60")
    fig.subplots_adjust(top=.8, bottom=.14, left=.055, right=.945, wspace=.05)
    fig.savefig(path, dpi=160)
    plt.close(fig)
