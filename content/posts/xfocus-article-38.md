---
title: "The Solaris安全FAQ"
date: 2000-05-06T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-38"
---

(quack_at_xfocus.org)

The Solaris安全FAQ 


by quack 

参考资料：The Solaris Security FAQ by Peter Baer Galvin 


1) (概述--略)


2) 怎样将Solaris配置得更加强壮? 


2.1) 哪些文件的许可权限需要改变? 


有个叫fix-modes的软件([ftp://ftp.fwi.uva.nl/pub/solaris/fix-modes.tar.gz](ftp://ftp.fwi.uva.nl/pub/solaris/fix-modes.tar.gz))可以在

Solaris 2.4和2.5上运行并改变系统文件及目录的存取权限，这样会使非ROOT的用户更难

于更改系统文件或者取得ROOT权限。


2.2) 如何对ROOT的环境加以配置? 


将umask设为077或者027. 


查看你的环境中路径设置情况，不要有./


2.3) 我该更改哪些启动文件? 


通常情况下，你要检查所有在/etc/rc2.d和/etc/rc3.d以S开头的文件,所有并非必要的设备

或者服务都可以重命名(不要再以S开头)，然后你可以重新启动，从/var/adm/messages中来

观察自启动的情况，并且从ps -elf的输出中加以检查。


2.4) 如何将ROOT的远程登陆取消? 


在/etc/default/login里加上 "CONSOLE"行，在/etc/ftpusers里加上root。


2.5) 如何取消rlogin/rsh服务? 


移去/etc/hosts.equiv和/.rhosts以及各home目录下的.rhosts，并且在/etc/inetd.conf中

把r系列服务都杀掉，然后找出inetd的进程号，重启它。


2.6) 哪些帐号是不必须的? 


移去或者锁定那些不是必须的帐号，比如sys\uucp\nuucp\listen等等，简单的办法是在

/etc/shadow的password域中放上NP字符。


2.7) 怎样保护我的设备? 


在文件/etc/logindevperm中包含了对系统设备的许可权限配置信息，应该检视里面的各项

设定并且手动赋予你所想要的许可权限。


对于抽取式的BSM设备需要设定只有single user允许进入。


2.8) 我应该将/etc的存取权限改为什么才安全? 


用chmod -R g-w /etc命令来移去组用户对/etc的写权限。


2.9) Solaris机器充当路由器? 


默认情况下，如果Solaris机器有超过一块的网卡的话，它将会在不同网卡间转发数据包，这一行为可

以在/etc/init.d/inetinit中得到控制。要在Solaris 2.4或者更低版本机器下关闭它，可以将

ndd -set /dev/ip ip_forwarding 0添加于/etc/init.d/inetinit的未尾。在Solaris 2.5

中，只要touch /etc/notrouter. 


2.10) 如何取消automounter? 


Automounter是由/etc/auto_*这些配置文件控制的，要取消它，只要简单地移去这些文件,

并且/或者将/etc/rc2.d/S74autofs改名。 


2.11) 如何取消NFS服务? 


NFS的共享输出是由/etc/dfs/dfstab文件管理的.可以删除它。要将NFS服务器的守护进程关闭

则可以重命名/etc/rc3.d/S15nfs.server。要防止一台机器成为NFS客户机，可以重命名文件

/etc/rc2.d/S73nfs.client――当重命名这些自启动文件时，要注意不要将文件的首字母设为

“S”。 


2.12) 对cron任务我该注意些什么？ 


你得查看所有的cron任务――在/var/spool/cron/crontabs文件中你可以找到它们。还必须在

/etc/default/cron里设置了"CRONLOG=yes" 来记录corn的动作。 


2.13) 使用动态路由有什么风险吗? 


使用动态路由守护进程的机器用in.routed及in.rdisc来维护路由，这可能会大大增加路由协议的复杂程

度，而且路由更新会消耗相当大比便的可用带宽，因此在可能的情况下，还是建议你使用静态路由。


2.14) 何时及如何运用静态ARP? 


ARP是联系IP地址和以太网的协议(地址转换协议) 。默认地，Solaris机器动态地确定ARP地址，arp命令

可以用来静态地设定ARP表并且刷新它，如果你的系统里仅有少量无需更改的机器，那么这是一个很好的工具。

为了防止ARP欺骗，最好将受托机器的硬件地址作为永久条目保存在ARP的高速缓存中。


2.15) 运行rpcbind是不安全的吗? 


