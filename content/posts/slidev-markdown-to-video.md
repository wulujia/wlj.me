---
title: "用 Slidev 做视频的方案"
date: 2026-04-21T07:11:35+08:00
tags: ["slidev","video"]
draft: false
slug: "slidev-markdown-to-video"
---

方军发了一段文字：

> 内容用 markdown；画面用 slidev 制作，可以加兼容 vue 的网页效果；音频写在 slidev 的 speaker note 里，然后转成音频；slidev 自动播放，由音频往前推动，形成视频的感觉；录制视频用 obs（在 slidev 里写了 addon，一键驱动）。

我没完全看懂，问了 Claude 搞清楚了。

Slidev 原生提供：Markdown 写幻灯片、speaker notes（HTML 注释 `<!-- -->`）、Vue 组件、键盘翻页、演讲者模式。

需要自己写的三块：

1. **TTS**：解析 `slides.md`，把每页 notes 转成 `audio/slide-N.mp3`
2. **音频驱动翻页**：Vue 组件监听当前页，播对应 mp3，`audio.ended` 后调 `nav.next()`
3. **OBS 录制**：OBS 28+ 内置 WebSocket，浏览器直接连 `ws://localhost:4455` 就能控制 `StartRecord` / `StopRecord`
