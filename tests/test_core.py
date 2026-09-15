from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from common import normalize_status, safe_filename  # noqa: E402
from next_number import scan_numbers  # noqa: E402
from vault_scan import scan  # noqa: E402
from zotero_status import desired_tags  # noqa: E402


class CoreTests(unittest.TestCase):
    def test_safe_filename(self):
        self.assertEqual(safe_filename('A: Test / Paper?'), 'A Test Paper')

    def test_status(self):
        self.assertEqual(normalize_status('精读'), '状态/精读')

    def test_next_number(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / '001-First.md').write_text('', encoding='utf-8')
            (p / '004-Fourth.md').write_text('', encoding='utf-8')
            self.assertEqual(max(scan_numbers([p])) + 1, 5)

    def test_vault_scan(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / 'PCA.md').write_text('# PCA\nRelated to [[SVD]].', encoding='utf-8')
            result = scan(p, ['PCA'])
            self.assertEqual(len(result), 1)
            self.assertIn('SVD', result[0]['wikilinks'])

    def test_zotero_status_replaces_only_status_tag(self):
        current = [{'tag': 'method/CNN'}, {'tag': '状态/待读'}]
        new = desired_tags(current, '状态/精读')
        tags = [x['tag'] for x in new]
        self.assertIn('method/CNN', tags)
        self.assertIn('状态/精读', tags)
        self.assertNotIn('状态/待读', tags)


class CliSmokeTests(unittest.TestCase):
    def test_init_and_topic(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = Path(td) / 'ws'
            cp = subprocess.run(
                [sys.executable, str(SCRIPTS / 'init_workspace.py'), '--workspace', str(workspace), '--apply'],
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
            self.assertTrue((workspace / 'runtime-config.json').exists())

            cp = subprocess.run(
                [sys.executable, str(SCRIPTS / 'create_topic.py'), '--workspace', str(workspace), '--topic', 'Test Topic', '--apply'],
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
            self.assertTrue((workspace / 'topics' / 'Test-Topic' / 'topic.json').exists())

            cp = subprocess.run(
                [sys.executable, str(SCRIPTS / 'paper_state.py'), 'create', '--workspace', str(workspace), '--topic', 'Test-Topic', '--citekey', 'demo2026'],
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
            state = json.loads((workspace / 'state' / 'Test-Topic' / 'demo2026.json').read_text(encoding='utf-8'))
            self.assertEqual(state['status'], '状态/待读')


if __name__ == '__main__':
    unittest.main()
