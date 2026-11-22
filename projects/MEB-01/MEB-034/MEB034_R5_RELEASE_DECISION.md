# MEB-034 R5 — Engineering QA and production release decision

**Revision:** R5, 22 November 2026. **Status:** DESIGN_ONLY. **Production cut file approval: NOT GRANTED.**

## Verified in this iteration

- Exact DXF/SVG readback: **31/31 profile loops** and **88/88 R6 cut lines** match, within 1e-6mm.
- **Five separate 7.0mm fingers per roof short end**; first starts at x=328.000000mm and last ends at x=427.170854mm; front/rear profiles identical.
- Roof finger center stations (relative to x=328mm): **3.500, 18.746, 32.607, 76.959, 95.671 mm**. Arch notch centers (measured along chosen partial curved lip): **10.625, 21.625, 31.625, 63.625, 77.125 mm**. This correspondence is an affine construction between index stations, **NOT** a 3D manufacturing fit verification.
- **21 part groups / 210 potential part-pairs**, 2D outer profile clearances: minimum 1.000mm; occupied sheet bounds x=3..434.43446mm, y=3..437.69754mm inside 440×800mm.
- R6 line centers: minimum 8.585mm from other cutout outer profiles. Edge distance 15.35mm.
- Arch R4 check: all three existing holes per arch preserved; minimum nominal hole-to-outer contour 2.565mm, but no machine kerf, strength or functional joint verification.

## Critical incompatibility / why release remains blocked

1. Reference roof developed transverse dimension: **99.17085434mm**. Selected curved receiving rim arc length from CAD: **81.0386596mm**. They differ by **18.13219474mm**. The partial arch rim may not be the whole real contact surface; as-built roof-to-rim registration is unknown. **No claim that 18.13mm is a measured gap or that the two complete contact lengths necessarily ought to be equal.**
2. Although each arch has five 7.25mm receiving notches and each roof edge has five 7mm tabs, their actual positions in three-dimensional assembly have not been shown to mate. The normalized index mapping introduced in R5 does not resolve bending/contact length.
3. The front arch beginning cannot accept an unreinforced 4.1mm deep slot at the exact original curve endpoint. First R4 notch begins 7mm along the curve, avoiding the thin wedge; the owner asked for a finger at the start region. The unmodified rail mortises force nonuniform spacing.
4. Existing model V3 on the website is explicitly an unverified reconstruction, not a measured physical assembly. A correct digital assembly must separately model physical gap/overlap, insertion, 110° hinge motion, and beam mortises.
5. Material thickness, actual kerf, flexible hinge behavior, endurance, and joint retention have not been physically validated.

## Required gates to attain approval

- **G2 (CAD assembly):** establish a single verified datum and a full curved surface (including any front/back flats) for both lid ends and the roof skin. Derive matching tab-slot locations by true developed arc length and regenerate arch profiles, roof, and affected rail mortises simultaneously. Independent 3D collision, engagement and 110° sweep QA.
- **G3 (physical QA):** qualified fabricator provides measured plywood thickness and kerf, controlled fit coupon and bent roof/hinge evidence. Do not infer fit from nominal 7.0 vs 7.25mm drawings alone.
- **G4:** re-nest, re-run part, hole, slit, strength/material and independent file checks, then record formal product-owner production release.

### Repository
- R5 candidate SVG/DXF: `MEB034_R5_CO_REGISTERED_4MM_440x800_DESIGN_ONLY.{svg,dxf}`.
- Machine-readable report: `MEB034_R5_QA.json`.
- Earlier R1-R4 kept as audit history; R5 does not supersede engineering qualification.

**This report must not be construed as a guarantee of manufacturing fit.**
