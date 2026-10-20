# CTB-005 — independent automated CAD QA

2026-10-20. Issue #13; branch `codex/ctb-005-radial-webs`.
Reviewer/session: `/root/ctb005_qa`, separate from the implementing agent.
Approved source baseline: `6292a0e22c9aacade5aa7c7995332494aa8de005`.
**PASS for the bounded G1 DESIGN_ONLY alternatives/local CAD studies.** Lead concept/CR
selection remains pending; this report does not authorize a merge or physical cutting.

## Independence and authoritative inputs

Read root AGENTS, the ASSEMBL LAB engineering skill/playbook/gates/QA policy, CTB-000 v0.2,
P01/P02/P03 selection records, P04 A_RIM_OPEN/NO_HOLE selection/handoff, actual exported
profiles, issue #13 and the new source, reports and proposed contracts. Reviewed
IF-06/07/08/12/13 and B01/B02/B06/B10/B11. No obsolete V geometry or implicit central
aperture was used. Captured a separate pre-task SHA-256 inventory and independently
compared **259/259 CTB-000/P01–P04 original files** to the approved Git commit.

`parts/P05/tests/independent_occ_review.py` imports **no implementation model**. It reads
actual P05, selected P04 A, selected P03 A cheek/Y and P02 B SVG loops, independently checks
DXF polylines and mm dimensions, then builds finite material with CadQuery/OpenCASCADE.
Primary implementation uses Manifold. Exact boundary-prism polygon sweeps/extrusions
cover whole specified translations, not sampled frames. Read-only review of implementation
code supplements, rather than supplies, the alternate exported-geometry proof.

The reviewer wrote only this QA report and the independent runner, not component geometry,
primary tests or source configuration. Design challenges were sent to the implementer;
all actual geometry changes remained their responsibility.

## Independently executed tests

| Suite | Unique cases | PASS | Final FAIL/ERROR | Skipped |
|---|---:|---:|---:|---:|
| P05 real ribs |62|62|0|0|
| P04 disks |71|71|0|0|
| P03 Y/base |51|51|0|0|
| P02 spacers |52|52|0|0|
| P01 cheeks |61|61|0|0|
| CTB-000 contract |25|25|0|0|
| CTB-000 import |15|15|0|0|
| **Total** |**337**|**337**|**0**|**0**|

The unchanged275 upstream cases were independently executed once. New P05 had an early
reviewer run59PASS/3ERROR because handoff/CR documents had not yet been created; after
completion the same62 cases passed, and were repeated after the final cap-metric correction.
Reruns are not additional unique cases. Reviewed the
implementer's clean isolated generation/full-suite log, which also passes337 cases.
No test disabling or frozen-input change was used to conceal a failure.

## Alternate-kernel model, path and export evidence

The selected19-body base independently has171 static pairs at zero overlap. Reconstructed
Y_FIRST18 moving stages and **171 exact continuous prior-body checks**, zero overlap.
The prospective bottom skin remains an envelope, installed before either disk.

| Scenario | Real bodies / final pairs | Whole skin/disk/rib route | Independent result |
|---|---:|---:|---|
| A with original selected P04 |27 /351|207 exact checks|PASS, no overlap |
| B with original selected P04 |27 /351|207 counterfactual checks|**BLOCKED**: six upper-disk clashes28.8mm³/rib,172.8mm³ total |
| C with original selected P04 |27 /351|207 exact checks|PASS, no overlap; outward withdrawal remains free |
| B with named L/U-v2 proposals |27 /351|207 exact staged checks|PASS_CAD_CONDITIONAL, CR_REQUIRED |
| C with named L-v2/original-U pair |27 /351|207 exact staged checks|PASS_CAD_CONDITIONAL, CR_REQUIRED |

A/C baseline order: Y_FIRST base → bottom-skin envelope → L → U → six radial inward100mm
rib moves. Conditional B/C order: base → skin envelope → L → six ribs vertically down64mm
→ U. B's failed original route is not represented as an executable full sequence: later
counterfactual checks cannot repair its invalid starting geometry. The four valid routes
supply828 continuous comparisons; B's207 rejected trial comparisons remain separately
labelled. These and the1,755 final scenario pairs are nested evidence, not extra unique tests.

All five GLBs contain27 real positive-volume watertight nodes, including six instances
of the same master profile at0/60/120/180/240/300 degrees. Inverse-rotated rib vertices are
inside the actual master cut polygon at6mm tangential thickness. Applied node transforms,
metre-to-mm bounds and volumes agree with OCC: maximum bound difference0.0000124mm,
relative volume error below3×10⁻⁶. No skin, wall, tool, lock, fastener or hidden seventh
rib is in the actual model. Proposal disks substitute original disk bodies only in the
explicitly named CR_REQUIRED models; baseline files are exported separately.

