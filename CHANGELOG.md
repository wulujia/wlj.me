# Changelog

## 2026-11-28

- 新增资料页《iPad 与 Apple Pencil Pro 油画入门指南》，`static/research/ipad-oil-painting-guide/index.html`。针对零基础初学者的平板数字油画调研与分步实操指南，对比 iPad、安卓与鸿蒙主流油画软件与原生笔刷，拆解手写笔侧旋设置，并以一枚侧光红苹果完整演示从新建画布到厚涂高光的五步流程。

## 2026-11-24

- 删除 `AGENTS.md`，agent 规则只保留 `CLAUDE.md` 一份。`AGENTS.md` 独有的规则已移入 `CLAUDE.md`：保留 SEO 元信息、结构化数据用 JSON-LD、不批量生成低信息量页面、公开邮箱加 `email_off`、改模板后的本地检查、`research_tags.py check`。“用中文回复”一条不再保留，以全局规则为准。
- `AGENTS.md`、`CLAUDE.md` 标题注明本仓库发布 wulujia.com。`AGENTS.md` 的可索引页面补上 `/startupnotes/` 和 `/research/`，与 `CLAUDE.md` 一致。
- 修复 `publish.sh` 发文章的两个问题。标题含英文双引号时，frontmatter 不合法，整站构建失败；现在转义 `"` 和 `\`。远端有新提交时（另一台电脑或笔记 bot 先推送），推送被拒；现在推送前先 `git pull --rebase --autostash`。新增 `tests/test_post_publish.py`，GitHub Actions 改为运行 `tests/` 下全部测试。
- 正文里指向 wlj.me 的 8 处链接改为 wulujia.com（文章、创业笔记、4 条笔记、1 个研究页、slax-reader 旧跳转页）。wlj.me 以后可能停用，链接不能依赖它的跳转。代码示例和历史文字里的 wlj.me 保留。
- 站内搜索：新增 `/search/`（`content/search/index.md` + `layouts/_default/search.html`，Pagefind UI，按站点配色，noindex），菜单加“搜索”。索引只收文章、笔记、创业笔记和研究页：这些页面的正文容器加 `data-pagefind-body`（`_default/single.html`、`notes/single.html`、`startupnotes/single.html`；研究页由 `research_style.py --sync` 加在 `<main>` 上，模板同步改），列表、标签和首页不进索引。Cloudflare Pages 项目 wlj-me 的构建命令末尾加 `npx -y pagefind@1.6.0 --site public --force-language zh`，在 Hugo 之后生成 `/pagefind/`。`--force-language zh` 必须有：研究页的语言是 zh-CN，不合并时搜索页（zh）搜不到研究页。
- Cloudflare 设置（不在仓库里）：新增 `www.wulujia.com`（A 记录 192.0.2.1，代理）和 Page Rule `www.wulujia.com/*` → `https://wulujia.com/$1`（301）；`blog.wulujia.com/*` 改为直接跳 `https://wulujia.com/posts/$1`；wulujia.com 开启 HSTS（6 个月，不含子域名，不预加载）；wlj.me 新增 Page Rules `wlj.me/reading/*` → `https://wulujia.com/research/$1`、`wlj.me/*` → `https://wulujia.com/$1`，`www.wlj.me/*` 改为直接跳 `https://wulujia.com/$1`，均为 301。
- 图片替代文字：文章和笔记里 277 张 `![]()` 和 19 个没有 alt 的 `<img>` 补上 alt，用所在文章或笔记的标题加“配图 N”。构建产物里 Hugo 页面不再有缺 alt 的图片。notes 机器人（social-poster 1.4.6）以后发布时也这样写，并把长边超过 1600px 的图片缩小。
- 三张 2–3 MB 的笔记照片缩到长边 1600px（0.6–0.8 MB）。旧百度博客等 75 张 `http://` 图片里，只有 1 张在 Wayback 有存档，已换成存档地址；其余 74 张原站和存档都没有，保留原样。
- 仓库根目录整理：2026-05 的 SEO 工作记录 `findings.md`、`progress.md`、`task_plan.md` 移到 `docs/20260502-seo-*.md`；一次性的 `retag.py` 和 `retag_report.csv` 移到 `scripts/`。
- 全站同一设计：文章、笔记等 Hugo 页面改用研究页的配色和字体（`static/style.css`）。正文改无衬线字体、行高 1.8；站名、菜单、日期、页脚、代码保留 Fira Code。文字加深到 4.5:1 以上：亮色正文 `#28383d`、链接 `#17635d`、日期等 `#5b6a6e`；暗色正文 `#d2dbdb`、链接 `#5cc8bf`、日期等 `#93a1a1`。正文图片去掉绿色粗边框，引用只用缩进，不再有上下横线和“>”。主题色 `#2aa198` 只留给站名条、装饰线和边框。
- 删除 5 篇重复文章，每篇 301 到保留的那篇：`love-simple-longterm`→《喜欢，长期，简单》（`love`），`twelve-questions-end-of-2025`→《每年十二问：2025》（`12q1y-2025`，格式更好，精选里也换成它），以及旧博客镜像 `blog-xfocus-2602`、`i170-1824`、`i170-57437`。逐对比过全文（相似度 93.5%–100%，差别只在格式和一个表情图）。
- 删除 6 篇别人写的文章（公众号作者栏是别人）：郭玉珍《Slax Note AI 重写版正式上架》、肥狗《用躺平心态，我居然养成了5个新习惯》、Luge《小日子设计改版中的减法》、Yangzi 访谈《打怪打工之余，不如也来打卡》、丁邱洁《怎么用好律师》、邱岳《如果可以给 25 岁时的自己一句忠告》，以及只被其中一篇用到的配图。作者栏署“知识星球”的 7 篇（产品功能说明、星球推荐）保留。
- 全站检查后的修复：旧文章里 25 处丢了域名的 Wayback 链接（`/web/…`）补上 `https://web.archive.org`；22 处指向 2007 年前后 wulujia.com 旧博客的链接（如 `/Article_54851`，域名切换后成了 404）改为 Wayback 存档，年份取文章年份。构建产物里的站内死链从 43 个降到 0。RSS 只输出最新 30 条（`hugo.toml` 的 `[services.rss] limit = 30`），`index.xml` 从 3.9 MB 降到 28 KB。标签统一为英文：`ai`/`tools`/`writing` 并入 `AI`/`Tools`/`Writing`，`创业`→`Startup`、`翻译`→`Translation`、`产品`/`产品观察`→`Product`、`软件工程`→`Tech`。`scripts/sync-zsxq-dates.py` 的源目录改为 `~/Github/Luca/startupnotes`（原来写死了另一台电脑的路径）。README 的数量和目录结构更新。
- 站名条头像改用更宽的裁切（原图 400×400 区域），整个头部在圆里，四周留出底色，不再撑满。只换 `static/avatar.png`。
- 精选去掉三篇：《Apple Watch 九年数据让我盯上三件事》《GBrain 双机部署实录》《AI 时代，我们为什么还要学习？》，首页精选和 `/featured/` 分组里都去掉。首页精选剩 7 篇，精选共 33 篇。
- 站名条头像移到绿色框外、框的左边，34px 圆形，与框同高；新增 `static/avatar.png`（136×136），裁切让脸居中、眼睛略高于圆心。浏览器标签页图标 `favicon.png` 不变。Hugo 页面改 `layouts/partials/logo.html`，研究页改 `scripts/research_style.py` 和 `reading.css`，95 个研究页已同步。
- 新增资料页《Mac 与 Linux 单机白名单 HIDS 选型》，`static/research/hids-allowlist/index.html`。不依赖管理服务器、能按白名单拦截程序执行的开源主机防护工具，macOS 与 Linux 各有哪些选择，怎么上线。
- 新增资料页《活动平台、会务软件与线下连接行业研究》，`static/research/events-offline-connections/index.html`。活动行、Luma 等活动平台与线下连接公司的业务、融资、收入及网页流量研究。结合 Articuler 案例，评估知识星球的产品机会与试验方案。资料截至 2026 年 10 月 30 日。
- 站名条里加头像：文章、笔记等 Hugo 页面（`layouts/partials/logo.html`，覆盖主题模板）和研究页（`scripts/research_style.py` 生成的页眉，93 个页面已同步）在“Luca's Blog”前显示 24px 圆形头像，图片用 `/favicon.png`，alt 为“Luca 的头像”。主题给所有 img 加了外边距、8px 边框和内边距，头像的样式直接写在 img 上覆盖这些规则，预览环境也能正确显示。
- 精选按日期倒序：首页精选板块和 `/featured/` 每组内都按文章日期从新到旧排，不再按 `data/featured.toml` 里的顺序。
- 按公众号后台“发表记录”（396 条，2020-12 到 2026-11）核对，补入 18 篇 Luca 本人发的文章：《学得慢就不用学了，吗？》《写书的过程》《我为什么喜欢用 Cindy》《学习也得立个项》《半桶水》《科幻》《下一代公司会从哪里诞生？》《五个小时能干什么》《Dario Amodei 与 Sam Altman 的 AI 风险观点》《[翻译]几个人一个月做出 Grok Bot》《给还在看网页的朋友》《几个关于 AI 的问答》《新加坡的 Claude 使用强度全球第一：5.53 是什么意思》《稍后读的 Cli 玩法》《人味和情绪价值》《我们一位研发同事，自己 vibe 了个小程序》《一餐不只是一餐》《产品设计：敲敲里的小花》。2026-04 以前的文章全部已在站内。不导入：别人写的（刘容、郭玉珍、欧阳威等）、转载、已在站内的同文异题（《我怎么用 AI 辅助写作》即《AI 写文章》、《清明祭祖感受到的争执》、《视障摄影展》、《知识星球官方 Skill 发布》、《不可能的任务》研究页）、创业笔记 973、只有链接列表的《我看过的一些好文章》。删除当天早些时候导入的林晨《用 AI 重写了一个 App》（不是 Luca 本人的文章）。27 张配图存到 `static/images/<slug>-N`，alt 按上下文和图片内容写。导入方式与上一批相同。
- 站点图标换成 Luca 的头像：`static/favicon.png`（192×192）、`static/apple-touch-icon.png`（180×180）覆盖主题自带的图标，新增 `static/favicon.ico`（16/32/48）。研究页没有图标标签，浏览器默认读 `/favicon.ico`。图标用头部裁切，小尺寸下也认得出。
- 创业笔记补齐到 976：新增 969–976 共 8 篇，以及此前漏掉的 274、342、346、647 四篇（源文件没有 `.md` 后缀或是 `.txt`，导入脚本只读 `.md`）。仍按 `scripts/import-startupnotes.py` 切半，只发前半段。导入时用源文件夹的临时副本补后缀、给 342 的标题行加 `# `，`Luca` 仓库不改。日期取知识星球“星球创业笔记”（511244584）的发布时间，写入 `scripts/zsxq-dates.json`（11 条，带 topic_id）；346 按正文核对了 topic。脚本同时会把 966–968 的日期改成源文件里更晚的日期，并把 966 的链接改回旧的 wlj.me/reading，这三篇已还原，manifest 对应三行也还原。724 号在源文件夹里不存在，仍缺。
- 补入公众号“吴鲁加”2026-04-20 到 2026-11-04 发表、网站上还没有的 13 篇文章：《长期价值》《当 AI 让人人都能做产品，怎么做出你的不一样》《快时代需要慢技能》《极简主义》《所谓财务自由》《推荐文章 how to be good at research》《下一个三十年？》《残酷的 1.0》《选朴素的工具》《艹，是屎》《用龙虾等 Agent 访问知识星球》《AI-native 的公司与国家》，以及林晨的《用 AI 重写了一个 App，用了一个月，我学到了这些》（`author` 写林晨）。名单来自公众号的“随笔”“知识星球”两个合集和笔记里分享过的文章链接；不在合集里、也没分享过链接的文章可能还有遗漏。正文取公众号发表版本，日期用公众号发表时间，标签为 WeChat 加一个主题标签；去掉文末“欢迎你加入我的知识星球”推广段和封面出处行，与 2026-04-02 的公众号导入一致。8 张配图存到 `static/images/<slug>-N`，alt 按上下文写。与以往导入一样直接写入 `content/posts/`，没有走 publish.sh（脚本只能写当前时间）。
- 首页精选板块每篇前面加日期，与其他四个板块格式一致。
- 新增资料页《深圳及珠三角墨水屏设备采购调研》，`static/research/prd-epaper-suppliers/index.html`。比较深圳及珠三角墨水屏设备、开发套件与小批量采购，附联网限制、样机预算和验收计划。
- 首页改为五个板块，按顺序是精选、日志、研究、笔记、创业笔记。每块有“全部”链接，列最新几条，一行一条（日期和标题）：精选 10 篇（`data/featured.toml` 的 home 列表）、日志 8 篇、研究 6 篇（按 `research-materials.toml` 的日期，跳过 noindex）、笔记 5 条、创业笔记 5 篇（按笔记编号）。首页不再列带摘要的分页文章，`/page/N/` 301 到 `/posts/page/N/`（两边都是每页 10 篇，页码对应）。样式在 `static/style.css` 末尾的 `.home-section`、`.home-list`。
- 精选页（`/featured/`）去掉每篇文章下面的简介，只留标题和年月。`layouts/_default/featured.html` 删掉 `featured-desc` 一行。
- 研究页跟随站点主题：共用样式 `templates/research/reading.css` 改用站点的 Solarized 配色（亮色底 `#fdf6e3`、暗色底 `#002b36`，正文和链接加深到 4.5:1 以上），每页顶部加站点的站名条和菜单，底部加站点页脚。页眉和页脚由 `scripts/research_style.py` 按 `hugo.toml` 的菜单和站名生成，`--sync` 写入，检查时内容不一致就报错。原来的“主题”下拉菜单换成页脚的 `[dark/light]` 按钮，与文章页共用 `localStorage` 的 `theme`。页脚不写年份，避免每年一月全部页面过期。`publish.sh research` 发布前先运行 `--sync`。92 个研究页已同步。测试新增 3 个（页眉被改、页脚缺失、同步补齐页眉页脚并去掉旧菜单）。
- 域名合并准备（分支 merge-wulujia-com，切换域名后再合并）：`baseURL` 改为 https://wulujia.com/，`publish.sh` 的 `SITE_URL`、研究页模板、脚本和测试里的域名同步改。`/reading/` 改名 `/research/`，菜单“整理”改“研究”：目录 `static/`、`content/`、`layouts/`、`templates/` 下的 reading 改为 research，`data/reading-materials.toml` 改为 `research-materials.toml`（字段 `reading_url` 改为 `research_url`），脚本和测试改名为 `research_style.py`、`research_tags.py`、`test_research_*.py`。92 个研究页的 canonical 和返回链接改为新地址，“返回整理”改“返回研究”。`publish.sh research`、`research-tags` 是新命令，旧的 `reading`、`reading-tags` 保留为别名。页面内部的 CSS 类名和元素 id（如 `reading-theme`）不改。文章、笔记里指向 wlj.me 和 `/reading/` 的 Markdown 链接改为站内相对路径；正文里手写的 wlj.me 网址不改，由 wlj.me 的整站跳转接住。`static/_redirects` 新增 213 条：旧 Jekyll 文章 28 篇各三种写法、`/feed.xml`、分页、5 个分类页和 60 个标签页，以及 `/reading/*` 到 `/research/` 的通配跳转。关于页删掉 Homepage 和 Blog 两行，`sameAs` 去掉 wulujia.com。GitHub 工作流里的脚本名和目录同步改为 research。2026-11-24 wulujia.com 已绑定到 Cloudflare Pages 项目 wlj-me，随后合并到 main。
- 站名条文字从 “wlj's terminal” 改成 “Luca's Blog”（`hugo.toml` 的 `logoText`）。
- 停用 GitHub Pages：`.github/workflows/hugo.yml` 改名为 “Check site”，只跑整理页测试、标签检查、样式检查和一次 Hugo 构建，去掉上传和部署两步及 Pages 权限；删除 `static/CNAME`（只有 GitHub Pages 读它）。线上一直由 Cloudflare Pages 项目 wlj-me 构建和服务，访客看到的内容不变。README、CLAUDE.md 的托管说明同步改。
- 补齐从 wulujia.com 迁移时漏掉的内容：`static/img/` 新增 53 个图片文件（cloud-disk-encrypt、data-leak-prevention、osmocombb-guide、zsxq 等 10 个目录），`static/attachments/porticor/` 新增 2 份 PDF。其中 38 个图片和 2 份 PDF 被现有文章引用，线上原来是 404；另外 15 个图片保留旧站地址，供合并域名后的旧链接使用。新增两篇文章《知识星球的星星之火》：`content/posts/zsxq-spark-2018.md`（2018-07-09）和 `zsxq-spark-2020.md`（2020-02-03），保留原日期，按 2026-04-05 迁移提交的格式直接导入，不走 publish.sh（脚本只能写当前时间）。2018 版里用 Tab 缩进的引文改成 `>` 引用（旧站把它们显示成代码块），文字不变。
- 精选重选：`data/featured.toml` 从 55 篇减到 36 篇。标准是本人写的、现在还成立的文章优先，同一题目不重复；编译和意译的文章只留 5 篇，单列一组“读别人的公司”。新增一组“安全与早年”（《绿盟往事》《一个信息安全研究团队的五年》《关系万千重》等 6 篇），“AI 与产品”和“工具与实录”合并为“AI 与工具”。首页顶部的 10 篇全部换成本人写的文章。菜单里“精选”移到第一项（`hugo.toml` 的 weight 50 → 5）。
- 精选页新增 8 篇原 wulujia.com 首页列出的文章：`data/featured.toml` 的“创业与小而美”加《20 岁的小公司》《与创作者、学习者在一起的七年》《七年知识星球经验，剖析付费社群本质》，“生活与阅读”加《十年十二问：2025》《每年十二问：2024》《重新思考价值观》《喜欢，长期，简单》《我学习摄影的一些体会》。原因：两站合并后旧首页的 28 篇列表消失，这些文章在 1,385 篇里没有入口。首页顶部的 10 篇不变。
- 新增资料页《美图公司产品发展调研（2008–2026）》，`static/reading/meitu-product-history/index.html`。美图公司 2008–2026 年做过的产品、上线时间和现状，AI 时代赚钱的产品和失败的项目，以及年报里的收获和教训。

## 2026-11-20

- 新增资料页《非全日制博士项目与导师指南》，`static/reading/part-time-doctoral-study/index.html`。比较中国大陆、新加坡与香港博士项目，区分非全日制、全日制与待确认路径，并列出院系、导师成就、代表论文、招生证据与申请限制。

## 2026-11-14

- 新增资料页《构建常驻 agent（中文译文）》，`static/reading/building-always-on-agents-2026-11/index.html`。《Building always-on agents》中文全文译文：事件收件箱、定时器、记忆、权限、发件箱五个原语。
- 新增资料页《Cursor 安全事件更新：中文全文与后续报道》，`static/reading/cursor-security-incident-2026-11/index.html`。Cursor 2026 年 11 月 13 日安全事件更新的中文全文，并整理供应商、安全研究者和其他受影响公司的后续信息。
- 新增资料页《BrainCo 强脑科技调研》，`static/reading/brainco-2026-11/index.html`。强脑科技的业务、产品、融资、财务口径、港股上市进展、争议与竞争格局，资料截至 2026 年 11 月。
- 新增资料页《西湖大学深度调研：从一封建议书到建校第八年》，`static/reading/westlake-university/index.html`。西湖大学从 2015 年建议书到 2026 年的创校史、理念、关键人物、治理与资金、人才、科研成果、同行比较、影响与争议。

## 2026-11-07

- 新增资料页《币安热钱包安全事件：入侵经过、链上授权、资金流与证据边界》，`static/reading/binance-hot-wallet-incident-2026-10/index.html`。2026 年 10 月币安热钱包安全事件研究：官方初步报告所述的入侵经过、EIP-7702 委托、冻结与洗钱进展，以及仍待查明的证据缺口。
- 新增资料页《小鹅通港股上市进展与成功几率调研》，`static/reading/xiaoe-hk-ipo-2026-11/index.html`。小鹅通第二次递表港交所后的进展、公司基本面、港股市场环境、2025 年以来的上市规则变化，上市成功几率估算，以及招股书里的现金、负债、现金流和 2026 年财报预测。数据截至 2026 年 11 月 6 日。

## 2026-11-05

- 新增资料页《Mac 上装 Mac 虚拟机：安装、隔离与备份》，`static/reading/mac-vm-isolation/index.html`。在 M 系列 Mac 上用 UTM 安装 macOS 虚拟机：UTM 简介和上手难度，IPSW 下载与 ipsw.me，物理机被入侵时虚拟机为什么保不住，八条隔离规则，以及用 AES-256 加密 DMG 做离线备份的设置。资料查阅日 2026 年 11 月 5 日。

## 2026-11-03

- 新增资料页《深圳房价一年回顾与未来半年预测（2025-10 到 2026-10）》，`static/reading/shenzhen-housing-trend-2026-11/index.html`。用国家统计局 70 城指数和乐有家网签数据回顾深圳 2025 年 10 月到 2026 年 10 月的房价走势，并给出未来 3 到 6 个月的预测。
- 新增资料页《出门问问财务与 TicNote 销售分析》，`static/reading/mobvoi-financials-ticnote/index.html`。出门问问 2021—2026 年财务变化、现金状况及 TicNote 销售与盈利证据。

## 2026-11-02

- 新增资料页《群晖 NAS 勒索事件：漏洞、补丁与处置建议》，`static/reading/synology-nas-security/index.html`。群晖 NAS 勒索事件调研：核实零日漏洞争议，区分 QuickConnect、Cloud Sync 与断网建议。
- 保留《Omarchy 开源运营笔记》中的公开邮箱，关闭脚本时仍可阅读。
- 保留《Open Source Endowment 调研》中的公开邮箱，关闭脚本时仍可阅读。
- 保留《OpenClaw 开源运营笔记》中的公开邮箱，关闭脚本时仍可阅读。
- 统一整理页《权力掮客速查》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《检测与打击 AI 滥用：2026 年 9 月》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Crash (exploit) and burn：0day 供应链的中美对比》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Before Vegas：塑造中国网络生态的「红客」》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 整理页复用文章主题标签，支持标签筛选并保留资料类型。
- 统一整理页《《周易》经传十五讲 · 学习指南》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《台北國際照顧博覽會：養老產品分類與分析》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《张小珺 · 曾鸣 · 产业史观》的字体、配色、目录和主题控件，保留正文及附件，并记录逐行误报核对。
- 统一整理页《OpenAI–Hugging Face 事件主题》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Decluttering at the Speed of Life · 操作指南》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Digital Minimalism · 阅读指南》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Clio：保护隐私的真实世界 AI 使用观察》的字体、配色、目录和主题控件，保留正文及附件，并记录逐行误报核对。
- 统一整理页《达里奥·阿莫代公开信与访谈》的字体、配色、目录和主题控件，保留正文及附件，并记录逐行误报核对。
- 统一整理页《Fortune × 萨姆·奥特曼访谈》的字体、配色、目录和主题控件，保留正文及附件，并记录逐行误报核对。
- 统一整理页《托比·吕特克：多数公司把 AI 用错了》的字体、配色、目录和主题控件，保留正文及附件，并记录逐行误报核对。
- 统一整理页《Mobilizing Cyber Power：中国网络民兵体系》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 部署前运行整理页测试和全量规范检查，失败时停止构建及部署。
- 统一整理页《The Longing for Less · 阅读指南》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Science: A New Golden Age · 阅读指南》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Mythical Beasts：全球间谍软件市场图谱》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《人生七年 · 人物志》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《OpenClaw 开源运营笔记》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Temasek Review 2026 速读》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《Slax Reader · 项目地图与开发指南》的字体、配色、目录和主题控件，保留事实及附件，并修正文案检查告警。
- 统一整理页《泉州老城区公寓房价分析》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《新加坡政府的钱从哪来》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《新加坡经济战略检讨，讲了什么》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《TechCrunch 深度调研》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Product Hunt 深度调研》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Crunchbase 深度调研》的字体、配色、目录和主题控件，保留正文及附件。
- 清理整理页《新加坡烟霾政策与棕榈油利益关系》的旧主题标签，保留打印按钮。
- 统一整理页《计算机历史博物馆：技术脉络与展品研究》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《斯坦福与伯克利｜大学对比研究》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《新加坡烟霾政策与棕榈油利益关系》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《深圳房价走势与南山详析》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《塞特知识股份有限公司｜公司研究》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《罗丹的雕塑：美感、材料与真迹》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《10 Ken Goldberg：机器人、AI 和艺术（图文版）》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《DSH 的插件理念》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《诱骗研发人员安装恶意软件：四类动作与 35 种场景》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《DESIGN.md：创业公司的设计规则文件》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Agentic robot 研究报告》的字体、配色、目录和主题控件，保留正文及附件。
- 清理经济报告样式中的行末空白。
- 统一整理页《YubiKey 的使用场景》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《《海豚湾》与太地町海豚追猎：各方观点、科学证据和影响》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Tencent TeamAI CLI 调研：团队如何共享 AI 工作方式》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《共享电梯与发改环资〔2025〕1745 号：国家、福建、泉州的推进状态》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《这就是 AGI｜Sequoia AI Ascent 2026 主题演讲中文译文》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《罗伯特·摩西的权力从哪里来：七件事和一套法律技术》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《里克·鲁宾谈创作与 AI：中文访谈全文》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《旁遮普失踪案与《Satluj》封禁：事实、追责和资讯自由》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《PHP2Shell：两个 PHP 核心漏洞的现状与处置》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Open Source Endowment 调研》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Omarchy 开源运营笔记》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《老小区加装电梯：常见装法与适装条件》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Mac 安全：NIST 的建议》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《MSIG TravelEasy：从新加坡出发的旅行险》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《拆解一套利用 EtherHiding 的 macOS ClickFix 犯罪工具包》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Mac 入侵日志采集与排查》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Mac 企业端云防护产品》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《减少本地凭据：用 1Password 和不用 1Password 的做法》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Lenny 播客半年 AI 实践调研》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《与 Henry 的“AI 季报 26Q3”：Muse 引爆个人助理、Astra 进入机器人、OpenAI 收入猛增》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Kingfisher 密钥扫描工具》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Instinct 创始人 Noah Shinn 谈个人 AI 助手》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《一张 HEIC 图片如何打到 OpenAI 的内部仓库》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《怎么给 dsh 写插件》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《旧金山的两座美术馆：de Young 博物馆与荣勋宫》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《中国经济，好还是差》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《C2 通信现状、企业网络限制与遗留风险》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《伯克利周边博物馆：开门时间、票价和要逛多久》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Apple Business 免费设备管理部署指南》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《AMOS（Atomic macOS Stealer）资料汇总》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《AI 视频入门：40 分钟教学计划》的字体、配色、目录和主题控件，保留正文及附件。
- 统一整理页《Bybit 失窃事件》的字体、配色、目录和主题控件，保留正文及交互。
- 统一整理页《Jev 在知识星球的应用》的字体、配色、目录和主题控件，保留正文及交互。
- 统一整理页《ALPA 12 TC 后背指南》的字体、配色、目录和主题控件，保留正文及交互。
- 统一整理页《AssemblyAI 的特点与竞品》的字体、配色、目录和主题控件，保留正文及交互。
- 新增整理页统一模板和样式检查器。发布前检查全部 HTML 子页；新增 `--local`，支持本地检查和写入，不提交、不推送。现有页面正在迁移。
- 新增资料页《Bybit 失窃事件》，`static/reading/bybit-security-investigation/index.html`。Bybit 2025 年失窃事件图解：入侵、演练、执行、资产追索与安全整改。

## 2026-10-31

- 新增资料页《10 Ken Goldberg：机器人、AI 和艺术（图文版）》，`static/reading/ken-goldberg-robotics-2026-10/index.html`。Ken Goldberg 在伯克利关于机器人、AI 与艺术的课堂笔记，含机器人抓取、手术、农业、智能体机器人及相关背景资料。

## 2026-10-30

- 新增资料页《诱骗研发人员安装恶意软件：四类动作与 35 种场景》，`static/reading/developer-social-engineering/index.html`。按四类动作整理 35 种公开诱骗场景，含 28 张逐图复核的原报告配图和 31 个来源。

## 2026-10-29

- SEO：Person 结构化数据的别名加入 wulujia。
- SEO：描述长度按字符数计算，不再按字节数计算。手写的中文描述不再被误加“...”。
- SEO：创业笔记页的 `og:type` 改为 `article`；`og:locale` 改为 `zh_CN`。
- 新增资料页《计算机历史博物馆：技术脉络与展品研究》，`static/reading/computer-history-museum/index.html`。围绕博物馆展品解释计算机历史，包含技术机制、软件、网络与公开在线展览条目索引。
- 发布文章《盲人摄影展》，原文展示在首页日志列表。
- 新增资料页《新加坡烟霾政策与棕榈油利益关系》，`static/reading/singapore-haze-policy-ownership/index.html`。截至 2026 年 10 月 29 日，核查新加坡烟霾执法、区域合作与棕榈油股权关系。
- 新增资料页《AssemblyAI 的特点与竞品》，`static/reading/assemblyai-competitors-2026-10/index.html`。语音转文字接口 AssemblyAI 的产品、长处和短板，以及它和 Deepgram、ElevenLabs Scribe、Whisper 等竞品的准确率、延迟、价格对比，和按场景的选型建议。

## 2026-10-28

- 新增资料页《罗丹的雕塑：美感、材料与真迹》，`static/reading/rodin-sculpture/index.html`。通过八幅馆藏照片，解释罗丹的美感与风格变化，并区分雕塑材料、生前铸件、身后铸件与复制品。
- 新增资料页《Agentic robot 研究报告》，`static/reading/agentic-robot-research/index.html`。自主决策机器人研究：技术实现、商业证据、模型分工与世界模型影响。

## 2026-10-27

- 新增资料页《ALPA 12 TC 后背指南》，`static/reading/alpa-12tc-backs/index.html`。ALPA 12 TC 撕拉片后背、CFV II 50C 数码后背与 HAA 转接板的图文指南。
- 新增资料页《斯坦福与伯克利｜大学对比研究》，`static/reading/stanford-berkeley/index.html`。比较斯坦福与伯克利的本科教学、科研、教授、创业、资金、住房和治安。用同年班级与安全数据，说明两校优势及费用如何改变选择。

## 2026-10-23

- 新增资料页《MSIG TravelEasy：从新加坡出发的旅行险》，`static/reading/msig-traveleasy-2026-10/index.html`。MSIG TravelEasy 的投保条件、四档保额、购买步骤、急救热线和理赔方式。适合住在新加坡、从新加坡出发去第三国的行程。
- 新增资料页《伯克利周边博物馆：开门时间、票价和要逛多久》，`static/reading/berkeley-museums-2026-10/index.html`。伯克利校园及东湾七家博物馆的开门时间、票价、离 Haas 商学院的距离、值得看的东西和建议停留时间，另附旧金山四家。

## 2026-10-22

- 新增资料页《PHP2Shell：两个 PHP 核心漏洞的现状与处置》，`static/reading/php2shell-2026-10/index.html`。CVE-2026-109618 与 CVE-2026-109619 的机制、在野攻击证据、exploit 传播情况，以及修复与临时阻断方法。

## 2026-10-21

- 新增资料页《旧金山的两座美术馆：de Young 博物馆与荣勋宫》，`static/reading/deyoung-legion-of-honor/index.html`。介绍旧金山 de Young 博物馆和荣勋宫的历史、建筑、馆藏和参观方式。

## 2026-10-13

- 新增资料页《罗伯特·摩西的权力从哪里来：七件事和一套法律技术》，`static/reading/robert-moses-power-sources/index.html`。根据卡罗《权力掮客》整理：罗伯特·摩西在七件关键事件中靠什么做到、欺骗和伤害了谁，重点拆解 1924 年公园法和三区大桥管理局修法的条文技术。
- 将 Mac 日志指南改为中文，保留原网址和来源链接；修复整理页更新时未刷新列表标题和摘要的问题。

## 2026-10-11

- 新增资料页《YubiKey 的使用场景》，`static/reading/yubikey-use-cases-2026-10/index.html`。YubiKey 能用在哪些地方：网站登录、电脑登录、SSH 和 Git、加密签名、TOTP 验证码，它不做的事，以及按优先级的建议配置。
- 新增资料页《AI 视频入门：40 分钟教学计划》，`static/reading/ai-video-intro-40min/index.html`。教只用过聊天机器人的朋友用 AI 做视频：工具、流程、技巧、演示和案例。
- 新增资料页《Mac Intrusion Logging》，`static/reading/mac-intrusion-logging-2026-10/index.html`。How to send company Mac logs to a central server, which events to collect to detect an intrusion, which tools to use, and which files to check on a suspect Mac.

## 2026-10-10

- 新增资料页《Mac 安全：NIST 的建议》，`static/reading/nist-mac-security-mscp-2026-10/index.html`。NIST 对 Mac 安全的建议：mSCP 与 SP 800-219 的版本状态、用法、基线要求的设置，以及它不覆盖的风险。

## 2026-10-09

- 新增资料页《减少本地凭据：用 1Password 和不用 1Password 的做法》，`static/reading/local-credentials-1password/index.html`。按凭据类型列出用 1Password 和不用 1Password 的两套做法，包括无人值守的办公室机器。

## 2026-10-08

- 新增资料页《Open Source Endowment 调研》，`static/reading/open-source-endowment-2026-10/index.html`。Open Source Endowment（OSE）怎么运作、钱从哪来、谁在管、资助了谁、投资是否公开。数据截至 2026-10-08。

## 2026-10-07

- 新增资料页《C2 通信现状、企业网络限制与遗留风险》，`static/reading/c2-landscape-network-controls-2026-10/index.html`。恶意程序与控制服务器之间的通信有哪些方式，企业在网络层应做哪些限制，做完之后还剩什么风险。附 UniFi 实施示例、开源清单的自动更新和托管安全 DNS 方案。
- 新增资料页《Mac 企业端云防护产品》，`static/reading/mac-enterprise-security/index.html`。比较 Mac 企业端云防护产品，覆盖商业方案、开源方案与试用检查。
- 新增资料页《Apple Business 免费设备管理部署指南》，`static/reading/apple-business-free-mdm-guide/index.html`。面向新加坡与中国大陆企业，说明 Apple Business 免费设备管理的功能、注册、设备注册方式与部署检查。

## 2026-10-06

- 新增资料页《Kingfisher 密钥扫描工具》，`static/reading/kingfisher-secret-scanner/index.html`。MongoDB 开源的密钥扫描工具 Kingfisher：来历、四项能力（找密钥、在线验证、影响范围、吊销）、安全团队的正常用法，攻击者拿到它之后的用法和造成的破坏，以及防护办法。
- 新增资料页《AMOS（Atomic macOS Stealer）资料汇总》，`static/reading/amos-atomic-macos-stealer-2026-10/index.html`。AMOS 是 2023 年起在 Telegram 按月出租的 Mac 窃密木马。本页汇总它的分支（Poseidon、Odyssey、Banshee 等）、偷取的数据、2025 年加入的后门和 2026 年的远程 shell，以及 2023 年 4 月到 2026 年 9 月公开报道的 20 次传播事件和自查方法。

## 2026-10-05

- 新增资料页《拆解一套利用 EtherHiding 的 macOS ClickFix 犯罪工具包》，`static/reading/macos-clickfix-etherhiding-crimekit-2026-08/index.html`。NetbyteSEC 2026 年 8 月 macOS 恶意软件分析的中文译本。受害者被假验证页骗着把命令粘进终端，后门从 Polygon 智能合约读取 C2，按指令投放 AMOS 窃密木马、XMRig 矿工或远程 shell。作者从链上交易还原出 21 次 C2 轮换和出资路径。附原文 25 张图和完整入侵指标。

## 2026-10-03

- 新增资料页《与 Henry 的“AI 季报 26Q3”：Muse 引爆个人助理、Astra 进入机器人、OpenAI 收入猛增》，`static/reading/latetalk-ai-quarterly-26q3/index.html`。晚点聊 LateTalk 第三季度 AI 季报的中文全文整理稿：MUSE、Dots、Instinct 等个人助理产品，一家前沿实验室的年化收入从 400 亿美元涨到 700 亿美元，新一代旗舰模型之后的机器人和物理 AI，以及多智能体协作失控事件。人名和产品名由语音识别给出，请以原音频为准。

## 2026-10-02

- 新增资料页《Instinct 创始人 Noah Shinn 谈个人 AI 助手》，`static/reading/instinct-noah-shinn-2026-09/index.html`。Invest Like The Best 对 Instinct 创始人 Noah Shinn 的访谈中文全文译稿，按 17 个主题分节，谈助理之间的协作、订阅与支付、邀请制增长和算力成本。

## 2026-09-28

- 新增资料页《这就是 AGI｜Sequoia AI Ascent 2026 主题演讲中文译文》，`static/reading/sequoia-ai-ascent-2026/index.html`。Sequoia Capital AI Ascent 2026 主题演讲中文译文：Pat Grady、Sonya Huang、Konstantine Buhler 谈智能体、AI 应用与认知劳动。
- 新增资料页《里克·鲁宾谈创作与 AI：中文访谈全文》，`static/reading/rick-rubin-the-only-skill/index.html`。The Diary Of A CEO 对音乐制作人 Rick Rubin 的访谈中文全文译稿，按 30 个章节分节，可跳转至原视频对应时间。

## 2026-09-26

- 新增资料页《海豚湾》与太地町海豚追猎，`static/reading/the-cove/index.html`。

## 2026-09-25

- 新增资料页《旁遮普失踪案与《Satluj》封禁：事实、追责和资讯自由》，`static/reading/punjab-disappearances-satluj/index.html`。梳理旁遮普冲突死亡、强迫失踪、秘密火化、Jaswant Singh Khalra 案、《Satluj》的制作与封禁、导演和演员承受的压力，以及印度资讯自由的制度背景。
- 修复 `publish.sh reading` 在标题变量后紧接中文标点时触发未绑定变量、导致整理页无法发布的问题。

## 2026-09-24

- 新增资料页《塞特知识股份有限公司｜公司研究》，覆盖创始人与股权、课程收费及分润、用户市场、上市核查和 2025 年经营数据，附 46 个来源。

## 2026-09-22

- 新增资料页《Jev 在知识星球的应用》，`static/reading/jev-zsxq/index.html`。从星主待办、历史内容推荐到成员匹配，讨论 System One 判断模型的业务价值与验证方法。

## 2026-09-21

- 资料页《Tencent TeamAI CLI 调研》删除以 9 月 8 日旧稿为基线的变化记录，后续章节编号同步调整。
- 新增资料页《Tencent TeamAI CLI 调研：团队如何共享 AI 工作方式》，`static/reading/tencent-teamai-cli/index.html`。更新至稳定版 0.24.0，补充多项目、团队包、Agent 支持矩阵、安全边界与 2026-09-21 项目快照。
- 新增资料页《一张 HEIC 图片如何打到 OpenAI 的内部仓库》，`static/reading/hacking-openai/index.html`。拆解论坛图片上传、libheif 堆溢出、OpenAI 单点登录缺陷与防守动作。
- 新增资料页《老小区加装电梯：常见装法与适装条件》，`static/reading/old-neighborhood-elevator-guide/index.html`。
- 新增资料页《共享电梯与发改环资〔2025〕1745 号：国家、福建、泉州的推进状态》，`static/reading/shared-elevator-policy-quanzhou-2026/index.html`。

## 2026-09-20

- 更新资料页《泉州老城区公寓房价分析》：补充“平层入户”说明，按写作与 HTML 规范重做目录、亮暗主题和打印样式；发布脚本新增整理页安全更新模式。
- 列表页每页条数从 5 改为 10（`hugo.toml` 的 `pagination.pagerSize`）。日志、首页、创业笔记、标签页都受影响；笔记列表本来就是每页 20，不变。
- 分页改为带页码的导航：`layouts/partials/pagination.html` 覆盖主题只有上一页 / 下一页的版本。始终显示第 1 页和最后一页，当前页前后各两页，中间的用省略号折叠（只差一页时直接显示页码，不出现“1 … 3”）；当前页不是链接，带 `aria-current="page"`；上一页 / 下一页带 `rel="prev|next"`；底部加“第 N / M 页”；只有一页时整块不渲染。样式放在 `assets/css/pagination.css`（覆盖主题同名文件，Hugo 按 `resources.Match "css/*.css"` 取项目版本）。
- 整理页 `/reading/` 也分页，每页 10 条，页码样式和其他列表一致。整理页的条目来自 `data/reading-materials.toml` 而不是 Hugo 页面，又带分类筛选，Hugo 的 `/page/N/` 分页和筛选合不到一起，所以在浏览器里做：`layouts/reading/list.html` 的脚本先按分类筛选再切页，页码写进 hash（`#report/2`），换分类回到第 1 页。全部条目仍在 HTML 里，没有 JS 时显示全部，索引不受影响。

- 创业笔记列表改按笔记编号倒序：`layouts/startupnotes/list.html` 用 `sort .Pages "Params.note_number" "desc"` 排序后再分页。原先走 Hugo 默认的 date 倒序，但大量笔记的 date 是从同一次 git 提交回填的，同一时间戳内的先后由文件名决定，列表顺序因此是乱的（963、964、965、962、960）。
- `scripts/import-startupnotes.py`：frontmatter 新增 `note_number` 字段（列表排序依据，新增笔记必须有）；编号超出已知日期范围时，date 改用源文件 mtime，不再让新笔记全部塌到最后一个已知时间戳上；`SOURCE_DIR` 默认值改为 `~/Github/Luca/startupnotes`，不再写死 macOS 路径。
- 导入创业笔记 966、967，现有 963 篇回填 `note_number`，正文无改动。
- 新增资料页《怎么给 dsh 写插件》`static/reading/dsh-plugin-guide/index.html` 和《DSH 的插件理念》`static/reading/dsh-plugin-philosophy/index.html`，自包含 HTML，`index,follow` + canonical，顶部返回链接；`data/reading-materials.toml` 各新增 report 条目。
- 补齐五个整理页缺失的顶部返回链接（dario-amodei-pace-the-frontier-2026-09、detecting-and-countering-ai-misuse-2026-09、sam-altman-fortune-titans-2026-09、shenzhen-housing-outlook、slax-reader-project-guide），打印时隐藏。

## 2026-09-19

- `publish.sh` 支持在同一套检查、提交和推送流程中更新已有文章，并保留原发布日期。

## 2026-09-17

- 首页顶部的「Luca's Blog」大标题去掉。`layouts/_default/index.html` 的 `<h1>` 加上 `page-title--hidden`，和栏目页、关于页一致：标题仍在 DOM 里留给搜索引擎和读屏软件，导航到第一行内容的间距变成统一的 30px。`hugo.toml` 的站点标题不动，`<title>`、OG、JSON-LD 都不受影响。
- 关于页顶部还留着「关于」大标题和「by Luca」一行，和其它栏目页不一致。新增 `layouts/_default/about.html`，`content/about/index.md` 指定 `layout: "about"`，`<h1>` 改为和日志、整理、归档等页面相同的视觉隐藏写法（标题仍在 DOM 里），不再显示作者行。页面仍在 sitemap 里，索引策略不变。

## 2026-09-16

- 新增资料页《深圳房价走势与南山详析》，`static/reading/shenzhen-housing-outlook/index.html`。深圳全市宏观背景、人口、房价交易、住房供应与两年情景，附南山近年价格、片区及小区详析。
- 新增资料页《托比·吕特克：多数公司把 AI 用错了》，`static/reading/tobi-lutke-ai-judgment-2026-09/index.html`。The Knowledge Project 访谈中文问答整理；加入 Reading 索引、canonical、分享元信息与返回整理链接。
- 顶部导航顺序改为 日志、整理、笔记、创业笔记、精选、归档、标签、关于。
- 栏目页的大标题和导航重名，页面顶部会看到两个同名的词。日志、整理、笔记、创业笔记、精选、归档、标签七个页面的 `<h1>` 改为视觉隐藏（标题仍在 DOM 里，留给搜索引擎和读屏软件），导航到第一行内容的间距统一为 30px，和文章页相同。当前所在栏目在导航里加下划线。新增 `layouts/partials/menu.html`、`layouts/partials/mobile-menu.html`、`layouts/_default/terms.html` 覆盖主题模板，样式写在 `static/style.css`。2026-09-11 那条单独收紧 `/reading/` 标题间距的改动，被这次的统一规则取代。
- 归档页纳入整理页：`layouts/_default/archives.html` 把 `content/posts/` 的文章和 `data/reading-materials.toml` 的整理条目按时间排成一条时间线，整理条目标 `#整理`，年份活动条的计数一并计入。`content/archives.md` 的 description 同步改写。

## 2026-09-15

- 新增资料主题《OpenAI–Hugging Face 事件主题》，`static/reading/openai-huggingface-incident-2026-09/`。主题首页串联六份材料：OpenAI 技术报告中译、METR 调查中译、Black Hat USA 2026 演讲整理、JFrog Artifactory 零日笔记、HF Agent 回放收集、「像人与失控」解读；均含 canonical 与返回链接。

- `publish.sh` 新增 `reading` 子命令，整理页改为脚本发布：校验 HTML head（title、手写 description、robots、canonical 与 slug 一致、返回整理链接、图片 alt），复制目录到 `static/reading/<slug>/`，追加 `data/reading-materials.toml` 条目（date 取当前时间），在 CHANGELOG 当天标题下加一行，本机有 hugo 时构建并检查 sitemap，再 commit、push。支持 `--noindex`、`--post-slug`、`--changelog`、`--dry-run`。 发布前加两道检查：文章先过 luca-writing 的 `lint_ai_flavor.py`，整理页先过 luca-html 的 `check_html.py`（含正文的 luca-writing 检查），有 warning 或 error 就不写入、不提交；文章里的 `<!-- lint-disable-line -->` 标记发布时自动删掉。原有 `./publish.sh input.md tags` 用法不变，另加 `post` 子命令别名。`CLAUDE.md`、`AGENTS.md`、`README.md` 同步补发布流程。
- 新增资料页《张小珺 · 曾鸣 · 产业史观》，`static/reading/zhangxiaojun-zengming-industry-history-2026-09/index.html`。《张小珺商业访谈录》第 153 期问答整理；加入 Reading 索引、canonical、分享元信息与返回整理链接。


## 2026-09-14

- 新增日志《Artifactory 是什么》，简述软件包存储、公共仓库缓存和构建部署中的用途，附 JFrog 官方来源。

- 新增资料页《DESIGN.md：创业公司的设计规则文件》，`static/reading/design-md-guide/index.html`。保留中文说明、双页面互动示例、文件分工和来源；加入“杂项”索引、返回整理链接、canonical 与分享元信息，沿用明暗主题、手机目录和打印样式。
- 新增资料页《达里奥·阿莫代公开信与访谈》，`static/reading/dario-amodei-pace-the-frontier-2026-09/index.html`。公开信在前，CBS 加长访谈在后，保留 18 组问答、全文译文及来源说明；目录同步调整。加入 Reading 索引、canonical、分享元信息与返回链接，沿用明暗主题、手机目录和打印样式。

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
