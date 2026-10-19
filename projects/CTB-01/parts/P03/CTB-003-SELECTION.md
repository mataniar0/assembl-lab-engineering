# CTB-003 — Engineering lead design review and selection

**Decision ID:** CTB003-SEL-001
**Date:** 2026-10-19
**Reviewed PR:** #8; reviewed head `cf20ffdf5417cc5b0c149a66fcae4f448a4bf349`
**Selected working variant:** `A_COMPACT_CLOSED`
**Assembly method for ongoing studies:** `Y_FIRST` (install Y before all three cheek/spacer leg subassemblies)
**Status:** `SELECTED_FOR_DOWNSTREAM_COORDINATED_DESIGN / DESIGN_ONLY`
**Not approved:** final positive locking, physical assembly fit, design loads, structural stability, actual kerf compensation, nesting or production.

## Evidence and independent spot-check

- Reviewed three variant comparison reports, 19-piece base image, A working joint render, original/exported geometry, source controlling JSON, insertion evidence, issue matrix, primary QA and independent OpenCASCADE QA.
- Reported **204/204 final unique tests** passed: P03 51, P02 52, P01 61, CTB-000 25, CTB-000 import 15; independent agent reran tests and separately reconstructed exported geometry using a second CAD kernel.
- Independently read SVG polygons of all three P03 variants. Areas re-derived:
  - A: **5113.524876 mm²**; 489 points; maximum global XY radius **85.769983 mm**; no proper-segment self-crossings.
  - B: **5261.684236 mm²**; 621 points; maximum global XY radius **85.769983 mm**; no proper-segment self-crossings.
  - C: **4960.224855 mm²**; 489 points; maximum global XY radius **82.281468 mm**; no proper-segment self-crossings.
  - All single-piece profiles satisfy H800×W440 with provisional 10 mm sheet margins.
- Verified A's candidate P01 export has **one extra closed Y mortise per cheek**, retaining four existing P02/P02B holes. No original P01/P02/CTB-000 file was modified in the PR inventory; 118 protected sources were independently byte-compared by QA.
- A local arm endpoint at **r85.5 mm** leaves **4.5 mm nominal** to P01 outer r90. The old provisional Y tip r94 (4 mm overhang) is superseded **for downstream candidate geometry only**, without editing the frozen G0 contract.
- Reported all 19 solid bodies with **171/171 nominal static pair checks** and **171/171 continuous swept/prior-solid checks**, following **18 moving installation stages** on the Y-first method; independently repeated in OpenCASCADE. Known prebuilt-module translations for A all blocked. Physical fixtures, access, force, deformation and adhesive cure are not modeled.

## Rationale for selected A
One closed Y mortise per cheek instead of B's two, simpler cut geometry, more exterior residual land (A 15.8 mm) than B's near-edge 7.8 mm, preserved selected SOFT_CURVE exterior, and a continuous nominal CAD Y-first assembly route. C requires an externally visible inner-edge notch and a separate retainer to prevent reverse radial withdrawal; **C change request remains not selected**.

## Geometry authority and holds
- Downstream CTB-004/005/006/007/008/009 should reference `A_COMPACT_CLOSED` source and the versioned **P01-Y-mortise-study-v1** when checking the actual current leg geometry. These are design candidate authority, not cut-ready geometry.
- The model imposes **Y at Z407..413**. A's Y mortise Z406.8..413.2 has an **actual vertical edge clearance 13.6 mm** from the P02 S4 mortise ending Z393.2. Material margin value is geometric and not a validated strength/web requirement.
- Preserve CTB-002's working `Z=[35,90,200,390]` spacers with B joint; Z200 awaits CTB-006 real ring clearance.
- The baseline still lists historical provisional Y r94, and its 14 IF/13 B records remain byte-preserved. The **nominal B04 conflict is provisionally resolved for variant A**, but the official B04 issue remains open pending combined fit and load-path evidence.
- **Do not prebuild all three legs** and claim to install a closed-hole A Y afterwards. Use the demonstrated Y-first staging for all downstream assembly simulations.
- B01 positive top retention, B02 whole table assembly order, B05 ring, B06 radial ribs/discs, B07 tip-over, B10 measured thickness/kerf, B11 structural loads and positive **outward separation** of each cheek are unverified. Local collar/tab/gap geometry doesn't close these blockers.
- All 3D exports are nominal rigid material, no tested glue, clamps, fixtures, grain, load rating or production release.

**Decision:** Accept PR #8 as an accurately limited DESIGN_ONLY component design study. Authorized to merge and proceed with CTB-004 two anchor-disc study; do not announce a complete safe structure or cut-ready files.
