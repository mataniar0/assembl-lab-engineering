# CTB-006 / P06 brace-ring studies — DESIGN_ONLY

Issue15. Primary IF-09 P01/P06; affected IF-01 spacers, IF-02 selected Y and IF-14 floor
footprint. B02/B05/B07/B10/B11 and P05 outward retention remain open. Use selected
SOFT_CURVE, B_THROUGH_ADHESIVE at35/90/200/390, A_COMPACT_CLOSED/Y_FIRST, P04A/NO_HOLE
and P05A. Original CTB000/P01–P05 files remain unchanged; ring mortises are P06-local
versioned P01 overlays requiring review, not silently approved cheek changes.

A: one rounded-triangle ring, closed cheek mortises, ring before Y/cheek closure.
B: three matched jigsaw segments and six actual wood stop keys, open loading channels;
two-phase segment installation after closed legs. C: circular ring and six actual vertical
wood keepers, closed cheek mortises, ring before legs then keepers. Each retains four
spacers per leg. No hidden fixtures or hardware. Geometry checks do not prove strength.
Risk-based tests: new component tests plus focused active-interface/smoke checks. The complete
337-case upstream run is NOT_RUN;40 static checks ran and297 P01–P05 component cases
are NOT_RUN. See validation and test plan.
No physical cutting, measured fit, load rating or production release.


Clean build and risk-based test runner:

```sh
python -m venv /tmp/ctb006-venv
/tmp/ctb006-venv/bin/pip install -r projects/CTB-01/parts/P06/src/requirements.txt
PYTHON=/tmp/ctb006-venv/bin/python projects/CTB-01/parts/P06/tests/run_all.sh
```

`src/generate.py` emits all cut profiles, GLBs, sections and full material proofs;
`src/preview_stages.py` adds actual cropped route configurations. The runner does both.
DXF/SVG/PNG: `variants/`; versioned cheek CRs: `proposals/`; actual solids/proofs:
`assembly/`; exact input hashes: `src/upstream-sha256.json`; BOM: `BOM-v1.csv`.
See `DECISIONS.md`, `P01-INTERFACE-CHANGE-REQUESTS.md`, `CTB-007-008-009-HANDOFF.md`
and the five CTB-006 reports. C is recommended for next study, AWAITING_LEAD_SELECTION.
Keys are not self-retained; no fully mechanically captured or physically tested ring.
