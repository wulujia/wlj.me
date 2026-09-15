---
title: "Omarchy 用户常用的 mise 命令"
date: 2026-09-15T10:15:03+08:00
lastmod: 2026-09-15T10:15:03+08:00
author: "Luca"
tags: ["Tools","Tech"]
draft: false
slug: "20260915-mise-for-ordinary-users"
---

`mise` 来自法语 “mise en place”，意思是把东西准备妥当。厨师开工前备好食材，`mise` 则在进入项目时备好正确版本的 Node.js、Python、Go 等工具，以及环境变量和任务。

它解决的问题很直接：不同项目需要不同版本；换电脑后，开发环境很难重新配齐；`nvm`、`pyenv`、`rbenv` 各管一摊。项目把配置写进 `mise.toml`，`mise` 会按目录自动切换。

普通用户常用这些命令：

```bash
mise ls                    # 查看已安装及当前使用的工具
mise use node@22           # 给当前项目安装并指定 Node.js 22
mise use -g node@22        # 设置全局默认版本
mise install               # 安装项目声明的全部工具
mise outdated              # 查看哪些工具可以升级
mise up                    # 升级 mise 管理的工具
mise run test              # 运行 mise.toml 里的 test 任务
mise doctor                # 检查配置和环境问题
```

临时用某个版本运行命令，可以写：

```bash
mise x node@22 -- node app.js
```

在 Omarchy 里，更新所有 `mise` 工具还可以用：

```bash
omarchy update mise
```

进入一个配置好 `mise.toml` 的项目，通常只需运行：

```bash
mise install
mise run test
```
