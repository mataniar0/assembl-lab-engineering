# ETG-01 — מצב פרויקט

**Overall:** `G0_DRAFT` / **Production:** `DESIGN_ONLY`
**Tracked issue:** https://github.com/mataniar0/assembl-lab-engineering/issues/18
**Independent QA:** `INDEPENDENT_QA_PENDING`
**Native geometry:** `LEGACY_SOURCE_PENDING`; ETG-specific H1 CAD does not yet exist
**G3 physical validation:** `NOT_RUN`
**G4 manufacturing release:** `NOT_AUTHORIZED`

**Hinge:** `H1_OWNER_SELECTED / GEOMETRY_OPEN`, replaces FCIPH. Owner-approved architecture, NOT H1 3D or manufacturing validation.

## Baseline status
The scope is **project redefinition only**. No imported DXF is approved, generated or modified in this task. V7.2 and V7.6 historical reports are evidence to reconcile, NOT newly repeated tests.

## H1 Phase A (ETG-003) — ChatGPT feasibility screening complete, 2026-10-21
- Design note: `design/ETG-003_H1_PHASE_A_FEASIBILITY_HE.md` on this draft branch.
- One selected research hypothesis: `H1-ETG-C1` recessed layered fork (rear fixed P06 support / P09+P10 rotating cheeks / P11 pin / P12 flush cap); **candidate only**, not a selected CAD design.
- Analytical bounds only: nominal 248×148mm optimistic XY cavity under planar 6mm walls, nominal 48mm total spare per axis for 200×100 reference fruit, surrogate 160mm ray adds 25.28mm rear projection at 120° relative to 110°, fork-bearing sandwich 3×6 = 18mm *before* any gap or cap. MEB's example 12mm pin is inadequate for this candidate.
- **Codex B1 microtask created:** [ETG-003 B1 Issue #37](https://github.com/mataniar0/assembl-lab-engineering/issues/37). Codex has NOT run; scoped to one nominal captured-pivot/fork local 3D proxy with GO/REVISE/NO-GO.
- **Current execution boundary:** ChatGPT Phase A complete; one focused Codex B1 3D local retaining-cap/axial-stack and finite insertion test is needed for actual geometric evidence. Missing source from V7.6 means local surrogate evidence would be `PROXY_DESIGN_STUDY_ONLY`; actual ETG hinge/lid fitting remains `NOT_RUN`. Stop after B1; B2 not authorized.
- `G0_INDEPENDENT_QA_PENDING`; no current production DXF, G3 and G4 NOT_RUN.

## Planned part tasks
| Issue key | Scope | Dependency | Gate |
|---|---|---|---|
| ETG-000 | G0 parameters, parts, interfaces, legacy provenance | #18 | G0 |
| ETG-001 | Front/rear/ends/bottom — parametric source | G0 | G1 |
| ETG-002 | Four laminated corners and keyed slices | G0 + 001 interfaces | G1 |
| ETG-003 | H1 recessed body support, rotating lid cheeks, wooden pins, flush caps, 0–120° sweep and capture | G0 + 002 | G1/G2a |
| ETG-004 | Lid skin, frame, engraving safe zones | G0 + 003 | G1 |
| ETG-005 | Removable cradle and lining, subject to product decision | G0 + 001 | G1 |
| ETG-006 | Full model, order, hinge opening, collision and BOM | 001..005 as selected | G2b |
| ETG-007 | Measured coupons, real plywood/kerf/relief, prototype | 006 + qualified operator | G3 |
| ETG-008 | Production nesting, assembly instructions, frozen files | 007 and lead authorization | G4 |

H1 change record: `specifications/ETG-000/ETG-CR-001-H1.md`; old FCIPH audit does not substantiate the new hinge. 

See `specifications/ETG-000/OPEN_ISSUES.csv` for blockers. Lead approval and ≥90/100 independent QA are needed for scoped G0/G1 PR merge; no production implication.
