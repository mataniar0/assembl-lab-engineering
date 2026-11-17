# CRIB-01 · V0.6.8 — full 3D design study

**Status:** `DESIGN_ONLY / NO_CUT / NO_INFANT_USE / INDEPENDENT_QA_PENDING`. No manufacturing, infant use, sale, safety certification or verified structural joinery is implied.

## Baseline
- Owner-measured nominal mattress: **1200 × 600 × 150 mm**.
- Owner-approved overall height: **880 mm**.
- **Three-sided model:** unoccupied visual prototype only; not a safe sleeping arrangement.
- **Four-sided model:** future design illustration; not approved for infant use.
- Existing nominal plywood assumption: 10 mm birch. Real material, kerf, adhesive and load behavior NOT tested.

## Files

| File | What it contains |
|---|---|
| `models/three-sides-design-only.glb` | 108 wood meshes, original CAD millimeter coordinates |
| `models/four-sides-design-only.glb` | 137 wood meshes and 1 illustrative mattress mesh, original millimeter coordinates |
| `cad/three-sides-design-only.step.gz` | gzipped editable original STEP, wood geometry, not production-approved |
| `cad/four-sides-design-only.step.gz` | gzipped original STEP, wood geometry, not production-approved |
| `source/base-cassette-v067.step.gz` | base cassette STEP source dependency (33 solids) |
| `source/build_full_crib_3d.py` | historical V0.6.8 generation script; local absolute paths require adaptation |
| `qa/CRIB_V068_CHECKS.json` | author self-check evidence, **not independent QA** |
| `QA_REPORT_HE.md` | engineering limitations and context |

SHA-256 three-side GLB: `9b4a263f5b17e1a822013906bf5e952eb59ff95b8404dd4252f901c66b145014`  
SHA-256 four-side GLB: `1dc51b9de65b0a7693a006be09bb52e7f451473614109649fefe3f50af280cb2`

## Scale warning
These source GLBs preserve CAD **millimeter** numeric geometry, unlike glTF's meter convention. The ASSEMBL LAB website publishes separate web-viewer GLBs scaled by 0.001 (one CAD millimeter becomes 0.001 meters). No joint geometry was redesigned by that web conversion.

## Source reproducibility
The original generation script uses fixed paths under `/mnt/data` and needs CadQuery, trimesh, numpy, matplotlib and the V0.6.7 source STEP. Decompress `base-cassette-v067.step.gz` and adjust paths before rerunning in a different environment. Source and STEP re-export have **not** been reproduced from scratch by an independent reviewer in this PR.

## Unresolved P0 safety/engineering risks
- No verified continuous 3D insertion / retention for wall-to-post or slat-to-rail joints.
- No verified mattress-base structural anchors, strength, stability, or load path.
- No measured kerf, material tolerances, real wood test, or child-accessible opening/entrapment assessment.
- Fourth wall is conceptual only; all four walls must be permanently secure in any eventual validated use.
- No professional independent crib product assessment, G3 physical prototype, or G4 production release.

Tracked in [CRIB-066 #41](https://github.com/mataniar0/assembl-lab-engineering/issues/41) and independent CAD QA [CRIB-068 #42](https://github.com/mataniar0/assembl-lab-engineering/issues/42).

**This commit only preserves and shares a 3D concept study.** Do not use these files to fabricate an infant crib.
