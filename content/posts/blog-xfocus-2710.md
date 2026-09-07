---
title: "普通UNIX下SSH客户端做端口转发穿越GFW"
date: 2007-06-17T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2710"
---

本来一直用着putty作为SSH的客户端，并且按照《[利用PUTTY通过SSH端口转发实现FIREFOX和MSN加密代理访问](http://www.chedong.com/blog/archives/001246.html)》的方法，用plink脚本直接连国外的服务器做代理。最近用Linux和MAC的机率增大，偶尔在这些系统下要访问被伟大和谐的GFW过滤掉的网站，只好用普通的SSH客户端了。

在terminal中执行命令：ssh username@my_host_ip_address -D
localhost:55555，输入正确口令后登陆，这个加密代理就算建好了。

至于FIREFOX中的代理工具，我不喜欢[SwitchProxy
tool](http://addons.mozilla.org/firefox/125/)，因此一直用的是[FoxyProxy](http://addons.mozilla.org/firefox/addon/2464)，这个工具有一点比较酷的是可以使用SOCK5代理服务器来查找DNS，这样就不用担心某些网站连DNS都被和谐掉了。
