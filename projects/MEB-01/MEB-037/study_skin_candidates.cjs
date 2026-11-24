// Reproducible digital comparison; no cutting or manufacturing output.
// Usage: node study_skin_candidates.cjs original.svg MEB037_REFERENCE_QA.json R6_MEB032_SOURCE_88.json
const fs = require('node:fs');
function study(svg,qa,slits){
const p={};for(const g of svg.matchAll(/<g id="([^"]+)"[^>]*>([\s\S]*?)<\/g>/g)){let a=[...g[2].matchAll(/<polyline[^>]*points="([^"]+)"/g)].map(m=>m[1].trim().split(/\s+/).map(v=>v.split(",").map(Number)));let lo=[Math.min(...a[0].map(v=>v[0])),Math.min(...a[0].map(v=>v[1]))];p[g[1]]=a.map(b=>{let c=b.map(v=>v.map((w,i)=>+(w-lo[i]).toFixed(8)));if(Math.hypot(c[0][0]-c.at(-1)[0],c[0][1]-c.at(-1)[1])<1e-6)c.pop();return c});}
const c=qa.contact_curve,W=c.developed_mm,S=84.77646323552999;
const area=a=>a.length<3?0:a.reduce((sum,v,i)=>sum+v[0]*a[(i+1)%a.length][1]-v[1]*a[(i+1)%a.length][0],0)/2;
const cross=(a,b,c)=>(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
function clip(subject,convex){let p=subject;for(let i=0;i<convex.length;i++){const a=convex[i],b=convex[(i+1)%convex.length];let out=[];if(!p.length)return out;let prev=p.at(-1),dp=cross(a,b,prev);for(const x of p){let d=cross(a,b,x);if((d>=0)!==(dp>=0)){let t=dp/(dp-d);out.push([prev[0]+t*(x[0]-prev[0]),prev[1]+t*(x[1]-prev[1])]);}if(d>=0)out.push(x);prev=x;dp=d;}p=out;}return p;}
const point=(s,r)=>[c.center_depth_mm+r*Math.sin(s/c.radius_neutral_mm-c.half_angle_rad),c.center_height_mm+r*Math.cos(s/c.radius_neutral_mm-c.half_angle_rad)];
function wedges(a,b,step){const n=Math.ceil((b-a)/step);const r=c.radius_inner_mm;let out=[];for(let i=0;i<n;i++){const s=a+(b-a)*i/n,t=a+(b-a)*(i+1)/n;let v=[point(s,r),point(t,r),point(t,r+4),point(s,r+4)];if(area(v)<0)v.reverse();out.push(v);}return out;}
const rect=(y0,y1,z0,z1)=>[[y0,z0],[y1,z0],[y1,z1],[y0,z1]];
function sections(loops,x){let ys=[];for(const poly of loops)for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length];if((a[0]<=x&&x<b[0])||(b[0]<=x&&x<a[0]))ys.push(a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0]));}ys.sort((a,b)=>a-b);return ys.filter((_,i)=>i%2===0).map((v,i)=>[v,ys[2*i+1]]);}
const xPrisms=[],yPrisms=[],zPrisms=[];
const xp=(name,x0,x1,fn)=>xPrisms.push({name,x0,x1,loops:p[name].map(a=>a.map(fn))});
const yp=(name,y0,y1,fn)=>yPrisms.push({name,y0,y1,loops:p[name].map(a=>a.map(fn))});
for(const [side,end,sign] of [["L",0,1],["R",324,-1]]){
 xp("LID_END_"+side,Math.min(end,end+sign*4),Math.max(end,end+sign*4),([u,v])=>[u,64.5+v]);
 xp("BODY_END_"+side,Math.min(end,end+sign*4),Math.max(end,end+sign*4),v=>v);
 for(const [stem,layer] of [["FASCIA_HIDDEN_BACKER",1],["OUTER_FASCIA",2]]){let name=stem+"_"+side,a=p[name][1],zmax=Math.max(...p[name][0].map(v=>v[0])),v=(Math.min(...a.map(v=>v[1]))+Math.max(...a.map(v=>v[1])))/2;let x=end-sign*layer*4;xp(name,Math.min(x,x+sign*4),Math.max(x,x+sign*4),([u,w])=>[75+w-v,zmax-u]);}
 yp("CAPTIVE_PIN_"+side,73,77,([u,v])=>[end+sign*((side==="L"?u:12.5-u)-8),70+v]);
}
yp("BODY_FRONT",0,4,v=>v);yp("BODY_BACK",73,77,v=>v);
for(const [name,y] of [["LID_FRONT_RAIL",32],["LID_BACK_RAIL",45]])yp(name,y-2,y+2,([u,v])=>[u+.8,v+83]);
for(const [i,start] of [[1,104],[2,214]])xp("LID_CROSS_RIB_"+i,.8+start+.2,.8+start+4.2,([u,v])=>[u+5,83+7-13.25+v]);
const rail=p.LID_FRONT_RAIL[0];let pockets=[];for(let i=0;i<rail.length;i++){const a=rail[i],b=rail[(i+1)%rail.length];if(a[1]===4.25&&b[1]===4.25)pockets.push([Math.min(a[0],b[0]),Math.max(a[0],b[0])]);}pockets.sort((a,b)=>a[0]-b[0]);for(const [i,side] of ["L","R"].entries()){let [a,b]=pockets[i],x=.8+(a+b-4)/2;xp("INTERNAL_RAIL_SADDLE_"+side,x,x+4,([u,v])=>[27.5+u,83+4.25-9.95+v]);}
zPrisms.push({name:"BODY_FLOOR",z0:0,z1:4,loops:p.BODY_FLOOR});
function audit(bands,step){let out={};for(const part of [...xPrisms,...yPrisms,...zPrisms]){let volume=0;for(const [s0,s1,x0,x1] of bands){let ws=wedges(s0,s1,step);const ar=loops=>ws.reduce((v,w)=>v+loops.reduce((t,p,i)=>t+(i?-1:1)*Math.abs(area(clip(p,w))),0),0);
if("x0" in part){let overlap=Math.min(x1,part.x1)-Math.max(x0,part.x0);if(overlap>0)volume+=overlap*ar(part.loops);}
else{const boundaries=[x0,x1,...part.loops.flatMap(poly=>poly.map(v=>v[0])).filter(v=>x0<v&&v<x1)].sort((a,b)=>a-b);for(let i=0;i<boundaries.length-1;i++){let a=boundaries[i],b=boundaries[i+1];if(b-a<1e-8)continue;const nodes=[.1127016653792583,.5,.8872983346207417],weights=[5/18,8/18,5/18];for(let j=0;j<3;j++){const x=a+(b-a)*nodes[j];for(const [lo,hi] of sections(part.loops,x)){let rectp="y0" in part?rect(part.y0,part.y1,lo,hi):rect(lo,hi,part.z0,part.z1);volume+=(b-a)*weights[j]*ar([rectp]);}}}}
}out[part.name]=+Math.max(0,volume).toFixed(6);}return out;}
const candidates=[
 {id:"reference_straight_316",inset:4,tabDomain:null},
 {id:"clearance_limit_straight",inset:4.5,tabDomain:null},
 {id:"clearance_study_straight",inset:4.75,tabDomain:null},
 {id:"five_tab_full_width_study",inset:4.75,tabDomain:W},
 {id:"five_tab_supported_arc_study",inset:4.75,tabDomain:S}
];
const result=candidates.map(v=>{
 const bands=[[0,W,v.inset,324-v.inset]];
 let tabs=[];
 if(v.tabDomain!==null){tabs=Array.from({length:5},(_,i)=>[i*(v.tabDomain-7)/4,i*(v.tabDomain-7)/4+7]);for(const [a,b] of tabs){bands.push([a,b,v.inset-4,v.inset],[a,b,324-v.inset,328-v.inset]);}}
 const collisions=audit(bands,.05);
 const crossSlits=slits.filter(([a,s,b,t])=>tabs.some(([lo,hi])=>lo<=s&&s<=hi&&((a<=v.inset&&b>=v.inset-4)||(a<=328-v.inset&&b>=324-v.inset)))).length;
 return {id:v.id,nominal_envelope_span_mm:324-2*v.inset,tab_count_per_end:tabs.length,unsupported_tab_domain:v.tabDomain===W,original_r6_lines_crossing_candidate_tab_lands:crossSlits,skin_vs_19_parts_estimated_intersection_mm3:collisions,nonzero:Object.entries(collisions).filter(([k,w])=>w>0.0001),receiver_engagement:"NOT_MODELED"};
});
return {contact_curve:c,verified_original_svg_part_count:Object.keys(p).length,reference_skin_only_pair_count:xPrisms.length+yPrisms.length+zPrisms.length,result};
}
const [svg,qa,r6]=process.argv.slice(2);console.log(JSON.stringify(study(fs.readFileSync(svg,'utf8'),JSON.parse(fs.readFileSync(qa,'utf8')),JSON.parse(fs.readFileSync(r6,'utf8')).segments),null,2));
