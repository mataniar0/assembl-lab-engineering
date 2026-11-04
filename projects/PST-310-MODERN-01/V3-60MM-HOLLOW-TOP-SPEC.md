# PST-310 MODERN V3 — Ø310 pre-cut top, engineered 60 mm composite box

## User-verified changes (2026-11-04)
The user's already-cut **round disc is Ø310mm**, correcting the earlier assumed Ø330mm. They want the **same hollow engineered wood-top method** developed for CTB-01: 6mm upper/lower skins, internal radial reinforcement and flexible birch4 annular shell, **overall 60mm thick**. Pre-cut upper disc remains unaltered. Preserve total plant-stand height H550mm, and the V2 three wide engineered 120° legs with cut-out windows and triangular lower bracing.

## V3 dimensional design
- Existing **top skin Ø310mm**, **6mm ASSUMED material thickness** (must be measured); top Z544–550.
- New **bottom skin Ø310mm × birch6**, Z490–496. If a second pre-cut Ø310 disc is available, potentially reusable.
- Structural cavity **48mm high**, Z496–544. Six 6mm radial ribs from R42.5 to R148.5, plus 6mm inner support ring at R32..42.5. Real positive joints between ribs, disc skins and ring remain unengineered.
- Six curved birch4 annular shell sectors, outer radius R155, inner R151, centerline R153, height48, angle60° each. Total nominal developed midline perimeter **2π×153=961.327mm** and per-segment developed length **160.221mm**. **These lengths are theoretical and NOT physical cut lengths.** No slots/kerfs included in BREP. Flexible slit pattern with 4mm row spacing requires separate CAM geometry and real bending/gluing trial.
- Three original V2 double-laminate legs (2 × birch6 per leg) retained in shape family but upper Z161–544 profile mapped to Z161–490, preserving triangular brace interface at Z155. All z538..544 tabs remapped to 484..490; the slotted hidden spider moved from Z538..544 to Z484..490, located directly underneath the new bottom skin.
- Lower triangular brace unchanged at Z155..161 and side stiffeners Z136..155. H550 overall.
- 26 BREP solids: 2 discs +6 curved shells +6 core ribs +central ring + spider +6 leg plates +lower triangular ring +3 stiffening webs.

## Actual bounded checks
- **26/26** OCC BREP solids valid.
- STEP import re-read **26/26** valid solids; GLB read-back **26/26** geometry objects.
- Nominal final solids: **325/325 pairwise OCC intersection checks**; zero overlapping volume greater than0.01mm³.
- One actual failed design iteration: 6 upper spider–leg collisions of249.163271mm³ each, due to interpolating the upper notch level incorrectly. Piecewise elevation mapping corrected: Z538→484 and Z544→490, while retaining heights below Z161. Full 325-case rerun PASS.
- Source as CAD code plus STEP, GLB, PNG and structured QA bundled in the corresponding ChatGPT conversation as `PST_310_MODERN_V3_D310_60MM_CAD_STEP_GLB.zip`. **This PR contains the specification only; no binary CAD/ZIP or Python script was uploaded to GitHub.**

## Remain blocked / physical gates
- Actual existing plate thickness and whether one additional Ø310 plate is available; intended pot diameter/weight including soil and water.
- Plate-to-leg load transfer, cuttable mortises/finger-joints in core, upper/lower skins and spider, adhesive bond / deflection, stability and tip resistance.
- Seams, 4mm birch kerf flex cuts, developed rim length calibration and physical matching to two Ø310 skins. Experience with CTB-01 rim overlap proves geometric arc calculation alone is insufficient.
- Assembly process/interference during insertion, fit coupons and kerf, wood sealing and water collection.
- **Status: DESIGN_ONLY, NOT FOR CUTTING, NOT FOR PLANT LOADING.** Do not infer safety from nominal 325/325 collision-free final BREP results.

## Next action under LEAN TASK PLANNING
P1 / ChatGPT preferred. Convert six ribs, center ring and discs to mutually locked flat-pack parts; perform independent insertion-path and load/stability checks, then kerf test and measured physical prototype. No DXF/SVG nesting/production release until validation. If user has two already-cut discs, avoid recutting either.
