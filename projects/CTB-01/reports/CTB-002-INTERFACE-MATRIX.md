# CTB-002 dependency matrix — DESIGN_ONLY, before local modelling

Authority: Issue #5 and P01-SEL-001. Use the unchanged SOFT_CURVE parametric contour.
Work only in P02, with versioned P01 mortise study copies. No baseline status upgrades.

| IF | Frozen / provisional | Local evidence / remaining decision |
|---|---|---|
| IF-01 | 2×6 mm cheeks, t±10.5, gap15, outside27, exactly4 spacers; proposed holes TBD | Compare3 joints; prove local B assembly using actual solid material and continuous swept volumes. Nominal clearance is a hypothesis; no adhesive strength/physical fit signoff. |
| IF-09 | Ring OPEN, study z225..265 | Compare spacer relocation245→200 against local external bypass. No candidate hole in225..265 for the recommended relocation. CTB-006 must approve the changed provisional position. B05 remains OPEN. |
| IF-02 | Y at410, reference mortise406.9..413.1, arm94 vs cheek90 | Quantify Z separation from upper spacer390; no corrected Y designed; B04 remains. Whole Y envelope not authoritative CAD. |
| IF-03..05 | Tongue450..488, skin/discs unchanged | All mortise cuts stay below400; check no change to upper tongue. Insertion/locking of table still unverified. |
| IF-14 | Foot r240, z0; nominal6 mm birch | Check foot/outer contour untouched and lowest slot distance. B07/B11 load/stability remain unresolved. |

B03: selected exterior master remains untouched; candidate joinery still needs lead review.
B10: actual thickness and kerf are unknown (null, never assumed measured). Declare 0.2 mm
per-side CAD slot allowance and ideal radii separately from physical fit. Two identical
cheeks must share all candidate holes; three P02 spacers must be exact copies, only translated.
B01/B02: positive top retention and whole-table sequence remain unresolved despite a local
one-leg proof. Do not infer G2, physical assembly or load approval from a local CAD test.

## Proposed local decision PC-CTB002-01 (not a baseline edit)

Study heights35/90/200/390 replace35/90/245/390 only in P02 candidate data. Keep reinforced
P02B at35 and three identical P02. Orientation: plates in local (r,t), extruded in z by6;
P01 plates in (r,z), extruded in t by6. Center each mortise from the common intersection
of the exact SOFT_CURVE horizontal sections across the FULL slot-height slab. Do not use
raster or only a single center section. Outer profile and all P01 files remain untouched.

The ring comparisons use a conservative reservation box spanning the cheek and spacer
radial extents, not a finalized ring solid. Option1 relocation has Z separation. Option2
retains245 but reserves an OUTSIDE route at t18.5..24.5, giving5 mm to the nominal outer
cheek at13.5. A local route can avoid the spacer but its actual ring connection and strength
are unknown; this is explicitly conditional and no ring-specific hole is cut. B05 remains.
