---
title: "用AutoIndex建个文档交流的小环境"
date: 2006-11-28T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2279"
---

[AutoIndex](http://autoindex.sourceforge.net/)这个简单的文件上传下载软件还不错，小巧实用。以前曾经找到过，后来没有用，就给忘了，前些时候[包子](http://blog.xfocus.net/index.php?blogId=3)又提起来，正好，想建一个用于[合作伙伴文档交流的小环境](http://www.i170.com/Attach/52CA32E8-8F23-46C1-B83C-15792B073B9D)，就先用它了吧 :)

安装极其简单，就是中文支持还有些小问题，在[FreeLamp](http://www.freelamp.com/1109945774/index_html)上有篇小文章，可以参考。我修改了：

> //date_format 格式 添加了小时：分钟 H:I
> 
>   $date_format = 'Y-m-d H:i'; //see http://php.net/date
> 
>   
> 
>   //添加函数 html_entry ，需要再修改全部 htmlentities 函数为 html_entry 函数
> 
>   function html_entry($f) {
> 
>   return htmlentities($f,ENT_COMPAT,"UTF-8");
> 
>   }
