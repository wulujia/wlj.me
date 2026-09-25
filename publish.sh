#!/bin/bash
# publish.sh — publish content to wlj.me
#
# Posts:
#   ./publish.sh input.md [tag1,tag2,...]
#   ./publish.sh post input.md [tag1,tag2,...]
#   ./publish.sh update input.md [tag1,tag2,...]
#   First-line "# Title" becomes the title, the rest is the body.
#   slug = input file name without .md
#
# Reading (整理) pages:
#   ./publish.sh reading <dir-or-index.html> --category <book|report|documentary|misc> --author "<name>" [options]
#   Options:
#     --slug <slug>            default: input directory name
#     --year <yyyy>            default: current year
#     --subtitle "<text>"
#     --original-url <url>
#     --post-slug <slug>       related post under /posts/<slug>/
#     --changelog "<text>"     custom CHANGELOG line (default is built from title + description)
#     --noindex                page is noindex; also excluded from sitemap
#     --update                 replace an existing page; keep its list metadata
#     --dry-run                validate and show the plan, write nothing
#   title and description are read from <title> and <meta name="description"> in the HTML.
#   The HTML must carry robots + canonical for https://wlj.me/reading/<slug>/ and a link back to /reading/.
#
# Gates (no way around them from the command line):
#   posts   must pass luca-writing:  python3 ~/Github/luca-writing/scripts/lint_ai_flavor.py input.md
#   reading must pass luca-html:     python3 ~/Github/luca-html/scripts/check_html.py index.html
#   (check_html.py also runs the luca-writing lint over the page's visible prose)

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_URL="https://wlj.me"
WRITING_LINT="$HOME/Github/luca-writing/scripts/lint_ai_flavor.py"
HTML_CHECK="$HOME/Github/luca-html/scripts/check_html.py"
LINT_MARKER="<!-- lint-disable-line -->"

die() { echo "$*" >&2; exit 1; }

# Run a skill checker; its own output explains the hits. Exit non-zero = do not publish.
run_gate() {
  local label="$1" script="$2" file="$3" hint="${4:-}"
  [ -f "$script" ] || die "缺少 $label 检查器: $script（先安装对应 skill 仓库）"
  echo "== $label 检查: $(basename "$file")"
  python3 "$script" "$file" || die "$label 检查没过，先改稿再发布。$hint"
}

now_iso() {
  date +%Y-%m-%dT%H:%M:%S%z | sed 's/\([0-9][0-9]\)$/:\1/'
}

# Push to origin's default branch so this also works from worktree branches
# that have no upstream configured.
git_push_default() {
  local default_branch
  default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo main)
  git push origin "HEAD:$default_branch"
}

# Insert a bullet under today's "## yyyy-mm-dd" heading in CHANGELOG.md,
# creating the heading right after "# Changelog" when it is missing.
changelog_add() {
  local line="$1" today file
  today=$(date +%Y-%m-%d)
  file="$REPO_DIR/CHANGELOG.md"
  [ -f "$file" ] || die "找不到 CHANGELOG.md"
  if grep -q "^## $today\$" "$file"; then
    awk -v today="$today" -v line="$line" '
      { print }
      !done && $0 == "## " today { getline nxt; if (nxt != "") { print line; print nxt } else { print ""; print line }; done=1 }
    ' "$file" > "$file.tmp"
  else
    awk -v today="$today" -v line="$line" '
      { print }
      !done && /^# Changelog$/ { print ""; print "## " today; print ""; print line; done=1 }
    ' "$file" > "$file.tmp"
  fi
  mv "$file.tmp" "$file"
}

# ---------------------------------------------------------------- posts

