# Changelog

## 2026-05-07

- 新增站内搜索 `/search/`：基于 Pagefind 静态索引，菜单加入「搜索」入口；GitHub Actions 在 Hugo build 之后执行 `npx pagefind --site public` 生成索引到 `public/pagefind/`。
- 文章模板 `layouts/_default/single.html` 在 `posts` section 的 `<article>` 上加 `data-pagefind-body`，限定 Pagefind 仅索引 posts 正文；搜索页 `layouts/search/single.html` 加 `data-pagefind-ignore` 排除自身。
- 搜索 UI 颜色对齐 Solarized：`static/style.css` 末尾新增 Pagefind UI 的 CSS 变量（暗/亮模式分别配色），融入 terminal 主题。
- 归档页 `/archives/` 顶部新增「按主题浏览」区，从 `hugo.toml` 的 `params.archiveTopics`（默认 Startup / Tech / AI / Reading / Security / Product / Tools / Photography）读取主题列表，按 tag 数量展示入口。
- 搜索页 `content/search.md` 设置 `noindex: true` 且 `is-indexable.html` 默认排除非 posts/about/archives 页面，确保搜索页不进 sitemap、不被收录。

## 2026-05-02

- 关于页新增 `SGAI` 外链，指向 `https://sgai.md`。
- 完整补齐 SEO / GEO 基础设施：新增项目级 `head` partial、robots 生成模板、精简 sitemap、`llms.txt`、`llms-full.txt`。
- 新增 Schema.org JSON-LD：全站输出 `Person`、`WebSite`，文章页输出 `BlogPosting` 和 `BreadcrumbList`，关于页输出 `AboutPage`。
- 收敛索引面：首页、文章、文章列表、关于页、归档页保留索引；notes、tags、categories、分页页默认 `noindex,follow`，并从 sitemap 排除。
- 补作者和更新时间信号：文章页显示作者链接；`publish.sh` 新文章自动写入 `author` 和 `lastmod`。
- 补页面结构：首页、列表页、归档页、notes 单页增加 H1；tag 页文章标题从 H1 调整为 H2。
- 增强 Hugo 配置：开启 `enableRobotsTXT`，增加站点描述、作者资料、默认图片、关键词、`showLastUpdated`，允许可信旧内容中的 raw HTML 渲染。
- 更新未来协作规范：新增 `AGENTS.md`，扩展 `CLAUDE.md` 的 SEO / GEO 规则。

注意：线上 `robots.txt` 当前被 Cloudflare Managed Content 覆盖并阻止多个 LLM 爬虫。仓库已生成正确版本，部署后仍需在 Cloudflare 侧关闭或调整托管 robots/content signal 设置。
