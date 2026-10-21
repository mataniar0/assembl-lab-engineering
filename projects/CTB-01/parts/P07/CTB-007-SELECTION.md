# CTB-007 — Engineering lead selection, P07 skins and mathematical kerf perimeter

**Decision ID:** CTB007-SEL-001  
**Date:** 2026-10-21  
**PR:** #32; independently reviewed original head `f07c916dd10d2405823ad03fed747e82897560e8`  
**Selected CAD working concept:** `A_TWO_BUTT_BOND`  
**Status:** `SELECTED_FOR_DOWNSTREAM_DESIGN_STUDY / DESIGN_ONLY / KERF_COUPON_PENDING`.  
**NOT approved:** actual laser cutting, plywood bending, physical assembly/use, G3, G4, full structural skin attachment, positive locking, material/coupon parameters, released sheet nesting.

## Evidence and engineering-lead verification
- Examined PR #32 diff/path inventory (119 scoped paths: P07, CTB-007 reports and STATUS only), design review, independent second-kernel QA, tested nominal rigid insertion/blocked paths, 3D/exploded drawings, interface matrix, P08 handoff, physical validation plan and C-only coordinated change proposal.
- Agent reported **93/93 unique focused automated PASS** (46 new P07 +7 interface+25 baseline+15 import), independent OpenCASCADE scored **96/100** (zero in-scope critical or major). **347 unchanged old component cases NOT_RUN by approved risk-based policy**. No hosted CAD/nightly workflow PASS; infrastructure Issue #20 OPEN.
- Reviewed independent reconstruction of 31/32/33 true positive-volume CAD bodies, focused complete swept routes, cross-kernel profile comparisons and actual finite kerf openings, not an uncut cylindrical replacement. These are **mathematically pre-bent**, not wood bending results.
- As separate engineering-lead spot review, parsed **all 15 SVG files** (P07B/T + 2 A rim strips, +3 B rim strips, +4 C strips): independently measured signed polygon areas, path counts, bounding rectangles, zero duplicate consecutive vertices, zero proper self-intersections within each polygon, each part single-sheet H800×W440 screening including provisional10mm clearance. A bottom skin has exactly six removed tongue windows; A top is one continuous NO_HOLE exterior; each A rim strip has 63 actual interior cut apertures. Main A net SVG areas: P07B **90951.178 mm²**, P07T **91858.647 mm²**, each strip **25441.176 mm²**. Single-part bounding screen is **not production nesting**.
- Upstream 439 protected CTB-000/P01–P06 files were reported independently byte-for-byte unchanged and PR diff confirms none modified; current model consumes selected pre-P06-ring 27-body baseline with no hidden P06 ring or P08 lock.
- Primary generation, C micron-scale duplicate-edge export, contact/keepout/display corrections and second-kernel parser/sweep/contact counting repairs are disclosed in validation and QA reports. Expected blocked routes remain blocked.

## Alternative comparison and decision
- **A_TWO_BUTT_BOND — SELECTED_FOR_DOWNSTREAM_DESIGN_STUDY**: 2 flat 6mm skins at nominal inner-rim radius171; 2 nominal 4mm kerf strips inside annulus R171..175, preserving Ø350/50mm external envelope and stock. Least new interface change, 31 finite CAD bodies total. Nominal A rim insertion vertical or radial before top passes; rim after top can fit by a named route but cannot restore future top-lock installation access. No positive butt splice bond; actual join length/calibration UNKNOWN.
- **B_THREE_STEPPED_BOND — ALTERNATIVE / NOT_SELECTED**: 3 segments with staggered step joins; nominal vertical closure BLOCKED, radial route passes; **zero nominal step vertical clearance** is not physical fit or strength.
- **C_FOUR_EDGE_COMB — ALTERNATIVE / NOT_SELECTED**: 4 strips and a P07-local six edge tab construction, proposed `CR-CTB007-C-01`, **NOT_APPROVED**. C includes interrupted skin/rim contact, increased part count and timing restriction; no silent promotion of skin radial tab geometry.

## Critical physical and functional holds
- Frozen overall Ø350, H500, top50; bottom P07B Z450..456, core Z456..494, top P07T Z494..500; P04 L Z456..462/U Z480..486; P05 r81..169. A skins radius171, nominal perimeter r171..175. Mathematical R173 neutral circumference 1086.991mm is not an experimentally measured physical strip length. Workpiece H800×W440 portrait; **two nominal 543.496mm-arc segments** per A concept (actual export edge gap). Manufacturing seam dimensions, actual web/slot behaviors and grain/kerf response remain unknown. No physical bending claim.
- Bottom six actual slots align with six accepted P01 tongue positions, top NO_HOLE is closed. Upper cheek tongues endZ488, only2mm above P04U, 6mm below top skin underside494; six hypothetical Ø4 probes exist only with top open and **are BLOCKED after top closure**. CTB-008 MUST engineer real positive anti-withdrawal/tongue lock and assembly access before closing top.
- Original P05-to-rim `1.973375..2mm` **AIR gap**, not glue. P05-to-skin geometric edge area516mm² per rib/per skin, lower disk-to-bottom ≈26899.470mm², and A rim-to-skin ≈6441.722mm² per skin are only potential physical interface areas — zero qualified adhesive/contact strength. Upper P04 disk remains8mm below top underside; no fictitious upper-disk contact.
- **CTB-006R #23 OPEN** (P06 keeper lifts freely, selected C ring requires unapproved P01 mortises) and IF09/B05 remain OPEN. Project must not claim complete lower ring installed; B01/B02/B06/B07/B08/B09/B10/B11 remain OPEN as relevant. Original official interface/blocker records preserved.
- Rim is experimental kerfed 4mm birch with nominal0.8mm voids and8mm pitch only as study hypotheses. No physical bend coupons, measured kerf/stock, adhesive specification, kerf/finish validation, load/deflection/stability data, tool/hand fixture verification, or final production nesting.

**Decision:** Approve merge of PR #32 as a rigorously bounded G1/G2a CAD study; authorize opening CTB-008 top-lock concept and CAD task; keep physical G3 / release G4/production blocked. No candidate for real cutting is approved.
