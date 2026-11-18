# RR-001 R05 — geometry-repaired joint audit and 6mm cut-profile study
**Date:** 2026-11-18
**Status:** `DESIGN_ONLY / NO_CUT / NO_OCCUPANT_USE / INDEPENDENT_QA_PENDING`
**Linked:** [RR-001 Issue #117](https://github.com/mataniar0/assembl-lab-engineering/issues/117), [PR #118](https://github.com/mataniar0/assembl-lab-engineering/pull/118).

## Scope
A R04-to-R05 **design-only correction** based on source STEP geometry. R04 was not a single joined assembly: conservative AABB/proximity candidate analysis separated 105 solids into **four groups (87+16+1+1)**. R05 adds four rail-to-frame bridging plates with complementary nominal cheek receivers, replaces two non-sheet back rails by four 6mm laminations with end notches, removes two isolated brackets, reorients 10 side diaphragms as 6mm planar sheets, replaces four 2mm seat pads by 6mm sheets with a corresponding 4mm nominal seat-disk elevation, and adds clearance holes to two rear gussets.

### Reviewable geometric results (same-author tests, NOT independent QA)
| Check | R05 result |
|---|---|
| Re-imported STEP | 109 valid solids |
| Re-imported GLB | 111 mesh nodes |
| CAD candidate contact groups | 1 connected AABB/proximity-candidate group of 109; *not* a structural joint proof |
| Broad phase / 3D exact positive-volume overlaps | 56 candidate pairs out of 5,886 theoretical pairs; **0 positive-volume overlaps** after correcting two initial 360mm³ lower-back-bridge/gusset collisions |
| New bridge-to-rail/side nominal clearance | 12 tested relations, 0.15mm each; **not** positive retention |
| Planar 6mm single-sheet geometries | 107/107 plywood parts; source STEP face areas matched extracted 2D polygons |
| Individual 1:1 draft cut profiles | 107 DXF and 107 SVG; 145 closed rings including holes |
| Proposed 900H×450W stock sheets | 9 concept sheets in each format, **10mm nominal margins**, **4mm nominal contour spacing**; no kerf compensation or stock proof |
| Re-read DXF/SVG | 116 DXFs plus 116 SVGs parsed; same 145 rings, all within nominal margins |
| Negative-control checks | 6/6 detected planted invalid inputs |
| Independent design/engineering QA | **NOT_RUN** |
| G2 full swept-insertion + retention | **BLOCKED** |
| G3 physical / G4 manufacturing release | **NOT_RUN / BLOCKED** |

### Artifact custody
Full conversation artifact **not committed to GitHub**:
`RR001_R05_ENGINEERING_AND_CUT_STUDY_NO_CUT.zip` SHA-256 `9b0975502c396f9c1bc1ea3ac09b64da6456de0820e8d542d4c4e1f9bbc76091`.
Contents: R05 parametric source, STEP SHA-256 `9394f217ff0aa1bcb9a9f928b8fc67c5f800ca4f16b4b3a01bf6daa4b8b0f7fe`, GLB SHA-256 `6abc37716451b4ee16b2b1798eb306c438d9e1eaaac88f7167498753f8042c0e`, per-part drawings, nine-sheet layouts and detailed audit reports.

## Non-negotiable blockers
1. Actual natural seat and back wood discs never measured or strength-assessed, with visible cracks in reference photo. CAD cylinder sizes are assumptions.
2. Both wood discs remain **unretained mechanically**; R05 bridge FJs have nominal 0.15mm clearance and no anti-withdrawal lock.
3. Static potential contact and 0 volumetric overlap do **not** establish all physically load-bearing joints, insertion sequence, bonded-laminate fatigue or rocker structural safety.
4. Rocking with human occupancy: center of mass, forward/back and lateral tip risk, stops, dynamic loads and pinch points require qualified independent assessment and G3 physical testing.
5. 6mm stock, kerf, sheet margins and usable 900×450 laser area not physically calibrated; candidate DXF/SVG files are deliberately labeled `NO_CUT`.

## Next gate
Qualified engineer + measured real discs for G0 and safety concept, then truly captured disc joints and rocker runner cross-ties with full 3D swept assembly proof, calibrated physical samples, independent QA, and G3 before any G4 file release. **No cutting/manufacture/occupant use** from this design study.
