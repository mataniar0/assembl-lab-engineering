"""P07 cut contours, finite experimental rim material and nominal integration visuals."""
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


def export(folder,label,p,d,plane,annotation,grain=False,thickness=6):
    folder.mkdir(parents=True,exist_ok=True);loops=paths(p);x0,y0,x1,y1=p.bounds;m=20;w=x1-x0+40;h=y1-y0+40
    doc=ezdxf.new('R2010');doc.units=4;doc.layers.new('CUT_DESIGN_ONLY',dxfattribs={'color':1});doc.layers.new('NOT_CUT_DIMENSIONS',dxfattribs={'color':5});ms=doc.modelspace()
    for pts in loops:ms.add_lwpolyline(pts,close=True,dxfattribs={'layer':'CUT_DESIGN_ONLY'})
    for p0,p1 in (((x0,y0-5),(x1,y0-5)),((x1+5,y0),(x1+5,y1))):ms.add_line(p0,p1,dxfattribs={'layer':'NOT_CUT_DIMENSIONS'})
    text=[f'{label} DESIGN_ONLY {plane}',annotation,f'envelope W{x1-x0:g} x H{y1-y0:g} mm; thickness{thickness:g}; 1:1mm']
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
        p=mesh(s);p.visual.face_colors=[217,151,79,255] if k.startswith('P07R') else [60,174,160,170] if k.startswith('P07') else [137,99,177,255] if k.startswith('P04') else [205,169,118,255]
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


def dimensions(name,d,d5,d4,d3,u,b):
    length=circumference(d)/d[name]['segments'];records={}
    for i in range(d[name]['segments']):
        face=flat_profile(name,i,d);solid=bent_solid(name,i,d);ideal=4*face.area
        records[f'P07R{i+1}']={'intrinsic_plane':'(s,height), portrait sheet(x=height,y=s)',
            'intrinsic_paths_s_h_mm':paths(face),'slabs':slab_intervals(face),
            'phase_angle_deg':d['seam_phase_deg']+i*360/d[name]['segments'],
            'nominal_arc_length_mm':length,'nominal_seam_gap_mm':.4,'nominal_neutral_axis_radius_mm':173,
            'net_cut_area_mm2':face.area,'ideal_mapped_volume_mm3':ideal,'actual_faceted_volume_mm3':solid.volume(),
            'relative_mapping_volume_error':abs(solid.volume()/ideal-1),'straight_developed_geometry_only_not_bend_recipe':True,
            'bound_surface_chord_sagitta_mm':175*(1-math.cos(math.pi/360)),
            'actual_bent_bounds_mm':list(solid.bounding_box()),'kerf_status':'KERF_COUPON_PENDING'}
    return {'release':'DESIGN_ONLY / AWAITING_LEAD_SELECTION','source_commit':d['source_commit'],
        'units':'mm','skin_status':'EDGE_COMB_V2_PROPOSAL' if name=='C' else 'BASELINE_R171_NO_TOP_HOLE',
        'top_layers_mm':{'P07B':[450,456],'core':[456,494],'P07T':[494,500],'rim':[450,500]},
        'outer_diameter_mm':350,'skin_base_diameter_mm':342,'skin_max_radius_mm':175 if name=='C' else 171,
        'skin_thickness_mm':6,'rim_thickness_mm':4,'nominal_development_mm':circumference(d),
        'segments':records,'cut_parts':{},'contacts':contacts(name,d,d5,d4,d3,u,b),
        'nominal_circumference_coverage_mm':circumference(d)-d[name]['segments']*.4,
        'total_nominal_seam_gaps_mm':d[name]['segments']*.4,
        'kerf_grid_pitch_hypothesis_mm':8,'same_row_grid_pitch_nominal_mm':8 if name=='A' else 16,
        'kerf_slot_width_hypothesis_mm':.8,'remaining_lateral_web_screen_mm':7.2,
        'minimum_seam_keepout_screen_mm':12,'continuous_edge_rails_mm':8 if name=='A' else 6.5 if name=='B' else None,
        'C_local_end_bridges_mm':6.5 if name=='C' else None,'sharp_kerf_ends':'EXPERIMENTAL_STRESS_CONCENTRATION_NOT_TESTED',
        'bom':{'upstream':27,'skins':2,'rim_segments':d[name]['segments'],'total_real_bodies':29+d[name]['segments'],
            'P06_P08_fixtures_glue_hardware_actual_bodies':0},'physical_status':'NOT_RUN','kerf_compensation_mm':None}


