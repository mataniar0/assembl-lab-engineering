# P03 reproducible generation/tests

From repository root, Python3.12:

```sh
set -euo pipefail
python -m venv /workspace/.venvs/ctb-003
/workspace/.venvs/ctb-003/bin/python -m pip install --no-cache-dir -r projects/CTB-01/parts/P03/src/requirements.txt
export XDG_CACHE_HOME=/tmp/ctb-cache
export MPLCONFIGDIR=/tmp/ctb-mpl
/workspace/.venvs/ctb-003/bin/python projects/CTB-01/parts/P03/src/generate.py
/workspace/.venvs/ctb-003/bin/python projects/CTB-01/parts/P03/tests/test_connector.py
/workspace/.venvs/ctb-003/bin/python projects/CTB-01/parts/P02/tests/test_spacers.py
/workspace/.venvs/ctb-003/bin/python projects/CTB-01/parts/P01/tests/test_geometry.py
/workspace/.venvs/ctb-003/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-003/bin/python tools/check_ctb_baseline.py
```

51 P03 +52 P02 +61 P01 +25 contract +15 import =204 cases; nested solid comparisons are
not added to that total. Preserve generator/test exit status; old artifacts passing does
not establish successful generation. SciPy1.17.1 is inherited and required byGLB export.
Core libraries/pins inherit P02/P01 requirements. No network/services needed after install.
Pre-task commit ecee5f0633a6d7c122087ba75c92eddad4cb0932 must be available for byte comparisons.

Tests read real DXF/SVG paths, actual PNG pixels andGLB mesh volumes, then independently
check contours/symmetry/lands and run actual material intersections/full Minkowski sweeps.
A blocked trial route is expected by the test; it is NOT a geometric-path PASS. The
six explicit negative controls reject zero thickness, r94 oversize, lost arm web, shifted
slots, wrong cheek insertion and6.8 mm Y thickness. They pass only when bad geometry is
caught. C open mouth has0 closed-hole land; instead its19.8 mm outer bridge and CR status
are explicit. Global radius and local-r end margin are checked separately.

DXF handles/timestamps may vary. Compare semantically: paths, units, dimensions, solids,
not byte equality of regenerated DXF files. Original upstream bytes DO remain identical.
Rounded paths/chords/numerical epsilon do not imply physical machining accuracy.

Independent second-kernel reproduction (optional QA dependency; no implementation imports):

```sh
/workspace/.venvs/ctb-003/bin/python -m pip install 'cadquery==2.7.0'
/workspace/.venvs/ctb-003/bin/python projects/CTB-01/parts/P03/tests/independent_occ_review.py
```

This reconstructs all3 candidates from actual SVGs in OpenCASCADE,171 final pairs and
171 Y-first sweep checks/candidate,126checks per prebuilt route,18 per central-Y route,
DXF/SVG/mesh audit and independent negative controls. Output JSONs go to/tmp/ctb003-independent-*-results.json.
Core generator/tests do not require OCC. Independent results and QA report are preserved
in project reports. It is automated review, not engineering-lead G1 or manufacturing approval.
