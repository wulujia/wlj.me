---
title: "构建安全的e-commerce服务器"
date: 2001-06-01T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-186"
---

(quack_at_xfocus.org)

by Sinbad

May 25, 2001

[http://sinbad.dhs.org](http://sinbad.dhs.org/)


一．Background


基于Internet的网络经济一直吸引着人们的眼球，随着门户网站的局势已定，现在又涌现出

一批以“电子商务”命名的网络公司。相比之下，他们比较冷静和谨慎。在企业级应用上，

他们不仅仅满足于协助中小企业上网，更多的是想提供一些电子商务的主打产品：CRM、ERP

、SCM等，或者提供从IDC到ASP一条龙服务。


但是，就我所经历的情况来看，真正能埋头做产品的公司微乎其微。一是因为投入太大，二

是因为很难找到合适的市场定位。做方案和集成，无非是东拼西凑，糊弄初级客户，完全没

有自己的东西。那么，目前电子商务公司除了做一些网站建设和应用项目，还有哪些盈利点

？依我所见，由于国内的电子商务环境还不成熟，没有完整的信用体制和支付手段，在这个

基础上，许多电子商务活动都是很难开展的。客户的顾虑也很多，仅从安全性上考虑，比如

你做ASP（应用服务提供商），客户很难接受与其他人共享一块硬盘，把数据交给你维护更是

忧心忡忡；辛辛苦苦开发出一套系统，放到网上，很轻易的被黑客窃取了源代码，让人心痛

；架在一个不堪一击系统上的应用，黑客篡改了页面和数据，都很难向客户交待，影响了自

己的声誉和进一步的业务合作。


这就体现出了安全的重要性。是的，安全和黑客技术是比较偏，有些搞软件开发的人甚至对

此嗤之以鼻，但是我们不能否认安全在电子商务中的基石作用，不考虑安全和不懂安全的系

统分析员来设计开发电子商务系统，最后注定会失败的很惨。


安全是一个很复杂的系统工程，从最初的制度策略的制定，到最后整个系统的implement，有

很多环节。本文仅仅介绍构造一个e-commerce服务器，来说明在Internet上放置一个可以安

全运行的电子商务WEB服务器也不是那么的简单。


二．Apache


为什么要选择Apache？中小企业比较乐于接受较低的系统报价，UNIX的网管们也可以从技术

上替我解释这个问题。是的，相比于漏洞层出不迭的IIS来说，Apache在安全界享有良好的声

誉，但是一个默认安装的Apache还是不够。


1)操作系统

Apache尽管发布了Windows、Linux、BSD家族和其他操作系统的版本，但毫无疑问的是，UNI

X是最好的选择。首先是远程管理上的方便，同时SSH提供了远程管理维护的加密通道。在系

统性能上，UNIX类系统更加易于优化配置。


2)自身的漏洞

尽管Apache的内核没有太大的buffer overflows和exploits，但是在1.3.19以前的版本有一

个mod_rewrite漏洞。建议安装最新的版本1.3.20。


3)外来的隐患

现在的电子商务网站内容都不是静态，而是动态生成的，所以需要额外的一些模块，如Java

（Jserv）、Perl（mod_perl）、PHP（mod_php）。这些模块给Apache引入了安全隐患。如W

indows平台上的Apache+PHP存在目录遍历漏洞，UNIX平台上，某些版本的Tomcat引擎（Java

 Servlets和JSP）也存在目录遍历、甚至泄露.jsp源代码的漏洞。


Apache和其它软件产品一样，多多少少存在安全问题。我们不要在嘲笑IIS满身窟窿同时，对

Apache抱着100%的放心。一般情况下，有两个因素导致软件的不安全性：技术上和配置。如

果网管们都能很好的配置服务器，相比之下，软件中的一些BUG是很容易解决的。


三．SSL


Internet是一个开放的系统。大部分的网络通信都是不安全的，就好比传统邮政中的明信片

邮寄，恶意用户可以偷看明信片内容、篡改和伪造身份发送。


SSL，即Secure Socket Layer，是工作在网络层与会话层之间的协议，它在TCP/IP和HTTP之

