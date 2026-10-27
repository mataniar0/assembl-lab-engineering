# CTB-025 — Remaining birch6 parts after user cut P06_BONDED

The ring-with-spokes pictured by the user is treated as P06_BONDED, previously included in CTB-024. Removed BOTH its outer and inner cut contours; the previous remaining inventory goes from16 parts /41 contours to **15 parts /39 contours**. All 15 remaining original CTB-017 contours have unchanged coordinates, dimensions, contour vertices and locations from CTB-024. No part is rotated, resized or kerf-compensated.

## Compact nesting
- Full standard board option: 440mm wide by800mm high SVG/DXF.
- **Compact board option:440mm wide by620mm high SVG/DXF**. Identical cutter geometry to the full sheet, only the display stock envelope differs; perimeter reference rectangle is NOT a cut contour.
- All part geometry lies inside X5..433.388973, Y5..613mm; therefore compact sheet retains at least5mm to every edge, with7mm free at the top.
- Existing 440x800 stock can yield a usable180mm-long remainder if cut down to620.
- Exactly one 6mm sheet needed. 15 parts: L1_P01_1, L1_P01_2, L2_P01_1, L2_P01_2, P03, P05_1..P05_6, L3_S1..L3_S4.
- 15 closed CUT_OUTER and24 CUT_INNER geometries. Audit all105 part pairs, zero overlaps and no contour distance below1mm; nearest gap measured2mm. Laser kerf physical compensation is0; this is NOT manufacturing approval.
- CSV lists remaining parts and source data.

## Verify inventory first
Previous CTB-024 assumption excluded all four L1_S and four L2_S spacers plus two L3_P01 cheeks, both P07 upper/lower skins, and both P04 discs. If the actual already-cut 4 L1 /4 L2 parts or two legs mean different component IDs, this BOM is INVALID and requires a new nesting before cutting. Original physical circumference and assembly remain unresolved. DESIGN_ONLY and no merge to main until inventory verified.
