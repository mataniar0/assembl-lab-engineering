# ETG-01 — מצב פרויקט

**Overall:** `G0_DRAFT` / **Production:** `DESIGN_ONLY`
**Tracked issue:** https://github.com/mataniar0/assembl-lab-engineering/issues/18
**Independent QA:** `INDEPENDENT_QA_PENDING`
**Native geometry:** `LEGACY_SOURCE_PENDING`
**G3 physical validation:** `NOT_RUN`
**G4 manufacturing release:** `NOT_AUTHORIZED`

## Baseline status
The scope is **project redefinition only**. No imported DXF is approved, generated or modified in this task. V7.2 and V7.6 historical reports are evidence to reconcile, NOT newly repeated tests.

## Planned part tasks
| Issue key | Scope | Dependency | Gate |
|---|---|---|---|
| ETG-000 | G0 parameters, parts, interfaces, legacy provenance | #18 | G0 |
| ETG-001 | Front/rear/ends/bottom — parametric source | G0 | G1 |
| ETG-002 | Four laminated corners and keyed slices | G0 + 001 interfaces | G1 |
| ETG-003 | FCIPH ear, lid end, pin, anchor, movement/installation | G0 + 002 | G1/G2a |
| ETG-004 | Lid skin, frame, engraving safe zones | G0 + 003 | G1 |
| ETG-005 | Removable cradle and lining, subject to product decision | G0 + 001 | G1 |
| ETG-006 | Full model, order, hinge opening, collision and BOM | 001..005 as selected | G2b |
| ETG-007 | Measured coupons, real plywood/kerf/relief, prototype | 006 + qualified operator | G3 |
| ETG-008 | Production nesting, assembly instructions, frozen files | 007 and lead authorization | G4 |

See `specifications/ETG-000/OPEN_ISSUES.csv` for blockers. Lead approval and ≥90/100 independent QA are needed for scoped G0/G1 PR merge; no production implication.
