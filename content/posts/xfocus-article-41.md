---
title: "LOVE-LETTER-FOR-YOU病毒/蠕虫的分析"
date: 2000-05-05T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-41"
---

(quack_at_xfocus.org)

LOVE-LETTER-FOR-YOU病毒/蠕虫的分析


by quack

参考：Analysis of the LOVE-LETTER-FOR-YOU virus/worm


这些天这个病毒在欧洲的许多国家大行其道，不少知名的公司都中了标--这其实是一个用vbscript写出来的

可以通过email散布的病毒（这点同梅丽莎相似）。


潜伏与发作


所有一切都发生在你打开邮件的附件--该脚本运行，将自身拷贝到

$windir/Win32DLL.vbs ($windir = c:\windows on most windows systems)

$systemdir/MSKernel32.vbs ($systemdir = c:\windows\system)

$windir/LOVE-LETTER-FOR-YOU.TXT.vbs

然后将这些文件加载到注册表中以便在启动时自动运行。


然后它将改变默认的ie浏览页面--通过该页面你会下载一个可执行的代码--下载完毕后它会将其加入注册表而且

再把IE的默认浏览页面再改回about:bland。


接下来它就开始往你地址薄里的邮件地址发送信件了--扫描你的硬盘及网络共享硬盘，寻找后缀为：

           Vbs, vbe, js, jse, css, wsh, sct, hta, vbs, jpg, jpeg

所有这些文件将变改成这个病毒，而且当它发现mp2或者mp3格式的文件时，会将自身拷贝到同样目录下的一个

vbs script中、当找到mIRC时也将建立一个小的mIRC script--可以发送html页面--这样就可以对所有加入

你所在频道的所有用户发送html并感染他们的IE。


执行


它会将你的共享密码及IP地址通过email发送给作者。


解决


打开你的注册表编辑工具并且删除下列键值：

HKEY_CURRENT_USER\Software\Microsoft\CurrentVersion\Run\MSKernel32

HKEY_CURRENT_USER\Software\Microsoft\CurrentVersion\RunServer\Win32DLL

HKEY_CURRENT_USER\Software\Microsoft\CurrentVersion\Run\WIN_BUGSFIX


查找一个叫WIN-BUGFIX.exe的文件并删除它

删除文件$dirsystem\LOVE-LETTER-FOR-YOU.HTM


检查所有后缀为Vbs, vbe, js, jse, css, wsh, sct, hta, vbs, jpg, jpeg的文件，看是否已被感染，

如果是的话就删除它们。


如果安装了mIRC的话删除你的script.ini文件。

删除所有相关的email，或许还需要警告你的朋友们，收到相关信件时要小心:)


预防


不要打开任何你有疑惑的文件--如果你没把握的话:)

也可以关掉所有的脚本:(


(我们站上也有解决该问题的小代码供中毒者下载)
