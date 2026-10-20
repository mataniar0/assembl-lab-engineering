# CTB-005 — Engineering-lead selection of radial P05 rib

**Decision ID:** CTB005-SEL-001  
**Date:** 2026-10-20  
**Reviewed PR:** #14, initial reviewed head `a3287044e9f1dc84603bb1a1e9bad2ee9eb55835`  
**Selected baseline-compatible concept:** `A_RELIEVED_BOND`  
**Status:** `SELECTED_FOR_DOWNSTREAM_COORDINATED_DESIGN / DESIGN_ONLY`  
**No approval to cut, manufacture, use, load-test without plan, or represent as positively locked.**

## Evidence and independent engineering-lead spot review
- Inspected PR changed-file list (104 files, all P05 work/reports plus STATUS), three P05 study alternatives, exported profiles, section and 27-body preview, design/QA/interface reports, exact swept-route evidence, material/contact findings and CTB-007/008 handoff.
- Independent agent reports **337/337** unique test cases passing (62 P05, 71 P04, 51 P03, 52 P02, 61 P01, 25 G0, 15 import), QA score **96/100**; initial reviewer 59PASS/3 missing-document errors and later corrections were logged. Code/CAD regression counts are independently reproduced in project reports; **no GitHub-hosted CAD workflow run is registered** on this PR head.
- Engineering lead independently parsed the three actual exported P05 SVG cut profiles, recomputed polygon areas and verified no proper-segment self intersections, single connected outer contour per variant, and provisional single-part H800×W440 fit with 10mm margin:
  - A `3328.442583 mm²`, R/Z bounds `81..169/456..494`, **56 vertices**.
  - B `3081.444883 mm²`, bounds `82..169/456..494`, **158 vertices**.
  - C `3216.579431 mm²`, bounds `82..169/456..494`, **95 vertices**.
- All 259 protected CTB-000/P01/P02/P03/P04 files were reported SHA-preserved, consistent with Git diff: no upstream geometry changes.
- A produces 6 identical nominal 6mm P05 solids at 0°,60°,120°,180°,240°,300°, forming a **27-actual-body** local model with the selected 21-body base/disks and modeled collision-free continuous radial inward insertion. The P07 skins, wall, central locks and actual ring are NOT present in that 27-body BOM.

## Alternative disposition
- **A_RELIEVED_BOND — SELECTED as a CAD working design, NOT as load-bearing or positive-retention solution.** Fits original `A_RIM_OPEN/NO_HOLE` lower+upper P04 disks without versioned changes. Real rounded fillet profile has inner-edge remaining material 6.6mm upper /22.6mm lower; geometric screen only.
- **B_DOUBLE_RAIL — BLOCKED against currently selected unmodified P04.** It has nominal 28.8mm³ interference per rib with P04U. CR-CTB005-B-01 with revised L/U disk shapes remains **PROPOSED / NOT_APPROVED**, requiring separately reviewed reasons for upstream interface change, structural/assembly proof and tests.
- **C_LOWER_CAPTURE_STEP — BASELINE CAD FIT but not selected**; C's proposed lowerv2 capture has an actual filleted upper stop flat area only **2.4mm²**, below any demonstrated robust bearing performance, with neither capacity nor full restraint proven. CR-CTB005-C-01 remains **PROPOSED / NOT_APPROVED**.

## Mandatory downstream reservations and holds
- Current A radial outward withdrawal is **FREE**: no mechanical radial restraint. The P04 rim-open slots allow radial installation and reverse removal. Do not mark B06 / IF-06 or IF-08 structurally closed on strength of contact/free sliding.
- Nominal P05 plate spans Z456..494 (38mm), local r81..169, t thickness6mm; original P04 L Z456..462 / U Z480..486, 18mm between faces. A actual outer face reaches r169; radial air gap to prospective curved rim is **1.973375mm at t±3** and 2mm on axis. **Air gap is not glue or mechanical support.**
- P05-to-P07B/P07T interfaces are just flat boundary geometry; **no actual skins have been modeled, calibrated or physically bonded**. CTB-007 must engineer skin attachment, rib edge/joint, material/grain and compatible assembly sequence; any new P05 tabs, skin holes, near-rim extension or alternative anchorage is versioned and independently retested.
- Future CTB-008 top locking: tongues Z488 provide just2mm above upper disk Z486; access only while top remains OPEN. The six hypothetical Ø4 tool corridors are reservations, not valid retainers.
- B01 top anti-withdrawal and disk restraint, B02 whole-system assembly, B05 mid-ring, B06 hub/rib structural connection, B07 stability, B08/B09 rim/kerf, B10 measured thickness/kerf, B11 load/material and B13 future functional access remain open as applicable; all official CTB-000 B/IF records unchanged.
- G2 whole-assembly fit, G3 measured physical tests and G4 manufacturing release are **NOT_RUN / NOT_APPROVED**. Nominal0.2mm tangential air clearance and numerical CAD contacts are not tested adhesive bond or strength.

**Decision:** Accept PR #14 as DESIGN_ONLY six-rib study and authorize CTB-006 mid-level ring study. Keep original disks/selected A ribs as downstream CAD baselines; B/C changes remain unapproved CR proposals.
