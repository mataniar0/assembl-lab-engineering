# P01 — engineering-lead selection for downstream design

**Decision ID:** P01-SEL-001  
**Review scope:** CTB-001 / PR #4 / source head `3de6fcbafdc53d4bdf5c27121c57739c2bf00b57`  
**Date:** 2026-10-19  
**Selected variant:** `SOFT_CURVE`  
**Status:** `SELECTED_FOR_DOWNSTREAM_COMPONENT_DESIGN / DESIGN_ONLY`  
**Decision authority:** Engineering lead, under product owner's delegated progression authorization. User may change aesthetic choice through a documented design Change Request.

## Evidence reviewed
- P01 61/61 final automated geometry/export checks; contract 25/25 + import 15/15, independently rerun by separate QA.
- Engineering lead inspected `model.py`, `generate.py`, design input, comparison render, QA reports, and exported profile SVG for all three variants.
- Additional independent direct SVG checks: 3/3 contours with no strict segment crossings; computed areas matched recorded values, and each bounding envelope fits nominal portrait H800×W440 with provisional 10 mm margins.
- Repaired 4 initial failed automated cases, re-tested; no unresolved *concept-geometry* defect reported.

## Engineering / product rationale
`SOFT_CURVE` gives the most continuous balanced radial sweep and lowest flat face material area (24,385.48 mm²) while keeping the same candidate upper tongue and nominal ground landing as other variants. The selection is aesthetic/manufacturability concept judgment, **not** a strength or stability comparison.

## Scope of permission
- CTB-002 may use SOFT_CURVE as the active **6 identical P01 cheek** master profile.
- Other two variants remain in repository as alternatives/reference, not additive BOM.
- CTB-002 can propose spacer-to-cheek mortises or minor geometry modifications in a **separate coordinated proposal**; do not silently change the selected cheek profile, frozen CTB-000 baseline, or machine settings.
- IF-01 shall not be deemed mechanically resolved until modified cheek and spacer are co-validated with explicit 3D insertion/collision sequence.

## Open blockers and non-approvals
- B01 (positive top locking), B02 (whole-system assembly sequence), B04 (Y reaches r94 vs cheek r90), B05 (ring reserve z225..265 overlapping spacer reserve z237..253), B07 (stability), B10 (actual stock and kerf) and B11 (material/load) remain unresolved.
- All other CTB-000 interface statuses and B01–B13 remain unchanged.
- No final P01 slot geometry approved; no complete G1 joinery approval; G2 integration, G3 physical testing, manufacturing DXF release, and load ratings remain blocked.
- Comparison/layout render captions marked 'AWAITING_DESIGN_SELECTION' are historic exports from before this decision; they are not the selection authority. This signed-off decision text supersedes only that old status caption.

**Decision:** Approve SOFT_CURVE as a concept reference so coordinated CTB-002 spacer design can begin. Do not represent this as assembled, structurally verified or cut-ready.
