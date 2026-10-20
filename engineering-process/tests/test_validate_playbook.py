"""Isolated mutation tests; never edit the real checkout or CTB designs."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = '.agents/skills/assembl-lab-product-engineering/SKILL.md'


class PlaybookValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('engineering-process', '.agents', '.github', 'AGENTS.md', 'README.md'):
            src = ROOT / name
            if src.is_dir():
                shutil.copytree(src, self.root / name, ignore=shutil.ignore_patterns('__pycache__'))
            else:
                shutil.copy2(src, self.root / name)

    def mutate(self, path, old, new):
        p = self.root / path
        text = p.read_text()
        self.assertIn(old, text)
        p.write_text(text.replace(old, new))

    def validate(self, expected=0, diagnostic=None):
        result = subprocess.run([sys.executable, 'engineering-process/tools/validate_playbook.py'],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        if diagnostic:
            self.assertIn(diagnostic, result.stdout)
        self.assertNotIn('Traceback', result.stderr)

    def test_baseline(self):
        self.validate()

    def test_missing_required_document(self):
        (self.root / 'engineering-process/GATES.md').unlink()
        self.validate(1, 'Required nonempty file absent')

    def test_wrong_skill_name(self):
        self.mutate(SKILL, 'name: assembl-lab-product-engineering', 'name: wrong')
        self.validate(1, 'Skill name missing/mismatched')

    def test_missing_frontmatter(self):
        p = self.root / SKILL
        p.write_text(p.read_text().replace('---\n', '', 1))
        self.validate(1, 'must have YAML frontmatter')

    def test_empty_folded_description(self):
        p = self.root / SKILL
        text = p.read_text()
        start = text.index('description:')
        end = text.index('---', start)
        p.write_text(text[:start] + 'description: >-\n' + text[end:])
        self.validate(1, 'description missing or empty')

    def test_empty_scalar_description(self):
        p = self.root / SKILL
        text = p.read_text()
        start = text.index('description:')
        end = text.index('---', start)
        p.write_text(text[:start] + 'description: ""\n' + text[end:])
        self.validate(1, 'description missing or empty')

    def test_broken_skill_link(self):
        self.mutate(SKILL, '../../../engineering-process/GATES.md', '../../../engineering-process/MISSING.md')
        self.validate(1, 'Broken link')

    def test_broken_root_readme_link(self):
        self.mutate('README.md', '(engineering-process/GATES.md)', '(engineering-process/MISSING.md)')
        self.validate(1, 'Broken link in README.md')

    def test_broken_root_agents_link(self):
        self.mutate('AGENTS.md', '(engineering-process/GATES.md)', '(engineering-process/MISSING.md)')
        self.validate(1, 'Broken link in AGENTS.md')

    def test_link_outside_repository(self):
        p = self.root / 'engineering-process/README.md'
        p.write_text(p.read_text() + '\n[Outside](/etc/passwd)\n')
        self.validate(1, 'Broken link')

    def test_product_specific_stock_default(self):
        p = self.root / 'engineering-process/TEMPLATES/NEW_PRODUCT_BRIEF_HE.md'
        p.write_text(p.read_text() + '\nDefault stock: 800 × 440\n')
        self.validate(1, 'Product-specific cutting dimensions')

    def test_missing_release_gate(self):
        self.mutate('engineering-process/GATES.md', 'G5', 'REMOVED')
        self.validate(1, 'Approval gate G5 missing')


if __name__ == '__main__':
    unittest.main()
