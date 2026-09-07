---
title: "阻止软件包在Debian下升级"
date: 2004-05-20T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-41"
---

图新鲜，用了debian的unstable，结果fcitx的2.0.2-1版本似乎有问题，和firefox、gaim的配合总是会出错，只好装回2.0.1的。 
为了让fcitx在后续的upgrade中不升级，需要这么一条命令： 
risker:/home/aa# echo fcitx hold|dpkg --set-selections 
今后希望fcitx升级的时候，则可以简单用这么一条命令恢复： 
risker:/home/aa# echo fcitx install|dpkg --set-selections 
设置了hold后，upgrade的情况如下：

risker:/home/aa# apt-get upgrade 
正在读取软件包列表... 完成 
正在分析软件包的依赖关系树... 完成 
下列的软件包的版本将保持持不变： 
fcitx (2.0.1-2 => 2.0.2-1) 
共升级了 0 个软件包，新安装了 0 个软件包，要卸载 0 个软件包，有 1 个软件未被升级。
