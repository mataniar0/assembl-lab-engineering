#!/usr/bin/env python3
"""PST-230 V2 optimized 850x440 sheet nesting: 15 six-mm parts + single disc overflow.
Source: prior PST-230 CAD-derived individual DXF/SVG (fixed source geometry).
This script can reproduce placements and sheet SVG/DXF without changing CAD.
"""
import os,pathlib,math,json,shutil,zipfile,csv,itertools,hashlib,xml.etree.ElementTree as ET,sys
import ezdxf
from shapely.geometry import Polygon,MultiPolygon
from shapely import affinity
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PP
SCRIPT_DIR=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path(os.environ.get('PST230_SRC', str(SCRIPT_DIR.parent if SCRIPT_DIR.name=='source' else pathlib.Path('/mnt/data/PST_230_SOURCES'))))
OUT=pathlib.Path(os.environ.get('PST230_OUT','/mnt/data/PST230_V2_850_RELEASE'))
DATA=SCRIPT_DIR
OUT.mkdir(parents=True,exist_ok=True)
for sub in ['nesting','preview','qa','cut_parts_svg','cut_parts_dxf','cad','source','optional_scrap_250x250']:(OUT/sub).mkdir(exist_ok=True)
W,H=440.,850.;GAP=1.15;MARGIN=5.;

def load_from_dxf(name):
    file=SRC/'cut_parts_dxf'/(name+'.dxf')
    if not file.exists():return load_from_svg(name)
    doc=ezdxf.readfile(file)
    polys=[]
    for e in doc.modelspace().query('LWPOLYLINE'):
        pts=[(p[0],p[1]) for p in e.get_points()]
        if pts[0]!=pts[-1]:pts.append(pts[0])
        p=Polygon(pts)
        if abs(p.area)>1e-6:polys.append(p)
    polys.sort(key=lambda p:p.area,reverse=True)
    shell=polys[0];holes=[list(p.exterior.coords) for p in polys[1:] if shell.contains(p.representative_point())]
    g=Polygon(shell.exterior.coords,holes)
    assert g.is_valid
    return affinity.translate(g,-g.bounds[0],-g.bounds[1])

def load_from_svg(name):
    xml=ET.parse(SRC/'cut_parts_svg'/(name+'.svg')).getroot()
    ns='{http://www.w3.org/2000/svg}'
    ps=[]
    for child in xml.findall('.//'+ns+'polygon'):
        pts=[tuple(map(float,coord.split(','))) for coord in child.attrib['points'].split()]
        ps.append((child.attrib.get('class',''),pts))
    shell=next(p for cls,p in ps if cls=='CUT_OUTER');holes=[p for cls,p in ps if cls=='CUT_INNER']
    g=Polygon(shell,holes)
    assert g.is_valid
    return affinity.translate(g,-g.bounds[0],-g.bounds[1])

names6=[f'LEG_{i}_{a}_6MM' for i in range(1,4) for a in 'AB']+['TOP_DISC_D230_RIM_TABS_ONLY_6MM','BOTTOM_DISC_D230_6MM','LOWER_TRIANGLE_ONE_PIECE_6MM','CENTRAL_FLAT_6MM_SPIDER']+[f'CORE_RIB_{i:02d}_6MM' for i in range(1,7)]
original={n:load_from_dxf(n) for n in names6}
tri=original['LOWER_TRIANGLE_ONE_PIECE_6MM'];sp=original['CENTRAL_FLAT_6MM_SPIDER']
hole=Polygon(tri.interiors[0])
sp_in=affinity.translate(sp,hole.centroid.x-sp.centroid.x,hole.centroid.y-sp.centroid.y)
assert hole.contains(sp_in) and tri.distance(sp_in)>GAP
cluster=MultiPolygon([tri,sp_in])

# Locked placement manifest: source shape rotated around (0,0) then aligned by
# buffered part bounds (+0.7mm) in the 2mm discretized search frame, with 2mm inset.
base=json.loads((DATA/'one_disc_raster_solved.json').read_text())
placed={};manifest=[]
def rigid(n,angle,dx,dy,sheet):
    g=affinity.translate(affinity.rotate(original[n],angle,origin=(0,0)),dx,dy)
    placed[n]=g
    manifest.append(dict(sheet=sheet,name=n,angle_deg=angle,x_translation_mm=dx,y_translation_mm=dy))

