# MEB-016–018 — Finger joints and design-only nesting

**Issue #80 · 2026-10-22 · priority P1 · performed by ChatGPT, without Codex · `DESIGN_ONLY`.**

## One design candidate and geometry contract
Baseline MEB-015 J3 / H1 integrated pin. Preserve all 21 movable/fascia/etc parts except body profiles **BODY_END_L/R, BODY_FRONT, BODY_BACK, BODY_FLOOR** (5 revised shapes; 26 part count unchanged).

| Contract family | Count | Finger dimensions | Female slots |
|---|---:|---|---|
| Front long wall → two stationary end cheeks | 6 | Z width12mm × X insertion6mm | in both BODY_END profiles, front edge |
| Back long wall → two stationary end cheeks | 6 | Z width12mm × X insertion6mm | in both BODY_END profiles, back edge below hinge |
| Floor → two stationary end cheeks | 6 | Y width12mm × X insertion6mm | in both BODY_END profiles, bottom edge |
| Floor → front wall | 5 | X width28mm × Y insertion6mm | bottom-open front-wall mortises |
| Floor → rear wall | 5 | X width28mm × Y insertion6mm | bottom-open rear-wall mortises |
| **Total** | **28** | **Nominal ZERO clearance, not Kerf calibrated** | |

Bands (millimeters): end-wall Z=10..22,29..41,48..60; floor-end Y=12..24,31..43,50..62; floor long X=30..58,87..115,144..172,201..229,258..286. Stock base body x12..324; fingers extend to x6..12 and x324..330; nominal usable axial span remains312mm ≥ approved310mm. End cheek bearing and pivot upper area unchanged.

**Important 2.5D code correction:** prior `FlatPart.slices` used an incorrect rectangular bounding box for all XY cuts and a single Z interval for XZ rails. New source algorithm decomposes XY/XZ profiles into exact constant-X interval slabs before collision testing, including complex finger contours. Old flawed slab model must not be used to claim fingers fit.

## QA evidence (same-author, NOT independent reviewer)
- Geometric primary assertions **18/18 PASS**, including **441/441** 0..110° discrete samples with no moving-vs-fixed collision, allpart snapshots no solid overlaps at0/55/110.
- Insert both end cheeks **81+81=162/162** sampled axial positions before floor/spacers/pins; insert floor from below **61/61** poses (note bottom-open mortises have no self-retention without actual bonding).
- Negative control with original non-notched stationary end face correctly finds interfering area.
- Newly implemented DXF parser/outline comparison **113/113 PASS**, 26 per-part DXF source matches and 2 full sheet DXF source contour sets, mm units and 209 4mm kerf centerline lines.
- **Two technical QA/report corrections:** (1) preserve placement XY at 10 decimal precision instead of4, (2) break contour equal-area ordering ties with centroid. Initial 111/113 secondary FAIL; rerun **113/113 PASS**. Not a geometric design failure. Corrected wrong previous BOM skin thickness: 4mm, not analytical skin extruded span308mm.
- ZIP re-extracted to clean temporary directory and both tests rerun: **18/18 and113/113 PASS**.

## Nesting by exact geometry (NOT PRODUCTION)
1 proposed sheet of **440mm width ×800mm height** at6mm for21 separate parts; 1 sheet same dimensions at4mm for5 separate parts. Actual contour-to-contour minimum gap4.4mm and frame margin10mm. 6mm profile use **25.4%** of stock, 4mm use **15.3%** of stock, **209 uncalibrated zero-width kerf line centerlines** in curved lid skin. With two required distinct thicknesses, two boards is minimal count. All individual SVG/DXF and PNG images exist in ZIP.

## Artifact provenance / limitations
User-conversation delivery: `MEB016_018_FINGER_JOINTS_TO_NESTING_DESIGN_ONLY.zip` SHA256 **`3f706c915122777203aa6175771ff01f4bc386380a20d82506e0bb352cd0115c`**, **111 files**, ~1.81MB. Holds all original inherited source plus `build_variant_fj.py`, `run_fj.py`, `qa_secondary_fj.py`, **26 DXF+26 SVG+26 PNG parts**, DXF+SVG+PNG nests and reports. **The binary/source ZIP is in the user's ChatGPT conversation, NOT committed to GitHub**; this PR is audit metadata, cannot pass independent full-source QA without the ZIP.

Production gates remain **BLOCKED**: unmeasured Kerf and stock thickness, actual 4mm bend/neutral axis and uncut bands, H1 radial thin lip / wood pin load/strength, glue/retention for floor and saddle, 26-part actual assembly and QA external review. Provisional354mm outside length and rear-wall68.8mm owner aesthetic/datum freeze needed. No G3 or G4, no manufacturing approval; no merge.
