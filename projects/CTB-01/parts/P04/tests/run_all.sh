#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../../../.."
CTB_PYTHON="${CTB_PYTHON:-/workspace/.venvs/ctb-004/bin/python}"
export XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl
"$CTB_PYTHON" projects/CTB-01/parts/P04/src/generate.py
"$CTB_PYTHON" projects/CTB-01/parts/P04/tests/test_disks.py
"$CTB_PYTHON" projects/CTB-01/parts/P03/tests/test_connector.py
"$CTB_PYTHON" projects/CTB-01/parts/P02/tests/test_spacers.py
"$CTB_PYTHON" projects/CTB-01/parts/P01/tests/test_geometry.py
"$CTB_PYTHON" projects/CTB-01/specifications/CTB-000/validate_contract.py
"$CTB_PYTHON" tools/check_ctb_baseline.py
