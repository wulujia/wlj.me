---
title: "Couldn't load font Sans 10"
date: 2004-05-21T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-44"
---

因为stardict的音标总是无法正确显示，昨天加了几个字体后运行了defoma-reconfigure，结果却有问题，stardict一点设置就出错退出。 
开始没反应过来，直到早上运行ethereal的时候出问题，才意识到这是字体有误： 
[aa@risker:~$](mailto:aa@risker:~$) sudo ethereal 
** (ethereal:2120): WARNING **: Couldn't load font "Sans 10" falling back to "Sans 10" 
** (ethereal:2120): WARNING **: Couldn't load font "Sans 10" falling back to "Sans 10" 
** (ethereal:2120): WARNING **: All font failbacks failed!!!! 
找到症结就好办了，搜了一把，知道是/etc/pango/pangox.aliases这个文件出问题了，直接运行： 
# dpkg-reconfigure libpango1.0-common 
问题得到修正 :)
