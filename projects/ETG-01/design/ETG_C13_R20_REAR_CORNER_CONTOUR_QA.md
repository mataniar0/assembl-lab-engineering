# ETG-01 C13 — corrected R20 rear corners / verified CAD model

**Date:** 2026-11-15 · **Owner request:** correct visibly protruding rear end panel in C12 photo and continue through a tested CAD model. **Executor:** ChatGPT and local CadQuery/OCC. **Stage:** C13_LOCAL_CAD_PASS / DESIGN_ONLY / PRE_NESTING; independent QA pending; no Codex.

## Defect diagnosed and correction
Prior C12 P03/P04 rear sidewall edge extended to Y160, while P06 rear laminae were not complete R20 round corners and ended at Z114. This was actual inconsistent source geometry, not image shading.
- P03/P04 sides now terminate at **Y140**, tangent to the R20 rear outer quarter circle.
- P02 rear wall now extends to **X20..240** to meet tangencies below a necessary local upper hinge clearance; original rear wall started X30.6.
- P06 rear corners rebuilt with true R20 outer / R14 inner OCC quarter-annulus XY contours, 6mm horizontal lamination. Added six slices per rear corner: **24 rear layers each** (48 total) to Z150, versus 18 each in C12.
- Upper 36mm layers have localized flat XY cutouts for external H1 stationary ears. The highest 6mm layer has an additional intentional H1 P11 motion recess. This is not a perfectly uninterrupted R20 contour in the hinge region: the visible raised hinge remains. Every part stays a constant 6mm laser-flat geometry.
- P05 and P07 R20 profiles, H1 axis Y160/Z154, 120 degree lid opening direction and the nominal body 260×160×150mm were preserved. P12 clip remains retired per owner approval of adhesive pin retention. No kerf compensation or nesting.

## Auditable CAD test evidence
- **114 separate pieces** versus 102 in C12; 114 DXF and 114 SVG files, each successfully parsed and matched by contour count. All individually fit H800×W440 stock; maximum flat contour area tessellation error 0.0319%.
- Basic focused geometry **19/19 PASS**; 624 stationary changed-relevant parent comparisons with zero overlap; 21,777 moving-vs-changed tests at 61 angles (every 2 degrees from 0 to120), zero overlaps.
- Extended **6/6 PASS**; 241 angular samples every 0.5 degree, **86,037** moving-vs-changed part pairs, zero intersections. Negative control: old sidewall physically overlaps new corner shell; reverting final top notch causes **31.2554mm³** real overlap with moving P11 at 120 degrees.
- STEP/GLB and render process 12/12 source assertions PASS, reimported **114 valid STEP solids** and **114 GLB geometries**. Independent roundtrip file verification **13/13 PASS**; all 114 DXF/SVG contour counts agree.
- These are implementer-run finite sampled rigid-body CAD checks, NOT independent QA, formal continuous swept-volume proof or physical load/durability testing.

## Delivery/provenance
User chat ZIP: ETG_01_C13_FLUSH_REAR_CORNERS_DESIGN_ONLY.zip, SHA256 7b051e7e2ae0c59801128d2d91803f796898a4445ab03e10db41343fdcdc1a07; **253 files** incl. source and dependencies, editable STEP, GLB, 228 vectors, comparison, views, JSON tests and Hebrew report. The actual source/STEP/DXF binary files are in chat ZIP and **not committed to GitHub** with this report. Independent replication requires the actual ZIP.

## Open / not approved
Two P07 rear H1 roof relief openings remain unsealed. At raised H1 bearings and the top lamination recess the curvature is locally interrupted as needed for motion; appearance and physical clearance still need review. Nominal birch thickness, kerf, glue migration into bearing, pin bond strength, contact/glue strength, physical operation, etrog clearance, independent QA and G3/G4 manufacturing release NOT_RUN. Nesting NOT_PERFORMED.

**Disposition:** corrected visible rear shell flushness and built source-backed verified model C13; DESIGN_ONLY. Do not claim production readiness or merge Draft PR #71.