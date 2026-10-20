#!/usr/bin/env bash
set -euo pipefail
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
python_bin=${PYTHON:-python}
export XDG_CACHE_HOME=${XDG_CACHE_HOME:-/tmp/ctb006-cache}
export MPLCONFIGDIR=${MPLCONFIGDIR:-/tmp/ctb006-mpl}
"$python_bin" projects/CTB-01/parts/P06/src/generate.py
"$python_bin" projects/CTB-01/parts/P06/src/preview_stages.py
"$python_bin" -m unittest discover -s projects/CTB-01/parts/P06/tests -p 'test_*.py' -v
"$python_bin" projects/CTB-01/specifications/CTB-000/validate_contract.py
"$python_bin" tools/check_ctb_baseline.py
