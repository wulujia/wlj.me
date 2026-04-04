---
title: "用monit监视与保护进程"
date: 2007-04-16T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2576"
---

[monit](http://www.tildeslash.com/monit/)是一款用于Unix系统的进程监视与保护程序，在Debian和Ubuntu下，只需要运行：

# apt-get install monit

即可安装完毕，其它系统下，也是简单的 ./configure && make
&& make install 三部曲。

安装完毕后，需要调整两份文件：

**1、/etc/default/monit**

> startup=1 # 设置程序启动
> 
> CHECK_INTERVALS=120 # 每 120 秒检查一次进程

**2、/etc/monit/monitrc**

> # 这里仅以 Apache 为例
> 
> check process apache with pidfile /var/run/apache2.pid # 检查 pid
> 文件
> 
>    group www-data # 检查程序启动时的用户组
> 
>    start program = "/etc/init.d/apache2 start" #
> 启动程序的脚本
> 
>    stop  program = "/etc/init.d/apache2 stop" 
> # 停止程序的脚本
> 
>    if failed host localhost port 443 type TCPSSL
> 
>         protocol HTTP then
> restart  # 以一定的协议检查端口是否开放
> 
>    if 5 restarts within 5 cycles then
> timeout

配置文件的写法简洁，功能非常丰富，也可以用来检查远程或本地主机开放端口情况等。如果需要
web 输出，也可以配合 apache
生成一个进程状态检测的图表。更详细的信息和配置样例，可以参考它的[安装说明](http://www.tildeslash.com/monit/doc/install.php)和[配置样例](http://www.tildeslash.com/monit/doc/examples.php)。

初步测试，还是比较稳定可靠的，推荐使用。与[WatchDog](http://wulujia.com/Article_60533)相比，monit运行于应用层，能够监测的项目不如WatchDog，并且如果一些底层应用出现问题时，很可能无法监视和控制。但它的优点在于无需重新编译内核，配置简单可靠，不用担心配置失误导致的系统故障（我在配置WatchDog时就出过不少洋相）。
