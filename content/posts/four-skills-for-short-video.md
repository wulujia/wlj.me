---
title: '给做短视频产品的同事：先看这四个 Skill'
date: 2026-04-19T21:51:59+08:00
tags: ["AI","Claude","Video"]
draft: false
slug: "four-skills-for-short-video"
---

同事 liurong 想做短视频产品，让我给点建议。我的建议是先把下面四个 Claude Code Skill 过一遍。两个帮你做产品，两个做视频本身。

## 做产品的两个

### superpowers — [obra/superpowers](https://github.com/obra/superpowers)

一套软件开发方法论。装上之后 Claude Code 不会直接写代码，会先和你对齐需求、出 spec、等你确认，然后出实现计划，再派 subagent 一个任务一个任务做，过程里走 TDD、守 YAGNI 和 DRY。

作者 Jesse（obra）是 Anthropic 工程师，已进入官方 plugin marketplace：

```bash
/plugin install superpowers@claude-plugins-official
```

### gstack — [garrytan/gstack](https://github.com/garrytan/gstack)

YC 总裁 Garry Tan 的个人工具包。把 Claude Code 拆成 23 个角色：CEO、eng manager、designer、code reviewer、QA、security officer、release engineer 等，每个都是 slash command。

和做产品相关的几个：

- `/office-hours`：YC 式产品拷问，六个问题
- `/plan-ceo-review`：以 CEO 视角审视功能
- `/design-review`、`/qa`：设计和质量检查
- `/review`、`/ship`：代码审查和发布

起手可以先跑一次 `/office-hours`，描述你的短视频产品。

## 做视频的两个

### hyperframes — [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)

HeyGen 开源的视频渲染框架：Composition 是 HTML 文件，动画用 GSAP，渲染成 MP4。专为 AI agent 设计，agent 直接写 HTML，不需要学专有 DSL。

装上后可以这样提需求：

> 用 /hyperframes 做一个 10 秒产品片头，标题淡入，背景视频，背景音乐。

适合批量生产模板化视频。

### video-use — [browser-use/video-use](https://github.com/browser-use/video-use)

browser-use 团队出的剪辑工具。把原始素材放进文件夹，在 Claude Code 里说"剪成发布视频"，得到 `final.mp4`。

它会做的事：

- 剪掉口癖（umm、uh）和 take 之间的空白
- 自动调色
- 每个切口 30ms 音频淡入淡出
- 烧字幕（默认两词一段大写）
- 用 Manim / Remotion / PIL 生成动画叠层
- 渲完自检每个切口

原理：LLM 不看视频，只读转录后的词级时间戳文本（约 12KB）。和 browser-use 给 LLM 读 DOM 而不是看截图是同一思路。

适合要给用户做长视频剪辑、精华片段的产品。

## 小结

- **做产品阶段**：superpowers 给方法论，gstack 给角色
- **做视频阶段**：hyperframes 做生成，video-use 做剪辑

先把四个 README 过一遍，装上试一下。
