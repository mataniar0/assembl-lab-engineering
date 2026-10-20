# ETG-000 — Codex delivery instructions

1. Read root `AGENTS.md`, Playbook, Gates, Quality Standard and the named `assembl-lab-product-engineering` Skill. Then read ETG-01 BRIEF/STATUS/DECISIONS and the entire ETG-000 directory.
2. Treat this PR as **G0 draft only**. Verify historical dimensions from original etrog sources if provided; **do not** import the Megillah V8.3.9 components.
3. Independently cross-validate BOM IDs vs interface endpoints, numeric derivations, stock orientation, source claims and contradictions. Add negative controls (missing BOM entry, wrong part ID, swapped sheet axes, inconsistent hinge radial formula).
4. Reconcile/recover actual V7.6 etrog parametric CAD and exported DXFs, record SHA/checksums and version, then propose revisions via Change Request if required.
5. Do not change source dimensions to force PASS without documenting alternatives, impacted IFs, and lead decision.
6. Report meaningful **unique** tests, failed attempts, number of fixes and independent reviewer identity. If reviewer absent, record `INDEPENDENT_QA_PENDING`.
7. Prepare next Issues ETG-001..008 only with scoped dependencies; do not build all components inside ETG-000.
8. No merge by implementer, no physical tests claimed and no production authorization from this stage.
