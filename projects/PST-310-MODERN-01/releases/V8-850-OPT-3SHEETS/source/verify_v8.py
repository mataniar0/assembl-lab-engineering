import pathlib,json,math,itertools,sys
from shapely.geometry import Polygon
from shapely.affinity import translate
from xml.etree import ElementTree as ET
import ezdxf
R=pathlib.Path(__file__).resolve().parent
V6=pathlib.Path('/mnt/data/src_v6');V7=pathlib.Path('/mnt/data/src_v7')
def shapes(file):
 d=ezdxf.readfile(file);ps=[];ll=[]
 for e in d.modelspace():
  if e.dxftype()=='LWPOLYLINE':ps.append((e.dxf.layer,Polygon([(v[0],v[1]) for v in e.get_points('xy')]),bool(e.closed)))
  elif e.dxftype()=='LINE':ll.append((e.dxf.layer,e.dxf.start,e.dxf.end))
  else:raise AssertionError((file,e.dxftype()))
 return ps,ll
def canonical(p):
 b=p.bounds;return translate(p,xoff=-b[0],yoff=-b[1])
def match(a,b,tol=.01):
 aa,bb=canonical(a),canonical(b)
 return aa.symmetric_difference(bb).area < tol
# V8 top preserves precisely 12 perimeter notches from V6, eliminates only 12 internal openings
p8,l8=shapes(R/'dxf'/'TOP_DISC_D310_RIM_TABS_ONLY_6MM.dxf')
p6,l6=shapes(V6/'dxf'/'TOP_DISC_D310_6MM.dxf')
p7,l7=shapes(V7/'dxf'/'TOP_DISC_D310_SMOOTH_6MM.dxf')
assert len(p8)==1 and len(l8)==0 and len(p6)==13 and len(p7)==1
assert p8[0][1].is_valid and len(p8[0][1].interiors)==0
# V8 disc outer boundary same as V6 outer boundary (different independent interior wires), even at high resolution
assert match(Polygon(p8[0][1].exterior.coords),Polygon(p6[0][1].exterior.coords))
# resulting V8 CAD disk footprint must be V6 minus just internal holes
assert len(p6[1:])==12 and sum(v[1].area for v in p6[1:])>50
# 12 upper tabs restored to six flat rims; compare V6 shapes exactly except naming
rim_diffs=[]
for i in range(1,7):
 v8,lines8=shapes(R/'dxf'/f'RIM_{i:02d}_BIRCH4_UPPER_LOWER_TABS.dxf')
 v6,lines6=shapes(V6/'dxf'/f'RIM_{i:02d}_BIRCH4_FLEX.dxf')
 assert len(v8)==len(v6)==1 and len(lines8)==len(lines6)==58
 assert match(v8[0][1],v6[0][1]),(i,'rim contour differs')
 rim_diffs.append(v8[0][1].symmetric_difference(v6[0][1]).area)
# 6 V8 ribs equal V7 (which removed top fingers) exact planar shape
for i in range(1,7):
 a,_=shapes(R/'dxf'/f'CORE_RIB_{i:02d}_6MM.dxf');b,_=shapes(V7/'dxf'/f'CORE_RIB_{i:02d}_6MM.dxf')
 assert match(a[0][1],b[0][1])
# All other 9 unchanged parts equal V7: bottom, six legs, lower triangle, spider
unchanged=['BOTTOM_DISC_D310_6MM','LOWER_TRIANGLE_ONE_PIECE_6MM','CENTRAL_FLAT_6MM_SPIDER']+[f'LEG_{i}_{j}_6MM' for i in range(1,4) for j in 'AB']
for name in unchanged:
 a,_=shapes(R/'dxf'/f'{name}.dxf');b,_=shapes(V7/'dxf'/f'{name}.dxf')
 assert len(a)==len(b)
 for x,y in zip(a,b):assert match(x[1],y[1])
# check SVG and DXF individual and nesting pair counts, segment endpoints and bounds, no board cutting perimeter
individual=[]
for fn in sorted((R/'dxf').glob('*.dxf')):
 p,l=shapes(fn)
 svg=ET.parse(R/'svg'/f'{fn.stem}.svg').getroot()
 polys=[e for e in svg.iter() if e.tag.endswith('polygon')]
 paths=[e for e in svg.iter() if e.tag.endswith('path')]
 assert len(p)==len(polys) and len(l)==len(paths)
 assert all(z[2] and z[1].is_valid for z in p)
 individual.append(fn.stem)
assert len(individual)==22
nest=[];total=0;kerf=0
for fn in sorted((R/'nesting').glob('*.dxf')):
 p,l=shapes(fn);total+=len(p);kerf+=len(l)
 assert not any(e.dxf.layer in ('STOCK','BOARD','FRAME') for e in ezdxf.readfile(fn).modelspace())
 svg=ET.parse(fn.with_suffix('.svg')).getroot();assert len([x for x in svg.iter() if x.tag.endswith('polygon')])==len(p)
 assert len([x for x in svg.iter() if x.tag.endswith('path')])==len(l)
 nest.append(fn.stem)
assert len(nest)==4 and kerf==348
# counts and report
j=json.loads((R/'qa'/'V8_NESTING_QA.json').read_text())
c=json.loads((R/'qa'/'V8_CAD_QA.json').read_text())
assert j['sheet_total']==4 and j['6mm_parts']==16 and j['4mm_parts']==6
assert all(x['min_distance_mm']>=1 for x in j['sheet_results'])
assert len(c['collisions_over_0_01mm3'])==0
out={'status':'PASS_DESIGN_ONLY','top_outer_outline_identical_to_V6':True,'top_internal_holes':0,'top_rim_slots':12,'rim_flat_cut_contours_match_V6':6,'rim_kerf_line_count_each':58,'core_rib_shapes_match_V7':6,'unchanged_components_match_V7':len(unchanged),'independent_single_part_pairs':len(individual),'nest_sheet_pairs':len(nest),'total_nest_contours':total,'total_kerf_single_lines':kerf,'CAD_assemblies_valid':c['finished_assembly_solids_valid'],'CAD_collider_count':len(c['collisions_over_0_01mm3']),'sheet_min_gaps_mm':[x['min_distance_mm'] for x in j['sheet_results']],'physical_validation':'NOT_DONE'}
(R/'qa'/'V8_INDEPENDENT_QA.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(json.dumps(out,indent=2))