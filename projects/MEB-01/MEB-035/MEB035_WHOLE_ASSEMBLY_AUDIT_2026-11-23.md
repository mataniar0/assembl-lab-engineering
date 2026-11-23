# MEB-035 / Issue #120 — Whole-assembly interface QA (23 Nov 2026)

**Gate decision: FAIL for drop-in compatibility; G2b/G3/G4 BLOCKED.** This report compares the newest five-part MEB035 R6-R2 lid study with the original MEB033 **4mm** product. This does not assert a physically validated whole assembly.

## Provenance
- Original SVG: `projects/MEB-01/MEB-033/cutting/MEB033_ALL20_PLUS_CURVE_R6_4MM_440x800_GAP1MM_DESIGN_ONLY.svg` (main, Git blob `8644b71371b5c4f02233b65d432ce22136e02199`).
- Candidate: `build_lid_study.py` and the R6-R2 5-part DXF/GLB delivered through the task's artifact bundle. Original geometry was re-read from GitHub and source datum/contours independently compared against candidate CAD parameters.
- Original inventory: **20 physical product parts + 1 single-curve jig** on a 440×800mm 4mm sheet. Candidate includes only **5 physical subassembly cut parts** and 15 GLB meshes (the latter subdivide ten fingers; NOT 15 cut parts).

## Nominal interface differences (source-relative mm)
| Interface | MEB033 | MEB035 | Difference | Status |
|---|---:|---:|---:|---|
| Hinge center along arch | 75 | 68 | −7 | FAIL |
| Hinge center vertical | 2.5 | 2.5 | 0 | MATCH |
| Hinge bore diameter | 8.4 | 8.4 | 0 | MATCH |
| First rail notch station | 32 | 26 | −6 | FAIL |
| Second rail notch station | 45 | 58 | +13 | FAIL |
| Rail notch center height (both) | 16.5 | −1 | −17.5 each | FAIL ×2 |
| Rail notch width | 4.5 | 4.3 | −0.2 | FAIL |
| Rail notch height | 6.5 | 7.3 | +0.8 | FAIL |
| Maximum arch rise | 23.434783 | 21.429271 | −2.005512 | FAIL |
| Original flat rail length vs proposed | 322.4 | 324 | +1.6 | FAIL |
| Original rail flat-profile height vs proposed | 11.843131 | 11 | −0.843131 | FAIL |

**Total: 10 inconsistent dimensional entries** (two rail centers are counted separately). These are intended proposed changes in some cases, but no compatible original body/hinge model or approved change request exists.

## Missing interfaces
- Original seven lid components included `LID_CROSS_RIB_1` and `LID_CROSS_RIB_2`. Both are **absent** from the five-part redesigned lid candidate. This is an incomplete structural/load-path comparison, not yet proof that ribs are indispensable.
- Existing box ends, front/back walls, bottom, fascia/backers, pin retainers and rail saddles are absent from MEB035 3D.
- Source model's assembly sequence and full **0–110° hinge sweep** were not tested.
- The newer circular arch changes hinge and mortise datum despite holding an 85.5mm chord. No proof of 3D compatibility with original body.

## New bounded 2D checks (actual newest DXF/GLB files)
- 5 cut parts; 11 contour loops including holes; 88 R6 cut LINE entities; 22 rows with 4 slits, 3 bridges of 4mm each.
- Front/rear skin tabs: **5 each, identical**. Minimum kerf centerline-to-tab-land distance **3.457286mm**, **nominal only**, not laser kerf compensated.
- 5-part 440×800mm nesting: **zero pairwise polygon overlaps**, minimum outline gap **8.0mm**.
- GLB contains **15 watertight meshes**, with 10 tabs split into separate graphical solids. This does not validate 20-part product integration.
- 22 R6 end segments have changed from the older physically tested R6 design; bending/fatigue in actual wood **NOT_RUN**.

## Decision / next required work
1. **No production cut or merge** of PR #121; Issue #120 remains open and in-scope G2b FAIL/BLOCKED.
2. Restore hinge local `(75,2.5)` and rail stations `(32,16.5)`, `(45,16.5)`, including original rail cross-sections, **or** authorize a formal Change Request and rebuild the matching body/hinge system.
3. Account for the two cross ribs with verified retaining interfaces or an explicitly engineered alternative.
4. Make a complete source-driven assembly of all 20 product parts; run continuity of insertion, full 110° sweep and clearances. Then re-nest all required components and independently audit.
5. For G3, test actual material thickness, cutting kerf, hinge strength and R6-R2 bending/durability. Require independent QA and formal G4 approval before any production release.

**Executor routing:** P1. ChatGPT: source inspection and 2D QA completed. Codex/CAD engineer: comprehensive 3D G2 redesign and regression recommended. Qualified fabrication professional: G3. Independent QA **PENDING**; do not describe self-review as independent.
