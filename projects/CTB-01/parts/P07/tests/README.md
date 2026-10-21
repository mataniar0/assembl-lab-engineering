# Focused CTB007 verification

`PYTHON=/path/to/python projects/CTB-01/parts/P07/tests/run_all.sh` regenerates source-derived
exports then tests, using set-euo-pipefail. A failed generator stops before stale files can
be accepted. Install src/requirements.txt into an isolated Python3.12 environment.

Tier1: test_skins_rim.py46 unique cases (7global+13per variant). Real DXF/SVG/PNG dimensions,
closed finite connected material, skin6/rim4, all six slots, sheet-axis/stock, actual web/seam
screens, mathematical bent volume/slabs, GLB+BOM, static full matrices, real sweeps, access,
free top uplift and broken geometry controls. Repeat after meaningful geometry revisions.

Tier2: all 46 plus7 focused test_integration.py,25 contract +15 import smoke =93 unique.
Affected IF03/07/08/10/11/12, protected439 bytes, active pre-ring 27 and all4 spacers per leg,
unchanged original disks/ribs/top budget, no P06 or invented P08. Reviewer runs separate
OpenCASCADE reconstruction of actual outputs using src/requirements-qa.txt, not production
geometry code. Repeated cases and pair comparisons do not increase unique test count.

Tier3:347 old component cases NOT_RUN (297 P01–P05 +50 P06). No reason to rerun untouched
suites for this bounded component study. Broad testing remains required on shared/upstream
change or before G2b/G3/G4; planned periodic pipeline trackedIssue20, currently
NIGHTLY_REGRESSION_NOT_CONFIGURED. Physical kerf/stock/glue/load/stability NOT_RUN.
