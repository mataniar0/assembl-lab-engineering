# MEB-000 — QA intake, evidence boundaries

## Evidence already read (source-reported)
- V8.2.2 source README: 310×65×65 mm cavity, 6/4 mm nominal plywood, three identified repairs.
- Historical audit CSV: **56 PASS rows, indices 0..55**; 14 file/BOM checks and further dimensions/fits/motion/nesting assertions. The first 14 indices are item-presence/quantity assertions, not separate physical parts.
- Repairs: (1) BODY_RING foot glue overlap 72 → 192 mm²; (2) rib/beam 5+5 mm half-laps; (3) centered 14 mm uncut lid strip and 12 mm side margins.
- Pinned inventory at source commit `ebeefe308efaf80329e16e42a84d51557878fd58`: 14 per-part DXFs + two sheets + one ring/pin fit coupon = 17 DXFs; three auxiliary docs = 20 files.
- Historic audit's `PASS` entries are **unverified as new validation**. Do not aggregate them with any new tests.

## Newly verified in the initial intake
- GitHub source paths, sizes, blob SHA metadata and file counts checked against pinned version.
- Source/issue/baseline labels and explicit legacy-vs-current status partition reviewed during documentation assembly.
- Actual DXF geometry **NOT PARSED** for the new G0 in this change; Python validator has **not** been run in a repository checkout unless subsequent log says so.
- Independent QA **PENDING**. Numerical CAD test score: **NOT SCORED**.

## Work required before claiming G0 pass
1. Run `python projects/MEB-01/specifications/MEB-000/validate_intake.py` on the checked-out branch and attach its actual stdout/stderr.
2. Run the validator's `--self-test` negative controls and attach actual output.
3. Independently retrieve the 17 pinned DXFs, parse contour types/layers/units, compare BOM to exports and inventory to Git SHA. Compute rather than trust existing report numbers.
4. Reproduce physical 3D swept route (G2) and measured fit/kerf/bend/strength (G3) only when those later scoped tasks are authorized.
5. Record independent QA reviewer identity, unique test counts, failures, repairs and exact release boundary.

## Intake blockers
MEB-B01 through MEB-B11 remain OPEN. G3 = NOT_RUN; G4 = NOT_APPROVED. No unchanged legacy file is automatically approved for production by importing its provenance.
