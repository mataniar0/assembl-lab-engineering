"""Three-arm CSH3Y studies; actual extruded solids and full translational sweeps."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator
from shapely.affinity import rotate, translate
from shapely.geometry import Polygon, Point, LineString, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

PART=Path(__file__).resolve().parents[1]
PROJECT=PART.parents[1]
ROOT=PROJECT.parents[1]
spec=importlib.util.spec_from_file_location('p02_reference',PROJECT/'parts/P02/src/model.py')
p02=importlib.util.module_from_spec(spec);spec.loader.exec_module(p02)
CONCEPTS=('A_COMPACT_CLOSED','B_DUAL_CLOSED','C_OPEN_REMOVABLE')
EPS=1e-6


def inputs():
    d=json.loads((PART/'src/design.json').read_text())
    Draft202012Validator(json.loads((PART/'src/design.schema.json').read_text())).validate(d)
    upstream,base=p02.inputs()
    return d,upstream,base


def paths(poly):
    p=orient(poly,1)
    return [[[round(x,6),round(y,6)] for x,y in list(p.exterior.coords)[:-1]]]+[
        [[round(x,6),round(y,6)] for x,y in list(h.coords)[:-1]] for h in p.interiors]


def digest(poly):return hashlib.sha256(json.dumps(paths(poly),separators=(',',':')).encode()).hexdigest()


def y_profile(name,d):
    hub=Point(0,0).buffer(d['hub_radius_mm'],quad_segs=d['hub_circle_segments']//4)
    pieces=[hub];half=d['arm_core_width_mm']/2
    for angle in (0,120,240):
        arm=box(0,-half,d['variants'][name]['arm_tip_local_r_mm'],half)
        tabs=[box(a,-d['tab_tip_abs_t_mm'],b,d['tab_tip_abs_t_mm']) for a,b in d['variants'][name]['tabs_r_mm']]
        pieces.append(rotate(unary_union([arm,*tabs]),angle,origin=(0,0)))
    raw=orient(unary_union(pieces),1)
    coords=np.array(list(raw.exterior.coords)[:-1])
    radii=[]
    for i,v in enumerate(coords):
        u=v-coords[i-1];w=coords[(i+1)%len(coords)]-v
        cross=u[0]*w[1]-u[1]*w[0]
        radii.append(d['convex_radius_mm'] if cross>0 else d['concave_radius_mm'])
    out=p02.master.Outline(d['fillet_chord_mm'])
    p02.master.rounded_polygon(out,coords,radii)
    face=Polygon(out.final())
    if not face.is_valid or face.geom_type!='Polygon' or face.interiors:
        raise ValueError('Y must be one connected simple part')
    return orient(face,1)


def cheek(name,d,u):
    material,old_holes=p02.cheek('B_THROUGH_ADHESIVE',u)
    half=d['thickness_mm']/2+d['slot_allowance_each_side_mm'];z=d['y_center_z_mm']
    extra=[]
    for a,b in d['variants'][name]['tabs_r_mm']:
        low=a-d['slot_allowance_each_side_mm']
        if name=='C_OPEN_REMOVABLE':low=d['open_channel_inner_r_mm']
        extra.append(p02.rounded_rect(low,z-half,b+d['slot_allowance_each_side_mm'],z+half,d['slot_radius_mm']))
    return material.difference(unary_union(extra)),extra


def rotation(solid,angle):
    a=math.radians(angle);c,s=math.cos(a),math.sin(a)
    return solid.transform([[c,-s,0,0],[s,c,0,0],[0,0,1,0]])


def local_parts(name,d,u,b):
    material,_=cheek(name,d,u)
    t=b['frozen']['cheek_thickness_mm'];offsets=b['coordinate_frame']['cheek_center_t_offsets_mm']
    result={f'P01_{i+1}':p02.cheek_solid(material,center-t/2,t) for i,center in enumerate(offsets)}
    for st in p02.stations(u):
        face=translate(p02.spacer('B_THROUGH_ADHESIVE',st['part'],u,b),xoff=st['r_mm'])
        result[st['id']]=p02.plate_solid(face,st['z_mm']-u['spacer_thickness_mm']/2,u['spacer_thickness_mm'])
    return result


def assembly(name,d,u,b):
    solids={'P03':p02.plate_solid(y_profile(name,d),d['y_center_z_mm']-d['thickness_mm']/2,d['thickness_mm'])}
    local=local_parts(name,d,u,b)
    for leg,angle in enumerate(b['frozen']['leg_angles_deg'],1):
        solids.update({f'L{leg}_{k}':rotation(v,angle) for k,v in local.items()})
    return solids


def final_matrix(solids):return p02.collision_matrix(solids)


def cheek_sweep(name,d,u,b,which):
    material,_=cheek(name,d,u);thickness=b['frozen']['cheek_thickness_mm']
    tmin=b['coordinate_frame']['cheek_center_t_offsets_mm'][which]-thickness/2
    distance=d['cheek_insertion_t_mm']
    if which==0:tmin-=distance
    return p02.cheek_solid(material,tmin,thickness+distance)


def y_first(name,d,u,b):
    all_parts=assembly(name,d,u,b);prior={'P03':all_parts['P03']};steps=[]
    for leg,angle in enumerate(b['frozen']['leg_angles_deg'],1):
        movements=[('P01_1',cheek_sweep(name,d,u,b,0),[0,-d['cheek_insertion_t_mm'],0])]
        for st in p02.stations(u):
            face=translate(p02.spacer('B_THROUGH_ADHESIVE',st['part'],u,b),xoff=st['r_mm'])
            sweep=p02.plate_solid(p02.swept_polygon(face,0,d['cheek_insertion_t_mm']),st['z_mm']-3,6)
            movements.append((st['id'],sweep,[0,d['cheek_insertion_t_mm'],0]))
        movements.append(('P01_2',cheek_sweep(name,d,u,b,1),[0,d['cheek_insertion_t_mm'],0]))
        for key,sweep,start in movements:
            moving=f'L{leg}_{key}';sweep=rotation(sweep,angle)
            intersections=[{'fixed':k,'volume_mm3':max(0,(sweep^v).volume())} for k,v in prior.items()]
            steps.append({'moving':moving,'angle_deg':angle,'local_start_offset_mm':start,'local_end_offset_mm':[0,0,0],
                          'continuous_intersections':intersections})
            prior[moving]=all_parts[moving]
    worst=max(x['volume_mm3'] for s in steps for x in s['continuous_intersections'])
    return {'status':'PASS_CAD_LOCAL_BASE_PATH' if worst<EPS else 'BLOCKED',
            'steps':steps,'moving_stages':len(steps),'checks':sum(len(s['continuous_intersections']) for s in steps),
            'maximum_intersection_mm3':worst,'epsilon_mm3':EPS,
            'initial_state':'P03 at410 in fixture; no tabletop/discs/ring; spacers and cheeks externally supported'}


def module_sweeps(name,d,u,b,axis):
    material,_=cheek(name,d,u);distance=d['module_vertical_stroke_mm'] if axis=='vertical' else (
        d['module_radial_stroke_mm'] if axis=='radial' else d['cheek_insertion_t_mm'])
    result={};thickness=b['frozen']['cheek_thickness_mm']
    for i,center in enumerate(b['coordinate_frame']['cheek_center_t_offsets_mm'],1):
        if axis=='tangential':s=p02.cheek_solid(material,center-thickness/2,thickness+distance)
        else:
            swept=p02.swept_polygon(material,distance if axis=='radial' else 0,distance if axis=='vertical' else 0)
            s=p02.cheek_solid(swept,center-thickness/2,thickness)
        result[f'P01_{i}']=s
    for st in p02.stations(u):
        face=translate(p02.spacer('B_THROUGH_ADHESIVE',st['part'],u,b),xoff=st['r_mm'])
        if axis=='vertical':s=p02.plate_solid(face,st['z_mm']-3,6+distance)
        else:s=p02.plate_solid(p02.swept_polygon(face,distance if axis=='radial' else 0,
                                               distance if axis=='tangential' else 0),st['z_mm']-3,6)
        result[st['id']]=s
    return result,distance


def prebuilt(name,d,u,b,axis):
    all_parts=assembly(name,d,u,b);sweeps,distance=module_sweeps(name,d,u,b,axis)
    prior={'P03':all_parts['P03']};stages=[]
    for leg,angle in enumerate(b['frozen']['leg_angles_deg'],1):
        checks=[]
        for key,sweep in sweeps.items():
            moving=f'L{leg}_{key}';world=rotation(sweep,angle)
            checks.extend({'moving':moving,'fixed':k,'volume_mm3':max(0,(world^v).volume())} for k,v in prior.items())
        stages.append({'leg':leg,'angle_deg':angle,'continuous_checks':checks})
        prior.update({k:v for k,v in all_parts.items() if k.startswith(f'L{leg}_')})
    worst=max(x['volume_mm3'] for s in stages for x in s['continuous_checks'])
    return {'status':'PASS_CAD_REMOVABLE_PATH' if worst<EPS else 'BLOCKED',
            'axis':axis,'stroke_mm':distance,'stages':stages,'maximum_intersection_mm3':worst,
            'checks':sum(len(s['continuous_checks']) for s in stages),'epsilon_mm3':EPS,
            'limits':'If first stage blocks, later checks are counterfactual witnesses, not executable assembly stages; no general proof about all possible rigid rotations.'}


def central_insertion(name,d,u,b,axis):
    face=y_profile(name,d);z0=d['y_center_z_mm']-d['thickness_mm']/2
    if axis=='vertical':
        sweep=p02.plate_solid(face,z0,d['thickness_mm']+d['module_vertical_stroke_mm'])
    else:
        sweep=p02.plate_solid(p02.swept_polygon(face,d['module_radial_stroke_mm'],0),z0,d['thickness_mm'])
    fixed=assembly(name,d,u,b)
    checks=[{'fixed':k,'volume_mm3':max(0,(sweep^v).volume())} for k,v in fixed.items() if k!='P03']
    worst=max(x['volume_mm3'] for x in checks)
    return {'status':'BLOCKED' if worst>EPS else 'PASS_CAD_PATH','axis':axis,
            'continuous_intersections':checks,'checks':len(checks),'maximum_intersection_mm3':worst,
            'limits':'Specified vertical or global-X translation only; no proof about all possible rigid motions'}


def metrics(name,d,u,b):
    face=y_profile(name,d);material,holes=cheek(name,d,u)
    old,_=p02.cheek('B_THROUGH_ADHESIVE',u)
    _,s4holes=p02.cheek('B_THROUGH_ADHESIVE',u)
    old_s4=s4holes[-1]
    zmin=d['y_center_z_mm']-d['thickness_mm']/2
    return {'area_mm2':face.area,'maximum_global_radius_mm':max(math.hypot(x,y) for x,y in face.exterior.coords),
            'arm_tip_local_r_mm':d['variants'][name]['arm_tip_local_r_mm'],'local_end_land_to_r90_mm':90-d['variants'][name]['arm_tip_local_r_mm'],
            'old_overhang_mm':94-90,
            'tab_through_cheek_depth_mm':d['tab_tip_abs_t_mm']-7.5,
            'slot_radial_and_Z_allowance_each_side_mm':d['slot_allowance_each_side_mm'],
            'disc_lower_Z_gap_mm':456-(zmin+d['thickness_mm']),
            'disc_upper_Z_gap_mm':480-(zmin+d['thickness_mm']),'core_gap_each_side_mm':(15-d['arm_core_width_mm'])/2,
            'tabs_r_mm':d['variants'][name]['tabs_r_mm'],'tab_bearing_radial_sum_mm':sum(b-a for a,b in d['variants'][name]['tabs_r_mm']),
            'Y_z_mm':[zmin,zmin+d['thickness_mm']],
            'Y_hole_z_mm':[d['y_center_z_mm']-d['thickness_mm']/2-d['slot_allowance_each_side_mm'],
                           d['y_center_z_mm']+d['thickness_mm']/2+d['slot_allowance_each_side_mm']],
            'new_hole_to_outer_land_mm':[h.distance(p02.outer().exterior) if p02.outer().covers(h) else 0 for h in holes],
            'new_hole_to_S4_hole_mm':[h.distance(old_s4) for h in holes],
            'new_hole_between_web_mm':holes[0].distance(holes[1]) if len(holes)>1 else None,
            'cheek_material_area_removed_mm2':old.area-material.area,
            'cheek_original_outer_preserved':Polygon(material.exterior).symmetric_difference(p02.outer()).area<1e-6,
            'Y_to_spacer_S4_Z_gap_mm':zmin-(390+3),'Y_to_underside_Z_gap_mm':450-(zmin+d['thickness_mm']),
            'Y_to_ring_band_Z_gap_mm':zmin-265,'hub_area_mm2':Point(0,0).buffer(d['hub_radius_mm'],quad_segs=36).area,
            'arm_neck_nominal_section_mm2':d['arm_core_width_mm']*d['thickness_mm'],
            'status':'DESIGN_ONLY; ideal wood bearing hypotheses only, no adhesive/positive outward/strength/physical approval'}
