# Changelog

## 2026-09-12

- 新增资料页《Clio：保护隐私的真实世界 AI 使用观察》，`static/reading/clio-privacy-preserving-insights-2024-12/index.html`。arXiv:2412.13678v1 论文中文译本，15 张原图随文，提供双语 EPUB 下载。`index,follow` + canonical，顶部返回整理、arXiv 原文。`data/reading-materials.toml` 新增 report 条目。
- 为 Anthropic 威胁情报报告补充官方原文链接：报告页顶部显示「原文（Anthropic）」，Reading 列表显示「原文」。

## 2026-09-11

- 重做 Anthropic 报告 HTML 的目录与标题层级：拆分混入标题的正文，补齐各章真实小节，移除 GTG 正文和表格内容的错误目录项；修复锚点跳转及当前位置高亮。逐章校验文字及 61 张图片未变，保留 noindex 与双语下载。
- 收紧 `/reading/` 页面标题「整理」和说明文字之间的垂直间距。
- 新增资料页《检测与打击 AI 滥用：2026 年 9 月》，`static/reading/detecting-and-countering-ai-misuse-2026-09/index.html`。HTML 只保留中文译文，用 Kami 重排成长文阅读版，保留原报告 61 张图片，加入桌面固定大纲和移动端横向大纲，并提供双语 EPUB、PDF 下载。页面设为 `noindex,follow` 并从 sitemap 排除。`data/reading-materials.toml` 新增 report 条目；资料列表说明同步纳入中文翻译。

## 2026-09-09

- 拉取最新源仓库后，创业笔记从 962 更新到 965，新增《优惠券》《本职工作与向前一步》《牌桌现在的意义》三篇免费试读，沿用原有段落截半规则，后半篇不写入仓库。同步导入清单，日期暂用源文件首次 Git 提交时间，日期索引已标记来源，尚未核对星球实际发布日期。

- 新增日志《VPS 从 NixOS 迁出后，我会选 Debian》，`content/posts/20260909-nixos-server-debian.md`。记录从 NixOS 迁出虚拟主机服务时对 Debian、Ubuntu 和 Arch 的取舍，以及用新机、Docker Compose 和异机备份迁移的做法。
- 创业笔记从 957 更新到 962，新增《AI First》《Reader Feishu Data Bot 的想法》《速度与对齐上下文》《霰弹》《激进》五篇免费试读，沿用原有按段落截取约前半篇的规则，后半篇不写入仓库。同步导入清单；知识星球登录凭证暂不可读，五篇日期采用源文件首次 Git 提交时间，并在日期索引中标记 `date_source: source_git_first_commit`，待可查询时核对真实发布日期。

- 新增日志《AI 写代码快了，产品迭代还慢，怎么办？》，说明六阶段产出、执行方法与效果指标，补充 CLAUDE.md、REVIEW.md 和 eval。附原课瓶颈图及标明交接产出的循环图，保留课程来源链接。

## 2026-09-08

- 新增日志《TeamAI：给 AI 编程工具加一层团队协作》，`content/posts/20260908-teamai-cli.md`。整理腾讯开源 TeamAI 的定位、三层能力、Git/MR 同步方式、安装命令、适用范围、成熟度快照、MCP/Hooks/隐私等注意事项，以及官方资料链接和未验证部分。
- 新增資料頁《台北國際照顧博覽會：養老產品分類與分析》，`static/reading/caresexpo-2026-taxonomy/index.html`，自包含 HTML：研究結論 / 官方分類架構 / 展商 Top 20 / 攤位分布 / 十一個類別的產品卡 / 資料與方法說明，左側固定大綱，`index,follow` + canonical，頂部返回連結。發布前把 464 張產品卡的 `h4` 改為 `p.card-title`（卡片標題不是章節標題，原本 h2 直接跳 h4），並補 `:root[data-theme="dark"]` 讓手動切換主題生效。`data/reading-materials.toml` 新增 report 條目。
- 新增资料页《Lenny 播客半年 AI 实践调研》，`static/reading/lenny-podcast-ai-2026-09/index.html`，自包含 HTML：样本 / 提效 / 组织 / AI 进入流程 / 用 AI 挣钱 / 产品运营增长 / 分歧地图 / 30 期一览 / 方法与来源，284 条 YouTube 时间戳直链，左侧固定大纲，`index,follow` + canonical，顶部返回链接。`data/reading-materials.toml` 新增 report 条目。

## 2026-09-07

