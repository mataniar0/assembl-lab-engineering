# CTB-002 reproduction and geometric tests

From repository root, Python3.12:

```sh
set -euo pipefail
python -m venv /workspace/.venvs/ctb-002
/workspace/.venvs/ctb-002/bin/python -m pip install --no-cache-dir -r projects/CTB-01/parts/P02/src/requirements.txt
export XDG_CACHE_HOME=/tmp/ctb-cache
export MPLCONFIGDIR=/tmp/ctb-mpl
/workspace/.venvs/ctb-002/bin/python projects/CTB-01/parts/P02/src/generate.py
/workspace/.venvs/ctb-002/bin/python projects/CTB-01/parts/P02/tests/test_spacers.py
/workspace/.venvs/ctb-002/bin/python projects/CTB-01/parts/P01/tests/test_geometry.py
/workspace/.venvs/ctb-002/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-002/bin/python tools/check_ctb_baseline.py
```

Core P02 suite executes52 cases, followed by61+25+15 upstream checks. It reads real
DXF/SVG loops and PNG pixels, audits DXF, verifies6 watertightGLB solids/volumes,
checks actual continuous solid sweeps, land, spacing, unchanged upstream Git bytes,
BOM, ring envelope and documented allowances. Tests require source base Git commit
849d40c45ddad721dc2aafec8241b45d9cf56a62 to be available; normal history has it.

Explicit negative controls cover zero thickness schema, zero residual web, forced
spacer overlap, shifted holes, thick stock, wrong insertion direction and omitted
asymmetric spare holes. These pass when the bad model fails the intended predicate.
The A concept is intentionally BLOCKED and its low-land failure is asserted and
reported; that is not a claim that it meets the6 mm design hypothesis.

The independent QA script does not import P02 modelling code; it reads SVGs and JSON
placements and reconstructs OpenCASCADE solids. Optional QA dependency:

```sh
/workspace/.venvs/ctb-002/bin/python -m pip install 'cadquery==2.7.0'
/workspace/.venvs/ctb-002/bin/python projects/CTB-01/parts/P02/tests/independent_occ_review.py
```

It checks6 valid solids,15 final intersections,15 continuous sweep intersections,
3 deliberate interfering controls and4 minimum lands. Output JSON is written to
`/tmp/ctb002-occ-qa-results.json`; committed review evidence is in project reports.
OCC is optional for the normal generator/core tests; it was available and executed
in the review environment. These are ideal CAD tests, not material/machine, fit,
adhesive, structural, physical safety or production approvals.

SciPy1.17.1 is a required GLB export dependency; it is pinned because Trimesh color
conversion uses scipy.sparse. Preserve generator exit status and stop if it fails;
passing tests against older artifacts do not establish successful regeneration.
