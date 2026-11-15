#!/usr/bin/env python3
"""MEB-033: combine user-reported physically validated R6 lid slits
with 20 unchanged MEB-028 product profiles plus 1 MEB-029 inverse curve jig.

This script only changes stock positions (Y +0.35 roof; Y +0.85 seven
lower profiles) and replaces 194 old kerf centerlines with 88 R6 lines.
Geometry remains design-only for machine calibration / plywood fit.
"""
from pathlib import Path
from collections import Counter, defaultdict
import json, hashlib, math, zipfile
import ezdxf
from lxml import etree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union
from shapely.affinity import translate

BASE=Path('/mnt/data')
HERE=Path(__file__).resolve().parent
SRC_SHEET=HERE/'baseline/MEB030_ALL20_PLUS_SINGLE_CURVE_4MM_440x800_GAP1MM_DESIGN_ONLY.dxf'
if not SRC_SHEET.exists():
    SRC_SHEET=BASE/'MEB030_PRODUCT_PLUS_SINGLE_CURVE_DESIGN_ONLY/MEB030_ALL20_PLUS_SINGLE_CURVE_4MM_440x800_GAP1MM_DESIGN_ONLY.dxf'
SRC_SVG=SRC_SHEET.with_suffix('.svg')
R6_DXF=HERE/'R6_original/MEB032_R6_LID_THREE_WEBS_20MM_REVIEW_ONLY.dxf'
if not R6_DXF.exists():
    R6_DXF=BASE/'MEB032_R6_THREE_WEBS_20MM_REVIEW/MEB032_R6_LID_THREE_WEBS_20MM_REVIEW_ONLY.dxf'
R6_SVG=R6_DXF.with_suffix('.svg')
ROOT_NAME='MEB033_ALL20_PLUS_CURVE_R6_4MM_440x800_GAP1MM_DESIGN_ONLY'
OUT_DXF=HERE/(ROOT_NAME+'.dxf')
OUT_SVG=HERE/(ROOT_NAME+'.svg')
PREVIEW=HERE/'MEB033_NESTING_ACTIVE_AREA.png'
FULL=HERE/'MEB033_NESTING_FULL_440x800.png'
QA=HERE/'MEB033_QA.json'
README=HERE/'README_HE.md'
LID='LID_SKIN_RADIAL_4MM'
JIG='MEB029_SINGLE_INVERSE_CURVE_4MM'
# Chosen after checking true cutpaths (kerf overrun 0.35mm),
# while holding contours and 1mm nominal material separation.
ROOF_DY=0.35
LOWER_DY=0.85
LOWER_NAMES={'LID_END_L','LID_END_R','LID_FRONT_RAIL','LID_BACK_RAIL',
             'LID_CROSS_RIB_1','LID_CROSS_RIB_2',JIG}


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def part_data(doc):
    byid=defaultdict(lambda:defaultdict(list))
    for entity in doc.modelspace().query('LWPOLYLINE'):
        tag=entity.get_xdata('MEB028')
        name=tag[0].value; role=tag[1].value
        p=Polygon([(float(x),float(y)) for x,y,*_ in entity.get_points()])
        if not p.is_valid or p.area<=0:
            raise AssertionError((name,role,'invalid polygon'))
        byid[name][role].append((entity,p))
    out={}
    for name,roles in byid.items():
        assert len(roles['outer'])==1, name
        p=roles['outer'][0][1]
        if roles.get('hole'):
            p=p.difference(unary_union([q for _,q in roles['hole']]))
        assert p.is_valid and p.area>0, name
        out[name]=p
    return out


