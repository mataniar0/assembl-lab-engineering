"""Six actual P05 ribs per concept, exact material sweeps and explicit CR-only P04 variants."""
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import numpy as np
from jsonschema import Draft202012Validator
from shapely.geometry import Polygon,Point,LineString,box
from shapely.geometry.polygon import orient
from shapely.affinity import rotate,translate
from shapely.ops import unary_union

PART=Path(__file__).resolve().parents[1];PROJECT=PART.parents[1];ROOT=PROJECT.parents[1]
spec=importlib.util.spec_from_file_location('p04_reference',PROJECT/'parts/P04/src/model.py')
p04=importlib.util.module_from_spec(spec);spec.loader.exec_module(p04)
p03=p04.p03;p02=p04.p02;paths=p04.paths;digest=p04.digest
CONCEPTS=('A','B','C')


def inputs():
    d=json.loads((PART/'src/design.json').read_text())
    Draft202012Validator(json.loads((PART/'src/design.schema.json').read_text())).validate(d)
    return (d,*p04.inputs())


def fillet(poly,r,d):
    coords=np.asarray(list(orient(poly,1).exterior.coords)[:-1]);out=p02.master.Outline(d['polygon_fillet_chord_tolerance_mm'])
    p02.master.rounded_polygon(out,coords,[r]*len(coords))
    p=Polygon(out.final())
    if not p.is_valid or p.geom_type!='Polygon':raise ValueError('fillet created invalid/disconnected cut material')
    return orient(p,1)


def rib(name,d):
    z0,z1=d['core_z_mm'];end=d['outer_r_mm'];cfg=d[name]
    if name=='A':
        outer=p02.rounded_rect(cfg['inner_r_mm'],z0,end,z1,cfg['outer_radius_mm'])
        return outer.difference(p02.rounded_rect(*cfg['relief_rz_mm'],cfg['relief_radius_mm']))
    a,b=cfg['rail_r_mm'];body=box(d['outer_body_start_r_mm'],z0,end,z1)
    if name=='B':
        raw=unary_union([body,box(a,z0,b,z1),box(a,cfg['bridge_z_mm'][0],cfg['bridge_end_r_mm'],cfg['bridge_z_mm'][1])])
    else:
        raw=unary_union([body,box(a,z0,b,cfg['rail_top_z_mm']),box(a,cfg['head_bottom_z_mm'],end,cfg['head_step_z_mm']),
                         box(cfg['upper_head_inner_r_mm'],cfg['head_step_z_mm'],end,z1)])
    return fillet(raw,cfg['corner_radius_mm'],d)


def disk(name,layer,d,d4,d3,u,b,proposed=False,angle_error=0):
    if not proposed or layer not in d.get(name,{}).get('proposed_slots_r_mm',{}):
        return p04.disk('A',layer,d4,d3,u,b)
    a,c=d[name]['proposed_slots_r_mm'][layer];half=d['proposed_slot_width_mm']/2
    cut=p02.rounded_rect(a,-half,c,half,d['proposed_slot_corner_radius_mm'])
    holes=p04.tongue_slots(d4,d3,u,b)+[rotate(cut,angle+angle_error,origin=(0,0)) for angle in d['angles_deg']]
    return p04.circle(95,d4).difference(unary_union(holes))


def existing(d4,d3,u,b):return p04.assembly('A',d4,d3,u,b)


def rib_solids(name,d):
    solid=p02.cheek_solid(rib(name,d),-d['rib_thickness_mm']/2,d['rib_thickness_mm'])
    return {f'P05_{i+1}':p03.rotation(solid,angle) for i,angle in enumerate(d['angles_deg'])}


def assembly(name,d,d4,d3,u,b,proposed=False):
    out=existing(d4,d3,u,b)
    if proposed:
        for layer,z in d4['layers_z_mm'].items():out[layer]=p02.plate_solid(disk(name,layer,d,d4,d3,u,b,True),z[0],6)
    return {**out,**rib_solids(name,d)}


def sweep_rib(name,d,dr=0,dz=0,angle=0):
    face=p02.swept_polygon(rib(name,d),dr,dz)
    return p03.rotation(p02.cheek_solid(face,-3,d['rib_thickness_mm']),angle)


