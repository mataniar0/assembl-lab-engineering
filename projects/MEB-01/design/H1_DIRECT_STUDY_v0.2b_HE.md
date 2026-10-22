# MEB-01 A1/H1 — ChatGPT direct engineering study v0.2b
**Date:** 2026-10-20. **Status:** `DESIGN_ONLY`, `INDEPENDENT_QA_PENDING`, **PR #27 / Issue #26**. Executor: ChatGPT **without Codex**.

## Improvement on v0.1
- Corrected **all 6 volumetric moving-to-moving overlaps** detected in the previous 20-body model by replacing intersecting roof beams with arch-conforming rails and **four internal 6mm socket-plate laminates** on the insides of lid ends. The exposed outer lid cheeks remain unpierced at these joint locations; hidden laser-profiled recesses are proposed inside. Total **24 solids**.
- The pivot pin now traverses a nominal **Ø7.4mm through-bore** in the stationary cheek instead of ending against a glued face. Moving bore **Ø8.4mm**, pin **Ø7.0mm**, nominal radial motion clearance **0.70mm**; stationary bore nominal radial clearance **0.20mm**; flush cap diameter **13mm**. Center **Y=75, Z=75mm**, nominal. Face adhesive/capture still untested.
- Front and center rails have a mathematically coincident contact path beneath the **idealized** curved 4mm skin, with no volumetric skin intrusion. They enter recessed inside socket-plate channels with **~0.20mm model clearance**, not verified physical joinery.

## Computed geometric evidence (bounded scope)
- **441/441 fixed-versus-moving poses PASS** over 0..110° in 0.25° increments in exact 2.5D constant-X prismatic model.
- Minimum nominal modeled separation **0.500mm** and conservative between-sample Lipschitz lower bound **0.3362845mm**. This applies to perfect rigid conceptual solids only.
- **All 24 solid-pair intersections at 0°, 55°, 110°: 0 overlaps**.
- **Both axial insertion paths** of preassembled pin+cap geometry sampled at **121 positions each**: **0 intersections** with already-positioned model parts. Adhesive fixation/physical access remain unverified.
- **28/28 implementation SELF-REVIEW checks PASS**, including both 24-component manifold, positive-volume GLB meshes and 3 negative controls. **No independent reviewer ran these tests** and there is **no independent QA score**.
- Changes to sweep/QA implementation: after a slow first rebuild, the sweep was moved behind the main-entry guard to eliminate duplicate import-time runs. Versioned source and tests retained locally.

## Non-claim blockers
1. **Critical manufacturing gap:** some rail profiles are geometrically x-extruded prismatic solids with arch-conforming Y/Z top, not yet decomposed into directly laser-cuttable flat 6mm plywood pieces. Existing 7.5mm spacers are also not 6mm sheet parts. `STOCK_REALIZABLE_PARTS_NOT_PROVEN`.
2. **Critical joint strength/assembly gap:** rail-to-socket connection is an idealized loose-fit glue concept; no validated fastening strength, full assembly order, physical fit, or retention assurance for pin/wood head. Axial insertion no-collision is not a retention test.
3. Smooth 4mm lid skin is not a working kerf-flex patterned part; original approx **0.10mm slot ligament** `MEB-B12` stays OPEN. Bend, laser compensation, tolerance and glue `NOT_RUN`.
4. Outside length ~**345mm** vs inherited 322mm is **PROVISIONAL** and requires product-owner signoff. Scroll cavity 310×65×65mm remains nominal and not verified in actual assembled product. Sheet target **HEIGHT800×WIDTH440mm** remains FROZEN; no valid production nesting or cut-ready DXF prepared.
5. This study does **not** approve G0 complete, G1, G2, G3 or G4. `NO MERGE` until independent QA and narrowly approved scope.

## Reproducible deliverables
User-facing versioned ZIP `MEB_H1_A1_v02b_design_study.zip` created and validated in the conversation, SHA256:
`3e24e770c2f558ad1db0faeab4aac425914ee0d1fc4debcee19cb95d151ade51`
Includes `build_h1.py`, `render_h1.py`, `render_fast.py`, `qa_h1_v02.py`, 441-row CSV, diagnostics JSON, 28-case QA JSON, two actual `glb` mesh scenes, preview PNG and Hebrew engineering report. **Only this documentation is being committed to GitHub, not the binary scenes/source; the user has the downloadable ZIP in chat.** Do not assert that binaries are in GitHub.

## Next recommended executor
**ChatGPT:** redesign idealized roof rails and axial spacers into a genuine 6/4mm sheet-part architecture; develop robust interlocking joinery and captive pin fixation; rerun full model then present improved visual to owner. **Codex:** not needed until CAD system complexity or test automation demonstrably warrants it. **Independent reviewer:** mandatory before approval; **competent physical test** later required for G3.

Legacy V8.2.2 CAD untouched. See `A1_HINGE_STUDY_v0.1_HE.md` and `H1_DIRECT_STUDY_v0.1_HE.md`.
