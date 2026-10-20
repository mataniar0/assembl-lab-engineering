# CTB-006 — independent risk-based CAD QA

2026-10-20. Issue #15, branch `codex/ctb-006-ring`.
Reviewer: `/root/ctb006_qa`, separate from the implementing agent.
Approved upstream baseline: `c27f722e16668e4ed32cee1c72f5a699b40e504e`.
**PASS for bounded G1 DESIGN_ONLY alternatives and specified G2a nominal paths only.**
Score **96/100**, unresolved in-scope CRITICAL **0**, MAJOR **0**.
Lead selection and all proposed P01 changes remain pending. This is not merge permission,
whole-table integration approval, structural evidence or physical cutting authorization.

## Independence, authorities and unchanged inputs

Read Issue15, root AGENTS, the local product-engineering skill, playbook/gates/QA policy,
CTB-000 v0.2 parameters/interfaces/specification/decisions/blockers, STATUS, selected
SOFT_CURVE, B_THROUGH_ADHESIVE, A_COMPACT_CLOSED/Y_FIRST, P04 A_RIM_OPEN/NO_HOLE and
P05 A_RELIEVED_BOND. Reviewed actual jointed P03 cheek exports, not the old V-leg or
pre-mortise illustration. IF-09 is primary; IF-01/02/14 are the focused dependencies.

Captured an independent pre-work SHA-256 inventory of **336 CTB-000/P01–P05 files**;
the final runner separately verifies every file byte-for-byte with the approved Git base.
All336 match. Original CAD, selections and contracts remain unchanged. New P01 cuts are
P06-local `P01-ring-interface-study-v1` proposals, explicitly NOT_APPROVED/CR_REQUIRED.
Frozen H500, topØ350×50, six6mm cheeks,15mm gap, three120° axes and H800×W440 portrait
stock are preserved. Ring6mm, centre245 and its geometry remain provisional study inputs.

The reviewer owns only the independent runner/report and its evidence. Geometry, primary
tests and repairs were performed by the implementer. `independent_occ_review.py` imports
**no component implementation model**. It parses regenerated SVG/DXF cut loops, constructs
finite material with CadQuery/OpenCASCADE, and compares actual GLB nodes. Primary CAD
uses Manifold. Read-only source and documentation review supplements this separate proof.

## Executed scope and exact test counts

| Suite | Unique cases | Final result | Execution/evidence |
|---|---:|---|---|
| New P06 Tier1 |42|42 PASS|independently executed in clean CTB006 core runtime |
| Focused IF09/01/02/14 integration |8|8 PASS|independently executed; includes336 hashes, selected27 and Y_FIRST |
| CTB-000 data smoke |25|25 PASS|implementer's clean-run log independently inspected |
| Import/inventory smoke |15|15 PASS|implementer's clean-run log independently inspected |
| **Selected unique automatic cases** |**90**|**90 PASS,0 final FAIL**|repeat runs do not add cases |

The complete previous337-case suite is **NOT_RUN**. Its40 baseline/import cases were
selected as bounded smoke; the unaffected **297 P01–P05 component cases NOT_RUN** are
61+52+51+71+62. This follows Issue15's mandatory risk-based plan because all336 upstream
files are unchanged. The independent OCC matrices below are additional geometric evidence,
not invented unittest case counts. No test disabling or tolerance relaxation concealed a
real nominal part collision.

## Alternate-kernel geometry, paths and exports

Independent original27-body reconstruction: **351 static pairs, zero overlap**. Original
Y_FIRST:18 moving stages/**171 exact continuous checks, zero overlap**. Four spacers per
leg remain35/90/**200**/390, including the lower reinforced part and all finite tabs.

| Conditional proposed-cheek model | Real bodies / static pairs | Independently swept changed-interface route | Result |
|---|---|---|---|
| A |28 /378|ring fixed → Y down113 →18 Y_FIRST pieces;19 stages/190 comparisons|PASS;0 overlap |
| B |36 /630|closed27 →3 raised tangential entries/downward drops →6 wood stops;12 stages/363 comparisons|PASS;0 overlap |
| C |34 /561|ring fixed → Y →18 Y_FIRST pieces →6 vertical keys;25 stages/325 comparisons|PASS;0 overlap |

All1,569 conditional final pairs have zero positive overlap in OCC. These critical routes
provide878 continuous comparisons. The unchanged selected upper27 geometry is included in
each final model and in B's late route. Primary full early paths additionally cover the
skin reservation, disks and P05 continuation: A28/406, B no-ring28/378, C34/595. The
independent bounded ring-first routes stop after the affected lower interfaces; they do
not claim a separate rerun of every unchanged upper-component route.

