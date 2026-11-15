# ETG-001R C5 / ETG-004 C6 — ChatGPT-first continuation and CAD evidence

**Date:** 2026-10-22 · **Mode:** LEAN TASK PLANNING v1.1 · **QA:** self-check, INDEPENDENT_QA_PENDING · **Gate:** DESIGN_ONLY / G1-G2 NOT APPROVED.
**Supersedes nothing in C4:** This is a newer candidate on top of C4's provisional rear/corner/hinge geometry, **not** an exact recovery of missing native V7.6 CAD.

## C5: P01/P05 + P03/P04 closure geometry
- Added genuine CadQuery candidate **P05** full planar base 260×160×6mm; **P01** front 260×6×144mm (Z6..150); revised **P03/P04** full side sheets with three J-tongues at Z24,78,120; **P01** has six complementary CLOSED mortises nominally 0.1mm clearance. This is a research geometry, not a physical fit clearance.
- CAD self-check: **20/20 assertions PASS**, **171 static parent-pair comparisons** no material intersection, front can slide from negative Y onto tongue receivers in 17 sampled poses, side panels can insert without the front, and the front mortises obstruct nominal 2mm outward X motion of either side (each real Boolean intersection **205.2mm³**). Control of filled receiver hole has **216mm³** clash; X-shifted front creates **205.2mm³** clash.
- **CRITICAL C5 OPEN:** the front panel **can still leave along -Y** (10 poses clear), and bottom base **can drop along -Z** (10 poses clear). The positive sideways retention of P03/P04 and H1 P06 posts is therefore **conditional upon structural retention of front/base**, which has NOT been demonstrated. A bond-only load-path assumption is not a proven mechanical anti-extraction device. Do not claim a completed mechanically captive body.
- Exact physical layer kerf, plywood thickness, adhesive/strength, front corner detail, and fully connected body assembly order not measured/proven.

## C6: one candidate flat lid, actual 3D rigid-body sweep samples
- Screened ONE proposed non-frozen simple lid skin X6..254, Y0..150, Z150..156mm, connected by two nominal 6mm web blocks to two rotating H1 cheeks at study pivot Y144,Z134; against stationary C4 P02 rear panel, P03/P04 side, P06 ears/posts, P11 pins/P12 clips.
- **FAIL** at **53 of 61** sample angles (0..120° in 2° steps). First collision at **14°**: 11.922mm³ P07↔P02, additional minor contact with P06 posts. At 120° the candidate P07↔P02 overlap is **6073.22mm³**. This disproves this ONE roof hypothesis, not all H1 lid architectures.
- Additional 2D YZ planar analytical counterfactual: retracting rear edge to Y128 avoided P02-only collision in **481 sampled poses at 0.25°** but would leave **32mm uncovered** near rear wall when shut. **NOT an approved correction**: impacts appearance, closure and fruit protection; still no full CAD/P06 sweep. A small nominal H1 pivot reposition within existing 6mm-ish side-wall lands did not rescue Y150 flat lid in a 20-combination screening grid; no global optimum claimed.
- **Do not change** owner H1 visual integration, ETG 0..120° required sweep, nominal 260×160×150 body, birch6mm material or H800×W440 stock without appropriate CR and review.

## Reproduction/source provenance
Actual **Python parametric C5/C6**, C4 geometry parent module, C5 design STEP, both JSON checks, a C6 collision cross-section, and Hebrew report are included in **conversation ZIP** `ETG001R_C5_C6_DESIGN_ONLY.zip`, SHA256 `40a564fc2df26c431326a96fed912fd28ba7a7555bdf4f38a809c93b6d1ceb17`. **None of these actual binary CAD/source files were uploaded into GitHub with this note**. Any independent CAD review requires access to this ZIP. Do not claim GitHub-only reproducibility.

## QA and change log
One initial C5 geometry run, one revised negative-control/run (checker replacement, no geometry modification); C6 first screened and rerun unchanged with copied standalone source. **C5 CAD geometry corrections: 0**, checker assertions corrected: 1; C6 CAD geometry corrections: 0. Four higher-level test categories: C5 static/connectivity/insertion/extraction, C5 negative controls, C6 sampled swept positions and 2D planar counterfactual. Independent QA NOT_RUN. Physical G3/kerf/adhesive NOT_RUN; G4 manufacturing/nesting NOT_AUTHORIZED.

## Next limited actions
1. **ETG-001R P1:** design one positive or explicit bonded-and-testable P01/P05 retention path that captures P03/P04; do not mark PASS based only on C5 closed-state intersections. Minimal focused proof, not redoing H1 C4.
2. **ETG-004 P1:** owner-consistent full-cover lid/hinge geometry needed; the simple flat lid collides. A broad 32mm lid shortening is an **unapproved material aesthetic/functionality change**, requiring a product decision/CR or credible alternate roof contour.
3. Only then ETG-006 G2b full assembly and full sweeping collisions, independent QA. **Codex is not inherently required at this stage**; remaining blockers are design/appearance/physical closure, not lack of ChatGPT CAD runtime.
