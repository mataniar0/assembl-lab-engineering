#!/usr/bin/env python3
# CRIB-01 V0.6.8 full 3D assembly CONCEPT ONLY
# Prior measured user inputs / baseline; not manufacturing geometry.
import json, math, os, zipfile, hashlib, csv
from pathlib import Path
import numpy as np
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE=Path('/mnt/data/CRIB_V068_FULL_3D'); HERE.mkdir(exist_ok=True)
BASE_STEP=Path('/mnt/data/CRIB_V067_BASE_CAD_DESIGN_ONLY/CRIB_V067_BASE_CASSETTE_CONCEPT_NO_CUT.step')
assert BASE_STEP.exists()

# --------- Frozen design inputs ---------
MATTRESS=(1200.0,600.0,150.0)
TOTAL_HEIGHT=880.0
WALLS_SLEEP=4
WALLS_UNOCCUPIED_PROTOTYPE=3
# --------- Design-study provisional choices ---------
L,W=1204.,604. # internal mattress bay, not verified permissible gap
POST=70.; T=10.
TOP_RAIL=(800.,860.) # nominal, not certified measurement method
LOW_RAIL=(100.,180.) # candidate
SLAT_W=30.; SLAT_DEPTH=10.
LONG_SLATS=13; SHORT_SLATS=7
OUTER=(1344.,744.,880.)

assert abs((L-MATTRESS[0])/2-2.0)<1e-8
assert abs((W-MATTRESS[1])/2-2.0)<1e-8
assert 860-(180+MATTRESS[2])==530.0

base_compound = cq.importers.importStep(str(BASE_STEP))
base_shapes = base_compound.solids().vals()
assert len(base_shapes)==33, len(base_shapes)

parts=[]

# STEP parts reused verbatim, retaining exact model geometry from V0.6.7.
for i,s in enumerate(base_shapes,1):
    b=s.BoundingBox()
    # Characterize imported part based on bounding extents, for visualization only.
    if b.zmin>169.99 and b.xlen>300:
        group='base_panels'
    elif b.ylen>500 and b.xlen<22:
        group='base_ribs'
    else:
        group='base_shell'
    parts.append(dict(name=f'V067_BASE_{i:02d}',shape=s,group=group,when='both',source='V0.6.7 exact STEP geometry'))

# Simple CAD B-rep plates for *new conceptual* 3D wall/post geometry.
# This model intentionally has NO claimed rail-to-post fastening / slat mortise / load-path joints.
def make_box(name,xyz0,xyz1,group,when='both'):
    x0,y0,z0=xyz0;x1,y1,z1=xyz1
    if not(x1>x0 and y1>y0 and z1>z0):raise ValueError((name,xyz0,xyz1))
    s=(cq.Workplane('XY')
       .box(x1-x0,y1-y0,z1-z0,centered=(False,False,False))
       .translate((x0,y0,z0)).val())
    parts.append(dict(name=name,shape=s,group=group,when=when,source='V0.6.8 conceptual wall/post envelope'))

# Four corner box posts, outside the internal bay, separate sheet-like walls with 50x50 hollow core.
# Each vertical piece stays <= 880 mm, stock feasibility only (non-production).
for ip,(px,py) in enumerate([(-70.,-70.),(L,-70.),(-70.,W),(L,W)],1):
    make_box(f'POST{ip}_X_LOW',(px,py,0),(px+T,py+POST,TOTAL_HEIGHT),'posts')
    make_box(f'POST{ip}_X_HIGH',(px+POST-T,py,0),(px+POST,py+POST,TOTAL_HEIGHT),'posts')
    make_box(f'POST{ip}_Y_LOW',(px+T,py,0),(px+POST-T,py+T,TOTAL_HEIGHT),'posts')
    make_box(f'POST{ip}_Y_HIGH',(px+T,py+POST-T,0),(px+POST-T,py+POST,TOTAL_HEIGHT),'posts')

# Split all 4 skins at staggered butt joints (not structural joinery) for long rails > cutting length.
# Faces: outside web, inside web, bottom cap, top cap.
seams={'SIDE_A':470.,'SIDE_B':560.,'CAP_LOW':650.,'CAP_HIGH':740.}

