# PST-310 Modern V4 — precision tab, mortise and half-lap core | DESIGN_ONLY

## Confirmed owner decision (2026-11-04)
Owner permits **recutting both top and bottom Ø310mm discs** to provide physically interlocking structural connections rather than preserving an uncut pre-existing disc. Maintain final diameter310mm, total tabletop box height60mm, stand height550mm, three 120° legs and the owner-approved modern engineered leg profile.

## Datum (mm from floor)
- Lower 6mm disc: Z490..496
- Core webs and 4mm rim body: Z496..544 (**48mm high**)
- Upper 6mm disc: Z544..550
- Under-disc spider: Z484..490
- Lower triangular bracing: Z155..161
- Three double-layer 6mm birch legs at 0°/120°/240°; six radial 6mm core webs at 30°/90°/150°/210°/270°/330°.
- Six nominal 4mm shell sectors, 60° each; current bent CAD does not reproduce cut-line flexing or validate closure.

## Controlled joinery generated from common parametric dimensions
1. **Upper disc**: 12 through mortises (2 per radial web), 12 open-edge scallops to receive the flexible rim fingers. 12 closed face openings => 13 planar face wires including the outer contour.
2. **Lower disc**: same 12 web mortises and 12 rim scallops plus 6 through mortises (two per double-thickness laminated leg) => 18 closed face openings and 19 planar face wires including outer.
3. **Each of 6 radial core webs**: 2 top fingers and 2 bottom fingers, projecting 6mm into the respective discs; two radial finger spans 69–89mm and112–132mm, nominal 6mm plywood thickness, provisional +0.16mm clearance per side in plate slots.
4. **One central vertical ring**: six complementary bottom-open half-lap cuts at the web/ring junction, with web cutouts open from above. This makes an actual designed interlock, not a coincident solid.
5. **Legs**: three double-laminated 12mm legs connect to the existing spider and through the lower disc using upper finger spans 91–110mm and **121–140mm**. The outer finger pair was moved inward 8mm from the original V3 span129–148mm. Matching spider and lower-disc mortises were generated together (+0.18mm per side nominal). Nearest nominal remaining material from outside leg slot to disk radial perimeter ~14.7mm before considering nearby notches.
6. **Rim**: each of six nominal curved sectors includes two top and two bottom 12mm arc-length finger tabs. Matching disc edge scallops are generated; manufacturable flattened 4mm kerf-line slots and closure calibration remain OPEN.

The design differentiates *tab-and-slot mortise* from the usual visible long-edge alternating *finger joint*: these are positive, integral tab/mortise and half-lap joints, not merely decorative lines.

## Quantitative CAD validation performed in ChatGPT
- **26 OpenCASCADE BREP solids valid / STEP exported and 26 solids successfully reimported / 26 GLB meshes reimported**.
- **325/325 nominal static pair checks**; 0 overlaps >0.005mm³; of these 216 disjoint pairs were culled by conservative bounding boxes before Boolean evaluation. The remaining pairs were tested by actual Boolean intersection.
- **31 sampled Z offsets** for seating vertical central ring to radial webs: 0 >0.005mm³ volume collisions.
- **16 sampled Z offsets** for upper disc to radial webs: 0 collisions.
- Engineering design correction count: **1** (outer leg finger pair shifted inward 8mm, all mating slots regenerated, full collision and serializations checked again).
- A separate exploratory full-rim / all-leg motion-validation calculation exceeded compute budget. Its outcome is **NOT_RUN / NOT VERIFIED**, and must never be reported as PASS.

## Deliverables and current source locations
Generated locally in ChatGPT:
- `PST_310_MODERN_V4_FINGER_JOINTED_FULL.step` (26-solid assembly)
- `PST_310_MODERN_V4_HOLLOW_TOP_ONLY.step`
- `PST_310_MODERN_V4_FRAME_ONLY.step`
- `PST_310_MODERN_V4_FINGER_JOINTED_FULL.glb`, exploded GLB
- `parts_STEP/`: 26 individually exported STEP objects
- `build_pst_310_v4.py` (full parametric CAD source), `render_pst_310_v4.py`
- engineering CAD preview images, `BOM.csv`, `QA_REPORT.json`, `README_HE.md`
- `PST_310_MODERN_V4_PRECISE_JOINERY_CAD.zip`: 43 files, tested `ZipFile.testzip()==None`; SHA256 `6b24de730ae38b169d598a29f26e501c3088acf07db5fa6c869b8b0ed455526a`.

**Important:** Binary STEP/GLB/ZIP and source script have been delivered as downloadable conversation attachments, **not uploaded to this GitHub branch**. This PR includes only the design log and QA description, NOT the model itself. Do not pretend GitHub holds the full reproducible build.

## Hold gates
- **G1 candidate design**: reviewed parametric nominal contact geometry, closed slots and half-laps, qualified nominal collision and serialization checks above.
- **G2 assembly route: HOLD** until all three legs, bottom spider/brace, two plates and six flexible rim sectors have a complete continuous and practical insertion/gluing order. Nominal 1D ring/top insertion alone is insufficient.
- **G3 physical/material: HOLD** measured birch thickness, laser kerf with coupon fit, nominal 4mm shell bend (4mm slot pitch single-line only), rim length overlap calibration, sufficient glue areas and stability under pot+soil+water loading. Wetness and surface protection needed.
- **G4 cut release / DXF/SVG / nesting: BLOCKED** until above engineering/physical gates. Stock reference 800×440mm, kerf/nesting gap user pref 1mm subject to laser trial.

LEAN TASK PLANNING: ChatGPT preferred for parametric CAD updates and bounded tests. Escalate to Codex only if broad repeated continuous motion or integrated regression suite needs long-running repository environment; physical load tests cannot be substituted.
