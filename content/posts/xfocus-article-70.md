---
title: "用SSL构建一个安全的Apache"
date: 2001-03-02T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-70"
---

(quack_at_xfocus.org)

用SSL构建一个安全的Apache


by quack

参考资料：Installing and Securing the Apache Webserver with SSL


一、简介


这篇文章要说明的是如何将阿帕奇与SSL(Secure Socket Layer)结合起来安装

配置。众所周知，在网络上以明文传递敏感信息是相当不安全的，因此SSL提供

了一种加密手段，在底层上为上层协议提供服务和加密方案，因此当用户在以

HTTP协议传输数据时，窥探者将难以获取数据的信息。当然加密只是在传输过程

中的，对用户是完全透明的。                                    ^^^^^^^^


那么就开始吧……


二、准备工作


如果你的系统是从头装起的话，建议你留出一个叫/chroot的分区用来运行Apache。

至于这个分区的大小，取决于你自已，一般来说，一个普通的网站有40M也就够了。

但你的系统如果早就运行了Apache，你可以另外开辟一个分区，或者选择不用独立

分区来安装，仅仅在根下面开一个目录。


另外我假定你的系统已经通过了一定的安全检测――在安装Apache之前(如果有其它

漏洞存在的话，你认为运行在其上的Apache会怎样，所谓覆巢之下，焉有完卵:),检

测至少要包括(但不仅限于)――移除不安全的SUID程序、升级某些守护进程，去掉不

必要的服务。还假定你是的WEB SERVER是运行TCP/IP而且有自己的地址。


三、平台


以下测试都在下列平台下通过: 


1、Slackware 4.x distribution using gcc 2.7.2.3 and Perl v5.005_02


2、Solaris 7 on Sparc using gcc v2.8.1 and Perl v5.005_03 


四、获取所需要的软件


因为阿帕奇并没有在她的包里自己SSL，因此我们必须先下载到这些加密网页所必需的

部份：


