# MEB-01 — Megillat Esther Box / Kופסת מגילת אסתר
**Stage:** MEB-000 source-reference verification complete / G0 REVIEW_REQUIRED · **Release:** DESIGN_ONLY

This project migrates the historical V8.2.2 Megillat Esther case into the reusable [Engineering Playbook](../../engineering-process/PLAYBOOK_HE.md) and [Codex Skill](../../.agents/skills/assembl-lab-product-engineering/SKILL.md). Do not silently replace the old CAD with drawings inferred from renders.

- Tracking: [Issue #16](https://github.com/mataniar0/assembl-lab-engineering/issues/16).
- Immutable legacy source: [site repo at pinned commit](https://github.com/mataniar0/assembl-lab-site/tree/ebeefe308efaf80329e16e42a84d51557878fd58/megillat_esther_box/v8_2_2).
- All 14 nominal per-part DXFs, 2 legacy cutting sheets, and 1 fit coupon remain in the source repository; all were retrieved and parsed without modifying source. This PR adds measured coordinate-reference reconstruction and independent QA, **not** a validated high-level parametric CAD kernel.
- G0 source of truth: `specifications/MEB-000/`.
- Records: [brief](BRIEF.md) · [status](STATUS.md) · [decisions](DECISIONS.md) · [legacy QA intake](specifications/MEB-000/QA_INTAKE.md) · [Codex handoff](specifications/MEB-000/CODEX_HANDOFF.md).

Do not confuse **source-reported 56 passing checks** with a newly completed independent QA. G1/G2/G3/G4 are not authorized by this intake.

## New verification
Owner requirements: HEIGHT800 × WIDTH440mm stock,110deg opening. See [delivery](reports/MEB-000-DELIVERY.md), [independent QA](reports/MEB-000-INDEPENDENT-QA.md), [run instructions](tools/README.md) and [proposed reference frame](proposals/G0-reference/FRAME_AND_LIMITS.md). Full G0 remains subject to lead review; G1/G2/G3/G4 are not authorized.
