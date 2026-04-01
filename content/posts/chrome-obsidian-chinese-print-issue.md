---
title: "Chrome / Obsidian 打印时不显示中文问题"
date: 2025-01-01T00:00:00+08:00
tags: ["mac", "Chrome", "Obsidian"]
draft: false
slug: "chrome-obsidian-chinese-print-issue"
---

Chrome 及 Obsidian 在打印或"另存为 PDF"时，中文内容显示为方框（或完全消失），而 Safari 浏览器不受影响。这个问题主要出现在 macOS 15 Sequoia。原因是 macOS 15 Sequoia 系统字体架构变更。

Apple 在 macOS 15 中将"苹方 (PingFang)"字体改为使用新的 `hvgl` 格式，而 Chromium 内核（Chrome、Obsidian 等应用使用）的 PDF 渲染引擎无法正确处理这种新格式，导致打印时中文字符丢失。Safari 不受影响是因为它使用 Apple 自家的 WebKit 引擎。

最有效的方法是通过"字体册"重新下载标准格式的苹方字体：

1. 打开"系统设置" > "语言与地区"
2. 将"English"拖到"简体中文"之上（选择不重启）
3. 打开"字体册"应用，搜索"苹方"或"PingFang"
4. 点击下载所有苹方字体（会从灰色变为黑色）
5. 恢复语言设置（简体中文拖回顶部）
6. 重启 Chrome 和 Obsidian

![Font screenshot](https://phaven-prod.s3.amazonaws.com/files/image_part/asset/3378702/HujZbsImcywPTtHZkpdJjoirDVs/medium_font.png)
