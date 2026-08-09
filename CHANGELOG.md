# Changelog

## 2026-08-09

- 新增 `reading` section（`/reading/`，菜单「阅读」）：统一展示 11 份书籍/研究报告的中文阅读辅助材料。
- 每份材料为独立自包含 HTML 页（`static/reading/<slug>/index.html`），内联 CSS/JS，保持原有搜索、筛选、目录、暗色模式等功能。
- 材料页面统一 `noindex,follow`，不进 sitemap；`/reading/` 索引页可索引。
- 7 份较旧材料补了窄屏悬浮目录按钮（tocbtn + drawer）。
- 所有材料页补了 canonical、description、返回 `/reading/` 链接。
- 配置：`hugo.toml` 新增「阅读」菜单项（weight 13），`showMenuItems` 6→7。
- SEO：`is-indexable.html` 增加 reading section 支持；`data/reading-materials.toml` 集中管理材料元数据。

## 2026-06-08

- 新增 `startupnotes` section（`/startupnotes/`，菜单「创业笔记」）：把「星球创业笔记」（知识星球付费星球 511244584）做成**免费试读**漏斗——每篇只发前半段，结尾挂知识星球入口（邀请卡图 + 群链接）引流付费。
- 切半在导入脚本里完成，仓库内**只存前半段**，付费后半段只留在星球（公开仓库存全文等于泄露，且对 Google 算 cloaking）。
- 新增脚本：`scripts/sync-zsxq-dates.py`（用 zsxq-cli 拉每篇真实 `create_time`，按编号→标题→正文开头→正文中段短语四级匹配，带「一个星球主题最多对一篇笔记」的一对一约束，避免同名/同号笔记串日期；928/942 匹配真实日期，其余按编号插值，回填进源笔记 frontmatter）、`scripts/import-startupnotes.py`（切半 + 生成 slug/frontmatter，写入 `content/startupnotes/`）。
- 模板：`layouts/startupnotes/{single,list}.html`、`layouts/partials/paywall-cta.html`，样式加到 `static/style.css`。
- SEO/GEO：`startupnotes` section 与单页纳入可索引（sitemap 自动跟随）；单页输出 `BlogPosting` + `BreadcrumbList`；`llms.txt` 增加创业笔记索引区块；`llms-full.txt` 保持 posts-only。页面内容全部免费可读、不隐藏，故仍标 `isAccessibleForFree: true`，无 cloaking 风险。
- 配置：`hugo.toml` 增加「创业笔记」菜单项、设 `mainSections = ["posts"]`（首页/RSS 只列文章，新 section 用真实回溯日期不刷屏首页）、`showMenuItems` 5→6。

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