def review_views(name,d,d5,d4,d3,u,b,parts,proof,out):
    crop=p02.plate_solid(box(-300,-300,300,300),440,145)
    fig=plt.figure(figsize=(16,8),layout='constrained')
    for index,explode in enumerate((False,True),1):
        ax=fig.add_subplot(1,2,index,projection='3d',proj_type='ortho')
        for k,s in parts.items():
            if explode:
                if k=='P07T':s=s.translate([0,0,35])
                if k.startswith('P07R'):s=s.translate([0,0,65])
            shown=s^crop
            if shown.volume()<1e-8:continue
            color='#d9974f' if k.startswith('P07R') else '#4fada0' if k.startswith('P07') else '#9c7fb7' if k.startswith('P04') else '#bea47f'
            draw3(ax,shown,color,.8 if k.startswith('P07R') else .17 if k.startswith('P07') else .6)
        ax.set(xlim=(-190,190),ylim=(-190,190),zlim=(440,585),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((380,380,200));ax.view_init(27,35)
        if not explode:
            for radius in (d['skin_radius_mm'],d['outer_radius_mm']):
                xy=np.asarray(circle(radius,d).exterior.coords)
                for z in d['rim_z_mm']:ax.plot(xy[:,0],xy[:,1],np.full(len(xy),z),color='#64748b',lw=.5,ls='--')
        ax.set_title(('Exploded: display offsets, not insertion' if explode else f'Actual {len(parts)} bodies, lower base cropped')+'\nP06 reservation only; P08 absent',fontsize=10)
    fig.suptitle(f'CTB007 {name} / DESIGN_ONLY / finite perforated rim; dashed cylindrical envelope is non-BOM; physical bend NOT_RUN')
    fig.savefig(out/f'{name}-tabletop-and-exploded.png',dpi=115,bbox_inches='tight',pad_inches=.25);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(16,7),layout='constrained')
    ax=axes[0]
    draw2(ax,p05.rib('A',d5),'#c6a97f')
    for layer,z in [('P07B',450),('P07T',494)]:
        p=skin(name,layer,d,d4,d3,u,b);line=p.intersection(LineString([[0,0],[200,0]]))
        for seg in ([line] if line.geom_type=='LineString' else line.geoms):
            if seg.geom_type=='LineString' and not seg.is_empty and seg.length>1e-8:draw2(ax,box(seg.bounds[0],z,seg.bounds[2],z+6),'#64b6a5')
    for layer,z in d4['layers_z_mm'].items():
        cross=p04.disk('A',layer,d4,d3,u,b).intersection(LineString([[0,0],[200,0]]))
        for seg in ([cross] if cross.geom_type=='LineString' else cross.geoms):
            if seg.geom_type=='LineString' and not seg.is_empty and seg.length>1e-8:draw2(ax,box(seg.bounds[0],z[0],seg.bounds[2],z[1]),'#a38bb9')
    for i in range(d[name]['segments']):
        for (a,c),xy in bent_slabs(name,i,d):
            cross=xy.intersection(LineString([[0,0],[200,0]]))
            for seg in ([cross] if cross.geom_type=='LineString' else cross.geoms if hasattr(cross,'geoms') else []):
                if seg.geom_type=='LineString' and not seg.is_empty and seg.length>1e-8:draw2(ax,box(seg.bounds[0],450+a,seg.bounds[2],450+c),'#db9d60')
    ax.set(xlim=(0,181),ylim=(445,505),aspect='equal',xlabel='r at Y0 mm',ylabel='Z mm',title='Actual radial section / 50mm total\nP05 ends169, rim inner171: AIR, not glue')
    ax=axes[1];draw2(ax,skin(name,'P07B',d,d4,d3,u,b),'#69b2a4')
    for i in range(d[name]['segments']):
        ang=math.radians(d['seam_phase_deg']+i*360/d[name]['segments']);ax.plot([158*math.cos(ang),180*math.cos(ang)],[158*math.sin(ang),180*math.sin(ang)],color='#a35826',lw=2)
    for t in p04.tongues(d3,u,b):draw2(ax,t['xy'],'#c5a173')
    ax.set(xlim=(-183,183),ylim=(-183,183),aspect='equal',xlabel='X mm',ylabel='Y mm',title='Bottom skin / six real tongue slots\nseams shown; C edge-tabs are a separate study')
    fig.suptitle(f'{name} / NO_HOLE top / kerf neutral axis173 unmeasured / no load or capture proof')
    fig.savefig(out/f'{name}-sections-and-interfaces.png',dpi=115);plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(17,7),layout='constrained')
    for ax,(label,route) in zip(axes,proof['routes'].items()):
        if not isinstance(route,dict) or 'steps' not in route:continue
        lines=[label,route['status']]
        for i,s in enumerate(route['steps'],1):lines.append(f"{i:02} {s['moving']}: {s['status']} ({s['maximum_intersection_mm3']:.3g}mm3)")
        ax.text(.02,.98,'\n'.join(lines),va='top',family='monospace',fontsize=8,transform=ax.transAxes);ax.axis('off')
    fig.suptitle(f'{name}: exact translation sweeps of pre-bent ideal material / no deformation/P08 assembly claim')
    fig.savefig(out/f'{name}-assembly-orders.png',dpi=115);plt.close(fig)