for n,z in base.items():
    angle=z['angle'];p=cluster if n=='TRI_CLUSTER' else original[n]
    pb=affinity.rotate(p.buffer(.7),angle,origin=(0,0)).bounds
    dx=z['x']+2-pb[0];dy=z['y']+2-pb[1]
    if n=='TRI_CLUSTER':
        rigid('LOWER_TRIANGLE_ONE_PIECE_6MM',angle,dx,dy,'BIRCH6_S01_440x850')
        # the spider is translated within triangle hole BEFORE rotating cluster
        placed['CENTRAL_FLAT_6MM_SPIDER']=affinity.translate(affinity.rotate(sp_in,angle,origin=(0,0)),dx,dy)
        manifest.append(dict(sheet='BIRCH6_S01_440x850',name='CENTRAL_FLAT_6MM_SPIDER',angle_deg=angle,x_translation_mm=dx,y_translation_mm=dy,pre_translate_to_triangle_hole_centroid=True))
    else:rigid(n,angle,dx,dy,'BIRCH6_S01_440x850')

# Locked independently tested positions for six small ribs.
for i,ang,x,y in [(1,80,7,217),(2,20,7,757),(3,100,7,300),(4,200,82,765),(5,10,162,773),(6,110,173,611)]:
    name=f'CORE_RIB_{i:02d}_6MM'
    p=affinity.rotate(original[name],ang,origin=(0,0));b=p.bounds
    rigid(name,ang,x+1.5-b[0],y+1.5-b[1],'BIRCH6_S01_440x850')

# Single overflow disc alone on second birch6 board.
rigid('BOTTOM_DISC_D230_6MM',0,105,310,'BIRCH6_S02_440x850')
assert len(placed)==16 and set(placed)==set(names6)
sheet1=[n for n in names6 if n!='BOTTOM_DISC_D230_6MM']
sheet2=['BOTTOM_DISC_D230_6MM']
assert len(sheet1)==15 and len(sheet2)==1

# Re-export by original contours; no board-cut rectangle or scaling.
def write_sheet(stem,names,w=W,h=H,subdir='nesting'):
    file_svg=OUT/subdir/(stem+'.svg');file_dxf=OUT/subdir/(stem+'.dxf')
    doc=ezdxf.new('R2010');doc.header['$INSUNITS']=4
    for layer in ('CUT_OUTER','CUT_INNER','CUT_KERF_LINE'):doc.layers.add(layer,color=7)
    ms=doc.modelspace()
    lines=['<?xml version="1.0" encoding="UTF-8"?>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.5f}mm" height="{h:.5f}mm" viewBox="0 0 {w:.5f} {h:.5f}">','<g fill="none" stroke="black" stroke-width="0.12">']
    for n in names:
        p=placed[n]
        lines.append(f'<g id="{n}">')
        for layer,ring in [('CUT_OUTER',p.exterior)]+[('CUT_INNER',r) for r in p.interiors]:
            points=list(ring.coords)[:-1]
            ms.add_lwpolyline(points,close=True,dxfattribs={'layer':layer})
            lines.append('<polygon class="'+layer+'" points="'+' '.join(f'{x:.5f},{y:.5f}' for x,y in points)+'"/>')
        lines.append('</g>')
    lines.append('</g></svg>')
    file_svg.write_text('\n'.join(lines),encoding='utf8');doc.saveas(file_dxf)
    return file_svg,file_dxf

