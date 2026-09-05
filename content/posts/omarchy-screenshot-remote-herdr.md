---
title: "从 Omarchy 截图，贴进远程 Mac 上的 herdr"
date: 2026-09-05T19:25:25+08:00
lastmod: 2026-09-05T19:25:25+08:00
author: "Luca"
tags: ["Tech","Tools","AI"]
draft: false
slug: "omarchy-screenshot-remote-herdr"
---

## 问题

我的日常是：坐在 Linux（Omarchy）前面，ssh 到 Mac，在 Mac 上跑 herdr，里面开 Claude Code / Codex。

在 Linux 上截图，想贴给 agent 看，贴不过去。没有报错，没有 `[Image #1]`，什么都没发生。

## 原因

SSH 只传文字。截图在 Linux 的剪贴板里，Mac 根本看不到。

`ssh mac` 之后再运行 `herdr`，herdr 整个跑在 Mac 上。它读的是 Mac 的剪贴板，不是我面前这台机器的。

这不是 Omarchy 的问题，也不是 herdr 的 bug。是架构决定的。

## 解法：反过来跑

在 Linux 上也装一个 herdr，用它作为客户端去连 Mac：

```
herdr --remote username@host
```

这样 herdr 客户端在 Linux 上运行，UI 从 Mac 那边流过来。剪贴板在本地，所以图片可以桥接过去：按 Ctrl+V，herdr 把 PNG 通过 SSH 传到 Mac，再把 Mac 上的文件路径贴进 agent 的输入框。agent 读路径就行。

### 谁跑在哪

这样做以后 herdr 两边都有，但分工不一样：

- Mac：herdr 作为宿主。Claude Code、Codex 都在 Mac 上启动、运行、读文件。这才是干活的那个 herdr。
- Linux：herdr 只是一个薄客户端。`herdr --remote username@host` 通过 SSH 连到 Mac，把界面拉回来显示。它多做的一件事是读本机剪贴板，把 PNG 送到 Mac。

agent 和会话都留在 Mac 上。Linux 这一份只是一个窗口，替代原来 `ssh mac` 那个终端。