def install(name,d,d4,d3,u,b,proposed=False):
    allparts=assembly(name,d,d4,d3,u,b,proposed);prior=p04.base(d3,u,b);steps=[]
    start=d['disk_start_bottom_z_mm'];skinface=p04.skin(d4,d3,u,b);skin=p02.plate_solid(skinface,450,6)
    steps.append(p04.step('P07B_ENVELOPE',p04.lower_sweep(skinface,450,start),prior,[0,0,70],[0,0,0],'RESERVATION_NOT_BOM'))
    prior['P07B_ENVELOPE']=skin
    stages=['P04L']+([f'P05_{i+1}' for i in range(6)]+['P04U'] if proposed and name in ('B','C') else ['P04U']+[f'P05_{i+1}' for i in range(6)])
    for key in stages:
        if key.startswith('P04'):
            z=d4['layers_z_mm'][key][0]
            swept=p04.lower_sweep(disk(name,key,d,d4,d3,u,b,proposed),z,start);offset=[0,0,start-z]
        else:
            angle=d['angles_deg'][int(key.split('_')[1])-1];a=math.radians(angle)
            vertical=proposed and name in ('B','C')
            swept=sweep_rib(name,d,dz=d['vertical_stroke_mm'] if vertical else 0,dr=0 if vertical else d['radial_stroke_mm'],angle=angle)
            offset=[0,0,d['vertical_stroke_mm']] if vertical else [100*math.cos(a),100*math.sin(a),0]
        steps.append(p04.step(key,swept,prior,offset,[0,0,0],'REAL_P05' if key.startswith('P05') else ('PROPOSED_P04_CR_REQUIRED' if proposed and key in d.get(name,{}).get('proposed_slots_r_mm',{}) else 'REVIEWED_P04')))
        prior[key]=allparts[key]
    worst=max(s['maximum_intersection_mm3'] for s in steps)
    return {'status':'PASS_CAD_SPECIFIED_PATH' if worst<1e-6 else 'BLOCKED',
            'disk_authority':'P04_V2_PROPOSAL_NOT_APPROVED' if proposed else 'SELECTED_P04_A_UNCHANGED',
            'body_count':27,'method':'EXACT_TRANSLATIONAL_MINKOWSKI_SWEEP','steps':steps,
            'continuous_checks':sum(len(s['continuous_intersections']) for s in steps),'maximum_intersection_mm3':worst}


def checks_for_rib(name,d,d4,d3,u,b,proposed,dr=0,dz=0):
    solids=assembly(name,d,d4,d3,u,b,proposed)
    return p04.checks(sweep_rib(name,d,dr,dz),{k:s for k,s in solids.items() if k!='P05_1'})


def retention(name,d,d4,d3,u,b,proposed):
    if name=='B' and not proposed:
        return {'valid_start':False,'claim':'NOT_EVALUATED: original P04A already overlaps B; no restraint evidence from an invalid starting assembly'}
    result={'valid_start':True}
    for label,dr,dz in [('radial_out',20,0),('radial_in',-5,0),('lift',0,6.4),('lower',0,-6.4)]:
        checks=checks_for_rib(name,d,d4,d3,u,b,proposed,dr,dz)
        worst=max(c['volume_mm3'] for c in checks)
        result[label]={'stroke_rz_mm':[dr,dz],'maximum_intersection_mm3':worst,
                       'checks':checks,'status':'BLOCKED_TRANSLATION' if worst>1e-6 else 'FREE_TRANSLATION'}
    result['claim']='specified translations only; no 6DOF retention, adhesive or strength proof; disks still require CTB008 Z retention'
    return result


def access_and_controls(name,d,d4,d3,u,b,proposed):
    solids=assembly(name,d,d4,d3,u,b,proposed)
    dl,du=solids['P04L'],solids['P04U'];face=rib(name,d)
    circle=lambda r:p04.circle(r,d4)
    wall=p02.plate_solid(circle(175).difference(circle(171)),450,50)
    top=p02.plate_solid(circle(171),494,6)
    uncut=p02.cheek_solid(box(81,456,169,494),-3,6)
    fat=p02.cheek_solid(face,-3.4,6.8)
    shifted=p03.rotation(p02.cheek_solid(face,-3,6),5)
    upper_sweep=p04.lower_sweep(disk(name,'P04U',d,d4,d3,u,b,proposed),480,520)
    reverse=p04.lower_sweep(disk(name,'P04L',d,d4,d3,u,b,proposed),456,520)
    late=p04.lower_sweep(p04.skin(d4,d3,u,b),450,520)
    radial=sweep_rib(name,d,dr=100)
    tools=[]
    for t in p04.tongues(d3,u,b):
        xy=t['xy'].centroid;tool=p02.plate_solid(translate(circle(2),xoff=xy.x,yoff=xy.y),488.5,31.5)
        tools.append({'tongue':t['id'],'assumed_diameter_mm':4,'stop_z_mm':488.5,
                      'open_top':p04.checks(tool,solids),'closed_top':p04.checks(tool,{'P07T_ENVELOPE':top})})
    return {'uncut_38mm_web_mm3':sum(max(0,(uncut^s).volume()) for s in (dl,du)),
            'oversize_6p8mm_mm3':sum(max(0,(fat^s).volume()) for s in (dl,du)),
            'rotated_rib_5deg_mm3':sum(max(0,(shifted^s).volume()) for s in (dl,du)),
            'radial_insertion_after_wall_mm3':max(0,(radial^wall).volume()),
            'upper_after_rib_mm3':max(0,(upper_sweep^solids['P05_1']).volume()),
            'lower_after_upper_mm3':max(0,(reverse^du).volume()),
            'bottom_skin_after_disks_mm3':sum(max(0,(late^s).volume()) for s in (dl,du)),
            'lift_after_top_closure_mm3':max(0,(sweep_rib(name,d,dz=6.4)^top).volume()),
            'tool_reservations':tools,'tools_are_not_locks_or_real_fixture_clearance':True}


