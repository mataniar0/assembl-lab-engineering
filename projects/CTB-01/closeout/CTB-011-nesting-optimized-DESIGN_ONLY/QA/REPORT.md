# CTB-011 geometry and nesting QA — DESIGN_ONLY

- 11 native cut masters from CTB-010; two flexible rim bodies verified geometrically identical; original loop vertices preserved under 0°/180° rotations.
- Inventory: **32 instances** — 30 of 6mm and 2 of 4mm. All original instance IDs retained, exactly once.
- Before: 7 sheets 6mm and 1 sheet 4mm; after: **3 sheets 6mm and 1 sheet 4mm**. Four-sheet (50%) reduction.
- Bounds: all placements within 440×800mm stock at nominal 10mm edge margin — PASS.
- Clearance: **26** bounding-neighbor pairs within 6mm examined with exact external-contour segment-distance and polygon containment checks; minimum **5mm**, no overlaps — PASS. More distant pairs are excluded by rectangular bounds.
- Different stock thicknesses kept separate. Flexible rim parts remain 0°.
- Original closed loops including holes unchanged; no common-line cutting, no mirror, no geometry scaling; DXF as closed LWPolylines and SVG polygons.
- Nominal net-area values carried over from source manifest.

## Open gates

**DESIGN_ONLY.** Only planar CAD geometry has been checked. No independent CAD-kernel recheck or physical prototype verification was performed. Kerf measurement, stock thickness, grain/flex orientation, bending, glue, mechanical fit, load and stability remain open (G3 NOT PERFORMED, G4 BLOCKED). This is not a production release.
