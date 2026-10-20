# CTB-005 delivery — Issue #13

2026-10-20. Branch `codex/ctb-005-radial-webs`. Approved base:
`6292a0e22c9aacade5aa7c7995332494aa8de005`.
**G1 candidate / bounded G2a CAD evidence — DESIGN_ONLY / AWAITING_LEAD_SELECTION**.
Implementation agent `/root`; independent reviewer `/root/ctb005_qa`.

PR for review: https://github.com/mataniar0/assembl-lab-engineering/pull/14

Audited geometry/evidence committed at `0097e3ff238fe09e67839d83e630d69aef609d50`; subsequent delivery-link edits change documentation only.

- [Three-concept design review](CTB-005-DESIGN-REVIEW.md)
- [Interface evidence and holds](CTB-005-INTERFACE-MATRIX.md)
- [Tests, initial failures and corrections](CTB-005-VALIDATION.md)
- [Independent QA:96/100](CTB-005-INDEPENDENT-QA.md)
- [CTB-007/008 handoff](../parts/P05/CTB-007-008-HANDOFF.md)
- [Complete changed-file inventory](CTB-005-FILES.tsv)

## Delivered geometry and files

Exactly **P05×6** added to the reviewed21 parts makes27 real bodies per assembly scenario.
Each concept uses six identical one-piece6mm ribs at60° axes and38mm height. Tabletop
Ø350×50, H500, disk layers and18mm free gap remain unchanged. All259 CTB-000/P01–P04 files
are byte-preserved; there is no silent adoption of an old alternative or center opening.

| Paths | Contents / scope |
|---|---|
| `parts/P05/src/` | Parametric model, generator, input/schema, requirements and protected-source SHA inventory |
| `parts/P05/variants/A,B,C/` | Actual P05 DXF/SVG/PNG, dimensions, physical sections and connection/path JSON |
| `parts/P05/proposals/B,C/` | Explicit NOT_APPROVED disk-v2 change proposals and companion exports; C keeps original upper |
| `parts/P05/assembly/` | Five27-body GLBs with distinct baseline/proposal/BLOCKED labels, mesh evidence, core/exploded/staged views, continuous proofs, re-executed Y-first path |
| `parts/P05/tests/` |62-case suite, full fail-fast runner, independent OpenCASCADE audit, reproduction instructions |
| `parts/P05/BOM-v1.csv`, `DECISIONS.md`, handoff | Six added ribs only, proposed decisions and future skin/rim/lock contracts |
| `reports/CTB-005-*`, `STATUS.md` | Review/QA/validation/delivery, full inventory, all observed failure/correction evidence and current status |

Skins, kerfed wall, tools and locks remain explicitly non-BOM reservations. Proposed disks
substitute one/two bodies only within their named comparison models; they are not extra
hardware and do not override current selected P04. No physical cutting authorization.

## Acceptance and review decisions

| Criterion | Result | Evidence |
|---|---|---|
| Three real connected rib/joint concepts; six identical instances each | PASS_CAD | Actual cut loops/meshes, all six inverse-rotation checks |
| Original P04 fit and radial insertion | A/C PASS, B BLOCKED | B upper28.8mm³/rib,172.8 total; explicit baseline GLB/proofs |
| Positive outward capture with original open disks | OPEN / NOT_DEMONSTRATED | A/C reverse radial motion remains free; B original start invalid |
| Versioned B/C mechanical alternatives | CONDITIONAL_CAD_PASS / CR_REQUIRED | B two closed disks; C lower closed plus original-upper step; fixed-disk translation barriers |
|27 actual parts and continuous full local route | PASS for named valid scenarios |351 static pairs and207 skin/disk/rib swept comparisons/model; Y-first171 rechecked |
| No approved inputs changed | PASS |259 protected files equal approved commit |
| Reproducible exports and independent QA | PASS |337 unique cases, clean isolated rebuild, alternate kernel,96/100 |
| Single-part stock screening | PASS | H800×W440 with10mm margins; actual nesting NOT_RUN |
| Actual bonding, complete lock/load path, whole product | OPEN/BLOCKED | IF-06/07/08/12 and B01/B02/B06/B10/B11 holds |
| Physical G3 / manufacturing G4 | NOT_RUN / NOT_AUTHORIZED | No measured stock/kerf/glue/loads, no production or cut release |

Recommend **A_RELIEVED_BOND for compatible downstream design**, retaining radial restraint
and skin-bonding strength as OPEN. B is a separate mechanical-capture CR option; C has only
2.4mm² geometric flat-stop area and needs particular stress review. The recommendation
and QA score do not select a concept or approve either CR. Lead review remains pending.

## Executed checks and corrections

**337/337 unique checks passed**:62 P05 +71 P04 +51 P03 +52 P02 +61 P01 +25 contract +15 import.
The separate agent independently repeated all337, including the final62-case cap-metric
update, and reconstructed actual exports in OpenCASCADE. Nested comparisons/reruns are
not added to337. All seven actual/proposal DXF/SVG/PNG cut sets also matched in a retained
whole-export audit. Five GLBs each contain27 real nodes with correct metre scale/volumes.

Initial primary62 tests passed. Clean generation/full337 passed. Final metadata clarification
regenerated and62 affected cases passed. Independent initial readiness attempt had59PASS/
3ERROR because three documents were not written yet; all corrected and logs retained.
Preliminary C escape reasoning failed an actual collision probe and was replaced with an
explicit stepped-capture design. B original interference and free original radial withdrawal
are retained blocked/open findings, not hidden by passing unit assertions.

Two presentation/provenance/metric correction cycles clarified A's curve approximation,
reframed labels, corrected rounded-slot lands and distinguished actual6.6/22.6mm inner-edge
spans from7.6/23.6mm envelope budgets. A reporting probe used system Python without Shapely;
retry with the verified CAD venv succeeded and is disclosed. No cut geometry or approved
source changed to force a passing result. See validation and raw logs for every attempt.

## Runtime and remaining limits

Fresh core venv `/workspace/.venvs/ctb-005` and `pip check` verified. Exact commands and
versions are in tests/README.md and CTB-005-logs/environment.json. Reusable install/start
instructions were saved as an environment configuration draft, preserving other settings.
Saving does not apply or publish it; review/save in environment settings and publish if
this prepared setup should serve future tasks. No fresh-task restoration is claimed.

G1 lead selection and CR approval are pending. Full G2b, physical G3 and production G4
remain blocked/unperformed. Fixed-disk obstruction of named translations is not6DOF
retention, glue strength, stability or a safe load rating. Hands, real tools, clamping,
adhesive cure and measured fit were not modeled or physically tested. B01/B02/B06/B10/B11
and dependent interfaces stay open. PR for review only; implementation agent does not merge.
