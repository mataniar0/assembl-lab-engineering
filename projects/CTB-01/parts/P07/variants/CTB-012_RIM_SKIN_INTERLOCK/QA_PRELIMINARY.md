# CTB-012 preliminary self-QA (NOT independent QA)

All checks below are limited to source and exported **planar** geometry. Implementer self-check, not a G1 approval, and **INDEPENDENT_QA_PENDING**.

## Observed checks
- P07T_TABBED DXF/SVG: 1 closed contour, identical exported vertices, 408 outer vertices, no outer polygon proper self-crossings.
- P07B_TABBED DXF/SVG: 7 closed contours, identical exported vertices, 408 outer vertices; all six original 36-vertex holes preserved exactly.
- P07R1/R2_NOTCHED DXF/SVG: each 64 contours (1 external +63 original kerf slots), matched coordinates, no exterior self-crossing.
- P07R1/R2_REINFORCED DXF/SVG: each 64 contours (1 external +63 kerf slots), matched coordinates, no exterior self-crossing; 18/63 kerf slots shortened per segment, source kerf Y pitch and slot count preserved.
- Base disk perimeter radius171mm, tab tip radius174.8mm, outer shell radius175mm. Tab width along neutral developed arc11.5mm versus matching notch12mm -> nominal 0.25mm per tangential side, with **no physical tolerance inference**.
- Reinforced notch-to-nearest slotted axial strip gap **6mm nominal** versus 2mm in initial version. Full material stress/rigidity not established.
- Original stock 440×800mm: each modified master fits separately by bounding box (<350×350 skins and 50×543.1 rims); combined 4-sheet stock optimization NOT rerun.
- Geometry correction count: **1 engineering revision** (2mm land initial candidate -> local strengthened kerfs). Export contour failures observed: 0. Generator source path bug found and repaired once (parent-level resolution), runtime validation of Python generator from clean repo remains NOT_RUN.

## Negative/independent checks still required
- No deliberately broken geometric samples injected; negative controls NOT_RUN.
- Independent parser/solid CAD-kernel full intersection and topology checks of ALL cut loops: INDEPENDENT_QA_PENDING.
- Actual 3D rim phase/orientation and notch-to-tab overlap / insertion sweep: NOT_RUN.
- Physical kerf, 4mm plywood flex at 18 modified cuts, adhesive, pullout, static/dynamic load and stability: NOT_RUN.
- IF-11 rim splice, internal rib/skin load transfer: OPEN.
- Source 6mm/4mm nesting: invalidated by new outline; re-nesting NOT_RUN.

**Verdict:** PROVISIONAL DESIGN-STUDY candidate, no production or physical-trial cutting authorization; G3 NOT_PERFORMED and G4 BLOCKED.
