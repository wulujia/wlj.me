---
title: "用watchdog保证服务器程序运行稳定"
date: 2007-03-20T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2519"
---

**1、重新编译内核，加入watchdog**

> Device Drivers ->
> 
>   Character Devices ->
> 
>     Watchdog Cards ->
> 
>       [*] Watchdog Timer Support
> 
>       [ ]   Disable watchdog
> shutdown on close
> 
>       ---   Watchdog Device
> Drivers
> 
>       <*> Your Watchdog card or
> chip

**2、安装watchdog程序**

# apt-get install watchdog

**3、配置watchdog**

可以参考的文档包括：

> http://gentoo-wiki.com/HOWTO_Watchdog_Timer
> 
> man 8 watchdog
> 
> man 5 watchdog.conf
> 
> /usr/share/doc/watchdog/examples

我只是用它来保障sshd、apache和mysql运行稳定。

**4、确保apache、ssh和mysql在watchdog之前起来**

重起机器后，watchdog会查找这三个进程的pid，如果不存在，默认会重起机器（除非我们设置了repair
binary），因此，一定要在启动脚本中改变启动顺序，让watchdog在这三者启动之后才启用。

**5、设置repair脚本**

我并不想这几个应用程序随便出点啥事就重启计算机，所以，写了个简单的脚本：

> root@wlj:/var/run# cat /usr/sbin/repair.sh
> 
> #!/bin/sh
> 
> 
> 
> if [ -x /etc/init.d/networking ]; then
> 
>     # Debian
> 
>     /etc/init.d/networking restart
> 
> elif [ -x /etc/rc.d/init.d/network ]; then
> 
>     # Redhat
> 
>     /etc/rc.d/init.d/network restart
> 
> else
> 
>     echo "Couldn't find network script to relaunch
> networking. Please edit $0" | logger -i -t repair -p
> daemon.info
> 
>     exit $1
> 
> fi
> 
> 
> 
> if [ -x /etc/rc.local ]; then
> 
>     /etc/rc.local
> 
> else
> 
>     echo "rc.local restart error" |logger -i -t
> repair -p daemon.info
> 
>     exit $1
> 
> fi
> 
> 
> 
> if [ -x /etc/init.d/apache2 ]; then
> 
>     /etc/init.d/apache2 restart
> 
> else
> 
>     echo "apache restart error" |logger -i -t repair
> -p daemon.info
> 
>     exit $1
> 
> fi
> 
> 
> 
> if [ -x /etc/init.d/ssh ]; then
> 
>     /etc/init.d/ssh restart
> 
> else
> 
>     echo "sshd restart error" |logger -i -t repair
> -p daemon.info
> 
>     exit $1
> 
> fi
> 
> 
> 
> if [ -x /etc/init.d/mysql ]; then
> 
>     /etc/init.d/mysql restart
> 
> else
> 
>     echo "mysql restart error" |logger -i -t repair
> -p daemon.info
> 
>     exit $1
> 
> fi
> 
> exit 0

**6、测试watchdog是否成功启用**

试着杀断ssh，然后看/var/log/syslog中的日志

> Mar 20 11:34:26 SH600 watchdog[11662]: cannot open
> /var/run/sshd.pid (errno = 2 = 'No such file or directory')
> 
> Mar 20 11:34:28 SH600 mysqld[29396]: 070320 11:34:28 [Note]
> /usr/sbin/mysqld: Normal shutdown
> 
> Mar 20 11:34:28 SH600 mysqld[29396]:
> 
> Mar 20 11:34:28 SH600 mysqld[29396]: 070320 11:34:28  InnoDB:
> Starting shutdown...
> 
> Mar 20 11:34:30 SH600 mysqld[29396]: 070320 11:34:30  InnoDB:
> Shutdown completed; log sequence number 0 43655
> 
> Mar 20 11:34:30 SH600 mysqld[29396]: 070320 11:34:30 [Note]
> /usr/sbin/mysqld: Shutdown complete
> 
> Mar 20 11:34:30 SH600 mysqld[29396]:
> 
> Mar 20 11:34:30 SH600 mysqld_safe[883]: ended
> 
> Mar 20 11:34:31 SH600 mysqld_safe[988]: started
> 
> Mar 20 11:34:31 SH600 mysqld[991]: 070320 11:34:31  InnoDB:
> Started; log sequence number 0 43655
> 
> Mar 20 11:34:31 SH600 mysqld[991]: 070320 11:34:31 [Note]
> /usr/sbin/mysqld: ready for connections.
> 
> Mar 20 11:34:31 SH600 mysqld[991]: Version:
> '5.0.24a-Debian_9ubuntu1-log'  socket:
> '/var/run/mysqld/mysqld.sock'  port: 3306  Debian etch
> distribution
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1034]: Checking for
> crashed MySQL tables.
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1044]: Upgrading
> MySQL tables if necessary.
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]: This script
> updates all the mysql privilege tables to be usable by
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]: MySQL 4.0 and
> above.
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]:
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]: This is needed
> if you want to use the new GRANT functions,
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]: CREATE
> AGGREGATE FUNCTION, stored procedures, or
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]: more secure
> passwords in 4.1
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]:
> 
> Mar 20 11:34:32 SH600 /etc/mysql/debian-start[1048]:
> done
