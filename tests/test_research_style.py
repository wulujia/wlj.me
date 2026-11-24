"""Test the shared reading-page contract."""

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('research_style', ROOT / 'scripts/research_style.py')
style = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(style)


class ReadingStyleTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / 'templates/research/index.html').read_text()

    def check(self, html):
        return style.check(html, 'https://wulujia.com/research/example/')

    def test_template_passes(self):
        self.assertEqual(self.check(self.html), [])

    def test_changed_shared_css_fails(self):
        self.assertTrue(self.check(self.html.replace('--bg: #fdf6e3', '--bg: pink')))

    def test_missing_heading_in_outline_fails(self):
        self.assertTrue(self.check(self.html.replace('<a href="#sources">方法与来源</a>', '方法与来源')))

    def test_wrong_outline_label_fails(self):
        self.assertTrue(self.check(self.html.replace('href="#sources">方法与来源', 'href="#sources">来源')))

    def test_wrong_canonical_fails(self):
        self.assertTrue(self.check(self.html.replace('/research/example/', '/research/wrong/')))

    def test_missing_theme_script_fails(self):
        self.assertTrue(self.check(self.html.replace("toggle.addEventListener", "toggle.removeEventListener")))

    def test_changed_site_header_fails(self):
        self.assertTrue(self.check(self.html.replace('<a href="/research/" aria-current="page">研究</a>', '<a href="/research/">研究</a>')))

    def test_missing_site_footer_fails(self):
        self.assertTrue(self.check(self.html.replace('id="theme-toggle"', 'id="toggle"')))

    def test_sync_adds_header_and_footer_and_drops_old_theme_menu(self):
        import re
        old = re.sub(style.HEADER_RE, '', self.html, flags=re.S)
        old = re.sub(style.FOOTER_RE, '', old, flags=re.S)
        old = old.replace('<a href="/research/">返回研究</a>', '<a href="/research/">返回研究</a>\n<label for="reading-theme">主题</label>\n<select id="reading-theme"><option value="system">跟随系统</option></select>')
        self.assertTrue(self.check(old))
        self.assertEqual(self.check(style.sync(old)), [])

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
