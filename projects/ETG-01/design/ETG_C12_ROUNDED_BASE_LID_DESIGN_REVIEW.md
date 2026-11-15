# ETG-01 C12 — correction: R20 P05 bottom and P07 roof (DESIGN_ONLY)

**Date:** 2026-10-28 · **Project-owner observation:** in C11, the bottom remained rectangular and the opened lid had square front corners although the body front corners were rounded. This is a CAD source-consistency defect, not intended design.

## Change
- **P05:** replaced 260×160 rectangle with actual planar 260×160 outer **R20 all four corners** and 6mm sheet thickness. Flat net area 41,600 → 41,256.637mm².
- **P07:** replaced former X6..254 mostly rectangular roof with **260×160 R20 outer footprint**, rounded front corners, and the necessary original hinge clearances at both rear sides. Removed thin side slivers near rear cutouts. Flat net area 38,165.20 → 39,493.519mm². **Rear cutouts remain OPEN; rear lid corners are not a full uninterrupted R20 quadrant.**
- **Other 100 distinct parts:** exact C11 OCC shapes unchanged. Total **102 nominal 6mm laser-flat separate part geometries**.
- H1 axis/Y160 Z154 and opening 0–120° preserved. No measured wood, glue, laser kerf, finishing, nesting or production-release claims.

## Repeated local evidence
- **21/21** focused source and exchange tests PASSED. Source-normal 6mm, outer envelope, R20 OCC circle edges, only 2 parts altered, all 102 SVG and 102 DXF parsed, all 102 matching contour counts, all geometry section area discrepancies under 0.04%, reimported STEP 102 valid solids, no P12.
- New P07 against every stationary C12 part, **61 modeled poses** (0°..120° every 2°, 5,795 potential part pairs), no volumetric collision; P05 against stationary body no volumetric intersections.
- **Not continuous swept-body proof**; not a prototype, real structural support or independent QA. No G3/G4.
- **Important newly exposed risk:** the legacy reconstructed C11 rear P06/sidewall contour does **not** faithfully make a continuous quarter-annular R20 wall to all heights. Therefore nominal base R20 corners could leave unsupported rear sidewall edge contact; rear corner/body re-engineering is required prior to G1/G2 closure, not hidden by a pretty image.
- Original historical V7.6 CAD remains absent. Current files are from chat-derived C11/C12 parametric design, not original native source.

## Source and package integrity
Conversation ZIP **`ETG_01_C12_MATCHED_ROUNDED_LID_BASE_DESIGN_ONLY.zip`**, SHA256 **`fecfc7b1b1d88c85cb0d20611b52163a1b6936a7a912fa4816facd64648635a5`**; 231 entries and CRC OK. Contains 102×SVG/DXF, source Python including exact C11 dependency, CAD STEP with open 120° assembly, GLB, 3 preview PNGs, QA JSON, changed-profile P05/P07 standalone, BOM and Hebrew README. **Not committed to GitHub**: this PR hosts evidence/status only; independent QA must obtain the ZIP.

## Disposition
`C12_LOCAL_21_OF_21_PASS / REAL_REAR_CORNER_INTERFACE_OPEN / PRE_NESTING_DESIGN_ONLY`.
Recommended next LEAN P1 ChatGPT task: make rear P06 + left/right sidewall/rear P02 contours a coherent rounded closed-wall design consistent with chosen P05/P07, preserving raised H1 clearance and gluing, verify physically meaningful face contacts and whole 0–120° sample recheck. Owner approval required if visible rear hinge outline/large roof gap changes. No merge or nesting for production.
