---
title: "windows下的sock代理"
date: 2000-05-27T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-68"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

windows下的sock代理


译：quack

参考资料：《ANONYMOUS CONNECTIONS OVER THE NET:Socks Chains in Windows》by zoa_chien


一、概要


这份文档讲述如何在ms windows下通过socks chain接入internet，使你能够匿名

地接入网络，别人想定位你也更不容易了。


二、原理


你传输数据时用了越多跳板，要找出你的真实踪迹就越困难，就如下面：


     you --> socks1 --> socks2 --> socks3 --> ... --> socksx --> target


想要找出你，就必须连接x个你所通过的机器，并且找出他们的log，如果碰巧有一

个没有记录，线就断了:)，即使都记录了，log里面登记的IP也是上一级跳板主机

的IP……


这种技巧可以用于：

. ICQ或者相似工具

. ftp客户端

. mail客户端

. telnet客户端

. 端口扫描器

. (以及几乎所有在网络中所使用的工具)


这可能不适用于某些IRC服务器，因为它们常常查看打开着的wingates及proxies。


三、开始吧


1、找到一些运行wingate的主机


     因为wingates的默认安装打开端口1080并且不记录socks连接。


     你可以从

     [http://proxys4all.cgi.net/win-tel-socks.shtml](http://proxys4all.cgi.net/win-tel-socks.shtml)或者

     [http://www.cyberarmy.com/lists/wingate/](http://www.cyberarmy.com/lists/wingate/)找到一些公布出来的wingate的IP，或者

     你可以自己找到它们，你可以用'代理猎手'(?我不知道是不是国内流行的那个，似乎

     不太象，懒得去看了)，可以从[http://www.securax.org/ZC/anon/proxyht300beta5.exe](http://www.securax.org/ZC/anon/proxyht300beta5.exe)

     下载。


     或者你可以用一个叫wingatescan的工具,下载连接在：          [http://www.securax.org/ZC/anon/wgatescan-22.zip](http://www.securax.org/ZC/anon/wgatescan-22.zip)


     速度是非常重要的――因为我们要使用的多socks连接，所以klever dipstick可以帮

     助你断定哪个wingate是速度最快的，你可以从下面的连接下载：     [http://klever.net/kin/static/dipstick.exe](http://klever.net/kin/static/dipstick.exe)

     (其实这个工具应该就是ping每台主机，看它的反应速度罢了，找出回应最快的)


2、确认列表中的主机的确运行着wingate


     同样有很多工具能做这种事，比如server 2000，可以从          [http://freespace.virgin.net/david.wood6/Server/Server.htm](http://freespace.virgin.net/david.wood6/Server/Server.htm)下载。


3、安装一个能截取发送的信息包的软件


     我使用的是一个叫purpose的工具，你可以从

     [http://www.socks.nec.com/sockscap.html](http://www.socks.nec.com/sockscap.html)得到它。


     要设置它，只要在socks server填上: 127.0.0.1  port  8000.

     选择'socks  version  5'.再点击'resolve  all  names  remotely'.

     不要选'supported authentication'。


     在主界面，选择new然后建立一个你希望socks支持的程序的快捷方式


     对所有你想匿名的程序做同样的工作……


4、安装socks chainer


     从[http://www.ufasoft.com/socks](http://www.ufasoft.com/socks)下载该工具


     在service菜单, 点击new。在name段输入Chain，port则输入8000。


     点击new 并且将你找到最快的wingates的IP填进去，端口则填1080。


     使用 '<' 和 '>',  你可以添加或者移除socks. 记得一定要在使用前测试所有的socks.


四、测试你的设置


要想检查你的电脑连接到哪些socks，可以使用工具x-ploiters totostat ([http://idirect.tucows.com/files/totostat_install.exe](http://idirect.tucows.com/files/totostat_install.exe)).

检查端口1080的连接。


用你所建立的浏览器的快捷方式打开浏览器，连接到

[http://cavency.virtualave.net/cgi-bin/env.cgi](http://cavency.virtualave.net/cgi-bin/env.cgi)或者

[http://internet.junkbuster.com/cgi-bin/show-http-headers](http://internet.junkbuster.com/cgi-bin/show-http-headers)


同样，打开你的telnet客户端并尝试telnet到

ukanaix.cc.ukans.edu


你可以通过[https://sites.inka.de:8001/cgi-bin/pyca/browser-check.py](https://sites.inka.de:8001/cgi-bin/pyca/browser-check.py)来检测SSL或者

FTP到ftp.zedz.net――或者其它的FTP来验证你的IP。


在上面的测试中，远程主机上留下的将是你最后一个chain的IP地址。当然你可以在自己的

网络里进行测试……


五、最后……


never use  internet explorer to do tricky  stuff as it might reveal your ip.

my personal favorite browser is opera 4.0 ([http://www.opera.com/](http://www.opera.com/))


if   you  looked   carefully   to   what  is   displayed  when   you  go  to

the [http://internet.junkbuster.com/cgi-bin/show-http-headers](http://internet.junkbuster.com/cgi-bin/show-http-headers) page, you might

have  noticed  that  a  lot  of  stuff  about  our  client  is  being  sent.

to avoid this, we  could install another proxy  between the sockscap and the

sockschainer proxy that would filter out those things.

A4proxy is an example of a proxy capable of doing such things.


remember, if you want to do the real stuff, better switch to linux.


==============================

好象没多大价值，将就着看吧……
