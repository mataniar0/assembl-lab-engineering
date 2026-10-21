# CTB-011 — geometric nesting optimization (DESIGN_ONLY)

Source: CTB-010 personal-prototype DESIGN_ONLY package, **not production approved**.

**Improvement:** eight source sheets to four: 6mm birch seven to three; 4mm birch remains one. Stock 440×800mm portrait (same as 800×440), 10mm nominal margin and minimum 5mm geometric gap. Thirty 6mm and two 4mm pieces = 32; geometry preserved with translations / 180° planar rotations. No mirrors; flexible rim strips remain at 0°.

- `nesting/BIRCH6_S01..S03.{dxf,svg}`: revised 6mm sheets.
- `nesting/BIRCH4_S01.{dxf,svg}`: unchanged stock allocation for flexible rim pieces; regenerated from native profiles.
- `BOM/instances.csv`: unique instance IDs and coordinates.
- `nesting/SHEETS.csv`: allocations and nominal material utilization.
- `manifest/layout.json`: placements and provisional parameters.
- `QA/REPORT.md`: checks and limitations.

`CUT_OUTER` and `CUT_INNER` are cut profiles; `REFERENCE_SHEET_NOT_CUT` and `ANNOTATION_NOT_CUT` are **only references/labels**. Units mm, 1:1. DXF uses +Y upwards and SVG flips the sheet viewport for display; source contours are not mirrored individually.

**No fabrication release:** physical material dimensions, grain/flex orientation, cutting kerf, bend, bonding, fit, load and stability remain unverified; zero kerf compensation. Keep CTB-010 unmodified. No physical tests performed.
