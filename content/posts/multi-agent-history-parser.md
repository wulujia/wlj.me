---
title: "让每个 AI 助手的对话都进我的记忆系统"
date: 2026-04-21T06:56:53+08:00
tags: ["Tech","AI","Tools","Claude"]
draft: false
slug: "multi-agent-history-parser"
---

我维护着一个叫 `context` 的个人上下文系统：一份中心 markdown，分发到 Claude Code、Codex CLI、Gemini CLI、OpenClaw 的配置路径里，保证同一个"我"在各个工具之间一致。

这个系统每天自动扫当天的对话，把我说过的偏好、决策、踩坑提炼到 `OBSERVATIONS.md`。问题是——它只懂 Claude Code 一家的 JSONL 格式。我同时还在用 Codex、Gemini、OpenCode，这些对话历史全都被扔在一边。

每家 AI 助手的对话都存在本地，但格式各家不同。Claude 用 JSONL，Codex 也用 JSONL 但 schema 不一样；Gemini 用整块 JSON；OpenCode 用 SQLite，message 和 part 分两张表；Cline 和 Cursor 藏在 VSCode 扩展的 globalStorage 里；Aider 干脆写在项目目录的 markdown 里。

自己从零逆向这些格式，不是我想干的活。

在 GitHub 上撞见 `jhlee0409/claude-code-history-viewer`，简称 CCHV。本意是个桌面历史查看器——七家 AI 助手的对话在一个界面里翻。我对桌面 app 本身不感兴趣，但它的 Rust 源码里有一个 `providers/` 目录：七个文件，每家一个解析模块。每家的存储路径它替我找好了，每种格式的 schema 它替我逆向完了。

让 AI 把这部分代码翻成 Python，挪进 context 项目。
