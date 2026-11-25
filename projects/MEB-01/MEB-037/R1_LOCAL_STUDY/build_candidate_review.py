from review import *
import struct
P=Path(__file__).parent
S=build();j=json.loads((P/'candidate_R2_result.json').read_text());tabs=j['candidate_tab_station_intervals_mm'];gap=.125;shoulders=[(tabs[i][1]+gap,tabs[i+1][0]-gap) for i in range(4)];skin='LID_SKIN_RADIAL_4MM'
C=dict(S);C[skin]=sector(4.6,319.4,0,DEV).fuse(*[sector(x0,x1,a,b) for x0,x1 in ((0,4.6),(319.4,324)) for a,b in tabs],tol=BEPS).clean()
for n,x0,x1 in [('LID_END_L',0,4),('LID_END_R',320,324)]:C[n]=S[n].fuse(*[sector(x0,x1,a,b,R-.2,R+T) for a,b in shoulders],tol=BEPS).clean()
move=lambda n:n.startswith(('LID_','INTERNAL_RAIL_SADDLE_'))
opened={n:s.rotate((0,75,75),(1,75,75),-110) if move(n) else s for n,s in C.items()}
center=cq.Vector(162,38.5,50);exploded={n:s.translate((s.Center()-center).multiply(.6)) for n,s in C.items()}
def export(name,solids):
    a=cq.Assembly(name='MEB037_R1_B_'+name)
    for n,s in solids.items():a.add(s,name=n,color=cq.Color(.76,.53,.31) if move(n) else cq.Color(.87,.68,.44))
    a.export(str(P/f'MEB037_R1_B_{name}_DESIGN_ONLY.glb'),tolerance=.05,angularTolerance=.15)
for n,d in [('CLOSED',C),('OPEN_110',opened),('EXPLODED',exploded)]:
    export(n,d)
    f=P/f'MEB037_R1_B_{n}_DESIGN_ONLY.glb'
    data=f.read_bytes();magic,ver,tot,ln,tag=struct.unpack_from('<5I',data)
    doc=json.loads(data[20:20+ln]);root=doc['nodes'][doc['scenes'][doc.get('scene',0)]['nodes'][0]]
    root['scale']=[.001,.001,.001];doc['extras']={'review_status':'DESIGN_ONLY','source_geometry_unit':'mm','gltf_world_unit':'m','R6':'rigid envelope only'}
    h=json.dumps(doc,separators=(',',':')).encode();h+=b' '*((-len(h))%4);tail=data[20+ln:]
    f.write_bytes(struct.pack('<5I',magic,ver,20+len(h)+len(tail),len(h),tag)+h+tail)
a=cq.Assembly(name='MEB037_R1_B_DESIGN_ONLY')
for n,s in C.items():a.add(s,name=n)
a.export(str(P/'MEB037_R1_B_CLOSED_DESIGN_ONLY.step'))
