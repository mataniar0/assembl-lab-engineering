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
    path.write_bytes(scene.export(file_type='glb'));save_json(path.with_suffix('.json'),{'role':role,'actual_bodies':len(solids),'units':'GLTF metres; source millimetres','parts':data})


def draw2(ax,poly,color,alpha=1):
    if poly.is_empty:return
    polys=[poly] if poly.geom_type=='Polygon' else list(poly.geoms)
    for p in polys:
        if p.geom_type!='Polygon':continue
        for i,pts in enumerate(paths(p)):ax.add_patch(Patch(pts,facecolor=color if i==0 else 'white',edgecolor='#334155',lw=.6,alpha=alpha))


def draw3(ax,s,color,alpha=1):
    p=mesh(s);ax.add_collection3d(Poly3DCollection(p.vertices[p.faces],facecolor=color,edgecolor='none',alpha=alpha))


def metrics(name,d,d3,u):
    sec=sections(d,d3,u);parts=planar_parts(name,d,d3,u);face,cut=cheek_overlay(name,d,d3,u)
    keys=0 if name=='A' else 6
    land=sec['joint_common_r_mm'][1]-(sec['joint_center_r_mm']+d[name]['tab_radial_width_mm']/2+.2)
    return {'release':'DESIGN_ONLY / CR_REQUIRED / AWAITING_LEAD_SELECTION','units':'mm',
        'sections':sec,'material':'birch; nominal6mm provisional; measured thickness/kerf UNKNOWN',
        'outer_convex_fillet_radius_mm':d['outer_fillet_radius_mm'],'ring_slab_z_mm':[242,248],'ring_band_width_mm':d[name]['band_width_mm'],'arm_width_mm':d['arm_width_mm'],
        'arm_gap_each_side_mm':(15-d['arm_width_mm'])/2,'six_cheek_mortise_allowance_each_side_mm':.2,
        'tab_radial_width_mm':d[name]['tab_radial_width_mm'],'tab_abs_t_mm':d[name]['tab_abs_t_mm'],
        'ring_cut_area_mm2':sum(p.area for p in parts.values()),'removed_holes':'interior loops are waste; remove completely, no floating retained inserts',
        'screened_ring_band_minimum_mm':d[name]['band_width_mm'],
        'screened_specific_neck_mm':6.8 if name=='B' else 6.2 if name=='C' else 12,
        'screened_neck_basis':'B:(24-10.4)/2 female splice land; C:26.5-20.3 outer keyslot land; A:12 radial tab',
        'cheek_outer_land_at_expanded_ring_band_mm':land,'cheek_proposal_area_mm2':face.area,
        'sheet_height_width_mm':d['sheet_hw_mm'],'single_part_margin_mm':10,'nesting':'NOT_RUN_NOT_APPROVED',
        'bom':{'unchanged_family_counts':{'P01_overlay':6,'P02':9,'P02B':3,'P03':1,'P04':2,'P05':6},
               'ring_pieces':len(parts),'actual_wood_keys':keys,'added_p06_count':len(parts)+keys,'total_real_bodies':27+len(parts)+keys,
               'fixtures_hardware_skins_locks':0,'fixture_requirement':'external holding before cheek closure for A/C, not designed; not a hidden solid'},
        'cut_parts':{},'measured_strength':'NOT_RUN'}


