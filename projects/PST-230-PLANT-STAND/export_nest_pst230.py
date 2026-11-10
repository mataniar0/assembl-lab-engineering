#!/usr/bin/env python3
"""PST-230: exact CAD-derived 2D source and 2+1 stock nesting, model-only validation."""
from __future__ import annotations
import runpy,pathlib,math,random,itertools,copy,json,csv,hashlib,time,xml.etree.ElementTree as ET
import numpy as np
import cadquery as cq
from shapely.geometry import Polygon, LineString, box, MultiPolygon
from shapely.affinity import translate,rotate
from shapely.ops import unary_union
import ezdxf
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PolygonPatch
ROOT=pathlib.Path(__file__).resolve().parent
NS=runpy.run_path(str(ROOT/'build_pst_230.py'))
parts=NS['parts']; Q=NS['Q'];RNEUTRAL=NS['RNEUTRAL'];P=NS['P'];
for name in ['cut_parts_svg','cut_parts_dxf','nesting','preview','qa']:(ROOT/name).mkdir(exist_ok=True)
# Extract cross sectional faces sampled from real OCC BREP. In-plane segmentation sag ~.003mm.
orig=(ROOT/'source'/'make_nesting_v8.py').read_text()
code='def face_polygon'+orig.split('def face_polygon',1)[1].split('\ndef cut_item',1)[0]
ctx={'math':math,'Polygon':Polygon}
exec(code,ctx)
face_polygon=ctx['face_polygon']
cut={}
for label,solid in parts.items():
    if label.startswith('RIM_'):continue
    if label.startswith('CORE_RIB_') and label!='CORE_RIB_01_6MM':continue
    if label.startswith('LEG_') and label!='LEG_1_A_6MM':continue
    # cross-sectional unrotated part without assembly angular rotation for 6mm profiles
    if label.startswith('CORE_RIB_'):solid=NS['rib_blank'](0)
    if label.startswith('LEG_'):solid=NS['leg_blank']()
    plane='xz' if label.startswith(('CORE_RIB_','LEG_')) else 'xy'
    geom,parity=face_polygon(solid,plane)
    b=geom.bounds
    geom=translate(geom,-b[0],-b[1])
    cut[label]=(geom,[],parity)
# duplicate the six identical rib/leg blank outlines with exact part IDs.
for i in range(1,7):
    name=f'CORE_RIB_{i:02d}_6MM';cut[name]=cut['CORE_RIB_01_6MM']
for i in range(1,4):
    for suff in ['A','B']:
        name=f'LEG_{i}_{suff}_6MM';cut[name]=cut['LEG_1_A_6MM']
# Unfold curved 4mm rim sectors by neutral axis, retaining 12mm arc-length upper/lower finger tabs.
arc=RNEUTRAL*math.pi/3
centers=[RNEUTRAL*math.radians(v) for v in [12,48]]
for i in range(1,7):
    body=box(0,6,arc,54)
    tabs=[box(c-6,0,c+6,6) for c in centers]+[box(c-6,54,c+6,60) for c in centers]
    geom=unary_union([body,*tabs]).buffer(0)
    strokes=[]
    x=4.;row=0
    while x<arc-3.5:
        near=any(abs(x-v)<9 for v in centers)
        if row%2==0:strokes.append(LineString([(x,12 if near else 9),(x,48 if near else 51)]))
        else:
            strokes.extend([LineString([(x,8 if near else 6),(x,23 if near else 26)]),LineString([(x,37 if near else 34),(x,52 if near else 54)])])
        row+=1;x=4+4*row
    name=f'RIM_{i:02d}_BIRCH4_UPPER_LOWER_TABS'
    assert all(geom.covers(line) for line in strokes)
    cut[name]=(geom,strokes,{'developed_length_mm':arc,'kerf_rows':row})
assert len(cut)==22
assert all(p.is_valid and p.area>5 for p,_,_ in cut.values())

# DXF/SVG preservation of line geometry, identical source for individual and nested drawings.
def write_svg_dxf(stem,items,base,width,height):
    doc=ezdxf.new('R2010');doc.header['$INSUNITS']=4
    for layer in ('CUT_OUTER','CUT_INNER','CUT_KERF_LINE'):doc.layers.add(layer,color=7)
    d=doc.modelspace()
    lines=['<?xml version="1.0" encoding="UTF-8"?>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.5f}mm" height="{height:.5f}mm" viewBox="0 0 {width:.5f} {height:.5f}">','<g stroke="black" fill="none" stroke-width="0.12">']
    for it in items:
        p,kerfs=it['geometry'],it['cutlines'];lines.append(f'<g id="{it["name"]}">')
        for layer,ring in [('CUT_OUTER',p.exterior),* [('CUT_INNER',w) for w in p.interiors]]:
            pts=list(ring.coords)[:-1]
            d.add_lwpolyline(pts,close=True,dxfattribs={'layer':layer})
            lines.append(f'<polygon class="{layer}" points="'+ ' '.join(f'{x:.5f},{y:.5f}' for x,y in pts)+'"/>')
        for ln in kerfs:
            a,b=list(ln.coords);d.add_line(a,b,dxfattribs={'layer':'CUT_KERF_LINE'})
            lines.append(f'<path class="CUT_KERF_LINE" d="M {a[0]:.5f},{a[1]:.5f} L {b[0]:.5f},{b[1]:.5f}"/>')
        lines.append('</g>')
    lines.append('</g></svg>')
    svg=base/(stem+'.svg');dxf=base/(stem+'.dxf')
    svg.write_text('\n'.join(lines),encoding='utf8');doc.saveas(dxf)
    return svg,dxf

