# CTB-01 status — CTB-005 reviewed radial-web working concept

**BASELINE_FOR_COMPONENT_DESIGN_NOT_PRODUCTION** — CTB-000 v0.2 merged in PR #2.
**CTB-001 / P01: SOFT_CURVE SELECTED_FOR_DOWNSTREAM_COMPONENT_DESIGN — DESIGN_ONLY.**
Three parametric cheek candidates delivered under Issue #3; the engineering lead selected
SOFT_CURVE for downstream coordinated design, per `parts/P01/P01-SELECTION.md`.
This is not complete G1 joinery approval, nor permission for physical manufacture/nesting.
See [design review](reports/CTB-001-DESIGN-REVIEW.md),
[interface matrix](reports/CTB-001-INTERFACE-MATRIX.md) and
[validation record](reports/CTB-001-VALIDATION.md).
Final automated checks: 61 P01 + 25 source + 15 import = 101 passed, zero final failures.
Initial failures and repairs are retained in the validation record; independent automated
QA is recorded separately and does not replace engineering-lead approval.

## CTB-002 — B SELECTED_FOR_COORDINATED_DESIGN / DESIGN_ONLY

Issue #5: three spacer joint studies and a versioned SOFT_CURVE mortise proposal.
Engineering lead selected B_THROUGH_ADHESIVE as DESIGN_ONLY working concept.
See `parts/P02/CTB-002-SELECTION.md` for decision/limitations.
B_THROUGH_ADHESIVE has one reinforced P02B at35 and three identical P02
at90/200/390. Candidate BOM P02×9 +P02B×3 +P01×6. Original P01 files/exterior unchanged.
Local rigid CAD final/swept checks pass for B; this does not prove adhesive, material,
physical fit, retention or whole-table assembly. A explicitly BLOCKED; C alternative
requires review. PC-CTB002-01 adopts Z200 as provisional downstream candidate, pending CTB006
ring coordination. Ring remains OPEN; no ring-specific holes. All B01–B13 preserved.
See [CTB002 comparison](reports/CTB-002-DESIGN-REVIEW.md),
[interface matrix](reports/CTB-002-INTERFACE-MATRIX.md) and
[validation/failures](reports/CTB-002-VALIDATION.md).
Final automated suites52 P02 +61 P01 +25 baseline +15 import =153 passed;
independent CAD-kernel QA is recorded in CTB002-INDEPENDENT-QA.
No final G1 joinery or physical cutting approval. No automatic merge.

## CTB-003 — A_COMPACT_CLOSED SELECTED_FOR_DOWNSTREAM_COORDINATED_DESIGN / DESIGN_ONLY

Issue #7: three single-piece CSH-3Y/P03 joint studies. Engineering lead selected
A_COMPACT_CLOSED as working DESIGN_ONLY solution, per `parts/P03/CTB-003-SELECTION.md`. Local armtip85.5/maxXYradius85.769983 resolves94/90
mismatch in candidate geometry, with4.5 mm local end margin. Official B04 remains open pending integrated evidence. A/B closed-hole prebuilt translation approaches BLOCK;
19-piece Y-first route has18 moving stages/171 continuous checks PASS per concept.
C radial prebuilt route PASS requires open-edge cheek CR and has no reverse retainer.
Only versioned P03 cheek copies change; all original P01/P02/CTB000 bytes preserved.
Selected spacer B and provisional35/90/200/390 unchanged, all4 spacers retained/leg.
See [comparison](reports/CTB-003-DESIGN-REVIEW.md),
[interface matrix](reports/CTB-003-INTERFACE-MATRIX.md),
[validation/failures](reports/CTB-003-VALIDATION.md).
Final suites51P03+52P02+61P01+25contract+15import=204 passed; separate automated QA
is recorded in CTB-003-INDEPENDENT-QA.md. No human G1/whole-table G2, stock/kerf,
physical strength/stability or cutting approval. No automatic merge.

## CTB-004 — A_RIM_OPEN / NO_HOLE SELECTED_FOR_COORDINATED_DESIGN — DESIGN_ONLY

