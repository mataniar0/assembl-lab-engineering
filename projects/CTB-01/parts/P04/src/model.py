"""CTB004 candidate material, explicit mating witnesses and exact translational sweeps.
No upstream geometry is edited. Witnesses are interface reservations, not final P05 parts.
"""
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator
from shapely.affinity import rotate, translate
from shapely.geometry import Point, Polygon, LineString, box
from shapely.ops import unary_union

PART=Path(__file__).resolve().parents[1]
PROJECT=PART.parents[1]
ROOT=PROJECT.parents[1]
spec=importlib.util.spec_from_file_location('p03_reference',PROJECT/'parts/P03/src/model.py')
p03=importlib.util.module_from_spec(spec);spec.loader.exec_module(p03)
p02=p03.p02
paths=p03.paths
digest=p03.digest
CONCEPTS=('A','B','C')


def inputs():
    d=json.loads((PART/'src/design.json').read_text())
    Draft202012Validator(json.loads((PART/'src/design.schema.json').read_text())).validate(d)
    d3,u,b=p03.inputs()
    return d,d3,u,b


def circle(radius,d):return Point(0,0).buffer(radius,quad_segs=d['circle_segments']//4)


def tongues(d3,u,b):
    cheek,_=p03.cheek('A_COMPACT_CLOSED',d3,u)
    rz=cheek.intersection(box(-1000,450,1000,488))
    r0,_,r1,_=rz.bounds
    result=[]
    for leg,angle in enumerate(b['frozen']['leg_angles_deg'],1):
        for i,t in enumerate(b['coordinate_frame']['cheek_center_t_offsets_mm'],1):
            xy=rotate(box(r0,t-3,r1,t+3),angle,origin=(0,0))
            solid=p03.rotation(p02.cheek_solid(rz,t-3,6),angle)
            result.append({'id':f'L{leg}_P01_{i}','angle_deg':angle,'t_center_mm':t,
                           'rz':rz,'xy':xy,'solid':solid})
    return result


def tongue_slots(d,d3,u,b):
    result=[]
    for item in tongues(d3,u,b):
        r0,_,r1,_=item['rz'].bounds;t=item['t_center_mm']
        a=d['tongue_allowance_radial_each_side_mm'];c=d['tongue_allowance_t_each_side_mm']
        poly=p02.rounded_rect(r0-a,t-3-c,r1+a,t+3+c,d['tongue_slot_corner_radius_mm'])
        result.append(rotate(poly,item['angle_deg'],origin=(0,0)))
    return result


def family(name,angle):return 'OPEN' if name=='A' or (name=='C' and angle%120==0) else 'RAIL'


def web_cuts(name,layer,d):
    result=[]
    for angle in range(0,360,60):
        kind=family(name,angle);half=d['web_slot_width_mm']/2
        a,c=(d['open_start_r_mm'][layer],96.5) if kind=='OPEN' else d['rail_cut_r_mm'][layer]
        poly=rotate(box(a,-half,c,half),angle,origin=(0,0))
        result.append({'angle_deg':angle,'family':kind,'poly':poly})
    return result


def disk(name,layer,d,d3,u,b,omit_tongue=None,web_angle_error=0):
    holes=[s for i,s in enumerate(tongue_slots(d,d3,u,b)) if i!=omit_tongue]
    holes += [rotate(c['poly'],web_angle_error,origin=(0,0)) for c in web_cuts(name,layer,d)]
    diameter=d['variants'][name]['upper_center_diameter_mm'] if layer=='P04U' else 0
    if diameter:holes.append(circle(diameter/2,d))
    return circle(d['disk_diameter_mm']/2,d).difference(unary_union(holes))


def witness(kind,d):
    full=box(*[d['web_range_r_mm'][0],d['web_range_z_mm'][0],d['web_range_r_mm'][1],d['web_range_z_mm'][1]])
    if kind=='OPEN':return full.difference(box(*d['open_witness_relief_rz_mm']))
    a,c=d['rail_r_mm'];z0,z1=d['web_range_z_mm']
    return unary_union([box(a,z0,c,z1),box(d['outer_web_start_r_mm'],z0,169,z1),box(*d['bridge_rz_mm'])])


def witness_solids(name,d):
    return {f'W{angle//60+1}_{family(name,angle)}':p03.rotation(p02.cheek_solid(witness(family(name,angle),d),-3,6),angle)
            for angle in range(0,360,60)}


def base(d3,u,b):return p03.assembly('A_COMPACT_CLOSED',d3,u,b)


def assembly(name,d,d3,u,b):
    solids=base(d3,u,b)
    solids.update({layer:p02.plate_solid(disk(name,layer,d,d3,u,b),z[0],6) for layer,z in d['layers_z_mm'].items()})
    return solids


def skin(d,d3,u,b):return circle(171,d).difference(unary_union(tongue_slots(d,d3,u,b)))


def checks(swept,prior):return [{'fixed':k,'volume_mm3':max(0,(swept^s).volume())} for k,s in prior.items()]


def step(label,swept,prior,start,end,role):
    hits=checks(swept,prior);worst=max([0]+[i['volume_mm3'] for i in hits])
    return {'moving':label,'role':role,'start_offset_xyz_mm':start,'end_offset_xyz_mm':end,
            'method':'EXACT_TRANSLATION_SWEPT_SOLID','continuous_intersections':hits,
            'maximum_intersection_mm3':worst,'status':'PASS_CAD_PATH' if worst<1e-6 else 'BLOCKED'}


def lower_sweep(face,target,start):return p02.plate_solid(face,target,start+6-target)


def assembly_paths(name,d,d3,u,b):
    all_solids=assembly(name,d,d3,u,b);prior=base(d3,u,b);steps=[];start=d['path_start_bottom_z_mm']
    envelope=p02.plate_solid(skin(d,d3,u,b),450,6)
    steps.append(step('P07B_ENVELOPE',lower_sweep(skin(d,d3,u,b),450,start),prior,[0,0,start-450],[0,0,0],'RESERVATION_NOT_BOM'))
    prior['P07B_ENVELOPE']=envelope
    for layer,z in d['layers_z_mm'].items():
        steps.append(step(layer,lower_sweep(disk(name,layer,d,d3,u,b),z[0],start),prior,[0,0,start-z[0]],[0,0,0],'REAL_PART'))
        prior[layer]=all_solids[layer]
    reverse=step('P04L_AFTER_P04U',lower_sweep(disk(name,'P04L',d,d3,u,b),456,start),
                 {'P04U':all_solids['P04U']},[0,0,64],[0,0,0],'COUNTERFACTUAL_BLOCKED_ORDER')
    late_skin=step('P07B_AFTER_DISKS',lower_sweep(skin(d,d3,u,b),450,start),
                   {k:all_solids[k] for k in ('P04L','P04U')},[0,0,70],[0,0,0],'COUNTERFACTUAL_BLOCKED_ORDER')
    # Correct prospective matching interfaces: rail witnesses before U; open witnesses after U.
    virtual=base(d3,u,b);virtual['P07B_ENVELOPE']=envelope;virtual['P04L']=all_solids['P04L'];wsteps=[]
    ws=witness_solids(name,d)
    for angle in range(0,360,60):
        if family(name,angle)!='RAIL':continue
        key=f'W{angle//60+1}_RAIL'
        rz=p02.swept_polygon(witness('RAIL',d),0,64)
        sweep=p03.rotation(p02.cheek_solid(rz,-3,6),angle)
        wsteps.append(step(key,sweep,virtual,[0,0,64],[0,0,0],'INTERFACE_WITNESS_NOT_P05_RELEASE'))
        virtual[key]=ws[key]
    wsteps.append(step('P04U',lower_sweep(disk(name,'P04U',d,d3,u,b),480,start),virtual,[0,0,40],[0,0,0],'REAL_PART'))
    virtual['P04U']=all_solids['P04U']
    radial_sweeps=[]
    for angle in range(0,360,60):
        if family(name,angle)!='OPEN':continue
        key=f'W{angle//60+1}_OPEN';a=math.radians(angle);dist=d['web_radial_stroke_mm']
        rz=p02.swept_polygon(witness('OPEN',d),dist,0)
        sweep=p03.rotation(p02.cheek_solid(rz,-3,6),angle);radial_sweeps.append((key,sweep))
        wsteps.append(step(key,sweep,virtual,[dist*math.cos(a),dist*math.sin(a),0],[0,0,0],'INTERFACE_WITNESS_NOT_P05_RELEASE'))
        virtual[key]=ws[key]
    wall=p02.plate_solid(circle(175,d).difference(circle(171,d)),450,50)
    radial_wall=[]
    for k,s in radial_sweeps:
        a=math.radians((int(k[1])-1)*60);dist=d['web_radial_stroke_mm']
        radial_wall.append(step(k,s,{'P07R_ENVELOPE':wall},[dist*math.cos(a),dist*math.sin(a),0],[0,0,0],'WALL_CLOSED_NEGATIVE_CONTROL'))
    open_early=[]
    if name in ('A','C'):
        key='W1_OPEN'
        open_early.append(step('U_AFTER_OPEN',lower_sweep(disk(name,'P04U',d,d3,u,b),480,start),
                               {key:ws[key]},[0,0,40],[0,0,0],'COUNTERFACTUAL_BLOCKED_ORDER'))
    rail_late=[]
    if name in ('B','C'):
        angle=60 if name=='C' else 0
        rz=p02.swept_polygon(witness('RAIL',d),0,64)
        rail_late.append(step('RAIL_AFTER_U',p03.rotation(p02.cheek_solid(rz,-3,6),angle),
                              {'P04U':all_solids['P04U']},[0,0,64],[0,0,0],'COUNTERFACTUAL_BLOCKED_ORDER'))
    # Tool approach is an assumed Ø4 envelope, stops above tongue nose, not a lock design.
    top=p02.plate_solid(circle(171,d),494,6);lock_access=[]
    for item in tongues(d3,u,b):
        xy=item['xy'].centroid;tool=p02.plate_solid(translate(circle(2,d),xoff=xy.x,yoff=xy.y),488.5,31.5)
        lock_access.append({'tongue':item['id'],'assumed_tool_diameter_mm':4,'stop_bottom_z_mm':488.5,
                            'open_top':checks(tool,virtual),'closed_top':checks(tool,{'P07T_ENVELOPE':top})})
    return {'base_strategy':'Y_FIRST (upstream 18 stages /171 sweeps preserved)',
            'real_body_count':21,'envelopes_are_not_bom':True,'disk_stages':steps,
            'reverse_order':reverse,'late_bottom_skin':late_skin,'witness_stages':wsteps,
            'rail_after_upper':rail_late,'upper_after_open':open_early,'radial_web_after_wall':radial_wall,'upper_access':lock_access,
            'physical_lock':'NOT_DESIGNED_CTB008; top-side tool envelope only',
            'maximum_disk_path_intersection_mm3':max(s['maximum_intersection_mm3'] for s in steps),
            'maximum_witness_path_intersection_mm3':max(s['maximum_intersection_mm3'] for s in wsteps)}


def extraction(d,d3,u,b):
    data=[]
    for item in tongues(d3,u,b):
        samples=[]
        for z in (450,456,462,480,486,487,487.5,488):
            section=item['rz'].intersection(LineString([[-100,z],[200,z]]))
            r0,_,r1,_=section.bounds;t=item['t_center_mm']
            xy=rotate(box(r0,t-3,r1,t+3),item['angle_deg'],origin=(0,0))
            samples.append({'z_mm':z,'r_interval_mm':[r0,r1],'xy_loops_mm':paths(xy)})
        data.append({'id':item['id'],'angle_deg':item['angle_deg'],'t_center_mm':item['t_center_mm'],
                     'rz_loops_mm':paths(item['rz']),'full_xy_envelope_loops_mm':paths(item['xy']),
                     'samples':samples,'volume_mm3':item['solid'].volume()})
    return {'source':'P03 A_COMPACT_CLOSED current cheek material, including all B and Y mortises',
            'method':'intersect actual P01 r-z material with Z450..488 then extrude actual6mm tangential thickness',
            'tongues':data,'nominal_kerf_mm':None,'measured_thickness_mm':None}


def center_studies(name,layer,d,d3,u,b):
    slots=tongue_slots(d,d3,u,b);wc=web_cuts(name,layer,d)
    raw=circle(95,d).difference(unary_union(slots+[x['poly'] for x in wc]))
    out=[]
    for diameter,label in zip(d['center_study_diameters_mm'],('NO_HOLE','ACCESS_HOLE_PROVISIONAL','FUNCTIONAL_PORT_PROPOSAL')):
        hole=circle(diameter/2,d) if diameter else Point(0,0)
        material=raw.difference(hole) if diameter else raw
        out.append({'mode':label,'diameter_mm':diameter,'removed_area_mm2':raw.area-material.area,
                    'min_land_to_tongue_mm':min(hole.distance(x) for x in slots),
                    'min_land_to_web_cut_mm':min(hole.distance(x['poly']) for x in wc),
                    'min_land_to_outer_boundary_mm':hole.distance(raw.exterior),
                    'connected_material':material.geom_type=='Polygon',
                    'function':'no demonstrated need' if not diameter else f'assumed20mm inspection/probe +{(diameter-20)/2:g}mm radial access; no real tool measured',
                    'status':'RECOMMENDED_BASELINE' if not diameter else 'UNSELECTED_PROVISIONAL_STUDY; inaccessible externally after closed top skin'})
    return out


def metrics(name,layer,d,d3,u,b):
    face=disk(name,layer,d,d3,u,b);holes=tongue_slots(d,d3,u,b);cuts=web_cuts(name,layer,d)
    lands=[h.distance(face.exterior) for h in holes]
    closed=[c['poly'] for c in cuts if c['family']=='RAIL']
    return {'name':d['variants'][name]['name'],'layer':layer,'units':'mm','release':'DESIGN_ONLY',
            'nominal_diameter_mm':190,'radius_mm':95,'z_mm':d['layers_z_mm'][layer],
            'thickness_mm':6,'area_mm2':face.area,'volume_mm3':face.area*6,'bounds_mm':list(face.bounds),
            'hash':digest(face),'paths_mm':paths(face),'cut_loop_count':len(paths(face)),
            'tongue_hole_count':6,'web_interface_count':6,'tongue_to_outer_lands_mm':lands,
            'min_tongue_to_tongue_mm':min(a.distance(c) for a,c in itertools.combinations(holes,2)),
            'min_tongue_to_web_cut_mm':min(h.distance(c['poly']) for h in holes for c in cuts),
            'closed_web_outer_lands_mm':[c.distance(circle(95,d).exterior) for c in closed],
            'web_cuts':[{'angle_deg':c['angle_deg'],'family':c['family'],'loops_mm':paths(c['poly'])} for c in cuts],
            'tongue_slots_mm':[paths(h) for h in holes],
            'center_diameter_mm':d['variants'][name]['upper_center_diameter_mm'] if layer=='P04U' else 0,
            'nominal_contacts':'zero interference and zero adhesive contact with clearance; no bond/retention claimed',
            'tongue_full_thickness_engagement_mm':6,'tongue_over_upper_disk_mm':2,
            'tongue_t_clearance_each_side_mm':.1,'tongue_radial_clearance_each_side_mm':.2,
            'web_t_clearance_each_side_mm':.2,'web_disk_layer_engagement_mm':6,
            'center_study':center_studies(name,layer,d,d3,u,b)}


def negative_controls(name,d,d3,u,b):
    all_solids=assembly(name,d,d3,u,b);ts=tongues(d3,u,b)
    def collision(face):return sum((p02.plate_solid(face,456,6)^x['solid']).volume() for x in ts)
    rotated=rotate(disk(name,'P04L',d,d3,u,b),10,origin=(0,0))
    missing=disk(name,'P04L',d,d3,u,b,omit_tongue=0)
    cheek=ts[0]['rz'];fat=p02.cheek_solid(cheek,ts[0]['t_center_mm']-3.3,6.6)
    wrong_web=p02.plate_solid(disk(name,'P04L',d,d3,u,b,web_angle_error=5),456,6)
    ws=witness_solids(name,d)
    uncut=p03.rotation(p02.cheek_solid(box(81,456,169,494),-3,6),0)
    return {'rotated_disk_10deg':{'intersection_mm3':collision(rotated),'expected':'BLOCKED'},
            'missing_tongue_slot':{'intersection_mm3':collision(missing),'expected':'BLOCKED'},
            'oversize_tongue_6p6mm':{'intersection_mm3':max(0,(fat^all_solids['P04L']).volume()),'expected':'BLOCKED'},
            'misplaced_web_5deg':{'intersection_mm3':sum(max(0,(wrong_web^w).volume()) for w in ws.values()),'expected':'BLOCKED'},
            'uncut_38mm_web':{'intersection_mm3':sum(max(0,(uncut^all_solids[k]).volume()) for k in ('P04L','P04U')),'expected':'BLOCKED'},
            'incorrect_24mm_free_gap':{'proposed_upper_z_mm':[486,492],'free_gap_mm':24,
                                      'actual_tongue_full_engagement_mm':2,'required_full_engagement_mm':6,
                                      'fixed_layer_contract_matches':False,'expected':'REJECT_DIMENSION_AND_ENGAGEMENT'},
            'radius190_error':{'candidate_diameter_mm':380,'expected_diameter_mm':190,'expected':'REJECT_DIMENSION'}}
