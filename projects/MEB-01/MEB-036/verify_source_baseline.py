#!/usr/bin/env python3
"""Reproduce source inventory and fail-closed assembly readiness checks.
This does not assign unknown assembly poses or generate manufacturing files.
"""
from pathlib import Path
import csv, json, itertools, math, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'MEB-033'/'cutting'/'MEB033_ALL20_PLUS_CURVE_R6_4MM_440x800_GAP1MM_DESIGN_ONLY'
NS={'s':'http://www.w3.org/2000/svg'}
def clean(p):
    return p[:-1] if len(p)>1 and math.dist(p[0],p[-1])<1e-6 else p
groups={}
root=ET.parse(BASE.with_suffix('.svg')).getroot()
for g in root.findall('.//s:g',NS):
    name=g.get('id')
    loops=[clean([tuple(map(float,v.split(','))) for v in e.get('points').split()])
           for e in g.findall('s:polyline',NS)]
    if loops: groups[name]=loops
product=[n for n in groups if not n.startswith('MEB029_')]
assert len(product)==20 and len(groups)==21
assert sum(map(len,groups.values()))==31
r6=root.find('.//s:g[@id="LID_SKIN_RADIAL_4MM"]',NS)
svg_lines=[tuple(float(e.get(k)) for k in ('x1','y1','x2','y2')) for e in r6.findall('s:line',NS)]
assert len(svg_lines)==88
raw=BASE.with_suffix('.dxf').read_text().splitlines()
assert len(raw)%2==0
pairs=list(zip((x.strip() for x in raw[::2]),(x.strip() for x in raw[1::2])))
seen=set(); lines=[]; i=0
while i<len(pairs):
    if pairs[i] not in [('0','LWPOLYLINE'),('0','LINE')]:
        i+=1;continue
    j=i+1
    while j<len(pairs) and pairs[j][0]!='0':j+=1
    p=pairs[i:j]
    if p[0][1]=='LINE':
        d=dict(p);lines.append(tuple(float(d[k]) for k in ('10','20','11','21')))
    else:
        k=p.index(('1001','MEB028'));name=p[k+1][1]
        pts=clean([(float(v),float(p[h+1][1])) for h,(key,v) in enumerate(p[:-1])
                   if key=='10' and p[h+1][0]=='20'])
        match=[n for n,q in enumerate(groups[name])
               if len(q)==len(pts) and all(math.dist(a,b)<1e-6 for a,b in zip(q,pts))]
        assert len(match)==1 and (name,match[0]) not in seen, (name,match)
        seen.add((name,match[0]))
    i=j
assert len(seen)==31 and len(lines)==88
assert all(all(abs(a-b)<1e-6 for a,b in zip(p,q)) for p,q in zip(svg_lines,lines))
register=list(csv.DictReader((ROOT/'MEB036_PAIR_REGISTER.csv').open()))
expected={frozenset(p) for p in itertools.combinations(product,2)}
actual={frozenset((r['part_a'],r['part_b'])) for r in register}
assert len(register)==len(actual)==len(expected)==190 and actual==expected
# An inventory of pairs is not a collision test.
unrun=sum(r['collision']=='NOT_RUN' for r in register)
report={'original_source_contours_match':len(seen),'original_r6_lines_match':len(lines),
        'product_parts':len(product),'jigs':1,'pair_register_size':len(register),
        'collision_not_run':unrun,'whole_assembly_status':'BLOCKED',
        'reason':'No validated assembly placements or motion / insertion evidence.',
        'production_release':False}
print(json.dumps(report,indent=2))
