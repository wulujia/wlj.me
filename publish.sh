#!/bin/bash
# publish.sh — 从 markdown 文件发布文章到 wlj.me
# 用法: ./publish.sh input.md [tag1,tag2,...]
# 顶层 # 标题作为 title，其余内容作为正文
# slug 从文件名取（去掉 .md 后缀）

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUT="$1"
TAGS="${2:-}"

if [ ! -f "$INPUT" ]; then
  echo "文件不存在: $INPUT" >&2
  exit 1
fi

# 从第一行 # 标题提取 title
TITLE=$(grep -m1 '^# ' "$INPUT" | sed 's/^# //')
if [ -z "$TITLE" ]; then
  echo "找不到 # 标题" >&2
  exit 1
fi

# slug 从输入文件名取
SLUG=$(basename "$INPUT" .md)
DATE=$(date +%Y-%m-%dT%H:%M:%S%z | sed 's/\([0-9][0-9]\)$/:\1/')
TARGET="$REPO_DIR/content/posts/${SLUG}.md"

if [ -f "$TARGET" ]; then
  echo "文件已存在: $TARGET" >&2
  exit 1
fi

# 构建 tags 行
if [ -n "$TAGS" ]; then
  TAG_JSON=$(echo "$TAGS" | tr ',' '\n' | sed 's/.*/"&"/' | paste -sd',' - | sed 's/^/[/;s/$/]/')
  TAG_LINE="tags: $TAG_JSON"
else
  TAG_LINE=""
fi

# 提取正文（跳过第一行 # 标题和紧随的空行）
BODY=$(awk 'NR==1 && /^# /{found=1; next} found && NR==2 && /^$/{next} {found=0} !found || NR>2{print}' "$INPUT")

# 写入文件
{
  echo "---"
  echo "title: \"$TITLE\""
  echo "date: $DATE"
  [ -n "$TAG_LINE" ] && echo "$TAG_LINE"
  echo "draft: false"
  echo "slug: \"$SLUG\""
  echo "---"
  echo ""
  echo "$BODY"
} > "$TARGET"

# git commit & push
cd "$REPO_DIR"
git add "$TARGET"
git commit -m "Add post: $TITLE"
git push

echo "已发布: $SLUG"
