# PST-310 V6 — exact nominal circumference / rim-to-plate tab QA (2026-11-05)

**Result: NOMINAL CIRCUMFERENCE PASS / OWNER APPROVED / PHYSICAL END-CLOSURE GAP STILL UNMEASURED.** User personally accepted bend behavior and load/stability as satisfactory for advancing this milestone. This acceptance is logged as the user's decision; we did not independently prove physical capacity or bend behavior.

## Original V6 cut-file data, no changes
Two Ø310.000mm laser-cut birch6 top/bottom discs, radius R155; six 4mm birch outer-rim flat sectors, each nominally 60 degrees when bent, with 39 rows at4mm pitch /58 one-line slit strokes. Wall section reference R151..R155, geometrical midline R153, total top box 60mm.

## Independently computed perimeter quantities
- Plate outer circumference π×310 = **973.893722613mm**.
- Wall centerline circumference 2π×153 = **961.327351998mm**.
- Wall inner circumference 2π×151 = **948.760981384mm**.
- Required neutral developed arc per sector π×153/3 = **160.221225333mm**.
- Actual V6 SVG sector main-body x extent = **160.221230mm**, each of six; developed total **961.327380mm**, discrepancy to exact midline **+0.000028mm** from 5-decimal coordinate rounding — geometrically negligible.
- Difference between plate external circumference and wall neutral circumference **12.566370614mm** is **EXPECTED** from the 2mm difference in radii, not an excessive rim or missing material.
- Six modeled butt seams are gap-free and overlap-free at the nominal ideal R153, but the production SVG files have no measured-kerf allowance; actual seam gap/overlap cannot be inferred from this numeric equality.

## Actual vector checks completed
- Verified 6 separate rim SVG and DXF pairs, 2 plate SVG/DXF pairs, all same layers and coordinate vertices.
- Plate boundary outside diameter independently confirmed 310mm in both SVGs.
- Each plate contains **12 correctly oriented edge notches**, at global angles 12,48,72,108,132,168,192,228,252,288,312,348 degrees, with inner-notch radial depth to R150.5mm; sectors occupy R151..155.
- Each sector has top+bottom protruding 12.000mm wide finger tabs centred at 12° and 48° relative to the sector; matching notches have nominal arc widths **12.500mm**, leaving **0.250mm per side** before kerf.
- Six rim file profiles and **348** one-line kerf strokes verified on BIRCH4_S01_440x800 SVG/DXF nest; **all 6 nested vs individually exported rim profiles + strokes preserve exact geometry by translation** (max roundoff 0.00001mm).
- All six sector borders butt end-to-end nominally. There is no inter-sector puzzle seam or mechanical positive lock modeled.
- **No revisions to STL/STEP, source SVG/DXF or the V6 nesting.**

## Manufacturing decision boundary
The user has approved the bend and strength/stability from their own perspective; this report **does not override that acceptance**, but it documents that actual end-to-end closure after flexing + laser cutting has not yet been measured. As in a previously physically corrected coffee table rim, **effective developed length may differ from ideal midline due to bend axis movement, slit opening and laser kerf**. Before stating the physical circumference has passed, dry-fit all six sections around the pair of Ø310 plates without forcing or glue, note total physical overlap (+E) or visible gap (-G) and verify all24 end tabs meet plate notches.

If observed global overlength E mm, preliminary equal-sector correction is -E/6 per sector. If observed deficiency G mm, preliminary increase is +G/6 per sector. Any such correction must be regenerated as geometry and rechecked for tabs/notches, without modifying plates by default. Do not automatically rescale the entire file or blindly trim all sectors.

**Audit files** created and downloadable from current ChatGPT conversation: V6_CIRCUMFERENCE_AUDIT.json, README_HE.md, PERIMETER_AUDIT_DIAGRAM.png, and PST310_V6_CIRCUMFERENCE_QA_ONLY.zip. These attachments are not uploaded to GitHub by this report.

## OWNER APPROVAL — 2026-11-05

The user expressly confirmed in this conversation: **"אני מאשר את ההיקף"** (I approve the circumference). This freezes the **nominal** V6 six-sector rim geometry for proceeding with the already prepared digital nesting: Ø310mm disks, six 60° sectors, each 160.22123mm developed midline, total ~961.32738mm. **No source STEP/SVG/DXF nesting or part geometry changed**. It is a design/owner acceptance, and does not itself establish physical dry-fit measurement or an actual seam closure measurement. Do not record a physical pass or introduce an automatic trim allowance. Should physical cutting later show a gap or overlap, reopen only the rim-length issue while preserving the existing disks where practical.
