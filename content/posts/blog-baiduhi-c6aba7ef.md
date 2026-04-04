---
title: "WEB服务器配置(nginx+php+mysql)"
date: 2008-12-21T20:57:00+08:00
tags: ["Life"]
draft: false
slug: "blog-baiduhi-c6aba7ef"
---

记录备忘，也供有需求的朋友参考，这篇主要是san@xfocus帮着配的:)

准备条件：

apt-get install gcc libxml2-dev libmysql++-dev libpng12-dev autoconf libpcre3-dev make bzip2 libevent-dev patch

--[ 1. 软件安装

1. PHP [http://www.php.net/](http://www.php.net/)，php-fpm [http://php-fpm.anight.org/](http://php-fpm.anight.org/)

# gzip -cd php-5.2.5-fpm-0.5.7.diff.gz | patch -d php-5.2.5 -p1

# ./configure \

--prefix=/usr/local/php-fcgi \

--enable-fastcgi \

--enable-discard-path \

--enable-force-cgi-redirect \

--enable-fpm \

--with-config-file-path=/usr/local/php-fcgi/etc \

--with-mysql \

--enable-inline-optimization \

--disable-debug \

--with-gd \

--with-zlib

# make && make install

# cp php.ini-recommended /usr/local/php-fcgi/etc/php.ini

2. eaccelerator [http://eaccelerator.net/](http://eaccelerator.net/)

# /usr/local/php-fcgi/bin/phpize

# ./configure \

--enable-eaccelerator=shared \

--with-php-config=/usr/local/php-fcgi/bin/php-config

# make && make install

3. memcache [http://pecl.php.net/package/memcache](http://pecl.php.net/package/memcache)

# /usr/local/php-fcgi/bin/phpize

# ./configure  \

--enable-memcache \

--with-zlib-dir \

--with-php-config=/usr/local/php-fcgi/bin/php-config

# make && make install

4. nginx [http://www.nginx.net/](http://www.nginx.net/)

# ./configure --prefix=/usr/local/nginx

# make && make install

5. memcached  [http://www.danga.com/memcached/download.bml](http://www.danga.com/memcached/download.bml)

# ./configure --prefix=/usr/local/memcached

# make && make install

6. MySQL http://www.mysql.com

# apt-get install mysql-server-5.0

# mysqladmin -u root -p password *newpassword*

--[ 2. 配置文件

1. php-fpm.conf

编辑/usr/local/php-fcgi/etc/php-fpm.conf文件

找到“Unix user of processes”和“Unix group of processes”两段，将前面注释去掉，并将值改为与nginx配置相同的用户和组。如下：

     Unix user of processes

     <value name=”user”>www-data</value>

     Unix group of processes

     <value name=”group”>www-data</value>

2. nginx.conf

user  www-data www-data;

worker_processes 2;

worker_rlimit_nofile 16384;

error_log  logs/error.log;

#error_log  logs/error.log  notice;

#error_log  logs/error.log  info;

pid         logs/nginx.pid;

events {

     worker_connections  10240;

     use epoll;

}

http {

     include        mime.types;

     default_type  application/octet-stream;

     log_format  main  '$remote_addr - $remote_user [$time_local] $request '

                       '"$status" $body_bytes_sent "$http_referer" '

                       '"$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for"';

     #access_log  logs/access.log  main;

     sendfile         on;

     tcp_nopush      on;

     #keepalive_timeout  0;

     keepalive_timeout  65;

     gzip on;

     gzip_min_length  1100;

     gzip_buffers      4 8k;

     gzip_proxied any;             

     gzip_types  text/plain text/html text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript;

     include vhost/stat.conf;

}

3. vhost/stat.conf

     server {

         listen        80;

         server_name  s.sucop.com;

         access_log  logs/stat.access.log  main buffer=64k;

         location / {

             root    /home/web/stat;

             index  index.php index.html index.htm;

         }

         #error_page  404               /404.html;

         error_page    500 502 503 504  /50x.html;

         location = /50x.html {

             root    html;

         }

         location ^~ /view/ {

             root    /home/web/stat;

             auth_basic            "Restricted";

             auth_basic_user_file mypasswordfile.pw;

             location ~ \.php$ {

                 include         fastcgi_params;

                 fastcgi_pass    127.0.0.1:9000;

                 fastcgi_index  index.php;

                 fastcgi_param  SCRIPT_FILENAME     /home/web/stat$fastcgi_script_name;

             }

         }

         location ~ \.php$ {

             include         fastcgi_params;

             fastcgi_pass    127.0.0.1:9000;

             fastcgi_index  index.php;

             fastcgi_param  SCRIPT_FILENAME     /home/web/stat$fastcgi_script_name;

         }

     }

注意配置文件里针对php的参数：

fastcgi_param  SCRIPT_FILENAME     /home/stat$fastcgi_script_name;

里面的路径要设置正确，否则会出现“No input file”。

测试配置文件是否正确：

/usr/local/nginx/sbin/nginx -t

重载配置文件：

kill -HUP `cat /usr/local/nginx/logs/nginx.pid`

无缝分割生成日志：

mv /usr/local/nginx/logs/access.log /usr/local/nginx/logs/access.log.date

kill -USR2 `cat /usr/local/nginx/logs/nginx.pid`

4. sucop.pw

在 /usr/local/nginx/conf 下放置 sucop.pw 密码文件，内容如下：

test:N7NAb31FTcBRI

5. php.ini

设置/usr/local/php-fcgi/etc/php.ini配置文件：

cgi.fix_pathinfo=1

expose_php = Off

6. /etc/mysql/my.cnf

注释掉：#log             = /var/log/mysql/mysql.log

做/var/lib/mysql的连接到/server/mysql：

/etc/init.d/mysql stop

mv /var/lib/mysql/* /home/mysql/

rm -fr /var/lib/mysql

chown -R mysql.mysql /home/mysql

ln -s /home/mysql /var/lib/mysql

--[ 3. 程序启动

在 /etc/rc.local 中加入：

ulimit -SHn 51200

/usr/local/php-fcgi/sbin/php-fpm start

/usr/local/nginx/sbin/nginx

/usr/local/memcached/bin/memcached -d -l 127.0.0.1 -u www-data -m 256

--[ 4. 说明

/usr/local/memcached/bin/memcached -d -l 127.0.0.1 -u www-data -m 256

由于机器没有负载，暂时不用memcached。
