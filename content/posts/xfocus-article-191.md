---
title: "VPN On OpenBSD 配置小记"
date: 2001-06-10T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-191"
---

(quack_at_xfocus.org)

VPN On OpenBSD 配置小记　　


作者：刘稳


　　VPN(Vitual Private Network)近年来应用愈见广泛，关于Windows系统的配置已经有不少专述，笔者就不准备赘述。本文只是针对个人在PC机上配置OpenBSD系统上的VPN作一小述，同时声明所有操作只针对本人的配置经历，在读者自己实施的过程中可能有细微的差别，相信有一定OpenBSD操作经验的读者能够胜任"因材施教"。


### 1．什么是VPN?


　　提出这个问题只是为了"例行公事",事实上，关于VPN的论述也是有了很多种版本，包括china-pub.com的eMook专栏已经有不少精彩的论述。笔者不想从Ipsec、NAT、ipfilter、PPP等基础概念讲起，只是介绍一些入门知识，更深的知识请大家自行阅读OpenBSD的相关文档(FAQ和manpages等)。

　　VPN是Vitual Private Network的简称，即虚拟专用网络。本文中应用的网络环境是两个物理上分隔开的LAN，通过一个公用的网络(比如Internet)进行通信�D�D当然，最重要的是确保两个LAN中间进行的任何通信都无法被这个公用网络上任何未授权的用户窃听。 

　　经过简化的网络拓扑简图如下： 


[img]http://www.xfocus.org/other/aqpz/openbsd_vpn.gif[/img]


　　　　　　　　　　　　　　图一

　　这时候就是VPN的用武之地了。VPN对于连接两个物理分割的LAN是最好的选择，它可以做到配置好以后，两个LAN完全像物理上连接的网络！这时，两个LAN利用Internet作为主要的数据传输介质来传递数据。无论从概念上还是功能上都讲远远超出原先平常连接的程序工作效率。


### 2．配置VPN


　　首先需要明确笔者的联网环境。如果你的环境跟笔者的差不多甚至完全一样，那么恭喜你，你基本上可以按照以下步骤拷贝到你的系统上；如果有一定的差别，那么，就像上面提到的，读者应该完全有能力"即兴发挥"找出解决办法。何况这并不困难。

　　　 网络的连接跟(图一)相同。LAN1和LAN2中间间隔大概1600KM(之所以选择这么长距离的两个LAN,是为了突出VPN的强大性能)，Gateway1和Gateway2(网关)都是OpenBSD系统的路由器。Gataway1有永久性的Internet连接和一个固定的IP地址，而Gateway2就没有那么幸运，他只是一个拨号连接到Internet,而且每次拨号被必须ISP指定新的IP地址(这个网关是用域名来工作的，所以，不要担心这种网关是否存在)。LAN1的IP地址为192.168.35.0/24(这种写法是"借用了"R.Stevens的TCP/IP Illustrated里面的写法，表示LAN1的网络号是192.168.35，主机数为24，IP地址分别为192.168.35.1到192.168.35.24) ，LAN2 是 192.168.105.0/24。 Gateway1对于LAN1有一个内部IP地址192.168.35.1，外部地址为25.50.100.200(不用说，这是个假的，呵呵)；Gateway2 有一个内部地址192.168.105.1和随每次拨号都要更新的外部地址。 

　　配置开始。首先，Gateway得安装号OpenBSD2.8并配置成标准网关，也就是说，进行IP转发，给网关分配相应得IP地址。同时需要注意得是暂时不用配置ipfilter，这个可以在VPN配置完成以后再配；也不要打开任何OpenBSD安装时得缺省启动得服务，比如ftp/telnet/finger/rpc/portmap之类得，这是一台安全得服务器所必要得条件，而且可能回影响VPN配置过程，如果一定要开开，那么请在VPN配置完成以后再一个一个得打开，确认VPN工作无误。 

　　・然后，升级OpenBSD 2.8到OpenBSD-current. 因为在OpenBSD2.8的ipsec/ipf/ipnat 实现部分有问题，所以不要尝试在OpenBSD2.8上配置VPN。具体来讲，升级主要升级以下部分到current：

　　・内核。在链接新内核之前重新链接和安装usr.sbin/config

　　・isakmpd

　　・ipf

　　・ipnat 以上三项需要重新链接之前安装内核头文件(include 的时候 "make include")

　　只有升级这些才可以修复OpenBSD 2.8中IPSec的问题，这些问题主要包括isakmpd导致的错误选路，同时也至少崩溃过几次。而且理论上AES的问题也可以得到解决，虽然笔者还没有实验过。

为了升级到最新内核，需要

　　・编译和安装libkvm

　　・编译ps,vmstat,top并安装到已经有新内核的机器上

