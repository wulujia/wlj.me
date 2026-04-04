---
title: "建立virtual honeynet"
date: 2002-06-24T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-403"
---

(quack_at_xfocus.org)

建立virtual honeynet


作者：Etsh911<etsh_cucu@yahoo.com>

整理：quack

日期：2002-06-19


☆ 介绍


    Virtual Honeynet所需要的费用较低，但功能强大、易于管理。这篇文档将尽量清晰地对建立Virtual Honeynet的过程进行描述，在开始之前，我们需要了解下面一些内容：


  ★ 何谓DCAP与DCON


    DCAP（Data CAPture--数据搜集）工具是指我们用来捕获网络中的数据流或者主机上的动作的系列工具。这些工具可能放置在Honeynet中的任何地方，用来搜集攻击者的所有举动。

    DCON（Data CONtrol--数据控制）工具是指我们用来限制网络资源活动的设备、系统或程序。譬如一个防火墙可以限制主机外发连接的数量，这就是数据控制。

    在本文档中，象SNARE就是作为数据搜集工具工作的，而fwbuilder，则是数据控制工具。


  ★ 什么是IDS


    IDS（Intrusion Detection Systems--入侵检测系统）是用来发现并且减少风险的工具。

Danny Rozenblum有一篇关于IDS的经典文档<Understanding Intrusion Detection Syste

