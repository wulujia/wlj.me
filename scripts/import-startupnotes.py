#!/usr/bin/env python3
"""
import-startupnotes.py — 把源创业笔记切半，导入 wlj.me 的 startupnotes section

源：Luca/startupnotes/NNN-*.md（已由 sync-zsxq-dates.py 回填真实 date）。
对每篇：
  1. 取标题（首行 # …），从正文移除；去掉尾部 #starupnotes。
  2. 切半（cut_half）：约 50% 处、段落边界、尽量切在「payoff」之前，制造好奇缺口。
  3. 只把前半段 + frontmatter 写到 content/startupnotes/<slug>.md。
     —— 后半段算出来只为校验「确实有内容被留在星球」，绝不写入仓库。
日期：优先用源文件 frontmatter 的 date；缺失则查 zsxq-dates.json；再缺失按编号线性插值。

用法：
  ./scripts/import-startupnotes.py --dry-run            # 不写文件，只报告
  ./scripts/import-startupnotes.py --limit-notes 5      # 只导前 5 篇（调试）
  ./scripts/import-startupnotes.py                      # 全量导入
"""
import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE_DIR = Path(
    "/Users/lucawu/Library/CloudStorage/Dropbox/Github/Luca/startupnotes"
)
OUT_DIR = REPO / "content" / "startupnotes"
DATES_JSON = REPO / "scripts" / "zsxq-dates.json"
MANIFEST = REPO / "scripts" / "startupnotes-manifest.csv"

FILE_NUM_RE = re.compile(r"^0*(\d+)-")
TITLE_RE = re.compile(r"^#\s+(.*?)\s*$", re.M)
FOOTER_RE = re.compile(r"\n*#\s*starupnotes\s*$", re.I)
SHORT_NOTE_CHARS = 250          # below this, publish whole (half is meaningless)
CUT_LO, CUT_HI = 0.45, 0.60     # acceptable cut window as fraction of total

# A block that begins the "payoff" — cut right before it so the answer stays paid.
PAYOFF_RE = re.compile(
    r"^(结论|所以|因此|我的做法|我的方法|具体做法|具体|第一|首先|关键|核心|"
    r"重点|总结|答案|后来|于是|建议|那么|其实|说白了)"
)
LIST_RE = re.compile(r"^([-*]|\d+[.)、]|[一二三四五六七八九十]+[、.])")


# --- frontmatter helpers -----------------------------------------------------

def split_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is not None:
            fm = {}
            for ln in lines[1:end]:
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"')
            return fm, "\n".join(lines[end + 1:])
    return {}, text


def yaml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# --- the half-cut ------------------------------------------------------------

def split_blocks(body: str) -> list[str]:
    raw = re.split(r"\n\s*\n", body.strip())
    return [b.strip() for b in raw if b.strip()]


def is_payoff(block: str) -> bool:
    first = block.lstrip()
    return bool(first.startswith("#") or LIST_RE.match(first) or PAYOFF_RE.match(first))


def cut_by_sentence(body: str, frac: float) -> tuple[str, str]:
    target = int(len(body) * frac)
    ends = [m.end() for m in re.finditer(r"[。！？\n]", body)]
    if not ends:
        return body, ""
    cut = min(ends, key=lambda e: abs(e - target))
    return body[:cut].strip(), body[cut:].strip()


def cut_half(body: str) -> tuple[str, str]:
    """Return (free_half, withheld). Withheld is never written — verification only."""
    body = body.strip()
    total = len(body)
    if total < SHORT_NOTE_CHARS:
        return body, ""

    blocks = split_blocks(body)
    if len(blocks) >= 2:
        lens = [len(b) for b in blocks]
        cum_before = []
        c = 0
        for l in lens:
            cum_before.append(c)
            c += l
        T = c
        lo, hi = CUT_LO * T, CUT_HI * T
        target = 0.5 * T
        candidates = [i for i in range(1, len(blocks)) if lo <= cum_before[i] <= hi]
        if candidates:
            payoff = [i for i in candidates if is_payoff(blocks[i])]
            pool = payoff or candidates
            cut = min(pool, key=lambda i: abs(cum_before[i] - target))
            return "\n\n".join(blocks[:cut]), "\n\n".join(blocks[cut:])
        # no block boundary in window -> closest boundary to 50%
        cut = min(range(1, len(blocks)), key=lambda i: abs(cum_before[i] - target))
        return "\n\n".join(blocks[:cut]), "\n\n".join(blocks[cut:])

    # single block -> sentence-level cut
    return cut_by_sentence(body, 0.5)


def make_teaser(text: str, n: int = 120) -> str:
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)   # links -> label
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)           # blockquote marker
    t = re.sub(r"^\s*([-*]|\d+[.)、])\s*", "", t, flags=re.M)  # list bullets
    t = re.sub(r"[#*`]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n]


# --- date resolution ---------------------------------------------------------

def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s)


