# MEB-01 A1/H1 — direct ChatGPT geometric hinge research v0.1
**Date:** 2026-10-20 · **Status:** DESIGN_ONLY · **QA:** SELF_CHECK_PASS / INDEPENDENT_QA_PENDING · **Related:** #25 #26 · **PR:** #27

## Performed without Codex
ChatGPT built a fresh 20-body rigid prismatic CAD-equivalent research assembly using a single mathematical 2D Y/Z profile source and extruded 3D meshes, and produced two watertight-component GLB visualizations (lid 0° and 110°), full-source Python generators, QA/replay scripts, 5 model-derived PNG previews and a 441-row sweep log. **Those binary GLB/PNG artifacts and Python sources were delivered as a ZIP in the project conversation; they are not committed in this GitHub PR.** This report is a trace of the experiment, not a false claim of Git-hosted artifact availability.

## Selected mechanical research geometry
**Owner-frozen input:** sheet HEIGHT **800 mm** × WIDTH **440 mm**, lid opening target **110°**. All dimensions below PROVISIONAL:
- Frame X lengthwise, Y front to back, Z upward, mm; pivot axis X.
- Pivot Y=75, Z=75 mm in proposed body frame. Replaces historical external-looking pivot Y=-8,Z=78 *in inferred V8.2.2 registration*.
- Inner cavity 310×65×65 mm intended; fixed body core span 336mm, outer laminated cheek envelope span ~345mm (NOT owner approved; original nominal outer length 322mm).
- Outer circular pocket R11.5mm, moving recessed boss R10.5mm; pin R3.5mm, rotating hole R4.2mm; exterior flush cap R6.5mm.
- Two stationary cheek laminates, two outer 4mm side fascias, two moving 6mm lid cheeks with mechanical pocket, two wood pivot pins/caps, four body spacer blocks, box shell panels, idealized unslotted 4mm curved lid skin, two lid rails. These are **20 3D reference solids**, not a finalized physical BOM or cut-part definition.

## Results and evidence boundary
1. One geometry correction: an initial candidate pivot Y=70,Z=78 mm caused lid-skin intrusion into the static rear wall at intermediate angles; relocated research pivot to Y=75,Z=75 mm, with axial skin gap.
2. A model-space 2.5D exact prismatic extrusion sweep at **441 angles, 0..110° in 0.25° steps**, found **0 moving-vs-static volumetric intersections**. The smallest fixed-vs-moving modeled gap was **0.500mm**. Conservative nearest-sample movement upper bound Rmax×0.125°=**0.16372mm** gives strictly positive between-sample clearance lower bound **0.33628mm**, **only for this mathematically idealized rigid prismatic model**.
3. Primary mathematical checks: **14/14 PASS**; second self-replay checking generated GLBs/sweep/counterexamples: **15/15 PASS**. These are overlapping SELF checks, **not independent QA**. All 20 component meshes in both scene poses were closed/watertight with positive volume. Wrong-pivot negative control at 40° yields **~0.948mm²** rear-wall overlap.
4. **A blocker remains:** **6 unintended moving-to-moving solid volume overlaps** (rails vs lid-end cheeks/skin). These are acknowledged *joint placeholders*, not validated local part joinery. Entire lid still lacks an insertion/joinery solution.
5. Pivot shaft and flush retaining cap are only nominally touching/face bonded to stationary cheek, and retention/adhesive/axial stack strength/insertion is NOT_RUN. Some research spacers are 7.5mm thick, not directly realizable as one nominal 6mm sheet; require real lamination and fit design.
6. The roof surface is **unslotted smooth conceptual 4mm stock**, NOT the physical living-hinge assembly. Legacy ~0.10mm thin-web finding MEB-B12 stays OPEN; G3 bending/kerf/bond and actual moving hinge durability all NOT_RUN.
7. Legacy V8.2.2 sources were not changed; new outer envelope/side visual proportions are **design proposals awaiting owner feedback**. G0 full, G1, G2 assembly, G3 and G4 remain BLOCKED/NOT_APPROVED.

## Process corrections and provenance
- One geometric revision and two tooling/self-QA repairs: Delaunay triangulation was unconstrained (lid mesh invalid), switched to Shapely constrained triangulation; volume equality after 110° GLB rotation used appropriate float32 export tolerance.
- No CAD kernel STEP export was achieved; two **GLB polygon-mesh scenes** were exported, and full parameter source code + technical images were delivered in chat. No STEP/DXF/production file claim.
- Independent mechanical CAD QA was **not** performed. This PR must remain Draft until third-party independent review and design-owner choice. No automatic merge.

## Next review
Present the model-based 0° and 110° visualizations and side detail to owner. If owner chooses recessed H1 over other options, a later scoped task should (a) remove 6 moving-to-moving overlaps with actual joint geometry, (b) design pin/cap assembly/retention with a continuous insertion path, (c) replace idealized lid shell with manufacturable kerf geometry, and (d) independently retest the whole 110° assembly including material/tolerances. No G4 release.

**Who should execute:** ChatGPT for design alternatives/visual geometry where efficient; Codex only for complex parametric engine / mass automated integration where speed or reliability benefits; separate reviewer for independent QA.
