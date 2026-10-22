# CTB-016 — PROVISIONAL five-sheet nesting, DESIGN_ONLY

## Status and decision boundary
**NESTING_FILES_DELIVERED / ASSEMBLY_ROUTE_UNVERIFIED / NOT_FOR_CUTTING.**
The owner accepted as a *planning assumption only* that the puzzle neck has sufficient strength. That does **not** resolve the experimentally unproven bend/snap path or the inherited rigid route collision at +2mm (PR61), nor demonstrate sheet grain/bending behavior.

This package is an intentionally conservative **5-board** usable-for-layout study. It is **NOT** the older four-board CTB-011 layout, nor a production release. Source geometry is versioned; no original CTB-010/011/012/013/015 files were changed.

## Files
All files are 1:1 millimetres, SVG + DXF for each sheet:
- `nesting/BIRCH6_S01`: 19 minor parts from CTB-011 S01, two formerly located P07 skins omitted.
- `nesting/BIRCH6_S02`: 6 parts, geometry unchanged vs CTB-011 (P01×4, P04L/U).
- `nesting/BIRCH6_S03`: 3 parts, geometry unchanged vs CTB-011 (P01×2, P06).
- `nesting/BIRCH6_S04`: NEW tabbed P07B/P07T skins from CTB-012; centers nominal (185,190) and (185,560)mm; envelope separation20.4mm.
- `nesting/BIRCH4_S01`: NEW length-corrected P07R1/R2 neck-and-head profiles from CTB-015, at x10/65, y20; 5mm X-axis envelope separation; both envelopes fit 440×800mm.

Old sheet dimensions are preserved: WIDTH440 × HEIGHT800mm; nominal margin >=10mm, target interpart gap5mm. No kerf compensation, no grain orientation claim. DXF CUT_OUTER/CUT_INNER only, REF sheet is NOT_CUT in SVG.

## Body count / QA
| Sheet | Material | Bodies | Closed contours | Edge margin verified |
|---|---|---:|---:|---|
| BIRCH6_S01 | 6mm birch | 19 | 19 | >=10mm |
| BIRCH6_S02 | 6mm birch | 6 | 42 | >=10mm |
| BIRCH6_S03 | 6mm birch | 3 | 16 | >=10mm |
| BIRCH6_S04 | 6mm birch | 2 | 8 | >=10.2mm |
| BIRCH4_S01 | 4mm birch | 2 | 128 | >=10mm |
| **Total** | | **32** | **213** | all nominal sheet bounds pass |

Five SVG vs DXF reimports through two custom parsers showed matching every contour, closed flags, CUT layer, and coordinate at <1µm numerical comparison threshold; **5/5 sheet comparisons PASS**, 213/213 contours matched. 32/32 body instances present. Four original CTB-011 6mm legacy part classes remain unchanged; S01 deletion only, S02/S03 remade text exporters, and 6mm S04 new skins / 4mm sheet new rim. Retained CTB-011 pack checking for S01 remainder/S02/S03 relies on inherited near-neighbor QA; **no new independent polygon-to-polygon spatial sweep for all five sheets was performed**. New S04 two disk envelopes are separated by20.4mm. Two 4mm rim envelopes separated by5mm and have no bbox intersection. Nominal bounds 5/5 sheets PASS; all32 instances have no duplicate body names (BOM validation limited to counts, inherited CTB-011 structure).

### QA scope caveats
- Independent DXF ezdxf1.4.4/audit NOT_RUN here: new exporters have explicit AcDbPolyline subclass and LAYER owner handles; raw coordinate-parser comparison is only a self-check.
- Full geometric collision/near-pair re-verification for inherited CTB-011 sheets NOT_RERUN; legacy CTB-011 self-check is not independent.
- No verified assembly path: CTB-015-B1 existing vertical route FAIL, A/B alternative routes pending; this nesting is for planning and inspection **only**, not laser cutting.
- Real 4mm kerf-flex, adhesive/neck strength, actual kerf, grain, materials, load, stability NOT_RUN.
- CTB-011 previously used four sheets, and five-sheet CTB-016 is **not optimized**. 4-sheet optimization OPEN, but not a reason to claim a proven final/cut-ready layout.
- Independent QA PENDING; G3 NOT_RUN, G4 BLOCKED; no merge or manufacturing permission.

## Source provenance
CTB-011 optimized branch `chatgpt/ctb-011-nesting-optimized-design-only`; P07 skin tab geometry CTB-012 variant; P07R corrected nominal circumference CTB-015 length-corrected SVG; DXF metadata study CTB-015C. Rim geometry uses CTB-015 SVG; rim segments both have male/female puzzle seams and strengthened kerf profile,63 kerf openings per segment.

## Next decision
For proof of actual 3D assembly, scoped Codex B1 in `projects/CTB-01/studies/CTB-015C-CHATGPT/CODEX_MINIMAL_TASK.md` (PR63) remains necessary. If revising the joint/sequence, this nesting must be regenerated and cannot remain the released layout. No external real-world validations have been made.
