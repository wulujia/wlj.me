#!/usr/bin/env python3
"""Mark thin archive posts noindex so Google indexes the real essays.

Rule (2026-09-07, see CHANGELOG): a post gets `noindex: true` when
  - it is dated before 2010 and its body is under 1500 characters, or
  - its body is under 150 characters,
unless its slug is in EXEMPT (pages Search Console already shows).
Idempotent: never touches a post that already declares `noindex`.
Run: python3 scripts/seo-noindex.py [--dry-run]
"""
import glob, re, sys
from pathlib import Path

EXEMPT = {  # >=5 impressions in GSC, 2026-06-07..09-04
    "arch-linux-remove-orphan-packages", "uninstall-glance-chamburr", "install-gemini-cli",
    "xfocus-article-46", "freemind", "gbrain-multi-device", "pm-frameworks-100",
    "hisense-a9-root-and-install-google-play", "security-company-cloudlock", "vimium-keyboard-browser-navigation",
}
ALWAYS = {"12q1y-2025"}  # near-duplicate of twelve-questions-end-of-2025

dry = "--dry-run" in sys.argv
changed = 0
for f in sorted(glob.glob(str(Path(__file__).resolve().parent.parent / "content/posts/*.md"))):
    text = Path(f).read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        continue
    fm, body = m.groups()
    if re.search(r"^noindex:", fm, re.M):
        continue
    slug = (re.search(r'^slug:\s*"?([^"\n]*)"?', fm, re.M) or [None, ""])[1]
    year = int((re.search(r'^date:\s*"?(\d{4})', fm, re.M) or [None, "0"])[1])
    n = len(re.sub(r"\s", "", body))
    thin = (year < 2010 and n < 1500) or n < 150
    if slug in ALWAYS or (thin and slug not in EXEMPT):
        changed += 1
        if not dry:
            Path(f).write_text(f"---\n{fm}\nnoindex: true\n---\n{body}", encoding="utf-8")
print(f"{'would mark' if dry else 'marked'} {changed} posts noindex")
