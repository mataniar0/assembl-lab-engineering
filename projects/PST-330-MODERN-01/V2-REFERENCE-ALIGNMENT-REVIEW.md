# PST-330-MODERN-01 — V2 reference-aligned engineering CAD (2026-11-04)

## Target and preservation

User requested iterative self-checking to make the CAD assembly **closer to their previously approved photorealistic engineering-leg concept**, without modifying the already-cut Ø330mm circular top plate. V2 preserves three 120° radially disposed legs, overall H550mm, and laminated birch 6mm ×2 =12mm per leg. Top plate remains full/uncut, with a hidden support spider glued beneath it; thickness6mm is provisional pending measurement.

## Visual design changes from V1
1. Broader triangular shoulder, with a single purposeful angled elbow rather than narrow near-straight bar.
2. Prominent tapered triangular/diagonal through-window following leg's load path, bounded by nominal min ~8.976mm edge ligament.
3. Two additional narrow lower-leg through-slits per panel for similarity to the reference.
4. Lower triangular brace now includes three additional vertical edge-web panels (6mm birch) so the visible frame is deep rather than just a flat ring.
5. Lower brace frame lowered after visual comparison: horizontal triangle Z155–161, edge stiffeners Z136–155, matching solid support shelves in the legs at Z141–155.
6. Narrower underside ring on the concealed upper support spider; the pre-cut disc remains completely unchanged.

## Actual correction history — three cycles

- Geometry candidate #1: initial tapered aperture protruded beyond leg outer contour — **FAIL**. Corrected with inset body constraint; geometry contained and minimum cut-edge ligament 8.976mm — PASS.
- V2 render #1: external shoulder showed an overly sharp secondary zigzag — modified original outer profile and rebuilt full CAD; repeated intersection and serialization QA — PASS.
- V2 render #2: lower brace visibly higher than target reference — lowered frame 29mm and relocated integral leg shelf; rerendered and reran all model checks — PASS.

## Bounded quantitative CAD QA (final V2)

- **12/12** individual OpenCASCADE BREP solids valid, 1 solid per named assembly component.
- Components: original unchanged disc x1; leg laminations x6; upper spider x1; horizontal lower triangular ring x1; lower vertical side edge braces x3.
- **66/66** distinct solid-pair intersection checks, **0 volume overlaps above 0.01mm³** in nominal assembly pose.
- **12/12** STEP solids valid on reimport; **12/12** GLB geometries reimported.
- No production joint approval: test certifies only nominal geometric nonintersection and file validity, not continuous assembly path, physical thickness/kerf, gluing, pot loading, tipping, or wet resistance.

## Delivery

Full assembly STEP, frame-only STEP, per-part STEP, GLB full/frame/exploded, QA_REPORT.json, BOM, PNG side-by-side reference/V1/V2 report, source CadQuery script and Mac-compatible ZIP are **generated and shared as local ChatGPT conversation artifacts**; binaries and Python source are **not** committed to the repo by this update. An actual source-artifact upload is a separate action and must not be assumed.

**Status: DESIGN_ONLY — not for laser cutting, loading, or production release.** Next gate: measured 6mm plywood thickness, pot+soil+water max mass and pot base footprint, defined joint routes, retention, adhesive and stability checks, then pilot cutting.
