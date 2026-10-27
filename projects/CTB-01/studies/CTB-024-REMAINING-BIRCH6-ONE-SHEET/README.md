# CTB-024 — Coffee table remaining parts, birch6 one-sheet nesting

**Status DESIGN_ONLY** — VERIFY ALREADY-CUT INVENTORY FIRST. Based on the frozen CTB-017 30-instance 6mm source geometry, without recutting parts listed as already cut.

## Important inventory interpretation
User wrote: "P04U P04L, 4 L1 parts +4 L2 parts, the plate parts and 2 leg parts". This draft interprets 4 L1 /4 L2 as spacers L1_S1..S4 and L2_S1..S4; the two large already-cut leg pieces are assumed L3_P01_1 and L3_P01_2; plates assumed P07T/P07B. See QA_REPORT.json for the exact 14 excluded IDs. **If four L1/L2 pieces instead meant leg cheeks, STOP: this BOM is incorrect.**

## Packing result
Remaining **16 birch6 pieces**: 4 original L1/L2 cheek components, P06_BONDED, P03, 6 P05 web pieces, and L3_S1..S4. All fit on **ONE** 440x800mm stock sheet. Four original cheek contour groups stay in their previous CTB-017 sheet positions; all 12 remaining components are translated into unused actual polygon areas, including between leg profiles. Orientation and all cut contour vertices unchanged. 16 closed outer paths, 25 inner paths, total41, no sheet perimeter CUT geometry. 5mm stock-edge margin target; **minimum 1mm required between CUT contours**, digital vector pair checks PASS (120 distinct part pairs, no overlap, pairwise cut-path separation audit; nearest candidate gaps >=1mm). Individual source part shapes and sizes preserved to 0.000001mm via translation-only.

**Caution:** 1mm between cuts can be impractical for laser kerf, heat-affected edges, sheet flatness and hold-down; trial fit/cut and appropriate actual kerf compensation still needed. Geometry is DESIGN_ONLY and CTB-022 rim physical fit unresolved. Original 4mm rim pieces are NOT included here. No physical manufacture approval or merge.

Outputs: CTB-024_BIRCH6_440x800_ONE_SHEET.svg, matching .dxf, CUTLIST.csv, QA_REPORT.json. Confirm exact already-cut pieces before using.
