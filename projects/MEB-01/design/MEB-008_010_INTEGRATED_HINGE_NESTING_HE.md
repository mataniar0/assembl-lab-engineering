# MEB-01 — H1-IF2 integrated pivot and nesting, ChatGPT handoff (MEB-008–010)
**Date:** 2026-10-22 · **Owner request:** complete ChatGPT-first work through nesting · **Executor:** ChatGPT; no Codex · **Status:** `DESIGN_ONLY / INDEPENDENT_QA_PENDING / G3_NOT_RUN / G4_NOT_APPROVED` · **Issue:** #70.

## Existing contract / design
Owner-frozen: minimum net usable cavity X310mm, 110° lid opening, sheet HEIGHT800×WIDTH440mm. Chosen product appearance: A1 classic arched lid and H1 wooden pivot elegantly integrated into side. Provisional physical values: structural birch6mm, kerfed skin4mm; final outer X length, glue, actual stock thickness, bend neutral axis all require owner/physical validation.

## Direct ChatGPT design evolution
- MEB-006 B1 used E1 roof ear concept; MEB-007 increased ear axial length to 6mm. Initial concentric discs (PIN and CAP) were **unbonded** and failed true positive restraint: pin could travel inward ≥3mm.
- MEB-008 H1-IF2 concept: 1 flat `XZ` integral headed wooden pin per end from nominal6mm plywood. The shaft has Y thickness6mm, Z width3.4mm and a 4mm-long shoulder of Y6×Z10mm. Updated middle body side veneer (4mm) carries a recess for shoulder; **additional exterior 4mm continuous wood overlay with small 6.4×3.8mm tip aperture** catches the head outward. The round moving lidend hole catches the head inward after ~0.5mm play. The face of pin tip is level with outer overlay. The two original decorative floating caps and four laminated round discs are removed.
- The 4mm fascia/overlay outer contours now include **smooth cubic-Bezier transitions from side panel to hinge boss**. The rear boss is part of the continuous SIDE PANEL contour. It **still projects nominally 9.5mm behind the original straight wall**: do not imply a totally flush rectangular silhouette or claim owner-approved aesthetics.
- The two outside 4mm veneer additions extend overall X envelope to **354mm provisional** vs 346mm previous. Actual internal cheek-to-cheek span still **312mm** X12..324. Roof ear retention is geometric only, 2.1mm wood lip remains untested. Back-body top relief68.8mm is provisional, not approved.

## Bounded CAD checks
- 24 source parts; nominal19×6mm +5×4mm. Flat profiles from one parametric source.
- **21/21 self-authored geometric test assertions**; zero mixed stationary/moving volume collisions at **441** sampled angles from0° to110°; **0 3D-prismatic pair overlaps** at0°,55°,110°.
- **Two pins × inward/outward × 0/110 =8 retention displacement scans** demonstrated first clash outward0.05mm with external overlay and inward0.55mm with moving end plate, CONDITIONAL on strong overlay attachment and rigid body model.
- Six selected insertion paths PASS across **504** sampled positions: four pin introductions at0/110 and two outer veneer applications *after* pins. Two deliberate negative-order tests identified interference as expected; no full 24-part assembly insertion proof.
- Actual storage prism X12..324, Y6..71,Z6..65 had **0 modelled intrusions**; this is not a fit test with actual rolled scroll.
- Three development corrections: (1) distinguish roof X length vs 4mm stock thickness in assertions; (2) align kerf-line rotation/translation with whole roof shape; (3) smooth boss transition while preserving original bearing annulus.

## MEB-010 contour nesting
Computed with **real Shapely part outlines** (not just rectangles), with exact collision/distance checks after deterministic shelf placement, no optimization claim.
| board material | parts | boards 440W×800H | net profile area utilization | occupied length H | centerline slits |
| 6mm |19|1|25.3%|~345mm|0|
| 4mm |5|1|15.34%|~200mm|209|
Minimum outline distance **4mm**, nominal sheet margin **≥10mm** for each. All 24 DXFs/SVGs and both sheet DXFs/SVGs generated from source; DXF unit flag millimeters and path counts reparsed; SVG files parsed. 209 slits remain **zero-width theoretical centerlines**, neutral-axis parameter ~99.17mm developed distance remains **unmeasured**. **Not manufacturing nesting / not cut-ready**.

## Reproducible files
Local ZIP created and verified in a separate fresh extraction:
`MEB_H1_Integrated_To_Nesting_DESIGN_ONLY.zip`; SHA256 `613220637eab6d3f88ad4d037f36a505eb385aa9fe4bacc123726e491b89aad5`; 76 entries, around903 KB. Includes complete Python sources `build_integrated.py`, `assembly_qa.py`, `export_and_nest.py`, `render_assembly.py`, inherited reference sources, 24 DXF+24SVG, 2 nesting DXF+2 nesting SVG+PNGs, 0/110 GLBs, CAD preview, JSON QA, manifest and Hebrew delivery report.
**These CAD/binary files are available in user's conversation ZIP, NOT committed to GitHub**. A scoped code review requires making source available to the reviewer. This GitHub document is audit metadata only; no merge yet.

## Nonclaims / next gate
- No proof physical H1 pin/fascia bond, bearing load, 2.1mm lip integrity, 4mm kerf wood bend, fatigue, dimensional tolerance, full 24-piece assembly, independent QA or G3/G4 physical/production readiness.
- **P1 next:** independent model QA with a separate reviewer then prototype and owner approval of 354mm exterior/smooth bearing silhouette; a separate physical materials assessment is needed. **No Codex at this handoff**; LEAN ChatGPT-first, targeted Codex only if a new bounded computational gap is demonstrated.
- This report does not modify V8.2.2 reference or approve dimensions.
