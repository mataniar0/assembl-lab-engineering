# MEB-000 / Issue16 / Draft PR17 — G0 reference verification delivery

**Branch:** `feature/meb-000-legacy-intake`.
**Reviewed starting head:** `50e1c6b753f0d12dc54057c4063b1992405bfb78`.
**Implementation:** Codex `/root`. **Independent reviewer:** `/root/independent_meb_qa`.
**Date:**2026-10-20. **Release:** DESIGN_ONLY. **Full G0:** REVIEW_REQUIRED / BLOCKED
pending engineering-lead acceptance of the proposed datum and bounded geometry.
No merge, G1 start, physical test or production authorization is claimed.

## Outcome and requirements

Owner explicitly confirmed **stock HEIGHT800 × WIDTH440mm** and **opening110deg**
in this task. These three values alone are FROZEN requirements with owner/date
provenance. They do not freeze measured material or imply achieved motion.
The earlier attribution of110deg to the pinned README was wrong and corrected:
that README contains no angle requirement. The new110deg value comes from the owner.

Verified all20registered source blobs by pinned Git SHA/size and working-copy
byte equality; parsed all17DXFs with explicit mm units. Source geometry is read,
never healed or rewritten. Site worktree remains clean. No CTB planning files or
other project files were modified. Immutable legacy inventory remains unchanged.

The reconstructed reference covers all14part definitions/17assembly instances.
One measured-vertex JSON model generates separate DESIGN_ONLY DXF/SVG proposals.
This is a coordinate-parametric trace, not a fully generative dimension-driven
CAD kernel. Body/envelope and interface numbers below are nominal CAD evidence,
not frozen product dimensions or manufacturing approval.

- Proposed body envelope322×77×71; cavity310×65×65 with nominal6mm construction.
- Proposed right-handedXYZ frame and partial hinge/lid registrations are explicit
  in FRAME_AND_LIMITS. Complete finished envelope and datum approval remain OPEN.
- Pin/bore/cap14/14.6/22mm; nominal radial running gap0.30mm, cap overlap3.70mm.
- Ring-foot192mm² geometric overlap under the explicitly inferred transform;
  no strength claim.190kerf lines and14mm uncut center band independently checked.
- **Existing6mm layout FAILS target:** bbox822×348 cannot fit800×440 in either
  right-angle orientation. This is failure of the present arrangement, not proof
  that a new nesting is impossible. The4mm layout bbox322×94.796544 fits bounds
  only. Original sheets remain unchanged; new packing is still needed for G4.
- **New MEB-B12 risk:** shortest exterior material at each curved lid-slot is
  about0.09974969mm. This differs from5.780053mm between-hole bridge. Keep OPEN
  for competent geometry/kerf/material assessment before dependent G1/release.

## Requirement-to-evidence acceptance

| Requirement | Result | Evidence |
|---|---|---|
| Pin source identity and leave original files unchanged | PASS | MEB-000-geometry.json provenance20items; independent63case raw evidence; clean site Git status |
| Inspect every originalDXF | PASS |17file metrics, polygon topology/layers/unit checks |
| Check BOM against actual sheet geometry | PASS for shape groups |14definitions/17instances; identical A/B shapes cannot establish semantic labels separately |
| Reproduce all56historicalPASS claims | NOT_COMPLETE |49scoped2D/intakePASS;7NOT_RUN; no56PASS claim |
| Reconstruct reproducible G0 proposals | PASS within traced-reference scope |14DXF/SVG pairs round-trip; high-level generative kernel not implemented |
| Establish approved complete product datum/geometry | BLOCKED | Body frame proposed; full finished envelope/datum needs lead review |
| Current6mm nesting meets approved stock | FAIL |822×348 vs800H×440W; target JSON and audit exit1 |
|110deg continuous solid motion and complete insertion | NOT_RUN | G2 separately scoped evidence required |
| Independent review | COMPLETE for bounded source-reference evidence | MEB-000-INDEPENDENT-QA.md, score94/100 |
| Physical/material/kerf/bend/bond/load | NOT_RUN | G3 |
| Production | NOT_APPROVED | G4 |

## Actual test accounting and commands

All commands run from repository root; retained stdout/stderr/exit status in
`MEB-000-logs/`. The tested dependency lock is in `../tools/requirements.lock`.

