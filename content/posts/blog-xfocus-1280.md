---
title: "又见后门"
date: 2005-09-12T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1280"
---

前些天一位朋友的 Linux 主机上说有个莫名其妙的 inetd 进程，开了 21000 端口，让我看看。
简单检查了一下，发现是个用 perl 脚本写的后门，叫 [Telnet-like Standard Daemon](http://blog.xfocus.net/resserver.php?blogId=1&resource=tlsd.txt)，但实际上是这个骇客不留神把后门给搁临时目录下，才知道是它。

它的麻烦在于两个地方：

1、“$0”被设置为一个虚假的名称：

my $PROC        = "inetd";                 # name of the process
$0=$PROC."＼0";

因此在进程中看到进程名是 inetd

2、因为是 perl 脚本后门，在 proc 里面看到的是 perl 的信息。

因此，虽然我们很容易通过 netstat、lsof 看出这个 inetd 和 21000 是后门，但却找不到后门究竟搁在哪个地方，试过用 strace 也无法找出路径。

目前只能用土办法 find / -type f -print |xargs grep -i 'Password Errata!' 来查找文件。可如果骇客用了简单的 lkm，隐藏端口和文件怎么办？

有没有应用层的解决方法？哪位对 perl 比较熟的朋友帮帮忙教我一把吧 :)
