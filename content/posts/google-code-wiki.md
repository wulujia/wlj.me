---
title: "Code Wiki：Google 给 GitHub 仓库自动生成的可交互 wiki"
date: 2026-05-10T22:35:00+08:00
lastmod: 2026-05-10T22:35:00+08:00
author: "Luca"
tags: ["AI","Docs","Tools"]
draft: false
slug: "google-code-wiki"
---

Google 在 2025 年 11 月推出了 [Code Wiki](https://codewiki.google)，对着任意 GitHub 公开仓库自动生成持续同步的可交互文档站——架构图、类图、时序图，加一个用这份 wiki 当上下文的 Gemini chat。

用法：把 `github.com/<org>/<repo>` 换成 `codewiki.google/github.com/<org>/<repo>`。

丢一个看效果：[openclaw/openclaw 的 Code Wiki 视图](https://codewiki.google/github.com/openclaw/openclaw)。

私有仓库要走 Gemini CLI extension。

官方介绍：[Introducing Code Wiki](https://developers.googleblog.com/introducing-code-wiki-accelerating-your-code-understanding/)。