publish_post() {
  local input="${1:-}" tags="${2:-}" mode="${3:-create}"
  [ -n "$input" ] || die "用法: ./publish.sh input.md [tag1,tag2,...]"
  [ -f "$input" ] || die "文件不存在: $input"

  local title slug date lastmod target tag_line tag_json body
  title=$(grep -m1 '^# ' "$input" | sed 's/^# //')
  [ -n "$title" ] || die "找不到 # 标题"

  slug=$(basename "$input" .md)
  date=$(now_iso)
  lastmod="$date"
  target="$REPO_DIR/content/posts/${slug}.md"
  case "$mode" in
    create) [ ! -f "$target" ] || die "文件已存在: $target" ;;
    update)
      [ -f "$target" ] || die "要更新的文章不存在: $target"
      date=$(sed -n 's/^date: //p' "$target" | head -1)
      [ -n "$date" ] || die "要更新的文章没有 date: $target"
      ;;
    *) die "未知文章发布模式: $mode" ;;
  esac

  run_gate "luca-writing" "$WRITING_LINT" "$input" "确认是误报的行，在行尾加 $LINT_MARKER"

  if [ -n "$tags" ]; then
    tag_json=$(echo "$tags" | tr ',' '\n' | sed 's/.*/"&"/' | paste -sd',' - | sed 's/^/[/;s/$/]/')
    tag_line="tags: $tag_json"
  else
    tag_line=""
  fi

  # Body: skip the first "# title" line and the blank line right after it.
  # Lint-disable markers are for the checker only; keep them out of the published post.
  body=$(awk 'NR==1 && /^# /{found=1; next} found && NR==2 && /^$/{next} {found=0} !found || NR>2{print}' "$input" \
    | sed -e "s/ *$LINT_MARKER//g")

  {
    echo "---"
    echo "title: \"$title\""
    echo "date: $date"
    echo "lastmod: $lastmod"
    echo "author: \"Luca\""
    [ -n "$tag_line" ] && echo "$tag_line"
    echo "draft: false"
    echo "slug: \"$slug\""
    echo "---"
    echo ""
    echo "$body"
  } > "$target"

  cd "$REPO_DIR"
  git add "$target"
  if [ "$mode" = "update" ]; then
    git commit -m "Update post: $title"
  else
    git commit -m "Add post: $title"
  fi
  git_push_default
  echo "已发布: $slug"
}

# ---------------------------------------------------------------- reading

html_unescape() {
  sed -e 's/&amp;/\&/g' -e 's/&lt;/</g' -e 's/&gt;/>/g' -e 's/&quot;/"/g' -e "s/&#39;/'/g" -e "s/&#x27;/'/g"
}

# Escape a value for a TOML basic string.
toml_escape() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'
}

# Read the content="" attribute of a <meta name="..."> or <meta property="..."> tag.
html_meta() {
  local file="$1" name="$2"
  grep -o -i "<meta[^>]*\(name\|property\)=\"$name\"[^>]*>" "$file" | head -1 \
    | sed -n 's/.*content="\([^"]*\)".*/\1/p' | html_unescape
}

