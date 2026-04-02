#!/usr/bin/env python3
"""Reorganize blog tags: consolidate 32 tags into ~16, auto-tag WeChat-only articles."""

import argparse
import csv
import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime

POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content", "posts")

# ── Old → New tag mapping ──────────────────────────────────────────────────────

OLD_TO_NEW = {
    "WeChat": "WeChat",
    "Reading": "Reading",
    "Product": "Product",
    "Security": "Security",
    "Idea": "Idea",
    "Tools": "Tools",
    "Movie": "Movie",
    "Investment": "Investment",
    "Marketing": "Marketing",
    "Work": "Work",
    # Consolidations
    "Linux": "Tech",
    "Arch Linux": "Tech",
    "Ubuntu": "Tech",
    "ssh": "Tech",
    "neovim": "Tech",
    "CLI": "Tech",
    "mac": "Tools",
    "iterm2": "Tools",
    "Chrome": "Tools",
    "Obsidian": "Tools",
    "Font": "Tools",
    "Input Method": "Tools",
    "Slax Note": "Tools",
    "Self-improvement": "Life",
    "Habit": "Life",
    "Business": "Startup",
    "Company": "Startup",
    "EasyDay": "Startup",
    "Misc": "Idea",
    "Prompt": "AI",
    "Research": "Tools",
    "Tips": None,  # Score-based reassignment
}

# ── Keyword rules for auto-tagging ─────────────────────────────────────────────
# title_kw: +3 points each; body_kw: +1 per occurrence (capped at 5 per keyword)

