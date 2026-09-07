---
title: "Linux下方便的备份工具"
date: 2006-08-13T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2003"
---

服务器上重要数据越来越多了，不做个备份，睡觉也不踏实。以前用过rsync做过服务器同步，但现在想想，需要的功能很简单：

1、能通过配置文件方便地指定目录打包、压缩后统一存放到指定目录下；

2、能够配置保留几份备份文件；

3、可以创建md5校验值；

4、必要的时候，可以将文件通过ftp或者ssh上传到其它服务器保存；

翻了一堆开源软件，找到了[backup-manager](http://www.backup-manager.org/)，非常合用。另外找到一款用于对压缩包进行管理的[atool](http://www.nongnu.org/atool/)，用perl写的脚本，很简单实用。

顺手将它们记在wiki上了，感兴趣的朋友可以看[backup-manager wiki](http://wiki.xfocus.net/cgi-bin/moin.cgi/backup-manager)和[atool wiki](http://wiki.xfocus.net/cgi-bin/moin.cgi/atool)，也欢迎对[XFOCUS的维基百科](http://wiki.xfocus.net/)进行编辑 :)
