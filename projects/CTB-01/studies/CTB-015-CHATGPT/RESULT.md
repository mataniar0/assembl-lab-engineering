# CTB-015 — ChatGPT-first source repair / DESIGN_ONLY

**Status:** PARTIAL CORRECTION / 3D_REVALIDATION_REQUIRED / G3_NOT_RUN / G4_BLOCKED. Original source CTB-012 and CTB-013 unaffected. Stacked from CTB-013 draft branch; CTB-014 B1 NO-GO evidence in PR #58 is the input diagnosis, not a passed result for this candidate.

## Changes actually implemented
1. P07R1 and P07R2 source outer end contours: corrected developed half-length from 543.095529 mm to nominal π·173 = 543.495529071 mm by translating fourteen high-end contour points +0.400000071mm in unrounded math. Old end Y543.295529, new end Y543.695529 nominal. Original 63 cutouts per piece unchanged; source reinforced 18 slots/half preserved.
2. Re-exported the two changed rim masters as DXF with DXF R2000 `AcDbEntity` / `AcDbPolyline` subclass markers; previous CTB-013 DXFs missing subclass. SVG master outputs reflect corrected coordinates.

## Measured digital QA (implementer self-check)
- Two updated SVG files have 64 polygons each; each regenerated DXF has 64 LWPOLYLINE entities, proper `AcDbPolyline` entity subclass and closed flags. Round-trip read of raw tags matches corresponding SVG polygon vertices at 1µm coordinate tolerance: **2/2 PASS**.
- Endpoints verify max Y543.695529 for both parts; 63 kerf holes/segment still present. Corrections: one versioned length adjustment plus serialization fix, no existing approved masters modified.
- **NOT VERIFIED:** DXF loading through an independent `ezdxf` parser; complete polygon topology and geometric intersection of corrected head/female seam; 3D CAD full fit and insertion sweep; phase/skin registration; measured kerf, material, glue, bending or load.

## Known high-risk geometry
The former male/female puzzle-head contours are otherwise unchanged. Fixing 0.400000071mm nominal body length alone does not prove removal of the previous 0.071992mm³ per-seam 3D collision. Reciprocal edge still has zero machining allowance; real mating and assembly path are NOT_PROVED. The current closed shell / two seams MUST NOT be called a GO before independent CAD-kernel validation and design revision if needed.

## Decision / execution boundary
**STOP BEFORE NESTING.** Code Mode completed source repair, generated four versioned SVG/DXF masters, and checked raw DXF tag correspondence. No external kernel or independent 3D path review was executed. Independent CAD QA PENDING. Minimal Codex job is a new B1: import corrected geometry with real ezdxf and OCC, check two curved seams plus tabs/skins in 3D and viable insertion; report GO/REVISE/NO-GO. Do not perform nesting until a GO with independent review.