Sweeps are endpoint profiles plus every translated boundary-edge prism, with finite6mm
material, not sampled frames. B entries occur at+6.4mm before lowering6.4; endpoint metadata
preserves that raised plane. A/C require externally holding the initial ring; fixture
design/handling is OPEN and no fixture is hidden in the CAD/BOM. A/C tested late downward
and radial60 routes are genuinely BLOCKED, despite clean final placement. This proves
those routes blocked, not every conceivable rigid-body motion impossible.

All six original selected P01 cheeks collide with each alternative's ring. Conditional
fits rely on the named proposals, and do not establish backward compatibility. All six
proposed cheeks preserve external profiles, floor interfaces and existing spacer/Y holes.
Exact original-P01 collision values and all route pair results are retained in the JSON.

All actual cut profiles are connected valid polygons, with closed unique DXF polylines,
no self-crossings/orphan retained islands, SVG/DXF symmetric-difference area zero and
DXF units4/mm. Inner loops are waste to remove. Actual outer convex0.5mm fillets survive
in the final exports. Every standalone cut part fits W440×H800 with10mm provisional
margins; **production nesting remains NOT_RUN**. Primary tests independently rerun by
this reviewer verify PNG physical-size/DPI parity and non-cut dimension layers.

Three GLBs contain exactly28/36/34 real positive-volume watertight nodes. Finite ring
pieces/keys replace no hidden hardware: A1, B3+6, C1+6 added bodies. Six proposal cheeks
substitute the six original cheeks in explicitly conditional models. No skin, fixture,
tool or retainer is silently added. Metre-to-mm transformed bounds agree with OCC within
**0.000012398mm**; maximum relative volume discrepancy **2.960×10⁻⁶**. Export SHA-256
inventory binds26 actual SVG/DXF/GLB artifacts in `assembly/independent-occ-review.json`.

## Derived interfaces, retention and physical limits

Actual slab242..248 has ring-level common cheek radial interval86.498761..137.534325.
The expanded proposed cutout241.8..248.2 gives86.598678..137.436614 and joint centre
**112.017646mm**. Core outer radius71.389534 stays12mm inside the minimum inner edge
over that expanded band. Export-derived arm width14.6 leaves nominal0.2 per inner cheek.
Independent outer radial cheek lands are A/B19.218968 and C12.218968mm. B splice radial
lands are6.7999995/6.7999992mm; C keyslot outer lands6.2mm. These are geometric screens,
not plywood stress limits.

Actual S3 Z197..203 has0 overlap with every P06 family. Slab face gap is39mm, but the
complete family gap is **A39/B35.8/C32mm** because B stops reach238.8 and C keys235.
Y407..413 remains clear. Hypothetical S3 at245, mapped to the ring-level cheek station,
clashes independently by2730.957mm³ for A/B and3809.794mm³ for C. The old conflict is
not hidden by deleting/moving any of the12 selected spacer bodies.

Isolated ring/key checks exclude Y/spacer restraints: every cheek's radial±4 translation
is obstructed in all three models. A/B outward-t spreading remains FREE. C outward-t
is obstructed only with its keys fixed; removing keys restores the free route in all six
positions. **C key uplift and B stop-key transverse ejection remain FREE**, independently
swept against the complete remaining assembly. No6DOF retention or solved mechanical
capture is claimed. C's actual R0.4 lower head seat at Z248 bears only over t20.3..21.6:
**1.3×6=7.8mm² per key**. The nominal6mm neck has5.2mm terminal flat after corner fillets.
Seat stress, retention and material adequacy are UNKNOWN; C is only a further-study choice.

Six actual floor patches are r222..258×6mm:216mm² each, total1296. The R240 module-centre
triangle has inradius120; the full six-foot convex hull minimum centre-to-edge distance is
**140.691343mm**, below top radius175. This distinction is retained. No mass, load case,
friction or centre-of-gravity evidence exists; no stability, tip-proof or load rating follows.

## Failures, corrections and retests

| Observation | Disposition and retained evidence |
|---|---|
| Real initial C ring/key fillet clash0.022487934mm³ | implementer enlarged hole outert19.9→20.3 and tab26→26.5; old collision remains a deliberate test; final actual OCC geometry/routes PASS |
| Generator KeyError `start_offset_mm` | actual step field names used; complete regeneration succeeds; initial error log retained |
| Tier1 assembled-B union expected MultiPolygon (41/42 PASS) | corrected invalid test assumption: separately connected bodies may share boundaries; independent pairwise material overlap/area checks and all42 now PASS |
| IF14 exact floating equality (7/8 PASS) | numeric tolerance replaces1295.9999999999998==1296; all8 PASS, footprint unchanged |
| Rounded core arcs swallowed by arms in first A contour | reviewer challenged source-intent-only rounding; real outer0.5 fillets added, source/schema/exports regenerated; final audit PASS |
| A section caption mentioned C keys; raised B endpoint metadata misleading | conditional caption and explicit raised endpoint corrected; final views/test evidence inspected |
| Reviewer OCC `Standard_NullObject` while extruding B3 generated sweep | quantified one numerical hole area2.524354896707238×10⁻²⁸mm², minimum edge2.13×10⁻¹⁴mm. Only generated-sweep holes below10⁻¹⁴mm² are removed and area delta recorded. **No actual exported profile is filtered.** Full final OCC rerun A/B/C PASS; first traceback retained |

