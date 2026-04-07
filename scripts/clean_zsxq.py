#!/usr/bin/env python3
"""
clean_zsxq.py — 清理 zsxq 导出 markdown 里的非法 <e> 标签

zsxq 导出的 <e type="web" .../> 和 <e type="mention" .../> 是自闭合
自定义元素，HTML5 解析器会把它们当成开标签，吞掉后续所有内容，
导致 Hugo 渲染时笔记显示为空。

转换规则：
  <e type="web" href="X" title="Y" /> → [Y_decoded](X_decoded)
  <e type="mention" title="@N" />     → @N

用法：
  ./scripts/clean_zsxq.py content/notes/             # 处理整个目录（递归）
  ./scripts/clean_zsxq.py content/notes/foo.md       # 处理单个文件
  ./scripts/clean_zsxq.py --dry-run content/notes/   # 只预览，不写入

每次从 zsxq 拉新内容后，跑一遍这个脚本即可。
"""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

TAG_RE = re.compile(r'<e\s+([^/>]+?)\s*/>')
ATTR_RE = re.compile(r'(\w+)="([^"]*)"')


def parse_attrs(attr_str: str) -> dict:
    return dict(ATTR_RE.findall(attr_str))


def replace_tag(match: re.Match) -> str:
    attrs = parse_attrs(match.group(1))
    t = attrs.get("type", "")
    if t == "web":
        href = unquote(attrs.get("href", ""))
        title = unquote(attrs.get("title", "")) or href
        if not href:
            return ""
        return f"[{title}]({href})"
    if t == "mention":
        return attrs.get("title", "").strip()
    print(f"  ⚠ unknown <e type={t}> in {attrs}", file=sys.stderr)
    return match.group(0)


def process_file(path: Path, dry_run: bool) -> int:
    text = path.read_text(encoding="utf-8")
    if "<e type=" not in text:
        return 0
    new_text, n = TAG_RE.subn(replace_tag, text)
    if n and not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return n


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("path", type=Path, help="文件或目录")
    p.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    args = p.parse_args()

    if args.path.is_file():
        files = [args.path]
    elif args.path.is_dir():
        files = sorted(args.path.rglob("*.md"))
    else:
        sys.exit(f"路径不存在: {args.path}")

    modified = 0
    total = 0
    for f in files:
        n = process_file(f, args.dry_run)
        if n:
            modified += 1
            total += n
            print(f"  {f}: {n}")

    verb = "would modify" if args.dry_run else "modified"
    print(f"\n✓ {verb} {modified} files, {total} replacements")


if __name__ == "__main__":
    main()
