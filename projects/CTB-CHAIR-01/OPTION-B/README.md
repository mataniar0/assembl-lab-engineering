# CTB-CHAIR-01 — Option B, 4-leg birch stool — DESIGN_ONLY

## User selection
User selected **Option B**: a new adult-size candidate seat, Ø420mm, converted from the visual language of the 3-leg CTB-022 table. 4 legs, no backrest.

## Model CAD generated 2026-10-27, locally in ChatGPT (NOT committed as binaries here)
Python / CadQuery 2.8 / OCP 7.9 / Trimesh / VTK. Full assembly with **44 OCC solids**; exported and reimported STEP to confirm 44 valid solids. Interactive GLB reimported with44 components. Model and ZIP supplied in originating conversation; **the binary STEP/GLB/ZIP and Python source are local conversation artifacts and are NOT uploaded to this GitHub branch**.

## Draft parameters
- Outer seat Ø420mm, final seat level Z450mm.
- Box construction 50mm tall, lower plate Z400..406, upper plate Z444..450.
- 2 birch6 skins (new Ø412mm design bases; no legacy Ø350 skin reuse).
- 6 birch4 annular wall sectors, nominal inner R206mm, outer R210mm, midline R208mm; physical bend/kerf and segment closure uncalibrated.
- 4 double-cheek legs at angles 0/90/180/270 degrees, each with two parallel 6mm side cheeks and 15mm gap. Leg visual outlines adapted from an **existing CTB-022 proxy**, NOT from laser-accurate original cut files.
- 16 leg spacer plates (4 per leg), 8 upright radial seat webs, 2 interior seat ring ribs, central X4 connector and inter-leg stabilizing ring: altogether **44 modeled solids**.
- All design dimensions, offset profiles, contact interfaces and support structural paths must be verified and revised before DXF creation. No previous table 6mm parts should be assumed reusable.

## Evidence and acceptance gates
- **PASS**: 44 CAD solid entities; BREP geometry valid; assembly STEP reimport 44 solids; visual GLB reimport 44 meshes. Rendering of full stool and opened top completed.
- **PENDING**: CAD modeling of *actual manufacturing finger joints/mortises*, clearance/kerf adjustment, sheet nesting.
- **PENDING**: positive mechanical load path from seating surface to four legs, load cases for central and eccentric sitting, lateral forces, stability, glue bond/wet/aging strength and wood species/ply specification; independent simulation or mechanical design review.
- **PENDING**: destructive and nondestructive prototype structural/rocking checks by competent adult testers; formal furniture safety conformity if sold.
- **NOT ACCEPTABLE TO SIT ON**: no actual load safety proof, stress/deflection bound, standardized test or physical validation.

## Next task, LEAN TASK PLANNING
P1, preferred performer ChatGPT with CadQuery: rebuild legs, new seat reinforcement, connection between X4 and feet as manufacturable interlocking 6mm parts; add parametric clearances. Acceptance: joinery cut contours all generated from same source; BREP pair interference check under assembled nominal positions; complete cut-list and staged assembly pathway with candid blocked cases. Codex only if independent broad CAD integration or test automation needed. **Do not release DXF/nesting as production files until physical load validation.**
