---
title: "用LKM更改linux缺省安全等级"
date: 2000-08-05T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-39"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

用LKM更改linux缺省安全等级


作者：warning3 <warning3@nsfocus.com>

               <[http://www.nsfocus.com>](http://www.nsfocus.com>/)


Linux缺省的安全等级是0,如果将其升到1,就可以一定程度上提高系统的安全性.安全等级

为1的时候,它会禁止修改ex2fs系统中文件的immutable和append-only位,同时禁止装入

/移除module.所以我们可以先用chattr +i <file>将大部分的可执行文件,动态连接库,

一些重要的系统文件(inetd.conf,securetty,hosts.allow,hosts.deny,rc.d下的启

动script...)加上immutable位,这样"黑客"就很难在你的机器上放置木马和留后门了.

(即便他已经得到了root权限,当然通过直接硬盘读写仍然可以修改,但比较麻烦而且危险

).

"黑客"们一旦进入系统获得root,首先会清除系统的记录文件.你可以给一些系统记录文件

(wtmp,messages,syslog...)增加append-only位,使"黑客"不能轻易的修改它们.要抓

他们就容易多了.:-)

修改安全等级比较直接的办法是直接修改内核源码.将linux/kernel/sched.c中的

securelevel设成1即可.不过如果要改变安全等级的话需要重新编译内核,我太懒,不想那

么麻烦.:-)

为什么不用module呢?我写了个很简单的lkm和一个client程序来完成安全等级的切换.


方法: insmod lkm; clt -h;      


注意:普通用户也可以执行clt来切换安全等级,所以最好是在clt和lkm中加段密码检查,

如果密码不对就不允许执行.:-)        

这两个程序在Redhat 5.2(2.0.36)下编译运行通过.对于2.2.x的内核,securelevel

变成了securebits,简单的将它改到1,会连setuid()都被禁止了,这样普通用户就不能

登陆了.如果谁对2.2.x比较熟悉,请不吝赐教,共同提高嘛.:)


<在测试这些程序以前,请备份重要数据.本人不为运行此程序带来的任何损失负责.>


(一旦securelevel=1,kernel将不允许装入modlue,所以你的kerneld可能不能正

常工作，而且禁止你访问/dev/kmem,所以有些用到svgalib的程序也不能正常工作

，象zgv什么的。不过这本来就是安全隐患，所以不工作就不工作好了，呵呵)

(关于chattr,lsaddr请man chattr和man lsattr)


                                      warning3@hotmail.com


/**************************** lkm.c ********************************/


/* Simple lkm to secure Linux.

* This module can be used to change the securelevel of Linux.

* Running the client will switch the securelevel.

*

* gcc -O3 -Wall -c lkm.c

* insmod lkm                

*

* It is tested in Redhat 5.2 (2.0.36).

* (It should be modified if you want to run it in 2.2.x kernel).

* It is really very simple,but we just for educational purposes.:-)

*

*                                  warning3@hotmail.com

*/


#define MODULE

#define __KERNEL__


#include <linux/config.h>

#include <linux/module.h>

#include <linux/version.h>

#include <linux/errno.h>

#include <linux/types.h>

#include <linux/fs.h>

#include <linux/string.h>

#include <linux/mm.h>

#include <linux/proc_fs.h>

#include <asm/segment.h>

#include <asm/unistd.h>                                              

#include <linux/dirent.h>

#include <asm/unistd.h>

#include <linux/sockios.h>

#include <linux/if.h>


#define __NR_secureswitch 250


extern void *sys_call_table[];


int sys_secureswitch(int secure)

{

   if(secure==0) securelevel=0;

   if(secure==1) securelevel=1;

   return securelevel;

}


int init_module(void)

{

        sys_call_table[__NR_secureswitch] = (void *)sys_secureswitch;

        return 0;

}                  

void cleanup_module(void)

{

        sys_call_table[__NR_secureswitch] = NULL;

        return;

}


/************************ clt.c **************************/


/*


* This client can switch the secure level of Linux.


*


*   gcc -O3 -Wall -o clt clt.c


*   Usage: clt -h/-l


*              -h  switch to the high secure level.

                                                            

*              -l  switch to the low secure level.


*


*   Most of codes are ripped from smiler@tasam.com,thanks smiler.:)


*                                warning3@hotmail.com


*/


#include <asm/unistd.h>


#include <stdio.h>


#include <errno.h>


#define __NR_secureswitch 250


static inline _syscall1(int, secureswitch, int, command);


int main(int argc,char **argv)


{


        int ret,level = 0;


        if (argc < 2)


         {


             fprintf(stderr,"Usage: %s [-h/-l]\n",argv[0]);


             exit(-1);

          }


        if (argv[1][1] == 'h') level++;


        else if (argv[1][1] != 'l')


         {


             fprintf(stderr,"Usage: %s [-h/-l]\n",argv[0]);


             exit(-1);


          }


        ret = secureswitch(level);


        if (ret < 0)


                printf("Hmmm...It seemed that our lkm hasn't been loaded.;-)\n");

         else {


                if (ret == 0) {


                        puts("Now the secure level is changed to 0!\n");


                } else {


                        puts("Now the secure level is chagned to 1!\n");


                }


        }


        return(1);


}
