---
title: '用 Claude Code History Viewer 翻自己的 AI 对话记录'
date: 2026-04-19T21:40:22+08:00
tags: ["Tools","AI","Claude"]
draft: false
slug: "claude-code-history-viewer"
---

同事问我平时怎么和 AI 沟通的，想看我的会话。于是推荐我用这个小工具——[Claude Code History Viewer](https://github.com/jhlee0409/claude-code-history-viewer)，把 Claude Code 本地 `~/.claude/projects/` 里的 JSONL 会话记录翻出来看。

![截图](/images/claude-code-history-viewer-1.png)

左边项目和会话列表，右边完整对话，Thoughts、工具调用、Token 消耗都展开。支持全文搜索，100% 本地运行。

macOS 一行装：

```bash
brew install --cask jhlee0409/tap/claude-code-history-viewer
```

Windows 和 Linux 去 [Releases](https://github.com/jhlee0409/claude-code-history-viewer/releases) 下载。打开自动扫描，不用配置。
