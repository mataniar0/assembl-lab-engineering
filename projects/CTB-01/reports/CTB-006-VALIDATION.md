# CTB-006 validation and failure record

DESIGN_ONLY / CR_REQUIRED. Base c27f722e16668e4ed32cee1c72f5a699b40e504e.
No G2b, measured material fit/kerf, structural/tipping test, G3/G4 or cutting approval.

## Risk-based coverage and exact counts

| Selected suite | Unique cases | PASS | Final FAIL | Scope |
|---|---:|---:|---:|---|
| P06 Tier1 test_ring.py | 42 | 42 | 0 | six global +12 per variant; actual exports, geometry, negative controls, full solids/routes |
| Tier2 test_integration.py | 8 | 8 | 0 | IF09/01/02/14, selected27, Y_FIRST, protected336 hashes, bounded upper interfaces |
| CTB-000 static data smoke | 25 | 25 | 0 | unchanged source validator |
| Import integrity smoke | 15 | 15 | 0 | unchanged inventory/schema/source consistency |
| **Executed unique automatic cases** | **90** | **90** | **0** | repeated reviewer runs do not increase90 |

The complete previous337-case run is NOT_RUN. Of those prior cases,40 static baseline/import
checks ran as bounded smoke; **297 P01–P05 component cases NOT_RUN** (61+52+51+71+62).
Upstream336 files are byte-identical, so no broad rerun is required by Issue15. New42/focused8
are not falsely added to a claimed337 run. Independent alternate-kernel audit is additional
geometric evidence, not an invented unittest case count; see separate reviewer report.

Tier1 was run after the final meaningful geometry revision (actual exterior fillets and C
slot repair). Initial42-case and8-case tests gave41PASS/1FAIL and7PASS/1FAIL respectively;
those assertion defects were repaired and the complete clean selected90-case run passed.
Final-candidate Tier2 is rerun on the committed PR head; exact SHA/result recorded in the PR.
Tracked clean reproduction log and independent source/export digests bind the report to inputs.

## Reproduction

Python3.12.14 in an isolated `/workspace/.venvs/ctb-006`, installed solely through inherited
pinned `src/requirements.txt`. Versions in `tests/logs/environment.json`/`pip-freeze.txt`:
Shapely2.1.2, manifold3d3.3.2, trimesh4.11.2, NumPy2.3.5, SciPy1.17.1, ezdxf1.4.4,
Matplotlib3.10.8, Pillow12.3.0, jsonschema4.26.0. Independent OCC uses requirements-qa.txt.

```sh
python -m venv /workspace/.venvs/ctb-006
/workspace/.venvs/ctb-006/bin/pip install -r projects/CTB-01/parts/P06/src/requirements.txt
PYTHON=/workspace/.venvs/ctb-006/bin/python projects/CTB-01/parts/P06/tests/run_all.sh
# final committed candidate, without rewriting CAD file metadata:
/workspace/.venvs/ctb-006/bin/python -m unittest discover -s projects/CTB-01/parts/P06/tests -p 'test_*.py' -v
/workspace/.venvs/ctb-006/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-006/bin/python tools/check_ctb_baseline.py
```

Runner `set -euo pipefail` preserves generator failure: it never treats prior exports as a
successful regeneration. DXF contains timestamps/handles, so rebuild equivalence is checked
semantically through actual closed loop coordinates, not a misleading whole-DXF byte assertion.
Source coordinates round6decimals on cut exports; Hausdorff tolerance1e-6mm. GLB uses metres,
positive watertight meshes, float32 bounds tolerance4e-5mm/relative volume1e-5. Full material
Manifold/OCC collision epsilon1e-6mm³; nominal B maximum≈3.503e-8 is below that epsilon.
PNG artboard exactly mm×96/25.4, integer raster rounding≤1pixel; SVG dimensions in mm.

## Unexpected failures, repairs and retests

