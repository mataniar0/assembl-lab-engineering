# CTB-017 — redistribution of 6mm S01 into S03 (4-sheet study)

**Status: DESIGN_ONLY / NESTING_PLANNING_ONLY / NOT FOR LASER CUTTING / ASSEMBLY_ROUTE_UNVERIFIED.**

The user requested to eliminate 6mm sheet S01 from CTB-016 if its parts fit on the other sheets. **Success: all 19 previous S01 bodies are now on previous S03 with an exact rectangle-separation proof for the new placements.** The former 6mm S01 is eliminated; total stock is reduced from **5 to 4 sheets**: THREE 6mm birch sheets + ONE 4mm birch sheet (all 440mm width ×800mm height). No source part geometry, material, thickness, grain specification or tool compensation was changed.

## Sheet mapping
| CTB-017 name | Source | Material | Body count | Contours |
|---|---|---|---:|---:|
| BIRCH6_S01 | previous CTB-016 BIRCH6_S02, same part coordinates | 6mm | 6 | 42 |
| BIRCH6_S02 | previous CTB-016 BIRCH6_S03 **plus all19 bodies from old BIRCH6_S01** | 6mm | 22 | 35 |
| BIRCH6_S03 | previous CTB-016 BIRCH6_S04, tabbed upper+lower circular P07 skins | 6mm | 2 | 8 |
| BIRCH4_S01 | previous CTB-016 BIRCH4_S01, corrected puzzle P07R1/P07R2 rim | 4mm | 2 | 128 |
| **Total** | | | **32** | **213** |

All eight vectors are in `nesting/` as per-sheet 1:1 DXF/SVG. `manifest/layout.json` and `BOM/instances.csv` locate every part (bbox in millimeters). Use only DXF CUT_OUTER and CUT_INNER layers for geometry; SVG board frame uses REFERENCE_SHEET_NOT_CUT and is NOT a laser cut contour.

## Redistributed geometry
Prior S03 has legacy P01×2 and P06, all with Y<=498mm; moved 19 S01 parts are packed at Y>=505mm. Rectangle separation to unchanged originals **>=7mm**. Between moved parts, conservative rectangle separation **>=5mm**.

Moved parts:
- P03 large irregular part: bbox left10/bottom505, 134.389×155.024mm.
- P05×6 ribs, 88×38mm: 3 columns X155,248,341 and rows Y505,548.
- P02B×3: X10,55,100 at Y668.
- P02×7: X145,180,215,250,285,320,355 at Y668.
- P02×2: X10,45 at Y700.

All 22 composite-sheet bodies were checked against their respective original CTB-016 individual contours, by normalizing translated vertices and requiring absolute discrepancy<=1.01e-6mm; **22/22 unchanged**.

## Verified bounded digital QA
1. All4 sheet dimensions 440×800mm; min observed margin >=10mm.
2. All32 instance IDs unique; 32/32 bodies; 213/213 contours.
3. All four resulting sheet SVG/DXF contour coordinate pairs (a total of213 contours), correct CUT layers, closed DXF LWPOLYLINE and AcDbPolyline subclass: **4/4 sheet comparisons PASS**, 213/213 contours.
4. New composite sheet: all19 imported pieces preserved; 22/22 contours normalized to source PASS.
5. Conservative **bounding-rectangle** separation: 19 moved parts mutual min5mm; from the three previous S03 parts min7mm. No pair of new parts is closer than5mm, even by their rectangular envelopes; adequate for purely 2D planning. Inherited original S03 geometry and old other sheets are unchanged; CTB-011 earlier near-neighbor CAD evidence is inherited, not rerun or counted as fresh independent proof.
6. Synthetic negative control: shift P05_2 4mm left, rectangle gap drops to1mm and the checker correctly flags a <5mm violation. No change to delivered parts.

No detected geometric repairs to source parts: **0**. Nesting edit: **1 redistribution iteration**, no failed candidate stored. Independent QA and external ezdxf loading NOT_RUN (self-parser consistency only).

## Release blockers
Previous actual CAD evidence PR61 shows old R2 vertical assembly route **FAIL at offset+2mm (~64mm³ per seam)** even though two final curved seams pass. No proven alternative A/B path exists; accepting a strong puzzle neck for planning does **not** prove bending/insertion. G3 physical grain/bend/kerf/glue/strength/loads NOT_RUN, G4 manufacturing blocked. This package is for digital review and costing, **not machine-ready** until assembly redesign/validation and physical gates. No merge required or performed for this study.
