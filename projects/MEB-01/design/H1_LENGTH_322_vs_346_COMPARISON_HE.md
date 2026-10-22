# MEB-01 — H1 length decision study: 322 mm vs 346 mm (2026-10-20)

**Status:** `DESIGN_ONLY / EXTERIOR_DIMENSION_NOT_FROZEN / INTERIOR_MIN_310MM_OWNER_APPROVED`. Comparison performed directly by ChatGPT from local H1 v0.3 geometry source (`build_v03.py`), BOM, flat exports and rectangular stock-pack proposals. No Codex used. **After the comparison the owner required preserving minimum usable interior length 310mm (MEB-D-008). Neither exterior length is owner-approved yet.**

## Verified reference data (model-nominal, not measured physical geometry)
- H1 v0.3 exterior X-envelope: **x=-5..341 mm**, total **346 mm** (outer facia extremes).
- Nominal clear length between stationary body end cheeks: **x=12..324 mm**, total **312 mm**. Actual unobstructed completed box must still be verified.
- A pair of side/end assemblies together consumes **34 mm** of total X-length (17 per side). Original legacy V8.2.2 conceptual body: **322 mm exterior and 310 mm nominal interior** (12mm total) using a different outer design, not the current H1 axial stack.
- Owner-FROZEN constraints remain **800mm HEIGHT × 440mm WIDTH cutting sheet** and **110° required opening**. Product materials 6mm structure and 4mm formed skin remain nominal/provisional; completed 4mm kerf design is not available.

## Options
| Variant | External length X | Internal length X (nominal) | Side-stack budget | Mechanical status |
|---|---:|---:|---:|---|
| A — Keep current H1 v0.3 | 346 | 312 | 17mm per side | 26-solid research model, not G2/G3 validated |
| B — Compress center length keeping H1 end design | 322 | **288** (312-24) | 17mm per side | **Concept only**; must shorten 4mm skin, rails, front/back/floor and move ribs; full motion and joinery rechecks required |
| C — Retain legacy interior and compact overall | 322 | **310** | 6mm per side | **Redesign only**; requires removing ~11mm external stack per side or changing internal pivot architecture, redoing hinge attachment/retention and checks |

External 346 vs322 difference **24mm (7.45% relative to 322)**. A with body width approx77mm is L/W **~4.49**; B/C with 322 is **~4.18**; this is comparison of nominal body width only, not assembled hinge projection. The visual style choice A1 is independent of these numeric options and must not be confused with exact mechanical approval. External 346 yields a more elongated/engraving-friendly front, 322 more compact; both can appear harmonious.

## Function
- A preserves or exceeds historical **310mm nominal** axial cavity by 2mm.
- B reduces nominal cavity **22mm below legacy 310mm** and **24mm below v0.3 312mm**, which may prevent fitting the intended scroll. **Actual scroll rolled length and required handling allowance UNKNOWN**.
- C preserves 310mm only if an **unproven reengineered hinge stack** achieves the total 12mm exterior-to-interior difference. Do not presume this is mechanically or aesthetically feasible with the selected recessed wooden hinge.

## Manufacturing
- v0.3 currently generates **25 nominal 2D DXF / 25 SVG**, plus 4mm **SVG-only skin placeholder** without kerf details, and 26 solids. Reference rectangle packs place 21 × nominal 6mm profiles on one 800×440mm sheet and 5 × nominal 4mm patterns including placeholder on another, under model margins; **BBOX_ONLY, not contour nesting, not production proof**.
- The individual elongated 346-variant patterns are generally much shorter than 440mm stock width (e.g. front body 312mm, nominal rail bbox322.4mm), but assembled 346mm dimension is not the same as the longest cut piece.
- Reducing box length to 322mm potentially reduces long-part area and skin width by up to24mm if end stacks are retained. No evidence of reduced sheet count (probably still two material thickness categories). All DXFs, BOM and nesting must be regenerated for a new variant.
- MEB-B12 ~0.10mm original thin web, formed-skin kerf pattern, actual plywood thickness, adhesive/pin durability, full assembly path and independent QA remain unresolved regardless of length.

## Engineering recommendation — NOT a decision
Prefer **A: 346mm as temporary working length**, because it keeps nominal cavity ≥310mm and preserves the existing H1 pivot/stack concept, avoiding an unsupported mechanical redesign just to save24mm. This is a time-to-next-validation/functional-risk preference, **not proof that its look or mechanical function is best**.
If compactness is a strong aesthetic constraint, model variant **C (322 outer, 310 inside)** *before deciding*; do not silently accept variant B's 288mm cavity until physical scroll length is measured.
### Required to freeze length
1. Owner selects target outer length and acceptable appearance/projection.
2. Measure actual intended Megillah rolled scroll length and required placement/removal clearance; verify usable cavity physically at G3.
3. Resolve and independently rerun CAD, motion, joints and real 4mm kerf-skin interface, and full object envelope/stock layouts.
4. QA quality warning: an **older** generated `diagnostics_v03.json` says minimum moving gap `0` whereas later current-version `sweep_v03_summary.json` and 441-row CSV report `0.5mm`; timestamps indicate they were generated at different source revisions. Treat this as **stale/reproducibility discrepancy to clean** before citing uninterrupted motion verification outside the bounded current sweep. No QA independent review. Do not freeze/merge on stale logs.

**Executor:** ChatGPT for comparison, 322 alternative concept and dimensions; Codex only if complex parametric restructuring clearly saves work; independent QA reviewer mandatory before acceptance. Prior V8.2.2 source untouched.

## Owner decision update — 2026-10-20
Owner stated **״לשמור על 310״**. Treat as **minimum 310 mm usable internal length**, including clearances for any installed end hardware and practical scroll accommodation; mere nominal open space measured between cheeks does not prove finished usability.

- **B: 322 outer/288 nominal interior — ELIMINATED** under new frozen functional requirement.
- **C: 322 outer/310 interior — NOT VALIDATED**, possible only through end-stack/pivot redesign; cannot be used until modeled and independently checked.
- **A: 346 outer/312 nominal interior — recommended temporary working candidate**; prove actual usable inside length >=310 after all hinge/retention encroachments. **346 external is not frozen or owner-approved.**
- Continue H1 lid/kerf design *conditionally* on working candidate A, do not silently lock exterior dimensions, and retain an explicit design review at next gate.