def drawings(name,d,d3,u,solids,proof,out):
    face,_=cheek_overlay(name,d,d3,u);original=active_cheek(d3,u);ring=full_ring(name,d,d3,u)
    fig,axes=plt.subplots(1,3,figsize=(17,7),layout='constrained')
    ax=axes[0];draw2(ax,ring,'#60b6ac');joint=sections(d,d3,u)['joint_center_r_mm']
    for angle in d['leg_angles_deg']:
        for t in (-10.5,10.5):draw2(ax,rotate(box(83.3895,t-3,140.5521,t+3),angle,origin=(0,0)),'#c8ac83',.45)
    ax.set(xlim=(-155,155),ylim=(-155,155),aspect='equal',title='XY ring / six cheek locations\nshaded cheek envelope, actual cutouts in section',xlabel='X mm',ylabel='Y mm')
    ax=axes[1];draw2(ax,face,'#d1b58c')
    # Exact r-z section at the centre of the +t cheek, with holes preserved.
    line=ring.intersection(LineString([[-200,10.5],[200,10.5]]))
    for seg in ([line] if line.geom_type=='LineString' else list(line.geoms)):
        if seg.geom_type=='LineString':draw2(ax,box(seg.bounds[0],242,seg.bounds[2],248),'#53ada8')
    if name=='B':draw2(ax,stop_key(d,d3,u),'#de925e')
    if name=='C':ax.add_patch(Rectangle((joint-3,235),6,21,fill=False,ec='#cf6b55',ls='--'))
    ax.set(xlim=(65,153),ylim=(225,268),aspect='equal',title='Actual P01 overlay / ring section t10.5\n'+('C keeper bounds dashed (outside cheek)' if name=='C' else 'B wood stop key shown' if name=='B' else 'A has no separate keys'),xlabel='r mm',ylabel='Z mm')
    ax=axes[2];draw2(ax,original,'#d1b58c',.65)
    for station in p02.stations(u):
        p=translate(p02.spacer('B_THROUGH_ADHESIVE',station['part'],u,inputs()[-1]),xoff=station['r_mm'])
        cross=p.intersection(LineString([[-100,10.5],[400,10.5]]))
        for seg in ([cross] if cross.geom_type=='LineString' else list(cross.geoms)):
            if seg.geom_type=='LineString':draw2(ax,box(seg.bounds[0],station['z_mm']-3,seg.bounds[2],station['z_mm']+3),'#6577b6')
    ax.axhspan(242,248,color='#399c91');ax.axhspan(407,413,color='#ab6dab');ax.axhspan(225,265,color='#399c91',alpha=.08)
    ax.text(165,200,'S3 197..203',fontsize=8);ax.text(152,245,'ring242..248',fontsize=8);ax.text(103,410,'Y407..413',fontsize=8)
    ax.set(xlim=(0,270),ylim=(0,505),aspect='equal',title='Actual cheek / four spacer stations\n39mm slab gap; keeper gap differs',xlabel='r mm',ylabel='Z mm')
    fig.suptitle(f'CTB006 {name} / DESIGN_ONLY / P01 overlay CR_REQUIRED, original untouched')
    fig.savefig(out/f'{name}-sections.png',dpi=115);fig.savefig(out/f'{name}-sections.svg',metadata={'Date':None});plt.close(fig)
    fig=plt.figure(figsize=(16,9),layout='constrained')
    for index,exploded in enumerate((False,True),1):
        ax=fig.add_subplot(1,2,index,projection='3d',proj_type='ortho')
        for k,s in solids.items():
            if exploded:
                if k.startswith('P06'):
                    if '_K' in k:s=s.translate([0,0,50])
                    elif name=='B':
                        a=math.radians(d['leg_angles_deg'][int(k[-1])-1]);s=s.translate([30*math.cos(a),30*math.sin(a),6.4])
                    else:s=s.translate([0,0,-35])
                elif 'P01' in k:
                    leg=int(k[1]);side=-1 if k.endswith('_1') else 1;a=math.radians(d['leg_angles_deg'][leg-1]);s=s.translate([-side*30*math.sin(a),side*30*math.cos(a),0])
            draw3(ax,s,'#3bada4' if k.startswith('P06') else '#ad7fb5' if k=='P03' else '#c8ad88',.85 if k.startswith('P06') else .2)
        ax.set(xlim=(-290,290),ylim=(-290,290),zlim=(0,510),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((580,580,510));ax.view_init(25,35)
        ax.set_title(('Exploded: display offsets only' if exploded else f'Conditional actual{len(solids)} bodies')+'\nP01 overlay requires approval; no skins/fixtures')
    fig.suptitle(f'P06 {name} / DESIGN_ONLY / no physical cutting approval');fig.savefig(out/f'{name}-actual-and-exploded.png',dpi=110);plt.close(fig)
    # Every numbered stage and its exact start/end offsets, including blocked routes.
    sequences=[('EARLY Y_FIRST + upper continuation',proof['early_path']),('AFTER CLOSED27',proof['late_path'])]
    fig,axes=plt.subplots(1,2,figsize=(19,12),layout='constrained')
    for ax,(label,seq) in zip(axes,sequences):
        lines=[label+' / '+seq['status'],seq.get('initial_state','all27 already in position with the P01 overlay')]
        for i,s in enumerate(seq['steps'],1):
            lines.append(f"{i:02d} {s['moving']}: {s['status']} start{s['start_offset_xyz_mm']} -> end{s['end_offset_xyz_mm']}")
        ax.text(.01,.98,'\n'.join(lines),va='top',family='monospace',fontsize=7.5,transform=ax.transAxes);ax.axis('off')
    fig.suptitle(f'{name}: exact full-material translation sweeps, no sampled-frame clearance claim / DESIGN_ONLY')
    fig.savefig(out/f'{name}-staged-paths.png',dpi=110);plt.close(fig)


def generate():
    d,d5,d4,d3,u,b=inputs();out=PART/'assembly';out.mkdir(exist_ok=True);summary={}
    save_json(out/'upstream-y-first-recheck.json',p03.y_first('A_COMPACT_CLOSED',d3,u,b))
    save_json(out/'leg-sections-and-support.json',{'sections':sections(d,d3,u),'support':support(d3,u)})
    for name in CONCEPTS:
        folder=PART/'variants'/name;folder.mkdir(exist_ok=True);met=metrics(name,d,d3,u)
        for label,p in planar_parts(name,d,d3,u).items():
            ex=export(folder,label,p,d,'X,Y','DESIGN_ONLY; nominal6; z242..248; no kerf; ring waste holes removed')
            ex['quantity']=1;met['cut_parts'][label]=ex
        if name!='A':
            label='P06'+name+'-KEY';poly=stop_key(d,d3,u) if name=='B' else vertical_key(d)
            ex=export(folder,label,poly,d,'r,z' if name=='B' else 't,z','six wood keys; nominal6; NOT a complete 6DOF retainer')
            ex['quantity']=6;met['cut_parts'][label]=ex
        proposal=PART/'proposals'/name;proposal.mkdir(parents=True,exist_ok=True)
        poly,_=cheek_overlay(name,d,d3,u)
        ex=export(proposal,'P01-ring-interface-study-v1',poly,d,'r,z','CR_REQUIRED; six identical cheeks; original P01/P02/P03 untouched',True)
        ex.update({'quantity':6,'approval':'NOT_APPROVED','affected_IF':['IF-09','IF-01','IF-02','IF-14']})
        save_json(proposal/'P01-ring-interface-study-v1-dimensions.json',ex)
        solids=assembly(name,d,d5,d4,d3,u,b);pairs=p02.collision_matrix(solids)
        original=assembly(name,d,d5,d4,d3,u,b,False);baseline=p02.collision_matrix(original)
        proof={'authority':'CR_REQUIRED_P01_RING_INTERFACE_STUDY_V1_NOT_APPROVED','actual_body_count':len(solids),
               'final_intersections':pairs,'maximum_final_intersection_mm3':max(x['intersection_mm3'] for x in pairs),
               'original_cheek_status':'BLOCKED_REQUIRES_OVERLAY','original_cheek_maximum_mm3':max(x['intersection_mm3'] for x in baseline),
               'early_path':early_path(name,d,d5,d4,d3,u,b),'late_path':late_paths(name,d,d5,d4,d3,u,b),
               'controls':controls(name,d,d5,d4,d3,u,b)}
        glb(solids,out/f'{name}-conditional-DESIGN_ONLY.glb',proof['authority'])
        save_json(out/f'{name}-original-cheeks-BLOCKED.json',{'final_intersections':baseline,'status':'BLOCKED','actual_bodies':len(original)})
        save_json(folder/'dimensions-and-bom.json',met);save_json(folder/'connections-and-paths.json',proof)
        summary[name]=proof;drawings(name,d,d3,u,solids,proof,out)
        print(name,'bodies',len(solids),'final',proof['maximum_final_intersection_mm3'],'early',proof['early_path']['status'],'late',proof['late_path']['status'],flush=True)
    save_json(out/'proofs.json',summary)
    refs={}
    for prefix in ('projects/CTB-01/specifications/CTB-000',*[f'projects/CTB-01/parts/P{i:02d}' for i in range(1,6)]):
        for name in subprocess.check_output(['git','ls-tree','-r','--name-only',d['source_commit'],prefix],cwd=ROOT,text=True).splitlines():
            refs[name]=hashlib.sha256(subprocess.check_output(['git','show',d['source_commit']+':'+name],cwd=ROOT)).hexdigest()
    save_json(PART/'src/upstream-sha256.json',refs)
    for svg in PART.rglob('*.svg'):svg.write_text('\n'.join(s.rstrip() for s in svg.read_text().splitlines())+'\n')

if __name__=='__main__':generate()
