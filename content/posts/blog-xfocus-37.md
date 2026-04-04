---
title: "Debian下的网络打印"
date: 2004-04-03T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-37"
---

有篇mini HOWTO不错，可以参考： 
http://gnu.kookel.org/ftp/LDP/HOWTO/Debian-and-Windows-Shared-Printing/index.html

1. 安装软件 
apt-get install cupsys cupsys-bsd cupsys-client foomatic-bin samba smbclient gs-esp a2ps

2. 确认打印机 
smbclient -L 192.168.100.4 -U guest

3. 安装网络打印机 
/usr/sbin/lpadmin -p RicePrinter -v smb://fred:mypass@rice/INKJET -P 
/root/inkjet.ppd 
/usr/bin/enable RicePrinter 
/usr/sbin/accept RicePrinter 
/usr/sbin/lpadmin -d RicePrinter 
我懒得那么麻烦，直接用CUPS的web配置界面了,访问http://localhost:631/ ;) 

里面我的一些配置的选项是： 
Device:Windows Printer via SAMBA 
Device URI:smb://guest@192.168.100.4/HPLaserJ 
把Output Resolution改成600 DPI了，打印测试页正常。

4. 各种程序下的中文打印 
有些程序直接打印就很正常，比如OO，有部份程序，比如gedit之类的可以设置打印字体，但对sylpheed之类的软件，直接发送命令给lpr的，打印总是乱码，这时采用bg5ps这个软件来辅助。 
apt-get install bg5ps

调整~/.bg5ps.conf，修改设定至少以下项目： 
Encoding="gb2312" 
chineseFontPath="/home/aa/.zh_CN" 
fontName_gb2312="simsun.ttc"

运行命令测试： 
bg5ps -if 20040324_DongGuan.txt |lpr 
打印中文正常。这样就可以在如sylpheed等软件中用类似bg5ps -if %s|lpr的命令输出中文了。

5. Mozilla的中文打印 
直接在/usr/lib/mozilla-firefox/defaults/pref/unix.js打开FreeType2再指定路径就行了，如下： 
pref("font.FreeType2.enable", true); 
pref("font.directory.truetype.1","/home/aa/.zh_CN"); 
但我这样后浏览有些网站英文字体发虚(如xfocus)，有些网站是好的(如linuxsir)，就又关了。

6. 多页打印在同一张纸上(类似fineprint) 
apt-get install mpage 
mpage -4 mozilla.ps > out.ps|lpr
