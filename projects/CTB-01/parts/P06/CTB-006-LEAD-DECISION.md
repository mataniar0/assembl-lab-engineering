# CTB-006 — Engineering lead review, conditional P06 study selection

**Decision:** CTB006-SEL-001  
**Date:** 2026-10-20  
**PR reviewed:** #22; candidate source HEAD `f1bc0804b5540f72c8ccf4974af4220aae06e73a`  
**Preferred further-development concept:** `C_CIRCULAR_WITH_VERTICAL_KEEPERS` (P06 C)  
**Release gate:** `DESIGN_STUDY_ACCEPTED / CR_REQUIRED / IF-09_OPEN`  
**Explicitly NOT approved:** existing P01 cheek modification, functional retention, G2b complete assembly, G3 physical fitting, G4 cut/production release.

## Engineering evidence reviewed
- Direct GitHub inspection of all 108 changed paths, P06 design/QA/interface/delivery reports, nominated P01 CRs, proposed C geometry, conditional 28/36/34-body assembly records and sections; 336 earlier CTB-000..P05 source/export artifacts remained unchanged by PR compare.
- Recorded focused testing: 42 new P06 + 8 interface tests + 25 contract and 15 import smoke = **90/90 PASS**, independent QA **96/100**. The **297 older unaffected component cases deliberately NOT_RUN** under Issue #15; no full nightly CAD CI exists (separate Issue #20). No hosted successful P06 CAD CI run was found on the head.
- Engineering lead separately parsed actual cut-profile SVG polygons (A ring, 3 B segments and B stop key, C ring and C keeper), recomputed net material areas, bounding rectangles and strict segment crossings; all match reports to SVG export precision and fit single H800×W440 portrait sheet with provisional margins. Independently reviewed OpenCASCADE report: changed conditional paths (A/B/C) have no nominal static/swept overlap in the **proposed** P01 variants, not in unchanged original cheeks.
- Corrected documented C fillet collision by enlarging keeper relief, rerun to clean state; other field-name, test-shape expectation and floating-point proof/preview corrections retained.

## Reason to pursue C
1. C uses a single continuous ring and six separate true wooden keepers. In its **conditional** geometry, the keys obstruct outward tangential separation of both cheeks at all three legs, which A and B do not achieve.
2. Compared with B it avoids three segmented ring pieces and the nine added P06 objects, but needs *ring before Y_FIRST cheek closure* and temporary support. This is a real assembly sequence dependency.
3. The real lower keeper shoulder seat is only **7.8 mm² per key** after rounded fillet processing, and the keeper's upward withdrawal remains free. Thus C does **not** provide a qualified self-retaining mechanical joint. Positive retention and load/bearing calculations remain **OPEN**, as do assembly access and fixture handling.

## Ring and upstream interface facts (study authority only)
- Ring 6mm birch provisional, centre **Z245**, slab **Z242..248**, band12mm and radius geometry from P06 model. Actual selected P02 S3 Z197..203 gives **39mm** clear face separation; C keeper family lower bound Z235 gives a **32mm** nominal nearest gap to spacer.
- All six original P01 cheeks **collide** with C as designed, so proposed **CR-CTB006-C-01** remains `PROPOSED / NOT_APPROVED_FOR_UPSTREAM`. The proposal replaces *all six identical* cheeks with versioned closed `26.4×6.4mm` ring mortises at the leg-local calculated station `r≈112.018,Z245`, and 12.219mm geometric exterior material land; existing four P02 and one P03 mortise must remain unchanged. No automatic mutation to selected upstream P01 sources.
- C nominal build: ring positioned/temporarily held → Y_FIRST insertion of six proposed-mortised cheeks, 12 spacers, P03 → six keys installed while accessible → unchanged 2 discs + 6 webs through their original stage order. Actual 34 finite bodies excluding reserved skins and locks. Other tested late insertions remain BLOCKED.
- All current IF-09/B05, B02 and P01 retention issues officially OPEN. Clearance is not strength; nominal material thickness/kerf, grain, glue, bearing, pullout/tipping, stability and complete table assembly NOT_RUN.

## Scope of stage completion
The *three alternatives design study* is complete and may be merged under G1 DESIGN_ONLY policy. The **ring-to-existing-leg interface is NOT complete** and **C CR approval is withheld** until an improved keeper seat and self-retention topology plus coordinated actual P01 model impact have independently passed nominal CAD. A follow-up Issue must resolve:
1. keeper **positive resistance to upward withdrawal** and meaningful load-bearing contact area with documented screened geometry, preserving insertion;
2. versioned six-identical P01 mortise updates and independent interface/swept tests for IF-09/01/02/14 against the actual current 27-body baseline;
3. ring/spacer/Y access and before-closure sequence, fixture concept and load path assumptions;
4. measured kerf/thickness and structural assessment later under physical G3, before any production claim.

**Future CTB-007** may progress with clearly declared ring geometry reservations, but must not assume IF-09 closed, approved revised P01 files or a self-retained ring. Coordination required before complete G2b integration.
