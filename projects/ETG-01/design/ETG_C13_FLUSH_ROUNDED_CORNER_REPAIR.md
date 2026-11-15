# ETG-01 H1-C13 — rear corner flush R20 repair, geometry QA & pre-nesting handoff

**Date:** 2026-11-15 · **Executor:** ChatGPT/CadQuery/OpenCascade · **Owner request:** eliminate the protruding square rear corner shown in the owner-provided close-up, and deliver a corrected independently re-openable CAD model after local testing. **Status:** `C13_CAD_SELF_TEST_PASS / DESIGN_ONLY`; not independent QA/G3/G4 release. Parent C12 ZIP and image inspected directly.

## Source-backed cause and correction
- **Root cause in C12:** `P03/P04` side sheets ran to Y160 although the theoretical R20 radius at the rear should tangent to side at **Y140**. `P06` lower laminated rear pieces did not follow a true quarter annulus; rectangular `P06_KEEPER` posts remained even though the P12 mechanical clip was retired. C12 P03's excess volume *outside the selected nominal R20 plan envelope* was measured as **8769.6334 mm³**.
- **C13 side walls P03/P04:** terminate at Y140, touching new true circular R20 exterior/R14 interior rear corner arcs. New source-side outside volume **0 mm³**.
- **P02 rear:** lower P02 wall spans X20..240, Y154..160, Z6..114; upper spans X30.6..229.4, Y154..160, Z114..150, leaving room for H1. One valid stepped sheet of nominal 6mm thickness normal to Y.
- **P06 four rounded corners:** front exact circular arcs replacing prior faceted approximation (24×6mm each); rear exact R20/R14 arcs **23×6mm each** (Z6..144). Upper five new rear layers add shell coverage where compatible with fixed hinge. A uniform laser-flat top rear layer at Z138..144 is partial (X<=12) to avoid the moving cheek; **Z144..150 corner shell deliberately absent** around H1. Square old keeper shafts deleted (2 pieces) since P12 clip is retired; inner fixed ears have flat 6mm-foot seat contacting lower P02 laminate at Z114. H1 annular bearings still extend above/behind nominal body, as previously authorized by owner.
- **P05 & P07:** retain C12's R20 outlines and necessary rear lid hinge cutouts. H1 pivot Y160/Z154, nominal external body 260×160×150, 6mm birch, opening 0–120° unchanged. **Two P07 hinge-relief openings remain unsealed**, separate later finishing work.
- C12: 102 cut components. C13: **110 nominal 6mm flat, single-solid components** (= 48 front laminae + 46 rear + 16 other active cut parts, no P12 and no old keepers). New 110 DXF+110 SVG profiles from one code source; not nested.

## Actual local tests and negative controls
- Focused C13 QA **33/33 assertions PASS**, code and JSON in chat bundle. 110 source solids valid. Verified each cut profile a constant 6mm layer, with CAD section area vs vector area max relative difference **0.000319 (0.0319%)**, all fit individually on portrait 800×440mm nominal stock.
- **5,253** stationary CAD part-pair checks: 0 positive-volume overlaps.
- **43,981** volume comparisons across 61 poses (0–120° at 2° intervals) of 7 moving solids vs 103 stationary solids: 0 positive-volume overlaps.
- **8,856** comparisons during 41 sampled P11 insertion positions for **each** side: 0 positive-volume overlaps.
- Verified one solid CAD shell section at Z42 with all four corners; negative control removing both rear corner layers yields multiple disconnected section solids.
- Negative external contour control: **C12 old left side exceeds R20 envelope by 8,769.633 mm³**, C13 side **0 mm³**; every wall/front/rear laminate body piece fits inside nominal R20 plan envelope. This excludes intentional H1 ear external extensions.
- Re-imported actual STEP (**110 valid solids**); re-imported GLB (**110 named meshes**); re-opened 110 SVG and 110 DXF files with matching closed contours; no bad records.

## Exact reproducible conversation assets (NOT committed in GitHub)
- Full `ETG_C13_ALL.zip` SHA256 `5f5f1ee772126ab9605e21e38ea10c2a02fc28c9d38b23778739473dba4c9f5b`, **243 ZIP entries / CRC PASS**.
- Smaller `ETG_C13_3D.zip` SHA256 `e6e488d95d506d5fbee3f1fc14029a67cd3901b1a0ca0c852eec98411dfaa50b`.
- Direct `ETG_C13_OPEN.step` SHA256 `c4bc665a0527fe9581e3fe01121c5853e499855425029eec078f9b4445c1305d`.
- Direct `ETG_C13_OPEN.glb` SHA256 `ae217a2e64705e4a8515b4486c208bf6ec589d51b816648e908bcb2aed476879`.
- Actual source files: `source/etg_c13_flush_rear_corners.py`, C4–C12 dependency chain, `build_open_c13.py`, `verify_c13.py`; tests `C13_QA_REPORT.json`, exact DXF/SVG and preview images. These are provided as user chat attachments; **PR #71 contains this handoff report but not the binary CAD and source ZIP**; do not assert GitHub-only reproduction.

## Remaining blockers / disposition
1. Top 6mm of rear curved shell is missing in the H1 clearance zone, and from Z138..144 only outer arc X<=12 is retained. The owner-approved raised H1 rings extend beyond the body, and P07 has two open rear hinge pockets. **Do not claim the body is fully sealed at rear** or that the final external H1 housing is approved.
2. CAD fit is nominal only: no measured plywood thickness, laser kerf, pin-bearing glue segregation, bonded joints' shear/peel/creep/fatigue, physical assembly or independent QA. Discrete 61 poses **are not a continuous swept-volume proof**.
3. No actual sheet nesting and no G4 production cutting files; part DXF/SVG remain `DESIGN_ONLY`.

**Outcome:** The user-reported protruding *rectangular rear corner* is corrected in the C13 solid CAD and proven within the intended external R20 body envelope (excluding intentional H1 hardware geometry), with traceable local QA. Continue to finish rear hinge relief/physical fit before production. ChatGPT-first; Codex not required for this completed local repair. Keep PR #71 Draft / do not merge.
