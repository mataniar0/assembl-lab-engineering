# CTB-001 independent automated QA — 2026-10-19

Result: **0 critical CAD/data defects found in the reviewed concept deliverables**.
DESIGN_ONLY / AWAITING_DESIGN_SELECTION remains mandatory. This separate reviewer
performed an independent source/export/report audit and executed the checks below.
This is automated component QA, **not human engineering-lead G1 approval**, owner
selection, manufacturing approval, permission to start CTB-002 or merge approval.

## Review scope and actual executions

Read root AGENTS.md, Issue #3, CTB-000 SPEC_HE/DECISIONS, authoritative parameters,
interfaces, parts and open-issue inventory; reviewed P01 design inputs/schema, model,
generator, exported dimensions, geometry tests, BOM, fit worksheet, runner instructions,
interface matrix/results, design review, validation record and updated STATUS.
Visually inspected GEOMETRIC layout and revised SOFT_CURVE/FLARED_CURVE layouts.
The three alternatives are visibly distinct and preserve common attachment/contact
geometry; previews explicitly omit unvalidated connections.

Commands independently run from the repository root using the existing venv:

```sh
/workspace/.venvs/ctb-001/bin/python -m unittest discover -s projects/CTB-01/parts/P01/tests -v
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/parts/P01/tests/test_geometry.py
/workspace/.venvs/ctb-001/bin/python projects/CTB-01/specifications/CTB-000/validate_contract.py
/workspace/.venvs/ctb-001/bin/python tools/check_ctb_baseline.py
```

Initial independent P01 execution: **57/57 passed**, zero failures. Revised P01
execution: **61/61 passed**, zero failures (0.754 s). Independent baseline runs:
**25/25 source checks + 15/15 import checks passed**. Final unique suite total:
**101/101 checks passed**, zero failures, zero skipped. The initial independent
run emitted an ezdxf read-only home-cache warning; this did not affect geometry or
exports. Runner instructions configure writable /tmp caches. Primary-agent initial
construction failures and repairs are separately preserved in CTB-001-VALIDATION.md;
this reviewer did not execute those failing development cycles or the fresh install.

Tests directly read DXF units/closed polyline/audit, SVG vertices and actual PNG
pixels/scale, then check contours, regenerated identity, inverse transforms, tangential
spacing, sheet allowance and reserved bands. Source inspection confirms layout/SVG/PNG
all receive the same flattened model contour; layout image content is visually
reviewed rather than fully reconstructed by a separate raster geometry algorithm.

## Independent calculations and corrected findings

1. The original 24 mm tongue dimension at the rounded nose could imply an incorrect
   flat-tip width. Independent section intersection at z488 found **22.0 mm** for all
   three variants. Corrected drawing labels say 24 mm nominal, reference the full-width
   section at z480 and explicitly give the 22 mm tip flat. All variants now assert
   22 mm at z488. No contour or approved dimension was changed.
2. Independently reconstructed convex hulls from actual six nominal ground-contact
   strips yield minimum origin-to-edge distance **140.691343 mm**, area
   **101905.922735 mm²** for all variants. This is distinct from the three contact-center
   triangle's **120 mm** inradius. Reports and machine-readable outputs correctly
   distinguish them; neither is stability evidence.
3. Independently computed tongue corner radius at both disc sections:
   `hypot(69,13.5) = 70.308250 mm`, leaving **24.691750 mm** inside the candidate
   disc's radius95 envelope. This does not measure disc-slot fit, lock or insertion.
4. Radius≥1 mm checks screen ideal planar curvature only. Final README, fit worksheet
   and review explicitly preserve unknown process/tool/edge-finishing capability.
   This resolves the potential overstatement suggested by the test name
   `achievable_corner_radii`; it is not a certified machinability test.

## Acceptance audit and residual blockers

- CTB-000 original15 files remain byte-for-byte unchanged; all14 IF and13 B records
  are preserved. Portrait H800×W440 and frozen dimensions remain unchanged.
- Three editable alternatives provide a valid one-contour DXF/SVG profile, matching
  PNG, dimensioned elevation/isometric layout, dimensions/instances and reproducible
  source. Padded envelopes fit the sheet with an explicitly provisional10 mm margin.
- P01 BOM is exactly6 identical cheeks of one selected variant, not18 pieces.
  Six instances use the common transform, orientations0/120/240 and t=±10.5; nominal
  6 mm material gives actual geometric15 mm gap and27 mm outside width.
- B04 Y r94/r90 discrepancy remains blocked with two proposed remedies and trade-offs;
  neither is adopted. Spacer/ring reservations remain uncut and overlapping near245.
- Both disc Z intervals retain full24 mm tongue section. Disc slots, positive locking,
  sequence/access and integrated3D collision evidence are absent and explicitly unknown.
- B01/B02/B03/B04/B05/B07/B10/B11 remain open as applicable. Grain, material properties,
  true thickness, kerf coupons, floor compliance, loads, strength, tipping and physical
  testing remain outstanding. No unsupported load rating or physical PASS is asserted.
- SOFT_CURVE is a documented recommendation only. Aesthetic/functional selection and
  explicit human engineering-lead G1 decision remain required before progression.

No additional critical defect or required source correction was identified in the
final reviewed concept set. Publication of a PR is appropriate for review; merging,
selection and downstream component design remain outside this QA determination.
