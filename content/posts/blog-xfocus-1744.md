---
title: "铁卷竞争产品介绍 1：Fasoo.com"
date: 2006-03-27T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1744"
---

DRM(dightal right management) 在国内已经越来越受到人们的重视。我们也相当看好这一市场，目前推出的[铁卷电子文档保护系统](http://www.unnoo.com/web/products/filesecure/)，有两个版本，工业制图版（保护 AutoCAD 等制图软件创建和另存的文档）和办公版（用于 Microsoft Office、金山 WPS、PDF 等文档）。工业制图版已经在一家重工企业全面部署，对工业图纸能够起到相当好的保护作用 ;)

想要产品更完善一些，就得多分析目前市场上的领先者的状况，所以近期我会对类似的电子文档安全产品做些学习和整理，这篇算个开始。如果朋友们有这些系统的使用经验，不妨给我些建议，先谢啦 ;)

Fasoo 的产品系列包括 FSD(Fasoo Secure Document)、FSF(Fasoo Secure File-server)、FSP(Fasoo Secure Print)、FSW(Fasoo Secure Web)、FSN(Fasoo Secure Node)、Wrapsody、CPmax 等。

根据 [XPower Lab 论坛](http://bbs.secyou.cn/)上 wireless 朋友的介绍，Fasoo 的功能大致如下：

1、分成 Agent 和 Server；
2、Agent 与 Server 之间需要通过帐号认证后才能通讯；
3、当对受控文档（如 doc、xls、ppt 等）进行写操作时，文件默认被加密保存；
4、打开文件前需要到服务器进行密码验证；
5、对文件的读取、写入等操作会在服务器进行记录；
6、Agent 可以申请出差或加班，得到批准后能够离线阅读文档；
7、所有加密文件有批量解密工具，由管理员控制。

客户端支持 Win98、98SE、2k、XP、2003，需要使用 IE 5.x 兼容浏览器。
服务器需要 WinNT/Win2k 或 AIX4 /HPUX 11/Solaris 5.6，Web 服务器 IIS 或 Apache 带 jsp 支持，采用 JDBC 2.0 兼容数据库

它还有一个给个人使用的 DRM 小产品，网站在 [www.drmone.com](http://www.drmone.com/)，我试了一下效果，在线安装一个客户端后，访问它的网页：

![](https://web.archive.org/web/20071014204645im_/http://blog.xfocus.net/resserver.php?blogId=1&resource=web.jpg)

如果试图采用拷屏软件来截图，会弹出下面的对话框：

![](https://web.archive.org/web/20071014204645im_/http://blog.xfocus.net/resserver.php?blogId=1&resource=notice.jpg)

如果用第三方拷屏/录像软件来截取图像，也会被截获，拷/录下的内容是：

![](https://web.archive.org/web/20071014204645im_/http://blog.xfocus.net/resserver.php?blogId=1&resource=confidential.jpg)

美中不足的是，记事本和画图软件都被它默认禁用了，很不爽。

广告时间：

[铁卷](http://www.unnoo.com/web/products/filesecure/)能够防止企业的 CAD、Office 文档泄露。用户在内网可以透明访问、创建文档，文档在保存时即时加密，即使流传出去，也无法在外部正常打开。非常适合制造、设计、咨询等行业使用。
咨询邮件：[wulujia@unnoo.com](https://web.archive.org/web/20071014204645/mailto:wulujia@unnoo.com)
