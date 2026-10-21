# CTB007 delivery — skins and experimental kerf perimeter

Issue[24](https://github.com/mataniar0/assembl-lab-engineering/issues/24), existing branch
`codex/ctb-007-skins-rim`, baseline 6db45fa7ba0d9a81ff9bbc6d1a432133ab955214.
**PR:** [#32](https://github.com/mataniar0/assembl-lab-engineering/pull/32), open for review; not merged. **Stage:** G1geometry/boundedG2a, DESIGN_ONLY / AWAITING_LEAD_SELECTION.
Implementation Codex/root; separate reviewer/root/ctb007_qa: **96/100, zero in-scope critical/major defects**; see CTB-007-INDEPENDENT-QA.md.
No self-merge, physical cutting, production or completeG2b/G3/G4 approval.

## Files and outputs

| Path under projects/CTB-01 | Delivery |
|---|---|
| parts/P07/src/ |parametricdesign/model/schema, pinneddependencies, exporter,439 protected hashes |
| parts/P07/variants/A/ |P07B/P07T and2P07R, 1:1DXF/SVG/PNG, dimensions/BOM/paths |
| parts/P07/variants/B/ |two skins and3 stepped P07R segments, explicit radial path/vertical blocked |
| parts/P07/variants/C/ |two proposed edge-comb skins and4 P07R, verticalbefore top vsblockedorders |
| parts/P07/assembly/ |real31/32/33-bodyGLBs/metadata, final/swept/access/contacts, exploded/sections/order views, non-BOM analytic envelope and independent evidence |
| parts/P07/tests/ |46 new+7 focused executable cases, runner, independentOCC audit, all retained failures/pass/version logs |
| parts/P07/BOM-v1.csv |2skins +2/3/4segments, explicitIDs/quantities/thicknesses; no hidden hardware |
| parts/P07/DECISIONS.md |10 bounded study decisions, assumptions and release limits |
| parts/P07/proposals/COORDINATED-CHANGES.md |Cskin construction CR and nonimplementedP05tip alternative, upstream untouched |
| parts/P07/KERF-COUPON-PLAN.md |future measured validation planning only; no physical trial authorization |
| parts/P07/CTB-008-HANDOFF.md |real lock/access/retention/assembly reservations and P06R dependency |
| reports/CTB-007-* (5 reports),STATUS.md |design/interface/validation/independentQA/delivery and preserved gates |

Complete exact path list in `parts/P07/DELIVERY-FILES.txt`. All 439 earlierCTB000/P01–P06
source/export/selection files remain byte-identical. No legacyCAD imported and no approved
P01ring mortises substituted. CTB006R Issue23 stays OPEN; P06 reservation not realBOM.

## Requirement acceptance

| Criterion | Result | Evidence/limit |
|---|---|---|
|Two complete nominal 6mm skins, six actual lower apertures, NO_HOLEtop |PASS geometry |real exported connected material, exact currenttongue transforms |
|Three4mm experimental rim/joint alternatives |PASS study |A2butt/B3step/C4edgecomb, true flatpatterns+mapped perforated material |
|Ø350/H500/top50, portraitH800×W440 |PASS frozengeometry |allactual segments fit10mmmargin, no productionnesting |
|Interfaces disks+sixribs+skins/rim |PASS nominal fit/contact only |face/boundaryareas, allfinalpairs, intentional1.973mmAIR retained |
|Accessible claimed tabletop routes |PASS specifiedidealrigidroutes |Avertical/radial; Bradial; Cverticalbefore top |
|Other tested orders / closedtoplockaccess |BLOCKED, retained |Bvertical,Ctop-first/radial,latebottom,closedwallrib,all sixclosedtop probes |
|Full material deformation/bend, physical joints/retention |NOT_RUN/OPEN |KERF_COUPON_PENDING, no actual P08 or structural bond |
|P06 ring/modifiedcheeks usable/approved |NOT_APPROVED |separateIssue23; noneincluded |
|G2b/G3/G4 and cutting/manufacture |NOT_APPROVED |no material/load/physical evidence |

RecommendationA for least change continued geometry/coupon planning; no selection made.
B needs radial joint closure; C changes only new P07 skin radialconstruction and must precede
top closure. Top uplift remains FREE in allthree; do not mistake seat/edgecontact for a lock.

## Validation, initial failures and repairs

46 new+7 focused+25G0+15import = **93 uniquePASS,0 final unexpected FAIL** in cleanisolated runtime.
347 old untouched componentcasesNOT_RUN (297P01–P05 +50P06); no false fullregression claim.
Independent kernel/method/score and reruns recorded in QA report, not added to unique93.
Exactcommands/versions and retainedlogs in CTB-007-VALIDATION; finalcommitted candidate
SHA/testresult recorded in PR body. All 439 protected bytes and actual export hashes verified.

First generation failed on emptysectionrendering; first 46-caseTier1 had45PASS/1 Cduplicate
failure from a1.745e−12mm edge. Repaired emptygeometry guard and Ctopology-preserving1e−9
cleanup. Contact coincidence, Bseam keepout and explodedcrop corrections retained. Explicit
blockedroutes stayedblocked; B's passingradialalternative proved separately. Independent
legacy-parser, numerical-sweep and partial-facet contact-measurement errors/repairs are
separately logged; no actual component was altered to conceal them. No remaining unexplained scopedCAD failure.

## Open decisions / handoff

Leadselects concept and reviews CskinCR if pursued. Real50mmKERF4 coupon/neutralaxis,
material/grain/kerf/adhesive/clamping/cure, seam/skin bearing/shear/pullout, finish, P08lock/
service access and complete physical sequence remain NOT_RUN/OPEN. P05tipgap isAIR; no
filler or hidden additional member claimed as support. B01/B02/B05/B06/B08–11 and all official
B/IF records preserved, ringfollowupIssue23 required beforeG2b. ScheduledbroadCI absent,
Issue20 tracked separately, NIGHTLY_REGRESSION_NOT_CONFIGURED. No merge or cutting release.