write_sheet('BIRCH6_S01_440x850',sheet1)
write_sheet('BIRCH6_S02_440x850',sheet2)
# Optional single 6mm plate in a small 250×250mm scrap instead of using a whole 850×440mm board.
original_overflow=placed['BOTTOM_DISC_D230_6MM']
placed['BOTTOM_DISC_D230_6MM']=affinity.translate(original['BOTTOM_DISC_D230_6MM'],10,10)
write_sheet('BOTTOM_DISC_D230_ON_250x250',sheet2,w=250,h=250,subdir='optional_scrap_250x250')
assert abs(placed['BOTTOM_DISC_D230_6MM'].bounds[0]-10)<1e-6
assert abs(250-placed['BOTTOM_DISC_D230_6MM'].bounds[2]-10)<1e-6
placed['BOTTOM_DISC_D230_6MM']=original_overflow
for ext in ('svg','dxf'):
    shutil.copy2(SRC/'nesting'/('BIRCH4_S01_440x850.'+ext),OUT/'nesting'/('BIRCH4_S01_440x850.'+ext))
for n in names6+[f'RIM_{i:02d}_BIRCH4_UPPER_LOWER_TABS' for i in range(1,7)]:
    for ext in ('svg','dxf'):
        shutil.copy2(SRC/('cut_parts_'+ext)/(n+'.'+ext),OUT/('cut_parts_'+ext)/(n+'.'+ext))
for p in (SRC/'cad').glob('PST_230_*'):
    shutil.copy2(p,OUT/'cad'/p.name)
for p in [SRC/'build_pst_230.py',SRC/'export_nest_pst230.py']:
    shutil.copy2(p,OUT/'source'/p.name)
shutil.copy2(__file__,OUT/'source'/'repack_pst230_v2.py')
shutil.copy2(SRC/'BOM.csv',OUT/'BOM.csv')
with (OUT/'PLACEMENTS_V2.csv').open('w',newline='',encoding='utf8') as f:
    fieldnames=['sheet','name','angle_deg','x_translation_mm','y_translation_mm','pre_translate_to_triangle_hole_centroid'];w=csv.DictWriter(f,fieldnames=fieldnames)
    w.writeheader();w.writerows(manifest)
shutil.copy2(DATA/'one_disc_raster_solved.json',OUT/'source'/'one_disc_raster_solved.json')

# Validate drawing parity, actual geometry, and no missed parts.
shnames={"BIRCH6_S01_440x850":sheet1,"BIRCH6_S02_440x850":sheet2,"BIRCH4_S01_440x850":[f'RIM_{i:02d}_BIRCH4_UPPER_LOWER_TABS' for i in range(1,7)]}
qa={'project':'PST-230 PLANT STAND','version':'V2-850-15PLUS1','status':'DESIGN_ONLY / GEOMETRIC_NESTING_PASS / G4_PHYSICAL_HOLD','board_mm':[440,850], 'minimum_required_cut_gap_mm':GAP,'required_margin_mm':MARGIN,'sheets':[], 'cad_geometry_modified':False,'original_22_individual_parts_unchanged':True}
allids=[];total_contours=0;total_kerfs=0
for stem,names in shnames.items():
    doc=ezdxf.readfile(OUT/'nesting'/(stem+'.dxf'))
    entities=list(doc.modelspace())
    outer=sum(e.dxftype()=='LWPOLYLINE' and e.dxf.layer=='CUT_OUTER' for e in entities)
    inner=sum(e.dxftype()=='LWPOLYLINE' and e.dxf.layer=='CUT_INNER' for e in entities)
    kerfs=sum(e.dxftype()=='LINE' and e.dxf.layer=='CUT_KERF_LINE' for e in entities)
    assert all(e.dxf.layer in ('CUT_OUTER','CUT_INNER','CUT_KERF_LINE') for e in entities)
    assert all(e.closed for e in entities if e.dxftype()=='LWPOLYLINE')
    assert outer==len(names)
    svg_root=ET.parse(OUT/'nesting'/(stem+'.svg')).getroot();ns='{http://www.w3.org/2000/svg}'
    assert len(svg_root.findall('.//'+ns+'g[@id]'))==len(names)
    assert len(svg_root.findall('.//'+ns+'polygon'))==outer+inner
    assert len(svg_root.findall('.//'+ns+'path'))==kerfs
    if stem.startswith('BIRCH6'):
        mm=[placed[n] for n in names]
        gaps=[(a.distance(b),x,y) for (x,a),(y,b) in itertools.combinations([(n,placed[n]) for n in names],2)]
        min_gap=min((x[0] for x in gaps),default=None)
        margin=min(min(p.bounds[0],p.bounds[1],W-p.bounds[2],H-p.bounds[3]) for p in mm)
        assert margin>=MARGIN-1e-5
        if min_gap is not None:assert min_gap>=GAP-1e-4
        # entity count source parity
        assert outer+inner==sum(1+len(placed[n].interiors) for n in names)
        assert kerfs==0
        source_geom_area=sum(original[n].area for n in names)
        moved_geom_area=sum(placed[n].area for n in names)
        assert abs(source_geom_area-moved_geom_area)<.001
    else:
        # from independently approved exact source board copied byte-for-byte
        min_gap=7.;margin=5.
        for ext in ('svg','dxf'):
            assert hashlib.sha256((SRC/'nesting'/(stem+'.'+ext)).read_bytes()).digest()==hashlib.sha256((OUT/'nesting'/(stem+'.'+ext)).read_bytes()).digest()
    total_contours+=outer+inner;total_kerfs+=kerfs;allids+=names
    qa['sheets'].append(dict(stem=stem,material='birch 4mm' if stem.startswith('BIRCH4') else 'birch 6mm',parts=len(names),names=names,min_cut_clearance_mm=min_gap,minimum_stock_margin_mm=margin,closed_contours=outer+inner,bend_strokes=kerfs))
