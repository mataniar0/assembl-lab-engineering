# ETG-01 — C11 | סיום שלב התכנון לקראת נסטינג (DESIGN_ONLY)

**תאריך:** 2026-10-26 · **מבצע:** ChatGPT, ללא Codex · **מצב:** PRE_NESTING_DRAFT, NOT_PRODUCTION_RELEASED · **Independent QA:** PENDING.

## Owner decisions and scope
- Body nominal 260×160×150 mm, birch plywood 6 mm, cutting stock **HEIGHT800 × WIDTH440 mm (portrait)**, integrated recessed wooden H1 hinge, opening 0–120°, four rounded corners.
- Owner explicitly accepts **permanent wood glue**: fixed structural joints and moving P11-to-P09/P10 connection are adhesive-based. **P12 separate mechanical pin-retaining clip retired**; P06 remains the free pivot bearing. Bond strength, wear and glue migration to bearing NOT physically verified.
- Rear/upward hinge extension remains a studied shape, **not** a locked production envelope.

## Newly completed scoped CAD research
- **C9:** Changed P11 to a glued moving pin with a laser-flat birch profile; eliminated the P12 clip. A real collision of the first C9 pin head with P02/P03 at 60° was repaired by recessing head X6..12 and trimming inner tip to X30.58. **12/12** focused checks PASSED after correction (including local samples).
- **C10:** Found nonflat 14mm side and out-of-plane post tabs in the legacy ChatGPT C7 proxy. Replaced them with nominal 6mm-sheet-flat P01/P03/P04 and P06 post designed for glue. **6/6** local geometry checks PASS.
- **C11:** Restored TWO missing front rounded corners, 24 slices×2, outer R20/inner R14 nominal. Refit front and side flats. **6/6** specific checks PASS; all cutting parts now flatten to 6mm nominal stock.

## C11 BOM — 102 individual flat source profiles
- P01–P05: 5 body wall/base pieces.
- P06 rounded FRONT corner laminates: 48 pieces (24 each).
- P06 rounded REAR corner laminates: 36 pieces (18 each).
- P06 fixed H1 ears: 4; rear keepers: 2.
- P07 roof: 1; P08 webs: 2; P09/P10 moving cheeks: 2; P11 wooden pins: 2; P12 mechanical clip: **0**.
- **Total = 102 cut profiles, all nominal 6 mm**; individually within 440×800 mm. Legacy FCIPH 96 corner-slice count is NOT equivalent to present H1 84 slices.

## Results actually verified
- **C11 final verification: 20/20 local assertions PASS**. 102 DXF and 102 SVG individual vectors regenerated from the same CAD section source; DXF/SVG reopened with 0 contour mismatches and no single-part sheet-bound violation. Maximum planar-vs-3D section area discrepancy after curve tessellation: 0.0319%; reimported STEP reports **102 valid solids**.
- 61 moving-to-fixed angular samples 0..120° have no Boolean clash in the rebuilt C11 candidate. Front corner clearance has a separate conservative 2D YZ analytic bound. Left/right glued pin candidate follows collision-free sampled axial insertion path. This is finite-sample nominal CAD evidence, **NOT** proof of continuous 3D swept-volume clearance, operator assembly, adhesion or strength.
- A timed-out broad C9 test and timed-out initial C11 full scan are **NOT_RUN**, not counted as PASS. One explicit C11 test expectation error (54 vs 102 manifest count) was corrected in the tester; no geometry change was caused by that false failure.

## Exact artifact provenance
The editable CAD sources, complete 102 DXF+102 SVG individual files, assembled STEP, BOM/IF manifest, image overview, complete Hebrew handoff and JSON QA were delivered as an in-conversation ZIP:
`ETG_01_C11_PRE_NESTING_DESIGN_ONLY.zip`, **SHA256 `ee6b1068eca3bb9ba65d0655a20138478a98609e7e16968d4bd4a5dacbfe60e1`**, 218 files.
**This ZIP is not present in this GitHub PR**; this commit is the audit/handoff record only. A reviewer cannot independently rerun CAD without obtaining the actual ZIP.

## Open gates — why this is NOT production nesting
1. **Two rear corner cutouts in P07 remain uncovered** (each historical C7R cutout ~756 mm²), and final aesthetic/functional finishing requires product QA before approval.
2. Permanent wood-glue bonding of P11 to rotating cheek, prevention of adhesive transfer to P06 fixed bearing, and edge-bond strength of body/four corners: physical G3 coupon and prototype **NOT_RUN**. No guarantee of retention if adhesive fails.
3. Actual sheet thickness, laser kerf, material fit, physical 120° sweep, finish, site operator verification, independent QA >=90 with no in-scope CRITICAL blockers: pending.
4. NESTING **NOT_PERFORMED**, number of stock sheets **NOT VERIFIED**, manufacturer DXF **NOT AUTHORIZED**. The 102 DXF/SVG are individually vectorized **DESIGN_ONLY**, no kerf comp.

**Next phase:** DESIGN_ONLY trial nesting can be attempted by ChatGPT for area/stock planning on portrait 800×440 mm. Formal production nesting/release stays gated on G3 and G4. Codex remains unnecessary at this boundary. No automatic merge.