　　读者可以在[http://www.openbsd.org/anoncvs.html](http://www.openbsd.org/anoncvs.html) 查阅最新的更新。 

　　新内核开始工作以后，两台可以作OpenBSD VPN的网关就出现了。保证两台系统的/etc/sysctl.conf里面都有"net.inet.esp.enable=1" ，这使esp(Encapsulated Security Protocol)能够工作，以后所有通过VPN隧道到达网关的流量都是以esp形式的。只要应用了正确的密钥，这些esp包就会被根据他们真正的解密协议、端口和内容进行重新处理。 

　　下一件需要作的事情是让isakmpd开始工作，这样才可以让两个网关能够找到对方、验证对方的可信度从而开始交换密钥。 

　　这部分工作就不详细描述了，man isakmpd应该已经能够解决问题，而且笔者用的是非常标准的配置。两台机器利用商定的公共秘密句子来交换密钥，这个密钥是给AES加密算法用的。下面是笔者的isakmpd的配置文件，依次为isakmpd.policy (适用LAN 1和2), isakmpd.conf.lan1, 和 isakmpd.conf.lan2.


[h4]1．KeyNote-Version: 2[/h4]

Comment: This policy accepts ESP SAs from a remote that uses the right password

Authorizer: "POLICY"

Licensees: "passphrase:SecRetPhrasE"

Conditions: app_domain == "IPsec policy" &&

esp_present == "yes"; 


[h4]2. # $OpenBSD: VPN-east.conf,v 1.11 2001/04/09 23:27:29 nick1 Exp $[/h4]

# $EOM: VPN-east.conf,v 1.12 2001/04/09 22:08:30 nick2 Exp $


# A configuration sample for the isakmpd ISAKMP/Oakley (aka IKE) daemon.

#


[General]

Retransmits= 5

Exchange-max-time= 120


[Phase 1]

Default= ISAKMP-LAN2gw


[Phase 2]

Connections= IPsec-LAN1-LAN2


[ISAKMP-LAN2gw]

Phase= 1

Transport= udp

Configuration= Default-main-mode

Authentication= SecRetPhrasE


[IPsec-LAN1-LAN2]

Phase= 2

ISAKMP-peer= ISAKMP-LAN2gw

Configuration= Default-quick-mode

Local-ID= Net-LAN1

Remote-ID= Net-LAN2


[Net-LAN2]

ID-type= IPV4_ADDR_SUBNET

Network= 192.168.105.0

Netmask= 255.255.255.0


[Net-LAN1]

ID-type= IPV4_ADDR_SUBNET

Network= 192.168.55.0

Netmask= 255.255.255.0


[Default-main-mode]

DOI= IPSEC

EXCHANGE_TYPE= ID_PROT

Transforms= 3DES-SHA


[Default-quick-mode]

DOI= IPSEC

EXCHANGE_TYPE= QUICK_MODE

Suites= QM-ESP-AES-SHA-PFS-SUITE


[h4]3．# $OpenBSD: VPN-east.conf,v 1.11 2001/04/09 23:27:29 nick1 Exp $[/h4]

# $EOM: VPN-east.conf,v 1.12 2001/04/09 22:08:30 nick2 Exp $


# A configuration sample for the isakmpd ISAKMP/Oakley (aka IKE) daemon.

#


[General]

Retransmits= 5

Exchange-max-time= 120

Listen-on= 25.50.100.200


[Phase 1]

25.50.100.200= ISAKMP-LAN1gw


[Phase 2]

Connections= IPsec-LAN2-LAN1


[ISAKMP-LAN1gw]

Phase= 1

Transport= udp

Address= 25.50.100.200

Configuration= Default-main-mode

Authentication= SecRetPhrasE


[IPsec-LAN2-LAN1]

Phase= 2

ISAKMP-peer= ISAKMP-LANAgw

Configuration= Default-quick-mode

Local-ID= Net-LAN2

Remote-ID= Net-LAN1


[Net-LAN1]

ID-type= IPV4_ADDR_SUBNET

Network= 192.168.35.0

Netmask= 255.255.255.0


[Net-LAN2]

ID-type= IPV4_ADDR_SUBNET

Network= 192.168.105.0

Netmask= 255.255.255.0


[Default-main-mode]

DOI= IPSEC

EXCHANGE_TYPE= ID_PROT

Transforms= 3DES-SHA


[Default-quick-mode]

DOI= IPSEC

EXCHANGE_TYPE= QUICK_MODE

Suites= QM-ESP-AES-SHA-PFS-SUITE


　　(其他的例子可以在isakmpd.policy和isakmpd.conf的手册里找到)。这些文件都应该在网关的/etc/isakmpd下。 

　　读入这些配置文件的信息以后，两个网关就掌握了足够的信息来验证对方身份、交换密钥然后用正常的过程来改变和同步他们的加密密钥。 

　　对于第一次连接来说，笔者推荐先改动一下这些文件来适合你个人的需求，再确保两头的机器都正确无误的连接到了Internet上。 

　　isakmpd -d -DA=99

　　在两头的机器上，这会确保isakmpd在前台运行并显示最多的调试信息。你会得到一页又一页的调试信息，然后你就可以去看看真正加密的信息是怎样在机器间传输的。 

　　现在，你就已经应该得到一个可以运行的VPN了。当然，还需要进一步的测试。如果还是不能够运行，那么就检查一下，找出出问题的地方。一个简单的测试方法是ping对方LAN里面的一台机器。注意:你不能在网关上作这个试验。所以比如从192.168.35.2 ping 192.168.105.2，然后从192.168.105.2 ping 192.168.35.2, 你就应该看到两台机器跟一般的ping一样，就像是一个LAN内的两台机器(不必多讲，就是看TTL)。如果有兴趣，还可以再看看ftp/telnet之类的。如果你的ping工作不正常，可以看看本文最后提到的"测试和调试"。


### 3. 将过程自动化


为了避免每次需要使用VPN的时候都配置一大堆东西，一些步骤可以自动化。我们应该能够自动ping对方机器、让VPN自动开始工作。需要：

　　・ 每当另一头的VPN需要访问，这边的拨号PPP连接就应该建立

　　・ 自动运行isakmpd 

　　建立PPP连接并不是什么难事：在使用拨号连接的网关的/etc/rc.local文件里面加上"ppp -auto -nat ISP"。这样就使LAN2的机器一旦要连接出局域网，网关2就会建立ppp连接。 

　　而运行isakmpd就比较复杂了，他在静态的网关和需要拨号连接的网关上工作方法不同。对于静态网关，只需要修改/etc/rc.conf成'isakmpd_flags=""'，然后isakmpd就可以每次重起都自动运行了。但是在拨号连接的网关上，这种方法就会毫无用处，因为他刚刚重起过以后并没有Internet连接。这时候，如果我们需要每次建立PPP连接以后都自动运行isakmpd、取消PPP连接的时候也同时关闭isakmpd。可以在/etc/ppp.linkup和/etc/ppp.linkdown里面加入一行字。在/etc/ppp.linkup里面加入

MYADDR:

!bg isakmpd

而在/etc/ppp.linkdown里面加入

MYADDR:

!bg /etc/ppp/killisakmpd

这里killisakmpd是一个shell脚本，内容如下：

#!/bin/sh

kill `cat /var/run/isakmpd.pid`

这样，就可以完全将VPN的配置运行自动化了，很方便。 


### 4．测试和调试


　　如果读者的VPN第一次没有正常运行，那么你就不得不调试。如果isakmpd的一些功能没有正确配置、也就是虽然能够设立路由，但是没能加密所有的密钥，那这将是极为危险的。 

　　首先，最好先ping一下对方LAN的机器。上面已经讲过。如果工作不正常，那么在Gateway1上： 

tcpdump -i [网络外部接口名称，比如fxp1, tun0 等等] host [Gateway2的IP]

这条命令可以显示所有从 Gateway2到Gateway1的流量。理论上应该只有加密的ping命令被传送，就像这样： 

16:10:07.543323 esp d7-lp-23.dial-up.net > gateway.whatever.com spi

0xEFBF34AA seq 146 len 132

16:10:07.712902 esp gateway.whatever.com spi > d7-lp-23.dial-up.net

0xB17F45A2 seq 146 len 132

　　这表示进入的所有信息都是以esp方式进行加密的，而且你的VPN正常工作。如果你没有看到任何有关ICMP的信息，你的Internet连接还是未被VPN加密的。 

　　当笔者的VPN没有正常工作的时候，却也得到了以上信息，但是没有ping的回答，表示加密的信息根本没有在对方Gateway上处理。原因很简单：对方Gateway运行的是OpenBSD 2.8系统！ 


### 5. 与NAT和防火墙(ipf)的交互性


　　当以上所有工作都完成，并在没有Ipfilter的情况下正常工作了，笔者就打开了NAT和ipf。没有对标准的NAT设置作任何修改。然后在/etc/ipf.rules加上几行用来允许加密信息可以通过网关

# VPN: allow any traffic on the ISAKMP port

pass in on fxp1 proto udp from any port = 500 to 25.50.100.200 port = 500

pass out on fxp1 proto udp from 25.50.100.200 port = 500 to any port = 500


# VPN: allow all traffic in ESP form

pass in proto esp from any to 25.50.100.200

pass out proto esp from 25.50.100.200 to any

这些规则会允许所有通过isakmpd进行的的密钥交换和后来的加密esp过程能够正常进行。 


### 6. 结论


　　从以上的记述来讲，对于一个对网络、网关、NAT、ipf、ppp有基本认识的读者，配置一个VPN不是很难的事情。当设定好一切，还可以尝试运用各种不同的加密和认证手段。
