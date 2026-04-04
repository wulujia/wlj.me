---
title: "Chrooting 后台服务和系统程序指导"
date: 2001-11-11T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-301"
---

文章提交：[inburst](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=2721) (inburst_at_263.net)

Chrooting 后台服务和系统程序指导

作者：Jonathan A. Zdziarski  <jonathan@networkdweebs.com>

翻译和修改：张务鸣 (wuming) <wuming@wuming.net>

目录

第一部分：Chrooting 简介

* 1.1 什么是 chrooting？

* 1.2 什么时候应该使用 chroot？

* 1.3 所有后台程序都能使用 chroot 吗？

* 1.4 chrooting 会给用户带来什么后果？

* 1.5 chrooting 需要些什么？

第二部分：系统资料收集

* 2.1 我们是否能 chroot 这个进程？

* 2.2 trss, lsof 和 ldd 简介

* 2.3 查找所依赖的数据文件

* 2.4 策略性的建立数据文件

* 2.5 查找所使用的Library(库)文件

* 2.6 寻找一个好的监狱地方(jail home)

第三部分：建立chrooted 环境

* 3.1 建立新的监狱 

* 3.2 拷贝程序文件，数据文件和设置cron

* 3.3 拷贝库数据文件

* 3.4 建立 devices (安装设备驱动程序)

* 3.5 交替启动脚本

* 3.6 成品

第四部分：词汇解释

第一部分

1.1什么是 chrooting？

指令chroot 是 ”change root” 的缩写，为了是交换本身根(root)系统环境所设计。就是相对来说 / (根目录)由此改变。比如：一个文件的路径实际上是 /home/wuming/hello.txt 在现有的系统中。我现在chroot /home/wuming目录后，那么这个文件在我chrooted 过的环境下的路径是 /hello.txt

Chroot 本身目的是为了建立一个难以渗透的(理论上)的”监狱式”的保护层。不允许chroot过的环境下访问任何以外文件数据。比如在chroot过的/home/wuming目录下，我将无法访问任何 /home/wuming 以外的文件。普通情况下是限制一个多用户系统中用户访问系统文件。Chroot也可以用来限制各种不同类型的后台程序，从而避免骇客入侵的机会。或者让入侵者获得根(root)权限更加困难。比如系统使用一个有漏洞的远程服务，如果被黑客入侵而得到shell，但是这个shell并不包含在本身系统中，从而阻止了黑客访问其他系统文件。虽然很多人声称能够突破chroot过的jail，但是多数时候是从一个shell中突破的。在我们所讨论的例子中不存在这样的问题，所以攻破daemon 环境是非常困难的。

1.2什么时候应该使用 chroot？

Chroot 化 daemons 是十分实践的使用方法在系统中添加不同层次，从而保护你现有系统。很多系统进程和第三方软件已经有对于漏洞的安全措施。也有很多进程使用非根用户(non-root user)，同样也使用户入侵root更加困难。

网络安全层中有比如说防火墙，TCP wrappers，过滤层和其他附加程序等。与他们一样chrooting 可以在多数环境中适当使用，同时不对本身功能作出太多危及。

* 1.3 所有后台程序都能使用 chroot 吗？

从技术上说完全可以chroot 所有东西，甚至你女朋友的收音机。但是在其他情况下chrooting是否是最好解决方式，那就没准了。某些 daemon 后会带来很多问题，这些都是应当考虑的问题。比如说 sendmail 在 chroot 的环境下，无法阅读用户目录下的 .forward 文件，就是一个很好的例子。所以要想chroot sendmail，首先应该精心策划所有细节问题。当然在我提到的这个例子实际上最好使用smrsh (sendmail restricted shell)，而不需要chroot。无论如何，只要稍微努力一下我们就能安全的 chroot 很多系统 daemons.

* 1.4 chrooting 会给用户带来什么后果？

如果一切设置正确，你的用户不应该感觉到任何系统变动。本身系统并没有变动，而是在现有系统上建立一个监狱式的环境。在这里我们并不是讨论什么安全的建立ftp或者ssh daemons。对于他们也有类似的方法，但是要复杂的多。这里将主要介绍如何给普通的服务带来更大的安全系数。

* 1.5 chrooting 需要些什么？

Chroot各种 daemon 有一个步骤，基本如下：

#建立”监狱式”目录

