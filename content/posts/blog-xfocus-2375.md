---
title: "UPX压缩时可能会导致资源图标丢失的解决方法"
date: 2007-01-01T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2375"
---

UPX是一款绝佳的压缩软件，通常用于发布软件前的压缩，可以让生成的软件更小。

昨天在用UPX压缩[X影音2.1.6](http://www.secyou.cn/viewthread.php?tid=2390&extra=page%3D1)时，却意外地发现，压缩完毕后，内置的资源图标就没掉了，一时有些发蒙。

刚刚看了看参数，原来UPX有个--compress-icons=0的参数，表示不压缩图标，所以，这个版本[X影音绿色版](http://www.secyou.cn/viewthread.php?tid=2430&extra=page%3D1)，就用了：

> upx XPlayer.exe -k --compress-icons=0
