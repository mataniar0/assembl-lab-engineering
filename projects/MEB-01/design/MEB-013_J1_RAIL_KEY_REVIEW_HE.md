# MEB-013 — J1 rail-to-endcheek through-keys (DESIGN_ONLY / NOT SELECTED)

2026-10-22 · P1 · Executor: ChatGPT direct · Codex NOT_USED · Independent QA PENDING · design-review status **REVISE_FOR_A1_AESTHETICS**. Issue #70 / Draft PR #72.

## Why
Prior **MEB-011** second-method CAD check found five nominal *rigid-contact* clusters in the moving lid because 0.2–0.4mm clearances intentionally separate joints. MEB-012 relative-translation checks found blocking obstacles, but physical connection/load transfer isn't established. We explored one cheap local flat-cut alternative for linking rails through both moving side cheeks rather than only sockets.

## J1 candidate geometry
In the existing H1-IF2 T1 nominal source, change only **6** flat-cut profiles:
- LID_FRONT_RAIL and LID_BACK_RAIL: use same 6mm stock; extend left tenons to X0.5..12, right to X324..335.5; alter tongue cross-section Z84..90mm.
- LID_SOCKET_L and LID_SOCKET_R: re-position rail rectangular pockets to Z83.75..90.25mm while keeping the researched radial roof-capture geometry and 0.4mm radial roof-ear space.
- LID_END_L and LID_END_R: add **two rectangular through-cut holes per end cheek**, each nominal6.5×6.5mm, for the two 6×6mm flat plywood rail tenons. Modelled minimum vertical material bridge above those through-holes **~4.792mm**, unverified physically.
- Rest of original 24 part profiles unchanged.

## Model-based verification
- 24/24 profile geometry valid, **21/21 original self-check assertions PASS**, **441/441** rigid sampled opening angles to110° show zero moving-vs-stationary overlap, and all part pair overlaps at0/55/110° are zero.
- **66/66** sample poses of moving left/right end cheeks sliding axially over rail keys before fixed body/pins are mounted: no intersection.
- 6 original scoped pin/overlay insertion paths PASS, 2 deliberate negative-order paths FAIL as expected, 8 X pin stop probes indicate modeled stops conditional on actual veneer attachment.
- **16/17 secondary same-author QA checks PASS**, with the still-unresolved true load-bearing/direct-continuity item failing. Do not call this independent QA.
- Renewed **full-contour design-only nesting** fits 19 parts of6mm on 1 board and5 parts of4mm on 1 board, 440W×800H; min outline gap4.3mm, and209 hypothetical centerline kerf slots; no kerf compensation.
- Repaired one report-label bug in test output (rail names mistakenly replaced by top-Z values); same geometric results on re-run.

## Why NOT promote J1 to preferred A1
Two additional through-holes in **each visible moving end cheek** may violate the selected clean A1 aesthetics even if the H1 pivot itself is flush and integrated. The ~4.79mm nominal ligament and physical joint strength are not validated. **Keep T1 as the working research candidate** and J1 as an explicit unapproved mechanical alternative. It is not acceptable to silently replace the owner's appearance with visible rail keys.

## Source custody
User-chat standalone `MEB013_J1_DESIGN_ONLY.zip` SHA256 **`e37fd8797e8761eb9f7ca891ae5fd61a913f383e5397e16553249eaeaf5f4c53`**, 71 entries, integrity PASS; contains original inherited source, T1+J1 patch, per-part research DXF/SVG, two renewed nested sheets, explanatory side-profile comparison, test code/data and Hebrew report. **The actual source and binary CAD files are not committed in GitHub**; this file is traceability only.

## Strict gates and next
Owner-frozen net inside X>=310mm, opening110°, stock800H×440W. Provisional exterior354mm, rear relief, hinge side detail, cut tolerances/real plywood thickness. No physical 4mm bend test, shoulder pin/lip strength, full 24-piece assembly, independent QA or production gate approval. **G2a BLOCKED, G3/G4 NOT_RUN**.
Next candidate must preserve flush A1 without visible rectangular end holes; plan one hidden mechanical joint or explicitly document bond-only connection and physical test authority. Executor ChatGPT first, Codex only if a new parametric kernel is genuinely required. No merge or production claim.
