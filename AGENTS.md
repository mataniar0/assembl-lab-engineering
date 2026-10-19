# Engineering workflow

- Work in the existing isolated checkout; do not create worktrees unless requested.
- Use one dedicated branch and PR per task. Never merge automatically. Project manager reviews; product owner approves design decisions.
- Sequence: interface baseline → individual component design → component approval (G1) → integration (G2) → independent CAD/manufacturing QA → supervised physical validation (G3) → product/manufacturing approval (G4).
- Read `projects/CTB-01/specifications/CTB-000/` before CTB-01 work: SPEC_HE.md, DECISIONS.md, parameters, interfaces, parts, open issues and handoff. JSON parameters/interfaces are authoritative. List relevant IF IDs and dependencies before implementing a component; an OPEN dependency blocks dependent design.
- Approved `frozen` parameters are immutable without an approved Change Request using the imported template. Document and propagate provisional interface changes before integration. Never infer approved dimensions from images.
- Keep geometry and DXF/SVG/PNG exports DESIGN_ONLY until the relevant approvals and physical validation. Static checks, CAD fit, physical fit, bending, strength and stability are distinct evidence; never claim unperformed tests.
- CTB-01: Ø350 mm top, overall height 500 mm, top thickness 50 mm; three legs at 0°/120°/240°, each with two identical parallel 6 mm birch cheeks, 15 mm inner gap and four spacers. CSH-3Y hub, CSH-3P anchor disks, VTP-R KERF-4 FLEX 4 mm birch rim.
- Cutting sheet is portrait: HEIGHT 800 × WIDTH 440 mm. Sheet X=0..440, Y=0..800. `stock_sheet_mm` is [height,width], not [width,height]. No actual nesting is approved by this baseline.
- Preserve global right-handed XYZ and local (r,t,z); lengths are mm. Separate frozen, derived and provisional data.
- Quarantine legacy V-shaped LEG_A/LEG_B and tilted/multilayer CSH CAD as superseded reference only. Never put it into active component, assembly or manufacturing sources. No legacy CAD is imported by CTB-000.
- Preserve IF-01..IF-14 and B01..B13 until formally resolved with evidence. Upper locking, assembly order and final leg geometry remain blockers.
- CTB-000 import does not authorize starting CTB-001. Subsequent components need a separately authorized task.

## Validation

From repository root:

```sh
python projects/CTB-01/specifications/CTB-000/validate_contract.py
python tools/check_ctb_baseline.py
```

The first command is the unchanged source validator (25 static data checks). The second checks inventory/integrity, schema, cross-file references and baseline consistency. Install `jsonschema==4.26.0` if unavailable. Neither command validates physical geometry or manufacturing readiness.
