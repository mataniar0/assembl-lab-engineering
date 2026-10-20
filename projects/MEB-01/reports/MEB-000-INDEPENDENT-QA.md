# MEB-000 — independent G0 reference QA

**PR:** #17 / Issue #16. **Original intake head:** `50e1c6b753f0d12dc54057c4063b1992405bfb78`.
**Legacy source:** `mataniar0/assembl-lab-site` at `ebeefe308efaf80329e16e42a84d51557878fd58`.
**Reviewer:** `/root/independent_meb_qa`, a separate reviewer agent from the implementation agent `/root`.
**Scope:** read-only review of the pinned DXFs, nominal geometry, source identity,
new audit implementation and measured vertex-reference proposal. The owner
subsequently specified cutting stock HEIGHT 800 × WIDTH 440 mm and opening
110°; these are requirements, not tested geometry. This review does
not approve a new product datum, material, actual stock conformity, achieved opening,
G1 part design, G2 solid assembly or G3/G4 physical/manufacturing release.

**Disposition: PASS for bounded G0 source-reference evidence; full G0 approval remains BLOCKED.**
An engineering-lead review and approval of the proposed datum remain prerequisites. No merge
or manufacturing authorization was performed or recommended.

## Independence and commands

The reviewer read repository AGENTS, the engineering Skill, Playbook, gate/QA
policies, MEB brief/status/decisions, draft contract and handoff, the pinned README
and historical audit. The review uses a separately written standard-library raw
DXF group-code reader, Git-object hashing, vertex extrema, shoelace arithmetic
and axis clipping. It imports neither the implementation geometry code nor
`ezdxf`/`shapely` for its primary measurements.

From the repository root:

```sh
python projects/MEB-01/reports/MEB-000-independent-raw-qa.py /tmp/meb-legacy-site
```

The site repository must contain the pinned commit; the command reads blobs via
`git show` and never checks out or changes legacy files. The script writes only
`MEB-000-independent-evidence.json` beside this report.

Independent implementation replay, using the installed pinned geometry tools:

```sh
/workspace/.venvs/meb-000/bin/python projects/MEB-01/tools/audit_geometry.py \
  --source /tmp/meb-legacy-site \
  --output /tmp/independent-meb-replay.json \
  --profiles /tmp/independent-meb-replay-profiles.json
```

The returned evidence and profile objects were compared to the submitted JSON
objects and both matched after final regeneration to 49 PASS / 7 NOT_RUN,
including owner-decision wording. Audit exit status is **1**, correctly reporting
the failing 6 mm target-stock check; this is not a parser failure. The 4 mm
layout bounding fit passes; 6 mm existing layout fails. No failure is masked. The legacy Git worktree had no changes. Output hashes
are verified by the implementation and independently by the raw reader.

## Independent test accounting

| Suite | Unique cases | PASS | FAIL | NOT_RUN |
|---|---:|---:|---:|---:|
| Registered legacy blob byte sizes and Git-object SHA-1 | 20 | 20 | 0 | 0 |
| Raw structural DXF parse, explicit mm units, layers, closed polygon declarations and vertex counts | 17 | 17 | 0 | 0 |
| Direct dimensions, nominal interfaces, symmetry, kerf extents, sheet extrema, clipping and thin-land observation | 22 | 22 | 0 | 0 |
| Expected rejection of wrong units, open contour, missing EOF and wrong vertex count | 4 | 4 | 0 | 0 |
| **Independent raw total** | **63** | **63** | **0** | **0** |
| Generated SVG path/units/closure/label check, one per profile | 14 | 14 | 0 | 0 |
| **Independent raw + export total** | **77** | **77** | **0** | **0** |

These are 63 separately identified reviewer cases, not the historical 56-row
suite and not 63 physical tests. Raw structural parsing is not a full proof of
non-self-intersection, hole nesting or manufacturing contour suitability.
Implementation replay and repeated runs are not added as new unique raw cases.
The implementation unit suite initially passed 13/13 test methods, including
14 DXF round-trip profile subtests. After the output-protection guard was added,
the independent 14-method replay exposed one new error: valid temporary output
was rejected due to the platform `/tmp/.git` mount stub. The implementer repaired
Git-root detection; **final independent replay is 14/14 PASS**, including the
source-protection test and all 14 profile round-trip subtests. The original error
log remains at `MEB-000-independent-unit-initial-error.log`. These are replays, not additional independent raw cases. See `MEB-000-independent-unit-replay.log`.
Generated SVG XML was parsed independently for all 14 profiles: every path
coordinate matched the measured model within 1e-8 mm, closed states matched,
root dimensions declared mm and titles declared DESIGN_ONLY. See
`MEB-000-independent-svg-replay.log`. SVG screen-y orientation is not an
assembly coordinate transform.
The implementation maps 49 scoped PASS and 7 NOT_RUN to the 56 historical
indices; these statuses are not 49 fully reproduced historical physical claims.
`MEB-000-independent-audit-replay.log` retains the independent replay output.
Intake registry was independently replayed: baseline and 8 expected rejection
controls PASS (`MEB-000-independent-intake-replay.log`). The approved parameter
set is limited to three owner targets with Product owner identity/date; no
geometry/material measurement is promoted to FROZEN.
G2/G3 evidence is NOT_RUN, rather than silently counted as PASS.

During creation of the review harness, two attempts incorrectly rejected valid
legacy layer names (`CUT_6MM` and `LIVING_HINGE_CUTS`), and one attempt incorrectly
measured end margins from tab extrema instead of main skin edges. These were
reviewer-harness errors, corrected without touching any DXF. The final run passes;
no source failure was hidden by modifying source geometry.

