# [PRODUCT-ID]-[TASK] — [Component] (DESIGN_ONLY)

**Issue:** [link] · **Branch:** [branch] · **Source SHA / contract version:** [ ]  
**Component ID / quantity / units / material:** [ ]  
**Scope:** single component [ ] / local subassembly [ ] / other [ ]
**Responsible:** implementation agent [ ] · independent QA [ ]

## Requirements & boundaries
- **Goal:** [...]
- Frozen constraints (with file links): [...]
- Derived parameters: [...]
- Provisional values and unresolved external decisions: [...]
- Required interface IDs: [...]
- Related Part IDs and dependent tasks: [...]
- Explicit OUT-OF-SCOPE items: [...]

## Work
1. Read `AGENTS.md`, `engineering-process/PLAYBOOK_HE.md`, applicable G0 and current product decisions.
2. Analyze at least [N] genuinely different feasible/blocked design concepts when alternatives matter; never conceal a blocked concept.
3. Generate reproducible parametric model and 1:1 files; include per-part dimension data and BOM.
4. Model actual joint cut geometry, final contact and collision-free **insertion sequence**, if this issue claims assembly evidence.
5. Run geometric and source integrity tests, negative controls, regressions and per-project sheet-fit screen.
6. Commission **independent** QA; disclose failures, corrections and retests.
7. Open PR; do not merge.

## Deliverables
- `src/`: [paths]
- `variants/`: [DXF/SVG/PNG/3D]
- `tests/`: [commands and expected output]
- `reports/`: [design-review/interface matrix/QA/delivery]
- `STATUS.md` and `DECISIONS.md` update proposals

## Acceptance criteria (measurable)
- [ ] Source contract and frozen values unchanged or approved CR attached.
- [ ] All output contours/units/BOM verified.
- [ ] Interactions with every declared IF accounted for.
- [ ] Actual insertion/blocked paths correctly reported for claimed assembly scope.
- [ ] No unmeasured material/kerf/load claim presented as PASS.
- [ ] QA independent and reproducible; zero in-scope critical blockers. Later-gate risks remain explicitly OPEN.
- [ ] PR has status and evidence; no production approval.

## Stop conditions
Missing G0 for dependent design, irreconcilable upstream mismatch, a failed assembly path required by the claimed scope, an unmeasured parameter assumed released, or need for unapproved aesthetic/function/structural change ⇒ `BLOCKED` and/or [Change Request](CHANGE_REQUEST.md).

A blocked alternative or later-gate dependency does not block a clearly bounded `DESIGN_ONLY` study that neither depends on it nor claims it resolved; preserve the blocker and evidence under [gate hard-stop rules](../GATES.md). A study may propose a provisional change, but cannot alter frozen inputs before CR approval.
