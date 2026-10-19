"""Independent CTB003 review from SVG/DXF exports, without implementation imports."""
import json, math, itertools, sys, xml.etree.ElementTree as ET
from pathlib import Path
import cadquery as cq
from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import translate
from shapely.ops import unary_union
ROOT=next((p for p in Path(__file__).resolve().parents if (p/'projects/CTB-01/parts/P03').is_dir()), Path('/workspace/assembl-lab-engineering'))
PART=ROOT/'projects/CTB-01/parts/P03'
P02=ROOT/'projects/CTB-01/parts/P02'


def svg_polygons(path):
    root=ET.parse(path).getroot()
    loops=[]
    for n in root.findall('.//{http://www.w3.org/2000/svg}polygon'):
        if n.attrib.get('points'):
            loops.append([(float(a),float(b)) for a,b in [v.split(',') for v in n.attrib['points'].split()]])
    assert loops, path
    p=Polygon(loops[0],loops[1:]); assert p.is_valid and p.area>0,(path,p.is_valid)
    return p


def planar(poly,plane,h):
    assert poly.geom_type=='Polygon'
    wp=cq.Workplane(plane).polyline(list(poly.exterior.coords)[:-1]).close()
    for ring in poly.interiors:wp=wp.polyline(list(ring.coords)[:-1]).close()
    x=wp.extrude(h).val(); assert x.isValid()
    return x


def plate(poly,z=407,h=6):
    return planar(poly,cq.Plane(origin=(0,0,z),xDir=(1,0,0),normal=(0,0,1)),h)


def cheek(poly,top_t=13.5,h=6):
    return planar(poly,cq.Plane(origin=(0,top_t,0),xDir=(1,0,0),normal=(0,-1,0)),h)


def rotate(s,theta):return s.rotate((0,0,0),(0,0,1),theta)


def sweep2(poly,dx=0,dy=0):
    # Independent boundary-prism construction, including every hole boundary.
    pieces=[poly,translate(poly,xoff=dx,yoff=dy)]
    for ring in [poly.exterior,*poly.interiors]:
        coords=list(ring.coords)
        for a,b in zip(coords,coords[1:]):
            q=Polygon([a,b,(b[0]+dx,b[1]+dy),(a[0]+dx,a[1]+dy)])
            if q.area>1e-10:pieces.append(q)
    r=unary_union(pieces);assert r.is_valid
    return r


def volume(a,b):
    x=a.BoundingBox();y=b.BoundingBox()
    if any(getattr(x,k+'max')<getattr(y,k+'min')-1e-9 or getattr(y,k+'max')<getattr(x,k+'min')-1e-9 for k in 'xyz'):return 0.
    v=abs(a.intersect(b).Volume()); assert math.isfinite(v)
    return v