for name,(poly,lines,_) in cut.items():
    # individual sources padded by 2mm on all sides.
    shift=(2-poly.bounds[0],2-poly.bounds[1]);gp=translate(poly,*shift)
    kerfs=[translate(l,*shift) for l in lines]
    w=gp.bounds[2]+2;h=gp.bounds[3]+2
    obj={'name':name,'geometry':gp,'cutlines':kerfs}
    # duplicated export to separate directories
    svg,dxf=write_svg_dxf(name,[obj],ROOT/'cut_parts_svg',w,h)
    dxf.replace(ROOT/'cut_parts_dxf'/dxf.name)

# Approximate seed positions for geometry-aware optimization on 2x6mm + 1x4mm.
W,H=440.,850.;MARGIN=5.;GAP=1.15
# To include inner spider in scrap triangle hole without collision, translate it to hole centroid.
tri=cut['LOWER_TRIANGLE_ONE_PIECE_6MM'][0]
sp=cut['CENTRAL_FLAT_6MM_SPIDER'][0]
assert len(tri.interiors)==1
hole=Polygon(tri.interiors[0]);center_delta=(hole.centroid.x-sp.centroid.x,hole.centroid.y-sp.centroid.y)
sp_in=translate(sp,*center_delta)
assert hole.contains(sp_in) and tri.distance(sp_in)>1.15,(hole.area,sp_in.area,tri.distance(sp_in))

# deterministic 2-sheet group layout: 4 legs and triangle + spider + 6 ribs on sheet 1;
# 2 legs and two discs on sheet 2. Search placement by fast shapely simulated annealing.
groups=[['LEG_1_A_6MM','LEG_1_B_6MM','LEG_3_A_6MM','LEG_3_B_6MM','TRI_CLUSTER',*[f'CORE_RIB_{i:02d}_6MM' for i in range(1,7)]],
        ['LEG_2_A_6MM','LEG_2_B_6MM','BOTTOM_DISC_D230_6MM','TOP_DISC_D230_RIM_TABS_ONLY_6MM']]
shapes={name:poly for name,(poly,_,_) in cut.items()}
shapes['TRI_CLUSTER']=MultiPolygon([tri,sp_in])

def transformed(shape,x,y,angle):
    s=rotate(shape,angle,origin=(0,0),use_radians=False)
    b=s.bounds
    return translate(s,xoff=x-b[0],yoff=y-b[1])
def limits(shape,angle):
    p=rotate(shape,angle,origin=(0,0))
    b=p.bounds
    return MARGIN,W-MARGIN-(b[2]-b[0]),MARGIN,H-MARGIN-(b[3]-b[1])
def objective(st,names,bufshapes):
    gg={n:transformed(bufshapes[n],*st[n]) for n in names}
    pen=0.
    for n,g in gg.items():
        x0,y0,x1,y1=g.bounds
        pen+=max(0,MARGIN-x0)*100+max(0,x1-(W-MARGIN))*100+max(0,MARGIN-y0)*100+max(0,y1-(H-MARGIN))*100
    for a,b in itertools.combinations(names,2):
        aa,bb=gg[a],gg[b]
        if aa.bounds[2]<bb.bounds[0] or aa.bounds[0]>bb.bounds[2] or aa.bounds[3]<bb.bounds[1] or aa.bounds[1]>bb.bounds[3]:continue
        if aa.intersects(bb):
            # geometries may have micro invalidities; convert to 0 distance + intersection area
            pen+=20*aa.intersection(bb).area+10
    return pen

def seed_group(names,index):
    st={};rnd=random.Random(1337+index)
    for name in names:
        for _ in range(500):
            angle=rnd.choice([0,90,180,270,30,60,120,150,210,240,300,330]) if name!='TRI_CLUSTER' else rnd.choice([0,30,60,90,120,150,180])
            lo,hi,bot,top=limits(shapes[name],angle)
            if hi>lo and top>bot:break
        else:raise RuntimeError('shape does not fit board '+name)
        st[name]=(rnd.uniform(lo,hi),rnd.uniform(bot,top),angle)
    return st

