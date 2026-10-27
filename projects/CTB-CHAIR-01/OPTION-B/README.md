# CTB-CHAIR-01 — Option B V3, 60mm seat, 4-leg birch stool — DESIGN_ONLY

## Confirmed user choices
- **Option B** four-leg stool, round seat Ø420mm.
- Total height **450mm**; structural seat box thickness **60mm** (replaces V2 80mm and initial V1 50mm).
- Lower face Z390mm, lower 6mm skin Z390–396, upper 6mm skin Z444–450, internal radial webs 48mm tall.
- Four legs at 0°, 90°, 180°, 270°; 2×6mm birch cheek profiles per leg with 15mm nominal internal gap.
- Birch4 curved 6-segment rim, nominal inner radius206mm, mid radius208mm, outer radius210mm, height60mm.
- Eight radial webs, two interior horizontal rings (at Z404,428), sixteen leg spacers (four per leg), central four-way X4 connector and inter-leg tie ring.
- **44 modeled CAD solids**. New stool Ø420 design cannot reuse original Ø350 table skins.

## Latest CAD evidence — 2026-10-27
Generated **V3** locally in ChatGPT with Python / CadQuery 2.8.0 / OpenCASCADE / Trimesh 4.11 and exported:
- `CTB-CHAIR-01_B_V3_60MM_FULL_CONCEPT.step`
- `CTB-CHAIR-01_B_V3_60MM_SEAT_ONLY.step`
- `CTB-CHAIR-01_B_V3_60MM_FRAME_ONLY.step`
- `CTB-CHAIR-01_B_V3_60MM_FULL_CONCEPT.glb`
- two PNG previews, QA_REPORT.json, README.txt, and reproducible `build_ctb_chair01_b_v3_60mm.py`
- bundle `CTB-CHAIR-01_OPTION_B_V3_60MM_CAD_CONCEPT.zip` supplied in the current ChatGPT conversation.

**Important:** The STEP/GLB/ZIP and Python source are conversation artifacts and have **not** been committed to this GitHub branch. This version-controlled README is the authoritative decision log in GitHub.

## Checks
PASS (limited scope): 44 OCC solids valid; STEP exported and reimported with44 valid solids; GLB reimported with44 geometries; output ZIP passed `unzip -t`. This validates CAD serialization, not physical manufacturability.
NOT RUN / BLOCKED: 3D Boolean collision-free joint validation, complete assembly sequence, realistic cut mortises and finger joints, wood kerf calibration, gluing surface strength, calculated static/dynamic sitting load cases, tip stability, and physical prototype safety testing.

## Engineering safety boundary
This **is not a safe-to-sit or manufacturing-approved chair**. The 6mm cheek profiles were transformed from an earlier Trimesh *proxy*, not exact laser-cut contours; radial webs/rings have uncut intersections; four-way connector and feet remain conceptual; curved rim has no kerf slots or measured bend calibration. Increasing or decreasing seat box thickness by itself **does not demonstrate safe strength**. No human sitting tests should be conducted before competent design review and controlled non-occupant mechanical testing.

## Next task (LEAN TASK PLANNING)
Priority P1. Preferred ChatGPT with CadQuery: establish exact independent load path from the top skin through ribs, joints and four feet; replace proxy members with laser-accurate source geometry, design positive joints and clearance; run OCC interference checks; perform analytical or independent professional load/stability assessment and prototype testing. Codex only for necessary integration/test repetition beyond ChatGPT scope. Production DXF/SVG/nesting not approved yet.
