# MEB-011 — Secondary-method self audit and T1 tolerance study

**2026-10-22 | P1 | Executor: ChatGPT | Stage: DESIGN_ONLY | QA: SAME AUTHOR, NOT INDEPENDENT | No G3/G4**

This is versioned research supplementary to MEB-008–010, owner target opening 110°, net usable inside X >=310mm, board WIDTH440 × HEIGHT800mm. Exterior X354mm, 2.2mm rear-wall relief, birch4/6 and veneer changes are **provisional**, not owner-frozen. Original H1-IF2 CAD ZIP remains unchanged.

## Re-parsing the original H1-IF2 exports
Using a newly authored DXF reader and Shapely contour matching rather than trusting the original nesting script:
- All **24 individual DXF files** match corresponding source part outlines; $INSUNITS = mm.
- Both cut-sheet DXF contour sets match all positioned parts; the **209 kerf CENTERLINES** are present and match source shape transforms.
- Original 6mm sheet minimal pair contour separation is **3.99996889mm**, 0.00003111mm below exactly 4mm due numerical geometry. This is **not** a measured manufacturing issue; nonetheless a strict exact-4 test fails.
- More material: simple **direct rigid-surface-contact graph** separates the moving lid into **5 disconnected groups** at its nominal assembled resting pose: skin+two ribs+ears, two longitudinal rails separately, left cheek/socket pair, right cheek/socket pair. This is due to intentional **0.2–0.25mm assembly clearances**, **not** proof parts cannot be mechanically captured. But absence of overlap or direct contact does **not** prove load transfer, locking or a complete assembly path, so claim of rigid integrated lid **remains BLOCKED for G2a**.
- Fixed body face-contact graph is connected (not proof of physical adhesive/strength).

## Tolerance sensitivity — 36 perturbation directions per magnitude
Original H1-IF2 candidate allows a nominal free clearance of **0.2mm** around a roof ear in its capture channel and ±0.2mm around the wooden pin tip in its outer veneer aperture. Relative translation by 0.21mm created model intersections in **10/36 ear directions** and **12/36 tip directions**. Values are model-sensitivity observations, **not allowed manufacturing tolerances**.

## T1 single research correction (6 profiles changed, total still24)
- Widen radial roof capture clearance to **0.4mm each side**, maintaining the nominal **2.1mm wood retaining lip** by expanding the outer arc band by **0.2mm**.
- Widen exterior tip aperture **6.4×3.8 → 6.8×4.2mm** for nominal pin tip 6×3.4mm; increase underlying middle veneer shoulder pocket to **7.2×10.4mm** so it doesn't obstruct the expanded aperture.
- Sheet design-only contour spacing increased to **4.3mm** (NOT kerf compensation) while keeping 440W×800H.
- Retains one 6mm board with **19 profiles** and one 4mm board with **5 profiles**, 209 zero-width uncalibrated kerf centerlines, nominal inside span312mm and provisional outer X354mm.
- T1 sampled relative shift **0.30mm × 36 directions**: **0/36 roof-ear** and **0/36 pin-tip** intersections; at 0.41mm shift: **10/36** ear and **12/36** pin-tip intersections. Still no material tolerance guarantee.
- **21/21 self model assertions**, **441/441 angular nominal poses 0–110° without cross-group solid penetration**, 0 overlapping solid pairs at 0/55/110°, 6/6 sampled *partial* insertion paths and 2/2 deliberately failing wrong-order controls. 8/8 pin displacement stop scans conditional on veneer attachment.
- **16/17 secondary-method same-author audit checks PASS**. The 17th does **not** pass: nominal lid contact graph still consists of five components separated by nominal fit gaps; positive connection/strength not proved. **Do not force this check to green.**
- Two local study correction cycles: repairing expanded veneer pocket after a 20/21 result, and increasing nominal design-only sheet clearance to avoid an exact-4 rounding edge.
- Fresh extraction and local source rerun: **PASS**, without relying on original /mnt/data paths.

## Source and QA location
Complete versioned user-chat ZIP **`MEB011_T1_DESIGN_ONLY.zip`**, SHA256 `4ce6a132bdb7a8fea9a98739a2b1d8d65c5644e11bbad10b92944a9ddd08d335`. Contains the base inherited source, `build_variant_t1.py`, `run_t1.py`, `qa_secondary_T1.py`, 24 DXF+SVG, 2 nested DXF+SVG with PNG previews, and raw JSON self-audit. **No full CAD/binary files are committed in this PR**. PR content is traceability/evidence summary only; independent reviewer needs the actual ZIP. Original archive MEB_H1_Integrated_To_Nesting_DESIGN_ONLY.zip unchanged.

## Strict stop before manufacturing
- Genuine independent QA and full G2a joined load-path / mechanical retainer/insertion contract, full 24-piece assembly, and material tests are all outstanding.
- A full-arc uncut land in 4mm kerfed skin is a major physical bending uncertainty. 2.1mm socket lip and wooden shoulder-pin/cap retention need physical testing by an appropriately skilled person.
- Actual measured veneer/pin thickness, kerf, real bending behavior and final usable interior >=310mm **NOT_RUN**.
- Owner has not yet frozen outer354mm/modified bearing side contour.
- **G3 NOT_RUN / G4 NOT_APPROVED**. This document and T1 cuts are **DESIGN_ONLY**.

**Next task:** MEB-012 / P1 — ChatGPT-first positive-joint connection study for five lid groups (rail↔rib, rail↔socket, socket↔ear, endcheek↔socket) with explicit mechanical load-transfer and assembled insertion paths. Only rerun affected part/nesting regression; Codex not justified simply by exporting known CAD. If major architecture changes required, escalate design to owner first.

## Final artifact checksum
The complete ZIP in the user's conversation is `MEB011_T1_DESIGN_ONLY.zip`, SHA256 `4ce6a132bdb7a8fea9a98739a2b1d8d65c5644e11bbad10b92944a9ddd08d335`, 71 files, ZIP integrity PASS. Full source and 24 DXF/SVG profiles and both nesting sets are in that ZIP, **not GitHub**. Fresh-directory regeneration of the candidate: primary model PASS 21/21 + 441/441 angles; second same-author method 16/17, failing only rigid surface-contact continuity; no independent QA claimed.
