# PST-310 MODERN V5 — CAD, sampled assembly QA and completed cutting nesting

**Date: 2026-11-04** · **Status: NESTING_COMPLETE / DESIGN_ONLY — physical cut/strength release HOLD.**

## Scope and approved dimensions
- Plant stand, 3 radially spaced legs at 0°/120°/240°.
- Ø310 mm circular top **re-cut two 6mm discs with integral mortises** (explicit owner approval), 60mm hollow tabletop depth, overall stand H550mm.
- 6mm birch structure; six 4mm birch curved flex-wall sectors.
- 440mm width × 800mm height nesting sheets, 5mm minimum sheet-edge clearance, 1.0mm minimum part-to-part separation, zero kerf compensation until machine-specific calibration.

## Design corrections from V4 (do not reuse V4 source cuts)
1. V4 vertically continuous 48mm-tall Ø114mm annular core was NOT a feasible one-pass flat 6mm laser-cut piece. Replaced with one **6mm-thick flat slotted center disc** at Z522..528, radial-open recesses with 6.32mm nominal width, adhesive side restraint rather than positive half-lap. Load-bearing performance is unverified.
2. Three V4 19mm-high solid underside edge beams were physically not directly obtainable from a single 6mm stock sheet; replaced by **9 separately cut 6mm laminations**, assembled 3 layers per triangular side to approximately 18mm.
3. Single-piece 6mm lower triangular frame encountered collisions during rigid slide installation; replaced by **3 independent corner-sector V-pieces**. Each is first bonded/fixtured to a corresponding two-plate leg and raised **as a leg+corner subassembly** into the bottom 6mm disc and the lower leg spider. Three side laminated beams bridge the joints with glue.
4. 4mm flexible rim flattened according to neutral radius R153mm: **160.221225 mm length per 60° piece**, 6 pieces, sum **961.327352mm**. Every segment has **39 continuous kerf rows at 4mm pitch**, **58 single-line cut strokes** alternating 42mm center and paired 20mm edge cuts (locally shorter near 4 upper/lower finger tabs). No actual-width cut slots or end puzzle neck. Physical bend springback and assembled rim circumference HAVE NOT been measured.
5. No change to chosen outside styling; all three modern tapered legs with long slots retained.

## Computed BOM and nesting
- **34 independently laser-flattened part instances**: **28×6mm**, **6×4mm**.
- **4 sheets 6mm**, **1 sheet 4mm** = **5 sheets total**, each **440×800 mm portrait**.
- A conservative rectangle-only nesting required five 6mm sheets; after shape-aware placement of three tapered leg silhouettes per board, achieved four 6mm sheets.
- Min part-to-part contour clearance on each sheet: S01 1.0mm, S02 1.001mm, S03 1.0mm, S04 1.0mm, BIRCH4_S01 6.0mm. Min edge distance 5.0mm.
- 34 separate SVG and 34 separate DXF, five SVG and five DXF sheet files, matching exactly on type, closed cuts and mm coordinates. Layers: CUT_OUTER, CUT_INNER; CUT_KERF_LINE for 4mm shell only. **No stock-board outline in cutting geometry**.
- Preview PNGs and Hebrew instructions, BOM, per-part placements, source Python/CadQuery, STEP/GLB and QA reports were generated and archived locally in chat (two validated ZIPs).

## CAD and assembly evidence
- **34 valid OpenCASCADE BREP solids**; full STEP exported and reopened with **34 valid solids**, GLB export produced.
- **561** distinct final-pose solid pairs checked; **430** pairs proven disjoint by 3D bounding boxes and **131** tested with real CAD Boolean intersection; **0 collisions >0.01 mm³**.
- Proposed **26-stage** assembly order: bottom disk+lower spider; three leg+triangle-corner subassemblies raised from below; nine laminated lower-beam layers applied from below; six core ribs lowered; slotted horizontal central disc lowered; six curved rim sectors lowered to bottom disk; **top disk lowered last**.
- **464 sampled rigid configurations** over stages, **10,123** stationary/moving body pair considerations, **803 actual Boolean checks**, **0 sampled rigid intersections >0.01mm³**.
- Independent CAD geometry and sheet SVG↔DXF serialization rechecks PASS. This is *discrete sampled rigid-path evidence*, **not complete continuous 6-DOF proof**, especially not proof of flexed-rim behavior or jig feasibility.

## Blocked physical acceptance gates
- Actual 6mm/4mm ply thickness and actual laser kerf unmeasured; tab/mortise allowances 0.16–0.18 mm nominal/side are uncalibrated.
- Bend/motion of the six 4mm kerf-flex rims, seam closing/overlap, glue retention/springback not tested; **cut ONE rim sector as an initial sample only** until tested.
- Corner+leg preassembly holding, glued laminated brace load path and central plate's adhesive shear restraint are untested.
- Intended pot dimensions/mass with wet soil and water, tipping resistance, strength, moisture sealing and physical prototype tests remain open.
- **No full-production release.** Do not treat nesting as authorization to cut every part; this is a CAD-derived candidate to guide test coupons and manufacturing iterations.

## Delivery integrity / GitHub disclosure
Full binary STEP/GLB, sheet SVG/DXF, individual part files, all verification scripts and two CRC-valid ZIP archives have been created in the ChatGPT artifact runtime and linked to the user. **This GitHub PR includes only this traceable engineering report**; the CAD binaries, source scripts, cutting vectors and ZIP packages **have not been pushed to GitHub**. Do not claim GitHub hosts the production files.

## Next validation and owner action
LEAN TASK PLANNING v1.1: ChatGPT main executor, Codex optional only for necessary long-running regression/independent CAD review. Actual fabrication must first verify a 6mm finger-slot coupon, one 4mm flexible segment bent to R153mm, rim length around *both* new Ø310 top discs, and then a controlled adult-supervised load/tilt check using the real filled pot weight. No external power/load testing on a person.
