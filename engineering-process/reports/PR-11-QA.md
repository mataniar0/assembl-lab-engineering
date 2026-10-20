# PR #11 — independent QA of the Engineering Playbook

Date: 2026-10-20. Reviewed original head: `bad6cd85febca2de85dcfc4baee6b796bc43cc24`.
Base: `f49e3b3be73b7d474302823cc9072148319c8f67` (main).
Reviewer: Codex QA session, separate from the original implementation session.
Scope: process documentation, Codex Skill, all eight templates, GitHub issue/PR
forms, workflow and validator. All 19 original changed files were read.
No CAD, manufacturing release or physical performance is claimed.
The reviewer also implemented the repairs below; repair tests are self-verification,
not a second independent review of those repairs.

## Findings: 4 found, 4 corrected, 0 unresolved in inspected files

| ID | Severity | Original failure / reproduction | Correction and retest |
|---|---|---|---|
| QA-01 | MAJOR | Replace the Skill description with an empty folded block: original validator exits 0, 106/106. Skill has no usable activation description. | Require nonempty scalar/block text; folded and scalar empty controls now fail validation. Real YAML also parsed independently with PyYAML 6.0.3. |
| QA-02 | MAJOR | Append a nonexistent relative link to root README: original validator exits 0, 106/106. Root entry-point links were outside link validation. | Check root README/AGENTS and GitHub forms too. Broken README/AGENTS controls now fail. Removed misleading claim that marker checks establish absence of policy contradictions. |
| QA-03 | MAJOR | Manual policy trace: COMPONENT_TASK stops for geometry that fails assembly without the scoped-study qualification in GATES hard-stop 4. Its zero-blockers criterion was broader than the gate's zero-critical-blockers criterion. | Qualify required paths by claimed scope; explicitly preserve blocked alternatives/later-gate risks and frozen-input approval requirements; align critical-blocker criterion. |
| QA-04 | MINOR | Root AGENTS mixed generic and CTB-specific stock, axes and legacy instructions without an explicit project-only boundary. A new-product agent could apply these globally. | Add explicit CTB-01-only section heading. Original dimensions, baseline checks and restrictions remain unchanged. |

Negative controls are expected rejection tests, not failures of production designs.
Initial defect count is four distinct findings, not four failing production suites.
Two original false passes were experimentally reproduced before repair; two policy
findings were found by manual cross-document review. One repair cycle; all four
repairs checked again. No project design was modified.

## Validation evidence

Run from repository root with Python 3.12-compatible standard-library commands:

| Command | Result | Retained log |
|---|---|---|
| `python engineering-process/tools/validate_playbook.py` | 115/115 assertions PASS | `PR-11-playbook.log` |
| `python -m unittest discover -s engineering-process/tests -v` | 12/12 tests PASS: one valid baseline and 11 rejection controls | `PR-11-negative-controls.log` |
| `python projects/CTB-01/specifications/CTB-000/validate_contract.py` | 25/25 PASS | `PR-11-ctb-contract.log` |
| `python tools/check_ctb_baseline.py` | 15/15 PASS | `PR-11-ctb-baseline.log` |

Counts above are per-suite; validator assertions exercised again by mutations are
not additional unique cases. Retests are not counted again. No skipped cases in
these suites. CI now runs both the validator and mutation suite, with read-only
`contents: read` permissions. Hosted GitHub Actions itself was NOT_RUN here.

Additional independent checks: PyYAML parsed Skill and Issue YAML; workflow parsed
and verified for PR trigger, read-only permissions and both check commands.
`git diff --check` passed. Git comparisons of main vs original PR head and original
PR head vs repaired working tree show no changes under `projects/`; no untracked
project files were introduced. Existing baseline source-byte/inventory checks pass.

## New-product simulation and authority review

A scratch `NOVA-02` project was populated from brief, interface and status templates
under `/tmp/pr11-qa/`, outside the repository. Product IDs substituted correctly;
no 350/800/440 dimensions appeared. Required inputs remain OPEN, physical evidence
NOT_RUN and production status DESIGN_ONLY. This demonstrates usable initial
scaffolding, not a validated G0 contract or an approved product design.

Manual scenario trace:
- Missing dimensions/material/machine data: ask or retain OPEN; never copy CTB-01.
- Missing G0: create draft brief/BOM/interfaces; dependent part design cannot begin.
- Required assembly path fails: block the claimed assembly gate.
- Rejected alternative fails, selected scoped study is sound: preserve evidence and
  blocker; only that bounded DESIGN_ONLY study is eligible for review.
- Frozen-input change: reviewed CR required before changing the frozen source.
- Routine design: lead may approve within delegated authority; consequential
  functionality/material/safety choices escalate to owner/qualified assessor.
- G3/G4: measured physical evidence and explicit release authority required;
  QA score, CAD fit and merge do not authorize production.
- Implementer cannot self-merge. This QA task does not authorize any merge.

## Score and recommendation

Documentation-scope adaptation of the published 100-point rubric:
contract/traceability 19/20; Skill/template integrity 24/25; policy/interface
consistency 19/20; reproducibility/negative controls 19/20; handoff 14/15.
**Total: 95/100 after repairs. Recommend APPROVE for the inspected process-only
scope, subject to normal lead review; no merge performed.**

Limits: marker/link tests are not a complete YAML or natural-language policy
proof. Filled future product contracts need their own tests. GitHub API access
returned 403 (GraphQL and REST), so PR body, discussion, review state and hosted
checks could not be inspected. This recommendation covers repository content,
not unseen PR discussion. The original authors must not label this review as
independent review of its own subsequent repairs. Physical/CAD suites beyond the
unchanged baseline are NOT_APPLICABLE to this documentation PR.

Environment: no installation or startup configuration is needed for these
standard-library documentation checks; no service is required. No environment
configuration draft was changed. No publication or fresh-task restoration claimed.