original=ezdxf.readfile(SRC_SHEET)
assert original.header['$INSUNITS']==4
base_ents=list(original.modelspace())
assert Counter(x.dxftype() for x in base_ents)==Counter({'LINE':194,'LWPOLYLINE':31})
orig_parts=part_data(original)
assert len(orig_parts)==21
assert set(LOWER_NAMES)<=set(orig_parts)
assert LID in orig_parts
lid_base=orig_parts[LID]
assert lid_base.bounds[2]-lid_base.bounds[0]>90
# R6 contour must match the prior lid cut part exactly, not just a bounding box.
r6=ezdxf.readfile(R6_DXF)
assert r6.header['$INSUNITS']==4
assert len(r6.modelspace().query('LWPOLYLINE'))==1
r6_outline=r6.modelspace().query('LWPOLYLINE')[0]
local_lid=Polygon([(float(x),float(y)) for x,y,*_ in r6_outline.get_points()])
assert local_lid.is_valid
local_minx,local_miny,local_maxx,local_maxy=local_lid.bounds
# Original part was rotated +90° in the 1-board MEB030 nest:
# sheet_X = original_sheet_right - local_Y; sheet_Y = sheet_top + local_X.
sheet_right=lid_base.bounds[2]
sheet_top=lid_base.bounds[1]
def T(x,y,dy=0):return (sheet_right-y,sheet_top+x+dy)
rotated=Polygon([T(x,y) for x,y in local_lid.exterior.coords])
assert lid_base.symmetric_difference(rotated).area<1e-4, ('lid outline differs',lid_base.symmetric_difference(rotated).area)

# Prepare modified stock: all material outlines identical to source, moved only.
ms=original.modelspace()
for ent in list(ms.query('LWPOLYLINE')):
    name=ent.get_xdata('MEB028')[0].value
    offset=ROOF_DY if name==LID else (LOWER_DY if name in LOWER_NAMES else 0.0)
    if offset:
        ent.translate(0,offset,0)
# Remove ONLY previous 194 lid kerfs, not any part outline.
old_slits=list(ms.query('LINE'))
assert len(old_slits)==194 and all(e.dxf.layer=='KERF_LINES_UNVERIFIED' for e in old_slits)
for ent in old_slits: ms.delete_entity(ent)
new_slits=[]
for ent in r6.modelspace().query('LINE'):
    ax,ay=T(ent.dxf.start.x,ent.dxf.start.y,ROOF_DY)
    bx,by=T(ent.dxf.end.x,ent.dxf.end.y,ROOF_DY)
    ln=ms.add_line((ax,ay),(bx,by),dxfattribs={'layer':'KERF_LINES_UNVERIFIED'})
    new_slits.append(ln)
assert len(new_slits)==88
original.header['$INSUNITS']=4
original.saveas(OUT_DXF)

# SVG: source groups preserved; only the lid's 194 old line tags replaced,
# and necessary absolute Y coordinates translated to maintain real cut clearance.
NS='http://www.w3.org/2000/svg'
s={'s':NS}
tree=etree.parse(str(SRC_SVG)); root=tree.getroot()
svggroups=root.xpath('./s:g',namespaces=s)
assert len(svggroups)==21

def fmt(v):return f'{v:.8f}'
for group in svggroups:
    name=group.get('id')
    dy=ROOF_DY if name==LID else (LOWER_DY if name in LOWER_NAMES else 0)
    # All source geometry is explicit polylines and LINE elements, no transformation matrix.
    for elem in group:
        typ=etree.QName(elem).localname
        assert typ in ('polyline','line'),(name,typ)
        if typ=='polyline' and dy:
            points=[tuple(map(float,w.split(','))) for w in elem.get('points').split()]
            elem.set('points',' '.join(f'{fmt(x)},{fmt(y+dy)}' for x,y in points))
    if name==LID:
        old=list(group.xpath('./s:line',namespaces=s))
        assert len(old)==194
        for elem in old:group.remove(elem)
        for source in r6.modelspace().query('LINE'):
            ax,ay=T(source.dxf.start.x,source.dxf.start.y,ROOF_DY)
            bx,by=T(source.dxf.end.x,source.dxf.end.y,ROOF_DY)
            elem=etree.SubElement(group,'{'+NS+'}line')
            for key,value in (('x1',ax),('y1',ay),('x2',bx),('y2',by)):
                elem.set(key,fmt(value))
            elem.set('stroke','#b14444')
            elem.set('stroke-width','0.12')
            elem.set('data-cut','kerf-research-user-tested-R6')

