---
title: "一个信息安全研究团队的五年——我们的网络安全焦点"
date: 2004-08-26T00:00:00+08:00
tags: ["Tech", "Security"]
draft: false
slug: "xfocus-five-years"
---


2004年8月26日，是网络安全焦点的五岁生日，祝她生日快乐，并回忆从她出生起的点点滴滴……

## 1. 网站这些年

1999年8月26日，出于个人的兴趣，xundi建起了一个个人网站，取名为安全焦点。

![1999年的安全焦点](/images/xfocus-five-years-1.png)

以这个小小的站点为中心，几个对网络安全有一定兴趣的朋友便聚到了一起。聊天、学习，并且把自己的心得体会写下来，当时主要能做的仅仅是将国外的安全技术编译整理，并在网站上发表，临近2000年的时候，由于xundi所在的单位处理"千年虫"，因此他将网站的管理权限交给了quack和casper，由他们进行了一段时间的维护。到了2000年1月1日，站点改版。风格简单得不能再简单，实用——这是大家都欣赏的。在这段时间里，大家认识了很多新朋友，stardust、isno、glacier等兄弟都聚到了一起，很开心。

![2000年的安全焦点](/images/xfocus-five-years-2.png)

2001年1月1日，站点再次改版，将stardust搜集了很长时间的漏洞利用程序搜索引擎加入站点，整个主页由perl驱动。

![2001年Perl驱动版](/images/xfocus-five-years-3.png)

2001年3月17日，许多兄弟都混在北京了，这时san的加入很大程度上推进了这一版的站点改版，由php+mysql驱动。加入论坛、CVS项目、IRC、知识问答等，并把漏洞利用程序搜索引擎替换为在功能定义上更为完善的漏洞数据库。这次改版从形式到内容，都是一个比较大的飞跃，站点有了很强的可扩展性。与国内同类网站相比，我们希望有更好的文档和工具分类，更深入的归纳整理，更强大的检索功能，成为文档和工具中心可能是我们的发展方向之一。这一阶段中，我们的团队也趋于稳定，更多的技术爱好者加入进来了，alert7、benjurry、blackhole、eyas、flashsky、funnywei、refdom、tombkeeper、watercloud、wollf等大批兄弟们也因为共同的爱好，越走越近。

为了让国外的安全界的朋友们对国内安全现状有一个基本的了解，2001年11月10日，英文网站正式发布，使用 http://xfocus.org 的域名，原来的中文网站域名改为 http://xfocus.net 。英文站点上纯粹放自己的代码、程序以及心得体会。虽然在这之前，我们的一些漏洞利用代码、程序也陆续能够在securityfocus、packetstorm、securiteam等网站被转载，但这时总算有了一个自己对外的发布窗口了。

![英文网站](/images/xfocus-five-years-4.png)

时至今日，网络安全焦点的网站已经进一步改版，并有了很大的扩展了。我们所组织的"信息安全焦点峰会"即xcon，也在国际上有了一定的影响。

中文网站：

![中文网站2004](/images/xfocus-five-years-5.png)

英文网站：

![英文网站2004](/images/xfocus-five-years-6.png)

Blog网站：

![Blog网站](/images/xfocus-five-years-7.png)

Xcon网站：

![Xcon网站](/images/xfocus-five-years-8.png)

## 2. 我们的声音

### 2.1 比较

用alexa对xfocus和国内外安全领域的站点作了比较，结果不能说明什么，一切都将从头开始。

xfocus.net与nsfocus.net的比较：

![xfocus vs nsfocus](/images/xfocus-five-years-9.png)

xfocus.net与securityfocus.com的比较：

![xfocus vs securityfocus](/images/xfocus-five-years-10.png)

### 2.2 声音

国外的黑客对中国信息安全领域取得的成就是有一定程度认可的，其中包含了很多商业与非商业组织的努力，xfocus的技术研究，是否也在国外得到了认同呢？

- ZDnet、News.com等网站曾经报导过xfocus成员所进行的漏洞研究和利用程序开发；
- xfocus成员开发的安全工具与利用程序、文章多次被如SecurityFocus、PacketStorm、SecuriTeam等网站转载；
- xfocus成员发现的安全漏洞涉及Windows、AIX、HPUX、ORACLE、MSSQL甚至手机等多种不同平台和应用；
- xfocus组织的信息安全焦点峰会xcon到今年将是第三届，有国内外安全界高手的支持与参与；
- ……

我们仍在不断努力!

## 3. 一些记忆

有些事，不写下来，可能很快会忘却，这里是我记忆中的零星碎片，关于xfocus，关于xfocus的成员的。

### 3.1 xfocus的服务器

五年来，我们的网站都放在哪里呢？

最初的个人网站，没有自己的服务器，只是申请了碧海银沙的一个免费空间，网址是：http://focus.silversand.net ，在使用了stardust的Perl脚本后，网站搬到了万网，当时已经采用了域名 http://www.xfocus.org 了，租用了一个小小的空间，BSDi的服务器，有shell，有perl的执行权限。

访问量渐渐增大，网站的安全性也更大程度引起关注的时候，我们希望有自己的服务器了，这时在eist的帮助下，我们在黑龙江电信找了台Linux机器。再以后，spp提供的一台Solaris、Zlee提供的一台FreeBSD都为我们解决了当时很紧张的服务器和带宽问题。(这段时间内时不时遭受的拒绝服务攻击，曾经给我们和我们的朋友带来不少困扰)。

终于在2002年底，xfocus的成员决定每人每年为网站提供一笔捐款，规定了上限，没有下限。利用这笔钱，我们购买了一台服务器，并且在IDC租用了网络带宽，以往不断搬迁终于成为历史。

### 3.2 xfocus的一些伙伴

这段时间内，还有不少好朋友也加入过我们的团队，后来因为工作等种种原因又离开了，lzp、lhyx、vcat等人都是如此，走在一起的感觉很好 :)
