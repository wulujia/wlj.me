---
title: "用Tor实现有效和安全的互联网访问"
date: 2005-01-22T00:00:00+08:00
tags: ["Tech", "Tools", "Security"]
draft: false
slug: "tor"
---

吴鲁加 01/22/2005

## 一、为什么写？

google以很有创意的推广方式推出gmail后，在国内很是热闹了一段时间，但随即大家发现，gmail似乎不如传说中的那么好用，虽然号称容量上G，但总是动不动就弹出个对话框："Oops...unable to reach Gmail. Please check your internet connection and try again."，什么操作都是不灵光的。"什么google，骗人罢了……"很多朋友可能会这样想。

其实，google又何尝不想快？只是，很多事情，想是没有用的。本文仅从技术角度说明一种可以有效访问gmail的方法，供拥有gmail帐号但却难以正常连接的朋友参考。

## 二、什么是Tor？

Tor的全称是"The Onion Router"号称是"An anonymous Internet communicaton system"，主页在：http://tor.eff.org 。

它针对现阶段大量存在的流量过滤、嗅探分析等工具，在JAP之类软件基础上改进的，支持Socks5，并且支持动态代理链（通过Tor访问一个地址时，所经过的节点在Tor节点群中随机挑选，动态变化，由于兼顾速度与安全性，节点数目通常为2-5个），因此难于追踪，有效地保证了安全性。另一方面，Tor的分布式服务器可以自动获取，因此省却了搜寻代理服务器的精力。

下图是一个简单的Tor安全访问与危险访问的区别示意图：

![Tor工作原理](/images/tor-1.png)

## 三、如何安装与使用Tor

### 3.1 Debian上的安装与使用

#### 3.1.1 安装Tor及相关工具

在 `/etc/apt/sources.list` 中增加如下两行：

```
deb http://mirror.noreply.org/pub/tor stable main
deb-src http://mirror.noreply.org/pub/tor stable main
```

然后运行：

```bash
apt-get update && apt-get install tor tsocks
```

安装完毕后系统会创建Debian-tor的用户，并且以该用户的身份启动tor，开机自动起动，可以在 `/etc/rc2.d/` 下进行调整。

#### 3.1.2 编辑相关配置文件

需要编辑的文件其实只有一份，即 `/etc/tsocks.conf`，只需要三行即可：

```
server = 127.0.0.1
server_type = 5
server_port = 9050
```

要用Tor进行代理的程序，以tsocks启动，比如，希望用Tor代理所有web访问，则可以运行：

```bash
$ tsocks firefox
```

### 3.2 Windows上的安装与使用

在Windows上的使用要更为简单些，可以参考 http://tor.eff.org/cvs/tor/doc/tor-doc-win32.html 上的详细图形介绍。

也可以将Tor+Privoxy+OpenSSL+SocksCap32(SocksCap32可以用FreeCap替代)联合使用，将OpenSSL的库解压到Tor安装目录，最终你的Tor目录应该有至少 `libeay32.dll`、`ssleay32.dll`、`tor.exe`、`tor_resolve.exe` 等几份文件。

运行Tor会开启一个dos窗口，提示运行情况，可以置于后台，必要时可以编辑 `C:\Documents and Settings\User Name\Application Data\tor` 下面的配置文件torrc（通常不必）。之后运行Sockscap32，设置服务器地址为：`Socks5:127.0.0.1:9050`，将常用工具拉入Sockscap32运行即可。

### 3.3 测试

安装完毕后，打开浏览器，连接到检查proxy的地址：http://proxyjudge.com/prxjdg.cgi ，如果页面上找不到你现在自身的IP地址，说明已经能够通过tor代理上网了。

这时再试试连接 http://www.gmail.com ，就应该能够正常访问了。

## 四、写在最后

通过Tor不仅能够进行web浏览，实际上多数网络应用程序都能通过它进行透明socks代理。

最后介绍几款参考工具，可以与Tor联合使用，通过一些有创意的组合，达到有效连接互联网络的目的，比如tk琢磨的多重加密等。

- stunnel http://www.stunnel.org
- socat http://www.dest-unreach.org/socat/
- privoxy http://www.privoxy.org/
- snake http://xfocus.net/tools/200209/361.html

感谢flag告诉我这个软件，感谢tk提供的一些更有效访问互联网的思路。
