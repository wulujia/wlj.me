"""Check shared vocabulary and atomic metadata validation."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('reading_tags', Path(__file__).resolve().parents[1] / 'scripts/reading_tags.py')
tags = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tags)


class ReadingTagTests(unittest.TestCase):
    def test_shared_case_uses_most_common_article_name(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            posts = root / 'content/posts'
            posts.mkdir(parents=True)
            for i, value in enumerate(['AI', 'AI', 'ai']):
                (posts / f'{i}.md').write_text(f'---\ntags: ["{value}"]\n---\n')
            self.assertEqual(tags.normalize(['ai', 'AI'], tags.vocabulary(root)), ['AI'])

    def test_rejects_unknown_or_missing_tags(self):
        for values in ([], ['Unknown'], 'AI', [None]):
            with self.assertRaises(ValueError):
                tags.normalize(values, {'ai': 'AI'})

    def test_update_preserves_other_metadata(self):
        text = '[[materials]]\nslug = "one"\ncategory = "book"\ndate = "2020-01-01"\n'
        result = tags.replace_tags(text, {'one': ['AI', 'Tools']})
        self.assertIn('tags = ["AI", "Tools"]', result)
        self.assertEqual(tags.replace_tags(result, {'one': ['AI']}), text.replace('category = "book"', 'category = "book"\ntags = ["AI"]'))


if __name__ == '__main__':
    unittest.main()
