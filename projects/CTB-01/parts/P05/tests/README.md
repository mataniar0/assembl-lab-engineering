# CTB-005 reproduction and test accounting

From the repository root, with Python 3.12:

```sh
set -euo pipefail
python -m venv /workspace/.venvs/ctb-005
/workspace/.venvs/ctb-005/bin/python -m pip install --no-cache-dir -r projects/CTB-01/parts/P05/src/requirements.txt
/workspace/.venvs/ctb-005/bin/python -m pip check
CTB_PYTHON=/workspace/.venvs/ctb-005/bin/python bash projects/CTB-01/parts/P05/tests/run_all.sh
```

The runner regenerates P05 first, then executes 62 P05 +71 P04 +51 P03 +52 P02 +61 P01
+25 contract +15 import = **337 unique checks**. `set -euo pipefail` preserves the real exit
status. Never use stale exports as evidence after failed generation. The fresh core venv
excludes system site packages. No service is needed. Requirements inherit pinned P04/P03/
P02/P01 dependencies, including SciPy 1.17.1 for GLB export. Source commit 6292a0e and its
ancestors must remain local for the 259 protected-file byte comparisons.

The 62 P05 cases comprise eight shared checks, 14 per rib alternative and six per disk
proposal. They read actual DXF/SVG/PNG/GLB, compare the reviewed 21 bodies, verify six
identical instances, and test finite material and exact continuous swept solids. B's
original 27-body model is intentionally BLOCKED; its test passes only when that collision
is reported. B/C proposal restraint is conditional on the named disk substitutions and
fixed disk positions. Nested pair comparisons and repeated runs are not extra unique tests.

Coordinates export to six decimals: point error ≤sqrt(2)×0.5e-6 mm, Hausdorff <1e-6 mm;
the area bound derives from perimeter and rounding. Collision epsilon is 1e-6 mm³; GLB
float32 metre volumes use relative tolerance 1e-5. A's quad8 R1/R0.8 arcs have maximum
sagitta 0.004815/0.003852 mm; B/C fillets use 0.002 mm chord tolerance. None is a measured
manufacturing tolerance. The 6 mm material-neck screen is not strength certification.
Equivalent DXF handles/timestamps can vary; compare cut geometry, units and solids.

Optional independent OpenCASCADE audit, with no implementation imports:

```sh
# Install in a suitable separate venv if CadQuery is absent:
python -m pip install -r projects/CTB-01/parts/P05/src/requirements-qa.txt
XDG_CACHE_HOME=/tmp/ctb005-qa-cache /workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P05/tests/independent_occ_review.py
```

Executed QA used the existing CadQuery 2.7.0 / OCP 7.8.1.1 runtime at ctb-001; a fresh
optional CadQuery installation was not repeated. See the independent report and script
`--help` for exact commands/output. Core tests do not require CadQuery. Physical G3 tests
were NOT_RUN, and G4 manufacture/cutting is NOT_AUTHORIZED.
