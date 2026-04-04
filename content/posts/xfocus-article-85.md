---
title: "TIS防火墙详述"
date: 2001-03-02T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-85"
---

文章提交：[quack](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

TIS防火墙详述

by quack(quack@antionline.org)

什么是防火墙――不知道;)

什么是TIS?――这是一组由(Trusted Information Systems)写的一组构造防火墙的工具

包，又叫firewall toolkit，这个工具箱里的软件适当的安装并配置以一定的安全策略

就可以构成基本的防火墙了,而且它是免费的;)花点心思看一看，说不定可以省下一笔不

菲的防火墙购置资金哦……

一、编译运行

1、下载

可以到TIS的web站点下载[http://www.tis.com](http://www.tis.com/)，但它有一些很麻烦的认证过程，建议

直接到国内的安全站点转转，或者到[http://packetstorm.securify.com/](http://packetstorm.securify.com/)去下载，我

得到的版本是fwtk2.1.tar.Z的版本，此后的说明均以此版本为例，且在solaris7 x86

上通过，gcc版本为2.95.2。

2、编译

# gunzip fwtk2.1.tar.Z

# tar vfx fwtk2.1.tar

# cd fwtk

将fwtk2.1.tar.Z解压后，可以在./fwtk目录下发现有很多Makefile.config.*文件，

比如你使用的操作系统是solaris2.7，那么就直接将Makefile.config更名后，把

Makefile.config.solaris更名为Makefile.config就行了。

# mv Makefile.config Makefile.config.old

# mv Makefile.config.solaris Makefile.config

在solaris下的编译相当容易――至少solaris7与solaris8下面不用修改任何东西就

可以编译通过了。

# make && make install

如果你使用的是linux，仅仅把Makefile.config.linux当成当前Makefile.config还

不够，因为如果你要使用X的gw.那么你必须有 Athena Widget的设置。否则编译会

出问题。因此，可以修改Makefile让系统不编译x-gw。

所以可以

# vi Makefile 

查找下面这行：

# directories to build executables in

DIRS=   smap smapd netacl plug-gw ftp-gw tn-gw rlogin-gw http-gw x-gw

把后面的x-gw去掉就可以了。

如果是在bsd下，特别要注意，bsd的make 不认识象：.include "Makefile.config"

这种格式，因此，在bsd下要用TIS提供的fixmake来处理。或者用指定

CC＝    gcc

COPT=   -g -traditional -DBSDI

来适应bsd系统――比如我的FreeBSD3.4。

如果在编译过程中有出现sys_errlist的定义声明出错，那么要修改原程序，比如：

exter char *sys_errlist[];

把该行注释掉。

如果出现"Undefined symbol `_crypt' referenced from text segment"错误，则

看在你的Makefile.config中AUXLIB设置是否有"-lcrypt"。

如果还有问题……我懒得翻译那么多东西了，你可以到下面的URL看看：

[http://fwtk.netimages.com/fwtk/faq/](http://fwtk.netimages.com/fwtk/faq/)

这里列出了人们在编译及使用tis时遇到的一些常见问题。

二、配置前的准备工作

1、理解一些概念

a、wrapper

我的理解，wrapper应该是一个包装程序，说白了和那些login什么的后门没本质区别;)

比如说tcpd吧，我们用它来守护一些网络服务守护进程，比如，在超级服务守护进程

inetd的配置文件中，我们可以将

finger stream tcp nowait nobody /usr/etc/in.finger  in.fingerd

这一句替换掉，用tcpd来包装

finger stream tcp nowait nobody /usr/etc/tcpd  in.fingerd

发送一个HUP信号给inetd让它重启后，tcpd就发生作用了，如果此时收到一个对主机的

finger请求，tcpd便启动，先检查访问控制的配置文件，也就是/etc/hosts.allow和

/etc/hosts.deny，如果允许访问，再启动真正的finger守护进程去处理该请求。

怎么样，和login的后门相比原理是不是相同的？比如ulogin.c吧，是将真正的login改

名备份到另一个地方，用假的login包装起来，收到login请求时，先判断访问者是不是

有设置DISPLAY的环境变量，如果该变量和password相同的话，则启动/bin/sh，如果没

有，则以正常的login来响应该请求……哎，这是题外话，不说了……

b、gateway

应用级网关(Application Level Gateways)是在网络应用层上建立协议过滤和转发功能。

它针对特定的网络应用服务协议使用指定的数据过滤逻辑，并在过滤的同时，对数据包

进行必要的分析、登记和统计，形成报告。

呵，这种教材似的东西看着是不是觉得难理解，看了半天不知所云？其实在TIS下面，它

的各种gw比如tn-gw，是控制telnet的，当你连接到tn-gw运行的端口时，它会出现一个

自己的提示符……如下：

C:\>telnet 192.168.0.2

然后telnet窗口将出现

hi,i'm quack,welcome to my 3cr19TkI7's website! <------------这是我的tn-welcome.txt

tn-gw->                                                      它会在在连接时显示……

当我键入问号寻求帮助时，会有如下的提示信息…… 

tn-gw->?

Valid commands are: (unique abbreviations may be used)

   connect hostname [serv/port]

   telnet hostname [serv/port]

   x-gw [hostname/display]

   help/?

   password

   timeout seconds

   quit/exit

tn-gw->

看明白了吗，唔，没错，它提供的是穿越这台防火墙主机对其它机器的telnet访问;)

tn-gw-> telnet 192.168.0.2 55555

Trying 192.168.0.2 port -9981...

Connected to 192.168.0.2.

SunOS 5.7

login: quack

Password:

Last login: Fri Jun  9 00:27:48 from 192.168.0.1

Sun Microsystems Inc.   SunOS 5.7       Generic October 1998

Cracker%  

这下清楚了吧……稍安勿燥，后面我将说明这是如何配置的。 

c、proxy

代理服务(Proxy Service)也称链路级网关或TCP通道(Circuit Level Gateways or TCP 

Tunnels)，也有人将它归于应用级网关一类。它是针对数据包过滤和应用网关技术存在

的缺点而引入的防火墙技术，其特点是将所有跨越防火墙的网络通信链路分为两段。防

火墙内外计算机系统间应用层的"链接"，由两个终止代理服务器上的"链接"来实现，外

部计算机的网络链路只能到达代理服务器，从而起到了隔离防火墙内外计算机系统的作

用。此外，代理服务也对过往的数据包进行分析、注册登记，形成报告，同时当发现被

攻击迹象时会向网络管理员发出警报，并保留攻击痕迹。

2、文件介绍

默认的安装，TIS是安装在/usr/local/etc目录下的，现在我们来看看里面都有些什么吧

# cd /usr/local/etc

# ls -la

总数1092

drwxr-xr-x   2 root     other        512  6月  6 17:05 .

drwxr-xr-x  11 root     other        512  6月  6 17:02 ..

-rwxr-xr-x   1 root     other      17012  6月  6 17:05 authdump

-rwxr-xr-x   1 root     other      18752  6月  6 17:05 authload

-rwxr-xr-x   1 root     other      23132  6月  6 17:05 authmgr

-rwxr-xr-x   1 root     other      47500  6月  6 17:05 authsrv

-rwxr-xr-x   1 root     other      50952  6月  6 17:05 ftp-gw

-rwxr-xr-x   1 root     other     117712  6月  6 17:05 http-gw

-rwxr-x---   1 root     other        362  6月  6 17:05 mqueue

-rwxr-xr-x   1 root     other      26820  6月  6 17:05 netacl

-rw-r--r--   1 root     other       3101  6月  6 17:05 netperm-table

-rwxr-xr-x   1 root     other      30308  6月  6 17:05 plug-gw

-rwxr-xr-x   1 root     other      45892  6月  6 17:05 rlogin-gw

-rwxr-xr-x   1 root     other      31436  6月  6 17:05 smap

-rwxr-xr-x   1 root     other      28772  6月  6 17:05 smapd

-rwxr-xr-x   1 root     other      49940  6月  6 17:05 tn-gw

-rwxr-xr-x   1 root     other      44792  6月  6 17:05 x-gw

一个一个来解释吧……

  a.authdump:这是对TIS认证数据库进行管理的工具，它可以在数据库中建立信息的

    ASCII文本形式的备份。其中的密码是加密后输出的。

  b.authload:也是认证数据库管理工具，它对数据库中的单个记录进行处理，这个命

    令在你需要向数据库中添加一组条目或者需要在两个站点之间共享数据库时特别有

    用。

  c.authmgr:网络认证的客户程序，它是与认证方authsrv的接口。是用来访问网络上

    的认证服务器或者加密连接时用的。

  d.authsrv:第三方网络认证守护程序，它提供了多种谁形式的综合接口，比如口令、一

    次性口令或者令牌认证系统，它里面有一个包含用户和组记录的数据库，并且还有一个

    管理接口，允许一个获得认证的管理员管理本地或网络上的用户记录。后面会说它的

    配置的。

  e.ftp-gw:

    它是带有日志记录和访问控制的可以穿越的FTP代理服务。

  f.http-gw:

    带有日志记录和访问控制的gopher和http代理服务。

  g.mqueue:

    不知是不是message queue?不太懂……:(

  h.netacl:

    TCP网络访问控制，由inetd调用，对各种服务提供包装。

  i.netperm-table:

    所有各种服务的配置文件。

  j.plug-gw:

    通用的一个tcp连接代理服务程序。

    

  k.rlogin-gw:

    这是提供穿过rlogin的代理服务――r系统服务的危险大家是都知道的了，如果非要不

    可，用它来提供包装吧

  l.smap:

    sendmail包装程序――客户端，它实现了smtp的最小版本，接受来自网络的消息，并

    发给smapd由它作进一步传送，它一般是运行在chroot下的。

  m.smapd:

    sendmail包装程序――守护程序，它通过定期扫描由smap维护的邮件缓冲池区域并转

    发搜集和保存在那里的任意消息。

  n.tn-gw:

    telnet的代理服务器。

  o.x-gw:

    X网关服务器。

3、系统准备

  a.去除IP转发

    

    你的机器有两块网卡么？

    如果你不想你的防火墙轻易被人穿越，就得老老实实把IP转发功能干掉，因为IP转发

    会导致从一个接口接收到的报文重新转发到所有其它适用的接口――一般去除IP转发

    可能要重新配置内核。

    默认情况下，如果Solaris机器有超过一块的网卡的话，它将会在不同网卡间转发数

    据包，这一行为可以在/etc/init.d/inetinit中得到控制。要在Solaris 2.4或者更

    低版本机器下关闭它，可以将ndd -set /dev/ip ip_forwarding 0添加于

    /etc/init.d/inetinit的未尾。在Solaris 2.5中，只要touch /etc/notrouter. 

    如果是SunOS4.1x，则在内核运行adb，在核心配置文件中加入

    options "IPFORWARDING=-1"并重新编译生成新的内核。

    至于linux，你试着make menuconfig，找到IP:forwarding/gatewaying，将

    CONFIG_IP_FORWARD关掉，重新编译即可。其它的类似吧，自己琢磨琢磨，我也不会;)

    

  b.移除/etc/inetd.conf及/etc/rc2.d/内不必要的服务

    首先可以用

    # ps -elf

    看看系统启动时启动的服务

    你可以暂时先把/etc/inetd.conf内的所有服务都屏蔽掉――在每一项前面加上#号使其

    失效――因为稍后我们将用netacl或者各种*-gw来包装这些服务――启动的inetd.conf

    总是要改的;)

    并非所有的进程都是由inetd这一超级服务器守护进程来启动的，有一些直接在rc2.d里

    定义，直接在系统启动时就运行，如果你有运行下列服务的话，最好也关掉：

    pcnfsd      

    rwhod

    mountd

    protmap

    sendmail

    named

    printer

    timed

    nfsd

    rstatd

    xntpd

    nfsiod

    有些服务的关闭可能会影响系统服务，需要你自行分析了……。   

