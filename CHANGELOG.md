# Changelog

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
