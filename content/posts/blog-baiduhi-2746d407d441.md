---
title: "IE 7.0 漏洞临时解决方案(zz)"
date: 2008-12-11T11:02:00+08:00
tags: ["Life"]
draft: false
slug: "blog-baiduhi-2746d407d441"
---

[http://www.sucop.com/html/504.html](http://www.sucop.com/html/504.html)

一、事件说明

发布时间：2008-12-09

受影响的软件及系统：Microsoft Internet Explorer 7

微软 IE 7 浏览器被发现存在一个严重0day漏洞，HTML文件中错误格式的标签可以导致微软 IE 7 浏览器使用已被释放的对象的内存作为虚函数指针进行调用。成功利用该漏洞可以执行任意代码。

该漏洞是一个“0day”漏洞，被发现后通过地下漏洞黑市交易而扩散，进而被大量“挂马”攻击者所使用。所以目前尚无微软官方安全补丁可用。

二、临时解决方案

由于微软尚未正式推出补丁，很多企业都在咨询解决方案，目前我们建议：

1、暂时不要使用IE 7浏览器，可以使 Firefox 或 Opera 等非 IE 内核浏览器；

2、为IE打开系统的数据执行保护功能，虽然不能阻止漏洞的触发但有助于增加攻击者利用漏洞的难度，方法如下：

      右键单击我的电脑 -> 属性  -> 高级 -> 性能  -> 设置 -> 数据执行保护

      选择“除所选之外，为所有程序和服务启用数据执行保护”

      如果里面有内容，确认下面的框里“Internet Explorer”前没有打勾

      重启电脑后，系统就开启了数据执行保护功能。

      如下图所示：

[![](http://hiphotos.baidu.com/wulujia/abpic/item/cba60a46ce3fdc146b63e5cf.jpg)](http://hiphotos.baidu.com/wulujia/pic/item/cba60a46ce3fdc146b63e5cf.jpg)
