# Reproduce P01 exports and checks

From `/workspace/assembl-lab-engineering` (Python 3.12):

```sh
python -m venv /workspace/.venvs/ctb-001
/workspace/.venvs/ctb-001/bin/python -m pip install --no-cache-dir -r projects/CTB-01/parts/P01/src/requirements.txt
export XDG_CACHE_HOME=/tmp/ctb-cache
export MPLCONFIGDIR=/tmp/ctb-mpl
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P01/src/generate.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P01/tests/test_geometry.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-001/bin/python tools/check_ctb_baseline.py
```

Tests read actual DXF/SVG and PNG pixels, not just generator metadata. They also
check source regeneration, offsets, global-to-local inverses, bare cheek projections,
body sections, geometric erosion screening and analytical cubic curvature. All
61 test cases must execute (not a zero-test exit). The negative controls deliberately
submit a self-intersecting contour and oversized fillet; detecting those defects
passes those tests. Export validation is independent of `generate.py` but shares
`model.py` only for explicit regeneration/instancing comparison; geometric predicates
and DXF/SVG readers independently inspect the saved contours.

On a horizontal shoulder a connected cross-section can be represented by GEOS as
multiple adjacent LineStrings. `line_merge` must yield one connected LineString;
separated intervals still fail. PNG content tests allow gray antialiased stroke
pixels, require ink near every vertex and reject ink away from the contour.

These geometric screens are not stress/strength, manufacturing-process capability,
full assembly insertion, fit or physical testing. Radius≥1 mm is only a concept
screen. No micro-neck, material-strength or tooling claim extends beyond the stated
criteria. DXF internal handles/timestamps may vary on regeneration; compare contours,
units and metadata rather than requiring identical DXF file bytes.