| ID | Observed failure or reviewer finding | Correction | Retest / boundary |
|---|---|---|---|
| F01 | Initial C ring/key maximum0.022487934mm³ due to real R0.4 concave key-head fillet | C hole outert19.9→20.3; tab26→26.5 keeps6.2 land | all34-body pairs and complete early path belowepsilon; old geometry deliberately reproduced by test |
| F02 | First generator raised KeyError start_offset_mm while making stage text | use actual step keys start/end_offset_xyz_mm | complete generation2/3 and clean regeneration completed |
| F03 | Tier1 test required B assembled union MultiPolygon; it is Polygon because separate parts meet at boundaries | test each part connected, pairwise area overlap≤tol and union area=sum | same meaningful case passes; separate finite BOM solids retained |
| F04 | IF14 exact float equality1295.9999999999998 !=1296 | numeric tolerance1e-6mm² | footprint/hull unchanged; focused8 pass |
| R01 | Independent reviewer found intended triangle core arcs swallowed by arms | real outer convex0.5mm fillets added to all rings; input/schema/export updated | clean42 + alternate-kernel rerun on final contours |
| R02 | A section caption incorrectly mentioned C keys | conditional A/B/C caption | inspected final sections; no hidden A keys |
| R03 | B entry endpoint metadata showedzero despite raised entry plane | endpoint now[0,0,6.4] before separate lower stage | explicit motion test and staged visual |

Four observed execution failure conditions were repaired, plus three source/visual review
corrections. No unexpected nominal geometry failure remains in the conditional study scope.
Original-cheek incompatibility, A/C tested late routes, free release directions and unapproved
CRs remain deliberately BLOCKED/OPEN, not silently relabelled PASS. Reviewer-side numerical
sweep construction failure/repair is recorded separately in independent QA, not hidden here.
Initial logs are retained under `tests/logs/initial-*`; clean pass in `clean-build-and-tier2.log`.

## Motion matrices and negative controls

Conditional final bodies A28/B36/C34; all378/630/561 unique final pairs belowepsilon.
A early28 stages/406 comparisons; C early34/595. B no-ring early28/378 then post27
12/363; source Y_FIRST18/171 separately checked. These comparisons are not extra test cases.
Full-solid linear translation sweeps, including exact filled sweep of each hole boundary,
are checked against all prior fixed materials. Fixture design/initial support remains OPEN.

Negative controls: original uncut-for-ring cheeks clash in all6 positions; shrinking each proposed cut by0.3mm creates actual interference; S3 hypothetical245
clashes while actual200 stays clear; 2mm tab misregistration, Z+12 and5° out-of-plane collide;
missing tongue changes validated geometry and loses one intended engagement; missing C keeper
permits outward-t withdrawal. Invalid neck, material thickness6.8, sheet orientation, angles
and fake kerf measurements are schema-rejected. A/C thickness6.8 also collides; **B6.8 remains
geometrically clear inside its intentionally taller loading channel**, so B wrong-stock rejection
comes from the contract/schema, not a fabricated collision. A/C after-closure vertical/radial
trials are BLOCKED; no claim about all conceivable rotational approaches. Free C uplift and
B key withdrawal explicitly remain OPEN; no6DOF lock is certified.

## Tier3 and later gates

Only workflow currently present is `.github/workflows/playbook-validation.yml`, with selected
push/PR/manual triggers, no scheduled CAD suite. **NIGHTLY_REGRESSION_NOT_CONFIGURED**:
tracked separately in [Issue20](https://github.com/mataniar0/assembl-lab-engineering/issues/20).
No hosted successful nightly run is claimed. Implement/verify that infrastructure separately;
broad regression also required before G2b/G3/G4 or upstream/shared geometry changes.

No actual stock thickness, kerf, coupon, glue/cure, fixture, friction, loads, bearing, stress,
bending, deflection, fatigue or physical stability tests: **NOT_RUN**. Land/footprint/CAD fit
are geometry evidence only. B01–B13 official records and G3/G4 holds are preserved.


## Branch synchronization and environment reuse

Before submission, main advanced to11be8b370d4d7746a6f5501e2944cadd6e63a39a through an
unrelated MEB-01 change. The existing task branch was fast-forwarded before its P06 commit;
CTB-01, AGENTS and engineering-process inputs remained identical to the c27f722 baseline.
No unrelated project files are changed in the P06 PR.

Cloud setup/start draft saved for reuse: install P05 dependencies on main and P06 when
present, use the isolated P06 runtime/risk-based90 checks, retain no-auto-merge and gate
limits. Draft save does not apply/publish settings; environment settings require review/save
then Publish. Repository membership, secrets and network policy were not changed.
