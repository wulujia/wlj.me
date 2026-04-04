---
title: "了解你的敌人：被动式指纹探测"
date: 2000-05-24T00:00:00+08:00
tags: ["Security", "Translation"]
draft: false
slug: "xfocus-honeynet-finger"
---

> 本文是 Honeynet Project 的"了解你的敌人：被动式指纹探测"系列文章的中文翻译，原文发布于 [project.honeynet.org](http://project.honeynet.org/)，中文翻译来自 [xfocus.net](http://www.xfocus.net/)。

**网络安全的挑战之一就是你需要了解攻击者，要了解你存在的威胁并保护你自己的资源，你需要了解你的敌人，被动特征探测是了解攻击者而不被攻击者觉察的方法之一，虽然这种方法可能不是100%正确，但你会获得一些令你诧异的结果。Craig
Smith开发基本本文概念的工具[passfing](http://www.xfocus.www.xfocus.net/honeynet/papers/finger/passfing.tar.gz).另外subterrain
crew也开发了[siphon](http://www.subterrain.net/projects/siphon),一个可以被动探测端口和OS的工具。Fingerprinting**

传统上，操作系统特征可以通过"积极性"的工具，如queso或者nmap,这些工具是在每一个操作系统上的IP堆栈有自己不同特性的原理上来操作的，每个操作系统响应通过的多种信息包。所以这些工具只要建立一个基于不同的操作系统对应不同的信息包的数据库，然后，要判断远程主机的操作系统，发送多种不寻常的信息包，检测其是怎样响应这些信息包的，再与数据库进行对比做出判断。Fyodor的
[nmap](http://www.insecure.www.xfocus.net/nmap)工具就是利用这种方法的，他也写了一份具体的[文档](http://www.xfocus.www.xfocus.net/honeynet/papers/finger/nmap-fingerprinting-article.html)。

而被动特征探测（Passive Fingerprinting ）遵循相同的概念，但实现的方法不同。被动特征探测（Passive Fingerprinting
）基于嗅探远程主机上的通信来代替主动的去查询远程主机，所有你需要做的是抓取从远程主机上发送的信息包。在嗅探这些信息包的基础上，你可以判断远程主机的操作系统，就象主动特征探测一样，被动特征探测（Passive
Fingerprinting ）也是由每个操作系统的有自己的IP堆栈特征，通过分析sniffer traces 和鉴别他们之间的不同之处，就可以判断远程主机的操作系统了。

**信号**

判断主机的操作系统一般可以由4个方面来着手（当然也有其他信号存在）：

- TTL - 这个数据是操作系统对出站的信息包设置的存活时间。

- Window Size - 是操作系统设置的窗口大小，这个窗口大小是在发送FIN信息包时包含的选项。

- DF - 可以查看是否操作系统设置了不准分片位

- TOS - 是否操作系统设置了服务类型

通过分析信息包这些因数，你可以判断一个远程的操作系统，当然探测到的系统不可能100%正确，也不能依靠上面单个的信号特征来判断系统，但是，通过查看多个信号特征和组合这些信息，你可以增加对远程主机的精确程度。下面是一个简单的例子，下面是被探测的系统发送一个信息包，这个系统发起了一个mountd的漏洞攻击，因此我想了解这个主机,
我现在不使用finger或者NMAP等工具，而想要了解被动接受到的信息，使用[snort](http://www.xfocus.www.xfocus.net/honeynet/papers/finger/security.html)得到了下面的一些信号特征：

04/20-21:41:48.129662 129.142.224.3:659
-> 172.16.1.107:604

TCP TTL:45 TOS:0x0 ID:56257

***F**A* Seq: 0x9DD90553  
Ack: 0xE3C65D7   Win: 0x7D78

根据上面的四条准则，我们可以达到下面的情况：

- TTL: 45

- Window Size: 0x7D78  (or 32120
in decimal)

- DF: The Don't Fragment bit is set

- TOS: 0x0

我们在比较[信号特征数据库](http://www.xfocus.www.xfocus.net/honeynet/papers/finger/traces.txt)，首先，我们查看使用在远程系统上的TTL，从我们的获得信息可以看到TTL是45，这多数表示它通过19跳才到达我们主机，因此原始的TTL应该是设置为64，基于这个TTL，这个信息包应该看来是由LINUX和FREEBSD系统发来的（当然更多的系统信号特征需要放到数据库中），这个TTL通过了traceroute远程主机得到证实，如果你考虑到远程主机在检测你的traceroute,你可以设置你traceroute的time-to-live(默认是30跳），使用-m选项来设定到主机的跳数少1到2跳的数值，如，刚才的例子里，我们可以使用traceroute
-m 18来设置跳数为18跳，这样做可以让你看到到达主机的路径而不碰到远程主机。要更多关于TTL的信息，请查看这篇[文章](http://www.switch.ch/docs/ttl_default.html)

下一步是比较窗口大小-Windows size,用Windows size来判断是另一个非常有效的工具，特别是使用多大的窗口大小和改变大小的规律，在上面的信号特征中，我们可以看到其设置为0x7D78,这是LINUX通常使用的默认窗口大小。LINUX，FREEBSD和SOLARIS系统在完整的一个会话过程中窗口的大小是维持不变的，但是
，部分Cisco路由器（如2514）和WINDOWS/NT的窗口是经常改变的（在一个会话阶段），如果在初始化三次握手后衡量窗口大小是比较精确的，具体信息，可以看看Richard
Stevens的"TCP/IP Illustrated, Volume 1" 20章.

多数系统使用DF位设置，因此这个是一个限定的值，但是有些系统如SCO和OPENBSD不使用这个DF标志，所以就比较容易的用来鉴别一些没有这个DF位设置的系统，在更多的测试后，发现TOS也是一个限定的值，这就表示不是很多操作系统来判断TOS，而是协议在使用这个值。TOS的判定需要更多的测试。因此，根据上面的信息，一些特殊的TTL值和窗口大小值，你可以通过[信号数据库](http://www.xfocus.www.xfocus.net/honeynet/papers/finger/traces.txt)来比较结果。

注意，与主动特征探测一样，passive Fingerpinting有许多限制，首先，应用程序必须构建他们自己的与操作系统不同信号特征信息包（如NMAP，HUNT
，TEARDROP等）。其次，这种探测可以使用调整系统的信息包的值来逃避这种检测，如可以用下面的方法来改变TTL值：

[Solaris:](http://www.rvs.uni-hannover.de/people/voeckler/tune/EN/tune.html) ndd -set /dev/ip ip_def_ttl 'number'

**Linux:** echo 'number' > /proc/sys/net/ipv4/ip_default_ttl

[NT:](http://support.microsoft.com/support/kb/articles/Q120/6/42.asp?LN=EN-US&SD=gn&FR=0) HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Tcpip\Parameters

通过上面所说的方法结合，你就可以大致判断出远程操作系统的情况了。

**其他信息特征和使用**

上面的是讨论了4个信号特征，但还有其他的特征可以被跟踪，如一些初始化序列好，IP鉴定号码（IP Identification numbers ），TCP或者IP的选项。如:Cisco路由器趋向由0开始IP鉴定号码（IP
Identification numbers ）来代替随机的指派号码。也可以使用ICMP的有效负载来判断，[Max
Vision discusses](http://dev.whitehats.com/papers/passive/index.html) 使用ICMP有效负载类型或者TCP选项来鉴别远程主机，举个例子，微软的ICMP REQUEST的有效负荷包含字母，而SOLAIRS或者LINUX的ICMP
REQUEST有效符合包含数字和符号。又如TCP选项，选择性的应答Acknowledgement选项[SackOK](http://www.xfocus.www.xfocus.net/honeynet/papers/finger/rfc2018.txt)
通常被WINDOWS和LINUX使用，但FREEBSD和SOLARIS这个选项不使用。MSS(最大数据段大小)也可以用来判断，绝大多数系统使用1460
大小的MSS，NOVELL使用的是1368，而有些FREEBSD变种使用512大小的MSS，另一个信号特征是信息包状态，什么类型的信息包被使用，可以应用FYODOR的话说：

"例如，最开始的SYN请求对我来说是一块金子(因为它会被回复)，而RST信息包也有一些有趣的特征用来鉴定系统."其他多种特征和上面所说的特征组合能很好的判断远程操作系统。

被动特征探测可以用来其他一些用途，它当然也可以被攻击者用来秘密的探测系统，如可以请求WEB服务器的WEB页然后进行分析。这对于绕过一些IDS系统的检测有很大的帮助。而且被动特征探测也可以用来判断远程代理防火墙，因为代理防火墙重建对客户的连接，它有它自身的特征代码。也可以同来在同一网络中判断其他系统，如某个公司全部是MICROSOFT或者SUN系统，就可能很快的使用这种方法来判断是否有其他机器混在里面。

**构建数据库**

[数据库](http://www.xfocus.www.xfocus.net/honeynet/papers/finger/traces.txt)是通过对各种系统进行TELNET，FTP，HTTP，SSH等协议分析而得到的。还有更多其他的协议来进行扩充，如果你有任何特征码增加到数据库中去请发送到[project@honeynet.www.xfocus.net](project@honeynet.www.xfocus.net?Subject=Passive%20Fingerprinting)地址，我特别对TCP或者IP选项特征感兴趣，或者一些没有列入到数据库中的操作系统。

**总结**

被动特征探测让你隐秘的了解你的攻击者，通过组合多种特征，你可以大体判断远程操作系统，感谢下面的人提供帮助和想法：

Fyodor

Max Vision

Marty Roesch

Edward Skoudis

Dragos Ruiu

Craig Smith

Peter Grundl 

Subterrain Siphon Project