| Exported P05 profile | Area mm² | Bounds r /Z mm | Bottom/top geometric skin boundary area mm² |
|---|---:|---|---:|
| A |3328.442583|81..169 /456..494|516.0 /516.0|
| B |3081.444883|82..169 /456..494|454.8 /454.8|
| C |3216.579431|82..169 /456..494|464.4 /510.0|

All three are connected closed profiles without islands, holes, duplicate vertices or
self-intersections. B/C explicitly set the inner edge back1mm inside the provisional
r81..169 envelope. SVG/DXF cut profiles have zero symmetric-difference area at exported
coordinates. Unit/physical-scale checks pass; dimensions/grain annotations are non-cut.
Each part fits project H800×W440 with provisional10mm margins; this is not sheet nesting.
Primary tests also read actual PNG pixels/DPI. Reviewed sections/exploded and actual27-body
images; skin envelopes and proposal substitutions are labelled, including C's unchanged U.

Closed proposal slots preserve all six original tongue holes, NO_HOLE and R95, disk6mm
thickness and Z456..462/480..486. Independent min exterior lands: B L6.248247/U6.748075mm,
C L6.748075mm. Corresponding min tongue-to-web-hole lands:12.919865/13.390421mm. These are
geometric dimensions, not plywood strength thresholds. Free disk face gap18mm, pitch24mm,
core38 and external tabletop budget50mm remain distinct. Tongues still end488, only2mm
above U and6mm below top-skin underside494.

## Retention, contacts and limitations

A/C on original rim-open disks have a collision-free reverse outward path. **No positive
radial restraint** is demonstrated by their unchanged-disc fit. B cannot be evaluated as
a retained original assembly because its starting geometry already overlaps the upper disk.

With the named proposal disks fixed at their Z positions, real swept material rejects
outward/inward and up/down translations. Representative independent results:

| Conditional model | Outward max overlap mm³ | Lift6.4mm max mm³ | Lower6.4mm max mm³ |
|---|---:|---:|---:|
| B, both disks-v2 |244.140087|57.269919|128.148015|
| C, lower-v2/original-U |244.140087|28.589147|138.368537|

The independent outward trial100mm and inward20mm differ from the primary20mm/5mm trials;
both independently cross the same relevant barriers. These are specified-translation
obstructions, **not6DOF locking, structural bearing or positive Z retention of the disks**.
Both still depend on CTB-008. C's actual filleted horizontal stop is r82.4..82.8 at479.6:
only0.4×6=**2.4mm²**, with0.4mm gap to U underside. It is a stress concern, not a load rating.

A's7.6/23.6mm upper/lower head values are rectangular-envelope budgets. Independently
sectioning its actual rounded contour at r81 gives upper material486.4..493 (**6.6mm**) and
lower457..479.6 (**22.6mm**) after R1 outer corners. Both exceed the6mm geometric screening
threshold; the85.8mm radial backbone is unchanged. This distinction must accompany any
minimum-material claim; a CAD land/fillet does not certify stress or fatigue strength.

Independent broadside clearance-zone areas agree with component metadata: A L/U166.914/
141.013mm², B71.445/72.000, C71.859/140.953, both faces combined. Nominal0.2mm side gaps
and unmodelled adhesive mean these are **candidate coating reservations**, not tested
bonded area. Skin boundary length×6 likewise gives contact geometry only. Actual bond
coverage, properties, cure and strength are UNKNOWN/NOT_RUN.

Outer r169 at t±3 gives min curved gap171−sqrt(169²+3²)=**1.973375mm**, versus2mm on axis.
It is air, not glue. Handoff correctly compares flat skin bonding versus future versioned
tabs/skin slots and preserving this air gap versus a versioned near-rim tip/support.
Any real extra support must enter the future BOM; none is hidden here.

## Genuine negative controls and access

The independent actual-material controls detect an uncut38mm rib against the selected U
(64.8mm³),6.8mm ribs against6.4mm slots,5° rib rotation,1mm tangential displacement,
radial insertion through a closed wall and a late upper disk over A's wider head
(80.852mm³). All have positive overlap. Correctly staged B/C upper insertion passes,
whereas vertical rib insertion after their upper disk is installed is blocked.

Six assumedØ4 tool cylinders reach tongue centers from520 down to488.5 with each valid27
body model and top open; a closed top-skin envelope blocks each. These are hypothetical
space reservations, not actual retainer/hand/fixture access. Solid top offers no assumed
locking route. Complete skins, wall, ring, locks and fixtures remain absent.

