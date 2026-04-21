---
title: "我看懂 herdr 了"
date: 2026-04-22T06:55:15+08:00
tags: ["AI","Tools"]
draft: false
slug: "20260422-herdr-ai-agent-workspace"
---

我一开始把 [herdr](https://github.com/ogulcancelik/herdr) 看成另一个 `tmux`。

让 AI 把它的 README、集成文档和 socket API 读了一遍后，我才发现自己看岔了。它当然也能分屏，也有 `workspace`、`tab`、`pane`，但它盯的不是“终端怎么摆”，它盯的是“pane 里的 agent 现在是什么状态”。

这个差别很小，也很大。

我平时如果只开一个 `Codex` 或 `Claude Code`，再加一个 server，一个日志窗口，`tmux` 完全够用。可一旦同时开两三个 agent，事情就变了。一个在写功能，一个在修测试，一个可能停在授权提示上。`tmux` 很会把窗口摆好，也很会后台挂着，但它不知道哪个 agent 在等我，哪个已经做完。

`herdr` 补的就是这层。

它会识别 pane 里跑的是不是 agent，再把状态标出来：`working`、`blocked`、`done`、`idle`。有些工具如果支持 hook 或 plugin，它还可以直接接状态，不只靠猜。这样一来，我扫一眼侧边栏，就知道该切去哪个 pane。

我看到这里，才算明白它在解决谁的问题。

它不是给“想学终端”的人准备的，也不是给“只跑一个 agent”的人准备的。它是给已经在终端里工作、而且开始并行跑多个 agent 的人准备的。痛点不是 pane 不够，痛点是注意力不够。

还有一点我之前没想到：它不只给人看，也给 agent 用。agent 自己可以新开 pane、读别的 pane 输出、往别的 pane 发命令、等另一个 agent 做完。看到这里，我就不太想把它叫“分屏工具”了，更像一个终端里的多 agent 监督台。

所以我现在对它的理解很简单：

如果我平时就一个 agent，`tmux` 足够了。

如果我屏幕上常年挂着两三个以上 agent，`herdr` 这种东西，我就会一下看懂。

截至 2026-04-22，`herdr` 最新 release 是 `v0.5.0`，支持 macOS 和 Linux，已测试的工具包括 `Claude Code`、`Codex`、`pi`、`OpenCode`、`amp`、`droid`。
