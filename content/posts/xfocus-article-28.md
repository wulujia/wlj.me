---
title: "sniffit的安装使用简述(linux)"
date: 2000-01-05T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-28"
---

文章提交：[quack](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

sniffit的安装使用简述(linux) 

=========================== 

by quack 

[http://www.xfocus.org](http://www.xfocus.org/) 安全焦点

Sniffit是由Lawrence Berkeley Laboratory开发的，可以在Linux、Solaris、SGI等各种平台运行的 网

络监听软件，它主要是针对TCP/IP协议的不安全性对运行该协议的机器进行监听――当然，数据包必须 

经过运行sniffit的机器才能进行监听，因此它只能够监听在同一个网段上的机器。而且还能够自由地为

其 增加某些插件以实现额外功能。

一、安装 软件的安装很简单:

1、用tar zvfx sniffit.*.*.*.tgz将下载下来的sniffit.*.*.*.tgz解压缩到你想要的目的文件夹， 如

果版本是0.3.7的话（应该是最新版本吧，我不敢确定……），你会看到该目录下出现一个 

sniffit.0.3.7的目录。 

2、cd sniffit.0.3.7 

3、./configure && make ，只要在这个过程中终端上没有意外的error信息出现，你就算编译成功 了―

―可以得到一个二进制的sniffit文件。 

4、make clean把不用的垃圾扫掉…… 

二、使用方法 

1、参数 

这个东东具有如下的命令选项： 

-v 显示版本信息 

-t <ip nr/name> 让程序去监听指定流向某IP的数据包 

-s <ip nr/name>让程序去监听从某IP流出的IP数据包，可以使用@通配符，如 -t 199.145.@ 

-i 显示出窗口界面，能察看当前在你所属网络上进行连接的机器 

-I 扩展的交互模式，忽略所有其它选项，比-i强大得多…… 

-c <file> 利用脚本来运行程序 

-F <device> 强制使程序使用网络硬盘 

-n 显示出假的数据包。象使用ARP、RARP或者其他不是IP的数据包也会显示出来 

-N 只运行plugin时的选项，使其它选项失效 

在-i 模式下无法工作的参数： 

-b 同时做-t和-s的工作…… 

-d 将监听所得内容显示在当前终端――以十六进制表示 

-a 将监听所得内容显示在当前终端――以ASCII字符表示 

-x 打印TCP包的扩展信息(SEQ, ACK, Flags)，可以与'-a', '-d', '-s', '-t', '-b'一起运作，注意―

―它是输出在标准输出的，如果只用-t,-s,-b 而没有其它参数配合的话不会被写入文件。 

-R <file> 将所有通信记录在文件中 

-r <file> 这一选项将记录文件送往sniffit,它需要-F的参数配合指明设备，假设你用 'eth0'(第一块网

卡)来记录文件，你必须在命令行里面加上'-F eth0'或者 '或者'或者'或者'或者'-F eth' -A 遇到不认

识的字符时用指定的字符代替 

-P <protocol> 定义监听的协议，DEFAULT为TCP――也可以选IP、ICMP、UDP…… 

-p <prot >定义监听端口，默认为全部 

-l <length> 设定数据包大小，default是300字节。 

-M <plugin> 激活插件 

-I，-i 模式下的参数 

-D <device> 所有的记录会被送到这个磁盘上。 

-c 模式下的参数 

-L<logparam>

其中logparam可以是如下的内容： 

raw : 轻度 

norm : 常规 

telnet: 记录口令（端口23） 

ftp : 记录口令（端口21） 

mail : 记录信件内容（端口25） 

比如说"ftpmailnorm"就是一个合法的logparam 

2、图形仿真界面 

就是上面所说的-i选项啦，我们输入sniffit -i 会出现一个窗口环境，从中可以看到自己所在的 网络中

有哪些机器正在连接，使用什么端口号，其中可用的命令如下：

q 退出窗口环境，结束程序 

r 刷新屏幕，重新显示正在在连线的机器 

n 产生一个小窗口，包括TCP、IP、ICMP、UDP等协议的流量 

g 产生数据包，正常情况下只有UDP协议才会产生，执行此命令要回答一些关于数据包的问题 

F1 改变来源网域的IP地址，默认为全部 

F2 改变目的网域的IP地址，默认为全部 

F3 改变来源机器的端口号，默认为全部 

F4 改变目的机器的端口号，默认为全部 

3、一些示例 

假设有以下的设置：在一个子网中有两台主机，一台运行了sniffer，我们称之为sniffit.com，另 一台

是66.66.66.7，我们称之为target.com。

1、你希望检查sniffer是否能运行 

sniffit:~/# sniffit -d -p 7 -t 66.66.66.7 

并且开另一个窗口:

sniffit:~/$ telnet target.com 7 

你可以看到sniffer将你telnet到对方7号端口echo服务的包捕获了。 

2、你希望截获target.com上的用户密码 

sniffit:~/# sniffit -p 23 -t 66.66.66.7 

3、target.com主机的根用户声称有奇怪的FTP连接并且希望找出他们的击键

sniffit:~/# sniffit -p 21 -l 0 -t 66.66.66.7 

4. 你希望能阅读所有进出target.com的信件 

sniffit:~/# sniffit -p 25 -l 0 -b -t 66.66.66.7 & 

或者

sniffit:~/# sniffit -p 25 -l 0 -b -s 66.66.66.7 & 

5. 你希望使用用户交互界面 

sniffit:~/# sniffit -i 

6. 有错误发生而且你希望截获控制信息

sniffit:~/# sniffit -P icmp -b -s 66.66.66.7 

7. Go wild on scrolling the screen. 

sniffit:~/# sniffit -P ip -P icmp -P tcp -p 0 -b -a -d -x -s 66.66.66.7 

与之效果相当的是 

sniffit:~/# sniffit -P ipicmptcp -p 0 -b -a -d -x -s 66.66.66.7 

8. 你可以用'more 66*'读取下列方式记录下的密码 

sniffit:~/# sniffit -p 23 -A . -t 66.66.66.7 

或者

sniffit:~/# sniffit -p 23 -A ^ -t dummy.net 

  

三、高级应用 

1、用脚本执行 

这是配合选项-c的，其执行方法也很简单，比如以如下方式编辑一个叫sh的文件

select from host 180.180.180.1

select to host 180.180.180.10 

select both port 21 

然后执行：sniffit -c sh 

说明：监听从180.180.180.1送往180.180.180.10的数据包，端口为FTP口。这里不做更多说明，你 可以

自己去看里面的README。

2、插件 

要获取一个插件是很简单的，你将它放入sniffit的目录下，并且象如下方式编辑sn_plugin.h 文件：

#define PLUGIN1_NAME "My plugin" 

#define PLUGIN1(x) main_plugin_function(x) 

#include "my_plugin.plug" 

注意: 

a) 你可以让plugin从0-9，所以从PLUGIN0_NAME到PLUGIN1_NAME……不必是连续的 

d) #include "my_plugin.plug" 这是我的插件源代码放置的地方。 如果想详细了解的话，还是看看里面

的plugin.howto吧。

3、介绍 tod

这东东便是sniffit最有名的一个插件了，为什么叫TOD呢――touch of death,它可以轻易地切断一个 

TCP连接，原理是向一个TCP连接中的一台主机发送一个断开连接的IP包，这个IP包的RST位置1，便可以了

。

将下载下来的tod.tar.gz拷贝到sniffit所在目录下，解压安装后

ln -s tod sniffit_key5 

就可以将这相程序与F5键连接起来，想切断哪台机器的话，只要在窗口中将光标指到需要断线的机器上 

按下F5键就可以了。你可以自由地定义成其它的F功能键――F1~F4不行，它们已经被定义过了…… 

写了这么多，好了，下课……
