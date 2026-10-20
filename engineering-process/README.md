# ASSEMBL LAB — Engineering Process

## Start here
- [Playbook (Hebrew)](PLAYBOOK_HE.md)
- [Approval gates and release definitions](GATES.md)
- [QA policy](QUALITY_STANDARD.md)
- [Copy-and-fill templates](TEMPLATES/)
- [Codex Skill](../.agents/skills/assembl-lab-product-engineering/SKILL.md)

## Golden rule
**Every new product starts with a design brief and project-local G0 interface contract.**
Do not clone another product's dimensions, geometry, materials, machine-bed size, approved fit or production status.

The agent creates one issue + branch + PR per scoped work package, never self-merges, discloses what was and was not tested, and hands the PR to the engineering lead for review. When a decisive design trade-off arises, escalate to the owner; routine reviewed milestones may proceed under delegated authorization.

## Recommended project structure
```
projects/<PRODUCT-ID>/
  BRIEF.md
  STATUS.md
  DECISIONS.md
  specifications/G0/
  parts/<PART-ID>/{src,variants,tests}/
  assemblies/
  reports/
  release/
```
Folders appear when needed; do not generate placeholder fake evidence. Project-specific `AGENTS.md` may refine the generic process without bypassing its safety/release gates.

## General engineering conventions
- Stable part IDs, consistent units and reference frames, explicit tolerances and source-of-truth version.
- Identify **frozen**, **derived** and **provisional** values; unspecified values stay `OPEN`.
- One parametric source should generate matching DXF/SVG/3D preview and geometry data; renders are not manufacturing authority.
- Review individual parts before combining them into independently tested subassemblies.
- Report all failures and corrections, including blocked assembly paths and unrun tests.
- `DESIGN_ONLY` CAD is not a real-world cut authorization.

The CTB-01 specific setup stays under `projects/CTB-01/` and in root `AGENTS.md`; it is an example **not a new-product default**.

## Validate the process documents

From the repository root (Python 3.12, standard library only):

```sh
python engineering-process/tools/validate_playbook.py
python -m unittest discover -s engineering-process/tests -v
```

The second command tests intentionally broken copies in temporary directories. Neither command substitutes for manual policy review or validates a filled project contract.