| Suite | Unique cases/assertions in that suite | Result |
|---|---:|---|
| Intake CLI baseline + registry negative controls |1positive aggregate +8negative cases | PASS, exit0 |
| Geometry/reconstruction unittest |14test methods;14profile subtests within one method |14/14PASS, exit0 |
| Legacy-index mapping in geometry audit |56indices |49scopedPASS,7NOT_RUN |
| Target stock checks in same geometry audit |2layouts |1PASS,1FAIL; overall audit exits1 |
| Independent raw checker |63cases |63PASS |
| Independent SVG coordinate/units/closure checks |14profiles |14PASS |
| Existing playbook validator |115assertions |115PASS |
| Existing playbook mutation suite |12test methods |12PASS |
| Existing CTB static contract / source inventory |25+15assertions |40PASS |

Do not sum these rows as distinct product tests: repeated source dimensions,
implementation replay and subtests overlap. Independent review's own unique total
is77raw/export cases, separately identified in its report. No skipped unit tests.
Expected negative-control rejection is a pass for the checker, not a good part.
The7NOT_RUN historical indices are31–33(bent-tab containment),43(pin/ear bond
placement),44(unspecified neck section),45(axial-shim setup),46(solid swept motion).
Some partial2D metrics were measured for these; the full original claim stays NOT_RUN.

The audit explicitly retains targetFAIL and exit1. Neither successful parser work
nor a high QA score overrides that failure. See tools/README for exact commands.

## Failure and repair history

Four findings from the independent review were corrected/retested:
1. False pinned-README110deg attribution; corrected provenance before recording
   the owner's newly supplied110deg requirement.
2. Initial curved-slot PASS labels implied more than the implemented dimension
   checks; final indices31–33 are NOT_RUN for the original full containment claim.
3. Generator safety guard treated platform empty `/tmp/.git` mounts as checkouts,
   breaking valid temp-output roundtrips. Corrected to real Git metadata markers;
   source-write refusal and positive temp generation both now pass.
4. Frozen requirement values initially lacked unit verification. Enforced mm/mm/deg
   and coordinate mm/deg; added intentional wrong-unit negative control.

Four additional checker-development defects were corrected before final delivery:
- Initial coupon parser rejected legitimate nested detached pins in bores. Added
  explicit even/odd contour-depth interpretation, tested by a nested-island case.
- Initial ezdxf Vec3 slicing raised TypeError. Read explicit x/y components.
- Two band checks initially failed because cuts touch band boundaries. They test
  penetration into the band interior; ending exactly on its edge remains visible.
- Three curved-slot dimension checks initially used slot mid-radius arc instead
  of the historical outer-radius reference. Report both11.594819actual mid-arc and
 12.2outer-reference arc; preserve full bent-tab containment as NOT_RUN.

Thus8functional implementation/intake corrections are recorded, not8alterations
of legacy geometry. Audit creation logs retain initial failure and repair stages;
independent initial guard-error output is retained separately. The original
historical3geometry corrections remain historical; none is counted as a repair
performed by this task. CSV newline normalization is formatting, not a functional
repair. Source findings were not suppressed: target packingFAIL and thin-web risk
remain open. All final commands are rerun with exit statuses retained.

## Changed-file groups and remaining work

Only MEB-01 files changed: contract/decisions/status, proposal/reference model and
separate exports, read-only audit/reconstruction tooling, scoped tests and reports.
The original DXF inventory and source repository remain unchanged.
AllIF-01..IF-11 are still OPEN with per-interface new2D evidence mappings.
MEB-B01..B12 stay recorded; owner stock/angle requirement questions are answered,
but packing/motion evidence remains open. No blocker was silently deleted.

Lead review should accept or revise the proposed reference frame and finished
geometry boundary, assess B12 and scope G1 tasks in handoff order: bodyP01..P05,
hingeP06..P10, lid carcassP09..P13, skinP14; G2/G3 follow under separate authority.
No automatic component development or production work is authorized by this report.

GitHub GraphQL and REST API requests returned403. The task uses the repository's
Issue16 handoff; unseen Issue/PR comments and hostedActions were unavailable.
Delivery is committed/pushed to the existing PR branch so these results are visible
as PR files. No claim is made that PR description/comments or draft status were
edited via API. No merge was attempted.

Environment setup and activation instructions were saved in the environment draft
(`install_script`, `start_skill`), using the tested workspace venv. Custom network
addition `api.github.com` was saved to support future Issue/PR API access, preserving
package-manager presets. Saving does not apply/publish changes: review/save in
environment settings and publish to activate the reusable configuration. Current
Git push access is separate from blocked API access. No credentials are needed
for the geometry workflow and no secret values were requested or saved.