def optimize_group(names,index):
    buff={n:shapes[n].buffer(GAP/2) for n in names}
    rnd=random.Random(9123+index)
    best=None;best_pen=float('inf')
    timer=time.time()
    for repeat in range(7):
        st=seed_group(names,index+repeat*10)
        pen=objective(st,names,buff)
        T=400.
        for step in range(26000):
            n=rnd.choice(names);x,y,theta=st[n]
            if rnd.random()<.13:
                aa=rnd.uniform(0,360)
                lo,hi,bot,top=limits(buff[n],aa)
                if hi<lo or top<bot:continue
                nx=rnd.uniform(lo,hi);ny=rnd.uniform(bot,top)
            else:
                aa=theta+rnd.uniform(-15,15)
                lo,hi,bot,top=limits(buff[n],aa)
                if hi<lo or top<bot:continue
                nx=min(max(x+rnd.uniform(-65,65),lo),hi)
                ny=min(max(y+rnd.uniform(-90,90),bot),top)
            nextst=st.copy();nextst[n]=(nx,ny,aa)
            pn=objective(nextst,names,buff)
            if pn<pen or rnd.random()<math.exp(min(0.,(pen-pn)/max(T,1e-6))):
                st=nextst;pen=pn
                if pen<best_pen:
                    best,best_pen=st.copy(),pen
                    if best_pen<1e-7:
                        print('fit board',index,'restart',repeat,'step',step,flush=True)
                        return best,best_pen
            T*=.99979
        print('trial',index,repeat,'best',best_pen,'secs',round(time.time()-timer,2),flush=True)
    return best,best_pen

sheet_groups=[]
for idx,names in enumerate(groups,1):
    st,pen=optimize_group(names,idx)
    if pen>1e-6:raise RuntimeError(f'Sheet {idx} not nested: penalty={pen}')
    its=[]
    for n in names:
        if n!='TRI_CLUSTER':
            polygon,lines,_=cut[n];tr=transformed(polygon,*st[n]);
            a=rotate(polygon,st[n][2],origin=(0,0));b=a.bounds
            dx,dy=(st[n][0]-b[0],st[n][1]-b[1])
            its.append({'name':n,'geometry':tr,'cutlines':[translate(rotate(ln,st[n][2],origin=(0,0)),dx,dy) for ln in lines],'placement':st[n]})
        else:
            name='LOWER_TRIANGLE_ONE_PIECE_6MM';poly=tri;ref=shapes[n]
            rotref=rotate(ref,st[n][2],origin=(0,0));rb=rotref.bounds
            dx,dy=st[n][0]-rb[0],st[n][1]-rb[1]
            for n2,p2 in [(name,tri),('CENTRAL_FLAT_6MM_SPIDER',sp_in)]:
                pp=translate(rotate(p2,st[n][2],origin=(0,0)),dx,dy)
                its.append({'name':n2,'geometry':pp,'cutlines':[],'placement':st[n]})
    sheet_groups.append((f'BIRCH6_S{idx:02d}_440x850',its))
# 4mm: six 118.333x60 sectors, two across x and 3 rows.
items4=[]
for i in range(1,7):
    name=f'RIM_{i:02d}_BIRCH4_UPPER_LOWER_TABS';poly,lines,_=cut[name]
    dx=5+(i-1)%2*(arc+7);dy=5+(i-1)//2*68
    items4.append({'name':name,'geometry':translate(poly,dx,dy),'cutlines':[translate(ln,dx,dy) for ln in lines],'placement':(dx,dy,0)})
sheet_groups.append(('BIRCH4_S01_440x850',items4))

ids=[i['name'] for _,items in sheet_groups for i in items]
assert len(ids)==len(set(ids))==22 and set(ids)==set(cut)
qa={'project':'PST-230','version':'V1-CAD-NESTING','status':'DESIGN_ONLY / DIGITAL_NESTING_PASS / PHYSICAL_HOLD',
 'top_diameter_mm':230,'total_height_mm':550,'board_size_mm':[440,850],
 'parts':len(ids),'required_min_gap_mm':GAP,'required_stock_margin_mm':MARGIN,'sheets':[],'closed_contours':0,'bend_lines':0,
 'rim_developed_length_per_sector_mm':arc,'rim_developed_total_length_mm':arc*6,
 'stock_material':['6mm birch','4mm birch'],'physical_strength_qualified':False}
