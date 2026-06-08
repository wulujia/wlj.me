---
title: "创业笔记 936：一种问题的多种解法"
date: 2026-05-04T11:04:23+08:00
lastmod: 2026-05-04T11:04:23+08:00
author: "Luca"
tags: ["Startup"]
draft: false
slug: "startup-note-936"
summary: "前几天，老朋友孟岩在一个小群里说：最近沉迷编程，做了一个我自己用的 Agent 客户端哈哈，昨天推荐给了池老师，大辉和吴老有空可以试试。 然后发了个链接：https://github.com/dreamwords/hammer-releas"
paywall: true
---

前几天，老朋友孟岩在一个小群里说：最近沉迷编程，做了一个我自己用的 Agent 客户端哈哈，昨天推荐给了池老师，大辉和吴老有空可以试试。

然后发了个链接：https://github.com/dreamwords/hammer-releases

我看了看，他想解决的问题，以及解法是：

> AI 编程助手越来越多，但每个都有自己的界面、自己的会话记录、自己的操作方式。你在 Claude Code 终端里开了一个任务，又想用 ChatGPT 试试另一个方案，再看看 Kimi 对某段代码的理解——结果三个窗口、三套工具、三份散落的历史。
>
> Hammer 把这些装进一个桌面应用：不同对话用不同模型，历史永久保存，文件树、任务进度、用量统计都在一个界面里。你只管和 AI 说话，不用在工具之间来回切。

我自己也碰到类似的麻烦，但切入的角度不一样。我同时用 Claude Code 写代码、Codex 做审查、Gemini 做研究、OpenClaw 跑自动化。同时我很喜欢用不同工具时体验他们的细微差异——Zed、Obsidian、Neovim、Cursor、vscode 等等……

每个工具都要我重新解释一遍"我是谁、怎么沟通、决策原则是什么"。配置文件名还各不相同——Claude 读 CLAUDE.md，Codex 读 AGENTS.md，Gemini 读 gemini.md。改一处，其他地方不会自动更新。我在 Claude Code 里踩过的坑，Codex 不知道。时间一长，各工具对我的"理解"开始分裂。
