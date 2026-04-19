---
title: '用 Claude Code History Viewer 翻自己的 AI 对话记录'
date: 2026-04-19T21:40:22+08:00
tags: ["Tools","AI","Claude"]
draft: false
slug: "claude-code-history-viewer"
---

同事问我："你平时都是怎么和 AI 沟通的？"他想学我的提问方式，看我怎么一步步把活儿交代清楚。于是推荐我用这个小工具——[Claude Code History Viewer](https://github.com/jhlee0409/claude-code-history-viewer)（CCHV），把 Claude Code 本地的会话记录翻出来看。

装完打开就是下面这样，左边项目和会话列表，右边是完整对话，连 Thoughts、工具调用、Token 消耗都展开呈现。

![截图](/images/claude-code-history-viewer-1.png)

## 它做了什么

Claude Code 的每次会话都会在本地 `~/.claude/projects/` 下存一份 JSONL，平时这些文件躺在那没人翻。CCHV 的作用就是给这些 JSONL 做一个漂亮的阅读器：

- 按项目、会话浏览历史对话
- 全文搜索，跨项目、跨会话
- Token 统计和成本分析
- 工具调用（Bash、Read、Edit、Grep 等）单独渲染
- 100% 本地运行，不上传任何东西

顺带还支持 Gemini CLI、Codex CLI、Cline、Cursor、Aider、OpenCode——七个 AI 编程助手一个界面看完。

## 怎么装

macOS 一行命令：

```bash
brew install --cask jhlee0409/tap/claude-code-history-viewer
```

Windows 和 Linux 去 [Releases](https://github.com/jhlee0409/claude-code-history-viewer/releases) 下载 `.exe` 或 `.AppImage`。

装完直接打开，它会自动扫描 `~/.claude/projects/`，不用任何配置。

## 怎么用来复盘自己和 AI 的沟通

同事的需求其实挺典型：想看别人怎么写 prompt。但对话记录一条条翻太慢，我的用法是：

1. **挑一个最近做完的项目**，点进去看完整 session
2. **看第一条消息**——我最初是怎么交代任务的，有没有给够上下文
3. **看中间的来回**——哪里我被迫补充说明，说明第一句没说清
4. **看 Thoughts**——Claude 的思考过程能反推出我哪些意图表达得不够明确
5. **看 Token 消耗**——哪些会话特别烧钱，通常是我自己绕了弯路

我把这个工具推给同事的时候说：别光看我的，你也装一个翻自己的，对比一下就知道差在哪。

## 数据隐私

全程离线。所有数据都在本地读，不发任何云端请求。这是它最让我放心的地方——你和 AI 聊的内容，本来就不该再走一次网络。

开源在 GitHub：[jhlee0409/claude-code-history-viewer](https://github.com/jhlee0409/claude-code-history-viewer)
