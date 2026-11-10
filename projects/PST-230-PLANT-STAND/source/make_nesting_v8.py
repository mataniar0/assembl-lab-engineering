#!/usr/bin/env python3
"""Generate 1:1 mm laser source contours and conservative MaxRects nesting for PST-310 V5.
No claim of physical fit, load stability, continuous assembly route, or kerf calibration.
"""
from __future__ import annotations
import json,math,random,functools,pathlib,csv,itertools,zipfile,datetime,copy
import numpy as np
import cadquery as cq
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
from shapely.affinity import translate, rotate
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
OUT=pathlib.Path(__file__).resolve().parent
SRC=(pathlib.Path(__file__).resolve().parent/'build_pst_310_v4.py').read_text()
ns={'__name__':'pst_v4_source_definition'}
exec(SRC.split('parts={}')[0],ns)
W,H=440,800
GAP=1.0; EDGE=5.0
CUT6=[];CUT4=[]

# For an extruded CAD BREP, extract the actual planar milling face contours.
# Sample each analytic circular edge with max chord-sag tolerance below approximately .005mm.
def face_polygon(shape, plane='xy'):
    axis=2 if plane=='xy' else 1
    axes=(0,1) if plane=='xy' else (0,2)
    faces=[f for f in shape.Faces() if abs((f.normalAt().z if axis==2 else f.normalAt().y))>.995]
    if not faces:raise RuntimeError('No planar face for '+plane)
    f=max(faces,key=lambda x:x.Area())
    def wire_pts(w):
        edges=[]
        for e in w.Edges():
            vectors=e.sample(.003)[0]
            vv=[(p.x,p.y,p.z) for p in vectors]
            pt=[(round(v[axes[0]],5),round(v[axes[1]],5)) for v in vv]
            if len(pt)>1:edges.append(pt)
        if not edges:raise RuntimeError('empty wire')
        ans=edges.pop(0)
        while edges:
            d1=[(math.dist(ans[-1],e[0]),i,False) for i,e in enumerate(edges)]
            d2=[(math.dist(ans[-1],e[-1]),i,True) for i,e in enumerate(edges)]
            d,i,rev=min(d1+d2)
            if d>.025:raise RuntimeError(f'wire edge endpoint gap {d}')
            seq=edges.pop(i)
            if rev:seq=seq[::-1]
            ans.extend(seq[1:])
        if math.dist(ans[0],ans[-1])>.025 and not(len(w.Edges())==1 and w.Edges()[0].geomType()=='CIRCLE'):
            raise RuntimeError(f'open wire {plane} face_area={f.Area():.2f} start={ans[0]} end={ans[-1]} gap={math.dist(ans[0],ans[-1]):.3f} edges={len(w.Edges())}')
        if ans[-1]==ans[0]:ans.pop()
        return ans
    rings=[wire_pts(w) for w in f.Wires()]
    shell=max(range(len(rings)),key=lambda i:abs(Polygon(rings[i]).area))
    pp=Polygon(rings[shell],[v for i,v in enumerate(rings) if i!=shell]);
    if not pp.is_valid:pp=pp.buffer(0)
    if pp.geom_type!='Polygon' or not pp.is_valid:
        raise RuntimeError('Source CAD face invalid after polygon approximation')
    # independent area parity, 0.003mm discretization gives ~few mm² worst-case over 310mm disk
    if abs(pp.area-f.Area())>max(3,0.00013*f.Area()):
        raise RuntimeError(f'CAD face/2D area mismatch: cad={f.Area()} actual={pp.area}')
    return pp,dict(cad_area_mm2=f.Area(),cut_area_mm2=pp.area,area_error_mm2=pp.area-f.Area(),face_wires=len(f.Wires()))

def cut_item(name,layer,geom,source,ref=None):
    if not geom.is_valid:geom=geom.buffer(0)
    if geom.geom_type!='Polygon' or geom.area<=1:raise ValueError('invalid cut polygon '+name)
    bb=geom.bounds
    # Normalize every part for file export; shape dimensions are preserved by pure translation.
    normalized=translate(geom,xoff=-bb[0]+2,yoff=-bb[1]+2)
    w=bb[2]-bb[0];h=bb[3]-bb[1]
    rec=dict(id=name,layer=layer,poly=normalized,source=source,ref=ref,original_size=[round(w,6),round(h,6)],
             original_area=geom.area,detail={})
    (CUT6 if layer=='6mm' else CUT4).append(rec)
    return rec

