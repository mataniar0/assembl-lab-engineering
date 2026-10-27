# ETG-004 C7R / C8 — raised H1 pivot, lid-sweep recovery and assembly-path blocker

**Date:** 2026-10-26 · **Owner decision:** Keep full central rear lid cover; allow a smoothly integrated small rounded hinge extension upward/rearward. **Stage:** `DESIGN_STUDY_ONLY / REVISE` · **Executor:** ChatGPT, no Codex. **QA:** self-check only, independent pending. **Issue:** #74. **Related body closure:** #73. **PR:** #71 remains draft/unmerged.

## Frozen vs study-only
- Owner baseline retained: nominal body `260×160×150mm`, birch 6mm, sheet H800×W440mm, H1 integrated recessed wooden pivot, lid range `0–120°`.
- Candidate center `Y160,Z154mm` and fixed ear radius16mm puts closed hinge geometry **16mm behind / 20mm above** body. This is a **study dimension, not an approved exterior profile**. Native historical V7.6 ETG parametric CAD remains unavailable.
- C7R lid `P07` is nominal single 6mm panel `X6..254/Y0..160/Z150..156`, with TWO local stepped corner cutouts, **756mm² each**, to clear the P06 ring/post during rotation. Central rear coverage is complete; **the rear-side openings remain physically open, not sealed**.

## Reproducible local evidence from current C4/C5 proxy
- First C7 had **4 collisions of 13** coarse angular positions (20°–50°) between P07 and P06 post. Fixed only local cutout profile (staggered 6mm outer strip back to Y125) and connected P06 lower post/receiver profile to valid material-land; kept body dimensions and central rear roof length unchanged.
- C7R **23/23 focused local self-check assertions PASS**, including 136 nonoverlapping fixed-parent group pairs, 25 modeled 5° moving-assembly poses, 43 extra modeled 1° positions for P07↔post in the earlier risk window, two real positive geometric web-contact checks and meaningful negative controls.
- **61/61 3D rigid CAD samples** at 2° from `0°..120°` found **no moving-vs-fixed volume clashes in this proxy**. A separate analytic central-roof-vs-rear-wall YZ section had **0/481** sampled area collisions. Finite samples **do not prove continuous swept-volume motion**, physical fit, adhesive/bearing strength or real product clearance. Original C6 flat roof had 53/61 sampled collisions at the old axis.
- Negative control: full *uncut* roof vs outer ear **383.8372mm³** clash; earlier inadequate corner cutout vs P06 keeper at 40° **64.2076mm³** clash. These are counterchecks, not failures in corrected C7R.

## Crucial honest FAIL: the entire assembly path is NOT solved
- **15/15** sampled downward insertion poses for full lid+both moving cheeks clear only with shafts/clips absent.
- **Existing P11 pin path fails on both sides** when the roof is present: first axial staging pose strikes P07 with **786.3mm³** overlap per side. The shafts therefore cannot be installed in that assumed order.
- P12 clip local top-insertion passes **11/11 each side**; keeper-post cannot install with P03/P04 sidewalls already present (at intermediate positions **144mm³** clash with the relevant wall). Assembly must be reordered and validated.
- C8 *one alternative pin direction* (head on the external side, narrow neck inside) passes **41/41** axial insertion positions per side after roof installed. However, an unchanged inner P12 circular clip has **122.18345mm³** overlap with P02 rear wall, so **internal retainer lock is NOT DESIGNED**. Pin still has an open extraction path without a positive inner clip.
- `P01/P05` front/bottom positive retention from C5/#73 remains OPEN. C7R hinge corner roof cutouts are NOT fully covered. No independent QA.

## Source, SHA and status
Actual editable Python source, STEP closed-model, 2 engineering PNG drawings, test JSON and this comprehensive Hebrew note are **in conversation ZIP** `ETG004_C7_C8_DESIGN_ONLY.zip` SHA256 `8d2356004a16f2ead9a4ed2076ab094aa93eb71593322ccbd5b627a5cb91365a`, **NOT hosted in GitHub**. This PR adds only the evidence digest; do not assert independent code review or full reproducibility from GitHub alone. `etg004_c7.py` SHA256 `1bbf2a48587a9ac2b45bab5170cfbfea1f110d453e5e0814877e2db9c22ea1db`.

## Next LEAN P1 (ChatGPT-first)
1. **ETG-004R**: choose just one P11/P12 geometry/assembly-sequence change providing actual **mechanical positive inner retention** without P02 collision and with credible flat-sheet layered construction, plus missing-retainer negative control. No blanket use of glue/friction as pin capture.
2. Check whether raised rear H1 extensions and local roof openings can have a rounded/sealed/visually acceptable cover without colliding 0–120°; keep geometry as PROPOSED until real lid design and owner-reviewed final appearance.
3. In parallel #73 body P01/P05 positive closure remains required. Defer full G2b, independent QA (>=90/no critical) and G3 material/kerf/adhesive/strength testing, G4 production. No production DXF release.

**Disposition:** `C7R_LOCAL_LID_SAMPLED_CLEAR / OVERALL_H1_REVISE`. A Codex run is **not needed merely to interpret this evidence**; delegate only a narrowly identified computational/CAD gap that cannot reliably be completed here.
