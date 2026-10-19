# CTB-003 validation / DESIGN_ONLY

Base ecee5f0633a6d7c122087ba75c92eddad4cb0932. Full commands in P03/tests/README.md.
Python3.12; pinned P03 requirements inherit proven P02/P01 dependencies including
Manifold3D3.3.2, Trimesh4.11.2, Shapely2.1.2, SciPy1.17.1. No service required.

## Executions and actual outcomes

| Run | Cases | Pass | Fail | Evidence |
|---|---:|---:|---:|---|
| Initial P03 suite |51|51|0|CTB-003-tests-cycle1.log|
| Clean venv regeneration/retest |51|51|0|CTB-003-clean-tests.log|
| Final material-section drawing repair retest |51|51|0|CTB-003-tests-final.log|
| Unchanged P02 regression |52|52|0|CTB-003-P02-regression.log|
| Unchanged P01 regression |61|61|0|CTB-003-P01-regression.log|
| CTB000 contract |25|25|0|CTB-003-contract.log|
| Baseline integrity |15|15|0|CTB-003-import.log|

Final suites **204 cases,204 PASS,0 FAIL,0 skipped**. Nested solid intersections do not
inflate the case count. Clean generation is required to exit0 before tests (`set -euo
pipefail`), and its log is CTB-003-clean-generation.log. This is current-instance and
isolated-venv evidence, not validation in a restored/new cloud task. Separate QA evidence
and execution logs are appended after its final run; no human G1 approval is implied.

## Path outcomes, failures and repairs

- Geometry/preflight and initial executable suite had0 critical CAD defects/failed cases.
  Source generation logs cycle1/cycle2 preserve expansion from final/path metrics to
  explicit simultaneous-Y insertion trials and an improved stage visualization.
- **Attempted prebuilt approaches are not all feasible:** of9 module approach trials
  (3 concepts×3 axes),8 BLOCKED,1 C-radial PASS. Each has126 continuous checks. A/B closed
  side-hole material obstructs entry despite final fit. These failures are retained,
  not disabled; tests pass by checking the expected obstruction with nonzero volume.
- All6 simultaneous-central-Y trials (3 concepts×vertical/global-X) BLOCKED,18 checks
  each. They are explicit translational obstructions, not claims about every possible
  rotation. Full trial matrices and worst witnesses are preserved in assembly-proofs.
- All3 Y-first routes PASS nominal geometry:18 moving stages/171 swept pair checks each,
  plus171 final body pairs each. These are19-piece local-base checks, not G2 whole product.
- Visual QA found the initial sequence PNG was only a text list, not a motion diagram.
  Replaced it with18 actual projected part start/end frames and directional arrows,
  split across3 rotated legs; JSON3D proof remains authoritative for collisions.
- Visual QA found long C title clipped/approached the panel title. Wrapped title into
  two lines/reduced font; clean generation includes the corrected layout. No model
  contour/dimension changed in these presentation repairs.
- Independent GLB comparison initially used absolute0.06 mm³ allowance; actual P03
  float32 roundoff produced0.090809 mm³ /2.96e-6 relative volume deviation. Reviewer
  corrected that review-only assertion to5e-6 relative after verifying all3D coordinates
  and mesh quantization. No implementation geometry change and no physical precision
  claim. Primary GLB test already uses appropriate1e-5 relative tolerance.

- Primary image review additionally found a dashed full-width Y Z-band could be read
  as actual material across the cheek. Replaced it with the TRUE Y footprint intersection
  at localt10.5, extruded407..413 in the detail view: only the tab sections are filled.
  Regenerated all3 layouts in the clean venv (CTB-003-layout-section-repair.log), then
  reran51/51 tests. No contour/solid/path or source selection was changed.

Two presentation repair batches; three primary51-case suite executions (initial, clean,
final drawing retest). No repair to approved or provisional model dimensions
was required after geometry tests. C was deliberately differentiated during initial
modelling (tip82/tabs54..70), not falsely presented as identical P03 with a new label.
A/B/C blocked path statuses and C CR hold are engineering limits, not repaired away.

Six primary negative controls detect zero thickness, restored94 oversize, lost arm web,
wrong Y-hole position, wrong cheek insertion direction and6.8 mm Y stock. They are
intentionally invalid test inputs; catching them passes the tests. Actual measurements
are never inferred; nominal rigid clearances are not physical fit. Independent QA also
uses exported-SVG wrong-hole/thick-stock/lost-neck examples with explicit positive
interference or disconnected material to prevent a trivial always-clear checker.

## Scope of validation

Tests independently parse actualDXF/SVG paths/units/closure and actual PNG pixel/scale,
verify source regeneration and all3 arms,6 identical rotated candidate cheek patterns,
19 correct parts, GLB watertight positive volumes and absoluteZ. Check Y residual-neck
geometry, cheek lands, old B mortises, ring/foot/tongue preservation, local and circular
radial envelopes, slot/S4 distance and dimensional reservations. Every original upstream
file is compared against Git pre-task commit as well as SHA256 inventory.

CSG runs on real material solids, including holes. Continuous translational sweeps are
segment Minkowski sums, not sparse frames. Numeric1e-6 mm³ applies to flattened ideal
geometry (P01 chord≤0.02; P03 arc≤0.005), not material/process accuracy. Global radius
and local-r are distinct. C's edge-open mouth has0 land;19.8 outer bridge is separately
reported and requires reviewed exterior change under CTB003-CR-002.

No machine/kerf coupon, bending, adhesive, force/friction/deformation, physical load,
strength/stability or safe cutting test executed. No complete tabletop/disc/ring/top
retention integration. These remain unrun/unverified, not skipped/PASS mechanical tests.

## Delivered inventory

- P03/src: model/generator, controlling JSON/schema, pinned inherited requirements,
  upstream SHA256/frozen source reference.
- Each3 variants: P03 and P01-Y-mortise-study-v1 DXF/SVG/PNG/dimensions, layoutPNG/SVG,
  layout provenance and full mechanical/path JSON.
- Assembly:19-part GLB, full3-leg assembled/exploded image,18-stage motion image,
  per-concept final/swept/blocked matrices and assembly instructions.
- Tests/core runner, portable independent OCC scripts/evidence when preserved; README,
  proposed19-part BOM, shortening and separate unapproved cheek change proposals.
- CTB003 comparison/interface/validation/independent QA reports and actual logs/results.
- Updated project STATUS. All CTB000, P01 and P02 source/outputs remain byte-preserved.

No merged PR, approved candidate/production release or cut-ready data is claimed.

Preserved independent OCC/export/negative/central-Y JSON results describe nested checks
separately from204 unique suite cases. Optional direct vertex audit compares7602 GLB
vertices against extruded SVG/JSON transforms with float32-scale rounding, not physical
measurement. Final whitespace and protected-source diff checks must be clean before PR.

Reusable cloud draft install_script/start_skill now record pinned P03 installation and
the204-case workflow. Draft save does not apply/publish it. Review/save/publish in
environment settings to activate future tasks; new-task restoration is untested.

Independent reviewer also repaired a combined-script wrapper name collision (dictionary
shadowing a helper), then completed the portable export-only OCC script with exit0.
This reviewer-harness packaging failure did not change implementation artifacts or
collision criteria. Full details are in CTB-003-INDEPENDENT-QA.md. The primary agent
executed the preserved portable file from its repository path successfully; output is
CTB-003-independent-OCC-reproduction.log. Final independent51-case log was recopied
only after its execution completed; all5 JSON evidence files parse and are preserved.
