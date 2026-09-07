---
title: "如何开启Apache的SSI支持"
date: 2006-09-12T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2076"
---

昨天晚上为[killer](http://www.dswlab.com/)装一个[slim-cms](http://developer.berlios.de/projects/slimcms/)，因为是shtml，需要[SSI](http://www.uplinux.com/download/doc/apache/ApacheManual/howto/ssi.html)（Server Side Includes）支持，一开始只是简单地加了两句：

> AddType text/html .shtml
> 
>   AddHandler server-parsed .shtml
却发现服务器怎么也解释不了.shtml文件，搜索了许久，才注意到有篇文章里提到：

> # AddType指令会要求服务器在传回任何附属档名为.shtml的网页时，以text或HTML做为传回文件的内容格式
> 
>   # AddHandler 则是用来指示服务器将文件内容送交给mod_include 处理。之后，mod_include 就会判断该如何响应这样的文件
猜到是mod_include没有开启，于是在apache2下运行：

> # a2enmod include
> 
>   # /etc/init.d/apache2 force-reload
一切就OK了 :)
