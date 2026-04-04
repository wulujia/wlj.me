---
title: "Apache控制连接请求的模块"
date: 2004-08-29T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-428"
---

1、mod_limitpconn
[http://dominia.org/djao/limitipconn2.html](http://dominia.org/djao/limitipconn2.html)
减轻客户端通过webzip，teleport之类的抓网页工具对Web Server造成的繁重压力。

2、mod_dosevasive
[http://www.nuclearelephant.com/projects/dosevasive/](http://www.nuclearelephant.com/projects/dosevasive/)
在/tmp下面给每一个IP建立一个跟踪文件，当该IP请求频度超过设置警戒，即判定是可能的DoS攻击，然后禁止该IP在一段时间之内的请求。
