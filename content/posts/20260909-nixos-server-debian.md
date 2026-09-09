---
title: "VPS 从 NixOS 迁出后，我会选 Debian"
date: 2026-09-09T10:27:12+08:00
lastmod: 2026-09-09T10:27:12+08:00
author: "Luca"
tags: ["Tech","Tools"]
draft: false
slug: "20260909-nixos-server-debian"
---

我有一些服务放在虚拟主机上，以前一直跑 NixOS。最近我把 NixOS desktop 都删掉了，服务器上的 NixOS 还在，但我已经不再每天碰它。

NixOS 的配置能进 Git，换机器能重建，升级和回滚也有边界。服务多、机器多、配置经常改时，这一套很有用。

我现在的 VPS 规模不大，服务也相对稳定。上服务器多半是续证书、查日志、升级服务，或者处理故障。NixOS 的配置语言、包版本和模块机制，成了额外一层要记住的东西。

这次我会选 Debian。

Debian stable 的包不会频繁换大版本，安全更新会继续进入。Debian 13 的完整支持到 2028 年，LTS 到 2030 年。[Debian 的发布页](https://www.debian.org/releases/index.en.html) 也把 stable 作为生产环境的推荐版本。

Ubuntu 也可以。某个服务的官方安装文档只覆盖 Ubuntu，或者需要更近的新版本时，我会直接用 Ubuntu。Ubuntu Server 26.04 LTS 的免费安全和维护更新到 2031 年。[官方支持周期在这里](https://ubuntu.com/server)。

Arch 留给桌面。它采用滚动发布，系统要完整升级，部分升级不受支持。[ArchWiki](https://wiki.archlinux.org/title/System_maintenance) 的维护要求，对无人盯着的 VPS 不合适。

我会新开一台 Debian 13 虚拟主机迁服务，不在旧机上硬改发行版。服务配置放 Docker Compose，数据做异机备份；新机先恢复和验证，再切域名。旧 NixOS 机器留到恢复流程跑通后再下线。

先从最简单的一台开始。
