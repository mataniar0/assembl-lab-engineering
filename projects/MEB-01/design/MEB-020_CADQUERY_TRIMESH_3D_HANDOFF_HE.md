# MEB-020 — CAD solid 3D handoff (CadQuery / Trimesh / Matplotlib / VTK)

**2026-10-26 · DESIGN_ONLY · ChatGPT direct, Codex not used.** This is the same 24-part glued-skin H1 research design, not a new product geometry or release. Original model source and last vector files unchanged.

## Construction
- Source: MEB-020 `build_variant_m020.py` and 24 underlying plywood part shapes.
- **CadQuery/OpenCascade** extruded each source-cut polygon with its actual assigned 4mm/6mm thickness; preserved inner bearing holes, finger-joint cutouts, H1 integral plywood shoulder pins. Two finite side-bond flanges were fused with the radial-shell skin as **one solid**, retaining 24 physical parts.
- 24 valid CAD solids; summed volume **752,073.1635 mm³**. Curved shell is a sampled source polyline surface, *not* newly fitted NURBS.
- 24 watertight Trimesh models tessellated directly from CadQuery BRep; exported two GLBs 0° /110°, plus one exploded GLB.
- Exported OpenCascade STEP assemblies for 0° and110°. Roundtrip reimport passed: **24 valid solids in each STEP, 24 watertight meshes in each GLB**.
- **CadQuery 3D BRep intersection test**, rigid moving vs static at0°,55°,110°: **0 penetrating pairs** among 12,6,6 bounding-box-filtered potential pairs. This is **only 3 poses** from CAD; 441-pose rigid sweep cited elsewhere belongs to previous 2.5D source model.
- Matplotlib did basic plots; polished 3D PNG previews produced from the same GLBs using VTK to avoid Matplotlib face-sorting glitches.

## User files
`MEB020_CADQUERY_TRIMESH_3D_DESIGN_ONLY.zip`, SHA256 **`443abefffd6b1f08ca597631cdf8efd9157fd6ca69147e1bb82b0a963f64e0a7`**, **128 archive entries**, ~6MB zipped. Contains CadQuery/Trimesh source, the complete model_source tree with DXF, both STEP, 3 GLB, three final preview PNG, material+collision QA JSON and README. ZIP itself lives in the owner's ChatGPT conversation **not Github**.

## Explicit hard limits
3D curved skin is the **ideal formed shell with no physical kerf cuts modeled in STEP/GLB**. The 188 theoretical kerf centerlines exist **only in flat SVG/DXF manufacturing-research files**. Real 4mm plywood kerf bending, glue strength, hinged wooden pin wear, free assembly path, tolerances and independent QA **NOT_RUN**. H1 bearing rear-wall relief and 354mm exterior not owner-frozen. This does not advance G3 or authorize G4/laser cutting.