- 中国经济资料页目录：不带编号的二级条目（访谈时怎么问、评估部分引用）之前被竖排成一字一行，原因是子链接用了两列 grid，没有编号的文字落进 14px 的编号列。改为编号用固定宽度 inline-block，grid 去掉。
- 资料页《中国经济，好还是差》新增三个月度跟踪指标（第 7 到 9 项）：PPI 同比（2015 年 1 月起，统计局，东方财富整理历史序列）、M1 与 M2 增速差（2024 年 1 月起，人民银行；2024 年 M1 用 2025 年 1 月报告附的可比口径回溯值）、工业企业产成品存货 / 应收账款 / 营业收入同比（2024 年 2 月起，统计局月度工业企业利润发布，含周转天数和回收期）。总览板、目录、来源列表同步加；正文里“六个指标”改“九个”。页内把“数据说了什么 / 判断标准”和图表列标题从 h3 降为 div，只保留两个真正的三级标题并入目录，检查器 0 error 0 warning。
- 资料页《中国经济，好还是差》（`static/reading/china-economy-2026-09/index.html`）加左侧固定大纲（桌面 sticky，900px 以下折成 details），顶部六个 h2 加 id，六个跟踪指标作为二级条目；补全打印样式（强制亮色、隐藏导航、图表和表格不跨页）。正文按写作规则过一遍：去掉“两个提醒。一是……二是”“这是真实力，不是刺激出来的”“现在是跌幅收窄，不是止跌”等对比句和结构报幕，改为直陈。
- 新增 `static/_redirects`：旧域名改名过的 67 篇文章，从 `/posts/<旧 slug>/` 301 到新 slug（Cloudflare Pages 读取此文件；配合 wulujia.com 上 `blog.wulujia.com/*` → `wlj.me/posts/$1/` 的通配跳转，不再需要 Bulk Redirects）。
- 索引策略：上午给 697 篇旧转帖 / 短文加了 `noindex: true`（2010 年前且不足 1500 字，或不足 150 字），Luca 决定全部撤回，同日恢复为全部可索引，`scripts/seo-noindex.py` 一并删除。原因：站点拿不到排名的主因是没有外链，不是页面数量；这批页面是否收录对结果影响很小，先不动。`12q1y-2025` 与 `twelve-questions-end-of-2025` 内容重复的问题保留待处理。
- 40 篇 2024 年以来正文超 2000 字的文章手写 `description`，不再用自动摘要。
- 新增 `/featured/` 精选页（`content/featured.md` + `layouts/_default/featured.html`，数据在 `data/featured.toml`，四组），加入菜单，`showMenuItems` 7 → 8；首页顶部新增 10 篇精选链接块。`is-indexable` 把 `/featured/` 列为可索引，sitemap 自动带上。
- 文章页末尾新增「相关文章」：Hugo Related 按标签取 5 篇，排除 noindex 页。
- 新增 `scripts/blog-wulujia-redirects.csv`：旧域名 blog.wulujia.com 的文章 URL 到 wlj.me 的 301 映射（Wayback 抓到的路径 + 首次迁移的 53 篇 + 改名记录），格式对应 Cloudflare Bulk Redirects。旧域名目前返回 525，需要在 Cloudflare 上传这份列表或加通配规则。

## 2026-09-06

- 新增资料页《OpenClaw 开源运营笔记》，`static/reading/openclaw-open-source-ops/index.html`，自包含 HTML（规模 / 小项目能搬走什么 / 对贡献者的具体要求 / Barnacle 规则引擎 / ClawSweeper AI 评审 / 分层 AGENTS.md / 安全 / 发布 / 治理 / 社区 / CI / 标签 / 代价 / 方法与来源），左侧固定大纲，`index,follow` + canonical，顶部返回链接。`data/reading-materials.toml` 新增 report 条目。
- 新增资料页《Omarchy 开源运营笔记》，`static/reading/omarchy-open-source-ops/index.html`，同款规格（规模 / 可借鉴 / omarchy 技能 / 崩溃分诊技能 / 四条更新通道 / 更新安全网 / 贡献者要求 / 插件分流 / 测试 / 设计先行 / 发布 / 合并 / 治理 / 社区 / 欠账 / 方法与来源）。`data/reading-materials.toml` 新增 report 条目。
- 撤回日志《Slax Reader · 项目地图与开发指南》，改为自包含 HTML 资料页 `/reading/slax-reader-project-guide/`；`data/reading-materials.toml` 新增资料索引。旧 `/posts/` URL 改为 noindex 跳转页。
- 整理列表按钮「打开整理」改「打开」，各页顶部「← 返回整理」改「← 返回」。
- `reading` 栏目改名「整理」（URL 保持 `/reading/` 不变）：`content/reading/_index.md` 标题、`hugo.toml` 菜单名、列表页「打开整理」按钮、各整理页顶部「← 返回整理」同步改。

- 新增资料页：《新加坡政府的钱从哪来》，`static/reading/singapore-government-revenue/index.html`。用 2025 财年修订数拆经常收入、NIRC、卖地和储备；`data/reading-materials.toml` 补条目。
- 新增资料页《新加坡经济战略检讨，讲了什么》，`static/reading/singapore-esr-2026/index.html`，自包含 HTML（时间线 / 三个原则 / 八个方向 32 条建议与已落地政策 / 数字速览 / 与 2010、2017 两次检讨的对比 / 对创业者相关条目表 / 委员会名单 / 来源），`index,follow` + canonical，顶部返回资料链接。`data/reading-materials.toml` 新增 report 条目，`original_url` 指向 MTI 的报告 PDF。

