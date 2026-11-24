"""R18-A visual model reconciliation only. Not CAD manufacturing geometry.
Usage for digital review: python review_model.py path/to/R16_BODY_VISUAL_ONLY.glb
No mating profiles, lock geometry, toolpaths, or load claims.
"""
import sys, csv, json, re, hashlib
from pathlib import Path
import numpy as np
import trimesh
from scipy.spatial import ConvexHull

OUT=Path(__file__).resolve().parent
TARGET_LAYER_MM=4.0
TARGET_HEIGHT_MM=400.0
COLORS={'walls':[(210,173,117,255),(237,209,163,255)],'diaphragm':[(222,140,66,255)],'cap':[(150,115,78,255),(178,139,93,255)],'rail':[(48,145,153,255)],'stretcher':[(196,162,111,255),(219,189,144,255)],'gusset':[(185,142,95,255),(216,180,129,255)]}

def load_world(path):
    scene=trimesh.load(path,force='scene'); result={}
    for name in scene.graph.nodes_geometry:
        matrix,geom=scene.graph[name]; m=scene.geometry[geom].copy(); m.apply_transform(matrix);m.vertices*=1000;m.merge_vertices();m.remove_unreferenced_vertices();result[name]=m
    return result

def width(m):
    hull=ConvexHull(m.vertices); ns=hull.equations[:,:3]; spans=np.ptp(m.vertices@ns.T,axis=0); k=np.argmin(spans); n=ns[k]; n=n if n[np.argmax(abs(n))]>=0 else -n
    return float(spans[k]),n

def project_width(m,n,newwidth,delta=0.,keep_z=False):
    # Visualization transform; does not produce mating profiles.
    c=m.copy();v=c.vertices;vals=v@n;mid=(vals.min()+vals.max())/2; w=np.ptp(vals)
    direction=n.copy()
    if keep_z: direction[2]=0
    direction/=direction@n
    c.vertices=v+np.outer((vals-mid)*(newwidth/w-1)+delta,direction)
    return c

