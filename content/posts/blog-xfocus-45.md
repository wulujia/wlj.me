---
title: "fonts.conf"
date: 2004-03-26T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-45"
---

今天升级gtk后simsun字体有点奇怪，antialias又出来了，而且似乎字体不受~/.gtkrc-2.0的控制，所以gvim、gaim、gqview、gimp之类的程序用起来都感觉巨不爽。 
查了一下fonts.conf的资料，找到两个小tip： 
1、让大小为9~13的simsun统一显示成13：[http://linuxsir.org/bbs/showthread.php?s=&threadid=95687](http://linuxsir.org/bbs/showthread.php?s=&threadid=95687) 
2、小于等于14点不用平滑效果：[http://linuxsir.org/bbs/showthread.php?s=&threadid=23073](http://linuxsir.org/bbs/showthread.php?s=&threadid=23073)
