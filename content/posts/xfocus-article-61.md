---
title: "几个DNS问题"
date: 2000-08-10T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-61"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

几个DNS问题


by xxbin


现在的Internet上存在的DNS服务器有绝大多数都是用bind来架设的,使用的bind版本

主要为bind 4.9.5+P1以前版本和bind 8.2.2-P5以前版本.这些bind有个共同的特点,

就是BIND会缓存(Cache)所有已经查询过的结果,这个问题就引起了下面的几个问题的

存在.


1>.DNS欺骗

在DNS的缓存还没有过期之前,如果在DNS的缓存中已经存在的记录,一旦有客户查询,

DNS服务器将会直接返回缓存中的记录.


下面我们来看一个例子:

一台运行着unix的Internet主机,并且提供rlogin服务,它的IP地址为123.45.67.89,

它使用的DNS服务器(即/etc/resolv.conf中指向的DNS服务器)的IP地址为98.76.54.32,

某个客户端(IP地址为38.222.74.2)试图连接到unix主机的rlogin端口,假设unix主机的

/etc/hosts.equiv文件中使用的是dns名称来允许目标主机的访问,那么unix主机会向

IP为98.76.54.32的DNS服务器发出一个PTR记录的查询:


123.45.67.89 -> 98.76.54.32 [Query]

NQY: 1 NAN: 0 NNS: 0 NAD: 0

QY: 2.74.222.38.in-addr.arpa PTR


IP为98.76.54.32的DNS服务器中没有这个反向查询域的信息,经过一番查询,这个DNS

服务器找到38.222.74.2和38.222.74.10为74.222.38.in-addr.arpa.的权威DNS服务器,

所以它会向38.222.74.2发出PTR查询:


98.76.54.32 -> 38.222.74.2 [Query]

NQY: 1 NAN: 0 NNS: 0 NAD: 0

QY: 2.74.222.38.in-addr.arpa PTR


请注意,38.222.74.2是我们的客户端IP,也就是说这台机子是完全掌握在我们手中的.

我们可以更改它的DNS记录,让它返回我们所需要的结果:


38.222.74.2 -> 98.76.54.32 [Answer]

NQY: 1 NAN: 2 NNS: 2 NAD: 2

QY: 2.74.222.38.in-addr.arpa PTR

AN: 2.74.222.38.in-addr.arpa PTR trusted.host.com

AN: trusted.host.com A 38.222.74.2

NS: 74.222.38.in-addr.arpa NS ns.sventech.com

NS: 74.222.38.in-addr.arpa NS ns1.sventech.com

AD: ns.sventech.com A 38.222.74.2

AD: ns1.sventech.com A 38.222.74.10


当98.76.54.32的DNS服务器收到这个应答后,会把结果转发给123.45.67.98,就是那台

有rlogin服务的unix主机(也是我们的目标 :) ),并且98.76.54.32这台DNS服务器会

把这次的查询结果缓存起来.


这时unix主机就认为IP地址为38.222.74.2的主机名为trusted.host.com,然后unix主机

查询本地的/etc/hosts.equiv文件,看这台主机是否被允许使用rlogin服务,很显然,

我们的欺骗达到了.


在unix的环境中,有另外一种技术来防止这种欺骗的发生,就是查询PTR记录后,也查询

PTR返回的主机名的A记录,然后比较两个IP地址是否相同:


123.45.67.89 -> 98.76.54.32 [Query]

NQY: 1 NAN: 0 NNS: 0 NAD: 0

QY: trusted.host.com A


很不幸,在98.76.54.32的DNS服务器不会去查询这个记录,而会直接返回在查询

2.74.222.38.in-addr.arpa时得到的并且存在缓存中的信息:


98.76.54.32 -> 123.45.67.89 [Query]

NQY: 1 NAN: 1 NNS: 2 NAD: 2

QY: trusted.host.com A

AN: trusted.host.com A 38.222.74.2

NS: 74.222.38.in-addr.arpa NS ns.sventech.com

NS: 74.222.38.in-addr.arpa NS ns1.sventech.com

AD: ns.sventech.com A 38.222.74.2

AD: ns1.sventech.com A 38.222.74.10