Issue #9 / PR #12: three central P04L/P04U disk studies and nominal continuous insertion
with the selected Y_FIRST 19-part base (21 actual CAD bodies).
Engineering lead selected `A_RIM_OPEN` with `NO_HOLE` as the P05 design baseline;
see `parts/P04/CTB-004-SELECTION.md`.
The disk planes remain P04L Z456..462 and P04U Z480..486; 18mm free face gap.
Six tongue holes and six distinct web openings exist in each candidate disk.
A's radial OPEN P05 connection has no verified positive retention; no real P05,
P07 skins, P08 lock or final ring is in the 21-body model.
Independent QA reports 275/275 test PASS and 96/100. The primary 22 initial
test failures and corrections are retained in CTB-004-VALIDATION.md.
Nominal stiffness, material fit, load, retention, whole-product assembly,
physical kerf calibration and manufacturing release remain OPEN.
B13 center opening is resolved provisionally as NO_HOLE for downstream CAD only.

## Authoritative baseline

All 15 original files are in `specifications/CTB-000/`, byte-for-byte unchanged.
Use `CTB-000_parameters.json` and `CTB-000_interfaces.json`; diagrams are schematic.
Preserved interfaces: IF-01 through IF-14; no interface is upgraded to validated.

Ø350 mm tabletop, 500 mm overall height, 50 mm top thickness; three legs at
0°/120°/240°, each with two parallel 6 mm birch cheeks, 15 mm inner gap, four
spacers per leg. CSH-3Y hub, CSH-3P anchor disks, VTP-R KERF-4 FLEX 4 mm birch rim.
Cutting stock: **800 mm height × 440 mm width**, portrait; X≤440/Y≤800.
Compatibility array is `[height,width] = [800,440]`.

## Unresolved issues (preserved, not closed by import)

| ID | Severity | Topic | Owner | Closure condition |
|---|---|---|---|---|
| B01 | BLOCKER | TOP LOCK | CTB-004 / CTB-008 | No structural assembly release |
| B02 | BLOCKER | ASSEMBLY ORDER | CTB-003 / CTB-004 / CTB-009 | Demonstrate a collision-free sequential assembly |
| B03 | BLOCKER | LEG GEOMETRY | CTB-001 | Produce single source of truth for six identical cheeks |
| B04 | HIGH | Y ARM ENVELOPE | CTB-001 / CTB-003 | Resolve 4mm overhang and mechanical joint reach |
| B05 | HIGH | RING INTERFACE | CTB-002 / CTB-006 | Specify one engagement design and no clash |
| B06 | HIGH | HUB-RIB INTERFACE | CTB-004 / CTB-005 | Demonstrate 3D intersections and assembly |
| B07 | HIGH | STABILITY | CTB-001 / CTB-009 | Set design loads and test stability |
| B08 | HIGH | KERF WALL | CTB-007 | Build 50mm coupons and test bend/joint/glue/filler |
| B09 | MEDIUM | RIM GEOMETRY | CTB-007 | Design and calibrate 2+ segments |
| B10 | HIGH | FIT | CTB-001..007 | Measure actual stock; fit coupon tests |
| B11 | HIGH | MATERIAL/LOAD | CTB-009 / physical trial | Do not present load rating |
| B12 | MEDIUM | SINGLE SOURCE | CTB-000 | Strictly quarantine superseded CAD |
| B13 | MEDIUM | CENTER HOLE | CTB-004 | Verify actual DXF and define opening only if functional |

The complete descriptions remain in the authoritative open-issues CSV. In particular,
B01 upper retention, B02 assembly order and B03 final leg geometry block assembly release.
Legacy V-leg LEG_A/LEG_B and tilted/multilayer CSH CAD remain quarantined as historical
references; no obsolete CAD is present in active sources or imported by this task.
The four historical ZIPs named in MANIFEST.json were not supplied; their hashes and
mechanical contents have not been independently verified in this task.

## CTB-000 baseline validation history and source discrepancies

See `reports/CTB-000-DELIVERY.md`, the complete test logs and source SHA-256 inventory.
Source validator: 25/25 PASS. Additional import consistency checks: 15/15 PASS.
Original CTB-000 frozen and provisional data remain unchanged. CTB-002 separately proposes
spacer245→200 only in versioned candidate data, pending CTB006 coordination. Local
one-leg nominal CAD collision/insertion proof is documented above; full-table3D integration,
physical fit/bending, load/stability and actual nesting remain unverified.