def add_x_rail(prefix, y0, z0,z1,when):
    depth=40.;x0=0.;x1=L
    faces=[('SIDE_A',y0,y0+T,z0,z1),
           ('SIDE_B',y0+depth-T,y0+depth,z0,z1),
           ('CAP_LOW',y0+T,y0+depth-T,z0,z0+T),
           ('CAP_HIGH',y0+T,y0+depth-T,z1-T,z1)]
    for face,ya,yb,za,zb in faces:
        seam=seams[face]
        make_box(f'{prefix}_{face}_A',(x0,ya,za),(seam,yb,zb),'walls',when)
        make_box(f'{prefix}_{face}_B',(seam,ya,za),(x1,yb,zb),'walls',when)

def add_y_rail(prefix,x0,z0,z1,when):
    depth=40.; y0=0.;y1=W
    faces=[('SIDE_A',x0,x0+T,z0,z1),
           ('SIDE_B',x0+depth-T,x0+depth,z0,z1),
           ('CAP_LOW',x0+T,x0+depth-T,z0,z0+T),
           ('CAP_HIGH',x0+T,x0+depth-T,z1-T,z1)]
    for face,xa,xb,za,zb in faces:
        make_box(f'{prefix}_{face}',(xa,y0,za),(xb,y1,zb),'walls',when)

# rear long side and two short sides are cut-first prototype sides
# front long side is FUTURE ONLY, not built now
walls=[
 ('REAR','x',-40.,'both',LONG_SLATS),
 ('FRONT_FUTURE','x',W,'four',LONG_SLATS),
 ('LEFT','y',-40.,'both',SHORT_SLATS),
 ('RIGHT','y',L,'both',SHORT_SLATS),
]
for side,orient,offset,when,nslat in walls:
    if orient=='x':
        for nm,zz in [('LOW',LOW_RAIL),('TOP',TOP_RAIL)]:
            add_x_rail(f'{side}_{nm}',offset,*zz,when)
        gap=(L-SLAT_W*nslat)/(nslat+1)
        for k in range(nslat):
            center=gap+SLAT_W/2+k*(gap+SLAT_W)
            make_box(f'{side}_SLAT_{k+1:02d}',
                     (center-SLAT_W/2,offset+15,LOW_RAIL[1]),
                     (center+SLAT_W/2,offset+25,TOP_RAIL[0]),'slats',when)
    else:
        for nm,zz in [('LOW',LOW_RAIL),('TOP',TOP_RAIL)]:
            add_y_rail(f'{side}_{nm}',offset,*zz,when)
        gap=(W-SLAT_W*nslat)/(nslat+1)
        for k in range(nslat):
            center=gap+SLAT_W/2+k*(gap+SLAT_W)
            make_box(f'{side}_SLAT_{k+1:02d}',
                     (offset+15,center-SLAT_W/2,LOW_RAIL[1]),
                     (offset+25,center+SLAT_W/2,TOP_RAIL[0]),'slats',when)

# A modest visual footer can be added in preview but NOT geometry, avoiding unapproved brace details.
COLORS={
 'posts':[181,136,89,255],
 'walls':[206,172,127,255],
 'slats':[229,194,146,255],
 'base_shell':[187,151,110,255],
 'base_ribs':[210,180,138,255],
 'base_panels':[229,207,173,255],
}

# Tessellate real STEP BReps with acceptable screen quality, preserve each part as separate named GLB node.
def to_mesh(shape,group):
    v,f = shape.tessellate(1.4, 0.25)
    v=np.asarray([(p.x,p.y,p.z) for p in v],dtype=np.float64)
    f=np.asarray(f,dtype=np.int64)
    mesh=trimesh.Trimesh(vertices=v,faces=f,process=False)
    # Determine orientation; OCC faces generally have correct orientation, but normals not structural.
    color=COLORS[group]
    mesh.visual.vertex_colors=np.tile(color,(len(mesh.vertices),1))
    return mesh

meshes=[]
for i,p in enumerate(parts):
    m=to_mesh(p['shape'],p['group'])
    meshes.append(m)