publish_reading() {
  local input="" slug="" category="" author="" year="" subtitle="" original_url="" post_slug="" changelog_line="" noindex=0 update=0 dry_run=0

  while [ $# -gt 0 ]; do
    case "$1" in
      --slug) slug="$2"; shift 2 ;;
      --category) category="$2"; shift 2 ;;
      --author) author="$2"; shift 2 ;;
      --year) year="$2"; shift 2 ;;
      --subtitle) subtitle="$2"; shift 2 ;;
      --original-url) original_url="$2"; shift 2 ;;
      --post-slug) post_slug="$2"; shift 2 ;;
      --changelog) changelog_line="$2"; shift 2 ;;
      --noindex) noindex=1; shift ;;
      --update) update=1; shift ;;
      --dry-run) dry_run=1; shift ;;
      --*) die "未知参数: $1" ;;
      *) [ -z "$input" ] || die "多余的参数: $1"; input="$1"; shift ;;
    esac
  done

  [ -n "$input" ] || die "用法: ./publish.sh reading <dir-or-index.html> --category <book|report|documentary|misc> --author <name> [options]"

  # Resolve the source directory and its index.html.
  local src_dir src_html
  if [ -d "$input" ]; then
    src_dir="${input%/}"
    src_html="$src_dir/index.html"
  elif [ -f "$input" ]; then
    src_html="$input"
    src_dir="$(dirname "$input")"
    [ "$(basename "$input")" = "index.html" ] || die "HTML 文件必须命名为 index.html: $input"
  else
    die "文件或目录不存在: $input"
  fi
  [ -f "$src_html" ] || die "找不到 $src_html"

  [ -n "$slug" ] || slug="$(basename "$(cd "$src_dir" && pwd)")"
  [[ "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "slug 必须是英文 kebab-case（当前: $slug）。目录名就是 slug，或用 --slug 指定"

  # Required and defaulted fields.
  case "$category" in
    book|report|documentary|misc) ;;
    "") die "缺少 --category（book / report / documentary / misc）" ;;
    *) die "category 只能是 book / report / documentary / misc（当前: $category）" ;;
  esac
  [ -n "$author" ] || die "缺少 --author"
  [ -n "$year" ] || year=$(date +%Y)
  [[ "$year" =~ ^[0-9]{4}$ ]] || die "year 必须是四位年份（当前: $year）"
  if [ -n "$post_slug" ] && [ ! -f "$REPO_DIR/content/posts/$post_slug.md" ]; then
    die "post_slug 对应的文章不存在: content/posts/$post_slug.md"
  fi

  # New targets must be free. Updates must already exist in both locations.
  local target_dir toml reading_url canonical
  target_dir="$REPO_DIR/static/reading/$slug"
  toml="$REPO_DIR/data/reading-materials.toml"
  reading_url="/reading/$slug/"
  canonical="$SITE_URL$reading_url"
  if [ "$update" = 1 ]; then
    [ -d "$target_dir" ] || die "要更新的目录不存在: $target_dir"
    grep -q "^slug = \"$slug\"\$" "$toml" || die "reading-materials.toml 里没有 slug: $slug"
  else
    [ ! -e "$target_dir" ] || die "目录已存在: $target_dir"
    ! grep -q "^slug = \"$slug\"\$" "$toml" || die "reading-materials.toml 里已有 slug: $slug"
  fi

  # Title and description come from the HTML head.
  local title description
  title=$(grep -o -i '<title>[^<]*</title>' "$src_html" | head -1 | sed -e 's/^<[Tt][Ii][Tt][Ll][Ee]>//' -e 's/<\/[Tt][Ii][Tt][Ll][Ee]>$//' | html_unescape)
  [ -n "$title" ] || die "HTML 里找不到 <title>"
  description=$(html_meta "$src_html" "description")
  [ -n "$description" ] || die "HTML 里找不到 <meta name=\"description\">，整理页必须手写 description"

  # SEO checks: robots, canonical, and a way back to /reading/.
  local robots expected_robots found_canonical
  robots=$(html_meta "$src_html" "robots")
  if [ "$noindex" = 1 ]; then expected_robots="noindex,follow"; else expected_robots="index,follow"; fi
  [ "$robots" = "$expected_robots" ] || die "robots 应为 \"$expected_robots\"（当前: \"${robots:-无}\"）。用 --noindex 发布不索引的页面"
  found_canonical=$(grep -o -i '<link[^>]*rel="canonical"[^>]*>' "$src_html" | head -1 | sed -n 's/.*href="\([^"]*\)".*/\1/p')
  [ "$found_canonical" = "$canonical" ] || die "canonical 应为 $canonical（当前: ${found_canonical:-无}）"
  grep -q -E 'href="(https://wlj\.me)?/reading/"' "$src_html" || die "HTML 里没有返回整理的链接（href=\"/reading/\"）"
  ! grep -q -E '<img[^>]*alt=""' "$src_html" || die "HTML 里有空 alt 的图片，整理页图片必须写有意义的 alt"

  # luca-html checker: structure, theme, print, outline, AI byline, plus luca-writing prose lint.
  run_gate "luca-html" "$HTML_CHECK" "$src_html"

  local date
  date=$(now_iso)

  if [ -z "$changelog_line" ]; then
    if [ "$update" = 1 ]; then
      changelog_line="- 更新资料页《${title}》，\`static/reading/$slug/index.html\`。"
    else
      changelog_line="- 新增资料页《${title}》，\`static/reading/$slug/index.html\`。${description}"
    fi
  fi

  local entry
  entry=$(
    echo ""
    echo "[[materials]]"
    echo "slug = \"$slug\""
    echo "title = \"$(toml_escape "$title")\""
    echo "subtitle = \"$(toml_escape "$subtitle")\""
    echo "author = \"$(toml_escape "$author")\""
    echo "category = \"$category\""
    echo "date = \"$date\""
    echo "year = \"$year\""
    echo "description = \"$(toml_escape "$description")\""
    echo "original_url = \"$(toml_escape "$original_url")\""
    echo "reading_url = \"$reading_url\""
    [ -n "$post_slug" ] && echo "post_slug = \"$post_slug\""
    [ "$noindex" = 1 ] && echo "noindex = true"
    true
  )

  echo "slug:        $slug"
  echo "title:       $title"
  echo "category:    $category"
  echo "author:      $author · $year"
  echo "description: $description"
  echo "source:      $src_dir/ -> static/reading/$slug/"
  echo "changelog:   $changelog_line"

  if [ "$dry_run" = 1 ]; then
    echo ""
    if [ "$update" = 1 ]; then
      echo "[dry-run] 将替换现有整理页，保留 data/reading-materials.toml 条目"
    else
      echo "[dry-run] 将追加到 data/reading-materials.toml:"
      echo "$entry"
    fi
    echo ""
    echo "[dry-run] 未写入任何文件"
    return 0
  fi

  mkdir -p "$REPO_DIR/static/reading"
  if [ "$update" = 1 ]; then
    find "$target_dir" -mindepth 1 -maxdepth 1 -delete
    cp -R "$src_dir"/. "$target_dir"/
  else
    cp -R "$src_dir" "$target_dir"
    printf '%s\n' "$entry" >> "$toml"
  fi
  changelog_add "$changelog_line"

  # Local build check when hugo is available: the sitemap must list the new page.
  if command -v hugo >/dev/null 2>&1; then
    local out="/tmp/wlj-check"
    (cd "$REPO_DIR" && hugo --quiet --destination "$out")
    if [ "$noindex" = 1 ]; then
      ! grep -q "<loc>$canonical</loc>" "$out/sitemap.xml" || die "noindex 页面出现在 sitemap 里，检查 layouts/sitemap.xml"
    else
      grep -q "<loc>$canonical</loc>" "$out/sitemap.xml" || die "sitemap 里没有 $canonical，检查 data/reading-materials.toml"
    fi
    [ -f "$out/reading/$slug/index.html" ] || die "构建产物里没有 reading/$slug/index.html"
  else
    echo "提示: 本机没有 hugo，跳过本地构建检查" >&2
  fi

  cd "$REPO_DIR"
  git add "static/reading/$slug" data/reading-materials.toml CHANGELOG.md
  if [ "$update" = 1 ]; then
    git commit -m "Update $title in Reading" -m "Replace /reading/$slug/ after the reading-page checks pass."
  else
    git commit -m "Publish $title in Reading" -m "Add /reading/$slug/ and list it in reading-materials.toml."
  fi
  git_push_default
  echo "已发布: $canonical"
}

# ---------------------------------------------------------------- dispatch

case "${1:-}" in
  reading) shift; publish_reading "$@" ;;
  post) shift; publish_post "$@" ;;
  update) shift; publish_post "${1:-}" "${2:-}" update ;;
  -h|--help|"") awk 'NR == 1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "$0"; exit 0 ;;
  *) publish_post "$@" ;;
esac
