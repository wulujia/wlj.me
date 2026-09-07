---
title: "又装了个debian和nessus"
date: 2007-02-20T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2483"
---

还是年后要用，很久没有折腾过这些东西，居然在配置X的时候卡了一下，花了将近一小时才全部搞好。顺手记录一下：

1、修改/etc/apt/sources.list

> deb http://debian.cn99.com/debian sarge main non-free
> contrib
> 
> deb http://debian.cn99.com/debian testing-proposed-updates main
> contrib non-free
> 
> deb http://debian.cn99.com/debian-security sarge/updates main
> contrib non-free
> 
> deb-src http://debian.cn99.com/debian sarge main non-free
> contrib
> 
> deb-src http://debian.cn99.com/debian testing-proposed-updates main
> contrib non-free

2、安装必备的软件包，如SSH服务器、X、桌面管理器、SSL等

> apt-get install ssh x-window-system-core gnome-core ftp
> openssl

其中X刚开始没能起来，编辑/etc/X11/XF86Config-4，注释掉其中的DefaultDepth
16才行。

3、安装及配置Nessus

> dpkg -i Nessus-3.0.5-debian3_i386.deb
> NessusClient-1.0.2-debian3_i386.deb

到http://www.nessus.org/plugins/index.php?view=register注册，用类似如下命令注册并升级：

> /opt/nessus/bin/nessus-fetch --register
> ACD8-98A4-6E9F-4948-6EEA

创建一个Nessus用户：

> /opt/nessus/sbin/nessus-adduser

后台启动Nessusd服务器：

> /opt/nessus/sbin/nessusd -D

运行客户端并对Global设置进行初步调整

> NessusClient