# viewer files: prototype with 3 sides only; future complete 4 sides with an indicative mattress.
def create_glb(tag,include_future,add_mattress):
    scene=trimesh.Scene()
    cnt=0
    for p,m in zip(parts,meshes):
        if p['when']=='four' and not include_future:continue
        scene.add_geometry(m,geom_name=p['name'],node_name=p['name'])
        cnt+=1
    if add_mattress:
        mattress=(trimesh.creation.box(extents=np.array(MATTRESS)))
        mattress.apply_translation((L/2,W/2,180.+150./2))
        mattress.visual.vertex_colors=np.tile([194,218,209,230],(len(mattress.vertices),1))
        scene.add_geometry(mattress,geom_name='MATTRESS_VISUAL_ONLY',node_name='MATTRESS_VISUAL_ONLY')
    out=HERE/f'CRIB_V068_{tag}_DESIGN_ONLY.glb'
    scene.export(str(out),file_type='glb')
    reload=trimesh.load(str(out),force='scene')
    assert len(reload.geometry)==cnt+int(add_mattress),(len(reload.geometry),cnt)
    bd=reload.bounds
    assert np.allclose(bd[0],[-70.,-70.,0.],atol=0.01),bd
    assert np.allclose(bd[1],[L+70,W+70,TOTAL_HEIGHT],atol=0.01),bd
    return out,cnt

three_glb,nthree=create_glb('THREE_SIDES_PROTOTYPE',False,False)
four_glb,nfour=create_glb('FOUR_SIDES_FUTURE',True,True)

# Export editable exchange CAD STEP for both conceptual configurations; no mattress in STEP.
def create_step(tag,include_future):
    items=[p['shape'] for p in parts if include_future or p['when']!='four']
    cmp=cq.Compound.makeCompound(items)
    fp=HERE/f'CRIB_V068_{tag}_DESIGN_ONLY.step'
    cq.exporters.export(cmp,str(fp))
    back=cq.importers.importStep(str(fp)).solids().vals()
    assert len(back)==len(items),(len(back),len(items))
    return fp,len(items)

three_step,nthree_step=create_step('THREE_SIDES_PROTOTYPE',False)
four_step,nfour_step=create_step('FOUR_SIDES_FUTURE',True)

# Scope-specific AABB geometry intersection checks for only newly added vs base and among other new plates;
# contact (zero-volume shared boundary) is fine. Honest: AABB is a prefilter; perform BREP if overlap.
clashes=[]
for i,p in enumerate(parts):
    a=p['shape'].BoundingBox()
    for j in range(i+1,len(parts)):
        q=parts[j];b=q['shape'].BoundingBox()
        if min(a.xmax,b.xmax)-max(a.xmin,b.xmin)<=1e-6:continue
        if min(a.ymax,b.ymax)-max(a.ymin,b.ymin)<=1e-6:continue
        if min(a.zmax,b.zmax)-max(a.zmin,b.zmin)<=1e-6:continue
        v=p['shape'].intersect(q['shape']).Volume()
        if v>0.05:clashes.append((p['name'],q['name'],round(v,3)))

# Static preview rendered with matplotlib 3D box faces: show overall layout while avoiding CAD visualization dependence.
# Render representative solids excluding split skins' segmentation as separate fully shaded faces.
def cuboid_faces(bounds):
    x0,x1,y0,y1,z0,z1=bounds
    v=np.array([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],
                [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]])
    return [v[i] for i in [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]]

def preview(ax,show_front=False):
    ax.set_proj_type('persp')
    # For speed and clarity draw parts grouped by layer; first show base blocks then slats/posts/walls.
    order=['base_shell','base_ribs','base_panels','posts','slats','walls']
    for group in order:
        for p in parts:
            if p['group']!=group:continue
            if p['when']=='four' and not show_front:continue
            b=p['shape'].BoundingBox()
            surfaces=cuboid_faces((b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax))
            color=np.array(COLORS[group][:3])/255
            faces=[tuple(np.clip(color*f,0,1)) for f in [0.86,1.04,0.94,0.90,0.99,0.79]]
            ax.add_collection3d(Poly3DCollection(surfaces,facecolors=faces,
                                edgecolors=(0.37,0.29,0.2,0.4),linewidths=.13))
    if show_front:
        b=(2.,1202.,2.,602.,180.,330.)
        ax.add_collection3d(Poly3DCollection(cuboid_faces(b),facecolors=(0.73,0.84,0.78,0.17),
                            edgecolors=(0.25,0.44,0.39,.3),linewidths=.2))
    ax.set_xlim(-220,1400);ax.set_ylim(-210,870);ax.set_zlim(0,950)
    ax.set_box_aspect((1344,744,880),zoom=0.78)
    ax.view_init(elev=23,azim=55)
    ax.set_axis_off()

