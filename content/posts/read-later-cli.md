---
title: "稍后读的 Cli 玩法"
date: 2026-05-18T08:07:45+08:00
tags: ["WeChat", "Tools"]
draft: false
slug: "read-later-cli"
---

先说一句：如果要注册 Slax Reader，用 https://r.slax.com/luca-reader，送几个月的 Pro 功能。不过我刚刚盘了一下，同事们有点慷慨，不用 Pro 就能用了。比如：

- 永久备份功能免费：书签 + 缓存功能直接给永久免费——这个在 readwise / Instanpaper / Matter / 曾经的 Pocket 都是付费能力，这个其实很给力。

- 全文搜索、划线评论功能免费：这也是其他产品的付费能力。

- 开源：Apache 2.0 开源，可导出，可自托管，公司现金流稳定愿意长期运行。

- 多语言网页持续优化改进：以中文为例，对微信公众号、小红书、微博、知乎的解析水平和持续改进非常好。

- 跨平台支持：iOS、Android、Web、浏览器扩展。

Slax Reader 新推出的 Cli 的几种玩法

玩法一：批量收藏

让 agent 帮你扫一个页面、一个 feed、一整个网站，按你的标准批量存。比如你可以：

- 扫 Hacker News 首页，把分数超过 200 的链接存为 archive 模式（连快照都抓）

- 把某个公众号近 30 天的文章扫一遍，标题里带"agent"的存起来

- 看你的 Twitter timeline，把那几个你最常点保存的人发的链接全收了

听起来像爬虫——区别是你不用写爬虫，跟 agent 说人话就行。

玩法二：筛选式订阅 — 替代 RSS / Newsletter，盯某个页面

传统的信息流处理是：订阅源 → RSS reader 抓 → 你逐条扫 → 觉得有用的存下来 → 真有空时回去读

现在变成：Agent 替你扫信息源 → 给你一份摘要简报 → 你说哪几条有用 → agent 直接存进 Reader

我自己发现这条之后，把绝大多数 RSS 订阅和 newsletter 的优先级都降到了底。不是它们不好用，是中间那段"逐条扫标题"现在该由 AI 干。

落地例子：

- 关注几个云服务（Cloudflare、Vercel、Supabase）。让 agent 每周扫一遍 changelog，写成简报。你说"这三条细看"，agent 把链接存进 Reader 加上 cloudflare 标签

- 关心新加坡 AI 政策。让 agent 每天扫几个媒体源，把"和新加坡 AI 战略相关"的存进 Reader，月底自动合成一份月报

- 写博客。让 agent 扫你关注的 30 个独立博客，把这周新发的、和你当前写作主题相关的存起来

玩法三：稍后读 → 知识管道

reader-cli get <id> --markdown 这个组合，多数人低估了它的威力。你 Reader 里的每一篇文章，现在都是 AI 可以拿来再加工的原料。下游接什么都可以。比如：

- AI 帮我读长文：30 分钟的文章丢给 agent，让它返回"3 个最反共识的点 + 1 个我大概率不同意的点"。不是总结，是过滤

- 多语翻译：英文长文存下，让 agent 译成中文回写到你的 Notion

- 转播客：markdown → TTS → 通勤路上听

- 接知识库：存的同时让 agent 抽实体（人、公司、概念），写进你的 Obsidian / 飞书 / 自建笔记

- 写作素材库：写新文章前，让 agent 在你 archive 里搜相关旧文，自动列出引用源

玩法四：写作时的"过去的自己"

每个写作者都重复发明过轮子——明明上个月读过一篇文章把这个观点讲得很清楚，但忘了它在哪。

有了 reader-cli，写作前你可以让 agent 跑一次："在我 Reader 过去 90 天的存档里，找出所有讲 AI agent 设计模式的文章"

Agent 会回一份"你自己的研究笔记"，不重复造轮子。

进阶玩法：每次读到反驳你过去某个观点的内容，存的时候打个 #self-challenge 标签。季度盘点一次——这就是你观点演化的可视化。

玩法五：跨 agent 的"信息状态层"

你可能在 Claude Code 里干活，也可能用 OpenClaw 浏览，也可能跑 ChatGPT 写东西。每个 agent 都是孤岛——它们彼此不知道你在另一边干了什么。

但 Slax Reader 不是孤岛。它有 API、有 CLI、有 Skill。

意思是：A agent 存的内容，B agent 能读到。

实际场景：

- 上午 OpenClaw 浏览时存了 10 篇文章

- 下午让 Claude Code 给你写一篇相关博客

- Claude Code 调 reader-cli 读出今天存的 10 篇，作为写作素材

Reader 变成了你 AI 工具栈里的"共享内存"。

安装 Slax Reader Cli

Slax Reader Cli （https://github.com/slax-lab/slax-reader-cli）工具上线，目前是 v0.1.1 版本，各位可以去摸摸。去 https://r.slax.com/user 中，定位到 API Key 栏目，生成相应的 API Key，按指引，让 Agent 自己装就行了。

如果要注册，用我的分享链接：https://r.slax.com/luca-reader，送几个月的 Pro 功能。
