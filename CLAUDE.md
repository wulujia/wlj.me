# wlj.me

Hugo 博客，Cloudflare Pages 托管（推送 main 后自动构建），Terminal 主题。

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

## 发布研究页（research）

先读 `docs/spec.md`。新页面从 `templates/research/index.html` 起稿。
复制模板后，替换标题、摘要、日期、canonical 和正文。
保留统一样式、站点页眉和页脚、返回链接和目录结构。
`publish.sh research` 发布前自动同步共用样式、脚本、页眉和页脚。改了 `hugo.toml` 的菜单或站名后，运行 `python3 scripts/research_style.py static/research --sync` 更新全部研究页。
目录按顺序列出全部 `h2`、`h3`，文字必须与标题一致。
每个标题有独立 id。

统一样式和脚本在 `templates/research/reading.css`、`reading.js`。
禁止逐页修改内嵌副本。更新副本使用：

```bash
python3 scripts/research_style.py /tmp/slug-name --sync --url-prefix https://wulujia.com/research/slug-name/
```

组件样式放在共用样式之前。组件不得另设正文主题和字体。
专题目录中的 HTML 子页也必须使用模板。

研究页是 `static/research/<slug>/index.html` 下的自包含 HTML，不是 Hugo 页面。必须通过 publish.sh 发布，不要手动复制目录、手动改 `data/research-materials.toml` 或手写 CHANGELOG 条目：

1. 在 /tmp/ 下建目录，目录名为英文 kebab-case（这就是 slug），里面放 `index.html`（图片、EPUB 等附件一起放在目录里）
2. HTML 的 head 必须有：`<title>`、手写的 `<meta name="description">`、`<meta name="robots" content="index,follow">`、`<link rel="canonical" href="https://wulujia.com/research/<slug>/">`；正文要有返回研究的链接 `href="/research/"`；图片不能空 alt
3. 运行：

```bash
./publish.sh research /tmp/slug-name --category misc --author "作者" --tags AI,Tools [--year 2026] [--subtitle "副标题"] [--original-url URL] [--post-slug 相关文章slug] [--changelog "自定义日志行"]
```

publish.sh 自动处理：校验上面的 head 要求、跑 luca-html 的检查器（`~/Github/luca-html/scripts/check_html.py`，它同时会对页面正文跑 luca-writing 的检查，0 error 0 warning 才放行）、把目录复制到 `static/research/<slug>/`、在 `data/research-materials.toml` 追加条目（date 取当前时间，title / description 从 HTML 读）、在 CHANGELOG.md 当天标题下加一行、本机有 hugo 时构建并检查 sitemap、git commit、git push。

规则：
- category 只能是 book / report / documentary / misc
- 不索引的页面加 `--noindex`，HTML 里 robots 要写 `noindex,follow`，脚本会把它排除出 sitemap
- 先跑 `--dry-run` 看校验结果和将写入的条目，再正式发布
- 更新页面加 `--update`。只写本地加 `--local`，脚本仍检查和构建，但不提交、不推送
- 发布前递归检查全部 HTML 子页。任一子页失败时，不写入目标目录
- 推送后 GitHub Actions 运行研究页测试、`python3 scripts/research_style.py static/research` 和一次 Hugo 构建，失败时提交显示红叉。这个工作流不部署；要让检查拦住上线，Cloudflare Pages 的构建命令须先跑同样的检查
- 引文或专业术语确属误报时，逐行核对并记录到 `docs/20261102-reading-lint-reviews.md`。不得整页豁免；修改标记行时必须重新核对。
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

- 可索引：首页、`/posts/`、文章页、`/startupnotes/` 及其文章页、`/about/`、`/archives/`、`/research/` 索引页、研究页（`static/research/<slug>/`，页面内硬编码 `index,follow` + canonical）
- 默认 noindex：`/notes/`、note 单页、tags、categories、分页页
- sitemap 只放可索引页面，不放 notes、tags、categories、分页页；研究页是 static 文件不是 Hugo 页面，由 `layouts/sitemap.xml` 从 `data/research-materials.toml` 读取补进 sitemap（条目 `noindex = true` 的不放）

GEO 规则：

- `llms.txt` 和 `llms-full.txt` 由 Hugo 自动生成，不要手写静态文件
- `robots.txt` 必须允许 `GPTBot`、`ClaudeBot`、`anthropic-ai`、`PerplexityBot`、`Google-Extended`、`Bytespider`、`CCBot`
- 文章页必须保留 JSON-LD：`BlogPosting`、作者 `Person`、`BreadcrumbList`
- 关于页是作者权威页，外部 profile 和作者简介要保持准确
- 重要文章建议手写 `description`，不要只依赖自动摘要
- 图片必须有有意义的 alt，不要新增 `![](...)`

部署注意：

- 线上 `robots.txt` 可能被 Cloudflare Managed Content 覆盖。仓库内模板正确不等于线上生效；部署后要 `curl https://wulujia.com/robots.txt` 验证。
- Cloudflare 如继续输出 Managed Content 并 block LLM crawler，需要在 Cloudflare 侧关闭或调整。

## 变更记录（强制）

任何影响构建、SEO/GEO、发布流程、模板、索引策略的改动，都要更新 `CHANGELOG.md`。

### 研究页主题标签

`category` 保留书、报告、纪录片、杂项四种资料类型。
主题使用文章已有的英文标签，每页 1–5 个。
新建时必须传入 `--tags`，多个标签以逗号分隔。
更新时省略该参数会保留已有标签。
检查器统一大小写，并拒绝文章中不存在的标签。

仅修改已有资料的标签时，准备 JSON 清单：

```json
{"example-slug": ["AI", "Security"]}
```

先检查，再更新本地：

```bash
./publish.sh research-tags /tmp/research-tags.json --local --dry-run
./publish.sh research-tags /tmp/research-tags.json --local
```

此命令只修改标签并生成变更记录。
命令不修改 HTML，不提交、不推送。
列表支持主题筛选，例如 `/research/#Security`。
旧类型链接（如 `/research/#report/2`）继续可用。
