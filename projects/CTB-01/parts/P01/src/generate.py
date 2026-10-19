"""Generate all exports from the one flattened contour (0.02 mm chord bound)."""
import hashlib
import json
import math
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as Patch, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import Polygon, LineString, MultiPoint, Point

from model import PART, inputs, profile, instances, digest, section


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def write_svg(path, points, bounds, margin, name):
    x0,y0,x1,y1 = bounds
    w,h = x1-x0+2*margin,y1-y0+2*margin
    coords = ' '.join(f'{x:.6f},{y:.6f}' for x,y in points)
    path.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="{x0-margin} {-y1-margin} {w} {h}">
<title>P01 {name} DESIGN_ONLY — mm, 1:1, no kerf compensation</title>
<metadata>profile_sha256={digest(points)}; local x=r y=z; displayed z upwards</metadata>
<g transform="scale(1,-1)"><polygon id="CUT_DESIGN_ONLY" points="{coords}" fill="none" stroke="black" stroke-width="0.1"/></g>
</svg>\n''')


def dimension(ax, a, b, text, offset=0, vertical=False):
    if vertical:
        x = a[0]+offset
        ax.plot([a[0], x], [a[1],a[1]], color='#64748b',lw=.5)
        ax.plot([b[0], x], [b[1],b[1]], color='#64748b',lw=.5)
        ax.annotate('',(x,a[1]),(x,b[1]), arrowprops={'arrowstyle':'<->','lw':.6})
        ax.text(x-3,(a[1]+b[1])/2,text,rotation=90,ha='right',va='center',fontsize=8)
    else:
        y=a[1]+offset
        ax.plot([a[0],a[0]],[a[1],y],color='#64748b',lw=.5)
        ax.plot([b[0],b[0]],[b[1],y],color='#64748b',lw=.5)
        ax.annotate('',(a[0],y),(b[0],y),arrowprops={'arrowstyle':'<->','lw':.6})
        ax.text((a[0]+b[0])/2,y+3,text,ha='center',fontsize=8)


def layout(name, points, assembly, design, baseline, directory):
    poly=Polygon(points)
    fig=plt.figure(figsize=(16,10),layout='constrained')
    ax=fig.add_subplot(121)
    ax.add_patch(Patch(points,facecolor='#e5cfab',edgecolor='#473b2c',lw=1))
    p=baseline['provisional']; s=design['study']
    for z in p['spacer_reference_heights_z_mm']:
        ax.axhspan(z-s['spacer_reservation_half_height_mm'],z+s['spacer_reservation_half_height_mm'],color='#3b82f6',alpha=.12)
        ax.text(288,z,f'Spacer {z:g}\nRESERVED',fontsize=7,va='center',color='#1d4ed8')
    low,high=s['mid_ring_reservation_z_mm']
    ax.axhspan(low,high,facecolor='none',edgecolor='#7c3aed',hatch='//',lw=.5)
    ax.text(288,low+3,'Ring study: OPEN / overlap',fontsize=7,va='bottom',color='#7c3aed')
    y0=p['Y_connector_center_z_mm']-p['Y_cheek_cutout_mm'][1]/2
    ax.add_patch(Rectangle((s['Y_reservation_radial_limits_mm'][0],y0),p['Y_cheek_cutout_mm'][0],p['Y_cheek_cutout_mm'][1],fill=False,edgecolor='#d97706',linestyle='--'))
    ax.plot([90,94],[410,410],color='red',lw=2)
    ax.annotate('Y r94 vs r90: 4 mm OPEN',(94,410),(140,420),fontsize=8,arrowprops={'arrowstyle':'->','lw':.6},color='#b91c1c')
    ax.plot([0,300],[450,450],ls='--',color='#64748b',lw=.6)
    ax.annotate('Table underside z450',(260,450),(180,466),fontsize=8,arrowprops={'arrowstyle':'->','lw':.5})
    ax.text(125,492,'Tongue r45..69; z450..488\nR1 tip (22 mm flat) / R2 root below z450\nDiscs: 456..462 / 480..486\nLock/access z486..494: OPEN',fontsize=8,va='bottom')
    dimension(ax,(35,0),(35,488),'488 mm',offset=-25,vertical=True)
    dimension(ax,(45,480),(69,480),'24 mm nominal',offset=59)
    foot=poly.intersection(LineString([[-1000,0],[1000,0]]))
    dimension(ax,(foot.bounds[0],0),(foot.bounds[2],0),f'Landing {foot.length:.1f} mm',offset=-18)
    dimension(ax,(poly.bounds[0],0),(poly.bounds[2],0),f'Envelope {poly.bounds[2]-poly.bounds[0]:.1f} mm',offset=-45)
    ax.scatter([240],[0],s=12,color='#111827')
    ax.text(240,14,'r240 center',ha='center',fontsize=8)
    ax.set(xlim=(-10,370),ylim=(-65,555),xlabel='Local r [mm]',ylabel='Global / local z [mm]',title='Dimensioned elevation — uncut reservations')
    ax.set_aspect('equal'); ax.grid(alpha=.15)
    iso=fig.add_subplot(122,projection='3d',proj_type='ortho')
    colors=['#c7a675','#bda482','#d6bb91']
    for index, item in enumerate(assembly):
        sides=item['surfaces_xyz_mm']
        faces=[sides[0],sides[1]]
        for i in range(len(points)):
            j=(i+1)%len(points)
            faces.append([sides[0][i],sides[0][j],sides[1][j],sides[1][i]])
        iso.add_collection3d(Poly3DCollection(faces,facecolor=colors[index//2],edgecolor='none',alpha=.90))
    angles=np.linspace(0,2*math.pi,180)
    for z in [450,500]:
        iso.plot(175*np.cos(angles),175*np.sin(angles),z,color='#64748b',ls='--',lw=.6)
    iso.set(xlim=(-290,290),ylim=(-290,290),zlim=(0,520),xlabel='X [mm]',ylabel='Y [mm]',zlabel='Z [mm]')
    iso.set_box_aspect((580,580,520)); iso.view_init(elev=35.264,azim=45)
    iso.set_title('Isometric: 3 legs / 6 identical cheeks\nConcept placement only; connections omitted',fontsize=11)
    fig.suptitle(f'P01 / {name} / DESIGN_ONLY — AWAITING_DESIGN_SELECTION',fontsize=17)
    fig.text(.53,.06,'6 mm nominal birch; t = ±10.5 mm\n15 mm gap / 27 mm overall; angles 0° / 120° / 240°\nNo fit, locking, assembly, load or stability approval.',fontsize=11,color='#9a3412')
    fig.savefig(directory/'layout.png',dpi=130,metadata={'Description':f'DESIGN_ONLY; profile_sha256={digest(points)}'})
    fig.savefig(directory/'layout.svg',metadata={'Date':None,'Description':f'DESIGN_ONLY; profile_sha256={digest(points)}'})
    plt.close(fig)


def ground_support(assembly):
    # Only points on the actual z=0 landing, including the 6 mm thickness surfaces.
    contacts=[(x,y) for item in assembly for surface in item['surfaces_xyz_mm']
              for x,y,z in surface if abs(z)<1e-8]
    hull=MultiPoint(contacts).convex_hull
    return {'contacts_xy_mm':contacts, 'support_hull_xy_mm':list(hull.exterior.coords),
            'hull_area_mm2':hull.area,
            'origin_to_support_edge_min_mm':hull.exterior.distance(Point(0,0)),
            'foot_center_triangle_inradius_mm':120,
            'status':'PLANAR_PROJECTION_ONLY; LOAD_CASES_CENTRE_OF_MASS_FLOOR_COMPLIANCE_UNKNOWN'}


def comparison(design, baseline):
    fig, axes=plt.subplots(1,3,figsize=(13,9),layout='constrained')
    for ax,name in zip(axes,design['variants']):
        points,_=profile(name,design,baseline)
        poly=Polygon(points)
        ax.add_patch(Patch(points,facecolor='#e5cfab',edgecolor='#473b2c'))
        ax.set(xlim=(0,300),ylim=(-25,520),title=name,xlabel='r [mm]')
        ax.set_aspect('equal'); ax.grid(alpha=.15)
        ax.text(150,-15,f'{poly.area:.0f} mm² / height488 mm',ha='center',fontsize=9)
    axes[0].set_ylabel('z [mm]')
    fig.suptitle('P01 alternatives — same scale / DESIGN_ONLY / no selection approved',fontsize=15)
    fig.savefig(PART/'comparison.png',dpi=130)
    fig.savefig(PART/'comparison.svg',metadata={'Date':None})
    plt.close(fig)


def generate():
    design, baseline=inputs()
    for name in design['variants']:
        directory=PART/'variants'/name
        directory.mkdir(parents=True,exist_ok=True)
        points, outline=profile(name,design,baseline)
        poly=Polygon(points)
        assembly=instances(points,baseline)
        margin=design['study']['sheet_margin_mm']
        minx,minz,maxx,maxz=poly.bounds
        dimensions={
            'part_id':'P01','variant':name,'status':'DESIGN_ONLY','units':'mm',
            'profile_sha256':digest(points),'contour_rz_mm':points,
            'source_inputs_sha256':hashlib.sha256((PART/'src/design.json').read_bytes()).hexdigest(),
            'bounds_rz_mm':list(poly.bounds),'area_mm2':poly.area,
            'perimeter_mm':poly.length,'thickness_nominal_mm':baseline['frozen']['cheek_thickness_mm'],
            'foot_landing_r_mm':list(poly.intersection(LineString([[-1000,0],[1000,0]])).bounds[::2]),
            'tongue_candidate':{'radial_mm':baseline['provisional']['upper_cheek_tongue_radial_interval_mm'],
                                'z_mm':baseline['provisional']['upper_cheek_tongue_z_range_mm'],
                                'fit_status':'PROVISIONAL / PENDING_PHYSICAL'},
            'sheet_check':{'height_mm':800,'width_mm':440,'margin_each_edge_mm':margin,
                           'padded_width_mm':maxx-minx+2*margin,'padded_height_mm':maxz-minz+2*margin,
                           'placement_translation_rz_to_sheet_xy_mm':[margin-minx,margin-minz],
                           'status':'SINGLE_PART_ENVELOPE_ONLY_NOT_NESTING'},
            'nominal_arc_radii_mm':outline.radii,'analytic_bezier_controls_rz_mm':outline.cubics,
            'chord_tolerance_mm':outline.tolerance,'raster_dpi':design['study']['raster_dpi'],
            'spacer_reserved_z_mm':[[z-design['study']['spacer_reservation_half_height_mm'],
                                     z+design['study']['spacer_reservation_half_height_mm']]
                                    for z in baseline['provisional']['spacer_reference_heights_z_mm']],
            'ring_reserved_z_mm':design['study']['mid_ring_reservation_z_mm'],
            'Y_envelope_overhang_mm':baseline['provisional']['Y_arm_end_radius_mm']-baseline['provisional']['Y_cheek_interface_radial_limits_mm'][1],
            'disc_sections':[{'z_range_mm':interval,'tongue_full_width_mm':24,
                              'nominal_radial_disc_envelope_clearance_mm':95-math.hypot(69,13.5),
                              'status':'PASS_CAD_SECTION_ONLY; SLOT_FIT_INSERTION_LOCKING_UNKNOWN'}
                             for interval in baseline['provisional']['anchor_disc_z_ranges_mm']],
            'minimum_body_section_width_mm':min(section(poly,z) for z in np.linspace(0,448,1000)),
            'instances':assembly,
            'ground_contact_projection':ground_support(assembly),
        }
        write_json(directory/'dimensions.json',dimensions)
        doc=ezdxf.new('R2010'); doc.units=4
        doc.layers.new('CUT_DESIGN_ONLY',dxfattribs={'color':1})
        doc.modelspace().add_lwpolyline(points,close=True,dxfattribs={'layer':'CUT_DESIGN_ONLY'})
        doc.header['$INSUNITS']=4; doc.header['$MEASUREMENT']=1
        doc.set_modelspace_vport(height=600,center=(150,244))
        doc.saveas(directory/'profile.dxf')
        write_svg(directory/'profile.svg',points,poly.bounds,margin,name)
        dpi=design['study']['raster_dpi']
        fig=plt.figure(figsize=((maxx-minx+2*margin)/25.4,(maxz-minz+2*margin)/25.4),dpi=dpi)
        ax=fig.add_axes([0,0,1,1]); ax.add_patch(Patch(points,fill=False,lw=.5,color='black'))
        ax.set(xlim=(minx-margin,maxx+margin),ylim=(minz-margin,maxz+margin)); ax.axis('off')
        fig.savefig(directory/'profile.png',dpi=dpi,metadata={'Description':f'P01 {name} DESIGN_ONLY; 1:1 at {dpi} dpi; profile_sha256={digest(points)}'})
        plt.close(fig)
        layout(name,points,assembly,design,baseline,directory)
        print(f'{name}: {len(points)} vertices; area {poly.area:.3f} mm2; bounds {poly.bounds}; valid={poly.is_valid}')
    comparison(design, baseline)
    # Matplotlib writes trailing blanks inside multiline path attributes. Normalize
    # generated review SVG formatting only, without changing coordinates or paths.
    svgs=[PART/'comparison.svg']
    for name in design['variants']:
        svgs.extend([PART/'variants'/name/'profile.svg', PART/'variants'/name/'layout.svg'])
    for svg in svgs:
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')


if __name__=='__main__':
    generate()
