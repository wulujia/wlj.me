"""Check post publication in a throwaway Git repository."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PostPublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        remote = self.work / 'remote.git'
        self.repo = self.work / 'repo'
        self.git('init', '-q', '--bare', '-b', 'main', str(remote))
        self.git('init', '-q', '-b', 'main', str(self.repo))
        for args in (('config', 'user.email', 'test@example.com'), ('config', 'user.name', 'Test'), ('remote', 'add', 'origin', str(remote))):
            self.git('-C', str(self.repo), *args)
        shutil.copy(ROOT / 'publish.sh', self.repo)
        (self.repo / 'content/posts').mkdir(parents=True)
        self.git('-C', str(self.repo), 'add', '.')
        self.git('-C', str(self.repo), 'commit', '-qm', 'init')
        self.git('-C', str(self.repo), 'push', '-q', 'origin', 'main')
        # Test the publication flow without the installed luca-writing repository.
        home = self.work / 'home'
        lint = home / 'Github/luca-writing/scripts/lint_ai_flavor.py'
        lint.parent.mkdir(parents=True)
        lint.write_text('raise SystemExit(0)\n')
        self.env = dict(os.environ, HOME=str(home))

    def git(self, *args):
        subprocess.run(['git', *args], check=True, capture_output=True)

    def test_title_quotes_and_backslashes_are_escaped(self):
        source = self.work / 'quoted-title.md'
        source.write_text('# A "quoted" title \\ end\n\nBody text.\n')
        result = subprocess.run(['bash', str(self.repo / 'publish.sh'), str(source), 'Blog'], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        post = (self.repo / 'content/posts/quoted-title.md').read_text()
        self.assertIn('title: "A \\"quoted\\" title \\\\ end"\n', post)

    def test_publish_succeeds_when_the_remote_is_ahead(self):
        # Another computer pushed a commit after this clone last synced.
        other = self.work / 'other'
        self.git('clone', '-q', str(self.work / 'remote.git'), str(other))
        (other / 'other.txt').write_text('x\n')
        for args in (('add', 'other.txt'), ('-c', 'user.email=t@example.com', '-c', 'user.name=T', 'commit', '-qm', 'other'), ('push', '-q', 'origin', 'main')):
            self.git('-C', str(other), *args)
        source = self.work / 'second-post.md'
        source.write_text('# Second\n\nBody text.\n')
        result = subprocess.run(['bash', str(self.repo / 'publish.sh'), str(source)], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        log = subprocess.run(['git', '-C', str(self.work / 'remote.git'), 'log', '--format=%s', '-2'], capture_output=True, text=True).stdout
        self.assertEqual(log, 'Add post: Second\nother\n')


if __name__ == '__main__':
    unittest.main()
