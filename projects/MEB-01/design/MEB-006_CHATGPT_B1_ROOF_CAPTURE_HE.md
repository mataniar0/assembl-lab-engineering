# MEB-006 B1 — H1 roof capture | ChatGPT direct feasibility study

**Date:** 2026-10-22 · **Priority:** P1 · **Executor:** ChatGPT without Codex · **Status:** `GO_FOR_NOMINAL_RIGID_2p5D_GEOMETRY_ONLY`, **DESIGN_ONLY**, `INDEPENDENT_QA_PENDING`. **Owner exterior 346mm not frozen; 2.2mm rear relief not owner-approved.** Issue #31. Parent research draft PR #29.

## One candidate E1 (not multiple full concepts)
A 4mm *radial* curved roof has two narrow **integral axial ears**, left `X10..14` and right `X322..326`, only over arc coordinate `S40..56mm` (origin front edge on the inner radius **R=43.3423913mm**). The moving 6mm internal LID_SOCKET cheeks (X5.5..11.5 and X324.5..330.5) use a curved enclosed groove over `S36..60` with clearance window `S39.5..56.5`, radial `R-0.2..R+4.2`; local outer lip **2.1mm radial ligament** (R+4.2 toR+6.3), and ~2.3mm raised over nominal skin. Roof main width X14..322. Trapped by fitting socket cheeks **axially from outside** after roof/rails/ribs, before outer lid-end cheeks and pivot. Feasibility of *complete* assembly and axial retention against service loads has not been proven. Visually raised side detail may require owner approval.

## Direct model-based evidence
- Reused original v0.3 `build_v03.py` and MEB004/MEB005 recovered research instead of reconstructing 26 parts.
- Analytically exact 2.5D **X-slab overlap + YZ rigid rotation** using true normal-offset 4mm roof polygon.
- Rigid moving/static roof+tabs+socket: **441/441** sampled angular poses, 0–110° step0.25°, zero volumetric collisions among 73 relevant overlapping-X pairs. Extra **1101/1101** poses step0.1° also zero.
- Local *two moving socket insertion* checks: **25+25 positions**, zero colliding with moving roof, rails and ribs under a stated assembly order. **Does not include lid ends and stationary body during socket insertion**.
- Moving/moving 0°,55°,110°: zero overlaps; folded roof and ribs match source inner arc geometry at common vertices.
- Negative control rear wall *without* Z71→68.8 relief: **256/441 FAIL as expected** (first at46.25°).
- Negative control full roof extended X11.5..324.5: **111/111 FAIL as expected**.
- Nominal stationary cheek-to-cheek inside axial space X12..324 **312mm**; at closure no moving solids intruded into studied inner usable prism Y6..71, Z6..65. Actual user-required **≥310mm** effective clearance remains to verify with all retention hardware/physical prototype.
- **13/13 self-authored assertions PASS** after three documented code/model correction cycles, **2 DXF readback** and two SVG diagrams generated. All derived DXF/SVG are **DESIGN_ONLY**, not cutter-ready. Source ZIP 11 entries verified (CRC).
- Not an unsampled-angle mathematical proof, not a material bending/fracture test, not independent QA.

## Corrections in direct study: 3
1. Found a spurious ~0.00311mm³ overlap from mismatched source-arc sampling. Fixed by using identical v0.3 inner arc vertices. Recheck moving/moving zero.
2. Curved groove boundaries originally coincided with ear. Extended window S0.5mm each direction and reran; ear strictly inside.
3. Corrected a precedence/parentheses bug in the usable-inner-prism overlap volume calculation and reran.

## Open / gated
1. **2.1mm nominal upper wood web can be fragile**; physical quality, strength and fatigue NOT_RUN, cannot approve manufacture.
2. The 4mm kerfed plywood bend, assumed neutral line at mid-radius, real kerf, uncut full-arc lands and joint strength are NOT_RUN.
3. Socket's own axial pin retention, lid-end cheek placement after socket slide, glue/tenon fit and whole 26-piece **assembly path NOT_RUN**.
4. Exterior appearance raised detail, rear Z68.8mm relief and final 346mm exterior remain provisional and may require owner decision.
5. Independent QA, G2 complete, G3, G4 and full contour nesting NOT_RUN.
6. Report should not imply that final body G0 is approved; the main MEB project remains gated.

## Artifacts and reproducibility
Direct ChatGPT conversation download **`MEB006_CHATGPT_B1_DESIGN_ONLY.zip`**, SHA256 **`4ce43518edeb57e92e0e30b195337ead8db096931460817a86b71c2e02f52f08`**, **11 files**, containing **reproducible Python source** `meb006_b1.py`, `export_b1.py`, exact reused `MEB_H1_A1_v03/build_v03.py`, JSON result, SVG/DXF reference profiles, explanatory diagram and Hebrew report. **ZIP source/code is in user's chat and not yet committed to GitHub;** this commit is traceability only, not standalone source review. Runtime depends on Python numpy, shapely, matplotlib and ezdxf.

### LEAN next
**B1 result = scoped GO** for a research candidate only. Engineering lead must inspect proof, NOT_RUN and owner appearance tradeoff before a separate B2. **Recommended executor ChatGPT first** for narrower full lid-end/pin/ear insertion and retention investigation; Codex only if demonstrably needed. Independent reviewer required for merging any CAD assertion. Do not auto-merge or release G4.
