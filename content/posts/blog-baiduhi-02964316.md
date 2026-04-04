---
title: "铁卷防泄密网关部份压力测试数据"
date: 2011-06-26T19:57:00+08:00
tags: ["Life"]
draft: false
slug: "blog-baiduhi-02964316"
---

时间：2011-05-22

作者：anonymous@unnoo.com，大成天下

关键词：数据防泄露,加密,安全网关,压力测试

一、测试环境

由于铁卷防泄密网关近期要在大用户环境下部署，因此希望测试出其能承载的压力情况，测试环境如下：

[![](http://hiphotos.baidu.com/wulujia/pic/item/1d595982c8829fc20df4d267.jpg)](http://blog.unnoo.com/wp-content/uploads/2011/05/bridge.png)

后台web服务器：dell 2950双核，8G内存，千兆网卡

铁卷防泄密网关：赛扬1.6，2G内存，双百兆intel网卡

前端LoadRunner测试机：AMD Athlon64 2.20GH双核，1G内存，百兆网卡

每台LoadRunner测试机模拟一千用户并发，分别测试1000用户、3000用户下通过网桥访问后端web服务器时，网桥的性能损耗情况。

二、初步结论

在3000用户同时并发访问的情况下，铁卷防泄密网关仍然能够稳定地提供服务，所有连接都能够成功建立，并且铁卷防泄密网关本身系统资源占用不超过25%。

部份截图如下，下图是没有并发压力情况下的铁卷防泄密网关资源占用情况，服务器CPU占用为0.7%，网关进程tfgfilter资源占用为零：
[![](http://hiphotos.baidu.com/wulujia/pic/item/a9b5bc3e08007c9a838b1367.jpg)](http://blog.unnoo.com/wp-content/uploads/2011/05/0.png)

1000用户时铁卷网关资源占用情况，CPU占用20.7%，其中tfgfilter占了15%：
[![](http://hiphotos.baidu.com/wulujia/pic/item/32e6a61e15e6b27f40341767.jpg)](http://blog.unnoo.com/wp-content/uploads/2011/05/1000.png)

3000用户时铁卷网关资源占用情况，CPU占用22%，其中tfgfilter占了17%：
[![](http://hiphotos.baidu.com/wulujia/pic/item/f159970af17b6a7f94ca6b67.jpg)](http://blog.unnoo.com/wp-content/uploads/2011/05/3000.png)

从LoadRunner的测试情况看，所有的连接请求都成功建立，即便在3000用户并发访问的情况下，也没有到达性能瓶颈：

[![](http://hiphotos.baidu.com/wulujia/pic/item/17ebc917b80b2869c83d6d67.jpg)](http://blog.unnoo.com/wp-content/uploads/2011/05/loadrunner.png)

三、某用户处稳定运行超过3个月的铁卷防泄密网关

最近一个月的网络流量监测图，流出峰值曾达到36Mbps：

[![](http://hiphotos.baidu.com/wulujia/pic/item/cf53670900083faf3ac76367.jpg)](http://blog.unnoo.com/wp-content/uploads/2011/05/network.png)

最近一个月的CPU性能监测图，CPU负载一直在0.15以下：

[![](http://hiphotos.baidu.com/wulujia/pic/item/7b827609cb03e3cf2fddd467.jpg)](http://blog.unnoo.com/wp-content/uploads/2011/05/load.png)

相关文章：

用防泄密网关 保密加速度：http://blog.unnoo.com/?p=1365

用防泄密网关 保服务器数据：http://blog.unnoo.com/?p=1323
