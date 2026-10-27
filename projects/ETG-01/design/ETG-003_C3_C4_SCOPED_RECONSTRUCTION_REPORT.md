# ETG-003 C3/C4 — scoped rear body reconstruction (LEAN / DESIGN_ONLY)

**Date:** 2026-10-22 · **Owner authorization:** reconstruct missing P02 rear wall and both P06 rear corners, while preserving ETG-01 260×160×150mm body, 6mm nominal birch, H800×W440mm cutting stock, and H1 recessed pivot architecture. This is **NEW candidate geometry**; the original V7.6 native CAD remains missing. **QA:** SELF_CHECK / INDEPENDENT_QA_PENDING. **G3/G4:** NOT_RUN / NOT_AUTHORIZED.

## C3 results — rear wall and rear corners
- P02 rear panel candidate: X30.6..229.4, Y154..160, Z6..150mm; three 6×6 side mortises on each edge. Two rounded P06 rear corners: 19 stacked 6mm XY sheets each, tongue/mortise matching P02, each with two full fixed H1 ears, one moving cheek, one P11 pin, one P12 U-clip and an integrated one-piece keeper-post/bridge.
- Failed first *completed* CAD test: both static and pin-insertion checks detected the same P11 ↔ rear P02 overlap (201.6mm³). Corrected exploratory pivot location from Y152 to Y144 (not frozen).
- Retest: **17/17 local detection checks PASS**, 105 parent-pair static comparisons zero intersection, 121 angular samples per cheek and local insertion checks non-overlapping, STEP re-import **51 valid solids**. Crucial open limitation: keeper-post still extracts toward outside X in absence of the side panel. This expected-open negative observation is a passing *detector*, not a finished mechanical lock.

## C4 results — candidate P03/P04 sidewall closure
- Sidewalls **are NEW PROPOSALS**, not restored from V7.6: nominal 6mm faces x0..6 and x254..260, y0..160, z6..150 with circular pin/cap windows radius 8.4mm. H1 pivot reference Y144, Z134mm (study proposal only, not approved final geometry). Window nominal top **and rear** edge ligaments each **7.6mm**, after screening initial 1.6mm-ligament risks. P06 lower corner slices revised to 18 per side, with changed fixed-ear land and integral post geometry; actual 96 legacy FCIPH corner slices do not automatically apply.
- **23/23 local check assertions PASS**, including deliberate detection of unclosed X-extraction when P03/P04 are absent. 136 static parent-pair comparisons zero collision, 121 sampled angular positions for each local cheek, 19 pin insertion / 21 clip insertion / 16 keeper-post insertion / 21 sidewall installation poses clear (nominal geometry only). STEP independently re-read: **51 valid solids**.
- With both candidate sidewalls present, outward post X extraction is blocked at sampled 1mm displacement; without them the route is open. The upward P12 path is stopped by an integral bridge in the model; nothing yet proves real sidewall positive structural attachment to P01/P05/front corners or the full lid sweep.

## In-scope correction/efficiency log
One initial overly broad geometry run timed out — NOT a pass. Added bounding-box culling and risk-scoped samples. Five full CAD runs completed across C3/C4, with three exploratory geometry corrections (Y pivot, Z pivot and sidewall back extent), one export inclusion correction and one runtime optimization. Original V7.6 six historical fixes are unrelated. Independent QA NOT_RUN, physical fabrication/wear/kerf NOT_RUN.

## Exact conversation attachments (not hosted in GitHub)
- C3: `ETG003_C3_REAR_REBUILD_DESIGN_ONLY.zip`, SHA256 `481b6460427d5ab380b8b5d3471ced00e95472e0185fcbf0badbaca613f80c11`.
- **C4 preferred study:** `ETG003_C4_SIDE_INTEGRATION_DESIGN_ONLY.zip`, SHA256 `e482143e55fc86b4fa1e7f74d44809b7d8879006b49161b0047e5ea41a408278`.
- ZIPs contain actual parametric Python source, STEP/GLB, JSON evidence, one preview, and detailed Hebrew report. **The CAD source and binary files are not in this PR**, only this auditable handoff. A reviewer/Codex must obtain the ZIP rather than assuming the attachments are in the repository.

## Remaining gates / next tasks
1. **P1 ETG-001**: design/check the **real** P03/P04↔P05/P01/front-corner restraints and assembly order; only then claim closed sidewalls keep P06 keeper captive. Existing C4 sidewalls are conditional local references.
2. **P1 ETG-004**: define one real P07/P08 lid/roof source, demonstrate finite whole-lid motion 0–120° (continuous conservative proof where possible) and no H1/rear-wall/fruit-cavity interference. Local rotating *cheek* samples are NOT this proof.
3. ETG-006 actual integrated BOM, assembly path, IF matrix, and independent QA. No stock nesting/production until physical G3 and G4 gates.
4. Source/quality policy: existing G0 Draft PR #19 is NOT merged. This draft PR is based on that draft branch, not main, and may require rebase. G0/G1/G2/G3/G4 approvals remain pending; do not auto-merge.

**Phase boundary:** ChatGPT can continue engineering interface design with available CAD tools; **Codex is not automatically required** by these findings. Stop on an owner-frozen change, missing required source, or when a specific executable integration gap cannot be resolved reliably in ChatGPT.