# V6 modified source cut geometries: only flat laser-cut parts; NO lower circular spider,
# NO three split triangle corners, NO nine bridge strips. Preserve upper & lower ø310 discs.
V7_NS={'__file__':str(OUT/'build_v8.py'),'__name__':'pst_v7_defs'}
exec((OUT/'build_v8.py').read_text().split('\nparts={')[0],V7_NS)
for label,solid in [('TOP_DISC_D310_RIM_TABS_ONLY_6MM',V7_NS['top_disc_rim_fingers_only']()),
 ('BOTTOM_DISC_D310_6MM',ns['disk'](False)),
 ('LOWER_TRIANGLE_ONE_PIECE_6MM',ns['lower_triangle']()),
 ('CENTRAL_FLAT_6MM_SPIDER',V7_NS['NS']['flat_core']())]:
 print('extract',label,flush=True)
 geom,parity=face_polygon(solid,'xy');p=cut_item(label,'6mm',geom,'V6 actual 6mm CAD BREP',parity);p['detail']=parity
rib_geom,parity=face_polygon(V7_NS['rib_bottom_fingers_only'](0),'xz')
for i in range(6):
 p=cut_item(f'CORE_RIB_{i+1:02d}_6MM','6mm',rib_geom,'V7 6mm rib BREP with top fingers clipped flush' ,parity);p['detail']=parity
leg_geom,parity=face_polygon(V7_NS['NS']['leg_v6'](),'xz')
for i in range(3):
 for suffix in ('A','B'):
  p=cut_item(f'LEG_{i+1}_{suffix}_6MM','6mm',leg_geom,'V6 real BREP raised 6mm shoulder and retained 6mm fingers',parity)
  p['detail']=parity
assert len(CUT6)==16
# Rim development: neutral arc-length r=153mm, sectors angular width exactly 60 degrees.
# Structural wall body is y6..54 (48mm); BOTTOM ONLY tabs of 6mm at 12° and 48°. No upper tabs.
rim_arc=153*math.pi/3
rim_centers=[153*math.radians(a) for a in [12,48]]
body=box(0,6,rim_arc,54)
for i in range(6):
    tab_polys=[box(x-6,0,x+6,6) for x in rim_centers]+[box(x-6,54,x+6,60) for x in rim_centers]  # V8: both top and bottom tabs
    flat=unary_union([body]+tab_polys).buffer(0)
    rec=cut_item(f'RIM_{i+1:02d}_BIRCH4_UPPER_LOWER_TABS','4mm',flat,'V7 neutral-radius 153mm / 60° flat development, both upper and lower tabs' )
    # 4mm staggered rows. 42mm central cut alternates with pair of 20mm edge cuts (8mm central bridge).
    # In reinforced tab zones all rows remain, but are locally shorter to reduce tearing.
    strokes=[]
    x=4.0
    row=0
    while x<rim_arc-3.5:
        near=any(abs(x-v)<9 for v in rim_centers)
        if row%2==0:
            strokes.append(LineString([(x,12 if near else 9),(x,48 if near else 51)]))
        else:
            strokes.append(LineString([(x,8 if near else 6),(x,23 if near else 26)]))
            strokes.append(LineString([(x,37 if near else 34),(x,52 if near else 54)]))
        row+=1;x=4.0+4*row
    # add translation +2mm from part normalize, cut line ends remain inside face body
    strokes=[translate(l,xoff=2,yoff=2) for l in strokes]
    assert all(rec['poly'].covers(l) for l in strokes),rec['id']
    rec['kerf_lines']=strokes
    rec['kerf_rows']=row
    rec['detail']={'flat_length_mm':rim_arc,'body_width_mm':48,'rim_t_mm':4,
                   'rows':row,'line_segments':len(strokes),'pitch_mm':4,
                   'end_seam':'straight butt edge; joint/retention unverified',
                   'developed_length_total_mm':6*rim_arc}
assert len(CUT4)==6
print('CUT SOURCES',len(CUT6),len(CUT4),'6mm area',round(sum(p['poly'].area for p in CUT6)),flush=True)

