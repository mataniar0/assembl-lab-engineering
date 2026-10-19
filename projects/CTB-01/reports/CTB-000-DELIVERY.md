# CTB-000 v0.2 delivery

Issue: https://github.com/mataniar0/assembl-lab-engineering/issues/1
Branch: `codex/ctb-000-baseline-import`, based on main commit
`c33c44d61bb6470a0e72ca0186bbf2feabe52a25`.

## Source provenance

Supplied ZIP SHA-256 (matches Issue #1):
`9cfdc8e39bb575341a02dd56440da2c5b2eaee2f7ae1a9b02525d8ebe3a89c64`.
Archive inventory and MANIFEST.files match exactly: 15 files, all imported byte-for-byte.
No missing/extra files relative to the manifest. Individual SHA-256 values are recorded
in `CTB-000-source-sha256.json`, computed directly from the verified ZIP members.
All JSON/CSV/Markdown, validator source, SVG content and rendered PNG were inspected.

## Delivered files

Under `projects/CTB-01/specifications/CTB-000/`:

- AGENT_HANDOFF_HE.md
- CHANGELOG.md
- CHANGE_REQUEST_TEMPLATE.md
- CTB-000_interface_diagram.png
- CTB-000_interface_diagram.svg
- CTB-000_interfaces.json
- CTB-000_open_issues.csv
- CTB-000_parameters.json
- CTB-000_parts.csv
- CTB-000_schema.json
- DECISIONS.md
- MANIFEST.json
- SOURCE_REGISTER.md
- SPEC_HE.md
- validate_contract.py

Repository additions: root `AGENTS.md`, `tools/check_ctb_baseline.py`,
`projects/CTB-01/STATUS.md`, and this report plus
`CTB-000-source-sha256.json`, `CTB-000-validator.log`, `CTB-000-import-checks.log`
in `projects/CTB-01/reports/`. Existing README and source files remain unchanged.

## Reproduce

From repository root, with Python 3.12 and jsonschema 4.26.0:

```sh
python projects/CTB-01/specifications/CTB-000/validate_contract.py
python tools/check_ctb_baseline.py
git diff origin/main --check -- . ":(exclude)projects/CTB-01/specifications/CTB-000/**"
rg -n '900' projects/CTB-01/specifications/CTB-000 -g '!*.png'
```

Validated in an isolated venv at `/workspace/.venvs/ctb-000`.
Source validator: **25/25 PASS, 0 FAIL** (complete output in validator log).
Additional consistency suite: **15/15 PASS, 0 FAIL**, including JSON Schema 2020-12,
byte integrity, inventory, versions, references, all 14 IF IDs and all 13 open issues,
critical blockers, sheet orientation, image format checks and no legacy CAD import.
Text audit: five 900 references, all explicitly historical/superseded; no active 900
numeric settings. SVG/PNG were inspected; sheet label is H800 × W440.
New-file whitespace check excluding the byte-preserved source directory: PASS.
Full baseline diff reports 28 pre-existing source whitespace warnings: CRLF in the
two CSVs (27 lines) and one Markdown hard line break in SPEC_HE.md. Preserved rather
than normalizing authoritative source bytes. Original dimensions changed: **0**.
Contract corrections: **0**.

## Failures, discrepancies and disposition

- No static validation failures. Initial source and import suites passed without a repair cycle;
  the saved environment commands were also exercised successfully.
- SVG and PNG title says v0.1, while package metadata says v0.2. Both depict a schematic
  forked side silhouette, not the authoritative parallel-cheek part design. Retained unchanged
  and flagged for project-manager review; no inferred geometry was implemented.
- MANIFEST.sources names four historical archives, not included in this delivery. Their
  listed hashes are provenance claims from the source, not newly verified artifacts.
- GitHub API access returned proxy CONNECT 403. Git reads work and Issue #1 was read via
  its HTML page. `api.github.com` was added to the environment configuration draft;
  saving a draft alone does not apply runtime access or create a PR.

## Remaining engineering gates

All B01–B13 remain open (see STATUS.md and original CSV). Upper locking, assembly order
and missing final leg geometry remain BLOCKERs. CAD integration, material/kerf calibration,
fit, actual bending, structural loads, stability, physical assembly and nesting were not run.
The baseline is DESIGN_ONLY / G0 and is not a manufacturing or physical safety approval.
CTB-001 has not started. No merge is authorized.