间增加了一个加密层，主要是使用公开密钥体制和X.509数字证书技术保护信息传输的机密性

和完整性，它不能保证信息的不可抵赖性，主要适用于点对点之间的信息传输，常用于Web 

Server方式。


电子商务系统中，最常用的加密协议是SSL和SET。SET是在应用层，而SSL是在会话层，对工

作在HTTP协议以上的用户而言，加密是透明的。关于SSL和SET的比较，请参考其他文章。事

实上，最容易实现的方案就是采用SSL，新推出的TLS也未被广泛使用。


四．Apache+SSL


好，下面将给出一些实践内容，介绍如何安装一个安全的Apache SSL Server。首先，必须保

证网络和操作系统的安全性：安装了防火墙和路由器并且配置正确，操作系统已打补丁且做

了安全优化，系统日志的单独存放等等。


Apache服务器本身不支持SSL，我们有很多选择可以完成Apache/SSL的合并：（1）Apache-S

SL计划（[http://www.apache-ssl.org](http://www.apache-ssl.org/)），它集成了Apache服务器和SSL；（2）第三方的SSL

补丁，例如Covalent Networks的Covalent SSL ([http://www.covalent.com](http://www.covalent.com/))；（3）mod_ss

l，它是通过可动态加载的模块mod_ssl（[http://www.modssl.org](http://www.modssl.org/)）来支持SSL；（4）基于A

pache并集成了SSL能力的商业Web服务器，然而使用这些商业Web服务器主要是北美，这是因

为在那里SSL使用的公开密钥的算法具备专利权，例如RedHat Secure Server（[http://stor](http://stor/)

e.redhat.com/commerce/）。


我们选择第三种方法，这样我们就使用Apache的最新版本。去三个站点下载以下软件包：

Apache：[http://www.apache.org](http://www.apache.org/)

OpenSSL：[http://www.openssl.org](http://www.openssl.org/)

mod_ssl：[http://www.modssl.org](http://www.modssl.org/)


下面是安装步骤：


A．准备

解开apache、openssl和mod_ssl到/usr/local/src目录下。


B．编译Openssl

切换到目录/usr/local/src/openssl-0.9.6：

（1）./Configure linux-elf threads �CfPIC �Cprefix=/usr/local/ssl

（2）make

（3）make test

（4）make install


C．配置mod_ssl

进入目录/usr/local/src/mod_ssl-2.8.0-1.3.17执行以下命令：

./configure --with-apache=../apache_1.3.17


D．配置Apache

进入目录/usr/local/src/apache_1.3.17：

1. export SSL_BASE=../openssl-0.9.6

2. ./configure \

--prefix=/usr/local/apache \

--enable-module=ssl \

--disable-rule=SSL_COMPAT \

--enable-module=rewrite \ 

--enable-module=auth-digest \ # use MD5 hashes for HTTP

# basic authentication

--enable-module=vhost_alias \ # enable virtual hosts

--enable-module=log_referer \ # enhance logging

--disable-module=userdir \ # not used in e-commerce apps

--disable-module=autoindex \ # do not list directories

3. make

4. make certificate TYPE=dummy

5. make install

6. /src/httpd �Cl


现在Apache已经安装好了，可以通过httpd �Cl来查看安装的模块。


下面是一些要检查的安全设置：


SSL：

在httpd.conf中打开SSL

Port 80

<IfDefine SSL>

Listen 80

Listen 443

SSLSessionCache dbm:/usr/local/apache/ logs/ssl_scache

SSLSessionCacheTimeout 1200

# For increased performance use "SSLMutex sem" instead of the line below

SSLMutex file:/usr/local/apache/logs/ssl_mutex

SSLLog /usr/local/apache/logs/ssl_engine_log

# change the log level default from "info" to "warn"

SSLLogLevel warn

SSLOptions +OptRenegotiate

</IfDefine>


打开虚拟主机的SSL支持：

# Within the <IfDefine SSL>...</IfDefine>

<VirtualHost _default_:443>

SSLEngine on

# Replace <name> with certificate file name

SSLCertificateFile /usr/local/apache/conf/ssl. 

cert/<name> 

# Replace <name> with key file name

SSLKeyFile /usr/local/apache/conf/ssl.key/<name>

SSLVerifyClient none

</VirtualHost>


定制SSL的LOG格式：

LogFormat clfa "%h %l %u %t \"%r\" %>s %b\ %{SSL_PROTOCOL}x  %{SSL_CIPHER}x \"%{

SSL_CLIENT_S_DN_CN}x\""

CustomLog /usr/local/apache/logs/access_log clfa


被保护的目录：

<Location /test/>

SSLCipherSuite HIGH: MEDIUM

AuthType Digest

AuthName "Beta code testing"

AuthDigestDomain /test/ [http://test.my.dom/beta/](http://test.my.dom/beta/)

AuthDigestFile /usr/local/apache/conf/

digest_pw

Require valid-user

</Location>


最后的文件检查：

1. SSL证书和公钥不能存放在DocumentRoot下；

2. SSL 证书和公钥必须被root所拥有，chmod 400 *.crt；

3. 移去/htdocs和/cgi-bin中的所有示例文件；

4. /htdocs下的所有文件被nobody所拥有。

如果你不怕配置麻烦，最好把Apache放到一个chroot的环境中运行。：）


关于如何生成证书请求包和到CA中心去签署，请参考其他文章。目前国内也有很多CA中心，

如中国电信电子商务安全认证中心（[http://www.sinocol.com/](http://www.sinocol.com/)），都可以对个人颁发证书。


五．Hardening e-commerce Server


尽管Apache安装和配置的都很安全，但是一台具有薄弱口令或者运行着象wu-ftpd那样不安全

服务的LINUX还是很容易被攻破。一般来讲，一台WEB服务器仅仅需要的其他服务只有SSH―远

程管理所用。不要安装x-windows，编译器如gcc等应该在系统稳定运行后删去，这样可以避

免一些script-kiddiez的破坏。


同时，一些包过滤规则（ipfw，ipchains，iptables）应该被应用。这里我们将讨论Linux下

的ipchains，假定有以下需求：


1．服务器有两块网卡

2．外网卡仅仅允许80和443端口数据的incoming

3．外网卡仅仅允许>1023端口数据的outgoing

4．内网卡仅仅允许22、80、443端口的incoming

5．内网卡仅仅允许>1023端口数据的outgoing。一般的连接是数据库，oracle是1524port，

SQL Server是1443，SSH可以加上-P选项来指定大于1023的用户端口。

6．内网卡允许ICMP响应


命令如下（eth0外网卡，eth1内网卡）：

ipchains -A in-eth0 -p tcp --dport 80 -j ACCEPT

ipchains -A in-eth0 -p tcp --dport 443 -j ACCEPT

ipchains -A in-eth0 -p udp --dport 53 -j ACCEPT

ipchains -A in-eth0 -j DENY

ipchains -A out-eth0 -p tcp --dport 1024:65535 -j ACCEPT

ipchains -A out-eth0 -p udp --dport 53 -j ACCEPT

ipchains -A out-eth0 -j DENY

ipchains -A in-eth1 -p tcp --dport 22 -j ACCEPT

ipchains -A in-eth1 -p tcp --dport 80 -j ACCEPT

ipchains -A in-eth1 -p tcp --dport 443 -j ACCEPT

ipchains -A in-eth1 -p udp --dport 53 -j ACCEPT

ipchains -A in-eth1 -p icmp -j ACCEPT

ipchains -A in-eth1 -j DENY

ipchains -A out-eth1 -p tcp --dport 22 -j ACCEPT

ipchains -A out-eth1 -p tcp --dport 1024:65535 -j ACCEPT

ipchains -A out-eth1 -p udp --dport 53 -j ACCEPT

ipchains -A out-eth1 -p icmp -j ACCEPT

ipchains -A out-eth1 -j DENY


剩下的工作就是重新编译系统内核，禁用不需要的模块，可以使某些rootkits失效。

最后，检查WEB SERVER上运行着的程序的安全性，有没有缓冲区溢出等安全问题。


六．参考资料

Improving Apache, by GARY BAHADUR & MIKE SHEMA

SSL: Theory and Practice, Zeus Technology

LASG, i.e. Linux Administrators Security Guide


(END)
