# CTB-006R-GLUE — Phase A: permanent bonded P06↔P01 joint study

**Date:** 2026-10-21 · **Issue:** [#23](https://github.com/mataniar0/assembl-lab-engineering/issues/23) · **Priority:** P1 · **Executor:** ChatGPT (no Codex)
**Owner decision:** permanent non-disassemblable bonding of the mid-height ring is acceptable. This is **NOT** approval of any adhesive's strength, the existing joint, physical fabrication or production.
**Status:** `DESIGN_ONLY / CAD_2D_SOURCE_SCREEN_COMPLETE / ADHESIVE_STRENGTH_UNKNOWN / IF-09_OPEN / P01_P06_CR_REQUIRED`.

## Narrow technical decision

**Prefer one new candidate: `P06C_BONDED_TABS_V1`.** Retain the C ring's nominal outer contour/circular band and broad six radial terminals, with all six original 6mm P01 cheek profiles replaced by one *versioned* six-identical source with C closed ring mortises. Study direct structural adhesive transfer **P06 terminal ↔ P01 closed mortise walls**. The six free C/C2 keeper bodies are **removed from this candidate**; simply gluing the existing C2 keepers is not adequate, since PR #43 measured **5.2mm free cheek travel even with a key artificially fixed**.

For the bonded variant, propose removing six now-unneeded C ring key holes (no key keeper); do not overwrite currently selected files. With ring already present, preserve the previously studied Y_FIRST cheek-mortise insertion sequence as a **hypothesis requiring recheck** with new geometry; adhesive availability, fixtures/curing, actual fit and assembly accessibility are not validated. No hardware needed in this candidate. Ring is intended to join three legs, not act merely as ornament (frozen CTB-000 D007 intent).

## Source-grounded numbers; one compact independent 2D recheck

Read current GitHub **source exported polygons**:
- `parts/P06/variants/C/P06C.svg` blob **`51dd2f4ff5b981bab4fc6c323991be4e4ee872ea`**, eight loops (one outer, central hole, six key holes); C ring Z242..248, nominal6mm.
- `parts/P03/variants/A_COMPACT_CLOSED/P01-Y-mortise-study-v1.svg` blob **`b6bc8c67cae188960e2ab0e5835449e80f4d1d1e`**; current P01 profile has no P06 C mortise. The **proposed** C cutout is a rounded closed `26.4×6.4mm` at local radial r≈`112.0176459184`, Z245. Ring male tab nominal radial width26mm, Z6mm, hence theoretical `0.2mm` radial and Z air per side before tolerances or adhesive fill.

An independent JS polygon clipping calculation (not an external CAD-kernel rerun) rotated the real P06C SVG polygons to leg-local coordinates at **0°,120°,240°**, intersected each with the proposed C cheek-mortise radial envelope `[r0−13.2,r0+13.2]` and each actual 6mm-thick cheek tangential interval `[−13.5,−7.5]` / `[7.5,13.5]`, and subtracted all ring holes. **6/6 identical results: 156.000mm² projected ring-face area within each cheek thickness footprint.** Both horizontal ring faces => **312mm²/cheek nominal double-face projection; total 6×312=1,872mm² potential geometrical facing area**. This is NOT true bonded contact area; nominal 0.2mm vertical air at top and bottom means no direct zero-gap face contact, adhesive suitability and actual bond-line thickness wholly unknown. Moreover the ring face-to-cheek slot-wall joint is geometrically mixed wood face-to-edge, NOT a conventional verified lap bond.

Each original key-slot hole has SVG planar area≈`43.485mm²`. Eliminating **six** unused holes in the future version would restore≈`260.91mm²` of ring planar wood, from original SVG net `10018.0866mm²` to hypothetical simplified `10278.9966mm²` (before new 3D source recomputation). The six holes lie outward of the cheek footprint in the current geometry; their removal does NOT create new direct cheek bonded area or prove strength.

### BOM/source-scope accounting
Selected P07A pre-ring baseline has **31 actual bodies** (P01 six, P02/P02B twelve, P03 one, P04 two, P05 six, P07A four). Bonded candidate adds **one** P06 ring, replaces six cheek *geometries* rather than adding cheeks, and adds **zero** C2 keeper bodies => **32 actual modeled wooden bodies**, excluding adhesive layers / fixtures / any future P08 parts. This is only a proposed BOM, not an integrated assembly.

## Engineering limits and release gates

- Adhesive joint must be treated as a **permanent structural joint** with a verified load path, not simply as a locked friction key. Need actual interface area/contact, shear, peel and tension/cyclic/tipping loads, grain/orientation and adhesive/material compatibility to be qualified by a competent engineer and appropriate physical tests before use.
- `0.2mm` nominal slot gap is a CAD tolerance hypothesis, not an adhesive design gap, cured bond-line, fit or finished kerf. **Cannot conclude that common wood glue will reliably bridge these gaps**. Likewise zero finite-solid penetration does not mean bonded connection.
- Four P02 spacers/leg, P03/Y_FIRST, six identical P01 profiles, rim/upper P07A and P08 remain protected. `IF-09/B05` and full `B02` assembly are OPEN. Actual ring-before-cheeks insertion and adhesive process access have not been re-tested for this new simplified ring profile.
- Geometry screen shows a nominal facing-area opportunity **only**. Existing C key-slot holes are not approved to be filled in active source; filling them and changing P01 mortises both require versioned CR. Nothing here authorizes release G2b, measured physical G3 or production G4. No DXF/SVG production exports or cutting guidance.

## Exact next lean execution gate

**ChatGPT can perform:** this source evidence, candidate selection, topological BOM/CR and acceptance plan (DONE), followed by independent read-only QA of any generated CAD result. No repeated C2 anti-return simulations.

**Codex ONLY if owner/lead accepts this candidate for CAD study:** do one **local** P06 C-without-keyholes, one proposed ring terminal and one true P01 C-mortised cheek; build actual 3D finite solids and test **ring-before-Y_FIRST cheek insertion**, no modified collisions with original spacer/Y, and quantify *actual geometric facing land*, positive/zero nominal contact and any local intrusion after hole filling. Report one small `GO_GEOMETRY_ONLY` or `NO_GO`, exact CR changes and one local witness; STOP before six-way production export, full regression or glue-strength claim. **No need to model a glue polymer until a reviewed adhesive/material specification exists.**

**Decision still needed for functional acceptance:** an independent structural/adhesive qualification for the anticipated loads and bond-line conditions. User's choice to accept permanent bonding **does not resolve that gate**.