for stem,items in sheet_groups:
    mind=1e9;pair=None; margin=1e9
    for it in items:
        g=it['geometry'];b=g.bounds
        margin=min(margin,b[0],b[1],W-b[2],H-b[3])
        assert margin>=MARGIN-1e-4,(stem,'stock margin',margin,it['name'])
        assert all(g.covers(l) for l in it['cutlines']),(stem,'kerf not covered')
    for a,b in itertools.combinations(items,2):
        d=a['geometry'].distance(b['geometry'])
        if d<mind:mind=d;pair=(a['name'],b['name'])
    assert mind>=GAP-1e-4,(stem,mind,pair)
    nc=sum(1+len(it['geometry'].interiors) for it in items);nk=sum(len(it['cutlines']) for it in items)
    qa['closed_contours']+=nc;qa['bend_lines']+=nk
    write_svg_dxf(stem,items,ROOT/'nesting',W,H)
    qa['sheets'].append({'name':stem,'part_names':[it['name'] for it in items], 'part_count':len(items),'minimum_clearance_mm':round(mind,5),'minimum_stock_margin_mm':round(margin,5),'closed_contours':nc,'bend_lines':nk})

# Independent file re-open validates layer and geometry entity counts.
for stem,items in sheet_groups:
    e=list(ezdxf.readfile(ROOT/'nesting'/(stem+'.dxf')).modelspace())
    count=sum(1+len(it['geometry'].interiors)+len(it['cutlines']) for it in items)
    assert len(e)==count,(stem,len(e),count)
    r=ET.parse(ROOT/'nesting'/(stem+'.svg')).getroot()
    ns='{http://www.w3.org/2000/svg}'
    assert len(r.findall('.//'+ns+'g[@id]'))==len(items)
    assert all(el.dxftype() in ('LWPOLYLINE','LINE') for el in e)
    assert all(el.dxf.layer in ('CUT_OUTER','CUT_INNER','CUT_KERF_LINE') for el in e)
    assert all(el.closed for el in e if el.dxftype()=='LWPOLYLINE')
( ROOT/'qa'/'NESTING_QA.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False))
# BOM, placements
with (ROOT/'PLACEMENTS.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['sheet','name','x_mm','y_mm','angle_deg'])
    for stem,items in sheet_groups:
        for it in items:w.writerow([stem,it['name'],*it['placement']])
with (ROOT/'BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['part_name','thickness_mm','count'])
    for n in sorted(cut):w.writerow([n,4 if n.startswith('RIM') else 6,1])
# preview
fig,axes=plt.subplots(1,len(sheet_groups),figsize=(13,10),layout='constrained')
for ax,(stem,items) in zip(axes,sheet_groups):
    ax.set_xlim(0,W);ax.set_ylim(H,0);ax.set_aspect('equal');ax.set_title(stem,fontsize=10)
    ax.add_patch(plt.Rectangle((0,0),W,H,fill=False,color='black'))
    for j,it in enumerate(items):
        g=it['geometry'];ax.add_patch(PolygonPatch(list(g.exterior.coords),facecolor=plt.cm.tab20(j%20),alpha=.46,edgecolor='black',linewidth=.4))
        for hole in g.interiors:ax.add_patch(PolygonPatch(list(hole.coords),facecolor='white',edgecolor='black',linewidth=.4))
        for ln in it['cutlines']:
            xs,ys=ln.xy;ax.plot(xs,ys,'k-',linewidth=.19)
        if not stem.startswith('BIRCH4'):
            x,y=g.representative_point().coords[0];ax.text(x,y,it['name'].replace('_6MM','').replace('_D230','').replace('_ONE_PIECE',''),fontsize=5,ha='center')
    ax.set_xticks([0,220,440]);ax.set_yticks([0,200,400,600,850]);ax.grid(alpha=.12)
fig.savefig(ROOT/'preview'/'ALL_SHEETS.png',dpi=160);plt.close(fig)
for stem,items in sheet_groups:
    fig,ax=plt.subplots(figsize=(6,10));ax.set_xlim(0,W);ax.set_ylim(H,0);ax.set_aspect('equal');ax.set_title(stem)
    ax.add_patch(plt.Rectangle((0,0),W,H,fill=False,color='black'))
    for j,it in enumerate(items):
        g=it['geometry'];ax.add_patch(PolygonPatch(list(g.exterior.coords),facecolor=plt.cm.tab20(j),alpha=.45,edgecolor='black',linewidth=.4))
        for hole in g.interiors:ax.add_patch(PolygonPatch(list(hole.coords),facecolor='white',edgecolor='black'))
        for ln in it['cutlines']:
            x,y=ln.xy;ax.plot(x,y,'k-',linewidth=.2)
    fig.savefig(ROOT/'preview'/(stem+'.png'),dpi=150);plt.close(fig)
print('NESTED',len(ids),'SHEETS',len(sheet_groups),'BENDS',qa['bend_lines'],'CONTOURS',qa['closed_contours'],flush=True)
for x in qa['sheets']:print(x['name'],x['part_count'],x['minimum_clearance_mm'],flush=True)