#!/usr/bin/env python3
"""PST-310 V8-850 2x6mm + 1x4mm nesting: shape-preserving transformations.
Source: existing V8 22 separate DXF part geometry, unchanged.
No kerf compensation; DESIGN_ONLY until real material trials.
"""
from pathlib import Path
import math, itertools, json, csv, hashlib, zipfile, shutil
from xml.etree import ElementTree as ET
from shapely.geometry import Polygon, LineString, box
from shapely.affinity import translate, rotate
from shapely.ops import unary_union
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPoly

SRC=Path('/mnt/data/PST_310_V8_WORK')
DST=Path('/mnt/data/PST_310_V8_850_RELEASE')
W=440.; H=850.; MARGIN=5.; MIN_GAP=1.
for folder in ['nesting', 'individual/SVG', 'individual/DXF', 'preview', 'cad', 'qa', 'source']:
    (DST/folder).mkdir(parents=True,exist_ok=True)

# raw source cut geometry (original independent V8 production-design part DXFs)
source={}
for path in sorted((SRC/'dxf').glob('*.dxf')):
    doc=ezdxf.readfile(path)
    outer=[]; inner=[]; kerf=[]
    for e in doc.modelspace():
        if e.dxftype()=='LWPOLYLINE':
            pts=list(e.get_points('xy'))
            if e.dxf.layer=='CUT_OUTER':outer.append(pts)
            elif e.dxf.layer=='CUT_INNER':inner.append(pts)
            else:raise AssertionError((path,e.dxf.layer))
        elif e.dxftype()=='LINE' and e.dxf.layer=='CUT_KERF_LINE':
            kerf.append(LineString([(e.dxf.start.x,e.dxf.start.y),(e.dxf.end.x,e.dxf.end.y)]))
        else:raise AssertionError((path,e.dxftype()))
    assert len(outer)==1, (path, len(outer))
    polygon=Polygon(outer[0],inner)
    assert polygon.is_valid and polygon.area>1,(path,polygon)
    b=polygon.bounds
    source[path.stem]=(translate(polygon,-b[0],-b[1]),[translate(g,-b[0],-b[1]) for g in kerf])
assert len(source)==22

# Placement coordinates (mm, x right, y down; angle degrees ccw in DXF plane)
# First sheet spatial optimization; triangle and spider move together but remain two distinct cut parts.
S1={
 'LEG_1_A_6MM': (275.7742068993378,316.0317723086005,-1.7564252259181519),
 'LEG_1_B_6MM': (129.74977269443423,5.0,8.930940300947295),
 'LEG_3_A_6MM': (22.14955746713673,5.0,14.3189319385238),
 'LEG_3_B_6MM': (178.8348642624278,83.59955407084303,9.895817335305818),
 'TRIANGLE_CLUSTER': (5.0,477.37451138953844,-3.289851011193246)
}
S2={
 'BOTTOM_DISC_D310_6MM': (5.0,5.0,58.27908989910341),
 'TOP_DISC_D310_RIM_TABS_ONLY_6MM': (13.13516882604322,481.98537659124173,26.07832988640382),
 'LEG_2_A_6MM': (298.9691291566197,5.0,172.69728273360934),
 'LEG_2_B_6MM': (343.424547011963,209.51439761582316,166.2805994134617),
 'CORE_RIB_01_6MM': (228.75704962971238,344.3595847746411,99.59288932185899),
 'CORE_RIB_02_6MM': (5.0,738.0874193200113,41.70536076844433),
 'CORE_RIB_03_6MM': (198.31558842041588,764.7545001332915,337.77944161770347),
 'CORE_RIB_04_6MM': (330.47883799597366,737.7664518507685,94.00111873471933),
 'CORE_RIB_05_6MM': (5.0,336.58248560890075,29.535661464088747),
 'CORE_RIB_06_6MM': (126.72078576644476,338.87582133622516,126.86423776887546)
}

def rigid_transform(shape, placement, reference_shape=None):
    """Rotate part and cluster about world origin; then shift so rotated reference's bbox min==(x,y)."""
    x,y,angle=placement
    reference=reference_shape if reference_shape is not None else shape
    ref_rot=rotate(reference,angle,origin=(0,0))
    b=ref_rot.bounds
    delta=(x-b[0],y-b[1])
    result=translate(rotate(shape,angle,origin=(0,0)),*delta)
    return result,delta