#拷贝本身服务软件和其他要求的文件

#拷贝所需要系统库文件

#变换启动脚本，使系统启动正确环境

第二步和第三步基本是同一时间。但是第二步骤中，更需要一些有周全的考虑，比如一个邮件服务，必须能访问所有mail目录，但是同时把所有邮件目录拷贝到jail目录下也不是个周全的办法。将在后面具体介绍如何解决以上问题。

第二部分

* 2.1 我们是否能 chroot 这个进程？

在建立目录或者生成文件前，让我们先考虑一下是否能建立chroot 环境。我将介绍三个系统进程的例子，有三个问题我们应当考虑。

#这个 daemon 否访的数据是否在一个普通目录下？

#是否可以拷贝文件其他地方或者周期性的使用cron替代？

#是否能够谨慎在这些指定文件目录中生成一个监狱式环境？

如果你对以上问题回答是都是不可能的话，那么可能chroot不是一个好的解决方法。让我们看以下例子：

Eudora Qpopper

#这个 daemon 否访的数据是否在一个普通目录下？

首先对于一邮件服务系统应当能访问用户邮件目录，同时/etc中的一些文件，比如passwd文件确认用户。所以这个问题答案是可以。因为主要文件通常在 /var/mail 下面。

#是否可以拷贝文件其他地方或者周期性的使用cron替代？

拷贝邮件箱不是什么好的想法，这样很容易给用户造成邮箱不稳定的感觉。

#是否能够谨慎在这些指定文件目录中生成一个监狱式环境？

当然可以，在这里我们有两种选择，一种是移动这些牵连文件到监狱环境中，一种是重新生成。对于原有连接可以使用symbolic links，Linux下常见的一种文件目录解决方式。

Sun的RPCBIND

#这个 daemon 否访的数据是否在一个普通目录下？

主要访问/etc下的一些小文件

#是否可以拷贝文件其他地方或者周期性的使用cron替代？

大部分文件很小而且很少更新，用cron一天拷贝一次足够。

#是否能够谨慎在这些指定文件目录中生成一个监狱式环境？

在/etc下进行chroot不是一个好的想法，对于很多黑客高手etc里面的文件足够提有用的信息。应该生成一个单独的监狱环境，将文件拷贝到这个环境就可以了。

Sendmail

#这个 daemon 否访的数据是否在一个普通目录下？

不是，Sendmail访问数个不同的目录和文件。比如/var/spool/mqueue和/var/mail还有/etc/mail下的一些文件，除此以外还有用户目录下的一些文件。

#是否可以拷贝文件其他地方或者周期性的使用cron替代？

理论上是可以的，但是似乎带来的工作量大于我们所想象的。其中比如用户目录下的.forward文件或者其他文件。似乎在实际中做到不太现实。

#是否能够谨慎在这些指定文件目录中生成一个监狱式环境？

首先，我们应该在mail目录那里进行jail限制，那么我们失去在spool的写权限，那么我们应该jail整个/var，这样导致其他问题。所以无论如何是否建立mirror目录都不太理想。所以我不推荐对sendmail使用chroot。

虽然我确定sendmail是可以被chroot的，我见过chroot过的Qmail，但是那些是专业做LINUX安全系统的公司为自己软件，要求考虑周详。初学者不推荐做这样的试验。

* 2.2 对 trss, lsof 和 ldd 简介

truss

如果你 man truss，你能看到truss是一个跟踪系统calls和signals的工具。系统calls包括库文件和反问数据文件。Truss一个很好工具测量哪些文件被使用。使用truss，很简单，敲如truss按照提示使用它。

lsof 

