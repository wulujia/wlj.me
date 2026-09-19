# wlj.me

Hugo 博客，GitHub Pages 托管，Terminal 主题。

## 写文章前必读（强制）

下笔前必须先读 `~/Dropbox/context/core/WRITING.md`，按里面的规则写。特别是：

- 只写用户交代过的事实。没发生的过程别编，没说过的感受别加
- 不做价值评估。用户没评的好坏、意义、聪明、适合谁，一律不写
- 不写"为什么这个方案聪明 / 本质上是 / 核心想法"这类提炼升华
- 不加对比（Remotion vs Slidev、和传统剪辑比）除非用户说过
- 不补充实现细节（缓存策略、具体选型建议）除非用户说过

写完自检一遍：每一段有没有用户没给的信息？有就删。

## 禁止直接写入 content 目录（强制）

不要用 Write 或 Edit 在 content/posts/ 或 content/notes/ 下创建文件，也不要手写 frontmatter。日期、frontmatter 由 publish.sh 自动生成，手动填写必然出错。

典型事故：手填 `date` 时间比 build 时间晚（比如 build 在 07:43，date 写成 10:30），Hugo 默认不发布未来时间的文章，文章不会出现在网站上。这种问题排查起来很费时间。

唯一允许的人为路径：通过 publish.sh，按下面流程走。

## 发布文章（posts）

必须通过 publish.sh 发布，流程：

1. 在 /tmp/ 下创建临时 md 文件，文件名为英文 kebab-case（这就是 slug）
2. 文件内容：第一行 `# 标题`，空一行，正文。不写 frontmatter
3. 运行 `./publish.sh /tmp/slug-name.md tag1,tag2`

更新已发布文章时，用同一份临时 Markdown 和 `./publish.sh update /tmp/slug-name.md tag1,tag2`。脚本会保留文章日期并更新 `lastmod`。

publish.sh 自动处理：先跑 luca-writing 的检查器（`~/Github/luca-writing/scripts/lint_ai_flavor.py`），有 warning 就不发；创建文章时生成日期和 frontmatter，更新文章时刷新 `lastmod`；最后 git commit、git push。

规则：
- slug 必须是英文 kebab-case，中文 slug 经 URL encode 后会 404
- tags 必须用英文，优先复用现有标签
- 检查器没过就改稿，不要绕过脚本手动发布。确认是误报的行，在行尾加 `<!-- lint-disable-line -->`，发布时脚本会把这个标记删掉

## 发布整理页（reading）

整理页是 `static/reading/<slug>/index.html` 下的自包含 HTML，不是 Hugo 页面。必须通过 publish.sh 发布，不要手动复制目录、手动改 `data/reading-materials.toml` 或手写 CHANGELOG 条目：

1. 在 /tmp/ 下建目录，目录名为英文 kebab-case（这就是 slug），里面放 `index.html`（图片、EPUB 等附件一起放在目录里）
2. HTML 的 head 必须有：`<title>`、手写的 `<meta name="description">`、`<meta name="robots" content="index,follow">`、`<link rel="canonical" href="https://wlj.me/reading/<slug>/">`；正文要有返回整理的链接 `href="/reading/"`；图片不能空 alt
3. 运行：

```bash
./publish.sh reading /tmp/slug-name --category misc --author "作者" [--year 2026] [--subtitle "副标题"] [--original-url URL] [--post-slug 相关文章slug] [--changelog "自定义日志行"]
```

publish.sh 自动处理：校验上面的 head 要求、跑 luca-html 的检查器（`~/Github/luca-html/scripts/check_html.py`，它同时会对页面正文跑 luca-writing 的检查，0 error 0 warning 才放行）、把目录复制到 `static/reading/<slug>/`、在 `data/reading-materials.toml` 追加条目（date 取当前时间，title / description 从 HTML 读）、在 CHANGELOG.md 当天标题下加一行、本机有 hugo 时构建并检查 sitemap、git commit、git push。

规则：
- category 只能是 book / report / documentary / misc
- 不索引的页面加 `--noindex`，HTML 里 robots 要写 `noindex,follow`，脚本会把它排除出 sitemap
- 先跑 `--dry-run` 看校验结果和将写入的条目，再正式发布
- 页面按 luca-html skill 从模板起稿，正文按 luca-writing 写。检查器没过就改页面，不要手动复制目录绕过脚本

## 笔记（notes）

notes 通过 social-poster bot 的 wlj 平台发布，不在 Claude Code 的职责范围内。

## SEO / GEO 维护规则（强制）

这些文件是 SEO / GEO 基础设施，改动前必须先读：

- `hugo.toml`
- `layouts/partials/head.html`
- `layouts/partials/seo/*`
- `layouts/sitemap.xml`
- `layouts/robots.txt`
- `layouts/index.LLMS.txt`
- `layouts/index.LLMSFULL.txt`

站点索引策略：

- 可索引：首页、`/posts/`、文章页、`/startupnotes/` 及其文章页、`/about/`、`/archives/`、`/reading/` 索引页、整理页（`static/reading/<slug>/`，页面内硬编码 `index,follow` + canonical）
- 默认 noindex：`/notes/`、note 单页、tags、categories、分页页
- sitemap 只放可索引页面，不放 notes、tags、categories、分页页；整理页是 static 文件不是 Hugo 页面，由 `layouts/sitemap.xml` 从 `data/reading-materials.toml` 读取补进 sitemap（条目 `noindex = true` 的不放）

GEO 规则：

- `llms.txt` 和 `llms-full.txt` 由 Hugo 自动生成，不要手写静态文件
- `robots.txt` 必须允许 `GPTBot`、`ClaudeBot`、`anthropic-ai`、`PerplexityBot`、`Google-Extended`、`Bytespider`、`CCBot`
- 文章页必须保留 JSON-LD：`BlogPosting`、作者 `Person`、`BreadcrumbList`
- 关于页是作者权威页，外部 profile 和作者简介要保持准确
- 重要文章建议手写 `description`，不要只依赖自动摘要
- 图片必须有有意义的 alt，不要新增 `![](...)`

部署注意：

- 线上 `robots.txt` 可能被 Cloudflare Managed Content 覆盖。仓库内模板正确不等于线上生效；部署后要 `curl https://wlj.me/robots.txt` 验证。
- Cloudflare 如继续输出 Managed Content 并 block LLM crawler，需要在 Cloudflare 侧关闭或调整。

## 变更记录（强制）

任何影响构建、SEO/GEO、发布流程、模板、索引策略的改动，都要更新 `CHANGELOG.md`。
