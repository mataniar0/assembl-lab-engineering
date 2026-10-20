"""Reproduce all DESIGN_ONLY exports from actual material; fail before tests on error."""
import json
import subprocess
import xml.sax.saxutils as xml

import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Polygon as Patch, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from model import *


def save_json(path,data):path.write_text(json.dumps(data,indent=2)+'\n')


def export(folder,label,poly,d,plane,annotation,roles=None):
    folder.mkdir(parents=True,exist_ok=True)
    loops=paths(poly);x0,y0,x1,y1=poly.bounds;m=20
    w,h=x1-x0+2*m,y1-y0+2*m
    doc=ezdxf.new('R2010');doc.units=4;msp=doc.modelspace()
    role_names=roles or ['CUT_OUTER']+['CUT_HOLE']*(len(loops)-1)
    for role in set(role_names)|{'NOT_CUT_DIMENSIONS'}:doc.layers.new(role,dxfattribs={'color':1 if role.startswith('CUT') else 5})
    for pts,role in zip(loops,role_names):msp.add_lwpolyline(pts,close=True,dxfattribs={'layer':role})
    short=f'{label} DESIGN_ONLY {plane}; {annotation}'
    # Explicit dimension witness lines and text in a non-cut layer, never duplicate cut contours.
    for p,q in (((x0,y0-6),(x1,y0-6)),((x0,y0-4),(x0,y0-8)),((x1,y0-4),(x1,y0-8))):
        msp.add_line(p,q,dxfattribs={'layer':'NOT_CUT_DIMENSIONS'})
    msp.add_text(f'{x1-x0:.3f} mm envelope',dxfattribs={'height':2.5,'insert':((x0+x1)/2-20,y0-11),'layer':'NOT_CUT_DIMENSIONS'})
    msp.add_text(short,dxfattribs={'height':1.6,'insert':(x0,y1+8),'layer':'NOT_CUT_DIMENSIONS'})
    if label.startswith('P04'):
        msp.add_text('190.000 mm nominal diameter; edge notches reduce X envelope',dxfattribs={'height':2,'insert':(x0,y1+13),'layer':'NOT_CUT_DIMENSIONS'})
    doc.saveas(folder/f'{label}.dxf')
    groups=''.join(f'<g id="{role}-{i}" data-layer="{role}"><polygon points="'+
                   ' '.join(f'{x},{y}' for x,y in pts)+'"/></g>' for i,(pts,role) in enumerate(zip(loops,role_names)))
    (folder/f'{label}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="{x0-m} {-y1-m} {w} {h}">
<title>{xml.escape(short)}</title><metadata>DESIGN_ONLY; sha256={digest(poly)}; plane={plane}; no kerf compensation</metadata>
<g id="CUT" transform="scale(1,-1)" fill="none" stroke="black" stroke-width="0.2">{groups}</g>
<g id="NOT_CUT_DIMENSIONS" fill="#334155" font-size="2.3">
<text x="{x0}" y="{-y1-10}">{xml.escape(label)} DESIGN_ONLY / {plane}</text>
<text x="{x0}" y="{-y1-6}" font-size="1.7">{xml.escape(annotation)}</text>
<path d="M{x0},{-y0+6} H{x1} M{x0},{-y0+4} v4 M{x1},{-y0+4} v4" fill="none" stroke="#334155" stroke-width="0.15"/>
<text x="{(x0+x1)/2-16}" y="{-y0+11}">{x1-x0:.3f} mm envelope</text></g></svg>\n''')
    dpi=d['raster_dpi'];fig=plt.figure(figsize=(w/25.4,h/25.4),dpi=dpi);ax=fig.add_axes([0,0,1,1])
    for pts in loops:ax.add_patch(Patch(pts,fill=False,color='black',lw=.8))
    ax.text(x0,y1+10,f'{label} DESIGN_ONLY / {plane}',fontsize=6)
    ax.text(x0,y1+6,annotation,fontsize=4.4)
    ax.plot([x0,x1],[y0-6]*2,color='#334155',lw=.5)
    for x in (x0,x1):ax.plot([x,x],[y0-4,y0-8],color='#334155',lw=.5)
    ax.text((x0+x1)/2,y0-12,f'{x1-x0:.3f} mm envelope',ha='center',fontsize=6)
    ax.set(xlim=(x0-m,x1+m),ylim=(y0-m,y1+m));ax.axis('off')
    fig.savefig(folder/f'{label}.png',dpi=dpi,metadata={'Description':f'{short}; sha256={digest(poly)};1:1 at{dpi}dpi'})
    plt.close(fig)
    return {'label':label,'plane':plane,'release':'DESIGN_ONLY','paths_mm':loops,'roles':role_names,
            'sha256':digest(poly),'bounds_mm':list(poly.bounds),'area_mm2':poly.area,
            'physical_artboard_wh_mm':[w,h],'raster_dpi':dpi,'nominal_thickness_mm':6,
            'sheet_hw_mm':[800,440],'provisional_sheet_margin_mm':10,'annotation':annotation}


def cut_roles(face,slots,cuts):
    out=['CUT_OUTER']
    for ring in face.interiors:
        hole=Polygon(ring);c=hole.representative_point()
        if any(h.covers(c) for h in slots):out.append('CUT_TONGUE')
        elif any(x['poly'].covers(c) for x in cuts):out.append('CUT_WEB')
        else:out.append('CUT_ACCESS')
    return out


def mesh(solid):
    obj=solid.to_mesh()
    return trimesh.Trimesh(vertices=np.asarray(obj.vert_properties)[:,:3],faces=np.asarray(obj.tri_verts),process=False)


def draw_material(ax,poly,color,alpha=1):
    for i,pts in enumerate(paths(poly)):ax.add_patch(Patch(pts,facecolor=color if i==0 else 'white',edgecolor='#334155',lw=.6,alpha=alpha))


def segments(shape):
    if shape.is_empty:return []
    if shape.geom_type=='LineString':return [shape]
    return [s for s in shape.geoms if s.geom_type=='LineString']


def horizontal_witness(kind,z,d):
    return [box(s.bounds[0],-3,s.bounds[2],3) for s in segments(witness(kind,d).intersection(LineString([[0,z],[200,z]])))]


def layout(name,d,d3,u,b,folder):
    fig,axes=plt.subplots(2,2,figsize=(15,10),layout='constrained');colors={'P04L':'#4c9bc6','P04U':'#a786c4'}
    ts=tongues(d3,u,b)
    for layer,ax in zip(('P04L','P04U'),axes[0]):
        z=sum(d['layers_z_mm'][layer])/2
        draw_material(ax,disk(name,layer,d,d3,u,b),colors[layer])
        for t in ts:
            section=t['rz'].intersection(LineString([[-100,z],[200,z]]));r0,_,r1,_=section.bounds
            poly=rotate(box(r0,t['t_center_mm']-3,r1,t['t_center_mm']+3),t['angle_deg'],origin=(0,0));draw_material(ax,poly,'#c9a36f')
        for angle in range(0,360,60):
            for p in horizontal_witness(family(name,angle),z,d):draw_material(ax,rotate(p,angle,origin=(0,0)),'#5baf95',.7)
            a=math.radians(angle);ax.text(106*math.cos(a),106*math.sin(a),f'{angle}°',ha='center',fontsize=8)
        ax.set(xlim=(-175,175),ylim=(-175,175),xlabel='X mm',ylabel='Y mm',title=f'{layer} physical horizontal section Z{z:g} / radius95');ax.set_aspect('equal');ax.grid(alpha=.15)
    for ax,t in zip(axes[1],(0,10.5)):
        for layer,z in d['layers_z_mm'].items():
            for s in segments(disk(name,layer,d,d3,u,b).intersection(LineString([[0,t],[175,t]]))):
                a,_,c,_=s.bounds;ax.add_patch(Rectangle((a,z[0]),c-a,6,facecolor=colors[layer],edgecolor='#334155'))
        if t==0:draw_material(ax,witness(family(name,0),d),'#5baf95',.55)
        else:draw_material(ax,ts[0]['rz'],'#c9a36f')
        for z,label,face in ((450,'P07B envelope',skin(d,d3,u,b)),(494,'P07T envelope',circle(171,d))):
            # Actual prospective material sections: bottom skin has six real tongue holes.
            for s in segments(face.intersection(LineString([[0,t],[175,t]]))):
                a,_,c,_=s.bounds
                ax.add_patch(Rectangle((a,z),c-a,6,facecolor='none',edgecolor='#64748b',hatch='///',lw=.5))
            ax.text(115,z+2,label,fontsize=7)
        ax.axhline(488,color='#b45309',ls='--',lw=.6);ax.text(5,489,'tongue tip488',fontsize=7)
        ax.set(xlim=(0,175),ylim=(448,502),xlabel='r mm',ylabel='Z mm',title=f'Positive-r section / local t={t:g}; hatched skins are reservations');ax.set_aspect('equal');ax.grid(alpha=.15)
    fig.suptitle(f'{d["variants"][name]["name"]} / DESIGN_ONLY — six tongues + six separate web interfaces\n6+38+6=50mm; L456..462; free18; U480..486; gap8 to top-skin underside494',fontsize=13)
    fig.savefig(folder/'plans-and-sections.png',dpi=120);fig.savefig(folder/'plans-and-sections.svg',metadata={'Date':None});plt.close(fig)


def assembly_render(name,d,d3,u,b,folder,solids):
    scene=trimesh.Scene()
    for key,solid in solids.items():
        p=mesh(solid);p.visual.face_colors=([60,147,190,255] if key=='P04L' else [159,118,187,255] if key=='P04U' else [205,170,117,255])
        p.apply_scale(.001);scene.add_geometry(p,node_name=key,geom_name=key)
    (folder/'actual-21-body-DESIGN_ONLY.glb').write_bytes(scene.export(file_type='glb'))
    save_json(folder/'mesh-evidence.json',{'units':'GLTF metres; source mm','body_count':len(solids),
              'bodies':{k:{'volume_mm3':s.volume(),'bounds_mm':mesh(s).bounds.tolist()} for k,s in solids.items()}})
    fig=plt.figure(figsize=(16,10),layout='constrained')
    for col,exploded in enumerate((False,True),1):
        ax=fig.add_subplot(1,2,col,projection='3d',proj_type='ortho')
        for key,s in solids.items():
            if exploded and key.startswith('P04'):s=s.translate([0,0,35 if key=='P04L' else 65])
            p=mesh(s);color='#4c9bc6' if key=='P04L' else '#a786c4' if key=='P04U' else '#a878ba' if key=='P03' else '#c9a36f'
            ax.add_collection3d(Poly3DCollection(p.vertices[p.faces],facecolor=color,edgecolor='none',alpha=.23 if 'P01' in key else 1))
        ax.set(xlim=(-280,280),ylim=(-280,280),zlim=(0,570),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
        ax.set_box_aspect((560,560,570));ax.view_init(23,40)
        ax.set_title('21 REAL bodies / nominal position' if not exploded else 'Exploded disks +35/+65mm / base remains Y_FIRST')
    fig.suptitle(f'{d["variants"][name]["name"]} / DESIGN_ONLY — no skins, webs, wall or locks in real21-body model',fontsize=14)
    fig.savefig(folder/'actual-and-exploded.png',dpi=120);plt.close(fig)


def core_view(name,d,d3,u,b,folder):
    """Finite real tongue sections and distinct non-BOM reservations; never a finished tabletop."""
    fig=plt.figure(figsize=(17,8),layout='constrained')
    colors={'P04L':'#4c9bc6','P04U':'#a786c4'}
    for col,explode in enumerate((False,True),1):
        ax=fig.add_subplot(1,2,col,projection='3d',proj_type='ortho')
        shown={f'TONGUE_SECTION_{i}':x['solid'] for i,x in enumerate(tongues(d3,u,b),1)}
        shown.update({k:p02.plate_solid(disk(name,k,d,d3,u,b),z[0],6).translate([0,0,(20 if k=='P04L' else 50) if explode else 0]) for k,z in d['layers_z_mm'].items()})
        if not explode:shown.update(witness_solids(name,d))
        for key,solid in shown.items():
            p=mesh(solid);color=colors.get(key,'#5baf95' if key.startswith('W') else '#c9a36f')
            ax.add_collection3d(Poly3DCollection(p.vertices[p.faces],facecolor=color,edgecolor='none',alpha=.62 if key.startswith('P04') else .8))
        if not explode:
            for z in (450,456,494,500):
                coords=np.asarray(circle(171,d).exterior.coords)
                ax.plot(coords[:,0],coords[:,1],np.full(len(coords),z),ls='--',lw=.65,color='#64748b')
            for t in tongues(d3,u,b):
                p=t['xy'].centroid;ax.quiver(p.x,p.y,510,0,0,-21.5,color='#b45309',arrow_length_ratio=.12,lw=.8)
        ax.set(xlim=(-175,175),ylim=(-175,175),zlim=(448,545 if explode else 516),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
        # Keep actual units on axes; modest vertical exaggeration is explicitly labelled.
        ax.set_box_aspect((350,350,180));ax.view_init(28,35)
        ax.set_title('Material core detail / vertical display exaggerated\n6 green web witnesses; dashed skin bounds; orange assumed tool approach' if not explode else 'Exploded real disks +20/+50mm; six actual tongue sections\nDiagrammatic separation; validated order is in path report',fontsize=10)
    fig.suptitle(f'{d["variants"][name]["name"]} / DESIGN_ONLY — core interface reservation, no completed tabletop\nNominal Z450..500 budget50mm; actual real local BOM21; witness/skin/tool studies excluded',fontsize=13)
    fig.savefig(folder/'core-and-layer-stack.png',dpi=130);plt.close(fig)


def generate():
    d,d3,u,b=inputs();all_proofs={};summary={};assembly_dir=PART/'assembly';assembly_dir.mkdir(exist_ok=True)
    save_json(assembly_dir/'six-tongues.json',extraction(d,d3,u,b))
    for name in CONCEPTS:
        folder=PART/'variants'/name;folder.mkdir(parents=True,exist_ok=True)
        local={}
        for layer in ('P04L','P04U'):
            face=disk(name,layer,d,d3,u,b);met=metrics(name,layer,d,d3,u,b)
            kinds=[x['family'] for x in web_cuts(name,layer,d)]
            annotation=f'D190 x6; Z{met["z_mm"]}; 6 tongue24.4x6.2; 6 web W6.4 ({kinds.count("OPEN")} open/{kinds.count("RAIL")} rail); centerD{met["center_diameter_mm"]}'
            ex=export(folder,layer,face,d,'XY',annotation,cut_roles(face,tongue_slots(d,d3,u,b),web_cuts(name,layer,d)))
            met['export']=ex;save_json(folder/f'{layer}-dimensions.json',met);local[layer]=met
        witness_data={}
        for kind in sorted({family(name,a) for a in range(0,360,60)}):
            p=witness(kind,d)
            ex=export(folder,f'witness-{kind}',p,d,'r,z','INTERFACE_WITNESS_NOT_P05_RELEASE; nominal38 high; t thickness6')
            ex['role']='INTERFACE_WITNESS_NOT_P05_RELEASE';ex['quantity']=sum(family(name,a)==kind for a in range(0,360,60))
            save_json(folder/f'witness-{kind}-dimensions.json',ex);witness_data[kind]=ex
        solids=assembly(name,d,d3,u,b);static=p02.collision_matrix(solids)
        extended={**solids,**witness_solids(name,d)}
        mating=[x for x in p02.collision_matrix(extended) if x['a'].startswith('W') or x['b'].startswith('W')]
        proof=assembly_paths(name,d,d3,u,b)
        proof.update({'final_real_intersections':static,'interface_witness_intersections':mating,
                      'negative_controls':negative_controls(name,d,d3,u,b),'witness_profiles':witness_data})
        save_json(folder/'connections-and-paths.json',proof);all_proofs[name]=proof
        layout(name,d,d3,u,b,folder);assembly_render(name,d,d3,u,b,folder,solids);core_view(name,d,d3,u,b,folder)
        summary[name]={'name':d['variants'][name]['name'],'lower':local['P04L'],'upper':local['P04U'],
                       'real_body_count':21,'final_pair_checks':len(static),'witness_pair_checks':len(mating),
                       'disk_path_max_mm3':proof['maximum_disk_path_intersection_mm3'],
                       'witness_path_max_mm3':proof['maximum_witness_path_intersection_mm3']}
        print(name,'real21',len(static),'finalmax',max(x['intersection_mm3'] for x in static),
              'witnessmax',max(x['intersection_mm3'] for x in mating),'paths',proof['maximum_disk_path_intersection_mm3'],proof['maximum_witness_path_intersection_mm3'],flush=True)
    save_json(assembly_dir/'proofs.json',all_proofs);save_json(assembly_dir/'comparison.json',summary)
    refs={}
    for prefix in ('projects/CTB-01/specifications/CTB-000',*[f'projects/CTB-01/parts/{p}' for p in ('P01','P02','P03')]):
        names=subprocess.check_output(['git','ls-tree','-r','--name-only',d['source_commit'],prefix],cwd=ROOT,text=True).splitlines()
        for name in names:refs[name]=hashlib.sha256(subprocess.check_output(['git','show',d['source_commit']+':'+name],cwd=ROOT)).hexdigest()
    save_json(PART/'src/upstream-sha256.json',refs)
    for file in PART.rglob('*.svg'):file.write_text('\n'.join(s.rstrip() for s in file.read_text().splitlines())+'\n')


if __name__=='__main__':generate()