def item(name, placement, reference=None, geom_override=None):
    p,lines=source[name]
    if geom_override is not None:p=geom_override
    g,delta=rigid_transform(p,placement,reference)
    return dict(id=name,geom=g,cutlines=[translate(rotate(ln,placement[2],origin=(0,0)),*delta) for ln in lines],rotation_deg=placement[2],translate_xy_mm=list(delta))

triangle, _=source['LOWER_TRIANGLE_ONE_PIECE_6MM']
spider, _=source['CENTRAL_FLAT_6MM_SPIDER']
assert len(triangle.interiors)==1
tri_hole=Polygon(triangle.interiors[0])
# IMPORTANT: centroid of triangular inner polygon, *not* center of bbox. Bbox-center caused cutting overlap in early preview.
shift=(tri_hole.centroid.x-spider.centroid.x,tri_hole.centroid.y-spider.centroid.y)
spider_centered=translate(spider,*shift)
assert spider_centered.within(tri_hole), f'centered spider overlap {spider_centered.difference(tri_hole).area}'
spider_hole_clearance=triangle.distance(spider_centered)
assert spider_hole_clearance>MIN_GAP

# Use same outer triangle as reference of both positions.
items1=[item(name, pos) for name,pos in S1.items() if name!='TRIANGLE_CLUSTER']
items1.append(item('LOWER_TRIANGLE_ONE_PIECE_6MM',S1['TRIANGLE_CLUSTER']))
items1.append(item('CENTRAL_FLAT_6MM_SPIDER',S1['TRIANGLE_CLUSTER'],reference=triangle,geom_override=spider_centered))
items2=[item(name,pos) for name,pos in S2.items()]
items4=[item(f'RIM_{i+1:02d}_BIRCH4_UPPER_LOWER_TABS',(5+(i%2)*166.22123,5+(i//2)*66.,0)) for i in range(6)]
sheets={
 'BIRCH6_S01_440x850':items1,
 'BIRCH6_S02_440x850':items2,
 'BIRCH4_S01_440x850':items4,
}
ids=[q['id'] for vs in sheets.values() for q in vs]
assert len(ids)==22 and len(set(ids))==22 and set(ids)==set(source)

QA={'project':'PST-310','release':'V8-850-OPT-3SHEETS','status':'DIGITAL_NESTING_PASS__PHYSICAL_HOLD','stock_width_mm':W,'stock_height_mm':H,'min_gap_required_mm':MIN_GAP,'min_stock_margin_mm':MARGIN,'parts':len(ids),'sheets':[], 'spider_to_triangle_min_clearance_mm':spider_hole_clearance,'contours':0,'single_line_bend_cuts':0,'source_part_hashes':{},'physical_tests':'NOT DONE — kerf, bending, glue, rim closure, wet-load stability and physical joinery fit pending'}

for name,items in sheets.items():
    minsep=float('inf'); pair=None; margin=float('inf')
    for it in items:
        p=it['geom']; assert p.is_valid, (name,it['id'])
        b=p.bounds
        mm=min(b[0],b[1],W-b[2],H-b[3]);margin=min(mm,margin)
        assert mm>=MARGIN-1e-6,(name,it['id'],'stock margin',mm)
        for ln in it['cutlines']:
            assert len(ln.coords)==2
            assert box(0,0,W,H).covers(ln),(name,it['id'],'kerf outside stock')
    for aa,bb in itertools.combinations(items,2):
        sep=aa['geom'].distance(bb['geom'])
        if sep<minsep: minsep,pair=sep,[aa['id'],bb['id']]
        assert sep>=MIN_GAP-1e-6,(name,'overlap or insufficient gap',pair,sep)
    contours=sum(1+len(it['geom'].interiors) for it in items)
    kerfs=sum(len(it['cutlines']) for it in items)
    QA['contours']+=contours;QA['single_line_bend_cuts']+=kerfs
    QA['sheets'].append({'file_stem':name,'thickness_mm':4 if 'BIRCH4' in name else 6,'number_of_parts':len(items), 'part_names':[it['id'] for it in items], 'min_part_gap_mm':round(minsep,6), 'min_gap_pair':pair, 'min_stock_margin_mm':round(margin,6),'closed_contours':contours,'single_line_kerfs':kerfs})
assert QA['single_line_bend_cuts']==348 and QA['contours']==59,(QA['contours'],QA['single_line_bend_cuts'])

# Sheet DXF/SVG exports: no board outline on CUT layers; each part as unaltered rotated/transposed polygon, 1:1 mm.
def export(items,stem):
    doc=ezdxf.new('R2010');doc.header['$INSUNITS']=4
    for layer in ('CUT_OUTER','CUT_INNER','CUT_KERF_LINE'):doc.layers.add(layer,color=7)
    ms=doc.modelspace()
    header=['<?xml version="1.0" encoding="UTF-8"?>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:g}mm" height="{H:g}mm" viewBox="0 0 {W:g} {H:g}">',f'<title>{stem} | PST-310 V8-850 | DESIGN_ONLY</title>','<g fill="none" stroke="black" stroke-width="0.12">']
    for it in items:
        p=it['geom'];header.append(f'<g id="{it["id"]}">')
        for layer,ring in [('CUT_OUTER',p.exterior),*[( 'CUT_INNER',r) for r in p.interiors]]:
            pts=list(ring.coords)[:-1]
            ms.add_lwpolyline(pts,close=True,dxfattribs={'layer':layer})
            coord=' '.join(f'{x:.5f},{y:.5f}' for x,y in pts)
            header.append(f'<polygon class="{layer}" points="{coord}"/>')
        for ln in it['cutlines']:
            a,b=ln.coords[0],ln.coords[-1]
            ms.add_line(a,b,dxfattribs={'layer':'CUT_KERF_LINE'})
            header.append(f'<path class="CUT_KERF_LINE" d="M {a[0]:.5f},{a[1]:.5f} L {b[0]:.5f},{b[1]:.5f}"/>')
        header.append('</g>')
    header.append('</g></svg>')
    dxf=DST/'nesting'/f'{stem}.dxf';svg=DST/'nesting'/f'{stem}.svg'
    doc.saveas(dxf);svg.write_text('\n'.join(header),encoding='utf8')

for stem,its in sheets.items():export(its,stem)

# Independent re-open DXF+SVG and compare source contour geometry modulo rigid placement.
for stem,its in sheets.items():
    doc=ezdxf.readfile(DST/'nesting'/f'{stem}.dxf')
    assert doc.header['$INSUNITS']==4
    ed=list(doc.modelspace())
    expected=sum(1+len(it['geom'].interiors)+len(it['cutlines']) for it in its)
    assert len(ed)==expected,(stem,len(ed),expected)
    pos=0
    for it in its:
        expected_rings=[('CUT_OUTER',it['geom'].exterior)]+[('CUT_INNER',r) for r in it['geom'].interiors]
        for layer,ring in expected_rings:
            e=ed[pos];pos+=1
            assert e.dxftype()=='LWPOLYLINE' and e.closed and e.dxf.layer==layer
            p1=list(e.get_points('xy'));p2=list(ring.coords)[:-1]
            assert len(p1)==len(p2)
            assert all(math.dist(a,b)<1e-7 for a,b in zip(p1,p2)),(stem,it['id'],'DXF geometry drift')
        for line in it['cutlines']:
            e=ed[pos];pos+=1
            assert e.dxftype()=='LINE' and e.dxf.layer=='CUT_KERF_LINE'
            assert math.dist((e.dxf.start.x,e.dxf.start.y),line.coords[0])<1e-7 and math.dist((e.dxf.end.x,e.dxf.end.y),line.coords[-1])<1e-7
    assert pos==len(ed)
    root=ET.parse(DST/'nesting'/f'{stem}.svg').getroot()
    ns='{http://www.w3.org/2000/svg}'
    groups=root.findall(f'.//{ns}g[@id]')
    assert len(groups)==len(its)
    for group,it in zip(groups,its):
        assert group.attrib['id']==it['id']
        polys=group.findall(f'{ns}polygon');paths=group.findall(f'{ns}path')
        assert len(polys)==1+len(it['geom'].interiors) and len(paths)==len(it['cutlines'])
        for g,ring in zip(polys,[it['geom'].exterior,*it['geom'].interiors]):
            got=[tuple(float(t) for t in pair.split(',')) for pair in g.attrib['points'].split()]
            assert len(got)==len(ring.coords)-1
            assert max(math.dist(a,b) for a,b in zip(got,ring.coords))<0.000008
    # One-to-one source part shape comparison after undoing transformed placement:
    for it in its:
        name=it['id']; g=it['geom']; orig=source[name][0]
        assert abs(orig.area-g.area)<1e-5,(stem,name,'area changed')
        assert abs(orig.length-g.length)<1e-5,(stem,name,'perimeter changed')

# Copy original individual V8 source geometry unchanged.
for f in (SRC/'svg').glob('*.svg'):
    shutil.copy2(f,DST/'individual/SVG'/f.name)
    QA['source_part_hashes'][f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
for f in (SRC/'dxf').glob('*.dxf'):
    shutil.copy2(f,DST/'individual/DXF'/f.name)
    QA['source_part_hashes'][f.name]=hashlib.sha256(f.read_bytes()).hexdigest()

# Include 3D CAD and reproducible model-generation scripts (2D nesting unchanged CAD model).
for f in (SRC/'cad').glob('*'):
    shutil.copy2(f,DST/'cad'/f.name)
for f in ['build_v8.py','build_v6_reference.py','build_pst_310_v4.py','verify_v8.py','make_nesting_v8.py']:
    shutil.copy2(SRC/f,DST/'source'/f)
shutil.copy2(Path(__file__),DST/'source'/Path(__file__).name)

# Preview the three boards.
fig,axes=plt.subplots(1,3,figsize=(13,10),layout='constrained')
for ax,(stem,its) in zip(axes,sheets.items()):
    ax.set_xlim(0,W);ax.set_ylim(H,0);ax.set_aspect('equal');ax.set_title(stem,fontsize=10)
    ax.add_patch(plt.Rectangle((0,0),W,H,fill=False,color='black',linewidth=.8))
    for i,it in enumerate(its):
        g=it['geom'];ax.add_patch(PatchPoly(list(g.exterior.coords),closed=True,facecolor=plt.cm.tab20(i),edgecolor='black',linewidth=.6,alpha=.54))
        for h in g.interiors:ax.add_patch(PatchPoly(list(h.coords),closed=True,facecolor='white',edgecolor='black',linewidth=.5))
        for cut in it['cutlines']:
            xx,yy=cut.xy;ax.plot(xx,yy,color='black',linewidth=.18)
        if stem!='BIRCH4_S01_440x850':
            cx,cy=g.representative_point().coords[0]
            label=it['id'].replace('_6MM','').replace('LOWER_TRIANGLE_ONE_PIECE','TRIANGLE').replace('CENTRAL_FLAT','CENTER').replace('_D310_RIM_TABS_ONLY','_D310')
            ax.text(cx,cy,label,fontsize=5,ha='center')
    ax.set_xticks([0,220,440]);ax.set_yticks([0,200,400,600,850]);ax.grid(alpha=.13)
fig.savefig(DST/'preview'/'ALL_3_SHEETS_850x440.png',dpi=170);plt.close(fig)

for stem,its in sheets.items():
    fig,ax=plt.subplots(figsize=(6,11))
    ax.set_xlim(0,W);ax.set_ylim(H,0);ax.set_aspect('equal');ax.set_title(stem)
    ax.add_patch(plt.Rectangle((0,0),W,H,fill=False,color='black',linewidth=.8))
    for i,it in enumerate(its):
        p=it['geom']
        ax.add_patch(PatchPoly(list(p.exterior.coords),facecolor=plt.cm.tab20(i),alpha=.5,edgecolor='black',linewidth=.6))
        for inner in p.interiors:ax.add_patch(PatchPoly(list(inner.coords),facecolor='white',edgecolor='black',linewidth=.5))
        for ln in it['cutlines']:
            xx,yy=ln.xy;ax.plot(xx,yy,color='black',linewidth=.18)
        if 'BIRCH6' in stem:
            x,y=p.representative_point().coords[0]
            ax.text(x,y,it['id'].replace('_6MM','').replace('LOWER_TRIANGLE_ONE_PIECE','TRIANGLE').replace('CENTRAL_FLAT','CENTER'),fontsize=6,ha='center')
    ax.grid(alpha=.15)
    fig.savefig(DST/'preview'/f'{stem}.png',dpi=160)
    plt.close(fig)

# Source/position manifest for repro and independent review.
with (DST/'PLACEMENTS.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['sheet','part','rotation_degrees','translation_x_mm','translation_y_mm'])
    for stem,its in sheets.items():
        for it in its:w.writerow([stem,it['id'],f'{it["rotation_deg"]:.9f}',*[f'{v:.9f}' for v in it['translate_xy_mm']]])
(DST/'qa'/'NESTING_QA.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2),encoding='utf8')
report=f'''# PST-310 V8-850 — תכנון דיגיטלי סופי לנסטינג (DESIGN_ONLY)

**גרסה:** `V8-850-OPT-3SHEETS` | **תאריך:** 2026-11-05 | **סטטוס:** G3 CAD + Nesting passed; G4 physical qualification pending.

## החלטה הנדסית
12 חריצי Finger Joints היקפיים בלבד בפלטה העליונה (חיבור למעטפת בירץ' 4 מ״מ). ללא 12 חריצים פנימיים בפלטה העליונה; 6 צלעות חיזוק פנימיות ללא לשוניות עליונות, ומודבקות למשטח התחתון. המידות לא שונו: Ø310 מ״מ, גובה מעמד 550 מ״מ, גובה קופסת ראש 60 מ״מ.

## נסטינג ייצור דיגיטלי
- 2 לוחות בירץ' 6 מ״מ במידה **850×440 מ״מ** (מוצגים בפורמט רוחב 440×גובה 850).
- לוח אחד בירץ' 4 מ״מ באותה מידה, כולל 6 מקטעי מעטפת.
- 22 חלקים בשיטת 1:1, כולם פעם אחת; **59 מסלולי חיתוך סגורים** ו־**348 קווי כיפוף single-line**.
- לוח 6מ״מ 1: 4 רגליים + משולש תחתון + חיבור מרכזי עגול במרכז המשולש.
- לוח 6מ״מ 2: 2 רגליים + שתי הפלטות Ø310 + 6 צלעות פנימיות.
- לוח 4מ״מ: 6 מקטעי מעטפת.
- שוליים של לפחות {MARGIN:g} מ״מ; מרווח בין חלקים לפחות {MIN_GAP:g} מ״מ. אין גבול לוח בלייר CUT. יחידות DXF מ״מ; אין פיצוי Kerf.

## בדיקות CAD ונסטינג
- קבצי ה־DXF וה־SVG של הלוחות הופקו מחדש ונפתחו מחדש. כל 22 החלקים המקוריים הועתקו ללא שינוי; נבדקו היקף/שטח שווים תחת סיבוב והזזה.
- לכל זוג חלקים נמדדו המרחקים בין **גיאומטריות החיתוך האמיתיות**, ולא רק מלבני התיחום.
- `CENTRAL_FLAT_6MM_SPIDER` ממוקם לפי מרכז הגיאומטריה של החלל המשולש, לא לפי מרכז מלבן התיחום. מרווח מחומר המשולש: {spider_hole_clearance:.3f} מ״מ. התיקון מתקן התנגשות בניסיון המקדים.
- קובצי CAD של V8 ותוצאות בדיקות המבנה הקודמות נכללים בחבילה המלאה. לא בוצע שינוי בגיאומטריית חלקי המוצר, רק בסידורם על הלוחות.
- תוצאות מרווחים מפורטות: `qa/NESTING_QA.json`. כל השורות הותאמו ב־DXF ו־SVG עד טולרנס קואורדינטות 0.000008 מ״מ.

## גבולות האישור
**G3 PASS — גמר תכנון ונסטינג דיגיטלי בלבד.** **G4/G5 HOLD** עד ניסוי חיתוך 1:1, פיצוי Kerf לפי מכונה, התאמת חיבורי מעטפת, כיפוף 4מ״מ, פערי סגירת מקטעים, חוזק הדבקה של הצלעות, עומס עציץ עם אדמה רטובה ויציבות. אין לטעון לאישור ייצור בלתי מוגבל או לעומס נשיאה מאומת.

הקבצים `nesting/*.svg` ו־`nesting/*.dxf` מיועדים לייבוא ב־1:1 מ״מ. השתמש רק בגרסת V8-850 המאוחדת ואל תערבב עם V7/גרסאות נסטינג ישנות.
'''
(DST/'README_HE.md').write_text(report,encoding='utf8')
print('FINAL QA summary')
for sheet in QA['sheets']:print(sheet['file_stem'],sheet['number_of_parts'],'min',sheet['min_part_gap_mm'],'margin',sheet['min_stock_margin_mm'])
print('spider clearance',spider_hole_clearance,'contours',QA['contours'],'kerf lines',QA['single_line_bend_cuts'])

# ZIP distribution: cutting-only and full CAD package.
for filename,include in [('PST_310_V8_850_OPT_3_SHEETS_SVG_DXF_DESIGN_ONLY.zip', ['nesting','individual','preview','qa','README_HE.md','PLACEMENTS.csv']),('PST_310_V8_850_OPT_FULL_CAD_AND_NESTING_DESIGN_ONLY.zip',['nesting','individual','preview','qa','cad','source','README_HE.md','PLACEMENTS.csv'])]:
    target=Path('/mnt/data')/filename
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for entry in include:
            f=DST/entry
            if f.is_dir():
                for path in sorted(f.rglob('*')):
                    if path.is_file():z.write(path,str(path.relative_to(DST)))
            else:z.write(f,f.name)
    with zipfile.ZipFile(target,'r') as z:assert z.testzip() is None
    print('PACKAGED',target, 'bytes',target.stat().st_size)
print('DONE')