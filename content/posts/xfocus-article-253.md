---
title: "Netfilter的高级使用"
date: 2001-08-24T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-253"
---

(inburst_at_263.net)

Netfilter的高级使用

santa

santa2001@263.net


    netfilter有一些功能在标准发行的linux内核里面没有包括，例如基于时间的控制、dropped-table、反端口扫描等等。这些功能大部分将来会慢慢加入到linux内核中，但目前都没有经过仔细测试，所以要慎重使用。

   要使用这些功能，    请先下载最新的iptables源码。解压后，执行

make pending-patches KERNEL_DIR=<<where-your-kernel-is>>看看你的内核是不是太老了，然后make patch-o-matic，按照提示选择想要安装的新功能。下面是我觉得有用的一些功能：

1．    ah-esp 增加两个扩展，允许匹配ipsec包中ah或esp包头中的一段SPI(security parameters index)。

2．    ct-netlink 使用户空间程序可以通过netlink获得连接跟踪的状态，并可经由用户空间改变连接状态。这个补丁与其他大多数补丁冲突。

3．    dropped-table 加了一个drop表，被drop的包遍历这个表。和其他大部分补丁冲突。

4．    ftos 扩展的tos，可以设置tos为0x0到0xff之间的任何值，用于简单的Qos。

5．    iplimit 限制每客户到主机或网络的并发连接数。例如：

iptables -p tcp --syn --dport 23 -m iplimit --iplimit-above 2 -j REJECT

(每客户最多两个telnet连接)，等效于iptables -p tcp --syn --dport 23 -m iplimit ! --iplimit-above 2 -j ACCEPT

     限制到每个c类网络最多16个http连接

iptables -p tcp --syn --dport 80 -m iplimit --iplimit-above 16        \

    --iplimit-mask 24 -j REJECT

6．    ipv4options 匹配ip操作，使用该功能可以过滤掉源路由、记录路由、时间戳等ip操作。iptables -m ipv4options �Chelp可以得到详细的帮助。例如iptables -A input -m ipv4options --rr -j DROP 过滤掉记录路由的包，iptables -A input -m ipv4options --ts -j DROP 过滤掉带时间戳操作的ip包。

7．    irc-conntrack-nat 对irc的DCC(Direct Client-to-Client)协议的支持。

8．    length 允许以指定值或指定范围匹配包长度。例如POD这样的大包可以直接drop。最小包长为0，最大的是0xffff。

9．    mport 对multiport功能的增强。可以对单个端口和一段连续端口混合指定。看来是很好，不过我测试的时候这个功能不能用（2.4.6 & 2.4.9内核）。

10．    netlink 用户空间可以经由netlink接收包。一个可用的用户空间程序fwmon ([http://firestorm.geek-ware.co.uk](http://firestorm.geek-ware.co.uk/))。这个补丁基本类似ipchains的-o操作。

11．    netmap 为nat表增加了一个NETMAP目标。提供一对一的网络映射支持。它可以在PREROUTING链中改变流入包的目标地址，在POSTROUTING链中改变输出包的源地址。使用范例如下：

iptables -t nat -A PREROUTING -d 1.2.3.0/24 -j NETMAP --to 5.6.7.0/24

iptables -t nat -A POSTROUTING -s 5.6.7.0/24 -j NETMAP --to 1.2.3.0/24

      

12．    nth 提供对第n个包的匹配。

13．    pkttype 按类匹配包。例如broadcast、multicast等。使用范例如下：

iptables -A INPUT -m pkttype --pkt-type broadcast -j LOG。

14．    pool 提供一种方法，用位图中的每一位代表一个地址，使用时需要一个用户空间程序ippool。

15．    psd 端口扫描察觉，设计思想来自于Solar Designer的scanlogd。支持如下选项：

a.    --psd-weight-threshold <threshold>

同一主机到不同目标端口发出多少包之后匹配

b.    --psd-delay-threshold <delay>

同一主机到不同目标端口的连接间隔多少时间之内匹配

c.    --psd-lo-ports-weight <weight>

访问多少个特权目标端口后匹配

d.    --psd-hi-ports-weight <weight>

访问多少个非特权端口后匹配。

16．    realm 使用前要求设置Qos配置里的CONFIG_NET_CLS_ROUTE4，允许在iptables里使用realm key，可以依照匹配的路由表项分类输出包。

17．    record-rpc 增加两个模块ip_conntrack_rpc_udp和ip_conntrack_rpc_tcp，分别记录tcp和udp的portmap请求，增加record-rpc模块，可以鉴别一个rpc连接是一个到portmap的映射请求还是一个portmap映射后的连接。用这种方法可以方便的实现rpc过滤。

18．    SAME 类似于标准的SNAT，不过为客户端的每个连接提供相同的ip地址。同时提供―nodst选项，选择源ip的时候不会使用这个选项后的ip地址。与dropped-table不兼容。

19．    snmp-nat 这个模块实现snmp负载的ALC(应用层网关)，结合nat，它允许网络管理系统存取多个私有网络，即使他们的ip地址冲突也没有关系。他通过改变snmp负载中的ip地址来匹配ip层的nat映射。这是SNMP-ALG的基本形式，在rfc2962中有详细的描述。

20．    string 允许匹配含有特定字符串的包。可以做个简单的ids。

21．    tcp-MSS 增加tcp-MSS目标。允许调整tcp syn包里的MSS域，用于控制连接包的最大长度。

一些防火墙或主机会很不适当的过滤掉type 3、code 4（需要分片）的icmp包。表现出来的现象如下：

a．    浏览网页时，什么也没有收到连接就挂起了。

b．    小邮件能收到，大邮件收不到。

c．    ssh工作的很好，但scp在握手成功后就挂起了。

Tcp-MSS目标就是用来解决此类问题的。目前发行的linux的内核从2.4.7开始已经包含了这个补丁。

22．    tcp-window-tracking 这个补丁是依据Guido van Rooij [1]写的论文'Real Stateful TCP Packet Filtering in IP Filter'实现的tcp连接跟踪记录，可以对已经建立的tcp连接进行连接跟踪。增加了Window scaling支持。

[1] [http://www.iae.nl/users/guido/papers/tcp_filtering.ps.gz](http://www.iae.nl/users/guido/papers/tcp_filtering.ps.gz)

23．    time 增加对时间的匹配，可以指定某条规则在什么时间触发，在什么时间无效。iptables -m time �Chelp可以得到详细的帮助。这个补丁增加了如下参数：

a．--timestart HH:MM

何时触发

b．--timestop HH:MM

何时无效

c．--days Tue,Mon...

一周中的某几天有效

例如-m time --timestart 8:00 --timestop 18:00 --days Mon,Tue,Wed,Thu,Fri就是说每周的周一到周五从8：00到18：00这条规则有效。

需要注意的是这个补丁目前还不能处理时区，使用时只能使用UTC时间。

24．    TTL 增加一个TTL目标。可以使用户用指定值递增或递减ttl值。

25．    ulog 增加一个ULOG目标。跳到这个目标的包使用netlink multicast sockets送到用户空间守护进程。不像LOG目标，后者只能通过syslog来察看。Libipulog目录下是接收ulog信息的库文件。用户空间守护进程的一个实现ulogd可以从[http://www.gnumonks.org/projects/ulogd](http://www.gnumonks.org/projects/ulogd)得到。

因为条件所限，以上所写的大多没有经过测试，错漏之处，欢迎指正。
