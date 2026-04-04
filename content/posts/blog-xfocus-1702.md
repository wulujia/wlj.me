---
title: "Mantis 和 phpbt"
date: 2006-03-10T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1702"
---

公司一直用的是 [phpBugTracker](http://phpbt.sourceforge.net/) 作为公司软件缺陷管理的平台，搁在小呆的服务器上跑了将近一年。这回公司搬了新办公室，又来了几位新同事，就干脆将服务架回公司内部，也能省却安全上的烦恼。

可是很莫明其妙地，这回我 phpBugTracker 死活装不上了，先是没找着 [PEAR](http://pear.php.net/)，指定 PEAR 目录后，登陆出现空白，翻了下它在 sf.net 上的论坛，看到有类似的提问，但没有解决方法。懒得在上面花时间，看了看，原来数据库里未解决的 Bug 数量也不多，完全可以手工导入，于是就打起 [Mantis](http://www.mantisbt.org/) 的主意了。

几年前试过早期版本的 Mantis，没有惊艳的感觉，今天再装，仍然平淡，但很实用。

对比一下，我更推荐 Mantis。效果可以参考[这幅图片](http://blog.xfocus.net/resserver.php?blogId=1&resource=mantis.PNG)。
