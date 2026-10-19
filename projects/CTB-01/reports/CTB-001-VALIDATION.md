# CTB-001 validation record — DESIGN_ONLY

## Reproducible workflow

Full install/generate/check commands: `../parts/P01/tests/README.md`.
Python3.12.14, Shapely2.1.2, ezdxf1.4.4, NumPy2.3.5, Matplotlib3.10.8,
Pillow12.3.0, jsonschema4.26.0. Pinned requirements are in P01/src.
Run from repository root; writeable caches `XDG_CACHE_HOME=/tmp/ctb-cache` and
`MPLCONFIGDIR=/tmp/ctb-mpl` avoid read-only home/cache warnings.

```sh
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P01/src/generate.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P01/tests/test_geometry.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-001/bin/python tools/check_ctb_baseline.py
```

## Executed results

| Cycle / scope | Cases run | Passed | Failed | Disposition |
|---|---:|---:|---:|---|
| P01 initial, `CTB-001-tests-cycle1.log` | 57 | 53 | 4 | Diagnosed below; not hidden or called PASS |
| P01 repair/retest, `CTB-001-tests-cycle2.log` | 57 | 57 | 0 | Harness correction; contours unchanged |
| P01 QA corrections/retest, `CTB-001-tests-cycle3.log` | 57 | 57 | 0 | Corrected dimension/metadata; added schema and support output |
| P01 final, `CTB-001-tests-final.log` | 61 | 61 | 0 | Added schema rejection + independent support projection checks |
| Clean isolated venv repeatability, `CTB-001-clean-tests.log` | 61 | 61 | 0 | Reinstalled pinned requirements, regenerated exports |
| Final packaging retest, `CTB-001-packaging-tests.log` | 61 | 61 | 0 | SVG formatting normalized; all7 SVGs also parse |
| Unchanged CTB-000 source validator | 25 | 25 | 0 | `CTB-001-baseline-validator.log` |
| Baseline inventory/integrity suite | 15 | 15 | 0 | `CTB-001-baseline-import-checks.log` |

Final selected suites: **101 checks passed, zero failures, zero skipped**.
No physical or integrated mechanical tests ran. They are unrun, not passed/skipped.
A separately installed, isolated venv `/workspace/.venvs/ctb-001-clean` (without
system site packages) installed the pinned requirements and successfully regenerated
all three variants (`CTB-001-clean-generation.log`), then ran61/61 P01 tests with zero
failures (`CTB-001-clean-tests.log`). Source regeneration retained contour/dimensions
identity; DXF timestamps/handles are not required to be byte-identical.

Independent automated QA separately reran61+25+15 checks, all101 passing, inspected
exports and audited reports. See `CTB-001-INDEPENDENT-QA.md`. It found no critical
CAD/data defect after correction of the dimension annotation. This is not a human
engineering-lead G1 decision and does not close any mechanical blocker.

The four development suite cycles were followed by two61-case repeatability runs:
clean-environment and final packaging. These are six primary P01 suite executions
in total, with four initial failed cases corrected and zero failures in subsequent runs. Baseline byte
integrity is also exercised by the P01 suite, so the 101 count describes executed
cases across three suites, not 101 unrelated engineering claims.

## Failures, repairs and engineering corrections

Two functional repair iterations after the initial P01 run, followed by a formatting-only
packaging correction; four development suite cycles plus two repeatability runs. No silhouette/locked dimensions changed in response to failures.

1. Three failures: GEOS returned adjoining LineStrings at z448 shoulder (the union is
   one connected section). Explicit `line_merge` now requires a single joined LineString;
   separated intervals still fail. This corrects a representation-sensitive assertion,
   not a disconnected contour. Erosion, self-intersection and section tests remain active.
2. One failure: a thin antialiased PNG stroke around the FLARED_CURVE r270 extremum had
   grayscale155..184, exceeding the original black threshold150. Raster test now recognizes
   ink below220, still checks actual ink near every vertex, physical DPI/scale and absence
   of stray ink away from the outline. Source/contour did not change.
3. Independent reviewer identified a dimension annotation ambiguity:24 mm was drawn at
   the rounded nose. It now says24 mm nominal, references z480, and explicitly states the
   actual22 mm tip flat. Added an exact22 mm tip-section assertion to all variants.
4. Calculation review corrected disc-edge envelope metadata from naive95−69 to
   `95−hypot(69,13.5)=24.69175` mm, accounting for tangential thickness extent. This is an
   envelope clearance only, not measured slot clearance.
5. Moved ring reservation label to remove overlap with the z245 spacer label. Geometry
   still intentionally reserves overlapping bands, marked OPEN.
6. Repository diff review found Matplotlib-generated trailing blanks in review SVG
   paths. Normalized generated SVG line endings/whitespace in the exporter; coordinate
   values and render geometry remain unchanged. Baseline source was not touched.
7. Initial rendering produced read-only user-cache warnings. Writable /tmp caches resolved
   the setup warnings; no TLS/package verification was disabled.

Three initial construction screens require rejection of invalid inputs: bow-tie contour,
oversized consuming fillets and negative radius schema input. These deliberate negative
controls pass only when the bad input is rejected; they are not geometric model failures.

## Evidence boundaries

Checks cover closure, planarity, connected contour, no intersections/islands, duplicate and
short edges, ≥24 mm sampled body widths, radius6 erosion continuity, ideal corner/curve
radius screen≥1 mm, DXF audit/no repair, true DXF/SVG contour equality, actual PNG pixels
and print scale, six identical inverse-transformed instances, nominal15 mm gap/27 mm
section,120° orientation, bare footprint separation, disc-plane sections, candidate lower
skin allowances, Y mismatch, uncut spacer/ring reservations, ground support projection,
single-part sheet fit, regeneration and unchanged baseline bytes.

A PASS on these tests is not certified machining, plywood strength, fit calibration,
assembly order, positive retention, full 3D joint fit, nesting, bending, tipping, load or
physical verification. IF-02/09 remain BLOCKED; IF-04/05 cannot pass without slot/lock/
assembly evidence. All seven required IF outcomes are in `CTB-001-interface-results.json`.

## Deliverable inventory

- P01/src: `design.json`, `design.schema.json`, `model.py`, `generate.py`, `requirements.txt`.
- P01/variants/{SOFT_CURVE,FLARED_CURVE,GEOMETRIC}: `profile.dxf`, `profile.svg`,
  `profile.png`, `layout.svg`, `layout.png`, `dimensions.json` (six files per alternative).
- P01: `README.md`, `BOM.csv` (P01×6), `FIT-AND-RESERVATIONS.md`, `.gitignore`,
  `comparison.svg`, `comparison.png`.
- P01/tests: `test_geometry.py`, `README.md`.
- reports: interface matrix/results, design review, this validation report, generation log,
  four P01 cycle logs, clean generation/test logs, packaging retest log, two baseline check logs and the
  independent QA report.
- Updated project STATUS. CTB-000 contract, approved dimensions and source files unchanged.

`git diff --cached --check` passes after generated-SVG formatting normalization.

No CTB-002/003/004/006 components or manufacturing nesting files are produced.

## Reusable cloud setup

Saved environment draft fields `install_script` and `start_skill` install the pinned
P01 requirements in `/workspace/.venvs/ctb-001` and record these check/start commands.
No service process is required. Draft persistence does not execute or publish it;
review/save in environment settings and publish to activate future-task configuration.
The current-instance and clean-venv runs above are verified; new-task restoration is not.
