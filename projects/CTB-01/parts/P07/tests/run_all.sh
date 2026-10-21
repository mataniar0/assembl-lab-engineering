#!/usr/bin/env bash
set -euo pipefail
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
python_bin=${PYTHON:-python}
export XDG_CACHE_HOME=${XDG_CACHE_HOME:-/tmp/ctb007-cache}
export MPLCONFIGDIR=${MPLCONFIGDIR:-/tmp/ctb007-mpl}
"$python_bin" projects/CTB-01/parts/P07/src/generate.py
"$python_bin" -m unittest discover -s projects/CTB-01/parts/P07/tests -p 'test_*.py' -v
"$python_bin" projects/CTB-01/specifications/CTB-000/validate_contract.py
"$python_bin" tools/check_ctb_baseline.py
