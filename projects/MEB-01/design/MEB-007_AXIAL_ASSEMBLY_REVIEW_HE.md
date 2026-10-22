# MEB-007 — H1 assembly path + axial keeper audit [DESIGN_ONLY]

**Date:** 2026-10-22 · **Owner inputs FROZEN:** net usable inside X ≥310mm, opening110°, sheet 800H×440W · **Executor:** ChatGPT (no Codex) · **Stage:** `PARTIAL_CAD_GO_ASSEMBLY_SEQUENCE / BLOCKED_POSITIVE_PIN_RETENTION` · **Independent QA:** NOT_RUN · Issue #67.

## Source
Direct reuse of MEB-006 B1 and H1 v0.3 existing 2.5D CAD profiles; no global regeneration and no independent physical evidence. **Full executable source, DXF/SVG research outline, JSON and plots are delivered to the user as the ChatGPT-session ZIP** `MEB007_H1_E1b_ASSEMBLY_DESIGN_ONLY.zip` SHA256 `9cccae0b55795c4f5441dd27498de992f8fd08d81a2c3472650da352570af907`. This GitHub file documents the scoped findings; the binary study data are not hosted here.

## Assembly order findings
| Scope | Sample poses | Interfering poses |
|---|---:|---:|
| Outer moving cheek L after inner sockets | 25 | 0 |
| Outer moving cheek R after inner sockets | 25 | 0 |
| Whole nominal lid drops into fixed box from +65mm Z **before pin installation** | 131 | 0 |
| **Negative control:** lid drops with fixed pivot pins preinstalled | 131 | **26**, first at Zoffset13.5mm |
| Pins inserted from outside after lid placed: L/R at0° and110° | 4×73 | 0 |
| Flat outer caps placed last: L/R | 2×17 | 0 |

**Motion model:** exact X-slabs/YZ rigid polygons, discrete straight assembly paths. This is not an actual complete 26-part assembly demonstration; the roof/rails/ribs starter subassembly was assumed pre-positioned, bonded joins unproven. Does not prove physical kerf-flex, material strength or lifetimes.

## Axial end/socket stops
Left/right socket outward intersects moving end cheek at first nonzero shift0.05mm. Moving end cheek outward meets outer fixed cap after about0.5mm axial free space (first sampled overlap ±0.55mm). Socket inward meets longitudinal rail at ±0.55mm sampled translation. **These geometric stops depend on all end-cheek/rail/cap elements being truly connected and durable**, which is not yet proven.

**Critical retention blocker:** complete (unbonded) nominal 7mm diameter pinned 2×6mm shafts can each translate **≥3mm inward** along X against the finished body/lid geometry, even if fixed outer caps stay in place, with no geometric interference in31 samples per direction. **Outer caps do not positively retain the pins inward.** Do not conflate friction/glue speculation with permanent mechanical retention.

An added inner **4mm-thick, radius4.5mm round keeper disk** overlapping X12..16 would have **51.4697mm³** penetration of the 4mm roof in the initial closed pose. Reject simple full-round inner clip; different geometry would need a separate study.

The socket and adjacent moving end cheek have substantial projected YZ face contact (~**588.598mm²**), but only a flat butt/lamination interface, not a keyed mechanical interlock. No measured bond or structural torque-load proof.

## Small LEAN improvement E1b
Keep roof main slab X14..322; extend *local* ears only:
- Former E1 ear left X10..14, right X322..326, axial overlap 1.5mm each.
- E1b research variant left X8..14, right X322..328, axial overlap **3.5mm** each.
- After nominal0.5mm side cap play, geometrical engagement reserve rises **1.0→3.0mm**.
- Rechecked variant **441/441** moving-vs-fixed sampled angles 0°..110° at0.25° step with zero penetration, and no moving/moving penetration at0/55/110°. This only proves limited CAD geometry, not strength of an exposed 6mm tab or the **2.1mm radial wood lip**.
- E1b nominal flat outline bbox **320×99.17085mm**, using an assumed middle neutral plane; DXF and SVG parse checks PASS. **Kerf slots are not included; DO NOT CUT as production files**. Bounding rectangle fits 440W×800H stock, but no contour nesting was performed.

## QA and decision
- **11/11 self-authored assertions PASS** for the stated expected results (positive and negative controls). Insertion/axial translation samples: **826 total**. The E1b sweep is **441** additional angle poses. Counts are model pose evaluations, *not independent QA*. **No substantive geometric correction cycles in MEB-007**.
- **Blocked for G2a/G2b:** pin inward retention, shaft-to-fixed-cheek axial fastening, moving lidend/socket/rails positive joining and full part insertion, 4mm roof kerf-bend and 2.1mm lip mechanical durability, user acceptance of small raised rim/rear relief, full usable≥310mm physical verification.
- **G3 NOT_RUN; G4 NOT_APPROVED; no merge.**

## Next task (P1, ChatGPT first)
`MEB-008` — a narrow study of one mechanically positive fixed wooden pin restraint **versus** a noninterlocking bonded/fixed pin strategy, with exact parts, access, motion, positive stop and no owner-frozen constraint changes. If no credible flat-ply solution exists or owner-facing appearance must change, report `REVISE` and request decision rather than generating production files. Codex should remain OPTIONAL, not default; independent QA needed for this author's code.
