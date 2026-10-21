# CTB007 validation, failures and retests

Source6db45fa7ba0d9a81ff9bbc6d1a432133ab955214, existing branch `codex/ctb-007-skins-rim`.
DESIGN_ONLY, G1geometry/boundedG2a named paths. No physical bending, fit or manufacturing PASS.

## Executed risk-based checks

| Suite | Unique cases | PASS | Final unexpected FAIL | Evidence |
|---|---:|---:|---:|---|
| P07 Tier1 test_skins_rim.py |46|46|0|7global+13per variant; source/exports/material/routes/controls |
| Focused test_integration.py |7|7|0|IF03/07/08/10/11/12,439 upstream hashes,current27 |
| CTB000 static data |25|25|0|unchanged authoritative validator |
| Import/source integrity |15|15|0|unchanged import smoke checker |
| **Executed unique total** |**93**|**93**|**0**|reruns and matrix comparisons not extra cases |

347 unaffected old component cases **NOT_RUN**:297P01–P05 +50P06. The40 static G0/import
cases were selected as bounded smoke, not all prior cases skipped. No mandatory full old
regression run on this unchanged-source component PR. No previous Y_FIRST/leg/floor suite
rerun is falsely claimed; their selected19 and27 bodies are consumed and byte-checked.
Independent reviewer separately repeats53 and uses actual exported contours with OpenCASCADE;
see independent QA. Its geometric pair checks are additional evidence, not invented case counts.

Tier1 first run:45/46 PASS, one C contour-duplicate failure; repaired and all 46 pass.
Focused first7/7 pass. Final clean isolated reproduction:all 53 unittest +25+15=93 PASS.
Three existing stock/web cases were strengthened to measure actual7.2mm midheight webs
and12mm seam margins, not rely on metadata alone; full53 rerun and independent repeats pass.
Final committed candidate Tier2 SHA/result is recorded in PR body after the final head check.

## Clean environment and reproduction

Actual Python3.12.14 isolated `/workspace/.venvs/ctb-007`, inherited pinned dependency chain:
Shapely2.1.2, manifold3d3.3.2, trimesh4.11.2, NumPy2.3.5, SciPy1.17.1, ezdxf1.4.4,
Matplotlib3.10.8, Pillow12.3.0, jsonschema4.26.0. Full versions in tests/logs/environment.json
andpip-freeze.txt. Optional QA requiresCadQuery2.7.0/OCP7.8.1.1; no hidden dependency in core.

```sh
python -m venv /workspace/.venvs/ctb-007
/workspace/.venvs/ctb-007/bin/pip install -r projects/CTB-01/parts/P07/src/requirements.txt
PYTHON=/workspace/.venvs/ctb-007/bin/python projects/CTB-01/parts/P07/tests/run_all.sh
# final committed head: no rewriting DXF timestamp metadata
/workspace/.venvs/ctb-007/bin/python -m unittest discover -s projects/CTB-01/parts/P07/tests -p 'test_*.py' -v
/workspace/.venvs/ctb-007/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-007/bin/python tools/check_ctb_baseline.py
```

Fail-fast runner stops after generator failure, so stale exports cannot produce false clean
regeneration. Source geometry to6decimal cut paths; DXF/SVG Hausdorff tolerance1e−6mm,
actual closed contours/no duplicate cut points, separate dimension layers, unitsmm. Rebuild
DXF equivalence is semantic; native header timestamps can differ. PNGmm×96/25.4 integer
artboards have≤1pixel rounding. GLBmetres/positivewatertight material have≤4e−5mm bound/
1e−5 relative volume tolerances. Bent geometry uses common1deg faceted cylinders, maxsagitta
0.006664mm and mapped-volume error≈5.08e−5 relative to4×flat area. This is a stated ideal
mathematical mapping, not material deformation accuracy.

Manifold collision epsilon1e−6mm³ fixed before trials; nominal final maxima A6.689e−9,
B2.923e−8,C1.768e−7 are below it. Independent kernel reports exact reviewed evidence separately.
Skin/rim boundary contact uses1e−7mm coincidence tolerance to avoid GEOS roundoff losing
collinear clipped edges; it does not bridge the intentional0.2mm gaps or create an adhesive.

## Failure and correction history

