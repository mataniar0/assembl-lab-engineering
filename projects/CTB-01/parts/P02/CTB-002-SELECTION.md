# CTB-002 — Engineering-lead review and working concept decision

**Date:** 2026-10-19  
**PR:** #6, source head `ea90053a5b78c7cba4c8bb949dbea8cfcabc1a24`  
**Decision ID:** `CTB002-SEL-001`  
**Working joint design:** `B_THROUGH_ADHESIVE`  
**Ring-coordination proposal:** `PC-CTB002-01`, relocate the intermediate P02 spacer to `Z=200 mm` from the original provisional `Z=245 mm`  
**Authorization:** `SELECTED_FOR_COORDINATED_DESIGN / DESIGN_ONLY`. **No manufacturing, strength, fit or final mechanical joint approval.**

## Engineering-lead review evidence
1. Reviewed current GitHub PR #6, exported 3D and 2D illustration, `CTB-002-DESIGN-REVIEW.md`, `CTB-002-VALIDATION.md`, `CTB-002-INDEPENDENT-QA.md`, interface matrix, parametric design, generated SVG and collision/ring data.
2. Reported current suites: 52 P02 tests + 61 P01 regression + 25 CTB-000 contract + 15 baseline integrity = **153/153 passed**, independently rerun by a separate automated QA reviewer.
3. Independently read B candidate exported SVG polygons and checked dimensions and their four P01 opening positions. Computed minimum distances from each opening to original cheek exterior: **8.000374, 11.915840, 13.582199, 18.300000 mm**, consistent with independent OpenCASCADE QA. Each candidate plywood part fits a single portrait **H800×W440 mm** cutting sheet with **provisional** margins.
4. Original P01 source and CTB-000 frozen contract remain unchanged. Candidate P01 mortises were placed only under P02 study, not in the approved P01 source. Nominal spacer BOM: P02×9 + P02B×3; 4 spacers per leg.
5. Nominal B local 3D assembly reports 15/15 final pairwise and 15/15 swept insertion intersections at zero. This is **CAD collision evidence only**, not physical slip-free/adhesive load evidence.
6. Repair disclosure includes initial C weak-land failure, wrong test inventory assertion, review illustration corrections and broken fresh GLB generation due to missing SciPy; all reported corrected, including successful clean regeneration. Alternative A **BLOCKED** for 1.71687mm exterior land and incomplete lock/insertion concept.

## Reason for B working selection
- Four nominal mortises per cheek vs eight for C; no overhanging keyed-head envelope or very thin land as in A.
- Candidate B spacer sizes (P02 radial 30 mm; lower P02B radial 40 mm) give simple repeatable pieces, wider candidate lands, and an independently cross-checked collision-free *local* nominal insertion route.
- **Important limitation**: tab shoulders only resist one direction of cheek motion; there is no demonstrated positive outward retention without separately engineered adhesive/capture mechanism. Thus no completed G1 lock/release is granted.

## Ring interface (B05/IF-09)
- Working stations `Z=[35,90,200,390] mm`: lower part P02B at 35, P02 standard parts at 90/200/390, duplicated identically across 3 legs.
- Proposed S3 move from 245 to 200 leaves **22.0 mm** between its top surface at Z203 and the conservative ring reserve bottom Z225 (**21.8 mm** from candidate mortise edge).
- `Z200` is **accepted as a provisional downstream design coordinate**, subject to CTB-006 design and independent 3D ring collision checks. This decision **does not alter CTB-000** or close B05/IF-09.

## Conditions / holds for future tasks
- CTB-003 Y connector: preserve selected SOFT_CURVE exterior and versioned P01 B mortises; solve Y-tip `r94` vs P01 envelope `r90` (B04); coordinate with upper P02 at `Z390`. No silent modification of upstream.
- CTB-006 mid-ring: explicitly evaluate Z200 and finalize ring engagement; any P02 revision must be versioned and tested.
- CTB-008 positive top retention and complete system assembly remain unresolved. A later separate design decision must resolve B's cheek-spreading retention/adhesive strategy before G3 physical prototype approval.
- B01/B02/B03/B04/B05/B07/B10/B11 and all other baseline issues preserve their official state until evidence-backed issue closure.
- Real thickness, kerf, glue/cure, plywood/adhesive structural loads, tipping and full-three-leg integration have **not** been demonstrated.
- All DXF/SVG are `DESIGN_ONLY` uncalibrated study files, not released machine instructions.

**Decision:** Approve merging this reproducible *design study* and starting CTB-003 (Y coupling), without implying mechanical production release.
