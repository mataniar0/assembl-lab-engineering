# CTB-005 validation, failures and corrections

2026-10-20. **DESIGN_ONLY**. Approved source base:
`6292a0e22c9aacade5aa7c7995332494aa8de005`.

A fresh isolated Python 3.12 venv at `/workspace/.venvs/ctb-005` excludes system packages.
Pinned dependencies installed successfully; `pip check` reported no broken requirements.
The full fail-fast reproduction runner completed with exit 0.

| Executed suite | Unique cases | PASS | FAIL | Skipped |
|---|---:|---:|---:|---:|
| New P05 |62|62|0|0|
| P04 |71|71|0|0|
| P03 |51|51|0|0|
| P02 |52|52|0|0|
| P01 |61|61|0|0|
| CTB-000 contract |25|25|0|0|
| CTB-000 import |15|15|0|0|
| **Total** |**337**|**337**|**0**|**0**|

Executed command:
`CTB_PYTHON=/workspace/.venvs/ctb-005/bin/python bash projects/CTB-01/parts/P05/tests/run_all.sh`.
The complete log is `CTB-005-logs/clean-full-run.log`. Final cap-metric metadata changes
were regenerated and all 62 affected P05 checks rerun successfully; the unchanged 275
upstream cases had already completed. Both final component and full-run logs are retained.
No disabled/skipped/expected-failure unit cases. A passing negative-control assertion does
not make its deliberately invalid assembly feasible.

Core versions: Shapely 2.1.2, Manifold 3.3.2, NumPy 2.3.5, SciPy 1.17.1, trimesh 4.11.2,
ezdxf 1.4.4, Matplotlib 3.10.8, Pillow 12.3.0, jsonschema 4.26.0. No services needed.
A separate agent independently executed 337 checks and reconstructed actual exports in
CadQuery 2.7.0 / OpenCASCADE. See `CTB-005-INDEPENDENT-QA.md` for score, scope and logs.
Reruns and nested comparisons are not added to 337. All 259 protected files are unchanged.

## Finite material and continuous paths

The reviewed 21-body base matches the selected P04 A GLB. Exactly six identical P05 bodies
produce 27 bodies and 351 static pairs per model. A/C with original disks have maximum
intersection 2.14e-14 mm³. B has six original-upper-disk clashes of 28.8 mm³ each, 172.8
in total: **BLOCKED_BASELINE**. Separate B/C disk proposals have maximum 2.14e-14 mm³.
Individual solids are valid/watertight and positive-volume. Five GLBs each have 27 nodes;
metre scale, bounds, volumes and identical inverse-rotated rib instances are checked.

Each complete skin/disk/rib route has 207 exact swept/prior-body comparisons. Original A/C
radial routes and proposed B/C staged vertical routes pass with zero overlap. B's original
route remains blocked. The earlier Y_FIRST 18-stage/171-comparison path is re-executed.
Skin, wall and tool studies remain non-BOM reservations, never complete product geometry.

DXF/SVG closed material, physical millimetre scale, PNG pixels/DPI/hash and matching disk
interfaces are checked. Proposal slot/tongue geometry preserves fixed dimensions and
NO_HOLE, but **CR_REQUIRED / NOT_APPROVED** remains explicit. Single-part H800×W440
screening includes provisional 10 mm margins; no production nesting was performed.

## Observed failures, corrections and cycles

Three primary generator runs and three test cycles: initial generation/62 PASS; clean
fresh generation/337 PASS; final metadata clarification/generation/62 PASS. No unexplained
primary unit failure. Two presentation/provenance/metric correction cycles followed the
initial passing run. Independent readiness and concept probes are accounted separately.

| Observation | Cause / evidence | Correction or disposition | Recheck |
|---|---|---|---|
| Preliminary C escape hypothesis failed | A preliminary nose ending at Z475 collides 15.12 mm³ with U during a 6.4 mm lift; ending it at472 would allow escape | Rejected the escape claim before final geometry. Deliberately designed the final upper step to oppose lifting | Proposed C fit/path pass; upward trial blocks 28.589 mm³ |
| B original fit fails | Full-height rail r82..88 crosses selected U material at r82..82.8 | Explicitly BLOCKED; no silent P04 edit. Separate CR B disk pair | Six 28.8 mm³ clashes reproduced; proposal fit/path pass |
| Open interfaces do not capture outward motion | The reverse of a feasible radial insertion is free | A/C original withdrawal remains FREE. Capture claims use only separately labelled proposals | Exact outward sweeps: zero original A/C, positive proposed B/C |
| Reviewer tested before documents were ready | 59 PASS +3 ERROR: handoff and two CR Markdown files absent | Completed documents and preserved the incomplete-delivery log | Independent 62 PASS; total337 PASS |
| Chord parameter scope was unclear | 0.002 applies to B/C explicit fillets, not A's quad8 arcs | Renamed parameter and recorded actual A sagitta0.004815/0.003852 | Shape unchanged; clean reproduction passes |
| Drawing labels/clipping | Skin labels outside t10.5 view; C caption did not identify original U; some outer 3D labels clipped | Moved labels, specified L-v2/original U, tight bounding box for review images only | Regenerated and inspected; 1:1 cut images retain their physical scale |
| Rounded-slot land precision | CR text quoted old rectangular approximations6.24/6.74 | Use measured rounded-cut lands6.248/6.748 | Independent DXF/SVG measurement; shape unchanged |
| Runtime-version reporting probe | System Python has no Shapely package metadata; wrong interpreter selected for this reporting command | Retried with verified ctb-005 venv; environment.json records actual runtime | Success; no CAD/test result affected; runtime-metadata-probe.json retains the observation |
| Actual cap edge omitted outer corner radius | A's7.6/23.6 envelope budgets do not equal edge spans after R1 corners | Added actual r81 edge spans6.6/22.6, retaining envelope budgets | Independently intersected geometry; regenerated metadata and62 checks pass |

No approved source was edited to satisfy a test. Preliminary concept collisions are not
presented as failures of a selected production design. Logs preserve initial and final
attempts, including the reviewer's three sequencing errors. No physical test was invented.

## Negative controls and retained holds

Uncut 38 mm ribs clash; 6.8 mm material exceeds W6.4 slots; 5° rotation clashes; closed wall
blocks radial insertion; lower-after-upper and late bottom-skin installation collide. A's
upper disk after its existing rib head is blocked. Proposed B/C deliberately permit upper
last, so that route is correctly a pass for those proposals. Closed top blocks lifting
and the six assumed Ø4 tool approaches. These are specified translations, not an exhaustive
proof about every rigid rotation or real fixture/hand/adhesive path.

B's original starting assembly is invalid, so retention is NOT_EVALUATED there. With the
proposed disks fixed, B/C in/out/up/down sweeps collide; this is neither 6DOF nor strength
proof. Schema controls reject zero/non6 thickness, count3, invented measured kerf and
incorrect core height. Geometry screens do not certify C's tiny2.4 mm² stop.

G1 lead selection is pending. Whole-product G2b is NOT_RUN/BLOCKED. Material, kerf, glue,
fixtures, physical assembly, loads and stability at G3 are NOT_RUN. G4 production, calibrated
nesting and physical cutting are NOT_AUTHORIZED. B01/B02/B06/B10/B11 and dependent
IF-06/07/08/12 claims remain open, including real disk Z restraint and skin/rim load paths.
