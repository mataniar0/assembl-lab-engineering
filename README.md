# ASSEMBL LAB Engineering

Parametric engineering designs, laser-cutting components, CAD source, and automated validation for ASSEMBL LAB.

## Projects

- **CTB-01 — Round coffee table (experimental)**: round Ø350 mm tabletop, height 500 mm, top thickness 50 mm, three 120°-spaced twin-cheek legs, central CSH-3Y/CSH-3P interfaces, and VTP-R KERF-4 FLEX tabletop edge.

## Engineering workflow

1. Establish an interface-control baseline (ICD) and record approved dimensions versus provisional assumptions.
2. Design and review **each component separately** against the ICD.
3. Integrate the assemblies only after component-design approval.
4. Run independent CAD and manufacturing-file QA; keep physical testing separate.
5. Publish manufacturing-ready files **only after** appropriate physical fit, material, structural, and stability validation.

**All designs are experimental unless their own release records explicitly state otherwise.** AI renderings and automated geometry checks are not proof of structural safety.

## Cutting stock

CTB-01 nominal nesting sheet: **800 mm height × 440 mm width (portrait)**. X runs 0–440 mm and Y runs 0–800 mm in sheet coordinates.

## Next step

See the CTB-000 baseline import task in GitHub Issues. The authoritative contract will live under `projects/CTB-01/specifications/CTB-000/` after review.

Codex should work on a dedicated branch, open a pull request, and refrain from automatic merging.
## Reusable engineering workflow

For each new ASSEMBL LAB product use the [Engineering Playbook (Hebrew)](engineering-process/PLAYBOOK_HE.md), [release gates](engineering-process/GATES.md) and [Codex Skill](.agents/skills/assembl-lab-product-engineering/SKILL.md). Templates for projects, interfaces, individual-component tasks, QA and deliveries are in [engineering-process/TEMPLATES](engineering-process/TEMPLATES/).

Run documentation checks:

```sh
python engineering-process/tools/validate_playbook.py
```

The playbook is **project-independent**. CTB-01 dimensions and test statuses are not defaults for new products.

