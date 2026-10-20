# CTB-006 delivery — P06 ring alternatives

**Issue:** [15](https://github.com/mataniar0/assembl-lab-engineering/issues/15)
**Branch:** `codex/ctb-006-ring`; baseline `c27f722e16668e4ed32cee1c72f5a699b40e504e`.
**PR:** PENDING_SUBMISSION.
**Stage:** G1/G2a bounded study, DESIGN_ONLY / AWAITING_LEAD_SELECTION / CR_REQUIRED.
Implementation: Codex `/root`. Independent reviewer: separate `/root/ctb006_qa`.
QA score/result: **96/100, zero in-scope critical/major defects**; see [independent report](CTB-006-INDEPENDENT-QA.md).
No self-merge, physical cutting, whole-product G2b, G3 or G4 approval.

## Delivered files

| Path under projects/CTB-01 | Content / part / source |
|---|---|
| parts/P06/src/ | parametric model/design/schema, pinned dependency chain, generator/staged preview,336 protected hashes |
| parts/P06/variants/A/ | P06A 1:1 DXF/SVG/PNG; dimensions/BOM; connections and exact motion proofs |
| parts/P06/variants/B/ | P06B1/B2/B3 +6 identical KEY blanks, 1:1 cut/dimension outputs |
| parts/P06/variants/C/ | P06C +6 identical KEY blanks, 1:1 cut/dimension outputs |
| parts/P06/proposals/{A,B,C}/ | six-identical P01-ring-interface-study-v1 overlay, not an approved original change |
| parts/P06/assembly/ | conditional28/36/34 real-body GLBs+metadata; original-cheek BLOCKED matrices; early/late full sweeps; support/sections; actual/exploded/staged PNG/SVG |
| parts/P06/tests/ |42 new +8 focused executable cases, independent OCC audit, clean runner, retained failure/pass/dependency logs |
| parts/P06/BOM-v1.csv | A1/B9/C7 actual added pieces, no hidden hardware |
| parts/P06/DECISIONS.md |8 bounded design decisions, selected-vs-provisional tracing |
| parts/P06/P01-INTERFACE-CHANGE-REQUESTS.md | precise unapproved CRs, altered material/assembly and acceptance conditions |
| parts/P06/CTB-007-008-009-HANDOFF.md | P01/P02/skin/lock/stability reservations and future tests |
| reports/CTB-006-{DESIGN-REVIEW,INTERFACE-MATRIX,VALIDATION,INDEPENDENT-QA,DELIVERY}.md | comparison, interfaces, actual tests/failures, distinct reviewer, delivery |
| STATUS.md | current P06 state; all official B/IF blockers preserved |

The complete file list is `parts/P06/DELIVERY-FILES.txt`. Approved CTB-000/P01–P05 originals,
selections and frozen dimensions are untouched;336 protected files match baseline SHA.

## Acceptance and evidence

| Requirement | Result | Evidence |
|---|---|---|
|3 meaningful parametric concepts, all6 cheek attachments | PASS conditional study | variants + proposal overlays + full matrices |
| Current S3 at200, four spacers preserved | PASS nominal | full27 consumption and IF01 tests;39mm slab gap |
| Historical245 S3, original cheeks, late A/C trials | deliberately BLOCKED | retained negative matrices/sweeps |
| Actual assembly sequence | PASS specified conditional routes | A28/406; B early28/378 then late12/363; C34/595 stages/checks |
| P01 change authorization / positive ring retention | OPEN / CR_REQUIRED | all3 source-preserved CRs; free release directions |
| Single part stock fit / cut export integrity | PASS geometry only | DXF/SVG/PNG parity,10mm margin; no nesting approval |
| Frozen inputs/top50 and all336 prior files | PASS unchanged | focused tests and SHA inventory |
| Physical fit/kerf/glue/load/stability / cutting | NOT_RUN / NOT_APPROVED | no measured evidence exists |
| Broad nightly CAD regression | NOT_CONFIGURED | infrastructure Issue20; no successful workflow claimed |

Recommendation: C for continued retention study, still AWAITING_LEAD_SELECTION. C obstructs
outward cheek translation only with fixed keys, which lift out freely;7.8mm² actual head seat
requires assessment/redesign. A/B simpler/segmented alternatives remain useful but do not
capture outward-t cheek motion. These limits are not hidden as a solved ring connection.

## Checks and failure history

Clean isolated build command and full versions/logs in CTB-006-VALIDATION.md:
42new +8 focused +25 source +15 import = **90 unique PASS**,0 final unexpected failures.
Complete prior337 run NOT_RUN:40 selected static cases ran,297 unaffected component cases
NOT_RUN. Independent repeat50 is not added to unique90; alternate OCC evidence is separate.
Final committed candidate SHA/retest result is recorded in the PR.

Four observed execution failure conditions: C key fillet overlap, generator stage field name,
B aggregate-topology assertion, footprint exact-float assertion. Repaired and retested.
Three review corrections: actual exterior fillets, conditional section caption, B raised-entry
endpoint metadata. Failure logs retained; deliberate BLOCKED trials remain. The independent
review's own numerical sweep-construction correction is reported separately and preserves
actual exports. See detailed rows in VALIDATION/INDEPENDENT-QA.

## Outstanding decisions and gate limits

Lead must select a concept/CR; decide keeper self-retention and C seat adequacy; review
cheek material loss/fixture access and all3 leg interactions. B02/B05/B07/B10/B11 remain
open; B01/B06 upper-lock/bond/P05 outward retention remains open, all B01–B13 preserved.
Measured thickness/kerf/grain/coupons, loads/friction/centre of gravity/stability, structural
assessment and supervised physical sequence are NOT_RUN. No DXF is released for cutting.

Submit only for independent engineering-lead review. No merge performed by implementation.