那么现在unix主机就认为38.222.74.2就是真正的trusted.host.com了,我们的目的达到了!


这种IP欺骗的条件是:你必须有一台Internet上的授权的DNS服务器,并且你能控制这台服务

器,至少要能修改这台服务器的DNS记录,我们的欺骗才能进行.


2>.拒绝服务攻击 Denial of service


还是上面的例子,如果我们更改位于38.222.74.2的记录,然后对位于98.76.54.32的DNS服务器

发出2.74.222.38.in-addr.arpa的查询,并使得查询结果如下:

因为74.222.38.in-addr.arpa完全由我们控制,所以我们能很方便的修改这些信息来实现我们

的目的.


38.222.74.2 -> 98.76.54.32 [Answer]

NQY: 1 NAN: 2 NNS: 2 NAD: 2

QY: 2.74.222.38.in-addr.arpa PTR

AN: 2.74.222.38.in-addr.arpa PTR trusted.host.com 

AN: [www.company.com](http://www.company.com/) A 0.0.0.1

NS: 74.222.38.in-addr.arpa NS ns.sventech.com

NS: 74.222.38.in-addr.arpa NS ns1.sventech.com

AD: ns.sventech.com A 38.222.74.2

AD: ns1.sventech.com A 38.222.74.10


这样一来,使用98.76.54.32这台DNS服务器的用户就不能访问[www.company.com](http://www.company.com/)了,因为这个IP

根本就不存在!


3>.偷取服务 Theft of services


还是上面的例子,只是更改的查询结果如下:


38.222.74.2 -> 98.76.54.32 [Answer]

NQY: 1 NAN: 3 NNS: 2 NAD: 2

QY: 2.74.222.38.in-addr.arpa PTR

AN: 2.74.222.38.in-addr.arpa PTR trusted.host.com

AN: [www.company.com](http://www.company.com/) CNAME [www.competitor.com](http://www.competitor.com/)

AN: company.com MX 0 mail.competitor.com

NS: 74.222.38.in-addr.arpa NS ns.sventech.com

NS: 74.222.38.in-addr.arpa NS ns1.sventech.com

AD: ns.sventech.com A 38.222.74.2

AD: ns1.sventech.com A 38.222.74.10


这样一来,一个本想访问[http://www.competitor.com](http://www.competitor.com/)的用户会被带到另外一个地方,

甚至是敌对的公司的竹叶(想想把华为和北电联起来是什么样的感觉. :) ).

并且发给company.com的邮件会被发送给mail.compertitor.com.(越来越觉得在网络上

的日子不踏实! xxbin这样想).


4>.限制


对这些攻击,也有一定的限制.

首先,攻击者不能替换缓存中已经存在的记录.比如说,如果在98.76.54.32这个DNS服务器

上已经有一条[www.company.com](http://www.company.com/)的CNAME记录,那么攻击者试图替换为[www.competitor.com](http://www.competitor.com/)

将不会成功.

然而,一些记录可以累加,比如A记录,如果在DNS的缓存中已经存在一条[www.company.com](http://www.company.com/)

的A记录为1.2.3.4,而攻击者却欺骗DNS服务器说[www.company.com](http://www.company.com/)的A记录为4.3.2.1,

那么[www.company.com](http://www.company.com/)将会有两个A记录,客户端查询时会随机返回其中一个.(呵呵,这不是

loading balance么?)


其次,DNS服务器有个缓存刷新时间问题,如果[www.netbuddy.org](http://www.netbuddy.org/)的TTL为7200,那么DNS服务

器仅仅会把[www.netbuddy.org](http://www.netbuddy.org/)的信息缓存7200秒或者说两个小时.如果攻击者放入一条TLL

为604800的A记录,那么这条记录将会在缓存中保存一周时间,过了默认的两天后,这个DNS

服务器就会到处"分发"攻击者假造的记录.


下面是常用的几种可以累加和不能累加的记录:


A can add

NS can add

MX can add

PTR cannot add

CNAME cannot add


以上资料由xxbin(xxbin@sina.com)整理收集.

转自netbuddy论坛([http://netbuddy.fjta.com](http://netbuddy.fjta.com/))


版权所有：xxbin 转贴自netbuddy网络论坛