The supplied SVG/PNG retain a v0.1 title inside a v0.2 package and a schematic forked
side silhouette. These are source presentation discrepancies, not authoritative leg CAD.
They are preserved for review; do not use their silhouette to start CTB-001.
The only 900×440 mentions document the superseded sheet, not active settings.

## Next gate

Engineering lead selected SOFT_CURVE; CTB-002 now proposes coordinated candidate P01
mortises and four spacers. Lead review selected B joinery as a CAD working concept and provisional Z200.
CTB003 lead selection approved A_COMPACT_CLOSED and Y_FIRST for downstream DESIGN_ONLY studies, per parts/P03/CTB-003-SELECTION.md. CTB004 lead selected A_RIM_OPEN / NO_HOLE for downstream DESIGN_ONLY development, per parts/P04/CTB-004-SELECTION.md. CTB005 selection now awaits review.
CTB006 ring agreement and B adhesive/outward retention remain unproven. Original P01/P02 and frozen system parameters remain unchanged.
See `parts/P01/P01-SELECTION.md` and CTB002 reports.
Y reach, ring/spacer coordination, fit, locking, assembly, stability and all B01–B13
records remain open. Complete G1 joinery, integration and production are not approved.
Production remains blocked through independent assembly QA and physical tests.

## CTB-004 — THREE_CANDIDATES_PENDING_LEAD_SELECTION / DESIGN_ONLY

Issue #9, PR #12 for review (unmerged), existing branch `codex/ctb-004-anchor-disks`: A_RIM_OPEN, B_CLOSED_RAIL and
C_MIXED_ACCESS. Two distinct Ø190×6 disks, L456..462/U480..486, freegap18, pitch24,
tabletop envelope50mm preserved. Six real tongue holes and six separate web interfaces
per disk; matching connected38mm web witnesses reserved for CTB-005, not final P05 CAD.
Actual19-body selected base +two disks =21 real bodies; skins/rim/web/tool studies excluded.
A with NO_HOLE is recommended only, not selected. C upperØ24 is provisional comparison.

Final primary and independently rerun suites:71 new P04 +204 upstream =275 uniquePASS.
Independent OpenCASCADE review reconstructs exports; source/output174 protected files
unchanged. Each variant210 actual final pairs,60 continuous skin/disks checks and conditional
web-route168 checks pass nominally. Tested reverse/late installation routes block explicitly.
See reports/CTB-004-DESIGN-REVIEW.md, INTERFACE-MATRIX, VALIDATION and INDEPENDENT-QA,
plus parts/P04/CTB-005-HANDOFF.md and assembly/proofs.json. Initial22 failed cases and
export/illustration repairs are retained; no final unexplained nominal CAD failure.

B01 positive lock, B02 complete order, B06 finalweb/structural attachment, B10 material/kerf,
B11 load/stability and B13 center decision remain OPEN, along with all other original records.
Only2mm tongue projection above U; no positive lock is designed. No complete tabletop,
physical fitting, nesting, cutting, strength or manufacturing release. PR for review only;
no self-merge.

## CTB-004 selection superseding historical pending text above

PR #12 was merged by the lead; `parts/P04/CTB-004-SELECTION.md` selects A_RIM_OPEN /NO_HOLE
for downstream coordinated design only. Earlier pending/unmerged captions are historical.
No actual P05/P07/P08, physical fitting, structural approval or cutting was implied.

## CTB-005 — A_RELIEVED_BOND SELECTED_FOR_DOWNSTREAM_COORDINATED_DESIGN / DESIGN_ONLY

Issue #13 / PR #14 reviewed for DESIGN_ONLY; source baseline6292a0e. Three real six-identical-rib
concepts: A_RELIEVED_BOND, B_DOUBLE_RAIL and C_LOWER_CAPTURE_STEP. All259 CTB-000/P01–P04
source/output files remain unchanged. Exactly P05×6 adds to the selected21 to make27 real
bodies; skin/wall/tool/lock studies remain non-BOM reservations. Ø350/H500/top50, rib38 and
free disk-face gap18 are preserved. Single-part H800×W440 fit is checked, not nesting.

