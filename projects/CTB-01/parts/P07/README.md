# CTB-007 — P07 skins and experimental segmented KERF rim

DESIGN_ONLY / AWAITING_LEAD_SELECTION. Source main6db45fa after CTB006 PR22; original
pre-ring 27 selected bodies, no P06-modified cheek. CTB006R Issue23 and IF09/B05 remain OPEN.
Primary IF03/07/08/10/11/12; selected disk-tongue IF04/05 consumed unchanged. All 439
CTB000/P01–P06 original files are preserved. No physical cutting, bend or production release.

A: two butt-seam segments, closed long slots, unmodified R171 skins, boundary-bond hypothesis.
B: three stepped-seam segments, staggered closed slots, R171 skins; radial entry works,
vertical seam closure blocks. C: four butt segments, alternating edge kerfs and P07-local
v2 skin edge-comb proposal; rim before top works, top-first/radial insertion blocks.
A/B/C have31/32/33 actual bodies (27+two skins+2/3/4 rim pieces). No hidden locks/hardware.
All top layers remain450..500=50mm, external maximumR175, portrait stockH800×W440.

```sh
python -m venv /tmp/ctb007-venv
/tmp/ctb007-venv/bin/pip install -r projects/CTB-01/parts/P07/src/requirements.txt
PYTHON=/tmp/ctb007-venv/bin/python projects/CTB-01/parts/P07/tests/run_all.sh
```

The runner fails fast on regeneration and then runs new/focused cases and40 static G0 smoke
checks. No automatic old component regressions. See tests/README.md and validation report.
Optional independent OCC dependencies: src/requirements-qa.txt, cadquery2.7.0.

Cut coordinates: skins globalXY; rim sheetX=bandheight, sheetY=local arc s, 1:1mm. Each cut
profile is nominal uncalibrated geometry, CUT_DESIGN_ONLY separate from dimension layers.
Flat patterns are not physically validated neutral-axis development: R173 is a hypothesis,
slot0.8/pitch8 are EXPERIMENTAL geometry, measured kerf/thickness/neutral-axis are null.
The bent GLB has actual perforated finite4mm material, mapped in orthogonal height slabs to
a shared360-facet annulus. Chord sagitta≤0.006664mm; volume differs from4×flat area by≈51ppm.
It is a mathematical pre-bent shape, not a simulation or proof of plywood deformation.

src/: source/schema/generator/hash inventory. variants/: all skins/segments DXF/SVG/PNG,
metadata/BOM and paths. assembly/: real GLBs, contacts, collision/access/path matrices,
sections/exploded views. proposals/: C edge-comb and optional upstream coordination notes.
See DECISIONS, KERF-COUPON-PLAN, CTB-008-HANDOFF and five CTB007 reports. All glue, retention,
finish, material strength, bending, load/stability and actual nesting remain NOT_RUN/OPEN.

`assembly/rim-envelope-RESERVATION.json` and dashed display circles define the full
R171..175/Z450..500 cylinder as a non-BOM analytic comparison, never as actual unperforated
material. Actual segmented perforated solids and explicit seam gaps remain in each GLB.