name_title=root.find('{'+NS+'}title')
if name_title is not None:
    name_title.text='MEB-033 | MEB-028 20 parts + inverse curve jig + user-tested R6 lid | 4mm stock one sheet 440x800 | DESIGN ONLY'
root.append(etree.Comment('R6 lid flex: user-reported physical fit acceptable. Manufacturing tolerances, strength and kerf remain unapproved.'))
tree.write(str(OUT_SVG),xml_declaration=True,encoding='utf-8',pretty_print=True)

# Independent readback method: parse final DXF and SVG back to polygons/lines,
# compare to original part shapes by symmetric difference after designed shifts.
readback=ezdxf.readfile(OUT_DXF)
parts=part_data(readback)
assert len(parts)==21
all_ent=list(readback.modelspace())
assert Counter(e.dxftype() for e in all_ent)==Counter({'LINE':88,'LWPOLYLINE':31})
assert all(e.closed for e in readback.modelspace().query('LWPOLYLINE'))
assert readback.header['$INSUNITS']==4
for name,poly in parts.items():
    offset=ROOF_DY if name==LID else (LOWER_DY if name in LOWER_NAMES else 0)
    prior=translate(orig_parts[name],yoff=offset)
    assert poly.symmetric_difference(prior).area<1e-5,('shape mutated',name,poly.symmetric_difference(prior).area)

# Check between actual material contours, and also each slit versus unrelated parts.
ids=list(parts)
pairs=[(a,b,parts[a].distance(parts[b])) for i,a in enumerate(ids) for b in ids[i+1:]]
assert len(pairs)==210
assert all(parts[a].intersection(parts[b]).area<1e-9 for a,b,_ in pairs)
assert min(d for _,_,d in pairs)>=1-1e-5
borders={name: min(p.bounds[0],p.bounds[1],440-p.bounds[2],800-p.bounds[3]) for name,p in parts.items()}
assert min(borders.values())>=3-1e-6
R6_Lines=[LineString([(e.dxf.start.x,e.dxf.start.y),(e.dxf.end.x,e.dxf.end.y)]) for e in readback.modelspace().query('LINE')]
assert len(R6_Lines)==88
min_distance_cut_other=min(seg.distance(poly) for seg in R6_Lines for name,poly in parts.items() if name!=LID)
assert min_distance_cut_other>=1.0-1e-6,('actual kerf protrusion too near neighboring part',min_distance_cut_other)
assert all(not seg.intersects(poly) for seg in R6_Lines for name,poly in parts.items() if name!=LID)
min_kerf_to_sheet_border=min(min(sg.bounds[0],sg.bounds[1],440-sg.bounds[2],800-sg.bounds[3]) for sg in R6_Lines)
assert min_kerf_to_sheet_border>=3-1e-6
assert all(sg.length<=138.001 for sg in R6_Lines)
# Preserve the source R6 actual cut lines exactly under a rigid placement transform.
for src,got in zip(r6.modelspace().query('LINE'),readback.modelspace().query('LINE')):
    a=T(src.dxf.start.x,src.dxf.start.y,ROOF_DY)
    b=T(src.dxf.end.x,src.dxf.end.y,ROOF_DY)
    assert math.dist(a,(got.dxf.start.x,got.dxf.start.y))<1e-7 and math.dist(b,(got.dxf.end.x,got.dxf.end.y))<1e-7

sr=etree.parse(str(OUT_SVG))
sgroups=sr.xpath('//s:g',namespaces=s)
assert len(sgroups)==21
assert len(sr.xpath('//s:line',namespaces=s))==88
assert len(sr.xpath('//s:polyline',namespaces=s))==31
# Verify SVG readback shape equivalence with DXF (path-only geometric independent representation).
for g in sgroups:
    name=g.get('id')
    for e in g.xpath('./s:polyline',namespaces=s):
        poly=Polygon([tuple(map(float,c.split(','))) for c in e.get('points').split()])
        assert any(poly.symmetric_difference(Polygon([(x,y) for x,y,*_ in entity.get_points()])).area<2e-4
                   for entity in readback.modelspace().query('LWPOLYLINE') if entity.get_xdata('MEB028')[0].value==name),('SVG profile mismatch',name)
