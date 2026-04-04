---
title: "libfetion短信通知与nagios整合"
date: 2008-12-21T21:01:00+08:00
tags: ["AI", "Life"]
draft: false
slug: "blog-baiduhi-1fae7931"
---

由于安装了nagios，就比较希望服务器出现状况的时候，我能够及时收到报警信息——飞信这时就是最好的选择了。

1、激活手机上的飞信

移动飞信下载地址：http://www.fetion.com.cn/，激活后，记住密码。

2、下载编译sendsms小程序

参见BLOG：http://blog.solrex.cn/articles/diy-free-weather-forecast-sms.html

sendsms实际上用了libfetion的库：http://libfetion.cn/Linux_demoapp_download.html

感谢这两位开发者。

在编译sendsms的时候遇到了问题，提示“__stack_chk_fail_local”，在libfetion论坛上也有人问起：

http://www.libfetion.cn/bbs/viewthread.php?tid=120&extra=page%3D1

解决方法很简单，将Makefile里CPP = g++后面加上-fstack-protector即可。

使用时发现，如果用手机号码，对方可能会收不到信息（sendsms作者代码中说可能是libfetion的bug），改用fetion号码就好了。

顺便提一句，本来我是想用“飞信机器人”的：http://www.it-adv.net/。

可是在debian上一运行就出现：/lib/tls/i686/cmov/libc.so.6: version `GLIBC_2.4' not found，放弃了。

3、配置nagios调用

编译好的sendsms我放到了/usr/local/fetion下面，同时在该目录下使用一个脚本sms.sh：

#!/bin/sh

/usr/local/fetion/sendsms -f 442103729 -p mypassword "$1"

在/usr/local/nagios/etc/objects/commands.cfg中新增：

#host notify by sms

define command {

command_name      notify-host-by-sms

command_line      /usr/local/fetion/sms.sh "Host $HOSTSTATE$ alert for $HOSTNAME$! on '$DATETIME$'">/dev/null 2>&1

}

#service notify by sms

define command {

command_name      notify-service-by-sms

command_line      /usr/local/fetion/sms.sh "'$HOSTADDRESS$' $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$">/dev/null 2>&1

}

在/usr/local/nagios/etc/objects/contacts.cfg中将service_notification_commands和host_notification_commands都新增sms提醒项目：

service_notification_commands     notify-service-by-email,notify-service-by-sms

host_notification_commands        notify-host-by-email,notify-host-by-sms

测试：/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg

重新载入nagios配置文件：/etc/init.d/nagios restart

4、停掉某个服务，测试是否nagios监测到，并且通过sms发了提醒消息
