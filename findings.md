# wlj.me SEO / GEO 发现

日期：2026-05-02

## 已确认现状

- Hugo 静态站，全站主要内容在原始 HTML 里，SSR / 预渲染天然合格。
- 线上 `robots.txt` 由 Cloudflare Managed Content 输出，当前阻止 `GPTBot`、`ClaudeBot`、`Google-Extended`、`Bytespider`、`CCBot` 等 LLM 爬虫。
- 线上没有 `/llms.txt`，访问返回 404 页面。
- sitemap 存在，但把大量低价值页面纳入索引面：notes、tags、categories 都在 sitemap 中。
- 构建产物约 3345 个 `index.html`，没有任何 `application/ld+json`。
- `content/posts` 约 1316 篇，`description` / `author` / `lastmod` 基本缺失。
- `content/notes` 约 843 条，多数非常短，适合做流式笔记，不适合单页索引。
- 页面已有 canonical、OG、Twitter card、RSS、viewport、HTTPS。

## 主要风险

- Cloudflare Managed Content 可能覆盖仓库中的 `robots.txt`，需要部署后在 Cloudflare 侧确认。
- 一些老文章含原始 HTML，Hugo 当前会省略部分 raw HTML，需要单独治理。
- 旧安全文章里代码块被 Markdown 标题误解析为 H1；已在模板层把正文内部 H1 降级，构建产物多 H1 页面为 0。
- Hugo 生成的 `llms.txt` / `llms-full.txt` 中仍可能出现少量 `&#34;` / `&#43;` 这类实体，主要来自 `.Plain` / `.Summary` 的渲染链路；文件可读且 URL、标题、正文仍可被 LLM 抓取。
