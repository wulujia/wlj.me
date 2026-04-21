---
title: "herdr 在解决什么问题"
date: 2026-04-22T06:55:15+08:00
tags: ["AI","Tools"]
draft: false
slug: "20260422-herdr-ai-agent-workspace"
---

我让 AI 把 [herdr](https://github.com/ogulcancelik/herdr) 的 README、集成文档和 socket API 读了一遍，才看清它在做什么。

很多人第一眼会把它看成另一个 `tmux`，或者一个新的 AI 编程助手。这样看都不准。

`herdr` 管的是中间这层：**当你同时跑多个 coding agent 时，谁在忙，谁卡住了，谁已经做完，哪个窗口现在该看。**

这个问题，普通终端工具并不管。

举个具体场景。

假设我在一个项目里同时开了四个 pane：

- 一个 pane 跑 `Claude Code` 写功能
- 一个 pane 跑 `Codex` 修测试
- 一个 pane 跑开发服务器
- 一个 pane 看日志

前两个 pane 过一会儿就会分化出不同状态。一个可能在等我授权，一个可能已经写完停在那里，一个还在跑。`tmux` 很擅长把四个 pane 摆好，也很擅长后台挂着、断线重连。但 `tmux` 不知道哪个 pane 里的 agent 正在等人，哪个已经 done。

`herdr` 做的，就是把这层“感知”补上。

它有三块东西。

第一块，还是终端工作区。它也有 `workspace`、`tab`、`pane`，可以分屏、切换、恢复 session。这一层和 `tmux` 很像，所以很多人会先把它看成“agent 版 tmux”。

第二块，是 agent 状态识别。它会看 pane 里的前台进程，也会读终端底部输出，判断这里跑的是不是 `Claude Code`、`Codex`、`OpenCode` 这类工具，再把状态归到四类：`working`、`blocked`、`done`、`idle`。有些工具如果支持 hook 或 plugin，`herdr` 还能直接接它们发出来的状态，不必全靠猜。

第三块，是监督和调度。侧边栏会把所有 workspace 和 agent 的状态列出来，哪个卡住了，哪个刚做完，一眼能看到。它还有本地 socket API，agent 自己也可以调用：新开 pane、读另一个 pane 的输出、往另一个 pane 发命令、等另一个 agent 完成。走到这一步，它更接近一个终端里的 agent 调度台。

所以，`herdr` 真正解决的是谁的问题？

是这些人：

- 已经把主工作流放在终端里，平时用 `Ghostty`、`Neovim`、`tmux`
- 已经不只跑一个 agent，而是两三个、四五个一起跑
- 痛点不在“不会开分屏”，在“分屏开完之后我盯不过来”

这种痛点，说白了是注意力管理。

一个人同时带多个 AI 助手干活，真正稀缺的不是 pane 数量，而是自己的注意力。你不怕 pane 不够，你怕的是漏掉一个授权提示，忘了一个已经跑完的结果，又或者反复切 pane 才知道到底谁还活着。

`herdr` 的作者盯的就是这里。他没有再做一个网页 dashboard，也没有做一个 Electron 壳，坚持把东西留在终端里。官方 README 里写得很直白：它要跑在你现有的终端里，`Ghostty`、`kitty`、`wezterm` 可以，甚至 `tmux` 里面也能跑。

这点很重要。

因为很多“多 agent”产品，一上来就把你从终端拉走，给你一个新的桌面界面。它们当然更好展示状态，但代价是你得换环境。`herdr` 走的是另一条路：环境不换，只把终端里本来没有的那层状态和监督补上。

这也解释了它和 `tmux` 的关系。

`tmux` 管的是终端会话。

`herdr` 管的是终端里的 agent 工作流。

如果我平时只开一个 agent，偶尔再开个 server、跑个测试，`tmux` 已经很好，没有必要切。`herdr` 也不是给所有终端用户准备的，它留给“多 agent 并行”这件事开始变乱的人。

我自己的判断是：真正会对 `herdr` 有感觉的人，屏幕上通常已经不止一个 AI 助手。

截至 2026-04-22，这个项目最新 release 是 `v0.5.0`，支持 macOS 和 Linux，已测试的工具包括 `Claude Code`、`Codex`、`pi`、`OpenCode`、`amp`、`droid`。从它现在的样子看，方向已经很清楚：终端里不缺 pane，缺的是有人替你盯着这些 pane 里的 agent。
