# CTB-020 — rim circumference mismatch after real cutting (DESIGN_ONLY / HOLD)

## Observed physical failure
User cut 6mm tabbed skins P07T/P07B and two 4mm CTB-019 flexible rim strips. During dry assembly the **rim ends overlap** rather than closing at the intended puzzle seams. Amount of overlap **NOT MEASURED**. No arbitrary production correction is authorized. Do not change or recut the already-cut 6mm parts. This document provides a **conditional, fully dimensioned test hypothesis for 4mm rim parts only**.

## Audited original cutting geometry
- 6mm skin core/base circle R171mm (Ø342), 12 protruding tabs to R174.8mm (Ø349.6). These are the exact CTB-017 cut skins.
- 4mm rim original nominal inner R171, mid-plane R173, outer R175 (design OD350).
- CTB-019 rim flat body length between seam stations: `Lold = π×173 = 543.495529mm` **per rim**, two-body total `2Lold = 1086.991058mm`.
- Main P07R1/R2 cutting envelope includes 8mm puzzle projection: width50mm, outer length551.495529mm.
- Angular registration of 12 tabs vs six notch stations per rim was previously confirmed in CTB-019; widths12mm and depths6mm nominal. No measured cutting tolerance.

## Correction relationship — requires actual overlap O
If **one puzzle joint is engaged, each rim is in its intended notch location, and O is the overlap along the circumference at the other joint**, a *first-order estimate* (not proof) is:
- two-rim new body total: `Cnew = 1086.991058 - O`
- each rim's new body length with symmetric correction: `Lnew = 543.495529 - O/2`
- implied developed fit radius: `R_eff = 173 - O/(2π)`.
- corrected nominal notch center y along rim (original centers 45,135,225,315,405,495): `ynew = 0.2 + (yold - 0.2)×(Lnew/543.495529)`.
- preserve **12mm notch aperture width, 6mm notch depth, the complete 50mm rim width, and both puzzle silhouettes**; shift each notch as a whole. Adjust flex rows inside available solid using the 4mm pitch, not by trimming only the two puzzle edges.
- correction is **conditional on uniform circumferential mismatch**. It cannot correct skew, local distortion, incorrect slot fits, wrong kerf setting, or end-seam motion collision.

## Single R171 numerical hypothesis — **DO NOT CUT AS AN APPROVED SOLUTION**
Consider the special possible case where `O = 2π×(173-171) = 12.566370614mm`. This is the theoretical difference between midline and inner circumferences, NOT an observed overlap.
- New body length each: `537.2123437mm`.
- New two-rim body sum: `1074.4246875mm`.
- Length reduction per rim: `6.2831853mm`.
- Seam end local max y shifts from543.695529 to537.412344, puzzle relative shape unchanged; new total silhouette length including 8mm projection: `545.212344mm`. Width remains50mm.
- Original y-notch centers [45,135,225,315,405,495] become [44.482081,133.441618,222.401156,311.360694,400.320231,489.279769]mm.
- All 12 physical 6mm skin tabs remain unchanged; their center angles align to the numerical R171 hypothesis within ~3e-9rad rounding.
- At each narrow notch band the rim slit pattern remains alternating A/B, shortened locally. Generated sample row pitch4mm, 130 rows (Y=8..524), 195 open one-pass slit cuts per rim. Baseline CTB-019 was 132 rows,198 open cuts. Old rim masters not overwritten.

**Hypothesis DXF/SVG files provided solely for engineering comparison:** `P07R1_R171_HYPOTHESIS_DO_NOT_CUT.{svg,dxf}`, `P07R2_R171_HYPOTHESIS_DO_NOT_CUT.{svg,dxf}`. They are deliberately NOT inserted in production nesting or a ready-to-cut ZIP to prevent accidental use before real calibration.

## QA completed in this study
- 2/2 hypothesis rim SVG↔DXF exact numeric outer vertices and all open line cut coordinates.
- 76 outer contour vertices/rim; correct closed DXF external contour and195 LINE entities/rim; zero slit exits through intended solid cross-section except intentional B edge termination.
- All six notch widths remain12mm under constant shift inside each 12mm band (contour point y positions shift by common center offset).
- Lower puzzle shape **exactly identical**; all14 high-end puzzle vertices translated by same6.283185mm, thus preserving local shape. Both rim halves identical, so their **relative mating geometry** retained.
- 4mm nominal slit pitch (Y successive increments exactly4mm); rows do not enter 8mm end puzzle profile.
- CAD Boolean, full 3D assembly movement and mechanical tests not run. Physical fit **FAIL for CTB-019**; candidate status **UNVERIFIED**, G3=HOLD.

## What measurement is still needed (non-destructive)
1. Assemble one puzzle connection loosely and place both 4mm rims around the already-cut 6mm skin, no glue; align all skin tabs in their corresponding rim notches (never force them).
2. Mark the amount by which the other seam overlaps **along the circumferential direction**, compare at top and bottom skin edges. Measure the marked distance after unwrapping (mm). Report O.
3. Report if all tab-to-notch sites actually register, and any cracking/visible bowing. If these do not register, do **not** assume uniform length reduction solves the issue.
4. Replace theoretical O by measured O in above equations and regenerate **rim-only** SVG/DXF and new 4mm nesting, followed by QA and short fit/bend coupon **before** another full 4mm rim cut.

## Escalation and workflow
P1 physical mismatch. ChatGPT: diagnostic, parameterized geometry, nominal 2D and file checks. Independent CAD-kernel verification if 3D fit or movement cannot be established locally; qualified physical test required for wood bending and kerf. Preserve all CTB-017 6mm source geometry unchanged. Do not merge this speculative PR or CTB-019 until failure resolved and review complete.