三、配置

1、netperm-table

这是防火墙工具箱里所有东西――netacl,smap,ftp-gw,tn-gw,plug-gw等的配置文件，

当一个应用被启动时，它就会从netperm-table中读取出自己相关的配置和许可信息的

策略文件。下面把默认安装后的netperm-table贴出来――它有许多注解的

#

# netperm配置表的示例文件

#

# 要更好地利用地这个netperm-table，最好把你的主机名用IP地址来替代

# (e.g.; 666.777.888)，这样比较不容易受到DNS欺骗的侵害。

#

# netacl示例规则:

# ---------------------

# 下面两行的注释如果去掉，将启动telnet

#netacl-telnetd: permit-hosts 127.0.0.1 -exec /usr/libexec/telnetd

#netacl-telnetd: permit-hosts YOURADDRESS 198.6.73.2 -exec /usr/libexec/telnetd

#

# 下面这行是tn-gw的

#netacl-telnetd: permit-hosts * -exec /usr/local/etc/tn-gw

#

# 下面是rlogin

#netacl-rlogind: permit-hosts 127.0.0.1 -exec /usr/libexec/rlogind -a

#netacl-rlogind: permit-hosts YOURADDRESS 198.6.73.2 -exec /usr/libexec/rlogind -a

#

# rlogin-gw的配置

