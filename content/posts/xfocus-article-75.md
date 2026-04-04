---
title: "ip路由的一些问题(spp)"
date: 2001-03-02T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-75"
---

(quack_at_xfocus.org)

ip路由的一些问题(spp)

                        

内容:很多网友问到这一方面的问题。所以想谈自己的看法。。不对的地方多指正 

F1.ip 如何在网络上走到目地？ 


A ip使用ospf . rip .hello 等路由协议来处理从本地主机到目标主机的路径。 

通常ip先比较地址的网络id , 如果不在同网段，那么它查询内核route table , 

试图找到匹配目标主机的下个路径，如果找到，发送ip包到该地址。如果没找到， 

发送ip包往缺省路由走。如果连default gw都没有。那么生成“目标主机不可到达” 

数据报返回主机。 


F2. ip 如何被主机响应？ 


A 当ip包通过路由走到目标网络后，该ip包并不知道哪台主机要接受。要查询该网段的 

ARP表，如果没找到匹配,它会伴随arp广播。ip包询问： 

ip -> (broadcast) ARP C Who is 10.10.10.10, 

domain.name.host 

10.10.10.10 -> ip ARP R 10.10.10.10,domain.name.host is 

a:b:c:d:e:f 

该过程结束后，mac地址为a:b:c:d:e:f ip 为10.10.10.10的主机将接受该ip包。 

而其他同网段的主机将忽视该ip包。因此 ip包的接受是根据mac而不是ip地址。 


F3. 如果我欺骗arp表，那么我可以接受该ip包吗？ 


A 可以。。通常的arp spoof就是根据这个过程，冒用合法主机的mac, 可以接收到非法 

数据。但是前提是该网段使用动态arp表。如果该网段由某台坚固的主机维护一个静态 

arp表，arp spoof 将失败。 


F4, 如果我想使用ip spoof , 我要如何处理ip路由问题？ 


A 使用ip spoof 并且要跨网段是很复杂的问题。在理论上我个人认为可以实现，但是 

实际操作并不那么简单。如果在同网段，那么你不必关心路由的问题。如果在别的 

网段，那么应该考虑除了按正常的ip spoof处理过程外，还要使用在该网段内某台 

合法主机的sniff转接。 


F5. 可以在交换环境使用sniff吗？ 


A 不可以。但是可以配合spoof . 交换环境下，HUB 根据 mac来处理，而mac列表通常 

为静态，因此HUB可以不经由广播来处理ip路径，而直接根据mac将ip发送给目标机器。 

如何配合spoof我以前有讨论过。
