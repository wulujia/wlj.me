"""Test the shared reading-page contract."""

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('reading_style', ROOT / 'scripts/reading_style.py')
style = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(style)


class ReadingStyleTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / 'templates/reading/index.html').read_text()

    def check(self, html):
        return style.check(html, 'https://wlj.me/reading/example/')

    def test_template_passes(self):
        self.assertEqual(self.check(self.html), [])

    def test_changed_shared_css_fails(self):
        self.assertTrue(self.check(self.html.replace('--bg: #f5f8f7', '--bg: pink')))

    def test_missing_heading_in_outline_fails(self):
        self.assertTrue(self.check(self.html.replace('<a href="#sources">方法与来源</a>', '方法与来源')))

    def test_wrong_outline_label_fails(self):
        self.assertTrue(self.check(self.html.replace('href="#sources">方法与来源', 'href="#sources">来源')))

    def test_wrong_canonical_fails(self):
        self.assertTrue(self.check(self.html.replace('/reading/example/', '/reading/wrong/')))

    def test_missing_theme_script_fails(self):
        self.assertTrue(self.check(self.html.replace("theme.addEventListener", "theme.removeEventListener")))

    def test_duplicate_id_fails(self):
        self.assertTrue(self.check(self.html.replace('<p>本文', '<p id="sources">本文')))

    def test_override_after_shared_css_fails(self):
        self.assertTrue(self.check(self.html.replace('</head>', '<style>body { color: red; }</style></head>')))

    def test_component_cannot_override_body(self):
        html = self.html.replace('<style id="reading-style">', '<style>body { color: red !important; }</style><style id="reading-style">')
        self.assertTrue(self.check(html))

    def test_component_cannot_override_outline(self):
        html = self.html.replace('<style id="reading-style">', '<style>@media (max-width: 900px) { .outline { display: none; } }</style><style id="reading-style">')
        self.assertTrue(self.check(html))

    def test_component_can_define_chart_color(self):
        html = self.html.replace('<style id="reading-style">', '<style>:root { --chart-export: #345; }</style><style id="reading-style">')
        self.assertEqual(self.check(html), [])

    def test_component_cannot_override_shared_color(self):
        html = self.html.replace('<style id="reading-style">', '<style>:root { --bg: red !important; }</style><style id="reading-style">')
        self.assertTrue(self.check(html))


if __name__ == '__main__':
    unittest.main()
