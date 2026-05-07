---
title: "Recordly：开源的桌面录屏 + 编辑器"
date: 2026-05-07T12:47:08+08:00
lastmod: 2026-05-07T12:47:08+08:00
author: "Luca"
tags: ["Tools","Video"]
draft: false
slug: "recordly-screen-recorder"
---

看到一个开源的桌面录屏工具 [Recordly](https://github.com/webadderallorg/Recordly)，macOS / Windows / Linux 都能跑。

它把录制和后期合在一个 app 里。录完直接进编辑器，时间轴上做 trim、zoom、变速、注释、额外音轨、裁剪，不再把素材丢进另一个剪辑软件。

## 主要功能

- 自动 zoom 建议、光标平滑、点击反馈
- 把录制内容放进 styled frame：壁纸、渐变、阴影、圆角、留白
- webcam 浮窗，位置可调、可镜像、可加阴影，可设置随 zoom 缩放
- 项目可存为 `.recordly` 文件，之后再打开继续改
- 导出 MP4 或 GIF
- 扩展市场 [marketplace.recordly.dev](https://marketplace.recordly.dev/extensions)

## 平台支持

- macOS 14.0+：用 ScreenCaptureKit 原生捕获
- Windows 10 19041+：用 Windows Graphics Capture + WASAPI 音频
- Linux 现代发行版：Electron 捕获，目前不支持隐藏鼠标

## 项目情况

- 许可证：AGPL 3.0
- 主页：[recordly.dev](https://www.recordly.dev)
- 仓库：[webadderallorg/Recordly](https://github.com/webadderallorg/Recordly)
- 从 [OpenScreen](https://github.com/siddharthvaddem/openscreen) fork 后另起的项目
