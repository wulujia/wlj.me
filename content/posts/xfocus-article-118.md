---
title: "如何利用终端服务入侵远程计算机"
date: 2001-03-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-118"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

如何利用终端服务入侵远程计算机


                    by coolweis

                    coolweis@sina.com


用过windows 2000终端服务的人一定可以体会到终端服务的方便。但是这也给我们造成了安全风险。

恶意用户可以通过猜密码进入系统，更危险的是，如果这台机器存在输入法漏洞的话，那么入侵者

可以完全控制这台机器。

下面我来讲讲如何利用输入法漏洞远程入侵开了终端服务的windows 2000的机器：


首先我们确定某台机器的3389端口是开放的：

D:\\Nmapnt>nmapNT.exe -sS -p 3389 xxx.xxx.xxx.xxx


Starting nmapNT V. 2.53 by ryan@eEye.com

eEye Digital Security ( [http://www.eEye.com](http://www.eeye.com/) )

based on nmap by fyodor@insecure.org  ( [www.insecure.org/nmap/](http://www.insecure.org/nmap/) )

Interesting ports on FGF-DELL4300 (xxx.xxx.xxx.xxx):

Port       State       Service

3389/tcp   open        msrdp

Nmap run completed -- 255 IP addresses (93 hosts up) scanned in 542 seconds


D:\TOOLS\nmapNT\Nmapnt>


现在我们已经可以看到这台机器的终端服务是开放的，那么我们就可以开始行动了。

打开终端服务客户端，添上IP地址，选择连接。

稍等片刻，一般是很快的，就会出现熟悉的登陆对话框了，这是我们看看有没有输入法的漏洞。有关

输入法的漏洞请参看相关文章。如果有输入法漏洞那么我们如何取得控制权呢？经过多次的研究试验。

终于想出了一个办法。我们发现在跳至url后，我们双击winnt目录下的explorer.exe并没什么反应（是

机上已经运行了，可是我们为什么看不到结果呢？），如果我们不断的进行双击，或者什么也不做，一

会儿连接将被断开，在断开的一霎那，我们似乎看到了我们双击出来的窗口。经过几次试验，我们发现

不登陆进去是不行的，将会被服务端断开。于是想办法先登陆进去，我想到了在帮助中打开用户管理器，

经过试验，在跳至url中添入：mk:@MSITStore:C:\WINNT\Help\TSHOOTconcepts.chm::/where_usermgr.htm

在右侧会出现一个可以打开本地用户和组的管理器的链接，本来在正常情况下是可以打开这个管理器的，

可是在没有登陆进去的时候就是出不来，于是想另外的办法。终于想到了建立一个命令行的快捷方式。在跳

至url中输入：c:\winnt\system32，然后找到net.exe，右键点击net.exe，选择创建快捷方式，于是创建了

一个文件名为快捷方式net.lnk的文件，然后再右键点击这个快捷方式，选择属性，这时我们就可以输入我们

的命令了。在目标中添入我们要执行的命令的路径和参数就行了，我们还是用net命令，因此不必改路径了，

添加个账号test的命令如下，C:\WINNT\system32\net.exe user test/add。密码为空。然后双击这个快捷方

式运行它。然后我们把这个账号添加到administrators组中，

C:\WINNT\system32\net.exe localgroup administrators test/add。OK!再运行。我们现在已经基本上成功了，

关掉帮助窗口，用test账号登陆，密码为空。进去后我们把刚才建的快捷方式删掉。然后再将本地用户的

TSinternetuser账号加进administrators组中，设置密码。这样我们下次就可以用这个账号进来了。然后

再用这个账号登陆一下，如果能够登陆，就删掉刚刚建立的test账号。


这台机器就这样控制在我们的手里了。。。。。。
