# CTB-01 — bonded P01/P06 coordinated local CAD source candidate v1

**Date:** 2026-10-21 · **Status:** `DESIGN_STUDY_ONLY / GEOMETRIC_2D_SCREEN_PASS / NOT_APPROVED_FOR_G2b_G3_G4_OR_PRODUCTION`. **Priority:** P1 inputs for CTB-009 P0.
**Architectural owner approval:** every appropriate joint may be **permanently bonded**, including P06↔P01 and upper P01↔P04/P05/P07 load-path interfaces. No need for a disassemblable free key; this is NOT passing adhesive, durability, fit or strength tests.

## Exact versioned outputs — isolated study, not production exports

1. `P01_BONDED_UNIFIED_V1_DESIGN_ONLY.svg`: **ONE authoritative study profile** to represent all **SIX IDENTICAL** P01 cheeks. Uses the original selected `P01-Y-mortise-study-v1.svg` polygon outer silhouette and original five P02/P03 cutouts **unchanged**, adding one closed nominal `26.4×6.4mm` rounded R0.2 mortise at `r=112.017645918429, Z=245`, extents `r=98.817646..125.217646, Z=241.8..248.2`. Six identical rotated placements at leg angles 0°/120°/240°, two cheek sides per leg, to be verified in eventual 3D integrator.
2. `P06C_BONDED_V1_DESIGN_ONLY.svg`: retain **exactly** first two original `P06C.svg` cut polygons (outer ring + central opening), **omit six obsolete C keeper openings**. Frozen C 6mm stock, Z242..248, all original ring external arm/terminal geometry kept. Does **NOT** incorporate wider C2 terminal; C2 had5.2mm free cheek spread and its free keys were rejected.
3. `P08_BONDED_DUAL_DISK_V1`: zero new wooden bodies; reuse **original** P01 upper tongue & selected P04L/U slot geometry unmodified for conceptual adhesive load path (P04U→P05→skins needs separate proof). Not a file in this candidate.

**Provenance:** base `parts/P03/variants/A_COMPACT_CLOSED/P01-Y-mortise-study-v1.svg` blob `b6bc8c67cae188960e2ab0e5835449e80f4d1d1e`; original `parts/P06/variants/C/P06C.svg` blob `51dd2f4ff5b981bab4fc6c323991be4e3990729eddbfbe76f728606b3937d29b77b07544e5c723c` (the valid Git content blob is listed in the QA evidence; the MD source here intentionally avoids claiming 3D regenerated CAD provenance). Current P04 L/U and P05/P07 sources do not change.

## Independent scoped JS geometry and consistency recheck

**17/17 checks passed after ONE test-script-only correction** (first read had false flags from a JavaScript polygon equality/reference/area calculation bug; **0 SVG geometry repairs**, no Codex use):
- Seven P01 closed outlines = one existing outer + five unchanged existing P02/P03 holes + new closed mid C mortise. Source-to-study **vertex-by-vertex exact preservation** of all six earlier loops.
- Two P06 loops = original outer + central hollow exactly preserved vertex-by-vertex, against original eight loops (six obsolete key openings omitted).
- New mortise R0.2 polygon is simple, non-self-crossing, bounding extents26.4×6.4mm, nominal polygon area≈**168.924858mm²**. It does not cross the original exterior or five old mortise polygons.
- Independent minimum **sampled vertex-to-original-edge** distance from new mortise to P01 exterior ≈**10.96395mm**; separation to nearest prior mortise≈**38.65287mm** by same screening technique. These are **polygon sample-based ligaments, not rounded 3D load strength or full clearance certificates**.
- Original P06 ring net polygon area≈**10,018.08661mm²**; proposed ring without six small holes≈**10,278.99575mm²**, difference **260.90914mm²**, consistent with six≈43.48486mm² former holes. Added material restores local ring section; does **not** itself increase bonded P01 contact area.
- Both files are unapproved study profiles, protected original CAD unchanged. They are not released cut profiles, production nesting, kerf compensation or a manufacturing BOM.

**Nominal interface only:** P06 ring tab r-span26mm; proposed P01 female radial span26.4mm, yielding0.2mm geometric air on each radial edge. 6mm ring Z242..248 within proposed P01 slot Z241.8..248.2 likewise leaves0.2mm air each axial side. These margins are **not** adhesive-qualified. Existing face projection estimate: per cheek approx156mm² for one horizontal ring face, twice≈312mm², all6≈1872mm² POTENTIAL facing-area projection — **not actual wet bond/contact, bearing or load capacity**.

## Coordination and assembly dependencies

- The previously recorded P06 original ring C conditional **Y_FIRST early ring** route passed34 steps/595 focused swept checks **on a conditional P01 C-mortised source with six C key holes**; that historic source and keys are different. Removing keeper-hole voids adds P06 material **within the P01 C-mortise r/Z envelope**, so for the documented straight cheek transverse translation no new moving cheek-solid overlap is expected, but **no fresh complete swept-kernel test has been executed**. There may be other assembly-stage clearance, fixture, tolerance or glue access changes requiring a new focused check.
- P07A existing geometry/31-body layout unchanged by merely annotating P04/P05 structural bonds. Add ONE ring body, *replace* six P01 cheeks with same quantity/versioned profiles and add ZERO P08/key solids ⇒ proposed full table **32 wooden bodies**, excluding adhesive, fixtures, or later reinforcements. Not yet a geometrically G2b-approved or physically fitted whole assembly.
- Proposed sequence constraint: temporary ring positioning before `Y_FIRST` cheek assembly, core bottom skin before P04L/U, P05 before exterior rim close, top P07T after qualified bonded operations. This is **a design precedence graph**, not glue application instructions, a proven cure sequence or full virtual assembly pass.
- `P01` profile is ONE source for all six cheeks; do not separately patch new mid-ring slot into six independent file copies or merge the rejected P08 1.4mm-roof slotted tongue. Upper tongue remains unchanged.
- Any functional contract IF12/B01 should be formally reviewed as `PERMANENT_BONDED_WITH_QUALIFIED_STRUCTURAL_RETENTION` replacing free mechanical keeper, while `IF09/B05` requires successful bond qualification; document CR before claiming an interface PASS.

## Remaining gates and next smallest executor

**ChatGPT:** performed both versioned digital profile derivations and 17 geometry consistency checks. Prepare one consolidated source/CR matrix and report partial G2 nominal status. Before any new Codex run, perform source-level checks on P01↔P06 slot/gaps, P04 L/U original contacts and unaffected geometry.

**Codex only when needed:** true 3D finite-body reassembly on **ONE changed P01↔P06 C ring local joint** (static fits, radial/tangential/axial path, no new P01→P02/P03 conflict), then a focused changed-interface integration if local check is admissible, rather than rerunning every prior P07A case. One draft PR/one JSON witness; STOP on blocker, MEDIUM initially, HIGH for geometric sweep if required. No production nesting or render suite.

**Independent material & structural acceptance is separate and cannot be inferred:** adhesives for real plywood, measured stock/kerf/bond line, longitudinal cheek stability, shear/peel under real loads, P04U→P05→P07T positive structural continuity (8mm U-to-top gap), P05→P07 skins/rim, table stability, real bend/physical G3 and final production G4. User's earlier **P06 bond-passes assumption is for design planning**, not a test record or an overall table safety signoff.

**Gate state:** `P01_VNEXT_PROPOSED / P06C_BONDED_V1_PROPOSED / OWNER_PERMANENT_BOND_OK / IF09_IF12_FUNCTIONAL_QA_OPEN / G2b_NOT_RUN / G3_G4_NOT_APPROVED`.