rpcbind是允许rpc请求和rpc服务之间相互连接的程序，但标准的rpc是不安全的:(,它使用的是"AUTH_UNIX"

验证, 也就是说它依靠的是远程系统的IP地址和远程用户的UID来验证。一般的系统可能需要某些rpc存在，但

对各种服务器如Web servers, ftp servers, mail servers, etc)最好将rpc服务关闭，你也可以通过

一些安全工具来确定rpc服务是否会影响到你系统的安全性。可以通过将/etc/rc2.d/S71RPC改名来禁止rpc。


2.16) /etc/utmp的权限应该如何设定? 


# chmod 644 /etc/utmp  


2.17) 哪些程序可以去掉SUID位? 


许多setgid和setuid程序都只是由root运行的，或者是由某些特定用户或组运行，那就可以将其setuid位

移去，下面是一个Solaris 2.6上setuid程序的列表，你应该根据自己的情况进行增减。


# find / -perm -4000 -print

/usr/lib/lp/bin/netpr

/usr/lib/fs/ufs/quota

/usr/lib/fs/ufs/ufsdump

/usr/lib/fs/ufs/ufsrestore

/usr/lib/fs/vxfs/vxdump

/usr/lib/fs/vxfs/vxquota

/usr/lib/fs/vxfs/vxrestore

/usr/lib/exrecover

/usr/lib/pt_chmod

/usr/lib/sendmail

/usr/lib/utmp_update

/usr/lib/acct/accton

/usr/lib/uucp/remote.unknown

/usr/lib/uucp/uucico

/usr/lib/uucp/uusched

/usr/lib/uucp/uuxqt

/usr/lib/sendmail.orig

/usr/openwin/lib/mkcookie

/usr/openwin/bin/xlock

/usr/openwin/bin/ff.core

/usr/openwin/bin/kcms_configure

/usr/openwin/bin/kcms_calibrate

/usr/openwin/bin/sys-suspend

/usr/dt/bin/dtaction

/usr/dt/bin/dtappgather

/usr/dt/bin/sdtcm_convert

/usr/dt/bin/dtprintinfo

/usr/dt/bin/dtsession

/usr/bin/at

/usr/bin/atq

/usr/bin/atrm

/usr/bin/crontab

/usr/bin/eject

/usr/bin/fdformat

/usr/bin/login

/usr/bin/newgrp

/usr/bin/passwd

/usr/bin/ps

/usr/bin/rcp

/usr/bin/rdist

/usr/bin/rlogin

/usr/bin/rsh

/usr/bin/su

/usr/bin/tip

/usr/bin/uptime

/usr/bin/w

/usr/bin/yppasswd

/usr/bin/admintool

/usr/bin/ct

/usr/bin/cu

/usr/bin/uucp

/usr/bin/uuglist

/usr/bin/uuname

/usr/bin/uustat

/usr/bin/uux

/usr/bin/chkey

/usr/bin/nispasswd

/usr/bin/cancel

/usr/bin/lp

/usr/bin/lpset

/usr/bin/lpstat

/usr/bin/volcheck

/usr/bin/volrmmount

/usr/bin/pppconn

/usr/bin/pppdisc

/usr/bin/ppptool

/usr/sbin/allocate

/usr/sbin/mkdevalloc

/usr/sbin/mkdevmaps

/usr/sbin/ping

/usr/sbin/sacadm

/usr/sbin/whodo

/usr/sbin/deallocate

/usr/sbin/list_devices

/usr/sbin/m64config

/usr/sbin/lpmove

/usr/sbin/pmconfig

/usr/sbin/static/rcp

/usr/sbin/vxprint

/usr/sbin/vxmkcdev

/usr/ucb/ps

/usr/vmsys/bin/chkperm

/etc/lp/alerts/printer


而且还应该建立一个setuid/setgid程序的列表，日后可以对比是否有新的setuid程序出现--这可能是

入侵者光临过的征兆。


2.18) 哪些系统工具我可以去掉它? 


所有的网络工具你都应该检查并且确定它在你的系统环境里是否是必需的，如果答案为否的话，就

干掉它，下面这些工具有些可以在开始文件中找到它，有些则上在/etc/inetd.conf中被启动的，注

释掉那些不必要的服务，并且kill -HUP inetd守护进程――类似的东西有：


tftp         systat        rexd    ypupdated    netstat

rstatd         rusersd        sprayd    walld           exec

comsat         rquotad        name    uucp


