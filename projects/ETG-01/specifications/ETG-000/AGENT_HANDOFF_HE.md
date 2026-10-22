# ETG-000 — LEAN v1.1 H1 design handoff

**Issue:** #18 · **PR:** #19 (DRAFT) · **Priority:** P1 · **Executor now:** ChatGPT · **Codex now:** NOT_NEEDED · **QA:** INDEPENDENT_QA_PENDING · **Gate:** G0_DRAFT/DESIGN_ONLY.

## Product-owner decision
ETG-CR-001 / D09 selects **H1 integrated recessed wooden pivot** to replace FCIPH. Keep ETG body260×160×150mm, structural birch6mm nominal, portrait H800×W440 sheet and ETG lid 0–120°. Do **not** copy MEB H1 research dimensions/110deg or MEB 310mm cavity. Old FCIPH reports/108 PASS are reference evidence for legacy body/corners **only**; no H1 validation.

## ChatGPT Phase A
1. Read current main LEAN/AGENTS/PLAYBOOK/GATES/QUALITY_STANDARD, and ETG BRIEF, STATUS, DECISIONS, params, PARTS, IF, blocker, CR and legacy registers.
2. Map the owner H1 A/B/C/D groups: P06 rear laminated body supports; P09/P10 moving lid cheeks; P11 two wooden pins; P12 two recessed low-profile retaining caps. Nominal 13 families, 28 IFs, 12 tracked blockers — these are G0 bookkeeping, not CAD passes.
3. Seek missing original V7.6 parametric + DXF sources if accessible, so existing panels/corners can be reused; avoid reconstructing discarded FCIPH hinge. If missing, mark LEGACY_SOURCE_PENDING and propose a minimal **authorized** parametric rear-corner rebuild, not full historical CAD recreation.
4. Screen H1 clearance/cavity and body/sheet envelope; identify one specific uncertainty remaining for 3D CAD. Coaxiality across both ends, positive pin capture/cap seating, cap insertion and reversibility, 0–120° sweep, rear P06 support integrity and cavity/tip/skin keep-out all remain OPEN. No virtual pass without real solids.
5. Preserve final source-of-truth versions, negative controls, actual test counts/failure logs and approved vs provisional geometry.

## Conditional Codex B1 — only after source or scoped rebuild authority
One ETG-specific H1 support/cheek/pin/cap **feasibility** study. Use nominal 6mm flat-layered rear corner and lid cheek model; simulate both pivot axes, lid 0–120° continuous motion, interference and pin/cap installation/escape, with negative missing-cap and misaligned-bore tests. Return one GO/REVISE/NO-GO, minimal section/coordinates and actual log counts, stop before B2. Do not output full production DXF or nesting.

## B2, QA and stop
B2 only after B1 review and approved interface changes. Require real independent document and geometry QA >=90/100 and zero in-scope critical blocker; no self-approval or automatic merge. Stop on frozen body/stock/material or functional tradeoff requiring owner. Physical fit, kerf, loading, wear and cap retention G3 NOT_RUN; G4 production NOT_AUTHORIZED.

**Next step:** G0 H1 baseline verification and source lookup in ChatGPT, separate QA of updated PR #19; afterwards authorize *one* B1 if needed.