# Exhaustively preserve exact SVG/DXF 2D geometry (0.00001mm vertex precision), no sheet outlines as cut.
def iterloops(poly):
    yield ('CUT_OUTER',list(poly.exterior.coords)[:-1])
    for h in poly.interiors:yield('CUT_INNER',list(h.coords)[:-1])

def make_svg(name,items,sw,sh):
    from xml.sax.saxutils import escape
    s=['<?xml version="1.0" encoding="utf-8"?>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw:.5f}mm" height="{sh:.5f}mm" viewBox="0 0 {sw:.5f} {sh:.5f}">',
       f'<title>{escape(name)} — DESIGN ONLY — DO NOT CUT UNTIL QA &amp; PHYSICAL TEST</title>',
       '<desc>Units in mm. CUT_OUTER, CUT_INNER closed contours; CUT_KERF_LINE single lines. No sheet frame in cutting paths. Gap 1.0mm minimum (conservative BBOX).</desc>',
       '<g fill="none" stroke="#000" stroke-width="0.12">']
    count=0;segments=0
    for it in items:
        p=it['poly'];s.append(f'<g id="{escape(it["id"])}">')
        for layer,coords in iterloops(p):
            pts=' '.join(f'{x:.5f},{y:.5f}' for x,y in coords)
            s.append(f'<polygon class="{layer}" points="{pts}"/>');count+=1
        for line in it.get('kerf_lines',[]):
            pp=list(line.coords);assert len(pp)==2
            s.append(f'<path class="CUT_KERF_LINE" d="M {pp[0][0]:.5f},{pp[0][1]:.5f} L {pp[1][0]:.5f},{pp[1][1]:.5f}"/>');segments+=1
        s.append('</g>')
    s.append('</g></svg>')
    return '\n'.join(s)+'\n',dict(contours=count,kerf_lines=segments)

def make_dxf(items):
    doc=ezdxf.new('R2010',setup=False);doc.header['$INSUNITS']=4
    for layer in ['CUT_OUTER','CUT_INNER','CUT_KERF_LINE']:
        doc.layers.add(layer,color=7)
    ms=doc.modelspace()
    for it in items:
        for layer,coords in iterloops(it['poly']):
            ms.add_lwpolyline([(round(x,5),round(y,5)) for x,y in coords],close=True,dxfattribs={'layer':layer})
        for line in it.get('kerf_lines',[]):
            a,b=line.coords
            ms.add_line(tuple(a),tuple(b),dxfattribs={'layer':'CUT_KERF_LINE'})
    return doc

# Independent per-part cuts and small per-piece cutting preview.
for p in CUT6+CUT4:
    x0,y0,x1,y1=p['poly'].bounds
    bw=math.ceil(x1+2);bh=math.ceil(y1+2)
    svg,c=make_svg(p['id'],[p],bw,bh)
    (OUT/'svg'/(p['id']+'.svg')).write_text(svg,encoding='utf-8')
    make_dxf([p]).saveas(OUT/'dxf'/(p['id']+'.dxf'))

# V6 improved SHAPE-AWARE four-total-board packing: THREE 6mm sheets + one 4mm.
# 2 sloped legs / board. On S01 and S02 a Ø310 disc is at the extreme top;
# the circular edge avoids the top ends of the legs by >2.6mm, despite bbox overlap.
# Small 90-degree ribs fit between leg envelopes. On S03 the 6mm triangular ring
# is rotated 30deg to nest above the legs. The flat center connector is *inside*
# its genuine scrap opening, with 9.07mm clearance, requiring cut sequencing
# that does not let loose inner scrap move before the inner part is complete.
def place(item,xmin,ymin,angle=0):
    origin_poly=item['poly'];rr=rotate(origin_poly,angle,origin=(0,0));x0,y0,x1,y1=rr.bounds
    dx=xmin-x0;dy=ymin-y0;final=translate(rr,xoff=dx,yoff=dy)
    strokes=[translate(rotate(l,angle,origin=(0,0)),xoff=dx,yoff=dy) for l in item.get('kerf_lines',[])]
    assert final.bounds[0]>=EDGE-1e-5 and final.bounds[1]>=EDGE-1e-5
    assert final.bounds[2]<=W-EDGE+1e-5 and final.bounds[3]<=H-EDGE+1e-5
    return {**item,'poly':final,'kerf_lines':strokes,
            'nest_rot':angle,'translation':[dx,dy],
            'bbox_nest_mm':[round(v,5) for v in final.bounds]}

