#!/usr/bin/env python3
"""MEB-035: reproducible 4 mm *design-only* lid subassembly study.

New arch profile is a provisional redesign, NOT the original MEB-033 arch.
Requires: cadquery, shapely, scipy, trimesh, numpy, ezdxf, lxml.
Never use these exports as approved manufacture files.
"""
from pathlib import Path
import json, math
import numpy as np
from scipy.optimize import brentq
from shapely.geometry import Polygon, Point, box
from shapely.affinity import translate
import cadquery as cq
import ezdxf, trimesh
from lxml import etree

OUT=Path(__file__).parent.resolve()
ROOF=99.17085434 # MEB-033 full unrolled roof transverse span (mm)
CHORD=85.5       # MEB-033 end outer width, NOT original partial curved rim
AXIAL=324.0      # measured 2D roof skin axial span
T=4.0            # nominal ply
FINGER=7.0
NOTCH=7.25
NOTCH_DEPTH=4.1
FLANGE=8.0        # proposed reinforced low edge
RAIL_Y=(26.,58.) # proposed rail locations: old mortises not reused
HINGE_Y=68.0     # proposed relocation from source local 75mm; G2b blocked
HINGE_Z=2.5
HINGE_R=4.2

R=brentq(lambda r:2*r*math.sin(ROOF/(2*r))-CHORD,ROOF/math.pi+1e-8,500)
HALF=ROOF/(2*R)
RISE=R*(1-math.cos(HALF))
def arc(s,depth=0):
    a=-HALF+s/R
    return(CHORD/2+(R-depth)*math.sin(a),(R-depth)*math.cos(a)-R*math.cos(HALF))
def pts(a,b,depth,step=.3):
    n=max(2,math.ceil((b-a)/step))
    return[arc(a+(b-a)*i/n,depth) for i in range(n+1)]

fingers=[(i*(ROOF-FINGER)/4,i*(ROOF-FINGER)/4+FINGER) for i in range(5)]
notches=[]
for i,(a,b) in enumerate(fingers):
    if i==0:notches.append((0,NOTCH))
    elif i==4:notches.append((ROOF-NOTCH,ROOF))
    else:c=(a+b)/2;notches.append((c-NOTCH/2,c+NOTCH/2))
assert len(fingers)==len(notches)==5
assert all(s0<=f0 and s1>=f1 for (f0,f1),(s0,s1) in zip(fingers,notches))

outline=[arc(0)];prev=0
for a,b in notches:
    if a>prev:outline+=pts(prev,a,0)[1:]
    outline.append(arc(a,NOTCH_DEPTH))
    outline+=pts(a,b,NOTCH_DEPTH,.2)[1:]
    outline.append(arc(b))
    prev=b
if prev<ROOF:outline+=pts(prev,ROOF,0)[1:]
outline += [(CHORD,-FLANGE),(0,-FLANGE)]
outer=Polygon(outline)
assert outer.is_valid
holes=[Point(HINGE_Y,HINGE_Z).buffer(HINGE_R,resolution=96)]
for y in RAIL_Y:holes.append(box(y-2.15,-4.65,y+2.15,2.65))
assert all(outer.contains(h) and h.distance(outer.exterior)>=2.5 for h in holes)
arch=Polygon(outer.exterior,[h.exterior for h in holes]);assert arch.is_valid

def extrude_yz(poly,start,depth):
    solid=cq.Workplane('YZ').polyline(list(poly.exterior.coords)[:-1]).close().extrude(depth)
    for h in poly.interiors:
        cut=cq.Workplane('YZ').polyline(list(h.coords)[:-1]).close().extrude(depth)
        solid=solid.cut(cut)
    return solid.val().translate((start,0,0))
def bent(s0,s1,x0,x1):
    cross=Polygon(pts(s0,s1,0,.25)+list(reversed(pts(s0,s1,T,.25))))
    assert cross.is_valid
    return extrude_yz(cross,x0,x1-x0)