#netacl-rlogind: permit-hosts * -exec /usr/local/etc/rlogin-gw

#

# 要将finger使能，把下面两行的注释去掉

#netacl-fingerd: permit-hosts YOURNET.* -exec /usr/libexec/fingerd

#netacl-fingerd: permit-hosts * -exec /bin/cat /usr/local/etc/finger.txt

# smap规则示例:

# -------------------

smap, smapd:    userid 6

smap, smapd:    directory /var/spool/smap

smapd:          executable /usr/local/etc/smapd

smapd:          sendmail /usr/sbin/sendmail

smap:           timeout 3600

# ftp gateway 规则示例:

# --------------------------

#ftp-gw:        denial-msg      /usr/local/etc/ftp-deny.txt

#ftp-gw:        welcome-msg     /usr/local/etc/ftp-welcome.txt

#ftp-gw:        help-msg        /usr/local/etc/ftp-help.txt

ftp-gw:         timeout 3600

# uncomment the following line if you want internal users to be

# able to do FTP with the internet

#ftp-gw:                permit-hosts YOURNET.*

# uncomment the following line if you want external users to be

# able to do FTP with the internal network using authentication

#ftp-gw:                permit-hosts * -authall -log { retr stor }

# telnet gateway规则示例:

# -----------------------------

