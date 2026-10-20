#!/usr/bin/env python3
"""Independent stdlib DXF group-code checks; no ezdxf/shapely/implementation imports.
Run: python projects/MEB-01/reports/MEB-000-independent-raw-qa.py /tmp/meb-legacy-site
Reads pinned Git blobs, does not check out/write the legacy repository.
"""
import collections
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SPEC = ROOT / 'projects/MEB-01/specifications/MEB-000'
INVENTORY = json.loads((SPEC / 'LEGACY_SOURCE_INVENTORY.json').read_text())
COMMIT = INVENTORY['source_commit_sha']
REPO = sys.argv[1] if len(sys.argv) > 1 else '/tmp/meb-legacy-site'
CASES = []

def check(name, condition, actual=None):
    CASES.append({'id': name, 'status': 'PASS' if condition else 'FAIL', 'actual': actual})

def get_blob(path):
    return subprocess.check_output(['git', '-C', REPO, 'show', COMMIT + ':' + path])

def parse(raw):
    lines = raw.decode('ascii').splitlines()
    if len(lines) % 2:
        raise ValueError('odd group-code line count')
    pairs = [(int(lines[i]), lines[i+1].strip()) for i in range(0, len(lines), 2)]
    if pairs[-1] != (0, 'EOF'):
        raise ValueError('no EOF')
    u = pairs.index((9, '$INSUNITS'))
    if pairs[u+1] != (70, '4'):
        raise ValueError('units not millimetres')
    start = pairs.index((2, 'ENTITIES')) + 1
    entities = []
    entity = None
    for code, value in pairs[start:]:
        if code == 0:
            if entity:
                entities.append(entity)
            if value == 'ENDSEC':
                break
            if value not in ('LWPOLYLINE', 'LINE'):
                raise ValueError('unsupported entity')
            entity = {'type': value, 'groups': []}
        else:
            entity['groups'].append((code, value))
    if not entities:
        raise ValueError('no entities')
    for entity in entities:
        g = entity['groups']
        if not all(v in ('CUT', 'CUT_6MM', 'CUT_4MM', 'LIVING_HINGE', 'LIVING_HINGE_CUTS') for c,v in g if c == 8):
            raise ValueError('wrong cut layer')
        if entity['type'] == 'LWPOLYLINE':
            if not int(next(v for c,v in g if c == 70)) & 1:
                raise ValueError('open polygon')
            xs = [float(v) for c,v in g if c == 10]
            ys = [float(v) for c,v in g if c == 20]
            n = int(next(v for c,v in g if c == 90))
            if len(xs) != n or len(ys) != n or n < 3:
                raise ValueError('wrong vertex count')
            pts = list(zip(xs, ys))
            if abs(area(pts)) < 1e-8:
                raise ValueError('zero polygon area')
        else:
            pts = [(float(next(v for c,v in g if c == 10)), float(next(v for c,v in g if c == 20))),
                   (float(next(v for c,v in g if c == 11)), float(next(v for c,v in g if c == 21)))]
            if pts[0] == pts[1]:
                raise ValueError('zero cut line')
        if not all(math.isfinite(v) for pt in pts for v in pt):
            raise ValueError('nonfinite coordinate')
        entity['points'] = pts
        entity['bbox'] = bbox(pts)
    return entities

def bbox(pts):
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]

def area(pts):
    return sum(a[0]*b[1] - b[0]*a[1] for a,b in zip(pts, pts[1:] + pts[:1]))/2

def near(a,b,tol=1e-7):
    return abs(a-b) < tol

def dim(e):
    b=e['bbox']; return b[2]-b[0], b[3]-b[1]

raws = {}; parsed = {}; summaries = {}
for item in INVENTORY['files']:
    path = item['path']; raw = get_blob(path); raws[Path(path).name] = raw
    digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    check('blob:' + path, len(raw) == item['size_bytes'] and digest == item['sha'], {'bytes':len(raw),'git_sha':digest})
    if path.endswith('.dxf'):
        try:
            es = parse(raw); parsed[Path(path).name] = es
            summary = {'entities':dict(collections.Counter(e['type'] for e in es)),
                       'bbox':bbox([p for e in es for p in e['points']]),
                       'polygons':[{'vertices':len(e['points']),'bbox':e['bbox'],'signed_area':area(e['points'])} for e in es if e['type']=='LWPOLYLINE']}
            summaries[Path(path).name] = summary
            check('raw_parse:' + path, True, summary['entities'])
        except Exception as exc:
            check('raw_parse:' + path, False, repr(exc))

front=parsed['FRONT_6mm.dxf'][0]; end=parsed['END_A_6mm.dxf'][0]; bottom=parsed['BOTTOM_6mm.dxf'][0]
check('front_dimensions',dim(front)==(322,71),dim(front))
check('end_dimensions',dim(end)==(77,71),dim(end))
check('bottom_dimensions',dim(bottom)==(322,77),dim(bottom))
cavity=[dim(front)[0]-12,dim(end)[0]-12,dim(front)[1]-6]
check('nominal_cavity_at_6mm',cavity==[310,65,65],cavity)
for a,b in [('FRONT_6mm.dxf','REAR_6mm.dxf'),('END_A_6mm.dxf','END_B_6mm.dxf'),('LID_END_A_6mm_REINFORCED.dxf','LID_END_B_6mm_REINFORCED.dxf'),('LID_FRONT_BEAM_6mm.dxf','LID_REAR_BEAM_6mm.dxf')]:
    check('symmetric_pair:'+a, raws[a]==raws[b])
