# CTB-002 / P02 and P02B / DESIGN_ONLY

Three joint studies, preferred **B_THROUGH_ADHESIVE** pending engineering-lead review.
Use SOFT_CURVE selected by P01-SEL-001. Four spacers per leg, P02×9 + P02B×3 per table.
No new lock parts or purchased hardware. Original P01 source/exports are untouched.

- `src/design.json` + schema: all controlling concept dimensions, ideal stock6,
  per-side slot allowance0.2, radii, stations, ring band and insertion offset.
- `src/model.py`: imports unchanged P01 parametric source, constructs spacers/slots
  and actual extruded solids; exact continuous translation sweeps.
- `src/generate.py`: all drawings, dimension JSON, GLB mockup, ring and stock studies.
- `variants/<concept>/`: P02/P02B and versioned P01 mortise candidate DXF/SVG/PNG,
  mechanical dimensions, review layout and layout provenance. A is explicitly BLOCKED;
  C is a feasible nominal CAD alternative after repair. Only B is the working proposal.
- `assembly/`: full one-leg GLB and assembled/exploded/insertion/ring views, continuous
  proof matrices, unchanged upstream hashes and hypothetical thickness sensitivity.
- `BOM-v1.csv`: versioned candidate BOM, excludes alternative parts from additive counts.

Spacer geometry is in local(r,t), extruded in z6 mm. Cheek geometry is(r,z), extruded
in t6 mm. One P02 geometry is translated to the exact common section centers at90,
200,390; P02B has40 mm radial body/24 mm tabs vs P02 body30/tabs18, at35.
Reinforcement means wider material/landing/engagement only, not a proven load increase.
Hypothesized primary face grain follows t in the spacer bridge; actual plywood layup,
face grain, defects, adhesive and loads must be specified and tested. No stiffness value.

B mortises: P02 radial18.4×z6.4; P02B24.4×6.4, rounded0.2 mm ideal corners.
Spacer convex radii0.5 and root0.1 are laser-candidate nominal geometry, not certified
machine capability. Finite beam kerf, heat, edge finish and stock thickness require
coupons. DXF/SVG1:1 mm; profile PNG1:1 only at96dpi/100% print; disable fit-to-page.
Review layouts are scaled sheets. All geometry is uncompensated, not ready to cut.

The approved external P01 contour and upper tongue/foot remain byte-for-byte unchanged
in original P01. New holes exist only in `P01-SOFT_CURVE-mortise-study-v1` under this
P02 proposal. No mortises in ring band225..265. Proposed spacer245→200 is provisional
PC-CTB002-01 and requires CTB006 coordination, not a silent baseline parameter edit.
Sheet check is per-part H800×W440 with provisional10 mm each edge, not actual nesting.

For actual measured thicknessT at fixed centers±10.5, gap=`21−T`, outer section=`21+T`.
AtT5.6 the proposed shoulder has0.2 mm unintended gap each side; at6.4/6.8 actual solid
collisions occur in this unchanged nominal candidate. Sensitivity values are hypothetical,
not measurements. Under uncompensated beam-center cutting an internal opening finishes
approximately drawn_width+kerf and an external tab drawn_width−kerf; CAM compensation
changes the bookkeeping and must not be doubled. Choose fit only after coupons.

No positive outward retention is provided by B/C without unverified adhesive or a
later reviewed capture strategy. B01/B02 whole-system lock/sequence remain open.
Read assembly/INSERTION-ORDER.md and ../../reports/CTB-002-* before using any artifact.