svg_lines=sr.xpath('//s:g[@id="LID_SKIN_RADIAL_4MM"]/s:line',namespaces=s)
for elem,segment in zip(svg_lines,R6_Lines):
    a=(float(elem.get('x1')),float(elem.get('y1')))
    b=(float(elem.get('x2')),float(elem.get('y2')))
    assert math.dist(a,segment.coords[0])<1e-7 and math.dist(b,segment.coords[1])<1e-7

# Print-friendly previews with actual source contours, R6 kerf lines, jig highlight.
def draw_preview(path,full=False):
    fig,ax=plt.subplots(figsize=(10.0,16 if full else 10.5),dpi=160)
    for name,p in parts.items():
        if name==JIG:
            xx,yy=p.exterior.xy
            ax.fill(xx,yy,color='#93c9c7',alpha=.50,zorder=1)
        if name==LID:
            xx,yy=p.exterior.xy
            ax.fill(xx,yy,color='#f9e5c0',alpha=.37,zorder=1)
        xx,yy=p.exterior.xy
        ax.plot(xx,yy,color=('#02786e' if name==JIG else '#55514d'),lw=1.0 if name==JIG else .65,zorder=3)
        for h in p.interiors: ax.plot(*h.xy,color='#55514d',lw=.6,zorder=3)
    for sl in R6_Lines:
        x,y=sl.xy; ax.plot(x,y,color='#c64e4b',lw=.45,zorder=5)
    ax.plot([0,440,440,0,0],[0,0,800,800,0],color='#b1b1b1',lw=.7,ls='--')
    ax.set_xlim(0,440);ax.set_ylim(800 if full else 466,0);ax.set_aspect('equal')
    ax.set_xlabel('Stock width (mm)');ax.set_ylabel('Stock height (mm)')
    ax.set_title('MEB-033 | user-tested R6 lid + 20 product parts + 1 curve jig\n4mm birch · one 440 × 800mm board · 1mm true contour clearance',fontsize=10)
    ax.grid(alpha=.08)
    fig.tight_layout();fig.savefig(path,facecolor='white',bbox_inches='tight');plt.close(fig)
draw_preview(PREVIEW);draw_preview(FULL,True)