1、Apache Web Server - [http://www.apache.org/dist/](http://www.apache.org/dist/)


不必多说，我们当然需要获得这个web server，现在的版本是1.3.11，阿帕奇是现在世界

上使用最广泛的web server。


2、mod_ssl - [http://www.modssl.org](http://www.modssl.org/)


这是一个为Apache1.3.x web server提供强力加密的的软件模块，它使用的是SSL v2和v3

以及TLS(Transport Layer Security)v1 协议。该软件包是在BSD的license下开发的，在

非商业的情况下，你可以自由地使用它，要判断该使用哪一个版本的mod_ssl很简单，它的

版本号是<mod_ssl-version>-<apache-version>格式的，也就是说，你如果用的是1.3.11

的Apache,那么就该用2.50-1.3.11的mod_ssl。


3、mod_perl - [http://perl.apache.org/dist/](http://perl.apache.org/dist/)


4、Open SSL - [http://www.openssl.org](http://www.openssl.org/)


这一软件包提供了SSL v2/v3(Secure Sockets Layer)及TLS v1(Transport Layer Security)

协议的加密保护。


5、RSAref - 用搜索引擎查找一下"rsaref20.tar.Z"应该就能找到了


我们将把这些程序安装于/usr/local目录下 


增加功能模块可以给阿帕奇更强大的功能，如果你需要更多的模块的话，自己去获

得它并且加载，比如mod_php这一模块也是现在流行的，可以使阿帕奇提供php脚本

支持……


五、软件包的安装


在实际安装前我们要决定我们将把web server安装在什么环境下，对于一个对

安全有相当高要求的人来说，可以将服务器和软件安装于chroot环境，chroot

改变root 目录并且仅在这一目录中执行程序，这提供了一个内建的小环境，即

使入侵者已经通过cgi程序或者其它办法通过80端口获得了系统的进入权限，它

也只能够在这一受限的环境中活动，从安全角度考量，这当然是最好的，但对

系统管理员来说，这样安装相对麻烦一些，还必须把一些必要的库，perl以及

相关工具也搬到chroot中，所以――你自己决定吧，这里我们介绍的是在chroot

下安装。


展开这些软件包:


#gzip -d -c apache_1.3.11.tar.gz | tar xvf -

#gzip -d -c mod_ssl-2.5.0-1.3.11.tar.gz | tar xvf -

#gzip -d -c openssl-0.9.4.tar.gz | tar xvf -

#gzip -d -c mod_perl-1.21.tar.gz | tar xvf -


展开并且编译rsaref


#mkdir rsaref

#cd rsaref

#gzip -d -c ../rsaref20.tar.Z | tar xvf -

#tar xvf rsaref.tar

#cp -rp install/unix temp

#cd temp

#make

#mv rsaref.a librsaref.a

#cd ../../


编译OpenSSL


#cd openssl-0.9.4

#perl util/perlpath.pl /usr/bin/perl (Path to Perl)

#./config -L`pwd`/../rsaref/temp/

#make

#make test

#cd ..


将mod_perl加到Apache的编译选项里


#cd mod_perl-1.21

#perl Makefile.PL APACHE_PREFIX=/usr/local/apache \


APACHE_SRC=../apache_1.3.11/src \


USE_APACI=1


你会得到下面的提示:


Configure mod_perl with ../apache_1.3.11/src ? [y]


直接按enter就是默认的yes


然后Makefile会问你是否建立httpd，可以用n选择不。


#make

#make install

#cd ..


将mod_ssl加到Apache中


#cd mod_ssl-2.5.0-1.3.11

#./configure --with-apache=../apache_1.3.11 \


--prefix=/usr/local/apache \


--with-ssl=../openssl-0.9.4 \


--with-rsa=../rsaref/temp \


--activate-module=src/modules/perl/libperl.a

#cd ..


编译Apache:


#cd apache_1.3.11


在编译以前我们可以再做一件事――编辑包含http server版本号的文件，使想得到它的入

侵者摸不着脑袋长哪儿:)


#<your favorite text editor> src/include/httpd.h


寻找下面的行 (approx. 454)并且改变server的名字及版本号――可以随便用你想改成的东西。


define SERVER_BASEVERSION "Apache/1.3.11"


现在你可以编译阿帕奇了


#make


现在你可以生成一个CA了(actual certificate).


#make certificate


按照该授权书的安装介绍做。


#make install


这将会把阿帕奇装在/usr/local/apache。


测试web server (还没装SSL)是否运行正常 ----调用web server:


/usr/local/apache/bin/apachectl start


当WEB服务器运行起来后，你可以用 lynx或者任意什么浏览器连接你的80端口，如果能看到apache

的欢迎页，就OK了。


停止server:


/usr/local/apache/bin/apachectl stop


测试web server (同时起SSL) - 调用带SSL的WEB服务器


/usr/local/apache/bin/apachectl startssl


服务器运行时你用Netscape或者其它支持SSL的浏览器来看[http://your.ip.here](http://your.ip.here/)，看到欢迎页了么？


要停止SERVER：


/usr/local/apache/bin/apachectl stop


六、阿帕奇的配置


现在我们可以来看看阿帕奇的配置文件了――需要记住的是如果你对它做了更改，

在未重新启动httpd守护进程前，它是不会发生作用的。好，现在我们可以进目录

/usr/local/apache/conf看看了。


httpd.conf -

这是阿帕奇的主要配置文件，你可以在这里设定服务器启动时的基本环境，比如服务

器的启动方式、端口号、允许的最多连接数等等，这一文件的注释非常详细，要看明

白应该没什么问题。


access.conf -

 

这一文件是设定系统中的存取方式和环境的，但现在已经可以在httpd.conf中设定了，

所以推荐你别动它，放空好了。


srm.conf - 


这家伙主要做的是资源上的设定，你也可以放空，仅仅设定httpd.conf中的相关项。


现在重启web server来使改动生效：


#/usr/local/apache/bin/apachectl restart


七、将阿帕奇设定在chroot环境下


现在我们开始把刚才建立的东西移到chroot环境下――包括阿帕奇服务器以及所有需

要的库文件。当然如前面所说的，这部份是可选的，如果你怕麻烦的话就算了，但转

移后可以对你的web server多一个可靠的保护。


建立/chroot目录


#mkdir /chroot


建立一些必需的子目录


#mkdir /chroot/dev

#mkdir /chroot/lib

#mkdir /chroot/etc

#mkdir /chroot/bin

#mkdir /chroot/usr

#mkdir /chroot/usr/local


在我们的chroot建立/dev/null


#mknod -m 666 /chroot/dev/null c 1 3


将阿帕奇拷贝到/chroot目录中


#cp -rp /usr/local/apache/ /chroot/usr/local


拷贝必需的二进制文件


#cp /bin/sh /chroot/bin


确定哪些库是必需的――这取决于你编译时内建了哪些模块


#ldd /usr/local/apache/bin/httpd


将需要的库拷贝到chroot目录


#cp /lib/libm.* /chroot/lib/

#cp /lib/libgdbm.* /chroot/lib

#cp /lib/libdb.* /chroot/lib

#cp /lib/libdl.* /chroot/lib

#cp /lib/libc.* /chroot/lib


拷贝网络连接所需要的函数库


#cp /lib/libnss* /chroot/lib


拷贝必需的/etc下的文件到chroot


#cp /etc/passwd /chroot/etc

#cp /etc/shadow /chroot/etc

#cp /etc/group /chroot/etc

#cp /etc/resolv.conf /chroot/etc

#cp /etc/hosts /chroot/etc

#cp /etc/localtime /chroot/etc

#cp /etc/localtime /chroot/etc

#cp /etc/ld.so.* /chroot/etc


测试chroot下的阿帕奇


#chroot /chroot /usr/local/apache/bin/apachectl start


现在再


#chroot /chroot /usr/local/apache/bin/apachectl stop


服务器就停下来了，如果不行的话，再次确认是否所有需要的库都拷到了/chroot/lib

下了，如果仍然无帮助的话，或者可以以strace方式运行httpd，它的输出可能会有一

些有价值的内容可以帮助确定是丢失了哪些库或者二进制文件。


然后我们可以做一些小工作了：默认情况下阿帕奇是以nobody用户及用户组运行的，不

要更改它。


在passwd\shadow\group等文件中包含了大量系统信息，所以你可以替换掉它们。


建立一个用户名为httpd，UID为80

建立一个组名为httpd，GID为80


用下面的命令来将/chroot下的passwd,shadow,group替换掉


#echo "httpd:x:80:100:,,,:/home/httpd:/bin/false" > /chroot/etc/passwd

#echo "httpd:*LK*:11010:0:99999:7:::" > /chroot/etc/shadow

#echo "httpd:x:80:" > /chroot/etc/group


设定好文件的许可权限


#chmod 600 /chroot/etc/passwd shadow group


现在我们可以编辑apache的配置文件并进行需要的配置，文件在

/chroot/usr/local/apache/conf/httpd.conf，寻找到包含apache运行用户

及组的信息的行并改变它(approx. line 263)，当然是改成httpd/httpd。


一切运行正常后我们可以删除前面的那些服务器安装的东西――/usr/local下的，

包括服务器以及那些内建的模块等等。


#rm -rf /usr/local/apache

#rm -rf /usr/local/mod_ssl-2.5.0-1.3.11/

#rm -rf /usr/local/mod_perl-1.21/

#rm -rf /usr/local/openssl-0.9.4/

#rm -rf /usr/local/rsaref


如果以后还想改变它们的配置，增加新的模块，那么将原先的apache留下来也行。


将阿帕奇设定为在开机时自启动，修改/etc/rc.d/rc.local并且加入以下行：


echo "Starting Apache-SSL"

/usr/sbin/chroot/apache/bin/apachectl startssl


如果一切都运行正常的话，那么恭喜你，你已经成功地运行了带SSL支持的阿帕奇

了，这会使你的web server更加安全，如果你希望加入更多的模块实现其它功能的

话，自己动手吧，最后要说明的是：在chroot环境中最好只有必需的一些二进制程

序，而SUID程序还是干掉比较好些。