TAG_RULES = {
    "AI": {
        "title_kw": [
            "AI", "ChatGPT", "GPT", "LLM", "大模型", "人工智能",
            "Claude", "Gemini", "OpenAI", "Manus", "Perplexity",
            "Agent", "Copilot", "Deep Research", "Operator", "DeepSeek",
        ],
        "body_kw": [
            "AI", "ChatGPT", "GPT", "LLM", "大模型", "人工智能",
            "Claude", "OpenAI", "Manus", "Perplexity", "提示词",
            "prompt", "token", "AGI", "机器学习", "深度学习", "DeepSeek",
        ],
    },
    "Startup": {
        "title_kw": [
            "创业", "创始人", "公司", "联合创始人", "融资", "知识星球",
            "EasyDay", "小日子", "经营", "星球", "全球化",
        ],
        "body_kw": [
            "创业", "创始人", "公司经营", "公司文化", "融资", "估值",
            "联合创始人", "知识星球", "EasyDay", "小日子", "团队管理",
            "CEO", "裁员", "盈利", "YC", "创业公司", "商业模式",
            "合伙人", "股权",
        ],
    },
    "Product": {
        "title_kw": [
            "产品", "MVP", "用户体验", "设计", "迭代", "简化",
            "功能", "需求",
        ],
        "body_kw": [
            "产品设计", "产品思维", "MVP", "用户体验", "产品迭代",
            "产品经理", "交互设计", "用户需求", "用户研究", "产品方向",
            "产品策略",
        ],
    },
    "Reading": {
        "title_kw": [
            "读书", "阅读", "书评", "好书", "读后", "推荐书", "看完",
            "月阅读", "传记", "这本书",
        ],
        "body_kw": [
            "读书", "阅读", "书评", "看完了", "这本书", "推荐这本",
            "读后感", "作者写", "书中",
        ],
    },
    "Life": {
        "title_kw": [
            "习惯", "运动", "微笑", "人生", "打卡", "健康", "挑战",
            "注意力", "冥想", "静坐", "散步", "断舍离", "孩子",
            "旅行", "父亲", "家人", "生活", "忠告", "清醒",
        ],
        "body_kw": [
            "习惯", "运动", "跑步", "健身", "冥想", "静坐", "散步",
            "打卡", "自律", "早起", "睡眠", "减肥", "生活方式",
        ],
    },
    "Investment": {
        "title_kw": ["投资", "理财", "财富自由", "股东信"],
        "body_kw": [
            "投资", "理财", "股票", "基金", "财务自由", "复利",
            "巴菲特", "估值", "资产", "现金流",
        ],
    },
    "Marketing": {
        "title_kw": ["营销", "增长", "流量", "推广", "用户增长", "卖货", "品牌"],
        "body_kw": [
            "营销", "增长", "流量", "推广", "转化率", "获客",
            "拉新", "留存", "广告", "品牌",
        ],
    },
    "Writing": {
        "title_kw": ["写作", "写公众号", "写书", "写文章", "日记"],
        "body_kw": ["写作", "写文章", "写公众号", "创作", "文笔", "写日记"],
    },
    "Tools": {
        "title_kw": [
            "工具", "软件", "装备", "App", "效率", "Slax", "Reader",
            "常用产品", "墨水屏", "Mac",
        ],
        "body_kw": [
            "工具", "软件", "效率", "App", "应用", "Slax Reader",
            "墨水屏", "手机", "相机", "自动化",
        ],
    },
    "Security": {
        "title_kw": [
            "安全", "隐私", "黑客", "漏洞", "密码", "后门",
            "骗子", "加密", "诈骗", "威胁",
        ],
        "body_kw": [
            "安全", "隐私", "黑客", "漏洞", "密码", "后门",
            "加密", "攻击", "钓鱼", "恶意", "防护",
        ],
    },
    "Tech": {
        "title_kw": [
            "技术", "开发", "Linux", "编程", "代码", "GitHub",
            "Flutter", "开源", "API", "Debian", "Ubuntu", "Arch",
            "ibus", "fcitx",
        ],
        "body_kw": [
            "技术", "开发", "Linux", "编程", "代码", "GitHub",
            "API", "服务器", "开源", "框架", "数据库",
            "Debian", "Ubuntu", "Arch Linux",
        ],
    },
    "Work": {
        "title_kw": ["工作", "职场", "办公", "OKR", "会议", "远程办公", "管理"],
        "body_kw": ["工作方法", "OKR", "团队协作", "远程办公", "领导力", "协作"],
    },
    "Community": {
        "title_kw": ["社群", "社区", "付费社群", "圈子", "组队"],
        "body_kw": ["社群", "社区", "社群运营", "圈子", "付费社群", "成员"],
    },
    "Movie": {
        "title_kw": ["电影", "观影", "纪录片", "影片"],
        "body_kw": ["电影", "观影", "影片", "纪录片", "影院"],
    },
    "Idea": {
        "title_kw": [],  # Fallback category, not scored
        "body_kw": [],
    },
}

FALLBACK_TAG = "Idea"


# ── Data structures ────────────────────────────────────────────────────────────

@dataclass
class Article:
    filepath: str
    filename: str
    title: str
    old_tags: list
    body: str
    raw_content: str
    new_tags: list = field(default_factory=list)
    change_type: str = ""
    scores: dict = field(default_factory=dict)


# ── Core functions ─────────────────────────────────────────────────────────────

def parse_frontmatter(content: str):
    """Extract title and tags from YAML frontmatter."""
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        return None, []
    fm = m.group(1)
    title_m = re.search(r'^title:\s*"(.*?)"', fm, re.MULTILINE)
    tags_m = re.search(r'^tags:\s*\[(.*?)\]', fm, re.MULTILINE)
    title = title_m.group(1) if title_m else ""
    tags = []
    if tags_m:
        tags = [t.strip().strip('"').strip("'") for t in tags_m.group(1).split(",") if t.strip()]
    return title, tags


