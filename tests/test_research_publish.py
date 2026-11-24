"""Check publication boundaries without changing the working repository."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadingPublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.repo = self.work / 'repo'
        self.repo.mkdir()
        shutil.copy(ROOT / 'publish.sh', self.repo)
        for folder in ('scripts', 'templates/research', 'data', 'static/research', 'content/posts', 'bin'):
            (self.repo / folder).mkdir(parents=True)
        shutil.copy(ROOT / 'scripts/research_style.py', self.repo / 'scripts')
        shutil.copy(ROOT / 'scripts/research_tags.py', self.repo / 'scripts')
        (self.repo / 'content/posts/example.md').write_text('---\ntags: ["AI", "Tools"]\n---\n')
        for path in (ROOT / 'templates/research').iterdir():
            shutil.copy(path, self.repo / 'templates/research')
        (self.repo / 'data/research-materials.toml').write_text('')
        (self.repo / 'CHANGELOG.md').write_text('# Changelog\n')
        self.source = self.work / 'example'
        self.source.mkdir()
        shutil.copy(ROOT / 'templates/research/index.html', self.source)
        # A fake build isolates these tests from Hugo. Any Git call fails.
        git = self.repo / 'bin/git'
        git.write_text('#!/bin/sh\necho unexpected-git-call >&2\nexit 91\n')
        hugo = self.repo / 'bin/hugo'
        hugo.write_text('#!/bin/sh\nwhile [ "$1" != "--destination" ]; do shift; done\nshift\nmkdir -p "$1/research/example"\ncp static/research/example/index.html "$1/research/example/index.html"\nprintf "<loc>https://wulujia.com/research/example/</loc>" > "$1/sitemap.xml"\n')
        for path in (git, hugo):
            path.chmod(0o755)
        # Keep the script's build destination inside this test directory.
        script = self.repo / 'publish.sh'
        script.write_text(script.read_text().replace('/tmp/wlj-check', str(self.work / 'build')))
        # Test the publication boundary without the installed skill repositories.
        test_home = self.work / 'home'
        self.html_checker = test_home / 'Github/luca-html/scripts/check_html.py'
        self.html_checker.parent.mkdir(parents=True)
        self.html_checker.write_text('raise SystemExit(0)\n')
        self.env = dict(os.environ, HOME=str(test_home), PATH=str(self.repo / 'bin') + os.pathsep + os.environ['PATH'])

    def test_external_checker_failure_prevents_writes(self):
        self.html_checker.write_text('raise SystemExit(72)\n')
        result = self.publish('--local')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / 'static/research/example').exists())
        self.assertEqual((self.repo / 'data/research-materials.toml').read_text(), '')

    def publish(self, *options):
        return subprocess.run(['bash', str(self.repo / 'publish.sh'), 'research', str(self.source), '--category', 'misc', '--author', 'Test', '--tags', 'AI', *options], env=self.env, capture_output=True, text=True)

    def test_unknown_tags_prevent_writes(self):
        result = self.publish('--tags', 'Unknown', '--local')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / 'static/research/example').exists())
        self.assertEqual((self.repo / 'data/research-materials.toml').read_text(), '')

    def test_update_preserves_tags_when_omitted(self):
        result = self.publish('--tags', 'tools', '--local')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = self.publish('--tags', '', '--update', '--local')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('tags = ["Tools"]', (self.repo / 'data/research-materials.toml').read_text())

    def test_dry_run_writes_nothing(self):
        result = self.publish('--dry-run')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.repo / 'static/research/example').exists())
        self.assertEqual((self.repo / 'data/research-materials.toml').read_text(), '')
        self.assertEqual((self.repo / 'CHANGELOG.md').read_text(), '# Changelog\n')

    def test_bad_child_prevents_all_writes(self):
        child = self.source / 'child'
        child.mkdir()
        (child / 'index.html').write_text('<h1>Invalid child</h1>')
        result = self.publish('--local')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('child/index.html', result.stdout)
        self.assertFalse((self.repo / 'static/research/example').exists())
        self.assertEqual((self.repo / 'data/research-materials.toml').read_text(), '')

    def test_local_create_and_update_do_not_call_git(self):
        result = self.publish('--local')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        target = self.repo / 'static/research/example'
        self.assertTrue((target / 'index.html').exists())
        metadata = (self.repo / 'data/research-materials.toml').read_text()
        (target / 'old-attachment').mkdir()
        (target / 'old-attachment/old.txt').write_text('old')
        (self.source / 'attachment.txt').write_text('new')
        result = self.publish('--local', '--update')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((target / 'attachment.txt').read_text(), 'new')
        self.assertFalse((target / 'old-attachment').exists())
        self.assertEqual((self.repo / 'data/research-materials.toml').read_text(), metadata)

    def test_overlapping_source_is_rejected(self):
        result = self.publish('--local')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.source = self.repo / 'static/research/example'
        before = (self.source / 'index.html').read_bytes()
        result = self.publish('--local', '--update')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.source / 'index.html').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