## Verified geometry and limits

- Front/rear profiles: 322 × 71 mm. End profiles: 77 × 71 mm. Bottom: 322 × 77 mm.
  Subtracting the **nominal, unmeasured** 6 mm construction yields the stated
  310 × 65 × 65 mm cavity under the proposed assembly registration.
- Front/rear, body ends, lid ends and beams are byte-identical symmetric pairs.
  They cannot be distinguished as A versus B by geometry alone. Sheet quantities
  therefore require shape-group accounting, not fictitious unique shape IDs.
- Bore/pin/cap diameters measure 14.6/14/22 mm. Nominal radial running clearance is
  0.30 mm and cap radial overlap 3.70 mm. These do not prove actual kerf fit,
  axial retention, adhesive strength or unobstructed rotation.
- Ring-foot clipping independently gives 192 mm² with the explicit **inferred**
  ring-to-end translation `(-22,+59)`. This registration is a proposal; it is
  not a stored 3D transform or an approved datum in the legacy DXF.
- Both lid ends have five closed openings, including two 6 × 6 mm beam slots.
  Nominal zero-clearance joints require physical calibration.
- The skin contains 190 open kerf lines. Their x envelope is 18..304 mm.
  This gives 12 mm margins from the main skin edges x=6..316, or 18 mm from the
  complete contour's tab extrema x=0..322. The uncut center band is x=154..168.
- Legacy sheet bounds are `[14,20,836,368]` (6 mm) and
  `[10,10,332,104.7965436107]` (4 mm). The legacy coordinate convention is X along
  900 and Y along 440; it is not CTB-01's portrait datum. Extents do not establish
  collision-free nesting by themselves; the implementation performs a separate
  polygon overlap check. The 822 × 348 mm 6 mm layout cannot fit either
  orientation of an 800 × 440 mm stock rectangle as presently arranged.
- Vertex-reference JSON is a reproducible coordinate tracing, **not a new
  high-level generative CAD design**. Its status and limits must stay explicit.

## Findings and disposition

| ID | Severity | Finding | Required disposition |
|---|---|---|---|
| IND-01 | MAJOR provenance | Intake claimed pinned V8.2.2 README specifies 110°; that README contains no opening-angle requirement. Historical audit row 46 asserts a 0–120° 2D sweep. | **CORRECTED** false attribution; owner subsequently chose 110° and the new decision is recorded. Achieved motion remains NOT_RUN. |
| IND-02 | HIGH G1/G3/G4 risk | Lid-end outer crown contains `(57.5,27.4347826087)` and centered skin-slot crown `(57.5,27.3347826087)`: only 0.100 mm nominal crown material. Independent Shapely replay reports shortest lands about 0.09974969 mm at all three skin openings. The old 5.780 mm between-hole bridge does not address this exterior web. | **OPEN as MEB-B12.** Source preserved; review kerf/manufacturability/material consequences before dependent design/release. No approved redesign is implied. |
| IND-05 | MAJOR unit guard | Mutating approved sheet-height unit from mm to inch while keeping value 800 and approval metadata passed intake validation. | **CORRECTED** approved mm/mm/deg and global mm/deg guards; the new unit mutation is among 8 expected-rejection controls. |
| IND-04 | MAJOR implementation regression | Generator output guard treated any ancestor `.git` stub as an actual checkout; valid temporary round-trip failed with one error. | **CORRECTED** actual `.git` file or `.git/HEAD` required; final 14-method suite passes and source-protection test remains active. |
| IND-03 | Evidence scope | Slot dimension checks do not reproduce the historical bent-tab `contained=1.000000` assertion. Exact shape-group counts do not distinguish identical A/B part identities. | **CORRECTED** final mapping is 49 scoped PASS / 7 NOT_RUN; bent containment and complete motion/retention are not claimed. |

The implementation agent was notified of all five findings before finalizing
its evidence: four reporting/implementation findings corrected and retested;
one newly identified legacy geometry risk preserved OPEN. Final replay returned
0 for the unit suite, 0 for intake registry/8 controls, and the expected 1 for
the documented target-layout failure. Audit and measured-model JSON exactly
matched submitted artifacts. The site source worktree remained clean. Reviewer-authored evidence is not a second independent review of
itself. No reviewer changes were made to implementation or legacy source files.

## Gate recommendation and score

For the **bounded reference-evidence delivery only**, the policy-adapted score is:
contract/traceability 18/20; measured geometry/export reference 24/25;
interface evidence boundaries 18/20; reproducibility/negative controls 20/20;
documentation/handoff 14/15: **94/100**.

**Recommendation: approve only the source-reference evidence for engineering-lead
review; do not approve full G0 or start dependent G1 work automatically.**
The owner has now resolved requirement values: stock HEIGHT 800 × WIDTH 440 mm
and opening 110°. This resolves uncertainty about the requested targets, not
MEB-B01 physical layout compliance (legacy 822 × 348 mm still fails the stock)
or MEB-B02 achieved 3D motion (NOT_RUN). MEB-B09 proposed datum/finished geometry
still requires review/approval. The new thin-web risk remains OPEN. Remaining adhesive, bend, axial, insertion and
physical risks retain their later-gate blockers. Score ≥90 cannot override any
blocker or imply fitness for cutting, assembly, physical safety or production.

GitHub API access was unavailable to the implementation session, so this review
covers repository content and source evidence, not unseen Issue/PR discussion or
hosted GitHub Actions results. The final branch diff and upload status are to be
verified by the implementation agent before submission.
