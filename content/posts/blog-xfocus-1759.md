---
title: "推荐开源软件 2：runasadmin"
date: 2006-04-01T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1759"
---

这个工具实际上是用自己的一个 shell 替代了 windows 系统中默认的 explorer 并且限制我们在该 shell 中的用户权限，这在目前险恶的计算机网络环境中极有意义！

安装 [runasadmin](http://runasadmin.sourceforge.net/) 后，我们默认所有的程序都是以普通的 User 权限打开，也就是说，这时我们基本不用害怕诸如 office 溢出、qq 溢出、图片溢出等听来极其吓人的客户端漏洞——因为默认情况下我们都是以低权限用户运行和察看这些程序/文件。

它也可以根据用户的需求以某一权限（如超级用户权限，或是完全不受信任的最低权限等）来执行程序：

![](https://web.archive.org/web/20071014204648im_/http://blog.xfocus.net/resserver.php?blogId=1&resource=runasadmin.jpg)

目前美中不足的是，点击“开始->关机”时，只有“注销”而没有“关机”了，因为普通用户没有关闭系统的权限 !@#$%^

我只好用 Ctrl+Alt+Del 键呼出登陆界面，点击上边的“关机”按钮。当然，也可以用 shutdown 或才 [pstools](http://www.sysinternals.com/Utilities/PsTools.html) 里面的 psshutdown -l 命令。
