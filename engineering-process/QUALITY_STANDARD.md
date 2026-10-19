# Independent QA, evidence, and scoring policy

## Independent review required
An independent reviewer must examine the actual source, exported geometry, fixture/assembly assumptions and logs. Do not call the implementer's own self-tests "independent QA." If a distinct reviewer cannot be reached, mark `INDEPENDENT_QA_PENDING`, not `PASS`.

## QA score for G0–G2 design/code delivery (100 points)
| Dimension | Points |
|---|---:|
| Contract, traceability, approved vs provisional values | 20 |
| Geometry / CAD / export integrity | 25 |
| Interfaces, assemblies, path checks (where applicable) | 20 |
| Reproducibility, negative controls, regression tests | 20 |
| Documentation, visuals and handoff clarity | 15 |
| **Total** | **100** |

Score >= 90 **and no critical blocker in the scope being approved** is required to approve a PR. A task may contain legitimately OPEN later-gate risks if the PR is unambiguously `DESIGN_ONLY` and does not claim those risks resolved. A passing score does not imply physical structural safety or manufacturing approval.

## Required review actions
1. Verify source-of-truth files and approved/derived/provisional values.
2. Rebuild exports from a clean environment when supported; log versions and commands.
3. Parse actual DXF/SVG paths: closed, unique, non-overlapping, no orphan islands, correct layers/units.
4. Derive geometry checks from exports, not solely source implementation tests.
5. For joints: quantify clearance, minimum geometric land, full 3D insertion paths, and obstructed alternatives. **Minimum CAD land is not material strength certification.**
6. Test intentionally broken examples to prove invalid geometry is detected; report negative controls separately from meaningful passing production geometry.
7. Check cut-stock dimensions **for that project** and distinction between single-part fit and production Nesting.
8. Compare BOM to model part instances and identify missing/extra parts.
9. Report every failure, correction, and retest. Do not replace failed logs with a passing-only account.
10. Mark absent actual plywood/kerf/glue/load/physical testing as `NOT_RUN`.

## Failure taxonomy
- `CRITICAL`: impossible required assembly path; major collision; invalid cut geometry; incompatible frozen specs; unsafe unsupported production claim; evidence fabrication.
- `MAJOR`: unverified important interface, loss of reproducibility, missed regression, inaccurate dimensional render.
- `MINOR`: cosmetic annotation, documentation layout, non-impacting readability issue.

## Reporting
Use [QA report template](TEMPLATES/QA_REPORT.md) and [delivery template](TEMPLATES/DELIVERY_REPORT.md). Log total **unique tests**, explicit counts per suite, **failed attempts**, number of repairs and cycles, unresolved issues and exact gates they block. The same logical case rerun is not a new unique test. Any report missing proof must say so.

When reviewing documents/templates only, adapt relevance: document checks, broken-reference tests, task simulation and policy contradiction checks replace non-applicable CAD geometry checks; mark that scope explicitly.
