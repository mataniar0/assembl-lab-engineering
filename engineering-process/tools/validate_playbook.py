#!/usr/bin/env python3
"""Validate reusable ASSEMBL LAB engineering playbook; stdlib only.

This verifies documentation integrity, not CAD geometry, strength, or physical safety.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
PROCESS = ROOT / "engineering-process"
SKILL = ROOT / ".agents" / "skills" / "assembl-lab-product-engineering" / "SKILL.md"
REQUIRED = [
    "engineering-process/README.md",
    "engineering-process/PLAYBOOK_HE.md",
    "engineering-process/GATES.md",
    "engineering-process/QUALITY_STANDARD.md",
    "engineering-process/TEMPLATES/NEW_PRODUCT_BRIEF_HE.md",
    "engineering-process/TEMPLATES/INTERFACE_CONTRACT.md",
    "engineering-process/TEMPLATES/COMPONENT_TASK.md",
    "engineering-process/TEMPLATES/DELIVERY_REPORT.md",
    "engineering-process/TEMPLATES/QA_REPORT.md",
    "engineering-process/TEMPLATES/CHANGE_REQUEST.md",
    "engineering-process/TEMPLATES/DECISION_LOG.md",
    "engineering-process/TEMPLATES/PRODUCT_STATUS.md",
    ".agents/skills/assembl-lab-product-engineering/SKILL.md",
    ".github/ISSUE_TEMPLATE/engineering-task.md",
    ".github/pull_request_template.md",
    ".github/workflows/playbook-validation.yml",
    "AGENTS.md",
    "README.md",
]
errors: list[str] = []
checks = 0


def assert_check(ok: bool, message: str) -> None:
    global checks
    checks += 1
    if not ok:
        errors.append(message)


for path in REQUIRED:
    p = ROOT / path
    assert_check(p.is_file() and p.stat().st_size > 20,
                 f"Required nonempty file absent: {path}")

skill = SKILL.read_text(encoding="utf-8") if SKILL.exists() else ""
frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", skill, flags=re.S)
assert_check(bool(frontmatter), "SKILL.md must have YAML frontmatter")
if frontmatter:
    f = frontmatter.group(1)
    assert_check(bool(re.search(r"(?m)^name:\s*assembl-lab-product-engineering\s*$", f)),
                 "Skill name missing/mismatched")
    # A YAML block indicator alone is not a usable description. Require actual
    # text for both the scalar and the folded/literal forms used by Skills.
    description = re.search(
        r"(?m)^description:[ \t]*([^\n]*)(?:\n((?:[ \t]+[^\n]*(?:\n|$))*))?", f)
    value = description.group(1).strip() if description else ""
    if value in (">", ">-", ">+", "|", "|-", "|+"):
        value = (description.group(2) or "").strip()
    assert_check(value not in ("", "''", '\"\"', "null", "~")
                 and not value.startswith("#"), "Skill description missing or empty")
assert_check("Never merge your own PR" in skill,
             "Skill must prohibit implementer auto-merge")
assert_check("NOT_RUN" in skill,
             "Skill must distinguish unperformed physical validation")
assert_check("CTB-01" in skill and "Never inherit CTB-01" in skill,
             "Skill must prohibit inheriting CTB-specific defaults")

gates_file = PROCESS / "GATES.md"
gates = gates_file.read_text(encoding="utf-8") if gates_file.exists() else ""
for token in ("G0", "G1", "G2a", "G2b", "G3", "G4", "G5"):
    assert_check(token in gates, f"Approval gate {token} missing")
for term in ("DESIGN_ONLY", "NOT_RUN", "Change Request"):
    assert_check(term in gates, f"Gate policy missing {term}")
for label in ("CRITICAL", "MAJOR", "MINOR"):
    qa_file = PROCESS / "QUALITY_STANDARD.md"
    qa = qa_file.read_text(encoding="utf-8") if qa_file.exists() else ""
    assert_check(label in qa, f"QA policy missing severity {label}")
assert_check("90" in qa and "100" in qa, "QA score threshold or total missing")

tmpl = PROCESS / "TEMPLATES"
essential = {
    "COMPONENT_TASK.md": ["Source SHA", "Interface", "Acceptance", "QA"],
    "DELIVERY_REPORT.md": ["SHA", "Unique cases", "Failed", "Independent"],
    "QA_REPORT.md": ["Reviewer", "Total unique", "CRITICAL", "NOT_RUN"],
    "CHANGE_REQUEST.md": ["Before", "After", "Approval", "regression"],
    "INTERFACE_CONTRACT.md": ["Interface", "FROZEN", "PROVISIONAL", "OPEN"],
    "PRODUCT_STATUS.md": ["STATUS", "Open", "Next"],
}
for name, fields in essential.items():
    p = tmpl / name
    contents = p.read_text(encoding="utf-8") if p.exists() else ""
    for term in fields:
        assert_check(term.casefold() in contents.casefold(),
                     f"Template {name} missing requirement: {term}")

# Reject accidental product-specific defaults in reusable guidance.
docs = [p for p in PROCESS.rglob("*.md")] + [SKILL]
for p in docs:
    if not p.exists():
        continue
    contents = p.read_text(encoding="utf-8")
    assert_check(not re.search(r"(?i)(?:800\s*[×x]\s*440|900\s*[×x]\s*440)", contents),
                 f"Product-specific cutting dimensions leaked into generic docs: {p.relative_to(ROOT)}")

# Validate relative Markdown hyperlinks in the playbook, README, templates and Skill.
link_docs = docs + [ROOT / "README.md", ROOT / "AGENTS.md",
                    ROOT / ".github/ISSUE_TEMPLATE/engineering-task.md",
                    ROOT / ".github/pull_request_template.md"]
for p in link_docs:
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    targets = re.findall(r"\]\(([^)]+)\)", text)
    for target in targets:
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # Paths in the templates are placeholders, not live Markdown links.
        ref = target.split("#", 1)[0].split(" ", 1)[0]
        expected = (p.parent / ref).resolve()
        assert_check(expected.exists() and expected.is_relative_to(ROOT.resolve()),
                     f"Broken link in {p.relative_to(ROOT)}: {target}")

agent_txt = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").exists() else ""
root_readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
assert_check("engineering-process/PLAYBOOK_HE.md" in agent_txt,
             "Root AGENTS.md must reference playbook")
assert_check(".agents/skills/assembl-lab-product-engineering/SKILL.md" in agent_txt,
             "Root AGENTS.md must reference skill")
assert_check("engineering-process/PLAYBOOK_HE.md" in root_readme,
             "Repository README.md must link to playbook")
assert_check("projects/CTB-01/" in agent_txt,
             "Original CTB-specific AGENTS instructions must remain")

result = f"playbook validation: {checks - len(errors)}/{checks} checks PASS"
print(result)
if errors:
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)
print("Required documents, checked relative links and policy markers passed. Manual review is still required for policy consistency.")
print("Scope: documentation integrity only; CAD/real-world validation NOT_RUN.")