Four primary execution failure conditions plus one reviewer construction error were
corrected, and source/visual review corrections are recorded separately. An earlier OCC
attempt was deliberately stopped when the implementer revised the actual fillets; it was
not scored as PASS or a CAD failure. No final unexpected nominal geometry/path/export
failure remains. Expected BLOCKED originals/routes and OPEN retention are preserved.

## Independent score and gates

| Dimension | Maximum | Awarded | Evidence/limit |
|---|---:|---:|---|
| Contract/traceability |20|20|authorities,336 unchanged files, provisional inputs and explicit CRs |
| Geometry/CAD/export integrity |25|25|actual cut loops, independent OCC, all real GLB bodies, finite keys/splices |
| Interfaces/assembly |20|19|continuous named routes, blocked originals and all-six coupling; real handling/fixtures unresolved |
| Reproducibility/controls |20|18|50 independently executed cases,40 inspected smoke, clean primary rebuild; existing optional OCC runtime reused and bounded numerical sweep handling disclosed |
| Documentation/visuals/handoff |15|14|scope and failed routes clear; staged text images remain dense |
| **Total** |**100**|**96**|bounded DESIGN_ONLY study only |

**QA≥90: YES; in-scope CRITICAL0/MAJOR0.** Recommend engineering-lead consideration of
the bounded study PR, with C available for further conditional retention development.
This reviewer does not select a concept, approve a P01 CR, close IF-09/B05, merge, or
authorize physical cutting. B01–B13 and all official interface states remain preserved;
P05 outward retention is still OPEN. Complete G2b, physical G3 and manufacturing G4 remain
NOT_APPROVED/NOT_RUN. Measured stock/kerf, glue/cure, fixtures, bearing, stress, bending,
deflection, fatigue, friction and physical stability have no test evidence.

No scheduled CAD regression workflow or successful nightly run exists:
**NIGHTLY_REGRESSION_NOT_CONFIGURED**, tracked separately in
[Issue20](https://github.com/mataniar0/assembl-lab-engineering/issues/20). The missing
unrelated pipeline does not turn this risk-based component study into a false broad-suite
PASS, nor require a needless337-case rerun for unchanged upstream artifacts.

## Reproduction and evidence

Reviewer core runtime: isolated CTB006 Python3.12.14; versions in `tests/logs/environment.json`.
Alternate CAD runtime: CadQuery2.7.0/OCP7.8.1.1, Shapely2.1.2, ezdxf1.4.4, trimesh4.11.2;
optional dependencies in `src/requirements-qa.txt`.

```sh
/workspace/.venvs/ctb-006/bin/python projects/CTB-01/parts/P06/tests/test_ring.py
/workspace/.venvs/ctb-006/bin/python projects/CTB-01/parts/P06/tests/test_integration.py
XDG_CACHE_HOME=/tmp/ctb006-qa-cache /workspace/.venvs/ctb-001/bin/python \
  projects/CTB-01/parts/P06/tests/independent_occ_review.py \
  --output projects/CTB-01/parts/P06/assembly/independent-occ-review.json
```

Retained: `tests/logs/independent-tier1.log`, `independent-tier2.log`,
`independent-occ-review.log`, `independent-occ-first-NullObject.log`,
`independent-upstream-baseline.json`, `independent-protected-before.json`, initial primary
failure logs and clean rebuild log. Final JSON retains matrices/routes, negative controls,
six-cheek restraints, keeper ejection, lands, GLB parity, numerical repair and26 export
hashes. The runner independently checks Git-base bytes without relying on `/tmp` snapshots.

## Final assertion expansion review

Before commit, the implementer strengthened six existing cases without changing geometry
or increasing the42-case count. The three `bom_glb` cases now compare `BOM-v1.csv` IDs,
quantities, nominal6mm thickness and DESIGN_ONLY release with actual exported cut parts.
The three `negatives` cases shrink each proposed cut inward0.3mm and demonstrate positive
real-material interference against its ring/keys, explicitly detecting insufficient
clearance for A/B/C. This reviewer independently executed these six targeted cases:
**6/6 PASS**, in `tests/logs/independent-expanded-six.log`. They are reruns within the
existing42, not six additional unique tests. Rechecked all26 reviewed export SHA-256s:
unchanged, so no repeat OCC sweep run was warranted. Score96/100 and gate limits remain.