ring=parsed['BODY_RING_6mm.dxf']; pin=parsed['PIN_DISC_14mm_6mm.dxf'][0]; cap=parsed['LOCK_CAP_22mm_6mm.dxf'][0]
bore=ring[1]
check('bore_diameter',all(near(d,14.6) for d in dim(bore)),dim(bore))
check('pin_diameter',dim(pin)==(14,14),dim(pin))
check('cap_diameter',dim(cap)==(22,22),dim(cap))
clearance=(dim(bore)[0]-dim(pin)[0])/2
check('nominal_radial_clearance',near(clearance,.3),clearance)
overlap=(dim(cap)[0]-dim(bore)[0])/2
check('nominal_cap_radial_overlap',near(overlap,3.7),overlap)
# Clip the outer ring to the remaining top-corner material of the body end.
# Explicit inferred registration: ring local -> end (x-22, y+59).
def clip_axis(points, axis, bound, keep_above):
    out=[]
    for a,b in zip(points, points[1:]+points[:1]):
        ina=(a[axis]>=bound) if keep_above else (a[axis]<=bound)
        inb=(b[axis]>=bound) if keep_above else (b[axis]<=bound)
        if ina: out.append(a)
        if ina != inb:
            t=(bound-a[axis])/(b[axis]-a[axis])
            out.append(tuple(a[k]+t*(b[k]-a[k]) for k in (0,1)))
    return out
foot = clip_axis(clip_axis(ring[0]['points'],0,28,True),1,12,False)
check('ring_foot_nominal_overlap_proposal',near(abs(area(foot)),192),
      {'area_mm2':abs(area(foot)),'ring_to_end_translation':[-22,59],
       'registration_status':'INFERRED_PROPOSAL_NOT_APPROVED'})
check('lid_independent_openings',len(parsed['LID_END_A_6mm_REINFORCED.dxf'])-1==5)
lid_end = parsed['LID_END_A_6mm_REINFORCED.dxf']
outer_crown = max(lid_end[0]['points'], key=lambda p:p[1])
slot_crown = max(lid_end[5]['points'], key=lambda p:p[1])
crown_land = outer_crown[1] - slot_crown[1]
check('skin_slot_crown_land_measurement', near(outer_crown[0],slot_crown[0]) and near(crown_land,.1),
      {'outer_point':outer_crown,'slot_point':slot_crown,'land_mm':crown_land,
       'assessment':'MEASURED_NOT_MANUFACTURING_ACCEPTED'})
beam_slots=[dim(e) for e in parsed['LID_END_A_6mm_REINFORCED.dxf'][1:3]]
check('lid_beam_slots',beam_slots==[(6,6),(6,6)],beam_slots)
skin=parsed['LID_SKIN_4mm.dxf']; cuts=[e for e in skin if e['type']=='LINE']; cutbox=bbox([p for e in cuts for p in e['points']])
check('skin_190_hinge_lines',len(cuts)==190,len(cuts))
check('skin_end_margins',near(cutbox[0]-6,12) and near(316-cutbox[2],12),{'main_panel_edges':[6,316],'cut_bbox':cutbox,'margins':[cutbox[0]-6,316-cutbox[2]]})
check('skin_solid_center_band',all(max(p[0] for p in e['points'])<=154 or min(p[0] for p in e['points'])>=168 for e in cuts),[154,168])
for name,expected in [('V8_2_2_6mm_PRODUCTION_CUT_ONLY.dxf',[14,20,836,368]),('V8_2_2_4mm_LID_SKIN_CUT_ONLY.dxf',[10,10,332,104.7965436107])]:
    bb=summaries[name]['bbox']
    check('sheet_bbox:'+name,all(near(a,b) for a,b in zip(bb,expected)),bb)
# Expected-rejection controls mutate bytes in memory only.
base=raws['FRONT_6mm.dxf']
for name,raw in [('units',base.replace(b'$INSUNITS\n70\n4',b'$INSUNITS\n70\n0')),('open_contour',base.replace(b'90\n41\n70\n1',b'90\n41\n70\n0')),('missing_EOF',base.replace(b'0\nEOF',b'')),('wrong_vertex_count',base.replace(b'90\n41',b'90\n40'))]:
    try:
        parse(raw); rejected=False
    except (ValueError,StopIteration):
        rejected=True
    check('negative:'+name,rejected)
result={'reviewer':'/root/independent_meb_qa','method':'stdlib raw group-code reader and direct arithmetic; no implementation geometry imports',
        'source_commit':COMMIT,'cases':CASES,'summary':dict(collections.Counter(c['status'] for c in CASES)),
        'dxf_measurements':summaries,'limitations':['No solid assembly/insertion path or physical proof','Raw polygon checks are structural, not a complete non-self-intersection or nesting proof','Dimensions deduct nominal unmeasured thickness']}
output=Path(__file__).with_name('MEB-000-independent-evidence.json')
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['summary']), 'unique cases',len(CASES))
for c in CASES:
    if c['status']!='PASS': print(c)
raise SystemExit(any(c['status']=='FAIL' for c in CASES))
