# ETG-000 v0.2 — H1 Interface Control Draft (ICD)

**Gate:** G0_DRAFT / DESIGN_ONLY. **Issue #18, ETG-CR-001.** The owner approved adopting the H1 architecture in place of FCIPH on 2026-10-21, but no H1 dimensions, physical construction or QA pass have been approved. Use LEAN TASK PLANNING v1.1, Engineering Playbook, QUALITY_STANDARD and GATES.

## Source of truth
`parameters.json`: frozen product-specific body/material/sheet and open H1 dimensions. `PARTS.csv`: 13 **provisional** part families. `interfaces.csv`: 28 OPEN IFs; `OPEN_ISSUES.csv`: 12 blockers. `LEGACY_REGISTER.md`: frozen historical FCIPH evidence only. `ETG-CR-001-H1.md` logs the owner change.

## ETG envelope and frames
Body outer 260×160×150mm, nominal structural birch6mm, sheet X0..440/Y0..800mm portrait. +X length, +Y rear, +Z up. **H1 external rear envelope, axis and clear fruit cavity are OPEN**; FCIPH depth ~178.4mm and diameters are not current design. Required H1 lid swing 0..120° in **ETG**, not MEB 110°. End user etrog and optional tray must remain accessible.

## Mechanism groups / BOM mapping
A **fixed body hinge support** integrated in rear P06 laminated corners (and dependent P02/P03/P04 details). B **moving lid cheeks** P09/P10 and P07/P08 joint. C **wooden pivot pins** P11 ×2. D **flush retaining caps** P12 ×2, seated in rear corner sides, mechanically captured without large external ring. Supports, moving cheek bores and pins coaxial in one XYZ reference system, with credible lamination from flat stock and no concealed incompatible parts.

MEB-01 H1 research diameters pin7, fixed bore7.4, moving bore8.4, cap13; 4mm cap; 0.5mm axial clearance and two 6mm pin-layer concept are **NOT** frozen ETG dimensions or proof of manufacturability. FCIPH Ø14 pin/Ø32 ear are historical only.

## Interface review
IF-01..08 original panels and corner joints. IF-09..14 + IF-25..28 H1 supports, rotating cheeks, dual pins, cap placement and positive axial capture. IF-15..19 and IF-24 moving lid-frame/skin fit with **real thickness** through 0..120°; check every angle and rear wall. IF-20..23 ensure internal tray and fruit keep-out. Legacy 96 corner layers and two-sheet nesting are unverified with H1.

## Acceptance boundaries
G0: validate traceability/IF references, state of unknowns and source provenance, independent QA >=90/100 and no in-scope critical blocker. G1: proposed parametric source, export geometry and actual part topology. G2a/G2b: independent real-solid motion, continuous insertion and anti-escape; test missing cap, wrong-axis and forced early assembly controls. G3 actual plywood/kerf/cap attachment wear and durability NOT_RUN; G4 cutting/production NOT_AUTHORIZED. H1 design-direction approval is not approval of fabricated parts.
