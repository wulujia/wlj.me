---
title: "用龙虾等 Agent 访问知识星球"
date: 2026-05-06T16:24:53+08:00
tags: ["WeChat", "AI"]
draft: false
slug: "agents-access-zsxq"
---

知识星球上线了官方 Skill，接入你的 AI 工具比如小龙虾后，它可以帮你查内容、搜主题、回复提问、出运营报告。

按下面的步骤安装知识星球的技能：

1. 安装 CLI 工具

npm install -g zsxq-cli

2. 安装 Skill

npx skills add https://github.com/unnoo/zsxq-skill --yes --global

之后，你可以查星球内容、搜帖子、看足迹等，比如：

- 直接告诉 AI 你想做什么，比如「帮我看看今天有多少未回答的提问」

- 涉及发帖、回复、删除这类操作，AI 会先给你看内容，确认后才执行

以及，有个细节值得说下，是否允许 AI 工具访问星球，这件事星主说了算。操作方式如图：

![知识星球里设置是否允许 AI 工具访问星球的界面](/images/agents-access-zsxq-1.png)

默认关闭——这也是有人觉得 Skill 鸡肋的原因。但我们的考虑是：

1. 优先解决星主管理星球的困难。星主直接可以针对自己的星球使用 skill。

2. 如果星主觉得开放 AI 访问他的星球，对他的星球有帮助，那可以选择打开，但默认关闭。

3. 星主可以随时关闭 AI 访问权限，不用担心失控。

4. 即便打开，我们也做了风控来识别爬虫等异常，目前不完善，但在持续改进。

Skill 官网在 https://garden.zsxq.com/skill，这是我们考虑的，[让一千朵花先开](https://mp.weixin.qq.com/s?__biz=Mzg5NDY4ODM1MA==&mid=2247485863&idx=1&sn=3ed3456871ffc4c35dac5f69e8107631&scene=21#wechat_redirect)，先绽放再说——在 AI 面前，跑得快可能是找死，跑得慢可能是等死，无论如何，还是跑起来比较开心。
