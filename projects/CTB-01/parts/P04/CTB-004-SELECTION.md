# CTB-004 — Engineering-lead selection (CSH-3P anchor disks)

**Decision ID:** CTB004-SEL-001  
**Date:** 2026-10-20  
**Reviewed PR:** #12, implementation head `d7cd012772b9c7e8eefa0faad36e5cd8553396ff`  
**Selected downstream candidate:** `A_RIM_OPEN / NO_HOLE`  
**Status:** `SELECTED_FOR_COORDINATED_COMPONENT_DESIGN / DESIGN_ONLY`  
**No manufacturing, physical fit, positive lock, physical stability or strength authorization.**

## What was independently reviewed
- Full design review, interface matrix, primary and independent OpenCASCADE QA reports, geometric export source, baseline inventory, and A's 21-real-body/exploded and plan/section drawings.
- Reported 71 P04 +51 P03 +52 P02 +61 P01 +25 contract +15 baseline = **275/275 PASS**; independent review **96/100** and 22 initial failed predicates documented/corrected. Current PR has no required product CI job; those are locally reproduced test reports, not a claimed green hosted CAD workflow.
- Independently parsed **all six exported disc SVGs** A/B/C, upper and lower. Recomputed material areas:
  - A L **26899.4704 mm²**, U **26976.2704 mm²** (7/7 closed loops).
  - B L **27159.8051 mm²**, U **27198.2051 mm²** (13/13).
  - C L **27029.6378 mm²**, U **26634.8714 mm²** (10/11).
  - All nominal single-piece rectangles fit H800 × W440 with 10mm margins. Calculated area values agree with CAD reports to export-coordinate rounding.
- Observed the original 19-base plus two P04 discs without mislabelling reserved P05 witnesses, P07 skins, top wall or locks as existing BOM objects. PR change inventory contains no changed upstream CTB-000/P01/P02/P03 geometry/source files.
- Existing CTB-01 top: bottom skin Z450..456, L Z456..462, U Z480..486, upper skin Z494..500; **free disc-face gap 18mm**, pitch 24mm; tongue ends Z488 and projects **2mm** above U; no hidden 24mm free spacer assumption.
- Six real tongue holes per disk, plus six distinct P05 web interfaces; three correct 120° leg rotations and six 60° prospective web angles.
- A CAD construction assumes **Y_FIRST** base, prospective bottom-skin envelope from above **before** discs, lower disc before upper, then six OPEN radial witness insertions before wall/top closure. It does not prove final P05, P07 or locking with physical fixtures.

## Design rationale
`A_RIM_OPEN` uses one repeated P05 web connection family and its OPEN radial insertion path is simpler than B's rail-before-upper-disc route and C's mixed families/provisional inspection aperture. Choosing `NO_HOLE` avoids a non-functional central opening, does not sacrifice disc material, and is appropriate until a demonstrated locking/service requirement exists.

**Important limitations:** A's rim-open notches have **no positive radial web retention**. Actual P05 geometry, web-to-disc/skins joint, glue/bearing/wood grain/fillets, load path, fixtures and final assembly remain **unvalidated**; their design belongs to CTB-005/007/008/009. A 6mm-wide generic web witness is **not** a released rib.

## Controlled downstream interface for CTB-005
- P04 nominal diameter 190mm, thickness 6mm.
- Lower disc Z456..462, upper Z480..486, six non-tongue OPEN interfaces at orientations 0/60/120/180/240/300 degrees.
- A lower web notch starts radial **r80.8**, upper starts **r82.8**; nominal tangential width **6.4mm**; final outer notch is open to disk edge, not a closed hole.
- P05 study envelope six 6mm birch radial ribs, each radial r81..169 and vertical Z456..494, requiring an actual upper inner-edge notch clearance r81..83/Z479.8..486.2 or reviewed revised coupling. Center hole `NO_HOLE`.
- All fits are nominal, kerf/thickness unmeasured, candidate P05 throat geometry and structural retention open. Changes to P04 geometry must be versioned and reviewed rather than silently overwrite exported files.

## Remain OPEN; no official closure by this decision
B01/IF-12 upper tongue lock, B02 complete assembly order, B05 mid-ring/Z200, B06/IF-06 completed P05 web connection, IF-08 load transfer, B07 stability, B08/09 kerf perimeter, B10 measured fit, B11 structural/material loads, and B13 functional center access if future locking work demonstrates a real need. The NO_HOLE choice is the *current design baseline*, not proof no future access is needed.

**Release scope:** Authorize PR #12 merge as DESIGN_ONLY evidence and start **CTB-005** rib design. **No physical cutting** or claim of completed 50mm tabletop.
