---
title: "了解你的敌人：II"
date: 2000-07-07T00:00:00+08:00
tags: ["Security", "Translation"]
draft: false
slug: "xfocus-honeynet-enemy2"
---

> 本文是 Honeynet Project 的"了解你的敌人：II"系列文章的中文翻译，原文发布于 [project.honeynet.org](http://project.honeynet.org/)，中文翻译来自 [xfocus.net](http://www.xfocus.net/)。

此文章是系列中的第二篇文章，在第一篇[Know
Your Enemy](http://www.xfocus.net/honeynet/papers/enemy/), 我们讲述了Script kiddie相关的工具和方法，特别是他们是怎样探测漏洞然后攻击的。在第三篇[Know
YourEnemy III](http://www.xfocus.net/honeynet/papers/enemy3/)中我们将会描述Script kiddie在获得ROOT的时候将会做的事情，特别是他们是怎样覆盖踪迹和他们下一步做的是什么。当前这文章，将涉及到有关则怎样跟踪他们的行为。我们会讲述到通过你的系统记录来判断你所需的操作，和你被扫描了以后，你需要了解被探测了以后主要被干什么用，他们使用了那些工具；这里的有些例子主要是基于LINUX操作系统，但是很容易移植到其他UNIX系统中，记住，没有绝对的方法能跟踪敌人的每一步，但是，这文章会是一个好的开始。

**加强系统LOG记录的安全性

**

这文章没有主要不是针对入侵检测进行讨论，关于IDS，internet上有很多优秀的源程序供你选择，如果你对入侵检测感兴趣，我建议你使用如[Network
Flight Recorder](http://www.nfr.net/) 和[snort](http://www.snort.org/)程序来尝试。此文主要集中在智力收集信息上，特别是，怎样通过查看你的系统记录来获取攻击者操作信息，可能你对你能在自己的LOG记录上能发现多少信息感到很惊讶，但是，在我们讲述查看你记录前，我们首先必须讨论下加强你的系统LOG安全性，如果你不能信任你系统记录的完整性那这些记录将会一文不值，多数black-aht在进入系统之后第一件事情就是怎样更改记录文件，网上非常多类型的Rootkit工具可以清楚记录文件中他们的留下的踪迹(如cloak)，或者阻止所有系统的记录(如伪造过的syslogd)，因此，要想查看系统记录，你必须保护好你的记录文件。

这意味着你需要使用远程的LOG服务器，先不管你有多少能力保护自己的系统，在一台被入侵的系统中你不能相信你的任何记录，即使你最好的保护被入侵系统的LOG记录,black-hat也可以简单的使用rm
-fr /*来完全清理你的硬盘。要保护这些文件，你必须使你所有系统的LOG记录既有本地记录也发向远程LOG服务器中，这里建立你一个只记录LOG的服务器来收集其他服务器上的信息，如果牵涉到钱的问题，你可以简单使用Linux服务器来充当你的LOG服务器，不过这台服务器必须保证非常安全，需要所有服务关闭，只允许控制台访问(如[Armoring
Linux](http://www.xfocus.net/honeynet/papers/enemy2/linux.html)所描述)，还有必须保证UDP 514口没有对外连接，这样可以保护你的LOG服务器不接受从外界来的不好的或者未认证的LOG信息。

由于上述原因，这里建议你重编译syslogd程序，并让syslogd读取不同的配置文件，如/var/tmp/.conf，此方法能让black-hat没有注意到真实的配置文件位置，这项操作你可以简单的在源代码中修改"/etc/syslog.conf"条目，接着我们可以设置我们新的配置文件把信息记录到本地和远程服务器,如[syslog.txt](http://www.xfocus.net/honeynet/papers/enemy2/syslog.txt)。这里请你维持一标准的配置文件/etc/syslog.conf指向所有本地LOG，虽然这份配置文件没有用，但可以让攻击者相信记录没有发忘远程记录。另一个选择方法就是让你的系统使用更安全的日志记录工具，如使用某些有完整性检查和其他方面安全加强的系统日志记录工具，如[syslog-ng](http://www.balabit.hu/products/syslog-ng.html)。

把记录都记录到远程服务器中，将想上面提到的，我们可以基本上相信这些LOG的完整性，而且由于所有系统都记录在单一资源中，就比较容易的判断这些LOG的样式。我们可以在一台机器上记录所有系统记录，你所做的是对比下本地系统和远程系统的不一致性。

**类型匹配** 

通过检查你的记录条目，你可以用来判断那些端口被扫描，许多Script kidde扫描整个网络只为一个漏洞，如你的记录显示你多数系统有来自同一远程系统的连接和同一端口，这就很可能以为着是一次漏洞的扫描，多数LINUX系统中，TCP
Wrapper默认安装的，所以你可以在/var/log/secure里找到多数连接，在其他UNIX系统中，我们可以通过启动inetd后增加-t标志就可以记录所有Inetd连接。下面是一个典型的漏洞扫描，是为了扫描wu-ftpd漏洞：

/var/log/secure

Apr 10 13:43:48 mozart in.ftpd[6613]: connect from 192.168.11.200

Apr 10 13:43:51 bach in.ftpd[6613]: connect from 192.168.11.200

Apr 10 13:43:54 hadyen in.ftpd[6613]: connect from 192.168.11.200

Apr 10 13:43:57 vivaldi in.ftpd[6613]: connect from 192.168.11.200

Apr 10 13:43:58 brahms in.ftpd[6613]: connect from 192.168.11.200

上面我们可以看到源主机192.168.11.200在扫描我们的网络，注意为何源主机连续扫描每个IP，这些记录就归功于LOG服务器，你可以方便的判断每个类型，连续的连接端口21，FTP，就暗示着攻击者在寻找wu-ftpd漏洞。一般来说，扫描是倾向于阶段性的，某些人发布了一个imap漏洞的利用代码，你就会发现记录里有imap扫描突然增多，下一个月如果有FTP利用程序发布，记录就会转向ftp突然增多，你可以在这个地址[http://www.cert.org/advisories/](http://www.cert.org/advisories/)获得当前最新的漏洞建议。有时，一个工具也会在同一时间里扫描多种漏洞，因此你也会看到一个源主机连接多个端口。

记住，如果你没有记录这些服务，你就不会知道你被扫描，例如，多数RPC连接没有被记录，但是服务记录是一件简单的事情，你可以通过在/etc/inetd.conf增加条目来让TCP
WRAPPER进行记录，如你在/etc/inetd.conf里增加NetBus条目，你就可以通过定义TCP Wrapper来安全的拒绝和记录NETBUS的连接(更多信息请查看[ids](http://www.xfocus.net/honeynet/papers/enemy2/ids.html)).

**判断使用工具**

有些时候你可以判断什么样的工具在扫描你的系统，因为一般工具都是扫描特殊的漏洞，如[ftp-scan.c](http://www.xfocus.net/honeynet/papers/enemy2/ftp-scan.txt)，如果你发现只是一个端口被扫描，一般他们使用的是单任务工具，但是也存在很多工具扫描多种系统漏洞和薄弱处，举两个非常有用的工具如jsbach写的sscan和Fyodor写的[nmap](http://www.insecure.org/nmap)，我只所以选择了这两个工具是因为他们能代表两种类别的扫描工具，这里强烈建议你用这些工具扫描下你自己的网络，或许你会得到让你吃惊的结果。

注：sscan工具是一个比较老的工具了，在这里只是把sscan拿来讨论，要扫描你网络系统的漏洞，这里建议使用[Nessus](http://www.nessus.org/)。

sscan代表着以"所有目标"为目的的Script kiddie扫描工具，它扫描网络一套的网络漏洞，它可以让你定制规则来对新漏洞的增加，你只要传递工具一个网络和网络掩码，其他的事情它来做，不过这个工具需要有ROOT权利才能使用，它的输出很容易理解，它会提供一个简洁的对漏洞服务的描述，所有你要做的就是让sscan扫描网络，然后你提取"VULN"的值，然后运行"exploit
du jour",下面是sscan对系统mozart (172.17.6.30)的扫描：

```
otto #./sscan -o 172.17.6.30

--------------------------<[ * report for host mozart *
<[ tcp port: 80 (http) ]>		<[ tcp port: 23 (telnet) ]>
<[ tcp port: 143 (imap) ]>		<[ tcp port: 110 (pop-3) ]>
<[ tcp port: 111 (sunrpc) ]>		<[ tcp port: 79 (finger) ]>
<[ tcp port: 53 (domain) ]>		<[ tcp port: 25 (smtp) ]>
<[ tcp port: 21 (ftp) ]>

--<[ *OS*: mozart: os detected: redhat linux 5.1
mozart: VULN: linux box vulnerable to named overflow.
<[ *CGI*: 172.17.6.30: tried to redirect a /cgi-bin/phf request.
<[ *FINGER*: mozart: root: account exists.
<[ *VULN*: mozart: sendmail will 'expn' accounts for us
<[ *VULN*: mozart: linux bind/iquery remote buffer overflow
<[ *VULN*: mozart: linux mountd remote buffer overflow
---------------------------<[ * scan of mozart completed *
```

Nmap代表"原始数据"工具集，它不告诉你系统有什么漏洞存在，相反，它告诉你系统有什么端口打开，你必须自己判断安全问题，Nmap很快变成扫描端口的首选，它是能很好的端口扫描工具并集合多种功能的工具包括OS探测，有多种端口组合选择，包括UDP和TCP扫描，不过这个工具需要你有一定的网络技能来使用这个工具并解析这些数据，下面是nmap对同一系统扫描的结果：

```
otto #nmap -sS -O 172.17.6.30

Starting nmap V. 2.08 by Fyodor (fyodor@dhp.com, www.insecure.org/nmap/)
Interesting ports on mozart (172.17.6.30):
Port State Protocol Service
21 open tcp ftp
23 open tcp telnet
25 open tcp smtp
37 open tcp time
53 open tcp domain
70 open tcp gopher
79 open tcp finger
80 open tcp http
109 open tcp pop-2
110 open tcp pop-3
111 open tcp sunrpc
143 open tcp imap2
513 open tcp login
514 open tcp shell
635 open tcp unknown
2049 open tcp nfs

TCP Sequence Prediction: Class=truly random Difficulty=9999999 (Good luck!)
Remote operating system guess: Linux 2.0.35-36

Nmap run completed -- 1 IP address (1 host up) scanned in 2 seconds
```

通过检查你的LOG记录，你可以判断那个工具在扫描你，不过你需要理解这些工具是如何工作的你才能判断出扫描你的工具，第一，sscan会在记录中留下下面的记录(这个是默认扫描没有增加任何修改和其他配置文件):

/var/log/secure

Apr 14 19:18:56 mozart in.telnetd[11634]: connect from 192.168.11.200 

Apr 14 19:18:56 mozart imapd[11635]: connect from 192.168.11.200 

Apr 14 19:18:56 mozart in.fingerd[11637]: connect from 192.168.11.200

Apr 14 19:18:56 mozart ipop3d[11638]: connect from 192.168.11.200 

Apr 14 19:18:56 mozart in.telnetd[11639]: connect from 192.168.11.200 

Apr 14 19:18:56 mozart in.ftpd[11640]: connect from 192.168.11.200 

Apr 14 19:19:03 mozart ipop3d[11642]: connect from 192.168.11.200 

Apr 14 19:19:03 mozart imapd[11643]: connect from 192.168.11.200 

Apr 14 19:19:04 mozart in.fingerd[11646]: connect from 192.168.11.200

Apr 14 19:19:05 mozart in.fingerd[11648]: connect from 192.168.11.200 

/var/log/maillog 

Apr 14 21:01:58 mozart imapd[11667]: command stream end of file, while reading
line user=??? host=[192.168.11.200] 

Apr 14 21:01:58 mozart ipop3d[11668]: No such file or directory while reading
line user=??? host=[192.168.11.200] 

Apr 14 21:02:05 mozart sendmail[11675]: NOQUEUE: [192.168.11.200]: expn root

/var/log/messages 

Apr 14 21:03:09 mozart telnetd[11682]: ttloop: peer died: Invalid or incomplete
multibyte or wide character 

Apr 14 21:03:12 mozart ftpd[11688]: FTP session closed 

sscan也扫描cgi-bin漏洞，这些探测没有通过syslogd记录，你可以在access_log中发现:

```
/var/log/httpd/access_log
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/phf HTTP/1.0" 302 192
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/Count.cgi HTTP/1.0" 404 170
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/test-cgi HTTP/1.0" 404 169
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/php.cgi HTTP/1.0" 404 168
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/handler HTTP/1.0" 404 168
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/webgais HTTP/1.0" 404 168
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/websendmail HTTP/1.0" 404 172
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/webdist.cgi HTTP/1.0" 404 172
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/faxsurvey HTTP/1.0" 404 170
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/htmlscript HTTP/1.0" 404 171
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/pfdisplay.cgi HTTP/1.0" 404 174
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/perl.exe HTTP/1.0" 404 169
192.168.11.200 - - [14/Apr/1999:16:44:49 -0500] "GET /cgi-bin/wwwboard.pl HTTP/1.0" 404 172
192.168.11.200 - - [14/Apr/1999:16:44:50 -0500] "GET /cgi-bin/ews/ews/architext_query.pl HTTP/1.0" 404 187
192.168.11.200 - - [14/Apr/1999:16:44:50 -0500] "GET /cgi-bin/jj HTTP/1.0" 404 163
```

注意上面对所有端口(SYN, SYN-ACK, ACK)进行了完整的连接，这是因为sscan判断应用层上的内容，不仅仅是sscan想知道你的ftp端口是否打开而且要知道什么样的FTP程序在运行，其他的imap,pop也是这样，你可以通过sniffit来嗅探起踪迹，sniffit是常用来嗅探密码的工具:

mozart $ cat 172.17.6.30.21-192.168.11.200.7238

220 mozart.example.net FTP server (Version wu-2.4.2-academ[BETA-17](1) Tue Jun
9 10:43:14 EDT 1998) ready. 

就想你上面所见到的，通过一次完整的连接来判断什么样版本的wu-ftpd在运行，当你在LOG文件里看到一次完整的连接，你就应该想到很可能是一次查找漏洞的工具在扫描。

Nmap，类似许多扫描器，并不关心你运行了什么，而是你运行了什么样特殊的服务，Nmap有一套功能强大的选项，让你选择什么类型的连接，包括SYN, FIN,
Xmas, Null等，你可以在[nmap_doc.html](http://www.xfocus.net/honeynet/papers/enemy2/nmap_doc.html)文章中获得详细的描述。由于使用到这些选项，你的记录上会因远程用户选择不同而不同，如果使用-sT标志，暗示一次完整的连接，你在记录上会看到和sscan类似的记录，不过nmap默认情况下扫描更多的端口:

/var/log/secure 

Apr 14 21:25:08 mozart in.rshd[11717]: warning: can't get client address: Connection
reset by peer 

Apr 14 21:25:08 mozart in.rshd[11717]: connect from unknown 

Apr 14 21:25:09 mozart in.timed[11718]: warning: can't get client address: Connection
reset by peer 

Apr 14 21:25:09 mozart in.timed[11718]: connect from unknown 

Apr 14 21:25:09 mozart imapd[11719]: warning: can't get client address: Connection
reset by peer 

Apr 14 21:25:09 mozart imapd[11719]: connect from unknown 

Apr 14 21:25:09 mozart ipop3d[11720]: warning: can't get client address: Connection
reset by peer 

Apr 14 21:25:09 mozart ipop3d[11720]: connect from unknown 

Apr 14 21:25:09 mozart in.rlogind[11722]: warning: can't get client address:
Connection reset by peer 

Apr 14 21:25:09 mozart in.rlogind[11722]: connect from unknown 

你必须注意Nmap有-D选项，它可以让用户来伪造源地址，你或许会在同一时间里看到从15个不同源主机来的扫描，其实这些地址真实的只有一个，所以从这些源地址中判断真实地址是比较困难的事情。还有，用户还会选择-sS标志，这是一隐蔽扫描选项，只发送SYN包，如果远程系统回应，连接就直接通过RST包来断开，所以这时候的记录会如下：

/var/log/secure

Apr 14 21:25:08 mozart in.rshd[11717]: warning: can't get client address: Connection
reset by peer

Apr 14 21:25:08 mozart in.rshd[11717]: connect from unknown

Apr 14 21:25:09 mozart in.timed[11718]: warning: can't get client address: Connection
reset by peer

Apr 14 21:25:09 mozart in.timed[11718]: connect from unknown

Apr 14 21:25:09 mozart imapd[11719]: warning: can't get client address: Connection
reset by peer

Apr 14 21:25:09 mozart imapd[11719]: connect from unknown

Apr 14 21:25:09 mozart ipop3d[11720]: warning: can't get client address: Connection
reset by peer

Apr 14 21:25:09 mozart ipop3d[11720]: connect from unknown

Apr 14 21:25:09 mozart in.rlogind[11722]: warning: can't get client address:
Connection reset by peer

Apr 14 21:25:09 mozart in.rlogind[11722]: connect from unknown

注意在连接中显示所有连接错误的，原因是SYN-ACK正确的顺序在完成完整连接之前被破坏，守护程序就判断不出源地址，这样记录虽然能记录被扫描，但不能记录谁在扫描，更甚的是，有些系统(包括新内核的LINUX)，没有一个错误记录会被记录。应用Fyodor的话"...基于所有'connection
reset by peer'信息，linux2.0.XX有点古怪--事实上每个其他系统(包括2.2和2.1后内核)会什么都不显示，这个BUG(accept()在完成3次连接之后返回)已经修补"

Nmap包含其他的一些隐蔽扫描选项，如:-sF, -sX, -sN ,在记录中会如下显示：

/var/log/secure

就是说没有任何显示，就是说你被扫描会你永远不会知道。所有这三种类型都是同样的结果，你只能记录-sT标志的扫描。要探测这些隐蔽扫描，你需要使用不同的记录程序如[tcplogd](http://www.kalug.lug.net/tcplogd/)或者[ippl](http://www.via.ecp.fr/%7Ehugo/ippl/)，某些商业防火墙也能探测到这些扫描，如Checkpoint
Firewall 1.

**判断他们是否进入 **

一旦你知道你被扫描了，下一个大问题就是"他们有没有进入你的系统"，现在多数远程利用程序基于缓冲溢出，简单的陈述就是当程序(一般是守护程序)接受到超多的输入后，会覆盖正确的内存区域，导致代码被执行，而获得远程ROOT访问，关于缓冲溢出更多信息，你可以查看Aleph1的phrack49-14.txt文章。

你一般可以在/var/log/messages或者/var/adm/messages文件中判断缓冲溢出攻击，如mountd。下面是对imapd进行的攻击，你在maillog里会发现如下的缓冲溢出信息：

Apr 14 04:20:51 mozart mountd[6688]:
Unauthorized access by NFS client 192.168.11.200.

Apr 14 04:20:51 mozart syslogd: Cannot glue message parts together

Apr 14 04:20:51 mozart mountd[6688]: Blocked attempt of 192.168.11.200 to mount

~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

P~P~P3Û3À°^[Í~@3Ò3À~KÚ°^FÍ~@þÂuô1À°^BÍ~@~EÀubëb^V¬<ýt^FþÀt^Këõ°0þÈ~HFÿëì^°^B~

I^FþÈ~IF^D°^F~IF^H°f1ÛþÃ~IñÍ~@~I^F°^Bf~IF^L°*f~IF^N~MF^L~IF^D1À~IF^P°^P~IF^H°

fþÃÍ~@°^A~IF^D°f³^DÍ~@ë^DëLëR1À~IF^D~IF^H°fþÃÍ~@~HÃ°?1ÉÍ~@°?þÁÍ~@°?þÁÍ~@¸.bin@~

I^F¸.sh!@~IF^D1À~HF^G~Iv^H~IF^L°^K~Ió~MN^H~MV^LÍ~@1À°^A1ÛÍ~@èEÿÿÿÿýÿPrivet

ADMcrew~P(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(Apr 14 04:20:51

mozart ^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^

E^H(-^E^H-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E

^H(-^E^H-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^ H(-^E^H(-^E^H(-^E^H(-^E^H(-^E^H(-^E

^H(-^E^H(-^E 

当你在LOG文件里看到如上的信息时，就可以判断有人尝试利用漏洞进入你的系统，不过是否成功就比较难判断，一种方法是，在漏洞利用之后查看是否有任何远程主机进入你系统，如果有从远程系统中成功的LOGIN，他们就已经进入你的系统，另一个线索是在/etc/passwd文件中查找可疑的帐户如"moof",
"rewt", "crak0", 或 "w0rm" 是否UID为0，一旦攻击者获得访问权利，他们会清除他们的记录和改装你的LOG记录，关于这方面更多信息，请查看[Know
Your Enemy: III](http://www.xfocus.net/honeynet/papers/enemy3/). 如果真的类似上面这样的操作，你就很难在你破坏的系统上获得任何信息。下一步该怎么做就是另一个话题了，这里建议你查看下面的文件：http://www.cert.org/nav/recovering.html

为了帮助我查找LOG文件中的反常记录，我写了一脚本程序来检查，关于更详细的查找和排序LOG文件，你可以查看此文：Marcus Ranum.（http://www.nfr.net/firewall-wizards/mail-archive/1997/Sep/0098.html)

这里是这个脚本的程序：

[Korn shell script](http://www.xfocus.net/honeynet/papers/enemy2/ksh.txt)

**总结**

你系统记录文件会告诉你详细的关于攻击者的信息，但是，首先你必须保证你LOG文件的完整性。一个最好的方法就是使用远程LOG服务器来接受和存储所有系统的系统。这样你可以判断LOG文件的信息类型，基于这些类型和LOG条目，你可以判断black-hat到底在干什么和判断他们使用的工具。根据这些知识，你可以更好的保护你的系统。