solids={
 'ARCH_LEFT':extrude_yz(arch,0,T),
 'ARCH_RIGHT':extrude_yz(arch,AXIAL-T,T),
 'ROOF_BODY':bent(0,ROOF,T,AXIAL-T)
}
for i,(s0,s1) in enumerate(fingers,1):
    solids[f'TAB_LEFT_{i}']=bent(s0,s1,0,T)
    solids[f'TAB_RIGHT_{i}']=bent(s0,s1,AXIAL-T,AXIAL)
for i,y in enumerate(RAIL_Y,1):
    main=box(y-2,-6.5,y+2,4.5)
    tip=box(y-2,-4.5,y+2,2.5)
    solids[f'RAIL_{i}']=extrude_yz(main,T,AXIAL-2*T).fuse(
        extrude_yz(tip,0,T),extrude_yz(tip,AXIAL-T,T))

checks=[]
for side in ('LEFT','RIGHT'):
    a=solids[f'ARCH_{side}']
    for i in range(1,6):
        tab=solids[f'TAB_{side}_{i}']
        overlap=tab.intersect(a).Volume()
        checks.append({'pair':f'{side}-{i}','overlap_mm3':overlap})
        assert overlap<.0001
    for i in (1,2):
        overlap=solids[f'RAIL_{i}'].intersect(a).Volume()
        checks.append({'pair':f'RAIL_{i}-{side}','overlap_mm3':overlap})
        assert overlap<.0001
assert all(solids[f'RAIL_{i}'].intersect(solids['ROOF_BODY']).Volume()<.0001 for i in (1,2))

assm=cq.Assembly(name='MEB035_DESIGN_ONLY')
scene=trimesh.Scene()
for name,solid in solids.items():
    assm.add(solid,name=name)
    vertices,faces=solid.tessellate(.9)
    m=trimesh.Trimesh(vertices=np.array([v.toTuple() for v in vertices]),
        faces=np.array(faces,dtype=int),process=False)
    m.merge_vertices(digits_vertex=5)
    assert m.is_watertight
    scene.add_geometry(m,geom_name=name)
assm.save(str(OUT/'MEB035_CONCEPT.step'))
(OUT/'MEB035_CONCEPT.glb').write_bytes(scene.export(file_type='glb'))

# R6-R2 contour defect fix: previously (ROOF,4) made finger 5 slope diagonally
# to (ROOF-FINGER,0); full-width tabs must be rectangular at both ends.
roof_flat=[(ROOF,0)]
for i in range(4,-1,-1):
    a,b=fingers[i]
    if i<4:roof_flat.extend([(b,4),(b,0)])
    roof_flat.append((a,0))
    if i>0:roof_flat.append((a,4))
roof_flat.append((0,AXIAL))
for i,(a,b) in enumerate(fingers):
    if i>0:roof_flat.extend([(a,AXIAL-4),(a,AXIAL)])
    roof_flat.append((b,AXIAL))
    if i<4:roof_flat.append((b,AXIAL-4))
roof_poly=Polygon(roof_flat);assert roof_poly.is_valid
# Exact regression: five rectangular 7mm finger tips at BOTH ends, no slopes.
_vertices=list(roof_poly.exterior.coords)[:-1]
_edges=list(zip(_vertices,_vertices[1:]+_vertices[:1]))
assert all(abs(a[0]-b[0])<1e-8 or abs(a[1]-b[1])<1e-8 for a,b in _edges)
def _tip_intervals(y):
    return sorted((min(a[0],b[0]),max(a[0],b[0])) for a,b in _edges
                  if abs(a[1]-y)<1e-8 and abs(b[1]-y)<1e-8 and abs(a[0]-b[0])>1e-8)
_t0,_t1=_tip_intervals(0),_tip_intervals(AXIAL)
assert len(_t0)==len(_t1)==5 and _t0==_t1
assert all(abs(y-x-FINGER)<1e-8 for x,y in _t0)
assert all(abs(x-a)<1e-8 and abs(y-b)<1e-8 for (x,y),(a,b) in zip(_t0,fingers))
rail_flat=Polygon([(0,-4.5),(4,-4.5),(4,-6.5),(320,-6.5),
 (320,-4.5),(324,-4.5),(324,2.5),(320,2.5),(320,4.5),
 (4,4.5),(4,2.5),(0,2.5)])
