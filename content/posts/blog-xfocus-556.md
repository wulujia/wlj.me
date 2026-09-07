---
title: "在Debian下安装FreeMind"
date: 2004-11-06T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-556"
---

关于FreeMind，可以参考这篇文章：http://risker.org/tech/FreeMind/index.html

1、安装Java

在/etc/apt/sources.list中加入ustc.edu.cn的uo并运行apt-update

deb http://debian.ustc.edu.cn/debian-uo/java ./

然后运行：

apt-get install j2re1.4

2、下载FreeMind并安装

我喜欢尝试新软件，因此用了0.8 alpha 2版本，下载地址：http://freemind.sourceforge.net/testversions/freemind-bin-0_8_0_alpha2.zip

3、中文支持

运行freemind.sh，界面上该有中文的地方都是乱码，也无法在脑图中输入中文。

修改~/freemind/下面的两个文件中的字体：user.properties和auto.properties，情况仍旧。

用strace跟了一下：

5147  access("/usr/lib/j2se/1.4/jre/lib/font.properties.zh_CN", R_OK) = 0

5147  open("/usr/lib/j2se/1.4/jre/lib/font.properties.zh_CN", O_RDONLY|O_LARGEFILE) = 4

……

……

5147  access("/usr/lib/j2se/1.4/jre/lib/fonts/fonts.dir", R_OK) = 0

5147  open("/usr/lib/j2se/1.4/jre/lib/fonts/fonts.dir", O_RDONLY|O_LARGEFILE) = 4

因此只要修订/usr/lib/j2se/1.4/jre/lib/font.properties.zh_CN和/usr/lib/j2se/1.4/jre/lib/fonts/fonts.dir，使之支持当前的中文字体就可以了。
