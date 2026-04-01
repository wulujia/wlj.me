---
title: "VS Code Commit 中文名乱码"
date: 2024-01-01T00:00:00+08:00
tags: ["Tips"]
draft: false
slug: "vs-code-commit-zhong-wen-ming-luan-ma"
---

Mac 和 Linux 下用 VS Code，中文文件名在 Commit 到 Github 时会乱码。解决方法：

```
git config --global core.quotepath false
```