def envelope_contract(d):
    return {'role':'ANALYTIC_CLOSED_CYLINDRICAL_RESERVATION_NOT_MATERIAL_NOT_BOM',
            'inner_radius_mm':d['skin_radius_mm'],'outer_radius_mm':d['outer_radius_mm'],
            'z_mm':d['rim_z_mm'],'angular_extent_deg':[0,360],
            'comparison':'actual segmented perforated material is in variant GLBs, including gaps',
            'physical_bending':'NOT_RUN','P06':'RESERVATION_ONLY_ISSUE23_OPEN','P08':'ACCESS_RESERVATION_ONLY'}


def generate():
    d,d5,d4,d3,u,b=inputs();out=PART/'assembly';out.mkdir(exist_ok=True);summary={}
    save_json(out/'rim-envelope-RESERVATION.json',envelope_contract(d))
    for name in CONCEPTS:
        folder=PART/'variants'/name;folder.mkdir(exist_ok=True);met=dimensions(name,d,d5,d4,d3,u,b)
        for layer in ['P07B','P07T']:
            p=skin(name,layer,d,d4,d3,u,b);ex=export(folder,layer,p,d,'global X,Y','DESIGN_ONLY; no kerf calibration; thickness6',thickness=6);ex.update({'quantity':1,'nominal_thickness_mm':6});met['cut_parts'][layer]=ex
        for i in range(d[name]['segments']):
            label=f'P07R{i+1}';flat=flat_profile(name,i,d);ex=export(folder,label,sheet_profile(flat),d,'X=bandheight,Y=arc s','EXPERIMENTAL4mm; KERF_COUPON_PENDING',thickness=4);ex.update({'quantity':1,'nominal_thickness_mm':4});met['cut_parts'][label]=ex
        parts=assembly(name,d,d5,d4,d3,u,b);pairs=p02.collision_matrix(parts);rr=routes(name,d,d5,d4,d3,u,b)
        proof={'authority':'DESIGN_ONLY_PROVISIONAL_P07_EDGE_COMB_NOT_APPROVED' if name=='C' else 'DESIGN_ONLY_BASELINE_SKIN_CONCEPT',
               'actual_bodies':len(parts),'P06':'RESERVATION_ONLY_CTB006R_ISSUE23_OPEN','P08':'NOT_MODELED_ACCESS_RESERVATION_ONLY',
               'final_intersections':pairs,'maximum_final_intersection_mm3':max(x['intersection_mm3'] for x in pairs),
               'routes':rr,'negative_controls':negatives(name,d,d5,d4,d3,u,b),'contacts':met['contacts']}
        glb(parts,out/f'{name}-actual-DESIGN_ONLY.glb',proof['authority'])
        save_json(folder/'dimensions-and-bom.json',met);save_json(folder/'connections-and-paths.json',proof);summary[name]=proof
        review_views(name,d,d5,d4,d3,u,b,parts,proof,out)
        print(name,'realbodies',len(parts),'finalmax',proof['maximum_final_intersection_mm3'],'routes',[(k,v.get('status')) for k,v in rr.items()],flush=True)
    save_json(out/'proofs.json',summary)
    refs={}
    for prefix in ['projects/CTB-01/specifications/CTB-000',*[f'projects/CTB-01/parts/P{i:02d}' for i in range(1,7)]]:
        for name in subprocess.check_output(['git','ls-tree','-r','--name-only',d['source_commit'],prefix],cwd=ROOT,text=True).splitlines():refs[name]=hashlib.sha256(subprocess.check_output(['git','show',d['source_commit']+':'+name],cwd=ROOT)).hexdigest()
    save_json(PART/'src/upstream-sha256.json',refs)
    for svg in PART.rglob('*.svg'):svg.write_text('\n'.join(x.rstrip() for x in svg.read_text().splitlines())+'\n')
if __name__=='__main__':generate()
