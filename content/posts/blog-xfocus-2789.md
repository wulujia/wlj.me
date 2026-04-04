---
title: "用超级巡警批量清除被挂马的网页"
date: 2007-07-28T00:00:00+08:00
tags: ["Startup"]
draft: false
slug: "blog-xfocus-2789"
---

经常看到网上有人在问：什么原因导致所有网页文件都被加了[iframe](http://www.google.cn/search?complete=1&hl=zh-CN&newwindow=1&client=firefox-a&rls=org.mozilla%3Azh-CN%3Aofficial&hs=UfL&q=%E7%BD%91%E9%A1%B5%E6%8C%82%E9%A9%AC+iframe&btnG=Google+%E6%90%9C%E7%B4%A2&meta=)？

至少可能有两种原因：

> 1、网站被挂马，所有页面被骇客加了iframe并指向木马文件；
> 
> 2、中了ARP病毒，例如[这个链接中接到](http://www.cn-pn.com/article/4/623.html)的8w8w8w病毒；

不管哪种原因，杀毒的方法并不复杂，但杀毒之后，所有网页中都还有着那条被插入的iframe，怎么处理呢？别急，[超级巡警](http://www.dswlab.com/)能帮您解决这个问题，在超级巡警4.0
beta3中的垃圾清理功能中，新增了“清除指定代码”的功能，如下图所示：


打开超级巡警，选择“垃圾清理->智能扫描->清除指定代码“后，在指定代码的内容中填入您的网页被插入的内容，之后选择扫描路径后，点击扫描或清除，世界就清静了，简单吧。
