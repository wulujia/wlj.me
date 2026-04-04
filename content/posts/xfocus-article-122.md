---
title: "探查DNS服务器运行状况"
date: 2001-03-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-122"
---

fjxufeng
 (quack_at_xfocus.org)

探查DNS服务器运行状况


[www.linuxaid.com.cn](http://www.linuxaid.com.cn/) fjxufeng


    在Linux环境下，也提供了广泛流行的BIND服务器，它是构建DNS服务器最常用的服务器软件。

介绍BIND的安装的文章现在很多，现在我们就一起来谈一下维护的话题。我们如何才能够了解DNS

服务器的运行情况下呢，它忙不忙、负载大不大？这一切，对于系统管理员而言，是比较重要的。

    想了解DNS服务器的运行状况，可以通过查看DNS服务器在运行时所产生的日志文件来实现。

    BIND 8提供了一些控制日志系统的手段，不过呢，缺省状态所生成的日志已经够用了，通过

这些日志信息，足以了解DNS服务器现在的运行状况了。

    在缺省情况下，BIND是通过syslog来生成日志的，存放在/var/log/message文件中。

注：与之相关的还有以下四个文件：

/var/log/message.1

/var/log/message.2

/var/log/message.3

/var/log/message.4

    其实是将日志分为了5个文件来存储，防止文件过大，当message文件够大后，就变成了

message.1，原来的message.1就成了message.2……，message.4的内容就消失了。

    由于这个文件中的日志信息是syslog生成的，所以不并是全都是关于BIND的日志信息。我们

执行以下命令，将所有BIND的日志信息挑选出来：

more /var/log/message|grep named >/tmp/named.log

注：BIND服务器的进程名是named。

    这样，/var/log/message中与BIND相关的日志信息都会写入/tmp/named.log文件中了。

最主要的日志有两种：LOG_NOTICE，LOG_INFO级的日志。


一、 LOG_NOTICE级日志

1.每次启动BIND服务器named时，会生成一个如下所示的LOG_NOTICE级日志信息：

  Nov 28 10:37:45 www named[10134]: starting.  named 8.2.2-P3

  其中:

  Nov 28 10:37:45  表示服务器启动时间

  www  显示DNS服务器所在机器名

  named[10134]： 显示DNS服务器进程名与进程ID

  starting.  表示正在启动DNS服务器

  named 8.2.2-p3  显示BIND软件版本

2.当给DNS服务器发送一个HUP信号，使DNS服务器重启时，会生成一个如下所示的LOG_NOTICE级日志信息：

  Nov 28 10:37:45 www named[10134]: reloading  nameserver

其中:

  Nov 28 10:37:45  表示服务器重启动时间

  www  显示DNS服务器所在机器名

  named[10134]： 显示DNS服务器进程名与进程ID

  reloading.  表示正在重新启动DNS服务器

  nameserver  显示正在重启的服务器名


二、LOG_INFO级日志

    在DNS服务器运行时，每隔一小时会生成一组如下所示的LOG_INFO级日志信息，反馈DNS

服务器的运行状态：

  Dec 26 10:23:52 www named[1033]: Cleaned cache of 26 RRset

  Dec 26 10:23:52 www named[1033]: USAGE 977797432 976760631 CPU=6.55u/6.24s CHILD CPU=0u/0s

  Dec 26 10:23:52 www named[1033]: NSTATS 977797432 976760631 0=2 A=13192 

CNAME=321 PTR=11204 MX=1173 TXT=4 AAAA=32 ANY=4956

  Dec 26 10:23:52 www named[1033]: XSTATS 977797432 976760631 RR=7629 RNXD=1368 

RFwdR=4836 RDupR=51 RFail=159 RFErr=0 RErr=12 RAXFR=0 RLame=175 ROpts=0 

SSysQ=2082 SAns=26234 SFwdQ=4520 SDupQ=1263 SErr=0 RQ=30889 RIQ=4 RFwdQ=0 

RDupQ=259 RTCP=2 SFwdR=4836 SFail=6 SFErr=0 SNaAns=21753 SNXD=10276


下面我们就逐句解读一下：

1.  Dec 26 10:23:52 www named[1033]: Cleaned cache of 26 RRset

   这是每一组日志信息的第一行，表示正在清空Cache。

其中：

  Dec 26 10:23:52  表示日志生成时间

  www  显示DNS服务器所在机器名

  named[1033]： 显示DNS服务器进程名与进程ID

  Cleaned cache of 26 RRset  表示正在清除cache

2. Dec 26 10:23:52 www named[1033]: USAGE 977797432 976760631 CPU=6.55u

  /6.24s CHILD CPU=0u/0s

这一行是USAGE行，用于统计DNS服务器占用的CPU时间。

其中：

  Dec 26 10:23:52  表示日志生成时间

  www  显示DNS服务器所在机器名

  named[1033]： 显示DNS服务器进程名与进程ID

  USAGE  行标记

  977797432 976760631  977797432-976760631的值就是DNS服务器运行的总秒数

  CPU=6.55u/6.24s  代表DNS服务器使用了用户态6.55秒，系统态6.24秒（u代表user，

s代表system），

  CHILD CPU  代表DNS服务器子进程的CPU占用情况。

3. Dec 26 10:23:52 www named[1033]: NSTATS 977797432 976760631 0=2 A=13192 

CNAME=321 PTR=11204 MX=1173 TXT=4 AAAA=32 ANY=4956

这一行是NSTATS行，用于统计接收到的查询总数

其中：

  Dec 26 10:23:52  表示日志生成时间

  www  显示DNS服务器所在机器名

  named[1033]： 显示DNS服务器进程名与进程ID

  NSTATS  行标记

  977797432 976760631  977797432-976760631的值就是DNS服务器运行的总秒数

  0=2   代表未知类型的DNS查询2个

  A=13192  代表A类地址查询13192个（最标准）

  CNAME=321  代表CNAME类地址查询321个（一般是有些版本的sendmail使用CNAME程序

规范化邮件地址而发出的，还有就是dig或nslookup发出的）

  PTR=11204  代表指针查询11204个（许多软件通过这种方法来查找IP地址）

  MX=1173  代表邮件交换器的查询1173个（是由邮件发送程序发起的）

  TXT=4  代表应用程序进行的文本查询共有4个

  AAAA=32  代表AAAA类查询32个

  ANY=4956 有些Sendmail使用的地址查询方式，共4956个

注：还有可能有：

NS=xx 代表名字服务器查询（例如：名字服务器试图查找根域的服务器）

SOA=xx 代表辅助DNS更新

HINFO=xx 主机信息查询

NSAP=xx 将域名映射成OSI网络服务访问点地址

AXFR=xx 辅助DNS的区传送

这些在本例中并未出现。

4. Dec 26 10:23:52 www named[1033]: XSTATS 977797432 976760631 RR=7629 RNXD=1368

RFwdR=4836 RDupR=51 RFail=159 RFErr=0 RErr=12 RAXFR=0 RLame=175 ROpts=0 SSysQ=2082

SAns=26234 SFwdQ=4520 SDupQ=1263 SErr=0 RQ=30889 RIQ=4 RFwdQ=0 

RDupQ=259 RTCP=2 

SFwdR=4836 SFail=6 SFErr=0 SNaAns=21753 SNXD=10276

这是XSTATS行，它用于统计其它一些数据。

其中：

  Dec 26 10:23:52  表示日志生成时间

  www  显示DNS服务器所在机器名

  named[1033]： 显示DNS服务器进程名与进程ID

  NSTATS  行标记

  977797432 976760631  977797432-976760631的值就是DNS服务器运行的总秒数

  RR=7629   代表收到其它主机的响应共有7629个（DNS向其它机器或进程发出的查询得到

的响应数、与RQ无关）

  RNXD=1368  代表收到“没有这样的域”回答共有1368个

  RFwdR=108 收到对原始查询的响应为108个 

  RDupR=51  重复响应51个（当DNS在它悬而未决的查询列表中，找不到引起该响应的原始

查询时，这个响应就是重复响应）

  RFail=159 收到SERVFAIL（远程服务器错误）159个

  RFErr=0 没有收到FORMERR（远程名字服务器认为本地名字服务器的查询有格式错误）

  Rerr=12 收到除了SERVFAIL、FORMERR以外的错误12个

  RAXFR=0 共有0次区传送

  RLame=175 收到175个坏授权（意味着有的区被授权给其它名字服务器，而这个名字服务

器不是这个区的权威）

  ROpts=0 共收到带有IP选项的包的个数为0

  SSysQ=2082 共发出系统查询2082个（系统查询是由本地名字服务器进行的查询。大多数

都是针对根名字服务器的）

  SAns=26234 共回答了查询26234个

  SFwdQ=4520 不在这个名字服务器，而转发共4520个

  SDupQ=1263 重复查询数1263个

  SErr=0 发出的非SERVFAIL、FORMERR的错误总数

  RQ=30889  收到的查询共有30889个

  RIQ=4  收到反向查询4个（反向查询是为了将地址映射为名字，现在这个功能被 PTR实

现了。较早的nslookup才使用这种查询）

  RFwdQ=0 没有需要进一步处理的查询

  RDupQ=259 重复查询共有259个

  RTCP=2 通过TCP连接收到2个查询（一般使用UDP）

  SFwdR=4836 来自其它名字服务器转发的响应4836个

  SFail=6 发出被认为SERVFAIL响应共6个

  SFErr=0 发出的被认为FORMERR的响应个数

  SNaAns=21753 非权威回答共21753

  SNXD=10276 发出没有这个域回答10276个


    这些统计数据都是从DNS开启后到现在的总统计，而非本小时内的统计数字。如何衡量

DNS服务器的负载呢？很简单，将总查询数除以DNS运行的总时间，不就知道了吗？在本例中：

DNS服务器已运行了： 977797432-976760631=1036801秒=288小时

注：从第2、3、4行都可以得到

    而总查询请求有： 2+13192+321+11204+1173+4+32+4956=20884次

注：从第2行都可以得到

也就是每小时107次查询请求，每秒不到2次，可见负载还是比较小的。
