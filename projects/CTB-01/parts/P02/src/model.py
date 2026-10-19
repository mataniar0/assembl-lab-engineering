"""Local r,t,z CTB002 candidates. Continuous sweeps are geometric, not physical tests."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import manifold3d as m
import numpy as np
from jsonschema import Draft202012Validator
from shapely import constrained_delaunay_triangles
from shapely.affinity import translate
from shapely.geometry import Polygon, LineString, box, MultiPoint
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

PART=Path(__file__).resolve().parents[1]
PROJECT=PART.parents[1]
P01=PROJECT/'parts/P01'
spec=importlib.util.spec_from_file_location('p01_master',P01/'src/model.py')
master=importlib.util.module_from_spec(spec)
spec.loader.exec_module(master)
CONCEPTS=('A_KEYED_HEAD','B_THROUGH_ADHESIVE','C_ASYMMETRIC')


def inputs():
    d=json.loads((PART/'src/design.json').read_text())
    schema=json.loads((PART/'src/design.schema.json').read_text())
    Draft202012Validator(schema).validate(d)
    _,b=master.inputs()
    return d,b


def outer():
    return Polygon(master.profile('SOFT_CURVE')[0])


def rounded_rect(x0,y0,x1,y1,r):
    if r<=0 or 2*r>=min(x1-x0,y1-y0):
        raise ValueError('Unachievable candidate radius/dimensions')
    return box(x0+r,y0+r,x1-r,y1-r).buffer(r,quad_segs=8)


def contour(poly):
    return [[round(x,6),round(y,6)] for x,y in list(orient(poly,sign=1).exterior.coords)[:-1]]


def digest(poly):
    return hashlib.sha256(json.dumps(contour(poly),separators=(',',':')).encode()).hexdigest()


def stations(d):
    result=[]
    p=outer()
    half=d['spacer_thickness_mm']/2+d['slot_allowance_each_side_mm']
    for index,z in enumerate(d['station_z_mm']):
        # Exact polygon extrema across the slab, including every rail vertex in it.
        levels=[z-half,z+half]+[y for x,y in p.exterior.coords if z-half<y<z+half]
        cuts=[p.intersection(LineString([[-1000,y],[1000,y]])) for y in levels]
        low=max(c.bounds[0] for c in cuts); high=min(c.bounds[2] for c in cuts)
        result.append({'id':f'S{index+1}','part':'P02B' if index==0 else 'P02',
                       'z_mm':z,'r_mm':(low+high)/2,'common_section_r_mm':[low,high]})
    return result


def spacer(concept,part,d,b):
    p=d['parts'][part]; gap=b['frozen']['leg_inner_gap_mm']; h=gap/2
    outside=h+b['frozen']['cheek_thickness_mm']
    w=p['body_radial_width_mm']
    if concept=='B_THROUGH_ADHESIVE':
        a=p['tab_radial_width_mm']/2
        vertices=[[-w/2,-h],[-a,-h],[-a,-outside],[a,-outside],[a,-h],[w/2,-h],
                  [w/2,h],[a,h],[a,outside],[-a,outside],[-a,h],[-w/2,h]]
    elif concept=='C_ASYMMETRIC':
        a=p['asymmetric_tab_width_mm']/2; off=p['asymmetric_radial_offset_mm']
        # Negative end uses -off, positive end +off; positive engagement only4 mm.
        short=outside-2
        vertices=[[-w/2,-h],[-off-a,-h],[-off-a,-outside],[-off+a,-outside],[-off+a,-h],[w/2,-h],
                  [w/2,h],[off+a,h],[off+a,short],[off-a,short],[off-a,h],[-w/2,h]]
    else:
        neck=p['key_neck_radial_width_mm']/2; head=p['key_head_radial_width_mm']/2
        e=d['key_head_extra_length_t_mm']
        vertices=[[-w/2,-h],[-neck,-h],[-neck,-outside],[-head,-outside],[-head,-outside-e],
                  [head,-outside-e],[head,-outside],[neck,-outside],[neck,-h],[w/2,-h],
                  [w/2,h],[neck,h],[neck,outside],[head,outside],[head,outside+e],
                  [-head,outside+e],[-head,outside],[-neck,outside],[-neck,h],[-w/2,h]]
    outline=master.Outline(.005)
    arr=np.array(vertices,float)
    radii=[]
    # Contours above are CCW; use smaller root radius for concave returns.
    sign=1 if Polygon(vertices).exterior.is_ccw else -1
    for i,v in enumerate(arr):
        a=v-arr[i-1]; c=arr[(i+1)%len(arr)]-v
        cross=a[0]*c[1]-a[1]*c[0]
        radii.append(d['convex_corner_radius_mm'] if cross*sign>0 else d['root_corner_radius_mm'])
    master.rounded_polygon(outline,vertices,radii)
    poly=Polygon(outline.final())
    if not poly.is_valid or len(poly.interiors):raise ValueError('Invalid spacer')
    return orient(poly,1)


def slot_shapes(concept,station,d):
    p=d['parts'][station['part']]; z=station['z_mm']; r=station['r_mm']
    a=d['slot_allowance_each_side_mm']; half=d['spacer_thickness_mm']/2+a
    radius=d['slot_corner_radius_mm']
    if concept=='B_THROUGH_ADHESIVE':
        width=p['tab_radial_width_mm']+2*a
        return [rounded_rect(r-width/2,z-half,r+width/2,z+half,radius)]
    if concept=='C_ASYMMETRIC':
        width=p['asymmetric_tab_width_mm']+2*a
        return [rounded_rect(r+off-width/2,z-half,r+off+width/2,z+half,radius)
                for off in (-p['asymmetric_radial_offset_mm'],p['asymmetric_radial_offset_mm'])]
    neck=p['key_neck_radial_width_mm']+2*a; head=p['key_head_radial_width_mm']+2*a
    # Union of the insertion window and laterally displaced seating window.
    return [unary_union([rounded_rect(r-neck/2,z-half,r+neck/2,z+half,radius),
                         rounded_rect(r+d['key_slide_r_mm']-head/2,z-half,
                                      r+d['key_slide_r_mm']+head/2,z+half,radius)])]


def cheek(concept,d):
    holes=[h for s in stations(d) for h in slot_shapes(concept,s,d)]
    return outer().difference(unary_union(holes)),holes


def cross_section(poly):
    p=orient(poly,1)
    return m.CrossSection([list(p.exterior.coords)[:-1]]+
                          [list(r.coords)[:-1] for r in p.interiors])


def plate_solid(poly,z0,height):
    return m.Manifold.extrude(cross_section(poly),height).translate([0,0,z0])


def cheek_solid(poly,t0,thickness):
    s=m.Manifold.extrude(cross_section(poly),thickness)
    return s.transform([[1,0,0,0],[0,0,1,t0],[0,1,0,0]])


def assembly(concept,d,b,stock=None):
    material,holes=cheek(concept,d)
    thick=b['frozen']['cheek_thickness_mm'] if stock is None else stock
    positions=b['coordinate_frame']['cheek_center_t_offsets_mm']
    solids={f'P01_{i+1}':cheek_solid(material,t-thick/2,thick) for i,t in enumerate(positions)}
    for s in stations(d):
        face=translate(spacer(concept,s['part'],d,b),xoff=s['r_mm'])
        solids[s['id']]=plate_solid(face,s['z_mm']-(d['spacer_thickness_mm'] if stock is None else stock)/2,
                                   d['spacer_thickness_mm'] if stock is None else stock)
    return solids


def collision_matrix(solids):
    names=list(solids)
    return [{'a':names[i],'b':names[j],'intersection_mm3':max(0,(solids[names[i]]^solids[names[j]]).volume())}
            for i in range(len(names)) for j in range(i)]


def swept_polygon(poly,dx,dy):
    # Exact Minkowski sum with a line segment using constrained triangulation.
    triangles=constrained_delaunay_triangles(poly)
    parts=[]
    for triangle in triangles.geoms:
        pts=list(triangle.exterior.coords)[:-1]
        parts.append(MultiPoint(pts+[(x+dx,y+dy) for x,y in pts]).convex_hull)
    return unary_union(parts)


def insertion(concept,d,b):
    if concept=='A_KEYED_HEAD':
        return {'status':'BLOCKED','reason':'head capture needs coordinated radial slide plus reverse-slide restraint; low cheek land also screened below hypothesis', 'steps':[]}
    material,_=cheek(concept,d)
    all_solids=assembly(concept,d,b)
    prior={'P01_1':all_solids['P01_1']}
    steps=[]; distance=d['insertion_start_offset_t_mm']
    for s in stations(d):
        face=translate(spacer(concept,s['part'],d,b),xoff=s['r_mm'])
        sweep=plate_solid(swept_polygon(face,0,distance),s['z_mm']-d['spacer_thickness_mm']/2,d['spacer_thickness_mm'])
        collisions={name:max(0,(sweep^solid).volume()) for name,solid in prior.items()}
        steps.append({'moving':s['id'],'translation_start_rt_z_mm':[0,distance,0],
                      'translation_end_rt_z_mm':[0,0,0],'continuous_sweep_intersections_mm3':collisions})
        prior[s['id']]=all_solids[s['id']]
    # Moving cheek from t50.5 to10.5 has the same r-z section over its full t sweep.
    tmin=b['coordinate_frame']['cheek_center_t_offsets_mm'][1]-b['frozen']['cheek_thickness_mm']/2
    sweep=cheek_solid(material,tmin,b['frozen']['cheek_thickness_mm']+distance)
    collisions={name:max(0,(sweep^solid).volume()) for name,solid in prior.items()}
    steps.append({'moving':'P01_2','translation_start_rt_z_mm':[0,distance,0],
                  'translation_end_rt_z_mm':[0,0,0],'continuous_sweep_intersections_mm3':collisions})
    worst=max([v for step in steps for v in step['continuous_sweep_intersections_mm3'].values()])
    return {'status':'PASS_CAD_LOCAL_SWEEP' if worst<1e-6 else 'FAIL',
            'volume_epsilon_mm3':1e-6,'maximum_collision_mm3':worst,'steps':steps,
            'limits':'Rigid nominal plates, translational paths only; support fixtures required; no glue/fit/physical/whole-table approval'}


def land_report(concept,d):
    material,holes=cheek(concept,d); exterior=outer().exterior
    return [{'station':s['id'],'z_mm':s['z_mm'],
             'minimum_hole_to_external_contour_mm':min(h.distance(exterior) if outer().covers(h) else 0 for h in slot_shapes(concept,s,d)),
             'contained':all(outer().covers(h) for h in slot_shapes(concept,s,d))}
            for s in stations(d)]