def section_intervals(poly,z):
    section=poly.intersection(LineString([[0,z],[200,z]]))
    segments=[section] if section.geom_type=='LineString' else list(section.geoms) if hasattr(section,'geoms') else []
    return [[s.bounds[0],s.bounds[2]] for s in segments if s.geom_type=='LineString' and s.length>1e-7]


def metrics(name,d,d4,d3,u,b):
    p=rib(name,d);top=section_intervals(p,494);bottom=section_intervals(p,456)
    skins={label:{'r_intervals_mm':v,'nominal_boundary_area_mm2':sum(c-a for a,c in v)*6,
                   'status':'GEOMETRIC_BOUNDARY_CONTACT_ONLY_NO_BOND_PROOF'} for label,v in (('P07B',bottom),('P07T',top))}
    bands={}
    for layer,z in d4['layers_z_mm'].items():
        chord=math.sqrt(95**2-3.2**2)
        region=p.intersection(box(0,z[0],chord,z[1]))
        bands[layer]={'broadside_geometric_reservation_area_both_faces_mm2':2*region.area,
                      'side_gap_mm':.2,'z_mm':z,'actual_bonded_area_mm2':0,
                      'section_intervals_at_midplane_mm':section_intervals(p,sum(z)/2),
                      'status':'PROPOSED_ADHESIVE_ZONE_UNSPECIFIED_NOT_TESTED'}
    necks=({'upper_cap_envelope_budget_mm':494-d['A']['relief_rz_mm'][3],
             'upper_inner_edge_span_mm':494-d['A']['outer_radius_mm']-d['A']['relief_rz_mm'][3],
             'lower_inner_edge_span_mm':d['A']['relief_rz_mm'][1]-(456+d['A']['outer_radius_mm']),
             'lower_head_height_mm':d['A']['relief_rz_mm'][1]-456,
             'radial_backbone_at_relief_mm':169-d['A']['relief_rz_mm'][2]} if name=='A' else
           {'rail_width_mm':d[name]['rail_r_mm'][1]-d[name]['rail_r_mm'][0],
            'bridge_height_mm':10 if name=='B' else d['C']['head_step_z_mm']-d['C']['head_bottom_z_mm']})
    return {'name':name,'release':'DESIGN_ONLY','units':'mm','plane':'r,z, thickness along t','paths_mm':paths(p),
            'sha256':digest(p),'area_mm2':p.area,'volume_mm3':p.area*6,'bounds_mm':list(p.bounds),
            'instances':6,'angles_deg':d['angles_deg'],'nominal_thickness_mm':6,'nominal_height_mm':38,
            'source_commit':d['source_commit'],'source_authorities':d['selected_sources'],
            'grain':d['grain_hypothesis'],'kerf_mm':None,'measured_thickness_mm':None,
            'corner_radius_mm':d['A']['outer_radius_mm'] if name=='A' else d[name]['corner_radius_mm'],
            'curve_approximation':{'method':'quad8 rounded rectangles' if name=='A' else 'explicit fillet arcs',
                                   'maximum_sagitta_or_chord_tolerance_mm':1-math.cos(math.pi/32) if name=='A' else d['polygon_fillet_chord_tolerance_mm']},
            'C_upper_step_flat_area_mm2':2.4 if name=='C' else None,
            'neck_screening_dimensions':necks,'screening_threshold_mm':6,
            'disk_bond_reservations':bands,'skin_reservations':skins,
            'outer_nominal_r_gap_mm':2,'outer_min_radial_gap_to_cylindrical_rim_mm':171-math.hypot(169,3),
            'status_fit_to_original':'BLOCKED_UPPER_DISK' if name=='B' else 'PASS_CAD_NO_RADIAL_RETAINER',
            'proposed_p04_layers':list(d.get(name,{}).get('proposed_slots_r_mm',{})),
            'load_rating':None,'physical_tests':'NOT_RUN'}
