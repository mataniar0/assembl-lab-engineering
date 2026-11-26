# MEB-037-R1 — PM numerical interface study (24 Nov 2026)

**PARTIAL / DESIGN_ONLY / G2 BLOCKED**. Owner's direction approval recorded on #125: preserve body, hinge and rails; restrict changes to skin and end-arch contact. This is not approval of a revised production geometry.

## Independent method
Read pinned MEB-033 SVG blob 8644b71371b5c4f02233b65d432ce22136e02199 and reference curve parameters at PR #128 head d66fce89f05de1b379f1ff4f8e1619b114c4e5f9. Used independent polygon/annular-sector integration in the end YZ plane times the axial slab overlap. The roof was treated as a rigid uncut nominal envelope, as in the reference. No original solid kernel rerun; direct GitHub clone was unavailable in the local CAD runtime. Tests are local end-arch studies, not a whole-assembly certification.

| Angular station subdivision (mm) | Original overlap per end (mm³) |
|---:|---:|
| 0.1 | 6.9314337029 |
| 0.025 | 6.9313593982 |
| 0.00625 | 6.9313554057 |
Reference CAD: L 6.9313552184, R 6.9313551812. Agreement within 0.000001 mm³ in the refined calculation. Left/right equivalent for this local cross-section study; the independent calculation used the left profile only.

## Candidate screening (unchanged original end profile; no mating notches)
| Candidate | Local end/skin overlap per end mm³ | Crossings of original R6 lines with proposed edge tabs, both ends |
|---|---:|---:|
| Historical stepped edge | 6.9313562 | not applicable |
| Straight baseline with no tabs | 0 | 0; fails the ten-joint requirement |
| Five evenly spaced tabs across full developed width | 24.4901877 | 12 |
| Five evenly spaced tabs across identified contact region | approximately 0 (1.28e-9 numerical) | 16 |
| Limited placement search within identified contact region | not separately recomputed; tabs remain within locally non-intersecting contact interval | minimum observed 10 |

The contact endpoint is 84.776463 mm on the developed neutral curve, and the remaining 14.394391 mm is not established as continuous end support. Extending the edge into the unsupported ear area causes overlap. The original curve parameters reproduce the historical width; the end profile, hinge axis, rails and body are unchanged in this screening. A five-tab edge on the real contact span is a candidate direction, not a validated mechanical joint. The source R6 edge lines intersect all tested five-tab candidates; the limited search cannot establish a global optimum, required material strength, or physical bending. No revised cut pattern is released. Compare mating-rim concepts in CAD and validate actual receiving geometry, rather than counting a tangent contact as a mated finger joint.

## Contact register — classification proposals only
The 26 zero-volume contacts previously marked CONTACT_UNASSESSED were grouped by expected role:
- 10 fixed fascia/backer-stack contacts (body-floor/wall/backer and backer/fascia).
- 4 hinge pin/retention contacts (end/pin and fascia/pin).
- 6 possible closure/axial-face contacts (back wall/end, end/backer, skin/backer).
- 6 saddle interface contacts (end/saddle and rail/saddle).
These are hypotheses inferred from the reference placement evidence, not verified intended contacts; all 26 remain open. No reclassification to PASS.

## Decision and remaining checks
A local collision-free straight-edge/five-tab envelope has been demonstrated numerically against the unchanged original end profile in the contact region. It is not a complete corrected CAD assembly; no ten matched receiving slots, complete insertion path, continuous motion, or material behavior has been validated. Original 190-pair results not replaced. Preserve original body/hinge/rail geometry and investigate a matched comb/rim interface in the digital CAD model, verify minimum ligaments and all joint paths, then rerun affected full assembly and export regressions. Do not use the local result to close QA-03/13/14/15/16 or to release the model. G2/G3/G4 remain blocked. No new cutting plans or manufacturing instructions.

**Count:** 1 numerical reference reproduction (three refinement levels); 3 local geometric alternatives evaluated; 1 limited placement search. Zero accepted whole-product geometry correction cycles this turn. Existing Codex correction cycle count remains one.
