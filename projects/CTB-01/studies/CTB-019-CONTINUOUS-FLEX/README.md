# CTB-019 — continuous kerf-flex, rim-only replacement (DESIGN_ONLY)

## Context
User cut CTB-017 plywood 6mm pieces and current rim P07R1/P07R2 4mm, and reported insufficient rim flex. CTB-018 alternated open kerfs but **omitted entire kerf rows** in the narrow regions of the six upper/lower skin notches (visible ~28mm gaps). CTB-019 reinstates a continuous alternating row sequence through those regions, with local slit shortening rather than row omission.

**Only P07R1/P07R2 flex pattern changes.** 6mm skin, leg, web, hub and other already cut components remain exactly untouched.

## Geometry
Nominal 4mm birch; each rim master keeps the **exact original CTB-015 outline** (76 vertices; includes all puzzle heads/necks and 6 notch zones on both edges). Source nominal local bounds X 0..50mm, Y -7.8..543.695529mm, full outside envelope **50 × 551.495529 mm** including puzzle features.

Main bending body: **132 rows, at Y=8,12,...,532mm (4mm pitch, absolutely no omitted rows)** per rim.
- A rows (66): one open line X=4..46 (42mm) in full-width region; **X=10..40 (30mm)** inside a narrowed notch.
- B rows (66): **two** open edge-origin lines X=0..20 and X=30..50 in full-width region; when notch width is narrowed by 6mm at each side, **X=6..20 and X=30..44**. Center remains10mm uncut on B rows.
- Notch y-bands: 39..51, 129..141, 219..231, 309..321, 399..411, 489..501mm. Exactly **18 rows** are adapted across these regions.
- Y beyond 532 or below8 belongs to end/seam safety land rather than the bendable main body. The puzzle profile itself is not slotted.
- Individual kerfs are **open zero-geometric-width line segments**, not the old closed0.8mm rectangles. Physical laser kerf is nonzero and uncalibrated.

## Deliverables
- P07R1_CONTINUOUS_FLEX_DESIGN_ONLY.svg/.dxf
- P07R2_CONTINUOUS_FLEX_DESIGN_ONLY.svg/.dxf
- BIRCH4_S01_RIMS_ONLY_DESIGN_ONLY.svg/.dxf — replacement-only **440×800mm** 4mm nesting, original offsets P07R1=(10,20), P07R2=(65,20), no sheet outline included among vector cut paths.
- ZIP includes six vectors (two masters and the rim-only sheet); does NOT include any already cut 6mm parts.

## Bounded QA (performer check, not independent G3)
- P07R1 and P07R2 outer SVG outlines equal the original CTB-015 outer contours: **2/2 exact**.
- New nested rim outlines match the old CTB-017 4mm nested outlines without even a coordinate adjustment: **2/2 exact**.
- 132/132 rows per piece; every consecutive row pitch equals4mm, zero gaps; 18/18 rows inside notch bands retained and shortened. Each rim has 198 single-pass open cuts (66 A +132 B edge cuts).
- For all396 open segments across both rims, horizontal cross-section of the source outline was checked: **0 exits through solid/exterior** beyond the expected edge-endpoints; at B rows cuts meet the perimeter deliberately.
- SVG vs DXF exact numeric coordinate, entity-type and closed-perimeter comparisons: **3/3 pairs PASS** (two master pairs and one nested sheet pair). The nested sheet has2 closed outlines+396 open LINE entities, and no reference rectangle.
- No other project geometry edited. Source polygon repair counts:0. One design iteration; 39 previously omitted V2 rows restored (132 vs93), 59 additional cut lines per rim (198 vs139).

## Open physical/engineering gates
- **NOT FOR FULL-SCALE CUTTING / DESIGN_ONLY.** Edge-origin kerfs cut into both outer rails, including 4mm-pitch rows near notch zones and seam lands. Local bridges/wood-grain, laser process, minimum ligament strength and 3D bending response are **not qualified**.
- The CTB-015-B1 inherited vertical assembly route still collides; this slotted alternative has not been shown to permit safe complete assembly. User's neck-strength assumption is not a validated material property.
- Recommendation: short test coupon of same material with several notch analogs; check R173 bend, cracks and dimensional retention before replacing both full rims. Independent standard ezdxf audit & full physical tests remain NOT_RUN.
