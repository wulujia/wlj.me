---
title: "nagios监控系统安装(1)"
date: 2008-12-21T21:00:00+08:00
tags: ["AI", "Life"]
draft: false
slug: "blog-baiduhi-84f6033b"
---

nagios http://www.nagios.org

完整的nagios中包含几个组成部分：

1、nagios软件本身，必须安装；

2、plugins，必须安装，是nagios用来监测远程主机运行状况的一系列小程序，安装后默认在/usr/local/nagios/libexec下；

3、npre，非必需，如果希望对机器的磁盘、进程、负载等状况进行监测并报警，那么就需要在该机器上安装；

4、ndoutils，非必需，将nagios的数据保存到mysql数据库中。

一篇不错的文章在：http://www.linuxtone.org/viewthread.php?tid=514，我学习了他的方法。

Nagios官网文档中有在Ubuntu下的安装指南，Debian基本相同：http://nagios.sourceforge.net/docs/3_0/quickstart-ubuntu.html。

我准备采用的应用程序路径都是默认的，如：

/usr/local/nginx

/usr/local/nagios

1、安装前的一些准备

安装部分软件：apt-get install build-essential libgd2-xpm-dev libssl-dev openssl libkrb5-dev

安装好web服务器，我用的是nginx，可以采用apache会更方便。

2、准备用户、用户组

/usr/sbin/useradd -m nagios

/usr/sbin/groupadd nagcmd

/usr/sbin/usermod -a -G nagcmd nagios

/usr/sbin/usermod -a -G nagcmd www-data

3、安装nagios

到http://www.nagios.org/download/download.php下载最新的Nagios和Nagios plugins。

解压后，进入nagios目录：

./configure --with-command-group=nagcmd

make all

make install

make install-init

make install-config

make install-commandmode

进入nagios plugins目录：

./configure --with-nagios-user=nagios --with-nagios-group=nagios

make

make install

4、配置nginx支持perl fcgi

nginx要支持perl fcgi，可以采用脚本perl-fcgi.pl如下：

#!/usr/bin/perl

use FCGI;

#perl -MCPAN -e 'install FCGI'

use Socket;

#this keeps the program alive or something after exec'ing perl scripts

END() { } BEGIN() { }

*CORE::GLOBAL::exit = sub { die "fakeexit\nrc=".shift()."\n"; }; eval q{exit}; if ($@) { exit unless $@ =~ /^fakeexit/; } ;

&main;

sub main {

                 #$socket = FCGI::OpenSocket( ":3461", 10 ); #use IP sockets

                 $socket = FCGI::OpenSocket( "/var/run/nagios.sock", 10 ); #use UNIX sockets - user running this script must have w access to the 'nginx' folder!!

                 $request = FCGI::Request( \*STDIN, \*STDOUT, \*STDERR, \%ENV, $socket );

                 if ($request) {request_loop()};

                         FCGI::CloseSocket( $socket );

}

sub request_loop {

                 while( $request->Accept() >= 0 ) {

                    #processing any STDIN input from WebServer (for CGI-GET actions)

                    $env = $request->GetEnvironment();

                    $stdin_passthrough ='';

                    $req_len = 0 + $ENV{CONTENT_LENGTH};

                    if ($ENV{REQUEST_METHOD} eq 'GET'){

                                 $stdin_passthrough .= $ENV{'QUERY_STRING'};

                         }

                         #running the cgi app

                         if ( (-x $ENV{SCRIPT_FILENAME}) &&  #can I execute this?

                                  (-s $ENV{SCRIPT_FILENAME}) &&  #Is this file empty?

                                  (-r $ENV{SCRIPT_FILENAME})      #can I read this file?

                         ){

                                 #http://perldoc.perl.org/perlipc.html#Safe-Pipe-Opens

                 open $cgi_app, '-|', $ENV{SCRIPT_FILENAME}, $stdin_passthrough or print("Content-type: text/plain\r\n\r\n"); print "Error: CGI app returned no output - Executing $ENV{SCRIPT_FILENAME} failed !\n";

                                 if ($cgi_app) {print <$cgi_app>; close $cgi_app;}

                         }

                         else {

                                 print("Content-type: text/plain\r\n\r\n");

                                 print "Error: No such CGI app - $req_len  - $ENV{CONTENT_LENGTH} - $ENV{REQUEST_METHOD} - $ENV{SCRIPT_FILENAME} may not exist or is not executable by this process.\n";

                         }

                 }

}

该脚本由start_nginx_cgi.sh调用启动，start_nginx_cgi.sh脚本如下：

#!/bin/bash

## start_nginx_cgi.sh: start nginx cgi mode

## ljzhou, 2007.08.20

PERL="/usr/bin/perl"

NGINX_CGI_FILE="/usr/local/nagios/bin/perl-cgi.pl"

