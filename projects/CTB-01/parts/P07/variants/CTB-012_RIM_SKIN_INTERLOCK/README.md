# CTB-012 — Rim-to-skin interlock, DESIGN_ONLY

This versioned study addresses CTB-01 interfaces IF-10 and IF-11 without editing CTB-010/011 original masters. It is **not approved for laser cutting or fabrication**. All dimensions below are nominal and are not measured fit allowances.

## Geometry and work allocation
- **P07T_TABBED** and **P07B_TABBED** (6mm birch): outer base radius 171mm with twelve local radial tabs extending to radius 174.8mm. P07B's six existing leg tongue slots remain byte-equal polygon coordinates.
- **P07R1/R2_NOTCHED** (4mm birch): six 12mm open slots at each long edge per half-rim, centered at developed lengths 45, 135, 225, 315, 405, 495mm. Notches are 6mm deep into the 50mm rim height. The 63 original bending openings per segment are unmodified. **Local minimum rail is only 2mm; comparative reference, NOT preferred candidate.**
- **P07R1/R2_REINFORCED** (4mm birch): same notches, but locally shorten 18 of 63 flex openings per segment from x8..42 to x12..38. Local bridge near a notch increases to nominal 6mm. **Preferred DESIGN-STUDY candidate**, bending stiffness and 50mm wrap remain unverified.

Original base geometry: outer tabletop 350mm diameter, 50mm total thickness, skins each 6mm, rim 4mm x 50mm high. Core assembly and P05 ribs were NOT modified. Original rim bending seam remains OPEN.

## Assembly coordinate model (nominal only)
Rim sheet x maps to table z450..500mm. Bottom slots lie x0..6 (z450..456) and top slots x44..50 (z494..500). Two half-rims start at nominal phases 15° / 195° respectively. A developed rim point s is mapped to angle phase + (s-0.2)/173 radians; neutral radius = 173mm. Each disk tab half-width is 5.75mm developed arc versus rim notch half-width 6mm (nominal tangential gap ~0.25mm/side). Skin tab outer tip radius174.8mm vs rim outside radius175mm.

In the nominal assembly: install lower skin before wrapping the rim; then upper skin via vertical insertion into open-top notches. This is a **proposed sequence**, NOT swept-motion or rigid-solid insertion validation. No vertical pull-out stop is provided by this joint alone; adhesive / additional retention is STILL NEEDED and unqualified.

## Files and reproducibility
Run `python3 build_ctb012.py --repo-root /path/to/assembl-lab-engineering --out /tmp/ctb012-export` to reconstruct variants from original P07/variants/A cut polygons, with no geometry refitting. Exactly 12 unique vector exports across the two skins and both rim alternatives. The source generator also emits BUILD_REPORT.json. The original CTB-011 nesting is NOT valid for these changed 6mm skin outlines and cannot be used as a manufacturing layout.

Only CUT_OUTER / CUT_INNER are cutter geometry. DXF stores millimeters in original assembly-sheet axes and SVG presentation uses Y flip (visual only). Compensation is zero, as in CTB-010.

## Blockers
- Mandatory independent actual-vector / CAD-kernel and 3D assembly fit/swept-path review: INDEPENDENT_QA_PENDING.
- Material thickness, laser kerf, grain/flex, 18 shortened-kerf slots' bend behavior, glue retention, peel, radial shear, load and stability: NOT_RUN.
- IF-11 rim-to-rim splice and IF-07/08/12 structural retention: OPEN, not fixed by added tabs.
- CTB-011 re-nesting must be recomputed from variant geometry; do not reuse as-is.
- G3 NOT_PERFORMED, G4 BLOCKED.
