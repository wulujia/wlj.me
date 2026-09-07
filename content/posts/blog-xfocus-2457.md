---
title: "Ubuntu系统的自动安全更新"
date: 2007-02-04T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2457"
---

安装了Ubuntu 6.10
Server，考虑到平时根本不会有时间去管理服务器，只能用懒汉的方法来折腾了，就是做个cron让它自己定时更新，特地看了一下，apt有个-y的参
数，可以跳过每次更新时的交互式确认，于是进/etc/cron.daily/打算扔个脚本，一看里面居然已经有个apt脚本，仔细看看，功能挺强，它的
注释如下：

> # This file understands the following apt configuration
> variables:
> 
> #
> 
> #  "APT::Periodic::Update-Package-Lists=1"
> 
> #  - Do "apt-get update" automatically every n-days
> (0=disable)
> 
> #
> 
> #  "APT::Periodic::Download-Upgradeable-Packages=0",
> 
> #  - Do "apt-get upgrade --download-only" every n-days
> (0=disable)
> 
> #
> 
> #  "APT::Periodic::AutocleanInterval"
> 
> #  - Do "apt-get autoclean" every n-days (0=disable)
> 
> #
> 
> #  "APT::Periodic::Unattended-Upgrade"
> 
> #  - Run the "unattended-upgrade" security upgrade
> script
> 
> #    every n-days (0=disabled)
> 
> #    Requires the package "unattended-upgrades" and
> will write
> 
> #    a log in /var/log/unattended-upgrades
> 
> #
> 
> #  "APT::Archives::MaxAge",
> 
> #  - Set maximum allowed age of a cache package file. If a
> cache
> 
> #    package file is older it is deleted
> (0=disable)
> 
> #
> 
> #  "APT::Archives::MaxSize",
> 
> #  - Set maximum size of the cache in MB (0=disable). If the
> cache
> 
> #    is bigger, cached package files are deleted
> until the size
> 
> #    requirement is met (the biggest packages will
> be deleted
> 
> #    first).
> 
> #
> 
> #  "APT::Archives::MinAge"
> 
> #  - Set minimum age of a package file. If a file is younger
> it
> 
> #    will not be deleted (0=disable). Usefull to
> prevent races
> 
> #    and to keep backups of the packages for
> emergency.

因此，考虑简单起见，俺就直接apt-get install
unattended-upgrades，然后在/etc/apt/apt.conf.d/里加了个文件99custom，内容只有一行：

> APT::Periodic::Unattended-Upgrade
> "1";

这表示每天检查一次安全更新。