#tn-gw:         denial-msg      /usr/local/etc/tn-deny.txt

#tn-gw:         welcome-msg     /usr/local/etc/tn-welcome.txt

#tn-gw:         help-msg        /usr/local/etc/tn-help.txt

tn-gw:          timeout 3600

tn-gw:          permit-hosts YOURNET.* -passok -xok

# if this line is uncommented incoming traffic is permitted WITH

# authentication required

#tn-gw:         permit-hosts * -auth

# rlogin gateway规则:

# -----------------------------

#rlogin-gw:     denial-msg      /usr/local/etc/rlogin-deny.txt

#rlogin-gw:     welcome-msg     /usr/local/etc/rlogin-welcome.txt

#rlogin-gw:     help-msg        /usr/local/etc/rlogin-help.txt

rlogin-gw:      timeout 3600

rlogin-gw:      permit-hosts YOURNET.* -passok -xok

# if this line is uncommented incoming traffic is permitted WITH

# authentication required

#rlogin-gw:     permit-hosts * -auth -xok

# auth server and client的规则示例

# ------------------------------------

authsrv:        hosts 127.0.0.1

authsrv:        database /usr/local/etc/fw-authdb

authsrv:        badsleep 1200

authsrv:        nobogus true

# clients using the auth server

*:              authserver 127.0.0.1 7777

# X代理的规则：

tn-gw, rlogin-gw:       xforwarder /usr/local/etc/x-gw

一头雾水是吧……我来归结一下……

  a.每一条规则都是按照要使用该规则的程序的名字开头，后跟一个冒号，当程序读

    取时也只读取其相关的规则。

  b.多个应用可以共用一条规则，各应用名字用逗号隔开或者用星号来通配――当然

    我不建议你这么做，这样简单是简单了，但维护或者阅读起来会比较烦。

不多说了，在各种服务中再慢慢谈配置吧。

2、netacl

这里我示例配置用netacl包装telnet以及ftp守护程序

首先我们在/etc/inetd.conf里添上下面两行――记得吗，前边我们disable了它们了;)

ftp     stream  tcp     nowait  root    /usr/local/etc/netacl   in.ftpd

telnet  stream  tcp     nowait  root    /usr/local/etc/netacl   in.telnetd

这根据你自己的不同来决定，比如你的守护进程是ftpd和telnetd，把in.ftpd及in.telnetd改

成它们好了。然后ps -ef|grep inetd找出进程号后发送HUP信号重启。

修改/usr/local/etc/netperm-table中相关条目如下：

# telnet rules:

netacl-in.telnetd:  permit-hosts 192.168.0.1 -exec /usr/sbin/in.telnetd

#这里我只允许从192.168.0.1这台机器telnet上来，所以连localhost都不行:)

netacl-in.telnetd:  deny-hosts unknow

#要注意这条信息哦，这是防止网络中恶意用户的IP spoof 的办法

#这样，你就可以让地址192.168.0.2 telnet到你机器上 ，而除了它之外的所有地址

#会被显示一条警告信息。最后一条保证了如果你主机的IN.APPR.ARPA反向DNS查询主机

#名错误的时候，该不知名的远程机器无法telnet进来。(DNS spoof)

netacl-in.telnetd:  permit-hosts * -exec /bin/cat /usr/local/etc/notelnet.txt

#这条会在不允许登陆时显示一条信息――你可以自己编辑内容。

#

# Ftp Rules:

netacl-in.ftpd: permit-hosts 127.0.0.1 -exec /usr/sbin/in.ftpd

#这条只允许本地机器localhost的ftp其它都被拒绝

netacl-in.ftpd: permit-hosts * -exec /bin/cat /usr/local/etc/noftp.txt

#对被拒绝的机器显示这一信息

OK,现在我们来测试一下我们的配置是否正常工作……

