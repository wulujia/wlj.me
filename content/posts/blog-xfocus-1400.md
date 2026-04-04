---
title: "Source quench received"
date: 2005-10-19T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1400"
---

晚上在 ping 两台 HP-UX 的服务器时，发现回应不太一样：

E:>ping 10.153.4.129

Pinging 10.153.4.129 with 32 bytes of data:

Reply from 10.153.4.129: Source quench received.
Reply from 10.153.4.129: Source quench received.

Ping statistics for 10.153.4.129:
Packets: Sent = 2, Received = 2, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:

志刚查了下资料，说没多大关系，是 HPUX 的一个老特性，只是这个 Interface 上的 ICMP 包到了一定限制，因此返回的拒绝包。在 HP-UX 11.X 上，可以用 ndd 命令查看：

ndd -get /dev/ip ip_send_source_quench 

值如果是 1，则表示此功能启用，可以将下面的命令放到：/etc/rc.config.d/nddconf

ndd -set /dev/ip ip_send_source_quench 0

关于 ICMP 控制信息的协议，可以参见：[http://www.faqs.org/rfcs/rfc792.html](http://www.faqs.org/rfcs/rfc792.html)
