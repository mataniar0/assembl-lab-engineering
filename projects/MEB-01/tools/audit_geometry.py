#!/usr/bin/env python3
"""Read-only pinned-DXF audit. No source repair, implicit unit conversion or geometry healing."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import ezdxf
from shapely import affinity
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union

PROJECT = Path(__file__).resolve().parents[1]
CONTRACT = PROJECT / 'specifications/MEB-000'
TOL = 1e-5


def load_geometry(data):
    doc = ezdxf.read(io.StringIO(data.decode('utf-8')))
    if doc.header.get('$INSUNITS') != 4:
        raise ValueError('DXF units must explicitly be millimetres')
    contours, lines, layers = [], [], collections.Counter()
    for e in doc.modelspace():
        layers[e.dxf.layer] += 1
        if e.dxftype() == 'LWPOLYLINE':
            if not e.closed or any(abs(v[4]) > 1e-12 for v in e.get_points()):
                raise ValueError('Open contour or unsupported curved bulge')
            if e.dxf.get('elevation', 0) != 0 or tuple(e.dxf.get('extrusion', (0, 0, 1))) != (0, 0, 1):
                raise ValueError('Non-planar contour')
            pts = [(float(x), float(y)) for x, y in e.get_points('xy')]
            poly = Polygon(pts)
            if not poly.is_valid or poly.area <= TOL:
                raise ValueError('Invalid/self-intersecting/zero-area contour')
            if any(poly.equals(q) for q in contours):
                raise ValueError('Duplicate cut contour')
            contours.append(poly)
        elif e.dxftype() == 'LINE':
            if abs(e.dxf.start.z) > TOL or abs(e.dxf.end.z) > TOL:
                raise ValueError('Non-planar cut line')
            line = LineString([(e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)])
            if line.length <= TOL or any(line.equals(q) for q in lines):
                raise ValueError('Zero-length/duplicate cut line')
            lines.append(line)
        else:
            raise ValueError(f'Unsupported DXF entity {e.dxftype()}')
    if not contours:
        raise ValueError('No cut contour')
    for a, p in enumerate(contours):
        for q in contours[a + 1:]:
            if p.intersection(q).area > TOL and not (p.contains(q) or q.contains(p)):
                raise ValueError('Crossing cut contours')
    # Explicit even/odd nesting: coupon nests detached pins inside ring holes.
    # These are separate solids, not material filling the entire bore.
    depth = {id(p): sum(q.contains(p) for q in contours if q is not p) for p in contours}
    solids = []
    for outer in contours:
        if depth[id(outer)] % 2:
            continue
        holes = [q for q in contours if outer.contains(q) and depth[id(q)] == depth[id(outer)] + 1]
        solids.append(Polygon(outer.exterior.coords, [q.exterior.coords for q in holes]))
    return {'doc': doc, 'contours': contours, 'lines': lines, 'solids': solids, 'layers': dict(layers)}


def normalized(poly):
    x, y, _, _ = poly.bounds
    return affinity.translate(poly, -x, -y)


def same_shape(a, b):
    if abs(a.area - b.area) > TOL:
        return False
    for angle in (0, 90, 180, 270):
        candidate = normalized(affinity.rotate(a, angle, origin=(0, 0)))
        if candidate.symmetric_difference(normalized(b)).area < TOL:
            return True
    return False


def cover(poly, rect):
    return rect.difference(poly).area < TOL


def absent(poly, rect):
    return rect.intersection(poly).area < TOL


def audit(source):
    inventory = json.loads((CONTRACT / 'LEGACY_SOURCE_INVENTORY.json').read_text())
    commit = inventory['source_commit_sha']
    subprocess.run(['git', '-C', str(source), 'cat-file', '-e', commit + '^{commit}'], check=True)
    measured, provenance = {}, []
    for item in inventory['files']:
        data = (source / item['path']).read_bytes()
        pinned = subprocess.check_output(['git', '-C', str(source), 'show', f"{commit}:{item['path']}"])
        sha = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        if data != pinned or sha != item['sha'] or len(data) != item['size_bytes']:
            raise ValueError(f"Source integrity mismatch: {item['path']}")
        provenance.append({'path': item['path'], 'git_blob_sha': sha, 'sha256': hashlib.sha256(data).hexdigest(), 'status': 'PASS'})
        if item['path'].endswith('.dxf'):
            measured[item['path']] = load_geometry(data)
    per = {Path(k).stem: v for k, v in measured.items() if '/per_part/' in k}
    p = lambda name: per[name]['solids'][0]
    rows = []
    def case(index, ok, evidence, status=None):
        rows.append({'index': index, 'status': status or ('PASS' if ok else 'FAIL'), 'evidence': evidence})
    parts = list(csv.DictReader((CONTRACT / 'PARTS.csv').open()))
    sheets = {Path(k).name: v for k, v in measured.items() if '/production/' in k}
    sheet6 = sheets['V8_2_2_6mm_PRODUCTION_CUT_ONLY.dxf']
    sheet4 = sheets['V8_2_2_4mm_LID_SKIN_CUT_ONLY.dxf']
    legacytext = (source / 'megillat_esther_box/v8_2_2/V8_2_2_FULL_CONNECTION_AUDIT.csv').read_text()
    legacyrows = list(csv.DictReader(io.StringIO(legacytext[legacytext.index('index,Category'): ])))
    for i in range(14):
        name = legacyrows[i]['Part A']
        part = next(r for r in parts if Path(r['legacy_filename']).stem == name)
        expected = int(part['qty'])
        matching = sum(same_shape(p(name), s) for s in (sheet4 if name == 'LID_SKIN_4mm' else sheet6)['solids'])
        # Identical A/B and front/rear profiles cannot be distinguished geometrically.
        group = sum(int(r['qty']) for r in parts if same_shape(p(Path(r['legacy_filename']).stem), p(name)))
        case(i, matching == group, f'{name}: registry qty={expected}; sheet identical-shape group={matching}/{group}; nominal thickness from filenames, not measured')
    front, end, bottom = p('FRONT_6mm'), p('END_A_6mm'), p('BOTTOM_6mm')
    fw, fh = front.bounds[2:]; ew, eh = end.bounds[2:]
    for i, actual, required in [(14, fw-12, 310), (15, ew-12, 65), (16, fh-6, 65)]:
        case(i, abs(actual-required)<TOL, f'Nominal cavity={actual} mm from DXF bounds minus nominal 6mm panels; inferred assembly registration')
    zs = sorted(set(y for x,y in front.exterior.coords if x in (0,6)))
    complementary = all(front.contains(Point(3,14.2*(i+.5))) != end.contains(Point(3,14.2*(i+.5))) for i in range(5))
    case(17, zs == [0,14.2,28.4,42.6,56.8,71] and complementary, f'Boundary levels={zs}; complementary mid-pitch occupancy={complementary}; 2D only')
    for i,a in enumerate([22,84,146,208,270],18):
        ok = all(cover(bottom,box(a,y,a+30,y+6)) for y in (0,71)) and absent(front,box(a,0,a+30,6)) and absent(p('REAR_6mm'),box(a,0,a+30,6))
        case(i,ok,f'Long bottom tabs and front/rear open recesses: x={a}..{a+30}, depth6; zero nominal clearance')
    for i,a in enumerate([14,47],23):
        ok = all(cover(bottom,box(x,a,x+6,a+16)) for x in (0,316)) and all(absent(p(n),box(a,0,a+16,6)) for n in ('END_A_6mm','END_B_6mm'))
        case(i,ok,f'End tabs/recesses: {a}..{a+16}, depth6; zero nominal clearance')
    lid = p('LID_END_A_6mm_REINFORCED'); holes = [Polygon(r) for r in lid.interiors]
    for i,bounds in [(25,(27,6,33,12)),(26,(82,6,88,12))]:
        case(i, any(q.symmetric_difference(box(*bounds)).area < TOL for q in holes),f'Beam slot bounds={bounds}; repeated ends identical')
    beam=p('LID_FRONT_BEAM_6mm'); rib=p('LID_CENTER_RIB_6mm')
    case(27,all(cover(beam,box(x,2,x+6,8)) for x in (0,316)), 'Beam end tenons6x6; nominal zero slot clearance; no insertion proof')
    for i,n in [(28,'LID_REAR_BEAM_6mm'),(29,'LID_FRONT_BEAM_6mm')]:
        ok=absent(p(n),box(158,5,164,10)) and all(absent(rib,box(x,0,x+6,5)) for x in (8,63))
        case(i,ok,'Beam notch x158..164 depth5; rib notches x8..14 and63..69 depth5; 5+5=10 nominal, 3D registration proposed')
    skin=p('LID_SKIN_4mm'); lines=per['LID_SKIN_4mm']['lines']
    band=box(154+1e-8,0,168-1e-8,skin.bounds[3])
    case(30,not any(l.intersects(band) for l in lines),'Rib proposed x158..164 inside uncut x154..168; 4mm margins under inferred registration')
    curved=sorted([h for h in holes if abs(h.area-36)>TOL],key=lambda h:h.centroid.x)
    # Slot centerline follows the common lid arc, fitted from measured circular vertices.
    # Analytic center from the 77mm chord and measured sag of the rib.
    sag=rib.bounds[3]; radius=(77**2/(8*sag)+sag/2); center=(57.5,4+sag-radius)
    slot_order=[curved[0],curved[1],curved[2]]
    # Match 30/50/70 percent by x order (mirrors s direction without changing containment).
    arc_angle=2*math.asin(77/(2*radius)); arc_len=radius*arc_angle
    for i,h in enumerate(slot_order,31):
        radii=[math.hypot(x-center[0],y-center[1]) for x,y in h.exterior.coords]
        radial=max(radii)-min(radii)
        angles=[math.atan2(y-center[1],x-center[0]) for x,y in h.exterior.coords]
        tangential=(max(angles)-min(angles))*radius
        actual_mid_arc=(max(angles)-min(angles))*((max(radii)+min(radii))/2)
        case(i,abs(radial-4.1)<.01 and abs(tangential-12.2)<.02, f'Measured curved slot radial={radial:.6f}, outer-reference arc={tangential:.6f}, actual mid-radius arc={actual_mid_arc:.6f}; nominal finger12x4. Arc length={arc_len:.6f}. 2D shape check only; bent 3D tab containment NOT_RUN', status='NOT_RUN')
    mindistance=min(a.distance(b) for i,a in enumerate(holes) for b in holes[i+1:])
    case(34,mindistance>=5,f'Minimum cut-hole bridge={mindistance:.6f} mm, not strength')
    case(35,len(holes)==5,f'{len(holes)} independent openings:2 beam+3 skin')
    main=box(6,0,316,skin.bounds[3])
    case(36,len(lines)==190 and all(main.contains(l) for l in lines),f'{len(lines)} internal kerf LINE cuts; no edge contact')
    minx=min(l.bounds[0] for l in lines); maxx=max(l.bounds[2] for l in lines)
    case(37,abs(minx-18)<TOL and abs(maxx-304)<TOL,f'Cut range x{minx}..{maxx}; 12mm from main skin x6..316 (18mm from tab extrema x0..322)')
    case(38,not any(l.intersects(band) for l in lines),'Uncut band x154..168, center161; 14mm')
    ring=p('BODY_RING_6mm'); bore=Polygon(ring.interiors[0]); pin=p('PIN_DISC_14mm_6mm'); cap=p('LOCK_CAP_22mm_6mm')
    bore_d=bore.bounds[2]-bore.bounds[0]; pin_d=pin.bounds[2]-pin.bounds[0]; cap_d=cap.bounds[2]-cap.bounds[0]
    radial=(bore_d-pin_d)/2
    case(39,abs(radial-.3)<TOL,f'Diameters {bore_d}/{pin_d}; nominal radial gap={radial}')
    wall=bore.distance(Polygon(ring.exterior).exterior)
    case(40,wall>=6,f'Minimum polygonal annulus wall={wall:.6f} mm')
    case(41,(cap_d-bore_d)/2>=3,f'Nominal cap overlap={(cap_d-bore_d)/2:.6f} mm')
    overlap=affinity.translate(ring,-22,59).intersection(end).area
    case(42,abs(overlap-192)<TOL,f'Proposed ring->end translation(-22,59): overlap={overlap:.6f} mm2; no bond-strength claim')
    case(43,False,'Pin14 / ear22 footprint: ear diameter22 inferred from circular profile; bond and 3D registration not proved',status='NOT_RUN')
    case(44,False,'13mm neck assertion lacks an unambiguous measurement section in registered source; preserve for G1/G2',status='NOT_RUN')
    case(45,False,'0.3mm axial shim is assembly instruction, no axial dimensions/physical record in 2D DXF',status='NOT_RUN')
    case(46,False,'Historical 2D sampled sweep cannot establish continuous 3D collision-free opening; required110deg from owner; solid sweep NOT_RUN',status='NOT_RUN')
    case(47,ring.geom_type=='Polygon' and ring.is_valid,'Ring/foot one valid connected polygon with one bore')
    for i,sheet,expected in [(48,sheet6,(14,20,836,368)),(53,sheet4,(10,10,332,104.7965436107))]:
        bounds=unary_union(sheet['solids']).bounds
        case(i,all(abs(a-b)<TOL for a,b in zip(bounds,expected)) and box(0,0,900,440).covers(unary_union(sheet['solids'])),f'Legacy frame X-long900,Y-short440 bounds={bounds}; not new stock approval. 6mm layout exceeds either orientation of800x440')
    overlaps=[(a,b) for a in range(len(sheet6['solids'])) for b in range(a+1,len(sheet6['solids'])) if sheet6['solids'][a].intersection(sheet6['solids'][b]).area>TOL]
    case(49,not overlaps,f'6mm part area overlaps={overlaps}; kerf/machine margins not verified')
    for i,n in [(50,'BODY_RING_6mm'),(51,'PIN_DISC_14mm_6mm'),(52,'LOCK_CAP_22mm_6mm')]:
        count=sum(same_shape(p(n),s) for s in sheet6['solids'])
        case(i,count==2,f'{n} normalized contour+holes matching sheet instances={count}')
    case(54,len(per)==14 and set(per)=={Path(r['legacy_filename']).stem for r in parts},'14 registered definitions present; A/B and front/rear identical shape groups disclosed')
    case(55,len(measured)==17,'17 DXFs parsed; mm header, planar closed valid nonduplicate contours, explicit open kerf lines')
    rows.sort(key=lambda r:r['index'])
    values = {v['id']: v['value'] for v in json.loads((CONTRACT/'parameters.json').read_text())['values']}
    height, width = values['TARGET_SHEET_HEIGHT'], values['TARGET_SHEET_WIDTH']
    target_checks = []
    for name, sheet in sheets.items():
        x0,y0,x1,y1 = unary_union(sheet['solids']).bounds
        long, short = x1-x0, y1-y0
        fits = (long <= height and short <= width) or (long <= width and short <= height)
        target_checks.append({'file':name,'target_height_mm':height,'target_width_mm':width,
                              'status':'PASS' if fits else 'FAIL','existing_layout_bbox_mm':[long,short],
                              'scope':'Untranslated layout shape in either right-angle orientation; no margins/kerf. FAIL requires new packing, not altered source.'})
    return {'source_commit':commit,'scope':'G0_REFERENCE_ONLY_DESIGN_ONLY','provenance':provenance,'file_geometry':{k:{'layers':v['layers'],'contours':len(v['contours']),'kerf_lines':len(v['lines']),'solids':len(v['solids']),'bounds':unary_union(v['solids']).bounds} for k,v in measured.items()},'thin_lid_slot_lands_mm':[h.distance(Polygon(lid.exterior).exterior) for h in curved],'target_stock_checks':target_checks,'legacy_case_recheck':rows,'case_counts':dict(collections.Counter(r['status'] for r in rows))}, per


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--profiles',type=Path)
    args=parser.parse_args()
    try:
        result,per=audit(args.source)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2)+'\n')
        if args.profiles:
            model={'status':'PROPOSED_MEASURED_VERTEX_REFERENCE_NOT_APPROVED','source_commit':result['source_commit'],'units':'mm','limitation':'Coordinate-parametric tracing, not a production-ready generative design kernel. Preserve original contour segmentation.','profiles':{name:{'contours':[list(p.exterior.coords) for p in v['contours']],'kerf_lines':[list(l.coords) for l in v['lines']]} for name,v in per.items()}}
            args.profiles.parent.mkdir(parents=True,exist_ok=True)
            args.profiles.write_text(json.dumps(model,indent=2)+'\n')
        print('PASS provenance 20/20 pinned blobs; parsed17/17 DXFs')
        print('Historical case mapping:',json.dumps(result['case_counts']))
        for target in result['target_stock_checks']:
            print('TARGET_STOCK', target['status'],target['file'],target['existing_layout_bbox_mm'])
        for row in result['legacy_case_recheck']:
            print(row['index'],row['status'],row['evidence'])
        return int(any(r['status']=='FAIL' for r in result['legacy_case_recheck']) or
                   any(r['status']=='FAIL' for r in result['target_stock_checks']))
    except (ValueError, OSError, KeyError) as exc:
        print('FAIL',exc)
        return 1

if __name__=='__main__':
    sys.exit(main())
