# CTB-015C ChatGPT-first / DESIGN_ONLY

Upstream PR #61 provides **PASS** for two static final curved puzzle seams and four rim-to-skin bands, **FAIL** for the inherited vertical-lowering route at Z+2mm (~64mm³ per seam), and a one-in-memory-fix-per-file DXF LAYER handle advisory. Current geometry remains unchanged.

## Completed change
Two CTB-015 corrected seam DXFs copied into this **versioned** folder, with LAYER table handle `2`, layer record handles `A`,`B` and owner `330=2`. Cut entity sections are byte-for-byte identical to CTB-015, including all 64 LWPOLYLINE contours per strip; SVG remains the authoritative prior CTB-015 file. Handle uniqueness and owner references were checked by raw text parsing; independent ezdxf audit **NOT_RUN**. No original files modified.

## Assembly-route design analysis (not a proven motion)
**Candidate A, prejoin/wrap:** with two necked ends, first interlock one seam while flat or semi-curved; wrap both around core to the source final nominal cylindrical position; close the second seam later. This intrinsically changes curvature during motion and requires a material-flex deformation model and/or physical qualification. The rigid OCC shell used at PR61 has no such validated elastic model, so no GO may be issued from schematic sequencing.

**Candidate B, co-planar symmetric placement:** bring rim half-arcs from opposing radial directions before upper skin installation and simultaneously close both joints in-plane. Unlike the inherited R2 vertical drop, this preserves the intended final Z-bands. But two opposite neck/head directions and the closed-ring topology require a continuous 6DOF motion demonstration, including the bottom skin/core obstruction and mutually swept material. Current evidence proves only final fit and failure of one vertical interior pose; it neither proves nor refutes this route.

Do not predeclare universal impossibility, assume elastic snap, change the neck to create a guessed clearance, or reduce kerf to achieve a GO.

## Check register
- DXF changed **metadata only**: 2/2 exact entity-section text comparison PASS.
- Unique handles and layer owner references: 2/2 PASS by raw token inspection.
- SVG and 63 kerf cuts: inherited unchanged (no new source export).
- DXF independent ezdxf loading/audit: NOT_RUN.
- Whole-shell alternative assembly paths A/B: NOT_RUN.
- Physical material/kerf/flex, edge radii, joint strength: NOT_RUN.
- CTB-016 nesting: **BLOCKED** pending an accepted collision-free and feasible assembly route.
- Code source geometry repair count: 0; DXF metadata edit count: 2 files; independent QA pending. G3 NOT_RUN/G4 BLOCKED.
