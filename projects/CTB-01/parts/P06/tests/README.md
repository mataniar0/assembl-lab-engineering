# CTB-006 risk-based verification

Use Python3.11+ and `pip install -r projects/CTB-01/parts/P06/src/requirements.txt`.
`PYTHON=/path/to/venv/bin/python projects/CTB-01/parts/P06/tests/run_all.sh`
regenerates exports before tests and fails immediately if generation fails. No stale-output
PASS after a failed generator is allowed.

Tier1: `python projects/CTB-01/parts/P06/tests/test_ring.py` (42 unique cases).
Run after each meaningful geometry revision. Includes actual DXF/SVG parsing, physical PNG
scale, all6 cheek contacts, nominal full matrices, exact early/late sweeps, negative controls,
BOM/GLB parity and repaired C key reproduction. `subTest`/loops do not inflate case counts.

Tier2: all Tier1 + `test_integration.py` (8 unique focused cases) + unchanged CTB-00025
and import15 static smoke checks. This checks IF09/01/02/14, selected27 consumption,
Y_FIRST18 stages/171 exact checks, all336 protected bytes, and bounded upper/top budgets.
Independent reviewer separately parses regenerated exports in OpenCASCADE; see the QA report
and `independent_occ_review.py` (requirements-qa.txt). Reviewer reruns are not extra unique tests.

Tier3: the complete prior337-case run is NOT_RUN;40 static cases ran and297 P01–P05 component cases are NOT_RUN in this PR, because protected files are
byte-identical. NIGHTLY_REGRESSION_NOT_CONFIGURED, tracked in infrastructure Issue20.
Run broad suites before G2b/G3/G4 or if protected/shared sources change. No such scheduled
successful hosted CAD run is claimed. Physical stock/kerf/strength/retention/stability NOT_RUN.