| ID | Observed issue | Correction/disposition | Retest/evidence |
|---|---|---|---|
| F01 | First generation GEOSException while rendering empty LineString section withnanbounds | skip empty/zero-length sections before drawing rectangles | complete gen2/gen3 and clean generation pass; traceback retained |
| F02 | FirstTier1 C contours45PASS/1FAIL; clippedtab edge1.745102216888e−12mm produced duplicate6dp point | Cskin topology-preserving simplify1e−9mm before export, eliminating numerical redundant edge | all 46 pass, actual exterior remainsR175-clipped; independent export QA |
| R01 | Initial direct-boundary contact intersection undercounted nominal coincident clipped edges | bounded1e−7 coincidence distance; report boundary geometry only | finalareas and independent alternate distance-method comparison |
| R02 | Initial kerf centres16..L−12 did not guarantee12mm Bstep seam keepout | centres20..L−20, preserving all widths/connectedness | source/export regeneration; measured web/end-margin tests |
| R03 | Exploded rim515..565 visually truncated by oldcrop550 | crop/axes to585 | final full 50mm rim inspected independently |

Two primary executed failure conditions were corrected, plus three implementation/review
corrections; no unexplained final nominal CAD failure. Deliberate blocked assembly orders
were preserved and solved only by different explicitly checked routes, not relabelled PASS.
Initial preflight (including original contact undercount), initial generator/Tier1 logs,
correctedTier1/focused and clean full reproduction logs are retained in P07/tests/logs.
Independent parser/sweep/contact harness failures and numerical repairs are documented separately
by the reviewer, not hidden as successful first attempts or actual-part geometry changes.

Reviewer harness failure detail (actual exported component geometry unchanged):

| Reviewer failure | Correction and retained evidence |
|---|---|
| Legacy upstream P03 SVG has no new CUT group | legacy-root fallback only for old upstream files; new P07 still requires explicit CUT; initial parser traceback retained |
| OCC radial sweep Standard_NullObject |22 generated union-hole artifacts, areas≈1e−28..8e−28mm²; only generated sweep holes below1e−14 removed, actual profiles untouched; diagnostic/first traceback retained |
| C contact area undercount≈127.337mm² | exactly12 partially clipped facet edges dropped by strict whole-edge/1e−7 test; exported normal offset≤5.4343e−7mm, within6dp uncertainty. Independent partial-collinear projection with1e−6mm tolerance recovers contact; existing0.005mm² area agreement criterion unchanged. Final bottom/top deltas<0.0001mm²; C kernel rerun and diagnostics in independent report |

These three reviewer harness failure conditions are additional to the two primary execution
failures. The final reviewed geometry, collision epsilon and structural/physical gate limits
were not relaxed to hide any nominal part defect.

## Final matrices, path trials and controls

A31/B32/C33 actual bodies, final465/496/528 unique pairs nominalclear. Full valid routes
A12stages/294 checks, B13/325(radialrim), C14/357(verticalrim before top). Avertical and
radial pass; Bvertical blocks, Bradial passes; Cradial andclosedtop-first block, Cvertical
before top passes. Aafter toprim trial2/59 passes but six lock-access probes remain blocked
bytop. Actual pre-ring 27, all 12 spacers and original disks/ribs unchanged. No P06 or P08 body.

Negative controls: no bottomholes, undersized tangential slots, wrong inner/outer radius,
bottom after disks, ribs after closed wall, top lowered incorrectly to487, full-height cuts
that disconnect material, missing segment/BOM mismatch, wrong stock orientation/thickness,
false measured kerf and incorrectCtop angular alignment. Six tool probes are clear before
P07T, allblocked after it. Top skin uplift remains FREE in allvariants; no positive skin
retention is inferred. Contact area, area/mapped-volume and cut scale do not prove load transfer.

## Scope retained OPEN

KERF_COUPON_PENDING:4mm through-slot pitch/depth/shape, 50mm bend, neutral axis/springback,
actualstock/kerf/grain, glue/preparation/cure/holding, seam tensile/bearing/creep, smoothfiller/
sanding/finish, structuralstiffness/deflection/strength, load/friction/stability all NOT_RUN.
No actual P08lock/tool/hand/P06 approvedring or complete table sequence. CTB006R Issue23,
B01–B13 and officialIF records remain OPEN/preserved. All prototypes/cutting/G3/G4 NOT_APPROVED.

Only playbook-validation.yml exists; it has no scheduled CAD regression. Issue20 remains
open for separate infrastructure. **NIGHTLY_REGRESSION_NOT_CONFIGURED**, no hosted successful
nightly claimed. Broad regression before full G2b/G3/G4 or actual shared/upstream changes.

Pre-commit hygiene: the first staged `git diff --check` flagged CRLF line endings in the new
BOM CSV as trailing whitespace. Normalized only that new CSV to LF; row values/counts
unchanged. Initial diagnostic is retained in tests/logs/initial-precommit-whitespace.log;
final staged whitespace check passes. This is separate from the two CAD/test failure
conditions and does not add or remove test cases.