parts=[('SKIN_WITHOUT_R6',translate(roof_poly,10,10)),
 ('ARCH_LEFT',translate(arch,130,39)),('ARCH_RIGHT',translate(arch,230,39)),
 ('RAIL_1',translate(rail_flat,10,366)),('RAIL_2',translate(rail_flat,10,385))]
min_gap=1e9
for i,(n,a) in enumerate(parts):
    assert a.is_valid and a.bounds[0]>=3 and a.bounds[1]>=3 and a.bounds[2]<=437 and a.bounds[3]<=797
    for n2,b in parts[i+1:]:
        assert a.intersection(b).area <1e-8
        min_gap=min(min_gap,a.distance(b))
assert min_gap>=1.0

svg=['<?xml version="1.0" encoding="UTF-8"?>',
 '<svg xmlns="http://www.w3.org/2000/svg" width="440mm" height="800mm" viewBox="0 0 440 800">',
 '<title>MEB035 DESIGN ONLY - R6 lines intentionally omitted</title>']
doc=ezdxf.new(dxfversion='R2013');doc.header['$INSUNITS']=4;ms=doc.modelspace()
for name,p in parts:
    svg.append(f'<g id="{name}" fill="none" stroke="black" stroke-width="0.15">')
    for i,ring in enumerate([p.exterior,*p.interiors]):
        xy=list(ring.coords)
        svg.append('<polyline points="'+' '.join(f'{x:.10f},{y:.10f}' for x,y in xy)+'"/>')
        ms.add_lwpolyline(xy[:-1],close=True,dxfattribs={'layer':name if i==0 else name+'_HOLE'})
    svg.append('</g>')
svg.append('</svg>')
(OUT/'MEB035_PARTIAL_NEST_DESIGN_ONLY.svg').write_text('\n'.join(svg)+'\n')
doc.saveas(OUT/'MEB035_PARTIAL_NEST_DESIGN_ONLY.dxf')
S=etree.parse(str(OUT/'MEB035_PARTIAL_NEST_DESIGN_ONLY.svg'))
ns={'s':'http://www.w3.org/2000/svg'}
sv=[Polygon([tuple(map(float,t.split(','))) for t in e.get('points').split()])
    for e in S.xpath('//s:polyline',namespaces=ns)]
dx=[Polygon([(float(x),float(y)) for x,y,*r in e.get_points()])
    for e in ezdxf.readfile(OUT/'MEB035_PARTIAL_NEST_DESIGN_ONLY.dxf').modelspace().query('LWPOLYLINE')]
assert len(sv)==len(dx)==11
assert all(a.symmetric_difference(b).area<1e-5 for a,b in zip(sv,dx))

report={'stage':'G1/G2a digital lid study, NOT approved as new product',
 'source_roof_developed_mm':ROOF,'source_complete_outer_arch_width_mm':CHORD,
 'proposed_radius_mm':R,'proposed_rise_mm':RISE,
 'arch_lid_contact_full_arc_mm':R*(2*HALF),
 'arch_rail_mortises':'redesigned at y=26,58 mm','hinge_moved_y_mm':-7,
 'roof_fingers_each_end':len(fingers),'arch_slots_each':len(notches),
 'nominal_3d_overlap_tests':checks,'watertight_meshes':len(solids),
 'concept_2d_nesting':{'parts':len(parts),'contours':len(sv),'minimum_gap_mm':min_gap},
 'R6_living_hinge_slits':'NOT INCLUDED; bending validation required',
 'insertion_path':'NOT_RUN','110_degree_hinge_sweep':'NOT_RUN',
 'whole_product_3d':'NOT_RUN','physical_material_and_kerf':'NOT_RUN',
 'independent_QA':'PENDING','manufacturing_release':'BLOCKED'}
(OUT/'MEB035_STUDY_QA.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
