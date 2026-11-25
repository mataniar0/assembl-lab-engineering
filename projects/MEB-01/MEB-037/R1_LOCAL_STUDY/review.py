from pathlib import Path
import json, math, csv, itertools
import numpy as np
import cadquery as cq
from shapely.geometry import Polygon
P=Path(__file__).parent
T=4.; L=324.; W=77.; H=75.; R=43.34239130654945; RN=R+2; CENTER=(38.5,52.5923913026939); HALF=math.asin(W/(2*R)); DEV=2*HALF*RN; END=84.77646323552999
VEPS=1e-4; DEPS=1e-5; BEPS=1e-7

def read():
    data=json.loads((P/'source_profiles_compact.json').read_text());result={}
    for name,v in data.items():
        if isinstance(v,str):result[name]=result[v];continue
        loops=[]
        for loop in v:
            pts=[]
            for q in loop:
                if q[0]=='a':
                    _,n,cx,cy,r,a,b=q;pts.extend([(cx+r*math.cos(a+b*i/(n-1)),cy+r*math.sin(a+b*i/(n-1))) for i in range(n)])
                elif q[0]=='c':
                    _,n,axis,cx,cy,r,a,b,sg=q;c=(cx,cy)
                    for i in range(n):
                        x=a+(b-a)*i/(n-1);y=c[1-axis]+sg*math.sqrt(max(0,r*r-(x-c[axis])**2));pts.append((x,y) if axis==0 else (y,x))
                else:pts.append(tuple(q))
            loops.append(np.round(np.array(pts),8))
        result[name]=loops
    return result

def extrude(profile,placement,d):
    wires=[cq.Wire.makePolygon([cq.Vector(*placement(*p)) for p in loop],close=True) for loop in profile]
    return cq.Solid.extrudeLinear(wires[0],wires[1:],cq.Vector(*d))
def point(s,r,x):
    a=s/RN-HALF;return cq.Vector(x,CENTER[0]+r*math.sin(a),CENTER[1]+r*math.cos(a))
def sector(x0,x1,s0,s1,r=R,ro=R+T):
    mid=(s0+s1)/2;p=lambda s,rr:point(s,rr,x0)
    edges=[cq.Edge.makeThreePointArc(p(s0,r),p(mid,r),p(s1,r)),cq.Edge.makeLine(p(s1,r),p(s1,ro)),cq.Edge.makeThreePointArc(p(s1,ro),p(mid,ro),p(s0,ro)),cq.Edge.makeLine(p(s0,ro),p(s0,r))]
    return cq.Solid.extrudeLinear(cq.Wire.assembleEdges(edges),[],cq.Vector(x1-x0,0,0))
def build():
    profiles=read();S={}
    def add(n,f,d):S[n]=extrude(profiles[n],f,d)
    add('BODY_FLOOR',lambda u,v:(u,v,0),(0,0,T))
    for n,y in [('BODY_FRONT',0),('BODY_BACK',W-T)]:add(n,lambda u,v:(u,y,v),(0,T,0))
    for side,x,sign in [('L',0,1),('R',L,-1)]:
        add('BODY_END_'+side,lambda u,v:(x,u,v),(sign*T,0,0))
        add('LID_END_'+side,lambda u,v:(x,u,64.5+v),(sign*T,0,0))
        for k,layers in [('FASCIA_HIDDEN_BACKER',1),('OUTER_FASCIA',2)]:
            n=k+'_'+side;ht=max(profiles[n][0][:,0]);_,y0,_,y1=Polygon(profiles[n][1]).bounds
            add(n,lambda u,v:(x-sign*layers*T,75+v-(y0+y1)/2,ht-u),(sign*T,0,0))
        n='CAPTIVE_PIN_'+side;pw=max(profiles[n][0][:,0]);add(n,lambda u,v:(x+sign*((u if side=='L' else pw-u)-8),73,70+v),(0,T,0))
    for n,y in [('LID_FRONT_RAIL',32),('LID_BACK_RAIL',45)]:add(n,lambda u,v:(.8+u,y-2,83+v),(0,T,0))
    for i,(a,b) in enumerate([(104,108.4),(214,218.4)],1):
        x=.8+(a+b-T)/2;add('LID_CROSS_RIB_'+str(i),lambda u,v:(x,u+5,83+7-13.25+v),(T,0,0))
    for side,(a,b) in zip(['L','R'],[(3,7.4),(315,319.4)]):
        x=.8+(a+b-T)/2;add('INTERNAL_RAIL_SADDLE_'+side,lambda u,v:(x,27.5+u,83+4.25-9.95+v),(T,0,0))
    S['LID_SKIN_RADIAL_4MM']=sector(8,316,DEV-13.38702989,DEV).fuse(sector(0,324,DEV-97.07856594,DEV-13.38702989),sector(8,316,0,DEV-97.07856594),tol=BEPS).clean()
    assert len(S)==20
    return S

def bboxgap(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox();return max([getattr(aa,k+'min')-getattr(bb,k+'max') for k in 'xyz']+[getattr(bb,k+'min')-getattr(aa,k+'max') for k in 'xyz'])
def penetration(a,b):
    if bboxgap(a,b)>DEPS:return 0.
    return sum(abs(s.Volume()) for s in a.intersect(b,tol=BEPS).Solids())
def check(S,dist=True):
    rows=[]
    for a,b in itertools.combinations(S,2):
        g=bboxgap(S[a],S[b]);v=penetration(S[a],S[b]);d=g if g>DEPS else (0. if v>VEPS else S[a].distance(S[b]) if dist else None)
        rows.append([a,b,v,d])
    return rows

def show(rows):return [[a,b,v] for a,b,v,d in rows if v>VEPS]
def save_csv(n,rows):
    with (P/n).open('w',newline='') as f:w=csv.writer(f);w.writerow(['part_a','part_b','positive_intersection_mm3','distance_or_bbox_lower_bound_mm']);w.writerows(rows)
def main():
    S=build();print('source validity',[(n,len(s.Solids()),s.isValid()) for n,s in S.items()],flush=True)
    rows=check(S);save_csv('reference_recheck.csv',rows);print('reference intersections',show(rows),flush=True)
    C=dict(S);C['LID_SKIN_RADIAL_4MM']=sector(4,320,0,DEV);base=check(C);save_csv('straight_baseline_recheck.csv',base);print('straight baseline intersections',show(base),flush=True)
    result={'source':'GitHub MEB033 SVG blob 8644b71371b5c4f02233b65d432ce22136e02199; normalized source profiles reconstructed via compact curve encoding, coordinate tolerance approx 1e-7 mm; not byte-identical source','CAD':cq.__version__,'volume_threshold_mm3':VEPS,'reference_intersections':show(rows),'baseline_intersections':show(base),'part_count':len(C),'pair_count':len(base),'baseline_state':'isolated straight-base hypothesis, no new joinery; not a finished design','release':False}
    (P/'baseline_result.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
