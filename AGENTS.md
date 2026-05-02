# wlj.me Agent 工作规范

本文件给 Codex、Claude Code 和其他 agent 使用。优先级：用户当前指令 > 本文件 > `CLAUDE.md` > README。

## 基本规则

- 用中文回复 Luca。
- 不要直接在 `content/posts/` 或 `content/notes/` 手写新内容；发布文章必须走 `publish.sh`，notes 由 social-poster bot 负责。
- 代码注释和 commit message 用英文；文档、changelog、站点规范用中文。
- 任何影响站点行为的改动，都要更新 `CHANGELOG.md`。

## SEO / GEO 规则

- `hugo.toml`、`layouts/partials/head.html`、`layouts/partials/seo/*`、`layouts/sitemap.xml`、`layouts/robots.txt`、`layouts/index.LLMS.txt`、`layouts/index.LLMSFULL.txt` 是 SEO / GEO 核心文件，改动前先读。
- 首页、`/posts/`、文章页、`/about/`、`/archives/` 是默认可索引页面。
- `/notes/`、note 单页、tags、categories、分页页默认 `noindex,follow`，不要轻易改成 index。
- sitemap 只放可索引页面，不放 notes、tags、categories、分页页、redirect、404。
- `llms.txt` 和 `llms-full.txt` 由 Hugo 自动生成，不要手写静态版本。
- 文章页必须保留 canonical、robots、OG、Twitter Card、JSON-LD、作者、发布时间、更新时间。
- 新增结构化数据时优先 JSON-LD，不用 microdata。

## 内容质量规则

- 新文章要有明确标题、英文 kebab-case slug、英文 tags。
- 重要文章建议手写 `description`，尤其是产品、技术、创业、AI、SEO/GEO 相关内容。
- 图片必须写有意义的 alt；不要新增空 alt 的 Markdown 图片。
- GEO 友好文章要有清晰判断、时间戳、来源链接、局限或适用边界。
- 不要为了 SEO 批量生成低信息密度页面。

## 发布后检查

- 本地必须跑 `hugo --destination /tmp/wlj-check`。
- 检查 `/tmp/wlj-check/robots.txt` 是否允许主要 LLM 爬虫。
- 检查 `/tmp/wlj-check/llms.txt` 和 `/tmp/wlj-check/llms-full.txt` 是否生成。
- 检查 `/tmp/wlj-check/sitemap.xml` 是否排除了 notes、tags、categories。
- 检查任意文章页是否包含 `application/ld+json` 和 `BlogPosting`。
- 部署后如果线上 `robots.txt` 仍是 Cloudflare Managed Content，需要到 Cloudflare 关闭或调整覆盖规则。