def load_articles():
    """Load all markdown articles from POSTS_DIR."""
    articles = []
    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(POSTS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        title, tags = parse_frontmatter(content)
        if title is None:
            continue
        # Body = everything after frontmatter
        body_start = content.index("---", 3) + 3
        body = content[body_start:].strip()
        articles.append(Article(
            filepath=fpath, filename=fname, title=title,
            old_tags=tags, body=body, raw_content=content,
        ))
    return articles


def _match_keyword(kw: str, text: str) -> int:
    """Match keyword in text. Uses word boundaries for ASCII keywords to avoid
    substring false positives (e.g., 'AI' matching 'pair')."""
    kw_lower = kw.lower()
    if kw.isascii():
        return len(re.findall(r'\b' + re.escape(kw_lower) + r'\b', text, re.IGNORECASE))
    else:
        return text.count(kw_lower)


def score_article(title: str, body: str) -> dict:
    """Score an article against all tag categories. Returns {tag: score}."""
    scores = {}
    body_text = body[:1500].lower()
    title_lower = title.lower()
    for tag, rules in TAG_RULES.items():
        if tag == FALLBACK_TAG:
            continue
        score = 0
        for kw in rules["title_kw"]:
            if _match_keyword(kw, title_lower) > 0:
                score += 3
        for kw in rules["body_kw"]:
            count = _match_keyword(kw, body_text)
            if count > 0:
                score += min(count, 5)
        if score > 0:
            scores[tag] = score
    return scores


def select_top_tags(scores: dict, max_tags: int = 2) -> list:
    """Pick top 1-2 tags from scores. Second tag needs >= 50% of best score."""
    if not scores:
        return []
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    selected = [ranked[0][0]]
    if len(ranked) > 1 and ranked[1][1] >= ranked[0][1] * 0.5 and max_tags >= 2:
        selected.append(ranked[1][0])
    return selected


def compute_new_tags(article: Article):
    """Determine new tags for an article."""
    old = article.old_tags

    is_wechat_only = old == ["WeChat"]
    has_wechat = "WeChat" in old

    if is_wechat_only:
        # Score content and add 1-2 content tags
        scores = score_article(article.title, article.body)
        content_tags = select_top_tags(scores) or [FALLBACK_TAG]
        article.new_tags = ["WeChat"] + content_tags
        article.scores = scores
        article.change_type = "scored"
        return

    # Map old tags through consolidation table
    mapped = []
    needs_scoring = False
    for t in old:
        if t in OLD_TO_NEW:
            new = OLD_TO_NEW[t]
            if new is None:
                needs_scoring = True
            elif new not in mapped:
                mapped.append(new)
        else:
            # Unknown tag — keep as-is (shouldn't happen)
            if t not in mapped:
                mapped.append(t)

    if needs_scoring:
        scores = score_article(article.title, article.body)
        extra = select_top_tags(scores, max_tags=1)
        article.scores = scores
        for t in extra:
            if t not in mapped:
                mapped.append(t)

    # For non-WeChat articles that only had a mapped tag, ensure at least one content tag
    if mapped == ["WeChat"] or not mapped:
        scores = score_article(article.title, article.body)
        content_tags = select_top_tags(scores) or [FALLBACK_TAG]
        mapped.extend(t for t in content_tags if t not in mapped)
        article.scores = scores

    article.new_tags = mapped
    article.change_type = "mapped" if mapped != old else "unchanged"


def build_tags_line(tags: list) -> str:
    """Format tags as YAML array string."""
    return 'tags: [' + ", ".join(f'"{t}"' for t in tags) + ']'


def apply_tag_change(content: str, new_tags: list) -> str:
    """Replace only the tags line in frontmatter."""
    new_line = build_tags_line(new_tags)
    return re.sub(r'^tags:\s*\[.*?\]', new_line, content, count=1, flags=re.MULTILINE)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Reorganize blog tags")
    parser.add_argument("--apply", action="store_true", help="Actually modify files (default: preview only)")
    parser.add_argument("--output", default="retag_report.csv", help="CSV report path")
    args = parser.parse_args()

    articles = load_articles()
    print(f"Loaded {len(articles)} articles\n")

    # Compute new tags for all articles
    for a in articles:
        compute_new_tags(a)

    changed = [a for a in articles if a.old_tags != a.new_tags]
    unchanged = [a for a in articles if a.old_tags == a.new_tags]

    # ── Preview report ──────────────────────────────────────────────────────
    print("=" * 60)
    print(f"  Tag Reorganization {'PREVIEW' if not args.apply else 'APPLYING'}")
    print("=" * 60)
    print(f"\n  Total articles:   {len(articles)}")
    print(f"  To modify:        {len(changed)}")
    print(f"  Unchanged:        {len(unchanged)}")

    # Tag stats before/after
    old_counter = Counter()
    new_counter = Counter()
    for a in articles:
        for t in a.old_tags:
            old_counter[t] += 1
        for t in a.new_tags:
            new_counter[t] += 1

    print(f"\n{'─' * 60}")
    print(f"  {'Tag':<16} {'Before':>8} {'After':>8}")
    print(f"{'─' * 60}")
    all_tags = sorted(set(list(old_counter.keys()) + list(new_counter.keys())))
    for t in all_tags:
        before = old_counter.get(t, 0)
        after = new_counter.get(t, 0)
        marker = ""
        if before == 0:
            marker = " (new)"
        elif after == 0:
            marker = " (removed)"
        print(f"  {t:<16} {before:>8} {after:>8}{marker}")

    # Show scored (WeChat-only) examples
    scored = [a for a in changed if a.change_type == "scored"]
    if scored:
        print(f"\n{'─' * 60}")
        print(f"  WeChat articles → content tags ({len(scored)} articles)")
        print(f"{'─' * 60}")
        for a in scored[:30]:
            top_scores = sorted(a.scores.items(), key=lambda x: -x[1])[:3]
            score_str = ", ".join(f"{t}={s}" for t, s in top_scores) if top_scores else "none"
            print(f"  {a.filename}")
            print(f"    Title:  {a.title}")
            print(f"    New:    {a.new_tags}")
            print(f"    Scores: {score_str}")
        if len(scored) > 30:
            print(f"  ... and {len(scored) - 30} more")

    # Show mapped (consolidation) changes
    mapped = [a for a in changed if a.change_type == "mapped"]
    if mapped:
        print(f"\n{'─' * 60}")
        print(f"  Consolidated tags ({len(mapped)} articles)")
        print(f"{'─' * 60}")
        for a in mapped:
            print(f"  {a.old_tags} → {a.new_tags}  {a.filename}")

    # Show fallback articles
    fallback = [a for a in articles if FALLBACK_TAG in a.new_tags and a.change_type == "scored"]
    if fallback:
        print(f"\n{'─' * 60}")
        print(f"  Fallback → Idea ({len(fallback)} articles)")
        print(f"{'─' * 60}")
        for a in fallback:
            print(f"  {a.filename}: {a.title}")

    # ── Write CSV report ────────────────────────────────────────────────────
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "title", "old_tags", "new_tags", "change_type", "top_scores"])
        for a in articles:
            top = sorted(a.scores.items(), key=lambda x: -x[1])[:3] if a.scores else []
            writer.writerow([
                a.filename, a.title,
                "|".join(a.old_tags), "|".join(a.new_tags),
                a.change_type,
                ", ".join(f"{t}={s}" for t, s in top),
            ])
    print(f"\nCSV report: {args.output}")

    # ── Apply changes ───────────────────────────────────────────────────────
    if args.apply:
        backup_dir = os.path.join(POSTS_DIR, f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(backup_dir)
        count = 0
        for a in changed:
            # Backup
            shutil.copy2(a.filepath, os.path.join(backup_dir, a.filename))
            # Apply
            new_content = apply_tag_change(a.raw_content, a.new_tags)
            with open(a.filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
        print(f"\nApplied changes to {count} files")
        print(f"Backup at: {backup_dir}")
    else:
        print("\nDry run — no files modified. Use --apply to apply changes.")


if __name__ == "__main__":
    main()