最好把常规的inetd.conf替换掉――改成只开telnet和ftp服务――如果你真的需要它们的话(建议再

用防火墙建立阻塞)。


2.19) 我应该运行in.fingerd吗? 


in.fingerd在过去有一些安全问题，如果你想提供finger工具，用nobody来运行它。


2.20) 如何让syslog有更大作用?

 

默认情况下，syslog仅提供最精简的记录，你可以通过编辑/etc/syslog.conf文件来让syslog记

录更多的信息，然后你需要重启syslog以使它读取配置文件。


你还可以通过


touch /var/adm/loginlog

chmod 600 /var/adm/loginlog

chgrp sys /var/adm/loginlog


来建立login的记录。


2.21) 对EEPROM如何做才能更安全? 


将EEPROM设于安全的模式：通过设定对"ok setenv security-mode=command"的密码保护来实现。

当然这并不能真正地防止入侵，如果某人可以物理接触某控制台的话，它就能打开机器并替换掉EEPROM，

更改hostid........


2.22) 我的机器是处于“混杂模式”下吗? 


在Solaris下，你只能通过安装某些工具来判断是否机器是处于混杂模式下，可以参见第三部分。只有当你

运行诸如snoop或者某些网络监听软件时机器才会处在混杂模式下，如果你并没有监听整个网络，那极大的可

能性就是黑客已经侵入到你的系统中并且开始以监听来接收数据了。


2.23) 如果我必须运行NFS，如何使它更安全? 


在/etc/dfs/dfstab中的所有文件将被所有人共享，默认情况下，NFS客户会以"-o rw"或者"-o ro"选项

共享。 

必须使用"nosuid"参数来使setuid程序失效。

不要通过rpcbind来运行nfs mount。而是用更安全的rpcbind替代程序或者安装SUN最新的rpcbind补丁。

在可能的情况下，尽量使用secure-RPC。否则的话，你运行的是"AUTH_UNIX"认证,它仅仅依靠客户的IP地

址来进行验证，很容易有IP欺骗的情况发生。

在可能的情况下，不要使用NFS，因为它的信息传递是通过明文的(甚至你用了"AUTH_DES"或者"AUTH_KERB"来

进行认证)所以传输的任何文件对嗅探来说是及危险的。

有程序可以猜度ROOT所mountr的文件名柄，并且获得NFS server上的文件。 


2.24) 如何让sendmail更安全? 


sendmail总是不断地有新漏洞被发现，怎样才能使它更安全呢？


使用最新版本的Berkeley sendmail (see section 3) 

使用smrsh (section 3) 

从/etc/aliases里删除decode 

将/etc/aliases的权限设为644 

可以考虑使用代理防火墙来过滤SMTP中不必要的命令。


2.25) NIS是安全的吗，如何使其更强壮? 


NIS从来就不是一个安全的服务，如果配置得当的话NIS+会更好些，就象暴力破解密码一样，NIS域名

如果被猜出来，就会给入侵者提供相当丰富的信息，要关闭这个漏洞，可以将信任主机的地址放在

/var/yp/securenets中。并且考虑使用NIS+或者secure RPC。


2.26) 匿名FTP要怎样才会安全可靠? 


Solaris 2.5 ftpd(1M)包含了一个很好的FTP配置说明


cp /etc/nsswitch.conf ~ftp/etc 

确保包含~ftp的文件系统在被安装是没有用nosuid选项

在~ftp下任何文件的属主都不是"ftp" 

更详细的信息参见它的配置说明及FAQ


2.27) 如何将X配置得更安全? 


使用SUN-DES-1选项来调用Secure RPC来通过X鉴别，可以使用xhost +user@host来通过访问请求。


2.28) 如何打开SUN-DES-1的鉴别机制? 


set DisplayManager*authorize: true 

set DisplayManager._0.authName: SUN-DES-1 

rm ~/.Xauthority 

增加对localhost的许可权限：通过xauth local/unix:0 SUN-DES-1 unix.local@nisdomain

                           xauth local:0 SUN-DES-1 unix.local@nisdomain 

Start X via xinit -- -auth ~/.Xauthority 

把你自己加入，并移去其他所有人：xhost +user@ +unix.local@nisdomain -local -localhost 

赋予用户foo进入主机"node"的权限: 


允许foo进入node:           xhost +foo@ 

建立适当的foo的xauthority： xauth add node:0 SUN-DES-1 unix.node@nisdomain 

