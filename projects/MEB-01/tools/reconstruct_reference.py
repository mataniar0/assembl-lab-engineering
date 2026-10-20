#!/usr/bin/env python3
"""Generate DESIGN_ONLY DXF/SVG from measured coordinate parameters; not a new cut release."""
import argparse
import html
import json
from pathlib import Path
import ezdxf

PROJECT = Path(__file__).resolve().parents[1]
MODEL = PROJECT / 'proposals/G0-reference/measured_profiles.json'


def generate(model, output):
    if model['units'] != 'mm' or model['status'] != 'PROPOSED_MEASURED_VERTEX_REFERENCE_NOT_APPROVED':
        raise ValueError('Unsupported/unapproved reference model')
    output=output.resolve()
    allowed=(PROJECT/'proposals/G0-reference/generated').resolve()
    if not output.is_relative_to(allowed) and any((p/'.git').is_file() or (p/'.git/HEAD').is_file() for p in (output,*output.parents)):
        raise ValueError('Refusing to write generated reference into a Git checkout outside the designated proposal folder')
    output.mkdir(parents=True, exist_ok=True)
    for name, profile in model['profiles'].items():
        doc=ezdxf.new('R2010'); doc.units=4
        doc.layers.new('DESIGN_ONLY_CUT');doc.layers.new('DESIGN_ONLY_KERF')
        m=doc.modelspace()
        for points in profile['contours']:
            m.add_lwpolyline(points,close=True,dxfattribs={'layer':'DESIGN_ONLY_CUT'})
        for points in profile['kerf_lines']:
            m.add_line(points[0],points[1],dxfattribs={'layer':'DESIGN_ONLY_KERF'})
        doc.saveas(output/(name+'.dxf'))
        allpts=[p for pts in profile['contours'] for p in pts]
        minx=min(p[0] for p in allpts);miny=min(p[1] for p in allpts)
        w=max(p[0] for p in allpts)-minx;h=max(p[1] for p in allpts)-miny
        paths=[]
        for pts in profile['contours']:
            commands='M'+' L'.join(f'{x:.12g},{y:.12g}' for x,y in pts)+' Z'
            paths.append(f'<path d="{commands}"/>')
        for pts in profile['kerf_lines']:
            paths.append(f'<path d="M{pts[0][0]},{pts[0][1]} L{pts[1][0]},{pts[1][1]}" stroke="blue"/>')
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="{minx} {miny} {w} {h}"><title>{html.escape(name)} DESIGN_ONLY measured reference</title><g fill="none" stroke="black" stroke-width="0.1">'+''.join(paths)+'</g></svg>\n'
        (output/(name+'.svg')).write_text(svg)
    return len(model['profiles'])


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    # Generated references must never target the external legacy source checkout.
    dest=a.output.resolve()
    if dest == Path('/tmp/meb-legacy-site').resolve() or Path('/tmp/meb-legacy-site').resolve() in dest.parents:
        raise ValueError('Refusing legacy source output directory')
    print('Generated',generate(json.loads(MODEL.read_text()),dest),'DESIGN_ONLY DXF/SVG profile pairs')

if __name__=='__main__':
    main()
