---
title: "chroot安装Unrealircd"
date: 2005-06-23T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1003"
---

Blog服务器坏的时间够长的，总算可以写字了 :)
大概还有许多朋友怀念多年前的irc吧，今天装了一个irc server，简单记下几个要点：

1、Unreal好象是把绝对路径写到应用程序里面了，所以我编译的时候指定了ircd在/bin下，配置文件放到/unreal中，起chroot的时候目录结构比较清晰。
2、除了/etc、/lib下的文件外，不要忘记将用到的/dev下的设备文件也创建好。
3、strace、lsof和ldd在帮助定位chroot需要的文件时很有用。

再做些事，该睡了。