fig=plt.figure(figsize=(16,8.5),facecolor='#f8f7f4')
for i,is_four in enumerate([False,True],start=1):
    ax=fig.add_subplot(1,2,i,projection='3d')
    preview(ax,is_four)
    ax.set_title('3 SIDES  |  UNOCUPIED PROTOTYPE' if not is_four else '4 SIDES  |  FUTURE CONCEPT',
                 fontsize=14,fontweight='bold',color='#293c34',pad=10)
fig.text(0.5,.06,'CRIB V0.6.8 • 1200×600×150 mm mattress • 880 mm total height • DESIGN ONLY — NOT FOR INFANT USE',
         ha='center',fontsize=10,color='#4c554e')
fig.tight_layout(rect=[0,.055,1,1])
preview_path=HERE/'CRIB_V068_3D_PREVIEW.png'
fig.savefig(preview_path,dpi=165,facecolor=fig.get_facecolor(),bbox_inches='tight')
plt.close(fig)

# BOM summary and integrity report
from collections import Counter
c3=Counter(p['group'] for p in parts if p['when']!='four')
c4=Counter(p['group'] for p in parts)
quality={
 'product':'CRIB-01 V0.6.8 3D VISUAL ASSEMBLY',
 'status':'DESIGN_ONLY / NO_CUT / NO_INFANT_USE / INDEPENDENT_QA_PENDING',
 'frozen':{'mattress_mm':MATTRESS,'overall_height_mm':TOTAL_HEIGHT,'closed_sides_for_possible_future_sleep':4,'unoccupied_prototype_sides':3},
 'provisional':{'bay_mm':[L,W],'posts_mm':[POST,POST,TOTAL_HEIGHT], 'rail_heights_mm':{'top':TOP_RAIL,'lower':LOW_RAIL}, 'plywood_nominal_mm':T},
 'base_step_reused':str(BASE_STEP),'base_component_solids_reused':len(base_shapes),
 'three_sides':{'cad_part_solids':nthree_step,'glb_wood_nodes':nthree,'per_group':dict(c3),'mattress_view':False},
 'four_sides':{'cad_part_solids':nfour_step,'glb_wood_nodes':nfour,'per_group':dict(c4),'mattress_view':True},
 'numerical':{'long_slats':LONG_SLATS,'short_slats_each':SHORT_SLATS,
              'long_nominal_gap_mm':round((L-LONG_SLATS*SLAT_W)/(LONG_SLATS+1),4),
              'short_nominal_gap_mm':round((W-SHORT_SLATS*SLAT_W)/(SHORT_SLATS+1),4),
              'rail_top_to_mattress_top_mm':530,
              'overall_envelope_mm':OUTER},
 'intersection_pairs':clashes,
 'open_issues':['IF-06A base cassette to walls/posts: no engineered load-bearing anchor','IF-06C panels retention not designed',
  'IF-06D long-rail and base bearer butt seams do not transmit verified loads',
  'IF-07 fourth wall permanent fixing not designed',
  'IF-05 slat-to-rail fastening/retention not modeled',
  'IF-09 child sleep safety, measured mattress fit, standards and G3 physical tests NOT_RUN'],
 'verification_done':['STEP existing cassette imported: 33 actual BRep solids','Two STEP conceptual assemblies exported and reimported with matching solid counts',
  'Two GLB files exported and reimported with matching node counts and bounding extents',
  'Scoped static BRep intersection check (not engineering strength validation)'],
 'verification_not_done':['Full 3D fastener and insert-path simulation','Physical fit/kerf and glue tests',
  'Structural/deflection/tipping/cot-standard assessment','Independent QA'],
}
(HERE/'CRIB_V068_CHECKS.json').write_text(json.dumps(quality,ensure_ascii=False,indent=2),encoding='utf-8')
report=f'''# CRIB-01 V0.6.8 | מודל תלת־ממדי של המיטה — להמחשה הנדסית בלבד

**מצב:** DESIGN_ONLY / NO_CUT / NO_INFANT_USE / INDEPENDENT_QA_PENDING.

## מה בוצע
- יובאו **33 חלקי STEP אמיתיים** של קסטת בסיס המזרן V0.6.7, ללא שינוי גיאומטרי.
- נבנה מודל 3D למעטפת המיטה עם ארבעה עמודים חלולים, שתי דפנות קצרות, דופן ארוכה קבועה ודופן ארוכה עתידית.
- הופקו שני קובצי GLB ושני קובצי STEP נפרדים: אב־טיפוס שלוש דפנות ({nthree_step} גופים) ומיטת ארבע דפנות ({nfour_step} גופים).
- מודל ארבע הדפנות כולל **ב־GLB בלבד** גוף חזותי של המזרן. קובצי STEP כוללים עץ בלבד.

## נתונים שנשמרו
- מזרן שנמדד בפועל 1200 × 600 × 150 מ״מ.
- גובה כולל 880 מ״מ.
- ארבע דפנות סגורות הן תנאי לתצורת שינה עתידית; שלוש דפנות משמשות **רק לאב־טיפוס ללא תינוק**.

## הנחות לא מאושרות
- חלל פנימי 1204×604 מ״מ — מרווח 2 מ״מ לכל צד.
- עמודים 70×70, דפנות בירץ׳ 10 מ״מ, ראש מעקה 860 מ״מ, מסילה תחתונה z=100..180.
- קורות חלולות, פאות ארוכות מפוצלות עם תפרים מדורגים, ללא תכן מחבר קורה נושא עומס.
- הסורגים מצוירים בגודל ומיקום נומינלי בלבד. מגרעות, חיבורי אצבע, נעילה ותפרי הדבקה לא מודלו.

## בדיקות ממוחשבות שבוצעו
- נפתח קובץ STEP קודם ונמצאו בדיוק 33 גופים.
- שתי גרסאות STEP נבנו ונקראו מחדש עם ספירות של {nthree_step} ו־{nfour_step} גופים.
- שני קובצי GLB נפתחו מחדש ונמצאו {nthree} ו־{nfour} גופי עץ, ומעטפת חוץ 1344×744×880 מ״מ.
- בדיקת החדירה הסטטית בין הגופים זיהתה {len(clashes)} זוגות עם חפיפה חיובית: {clashes[:8]}.

**לא בוצע**: תכן חיבור אמיתי בין הבסיס לדפנות, תכנון חיבור הדופן הרביעית, אימות חוזק, פיצויי kerf, בדיקת תקינה או QA עצמאי. אלה חסמי G2–G4.

## שימוש נכון בקבצים
- GLB: צפייה תלת־ממדית בדפדפן או תוכנת צפייה, כולל צבעי חלקים.
- STEP: עיון במכלול גיאומטרי בתוכנות CAD, **לא מקור הנדסי מאושר לייצור**.
- אין לחתוך או לייצר מיטה לשימוש תינוק על סמך קבצים אלה.
'''
(HERE/'CRIB_V068_REPORT_HE.md').write_text(report,encoding='utf-8')

zpath=Path('/mnt/data/CRIB_V068_FULL_3D_DESIGN_ONLY.zip')
with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in HERE.glob('CRIB_V068*'):
        if p.suffix.lower() in {'.glb','.step','.png','.json','.md'}:
            z.write(p,arcname=p.name)
    z.write(Path(__file__),arcname='build_full_crib_3d.py')
print('OUTPUTS')
for f in [three_glb,four_glb,three_step,four_step,preview_path,zpath]:print(f,Path(f).stat().st_size)
print('WOOD NODES',nthree,nfour,'COLLISIONS',len(clashes),clashes[:5])