ms>，可以参见[http://www.sans.org/infosecFAQ/intrusion/understand.htm](http://www.sans.org/infosecFAQ/intrusion/understand.htm)。

    

  ★ Honeynet及其与Honeypot的区别


    Honeynet模拟出一个真实的网络环境来捕获并且研究入侵者的行为。而Honeypot只是一台运行着模拟和记录程序的一台单独设备（例如一台服务器上运行着嗅探器、键盘记录工具并且伪装出部份存在脆弱性的服务），Lance Spitzner<lance@honeynet.org>对此有一些深入的分析，可以参见[http://www.enteract.com/~lspitz/honeypot.html](http://www.enteract.com/~lspitz/honeypot.html)。


  ★ OpenSSH


    OpenSSH是SSH的自由软件版本，用于替代互联网上以明文方式进行连接管理的telnet、rlogin、rsh、ftp等程序的，它对包括密码在内的所有的通信进行加密，可以消除网络中嗅探、连接劫持的危险。


  ★ User-Mode-Linux


    User-Mode-Linux是一种相当于在安全模式下（用户空间）运行Linux应用程序的工具，在测试有bug的程序、测试新内核或者在你的Linux中瞎折腾时，可以使用它以保护你系统的软、硬件不受损坏。

    可以从[http://sourceforge.net/projects/user-mode-linux/](http://sourceforge.net/projects/user-mode-linux/)或者[http://www3.informatik.unierlangen.de/Research/Projects/UMLinux/umlinux.html](http://www3.informatik.unierlangen.de/Research/Projects/UMLinux/umlinux.html)获得User-Mode-Linux的最新版本进行测试。在Linux Magazine有一篇介绍性文字，可以参见[http://www.linux-mag.com/2001-04/user_mode_01.html](http://www.linux-mag.com/2001-04/user_mode_01.html)。


  ★ Honeynet的优缺点


    优点在于：


    如果你的Honeynet存在于你真实的生产环境中，那么多数攻击者在入侵到你的真实系统前，会被Honeynet所吸引。

    通过一段时期的监控，能够帮助建立更为准确有效的安全策略。

    Honeynet有助于学习应急响应的技能。当一台Honeynet的机器被入侵后，你必须从中找出入侵者留下的痕迹，而所有这一切技能都不可能靠凭空想象得来的。

    许多攻击者把入侵行为当成一种挑战，所以你可以将你的真实网络环境另外镜像一份放到防火墙之外供人攻击，以此来考验你的网络配置的坚固程度。

    或者，你也可以把Honeynet当成学习入侵者的攻击策略、方法、技能和工具的一种手段。


    缺点在于：


    你必须将你的Honeynet的管理员权限拱手让给入侵者，最危险的事情在于，入侵者有可能会将你的Honeynet作为攻击他人的跳板，从而给Honeynet带来麻烦。

    你必须小心谨慎地配置你的网络，以避免在你Honeynet主机上取得最高权限的入侵者，通过一些配置或者程序上的漏洞突破Honeynet进入生产网络。

    Honeynet有可能使你获得一些错误的信息，反而危害你系统的安全。（比如通过对Honynet的研究你认识到telnet明文传输通信是不安全的，决定用ssh来替代它，但你安装了ssh1服务――但某些版本的ssh1存在严重安全漏洞可能导致最高权限的丧失）


  ★ Honeynet的类型


    Honeynet可以分为多种类型，由于篇幅所限，这里仅讨论主要的两种：


    传统的Honeynet：


    传统的Honeynet中的每个点采用的都是真实的主机系统，但这种方式由于费用高昂和管理困难这两个弱点，现在不被推荐使用。很多这种类型的Honeynet都是由于费用和管理上的问题，在开始一段时间后无力维持而夭折了。


    虚拟Honeynet：


    虚拟Honeynet则是采用虚拟环境（由各种虚拟机之类的工具）构造出一个模拟真实生产状态下的网络，这样可以在不丧失传统Honeynet优势的基础上使配置、管理和费用下降

。Honeynet Project<[http://project.honeynet.org/>](http://project.honeynet.org/>)的成员MikeClark<mike@honeynet

.org>有一篇很好的关于虚拟Honeynet的文档，可以参见[http://www.securityfocus.com/](http://www.securityfocus.com/)

infocus/1506


  ★ 注意要点


    Honeynet中的系统必须是基本的、尽量少修改的环境（至少不能让入侵者察觉这是一个陷阱）

    如前面所说的，Honeynet的一个危险之处是必须防止入侵者利用它攻击第三方，这可能有很多种实现方式，比如你可以简单限制从Honeynet系统外发的连接数量。

    你的Honeynet最好要遵守由honeynet research alliance（Honeynet研究联盟）在文章[http://project.honeynet.org/alliance/requirements.html](http://project.honeynet.org/alliance/requirements.html)里所涉及的一些定义、需求和标准。


☆ 预备


    部份工具是本文档描述的Honeynet设置时需要使用的，这些工具如下：


    MySQL<[http://www.mysql.com/>](http://www.mysql.com/>)

    Snort<[http://www.snort.org/>](http://www.snort.org/>)

    Eyes On Exec<[http://www.cs.uni-potsdam.de/homepages/students/linuxer/ok.ht](http://www.cs.uni-potsdam.de/homepages/students/linuxer/ok.ht)

ml>

    FireWall Builder<[http://www.fwbuilder.org/http://sourceforge.net/projects](http://www.fwbuilder.org/http://sourceforge.net/projects)

/fwbuilder/>

    OpenSSH<[http://www.openssh.org/>](http://www.openssh.org/>)

    Modular Syslog<[http://freshmeat.net/projects/msyslog/?highlight=modular+sy](http://freshmeat.net/projects/msyslog/?highlight=modular+sy)

slog>

    SNARE<[http://www.intersectalliance.com/projects/Snare/index.html>](http://www.intersectalliance.com/projects/Snare/index.html>)


    本文档描述的Honeynet网络结构如下：


                            InterNet(Attackers)

                                  +

                                  |

                   ----------------

                   +

                   |

    Honeynet     Real-System

       +                             +

       |                             |

      -------------------------------      -------------

      +        +          +         +      +           +

      |        |   |     |      |           |

     DNS     SMTP       HTTP      HTTPS   /log  LogServ+Snort

                                    |      |

                                    +------+


    Honeynet:ACCEPT to /log;ACCEPT to Internet

    Internet:DENY to Real-System

    Real-System:DENY to Internet


  ★ 建立主机


    安装主机，这台机器将充当网关、防火墙和路由设备。


  ★ 设置防火墙（第一层的DCON）


    安装：


    cd /usr/local/downloads

    tar -zxvf fwbuilder-0.9.7.tar.gz

    cd fwbuilder-0.9.7

    ./configure

    make

    make install


    环境：


    fwbuilder安装完毕之后，用一个GUI界面，这时你可以在其中建立下面这些对象。出于简单考虑，firewall、snort和syslog都放在同一台真实主机上。


--------------------------------------------------------------------------------

|Name     |Type        |IP or Group items         |Description                 |

--------------------------------------------------------------------------------

|Firewall |Workstation |10.10.10.1                |honeynet administrator      |

--------------------------------------------------------------------------------

|Roxen    |Workstation |10.10.10.80               |running the Roxen webserver |

--------------------------------------------------------------------------------

|DNS      |Workstation |10.10.10.53               |This is our DNS server      |

--------------------------------------------------------------------------------

|Sendmail |Workstation |10.10.10.110              |This is our mailserver      |

--------------------------------------------------------------------------------

|Apache   |Workstation |10.10.10.81               |webserver, vulnerabiliable  |

--------------------------------------------------------------------------------

|honeynet |Group       |Roxen+DNS+Sendmail+Apache |These are our honeypots     |

--------------------------------------------------------------------------------

[注]：这个honeynet没有说明故意留下了哪些漏洞，不过看来是通过Apache能够给用户一个nobody shell，再使用EOE防止普通用户成为root，这样限制了攻击者所能做的事。


    策略：


    所有主机都可以通过ssh或MYSQL连通"firewall"

    所有主机都可以连接到honeynet这个组

    honeynet允许连接到任意主机

    除了以上之外，所有的通信都被拦截

    所有防火墙允许通过的数据都记录


    因此策略可以有下面四条：


    Num Source   Destination   Service        Action   Log

    00  any      Firewall      ssh or MySQL   Accept   Log

    01  any      honeynet      any            accept   log

    02  honeynet any           any            accept   log

    03  any      any           any            drop     log


  ★ 配置远程日志服务器


    安装MYSQL：


    cd /usr/local/download

    tar xzf mysql-3.23.28-gamma-pc-linux-gnu-i686.tar.gz

    ln -s mysql-3.23.28-gamma-pc-linux-gnu-i686 mysql

    cd mysql

    mysql_install_db


    运行：


    cd /usr/local/mysql

    bin/safe_mysqld &


    设置密码：


    bin/mysqladmin -u root password mypass


    建立snort和ssyslog的用户并分别给他们对各自数据库的INSERT, DELETE, USAGE, SELECT权限：


    echo CREATE DATABASE snort; | mysql -u root -pmypass

    echo CREATE DATABASE ssyslog; | mysql -u root -pmypass

    mysql -u root -pmypass

    mysql> grant INSERT,SELECT on snort.* to root@*;

    mysql> grant INSERT,SELECT on ssyslog.* to root@*;

    mysql> quit


    安装msyslog-pre_1.08f.tar.gz


    cd /usr/local/downloads

    tar -zxvf msyslog-pre_1.08f.tar.gz

    cd msyslog-pre_1.08f

    ./configure

    make

    make install


    将msyslogd安装完毕，将syslog.mysql.conf拷贝覆盖syslog.conf，将logserver改为msyslogd。


  ★ 入侵检测系统（第二层的DCON）


    作为一个Honeynet，有大量的数据需要手工分析，IDS在这里可以起到很大的帮助。但我们要安装什么类型的IDS呢？


    分类：


    主机型入侵检测系统往往以系统日志、应用程序日志等作为数据源，当然也可以通过其他手段(如监督系统调用)从所在的主机收集信息进行分析。主机型入侵检测系统保护的一般是所在的系统。网络型入侵检测系统的数据源则是网络上的数据包。往往将一台机子的网卡设于混杂模式(promisc mode),监听所有本网段内的数据包并进行判断。一般网络型入侵检测系统担负着保护整个网段的任务。


    选用：


    因为我们是一个Honeynet，从我们的目的考虑，我们需要捕获网络及主机上的所有信息。从这个意义上考虑，这时主机IDS的必要性不是非常明显，所以我考虑使用某些工具，只要能够阻止用户执行shell或者成为超级用户就可以了。网络层我则考虑使用snort作为

入侵检测的记录工具。


    主机IDS：Eye on Exec


    如我们上面所说的，Eye on Exec就是一个阻止用户执行shell或者成为超级用户的微型HIDS，它可以在发现这样的企图后报警，并且发送mail给系统管理员。

    cd /usr/local/downloads

    tar -zxvf eoe-2.51.tar.gz

    cd EoE

    make

    make install

    安装完Eye on Exec后，我们可以编辑eoe.pl这份配置文档（主要修改email地址即可）。


    网络IDS：Snort


    由于Snort的安装配置描述需要比较长的篇幅，这里我推荐阅读Richard La Bella<richard@sfhn.net>的文档<HOWTO Build a Snort/ACID Console on Red Hat Linux >，可以在[http://www.sfhn.net/whites/snortacid.html](http://www.sfhn.net/whites/snortacid.html)获取。（此处链接已不可得，从google上搜得，放在[http://xfocus.net/honeynet/other/snort_acid.html](http://xfocus.net/honeynet/other/snort_acid.html)）。

    建议将snort配置为记录所有连接情况，HoneynetProject提供了一份他们的snort.conf文件，可以参考[http://project.honeynet.org/papers/honeynet/snort.conf](http://project.honeynet.org/papers/honeynet/snort.conf)。

    之所以这么做，有两个原因：一是用snort充当了嗅探器的作用，不用再加载一个sniffer，这样可以减轻系统负载；二是一旦snort没有发现攻击特征，我们还可以通过连接记录的情况来发现入侵企图。


  ★ 安全的远程登陆：OpenSSH


    准备：


    OpenSSH的安装还依赖于两个软件包，OpenSSL<[http://www.openssl.org/>](http://www.openssl.org/>)和zlibtp://www.gzip.org/zlib/>，你可以直接安装其二进制格式，或者直接下载源代码，然后

用./configure&&make&&make install安装。


    安装：


    rpm -Uvh zlib.rpm

    rpm -Uvh openssl-0.9.6c.rpm

    rpm -Uvh openssh-3.0.2p1.rpm


    这时用ssh -V察看，会显示出：


    OpenSSH_3.0.2p1, SSH protocols 1.5/2.0, OpenSSL 0x0090601f


    可能会有版本上的不同，但这无关紧要。


    配置：


    编辑/etc/ssh/sshd_config，将"#Protocol 2,1"改为"Protocol 2"，还可以配置是否允许RSA key等等。


☆ 配置Virtual Honeynet


    虚拟Honeynet通常依靠某些模拟软件，在一个操作系统上同时运行几个虚拟的系统，这样的软件有如vmware<[http://www.vmware.com/>](http://www.vmware.com/>) Bochs<[http://bochs.sourceforge.n](http://bochs.sourceforge.n/)

et/>, Plex86<[http://www.plex86.org/>](http://www.plex86.org/>)等，它们都可以在你真实的操作系统上模拟出一个虚拟系统来。但在使用一段时间之后，我发现它们存在着不同程度的问题，比如资源占用严重。于是我希望寻找一个软件来实现在Linux中运行Linux的功能，于是我找到了User-Mode-Linux。


  ★ 创建内核


    你可以直接下载User-Mode-Linux的二进制版本，但是，使用源代码编译无疑能给你更大的自由度，你可以对内核进行一些修改以更适合你的需要。

    从[http://www.kernel.org/](http://www.kernel.org/)下载内核，使用UML的patch对内核进行补丁。


    cd /usr/local/downloads/linux

    tar -zxvf linux-2.4.15.tar.gz

    cd linux-2.4.15

    wget [http://prdownloads.sourceforge.net/user-mode-linux/uml-patch-2.4.16-2](http://prdownloads.sourceforge.net/user-mode-linux/uml-patch-2.4.16-2)

.bz2

    cat uml-patch-2.4.16.bz2 | bunzip2 - |patch -p1


    然后你可以用你喜欢的方式编译内核了，只是记得加上"ARCH=um"，比如你用make xconfig，现在就需要用make xfocus ARCH=um，然后"make dep ARCH=um" 、"make linux ARCH=um", 编译完成后你会得到一个名为"linux"的可执行文件。

    你还必须下载或者自己创建root file system文件，并以之作为UML的启动参数。可以在[http://sourceforge.net/project/showfiles.php?group_id=429&release;_id=51115](http://sourceforge.net/project/showfiles.php?group_id=429&release_id=51115)下载。可以在一台真实的机器上用不同的root file system来启动UML。


    "ubdx=file" 表示在/dev/ubx的虚拟磁盘，另外还需要创建一个swap区。

    "umn=address" 表示IP地址，如果你没有输入这一参数，则默认的IP地址是192.168.

0.253，默认的子网掩码是255.255.255.0, 你也可以用ifconfig命令来修改它。

    "eth0=mcast" 告诉真实（物理的）系统使用第一块以太网卡作为多播设备。


    更多选项的意义可以参见User Mode Linux HOWTO<>。


    为了更好地使用UML的网络性能，你可能还需要uml_switch和uml_net工具，也可以从UML的主页获取并编译。


  ★ 启动虚拟系统


    现在可以用如下命令启动虚拟系统


    linux ubd0=root_fs.rh72.pristine.bz2 ubd1=swap eth0=mcast umn=10.10.10.50


    以root登陆系统，密码为空，然后你可以对你的虚拟系统进行配置了。这里并不打算探讨如何安装配置Apache、DNS、Sendmail和Roxen，从它们的文档中可以得到详细的帮助。当然，作为honeynet，你可以将日志记录等级设为最高。


    当然在虚拟系统中你可能会遇到一些问题，推荐阅读UML的HOWTO文档中networking部份。现在我们的整个Honeynet就算基本可以工作了。


☆ 陷阱


  ★ Ssyslog


    前面我们提到过将syslog更改并且将日志发送到MYSQL中，现在我们再做一次同样的工作，只是这次我们是在虚拟的机器中这么做，日志仍然发送到真实（物理的）机器上的MYSQL数据库中。


  ★ Snare


    Snare可以被看作是一个用来进行审计工作的内核级的HIDS，它有一个配置项，可以简单地使你的计算机达到C2级的标准。


    安装：


    rpm --install snare-core-0.8-1.i386.rpm snare-0.8-1.i386.rpm


    也可以从源代码安装，建议先阅读snare的文档[http://www.intersectalliance.com/](http://www.intersectalliance.com/)

projects/Snare/Documentation/index.html#SNARE_Installation。


    配置：


    在UML下，没有必要运行X，所以Snare的GUI界面可能用处不大，你可以简单编辑 /et

c/audit/audit.conf文件，[http://www.intersectalliance.com/projects/Snare/Docume](http://www.intersectalliance.com/projects/Snare/Docume)

ntation/index.html#AnnexC是Snare配置项的说明文字可供参考。

    你也可以配置Snare将日志存放于远程服务器上，这里可以存放在我们的真实（物理的）机器上，或者我们可以设置严格的ACL来管理日志，或者只允许日志以appen only形式存

在。[http://www.grsecurity.net/](http://www.grsecurity.net/)有一个很好的ACL工具，但你必须在创建UML前先patch上。最后，必须用ln -s /etc/init.d/auditd /etc/rc.d/rc3/S90audit命令让Snare在启动时运行。

    Snare没有记录可加载内核模块的加载，但可加载内核模块可能带来很大的安全风险，可以参见附件A，因此在附件B中有一个内核patch，能够对模块的加载进行记录。


☆ 附件


  ★ Appendix A: Situations - Loadable Kernel Modules (LKMs)

     [http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/LKM.php](http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/LKM.php)

  ★ Appendix B: Kernel patch for detecting and logging LKM loading

     [http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/module.patch](http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/module.patch)

  ★ Appendix C: Modified rc.firewall to block outgoing DDoS attacks

     [http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/rc.firewall](http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/rc.firewall)

  ★ Appendix D: Port-Scand

     [http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/detect1.txt](http://www.securitywriters.org/texts/internetsecurity/Virtual_HoneyNet_files/detect1.txt)
