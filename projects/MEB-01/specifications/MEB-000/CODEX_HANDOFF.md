# Codex handoff — MEB-000, Issue #16

## Required reads
`AGENTS.md`, `engineering-process/PLAYBOOK_HE.md`, `GATES.md`, `QUALITY_STANDARD.md`,
`.agents/skills/assembl-lab-product-engineering/SKILL.md`, `projects/MEB-01/BRIEF.md`,
`projects/MEB-01/STATUS.md`, `projects/MEB-01/DECISIONS.md`,
`projects/MEB-01/specifications/MEB-000/*`.

## Do next on this dedicated branch / PR
1. Verify every registered blob SHA against the pinned legacy site commit `ebeefe308efaf80329e16e42a84d51557878fd58`.
2. Reproduce all 56 historical source assertions **from real DXFs** when meaningful, separating static presence, geometry, 2D fitting, 3D motion and physical proof. Record each case and negative controls.
3. Create reproducible parametric G0 reconstruction proposals separately from the untouched V8.2.2 sources; classify deviations explicitly.
4. Establish x/y/z reference frames, derive exterior geometry and verify document vs CAD dimensions.
5. Resolve MEB-B01 sheet and MEB-B02 motion requirement with owner; never silently pick a stock size or required angle.
6. Mark source reported vs independently checked values clearly; do not relabel legacy PASS as independent.
7. Run baseline check and independent review. If independent QA unavailable, record INDEPENDENT_QA_PENDING.
8. Propose scoped G1 component issues only after documented G0 review.

## Recommended G1 ordering
- Shell: P01..P05 body/floor and finger joints.
- Wooden hinge: P06..P08 and P09/P10 ear interface.
- Lid carcass: P09..P13 beams, ends and half-lap.
- Curved skin P14: kerf pattern and attached rib/end interfaces.
- Then G2a/b whole-body 3D insertion/swept angle and G3 independent physical prototype.

## Restrictions
No changes to `assembl-lab-site` in this workstream; no production authorization, physical test claims or automatic merge. All modifications recorded through PR and engineering lead review. Open findings remain OPEN unless evidence proves closure.

## Execution update2026-10-20
Steps1/4/6/7 executed within documented scope. Step2 mapped all56indices:
49scopedPASS,7NOT_RUN. Step3 delivered a coordinate-parametric trace proposal,
not a fully generative design kernel. Owner approved step5 requirements:
HEIGHT800×WIDTH440mm,110deg; current6mm layout does not fit and3D motion is NOT_RUN.
See STATUS, FRAME_AND_LIMITS, independent QA and delivery for evidence.
Next: lead G0/datum review, B12 thin-web disposition, then separately authorized
G1 tasks. Do not repeat the old false README110 attribution or infer release.
