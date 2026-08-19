import tempfile
import unittest
from pathlib import Path

from demo.hermes_run_triage import analyze_lines, load_lines, render_markdown


class HermesRunTriageTests(unittest.TestCase):
    def test_detects_stale_browser_ref(self):
        analysis = analyze_lines([
            'mcp__playwright__browser_type returned Error: Ref f1e3544 not found in the current page snapshot. Try capturing new snapshot.',
            'mcp__playwright__browser_snapshot succeeded',
        ])
        self.assertEqual(analysis['category_counts']['stale_browser_ref'], 1)
        self.assertGreaterEqual(analysis['tool_counts']['mcp__playwright__browser_type'], 1)

    def test_detects_auth_signal(self):
        analysis = analyze_lines(['Authorization: Bearer *** token=example'])
        self.assertEqual(analysis['category_counts']['auth_or_permission'], 1)

    def test_load_lines_supports_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'session.jsonl'
            path.write_text('{"role":"tool","name":"terminal","content":"exit_code: 0 success"}\n', encoding='utf-8')
            lines = load_lines(path)
        self.assertEqual(len(lines), 1)
        self.assertIn('terminal', lines[0])
        self.assertIn('success', lines[0])

    def test_markdown_contains_recommendations(self):
        analysis = analyze_lines(['timeout while calling browser_click'])
        report = render_markdown('Test Report', Path('input.log'), analysis)
        self.assertIn('# Test Report', report)
        self.assertIn('timeout', report)
        self.assertIn('what I would check next', report)


if __name__ == '__main__':
    unittest.main()
