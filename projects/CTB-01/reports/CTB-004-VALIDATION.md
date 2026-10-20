# CTB-004 validation and repair record

2026-10-20. **DESIGN_ONLY**. Source base f49e3b3be73b7d474302823cc9072148319c8f67.

## Final executed result

Fresh isolated Python3.12 environment `/workspace/.venvs/ctb-004`, no system site packages,
installed inherited pinned requirements. `pip check`: no broken requirements.
Fail-fast generator and all-suite runner completed with exit0. **275 unique checks passed,
zero final failures, zero skips/disabled tests:**

| Suite | Executed unique checks | Final result |
|---|---:|---|
| New P04 geometry/artifacts/paths/negative controls | 71 | PASS |
| P03 selected/Y alternatives regression | 51 | PASS |
| P02 spacer regression | 52 | PASS |
| P01 outline regression | 61 | PASS |
| Unchanged CTB-000 source validator | 25 | PASS |
| CTB-000 import/integrity | 15 | PASS |
| Total | 275 | PASS |

Command: `CTB_PYTHON=/workspace/.venvs/ctb-004/bin/python bash projects/CTB-01/parts/P04/tests/run_all.sh`.
Raw complete log: [clean reproduction](CTB-004-logs/clean-reproduction-all-suites.log).
The runner uses `set -euo pipefail`; no testing old files after failed generation.
Core pins: Shapely2.1.2, manifold3d3.3.2, trimesh4.11.2, SciPy1.17.1, NumPy2.3.5,
ezdxf1.4.4, Matplotlib3.10.8, Pillow12.3.0, jsonschema4.26.0. No service process needed.

Independent second agent separately executed275 unique checks and reconstructed actual
exports in OpenCASCADE; see [independent QA](CTB-004-INDEPENDENT-QA.md) and its script/results.
Independent reruns are **not added again** to the275 total.

## Detailed nominal evidence (nested predicates, not extra unique tests)

Per A/B/C:21 real manifold/watertight solids,210 actual final pairs; six non-BOM matching
web witnesses and141 additional static pairs; all overlaps below1e-6mm³. Manifold nominal
maximum actual overlap2.14e-14mm³, zero witness overlap. Continuous skin/L/U sweeps check
19+20+21=60 prior solids; conditional web route168 sweeps, maximum0. Upstream Y-first
proof18 moving stages/171 comparisons preserved unchanged. All six tongue footprints and
finite6mm thickness align in both disk layers. Each disk is one connected planar material
with six separate tongue holes and six web interfaces; lower/upper are distinct.

DXF unitmm, closed CUT_* paths and non-cut dimension layer agree with SVG polygons and
JSON. Physical SVG1:1, PNG96dpi with actual cut pixels checked. GLB has exactly21 nodes,
metre units, watertight positive volumes and bounds consistent with mm source. Single
part fits portrait H800×W440 with provisional10mm margin. No physical nesting.
All174 protected CTB-000/P01/P02/P03 files byte-equal reviewed base commit.

## Failures, corrections and execution cycles

Three complete generator runs: initial; clean isolated after repairs; final after adding
core/layer-stack illustration. Three primary P04 suite executions: initial49PASS/22FAIL,
repair71PASS, final71PASS plus204 upstreamPASS. No required failure left unexplained.

| Initial problem | Affected cases / evidence | Correction and final evidence |
|---|---|---|
| Rounded export coordinates vs overly small fixed area threshold | 6 planar tests: symmetric difference0.000191..0.000209mm² exceeded1e-4 | No material geometry change. Enforce Hausdorff<1e-6mm plus perimeter×sqrt(2)×0.5e-6 area bound from six-decimal coordinate rounding; all6 pass |
| GEOS difference with a point reported tiny nonzero/negative removed area for NO_HOLE | 6 center tests, residual−3.27e-11..+3.64e-12mm² | NO_HOLE explicitly preserves original material; removed area exactly0; all6 pass |
| DXF nominal-diameter test found only notched X-envelope dimension | 4 DXF tests A/C: actual X envelopes A189.890/C189.945 vs nominalØ190 | Preserve true X-envelope dimension and add explicit190.000mm nominal-diameter annotation on NOT_CUT_DIMENSIONS; all6 DXF cases pass |
| Raster contours too faint at96dpi | 6 PNG tests: only403..425 pixels below100 with0.4pt stroke | Increase PNG stroke to0.8pt and SVG display stroke0.2mm; preserve exact paths. Ink-count and sampled path pixel checks pass |
| Bottom-skin section illustration hatched material across tongue slot | Visual inspection found mismatch despite correct skin solid/sweeps | Plot actual prospective skin cross-section including holes instead of full rectangle; all3 layouts regenerated and inspected |
| First test process attempted cache under unwritable home; CSV handle warning | Non-failing runtime warnings in initial log | Set XDG_CACHE_HOME=/tmp/ctb-cache, MPLCONFIGDIR=/tmp/ctb-mpl; close CSV with context manager; clean reruns |

Raw initial [71-case output with22failures](CTB-004-logs/tests-initial-22-failures.log),
[repair output](CTB-004-logs/tests-repair1.log), initial/clean generation summaries and final
full runner output are retained in CTB-004-logs. No failures were hidden by skipping tests
or changing approved dimensions. Independent review harness corrections are documented
separately in its QA report; they are distinct from primary product/export corrections.

## Deliberate invalid controls and blocked routes

These are expected rejections, **not unexplained suite failures**. Each A/B/C detects:
rotated disk10° (~5184mm³ tongue interference); missing one tongue slot864mm³;
6.6mm tongue against6.2slot57.6mm³; misplaced web cuts5° positive clash;
uncut38mm web positive clash. Incorrect24mm freegap violates U480..486 and leaves2/6mm
engagement even if otherwise collision-free. Radius190 is rejected asØ380 vsØ190.

Reverse U→L, late bottom skin, U-after-OPEN, RAIL-after-U and radial OPEN after wall closure
have actual positive swept intersections in connections-and-paths.json. No general claim
about every possible rotation is made. AssumedØ4 top access with matching webs passes
only with top open; the closed top-skin envelope obstructs it.

## Unrun/unverified and open decisions

No physical material/kerf, insertion force, fixtures/hands, glue/cure, positive retainer,
structural loads, deflection, stability, bending or manufacturing trials were performed.
Stock/kerf remain null. A is a recommendation, not selected design. C's upperØ24 aperture
is hypothetical only; B13 remains open. B01/IF-12 lock, B06/P05 topology/strength,
IF-08 load path, actual skins/rim and whole-system assembly remain open. Witnesses and
skin/wall/tool studies are reservations;21 real bodies do not make a finished50mm tabletop.
No merge, physical cut approval, G2/G3 or load rating is given.
