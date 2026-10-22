#!/usr/bin/env python3
"""MEB015 J3 hidden interior U-saddles, one per moving end.
Source delta is relative to MEB011 T1 code available in user handoff ZIP.
DESIGN_ONLY. Adhesion/bearing/wood flex are NOT physically proven.
"""
from shapely.geometry import box
import build_variant_t1
import build_integrated as m

CLIPS=[('L',11.5,17.5),('R',318.5,324.5)]
BANDS=[(30,36),(41,47)]
SLOT_TOP=87.25
CLIP_POCKET_BOTTOM=86.95
CLIP_TOP=92.7
CLIP=box(27.5,77,49.5,CLIP_TOP)
for ya,yb in BANDS:
    CLIP=CLIP.difference(box(ya-.25,CLIP_POCKET_BOTTOM,yb+.25,99))
CLIP=CLIP.buffer(0)

for name in ('LID_FRONT_RAIL','LID_BACK_RAIL'):
    q=m.BYPART[name]
    for _,x0,x1 in CLIPS:
        q.shape=q.shape.difference(box(x0-.2,79,x1+.2,SLOT_TOP))
    q.shape=q.shape.buffer(0)

ADDED=[]
for mark,x0,x1 in CLIPS:
    part=m.v.p('INTERNAL_RAIL_SADDLE_'+mark,'YZ',CLIP,x0,x1-x0,True,
      '#8f9676','Internal U rail brace, bonded to moving socket (strength NOT_RUN)')
    ADDED.append(part)
    m.BYPART[part.name]=part
m.PARTS.extend(ADDED)
m.REGIONS=m.collision_regions()
assert len(m.PARTS)==26
