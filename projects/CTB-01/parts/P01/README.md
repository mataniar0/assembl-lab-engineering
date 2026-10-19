# P01 — CTB-001 cheek candidates

DESIGN_ONLY / AWAITING_DESIGN_SELECTION. Choose one alternative, duplicate exactly
six times; no approved choice or manufacturing release exists. Nominal 6 mm birch.

- `src/design.json`: common tagged parameter inputs for SOFT_CURVE, FLARED_CURVE,
  GEOMETRIC; `model.py`: r-z contour and single instancing transform.
- `src/generate.py`: DXF/SVG/PNG, dimensioned elevation + six-cheek isometric preview,
  machine-readable dimensions/instances, and comparison sheet.
- `variants/<NAME>/profile.dxf`: one closed planar CUT_DESIGN_ONLY LWPOLYLINE,
  `$INSUNITS=4` (mm), local CAD X=r, Y=z, elevation0. This is a 2D drafting plane;
  assembly transform maps its second coordinate into global Z.
- `profile.svg`: physical mm width/height at 1:1, one closed cut polygon, display Y
  flipped to show z upwards; `profile.png`: 1:1 **only at 96 dpi / 100% print scale**,
  rounding to integer pixels <1 pixel. Disable printer/page fit. PNG is for review.
- `layout.svg/png`: dimensioned review sheet and orthographic isometric (35.264°/45°);
  review layout is scaled to its page, **not** a 1:1 cutting file.
- `dimensions.json`: flattened contour hash, controls, radii, sections, allowance,
  foot support projection, and explicit six-instance coordinates.

The final flattened contour is shared by all exports (≤0.02 mm chord approximation,
coordinates rounded to0.000001 mm). Smooth variants use monotone cubic Hermite rails,
with explicit zero r'(z) at both ends; geometric uses circular fillets of the control
polygon. No legacy silhouette or forked illustration was used. Upper stem r35..90,
shoulder easing ends below z450; the full-width24 mm tongue begins at z450. The R1
nose easing starts at487 so both disc planes retain the full candidate section.

10 mm per-edge sheet allowance is a P01 study assumption, not an approved nesting
margin. Only single-part envelope fit is shown; grain direction, process kerf,
heat, fixturing, nesting and actual joinery are not approved.

See `tests/README.md` for exact reproducible commands and `FIT-AND-RESERVATIONS.md`
for unknown fit measurements. Reports are under `../../reports/CTB-001-*`.