foo现在就能连上"node"了:    xload -display node:0 


2.29) 我需要安装哪些补丁? 


用showrev -p命令来察看补丁在系统里的安装情况，在你想保护的主机以及大众都可以访问的主机

上，你应该到SUN公司的主页上去查找相关的补丁包来安装，并且应该常常查看最新的补丁发布情况。


2.30) 如何防止在堆栈中执行代码? 


入侵者常常使用的一种利用系统漏洞的方式是堆栈溢出，他们在堆栈里巧妙地插入一段代码，利用

它们的溢出来执行，以获得对系统的某种权限。


要让你的系统在堆栈缓冲溢出攻击中更不易受侵害，你可以在/etc/system里加上如下语句：


set noexec_user_stack=1

set noexec_user_stack_log =1


第一句可以防止在堆栈中执行插入的代码，第二句则是在入侵者想运行exploit的时候会做记录:)


3) 应该增加或者替代哪些程序? 


3.1) inetd 

   

inetd可以用xinetd代替，以增加日志功能。 

xinetd: 

[ftp://qiclab.scn.rain.com/pub/security/xinetd](ftp://qiclab.scn.rain.com/pub/security/xinetd)* 

或 [ftp://ftp.dlut.edu.cn/pub/unix/sun-source/xinetd-2.1.tar.Z](ftp://ftp.dlut.edu.cn/pub/unix/sun-source/xinetd-2.1.tar.Z)(不知是否为最新版本). 

 

3.2) ifstatus 


ifstatus可以确定你的网卡是否工作于混杂模式（有人进行网络监听?） 

url: 

[ftp://coast.cs.purdue.edu/pub/tools/unix/ifstatus/](ftp://coast.cs.purdue.edu/pub/tools/unix/ifstatus/) 

 

3.3) xntp 


xntp是有个更安全的网络时间协议(Network Time Protocol). 

URL: 

[ftp://ftp.udel.edu/pub/ntp/xntp3-5.93.tar.gz](ftp://ftp.udel.edu/pub/ntp/xntp3-5.93.tar.gz) (1907KB)      

3.4) sendmail 


用Berkeley Sendmail([http://www.sendmail.org/](http://www.sendmail.org/))替代Solaris自带的sendmail. 

 

3.5) rpcbind 


可以用如下URL中的rpcbind替换Solaris自带的rpcbind, 这个rpcbind包含了类似 

于tcpwrapper的功能并关闭了通过rpcbind访问NFS. 

  

[ftp://ftp.win.tue.nl/pub/security/rcpbind_1.1.tar.Z](ftp://ftp.win.tue.nl/pub/security/rcpbind_1.1.tar.Z) 


3.6) 口令检查程序 


很不幸，Solaris 上还未发布passwd+及npasswd, 这两个程序可以用于检查在UNIX 

上那些愚蠢的口令。 

 

3.7) crack 


crack可以找出/etc/shadow中那些容易猜测的口令，虽然运行crack将会使CPU的 

负载加重，但它在第一次运行时就可以给出10%系统帐号的口令。 

 

URL： （我想国内很多站点已有此程序了。） 

[ftp://sable.ox.ac.uk/pub/comp/security/software/crackers/](ftp://sable.ox.ac.uk/pub/comp/security/software/crackers/) 

 

3.8) ftp 


不用多说，使用wu-ftpd, 国内站点上有的是，如果找不到，试试：     

URL： 

[ftp://ftp.dlut.edu.cn/pub/unix/ftp/wu-ftpd/](ftp://ftp.dlut.edu.cn/pub/unix/ftp/wu-ftpd/) 

OR: 

[ftp://wuarchive.wustl.edu/packages/wuarchive-ftpd](ftp://wuarchive.wustl.edu/packages/wuarchive-ftpd) 


3.9) fix-modes 


用于纠正Solaris 2.2 ~ 2.6系统中敏感文件及目录的属性，以适应安全性需要。 

URL: 

[ftp://ftp.dlut.edu.cn/pub/unix/security/fix-modes.tar.gz](ftp://ftp.dlut.edu.cn/pub/unix/security/fix-modes.tar.gz) 

OR: 

[http://www.fwi.uva.nl./pub/comp/solaris/fix-modes.tar.gz](http://www.fwi.uva.nl./pub/comp/solaris/fix-modes.tar.gz) 


3.10) noshell 


可用于不希望登陆系统的用户的shell, 能够记录发生的事件并防止用户login. 

    

3.11) bind


标准的Solaris里带的bind有着众所周知的安全问题(参见CERT第4部份)，现在的发行版已经做

了修补。


3.12) netcat


NetCat对系统管理员和入侵者来说都是很实用的工具，它可以在两个系统间建立灵活我TCP连接。


4) (一些有用的资源--略) 


