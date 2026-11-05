# PST-310 Modern V6 — one-piece lower triangular ring and four-sheet nesting

**2026-11-05 · DESIGN_ONLY / NESTING_COMPLETE / CUT-RELEASE HOLD**

## Approved scope
The user chose to remove the redundant lower round three-arm spider, the three segmented lower V-corners, and all nine laminated bridge-strip layers; replace with a **single continuous 6mm birch triangular brace**. Preserve the user's current plant-stand dimensions: Ø310mm top, 60mm hollow structural top, 550mm overall height, three modern double-6mm legs at 0°,120°,240°. Recut the top/bottom Ø310 discs with existing mortises. The six 4mm kerf-flex shell sectors remain 60° pieces requiring physical bend/closure calibration.

## Actual V6 parametric change
- REMOVE: `LOWER_LEG_SPIDER_6MM`, `TRIANGLE_CORNER_1..3_6MM`, and all `TRI_BEAM_1..3_LAYER_1..3_6MM`.
- ADD: one `LOWER_TRIANGLE_ONE_PIECE_6MM` originally defined from the CAD outer radial three-notch triangular ring, not three segments.
- CHANGE: raise the **wide bearing shoulders** of all six leg panels from Z484mm to Z490mm so each contacts the bottom face of the lower Ø310 disc at Z490–496. Retain 6mm upper finger projection to Z496 and regenerate all six leg cut profiles from the same CadQuery source.
- RETAIN: `CENTRAL_FLAT_6MM_SPIDER` — a *different small disc* inside the hollow top for six radial webs, not the deleted large 3-arm underside spider.

## New BOM / sheet result
- V5 **34 parts → V6 22**: 16 × birch6, 6 × birch4.
- V5 **5 sheets → V6 4 sheets**: **THREE 440×800mm birch6** and **ONE 440×800mm birch4**.
- Shape-aware polygon nesting combines two sloped leg profiles with a Ø310mm disc on each of two sheets. Three ribs are nested in the space between those legs on each sheet. Third 6mm sheet carries two leg profiles, the one-piece triangle rotated30°, and the small inner connector **inside the triangular cut-out (9.07mm clearance)**. Fourth sheet carries six flex-rim segments.
- Minimum modeled **inter-part geometric clearance 2.699808mm**, vs user requirement 1.0mm. At least **5.0mm** stock-edge clearance on every sheet. No kerf compensation, no stock outline in cut layers. Preserve original full 310mm disk diameter.
- All 22 individual SVG+DXF pairs, four 1:1 nesting SVG+DXF pairs; **71 closed contour loops and348 single-line flex slots**; 39 slot rows at4mm pitch per each of six rim sectors.
- For 6mm S03, **cut small connector inside the triangular scrap opening and interior cuts BEFORE freeing large external triangular contour**, and secure components; downstream CAM order/hold-down not asserted.

## Bounded actual computer-aided QA
- 22 valid CadQuery/OpenCASCADE CAD solids. STEP reimport22, GLB reimport22.
- 231 static final-pose component pairs; 158 disjoint by axis-aligned 3D boxes, **73 actual CAD Boolean intersection checks**, zero overlap >0.01mm³.
- New order tested using 18 distinct CAD stages: radial insert of three paired leg-laminates into open slots of single triangle, then lower disc lowered onto all six leg fingers, then six core ribs, flat central disc, six *nominal precurved rigid* sectors, finally upper disc lowered last.
- **311 sampled positions / 542 actual CAD Boolean intersection calculations / zero sampled rigid collisions**. NOT continuous-path or physical feasibility proof; no genuine flex-simulation, load simulation, moisture or glue testing.
- Independent export audit: all22 stand-alone sources agree with transformed nested output coordinates/layers to tolerance0.00006mm, all sheet SVG/DXF vectors match, no abandoned V5 parts, no duplicated IDs, no SVG cutting-border rectangles.
- ZIP archive integrity tested. Local conversation bundle SHA256:
  - `PST_310_V6_NESTING_SVG_DXF_4_SHEETS_DESIGN_ONLY.zip`: `65d70c89f6a702450371510f42e6b9f869135617b41c3bd99bf9078816077edf`
  - `PST_310_V6_COMPLETE_CAD_AND_NESTING_DESIGN_ONLY.zip`: `cd3f958f3540225672369cfb6abc564140171411f724ac1550cb67cfa6182bf1`

## Critical physical hold gates
1. Measure real 4mm/6mm plywood thickness and actual laser kerf. Coupon-fit mortise/finger and glue joints.
2. Cut a **single** 4mm shell sector for bend testing and calibrate physical circumference/springback/edge seam. Do not cut full batch based on nominal R153 perimeter alone.
3. Verify access to the three radial insertion slots with real wood and clamps. Glue strength and torsional bracing must be independently validated.
4. Establish intended pot + wet soil + water load, lateral stability and tipping margin. Add moisture protection.
5. Physical trials with qualified supervision; no full production release or verified load rating until passed.

## Source / delivery limitation
Complete STEP/GLB, 22 individual part DXF/SVG, 4 board DXF/SVG, PNG views, Python CadQuery source and QA JSONs were generated in ChatGPT's local runtime and supplied via downloadable chat archives. **This GitHub branch/PR currently commits only this report; the binary CAD/cutting files are NOT pushed to GitHub.** Do not confuse a doc merge with production release.
