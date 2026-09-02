---
title: "怎么给 Omarchy 提 PR"
date: 2026-09-02T20:55:28+08:00
lastmod: 2026-09-02T20:55:28+08:00
author: "Luca"
tags: ["Tools","Ops"]
draft: false
slug: "contribute-to-omarchy"
---

## 太长不看

Omarchy 装机自带一份给 AI 助手看的贡献指南，在仓库的 `default/agents/skills/omarchy/contributing.md`。跟 Claude 说"帮我给 Omarchy 报个 bug"，或者"把这个修法提成 PR"，它会读这份文件，自己走完收日志、截图、fork、跑测试、开 PR 的全过程。

下面是它照做的规矩，自己动手也一样。

## 去哪提

[Omarchy](https://omarchy.org/) 的代码在 [omacom/omarchy](https://github.com/omacom/omarchy)。issue 只收确认过的 bug，模板第一行写着 "an open source gift, not a product you bought from a vendor"。功能建议去 Discussions 的 Suggestions 分类，手册修改去 Manual 分类，不确定是不是 bug 去 [Discord](https://omarchy.org/discord)。求助发到 Issues 会被关掉。

## 规矩

它没有 `CONTRIBUTING.md`，代码规范在根目录的 [`AGENTS.md`](https://github.com/omacom/omarchy/blob/master/AGENTS.md)：命令一律 `omarchy-` 开头，bash 字符串判断用 `[[ ]]`、数字用 `(( ))`，缩进两空格，shebang 只能 `#!/bin/bash`。不合规会被打回。

## 动手

报 bug 带上这两条的输出，日志可传到 logs.omarchy.org，24 小时过期：

```bash
omarchy version
omarchy debug --no-sudo --print
```

指南点名要截图，用 `omarchy capture screenshot`，只能在网页上拖进去。

提 PR 别在 `/usr/share/omarchy/` 里改，那是包管理目录，更新时全覆盖：

```bash
gh repo fork omacom/omarchy --clone
cd omarchy
./test/all
gh pr create
```

修视觉问题的 PR 要附前后对比截图。

## 什么会被合并

2026 年 9 月初：开着的 PR 1503 个，合并 1174 个，关掉没合并 1710 个。合进去的外部 PR 是 SSH 登录加固、主题名注入防护、`.desktop` 文件转义这类，具体、小、多数是安全和 bug 修复。