我从192.168.0.1上telnet目标机器192.168.0.2

SunOS 5.7

login: ronin

Password:

Last login: Sat Jun 10 18:00:34 from 192.168.0.1

Sun Microsystems Inc.   SunOS 5.7       Generic October 1998

Cracker%           

唔，正常得很，看看阻塞的规则是否工作吧，我们就从localhost telnet本地吧……

Cracker% telnet localhost

Trying 127.0.0.1...

Connected to localhost.

Escape character is '^]'.

here is notelnet.txt file,means you can't access this host. <---我的notelnet.txt内容

Connection closed by foreign host.

Cracker% 

FTP的测试也是类似的，就不再多说了……

总结netacl的规则有如下表达：

permit-host  ip/hostname            指定允许主机

deny-host    ip/hostname            指定拒绝主机，被拒绝的主机会被syslogd记录

-exec executable[args]              为处理服务而激活的程序

-user userid                        程序启动时的身份――以root或者nobody等等

-chroot  rootdir                    标识在调用服务程序前的chroot目录

3、认证系统：

对于这个认证系统，也同样要编辑/etc/services，添加

authsrv         3333/tcp

然后在/etc/inetd.conf中加入一行

authsrv stream  tcp     nowait  root    /usr/local/etc/authsrv  authsrv

# ./authsrv             <-----------------运行authsrv

authsrv# ?              <-----------------它就跳出来authsrv#字样，我要看帮助，

                                          键?，得到下面的输出

                                          

Command List:

(Commands may be invoked with unique leading abbreviation)

authorize username [comment]

authenticate username

response <text>

quit

exit

display username

adduser username [fullname]      <----------添加用户

deluser username

enable username [onetime]        <----------给用户使能

disable username

password [username] passwordtext <----------设密码

passwd [username] passwordtext

proto username protoname         <----------标志用户使用的认证协议

group username groupname         <----------设组别

rename username newname [fullname]

wiz username

unwiz username

superwiz username

operation group/user username command dest [tokens]

list [group]

ls [group]

?

help

authsrv# adduser wlj      <--------------我在加用户了

ok - user added initially disabled

authsrv# password wlj wlj  <-------------设密码,xixi,passwd=username,so easy to crack

Password for wlj changed.

authsrv# group wlj other   <-------------设组别 

set group

authsrv# enable wlj        <-------------使能

enabled

authsrv# wiz wlj

set group-wizard

authsrv# superwiz wlj

set wizard

authsrv# ls                <-------------现在看看……

Report for users in database

user       group      longname      status proto      last

----       -----      --------      ------ -----      ----

user                                  n    passw      never                   

wlj        other                      y G  passw      never 

搞定了这个就可以试试authmgr的情况了……  

前面提到的authmgr这个客户程序则是用法如下：

Cracker# ./authmgr

Connected to server

authmgr-> login

Username: wlj

Password: 

Logged in

authmgr-> list

Report for users in database

user       group      longname      status proto      last

----       -----      --------      ------ -----      ----

admin      root                       y W  passw      never                   

wlj        other                      y G  passw      Sat Jun 10 11:26:18 2000

authmgr-> 

至于认证服务器也有它的规则，比如我的机器上的是这样的：

# Example auth server and client rules

# ------------------------------------

authsrv:        hosts 127.0.0.1

authsrv:        database /usr/local/etc/fw-authdb

authsrv:        badsleep 1200

authsrv:        nobogus true

# clients using the auth server

*:              authserver 127.0.0.1  3333

说说它的规则吧……关于authsrv可以有下面的规则项：

database pathname        指定authsrv数据库的数径

nobogus true             当用户认证失败返回一个友好的错误消息

badsleep seconds         对尝试口令的登陆的限制

userid name              指定authsrv运行的PID

hosts host-pattern[key]  跟加密有关的了

operation user id telnet-gw host    +

                                    +――――>存储在netperm-table中的操作规则 

                                    |

operation user id ftp-gw host put   +