def interpolate_dates(rows: list[dict]) -> None:
    """Fill any row with date=None by linear interpolation over note number."""
    known = [(int(r["num"]), parse_dt(r["date"])) for r in rows if r["date"]]
    if not known:
        sys.exit("No dates available at all — run sync-zsxq-dates.py first.")
    known.sort()
    for r in rows:
        if r["date"]:
            continue
        n = int(r["num"])
        lo = max((k for k in known if k[0] <= n), default=None)
        hi = min((k for k in known if k[0] >= n), default=None)
        if lo and hi and lo[0] != hi[0]:
            frac = (n - lo[0]) / (hi[0] - lo[0])
            ts = lo[1].timestamp() + frac * (hi[1].timestamp() - lo[1].timestamp())
            r["date"] = datetime.fromtimestamp(ts, tz=lo[1].tzinfo).replace(microsecond=0).isoformat()
        else:
            r["date"] = (lo or hi)[1].replace(microsecond=0).isoformat()


# --- main --------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source-dir", type=Path, default=SOURCE_DIR)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    ap.add_argument("--dates-json", type=Path, default=DATES_JSON)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit-notes", type=int, default=0, help="只处理前 N 篇（调试）")
    args = ap.parse_args()

    import json
    date_lookup = {}
    if args.dates_json.exists():
        date_lookup = json.loads(args.dates_json.read_text(encoding="utf-8"))

    # collect source notes
    notes = []
    for p in sorted(args.source_dir.rglob("*.md")):
        if "Temp" in p.parts:
            continue
        m = FILE_NUM_RE.match(p.name)
        if m:
            notes.append((int(m.group(1)), p))
    notes.sort()
    if args.limit_notes:
        notes = notes[: args.limit_notes]

    rows = []
    used_slugs: set[str] = set()
    for num, path in notes:
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        tm = TITLE_RE.search(body)
        title = tm.group(1).strip() if tm else f"创业笔记 {num}"
        if tm:
            body = body[: tm.start()] + body[tm.end():]
        body = FOOTER_RE.sub("", body).strip()

        free, withheld = cut_half(body)
        date = fm.get("date") or (date_lookup.get(str(num), {}) or {}).get("date") or None
        base = f"startup-note-{num:03d}"          # a few numbers label two notes
        slug, n2 = base, 2
        while slug in used_slugs:
            slug, n2 = f"{base}-{n2}", n2 + 1
        used_slugs.add(slug)
        rows.append({
            "num": str(num),
            "path": path,
            "slug": slug,
            "title": title,
            "date": date,
            "free": free,
            "withheld_chars": len(withheld),
            "free_chars": len(free),
            "teaser": make_teaser(free),
            "digested": (date_lookup.get(str(num), {}) or {}).get("digested"),
        })

    interpolate_dates(rows)

    # write content files
    if not args.dry_run:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        write_index(args.out_dir, rows)
    written = 0
    for r in rows:
        fmtext = (
            "---\n"
            f"title: {yaml_str(r['title'])}\n"
            f"date: {r['date']}\n"
            f"lastmod: {r['date']}\n"
            'author: "Luca"\n'
            'tags: ["Startup"]\n'
            "draft: false\n"
            f'slug: "{r["slug"]}"\n'
            f"summary: {yaml_str(r['teaser'])}\n"
            "paywall: true\n"
            "---\n\n"
            f"{r['free']}\n"
        )
        if not args.dry_run:
            (args.out_dir / f"{r['slug']}.md").write_text(fmtext, encoding="utf-8")
        written += 1

    # manifest
    if not args.dry_run:
        with MANIFEST.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["num", "slug", "date", "digested",
                        "free_chars", "withheld_chars", "title", "teaser"])
            for r in rows:
                w.writerow([r["num"], r["slug"], r["date"], r["digested"],
                            r["free_chars"], r["withheld_chars"], r["title"], r["teaser"]])

    # report
    withheld_empty = [r["num"] for r in rows if r["withheld_chars"] == 0 and r["free_chars"] >= SHORT_NOTE_CHARS]
    verb = "would write" if args.dry_run else "wrote"
    print(f"{verb} {written} notes to {args.out_dir}")
    print(f"  median free chars: {sorted(r['free_chars'] for r in rows)[len(rows)//2]}")
    print(f"  notes with NOTHING withheld (>=400 chars): {len(withheld_empty)} {withheld_empty[:10]}")
    print(f"  date range: {min(r['date'] for r in rows)[:10]} .. {max(r['date'] for r in rows)[:10]}")


def write_index(out_dir: Path, rows: list[dict]) -> None:
    oldest = min(r["date"] for r in rows)
    idx = (
        "---\n"
        'title: "创业笔记"\n'
        f"date: {oldest}\n"
        'description: "做知识星球这些年攒下的创业、产品、运营、安全笔记。这里是免费试读，完整版在知识星球。"\n'
        "---\n\n"
        "做知识星球的过程里，我把关于创业、产品、运营、安全的思考写成了一篇篇短笔记。\n\n"
        "这里放的是**免费试读**（每篇约前一半）。想看完整版、以及还在持续更新的 1800+ 篇，"
        "欢迎来知识星球「星球创业笔记」。\n"
    )
    (out_dir / "_index.md").write_text(idx, encoding="utf-8")


if __name__ == "__main__":
    main()
