## LEAN TASK PLANNING v1.1 / 2026-10-26
**P1 · Executor: ChatGPT directly · Codex not used.** Owner accepts glue and approved studying/removing separate roof `LID_SOCKET_L/R` rather than adding mechanisms. Baseline MEB-019 edge-open kerf / MEB-016 finger joints; original references preserved.

## One local candidate executed
- **Remove both LID_SOCKET parts**, 26→**24** total; 6mm birch parts21→**19**, 4mm stays5.
- Retain H1 fixed shoulder pins, circular pivot bearing and flush outer veneer, body finger joints, LID_END_L/R side silhouettes and roof center geometry.
- Extend only the two *longitudinal curved roof-side glue flanges*, each x **-0.5..14** and **322..336.5** but over finite arc geodesic S**8..74mm**. Do NOT extend the whole 4mm roof to stationary side cheeks, which produced an interference in previous model. The flange YZ shape is an exact subsection of the existing curved 4mm shell; meets LID_END upper curved edge for **66.0063mm** each side. Approx nominal plywood edge glue area **396.04mm² per side** (6mm cheek thickness × arc length), **not a bond-strength claim**.
- Relocate the existing two J3 6mm U-saddles to X**5.5..11.5** and **324.5..330.5**, face-glued to LID_END (modeled projected face contact **270.65mm² per side**); move half-lap cuts in the two longitudinal rails accordingly. U-saddles don't self-lock and glue remains a physical load-path prerequisite.
- Keep MEB019 central 22-row staggered kerfs; add 34 wing-edge research centerlines => **188 total**. No proven 4mm birch bend, stock/kerf calibration or adhesion. Wide wing uncut zones avoided by alternating open-edge lines but fatigue risk remains.

## Bounded numerical QA (same author, NOT independent)
- **26/26 direct model assertions** and **69/69 source-vs-DXF/SVG second-implementation assertions PASS** (second method not independent engineer).
- **441/441** discrete moving/static poses from0° to110° have zero modeled volumetric penetration, snapshots0/55/110 also clear. Retained negative control with rear wall not relieved correctly detects interference ~47°.
- Two U-saddle install paths **98/98** sample poses clear, moving end cheeks installed **66/66**, complete rigid lid drop before pin **131/131**, four pin insertion scans0/110° **260/260** sampled positions clear. This is NOT a fully proven practical assembly path nor strength proof.
- Model nominal usable axial cavity X12..324 = **312mm** ≥ required310, no intrusion in Y6..71,Z6..65 prism; not actual scroll fit.
- Only **three cut outlines** changed vs MEB019: LID_SKIN_RADIAL_4MM and LID_FRONT_RAIL/BACK_RAIL. Two U-saddle **spatial positions** changed but their 2D cut profiles did not; two LID_SOCKET profiles removed. All other21 retained profiles geometrically identical.
- Two boards **440W×800H**: 6mm19 parts, 4mm5 parts, min contour separation4.4mm; 188 theoretical kerf centerlines on roof, not machine-ready.
- Fresh-folder ZIP extract+rerun regenerated the 24-part two-board source and PASS 24/24 primary then69/69 secondary then26/26 extended checks. ZIP CRC PASS.

## Evidence and risk
User-chat ZIP **`MEB020_H1_DIRECT_GLUE_TO_LID_END_DESIGN_ONLY.zip`**, SHA256 **`f72787286eaa5804f46e9c30ac408de807fd5204e75eb75e21ead9c5d8a70199`**, **150 entries**, ~1.19MB. Complete actual 24 per-part SVG/DXF/PNG, 2 nesting DXF/SVG+PNG, 2 CAD-derived explanatory PNGs, QA JSON, complete inherited and changed Python and Hebrew report. **Archive is in user chat, not committed to GitHub**; this Issue documents evidence and handoff only.

### Hard gate blockers
Physical birch4mm tight curvature, edge-open kerf fatigue and breakage, **wood edge-grain glue bond** between skin/LID_END, J3 saddle-to-endplate adhesive shear/peel, pivot/overlay durability and exact material tolerances NOT_RUN. 354mm exterior and rear68.8mm relief remain provisional pending final owner approval. Independent QA absent; G2 full assembly pending, G3 NOT_RUN, G4 NOT_APPROVED. Do not merge or release manufacturing files by implication.

**Next narrow action:** perform qualified physical fit / bend / bond prototype and independent source QA before production. No other large design generation necessary until observations warrant it.

## Scope-preserving handoff
This GitHub branch intentionally commits a design-evidence summary. Complete executable model and DXF/SVG/PNG generated files remain in the user-conversation ZIP, so this PR alone is NOT sufficient for an independent full-source review. Use the exact SHA256 archive in Issue #91; never infer that source exports were pushed.
