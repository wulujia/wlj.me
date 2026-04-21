---
title: "herdr 是干什么的"
date: 2026-04-22T06:55:15+08:00
tags: ["AI","Tools"]
draft: false
slug: "20260422-herdr-ai-agent-workspace"
---

[herdr](https://github.com/ogulcancelik/herdr) 是一个给 AI coding agent 用的终端工作区管理器。

它自己也有 `workspace`、`tab`、`pane`，能分屏、切换、恢复 session。只看这一层，它很像 `tmux`。

它和 `tmux` 的区别，在另一层。

`tmux` 管的是终端会话。`herdr` 除了管会话，还会识别 pane 里跑的是不是 agent，再把状态标出来。README 里列出的状态有四类：`working`、`blocked`、`done`、`idle`。

比如同时开几个 pane：

- 一个 pane 跑 `Claude Code`
- 一个 pane 跑 `Codex`
- 一个 pane 跑开发服务器
- 一个 pane 看日志

`tmux` 可以把这些 pane 摆好，也可以后台挂着。`herdr` 额外做的是：识别哪个 pane 里在跑 agent，哪个 agent 在忙，哪个在等输入，哪个已经停下来。

它判断状态主要靠两种方式。

第一种，看前台进程和终端输出。

第二种，接工具自己的 hook 或 plugin。文档里已经写明支持给 `Claude Code`、`Codex`、`pi`、`OpenCode` 装集成，这样状态报告会更直接。

除了给人看，`herdr` 还有本地 socket API。agent 自己也可以调用这些接口，比如：

- 新开 workspace
- 新开 tab
- 分一个 pane
- 读另一个 pane 的输出
- 往另一个 pane 发命令
- 等另一个 agent 完成

所以它不只是“把几个终端摆在一起”，还多了一层对 agent 的状态管理和控制。

这个工具更适合这样的场景：

- 已经在终端里工作
- 已经开始同时跑多个 agent
- 需要知道哪个 agent 卡住了，哪个做完了

如果平时只开一个 agent，加几个普通 shell，`tmux` 一般就够了。

截至 2026-04-22，`herdr` 最新 release 是 `v0.5.0`，支持 macOS 和 Linux，README 里列出的已测试工具包括 `Claude Code`、`Codex`、`pi`、`OpenCode`、`amp`、`droid`。
