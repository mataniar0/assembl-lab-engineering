# CTB-003 / CSH-3Y / P03 — DESIGN_ONLY

Three coordinated joint concepts; A_COMPACT_CLOSED proposed as working candidate only.
B_DUAL_CLOSED distributes engagement across two side tabs; C_OPEN_REMOVABLE needs a
reviewed open-edge cheek revision and has no reverse-withdrawal retainer. None is approved
for cutting, fit, loads or full-product integration. Read CHANGE-PROPOSALS and reports.

`src/design.json`/schema are controlling inputs; source imports untouched P01/P02 models.
Use original selected SOFT_CURVE and B_THROUGH_ADHESIVE /35,90,200,390 from signed decisions.
No historic ZIP/image geometry is reconstructed. Original baseline and all P01/P02 files
remain byte-preserved; hashes and source commit are recorded under src.

`variants/<NAME>` contains1:1mm P03 DXF/SVG/PNG, updated candidate cheek exports/dimensions,
mechanical metrics, every pair/sweep matrix and layout provenance. SVG display flips y
only for upward convention. Cheek cut plane is(r,z), P03 plane(X,Y), both extruded6 mm
orthogonally. Raster1:1 only at96dpi/100% print; review layouts are scaled. Disable page-fit.
All contours are ideal uncompensated design geometry, not machine instructions.

A localtip85.5/maxradius85.76998 avoids the old94/90 mismatch; local margin4.5 is a study
hypothesis. A tabs58..74, B52..62+72..82; C54..70/tip82. Each reaches t±13.5 across6 mm
cheeks, while14.6 core in15 gap has0.2 per-side nominal gap. Candidate slots use0.2 per-side
radial/Z allowance andR0.2, height6.4 at410. ConvexR0.5/concaveR0.1 are ideal planar
laser-candidate easings, not certified tool/edge safety. HubR24 and arm neck14.6×6 section
are geometric descriptors, not structural minima or strengths. Grain along all3 arms
cannot align with one outer veneer grain direction: actual plywood layup/anisotropy,
notch stress, moisture, defects and material tests are mandatory before load claims.

Assembly output contains19-part GLB (metres),3-leg assembled/exploded views, actual18-stage
projection diagram and all continuous proofs. See assembly/ASSEMBLY-ORDER.md. Closed-hole
A/B prebuilt approaches block; Y-first tangential cheek/spacer sequence passes. C allows
radial prebuilt entry conditionally but changes the cheek/notch and allows withdrawal.
No extra hidden retainer, screw, glue-only lock or physical test is assumed.

Stock thickness and kerf are null/unmeasured. Nominal6 does not assert actual6.0. Atfixed
centers±10.5 actual gap21−measuredThickness; actual outside21+measuredThickness. Coupon
fit, glue/cure, retention and material/edge/process review remain open. Under uncompensated
beam-center cutting, internal holes approximately widen bykerf and external tabs shrink
bykerf; CAM compensation changes that relation and must not be applied twice. Do not
fabricate tolerances from these hypotheses. Per-part H800×W440 with provisional10 mm
margins is checked; actual nesting/grain/fixturing and physical cutting are unapproved.