## Findings, corrections and failure accounting

| Observation | Severity / disposition | Verification |
|---|---|---|
| Preliminary C nose475 sketch did not permit its hypothesized lift6.4→outward escape | Design-analysis correction before implementation, not a released-CAD defect | Independent OCC found15.12mm³ upper-disk overlap. Implementer replaced that hypothesis with the explicit captured-step C; final geometry/routes independently pass. |
| Reviewer ran62-case suite before handoff and two CR documents existed | Review sequencing error, corrected |59PASS/3FileNotFoundError retained; ready-document rerun62PASS. No CAD assertion failed. |
| Generic0.002mm chord label did not describe A's inherited quad8 rounded rectangles | MINOR numerical provenance, corrected | A sagittaR1=0.004815mm/R0.8=0.003852mm documented;0.002 field scoped to B/C explicit fillets. No cut geometry changed. |
| Some 3D labels clipped and C section caption implied two revised disks | MINOR presentation, corrected | Review images reframed; physical1:1cut PNG scale preserved; C now explicitly L-v2/original U. |
| A head envelope budgets versus actual rounded inner-edge spans | MINOR dimensional clarification, corrected | Source/export metadata, handoff and review now distinguish6.6/22.6mm actual edge spans from7.6/23.6 envelope budgets; independent contour measurement agrees. No geometry/fit/screen failure. |

Initial and enriched final independent OCC audits both passed all final scenarios and
negative controls; no OCC assertion failure occurred. Extra derived areas/lands and the
Git-based259-file integrity check were added to the enriched reviewer run. No final
unexpected nominal geometry/path/export failure or unreported in-scope critical blocker
was found. Expected BLOCKED alternatives/controls remain explicitly distinct from PASS.

## Independent score and gate disposition

| Area | Maximum | Awarded | Evidence / limit |
|---|---:|---:|---|
| Contract and traceability |20|20| Selected authorities,259 byte-preserved sources, explicit provisional changes and named unapproved disk CRs. |
| CAD geometry/export integrity |25|25| Actual closed exports, alternate OCC solids, five27-node GLBs, finite thickness and all six identical instances. |
| Interfaces and assembly |20|19| Exact full named routes/capture barriers and blocked originals; actual tools/fixtures and generalized rigid-motion retention remain outside the proof. |
| Reproducibility and negative controls |20|18|337 independent cases and alternate-kernel bad cases; primary clean rebuild inspected. Reviewer reused the existing CQ runtime rather than reinstalling optional QA dependencies in a fresh environment. |
| Documentation/visuals/handoff |15|14| Proposed versus approved and unresolved load path clearly separated; dense dimensional captions and minor precision clarifications require attentive review. |
| **Total** |**100**|**96**| G1/bounded local CAD scope only. |

**Score≥90: YES. Unresolved in-scope CRITICAL:0; MAJOR:0.** Remaining caption readability
is optional MINOR; later-gate blockers are preserved, not scored as solved. Recommendation:
**APPROVE_DESIGN_ONLY for engineering-lead consideration**, with A as the compatible-study
choice and B/C available only as explicit CR alternatives. This reviewer does not select
a concept, close interfaces, approve a merge or authorize production.

G1 selection is PENDING. G2a evidence covers the named local routes only. Full G2b remains
BLOCKED/NOT_RUN. **G3 physical and G4 manufacturing are NOT_RUN/NOT_AUTHORIZED**: no actual
stock/kerf, glue/cure, physical insertion/fixtures, load/deflection/stability or calibrated
nesting evidence. B01/IF-12, B02, B06/IF-06/08, B10, B11 and future CTB-007/008/009 work
remain open. Score or zero nominal overlap cannot establish a safe load or cut-ready part.

## Reproduction and evidence

Executed optional reviewer runtime: CadQuery2.7.0/OCP7.8.1.1, Shapely2.1.2, ezdxf1.4.4,
trimesh4.11.2. Core pins/clean setup are recorded in component tests README/validation.

```sh
XDG_CACHE_HOME=/tmp/ctb005-qa-cache /workspace/.venvs/ctb-001/bin/python \
  projects/CTB-01/parts/P05/tests/independent_occ_review.py \
  --output /tmp/ctb005-independent-occ-final-results.json
```

Install optional `parts/P05/src/requirements-qa.txt` when reproducing in another environment.
The runner derives root from its ancestors, requires the recorded baseline Git history and
checks protected files independently even without the pre-task/tmp snapshot. Independent
suite logs, initial3-error attempt, concept-preflight JSON, A edge-span measurement and
final OCC JSON/log should be retained with the project validation record.
