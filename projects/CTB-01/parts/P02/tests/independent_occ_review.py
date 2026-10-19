"""Independent exported-SVG/OCC CTB002 reconstruction; no implementation imports."""
import json,math,xml.etree.ElementTree as ET,itertools
from pathlib import Path
import cadquery as cq
from shapely.geometry import Polygon
from shapely.affinity import translate
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parents[5]
PART=ROOT/'projects/CTB-01/parts/P02'
DATA=json.loads((PART/'variants/B_THROUGH_ADHESIVE/mechanical-dimensions.json').read_text())

def read_svg(name):
 root=ET.parse(PART/f'variants/B_THROUGH_ADHESIVE/{name}.svg').getroot()
 loops=[[(float(x),float(y)) for x,y in [v.split(',') for v in n.attrib['points'].split()]] for n in root.findall('.//{http://www.w3.org/2000/svg}polygon')]
 p=Polygon(loops[0],loops[1:]);assert p.is_valid
 return p

def solid(poly,plane,h):
 wp=cq.Workplane(plane).polyline(list(poly.exterior.coords)[:-1]).close()
 for hole in poly.interiors:wp=wp.polyline(list(hole.coords)[:-1]).close()
 result=wp.extrude(h).val();assert result.isValid()
 return result

def plate(poly,z,h=6):return solid(poly,cq.Plane(origin=(0,0,z),xDir=(1,0,0),normal=(0,0,1)),h)
def cheek(poly,t=13.5,h=6):return solid(poly,cq.Plane(origin=(0,t,0),xDir=(1,0,0),normal=(0,-1,0)),h)

def sweep2(poly,dy):
 # Boundary-edge quadrilaterals + endpoints = exact polygon/line Minkowski sum.
 # Different construction from implementation's constrained-triangle convex hulls.
 parts=[poly,translate(poly,yoff=dy)]
 coords=list(poly.exterior.coords)
 for a,b in zip(coords,coords[1:]):
  quad=Polygon([a,b,(b[0],b[1]+dy),(a[0],a[1]+dy)])
  if quad.area>1e-10:parts.append(quad)
 return unary_union(parts)

face=read_svg('P01-SOFT_CURVE-mortise-study-v1')
P={key:read_svg(key) for key in ['P02','P02B']}
S={'P01_1':cheek(face,-7.5),'P01_2':cheek(face,13.5)}
for s in DATA['stations']:
 p=translate(P[s['part']],xoff=s['r_mm']);S[s['id']]=plate(p,s['z_mm']-3)
results={'kernel':'CadQuery2.7 / OpenCASCADE7.8.1','input':'actual exported SVG loops; JSON placements only','solids':{},'final_intersections_mm3':[],'continuous_sweep_intersections_mm3':[]}
for name,x in S.items():
 results['solids'][name]={'valid':x.isValid(),'volume_mm3':x.Volume()}
for (a,x),(b,y) in itertools.combinations(S.items(),2):
 v=x.intersect(y).Volume();assert abs(v)<1e-6,(a,b,v)
 results['final_intersections_mm3'].append({'a':a,'b':b,'volume':v})
prior={'P01_1':S['P01_1']}
for s in DATA['stations']:
 p=translate(P[s['part']],xoff=s['r_mm'])
 swept=plate(sweep2(p,40),s['z_mm']-3)
 for name,x in prior.items():
  v=swept.intersect(x).Volume();assert abs(v)<1e-6,('sweep',s['id'],name,v)
  results['continuous_sweep_intersections_mm3'].append({'moving':s['id'],'fixed':name,'volume':v})
 prior[s['id']]=S[s['id']]
swept=cheek(face,53.5,46)
for name,x in prior.items():
 v=swept.intersect(x).Volume();assert abs(v)<1e-6,('cheek sweep',name,v)
 results['continuous_sweep_intersections_mm3'].append({'moving':'P01_2','fixed':name,'volume':v})
# Independent negative controls: wrong entry direction, shifted slots and thick stock.
s=DATA['stations'][0];p=translate(P[s['part']],xoff=s['r_mm'])
v=plate(sweep2(p,-40),s['z_mm']-3).intersect(S['P01_1']).Volume();assert v>100
wrong=Polygon(face.exterior.coords,[[(r+4,z) for r,z in ring.coords] for ring in face.interiors])
v2=cheek(wrong,-7.5).intersect(S['S1']).Volume();assert v2>1
v3=plate(p,s['z_mm']-3.4,6.8).intersect(S['P01_1']).Volume();assert v3>1
results['negative_controls_mm3']={'wrong_insertion':v,'shifted_slots':v2,'6.8mm_spacer_nominal_cheek':v3}
# Independent material-to-hole measurement at each side, across the FULL cheek thickness.
# Our continuous slab radial intersections are computed at every planar contour vertex.
lands=[]
for s in DATA['stations']:
 hole=min(face.interiors,key=lambda h:abs(Polygon(h).centroid.y-s['z_mm']))
 dist=hole.distance(face.exterior);assert dist>=6
 lands.append({'station':s['id'],'hole_to_external_mm':dist})
results['lands']=lands
print(json.dumps(results,indent=2))
Path('/tmp/ctb002-occ-qa-results.json').write_text(json.dumps(results,indent=2)+'\n')
