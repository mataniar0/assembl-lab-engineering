"""Exports for all CTB002 concepts, candidate cheek copies and nominal local proof."""
import copy
import hashlib
import json
import math
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Polygon as Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.affinity import translate
from shapely.geometry import Polygon, box, LineString

from model import *


def save_json(path,data):
    path.write_text(json.dumps(data,indent=2)+'\n')


def loops(poly):
    return [contour(poly)]+[[[round(x,6),round(y,6)] for x,y in list(r.coords)[:-1]] for r in poly.interiors]


def export_profile(directory,name,poly,d,plane,status):
    directory.mkdir(parents=True,exist_ok=True)
    paths=loops(poly)
    doc=ezdxf.new('R2010');doc.units=4
    doc.layers.new('CUT_DESIGN_ONLY',dxfattribs={'color':1})
    for path in paths:doc.modelspace().add_lwpolyline(path,close=True,dxfattribs={'layer':'CUT_DESIGN_ONLY'})
    doc.saveas(directory/f'{name}.dxf')
    x0,y0,x1,y1=poly.bounds; margin=d['sheet_margin_mm'];w=x1-x0+2*margin;h=y1-y0+2*margin
    polygons=''.join('<polygon points="'+' '.join(f'{x},{y}' for x,y in path)+'"/>' for path in paths)
    (directory/f'{name}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="{x0-margin} {-y1-margin} {w} {h}">
<title>{name} DESIGN_ONLY {status}, {plane}, 1:1 mm</title>
<metadata>contour_sha256={digest(poly)}</metadata><g transform="scale(1,-1)" fill="none" stroke="black" stroke-width="0.1">{polygons}</g></svg>\n''')
    dpi=d['raster_dpi']
    fig=plt.figure(figsize=(w/25.4,h/25.4),dpi=dpi);ax=fig.add_axes([0,0,1,1])
    for path in paths:ax.add_patch(Patch(path,fill=False,color='black',lw=.6))
    ax.set(xlim=(x0-margin,x1+margin),ylim=(y0-margin,y1+margin));ax.axis('off')
    fig.savefig(directory/f'{name}.png',dpi=dpi,metadata={'Description':f'DESIGN_ONLY {status}; contour_sha256={digest(poly)}; 1:1 at {dpi}dpi'})
    plt.close(fig)
    dims={'name':name,'status':status,'release':'DESIGN_ONLY','plane':plane,'units':'mm',
          'paths_mm':paths,'contour_sha256':digest(poly),'area_mm2':poly.area,
          'bounds_mm':list(poly.bounds),'thickness_nominal_mm':d['spacer_thickness_mm'],
          'minimum_nominal_radius_mm':d['root_corner_radius_mm'],
          'sheet_height_mm':800,'sheet_width_mm':440,'margin_mm':margin,
          'padded_envelope_mm':[w,h],'raster_dpi':dpi}
    save_json(directory/f'{name}-dimensions.json',dims)
    return dims


def ring_study(d,b):
    old=copy.deepcopy(d);old['station_z_mm']=d['reference_z_mm']
    # Conservative reservation around the full cheek radial span in225..265.
    levels=np.linspace(*d['ring_band_z_mm'],101)
    cuts=[outer().intersection(LineString([[-1000,z],[1000,z]])) for z in levels]
    rmin=min(c.bounds[0] for c in cuts); rmax=max(c.bounds[2] for c in cuts)
    tmax=b['frozen']['leg_inner_gap_mm']/2+b['frozen']['cheek_thickness_mm']
    env=plate_solid(box(rmin,-tmax,rmax,tmax),d['ring_band_z_mm'][0],d['ring_band_z_mm'][1]-d['ring_band_z_mm'][0])
    bypass=plate_solid(box(rmin,d['bypass_t_mm'][0],rmax,d['bypass_t_mm'][1]),d['ring_band_z_mm'][0],d['ring_band_z_mm'][1]-d['ring_band_z_mm'][0])
    comparisons={}
    for label,data,envelope in [('REFERENCE_245_CONFLICT',old,env),('RELOCATE_200',d,env),('BYPASS_OUTSIDE_KEEP_245',old,bypass)]:
        solid=assembly('B_THROUGH_ADHESIVE',data,b)
        # Envelope overlap is a reservation conflict, not actual ring collision.
        comparisons[label]={name:max(0,(envelope^part).volume()) for name,part in solid.items() if name.startswith('S')}
    return {'status':'CONDITIONAL_CTB006_REVIEW','recommended':'RELOCATE_200',
            'ring_geometry_unknown':True,'reservation_rt_z_bounds_mm':[rmin,rmax,-tmax,tmax,*d['ring_band_z_mm']],
            'spacer_reservation_overlap_mm3':comparisons,
            'relocation_plate_z_clearance_mm':d['ring_band_z_mm'][0]-(d['station_z_mm'][2]+d['spacer_thickness_mm']/2),
            'relocation_slot_z_clearance_mm':d['ring_band_z_mm'][0]-(d['station_z_mm'][2]+d['spacer_thickness_mm']/2+d['slot_allowance_each_side_mm']),
            'bypass_gap_to_outer_cheek_t_mm':d['bypass_t_mm'][0]-tmax,
            'old_sections':[{'z_mm':s['z_mm'],'common_section_r_mm':s['common_section_r_mm']} for s in stations(old)],
            'new_sections':stations(d),
            'limits':'Bypass is only a local outside reservation; actual ring connections/strength and whole ring route not designed. No ring-specific holes.'}


def mesh(solid):
    data=solid.to_mesh()
    return trimesh.Trimesh(vertices=np.array(data.vert_properties)[:,:3],faces=np.array(data.tri_verts),process=False)


def draw_solid(ax,solid,color,alpha=1):
    m=mesh(solid)
    ax.add_collection3d(Poly3DCollection(m.vertices[m.faces],facecolor=color,edgecolor='none',alpha=alpha))


def assembly_views(d,b,solids):
    out=PART/'assembly';out.mkdir(exist_ok=True)
    scene=trimesh.Scene()
    for name,s in solids.items():
        part=mesh(s);part.visual.face_colors=[180,143,92,150] if name.startswith('P01') else [47,146,136,255]
        part.apply_scale(.001) # GLTF metres, source and evidence mm.
        scene.add_geometry(part,node_name=name,geom_name=name)
    (out/'one-leg-DESIGN_ONLY.glb').write_bytes(scene.export(file_type='glb'))
    fig=plt.figure(figsize=(15,10),layout='constrained')
    for i,exploded in enumerate((False,True)):
        ax=fig.add_subplot(1,2,i+1,projection='3d',proj_type='ortho')
        for name,s in solids.items():
            if exploded and name=='P01_2':s=s.translate([0,45,0])
            if exploded and name.startswith('S'):s=s.translate([0,18,0])
            draw_solid(ax,s,'#cda978' if name.startswith('P01') else '#29988c',.24 if name.startswith('P01') else 1)
        ax.set(xlim=(20,280),ylim=(-25,75),zlim=(0,500),xlabel='r [mm]',ylabel='t [mm]',zlabel='z [mm]')
        ax.set_box_aspect((260,160,500));ax.view_init(elev=18,azim=-55)
        ax.set_title('One leg / two identical mortised cheeks' if not exploded else 'Exploded placement / +t approach',fontsize=11)
        for s in stations(d):ax.text(s['r_mm'],35,s['z_mm'],s['id']+' '+s['part']+' z'+str(s['z_mm']),fontsize=8)
    fig.suptitle('CTB-002 / B_THROUGH_ADHESIVE / DESIGN_ONLY — rigid nominal CAD only',fontsize=16)
    fig.savefig(out/'one-leg-and-exploded.png',dpi=130);fig.savefig(out/'one-leg-and-exploded.svg',metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(1,5,figsize=(17,5),layout='constrained')
    for ax,index in zip(axes,range(5)):
        # Top projection at each moving spacer station; final panel second-cheek approach.
        st=stations(d)[min(index,3)];poly=translate(spacer('B_THROUGH_ADHESIVE',st['part'],d,b),xoff=st['r_mm'])
        lo,hi=st['common_section_r_mm']
        ax.add_patch(Patch([[lo,-13.5],[hi,-13.5],[hi,-7.5],[lo,-7.5]],color='#cda978',alpha=.6))
        ax.add_patch(Patch(contour(poly),color='#29988c',alpha=.7))
        if index<4:
            ax.add_patch(Patch(contour(translate(poly,yoff=40)),fill=False,ls='--',edgecolor='#29988c'))
            ax.annotate('',(st['r_mm'],17),(st['r_mm'],40),arrowprops={'arrowstyle':'->'})
            ax.set_title(f'{index+1}: insert '+st['id']+f' at z{st["z_mm"]}')
        else:
            for offset in (0,40):ax.add_patch(Patch([[lo,7.5+offset],[hi,7.5+offset],[hi,13.5+offset],[lo,13.5+offset]],fill=offset==0,edgecolor='#b48449',facecolor='#cda978'))
            ax.annotate('',(st['r_mm'],18),(st['r_mm'],40),arrowprops={'arrowstyle':'->'})
            ax.set_title('5: close second cheek')
        ax.set(xlim=(st['r_mm']-25,st['r_mm']+25),ylim=(-20,60),xlabel='r [mm]',ylabel='t [mm]');ax.set_aspect('equal');ax.grid(alpha=.2)
    fig.suptitle('Assembly order / translate in −t / fixture first cheek and support each spacer / not a physical test')
    fig.savefig(out/'insertion-order.png',dpi=120);plt.close(fig)


def concept_view(concept,d,b,directory,status):
    fig=plt.figure(figsize=(13,9),layout='constrained')
    for i,part in enumerate(d['parts']):
        ax=fig.add_subplot(2,2,2*i+1);p=spacer(concept,part,d,b)
        ax.add_patch(Patch(contour(p),facecolor='#9ed1c7',edgecolor='#183b35'))
        x0,y0,x1,y1=p.bounds
        ax.set(xlim=(x0-5,x1+5),ylim=(y0-7,y1+7),xlabel='local radial offset [mm]',ylabel='t [mm]',title=f'{part}: {x1-x0:g} × {y1-y0:g} × 6 mm')
        ax.set_aspect('equal');ax.grid(alpha=.2)
        ax.text(0,y1+2,'TAB / SHOULDER STUDY',ha='center',fontsize=8)
    ax=fig.add_subplot(1,2,2)
    material,holes=cheek(concept,d)
    ax.add_patch(Patch(contour(outer()),facecolor='#e3c9a5',edgecolor='#715132'))
    for h in holes:ax.add_patch(Patch(contour(h),facecolor='#ffffff',edgecolor='#a73822'))
    for s in stations(d):ax.annotate(f'{s["id"]}: z{s["z_mm"]}, r{s["r_mm"]:.2f}',(s['r_mm'],s['z_mm']),(270,s['z_mm']),fontsize=8,arrowprops={'arrowstyle':'->','lw':.4})
    ax.axhspan(*d['ring_band_z_mm'],color='#a78bfa',alpha=.22)
    ax.text(280,245,'Ring band\nNO CUT',fontsize=8,ha='center')
    ax.set(xlim=(20,330),ylim=(-10,500),xlabel='r [mm]',ylabel='z [mm]',title='Versioned P01 mortise study; exterior unchanged')
    ax.set_aspect('equal');ax.grid(alpha=.15)
    fig.suptitle(f'{concept} / DESIGN_ONLY / {status}',fontsize=15)
    fig.canvas.draw()
    save_json(directory/'layout-evidence.json',{'axes_bounds_fraction':[list(ax.get_position().bounds) for ax in fig.axes], 'spacer_hashes':{name:digest(spacer(concept,name,d,b)) for name in d['parts']}})
    fig.savefig(directory/'concept-layout.png',dpi=130);fig.savefig(directory/'concept-layout.svg',metadata={'Date':None});plt.close(fig)


def sensitivity(d,b):
    rows=[]
    for stock in [5.6,6.0,6.4,6.8]:
        collisions=collision_matrix(assembly(d['working_concept'],d,b,stock=stock))
        rows.append({'hypothetical_stock_mm':stock,'actual_gap_at_fixed_centres_mm':21-stock,
                     'shoulder_gap_each_side_mm':max(0,(6-stock)/2),
                     'maximum_material_intersection_mm3':max(x['intersection_mm3'] for x in collisions),
                     'measured':False,'physical_fit_status':'UNVERIFIED'})
    save_json(PART/'assembly/thickness-sensitivity.json',rows)


def study_views(d,b):
    study=ring_study(d,b)
    old=copy.deepcopy(d);old['station_z_mm']=d['reference_z_mm']
    a=stations(old)[2];n=stations(d)[2]
    fig=plt.figure(figsize=(16,7))
    ax=fig.add_subplot(131)
    ax.set_position([.05,.20,.27,.65])
    ax.add_patch(Patch(contour(outer()),facecolor='#e3c9a5',edgecolor='#715132'))
    ax.axhspan(*d['ring_band_z_mm'],color='#a78bfa',alpha=.3)
    for color,st,data in [('#d33',a,old),('#168577',n,d)]:
        for hole in slot_shapes(d['working_concept'],st,data):ax.add_patch(Patch(contour(hole),fill=False,edgecolor=color,lw=2))
        ax.text(st['r_mm']+14,st['z_mm'],f'z{st["z_mm"]} r{st["r_mm"]:.2f}',fontsize=8)
    ax.set(xlim=(60,190),ylim=(185,280),xlabel='r [mm]',ylabel='z [mm]',title='Full-slab section / holes study')
    ax.set_aspect('equal');ax.grid(alpha=.2)
    ax=fig.add_subplot(132)
    ax.set_position([.37,.25,.27,.55])
    poly=translate(spacer(d['working_concept'],'P02',d,b),xoff=a['r_mm'])
    ax.add_patch(Patch(contour(poly),facecolor='#d33',alpha=.65))
    r0,r1=study['reservation_rt_z_bounds_mm'][:2]
    ax.add_patch(Patch([[r0,-13.5],[r1,-13.5],[r1,13.5],[r0,13.5]],fill=False,edgecolor='#7c3aed',lw=2))
    ax.axhspan(*d['bypass_t_mm'],color='#3b82f6',alpha=.3)
    ax.set(xlim=(r0-10,r1+10),ylim=(-20,30),xlabel='r [mm]',ylabel='t [mm]',title='z245: clash / outside bypass study')
    ax.set_aspect('equal');ax.grid(alpha=.2)
    ax=fig.add_subplot(133,projection='3d',proj_type='ortho')
    env=plate_solid(box(r0,-13.5,r1,13.5),225,40)
    draw_solid(ax,env,'#a78bfa',.12)
    for color,st in [('#d33',a),('#168577',n)]:
        p=translate(spacer(d['working_concept'],'P02',d,b),xoff=st['r_mm'])
        draw_solid(ax,plate_solid(p,st['z_mm']-3,6),color,.85)
    ax.set(xlim=(60,190),ylim=(-20,30),zlim=(190,275),xlabel='r [mm]',ylabel='t [mm]',zlabel='z [mm]',title='3D section: reservation, NOT ring CAD')
    ax.set_box_aspect((130,70,85));ax.view_init(22,-55)
    ax.tick_params(axis='z',labelsize=7,pad=0);ax.set_zlabel('z [mm]',labelpad=-1)
    ax.set_position([.69,.15,.24,.70])
    fig.suptitle('B05 ring interaction / DESIGN_ONLY / relocate245→200 proposed; CTB006 approval pending')
    fig.savefig(PART/'assembly/ring-study.png',dpi=130)
    fig.savefig(PART/'assembly/ring-study.svg',metadata={'Date':None});plt.close(fig)


def generate():
    d,b=inputs(); all_results={}
    for c in CONCEPTS:
        directory=PART/'variants'/c;directory.mkdir(parents=True,exist_ok=True)
        land=land_report(c,d);material,holes=cheek(c,d)
        proof=insertion(c,d,b)
        eligible=min(x['minimum_hole_to_external_contour_mm'] for x in land)>=d['minimum_cheek_land_hypothesis_mm']
        status='CAD_WORKING_PROPOSAL' if c==d['working_concept'] else ('CAD_ALTERNATIVE' if eligible and proof['status'].startswith('PASS') else 'BLOCKED_NOT_SELECTED')
        for part in d['parts']:export_profile(directory,part,spacer(c,part,d,b),d,'(r,t), thickness along z',status)
        export_profile(directory,'P01-SOFT_CURVE-mortise-study-v1',material,d,'(r,z), thickness along t',status)
        solids=assembly(c,d,b)
        result={'status':status,'stations':stations(d),'holes_rz_mm':[contour(h) for h in holes],
                'cheek_area_mm2':material.area,'minimum_land_screen_mm':d['minimum_cheek_land_hypothesis_mm'],
                'lands':land,'land_screen_pass':eligible,'collision_matrix':collision_matrix(solids),
                'insertion':proof,'nominal_stock_mm':6,'measured_stock_mm':d['actual_stock_thickness_mm'],
                'measured_kerf_mm':d['measured_kerf_mm'],
                'slot_allowance_each_side_mm':d['slot_allowance_each_side_mm'],
                'mechanical_retention':'A: one-sided head capture, reverse-slide keeper unresolved; B/C: shoulders resist inward cheek approach only, no positive outward retention; adhesive unvalidated'}
        save_json(directory/'mechanical-dimensions.json',result)
        concept_view(c,d,b,directory,status);all_results[c]=result
        print(c,status,'min land',min(x['minimum_hole_to_external_contour_mm'] for x in land),'sweep',proof['status'])
    save_json(PART/'assembly/collision-and-insertion.json',all_results[d['working_concept']])
    save_json(PART/'assembly/ring-interference-study.json',ring_study(d,b))
    study_views(d,b)
    sensitivity(d,b)
    assembly_views(d,b,assembly(d['working_concept'],d,b))
    # Record baseline and P01 source bytes to independently detect unintended changes.
    paths=list((PROJECT/'specifications/CTB-000').iterdir())+[p for p in P01.rglob('*') if p.is_file() and '__pycache__' not in str(p) and not p.suffix=='.pyc']
    save_json(PART/'assembly/upstream-sha256.json',{str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()})
    for svg in [*PART.glob('variants/*/*.svg'),*PART.glob('assembly/*.svg')]:
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')


if __name__=='__main__':generate()
