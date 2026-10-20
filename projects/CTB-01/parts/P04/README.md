# CTB-004 / CSH-3P — DESIGN_ONLY

Issue #9 studies IF-03/04/05 (six actual tongues through bottom-skin envelope and both disks),
IF-06/08 (six prospective web joints and skin envelope), IF-12 (reserved positive retention),
and IF-13 (selected Y/base clearance). Open B01/B02/B06/B10/B13 dependencies permit only
explicit candidate contracts and envelope studies under this task, not completed P05/P07/P08 design.
SOFT_CURVE, B_THROUGH_ADHESIVE and A_COMPACT_CLOSED/Y_FIRST are the selected references.

Three alternatives: A rim-open, B closed-rail, C mixed with provisional inspection aperture.
A is recommended for review; no alternative is selected or released by this PR.
The real local model contains 21 bodies. Six matching interface witnesses and skin/wall/tool
studies are separate reservations, never hidden in the actual BOM or counted as finished P05.

```sh
python -m venv /workspace/.venvs/ctb-004
/workspace/.venvs/ctb-004/bin/pip install -r projects/CTB-01/parts/P04/src/requirements.txt
XDG_CACHE_HOME=/tmp/ctb-cache MPLCONFIGDIR=/tmp/ctb-mpl /workspace/.venvs/ctb-004/bin/python projects/CTB-01/parts/P04/src/generate.py
/workspace/.venvs/ctb-004/bin/python -m unittest discover -s projects/CTB-01/parts/P04/tests -p 'test_*.py' -v
```

Use `tests/run_all.sh` for all five upstream suites and P04. Fail-fast generation precedes tests.
See project reports/CTB-004-* and CTB-005-HANDOFF.md. All millimetres, right-handed XYZ.
No physical cutting, nesting, positive lock, load rating or full 50mm tabletop is approved.
