---
title: "用Tor实现有效和安全的互联网访问"
date: 2005-01-22T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-699"
---

Tor的全称是“The Onion Router“号称是“An anonymous Internet communicaton
system”。
它针对现阶段大量存在的流量过滤、嗅探分析等工具，在JAP之类软件基础上改进的，支持Socks5，并且支持动态代理链（通过Tor访问一个地址时，所
经过的节点在Tor节点群中随机挑选，动态变化，由于兼顾速度与安全性，节点数目通常为2-5个），因此难于追踪，有效地保证了安全性。另一方面，Tor
的分布式服务器可以自动获取，因此省却了搜寻代理服务器的精力。

详见：[http://risker.org](http://risker.org/tech/Tor/)
