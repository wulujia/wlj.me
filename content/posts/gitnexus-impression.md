---
title: "GitNexus 这类工具，大概率不需要"
date: 2026-05-01T07:12:55+08:00
tags: ["AI","Tools"]
draft: false
slug: "gitnexus-impression"
---

看了一下 [GitNexus](https://github.com/abhigyanpatwari/GitNexus)，一个把代码仓库索引成知识图谱、再通过 MCP 喂给 Claude Code / Cursor / Codex 的工具。

它解决的是一个具体的人的具体问题：写大型项目的工程师，让 AI 帮忙改代码时，经常遇到 AI 改了 A 函数、没注意到 B、C、D 也调用它。一次小改动，跑起来三处崩。

为什么会这样？AI 不是不会读代码，是不知道该读哪些。Context window 再大，AI 自己也不会主动把整个仓库塞进去，成本太高。grep 能找调用方，但要 AI 自己想到去 grep，还得来回跑好几轮。调用链一深，就漏。

GitNexus 的做法是预先把每个函数、每条依赖、每条调用链都建好图。AI 要改一个函数，先查图：谁调用我、我调用谁、改了会炸到哪里。一次查询出结果，不用反复读文件。

但我的判断是，大多数人不需要装这类工具。

过去半年 Claude Code、Cursor、Codex 这批 AI coding 工具进步得很快。grep、glob、Read 这些基础工具调度得很熟，subagent 可以预先装"探索代码"的 SOP，写好一份 CLAUDE.md 把架构地图、关键模块、依赖关系交代清楚，AI 漏改调用方的事故已经少了很多。原本 GitNexus 想解决的痛，AI 工具自己在解决。

什么时候才值得试？我的顺序是这样：

先调 AI 工具本身。CLAUDE.md 写清楚架构地图、关键模块、依赖关系，subagent 装好探索代码的 SOP，每次改代码前要求 AI 先列出受影响的调用方。这些都是免费的，先做。

做完还在频繁踩坑，再考虑 GitNexus 这类工具。频繁是多频繁？一周两三次都不够，得是改代码的过程里反复出事故、CLAUDE.md 怎么写都救不回来，才值得多装一个工具。

大多数人不会走到这一步。痛感真到那个程度，往往不是 AI 工具的问题，是项目本身的复杂度已经超出了人脑+AI 配合的舒适区。那时候装 GitNexus 也只是缓解，不是根治。

所以结论很简单：先把手上的 AI coding 工具用透，再去看新工具。