怎么样，看得明白么？我写得太乱，但实在表达不好;(不明白的话自己查帮助吧……

4、ftp-gw

现在要来配置ftp代理了，一般情况下，你可能希望既运行ftp代理又运行正常的ftp服务，

这样要对几个文件进行处理，首先编辑/etc/services，加入以下行：

ronin           4444/tcp

然后在文件/etc/inetd.conf中把与FTP相关的行改为如下：

ftp     stream  tcp     nowait  root    /usr/local/etc/ftp-gw   ftp-gw

ronin   stream  tcp     nowait  root    /usr/local/etc/netacl   in.ftpd

其中第二行的意思是配合/etc/services文件，将普通ftp端口移至4444，并以netacl包装。

而第一行就是我们的ftp-gw了。

重启进程后，用端口扫描可以看到4444端口是打开的，可以直接连通。

我们现在应该来配置ftp-gw的规则了――打开文件/usr/local/etc/netperm-table:

# Example ftp gateway rules:

# --------------------------

ftp-gw: denial-msg      /usr/local/etc/ftp-deny.txt

# 对拒绝访问者的信息

ftp-gw: welcome-msg     /usr/local/etc/ftp-welcome.txt

# 欢迎信息

#ftp-gw:        help-msg        /usr/local/etc/ftp-help.txt

ftp-gw:         timeout 3600

# 这里设定超时的时间

# uncomment the following line if you want internal users to be

# able to do FTP with the internet

#ftp-gw:                permit-hosts YOURNET.*

ftp-gw:         hosts 192.168.0.*

# 允许192.168.0.*的这些机器登陆 

ftp-gw:         authserver    localhost   3333

# 认证服务器是本地机器，端口为3333 <---------刚才在认证服务中定义的

它的程序规则如下：

userid user             指定了用户ID

directory pathname      ftp-gw之前的chroot目录

denial-msg filename     访问拒绝时显示的文件

welcome-msg filename    欢迎信息文件

help-msg filename       帮助信息文件

denydest-msg filename   受限制的访问显示文件

timeout secondvalue     超时设置

主机访问选项如下：

-dest pattern                        标志一个有效目标

-dest {pattern1 pattern2……}        标志一组有效目标

-auth                                说明代理要求用户出示有效ID证明才允许使用

-passok                              如果来自受托主机，则允许修改口令

下面我们来验证一下，先ftp到4444的netacl控制端口……

C:\>ftp

ftp> o 192.168.0.2 4444

Connected to 192.168.0.2.

sorry, you can't allow to access the ftp site!   <-------定义的noftp.txt……

Connection closed by remote host.

ftp>

阻塞规则起作用了……

然后来试试代理吧：

C:\>ftp 192.168.0.2

Connected to 192.168.0.2.

220 i am quack, welcome ^&^

User (192.168.0.2:(none)): wlj@localhost <---------记得我刚才输入的认证用户么？

331-(----GATEWAY CONNECTED TO localhost----)

331-(220 i am quack, welcome ^&^)

331 Enter authentication password for wlj

Password:

230 User authenticated to proxy

ftp>

成功连接了……至于允许及阻塞的规则――自己制订去吧。

5、tn-gw

和配置FTP没有什么两样，编辑/etc/services、/etc/inetd.conf、

/usr/local/etc/netperm-table等文件，定义好端口、规则……就不多说了。

6、plug-gw\rlogin-gw\http-gw\x-gw:这些代理的配置也大同小异，读者可以自行研究。

7、smap\smapd:至于这个，我没有配sendmail，也懒得弄了――没有尝试不敢胡说……

四、附加工具包

在tis的./tools/目录有一些管理工具，利用它们可以完成一些系统管理功能，

但是，可能是下载的版本的原因吧，我在packetstorm下载到的版本无法直接编译安

装通过，问题有二，一是./tools/server/下有个syslog，得改成syslogd，还有就

是make install时工具没法装到正确的目录，你可以修改一下Makefile或者干脆自

已动手拷贝――还要快些:)

这些工具如下：

./tools/admin/

1、flog 

这个东西是监视某一log文件的实时变化的工具，作者自述在控制台工作时经常运行

tail -f /usr/adm/syslog来实时察看log文件的变化，以确定系统的运行情况，而

flog是一个更加聪明的工具――你可以简单地键入flog&来运行它，默认情况下它察

看的是/var/log/messages――你可以在编译的时候自己定义它。

或者你可以用flog /var/log/auth.log&来察看其它的文件。

2、portscan

这东东似乎没必要多说――任谁看portscan也知道是个端口扫描工具了……

usage: portscan [-l low port] [-h high port] [-v] host

最简单直接的就是：./portscan localhost了……确定现在有哪些端口在提供服务。

如果用-v host参数也会得到一个冗余的输出――每个端口打印一个小圆点……通过

这个输出你可以判断它是不是还在跑……

3、netscan

这是一个网络ping程序，它将网络地址做为参数接受，并且ping该网络中的每个地址。

它的缺省输出是一组响应ping的地址列表及对应的主机名字。比如你可以用下面方式

运行：

# ./netscan 202.101.103

它会依次ping每个地址，并将有响应――就是存活的主机返回。

它还可以以冗余方式运行。在这种方式下，响应ping的地址与其名字放在一起或者左对

齐，没有响应的地址则会缩排，以tab方式缩进一个制表空格。可以用