## 2026-09-05

- 新增资料页《中国经济，好还是差》，`static/reading/china-economy-2026-09/index.html`，自包含 HTML（冷热两分的评估框架 / 主要指标同比图 / 数据和体感为何对不上 / 四个标准的判断 / 六个月度跟踪指标的逐月图表与数据表 / 来源与方法），`index,follow` + canonical，顶部返回资料链接。`data/reading-materials.toml` 新增 misc 条目。
- `/reading/` 资料页重设计：`layouts/reading/list.html` 从四组分类卡片改为与日志列表同款的时间倒序列表（标题 / 日期 / 作者·年份 / 副标题 / `#分类` 标签 / 简介 / `[打开资料]` `[原文]` `[相关文章]`）。顶部新增分类筛选（全部 / 书 / 研究报告 / 纪录片 / 杂项，带计数），纯前端切换，URL hash（如 `/reading/#book`）可直达某一分类，条目上的 `#分类` 标签也可点选。`data/reading-materials.toml` 每条新增 `date` 字段（收录时间，取自 git 首次提交时间），列表按它排序；新增资料时必须填 `date`。
- 新增资料页《TechCrunch 深度调研》，`static/reading/techcrunch/index.html`，规格同 Crunchbase 页；`data/reading-materials.toml` 新增 report 条目。
- 新增资料页《泉州老城区公寓房价分析》，`static/reading/quanzhou-old-town-housing/index.html`，自包含 HTML（官方成交指数曲线 / 挂牌均价曲线 / 板块均价 / 候选小区 / 六灌路定位 / 租金分析 / 来源），`index,follow` + canonical，顶部返回资料链接。`data/reading-materials.toml` 新增 `misc`（杂项）分类和条目；`layouts/reading/list.html` 新增「杂项」分组（无条目时不渲染）。
- 新增资料页《Product Hunt 深度调研》，`static/reading/product-hunt/index.html`，规格同 Crunchbase 页；`data/reading-materials.toml` 新增 report 条目。
- `posts` 栏目改名「日志」（URL 保持 `/posts/` 不变）：`hugo.toml` 菜单名、`layouts/_default/list.html` 默认标题、`layouts/partials/seo/jsonld.html` 的 section 名同步改；新增 `content/posts/_index.md` 设置栏目标题，页面 h1 和 `<title>` 从「Posts」变为「日志」。
- 新增资料页《Crunchbase 深度调研》，`static/reading/crunchbase/index.html`，自包含 HTML（产品 / 业务 / 财务 / 历程 / 护城河 / 对手 / 风险 / 来源），`index,follow` + canonical，窄屏悬浮目录；`data/reading-materials.toml` 新增 report 条目，随 sitemap 自动收录。

## 2026-08-18

- 创业笔记从 953 更新到 957，新增《Claude Tag 和知识星球》《飞书 aily》《温暖的话》《知识星球里的上下文》四篇免费试读，并同步知识星球真实发布日期与主题索引。

## 2026-08-17

- `reading` 栏目改名「资料」（URL 保持 `/reading/` 不变）：`content/reading/_index.md` 标题、`hugo.toml` 菜单名同步改；`layouts/reading/list.html` 免责句从「原书」改「原作」。
- `layouts/reading/list.html` 新增「纪录片」分组（`category = "documentary"`，无条目时不渲染）。
- 新增材料页：《人生七年》（The Up Series）人物志，`static/reading/the-up-series/index.html`，出身×九部对比总表 + 14 位参与者卡片；`data/reading-materials.toml` 新增条目并关联简介文章（`post_slug`）。
- 索引策略反转：11 个既有材料页 robots meta 从 `noindex,follow` 改为 `index,follow`，新页直接 `index,follow`；`layouts/sitemap.xml` 新增从 `data/reading-materials.toml` 读取材料页 URL 的循环（static 文件不是 Hugo 页面，不走 `is-indexable.html`）。
- 11 个既有材料页返回链接文字「← 返回阅读材料」改「← 返回资料」（href 不变）。
- `CLAUDE.md` 站点索引策略小节同步：可索引清单补 `/startupnotes/`、`/reading/` 和材料页，注明材料页进 sitemap 的机制。

## 2026-08-09

- 创业笔记从 942 更新到 953，补入 945–953，并修正 944 的标题、内容和真实发布日期。
- 刷新知识星球日期索引；导入脚本改用当前 `~/Github/Luca/startupnotes` 源目录，自动剥离「以下内容不发布」私有尾段。
- 修复日期同步 `--dry-run` 写缓存、CSV 行尾及摘要尾部空格问题。
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
