## Reusable product engineering procedure (for all projects)

- When planning a **new ASSEMBL LAB physical product**, use [Engineering Playbook](engineering-process/PLAYBOOK_HE.md), [approval gates](engineering-process/GATES.md), and [QA policy](engineering-process/QUALITY_STANDARD.md). Begin with a new project-local BRIEF and G0 interface contract.
- Codex reusable skill: `.agents/skills/assembl-lab-product-engineering/SKILL.md`; read/apply it for new-product, CAD/joinery, interfaces, QA and manufacturing-release tasks.
- Every product's machine-bed dimensions, materials, loads and geometry **must be newly specified and checked**. Do not transplant CTB-01 values into a new project.
- Each task: Issue → isolated branch → reproducible source and evidence → independent QA → PR → engineering lead review → approved merge or changes requested. Codex does not self-merge.
- Engineering lead may autonomously approve routine well-scoped design studies under delegated authority if QA ≥90/100 and zero **critical** blockers for that claimed scope; escalate consequential product/safety choices.
- Design-stage CAD can merge as `DESIGN_ONLY`; G3 measured physical fit, structural/stability assessment and G4 production authorization are independent gates, not inferred from CAD PASS.
- Use templates under `engineering-process/TEMPLATES/`; record versions and unknowns. If independent QA is unavailable, mark `INDEPENDENT_QA_PENDING`.

---

# Engineering workflow

- Work in the existing isolated checkout; do not create worktrees unless requested.
- Use one dedicated branch and PR per task. Never merge automatically. Engineering lead reviews and may approve routine scoped design decisions under delegated authority; product owner approves consequential aesthetic, functional and safety-related decisions.
- Sequence: interface baseline → individual component design → component approval (G1) → integration (G2) → independent CAD/manufacturing QA → supervised physical validation (G3) → product/manufacturing approval (G4).
- Approved `frozen` parameters are immutable without an approved Change Request using the imported template. Document and propagate provisional interface changes before integration. Never infer approved dimensions from images.
- Keep geometry and DXF/SVG/PNG exports DESIGN_ONLY until the relevant approvals and physical validation. Static checks, CAD fit, physical fit, bending, strength and stability are distinct evidence; never claim unperformed tests.
## CTB-01-specific constraints (apply only to CTB-01)

- Read `projects/CTB-01/specifications/CTB-000/` before CTB-01 work: SPEC_HE.md, DECISIONS.md, parameters, interfaces, parts, open issues and handoff. JSON parameters/interfaces are authoritative. List relevant IF IDs and dependencies before implementing a component. An OPEN dependency blocks the **specific design claim that depends on it**, not an unrelated bounded DESIGN_ONLY study; retain the blocker until proven resolved.
- CTB-01: Ø350 mm top, overall height 500 mm, top thickness 50 mm; three legs at 0°/120°/240°, each with two identical parallel 6 mm birch cheeks, 15 mm inner gap and four spacers. CSH-3Y hub, CSH-3P anchor disks, VTP-R KERF-4 FLEX 4 mm birch rim.
- Cutting sheet is portrait: HEIGHT 800 × WIDTH 440 mm. Sheet X=0..440, Y=0..800. `stock_sheet_mm` is [height,width], not [width,height]. No actual nesting is approved by this baseline.
- Preserve global right-handed XYZ and local (r,t,z); lengths are mm. Separate frozen, derived and provisional data.
- Quarantine legacy V-shaped LEG_A/LEG_B and tilted/multilayer CSH CAD as superseded reference only. Never put it into active component, assembly or manufacturing sources. No legacy CAD is imported by CTB-000.
- Preserve IF-01..IF-14 and B01..B13 until formally resolved with evidence. Upper locking, assembly order and final leg geometry remain blockers.
- Historically, CTB-000 import alone did not authorize CTB-001; it was later separately authorized and merged. Every future component needs its own scoped, authorized task.

## Validation

From repository root:

```sh
python projects/CTB-01/specifications/CTB-000/validate_contract.py
python tools/check_ctb_baseline.py
```

The first command is the unchanged source validator (25 static data checks). The second checks inventory/integrity, schema, cross-file references and baseline consistency. Install `jsonschema==4.26.0` if unavailable. Neither command validates physical geometry or manufacturing readiness.
