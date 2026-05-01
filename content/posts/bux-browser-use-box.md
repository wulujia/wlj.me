---
title: "browser-use 团队又出了一个东西，叫 bux"
date: 2026-05-01T10:31:12+08:00
tags: ["AI","Tools"]
draft: false
slug: "bux-browser-use-box"
---

[browser-use](https://github.com/browser-use/browser-use) 团队最近又放了一个新项目：[bux](https://github.com/browser-use/bux)，全名 Browser Use Box。

它解决的问题很具体：现在所有 AI 助手都绑在你设备上，合上电脑就死。bux 把 Claude Code 加一个真实 Chromium 浏览器，再加一个 Telegram 机器人，打包成一条安装脚本，扔到任何一台 5 美元的 VPS 上跑起来。

跑起来之后是什么效果？早上你在地铁上发一条 Telegram，"看看今天未读邮件，回那条 LinkedIn 消息说不感兴趣"，下班前活已经干完了。机器一直开着，账号一直登着，不用你守在电脑前。

三个细节我觉得做得对。

第一，用真实 Chromium，不是 headless 浏览器。Cookie、登录态都持久化在服务器上，账号一直在线。

第二，遇到验证码、2FA、登录墙的时候不硬刚。它会生成一个实时页面 URL 推给你，你点开手动过验证，AI 接着干。大多数自动化工具死在这一步——硬刚就被风控、被封号。bux 直接承认这件事 AI 做不了，让人来。

第三，整个架构就三个 systemd 服务：Telegram 机器人收消息，喂给 Claude，调浏览器。状态全在 `/home/bux` 一个目录里，重启不丢。打开看一眼就知道每个零件在哪。

安装是一条 curl 命令，三分钟从空白 VPS 到能用。

[browser-use](https://github.com/browser-use/browser-use) 主项目 GitHub 6 万多 star，bux 又是 Claude Code 加 Telegram 加云端浏览器一条龙打包好。这个团队战斗力真的强。
