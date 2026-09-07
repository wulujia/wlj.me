---
title: "MAC的缺点"
date: 2007-07-12T00:00:00+08:00
tags: ["Life"]
draft: false
slug: "blog-xfocus-2764"
---

众口一词地说MAC好，说OSX人性化，其实有部份也是夸大其辞了──JOBS头上的光环和他们极其出色的工业设计，包括大批铁杆拥簇者极高的容忍度，掩住了它的部份不足。至少目前OSX里面就有两个让我很不舒服的缺点：

> 1、压缩文件、mail附件如果采用中文名称，传递到Windows上会变成乱码
> 
> 
> 2、Preview.app拷贝并贴进word里面的图片，Windows下一律看不了，只能用插入图片方式的图才是正常的

前者，号称是MAC全部采用UTF-8，国际化程度高，而Windows对UTF-8的支持不够好，所以有问题，后者也可以号称是Windows下面图片解码技术不够优秀……但对消费者而言，这就是缺点。

另外，昨天让我比较跌眼镜的一个情况是，OSX下的zip命令，看man
page的时候，堂而皇之地写着：

> -e     Encrypt the contents of the
> zip archive using a  password  which
> 
>              
> is  entered  on  the terminal in response to a
> prompt (this will
> 
>              
> not be echoed; if standard error is not a  tty, 
> zip  will  exit
> 
>              
> with  an  error).   The  password prompt
> is repeated to save the
> 
>              
> user from typing errors.

可实际上一带-e参数运行，却提示：zip error: Invalid command
arguments (encryption not
supported)，这应该还是属于质量控制不严吧。