5) 如何使我的Solaris Web server更安全? 


下面的方法可以令你的以Solaris为基础的系统十分安全，你同时还可以配以利用防火墙及过滤路由

器来组成一个完整而强大的网络拓扑，但是，没有任何系统是完美的，所以你除了关注安全动态，给机

器作好防范之外，也不应该在机器上装载其他无关的第三方的软件--webserver需要的是安全，而不是

对管理员的方便。


5.0) Web server安全检查


用下面的安全检查列表来察看你的系统是否是安全地安装的，当然如果你有特殊的安全需求则不一定以此为准：


在完成一切安全设置前将系统与互联网断开

仅仅安装系统的核心部分以及需要的软件包

安装推荐的安全补丁

修改系统的开始文件来进行

在/etc/init.d/inetinit中关闭IP转发

改变/tmp的存取权限(可以在系统的开始文件中加入脚本

用ps检查进程情况

Invoke sendmail from cron to process queued mail occasionally. 

安装配置tcp_wrappers, S/Key, wu-ftp及tripwire于你的系统环境。

编辑/etc/hosts.allow来确定可进入的机器，并且编辑/etc/inetd.conf注释掉所有不需要的服务

用syslog记录下所有的telnet连接通信

Mount上的文件系统要是只读而且是no-suid的

确定/noshell是除了root之外所有不希望进入的帐号的默认shell

删除/etc/auto_*, /etc/dfs/dfstab, p/var/spool/cron/crontabs/* (except root). 

使用静态路由

测试你的系统，包括允许及拒绝访问的配置及记帐系统

考虑使用更安全版本的sendmail, syslog, bind以及crontab来替代现有的 

安装xntp来有更精确的时间戳

考虑更详细地系统记帐

保持监听和测试Web server的习惯 


在你完成上面的配置之后，你的系统已经会比安装一个标准的UNIX系统，并配以标准配置更安全了。


5.1) 硬件上......


在系统完全安装好并且配置得更安全之前，不要将它放到互联网上――从理论上说，一些入侵者喜欢

在你把系统弄得完美之前溜进去放几个后门――而且最好从CD-ROM安装你的系统并且将二进制文件

加载在磁带机或者软盘上物理写保护.......


5.2) 安装系统


从最新的，可靠的Solaris2.x版本安装，每一版本的Solaris都会比前一版更安全一些的。


Solaris是非常灵活并且包含了大量工具可供使用的。但不幸的是，这些外带的功能软件包可能也会

导致一些潜在的危险，所以要建立一个安全的系统，最好的办法是，只安装基本的OS部份，其余的软件

包则以必要为原则，非必需的包就可以不装――这样还可以使机器更快和更稳定:)


在Solaris的安装程序里，你可以选择Core SPARC installation cluster来安装，事实上，就连

这个选项都还有些东西是不必要的确良:(，但它的确是一个安全的系统基础，另一个好处是，它需要的空

间很少，看看下面你就知道了：


s0:    /         256 megabytes

s1:    swap        256 megabytes

s2:    overlap

s3:

s4:    

s5:    

s6:    /local        ??? megabytes (rest of the drive)

s7:


/var要足够大以放置审核记录文件，而swap分区则与你的硬件(内存)相适应就行了，当然大的swap

分区可以在应付DoS攻击时更强有力。


现在可以用另外的机器，ftp到sunsolve.sun.com:/pub/patches并且下载最新的推荐补丁，将它放

在磁带机中转到你的“安全主机”上，然后安装这些补丁，当然有些补丁可能安装不上，因为它所

要补的那个软件你没有安装:)


5.3) 系统里的Strip 


在Solaris下，你可以通过对/etc/rc[S0-3].d文件来修改启动时自引导的动作：


考虑移去/etc/rc2.d中在你系统中用不到的服务，我还建议你移除/etc/init.d里除下以下列表中

文件外的所有东西：


K15rrcd         S05RMTMPFILES   K15solved       S20sysetup

S72inetsvc      S99audit        S21perf         

S99dtlogin      K25snmpd        S30sysid.net    S99netconfig

K50pop3         S74syslog       S75cron         S92rtvc-config 

K60nfs.server   K65nfs.client   S69inet                     

K92volmgt       README          S95SUNWmd.sync

S01MOUNTFSYS    S71sysid.sys    S88utmpd        S95rrcd


这些文件可能会与你的不同--这取决于你机器里的图形卡/是否使用Solaris DiskSuits等等。

移除/etc/rc3.d里的文件........


举例来说，在Solaris 2.4中，你应该编辑/etc/init.d/inetinit在文件的尾部增加以下行：


ndd -set /dev/ip ip_forward_directed_broadcasts 0

ndd -set /dev/ip ip_forward_src_routed 0

ndd -set /dev/ip ip_forwarding 0


并且通过设定ndd -set /dev/ip ip_strict_dst_multihoming 1来关闭"ip_strict_dst_multihoming" 

核心变量。solaris机器就不会在两块网卡间转发IP包，这可以防止host spoof。


* 在Solaris 2.5下，只要建立一个叫/etc/notrouter的文件就能阻止IP转发，要重新打开它，只要移除

/etc/notrouter并重启动系统就行了。It's important to note that there is a small time 

window between when this file is created and when routing is disabled, 

theoretically allowing some routing to take place. 


在Solaris 2.4下,添加一个新的脚本名为/etc/init.d/tmpfix: 


#!/bin/sh

#ident  "@(#)tmpfix 1.0    95/08/14"


if [ -d /tmp ]

then

    /usr/bin/chmod 1777 /tmp

    /usr/bin/chgrp sys /tmp

    /usr/bin/chown root /tmp


并且连接/etc/init.d/tmpfix到/etc/rc2.d/S79tmpfix，这样这个脚本就会在系统启动时执行了。

这可以使入侵者更难在系统里夺取root权限。在Solaris 2.5则不必如此。


另外还有一些好的建议，就是在启动时为用户设定安全的umask，下面的script就是做这事儿的：


     umask 022  # make sure umask.sh gets created with the proper mode

     echo "umask 022" > /etc/init.d/umask.sh

     for d in /etc/rc?.d

     do

         ln /etc/init.d/umask.sh $d/S00umask.sh

     done


Note: 脚本名称中的".sh"是必需的，这样脚本才会在本shell而不是它的子shell中执行。


删除/etc/auto_*文件，删除/etc/init.d/autofs可以防止automounter在启动时就运行。


删除/etc/dfs/dfstab，清除/etc/init.d以防止机器成为NFS服务器。


删除crontab文件，你可以将/var/spool/cron/crontabs中属主root以外的文件全部删除。


使用静态路由，建立/etc/defaultrouter来维护之，以避免spoof。如果你必须通过不同的网关，考虑增

加/usr/bin/route命令于/etc/init.d/inetinit以取代运行routed。 


当地切完成时，重启机器，彻底地查看进程，ps -ef的输出应该是这样的：


     UID   PID  PPID  C    STIME TTY      TIME COMD

    root     0     0 55   Mar 04 ?        0:01 sched

    root     1     0 80   Mar 04 ?       22:44 /etc/init -

    root     2     0 80   Mar 04 ?        0:01 pageout

    root     3     0 80   Mar 04 ?       33:18 fsflush

    root  9104     1 17   Mar 13 console  0:00 /usr/lib/saf/ttymon -g -h -p myhost console login:  -T sun -d /dev/console -l co

    root    92     1 80   Mar 04 ?        5:15 /usr/sbin/inetd -s

    root   104     1 80   Mar 04 ?       21:53 /usr/sbin/syslogd

    root   114     1 80   Mar 04 ?        0:11 /usr/sbin/cron

    root   134     1 80   Mar 04 ?        0:01 /usr/lib/utmpd

    root   198     1 25   Mar 04 ?        0:00 /usr/lib/saf/sac -t 300

    root   201   198 33   Mar 04 ?        0:00 /usr/lib/saf/ttymon

    root  6915  6844  8 13:03:32 console  0:00 ps -ef

    root  6844  6842 39 13:02:04 console  0:00 -sh


/usr/lib/sendmail守护程序并没有打开，因为你不必总在25端口监听mail的列表请求，你可以在root的

crontab文件中增加：


0 * * * * /usr/lib/sendmail -q > /var/adm/sendmail.log 2>&1


这条命令要以每小时调用sendmail进程处理排队中的邮件。 


5.4) 安装第三方软件


你需要的第一个软件是TCP Wrappers软件包――由Wietse Venema写的，它提供了一个小的二

进制文件叫tcpd，能够用它来控制对系统服务的进出――比如telnet及ftp，它在/etc/inetd.conf

中启动，访问控制可以由IP地址、域名或者其它参数来限制，并且tcpd可以提升syslog的记录

级别，在系统遇到未经认证的连接时，发送email或者警告给管理员。 


然后安装S/Key来控制远程连接的安全性，可以在Q5.6中看到详细的配置方法。


如果你打算打开ftp服务(不管是匿名ftp或者是出了管理目的)，你需要取得一份WU-Archive ftp，

最好要拿到它的最新版本，否则会有一些安全漏洞存在，如果你认为需要管理员的远程登陆服务的

话，可能得修改S/Key来支持ftp daemon。在Crimelabs S/Key的发行版本中，你可以在找到

S/Key/misc/ftpd.c，这个C程序示范了如何让S/Key支持WU-Archive ftp，你可以对新版的WU-FTP

做类似的改动，当然你可能要阅读wu-ftp FAQ以增加了解。


编译并且安装了这些二进制文件后(tcpd, wu-ftpd及keyinit, keysu,keysh)，它们会被安装在

/usr/local/bin中，当编译wu-ftpd时你需要指定一个配置文件及日志的存放目录，我们推荐你将

配置文件放在/etc下，将日志文件放在/var下，Q5.7更详细地说明了wu-ftp的配置。


用/noshell来阻止那些不想让他们进入的帐号，让/noshell成为那些人的shell。这些帐号不允许登陆

并且会记录下登陆的企图，入侵者无法通过这种帐号入侵。


5.5) 限制通过网络进入系统 


telnet和ftp守护进程是从inetd进程启动的，inetd的配置文件是/etc/inetd.conf,还包含了其它

的各种服务，所以你可以干脆移去这个文件，新建一个只包括以下两行的文件：


ftp stream tcp nowait root /usr/local/bin/tcpd /usr/local/bin/wu-ftpd

telnet stream tcp nowait root /usr/local/bin/tcpd /usr/sbin/in.telnetd


当然这是基于你需要telnet及ftp的基础上的，如果你连这两个服务都不用的话，你就可以将它注释

掉或者删除，这样在系统启动的时候inetd甚至就起不来了:)


tcpd的访问控制是由/etc/hosts.allow和/etc/hosts.deny文件控制的，tcpd先查找/etc/hosts.allow

，如果你在这里面允许了某几台主机的telnet或ftp访问的话，那么deny访问就是对其它所有机器的了。

这是“默认拒绝”的访问控制策略，下面是一个hosts.allow文件的样本：


ALL: 172.16.3.0/255.255.255.0


这将允许172.16.3.0网络的主机上任何用户访问你的telnet及ftp服务，记住在这里要放置IP地址，因

为域名比较容易受到欺骗攻击…… 


现在我们准备拒绝其余所有人的连接了，将下面的语句放在/etc/hosts.deny中： 


ALL: ALL: /usr/bin/mailx -s "%d: connection attempt from %c" root@mydomain.com


这条指令不仅拒绝了其它所有的连接，而且能够让tcpd发送email给root――一旦有不允许的连接尝试

发生时。


现在你可能希望用syslog记录下所有的访问记录，那么在/etc/syslog.conf放进如下语句：


auth.auth.notice;auth.info           /var/log/authlog


注意两段语句间的空白是tab键，否则syslog可能会不能正常工作。


Sendmail将用以cron来调用sendmail来替代。


5.6) 配置S/Key 


S/Key是一个用于实现安全的一次性口令方案的软件，它根据一系列信息（包括一个秘密口令）通过MD4

处理而形成的初始钥匙，该初始钥匙再交给MD4进行处理，资助将128位的数字签名缩成64位，该64位信息

再次传给MD4函数，这个过程一直持续直到达到期望值……


开始使用S/Key时，要建立一个以/usr/local/bin/keysh为shell的帐号：

在/etc/passwd中加入


access:x:100:100:Access Account:/tmp:/usr/local/bin/keysh


并且在/etc/shadow中加入


access:NP:6445::::::


然后使用passwd access命令来设定用户的访问密码。


由于/usr/local/bin/keysh不是一个标准的shell，所以你的/etc/shells文件中内容如下：


/sbin/sh

/usr/local/bin/keysh


只有使用这两种login shell的用户才允许接入。


然后建立一个文件/etc/skeykeys并赋予一定的许可权限：


touch /etc/skeykeys

chmod 600 /etc/skeykeys

chown root /etc/skeykeys

chgrp root /etc/skeykeys


使用keyinit access命令来初始化S/Key秘密口令。


现在你可以配置允许用户通过keysu命令来成为超级用户，首先改变/etc/group:


root::0:root,access


只有在这里列出来的用户才允许通过keysu成为超级用户。现在你可以使用不着keyinit root命令来初

始化超级用户的S/Key秘密口令，我建议该口令要与user的有所区别。


本来你可以将/bin/su删掉以确定用户只能使用keysu……，但不幸的是，许多脚本使用/bin/su来开启

进程，所以你只需用chmod 500 /bin/su来改变它的权限就行了。


5.7) 配置wu-ftp 


配置wu-ftp需要经验:)，当你编译wu-ftpd时，你需要指定一个存放配置文件的地方，这个文件夹里将

包含一个pid文件夹和三个文件，一个ftp conversions文件可以是空的，但不能没有，还有ftpusers文

件包含了所有在password文件中存在但不允许登陆系统ftp的用户名称，也就是如uucp、bin之类的系统

帐号都将应该被限制。root最好是永远都被扔在这里面:)。


最后一个文件是ftpaccess：


class users real 172.16.3.*


log commands real

log transfers real inbound,outbound


这将允许从172.16.3.0的任何用户ftp而拒绝所有其它的，所有的文件与命令将被记录下来，并且存放

在你指定的记录文件目录。


至于建立匿名FTP，你要小心，因为很容易配置错误。


建立一个特殊帐户如：


ftp:*:400:400:Anonymous FTP:/var/spool/ftp:/bon/false


因为使用了chroot()功能，必须建立一个小的文件系统，包含了bin\etc\pub目录：


这里面要注意的有：


确保bin及etc下的所有文件属主都是root，且任何人不可写，只有执行权限，最好另外拷贝

一份passwd到ftp的etc中，即使被入侵者得到了，也不会泄露太多信息。


详细配置情况还需要看关于wu-ftp的faq。


5.8) 限制对文件及文件系统的存取权限


下载并使用fix-modes，这个程序会将系统里不安全的文件存取权限（文件/目录）找出来。


使用nosuid参数来配置/etc/vfstab，以防止setuid程序从UFS文件系统执行


/proc               -       /proc      proc    -   no   -

fd                  -       /dev/fd    fd      -   no   -

swap                -       /tmp       tmpfs   -   yes  -

/dev/dsk/c0t3d0s1       -       -          swap    -   no   -


/dev/dsk/c0t3d0s0 /dev/rdsk/c0t3d0s0  /       ufs  1   no   remount,nosuid

/dev/dsk/c0t3d0s4 /dev/rdsk/c0t3d0s4  /usr    ufs  1   no   ro

/dev/dsk/c0t3d0s5 /dev/rdsk/c0t3d0s5  /var    ufs  1   no   nosuid

/dev/dsk/c0t3d0s6 /dev/rdsk/c0t3d0s6  /local  ufs  2   yes  nosuid


5.9) 测试配置


重启你的机器，确定下面这些东西：


你可以从你配置为允许tcpd连接的机器telnet及ftp到你的server。


尝试从其它未被允许的机器进入，应该会拒绝并email告知当事人。


你只能以user的身份远程telnet或者ftp上站，不能以root登陆。 


用户可以通过/usr/local/bin/keysu成为超级用户。


ps -ef只有少量的进程显示，最好不要有sendmail和各种NFS进程。


touch /usr/FOO会得到错误提示，因为文件系统是ro的。


成为超级用户，将ps命令复制到/，要保持它的setuid位，然后删除它的二进制文件。


好了，祝贺你，你已经建立了一个比较安全的系统了:)


5.10) 最后：一些建议


使用XNTP来确定精确的时间。


在你把机器放到网上前，用tripwire和MD5做一个校验，如果系统被入侵，你可以通过保存的校验和

来判断哪些程序被替换掉了。


考虑使用进程记录来记来系统里占用资源的情况。


定期改变你的S/Key secrets并且选择一个好的密码，在各地方的密码最好不要一样……


-------------------------------------------------

对Solaris及网络安全我都没多少经验，不懂

的地方都是妄自猜度，错误想必不少，请指点！

mailto:quack@antionline.org