def main(src):
    source=load_world(src); output={}; family={}; parent={}; sources={}; split_axes={}; added=[]
    def add(n,m,f,p,origin,index=0):
        m.visual.face_colors=COLORS[f][index%len(COLORS[f])]; output[n]=m;family[n]=f;parent[n]=p;sources[n]=origin
    for n,m in sorted(source.items()):
        w,axis=width(m)
        if '_W_' in n:
            p=n.replace('CONCEPT_','A01A02_');split_axes[p]=axis
            for j,d in enumerate([-TARGET_LAYER_MM/2,TARGET_LAYER_MM/2]):
                add(p+f'_P{j+1}',project_width(m,axis,TARGET_LAYER_MM,d,True),'walls',p,n,j)
        elif '_D_' in n:
            p=n.replace('CONCEPT_','A03_'); add(p,project_width(m,axis,TARGET_LAYER_MM),'diaphragm',p,n)
        elif n.startswith('REFERENCE_A04'):
            p=n.removeprefix('REFERENCE_').rsplit('-P',1)[0];j=int(n[-1])-1
            v=m.copy();v.vertices[:,2]=(v.vertices[:,2]-v.bounds[0,2])*TARGET_LAYER_MM/np.ptp(v.vertices[:,2])+j*TARGET_LAYER_MM
            add(p+f'_P{j+1}',v,'cap',p,n,j)
        elif n.startswith('VISUAL_UPPER'):
            p=n.replace('VISUAL_UPPER_FLAT','B16_RAIL');add(p,m.copy(),'rail',p,n)
        elif n.startswith('REFERENCE_C01') or n.startswith('REFERENCE_E01'):
            p=n.removeprefix('REFERENCE_').rsplit('-P',1)[0];j=int(n[-1])-1
            add(p+f'_P{j+1}',m.copy(),'stretcher' if 'C01' in p else 'gusset',p,n,j)
        else: raise ValueError(n)
    # Third diaphragm: visual placeholder only, centered between the two existing locations.
    for i in range(1,5):
        a=f'A03_LEG{i}_D_LOW'; b=f'A03_LEG{i}_D_HIGH'; p=f'A03_LEG{i}_D_MID_REVIEW';m=output[a].copy();m.apply_translation((output[b].bounds.mean(axis=0)-output[a].bounds.mean(axis=0))/2);add(p,m,'diaphragm',p,'interpolated visual placeholder');added.append(p)
    # GLB files are in meters. Keep transforms separate from model definition.
    def export(path,exploded=False):
        scene=trimesh.Scene()
        for n,m in output.items():
            copy=m.copy()
            if exploded:
                center=copy.bounds.mean(axis=0);off=np.array([center[0]*.30,center[1]*.30,(center[2]-200)*.08]);
                if parent[n] in split_axes: off+=split_axes[parent[n]]*(10 if n.endswith('P2') else -10)
                copy.apply_translation(off)
            copy.vertices/=1000; scene.add_geometry(copy,node_name=n,geom_name=n)
        path.write_bytes(scene.export(file_type='glb'))
    glb=OUT/'R18A_BODY_REVIEW.glb';export(glb);export(OUT/'R18A_EXPLODED_REVIEW.glb',True)
    readback=load_world(glb); rows=[]
    for n,m in sorted(readback.items()):
        w,_=width(m);rows.append({'id':n,'family':family[n],'component':parent[n],'source':sources[n],'width_mm':round(w,6),'width_pass':abs(w-TARGET_LAYER_MM)<.01,'closed':bool(m.is_watertight),'z_min_mm':round(float(m.bounds[0,2]),6),'z_max_mm':round(float(m.bounds[1,2]),6),'status':'VISUAL_PLACEHOLDER' if n in added else 'REVIEW_GEOMETRY'})
    def csvwrite(path,rows):
        with path.open('w',newline='',encoding='utf-8-sig') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    csvwrite(OUT/'R18A_LAYER_QA.csv',rows)
    # Conservatively test convex projection separation of adjacent rail groups;
    # positive separation proves lack of contact, nonpositive cannot prove contact.
    leg_groups={i:[m for n,m in readback.items() if n.startswith(f'A01A02_LEG{i}_')] for i in range(1,5)}
    def separating_gap(v,w):
        h1=ConvexHull(v);h2=ConvexHull(w);ns=np.concatenate([h1.equations[:,:3],h2.equations[:,:3],np.eye(3)])
        p=v@ns.T;q=w@ns.T
        return float(max(np.max(q.min(0)-p.max(0)),np.max(p.min(0)-q.max(0))))
    interfaces=[]
    for i in range(1,5):
        for typ in ['upper','lower']:
            names=[n for n in readback if n==f'B16_RAIL_{i}'] if typ=='upper' else [n for n in readback if n.startswith(f'C01-LOWER-STRETCHER-{i}-')]
            verts=np.concatenate([readback[n].vertices for n in names]);
            for leg in [i,i%4+1]:
                vv=np.concatenate([m.vertices for m in leg_groups[leg]]);g=separating_gap(verts,vv)
                interfaces.append({'interface':f'{typ}-{i}-leg-{leg}','screen_gap_mm':round(g,6),'status':'FAIL_SEPARATED' if g>.01 else 'UNRESOLVED_NO_CONTACT_PROOF','method':'convex projection screen only'})
    csvwrite(OUT/'R18A_INTERFACE_SCREEN.csv',interfaces)
    allv=np.concatenate([m.vertices for m in readback.values()]);result={'source_sha256':hashlib.sha256(Path(src).read_bytes()).hexdigest(),'source_nodes':len(source),'output_layers':len(rows),'planned_layers':104,'component_count':len(set(parent.values())),'planned_components':60,'undefined_lock_layers':16,'width_pass':sum(r['width_pass'] for r in rows),'closed_pass':sum(r['closed'] for r in rows),'floor_cap_layers_at_zero':sum(r['family']=='cap' and abs(r['z_min_mm'])<.01 for r in rows),'floor_wall_layers_at_zero':sum(r['family']=='walls' and abs(r['z_min_mm'])<.01 for r in rows),'bounds_mm':[allv.min(0).tolist(),allv.max(0).tolist()],'separated_interfaces':sum(r['status']=='FAIL_SEPARATED' for r in interfaces),'unresolved_interfaces':sum(r['status']!='FAIL_SEPARATED' for r in interfaces),'full_overlap':'NOT_RUN','assembly_paths':'NOT_RUN','structural':'NOT_RUN','manufacturing':'BLOCKED','review_only':True}
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main(sys.argv[1])
