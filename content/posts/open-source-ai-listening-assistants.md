---
title: "Hedy 不开源，有哪些开源 AI 听课助手？"
date: 2026-08-09T09:24:25+08:00
lastmod: 2026-08-09T09:24:25+08:00
author: "Luca"
tags: ["AI","Tools","Education"]
draft: false
slug: "open-source-ai-listening-assistants"
---

需求很明确。

工具要在 Mac 上同时听到电脑声音和麦克风，边听边显示逐字稿。讲师提到新概念、数字或者值得怀疑的判断时，AI 能主动补充解释、联网查证、提出反例，也能结合提前提供的个人资料给出提示。课程结束后，再把录音、逐字稿和笔记存下来。

重点放在课程进行中的实时提示：AI 跟着一起听，及时提醒哪里值得多想一步。会后转写和总结工具不在这次比较范围内。

Hedy 已经覆盖实时转写和自动建议等主要功能，但它是商业闭源产品。本文把它作为参照，再检查三个开源项目：Raven、Anarlog 和 Meetily。

以下信息截至 2026 年 8 月 8 日，来自产品官网、文档和公开源码。本文没有一小时中文课程的实测数据，无法比较实时识别准确率和延迟。

## Hedy：商业闭源的参照

[Hedy](https://www.hedy.bot/) 能实时转写谈话，根据不同场景给出自动建议，还提供面向学生的课程模式。用户可以配置 Session Context，让 AI 预先知道个人背景、目标和词汇。

它的免费版每月 5 小时，每次 Session 的实时建议只覆盖前 30 分钟。Pro 版月付 12.99 美元，年付 99.99 美元，还有 299 美元的终身版。

Hedy 没有开放客户端源码。[使用条款](https://www.hedy.bot/terms-of-use/)把软件、算法和设计列为公司专有资产，并明确禁止反编译、反汇编和尝试推导源码。

Hedy 提供 REST API 和 Webhook，但它们主要用于把 Session 结果接到其他工具。[官方集成文档](https://www.hedy.bot/integrations/)列出的实时事件包括 `suggestion.created`，可以收到 Hedy 已经生成的建议；包含完整逐字稿的 `session.ended` 在 Session 结束后触发。官方集成文档未列出可供外部程序消费的实时逐字稿流，也没有说明自动建议会在课程中联网查证。

Hedy 可以直接用来验证自动提示是否有用。它没有开放源码，无法在客户端基础上继续改造。

## Raven：已有会中 AI 悬浮层

[Raven](https://github.com/Laxcorp-Research/project-raven) 使用 MIT 许可证，支持 macOS 和 Windows。它同时采集系统音频和麦克风，在本机完成回声消除，再把两路音频分别交给 Deepgram 实时转写。

它已经具备多项相关功能：

- 实时显示双方逐字稿，支持中文
- 始终置顶的悬浮层，不会出现在 Zoom、Meet、Teams 和 Discord 的屏幕共享里
- Learning 模式，可以设置专门的系统提示
- 可以上传 PDF、Word、Markdown 和纯文本，本地建立索引，在回答时引用
- 可以把屏幕截图和当前逐字稿一起发给 Claude 或 GPT

Raven 的 AI 需要手动触发。用户点击 Assist、What should I say、Follow-up、Recap，或者自己输入问题，AI 才会读取当前逐字稿并回答。截至本文检查的版本，公开源码里未见定时分析逐字稿、自动生成提示卡的程序，也未见 Web Search 工具。

开源版需要自己提供 Deepgram 和 Anthropic 或 OpenAI 的 API Key。Raven 为麦克风和系统音频各开一条 Deepgram 连接。按 [Deepgram 当前按量付费的限时流式价格](https://deepgram.com/pricing)，并假设两条连接连续运行一小时，Nova-3 单语转写约 0.58 美元，多语模式约 0.70 美元。这是按公开单价做的推算，不包含大模型费用。

要做一个 Hedy 风格的开源版本，本文检查的 Raven 公开版未见自动触发和带来源的网页查证。它已经实现双路音频、实时逐字稿、悬浮层和本地文档检索。

## Anarlog：本地模型和本地存储

[Anarlog](https://github.com/fastrepl/anarlog) 也是 MIT 许可证，前身叫 Hyprnote，是一个开源的 Granola 替代品。它可以录制系统音频和麦克风，把会议资料保存在本地 SQLite 数据库，支持导出 Markdown。

在 Apple Silicon Mac 上，Anarlog 可以下载本地转写模型。摘要和聊天可以连接 Ollama 或 LM Studio，因此录音、转写、总结和问答都能留在自己的电脑上。能否在会议中显示实时文字，取决于选择的模型，设置中标为 Live 的模型才支持。

Anarlog 的聊天已经能读取当前和历史会议，也有 Web Search 工具。不过[公开源码里的 Web Search](https://github.com/fastrepl/anarlog/blob/main/apps/desktop/src/chat/tools/web-search.ts)要求用户登录，再调用 Anarlog 的 `/research/search` 服务。这项网页搜索依赖网络和 Anarlog 官方服务。

官方文档主要围绕录音、备忘、逐字稿、总结和会后聊天，未列出会议中主动生成建议的功能。改造成实时听课助手，还要增加自动触发程序和提示卡界面。

## Meetily：本地转写和会后总结

[Meetily](https://github.com/Zackriya-Solutions/meetily) 使用 MIT 许可证，主体是 Tauri、Rust 和 Next.js。它能同时录制系统音频和麦克风，使用本地 Whisper 或 Parakeet 实时转写，并用 Ollama、Claude、Groq、OpenRouter 或兼容 OpenAI 的接口生成总结。

Meetily 的录音、模型、逐字稿和总结都可以保存在本机。使用 Ollama 时，总结也能在本机完成；选择 Claude、Groq 或 OpenRouter 时，生成总结所需的文本会发送给相应服务。macOS 已经提供 Apple Silicon 安装包，不需要自己编译整个项目。

它的官方 README 和架构文档没有列出会议中的 AI 对话、个人资料检索、自动建议或者网页搜索。公开架构只把大模型列在 Summary Engine 中，未列出会中 AI 交互。

Meetily 已经覆盖本地录音、实时文字和会后总结。要做会中实时助手，需要另外加入 AI 交互层。

## 放在一起比较

| 项目 | 许可证 | 系统音频 | 实时逐字稿 | 会议中 AI | 自动建议 | 网页搜索 | 本地转写 | 额外上下文 |
|---|---|---|---|---|---|---|---|---|
| Hedy | 闭源 | 支持 | 支持 | 支持 | 支持 | 未见会中查证 | 官方称支持设备端识别 | Session Context |
| Raven | MIT | 支持 | 支持 | 手动触发 | 公开版未见 | 公开版未见 | 使用 Deepgram | 本地文档检索 |
| Anarlog | MIT | 支持 | 取决于模型 | 支持聊天 | 文档未列出 | 依赖官方服务 | Apple Silicon 支持 | 当前及历史会议 |
| Meetily | MIT | 支持 | 支持 | 文档未列出会中 AI | 文档未列出 | 文档未列出 | Whisper、Parakeet | 文档未列出 |

Hedy 可以直接试自动提示，但不开源，每次免费实时建议限 30 分钟。Raven 已有双路音频、实时转写、会中手动 AI、悬浮层和文档检索，本文检查的公开版未见自动触发与网页查证。Anarlog 支持本地转写、本地模型和本地存储，还要补实时提示交互。Meetily 覆盖本地录音、实时文字和会后总结，公开资料未列出会中 AI。

按功能缺口看，Raven 是更直接的改造起点。不过本文没有中文课程实测和开发量评估，还不能判断哪条路线的总成本最低。准确率、延迟、提示频率和干扰程度也都没有实测数据。

## 资料来源

- [Hedy Pricing](https://www.hedy.bot/pricing/)
- [Hedy Features](https://www.hedy.bot/features/)
- [Hedy Terms of Use](https://www.hedy.bot/terms-of-use/)
- [Hedy Integrations](https://www.hedy.bot/integrations/)
- [Raven GitHub](https://github.com/Laxcorp-Research/project-raven)
- [Raven Documentation](https://docs.useraven.ai/)
- [Anarlog GitHub](https://github.com/fastrepl/anarlog)
- [Anarlog Documentation](https://docs.anarlog.so/)
- [Meetily GitHub](https://github.com/Zackriya-Solutions/meetily)
- [Deepgram Pricing](https://deepgram.com/pricing)
