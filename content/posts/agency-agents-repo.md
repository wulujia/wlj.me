---
title: "一个覆盖中文互联网的 AI Agent 人格库"
date: 2026-04-20T11:32:47+08:00
tags: ["AI","Tools"]
draft: false
slug: "agency-agents-repo"
---

GitHub 上有个项目叫 agency-agents（https://github.com/msitarzewski/agency-agents），184 个 AI agent 人格档案，分二十多个部门：工程、设计、营销、销售、财务、产品、项目管理、测试、支持、空间计算。每个档案是一个 markdown，写清楚这个 agent 的身份、工作流、交付物和成功指标。一行命令可以装到 Claude Code、Copilot、Cursor、Gemini CLI、Aider、Windsurf、Kimi Code 等十来个工具里。

同类项目不少，大多是"程序员的 Claude Code subagent 合集"。agency-agents 的不一样在两点。

一是跨工具。一套档案通过 `scripts/convert.sh` 生成适配各家工具的格式，不绑死在 Claude Code。这是硬工程活，大多数对手不做。

二是真的把中文互联网生态当作一级公民来写。小红书、公众号、抖音、知乎、B站、百度、微博、快手、私域（企微）、直播电商、淘系拼多多、跨境电商，还有小程序开发、飞书开发——每个平台一个专属档案。英文圈的 agent 仓库基本不碰这块。

让 AI 抽读了一遍中文生态的 13 个档案，质量良莠不齐。对这个项目的态度也简单：别整包用，挑着用。
