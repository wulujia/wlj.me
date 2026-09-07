---
title: "能杀毒的木马"
date: 2004-08-12T00:00:00+08:00
tags: ["Life"]
draft: false
slug: "blog-xfocus-329"
---

前几天，找我兄弟要了个小木马，有嗅探、记录击键、记录密码的功能。他写的程序，一般情况下是名家出品，品质保证的，测试了一把，在自己机器上装上了。
可是奇怪的是，隔天我重启系统时，居然发现出现下面的对话框：


唔，瞧，不是所有的牛人写的程序都没有bug嘛，俺一乐，拎着臭虫找我兄弟去了。
他觉得不太可能出这问题，于是我恨恨地查……发现注册表里面HKLM..Run: [ExFilter] 里写的：

Rundll32.exe C:WINDOWSSystem32hookdll.dll,ExecFilter solo

为了确认hookdll.dll是我兄弟的木马生成的，我特地删掉C:WINDOWSSystem32hookdll.dll，再运行一下我兄弟的木马，马上hookdll.dll诞生了，这下没话说了吧……哼哼，这么老土的招数，写这么没创意的注册表文件，害我检查到最后才检查注册表的这个土键值，我心里暗骂……发邮件兴师问罪去……

隔了一会，兄弟回邮：

WK，我仔细搜了一遍代码，注册表里的这行不是我写的，我的hookdll.dll里也没有导出ExecFilter这个函数。估计是跟其他软件的hookdll.dll重名了，你把这个hookdll.dll发给我瞅瞅吧。

再过一会儿，再发一封邮件给我：

google上找到两个跟“Rundll32.exe C:WINDOWSSystem32hookdll.dll,ExecFilter solo”有关的链接，不知道是IE插件还是病毒，反正挺狠的，不只你的机器上有。
[http://www.pcsos.cn/bbs/viewtopic.php?t=23743](http://www.pcsos.cn/bbs/viewtopic.php?t=23743)
[http://community.rising.com.cn/Forum/msg_read.asp?FmID=33&SubjectID=4182695&page=1](http://community.rising.com.cn/Forum/msg_read.asp?FmID=33&SubjectID=4182695&page=1)

原来……原来我又中招了，真没面子!真好运气!是我兄弟的木马帮我杀的毒呀……

得出两个结论：
1、我运气挺好 :)
2、我兄弟比我认真。
