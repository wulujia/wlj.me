#!/usr/bin/env python3
"""
sync-zsxq-dates.py — 从知识星球拉真实发布日期，回填进源笔记 frontmatter

做两件事：
  1. 用 zsxq-cli 分页拉 group 511244584 的所有主题，匹配文件夹里的创业笔记，记录
     {编号 → create_time / topic_id / digested / counts}，存到 scripts/zsxq-dates.json。
  2. 把真实 date 回填进源文件 startupnotes/NNN-*.md 顶部的 YAML frontmatter
     （date、topic_id），正文一字不动、可重复运行（幂等）。

匹配按三级兜底：编号（「创业笔记 943」「934-…」两种写法）→ 标题文本 → 正文开头。
还匹配不到的，交给 import 脚本按编号线性插值。

依赖 zsxq-cli（生产端、已登录）。不要用 mcp__zsxq__* —— 那是失效的 testing 端点。

用法：
  ./scripts/sync-zsxq-dates.py --dry-run        # 拉取 + 预览回填，不写源文件
  ./scripts/sync-zsxq-dates.py                  # 拉取 + 写入源文件 frontmatter
  ./scripts/sync-zsxq-dates.py --from-raw       # 复用 raw 缓存，离线重算匹配（快）
  ./scripts/sync-zsxq-dates.py --from-raw --dry-run
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

GROUP_ID = "511244584"
SOURCE_DIR = Path(
    "/Users/lucawu/Library/CloudStorage/Dropbox/Github/Luca/startupnotes"
)
HERE = Path(__file__).resolve().parent
DATES_JSON = HERE / "zsxq-dates.json"
RAW_CACHE = HERE / ".zsxq-topics-raw.json"

# zsxq titles encode the note number two ways:
#   "# 创业笔记 943：小鹅通重启上市"  and  "# 934-腾讯 ima 上线"
NUM_INLINE = re.compile(r"创业笔记\s*0*(\d+)")
NUM_PREFIX = re.compile(r"^#?\s*(?:创业笔记\s*)?0*(\d+)\s*[-—–:：]")
FILE_RE = re.compile(r"^0*(\d+)-(.+)\.md$")
ECLEAN = re.compile(r"<e\s+[^>]*?/>")               # zsxq custom <e .../> tags
KEY_LEN = 22                                         # chars used for content keys


def note_num(title: str) -> int | None:
    if not title:
        return None
    t = title.splitlines()[0]
    m = NUM_INLINE.search(t) or NUM_PREFIX.match(t)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 999:        # exclude years like "2026 年的 OKR"
            return n
    return None


def norm_title(title: str) -> str:
    """Strip number prefix / '#' / spaces so zsxq & folder titles compare equal."""
    if not title:
        return ""
    t = title.splitlines()[0]
    t = re.sub(r"^#?\s*", "", t)
    t = NUM_INLINE.sub("", t)
    t = re.sub(r"^\s*0*\d+\s*[-—–:：]\s*", "", t)
    t = re.sub(r"^\s*[:：]\s*", "", t)
    return re.sub(r"[\s　]+", "", t)


def content_key(text: str) -> str:
    """First KEY_LEN non-space chars of the body, after dropping a leading
    '# …' title line and zsxq <e> tags. Stable even when a note was expanded."""
    t = ECLEAN.sub("", text or "")
    lines = t.split("\n")
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    t = re.sub(r"[\s　]+", "", "".join(lines))
    return t[:KEY_LEN]


# --- zsxq fetch --------------------------------------------------------------

def find_cli() -> str:
    cli = shutil.which("zsxq-cli") or "/opt/homebrew/bin/zsxq-cli"
    if not Path(cli).exists():
        sys.exit("zsxq-cli not found. Install it or check PATH.")
    return cli


def fetch_page(cli: str, group_id: str, end_time: str | None, limit: int) -> dict:
    cmd = [cli, "group", "+topics", "--group-id", group_id,
           "--limit", str(limit), "--json"]
    if end_time:
        cmd += ["--end-time", end_time]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"zsxq-cli failed: {res.stderr.strip() or res.stdout[:200]}")
    return json.loads(res.stdout)


def fetch_all_topics(cli: str, group_id: str, limit: int,
                     delay: float, max_pages: int) -> list[dict]:
    """Page backwards through topics. zsxq repeats the tail one-at-a-time once
    real content is exhausted, so stop as soon as the cursor stalls."""
    topics: list[dict] = []
    seen: set[str] = set()
    end_time = None
    last_end_time = None
    stall = 0
    for page in range(1, max_pages + 1):
        data = fetch_page(cli, group_id, end_time, limit)
        if not data.get("success", True):
            raise RuntimeError(f"API error on page {page}: {data}")
        batch = data.get("topics_brief", [])
        new = [t for t in batch if str(t.get("topic_id")) not in seen]
        seen.update(str(t.get("topic_id")) for t in new)
        topics.extend(new)
        print(f"  page {page}: +{len(new)} new (total {len(topics)})", file=sys.stderr)
        end_time = data.get("next_end_time")
        if not data.get("has_more") or not batch or not end_time:
            break
        if not new or end_time == last_end_time:   # cursor no longer advancing
            stall += 1
            if stall >= 2:
                print(f"  cursor stalled at page {page}; stopping.", file=sys.stderr)
                break
        else:
            stall = 0
        last_end_time = end_time
        time.sleep(delay)
    return topics


def normalize_date(s: str) -> str:
    """'2026-05-27T08:50:06.380+0800' -> '2026-05-27T08:50:06+08:00'."""
    s = re.sub(r"\.\d+", "", s, count=1)              # drop fractional seconds
    s = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", s)   # +0800 -> +08:00
    return s


def norm_body(text: str) -> str:
    """Full normalized body (whitespace + <e> stripped) for substring matching."""
    return re.sub(r"[\s　]+", "", ECLEAN.sub("", text or ""))


def make_info(t: dict) -> dict:
    title = t.get("title", "") or ""
    counts = t.get("counts", {}) or {}
    return {
        "date": normalize_date(t["create_time"]),
        "topic_id": str(t.get("topic_id", "")),
        "digested": t.get("digested"),
        "readers": counts.get("readers"),
        "likes": counts.get("likes"),
        "title": title.splitlines()[0][:60] if title else "",
    }


def build_lookups(topics: list[dict]) -> tuple[dict, dict, dict]:
    """Return (by_num, by_title, by_content). Title/content keys that map to more
    than one distinct topic are AMBIGUOUS and dropped — matching on them would
    assign a wrong date (several different notes are all titled「闭环」)."""
    by_num: dict[str, dict] = {}
    title_topics: dict[str, dict] = {}
    content_topics: dict[str, dict] = {}
    for t in topics:
        title = t.get("title", "") or ""
        info = make_info(t)
        n = note_num(title)
        if n is not None and str(n) not in by_num:
            by_num[str(n)] = info
        nt = norm_title(title)
        if nt:
            title_topics.setdefault(nt, {})[info["topic_id"]] = info
        ck = content_key(t.get("content", ""))
        if len(ck) >= 12:
            content_topics.setdefault(ck, {})[info["topic_id"]] = info
    by_title = {k: next(iter(v.values())) for k, v in title_topics.items() if len(v) == 1}
    by_content = {k: next(iter(v.values())) for k, v in content_topics.items() if len(v) == 1}
    return by_num, by_title, by_content


# --- source frontmatter back-fill -------------------------------------------

def parse_simple_frontmatter(lines: list[str]) -> dict:
    fm = {}
    for ln in lines:
        if ":" in ln:
            k, v = ln.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def split_source(text: str) -> tuple[dict, str]:
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is not None:
            return parse_simple_frontmatter(lines[1:end]), "\n".join(lines[end + 1:])
    return {}, text


def render_frontmatter(fm: dict) -> str:
    out = ["---"]
    for k in ("date", "topic_id"):
        if k in fm:
            out.append(f"{k}: {fm[k]}")
    for k, v in fm.items():
        if k not in ("date", "topic_id"):
            out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out) + "\n"


def backfill_file(path: Path, info: dict, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    existing, body = split_source(text)
    merged = dict(existing)
    merged["date"] = info["date"]
    merged["topic_id"] = f'"{info["topic_id"]}"'
    new_text = render_frontmatter(merged) + body
    if new_text == text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def source_notes(source_dir: Path) -> list[tuple[str, str, str, Path]]:
    """(number, norm_title, content_key, path) for each numbered note, sans Temp/."""
    out = []
    for p in sorted(source_dir.rglob("*.md")):
        if "Temp" in p.parts:
            continue
        m = FILE_RE.match(p.name)
        if not m:
            continue
        _, body = split_source(p.read_text(encoding="utf-8"))
        out.append((str(int(m.group(1))), norm_title(m.group(2)), content_key(body), p))
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--group-id", default=GROUP_ID)
    ap.add_argument("--source-dir", type=Path, default=SOURCE_DIR)
    ap.add_argument("--dates-json", type=Path, default=DATES_JSON)
    ap.add_argument("--dry-run", action="store_true",
                    help="预览回填，不写源文件")
    ap.add_argument("--from-raw", action="store_true",
                    help="复用 raw 缓存离线重算（不联网）")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--delay", type=float, default=0.3)
    ap.add_argument("--max-pages", type=int, default=120)
    args = ap.parse_args()

    # 1) get topics (network or raw cache) and build lookups
    if args.from_raw:
        if not RAW_CACHE.exists():
            sys.exit(f"--from-raw but {RAW_CACHE.name} missing; run once online first.")
        topics = json.loads(RAW_CACHE.read_text(encoding="utf-8"))
        print(f"Loaded {len(topics)} topics from {RAW_CACHE.name}")
    else:
        cli = find_cli()
        print(f"Fetching topics from group {args.group_id} via zsxq-cli …", file=sys.stderr)
        topics = fetch_all_topics(cli, args.group_id, args.limit, args.delay, args.max_pages)
        RAW_CACHE.write_text(json.dumps(topics, ensure_ascii=False), encoding="utf-8")
    by_num, by_title, by_content = build_lookups(topics)
    args.dates_json.write_text(
        json.dumps(by_num, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(topics)} topics → {len(by_num)} by-number / "
          f"{len(by_title)} by-title / {len(by_content)} by-content keys")

    # 2) back-fill source frontmatter. Two passes so the reliable number match
    #    wins, and every zsxq topic maps to AT MOST ONE note (no stolen dates):
    #    duplicate-numbered / duplicate-titled notes fall through to interpolation.
    notes = source_notes(args.source_dir)
    title_counts: dict[str, int] = {}
    content_counts: dict[str, int] = {}
    for _, nt, ck, _ in notes:
        if nt:
            title_counts[nt] = title_counts.get(nt, 0) + 1
        if len(ck) >= 12:
            content_counts[ck] = content_counts.get(ck, 0) + 1

    assigned: set[str] = set()           # topic_ids already claimed
    result: dict = {}                    # path -> (via, info)

    def claim(path, info, via) -> bool:
        tid = info["topic_id"]
        if tid in assigned:
            return False
        assigned.add(tid)
        result[path] = (via, info)
        return True

    for num, nt, ck, path in notes:      # pass 1: number (most reliable)
        if num in by_num:
            claim(path, by_num[num], "num")
    for num, nt, ck, path in notes:      # pass 2: unique title, then unique content
        if path in result:
            continue
        if nt and title_counts.get(nt) == 1 and nt in by_title:
            if claim(path, by_title[nt], "title"):
                continue
        if len(ck) >= 12 and content_counts.get(ck) == 1 and ck in by_content:
            claim(path, by_content[ck], "content")

    # pass 3: unique mid-body phrase — recovers notes whose title/opening you
    # edited (the zsxq topic exists, just keyed differently). An exact 18-char
    # run matching exactly one still-unclaimed topic = very low false-positive.
    topic_pairs = [(make_info(t), norm_body(t.get("content", ""))) for t in topics]
    norm_contents = [(info["topic_id"], nb) for info, nb in topic_pairs]
    topic_info = {info["topic_id"]: info for info, _ in topic_pairs}
    for num, nt, ck, path in notes:
        if path in result:
            continue
        _, body = split_source(path.read_text(encoding="utf-8"))
        nb = norm_body(re.sub(r"^#.*$", "", body, count=1, flags=re.M))
        if len(nb) < 40:
            continue
        probe = nb[int(len(nb) * 0.45): int(len(nb) * 0.45) + 18]
        if len(probe) < 18:
            continue
        hits = {tid for tid, tn in norm_contents if tid not in assigned and probe in tn}
        if len(hits) == 1:
            claim(path, topic_info[next(iter(hits))], "phrase")

    # pass 4: consistency guard. The 创业笔记 numbering is ~chronological, so a
    # FUZZY match whose date sits >1 year off its number-neighbours is almost
    # certainly the wrong topic (another note with a similar phrase). Drop it so
    # it interpolates from neighbours instead. Number matches are trusted as-is.
    dated = sorted(
        (int(num), datetime.fromisoformat(result[path][1]["date"]), path, result[path][0])
        for num, nt, ck, path in notes if path in result
    )
    only_dates = [d for _, d, _, _ in dated]
    dropped = 0
    for idx, (n, d, path, via) in enumerate(dated):
        if via == "num":
            continue
        lo, hi = max(0, idx - 6), min(len(dated), idx + 7)
        neigh = sorted(only_dates[j] for j in range(lo, hi) if j != idx)
        if len(neigh) < 4:
            continue
        med = neigh[len(neigh) // 2]
        if abs((d - med).days) > 365:
            _, info = result.pop(path)
            assigned.discard(info["topic_id"])
            dropped += 1
            print(f"  pass4: dropped #{n} ({via}: {d.date()} vs neighbours ~{med.date()}) "
                  "→ interpolate", file=sys.stderr)
    if dropped:
        print(f"  pass4 dropped {dropped} inconsistent fuzzy match(es)", file=sys.stderr)

    updated = 0
    by_via = {"num": 0, "title": 0, "content": 0, "phrase": 0}
    unmatched: list[str] = []
    for num, nt, ck, path in notes:
        if path not in result:
            unmatched.append(num)
            continue
        via, info = result[path]
        by_via[via] += 1
        if backfill_file(path, info, args.dry_run):
            updated += 1
    matched = len(result)

    verb = "would update" if args.dry_run else "updated"
    print(f"\nSource notes: {len(notes)} | matched: {matched} "
          f"(num {by_via['num']}, title {by_via['title']}, content {by_via['content']}, "
          f"phrase {by_via['phrase']}) | {verb}: {updated} | unmatched: {len(unmatched)}")
    if unmatched:
        print("  unmatched numbers:", ", ".join(unmatched[:40]),
              "…" if len(unmatched) > 40 else "")


if __name__ == "__main__":
    main()