class Sheet:
    def __init__(self):self.items=[]

def by_id(x):return next(q for q in CUT6 if q['id']==x)

sheets=[Sheet() for _ in range(3)]
leg_items=sorted((p for p in CUT6 if p['id'].startswith('LEG_')),key=lambda p:p['id'])
rib_items=sorted((p for p in CUT6 if p['id'].startswith('CORE_RIB_')),key=lambda p:p['id'])
for i in range(3):
    sh=sheets[i]
    sh.items.append(place(leg_items[2*i],5,5))
    sh.items.append(place(leg_items[2*i+1],230,5))
for i,name in enumerate(['TOP_DISC_D310_RIM_TABS_ONLY_6MM','BOTTOM_DISC_D310_6MM']):
    sheets[i].items.append(place(by_id(name),5,485))
for i,rib in enumerate(rib_items):
    sheets[i//3].items.append(place(rib,181,15+(i%3)*115,90))
triangle=by_id('LOWER_TRIANGLE_ONE_PIECE_6MM')
rotated=rotate(triangle['poly'],30,origin=(0,0));rb=rotated.bounds
triangle_nest=place(triangle,5,795-(rb[3]-rb[1]),30)
sheets[2].items.append(triangle_nest)
core=by_id('CENTRAL_FLAT_6MM_SPIDER')
inner_poly=Polygon(triangle_nest['poly'].interiors[0].coords)
inner_center=inner_poly.centroid;cent=core['poly'].centroid
core_dx=inner_center.x-cent.x;core_dy=inner_center.y-cent.y
core_geom=translate(core['poly'],xoff=core_dx,yoff=core_dy)
assert inner_poly.buffer(-1).covers(core_geom)
sheets[2].items.append({**core,'poly':core_geom,'kerf_lines':[],
   'nest_rot':0,'translation':[core_dx,core_dy],
   'bbox_nest_mm':[round(v,5) for v in core_geom.bounds]})
assert sorted(q['id'] for sh in sheets for q in sh.items)==sorted(p['id'] for p in CUT6)
print('V8 SHAPE AWARE 3 SHEET BIRCH6',[[it['id'] for it in sh.items] for sh in sheets],flush=True)

rim_sheet=Sheet()
for j,p in enumerate(CUT4):
    b=p['poly'].bounds;w=b[2]-b[0];h=b[3]-b[1]
    rim_sheet.items.append(place(p,5+(j%2)*(w+GAP+5),5+(j//2)*(h+GAP+5)))
# Contour pairs: both actual shapely polygon gap and conservative bbox.
def validate_sheet(items):
    pp=[it['poly'] for it in items]
    failures=[];closest=(1e9,None)
    for i,j in itertools.combinations(range(len(items)),2):
        a,b=pp[i],pp[j]
        if a.intersects(b):failures.append((items[i]['id'],items[j]['id'],'overlap'))
        dist=a.distance(b)
        if dist<closest[0]:closest=(dist,[items[i]['id'],items[j]['id']])
        if dist+1e-5<GAP:failures.append((items[i]['id'],items[j]['id'],round(dist,6)))
    if failures:raise RuntimeError(f'cut paths too close {failures[:10]}')
    if any(min(p.bounds[0],p.bounds[1],W-p.bounds[2],H-p.bounds[3])<EDGE-.0001 for p in pp):
        raise RuntimeError('sheet edge insufficient')
    return {'parts':len(items),'pair_checks':len(items)*(len(items)-1)//2,'min_distance_mm':None if len(items)<2 else round(closest[0],6),
            'closest_pair':closest[1],'min_edge_mm':round(min(min(p.bounds[0],p.bounds[1],W-p.bounds[2],H-p.bounds[3]) for p in pp),6),
            'total_part_area_mm2':round(sum(p.area for p in pp),2)}

sheet_records=[]
for idx,sh in enumerate(sheets,1):
    itemlist=sh.items
    validation=validate_sheet(itemlist)
    sheetname=f'BIRCH6_S{idx:02d}_440x800'
    svg,cnt=make_svg(sheetname,itemlist,W,H)
    (OUT/'nesting'/(sheetname+'.svg')).write_text(svg,encoding='utf-8')
    make_dxf(itemlist).saveas(OUT/'nesting'/(sheetname+'.dxf'))
    sheet_records.append({'name':sheetname,'thickness_mm':6,**validation,**cnt,'ids':[it['id'] for it in itemlist]})
rim_validation=validate_sheet(rim_sheet.items)
name='BIRCH4_S01_440x800'
svg,cnt=make_svg(name,rim_sheet.items,W,H)
(OUT/'nesting'/(name+'.svg')).write_text(svg,encoding='utf-8')
make_dxf(rim_sheet.items).saveas(OUT/'nesting'/(name+'.dxf'))
sheet_records.append({'name':name,'thickness_mm':4,**rim_validation,**cnt,'ids':[it['id'] for it in rim_sheet.items]})
# Validate roundtrip DXF geometry vs SVG input: type, closed paths, equivalent polygon points with tolerance 1e-5.
from xml.etree import ElementTree as ET
for file in sorted((OUT/'nesting').glob('*.svg')):
    root=ET.parse(file).getroot()
    shapes=[];paths=[]
    for e in root.iter():
        if e.tag.endswith('polygon'):
            pts=[tuple(map(float,v.split(','))) for v in e.attrib['points'].split()]
            shapes.append((e.attrib['class'],pts))
        if e.tag.endswith('path'):
            paths.append(e.attrib.get('class'))
    doc=ezdxf.readfile(file.with_suffix('.dxf'))
    polys=list(doc.modelspace().query('LWPOLYLINE'));lines=list(doc.modelspace().query('LINE'))
    if len(polys)!=len(shapes) or len(lines)!=len(paths):raise RuntimeError('DXF mismatch counts for '+file.name)
    for lp,(layer,pts) in zip(polys,shapes):
        if lp.dxf.layer!=layer or not lp.closed or len(lp)!=len(pts):raise RuntimeError('DXF contour mismatch '+file.name)
        if any(abs(x-expected[0])>0.000011 or abs(y-expected[1])>0.000011 for (x,y,*_),expected in zip(lp,pts)):
            raise RuntimeError('DXF contour coordinate mismatch '+file.name)
    if any(line.dxf.layer!='CUT_KERF_LINE' for line in lines):raise RuntimeError('bad kerf layer')
print('DXF SVG parity PASS on all sheets',len(sheet_records),flush=True)
# Preview and BOM reports
plt.rcParams.update({'font.size':7,'font.family':'DejaVu Sans'})
for sr,sh in zip(sheet_records,[*sheets,rim_sheet]):
    fig,ax=plt.subplots(figsize=(6.1,11.0));ax.set_xlim(0,W);ax.set_ylim(0,H);ax.set_aspect('equal')
    ax.add_patch(plt.Rectangle((0,0),W,H,facecolor='#faf5eb',edgecolor='#a28d75',linewidth=2))
    cmap=plt.cm.get_cmap('Set3',len(sh.items)+1)
    for j,it in enumerate(sh.items):
        p=it['poly'];coords=list(p.exterior.coords)
        ax.add_patch(MplPolygon(coords,facecolor=cmap(j),edgecolor='#473b31',linewidth=.7,alpha=.8))
        for hole in p.interiors:
            ax.add_patch(MplPolygon(list(hole.coords),facecolor='white',edgecolor='#473b31',linewidth=.5))
        for line in it.get('kerf_lines',[]):
            xx,yy=line.xy;ax.plot(xx,yy,color='#7d513d',linewidth=.22)
        ctr=p.representative_point()
        if p.area>400:
            lbl=it['id'].replace('_6MM','').replace('_4MM','').replace('BIRCH','')
            ax.text(ctr.x,ctr.y,lbl,ha='center',va='center',fontsize=5,color='#26333c',bbox={'facecolor':'white','alpha':.55,'edgecolor':'none','pad':.2})
    ax.set_title(sr['name']+'\n'+str(sr['parts'])+' components, stock 440 x 800 mm, min 1 mm cut gap',fontsize=10)
    ax.grid(color='#ddd1bf',alpha=.2);fig.tight_layout();fig.savefig(OUT/'preview'/(sr['name']+'.png'),dpi=190);plt.close(fig)

items_all=[*CUT6,*CUT4]
# Compact overview of each sheet (images by Pillow to preserve original colors)
from PIL import Image,ImageDraw,ImageFont
thumbs=[]
for sr in sheet_records:
    im=Image.open(OUT/'preview'/(sr['name']+'.png')).convert('RGB');im.thumbnail((320,575))
    thumbs.append((sr,im))
canvas=Image.new('RGB',(350*len(thumbs),670),'#f8f5ee');draw=ImageDraw.Draw(canvas)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(font,16)
for i,(sr,im) in enumerate(thumbs):
    x=i*350+15;canvas.paste(im,(x,42))
    draw.text((x,8),sr['name'],font=f,fill='#38342d')
canvas.save(OUT/'preview'/'ALL_NESTING_SHEETS_OVERVIEW.png')

with (OUT/'BOM.csv').open('w',encoding='utf-8-sig',newline='') as fh:
    writer=csv.writer(fh)
    writer.writerow(['id','qty','nominal_thickness_mm','bbox_width_mm','bbox_height_mm','source','area_mm2','production_status'])
    for it in items_all:writer.writerow([it['id'],1,6 if it['layer']=='6mm' else 4,*[round(x,4) for x in it['original_size']],it['source'],round(it['original_area'],2),'DESIGN_ONLY_PHYSICAL_QA_HOLD'])
with (OUT/'PLACEMENTS.csv').open('w',encoding='utf-8-sig',newline='') as fh:
    writer=csv.writer(fh)
    writer.writerow(['sheet','item','x_mm','y_mm','rotation_deg','min_x','min_y','max_x','max_y'])
    for sr,sh in zip(sheet_records,[*sheets,rim_sheet]):
        for item in sh.items:
            bb=item['poly'].bounds
            writer.writerow([sr['name'],item['id'],*map(lambda x:round(x,5),item['translation']),item['nest_rot'],*map(lambda x:round(x,5),bb)])

qa={
 'title':'PST-310 V7 — smooth Ø310 upper disc without radial or edge perforations',
 'status':'NESTING_COMPLETE_DESIGN_ONLY_GLUE_UPPER_JOINT_NOT_STRUCTURALLY_QUALIFIED',
 'reference_geometry':'V7 CAD BREP: smooth Ø310 upper disk, trimmed rib upper tabs and rim upper tabs; V6 bottom/legs/triangle retained',
 'stock_mm':[440,800],'mm_unit':True,'nesting_target_gap_mm':1,'cut_stock_min_edge_mm':5,
 'sheet_count_6mm':len(sheets),'sheet_count_4mm':1,'sheet_total':len(sheet_records),
 '6mm_parts':len(CUT6),'4mm_parts':len(CUT4),
 '6mm_cut_area_mm2':sum(p['poly'].area for p in CUT6),
 'rim4_developed_per_sector_mm':rim_arc,'rim4_developed_total_mm':rim_arc*6,
 'rim4_rows_per_part':CUT4[0]['kerf_rows'],'rim4_single_line_segments_per_part':len(CUT4[0]['kerf_lines']),
 'sheet_results':sheet_records,
 'CAD_area_parity':{x['id']:{'cad':x['detail']['cad_area_mm2'],'polygonized':x['detail']['cut_area_mm2'],'diff':x['detail']['area_error_mm2']} for x in CUT6 if 'cad_area_mm2' in x['detail']},
 'SVG_DXF_1to1_parity':True,'all_individual_svg_dxf_generated':True,
 'kerf_compensation_mm':0,'physical_plywood_thickness_mm':'UNMEASURED',
 'not_verified':['rim physical flexibility, curvature and circumference closing without overlap','continuous full three leg insertion and full shell assembly','glued bond durability; strength/stability of heavy/wet plant','actual laser kerf; kerf slots are single-line 0 drawing width','full manufacturing release and glue-only top panel lift resistance'],
 'cut_permission':'HOLD: Validate glue-on lid pull-off and wet pot loads; no qualified joint yet'}
(OUT/'qa'/'V8_NESTING_QA.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False),encoding='utf-8')
print('NESTING V8 COMPLETE:',len(sheets),'6mm boards, 1 4mm board; all',len(items_all),'parts',flush=True)