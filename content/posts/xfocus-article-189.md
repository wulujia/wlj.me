---
title: "系统遭受入侵后使用TCT进行紧急恢复并分析"
date: 2001-06-10T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-189"
---

(inburst_at_263.net)

系统遭受入侵后使用TCT进行紧急恢复并分析


by inburst<inburst@263.net>

[http://xfocus.org;http://inburst.org](http://xfocus.org;http//inburst.org)

2001-6-10


    从事系统管理工作，就算你非常小心翼翼地做好了一切防护，还是可能有入侵者能够突破你

的防护进入系统，并且更改或者删除一些文件。这里，我们借用honeynet project里面的一些实

例，来对一个unix下的实用工具软件tct及其相关辅助软件做简要说明。并且在最后再介绍另外

一个比较不错的能恢复ext2文件系统的软件recover。

    首先说一下相关的软件：

    1、The Coroners Toolkit：也就是我们所说的TCT，想要在国内下载的话，您可以到安全焦

点([http://xfocus.org/tool/other/tct-1.07.tar.gz](http://xfocus.org/tool/other/tct-1.07.tar.gz))下载。这是一个unix下的命令行文件系统

工具集，支持FFS及ext2fs，从块及结点处来对数据进行恢复。它能够针对文件的最后修改、访

问或者改变(MAC)的时间来进行分析，并且根据数据节点的值提取出文件列表以进行恢复。

    2、TCTUTILs：在[http://xfocus.org/tool/other/tctutils-1.01.tar.gz](http://xfocus.org/tool/other/tctutils-1.01.tar.gz)可以下载当前最新

版本。它是对TCT的补充，提供了根据文件名对数据进行恢复的命令行工具。这两个工具都需要

使用者对一些底层基本知识比较了解。

    3、Autopsy Forensic Browser：可以从[http://xfocus.org/tool/other/autopsy-1.01.tar.gz](http://xfocus.org/tool/other/autopsy-1.01.tar.gz)

下载。它提供了一个友好的html界面给tct及tctutils。它能使枯燥的分析工作相对轻松些:)


    一、安装：TCT在各种unix平台下都经过了比较好的测试。现在能够支持FreeBSD、OpenBSD、

SunOS、Linux等平台。TCTUTILs和Autopsy则不一定能跑得起来，我测试的平台是一台默认安装

的Red Hat 6.2系统。


    1、tct


    # tar zvfx tct-1.07.tar.gz -C /usr/local/tct/; cd /usr/local/tct/tct*; make

    这样把tct展开到/usr/local/tct/tct-1.07/的目录下，并且进入，make。这里，如果是make

过之后，需要重新在编译的话，需要运行perl reconfig命令重新配置。


    2、tctutils:


    # tar zvfx tctutils-1.01.tar.gz -C /usr/local/tct;cd /usr/local/tct/tctu*;make

    现在tctutils似乎只在OpenBSD 2.8、Debian Linux 2.2、Solaris 2.7下经过详尽测试，而

对FreeBSD还支持不好。通常make不会出现什么问题，如果有，自己改下代码或者Makefile即可。


    3、Autopsy：


    解包后运行./configure后，它会自己寻找一些实用工具如grep、strings、md5sum的路径，

并要求确认tct以及tctutils的路径(如果没找到会要求你输入正确路径)。最后要求输入需要检

查的文件系统所在，才生成程序autopsy。


    二、honeynet scan15简介：


    关于honeynet project的详情，可以参见安全焦点([http://xfocus.org/honeynet/](http://xfocus.org/honeynet/))，他们

现在维护着国外honeynet项目的中文镜像。

    scan15是honeynet在2001年3月15日于一台受入侵的Linux机器上搜集到的数据而面临的问题。

入侵者下载了一些rootkit放在根目录下，成功安装后删除了。而honeynet project将当时的原始

数据镜像下来，作为题目出给网络安全爱好者，要求对这一被删除的rootkit进行恢复。

    详情可以参见[http://xfocus.org/honeynet/scans/](http://xfocus.org/honeynet/scans/)。

    根据要求，我下载了honeynet.tar.gz的包，约13M，解压后是一个270M左右的文件honeypot.hda8.dd

及一个README文件，README如下：


    ===================================================================


    SUMMARY

    -------

    You have download the / partition of a compromised RH 6.2

    Linux box.  Your mission is to recover the deleted rootkit

    from the / partition.   Below are a list of all the partitions

    that made up the compromised system.


    /dev/hda8       /      <----- The partition you downloaded

    /dev/hda1       /boot

    /dev/hda6       /home

    /dev/hda5       /usr

    /dev/hda7       /var

    /dev/hda9       swap


           - The Honeynet Project

             [http://project.honeynet.org](http://project.honeynet.org/)


    ====================================================================

            图一


    任务非常明确。


    三、操作过程


    1、确认下载数据无误


    # md5sum honeynet.tar.gz 

    0dff8fb9fe022ea80d8f1a4e4ae33e21 honeynet.tar.gz 

    # md5sum honeypot.hda8.dd 

    5a8ebf5725b15e563c825be85f2f852e honeypot.hda8.dd 


    这些md5校验值同honeynet网站上贴出来的一样，说明文件下载无误，未经篡改。


    2、将下载下来的镜像挂接到系统上


    # mount honeypot.hda8.dd /mnt/ -oloop,ro

    

    3、配置autopsy并运行之(其实在上面autopsy的configure过程中就做这步了)


    ====================================================================

    [root@test autopsy-1.01]# ./configure

       Autopsy Forensic Browser v.1.01 Installation

    MD5 found: /usr/bin/md5sum

    strings found: /usr/bin/strings

    grep found: /bin/grep

    Enter TCT Directory:

    /usr/local/tct

      TCT bin directory was found

    Enter TCTUTILs Directory:

    /usr/local/tctutils

      TCTUTILs bin directory was found

    Enter Morgue Directory:

    /home/inburst      

    Enter Default Investigator Name (for the Autopsy Reports):

    inburst

    Settings saved to conf.pl

    [root@test autopsy-1.01]#

    ====================================================================

                图二


    然后进入/home/inburst/，你存放honeypot.hda8.dd的地方，编辑文件fsmorgue,使其看来象

下面这样：


    ====================================================================

    # fsmorgue file for Autopsy Forensic Browser

    #

    # local_file name can contain letters, digits, '-', '_', and '.'

    #

    # local_file    mount_point

    honeypot.hda8.dd        /mnt/

    ====================================================================

                图三


    并且编辑zoneinfo，确定时间信息。


    然后可以运行命令：


    # ./autopsy 9999 192.168.168.130


    这里192.168.168.130是我所用的工作机，9999是端口号，屏幕上会输出：


    ====================================================================

    Autopsy Forensic Browser ver 1.01

    Investigator: inburst


    Paste this as your browser URL on 192.168.168.130:

        192.168.168.130:9999/1727589285/autopsy

    ====================================================================

                图四


    将192.168.168.130:9999/1727589285/autopsy粘贴到你的浏览器url里，就可以开始进一步的分析了。


    4、恢复被删除的rootkit，这里我们先纯用命令行来解决问题，其实利用autopsy可以令这些麻烦事

看起来相对直观些。


    a、搜集信息


    ====================================================================

    # ils honeypot.hda8.dd > ilsdump.txt

    # cat ilsdump.txt

    class|host|device|start_time

    ils|test.inburst.com.cn|honeypot.hda8.dd|992134159

    st_ino|st_alloc|st_uid|st_gid|st_mtime|st_atime|st_ctime|st_dtime|st_mode|st_nlink|st_size|st_block0|st_block1

    23|f|0|0|984706608|984707090|984707105|984707105|100644|0|520333|307|308

    2038|f|1031|100|984707105|984707105|984707105|984707169|40755|0|0|8481|0

    ……

    ……

    ====================================================================

                图五


    ils命令是用来显示inode信息的，它显示了每个被删除的文件节点的原始资料。上面显示的第一个域是

结点号。后面数据恢复时需要用到，关于这个输出的详细信息如下：


    st_ino：The inode number. 

    st_alloc：Allocation status: `a' for allocated inode, `f' for free inode. 

    st_uid：Owner user ID. 

    st_gid：Owner group ID. 

    st_mtime：UNIX time (seconds) of last file modification. 

    st_atime：UNIX time (seconds) of last file access. 

    st_ctime：UNIX time (seconds) of last inode status change. 

    st_dtime：UNIX time (seconds) of file deletion (LINUX only). 

    st_mode：File type and permissions (octal). 

    st_nlink：Number of hard links. 

    st_size：File size in bytes. 

    st_block0,st_block1：The first two entries in the direct block address list. 


    ====================================================================  

    # /usr/local/tct/extras/ils2mac ilsdump.txt > deletedfiles.txt

    # cat deletedfiles.txt

    class|host|device|start_time

    body|test.inburst.com.cn|honeypot.hda8.dd|992134159

    md5|file|st_dev|st_ino|st_mode|st_ls|st_nlink|st_uid|st_gid|st_rdev|st_size|st_atime|st_mtime|st_ctime|st_blksize|st_blocks

    |<honeypot.hda8.dd-dead-23>||23|100644|-rw-r--r--|0|0|0||520333|984707090|984706608|984707105||

    |<honeypot.hda8.dd-dead-2038>||2038|40755|drwxr-xr-x|0|1031|100||0|984707105|984707105|984707105||

    |<honeypot.hda8.dd-dead-2039>||2039|100755|-rwxr-xr-x|0|0|0||611931|984707090|1013173693|984707105||

    |<honeypot.hda8.dd-dead-2040>||2040|100644|-rw-r--r--|0|0|0||1|984707090|983201398|984707105||

    ……

    ……

    ====================================================================

                图六


    ils2mac重新排列输出了上面的信息，这在你有多个磁盘分区需要分析时比较有用。


    ====================================================================

    # mactime -p /mnt/etc/passwd -g /mnt/etc/group -b deletedfiles.txt 1/1/2001 > mactime.txt

    # cat mactime.txt

    Feb 08 02 21:08:13   611931 m.. -rwxr-xr-x root     root     <honeypot.hda8.dd-dead-2039>

    Jan 27 01 23:11:32     3278 m.. -rw-r--r-- root     root     <honeypot.hda8.dd-dead-2044>

    Jan 27 01 23:11:44    11407 m.. -rw-r--r-- root     root     <honeypot.hda8.dd-dead-2046>

    Feb 26 01 22:46:04   632066 m.. -rwxr-xr-x root     root     <honeypot.hda8.dd-dead-2061>

    Feb 26 01 23:22:55     4060 m.. -rwxr-xr-x root     root     <honeypot.hda8.dd-dead-2047>

    Feb 26 01 23:22:59     8268 m.. -rwx------ root     root     <honeypot.hda8.dd-dead-2053>

    Feb 26 01 23:23:10     4620 m.. -rwxr-xr-x root     root     <honeypot.hda8.dd-dead-2054>

    Feb 26 01 23:23:55    53588 m.. -rwxr-xr-x root     root     <honeypot.hda8.dd-dead-2058>

    Feb 26 01 23:24:03       75 m.. -rwx------ root     root     <honeypot.hda8.dd-dead-2059>

    Feb 26 01 23:28:40       79 m.. -rwxr-xr-x root     root     <honeypot.hda8.dd-dead-2045>

    Feb 26 01 23:29:51      688 m.. -rw-r--r-- root     root     <honeypot.hda8.dd-dead-2052>

    Feb 26 01 23:29:58        1 m.. -rw-r--r-- root     root     <honeypot.hda8.dd-dead-2040>

    Mar 03 01 11:05:12      708 m.. -rw-r--r-- root     root     <honeypot.hda8.dd-dead-2060>

    Mar 03 01 11:08:37     3713 m.. -rwx------ root     root     <honeypot.hda8.dd-dead-2041>

    Mar 15 01 19:17:36    33135 mac -rw-r--r-- root     root     <honeypot.hda8.dd-dead-56231>

    Mar 15 01 19:19:37       16 ma. lrwxrwxrwx root     root     <honeypot.hda8.dd-dead-12107>

                             16 ma. lrwxrwxrwx root     root     <honeypot.hda8.dd-dead-20883>

                             16 ma. lrwxrwxrwx root     root     <honeypot.hda8.dd-dead-28172>

    Mar 15 01 19:20:25       16 ..c lrwxrwxrwx root     root     <honeypot.hda8.dd-dead-12107>

                            239 .ac -rw-r--r-- root     root     <honeypot.hda8.dd-dead-16110>

    ……

    ……

    ====================================================================

                图七


    mactime命令则是按时间，inode对输出进行排列、对比，显示出哪些inodes被修改或者存取过。

    

    OK，有趣的东西玩过了，让我们来看看，其实用autopsy就不用这么麻烦，大家可以从[http://xfocus.org/tmp/autopsy.jpg](http://xfocus.org/tmp/autopsy.jpg)

看到相关的抓图，从图上就可以清楚地看出，我们要恢复的数据在哪里了:)                                 

    

    b、恢复数据

    

    通过上面的数据分析之后，我们应该能够自己判断哪些数据可能是比较有趣的，然后用icat命令加以提取。从上面的图中我们可以

知道，结点23处的lk.tgz应该是比较好玩的东西，好吧，让我们来看看。    


    ====================================================================

    # icat honeypot.hda8.dd 23 > file-23    <--提取

    # file file-23        <--看文件类型

    file-23: gzip compressed data, deflated, last modified: Sat Mar  3 11:09:06 2001, os: Unix

    # tar zvfx file-23    <--解包

    last/

    tar: Archive contains future timestamp 2002-02-08 21:08:13

    last/ssh

    last/pidfile

    last/install

    last/linsniffer

    last/cleaner

    last/inetd.conf

    last/lsattr

    last/services

    last/sense

    last/ssh_config

    last/ssh_host_key

    last/ssh_host_key.pub

    last/ssh_random_seed

    last/sshd_config

    last/sl2

    last/last.cgi

    last/ps

    last/netstat

    last/ifconfig

    last/top

    last/logclear

    last/s

    last/mkxfs

    ====================================================================

                图八


    很容易地就把被删除的rk.tgz恢复出来了。如果感兴趣的话，我们还可以对图中结点2038处的/last目录也一并恢复。现在

先看看2038里放着的是什么：


    ====================================================================

    # ils honeypot.hda8.dd 2038 

    …… 

    2038|f|1031|100|984707105|984707105|984707105|984707169|40755|0|0|8481|0 

                                      ^^^^

                                       |

                                       +-->注意这里

    # bcat -h honeypot.hda8.dd 8481 512

    0       f6070000 0c000102 2e000000 02000000     .... .... .... ....

    16      f4030202 2e2e0000 f7070000 0c000301     .... .... .... ....

    32      73736800 f8070000 10000701 70696466     ssh. .... .... pidf

    48      696c6500 f9070000 10000701 696e7374     ile. .... .... inst

    64      616c6c00 fa070000 14000801 636f6d70     all. .... .... comp

    80      75746572 65720000 fb070000 10000701     uter er.. .... ....

    96      636c6561 6e657200 fc070000 14000a01     clea ner. .... ....

    112     696e6574 642e636f 6e660000 fd070000     inet d.co nf.. ....

    128     10000601 6c736174 74720000 fe070000     .... lsat tr.. ....

    144     20000801 73657276 69636573 ff070000      ... serv ices ....

    160     10000501 73656e73 65000000 00080000     .... sens e... ....

    176     28000a01 7373685f 636f6e66 69670000     (... ssh_ conf ig..

    192     01080000 14000c01 7373685f 686f7374     .... .... ssh_ host

    208     5f6b6579 02080000 30001001 7373685f     _key .... 0... ssh_

    224     686f7374 5f6b6579 2e707562 03080000     host _key .pub ....

    240     18000f01 7373685f 72616e64 6f6d5f73     .... ssh_ rand om_s

    256     65656400 04080000 fc020b01 73736864     eed. .... .... sshd

    272     5f636f6e 66696700 05080000 0c000301     _con fig. .... ....

    288     736c3200 06080000 dc020801 6c617374     sl2. .... .... last

    304     2e636769 07080000 2c000201 70730000     .cgi .... ,... ps..

    320     08080000 20000701 6e657473 74617400     ....  ... nets tat.

    336     09080000 10000801 6966636f 6e666967     .... .... ifco nfig

    352     0a080000 0c000301 746f7000 0b080000     .... .... top. ....

    368     10000801 6c6f6763 6c656172 0c080000     .... logc lear ....

    384     84020101 73000000 0d080000 78020501     .... s... .... x...

    400     6d6b7866 73000000 00000000 00000000     mkxf s... .... ....

    416     00000000 00000000 00000000 00000000     .... .... .... ....

    432     00000000 00000000 00000000 00000000     .... .... .... ....

    448     00000000 00000000 00000000 00000000     .... .... .... ....

    464     00000000 00000000 00000000 00000000     .... .... .... ....

    480     00000000 00000000 00000000 00000000     .... .... .... ....

    496     00000000 00000000 00000000 00000000     .... .... .... ....

    ====================================================================

                图九


    我们可以看出last目录其实就是lk.tgz的解包，没有太大的恢复价值了;)

    

    c、进一步分析


    现在rootkit也已经找到了，我们就应该来看看究竟它们被装到哪里了，有个简单的办法，可以不用

我们花太多的精力手工寻找。

    

    # find /mnt -type f -exec md5sum {} \; > md5.all


    这样将我们mount上的盘中所有可执行文件都提取出来，用md5sum取它的hash，并且存入md5.all文件

中，准备跟rootkit进行对比。


    ====================================================================

    # for i in last/*

    > do echo $i;

    > grep `md5sum $i` md5.all;

    > done;

    last/cleaner

    last/ifconfig

    md5.all:086394958255553f6f38684dad97869e  /mnt/sbin/ifconfig

    last/inetd.conf

    md5.all:b63485e42035328c0d900a71ff2e6bd7  /mnt/etc/inetd.conf

    last/install

    last/last.cgi

    last/linsniffer

    md5.all:6c0f96c1e43a23a21264f924ae732273  /mnt/dev/ida/.drag-on/linsniffer

    md5.all:6c0f96c1e43a23a21264f924ae732273  /mnt/dev/ida/.. /linsniffer

    last/logclear

    md5.all:5f22ceb87631fbcbf32e59234feeaa5b  /mnt/dev/ida/.drag-on/logclear

    md5.all:5f22ceb87631fbcbf32e59234feeaa5b  /mnt/dev/ida/.. /logclear

    last/lsattr

    last/mkxfs

    md5.all:18a2d7d3178f321b881e7c493af72996  /mnt/dev/ida/.drag-on/mkxfs

    md5.all:18a2d7d3178f321b881e7c493af72996  /mnt/dev/ida/.. /mkxfs

    last/netstat

    md5.all:2b07576213c1c8b942451459b3dc4903  /mnt/bin/netstat

    last/pidfile

    md5.all:68b329da9893e34099c7d8ad5cb9c940  /mnt/etc/at.deny

    last/ps

    md5.all:7728c15d89f27e376950f96a7510bf0f  /mnt/bin/ps

    last/s

    md5.all:06d04fa3c4941b398756d029de75770e  /mnt/dev/ida/.drag-on/s

    md5.all:06d04fa3c4941b398756d029de75770e  /mnt/dev/ida/.. /s

    last/sense

    md5.all:464dc23cac477c43418eb8d3ef087065  /mnt/dev/ida/.drag-on/sense

    md5.all:464dc23cac477c43418eb8d3ef087065  /mnt/dev/ida/.. /sense

    last/services

    md5.all:54e41f035e026f439d4188759b210f07  /mnt/etc/services

    last/sl2

    md5.all:4cfae8c44a6d1ede669d41fc320c7325  /mnt/dev/ida/.drag-on/sl2

    md5.all:4cfae8c44a6d1ede669d41fc320c7325  /mnt/dev/ida/.. /sl2

    last/ssh

    last/ssh_config

    last/ssh_host_key

    md5.all:c2c1b08498ed71a908c581d634832672  /mnt/dev/ida/.drag-on/ssh_host_key

    md5.all:c2c1b08498ed71a908c581d634832672  /mnt/dev/ida/.. /ssh_host_key

    last/ssh_host_key.pub

    last/ssh_random_seed

    md5.all:ad265d3c07dea3151bacb6930e0b72d3  /mnt/dev/ida/.. /ssh_random_seed

    last/sshd_config

    last/top

    ====================================================================

                图十


    这种方法对入侵检测有着极大帮助。从上面的输出我们可以非常轻松地判断出rootkit被安装在几

个隐藏目录下，如

    /dev/ida/.. /

    /dev/ida/.drag-on/


    d、由于本文的重点不是放在入侵检测上，所以对该image中其它入侵者留下的痕迹就不再做进一步

分析了，建议如果感觉兴趣同志可以自己去下载这个包来进行一次模拟入侵实战，并且可以从honeynet

的高手们的分析过程中得出很多经验。

    

    最后，介绍一个由叫recover的软件。这个软件可以恢复ext2下被删除的文件，但是没有tct那样功能

强大。只是相对更“傻瓜”一些，操作起来比较方便。可以在[http://xfocus.org/tool/other/recover-1.2.tar](http://xfocus.org/tool/other/recover-1.2.tar)

获取。

    它的运行简单，只要运行./recover就OK了，然后会问你需要恢复的数据所以磁盘、删除时间、文件

大小等一系统信息，以帮助精确定位需要恢复的文件，但最后恢复出来的东西，都是以数字排序，分析

起来有一定的难度。


    大致如此，have fun。


参考资料：

1、《Honeynet Scan of the Month #15》 by Brian Carrier

2、[http://www.xfocus.org/honeynet/](http://www.xfocus.org/honeynet/) 安全焦点陷阱网络

3、tct\tctutils\autopsy的man page([http://www.xfocus.org/tmp/tct_man.zip](http://www.xfocus.org/tmp/tct_man.zip))

4、[http://www.incident-response.org/](http://www.incident-response.org/)