# ./netscan -v 202.101.103 

得到冗余方式的输出。

4、progmail

    这是一个简单的发送邮件的程序，要安装它，你可以将它拷贝到/usr/local/etc/中，

然后修改sendmail.cf中的行：

Mprog,  P=/bin/sh,   F=lsDFMeuP,  S=10, R=20, A=sh -c $u

    将其改为:

Mprog,  P=/usr/local/etc/progmail,   F=lsDFMeuP,  S=10, R=20, A=sh -c $u

5、reporting

# ls -la

-rw-r-----   1 ronin    other       2126 1994  11月  5 authsrv-summ.sh

-rw-r-----   1 ronin    other        962 1994  11月  5 daily-report.sh

-rw-r-----   1 ronin    other       4799 1996  11月 27 deny-summ.sh

-rw-r-----   1 ronin    other       2757 1994  11月  5 ftp-summ.sh

-rw-r-----   1 ronin    other       2796 1994  11月  5 http-summ.sh

-rw-r-----   1 ronin    other        247 1994  11月  5 login-summ.sh

-rw-r-----   1 ronin    other       2048 1994  11月  5 netacl-summ.sh

-rw-r-----   1 ronin    other       2017 1994  11月  5 smap-summ.sh

-rw-r-----   1 ronin    other       2256 1994  11月  5 tn-gw-summ.sh

-rw-r-----   1 ronin    other        960 1994  11月  5 today-report.sh

-rw-r-----   1 ronin    other        962 1994  11月  5 weekly-report.sh

这些东西不言而明是shell script写成的日志统计工具了，自己看看代码吧……

然后在client及server目录下还有以下工具――作个简略介绍吧：

ftpd            - a version of ftpd that uses the auth server

login-sh        - a login shell wrapper that uses the auth server

                  (see the man pages)

syslog          - a version of the 4.3bsd syslog that uses regexps

gate-ftp        - If invoked as "gate-ftp", the environment variable FTPSERVER is

                  searched for, and is contacted as a proxy ftp gateway. Autologin in done

                  through the proxy. If FTPSERVERPORT is set, that is used as the port

                  number for the gateway server.

tn              - a simple "expect" script that handles telnetting out through

                  the proxy automatically

好了，很久没打过这么多的字了……手酸死了……

结论：上面说了这么多，其实只是说明一些基本的配置，至于你自己的网络如何用这一防火

墙来将入侵者阻挡于大门之外，这需要你自行分析你的安全策略、网络结构等等再灵活地运

用这些防火墙工具及规则来确保安全。

附1、一些tip 译自fwtk faq 一文

1、我如何在toolkit里使用S/KEYS?

First, you must obtain the SecureID library from Axent Technologies (Security Dynamics)

or the Skey library.  In order to compile the SecureID with the toolkit, change the

"tis_sd_init" reference in securid.c to "sd_init". The "tis_" variant is a TIS fix that

ships with Gauntlet since the SecurID software won't work well with multi-homed hosts. 

For both, you need to edit the Makefile in the auth directory for the proper modules to be 

compiled and linked. Remove the "#" from the "SKEYDIR=" (etc..) lines and re-make. 

#if you are using the SKEY modules, define SKEYDIR to be the source 

#directory where the SKEY libraries and include files are. 

#SKEYDIR=../../skey 

#SKEYINC= -I$(SKEYDIR) 

#SKEYLIB= $(SKEYDIR)/libskey.a 

#SKEYOBJ= skey.o 

#if you are using the SecurID module, define SECURDIR to be the source 

#directory where the SecurID libraries and include files are. 

#SECURDIR= /var/ace/client 

#SECURLIB= $(SECURDIR)/sdclient.a $(FWLIB) #SECURINC= -I$(SECURDIR) 

#SECUROBJ= securid.o

2、 我如何在netperm-table指定一个子网掩码? 

使用如"network-number:netmask"之类的格式，下面是示例: 

    111.222.0.0:255.255.0.0 

这一特性在FWTK 2.x以上的版本才有效哦。

3、为什么当我要打开proxy时得到"inetd: xxx-gw/tcp: unknown service"的错误提示?

这表示在你/etc/inetd.conf中要打开的服务与/etc/services中定义的有冲突。

举例来说，你的inetd.conf文件中有如下行：

    ftp-gw stream tcp nowait root /usr/local/etc/ftp-gw ftp-gw 

最后就是指服务――service的名乐，把它改为ftp就OK了。

如果你运行的是Solaris 2.x,可能还要参考/etc/nsswitch.conf文件。

  

  

4、我如何将FWTK的log文件与其它标准syslog文件隔开?

