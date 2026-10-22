# MEB-014/015 ChatGPT-first to nesting (LEAN TASK PLANNING v1.1)
**Priority P1, executor ChatGPT; Codex not needed. Stage DESIGN_ONLY; no production approval or independent QA.**

Owner specifically authorized continuing autonomously until nesting. Working source: MEB-011 T1, open research PR #72. Frozen user constraints usable interior X≥310mm, lid opening110°, HEIGHT800×WIDTH440mm stock. **Exterior X354mm, rear wall relief2.2mm and 4mm bend/slit pattern remain provisional**.

## Concept decision
- J1 rejected: 2 visible rectangular openings per moving end cheek.
- J2 research: 4 underside bridge keys, 28 parts, nominally441 angles clear; failed aesthetic review because it leaves rectangular filled patches visible on the end cheek side. Never selected to replace T1.
- **J3 SELECTED FOR FURTHER RESEARCH**: leave the original moving end cheeks completely unmodified, make small lower half-lap reliefs in two lengthwise rails and add **two 6mm birch internal U-shaped saddle connectors** (one beside each moving socket). Connector planeYZ x11.5..17.5 and x318.5..324.5, contours Y27.5..49.5 Z77..92.7. Internal half-laps clear rails by0.30mm. Contiguous flat bonding interface between saddle and neighboring moving socket **255.05mm² each**; bond strength NOT_RUN and connectors are NOT self-locking.
- No new outside circular hinge piece / side perforation. Prior H1 wooden pivot with flush veneer unchanged, external bearing boss still locally rises behind side outline.

## Checks from direct executable ChatGPT source
- **26 unique flat parts: 21×6mm + 5×4mm**.
- **22/22 self checks PASS**; 441/441 rigid 2.5D sampled angles 0–110° show no intersections; 0 overlap at0/55/110 snapshots.
- **2×81=162** partial saddle insertion samples clear; **131** rigid lid-drop positions clear before wooden pins / outer veneer; reverse movement demonstrates lack of self-lock and STOP on mechanical strength claims.
- **15/15** same-author *second-method* DXF reads pass: 26 individual source outlines vs DXF entities, all nest DXF contours, sheet bounds, pair distances, intended slit counts, negative control with changed geometry.
- Clean-directory rebuild PASS with **39** .py/.svg byte-identical and **28** .dxf geometry-equivalent files by canonical modelspace entity comparison (DXF raw bytes differ in generated metadata/handles). This is not independent QA.

## Geometric contour nesting (DESIGN_ONLY; NOT cut-ready)
- 1 board 6mm (21 components), stock440W×800H, actual net material area25.43%, minimum contour gap4.39997mm.
- 1 board 4mm (5 components), same stock, area15.34%, minimum contour gap4.4mm. **209 UNVERIFIED zero-width kerf CENTERLINES**, not a demonstrated feasible 4mm wood-bend pattern.
- Full Python sources, part DXF/SVG, sheet DXF/SVG, diagrams, results, manifest, Hebrew delivery in user's conversation attachment **`MEB015_J3_H1_TO_NESTING_DESIGN_ONLY.zip`** SHA256 **`739affefc37dd096be1e5e45733d03c2f3a2e63a322e9643adf6897e7f70511c`**, 77 files; **ZIP itself is NOT committed to GitHub**.

## Strict blockers before production
Bonded end cheek ↔ socket ↔ saddle and saddle/rail shear unproven (not mechanical self-lock); 2.1mm roof-capture lip timber strength; 4mm birch full curvature physical kerf-bending and neutral-axis; measured real kerf and thickness; 26-part true physical assembly and working pin; owner visual approval of 354mm outer/side boss; independent QA. **G2 PARTIAL_CAD, G3 NOT_RUN, G4/G5 NOT_APPROVED. No merge/release.**


## Repository source custody
The following source delta is committed separately in this branch. All inherited build files and generated cut profiles are in the named owner ZIP only. Independent QA requires that handoff. This document by itself cannot validate physical strength.
