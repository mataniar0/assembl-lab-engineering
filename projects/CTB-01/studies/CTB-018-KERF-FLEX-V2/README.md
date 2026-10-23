# CTB-018 — P07 rim flex V2 only (DESIGN_ONLY)

**Only rim parts P07R1 and P07R2 changed. All previously cut 6mm tabletop/core/leg/skin pieces are untouched.**

Two new vector masters per rim (`.svg` + `.dxf`) in this folder. Preserve the **exact CTB-015 contour** with both jigsaw seam features and all six notch bands on each side, but replace the 63 old **closed 0.8mm-wide rectangles** with a new series of **OPEN single lines** for each rim.

Nominal units mm; 4mm birch; developed rim width50, length follows 543.695529mm source. Flex pattern at successive row locations (nominal 4mm pitch):
- Type A: one center line from X=4 to X=46, 42mm.
- Type B: two edge-origin lines X=0..20 and X=30..50, 20mm each, leaving10mm central bridge.
- Start at Y16mm, alternating A/B; exclude all rows with |Y - 45,135,225,315,405,495| < 12mm to preserve the tabbed-skin notch zones. End at Y528mm to leave seam neighborhood intact.
- Each piece: 93 rows (47 A rows, 46 B rows) yielding **139 OPEN cuts**; one exact original closed perimeter in DXF and SVG. No rectangle perimeter reference. No 0.8mm slot geometry.

## Implementer verification
2/2 SVG outer point lists **exactly identical** to CTB-015 nominal outlines; 139 LINE entities per DXF and139 open SVG paths per rim; no new row violates stated notch-zone or end-zone exclusions. Existing source P07T/P07B remain unchanged. The old CTB-017 4mm nesting contains OLD rim contours and is NOT updated. No other project's DXF or SVG touched. Parser-based checks only; independent ezdxf audit and bend-fit qualification NOT_RUN.

## Critical physical limits
**Prototype only — not authorized for full-size production cutting.** The B-type cuts connect to each outer edge, intentionally interrupting the continuous side rail. In a bent 4mm plywood sheet these may crack/split, especially with grain orientation, laser kerf, near the puzzle neck, and skin-notch stress concentrations. The blank is not guaranteed to retain shape. Start with a SHORT sample of same wood and laser settings using this pattern; test curvature ~R173mm and identify cracking/flex direction before committing both full P07 rims. No physical bend test performed. Previous rigid-shell assembly closing motion already failed in CTB-015-B1: this unverified flexibility layout is not proof of an assembly route.
