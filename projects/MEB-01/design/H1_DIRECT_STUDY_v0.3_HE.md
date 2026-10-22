# MEB-01 A1/H1 — ChatGPT direct study v0.3 (20 Oct 2026)
**Stage:** DESIGN_ONLY · **No Codex** · **SELF_QA_PASS / INDEPENDENT_QA_PENDING** · Related Issue #26 / Draft PR #27.

## What actually changed from v0.2b
- 26 CAD 3D bodies representing flat 6/4mm sheet profiles and an **idealized, formed** 4mm arched lid skin. This 4mm skin is **not** a finished laser-kerf pattern; MEB-B12 thin outside ligament (~0.10mm in V8.2.2) remains OPEN.
- Two long rails are flat 6mm-Y-thick X/Z contour parts with laser-profiled 6mm half-lap mortises and end tabs.
- Two arched internal ribs are flat 6mm-X-thick Y/Z contour parts with mating bottom-open half-lap mortises.
- Two concealed side socket laminates incorporate the rail pockets.
- Four previously non-stock-thickness cheek bridges became 6mm-Y-thick **X/Z-cut** spacer pieces, nominal 7mm overall reach along X (a 7mm bridge does **not** require 7mm thick plywood).
- Two pins are designed as 2×6mm Ø7 plywood discs plus 4mm Ø13 heads. Axial insertion demonstrated at ideal geometry; shaft/cap adhesives and retention **unverified**.
- The revised axial stack gives **0.5mm nominal CAD clearance** between rotating end cheeks and stationary neighbouring faces.
- Outer X envelope nominal **346mm** versus legacy 322mm, nominal interior X between end cheeks **312mm** vs 310mm legacy; both **PROVISIONAL**, require owner dimension/aesthetic acceptance.

## Exact bounded evidence from local versioned ZIP
Created in ChatGPT environment and delivered to user as `MEB_H1_A1_v03_DESIGN_ONLY.zip` (**69 packaged files**, ZIP integrity PASS), SHA256 **1a1168a3e66f330d5061da6146603f75497a4d764dfd6ee13937ba5652be5f8d**.

Actual contents include:
- reproducible source `build_v03.py`, `export_v03.py`, `sweep_v03_fast.py`, `qa_v03.py`, `render_fast_v03.py`;
- 25 **DESIGN_ONLY** individual laser-flat reference `DXF` profiles and 25 paired `SVG` profiles, plus one **SVG-only** unrolled 4mm skin *blank placeholder* (no real kerf pattern);
- 2 GLB assembled 3D scenes (0° and 110°), CAD-derived section/open/closed projections, provisional stock rectangle diagrams and BOM;
- 441-row angle sweep CSV, JSON evidence and Hebrew engineering delivery report.

**Scope qualification:** These binary scenes, drawings and Python files are **not in this GitHub PR**, only in the ChatGPT conversation ZIP. This Markdown file is the truthful GitHub-side pointer to their existence; do not claim GitHub host contains their bytes.

## Test outcomes
- **40/40 distinct ChatGPT SELF checks PASS**, **independent QA NOT_RUN**.
- Rigid-prismatic moving/static sweep at 0–110° / 0.25°: **441/441 zero volumetric collisions**, smallest sampled model gap **0.500mm**, conservative model-only unsampled-pose lower-bound **0.3362845mm**.
- All **26 component** volumetric intersections checked at 0°,55°,110°: **0 overlaps**.
- Partial assembly/insertion sequences sampled: 2 rail slides at 121 each, 2 right-side panel slides at 121 each, 2 cross ribs lowered at 51 each, 2 assembled pin placements at 121 each; no volumetric interference. **This does NOT validate a complete 26-part assembly sequence**.
- **25/25 DXF** cross-read geometry/closed loops/units, **26/26 SVG** XML parse, both GLB 26 watertight components/positive volume with model-origin source volume match.
- Separate 4mm and 6mm **bounding-rectangle** sheet feasibility diagrams inside OWNER FROZEN **800mm HEIGHT x440mm WIDTH**, with margins; **not validated part-contour production nesting**.
- Negative geometry cases intentionally failed (oversized pin, too-high tab, undercut half-lap).

Two geometric repair cycles were documented while converging to v0.3 axial stack (cap-lid interference; material-thickness-unrealizable bridge); see Hebrew report in ZIP. No original V8.2.2 source changed.

## Hard blockers preserved
1. Smooth curved shell assumes bent 4mm stock; actual kerf pattern, tabs, strength, and legacy MEB-B12 failure NOT_RUN.
2. Actual plywood measured thickness, kerf, glue/bearing fit, shaft retention strength and endurance NOT_RUN.
3. Full body joinery (including finger-joint reconstruction) and end-to-end 26-body insertion path NOT_RUN.
4. Body proportions changed, owner decision required before G0/G1 freeze.
5. Independent QA pending. No production-ready DXFs, laser plan, G2b assembly, G3 prototype, G4 manufacturing authority.

**Recommended performer next:** ChatGPT for real kerf-bending lid and joint design candidate; optionally Codex only if a larger parametric CAD framework has clear advantage; separate QA verifier.