assert len(allids)==len(set(allids))==22
assert total_contours==59 and total_kerfs==252,(total_contours,total_kerfs)
qa.update(parts=22,closed_cut_contours=total_contours,single_line_bends=total_kerfs,part_counts_by_sheet=[15,1,6],full_6mm_one_sheet_validated=False,optional_overflow_scrap_board_mm=[250,250],optional_overflow_scrap_stock_margin_mm=10.0)
(OUT/'qa'/'NESTING_QA_V2.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))

# Render previews.
color={'LEG':'#9ccbe5','CORE':'#e5b284','TOP':'#9fb9e8','BOTTOM':'#a5c4dd','LOWER':'#c8aadd','CENTRAL':'#ddcfa2','RIM':'#bddfbd'}
fig,axs=plt.subplots(1,3,figsize=(13,10),layout='constrained')
for ax,(stem,names) in zip(axs,shnames.items()):
    ax.set_xlim(0,W);ax.set_ylim(H,0);ax.set_aspect('equal');ax.set_title(f'{stem}\n{len(names)} parts',fontsize=10)
    ax.add_patch(plt.Rectangle((0,0),W,H,fill=False,lw=1.5,color='black'))
    if stem.startswith('BIRCH6'):
        for n in names:
            p=placed[n]
            label=next((k for k in color if n.startswith(k)),'RIM')
            ax.add_patch(PP(list(p.exterior.coords),facecolor=color[label],alpha=.85,edgecolor='#202020',linewidth=.55))
            for h in p.interiors:
                ax.add_patch(PP(list(h.coords),facecolor='white',edgecolor='#202020',linewidth=.5))
            point=p.representative_point();ax.text(point.x,point.y,n.replace('_6MM','').replace('D230_RIM_TABS_ONLY','D230').replace('LOWER_TRIANGLE_ONE_PIECE','TRIANGLE'),fontsize=5,ha='center')
    else:
        doc=ezdxf.readfile(OUT/'nesting'/(stem+'.dxf'))
        for entity in doc.modelspace():
            if entity.dxftype()=='LWPOLYLINE' and entity.dxf.layer=='CUT_OUTER':
                p=Polygon([(v[0],v[1]) for v in entity.get_points()])
                ax.add_patch(PP(list(p.exterior.coords),facecolor='#bddfbd',edgecolor='black',alpha=.7,linewidth=.55))
            elif entity.dxftype()=='LINE' and entity.dxf.layer=='CUT_KERF_LINE':
                a,b=entity.dxf.start,entity.dxf.end
                ax.plot([a.x,b.x],[a.y,b.y],linewidth=.18,color='#202020')
    ax.grid(alpha=.12);ax.set_xticks([0,220,440]);ax.set_yticks([0,200,400,600,850])
fig.savefig(OUT/'preview'/'PST230_V2_ALL_3_SHEETS.png',dpi=170);plt.close(fig)

readme=f'''# מעמד לעציץ PST-230 — V2 / אופטימיזציית נסטינג 15+1

**סטטוס: DIGITAL NESTING PASS / DESIGN_ONLY — לא אישור ייצור.**

הפרויקט מבוסס על אותו מודל CAD של PST-230 V1: קוטר פלטות 230 מ״מ, גובה 550 מ״מ, בירץ' 6 מ״מ ושלושה לוחות בגודל 850×440 מ״מ.

## שיפור V2

- לוח 6 מ״מ S01 כולל **15 חלקים**: שש רגליים, משולש, חלק עגול מרכזי, שש צלעות חיזוק ופלטה עליונה.
- לוח 6 מ״מ S02 כולל **רק פלטה תחתונה אחת**. אפשר לחתוך אותה גם משארית בירץ׳ 6 מ״מ בגודל **250×250 מ״מ**, באמצעות הקבצים הנפרדים בתיקייה `optional_scrap_250x250` (שוליים 10 מ״מ). חלופה זו מחליפה את לוח S02, ולא נחתכת בנוסף אליו.
- לוח 4 מ״מ S01 מכיל 6 מקטעי מעטפת, ללא כל שינוי.
- המטרה להכניס **את כל 16 חלקי ה־6 מ״מ ללוח אחד לא אומתה**. ניסיונות האריזה הותירו חפיפות; לא הוכח חוסר אפשרות מתמטי.
- שאר הגיאומטריה, החיבורים ו־CAD STEP/GLB נותרו כפי שהיו.

## QA גיאומטרי

- 22 חלקים בדיוק. 59 קווי מתאר סגורים ו־252 קווי כיפוף.
- S01 מרווח מינימלי {qa['sheets'][0]['min_cut_clearance_mm']:.3f} מ״מ, שוליים {qa['sheets'][0]['minimum_stock_margin_mm']:.3f} מ״מ.
- S02 מרווח בין חלקים: לא חל (חלק אחד); שוליים {qa['sheets'][1]['minimum_stock_margin_mm']:.3f} מ״מ.
- S03 מרווח מינימלי 7.0 מ״מ, שוליים ≥5 מ״מ.
- DXF/SVG נפתחו מחדש, יחידות DXF מ״מ, ללא מסגרות לוח בשכבת חיתוך.
- כל 22 קובצי החלקים העצמאיים זהים למקור; אין שינוי ב־CAD המבני.

**טרם נבדקו פיזית:** Kerf, עובי חומר בפועל, התאמת צירים/חיבורים, כיפוף מעטפת, סגירתה וחוזקה, הדבקה, יציבות ועומסי עציץ רטוב. לפני חיתוך, יש לכייל את המכונה ולבדוק שמידות הלוח תואמות.

## שחזור


def run: first run `python build_pst_230.py` and `python export_nest_pst230.py` to generate source DXF, then `python repack_pst230_v2.py` from this release's `source` directory (with `PST230_SRC`, `PST230_OUT` environment variables set to proper directories). Placement seed file `one_disc_raster_solved.json` accompanies the repack script.
'''
(OUT/'README_HE.md').write_text(readme,encoding='utf8')

# Create 2 zip packages + integrity tests.
def makezip(name,select):
    path=pathlib.Path('/mnt/data')/name
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for fn in select:z.write(fn,arcname=str(fn.relative_to(OUT)))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
    return {'name':path.name,'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'files':len(select)}
cutfiles=[p for p in OUT.rglob('*') if p.is_file() and ('cad' not in p.parts and 'source' not in p.parts)]
allfiles=[p for p in OUT.rglob('*') if p.is_file()]
archives=[makezip('PST230_V2_850_CUT_15PLUS1.zip',cutfiles),makezip('PST230_V2_850_FULL_CAD_15PLUS1.zip',allfiles)]
(OUT/'qa'/'PACKAGES_SHA256.json').write_text(json.dumps(archives,indent=2))
print(json.dumps({'qa':qa,'archives':archives},ensure_ascii=False,indent=2),flush=True)