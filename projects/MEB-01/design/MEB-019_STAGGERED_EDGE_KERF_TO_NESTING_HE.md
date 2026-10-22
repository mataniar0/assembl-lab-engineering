# MEB-019 — Edge-reaching staggered single-line kerf, lid skin only

**2026-10-22 · P1 · Executor ChatGPT · LEAN v1.1 · DESIGN_ONLY · Issue #83.** Based on MEB-016–018 / J3, draft PR #81.

## Owner-reported problem
Old skin had 209 short internal kerf centerlines inside three spaced groups, leaving long unkerfed longitudinal strips. Owner observed/believes lid cannot bend sufficiently. No other existing laser-cut part is authorized to change.

## New pattern (source-level numerical candidate)
- Exactly 22 horizontal row centerlines (7 segments per row = **154 DXF LINE entities**), pitch **4mm** across flat skin's **99.17085mm** developed arc height.
- Alternating six **6mm uncut bridges** between consecutive segments on each row; bridges stagger **22mm** between adjacent rows; maximum cut segment **42mm**.
- Both main long edges reached by slots in **every row**. Some lines terminate at the root of the 6mm axial hinge ears, which remain wholly uncut. **18 line ends on each true exterior edge**, 4 per side at ear shoulders.
- Not a 0.8mm-wide slot geometry; no Kerf compensation, only individual theoretical cut centerlines.
- Total nominal straight-line slit length old **3498mm**, new **5984mm**, +**71%**, but **actual bend radius/flexibility/cutting survivability cannot be calculated reliably from slit length alone**.

## Scope and guards
Source part `LID_SKIN_RADIAL_4MM` maintains **identical outer contour, dimensions and both H1 ear tabs**; **all 25 other part DXF and SVG byte-for-byte unchanged** and **both 6mm sheet DXF/SVG byte-for-byte unchanged**. Existing 4mm sheet keeps all 5 part contours and placements; **only kerf line entities differ**. Sheet orientation **800mm high × 440mm wide**.

Independent *method*, not independent *reviewer*: another same-assistant DXF/SVG reader and comparator passed **28/28** assertions on line counts, row spacing, line max length, 6mm ligaments, edge topology, 4mm nested translation, 25 unchanged part hashes, unchanged sheet contours, valid mm DXF flag and SVG line parity. Original full assembly geometry and H1 are unchanged, **no new physical movement or strength proof claimed**.

## Files delivered in user chat
- **Minimal changes only** `MEB019_ONLY_LID_SKIN_AND_UPDATED_4MM_NEST_DESIGN_ONLY.zip`, SHA256 `63df70bace0d77f14c0b48b3555e3fd592f00582a63aa751efd7b54e69efa7d0`, 10 entries.
- **Complete reference archive** `MEB019_EDGE_KERF_ONLY_DESIGN_ONLY.zip`, SHA256 `5c6e7792ff99bd8a1bbbdf8dcd0411a6d27224bab99ed2eb08a54f788fef6130`, 121 entries including rebuilt Python.
- SVG, DXF, before-after PNG, skin PNG and updated 4mm nest PNG contained in minimal ZIP. **Source/cut binaries not committed in GitHub**; this draft PR contains only traceability docs. Reviewer needs attached ZIP for reproducibility.

## Gate status
`CAD_2D_CHECKS_PASS` but `MATERIAL_BEND_NOT_RUN` and `INDEPENDENT_QA_PENDING`. Birch 4mm at nominal small roof radius≈43mm with line cuts is not proven feasible; edge tears, wing roots, structural sheet bending, real Kerf and wood sheet manufacturing tolerances are unknown. G3 NOT_RUN, G4 NOT_APPROVED. Do **not** present as guaranteed cut-ready or approved production export.

Recommended lean follow-up is a supervised, appropriately-qualified physical bend/fit test on specimen material, not additional blind retuning of CAD counts.