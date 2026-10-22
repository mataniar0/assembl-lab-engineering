# CTB-017 — Bounded geometry QA, implementer self-review

## Test groups
| Group | Test count | Observed result |
|---|---:|---|
| Count sheets, body identities and CUT contours | 3 summary assertions | PASS:4 sheets,32 unique bodies,213 contours |
| SVG↔DXF entire-sheet coordinate/layer/closed/subclass checks | 4 sheet pairs | PASS, all 213 contours |
| Each of4 stock sheets respects 10mm edge margin | 4 sheets | PASS |
| Composite S02 source part integrity, rigid X/Y translation only | 22 bodies | PASS, 22/22 |
| 19 new S02 placements have pairwise bbox distances >=5mm | 171 pairs | PASS, minimum5mm |
| 19 new S02 parts vs3 inherited S03 bodies | 57 pairs | PASS, minimum7mm |
| Intentionally invalid synthetic clearance case | 1 case | PASS: shifted P05_2 moves 5mm original gap to1mm and is rejected |
| Independent standard ezdxf parser and full G2 assembly | — | NOT_RUN |

**Test-count policy:** assertions over multiple entities shown transparently; one synthetic case is separate. Parser self-review is not independent QA. Previous inherited three-part geometric proximity was not rerun, and no physical validation is claimed.

### Geometry and layout changes
One regrouping/redistribution of 19 existing unchanged vectors into the former 6mm S03. Source changes **0**, failed geometry/export QA **0**, placement repair cycles **0**. CTB-016 former S02/S04 and birch4 S01 reused unchanged coordinates, relabeled as appropriate.

### Material and manufacturing limits
BIRCH6 = 6mm nominal birch, BIRCH4 = 4mm nominal birch. Board WIDTH440 x HEIGHT800. 0 kerf compensation; no real laser kerf, beam size or grain-oriented bending qualification. Nominal edge margin10mm, gap>=5mm. CTB-012/015 rim tabs/joint shape unresolved for assembly; PR61 vertical path had ~64mm³ intersection per seam at +2mm; no motion clearance evidence that supersedes it.

**Verdict: PASS for 4-sheet 2D bounded nesting scope, DESIGN_ONLY. G2 new assembly route NOT_VERIFIED, independent QA PENDING, G3 NOT_RUN, G4 BLOCKED. Do NOT cut from these files without validating requirements and process.**