reported={
 'version':'MEB-033', 'status':'PROTOTYPE_GEOMETRY_USER_REPORTED_R6_PASSED',
 'user_physical_evidence':'User stated R6 was validated and worked well; no independent measurements or formal strength test available.',
 'sources':{'product_plus_jig':'MEB-030 DXF/SVG','lid_slits':'MEB-032 R6 DXF/SVG'},
 'sheet_mm':{'W':440,'H':800,'thickness_nominal':4},
 'counts':{'product':20,'single_inverse_curve_jig':1,'stock_parts':len(parts),'outline_loops':len(readback.modelspace().query('LWPOLYLINE')),'old_lid_kerfs_removed':194,'R6_lid_kerfs_inserted':len(R6_Lines),'kerf_rows':22,'kerfs_per_row':4,'bridges_per_row':3},
 'intended_kerf_pattern':{'bridge_width_mm':4,'outside_bridges_mm_from_edge':'20–24 alternating','max_slot_mm':max(seg.length for seg in R6_Lines),'edge_open':True},
 'layout_adjustments':{'roof_shift_down_mm':ROOF_DY,'lower_7_parts_shift_down_mm':LOWER_DY,'why':'Restore >=1mm clearance between edge-overrunning slit centerlines and neighboring cuts; keep >=3mm sheet border'},
 'QA':{'DXF':str(OUT_DXF),'SVG':str(OUT_SVG),'parts':len(parts),'all_contour_pair_checks':len(pairs),'min_contour_to_contour_mm':min(d for _,_,d in pairs),'min_kerf_to_nonlid_material_mm':min_distance_cut_other,'min_outline_stock_margin_mm':min(borders.values()),'min_kerf_stock_margin_mm':min_kerf_to_sheet_border,'maximum_occupied_height_mm':max(p.bounds[3] for p in parts.values()),'per_part_shape_geometry_preserved':True,'SVG_DXF_outline_and_line_roundtrip':'PASS','any_overlap':False},
 'sources_sha256':{'MEB030_base_DXF':sha(SRC_SHEET),'MEB030_base_SVG':sha(SRC_SVG),'R6_lid_DXF':sha(R6_DXF),'R6_lid_SVG':sha(R6_SVG)},
 'remaining_risks':['Actual kerf width and machine-specific fit uncalibrated','R6 material compliance and durability beyond user dry-run not tested','Wood glue/load/jig/hinge strength and 4mm stock tolerances not independently validated','No independent engineering QA or release to serial manufacturing']
}
QA.write_text(json.dumps(reported,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
README.write_text('''# MEB-033 — נסטינג מעודכן למכסה R6\n\nהגרסה מבוססת על 20 חלקי המוצר של MEB-028 + תומכת אחת (SINGLE CURVE) מ-MEB-029, בדגם הנסטינג MEB-030.\nמחליפה רק את **194 חריצי הכיפוף של המכסה** ב־**88 חריצי R6** שהמשתמש דיווח שהצליחו בניסוי.\nהמתאר החיצוני של כל 21 החלקים זהה למקור. תנועות מיקום בלבד: המכסה הוזז 0.35 מ״מ למטה, ושבעה חלקים מתחתיו 0.85 מ״מ למטה, כדי למנוע קווי חריצה בולטים המתקרבים לפחות מ־1 מ״מ לחלקים שכנים.\n\n## תכולת החיתוך\n- לוח בירץ 4 מ״מ, רוחב 440 × גובה 800 מ״מ.\n- 20 חלקי קופסה + תומכת SINGLE CURVE אחת.\n- 22 שורות × 4 חריצים = 88 קווי חריצה, שלושה גשרים של 4 מ״מ בכל שורה.\n- ללא קו מסגרת הלוח בשכבות החיתוך ב־DXF/SVG.\n- קובץ SVG וגם DXF; שכבה נפרדת לחריצים ב־DXF.\n\n## QA\nהמיקום המקורי של החלקים נשמר מלבד הזזות קטנות למרווח חיתוך; כל 21 מתארי החלקים עוברים בדיקת התאמה מול המקור.\nהחריצים נלקחו מה־DXF של R6 ללא שינוי בצורת החיתוך, רק סיבוב ומיקום.\nראו MEB033_QA.json למרווחים, ספירת פריטים ובדיקת סבולות גאומטריות.\n\n## הגבלות\nהמשתמש אישר הצלחה פיזית עם דוגמת R6. אין בכך אישור חוזק, עומס או כיול Kerf למכשיר, והקבצים אינם מאושרים לייצור סדרתי.\n''',encoding='utf8')

ZIP=HERE.parent/'MEB033_R6_TESTED_LID_FULL_21_PART_NESTING.zip'
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for f in (OUT_DXF,OUT_SVG,PREVIEW,FULL,QA,README,Path(__file__),R6_SVG,R6_DXF,SRC_SHEET,SRC_SVG):
        prefix='baseline/' if f in (SRC_SHEET,SRC_SVG) else ('R6_original/' if f in (R6_SVG,R6_DXF) else '')
        z.write(f,prefix+f.name)
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
    assert len(z.namelist())==11
print(json.dumps({'files':[str(OUT_DXF),str(OUT_SVG),str(PREVIEW),str(ZIP)],'QA':reported['QA'],'ZIP_SHA256':sha(ZIP)},ensure_ascii=False,indent=2))
