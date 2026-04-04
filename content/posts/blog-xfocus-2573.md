---
title: "ubuntu的/etc/inittab哪去了？"
date: 2007-04-16T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2573"
---

今天用ubuntu 6.10
server，意外地发现，居然找不到/etc/inittab文件，极其纳闷，翻了半天，才知道，在ubuntu中，inittab软件包已经被[upstart](http://upstart.ubuntu.com/)软件包替换了，所有的配置信息都在/etc/event.d/目录下。顺手记一笔，说不定也有其它人和我一样找不到
:)
