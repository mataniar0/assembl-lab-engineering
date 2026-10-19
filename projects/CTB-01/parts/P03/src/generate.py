"""All P03 CAD, drawings and path evidence from a single flattened solid model."""
import json
import math
import subprocess
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Polygon as Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from model import *


def save_json(p,data):p.write_text(json.dumps(data,indent=2)+'\n')


def export(directory,label,poly,d,status,plane):
    directory.mkdir(exist_ok=True,parents=True)
    cuts=paths(poly);x0,y0,x1,y1=poly.bounds;m=d['sheet_margin_mm'];w=x1-x0+2*m;h=y1-y0+2*m
    doc=ezdxf.new('R2010');doc.units=4;doc.layers.new('CUT_DESIGN_ONLY',dxfattribs={'color':1})
    for points in cuts:doc.modelspace().add_lwpolyline(points,close=True,dxfattribs={'layer':'CUT_DESIGN_ONLY'})
    doc.saveas(directory/f'{label}.dxf')
    polytext=''.join('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+'"/>' for points in cuts)
    (directory/f'{label}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="{x0-m} {-y1-m} {w} {h}">
<title>{label} {status} DESIGN_ONLY, {plane}, 1:1mm</title><metadata>sha256={digest(poly)}</metadata>
<g transform="scale(1,-1)" fill="none" stroke="black" stroke-width="0.1">{polytext}</g></svg>\n''')
    dpi=d['raster_dpi'];fig=plt.figure(figsize=(w/25.4,h/25.4),dpi=dpi);ax=fig.add_axes([0,0,1,1])
    for points in cuts:ax.add_patch(Patch(points,fill=False,color='black',lw=.6))
    ax.set(xlim=(x0-m,x1+m),ylim=(y0-m,y1+m));ax.axis('off')
    fig.savefig(directory/f'{label}.png',dpi=dpi,metadata={'Description':f'DESIGN_ONLY {status}; sha256={digest(poly)};1:1 at{dpi}dpi'})
    plt.close(fig)
    save_json(directory/f'{label}-dimensions.json',{'label':label,'status':status,'release':'DESIGN_ONLY','plane':plane,
        'units':'mm','paths_mm':cuts,'sha256':digest(poly),'area_mm2':poly.area,'bounds_mm':list(poly.bounds),
        'padded_wh_mm':[w,h],'margin_mm':m,'raster_dpi':dpi,'nominal_thickness_mm':6,
        'sheet_hw_mm':[800,440]})


def mesh(solid):
    data=solid.to_mesh()
    return trimesh.Trimesh(vertices=np.asarray(data.vert_properties)[:,:3],faces=np.asarray(data.tri_verts),process=False)


def draw(ax,solid,color,alpha=1):
    p=mesh(solid);ax.add_collection3d(Poly3DCollection(p.vertices[p.faces],facecolor=color,edgecolor='none',alpha=alpha))


def layout(name,d,u,b,directory):
    y=y_profile(name,d);face,holes=cheek(name,d,u);met=metrics(name,d,u,b)
    fig=plt.figure(figsize=(16,10),layout='constrained')
    ax=fig.add_subplot(2,2,1)
    ax.add_patch(Patch(paths(y)[0],facecolor='#c6a7d6',edgecolor='#563071'))
    for a in (0,120,240):
        t=math.radians(a);ax.plot([0,90*math.cos(t)],[0,90*math.sin(t)],ls='--',lw=.6,color='#64748b')
        ax.text(98*math.cos(t),98*math.sin(t),f'{a}°',ha='center',fontsize=9)
    ax.text(0,-108,f'core14.6 / gap15; hubR24; thickness6 atZ410\nmaxXYradius{met["maximum_global_radius_mm"]:.3f}; localtip{met["arm_tip_local_r_mm"]:g}',ha='center',fontsize=9)
    ax.set(xlim=(-110,110),ylim=(-120,115),xlabel='X [mm]',ylabel='Y [mm]',title='P03 top view / 3 identical arms');ax.set_aspect('equal');ax.grid(alpha=.15)
    ax=fig.add_subplot(2,2,3)
    ax.add_patch(Patch(paths(face)[0],facecolor='#e2c8a5',edgecolor='#715132'))
    for points in paths(face)[1:]:ax.add_patch(Patch(points,facecolor='white',edgecolor='#a33'))
    # Actual material section at the positive cheek centre, not a filled Z-band.
    cut=y.intersection(LineString([[35,10.5],[90,10.5]]))
    segments=[cut] if cut.geom_type=='LineString' else list(cut.geoms)
    for section in segments:
        r0,_,r1,_=section.bounds
        ax.add_patch(Patch([[r0,407],[r1,407],[r1,413],[r0,413]],facecolor='#9754af',edgecolor='#7c3aed',alpha=.6))
    ax.text(36,415,'Y material at t10.5 / Z407..413; slot406.8..413.2',fontsize=8)
    ax.annotate('13.6 slot gap',(60,400),(78,398),fontsize=9,arrowprops={'arrowstyle':'->'})
    ax.text(36,383,'S4 B slot386.8..393.2 (unchanged)',fontsize=9)
    ax.set(xlim=(30,100),ylim=(380,425),xlabel='r [mm]',ylabel='z [mm]',title='Actual joint section / candidate holes');ax.set_aspect('equal');ax.grid(alpha=.15)
    ax=fig.add_subplot(1,2,2)
    ax.add_patch(Patch(paths(face)[0],facecolor='#e2c8a5',edgecolor='#715132'))
    for points in paths(face)[1:]:ax.add_patch(Patch(points,facecolor='white',edgecolor='#a33'))
    for h in holes:ax.add_patch(Patch(paths(h)[0],fill=False,edgecolor='#7c3aed',lw=1.5))
    for st in p02.stations(u):ax.text(275,st['z_mm'],f'{st["part"]} Z{st["z_mm"]}',fontsize=8)
    ax.axhspan(225,265,color='#a78bfa',alpha=.15);ax.text(275,245,'ring study\nOPEN',fontsize=8)
    ax.set(xlim=(25,325),ylim=(-10,505),xlabel='r [mm]',ylabel='z [mm]',title='P01 candidate / all B mortises retained');ax.set_aspect('equal');ax.grid(alpha=.15)
    fig.suptitle(f'{name} / DESIGN_ONLY\n'+('CR_REQUIRED: open edge, no retainer' if name.startswith('C_') else 'closed side-tab study'),fontsize=14)
    fig.canvas.draw()
    save_json(directory/'layout-evidence.json',{'axes_bounds':[list(a.get_position().bounds) for a in fig.axes],
              'P03_hash':digest(y),'cheek_hash':digest(face)})
    fig.savefig(directory/'layout.png',dpi=130);fig.savefig(directory/'layout.svg',metadata={'Date':None});plt.close(fig)


def assembly_view(d,u,b):
    name=d['working_concept'];solids=assembly(name,d,u,b);out=PART/'assembly'
    scene=trimesh.Scene()
    for key,s in solids.items():
        p=mesh(s);p.visual.face_colors=[151,84,175,255] if key=='P03' else ([202,163,107,100] if 'P01' in key else [41,145,128,255])
        p.apply_scale(.001);scene.add_geometry(p,node_name=key,geom_name=key)
    (out/'three-leg-base-DESIGN_ONLY.glb').write_bytes(scene.export(file_type='glb'))
    fig=plt.figure(figsize=(16,10),layout='constrained')
    for i,explode in enumerate((False,True)):
        ax=fig.add_subplot(1,2,i+1,projection='3d',proj_type='ortho')
        for key,s in solids.items():
            if explode and key!='P03':
                leg=int(key[1])-1;angle=b['frozen']['leg_angles_deg'][leg];a=math.radians(angle)
                dist=35 if 'P01_1' in key else (65 if 'P01_2' in key else 45)
                s=s.translate([-dist*math.sin(a),dist*math.cos(a),0])
            draw(ax,s,'#9754af' if key=='P03' else ('#d2ac7a' if 'P01' in key else '#299180'),.24 if 'P01' in key else 1)
        ax.set(xlim=(-290,290),ylim=(-290,290),zlim=(0,500),xlabel='X [mm]',ylabel='Y [mm]',zlabel='Z [mm]')
        ax.set_box_aspect((580,580,500));ax.view_init(25,40)
        ax.set_title('19 nominal parts / 3 legs + one Y' if not explode else 'Exploded placement / assembly in fixtures',fontsize=11)
    fig.suptitle('CTB003 / A_COMPACT_CLOSED / DESIGN_ONLY — local base only, no tabletop/discs/ring/locks',fontsize=16)
    fig.savefig(out/'three-leg-and-exploded.png',dpi=125);fig.savefig(out/'three-leg-and-exploded.svg',metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,6,figsize=(21,11),layout='constrained')
    local=local_parts(name,d,u,b)
    for leg,angle in enumerate(b['frozen']['leg_angles_deg']):
        rads=math.radians(angle);distance=d['cheek_insertion_t_mm']
        order=['P01_1','S1','S2','S3','S4','P01_2']
        for index,key in enumerate(order):
            ax=axes[leg,index]
            if key.startswith('P01'):
                face,_=cheek(name,d,u);r0,_,r1,_=face.bounds
                center=-10.5 if key=='P01_1' else 10.5
                projected=box(r0,center-3,r1,center+3)
            else:
                st=next(s for s in p02.stations(u) if s['id']==key)
                projected=translate(p02.spacer('B_THROUGH_ADHESIVE',st['part'],u,b),xoff=st['r_mm'])
            projected=rotate(projected,angle,origin=(0,0))
            offset=-distance if key=='P01_1' else distance
            dx,dy=-offset*math.sin(rads),offset*math.cos(rads)
            start=translate(projected,xoff=dx,yoff=dy)
            ax.add_patch(Patch(paths(y_profile(name,d))[0],facecolor='#bda2d0',edgecolor='none',alpha=.35))
            ax.add_patch(Patch(paths(projected)[0],facecolor='#d2ac7a' if 'P01' in key else '#299180',edgecolor='#334155',lw=.5))
            ax.add_patch(Patch(paths(start)[0],fill=False,edgecolor='#c2410c',linestyle='--',lw=1))
            cx,cy=projected.centroid.x,projected.centroid.y
            ax.annotate('',(cx,cy),(cx+dx,cy+dy),arrowprops={'arrowstyle':'->','color':'#c2410c','lw':1.3})
            extent=unary_union([projected,start]).bounds
            x0,y0,x1,y1=extent
            # Window follows the projected part; axis units retain the actual40mm travel.
            midx,midy=(x0+x1)/2,(y0+y1)/2;span=max(120,x1-x0+25,y1-y0+25)
            ax.set(xlim=(midx-span/2,midx+span/2),ylim=(midy-span/2,midy+span/2))
            ax.set_aspect('equal');ax.grid(alpha=.15);ax.tick_params(labelsize=6)
            stage=leg*6+index+1
            ax.set_title(f'{stage}: L{leg+1} / {key} / {angle}°\n{stage} prior-solid sweep checks',fontsize=9)
            ax.set_xlabel('X [mm]',fontsize=7);ax.set_ylabel('Y [mm]',fontsize=7)
    fig.suptitle('Y-first18 moving stages — actual XY projections; dashed=start / filled=end;40mm local-t travel\nThree-dimensional collision proof includes every prior part; projection overlaps are not collision evidence',fontsize=14)
    fig.savefig(out/'y-first-sequence.png',dpi=120);plt.close(fig)


def generate():
    d,u,b=inputs();summary={}
    for name in CONCEPTS:
        folder=PART/'variants'/name;y=y_profile(name,d);face,new_holes=cheek(name,d,u)
        status='CR_REQUIRED_NOT_SELECTED' if name.startswith('C_') else ('WORKING_CAD_PROPOSAL' if name==d['working_concept'] else 'CAD_ALTERNATIVE')
        export(folder,'P03',y,d,status,'(X,Y), thickness along Z')
        export(folder,'P01-Y-mortise-study-v1',face,d,status,'(r,z), thickness along t')
        results={'status':status,'metrics':metrics(name,d,u,b),'stations':p02.stations(u),
                 'new_Y_holes_rz_mm':[paths(h)[0] for h in new_holes],
                 'final_intersections':final_matrix(assembly(name,d,u,b)),
                 'y_first':y_first(name,d,u,b),
                 'prebuilt':{axis:prebuilt(name,d,u,b,axis) for axis in ('radial','tangential','vertical')},
                 'central_Y':{axis:central_insertion(name,d,u,b,axis) for axis in ('vertical','global_X')}}
        save_json(folder/'mechanical-dimensions.json',results);layout(name,d,u,b,folder);summary[name]=results
        print(name,status,'finalmax',max(v['intersection_mm3'] for v in results['final_intersections']),
              'Yfirst',results['y_first']['status'],'prebuilt',{k:v['status'] for k,v in results['prebuilt'].items()})
    (PART/'assembly').mkdir(exist_ok=True)
    save_json(PART/'assembly/assembly-proofs.json',summary)
    assembly_view(d,u,b)
    refs={}
    import hashlib
    for prefix in ('projects/CTB-01/specifications/CTB-000','projects/CTB-01/parts/P01','projects/CTB-01/parts/P02'):
        files=subprocess.check_output(['git','ls-tree','-r','--name-only',d['source_commit'],prefix],cwd=ROOT,text=True).splitlines()
        for name in files:refs[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    save_json(PART/'src/upstream-sha256.json',refs)
    for file in PART.rglob('*.svg'):file.write_text('\n'.join(s.rstrip() for s in file.read_text().splitlines())+'\n')


if __name__=='__main__':generate()
