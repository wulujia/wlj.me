---
title: "cacti监控系统安装"
date: 2008-12-21T20:59:00+08:00
tags: ["AI", "Life"]
draft: false
slug: "blog-baiduhi-08637bec3c68"
---

现在托管的服务器数量在增加，前段时间，已经不断出现各种由于系统管理水平不够，导致的服务器当机、系统不稳定等事件。

因此最近决定安装cacti和nagios这两套开源服务器监控的软件系统，对我们的服务器系统进行监控和报警。

cacti http://www.cacti.net/

这里是精简的安装指南：

http://www.cacti.net/downloads/docs/html/unix_configure_cacti.html

我在debian的安装过程如下：

1、安装辅助软件

apt-get install rrdtool snmp ttf-dejavu libmysql++-dev

2、配置web服务器和安装php

可以参照文章：http://hi.baidu.com/wulujia/blog/item/c6aba7efbb95ef11fcfa3c67.html

3、导入mysql数据库

mysqladmin -u root -p create cacti

mysql -uroot -p cacti <cacti.sql

mysql -uroot -p

mysql>grant all privileges on cacti.* to m1@localhost identified by 'password';

mysql> flush privileges;

4、编辑include/config.php文件，填入相关数据库信息，类似如下：

$database_type = "mysql";

$database_default = "cacti";

$database_hostname = "localhost";

$database_username = "cactiuser";

$database_password = "cacti";

5、设置目录权限

chmod 777 rra/ log/

6、在/etc/crontab下新建一行，内容如下：

*/5 *    * * *    root     /usr/local/php-fcgi/bin/php /home/web/cacti/poller.php > /dev/null 2>&1

7、将cacti的安装包解压到web根目录，改名为cacti，通过web访问该目录。

8、在Device菜单新建设备，之后Create Graphs for this Host，在Graph Trees、Data Sources做调整；

9、Debian的客户机要开启snmpd，需要：

apt-get install snmpd

编辑/etc/default/snmpd，将其中的127.0.0.1改为本机IP地址

编辑/etc/snmp/snmpd.conf，设置community string如下

#com2sec paranoid  default          public

com2sec readonly  default           mycommunitystring

运行/etc/init.d/snmpd restart重启snmpd。

10、Windows的客户机要开启snmpd，需要安装snmp service和snmp trap service：

打开 控制面板-->添加删除程序-->添加/删除windows组件-->管理和监视工具，选中并且安装

设置时打开控制面板-->管理工具-->服务-->snmp service，点击右键，属性-->代理随意输入联系人、位置，然后在“安全”处设置community string和允许的监控主机IP地址。