def solids(face,Y,stations):
    out={'P03':plate(Y)}
    for leg,theta in enumerate([0,120,240],1):
        out[f'L{leg}_P01_minus']=rotate(cheek(face,-7.5),theta)
        out[f'L{leg}_P01_plus']=rotate(cheek(face,13.5),theta)
        for s in stations:
            p=translate(svg_polygons(P02/f"variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
            out[f"L{leg}_{s['id']}"]=rotate(plate(p,s['z_mm']-3),theta)
    assert len(out)==19
    return out


def yfirst(face,Y,stations):
    fixed={'P03':plate(Y)};results=[]
    for leg,theta in enumerate([0,120,240],1):
        # Start minus cheek 40 mm outboard of its negative tangential side.
        name=f'L{leg}_P01_minus';swept=rotate(cheek(face,-7.5,46),theta)
        row={'moving':name,'fixed_count':len(fixed),'intersections':{n:volume(swept,x) for n,x in fixed.items()}}
        results.append(row);fixed[name]=rotate(cheek(face,-7.5),theta)
        for s in stations:
            name=f"L{leg}_{s['id']}";p=translate(svg_polygons(P02/f"variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
            swept=rotate(plate(sweep2(p,dy=40),s['z_mm']-3),theta)
            row={'moving':name,'fixed_count':len(fixed),'intersections':{n:volume(swept,x) for n,x in fixed.items()}}
            results.append(row);fixed[name]=rotate(plate(p,s['z_mm']-3),theta)
        name=f'L{leg}_P01_plus';swept=rotate(cheek(face,53.5,46),theta)
        row={'moving':name,'fixed_count':len(fixed),'intersections':{n:volume(swept,x) for n,x in fixed.items()}}
        results.append(row);fixed[name]=rotate(cheek(face,13.5),theta)
    assert len(results)==18 and sum(r['fixed_count'] for r in results)==171
    return results


def module_route(face,Y,stations,dx=0,dt=0,dz=0):
    # One complete leg translated from an outboard/vertical start to final.
    # Exact 2D polygon sweeps + orthogonal extrusion, not sampled frames.
    assert sum(x!=0 for x in [dx,dt,dz])==1
    sw=[]
    for t in [-7.5,13.5]:
        if dt: sw.append(cheek(face,t+max(0,dt),6+abs(dt)))
        else: sw.append(cheek(sweep2(face,dx=dx,dy=dz),t))
    for s in stations:
        p=translate(svg_polygons(P02/f"variants/B_THROUGH_ADHESIVE/{s['part']}.svg"),xoff=s['r_mm'])
        if dz: sw.append(plate(p,s['z_mm']-3+min(0,dz),6+abs(dz)))
        else: sw.append(plate(sweep2(p,dx=dx,dy=dt),s['z_mm']-3))
    fixed={'P03':plate(Y)};out=[]
    final=solids(face,Y,stations)
    for leg,theta in enumerate([0,120,240],1):
        out.append({'leg':leg,'intersections':{f'{j}:{n}':volume(rotate(x,theta),y) for j,x in enumerate(sw) for n,y in fixed.items()}})
        for n,x in final.items():
            if n.startswith(f'L{leg}_'):fixed[n]=x
    return out


if __name__=='__main__':
    from types import SimpleNamespace
    import ezdxf,trimesh
    from shapely.geometry import box
    from shapely.affinity import rotate as shapely_rotate
    q=SimpleNamespace(**globals())
    result={'method':'Actual SVG polygon loops, independent boundary-edge sweeps, CadQuery/OpenCASCADE solid kernel; no CTB source imports','variants':{}}
    for name in ['A_COMPACT_CLOSED','B_DUAL_CLOSED','C_OPEN_REMOVABLE']:
        data=json.loads((q.PART/f'variants/{name}/mechanical-dimensions.json').read_text());stations=data['stations']
        face=q.svg_polygons(q.PART/f'variants/{name}/P01-Y-mortise-study-v1.svg');Y=q.svg_polygons(q.PART/f'variants/{name}/P03.svg')
        assembled=q.solids(face,Y,stations)
        pair=[{'a':a,'b':b,'volume_mm3':q.volume(x,y)} for (a,x),(b,y) in itertools.combinations(assembled.items(),2)]
        assert len(pair)==171
        assert max(x['volume_mm3'] for x in pair)<1e-6,(name,'final',max(x['volume_mm3'] for x in pair))
        print(name,'19valid /171final PASS',flush=True)
        yfirst=q.yfirst(face,Y,stations)
        assert max(v for row in yfirst for v in row['intersections'].values())<1e-6,(name,'yfirst')
        print(name,'18stages /171Yfirst PASS',flush=True)
        routes={}
        for axis,args in [('radial',{'dx':60}),('tangential',{'dt':40}),('vertical',{'dz':80})]:
            rows=q.module_route(face,Y,stations,**args)
            vals=[v for row in rows for v in row['intersections'].values()]
            assert len(vals)==126
            worst=max(vals)
            if name=='C_OPEN_REMOVABLE' and axis=='radial':assert worst<1e-6,(name,axis,worst)
            else:assert worst>1,(name,axis,worst)
            print(name,axis,'max',worst,flush=True)
            routes[axis]={'checks':126,'max_volume_mm3':worst,'rows':rows}
        result['variants'][name]={'solid_volumes_mm3':{n:s.Volume() for n,s in assembled.items()},'final':pair,'yfirst':yfirst,'prebuilt':routes,'max_global_radius_mm':max(math.hypot(x,y) for x,y in Y.exterior.coords),'Y_area_mm2':Y.area,'cheek_area_mm2':face.area,'cheek_holes':len(face.interiors),'cheek_solids':len(q.cheek(face).Solids())}
    Path('/tmp/ctb003-independent-occ-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('All independent OCC main path checks passed',flush=True)

    result={}
    base=q.svg_polygons(q.P02/'variants/B_THROUGH_ADHESIVE/P01-SOFT_CURVE-mortise-study-v1.svg')
    original=q.svg_polygons(q.ROOT/'projects/CTB-01/parts/P01/variants/SOFT_CURVE/profile.svg')
    for name in ['A_COMPACT_CLOSED','B_DUAL_CLOSED','C_OPEN_REMOVABLE']:
        result[name]={}
        for label in ['P03','P01-Y-mortise-study-v1']:
            svg=q.svg_polygons(q.PART/f'variants/{name}/{label}.svg')
            doc=ezdxf.readfile(q.PART/f'variants/{name}/{label}.dxf');assert doc.header['$INSUNITS']==4
            loops=[]
            for e in doc.modelspace().query('LWPOLYLINE'):
                assert e.closed
                ring=[(v[0],v[1]) for v in e.get_points()]
                assert len(ring)==len(set(ring)),(name,label,'duplicate vertex')
                loops.append(ring)
            poly=Polygon(loops[0],loops[1:]);assert poly.is_valid
            delta=poly.symmetric_difference(svg).area;assert delta<1e-5,(name,label,delta)
            assert abs(poly.area-svg.area)<1e-5
            assert poly.geom_type=='Polygon'
            assert poly.bounds[2]-poly.bounds[0]+20<=440 and poly.bounds[3]-poly.bounds[1]+20<=800
            result[name][label]={'closed_loops':len(loops),'units':'mm','valid':True,'svg_dxf_area_delta_mm2':delta,'area_mm2':svg.area,'bounds_mm':list(svg.bounds)}
        y=q.svg_polygons(q.PART/f'variants/{name}/P03.svg');face=q.svg_polygons(q.PART/f'variants/{name}/P01-Y-mortise-study-v1.svg')
        delta=y.symmetric_difference(shapely_rotate(y,120,origin=(0,0))).area;assert delta<0.0002,(name,'rotation',delta)
        for h in base.interiors:
            p=Polygon(h)
            assert any(p.symmetric_difference(Polygon(v)).area<1e-7 for v in face.interiors),(name,'changed spacer mortise')
        outer_preserved=Polygon(face.exterior).symmetric_difference(original).area
        if name!='C_OPEN_REMOVABLE':assert outer_preserved<1e-7
        result[name]['rotation_area_delta_mm2']=delta
        result[name]['B_spacer_mortises_unchanged']=True
        result[name]['external_silhouette_change_mm2']=outer_preserved
        result[name]['Y_global_max_radius_mm']=max(math.hypot(x,y) for x,y in y.exterior.coords)
        assert result[name]['Y_global_max_radius_mm']<=86
    # The GLB convention is metres, apply every scene node transform before checking.
    scene=trimesh.load(q.PART/'assembly/three-leg-base-DESIGN_ONLY.glb',force='scene')
    meshes={}
    for node in scene.graph.nodes_geometry:
        tf,geom=scene.graph[node];m=scene.geometry[geom].copy();m.apply_transform(tf);m.apply_scale(1000)
        assert m.is_watertight and m.volume>0
        meshes[node]={'geometry':geom,'volume_mm3':float(m.volume),'bounds_mm':m.bounds.tolist()}
    assert len(meshes)==19
    result['GLB']={'nodes':meshes,'bounds_mm':(scene.bounds*1000).tolist(),'watertight_parts':19}
    Path('/tmp/ctb003-independent-export-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('DXF/SVG/units/loops/sheet/unchanged B mortises and19watertight GLB nodes PASS')

    folder=q.PART/'variants/A_COMPACT_CLOSED';face=q.svg_polygons(folder/'P01-Y-mortise-study-v1.svg');y=q.svg_polygons(folder/'P03.svg')
    # Wrong source thickness in the actual Y part, retaining nominal cheek holes.
    oversize=q.plate(y,z=406.6,h=6.8)
    v=q.volume(oversize,q.cheek(face,-7.5));assert v>1
    # Bridge cut across full upper neck: actual material disconnects into two parts.
    severed=face.difference(box(30,406.8,95,413.2));assert severed.geom_type=='MultiPolygon' and len(severed.geoms)==2
    # Move only the exported Y-hole (B spacer holes unchanged) to the wrong radial position.
    holes=[]
    for h in face.interiors:
     p=Polygon(h)
     if p.centroid.y>400:p=q.translate(p,xoff=4)
     holes.append(p)
    wrong=Polygon(face.exterior.coords,[list(h.exterior.coords) for h in holes])
    v2=q.volume(q.plate(y),q.cheek(wrong,-7.5));assert v2>1
    # Compare all19 exported GLB node volumes against independent OCC.
    r=json.loads(Path('/tmp/ctb003-independent-occ-results.json').read_text())['variants']['A_COMPACT_CLOSED']['solid_volumes_mm3']
    e=json.loads(Path('/tmp/ctb003-independent-export-results.json').read_text())['GLB']['nodes']
    diffs={}
    for name,data in e.items():
     mapped=name.replace('_P01_1','_P01_minus').replace('_P01_2','_P01_plus')
     diffs[name]=abs(data['volume_mm3']-r[mapped]);assert diffs[name]/r[mapped]<5e-6,(name,diffs[name])
    out={'6.8mm_Y_against_nominal_cheek_collision_mm3':v,'severed_neck_material_components':len(severed.geoms),'Y_mortise_shifted4mm_collision_mm3':v2,'GLB_OCC_volume_difference_mm3':diffs,'GLB_OCC_max_volume_difference_mm3':max(diffs.values())}
    Path('/tmp/ctb003-independent-negative-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

    out={}
    for name in ['A_COMPACT_CLOSED','B_DUAL_CLOSED','C_OPEN_REMOVABLE']:
     f=q.PART/f'variants/{name}'
     Y=q.svg_polygons(f/'P03.svg');face=q.svg_polygons(f/'P01-Y-mortise-study-v1.svg');data=json.loads((f/'mechanical-dimensions.json').read_text());assembled=q.solids(face,Y,data['stations'])
     out[name]={}
     for axis,swept in [('vertical',q.plate(Y,407,86)),('global_X',q.plate(q.sweep2(Y,dx=60)))]:
      vals={n:q.volume(swept,s) for n,s in assembled.items() if n!='P03'}
      assert len(vals)==18 and max(vals.values())>100
      out[name][axis]={'checks':18,'max_volume_mm3':max(vals.values()),'intersections':vals}
      print(name,axis,max(vals.values()),flush=True)
    Path('/tmp/ctb003-independent-central-results.json').write_text(json.dumps(out,indent=2)+'\n')
