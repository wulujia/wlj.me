---
title: "Narrow安全扫描器-2000pre1"
date: 2000-01-05T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-27"
---

文章提交：[quack](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

Narrow安全扫描器-2000pre1

===============================================================================

                                 quack译

                             

      1.0  关于NSS

      1.1  NSS的历史

      1.2  NSS的作者

      1.3  声明

      2.0  怎样使用NSS

      2.1  运行NSS需要的工具

      2.2  怎样使用子域扫描

      2.3  推荐配置

      2.4  NSS的臭虫

      3.0  镜像站

      3.1  怎样同作者联络

      3.2  感谢

================================================================================

1.0 - 关于Narrow Security Scanner

---------------------------------

Narrow安全扫描器是用perl写成，能够在*你*的服务器上查找249个已知漏洞的扫描工具。它

可以在所有支持perl 5及其更高看版本的系统运行。其Script在以下系统经过测试：

RedHat (4.2, 5.0, 6.0)

FreeBSD 3.0

OpenBSD 2.5,

Slackware 4.0 

SusE 6.1.

1.1 - Narrow Security Scanner的历史

-----------------------------------

我对编写NSS感觉充满乐趣――开始时是一个炎热的夏天，我想试试我的perl以及安全经验――写

下它前我写了NGC―Narrow CGI Check，NSS的第一个版本就在六月份向我的一些朋友发布了，他们

建议我完善它，于是我这么做了――经过好些个不眠之夜:)。第一个版本只能检查12个漏洞。

在我将一个副本发给".rain.forest.puppy." aka .r.f.p后不久，他回复了――稍微做了些改动，

使它运行得更顺畅并且更小。第一次公开发布的NSS版本是2.2版。

1.2 - Narrow Security Scanner的作者

-----------------------------------

呵，抱歉，我不会告诉你我的真实姓名的……;)

1.3 - 声明

-----------------------------------

作者"Narrow"不对你利用此程序出现的任何问题或导致的结果负责。软件包中也可能有病毒或木马。

你可以自由地使用和发布这个程序――但必须包括这个文档。记往，这是一个给管理员用来检查他

们的系统是否存在漏洞的程序!!!

                 !!!THIS SCRIPT IS FOR EDUCATIONAL USE ONLY!!!

2.0 - 怎样使用NSS

-----------------------------------

很简单――只要打入在目录下键入"perl scanner"就行了――当然如果你打包的，先解包:)

NSS 用法: perl ./scanner <主机文件> <记录文件>

<主机文件> - 包含要扫描的主机的文件――在包里有一个范例。

<记录文件> - 存放扫描结果的文件

在使用前你可能需要配置它，配置文件是"nss.conf"，默认它扫描的是所有漏洞。注意：扫描

所有漏洞的 话可能会使你的网络连接变得奇慢无比！但――谁在乎呢，你是用来扫自己的网络

的，是吗;)

2.1 - 需要的东东

----------------------------------

你需要有：Perl 5或更高版本, dig 以及 rpcinfo。

如果没有dig：    要改$scan_named to ZERO ($scan_named = 0).

如果没有rpcinfo：要改$scan_rcp to ZERO ($scan_rcp = 0).

2.2 - 如何使用子域扫描

-----------------------

如果你有很多子域的话，你可以用子域扫描将它写到一个文件中……

键入"perl ./generate"，够简单吧――支持perl5或更高版本的系统都可能运行。注意：子

域扫描里"host"可得到所有子域，windows用户没法用这一特性了……

子域扫描用法：(perl) ./generate <host> <log file>

<host> - 这儿填入你的主机，比如：host.com (前面不用写www了!)

<log file> - 所有的子域会被记录在这个文件中。

2.3 - 推荐配置

----------------

系统：支持Perl 5 或更高版本的系统

内存：能运行Unix就行了;)

剩余空间：100Kb

连接速率：28,800或更快

2.4 - 臭虫

--------------

你试试用root运行perl scanner /etc/(passwd or shadow) blah.log(我不知指的是什么意思

或许是说host文件不管格式如何都运行吧……)

3.0 - 镜像站

------------------

1. [http://www.legion2000.cc](http://www.legion2000.cc/)

2. [http://www.wiretrip.net/rfp/](http://www.wiretrip.net/rfp/)

3. [http://packetstorm.securify.com](http://packetstorm.securify.com/)

4. [http://www.securityfocus.com](http://www.securityfocus.com/)

3.1 - 怎样同作者联络 

--------------------------------

E-Mail: narr0w@legion2000.cc

3.2 - 致谢

---------------

nikel-com, _shocker_, tf8, wider, sid, sidux, _GrYpHoN_, .rain.forest.puppy.,

gov-boi, Condor, Packet Storm, Security Focus (BUGTRAQ), Hacker News, Zero,

Josh, cripto AND who wanted to be greeted :)
