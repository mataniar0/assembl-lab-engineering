# Reproduction and test interpretation

Run `CTB_PYTHON=/workspace/.venvs/ctb-004/bin/python bash projects/CTB-01/parts/P04/tests/run_all.sh`
from the repository. It regenerates P04 first and fails immediately on error, then runs71
P04 cases and204 upstream cases (51 P03 +52 P02 +61 P01 +25 contract +15 import).
No tests are disabled/skipped; nested pairwise checks are not additional unique cases.
Installation pins inherit P03→P02→P01; fresh venv does not use system site packages.
`pip check` and generation/GLB/test runs validate the installed core. No running server.

P04 reads actual DXF cut loops and layers, SVG polygons/physical dimensions, PNG pixels/DPI
and GLB21 node geometry/volume. It tests current material and genuine continuous swept
solids, all six actual tongues, connected mating witnesses, exact layer budget and blocked
orders/negative controls. Source commit f49e3b3be73b7d474302823cc9072148319c8f67 must be local
for174 protected upstream byte comparisons. Preserve logs/exit codes; stale artifacts passing
cannot establish successful regeneration. Equivalent DXF may vary handles/timestamps.

Numerics:6-decimal exported coordinates have <=sqrt(2)*0.5e-6mm point error. Export/model
comparison uses Hausdorff<1e-6mm and a perimeter×rounding-error area bound. Boolean volume
collision epsilon1e-6mm³; GLB float32 metre volume uses relative1e-5 tolerance. Neither is
physical manufacturing accuracy. Nominal circle has360 segments, sagitta0.003617mm.
PNG dimension stroke is0.8pt to survive96dpi raster; measured cut-path pixels are checked.

Independent alternate OpenCASCADE review (optional extra dependency outside core):
`/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P04/tests/independent_occ_review.py`
uses CadQuery2.7.0/OCP7.8.1.1 and independently reads exported geometry without importing
P04's model. See reports/CTB-004-INDEPENDENT-QA.md for actual execution/outcome and scope.
To provision the optional reviewer dependency in another venv, install
`python -m pip install -r projects/CTB-01/parts/P04/src/requirements-qa.txt`.
The executed independent audit used the existing ctb-001 runtime; a clean optional-QA
venv installation was not repeated. Core71 cases do not depend on CadQuery; independent
nested checks are separately counted.