A/C fit original P04 and have radial insertion paths, but outward withdrawal is free.
B is BLOCKED against original U at28.8 mm³ per rib. Separate CR B substitutes two v2 disks;
CR C substitutes only lower, keeping original U. Both CRs remain unapproved and only their proposal models pass fit and staged
paths and obstruct specified translations with disks fixed. This is not 6DOF or strength
proof; both CRs are NOT_APPROVED. Engineering lead selected **A_RELIEVED_BOND** for bounded downstream CAD only;
see `parts/P05/CTB-005-SELECTION.md`. Radial restraint remains OPEN.

Clean reproduction passes337 unique checks (62 new +275 prior), with independent reruns
and alternate OpenCASCADE audit. All initial concept/reviewer failures and corrections are
retained in CTB-005 validation. See reports/CTB-005-* and parts/P05/CTB-007-008-HANDOFF.md.
Positive upper locking/disk Z restraint, structural bonds, C's small stop, complete order,
real stock/kerf, glue/fixtures and load/stability remain open (B01/B02/B06/B10/B11).
Whole-product G2b, physical G3 and production G4 remain unapproved. No physical cutting.

## CTB-006 — THREE_CANDIDATES / AWAITING_LEAD_SELECTION / DESIGN_ONLY

Issue #15, review PR [#22](https://github.com/mataniar0/assembl-lab-engineering/pull/22),
branch `codex/ctb-006-ring`, basec27f722 after P05A selection. All336 protected
CTB-000/P01–P05 files are byte-identical. Three provisional6mm P06 ring/interface studies
atZ245/slab242..248: A triangular1piece (28actual bodies), B3 matched T-splice segments
+6 radial stops (36), C circular1+6 vertical keepers (34). All4 spacers/leg retained at
35/90/200/390. Ring slab gap to S3=39mm; complete-family minima A39/B35.8/C32.
Actual Y407..413 and unchanged top50 remain clear. Single-part portrait H800×W440 fit
with10mm margin passes, NOT approved production nesting.

All alternatives need P06-local `P01-ring-interface-study-v1` CRs; originals BLOCK.
Conditional A/C ring-before-Y_FIRST and B two-phase after-closed27 routes pass exact sweeps.
A/C tested late vertical/radial routes BLOCK. C is recommended only for further retention
study, NOT_SELECTED: keys-fixed transverse restraint exists, but keys lift out freely and
actual7.8mm²/key bearing seat is unverified. A/B outward cheek movement and B plug ejection
are free. No fully self-retained mechanically locked ring is claimed. B05/IF-09 OPEN/CR_REQUIRED.
Temporary fixture/handling, structural cheek material loss, whole-product order and all
physical measures remain OPEN. P05A outward-retention is not solved by P06.

Risk-based checks:42 new P06+8 focused IF09/01/02/14+25 baseline+15 import =90uniquePASS.
All-source hash inventory336 checked. Complete prior337-suite NOT_RUN;40 static cases ran,
297 unaffected P01–P05 component cases deliberately NOT_RUN. Tier3 scheduled CAD workflow
absent: NIGHTLY_REGRESSION_NOT_CONFIGURED, tracked in separate infrastructure Issue #20.
Independent reviewer and alternate OpenCASCADE:96/100, zero in-scope critical/major defects;
see CTB-006-INDEPENDENT-QA.md.
All initial failures/corrections preserved in CTB-006-VALIDATION.md and P06 tests/logs.

See five `reports/CTB-006-*`, P06 `DECISIONS.md`, `P01-INTERFACE-CHANGE-REQUESTS.md`,
`CTB-007-008-009-HANDOFF.md`, BOM, variants and actual assembly/section/staged outputs.
Official B01–B13 and IF-01..IF-14 records remain unchanged. No loads, stock/kerf, adhesive,
fixture, stress/bending/stability or physical tests: NOT_RUN. FullG2b/G3/G4 and physical
cutting NOT_APPROVED. PR for lead review only; no automatic merge.
