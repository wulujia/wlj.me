---
title: "用 ModSecurity 补上网站的小洞洞"
date: 2006-03-18T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1731"
---

上回 [superhei](http://superhei.blogbus.com/) 指出公司的网站有个小 bug，允许读出数据库里的内容，刚调整代码没多久，前两天 [poop](http://blog.xfocus.net/index.php?blogId=30) 又发邮件说 search.php 还有个小跨站脚本错误……恼了，虽然漏洞都很小，但终归不爽。

请教了下 coolc 和 baoz，给网站上了个 [ModSecurity](http://www.modsecurity.org/)，省得总得担心着……
