---
title: "升级到OSX 10.4.10 后 Finder 崩溃的问题"
date: 2007-07-12T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2763"
---

昨晚开始，总是在右键点击Finder中的文件时，Finder直接崩溃重起，平均点击三到四次会崩溃一回，回忆了一下最近可能导致这类问题的操作：

> 1、升级到最新的 OSX 10.4.10；
> 
> 2、装了个StuffIt
> 11，它往Finder的右键菜单里加了个Stuffit的选项；

于是：

> 1、在terminal下以root权限执行：update_prebinding -root
> / -force
> 
> 2、删除Stuffit，并且删除它在/Library/Contextual Menu
> Items/下的右键菜单项

重起系统后，Finder就恢复正常了。

刚刚Google了一下，看到MacFixit上有一篇文章《[Finder
crashes](http://www.macfixit.com/article.php?story=20070709083529674)》，看来这个问题不止我一个人遇到，可能是10.4.10的问题，MacFixit提出的解决办法是：

> 1、在terminal下以root权限执行：update_prebinding -root
> / -force
> 
> 2、重新安装补丁包（到Apple主站下载）
> 
> 3、删除Finder的.plist文件：~/Library/Preferences下的com.apple.finder.plist和com.apple.sidebarlists.plist
> 
> 
> 4、删除/Library/Contextual Menu Items/和~/Library/Contextual Menu
> Items/目录下的第三方右键菜单项
> 
> 5、检查字体是否有损坏，清空字体缓存，包括以下几个目录：~/Library/Fonts、/Library/Fonts、/System/Library/Fonts
> 
> 
> 6、检查自启动目录/Library/StartupItems里面是否有可能导致问题的项目
