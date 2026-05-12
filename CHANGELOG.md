# Changelog

## 2026-05-12

- `publish.sh`: 修复在 git worktree 临时分支上 `git push` 报 upstream 不匹配的问题。改为推送到 `origin` 的默认分支（`git push origin HEAD:<default>`），不再依赖当前分支的 upstream 设置。

## 2026-05-07

- 站内搜索（Pagefind）尝试后取消：方案完整推过三次（`/pagefind/`、`/search-index/`、`/find/` 三种路径），GitHub Pages origin 直连均 200，但通过 wlj.me 走 Cloudflare 时被改写为 404（伪造 404 body 是站点 Hugo 404.html，cf-cache-status: BYPASS）。判断 wlj.me 实际由 Cloudflare 服务（与 robots.txt 被 CF 改写的现象一致），新建路径不在 CF 服务的内容里。后续如要做搜索须先在 Cloudflare 后台确认部署链路。
- 归档页 `/archives/` 不再新增「按主题浏览」区——本质就是从 `/tags/` 选 8 个 tag 加快捷入口，跟 `/tags/` 没区别，纯装饰。

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
