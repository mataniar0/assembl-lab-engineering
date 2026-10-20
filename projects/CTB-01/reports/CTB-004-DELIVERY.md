# CTB-004 delivery — Issue #9

2026-10-20. Branch `codex/ctb-004-anchor-disks`; base `f49e3b3be73b7d474302823cc9072148319c8f67`.
PR for review: https://github.com/mataniar0/assembl-lab-engineering/pull/12

Status **DESIGN_ONLY / PENDING_LEAD_SELECTION**. Three alternatives delivered; recommend
A_RIM_OPEN without center opening for review only. No merge or physical-cut authorization.

- [Design comparison and dimensions](CTB-004-DESIGN-REVIEW.md)
- [Interfaces and open dependencies](CTB-004-INTERFACE-MATRIX.md)
- [Tests, all failures and repairs](CTB-004-VALIDATION.md)
- [Independent alternate-kernel QA](CTB-004-INDEPENDENT-QA.md)
- [Exact CTB-005 counterpart contract](../parts/P04/CTB-005-HANDOFF.md)
- [File inventory](CTB-004-FILES.tsv)

## Delivered files

`parts/P04/src/`: versioned input/schema, actual material model and reproducible exporter,
core/optional QA requirements,174-file protected SHA inventory.
`parts/P04/tests/`:71-case runner, fail-fast full reproduction runner, independent OCC audit
and instructions. `BOM-v1.csv`: exactly one P04L and one P04U, no hidden hardware.

For each `variants/A`, `B`, `C`: P04L/P04U dimensioned DXF, SVG, PNG and dimension JSON;
physical XY and vertical sections; actual/exploded21-body render; close core/layer/witness
reservation render; real21-node GLB and mesh-volume evidence; connection/path/negative
control data; finite matching witness DXF/SVG/PNG/JSON and recommendation README.

`assembly/`: exact six-tongue extraction, comparison, continuous sweeps and assembly order.
`reports/CTB-004-*`: comparison, interface matrix, validation/failures, independent QA,
complete file inventory and preserved initial/final/independent logs. `STATUS.md` updated.
The inventory lists every changed path; Python caches are excluded.

## Executed checks and fixes

**275/275 unique automated checks passed**, independently rerun by a second agent:
P04 71 +P03 51 +P02 52 +P01 61 +contract25 +import15. Clean isolated generation and `pip check`
passed. No final unexplained failures/skips. Ten DXF/SVG cut-file pairs (disks and all
counterpart witnesses) were additionally read and matched, with closed loops and mm units.
All174 protected upstream files remain byte-identical.

Per variant:21 real bodies,210 final pairs; non-BOM six matching witnesses141 pairs;
continuous prospective skin/L/U60 checks and conditional web route168 checks all pass.
Independent OpenCASCADE reconstructs exports and validates GLB21nodes/units/volume.
Nested comparisons and repeated independent executions are not added to275unique cases.

Initial primary71-case run had22 failures (6 export-rounding comparisons,6 NO_HOLE area
residues,6 faint PNGs,4 missing nominal-diameter annotations). All corrected and rerun;
no approved dimension changed. A misleading bottom-skin hatching overlay was separately
fixed. Independent harness initially assumed sharp tongue noses, then corrected to the
actual R1 geometry; its runtime dependency selection and repair are disclosed in QA.
Explicit bad geometry/reverse-order controls remain intentionally blocked, not hidden failures.

## Open engineering decisions

Lead selection of A/B/C and B13 center aperture is pending. Lower/upper disks remain
Ø190×6 at456..462/480..486; **freegap18**, pitch24, total tabletop envelope50. Actual tongues
end488, giving only2mm projection above upper disk. Sliding slots are not a positive lock.
B01/IF-12 CTB-008 retention, B06 final P05 joints/strength, IF-08 disk/core load path,
actual P07 skin/rim access, B02 full order, B10 stock/kerf and B11 load/stability remain open.
No full tabletop, tested adhesive, physical fit, fixtures, nesting or safe load is claimed.

## Development environment

Used the cloud-environment-onboarding:setup workflow. Current instance: clean pinned P04
venv verified. Reusable `install_script` and `start_skill` were saved as an environment
draft, retaining network/secrets/repository configuration. Draft saving does not publish
or apply it. Review/save the draft in environment settings and publish the environment
if this prepared configuration should be used for future tasks; no fresh-task restoration
claim is made. Existing optional CQ runtime supplied independent QA.

## Acceptance and updated process compatibility

Implementation agent `/root`; independent reviewer `/root/ctb004_qa`. Reviewed geometry
head `58bccbb3b3c7a6bb95563b1f837ef065e6645c4d`; later commits edit delivery/process notes only.
Scope: G1 candidate design with bounded G2a nominal assembly evidence; lead gate decision
pending, **G3 NOT_RUN / G4 NOT_AUTHORIZED**.

During submission, main advanced to `441d18b8fc9c2ad1a169fffc5556c12b5d2ce519` (ENG-001 PR #11),
adding the reusable engineering playbook/skill and QA scoring policy. Its diff changes no
CTB-000/P01/P02/P03 geometry. Read/applied that skill, playbook, gates, QA/delivery templates
and PR checklist to this existing product study. The independent reviewer assigns **96/100**, with zero in-scope critical/major findings
and one optional caption-readability item, in CTB-004-INDEPENDENT-QA.md. This does not
select a concept or authorize merge.
No rebase, merging into main or alteration of protected source was required for this
compatible documentation-only target-branch advance. Reported275 tests are the actual
component/baseline suites, not an unrun playbook suite counted as evidence.

| Requirement | Result | Evidence |
|---|---|---|
| Three meaningful alternatives, both disks distinct, six tongues/six web interfaces each | PASS_CAD_CANDIDATE | variants/A,B,C; design review and exact loops |
| Fixed layers, full6mm tongue engagement,18mm freegap,50mm external budget | PASS_CAD_DIMENSIONS | six-tongues.json; dimension JSONs;71 tests |
| Feasible21-body lowering and matching38mm web reservations | PASS_CAD_LOCAL_CONDITIONAL | proofs.json; independent OCC evidence |
| All prior sources preserved; correct single-part sheet margins and BOM | PASS |174 SHA checks; BOM-v1.csv;275suite logs |
| QA independent, failures/repairs disclosed, reproducible source and exports | PASS_DESIGN_STUDY | QA report/score, validation and raw logs |
| Lead selection/center opening decision | PENDING_REVIEW | P04/DECISIONS.md; no concept selected here |
| Positive lock, complete load path and whole-table integration | BLOCKED_LATER_SCOPE | IF-08/12, B01/B02/B06 and handoff |
| Real material/kerf/adhesive/load/physical tests | NOT_RUN | G3; stock and kerf null |
| Actual nesting/cutting/manufacturing release | NOT_AUTHORIZED | G4; user instruction and review gate |
