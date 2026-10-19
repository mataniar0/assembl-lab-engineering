---
name: assembl-lab-product-engineering
description: >-
  Reusable engineering workflow for ASSEMBL LAB parametric plywood and laser-cut products.
  Use when starting a new ASSEMBL LAB physical product, creating its G0 interface contract,
  designing parts or joinery, generating DXF/SVG and assembly previews, reviewing engineering
  PRs, running independent CAD QA, or preparing measured physical/manufacturing releases.
---

# ASSEMBL LAB Product Engineering

## Activation / when to use
Use this skill for engineering work for **any new or existing ASSEMBL LAB physical product** managed in this repository. Do not activate for unrelated website code or marketing copy, except a manufacturing-approved image/content handoff.

Always start by reading:
1. `AGENTS.md` at repository root.
2. [Engineering playbook](../../../engineering-process/PLAYBOOK_HE.md).
3. [Release gates](../../../engineering-process/GATES.md).
4. [QA policy](../../../engineering-process/QUALITY_STANDARD.md).
5. Project-local `BRIEF.md`, `STATUS.md`, G0 contract, `DECISIONS.md` and the relevant existing CAD sources (when those files exist).

If the project is new, create its own directory and use [product brief](../../../engineering-process/TEMPLATES/NEW_PRODUCT_BRIEF_HE.md) followed by [interface-control baseline](../../../engineering-process/TEMPLATES/INTERFACE_CONTRACT.md). **Never inherit CTB-01 stock size, material, measurements or design choices into a new project.** Ask or mark UNKNOWN/OPEN.

## Decision flow
- **No G0?** Create initial product brief/BOM/interfaces, status register and parameter provenance, and run source-consistency QA before downstream parts.
- **G0 available, single part needed?** Read relevant frozen/provisional inputs and IF IDs; use [component task template](../../../engineering-process/TEMPLATES/COMPONENT_TASK.md), develop meaningful alternatives where relevant, make parametric source and 1:1 exports, local checks, and independent reviewer handoff.
- **Assembled submodules available?** Use real solids and a documented full insertion path; distinguish final placement from feasible insertion. Validate parts counts/BOM, keep blocked trials.
- **Full geometry available?** Complete cross-part integration, model load path hypotheses, run independent CAD QA; do not claim unperformed structural tests.
- **Physical sample available?** Attach real thickness/kerf and physical test records. If absent, mark G3 NOT_RUN.
- **Manufacturing requested?** Require evidence for G3 and G4; absent evidence => only DESIGN_ONLY and clear blockers, no production authorization.

## Coding and deliverables
1. Declare units, coordinate frames, per-project sheet **height and width**, and source-of-truth hash/version.
2. List impacted IF IDs and frozen/provisional values BEFORE editing geometry. Avoid unapproved edits to previous parts; use versioned studies or [Change Request](../../../engineering-process/TEMPLATES/CHANGE_REQUEST.md).
3. Parameterize cut geometry; generate CAD/DXF/SVG and renders from the **same source**, not from visual imitation.
4. Validate contour validity, sheet *single-part* fit, BOM, rigid-solid collision and insertion (when claimed); add negative controls and regressions. Distinguish code PASS from verified material strength.
5. Track observed failures and fixes. Missing or blocked data is not a pass.
6. Request a genuinely **independent QA review** and use [QA report template](../../../engineering-process/TEMPLATES/QA_REPORT.md).
7. Produce [delivery report](../../../engineering-process/TEMPLATES/DELIVERY_REPORT.md), update [status](../../../engineering-process/TEMPLATES/PRODUCT_STATUS.md) and [decision log](../../../engineering-process/TEMPLATES/DECISION_LOG.md).
8. Open a scoped PR (see root PR template) and await engineering-lead review. **Never merge your own PR** or claim real-world release based on CAD.
9. Lead may advance routine documented stages with ≥90/100 QA and no in-scope critical blocker. Escalate consequential design/safety choices to product owner or qualified assessor.

## Always report
Stage and release boundary; approved versus provisional values; exact test commands and counts; initial/final failures, corrections and retests; independent QA identity and method; unknown geometry/physical fit/strength/kerf/stability; pending interface IDs, exact PR and files.

**Do not claim:** a rendering proves part mating, "0 CAD collision" proves mechanical load capacity, a 6mm nominal slot implies actual plywood fit, a passing design-review score is a physical approval, or a DXF file is ready to cut merely because it exists.

Reference documentation is stored under `engineering-process/`; this Skill is a process router, not a replacement for project-local technical definitions.