lsof 是另外一个工具看到那些文件被daemon使用。通过lsof你能看到哪些daemons正在运行。还会提示哪些端口等等很多信息。可以从[www.sunfreeware.com](http://www.sunfreeware.com/)下载，或者通过FTP到[ftp://vic.cc.purdue.edu/pub/tools/unix/lsof](https://web.archive.org/web/20160427103128/ftp://vic.cc.purdue.edu/pub/tools/unix/lsof) 获取。

ldd

ldd 是一个工具帮助你找出哪些库文件被程序使用。ldd的是list dynamic dependencies的缩写。使用ldd能够给你一个list哪些库文件应当拷贝到监狱环境中。

* 2.3 查找所依赖的数据文件

在2.1中已经介绍过我们应当首先找出所有daemon使用的文件。有些是直接可以找到的，有些必须新建立一个监狱环境。以上的三个例子中两个是完全可行的。(Eudora Qpopper和SUN RPCBIND)并且在前段时间在安全上漏洞一直很多。在这里简介如何为它们做到chroot。

Eudora Qpopper

/var/mail/* (监狱内部)

以下在/etc下文件应当周期性的拷贝

hosts.allow

hosts.deny

netconfig

nsswitch.conf

passwd

resolv.conf

services

shadow

Sun RPCBIND

以下在/etc下文件应当周期性的拷贝

hosts

netconfig

nsswitch.conf

resolv.conf

services

时间区文件 /usr/local/zoneinfo 或者 /usr/share/zoneinfo

和一个 tmp 目录。

* 2.4 策略性的建立数据文件

当你有一个列表哪些文件是被daemon运行时用到的时候，那么我们开始考虑建立一个什么样的监狱？是否使用周期性系统拷贝，还是在本身数据文件目录上建立监狱管制？当然绝对不应该在本身系统，比如/etc外面做监狱管制，那么等于没有建立任何管制。如果你在纸上圈圈画画，看哪些文件是属于系统，哪些应当包含在监狱管制内的，这样你将有一个很好的框架文件系统之间关系图案。设计好的监狱框架是我们做好安全系统的第一步。

* 2.5 查找所使用的Library(库)文件

所有软件往往不仅仅使用一个执行文件，常使用到各种不同库文件，没有这些文件，进程很可能不工作。查找这些文件最好使用ldd软件。在建立一个新的文件系统（监狱环境）时候，我们可以拷贝这些库文件到新的/lib目录中。

还是以上的两个例子，通过ldd查找出所使用的库文件。

Eudora Qpopper

/usr/lib/libnsl.so.1

/usr/lib/libsocket.so.1

/usr/lib/libresolv.so.2

/usr/lib/libmail.so.1

/usr/lib/librt.so.1

/usr/lib/libcrypt_i.so.1

/usr/lib/libc.so.1

/usr/lib/libdl.so.1

/usr/lib/libmp.so.2

/usr/lib/libaio.so.1

/usr/lib/libgen.so.1

/usr/lib/libpthread.so.1

/usr/lib/libthread.so.1

Sun RPCBIND

/usr/lib/libsocket.so.1

/usr/lib/libnsl.so.1

/usr/lib/libdl.so.1

/usr/lib/libc.so.1

/usr/lib/libmp.so.2

* 2.6 寻找一个好的监狱地方(jail home)

现在我们掌握了所有必要的数据，在哪里建立监狱比较合适呢？如果你想在原由的文件系统上建立监狱环境，拿Eudora Qpopper来说，我们将在原有的/var/mail打主意，以下将具体介绍如何做。注意，原由系统访问原有文件并没有变动，所以你如果目录或者数据文件有变动，应当在原有系统中建立symlink连接。第三节具体介绍！

第三部分：

* 3.1 建立新的监狱

第一步建立目录，如同造房子时候打地基一样。我们先拿Sun RPCBIND做例子，如果我们选择/var/rpcbind作为监狱环境的话，以下目录是必要的。

mkdir /var/rpcbind

mkdir /var/rpcbind/dev

mkdir /var/rpcbind/etc

mkdir /var/rpcbind/tmp

mkdir -p /var/rpcbind/usr/lib

因为这个daemon将被chroot，所以/dev devices 目录一定是必须的，还有/etc，暂时文件目录/tmp和库文件/lib目录。这仅仅是一个开始。

同时我们也提一下Eudora Qpopper，以上我们说过了我们将围绕着已经存在的文件系统上建立监狱环境，不同于Sun RPCBIND完全新建的环境。这里将围绕着/var/mail类建立我们所需要的目录。

mkdir /var/mail/dev

mkdir /var/mail/etc

mkdir -p /var/mail/usr/lib 

mkdir -p /var/mail/usr/local/lib

mkdir -p /var/mail/usr/sbin

mkdir -p /var/mail/usr/share/lib/zoneinfo/US

但是我们并没有结束，要知道，在chroot后的/var/mail就是/了，那么所有本来在/var/mail下邮件文件怎么办？所以我们很简单的使用象征性连接把它指向正确的目录去。

mkdir /var/mail/var

ln -s / /var/mail/var/mail 

这样一来当popper找/var/mail里面邮件文件的时候就能访问到本来的/var/mail目录了。

建立好的目录应该看上去这样：

Sun RPCBIND

drwxr-xr-x   7 root     other        512 Aug  1 18:31 ./

drwxr-xr-x  34 root     sys          512 Aug  1 18:07 ../

drwxr-xr-x   2 root     other        512 Aug  1 18:16 dev/

drwxr-xr-x   2 root     other        512 Aug  1 18:10 etc/

drwxr-xr-x   2 root     other        512 Aug  1 18:31 tmp/

drwxr-xr-x   6 root     other        512 Jul 28 15:55 usr/

drwxr-xr-x   3 root     other        512 Aug  1 18:19 var/

Eudora Qpopper

drwxrwxrwt   7 root     mail         512 Oct 18 19:36 ./

drwxr-xr-x  34 root     sys          512 Aug  1 18:07 ../

drwxr-xr-x   2 root     other        512 Jul 29 13:33 dev/

drwxr-xr-x   2 root     other        512 Jul 28 16:18 etc/

            - 有些邮箱文件应当参杂在这里 -

drwxr-xr-x   6 root     other        512 Jul 28 15:55 usr/

drwxr-xr-x   2 root     other        512 Aug  1 18:06 var/

 

* 3.2 拷贝程序文件，数据文件和设置cron

我们的目录结构已经做好，那么现在应当拷贝需要的文件。因为以后我们将让这些daemon通过init脚本启动，所以也应当瞧一下inetd等脚本里面调动哪些相关文件，有些可能是连接/usr/sbin/目录下某个相同文件，所以我们也应当建立同样目录。当你拷贝好所相关文件时候，你应该得到与我有类似的文件。

Sun RPCBIND

% ls -l /var/rpcbind/etc

-r--r--r--   1 root     other         90 Jul 28 16:18 hosts

-rw-r--r--   1 root     other       1239 Jul 28 16:09 netconfig

-rw-r--r--   1 root     other        835 Jul 28 15:32 nsswitch.conf

-rw-r--r--   1 root     other        140 Jul 28 16:14 resolv.conf

-r--r--r--   1 root     other       3649 Jul 28 16:14 services

Eudora Qpopper

% ls -l /var/mail/etc

-r--r--r--   1 root     other         90 Jul 28 16:18 hosts

-rw-------   1 root     other         73 Oct 18 19:15 hosts.allow

-rw-------   1 root     other          9 Jul 28 15:58 hosts.deny

-rw-r--r--   1 root     other       1239 Jul 28 16:09 netconfig

-rw-r--r--   1 root     other        835 Jul 28 15:32 nsswitch.conf

-r--r--r--   1 root     other        815 Oct 18 19:15 passwd

-rw-r--r--   1 root     other        140 Jul 28 16:14 resolv.conf

-r--r--r--   1 root     other       3649 Jul 28 16:14 services

-r--------   1 root     other        502 Oct 18 19:15 shadow

这里有些写好的cron，如果你系统常有变化，那么可以使用，无论如何有利无害。

0,30 * * * * cp -p /etc/passwd /var/mail/etc/passwd

0,30 * * * * cp -p /etc/shadow /var/mail/etc/shadow

0 0 * * * cp -p /etc/hosts.* /var/mail/etc/

0 0 0 * * cp -p /etc/services /var/rpcbind/etc

0 0 0 * * cp -p /etc/resolv.conf /var/mail/etc

* 3.3 拷贝库数据文件

有些系统的库文件分布在不同的地方，比如/usr/lib和/usr/local/lib等，我们应当按照不同目录拷贝，并且给予可执行权限。看上去应该差不多类似以下：

% ls -l /var/rpcbind/usr/lib

-rwxr-xr-x   1 root     other     200292 Jul 28 15:27 ld.so.1*

-rwxr-xr-x   1 root     other      41628 Jul 28 15:28 libaio.so.1*

-rwxr-xr-x   1 root     other     938940 Jul 28 15:28 libc.so.1*

-rwxr-xr-x   1 root     other      15616 Jul 28 15:27 libcrypt_i.so.1*

-rwxr-xr-x   1 root     other       4448 Jul 28 15:28 libdl.so.1*

-rwxr-xr-x   1 root     other      40540 Jul 28 15:28 libgen.so.1*

-rwxr-xr-x   1 root     other      29548 Jul 28 15:27 libmail.so.1*

-rwxr-xr-x   1 root     other      19584 Jul 28 15:28 libmp.so.2*

-rwxr-xr-x   1 root     other     730672 Jul 28 15:27 libnsl.so.1*

-rwxr-xr-x   1 root     other      35308 Jul 28 15:57 libpthread.so.1*

-rwxr-xr-x   1 root     other     326336 Jul 28 15:27 libresolv.so.2*

-rwxr-xr-x   1 root     other      39048 Jul 28 15:27 librt.so.1*

-rwxr-xr-x   1 root     other      65876 Jul 28 15:27 libsocket.so.1*

-rwxr-xr-x   1 root     other     166624 Jul 28 15:58 libthread.so.1*

-rwxr-xr-x   1 root     other      19648 Jul 28 16:17 nss_dns.so.1*

-rwxr-xr-x   1 root     other      38832 Jul 28 15:33 nss_files.so.1*

-rwxr-xr-x   1 root     other      38292 Jul 28 15:33 nss_nis.so.1*

-rwxr-xr-x   1 root     other      12284 Aug  1 18:15 straddr.so*

% ls -l /var/mail/usr/lib /var/mail/usr/local/lib

-rwxr-xr-x   1 root     other     200292 Jul 28 15:27 ld.so.1*

-rwxr-xr-x   1 root     other      41628 Jul 28 15:28 libaio.so.1*

-rwxr-xr-x   1 root     other     938940 Jul 28 15:28 libc.so.1*

-rwxr-xr-x   1 root     other      15616 Jul 28 15:27 libcrypt_i.so.1*

-rwxr-xr-x   1 root     other       4448 Jul 28 15:28 libdl.so.1*

-rwxr-xr-x   1 root     other      40540 Jul 28 15:28 libgen.so.1*

-rwxr-xr-x   1 root     other      29548 Jul 28 15:27 libmail.so.1*

-rwxr-xr-x   1 root     other      19584 Jul 28 15:28 libmp.so.2*

-rwxr-xr-x   1 root     other     730672 Jul 28 15:27 libnsl.so.1*

-rwxr-xr-x   1 root     other      35308 Jul 28 15:57 libpthread.so.1*

-rwxr-xr-x   1 root     other     326336 Jul 28 15:27 libresolv.so.2*

-rwxr-xr-x   1 root     other      39048 Jul 28 15:27 librt.so.1*

-rwxr-xr-x   1 root     other      65876 Jul 28 15:27 libsocket.so.1*

-rwxr-xr-x   1 root     other     166624 Jul 28 15:58 libthread.so.1*

-rwxr-xr-x   1 root     other      19648 Jul 28 16:17 nss_dns.so.1*

-rwxr-xr-x   1 root     other      38832 Jul 28 15:33 nss_files.so.1*

-rwxr-xr-x   1 root     other      38292 Jul 28 15:33 nss_nis.so.1*

* 3.4 建立 devices (安装设备驱动程序)

这一章有些技巧。因为被chroot后的daemon不能在访问原有的/dev目录，里面包括一些很重要的devices，比如/dev/null，/dev/log等等类似，一般可以使用truss查找出来他它们，也可以使用strings |grep dev 找出来一部分，但是多数时候你得等待错误日志中的提示。一下是必用的一些devices。

/dev/conslog

/dev/log

/dev/msglog

/dev/null

/dev/tcp

/dev/ticlts

/dev/ticots

/dev/ticotsord

/dev/udp

/dev/zero

如何生成这些devices？我们一步一步的生成。

1. 我们 ’ls -1L /dev/[devicename]’，一般你将得到：

crw-rw-rw- 1 root sys 13, 2 Oct 18 19:56 /dev/null

这里的13是’major’ 值，2是’minor’值，第一字母c是表示这个device是character 或者block device。根据这些值，我们可以建立节点(node)。

2. cd 到我们建立的监狱环境下，例如/var/mail/dev或者/var/rpcbind/dev。使用’mknod’来建立device，比如：mknod null c 13 2 这里我们建立一个新的 null。很多不同的系统有不同的 ’minor’ 值，所以不能一味的copy & paste。

3. 使用chmod和chown，让这些devices有正确的读写权限。拿Sun RCPBIND举例，后来我有发现需要建立一个rpc_door的目录，所以我必须建立其目录。

mkdir -p /var/rpcbind/var/run/rpc_door

chmod +t /var/rpcbind/var/run/rpc_door

等等

* 3.5 交替启动脚本

应该基本完工了吧！如果你没忘记什么，不过当你第一次启动的时候就知道了。（一般总有一两个错误。嘿嘿！）如果还有什么库文件找不到的话，使用truss和ldd找出来拷贝到正确的目录下。跑chroot的daemon很简单。

/usr/sbin/chroot /var/rpcbind /usr/sbin/rpcbind

你可以祈求点什么希望一切正常工作，当错误日志不再重复时，就是覆盖原来的自动启动的脚本的时候了。

在inetd下如何chroot

Eudroa Qpopper是通过inetd启动的而不是init.d启动。所以在这里我们将修改一指令行。

pop3 stream tcp nowait root /usr/sbin/chroot chroot /var/mail /usr/sbin/in.pop3 

如果你使用的是TCP wrappers，那么你需要骗过inetd，让你的inetd认为你的服务名字还是叫in.pop3(或者应该叫什么)。在这里使用symbink连接替代你原有的in.pop3文件。比如：

lrwxrwxrwx 1 root other 6 Jul 28 15:42 /usr/sbin/in.pop3 -> chroot* 

pop3 stream tcp nowait root /usr/sbin/tcpd in.pop3 /var/mail /usr/sbin/in.pop3 

这里/usr/sbin/in.pop3实际上是/usr/sbin/chroot。inetd启动的是in.pop3，实际上指令是chroot ’/var/mail /usr/sbin/in.pop3’，大致如此，应该没什么问题了吧！

* 3.6 成品

成品的文件列表如下：

Sun RPCBIND

d none /var/rpcbind 0755 root other

d none /var/rpcbind/dev 0755 root other

c none /var/rpcbind/dev/conslog 21 0 0666 root other

c none /var/rpcbind/dev/log 21 5 0640 root other

c none /var/rpcbind/dev/msglog 97 1 0600 root other

c none /var/rpcbind/dev/null 13 2 0666 root other

c none /var/rpcbind/dev/udp 41 0 0666 root other

c none /var/rpcbind/dev/tcp 42 0 0666 root other

c none /var/rpcbind/dev/ticlts 105 2 0666 root other

c none /var/rpcbind/dev/ticotsord 105 1 0666 root other

c none /var/rpcbind/dev/ticots 105 0 0666 root other

d none /var/rpcbind/var 0755 root other

d none /var/rpcbind/var/run 0755 root other

d none /var/rpcbind/var/run/rpc_door 1777 root root

d none /var/rpcbind/tmp 0755 root other

d none /var/rpcbind/usr 0755 root other

d none /var/rpcbind/usr/share 0755 root other

d none /var/rpcbind/usr/share/lib 0755 root other

d none /var/rpcbind/usr/share/lib/zoneinfo 0755 root other

d none /var/rpcbind/usr/share/lib/zoneinfo/US 0755 root other

f none /var/rpcbind/usr/share/lib/zoneinfo/US/Eastern 0644 root bin

d none /var/rpcbind/usr/lib 0755 root other

f none /var/rpcbind/usr/lib/ld.so.1 0755 root other

f none /var/rpcbind/usr/lib/libnsl.so.1 0755 root other

f none /var/rpcbind/usr/lib/libsocket.so.1 0755 root other

f none /var/rpcbind/usr/lib/libresolv.so.2 0755 root other

f none /var/rpcbind/usr/lib/libmail.so.1 0755 root other

f none /var/rpcbind/usr/lib/librt.so.1 0755 root other

f none /var/rpcbind/usr/lib/libcrypt_i.so.1 0755 root other

f none /var/rpcbind/usr/lib/libc.so.1 0755 root other

f none /var/rpcbind/usr/lib/libdl.so.1 0755 root other

f none /var/rpcbind/usr/lib/libmp.so.2 0755 root other

f none /var/rpcbind/usr/lib/libaio.so.1 0755 root other

f none /var/rpcbind/usr/lib/libgen.so.1 0755 root other

f none /var/rpcbind/usr/lib/nss_files.so.1 0755 root other

f none /var/rpcbind/usr/lib/nss_nis.so.1 0755 root other

f none /var/rpcbind/usr/lib/libpthread.so.1 0755 root other

f none /var/rpcbind/usr/lib/libthread.so.1 0755 root other

f none /var/rpcbind/usr/lib/nss_dns.so.1 0755 root other

f none /var/rpcbind/usr/lib/straddr.so 0755 root other

d none /var/rpcbind/usr/sbin 0755 root other

f none /var/rpcbind/usr/sbin/rpcbind 0555 root other

d none /var/rpcbind/usr/local 0755 root other

d none /var/rpcbind/usr/local/sbin 0755 root other

d none /var/rpcbind/usr/local/lib 0755 root other

d none /var/rpcbind/etc 0755 root other

f none /var/rpcbind/etc/nsswitch.conf 0644 root other

f none /var/rpcbind/etc/netconfig 0644 root other

f none /var/rpcbind/etc/services 0444 root other

f none /var/rpcbind/etc/resolv.conf 0644 root other

f none /var/rpcbind/etc/hosts 0444 root other

Eudora Qpopper

d none /var/mail 1777 root mail

d none /var/mail/usr 0755 root other

d none /var/mail/usr/share 0755 root other

d none /var/mail/usr/share/lib 0755 root other

d none /var/mail/usr/share/lib/zoneinfo 0755 root other

d none /var/mail/usr/share/lib/zoneinfo/US 0755 root other

f none /var/mail/usr/share/lib/zoneinfo/US/Eastern 0644 root bin

d none /var/mail/usr/lib 0755 root other

f none /var/mail/usr/lib/ld.so.1 0755 root other

f none /var/mail/usr/lib/libnsl.so.1 0755 root other

f none /var/mail/usr/lib/libsocket.so.1 0755 root other

f none /var/mail/usr/lib/libresolv.so.2 0755 root other

f none /var/mail/usr/lib/libmail.so.1 0755 root other

f none /var/mail/usr/lib/librt.so.1 0755 root other

f none /var/mail/usr/lib/libcrypt_i.so.1 0755 root other

f none /var/mail/usr/lib/libc.so.1 0755 root other

f none /var/mail/usr/lib/libdl.so.1 0755 root other

f none /var/mail/usr/lib/libmp.so.2 0755 root other

f none /var/mail/usr/lib/libaio.so.1 0755 root other

f none /var/mail/usr/lib/libgen.so.1 0755 root other

f none /var/mail/usr/lib/nss_files.so.1 0755 root other

f none /var/mail/usr/lib/nss_nis.so.1 0755 root other

f none /var/mail/usr/lib/libpthread.so.1 0755 root other

f none /var/mail/usr/lib/libthread.so.1 0755 root other

f none /var/mail/usr/lib/nss_dns.so.1 0755 root other

d none /var/mail/usr/sbin 0755 root other

f none /var/mail/usr/sbin/in.pop3 0755 root other

d none /var/mail/usr/local/lib 0755 root other

d none /var/mail/etc 0755 root other

f none /var/mail/etc/passwd 0444 root other

f none /var/mail/etc/shadow 0400 root other

f none /var/mail/etc/hosts.allow 0600 root other

f none /var/mail/etc/nsswitch.conf 0644 root other

f none /var/mail/etc/hosts.deny 0600 root other

f none /var/mail/etc/netconfig 0644 root other

f none /var/mail/etc/services 0444 root other

f none /var/mail/etc/resolv.conf 0644 root other

f none /var/mail/etc/hosts 0444 root other

d none /var/mail/var 0755 root other

s none /var/mail/var/mail=/

d none /var/mail/dev 0755 root other

c none /var/mail/dev/udp 41 0 0666 root other

c none /var/mail/dev/null 13 2 0666 root other

c none /var/mail/dev/conslog 21 0 0666 root other

c none /var/mail/dev/log 21 5 0640 root other

c none /var/mail/dev/msglog 97 1 0600 root other

以下是我见到过或者自己chroot过的daemons（没有任何问题）

popper

rpcbind

named (很多附加的细节，参见我写过的bind 9介绍)

stunnel

Apache web server

Nscd

RADIUS

Squid

syslogd

qmail

第四部分

chroot         执行指令或者shell在特定的根目录下

jail         在chroot下指定监狱环境

daemon    例如：named, imapd, smtp都是daemon

device        ls /dev 就知道了
