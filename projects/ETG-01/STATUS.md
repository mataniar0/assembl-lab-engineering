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

## ETG-001R C5 / ETG-004 C6 — 2026-10-22 (ChatGPT)
- **C5 conditional local:** P01 front/mortises and P05 base were reconstructed with J-tongued P03/P04. 20/20 focused assertion checks PASS, 171 parent-pair static booleans clear, 17 front insertion samples; front P01 still withdraws -Y and bottom P05 -Z, so the sidewall/hinge keeper is **NOT positively captive as a whole-body assembly**.
- **C6 flat lid NO-GO:** 53/61 angular proxy samples collide with P02 rear; first at 14°, at 120° large clash. 32mm-rear-gap shortening is a bad/unapproved counterfactual, not a design fix. Analytic raised/rear-biased H1 axis Y158/Z146 avoided P02-only intersection across 481 planar samples but would require modified rear/corner extension to approx Y174/Z162, a substantive appearance/interface proposal **NOT APPROVED**; real H1 and entire lid model NOT_RUN.
- Detailed report in child **Draft PR #71**: `design/ETG-001R_C5_ETG-004_C6_HINGE_BODY_REVIEW.md`. Actual CAD Python, STEP, JSON and section are in conversation ZIP `ETG001R_C5_C6_DESIGN_ONLY.zip`, SHA256 `40a564fc2df26c431326a96fed912fd28ba7a7555bdf4f38a809c93b6d1ceb17`, **not committed to GitHub**.
- P1 blockers: body P01/P05 closure issue #73 and owner-consistent H1 lid movement issue #74. **Not yet a Codex tools gap**. G0 QA still independent-pending; G1/G2 not approved; G3 physical and G4 manufacturing NOT_RUN.

## H1 Phase A (ETG-003) — ChatGPT feasibility screening complete, 2026-10-21
- Design note: `design/ETG-003_H1_PHASE_A_FEASIBILITY_HE.md` on this draft branch.
- One selected research hypothesis: `H1-ETG-C1` recessed layered fork (rear fixed P06 support / P09+P10 rotating cheeks / P11 pin / P12 flush cap); **candidate only**, not a selected CAD design.
- Analytical bounds only: nominal 248×148mm optimistic XY cavity under planar 6mm walls, nominal 48mm total spare per axis for 200×100 reference fruit, surrogate 160mm ray adds 25.28mm rear projection at 120° relative to 110°, fork-bearing sandwich 3×6 = 18mm *before* any gap or cap. MEB's example 12mm pin is inadequate for this candidate.
- **B1 run completed in ChatGPT (2026-10-22):** local OpenCascade 7-solid proxy, result **REVISE**; 21/21 static pairs, 100/100 split-leaf insertion poses, 121/121 local 0..120° angle samples non-overlapping. **Not a complete product motion proof.** P12 cap freely extracts and P06 split leaves can reverse out; mechanical positive retention remains UNSOLVED. Full CAD and STEP/GLB and tests delivered in user-chat ZIP `ETG003_B1_H1_PROXY_DESIGN_ONLY.zip`, SHA256 `90bdc855040c4b52d6882a4dafbdb902aeeb18ec39d35d1abe70a12095a58260`, not committed binary to GitHub. **B2 remains NOT AUTHORIZED.** Issue #37 contains results.
- **Codex B1 microtask created:** [ETG-003 B1 Issue #37](https://github.com/mataniar0/assembl-lab-engineering/issues/37). Codex was NOT used; ChatGPT performed a local proxy B1 and returned REVISE.
- **Current execution boundary:** ChatGPT Phase A complete; ChatGPT executed the bounded B1 proxy; P06/P12 mechanical securement requires revision and fresh tests before any later B2 or product-wide model. Missing source from V7.6 means local surrogate evidence would be `PROXY_DESIGN_STUDY_ONLY`; actual ETG hinge/lid fitting remains `NOT_RUN`. Stop after B1; B2 not authorized.
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
