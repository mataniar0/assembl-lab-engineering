"""CAD, cut contours and all visuals from the actual P05/P04 material model."""
import json
import subprocess
import xml.sax.saxutils as xml
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Polygon as Patch,Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from model import *


def save_json(path,data):path.write_text(json.dumps(data,indent=2)+'\n')


def export(folder,label,p,d,plane,annotation,grain=False):
    folder.mkdir(parents=True,exist_ok=True);loops=paths(p);x0,y0,x1,y1=p.bounds;m=20;w=x1-x0+40;h=y1-y0+40
    doc=ezdxf.new('R2010');doc.units=4;doc.layers.new('CUT_DESIGN_ONLY',dxfattribs={'color':1});doc.layers.new('NOT_CUT_DIMENSIONS',dxfattribs={'color':5});ms=doc.modelspace()
    for pts in loops:ms.add_lwpolyline(pts,close=True,dxfattribs={'layer':'CUT_DESIGN_ONLY'})
    for p0,p1 in (((x0,y0-5),(x1,y0-5)),((x1+5,y0),(x1+5,y1))):ms.add_line(p0,p1,dxfattribs={'layer':'NOT_CUT_DIMENSIONS'})
    text=[f'{label} DESIGN_ONLY {plane}',annotation,f'envelope W{x1-x0:g} x H{y1-y0:g} mm; thickness6; 1:1mm']
    for i,line in enumerate(text):ms.add_text(line,dxfattribs={'height':2,'insert':(x0,y1+13-4*i),'layer':'NOT_CUT_DIMENSIONS'})
    if grain:
        ms.add_line((x0+10,y0-12),(x1-10,y0-12),dxfattribs={'layer':'NOT_CUT_DIMENSIONS'})
        ms.add_text('face grain parallel r (hypothesis)',dxfattribs={'height':1.8,'insert':(x0+5,y0-17),'layer':'NOT_CUT_DIMENSIONS'})
    doc.saveas(folder/f'{label}.dxf')
    points=''.join('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+'"/>' for pts in loops)
    texts=''.join(f'<text x="{x0}" y="{-y1-13+4*i}">{xml.escape(t)}</text>' for i,t in enumerate(text))
    if grain:texts+=f'<path d="M{x0+10},{-y0+12} H{x1-10}" stroke="#986b34" stroke-width="0.25"/><text x="{x0+5}" y="{-y0+17}">face grain parallel r: hypothesis</text>'
    (folder/f'{label}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="{x0-m} {-y1-m} {w} {h}">
<title>{xml.escape(label)} DESIGN_ONLY {plane}</title><metadata>sha256={digest(p)}; no kerf compensation</metadata>
<g id="CUT" transform="scale(1,-1)" fill="none" stroke="black" stroke-width="0.2">{points}</g>
<g id="NOT_CUT_DIMENSIONS" font-size="1.9" fill="#334155">{texts}
<path d="M{x0},{-y0+5} H{x1} M{x1+5},{-y0} V{-y1}" fill="none" stroke="#334155" stroke-width="0.2"/>
<text x="{(x0+x1)/2-10}" y="{-y0+9}">W{x1-x0:g} mm</text><text x="{x1+7}" y="{-(y0+y1)/2}">H{y1-y0:g}</text></g></svg>\n''')
    dpi=d['raster_dpi'];fig=plt.figure(figsize=(w/25.4,h/25.4),dpi=dpi);ax=fig.add_axes([0,0,1,1])
    for pts in loops:ax.add_patch(Patch(pts,fill=False,color='black',lw=.8))
    for i,t in enumerate(text):ax.text(x0,y1+13-4*i,t,fontsize=5.4)
    ax.plot([x0,x1],[y0-5]*2,color='#334155',lw=.5);ax.text((x0+x1)/2,y0-9,f'W{x1-x0:g} mm',fontsize=5.4,ha='center')
    ax.plot([x1+5]*2,[y0,y1],color='#334155',lw=.5);ax.text(x1+7,(y0+y1)/2,f'H{y1-y0:g}',fontsize=5.4)
    if grain:ax.annotate('',(x1-10,y0-12),(x0+10,y0-12),arrowprops={'arrowstyle':'->','color':'#986b34'});ax.text(x0+5,y0-17,'face grain parallel r: hypothesis',fontsize=5.4)
    ax.set(xlim=(x0-20,x1+20),ylim=(y0-20,y1+20));ax.axis('off')
    fig.savefig(folder/f'{label}.png',dpi=dpi,metadata={'Description':f'DESIGN_ONLY;sha256={digest(p)};1:1mm at96dpi'});plt.close(fig)
    return {'paths_mm':loops,'sha256':digest(p),'bounds_mm':list(p.bounds),'artboard_wh_mm':[w,h],'raster_dpi':dpi,'plane':plane,'cut_layer':'CUT_DESIGN_ONLY','dimension_layer':'NOT_CUT_DIMENSIONS'}


def mesh(s):
    m=s.to_mesh();return trimesh.Trimesh(vertices=np.asarray(m.vert_properties)[:,:3],faces=np.asarray(m.tri_verts),process=False)


def glb(solids,path,role):
    scene=trimesh.Scene();data={}
    for k,s in solids.items():
        p=mesh(s);p.visual.face_colors=[53,155,129,255] if k.startswith('P05') else [137,99,177,255] if k.startswith('P04') else [205,169,118,255]
        data[k]={'volume_mm3':s.volume(),'bounds_mm':p.bounds.tolist()};p.apply_scale(.001);scene.add_geometry(p,node_name=k,geom_name=k)
    path.write_bytes(scene.export(file_type='glb'));save_json(path.with_suffix('.json'),{'role':role,'actual_bodies':27,'units':'GLTF metres; source millimetres','parts':data})


def draw2(ax,poly,color,alpha=1):
    if poly.is_empty:return
    polys=[poly] if poly.geom_type=='Polygon' else list(poly.geoms)
    for p in polys:
        if p.geom_type!='Polygon':continue
        for i,pts in enumerate(paths(p)):ax.add_patch(Patch(pts,facecolor=color if i==0 else 'white',edgecolor='#334155',lw=.6,alpha=alpha))


def draw3(ax,s,color,alpha=1):
    p=mesh(s);ax.add_collection3d(Poly3DCollection(p.vertices[p.faces],facecolor=color,edgecolor='none',alpha=alpha))


def sections(name,d,d4,d3,u,b,folder):
    proposed=name!='A';fig,axes=plt.subplots(2,2,figsize=(16,9),layout='constrained')
    face=rib(name,d)
    for ax,t in zip(axes[0],(0,10.5)):
        if t==0:draw2(ax,face,'#6bb498',.7)
        else:draw2(ax,p04.tongues(d3,u,b)[0]['rz'],'#cfa879')
        for layer,z in d4['layers_z_mm'].items():
            shape=disk(name,layer,d,d4,d3,u,b,proposed);line=shape.intersection(LineString([[0,t],[175,t]]))
            seg=[line] if line.geom_type=='LineString' else list(line.geoms)
            for s in seg:
                if s.geom_type=='LineString':ax.add_patch(Rectangle((s.bounds[0],z[0]),s.bounds[2]-s.bounds[0],6,facecolor='#579ec4' if layer=='P04L' else '#a888c5',edgecolor='#334155',alpha=.85))
        for z,p,label in ((450,p04.skin(d4,d3,u,b),'P07B'),(494,p04.circle(171,d4),'P07T')):
            line=p.intersection(LineString([[0,t],[175,t]]));seg=[line] if line.geom_type=='LineString' else list(line.geoms)
            for s in seg:
                if s.geom_type=='LineString':ax.add_patch(Rectangle((s.bounds[0],z),s.bounds[2]-s.bounds[0],6,fill=False,hatch='///',edgecolor='#64748b',lw=.5))
            ax.text(120 if t==0 else 78,z+2,label+' envelope',fontsize=7)
        ax.set(xlim=(70,175) if t==0 else (35,105),ylim=(448,502),xlabel='r mm',ylabel='Z mm',title=f'Physical section t={t:g} / '+('L/U-v2 CR proposal' if name=='B' else 'L-v2 CR / original U' if name=='C' else 'selected P04A'));ax.set_aspect('equal');ax.grid(alpha=.15)
    ax=axes[1,0];draw2(ax,face,'#6bb498');ax.set(xlim=(78,100),ylim=(454,496),xlabel='r mm',ylabel='Z mm',title='Actual filleted inner interface / detail');ax.set_aspect('equal');ax.grid(alpha=.2)
    if name=='C':ax.annotate('0.4mm flat / 2.4mm2 stop\nNOT strength',(82.6,479.6),(.04,.9),textcoords='axes fraction',fontsize=7,arrowprops={'arrowstyle':'->'})
    ax=axes[1,1]
    for layer,color in (('P04L','#579ec4'),('P04U','#a888c5')):
        # side-by-side disk details at the actual t/r plane, not superposed full disks.
        z=sum(d4['layers_z_mm'][layer])/2
        for a,c in section_intervals(face,z):ax.add_patch(Rectangle((a,z-1),c-a,2,facecolor='#6bb498'))
        ax.text(103,z,f'{layer}: rib intervals at Z{z:g}',fontsize=8)
    ax.set(xlim=(78,174),ylim=(450,500),xlabel='r mm',ylabel='Z mm',title='Rib material through lower/upper slab midplanes');ax.grid(alpha=.2)
    fig.suptitle(f'P05 {name} / DESIGN_ONLY / six identical actual ribs\n'+('Compatible selected P04A, no radial retainer' if name=='A' else 'Conditional retention with CR_REQUIRED P04-v2; upstream unchanged'),fontsize=14)
    fig.savefig(folder/'sections-and-joints.png',dpi=125);fig.savefig(folder/'sections-and-joints.svg',metadata={'Date':None});plt.close(fig)


def views(name,d,d4,d3,u,b,out):
    proposed=name!='A';solids=assembly(name,d,d4,d3,u,b,proposed)
    fig=plt.figure(figsize=(16,9),layout='constrained')
    for index,core in enumerate((False,True),1):
        ax=fig.add_subplot(1,2,index,projection='3d',proj_type='ortho')
        for k,s in solids.items():
            if core and not (k.startswith('P04') or k.startswith('P05')):continue
            draw3(ax,s,'#5cae92' if k.startswith('P05') else '#9e7abe' if k.startswith('P04') else '#cfa879',.8 if k.startswith('P05') else .48 if k.startswith('P04') else .19)
        if core:
            for z in (450,456,494,500):
                xy=np.asarray(p04.circle(171,d4).exterior.coords);ax.plot(xy[:,0],xy[:,1],np.full(len(xy),z),ls='--',color='#64748b',lw=.6)
            ax.set(xlim=(-175,175),ylim=(-175,175),zlim=(445,505));ax.set_box_aspect((350,350,120));ax.set_title('Actual 8-part core / skin bounds dashed\nvertical display exaggerated; no skins/locks in BOM')
        else:ax.set(xlim=(-280,280),ylim=(-280,280),zlim=(0,510));ax.set_box_aspect((560,560,510));ax.set_title('Actual27 bodies / selected base +6 identical P05')
        ax.set(xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.view_init(26,35)
    fig.suptitle(f'CTB005 {name} / DESIGN_ONLY / '+('original P04A' if name=='A' else 'CR_REQUIRED proposal disks; original baseline exported separately'),fontsize=14)
    fig.savefig(out/f'{name}-actual27-and-core.png',dpi=125,bbox_inches='tight',pad_inches=.25);plt.close(fig)
    fig=plt.figure(figsize=(16,8),layout='constrained')
    ax=fig.add_subplot(1,2,1,projection='3d',proj_type='ortho')
    for k,s in solids.items():
        if k.startswith('P05'):
            a=math.radians((int(k.split('_')[1])-1)*60)
            s=s.translate([45*math.cos(a),45*math.sin(a),0 if name=='A' else 22])
        elif k=='P04U':s=s.translate([0,0,55])
        elif not k.startswith('P04'):continue
        draw3(ax,s,'#5cae92' if k.startswith('P05') else '#a888c5',.75)
    ax.set(xlim=(-215,215),ylim=(-215,215),zlim=(450,550),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((430,430,200));ax.view_init(28,35);ax.set_title('Exploded geometry / diagrammatic separation\nuse exact staged route, not these display offsets')
    ax=fig.add_subplot(1,2,2)
    sequence=install(name,d,d4,d3,u,b,proposed)['steps']
    for i,s in enumerate(sequence):
        x=0;y=len(sequence)-i
        ax.text(x,y,f'{i+1}. {s["moving"]}: '+('down fromZ520' if s['moving'].startswith('P04') or s['moving']=='P07B_ENVELOPE' else 'radial inward100mm' if name=='A' else 'vertical down64mm'),fontsize=10)
    ax.set(xlim=(-.2,3),ylim=(0,len(sequence)+1));ax.axis('off');ax.set_title('Continuous route / skin envelope is non-BOM')
    fig.suptitle(f'{name} / DESIGN_ONLY / '+('selected-disk route' if name=='A' else 'CR_REQUIRED staged proposal route'),fontsize=14)
    fig.savefig(out/f'{name}-exploded-and-order.png',dpi=120,bbox_inches='tight',pad_inches=.25);plt.close(fig)


def generate():
    d,d4,d3,u,b=inputs();summary={};out=PART/'assembly';out.mkdir(exist_ok=True)
    save_json(out/'upstream-y-first-recheck.json',p03.y_first('A_COMPACT_CLOSED',d3,u,b))
    for name in CONCEPTS:
        folder=PART/'variants'/name;face=rib(name,d);met=metrics(name,d,d4,d3,u,b)
        met['export']=export(folder,'P05',face,d,'r,z',f'six identical; thickness6; outerR169; Z456..494; grain hypothesis',True)
        save_json(folder/'P05-dimensions.json',met)
        proof={'baseline':{},'proposal':None}
        for proposal in (False,True):
            if name=='A' and proposal:continue
            solids=assembly(name,d,d4,d3,u,b,proposal);pairs=p02.collision_matrix(solids);seq=install(name,d,d4,d3,u,b,proposal)
            branch={'authority':'CR_REQUIRED_NOT_APPROVED' if proposal else 'SELECTED_P04_A_UNCHANGED',
                    'body_count':27,'final_intersections':pairs,'maximum_final_intersection_mm3':max(x['intersection_mm3'] for x in pairs),
                    'insertion':seq,'retention':retention(name,d,d4,d3,u,b,proposal),
                    'controls_and_access':access_and_controls(name,d,d4,d3,u,b,proposal)}
            proof['proposal' if proposal else 'baseline']=branch
            filename=f'{name}-proposed-27-CR_REQUIRED.glb' if proposal else f'{name}-baseline-27-'+('BLOCKED.glb' if name=='B' else 'DESIGN_ONLY.glb')
            glb(solids,out/filename,branch['authority']+('; BLOCKED_FINAL_COLLISION' if name=='B' and not proposal else ''))
            if proposal:
                pdir=PART/'proposals'/name
                for layer in ('P04L','P04U'):
                    label=layer+('-v2-proposal' if layer in d[name]['proposed_slots_r_mm'] else '-v1-reference')
                    poly=disk(name,layer,d,d4,d3,u,b,True)
                    ex=export(pdir,label,poly,d,'X,Y',f'CR_REQUIRED {name}; D190 x6; NO_HOLE; six tongues +six web slots')
                    ex.update({'release':'CR_REQUIRED_NOT_APPROVED','layer':layer,'original_p04_preserved':True,'nominal_z_mm':d4['layers_z_mm'][layer]})
                    save_json(pdir/f'{label}-dimensions.json',ex)
            print(name,'proposal',proposal,'final',branch['maximum_final_intersection_mm3'],'path',seq['status'],flush=True)
        save_json(folder/'connections-and-paths.json',proof);summary[name]=proof
        sections(name,d,d4,d3,u,b,folder);views(name,d,d4,d3,u,b,out)
    save_json(out/'proofs.json',summary)
    refs={}
    for prefix in ('projects/CTB-01/specifications/CTB-000',*[f'projects/CTB-01/parts/{p}' for p in ('P01','P02','P03','P04')]):
        for name in subprocess.check_output(['git','ls-tree','-r','--name-only',d['source_commit'],prefix],cwd=ROOT,text=True).splitlines():
            refs[name]=hashlib.sha256(subprocess.check_output(['git','show',d['source_commit']+':'+name],cwd=ROOT)).hexdigest()
    save_json(PART/'src/upstream-sha256.json',refs)
    for svg in PART.rglob('*.svg'):svg.write_text('\n'.join(s.rstrip() for s in svg.read_text().splitlines())+'\n')

if __name__=='__main__':generate()