可以编辑firewall.h:

找到下面的行: 

#define LFAC LOG_DAEMON 

   替换为 

#define LFAC LOG_LOCAL6 

然后将： 

    local6.* /var/log/fwtk 

扔到syslog.conf里面去，然后把类似下面这行的东东干掉

*.info;local6,mail.none  /var/log/messages 

当然，在你的netperm-table里面要用-log的选项打开记录功能哦。

5、我如何为不同的服务建立分开的log文件? 

按照如下形式来编辑你的/etc/syslog.conf文件吧――具体内容可以参看syslog.conf的

man page。

# patterns to match for 

"authsrv"                    /home/log/auth 

"netacl.*fingerd"        /home/log/in-fingerd 

"netacl.*telnetd"        /home/log/in-telnetd 

"smap"                      /home/log/smap 

"ftp-gw"                    /home/log/ftp-gw 

"plug-gw"                  /home/log/plug-gw 

"rlogin-gw"                /home/log/rlogin-gw 

"tn-gw"                     /home/log/tn-gw 

# Standard system logs 

*.emerg;*.alert;*.crit;*.err;*.warning;*.notice;*.info;*.debug  /var/adm/messages 

*.emerg                                         * 

*.emerg;*.crit                                  /dev/console

最后，发送HUP信号给syslogd来重启进程就OK了。 

附2、一些相关术语(摘自防火墙的选型、配置、安装和维护一书)

1、防火墙(firewall)：在被保护网络和因特网之间，或在其它网络之间限制访问的一种

   或一系列部件。

2、主机(host)：连接到网络上的计算机系统，它可以是各种类型的机器，如SUN工作站，

   PC或者IBM主机等等，也可以运行不同的操作系统。

3、堡垒主机(bastion host)：它是一种被强化的可以防御进攻的计算机，被暴露于因特

   网之上，作为进入内部主机的一个检查点。通常情况下，堡垒主机上运行一些通用的操作

   系统。

4、双宿主主机dual homed host)：有两个网络接口的主机。

5、屏蔽路由器(screened router)：可以根据过滤原则对数据包进行阻塞和转发的机器。

6、屏蔽主机(screened host)：被放置到屏蔽路由器后面的网络上的主机，主机能被访

   问和程度取决于路由器的屏蔽规则。

7、屏蔽子网(screen subnet)：位于屏蔽路由器后面的子网，子网能被访问的程度取决

   于屏蔽规则。

8、代理服务器(proxy server)：一种代表客户和真正服务器通信的程序。典型的代理接受

   用户的客户请求，然后决定用户或用户的IP地址是否有权使用代理服务器(也可能支持其它

   的认证手段)，然后代表客户与真正服务器之间建立连接。

9、IP欺骗(ip spoofing)：这是一种黑客的攻击形式，黑客使用一台机器，而用另一台机

   器的IP地址，从而装扮成另一台机器与服务器打交道。例如，一个防火墙不允许某一竞争

   站点访问该站点，但竞争站点可以使用其它站点的IP和服务器通信，而服务器则不知道与

   它通信的机器是竞争站点的主机。

10、DNS欺骗(DNS spoofing)：通过破坏被攻击机上的名字服务器缓存，或破坏一个域名

    服务器来伪造IP地址和主机名的映射，从而冒充其它机器。

11、隧道路由器(trnneling router)：它是一种特殊的路由器，可以对数据包进行加密，

    让数据能通过非信任网，如因特网，然后在另一端用同样的路由器进行解密。

12、虚拟私用网(Virtual Private Network,VPN)：一种连接两个远程局域网的方式，

    连接要通过非信任网，如因特网，所以一般通过隧道路由器来实现互联。

13、差错与控制报文(ICMP)：这是TCP/IP协议中的一种，建立在IP层上，用于主机之间或

    主机在路由器之间传输错误报文以及路由建议。

14、纵深防御(Defense in Depth)：一种确保网络尽可能安全的安全措施，一般与防火墙

    联用。

15、最小特权(Least Privilege)：在运行和维护系统中，尽可能地减少用户的特权，但同

    时也要使用户有足够的权限来做事，这样就会减少特权被滥用的机会。内部人员滥用特权

    很可能在防火墙上打开一个安全缺口，这很危险，很多的入侵是由此引起的。

16、数据包过滤(package filtering)：一些设备，如路由器、网桥或单独的主机，可以有

    选择地控制网络上来往的数据流。当数据包要经过这些设备时，这些设备可以检查数据包

    的相应位，根据既定的原则来决定是否允许数据包通过。有时这也被称作屏蔽。

====================

错漏难免，请高手赐教
