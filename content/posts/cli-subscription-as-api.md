---
title: "把 CLI 订阅变成 API"
date: 2026-04-20T10:22:22+08:00
tags: ["AI","Tools"]
draft: false
slug: "cli-subscription-as-api"
---

[CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) 是一个 Go 写的本地代理服务器。它把 Gemini CLI、OpenAI Codex、Claude Code 这些需要 OAuth 登录的 CLI 工具，包装成 OpenAI / Gemini / Claude / Codex 兼容的 API 端点。

装上之后，Raycast、IDE 插件、自己写的脚本都能当成标准 API 来调用，不必再走官方 CLI。支持流式和非流式响应、函数调用、多模态输入、多账号轮询负载均衡，也能把 OpenRouter 这类上游 OpenAI 兼容服务接进来。配套有 Go SDK 和管理 API。

这类工具踩在各家 TOS 的灰线上。OpenAI 和 Anthropic 都明确禁止把订阅席位用作 API 式访问或转售，多账号池化、高频率轮询、不像真人的行为画像都是风控识别的信号。最近 Claude Code 订阅号被封得比较多，原因是拿订阅额度对外跑 API 流量。Gemini 相对宽松，AI Studio Build 大规模轮询也在收紧。自用一两个号本地接客户端风险不大，池化多号对外服务就是另一回事。

项目的赞助商里挂了六七家 API 中转服务商，都是做 Claude Code / Codex / Gemini 官方渠道代理的。