#bg_num=`jobs -l |grep "NGINX_CGI_FILE"`

#PID=`ps aux|grep "perl-cgi"|cut -c10-14|xargs kill -9`

PID=`ps aux|grep 'perl-cgi'|cut -c10-14|sed -n "1P"`

echo $PID

sockfiles="/var/run/nagios.sock"

kill -9 $PID

$PERL $NGINX_CGI_FILE &

sleep 3

`chown www-data.www-data $sockfiles`

# EOF: start_nginx_cgi.sh

之后运行/usr/local/nagios/bin/start_nginx_cgi.sh，并将它加到/etc/rc.local中。

nginx中加入对nagios的配置——我是直接做了个从/usr/local/nagios/sbin到web根目录下nagios的链接，并在相关vhost文件中增加：

         location ~ \.cgi$ {

                 root /usr/local/nagios/sbin;

                 rewrite ^/nagios/cgi-bin/(.*)\.cgi /$1.cgi break;

                 fastcgi_index index.cgi;

                 auth_basic               "Restricted";

                 auth_basic_user_file     nagios.pw;

                 fastcgi_pass     unix:/var/run/nagios.sock;

                 fastcgi_param    SCRIPT_FILENAME                      /usr/local/nagios/sbin$fastcgi_script_name;

                 fastcgi_param    QUERY_STRING                         $query_string;

                 fastcgi_param    REMOTE_ADDR                         $remote_addr;

                 fastcgi_param    REMOTE_PORT                         $remote_port;

                 fastcgi_param    REQUEST_METHOD                      $request_method;

                 fastcgi_param    REQUEST_URI                         $request_uri;

                 #fastcgi_param  SCRIPT_NAME                         $fastcgi_script_name;

                 fastcgi_param    SERVER_ADDR                         $server_addr;

                 fastcgi_param    SERVER_NAME                         $server_name;

                 fastcgi_param    SERVER_PORT                         $server_port;

                 fastcgi_param    SERVER_PROTOCOL                     $server_protocol;

                 fastcgi_param    SERVER_SOFTWARE                     nginx;

                 fastcgi_param    CONTENT_LENGTH                      $content_length;

                 fastcgi_param    CONTENT_TYPE                        $content_type;

                 fastcgi_param    GATEWAY_INTERFACE                   CGI/1.1;

                 fastcgi_param    HTTP_ACCEPT_ENCODING         gzip,deflate;

                 fastcgi_param    HTTP_ACCEPT_LANGUAGE         zh-cn;

                 }

之后重启nginx。

dbanotes提到过另一种使用perl fastcgi的方法，他的文章在：

http://www.dbanotes.net/techmemo/nginx_awstats_fastcgi_for_perl.html

其中提到的脚本参见：http://www.nginx.eu/nginx-fcgi.html

有时间的同学可以试试。

5、调整nagios配置文件

需要调整的文件包括：

/usr/local/nagios/etc/nagios.cfg

/usr/local/nagios/etc/cgi.cfg

/usr/local/nagios/etc/server/test.cfg

a./usr/local/nagios/etc/nagios.cfg

这是nagios的主配置文件，加入一句：

cfg_dir=/usr/local/nagios/etc/servers

b./usr/local/nagios/etc/cgi.cfg

use_authentication=0 #其实不推荐这样做，后续会做调整

c./usr/local/nagios/etc/server/hostgroup.cfg

在这里可以对服务器进行分组，这里的示例只有一组：

define hostgroup{

hostgroup_name update

alias update server 

members test

}

d./usr/local/nagios/etc/server/test.cfg

这个test.cfg实际上是一台测试的受监控服务器，可以简单配置监控存活、HTTP、FTP，文件如下：

define host {

        host_name                      test 

        address                        61.123.120.10

        check_command               check-host-alive

        max_check_attempts          4

        notification_interval       300

        notification_period         24x7

        notification_options        d,u,r

        contact_groups              admins

        }

define service {

         host_name                      test 

         check_period           24x7

         max_check_attempts     4

         normal_check_interval 1

         retry_check_interval  1

         contact_groups         admins

         notification_interval    600

         notification_period      24x7

         notification_options     w,u,c,r

         check_command check_ping!100.0,20%!500.0,60%

         }

define service{

         host_name                      test 

         service_description              HTTP

         check_period           24x7

         max_check_attempts     4

         normal_check_interval 1

         notification_interval    600

         notification_period      24x7

         notification_options     w,u,c,r

         contact_groups         admins

         check_command                    check_http

         notifications_enabled            1

         }

define service{

         host_name                      test 

         service_description              FTP 

         check_period           24x7

         max_check_attempts     4

         normal_check_interval 1

         notification_interval    600

         notification_period      24x7

         notification_options     w,u,c,r

         contact_groups         admins

         check_command                   check_ftp

         }
