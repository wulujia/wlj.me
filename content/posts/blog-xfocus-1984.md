---
title: "时间管理程序tracks安装"
date: 2006-08-06T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1984"
---

在[DBA notes](http://www.dbanotes.net/)看到他装了个GTD（Getting Things Done）工具[tracks](http://www.rousette.org.uk/projects/)，这种时间管理、日程管理的工具我试用过不少，比如webcalendar、todolist、google calendar等。

本来是想用google全系列产品包括calendar的，也认真试了段时间，可却有不少不满，比如它只能导出，不能导入日志，比如不能看到我实际上未完成的工作，应该说，日程管理工具中，google calendar和webcalendar相当不错了，就是这个无法填写工作完成与否，让我不太喜欢。todolist倒是基本满足需求，可惜它是一个PC端的应用程序，我现在不太愿意用笔记本电脑，为了保持家里与公司电脑的一致，自然是能用web应用的，就尽量使用web应用，嗯，因此看到tracks，我又起了试一试的念头。

本以为在debian上安装很简单，谁知道竟然花了我整整半天时间，记录一下，以后万一要重装，好歹能想起来（用mysql用烦了，这回采用轻量级的sqlite3，备份起来也方便些）：

1、安装ruby
apt-get install ruby1.8 ruby1.8-dev
如果要用apache启动，还需要装上irb1.8

2、安装rubygems
在http://www.rubyonrails.com/down下载rubygems
tar zvfx rubygems-0.8.1.tgz
ruby install.rb

3、安装rails
gem install rails -include-dependencies

4、安装sqlite3、sqlite3-dev和sqlite3-ruby
apt-get install sqlite3 libsqlite3-dev
gem install sqlite3-ruby

5、按文档中配置好config、log、db等目录及配置文件、数据库文件
6、运行rake migrate，如果没有错误提示，运行/usr/bin/ruby script/server应该就能跑起来了。（如果用Apache，跳到第9步）
7、用系统自建的WEBrick，在/var/init.d/目录下新增tracks文件，并链接到/etc/rc2.d/，tracks文件内容如下：

#! /bin/sh
set -e

export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"

case "$1" in
start)
echo -n "Starting Tracks"
start-stop-daemon --start --chuid wlj --exec /usr/bin/ruby -- /home/wlj/htdocs/gtd/script/server -d -e production
echo "."
;;
stop)
echo -n "Stopping tracks"
start-stop-daemon --stop --quiet --oknodo --retry 30 --exec /usr/bin/ruby
echo "."
;;

restart)
echo -n "Restarting tracks"
start-stop-daemon --stop --quiet --oknodo --retry 30 --exec /usr/bin/ruby
start-stop-daemon --start --chuid wlj --exec /usr/bin/ruby -- /home/wlj/htdocs/gtd/script/server -d -e production
echo "."
;;

*)
echo "Usage: /etc/init.d/tracks {start|stop|restart}"
exit 1
esac

exit 0

8、访问http://server:3000/signup，创建一个新用户，并用该用户登陆，就可以享用这个不错的时间管理工具了 :)
9、我用apache2，因此用a2enmod rewrite启用mod_rewrite，注意目录权限必须是apache可写，并创建一个vhost，其中包含：

Options ExecCGI FollowSymLinks
AddHandler cgi-script .cgi
AddHandler fastcgi-script .fcgi
AllowOverride all
Allow from all
Order allow,deny

10、最后，如果你懒得自己建，又想用的话，可以到[zenlist](http://www.zenlist.com/)申请一个帐号。
11、tracks对ie类浏览器的支持不如对firefox好，用ie看时感觉不太舒服。

附录：[什么是GTD](http://www.lifebang.com/archives/49) 

GTD，Getting Things Done的缩写。《 Getting Things Done-The Art of Stress-Free Productivity》一书的作者David Allen将GTD总结成为一种将繁重超负荷的工作生活方式变成无压力高效的时间管理系统。这种GTD系统的内容包括：

* 搜集记录所有你在操心的事情。
* 定义出可以付诸实施的行动及其结果和具体的实施步骤。
* 根据你需要获取的方式和时间，按照合适的分类，以流水线的方式组织整理备忘录和相关信息。
* 对你的承诺从目的、远景、目标、关注的范围、项目和行动几个方面保持及时和合理的回顾评估。

这些并不是空洞的说教。把你正在处理的每一件事以你信任的方式记录下来而不是放在脑子里，首先就可以减轻焦虑。找到马上可以实施的行动，制定完成的标准，以线性而不是并发方式一件一件处理，本身就是一种高效的方式，并能通过目标的完成感受到成就感。及时对这个系统中的信息回顾可以保证必须完成的事情不被遗忘，不必要的工作及时放弃，同时让你对这个系统本身更信任，更容易通过这个系统来记录每件工作来减轻焦虑和提高效率，以此进入一个良性循环。在无压力或者压力尽量少的状态下完成工作，GTD所倡导的并非一个不切实际的时间管理理论。
