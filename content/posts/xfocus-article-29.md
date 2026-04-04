---
title: "入侵检测工具Watcher"
date: 2000-07-24T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-29"
---

文章提交：[quack](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

入侵检测工具Watcher

===================

by quack  <quack@antionline.org>

参考资料 Watcher by hyperion <hyperion@hacklab.com> in pharck

 

一、写在前面

你如何了解系统是否被攻克？在你发现系统中多了些奇怪的帐号或者某些特洛伊程序时，

一切已经太迟了。除非你的机器非常强大，否则你的机会只存在于当你在机器被扫描后、

而攻击发生前的短暂的时间段里。当然你可以用类似于tcp wrappers的程序来保证系统

连接的安全，但它并不能监测到stealth扫描或者DOS攻击，你也可以购买商业版本的入

侵监测系统――只要你不嫌贵的话，其实性价比最高的就是从互联网上获取类似的免费

的软件，安装或者改造它以适应你的需求，watcher就是这么一个家伙。

二、功能

watcher检测所有通过的信息包，并且将它认为是恶意的攻击行为记录在syslog中，当前

的watcher能够检测下列的攻击行为：

    - 所有的TCP扫描

    - 所有的UDP扫描

    - Synflood攻击

    - Teardrop攻击

    - Land攻击

    - Smurf攻击

    - Ping of death攻击

所有的参数以及配置都是在命令行给出的，你可以配置它仅仅监视扫描行为或者仅仅监

视DOS攻击。它的监测行为是这样的：如果在短时间内有超过7个以上的端口收到信息包

(不管类型如何)，那么这一事件就被当成端口扫描记录下来。UDP扫描认定的原理也一

样。当watcher在同一端口收到超过8个的syn包没有带ack或者fin位的话，就会认定是

synflood攻击事件。如果UDP的碎片包――IP包的id号是242，它就认为是teardrop攻击，

因为发布的攻击代码使用的是242的id号――这点存在不足;(。对同一端口的大量TCP 

SYN包，带源地址及目标地址的，将被认为是land攻击，如果有超过5个icmp echo replies

在很短时间内出现(时间可以自定义)，将记录为smurf攻击……

Watcher有三种监测模式，在默认的模式下，它仅仅监测对本台主机的攻击行为，第二种

模式可以监测在C类子网内的所有主机，第三种模式则可以监测所有能接收到信息包的主

机。当你把watcher放在外部主机上时，监测多主机特别有效，当一台主机的log文件被

破坏时，其它主机上还有记录。

由于watcher把所有的信息包都当成“攻击”，然后再进行分析，这种判断是极为粗糙的，

可能会误判，所以在代码中作者加入了一些过滤的技巧。

比如一些web server上会有漂亮的gif图片或者flash等玩意儿，而客户端这时往往会开了

多个线程来下载它，这时watcher的规则就会认为这是一次tcp scan，所以作者只好加上了

只有超过40个tcp连接才记录下的的规则――这些都是可定制的。就不详述了，你可以自行

参看下面的代码。

它的输出是非常简单的，每隔10秒它就将可能的攻击行为记录在syslog当中，同时源IP以及

目标IP甚至相关的信息比如端口号，包的数量等等也将被记录下来，如果该攻击行为的IP是

假的，那么它同时将记下MAC地址――如果攻击来自外部，地址将是你本地接收到该包的route

的地址，如果攻击来自内部的话，呵，你可以用自己的方式来"感谢"攻击者;)

三、程序参数

Watcher是用于linux系统的，通常你只需要在命令行后台运行它就可以了，它的参数如下：

Usage: watcher [参数] 

  -d device       将'device'设定为当前的网卡，默认为第一个non-loopback的interface

  -f flood        设定接收到多少不完全的连接后才认为是flood的攻击

  -h              帮助信息

  -i icmplimit    设定接收到多少icmp echo replies就认为是smurf攻击

  -m level        可以设定监控的机器，比如subnet为子域中的机器，或者all为所有

  -p portlimit    在timeout的限制时间内有多少端口接收到信息包算是一次端口扫描

  -r reporttype   如果reporttype设为dos，那么只有拒绝服务攻击会被记录，如果是scan

                  的话，只有扫描行为会被记录，默认则记录所有东西

  -t timeout      每隔timeout的时间就记录信息包并打印出潜在的攻击行为

  -w webcount     设定我们从80口接收到多少信息包才算是一次端口扫描(cgi)

希望这个小玩意能使你的系统稍微安全一些，但是得警告你的是，系统安全是多方面的，别

指望一个应用程序或者什么东西能使你绝对安全――如果你不信，迟早都得重装系统的;)

----[  代码

<++> EX/Watcher.c

/*********************************************************************

Program: watcher

A network level monitoring tool to detect incoming packets indicative of

potential attacks.

This software detects low level packet scanners and several DOS attacks.

Its primary use is to detect low level packet scans, since these are usually

done first to identify active systems and services to mount further attacks.

The package assumes every incoming packet is potentially hostile.  Some checks

are done to minimize false positives, but on occasion a site may be falsely

identified as having performed a packet scan or SYNFLOOD attack.  This usually

occurs if a large number of connections are done in a brief time right before

the reporting timeout period (i.e. when browsing a WWW site with lots of

little GIF's, each requiring a connection to download).  You can also get false

positives if you scan another site, since the targets responses will be viewed

as a potential scan of your system.

By default, alerts are printed to SYSLOG every 10 seconds.

***********************************************************************/

#include <stdio.h>

#include <sys/types.h>

#include <sys/time.h>

#include <sys/socket.h>

#include <sys/file.h>

#include <sys/time.h>

#include <netinet/in.h>

#include <netdb.h>

#include <string.h>

#include <errno.h>

#include <ctype.h>

#include <malloc.h>

#include <netinet/tcp.h>

#include <netinet/in_systm.h>

#include <net/if_arp.h>

#include <net/if.h>

#include <netinet/udp.h>

#include <netinet/ip.h>

#include <netinet/ip_icmp.h>

#include <linux/if_ether.h>

#include <syslog.h>

#define PKTLEN 96    /* Should be enough for what we want */

#ifndef IP_MF

#define IP_MF    0x2000

#endif

/***** WATCH LEVELS ******/

#define MYSELFONLY    1

#define MYSUBNET    2

#define HUMANITARIAN    3

/***** REPORT LEVELS *****/

#define REPORTALL    1

#define REPORTDOS    2

#define REPORTSCAN    3

struct floodinfo {

    u_short sport;

    struct floodinfo *next;

};

struct addrlist {

    u_long saddr;

    int cnt;

    int wwwcnt;

    struct addrlist *next;

};

struct atk {

    u_long saddr;

    u_char eaddr[ETH_ALEN];

    time_t atktime;

};

struct pktin {

    u_long saddr;

    u_short sport;

    u_short dport;

    time_t timein;

    u_char eaddr[ETH_ALEN];

    struct floodinfo *fi;

    struct pktin *next;

};

struct scaninfo {

    u_long addr;

    struct atk teardrop;

    struct atk land;

    struct atk icmpfrag;

    struct pktin *tcpin;

    struct pktin *udpin;

    struct scaninfo *next;

    u_long icmpcnt;

} ;

struct scaninfo *Gsilist = NULL, *Gsi;

u_long Gmaddr;

time_t Gtimer = 10, Gtimein;

int Gportlimit = 7;

int Gsynflood = 8;

int Gwebcount = 40;

int Gicmplimit = 5;

int Gwatchlevel = MYSELFONLY;

int Greportlevel = REPORTALL;

char *Gprogramname, *Gdevice = "eth0";

/******** IP packet info ********/

u_long Gsaddr, Gdaddr;

int Giplen, Gisfrag, Gid;

/****** Externals *************/

extern int errno;

extern char *optarg;

extern int optind, opterr;

void do_tcp(), do_udp(), do_icmp(), print_info(), process_packet();

void addtcp(), addudp(), clear_pktin(), buildnet();

void doargs(), usage(), addfloodinfo(), rmfloodinfo();

struct scaninfo *doicare(), *addtarget();

char *anetaddr(), *ether_ntoa();

u_char *readdevice();

main(argc, argv)

int argc;

char *argv[];

{

    int pktlen = 0, i, netfd;

    u_char *pkt;

    char hostname[32];

    struct hostent *hp;

    time_t t;

    doargs(argc, argv);

    openlog("WATCHER", 0, LOG_DAEMON);

    if(gethostname(hostname, sizeof(hostname)) < 0)

    {

    perror("gethostname");

    exit(-1);

    }

    if((hp = gethostbyname(hostname)) == NULL)

    {

    fprintf(stderr, "Cannot find own address\n");

    exit(-1);

    }

    memcpy((char *)&Gmaddr, hp->h_addr, hp->h_length);

    buildnet();

    if((netfd = initdevice(O_RDWR, 0)) < 0)

    exit(-1);

    /* Now read packets forever and process them. */

    t = time((time_t *)0);

    while(pkt = readdevice(netfd, &pktlen))

    {

    process_packet(pkt, pktlen);

    if(time((time_t *)0) - t > Gtimer)

    {

        /* Times up.  Print what we found and clean out old stuff. */

        for(Gsi = Gsilist, i = 0; Gsi; Gsi = Gsi->next, i++)

        {

                clear_pktin(Gsi);

            print_info();

        Gsi->icmpcnt = 0;

        }

        t = time((time_t *)0);

    }

    }

}

/**********************************************************************

Function: doargs

Purpose:  sets values from environment or command line arguments.

**********************************************************************/

void doargs(argc, argv)

int argc;

char **argv;

{

    char c;

    Gprogramname = argv[0];

    while((c = getopt(argc,argv,"d:f:hi:m:p:r:t:w:")) != EOF)

    {

        switch(c)

        {

        case 'd':

        Gdevice = optarg;

        break;

            case 'f':

                Gsynflood = atoi(optarg);

                break;

        case 'h':

        usage();

        exit(0);

        case 'i':

        Gicmplimit = atoi(optarg);

        break;

        case 'm':

        if(strcmp(optarg, "all") == 0)

            Gwatchlevel = HUMANITARIAN;

        else if(strcmp(optarg, "subnet") == 0)

            Gwatchlevel = MYSUBNET;

        else

        {

            usage();

            exit(-1);

        }

        break;

        case 'p':

        Gportlimit = atoi(optarg);

        break;

        case 'r':

        if(strcmp(optarg, "dos") == 0)

            Greportlevel = REPORTDOS;

        else if(strcmp(optarg, "scan") == 0)

            Greportlevel = REPORTSCAN;

        else

        {

            exit(-1);

        }

        break;

        case 't':

                Gtimer = atoi(optarg);

                break;

        case 'w':

        Gwebcount = atoi(optarg);

        break;

        default:

                usage();

                exit(-1);

        }

    }

}

/**********************************************************************

Function: usage

Purpose:  Display the usage of the program

**********************************************************************/

void usage()

{

printf("Usage: %s [options]\n", Gprogramname);

printf("  -d device       Use 'device' as the network interface device\n");

printf("                  The first non-loopback interface is the default\n");

printf("  -f flood        Assume a synflood attack occurred if more than\n");

printf("                  'flood' uncompleted connections are received\n");

printf("  -h              A little help here\n");

printf("  -i icmplimit    Assume we may be part of a smurf attack if more\n");

printf("                  than icmplimit ICMP ECHO REPLIES are seen\n");

printf("  -m level        Monitor more than just our own host.\n");

printf("                  A level of 'subnet' watches all addresses in our\n");

printf("                  subnet and 'all' watches all addresses\n");

printf("  -p portlimit    Logs a portscan alert if packets are received for\n");

printf("                  more than portlimit ports in the timeout period.\n");

printf("  -r reporttype   If reporttype is dos, only Denial Of Service\n");

printf("                  attacks are reported.  If reporttype is scan\n");

printf("                  then only scanners are reported.  Everything is\n");

printf("                  reported by default.\n");

printf("  -t timeout      Count packets and print potential attacks every\n");

printf("                  timeout seconds\n");

printf("  -w webcount     Assume we are being portscanned if more than\n");

printf("                  webcount packets are received from port 80\n");

}

/**********************************************************************

Function: buildnet

Purpose:  Setup for monitoring of our host or entire subnet.

**********************************************************************/

void buildnet()

{

    u_long addr;

    u_char *p;

    int i;

    if(Gwatchlevel == MYSELFONLY)        /* Just care about me */

    {

    (void) addtarget(Gmaddr);

    }

    else if(Gwatchlevel == MYSUBNET)        /* Friends and neighbors */

    {

    addr = htonl(Gmaddr);

    addr = addr & 0xffffff00;

    for(i = 0; i < 256; i++)

        (void) addtarget(ntohl(addr + i));

    }

}

/**********************************************************************

Function: doicare

Purpose:  See if we monitor this address

**********************************************************************/

struct scaninfo *doicare(addr)

u_long addr;

{

    struct scaninfo *si;

    int i;

    for(si = Gsilist; si; si = si->next)

    {

    if(si->addr == addr)

        return(si);

    }

    if(Gwatchlevel == HUMANITARIAN)    /* Add a new address, we always care */

    {

    si = addtarget(addr);

    return(si);

    }

    return(NULL);

}

/**********************************************************************

Function: addtarget

Purpose:  Adds a new IP address to the list of hosts to watch.

**********************************************************************/

struct scaninfo *addtarget(addr)

u_long addr;

{

    struct scaninfo *si;

    if((si = (struct scaninfo *)malloc(sizeof(struct scaninfo))) == NULL)

    {

    perror("malloc scaninfo");

    exit(-1);

    }

    memset(si, 0, sizeof(struct scaninfo));

    si->addr = addr;

    si->next = Gsilist;

    Gsilist = si;

    return(si);

}

/**********************************************************************

Function: process_packet

Purpose:  Process raw packet and figure out what we need to to with it.

Pulls the packet apart and stores key data in global areas for reference

by other functions.

**********************************************************************/

void process_packet(pkt, pktlen)

u_char *pkt;

int pktlen;

{

    struct ethhdr *ep;

    struct iphdr *ip;

    static struct align { struct iphdr ip; char buf[PKTLEN]; } a1;

    u_short off;

    Gtimein = time((time_t *)0);

    ep = (struct ethhdr *) pkt;

    if(ntohs(ep->h_proto) != ETH_P_IP)

    return;

    pkt += sizeof(struct ethhdr);

    pktlen -= sizeof(struct ethhdr);

    memcpy(&a1, pkt, pktlen);

    ip = &a1.ip;

    Gsaddr = ip->saddr;

    Gdaddr = ip->daddr;

    if((Gsi = doicare(Gdaddr)) == NULL)

    return;

    off = ntohs(ip->frag_off);

    Gisfrag = (off & IP_MF);    /* Set if packet is fragmented */

    Giplen = ntohs(ip->tot_len);

    Gid = ntohs(ip->id);

    pkt = (u_char *)ip + (ip->ihl << 2);

    Giplen -= (ip->ihl << 2);

    switch(ip->protocol)

    {

    case IPPROTO_TCP:

        do_tcp(ep, pkt);

        break;

    case IPPROTO_UDP:

        do_udp(ep, pkt);

        break;

    case IPPROTO_ICMP:

        do_icmp(ep, pkt);

        break;

    default:

        break;

    }

}

/**********************************************************************

Function: do_tcp

Purpose:  Process this TCP packet if it is important.

**********************************************************************/

void do_tcp(ep, pkt)

struct ethhdr *ep;

u_char *pkt;

{

    struct tcphdr *thdr;

    u_short sport, dport;

    thdr = (struct tcphdr *) pkt;

    if(thdr->th_flags & TH_RST) /* RST generates no response */

    return;            /* Therefore can't be used to scan. */

    sport = ntohs(thdr->th_sport);

    dport = ntohs(thdr->th_dport);

    if(thdr->th_flags & TH_SYN)

    {

    if(Gsaddr == Gdaddr && sport == dport)

    {

        Gsi->land.atktime = Gtimein;

        Gsi->land.saddr = Gsaddr;

        memcpy(Gsi->land.eaddr, ep->h_source, ETH_ALEN);

    }

    }

    addtcp(sport, dport, thdr->th_flags, ep->h_source);

}

/**********************************************************************

Function: addtcp

Purpose:  Add this TCP packet to our list.

**********************************************************************/

void addtcp(sport, dport, flags, eaddr)

u_short sport;

u_short dport;

u_char flags;

u_char *eaddr;

{

    struct pktin *pi, *last, *tpi;

    /* See if this packet relates to other packets already received. */

    for(pi = Gsi->tcpin; pi; pi = pi->next)

    {

    if(pi->saddr == Gsaddr && pi->dport == dport)

    {

        if(flags == TH_SYN)

        addfloodinfo(pi, sport);

        else if((flags & TH_FIN) || (flags & TH_ACK))

        rmfloodinfo(pi, sport);

        return;

    }

    last = pi;

    }

    /* Must be new entry */

    if((tpi = (struct pktin *)malloc(sizeof(struct pktin))) == NULL)

    {

    perror("Malloc");

    exit(-1);

    }

    memset(tpi, 0, sizeof(struct pktin));

    memcpy(tpi->eaddr, eaddr, ETH_ALEN);

    tpi->saddr = Gsaddr;

    tpi->sport = sport;

    tpi->dport = dport;

    tpi->timein = Gtimein;

    if(flags == TH_SYN)

    addfloodinfo(tpi, sport);

    if(Gsi->tcpin)

    last->next = tpi;

    else

    Gsi->tcpin = tpi;

}

/**********************************************************************

Function: addfloodinfo

Purpose:  Add floodinfo information

**********************************************************************/

void addfloodinfo(pi, sport)

struct pktin *pi;

u_short sport;

{

    struct floodinfo *fi;

    fi = (struct floodinfo *)malloc(sizeof(struct floodinfo));

    if(fi == NULL)

    {

        perror("Malloc of floodinfo");

        exit(-1);

    }

    memset(fi, 0, sizeof(struct floodinfo));

    fi->sport = sport;

    fi->next = pi->fi;

    pi->fi = fi;

}

/**********************************************************************

Function: rmfloodinfo

Purpose:  Removes floodinfo information

**********************************************************************/

void rmfloodinfo(pi, sport)

struct pktin *pi;

u_short sport;

{

    struct floodinfo *fi, *prev = NULL;

    for(fi = pi->fi; fi; fi = fi->next)

    {

    if(fi->sport == sport)

        break;

    prev = fi;

    }

    if(fi == NULL)

    return;

    if(prev == NULL)    /* First element */

    pi->fi = fi->next;

    else

    prev->next = fi->next;

    free(fi);

}

/**********************************************************************

Function: do_udp

Purpose:  Process this udp packet.

Currently teardrop and all its derivitives put 242 in the IP id field.

This could obviously be changed.  The truly paranoid might want to flag all

fragmented UDP packets.  The truly adventurous might enhance the code to

track fragments and check them for overlaping boundaries.

**********************************************************************/

void do_udp(ep, pkt)

struct ethhdr *ep;

u_char *pkt;

{

    struct udphdr *uhdr;

    u_short sport, dport;

    uhdr = (struct udphdr *) pkt;

    if(Gid == 242 && Gisfrag)    /* probable teardrop */

    {

    Gsi->teardrop.saddr = Gsaddr;

    memcpy(Gsi->teardrop.eaddr, ep->h_source, ETH_ALEN);

    Gsi->teardrop.atktime = Gtimein;

    }

    sport = ntohs(uhdr->source);

    dport = ntohs(uhdr->dest);

    addudp(sport, dport, ep->h_source);

}

/**********************************************************************

Function: addudp

Purpose:  Add this udp packet to our list.

**********************************************************************/

void addudp(sport, dport, eaddr)

u_short sport;

u_short dport;

u_char *eaddr;

{

    struct pktin *pi, *last, *tpi;

    for(pi = Gsi->udpin; pi; pi = pi->next)

    {

    if(pi->saddr == Gsaddr && pi->dport == dport)

    {

        pi->timein = Gtimein;

        return;

    }

    last = pi;

    }

    /* Must be new entry */

    if((tpi = (struct pktin *)malloc(sizeof(struct pktin))) == NULL)

    {

    perror("Malloc");

    exit(-1);

    }

    memset(tpi, 0, sizeof(struct pktin));

    memcpy(tpi->eaddr, eaddr, ETH_ALEN);

    tpi->saddr = Gsaddr;

    tpi->sport = sport;

    tpi->dport = dport;

    tpi->timein = Gtimein;

    if(Gsi->udpin)

    last->next = tpi;

    else

    Gsi->udpin = tpi;

}

/**********************************************************************

Function: do_icmp

Purpose:  Process an ICMP packet.

We assume there is no valid reason to receive a fragmented ICMP packet.

**********************************************************************/

void do_icmp(ep, pkt)

struct ethhdr *ep;

u_char *pkt;

{

    struct icmphdr *icmp;

    icmp = (struct icmphdr *) pkt;

    if(Gisfrag)    /* probable ICMP attack (i.e. Ping of Death) */

    {

    Gsi->icmpfrag.saddr = Gsaddr;

    memcpy(Gsi->icmpfrag.eaddr, ep->h_source, ETH_ALEN);

    Gsi->icmpfrag.atktime = Gtimein;

    }

    if(icmp->type == ICMP_ECHOREPLY)

    Gsi->icmpcnt++;

    return;

}

/**********************************************************************

Function: clear_pkt

Purpose:  Delete and free space for any old packets.

**********************************************************************/

void clear_pktin(si)

struct scaninfo *si;

{

    struct pktin *pi;

    struct floodinfo *fi, *tfi;

    time_t t, t2;

    t = time((time_t *)0);

    while(si->tcpin)

    {

    t2 = t - si->tcpin->timein;

    if(t2 > Gtimer)

    {

        pi = si->tcpin;

        fi = pi->fi;

        while(fi)

        {

        tfi = fi;

        fi = fi->next;

        free(tfi);

        }

        si->tcpin = pi->next;

        free(pi);

    }

    else

        break;

    }

    while(si->udpin)

    {

    t2 = t - si->udpin->timein;

    if(t2 > Gtimer)

    {

        pi = si->udpin;

        si->udpin = pi->next;

        free(pi);

    }

    else

        break;

    }

}

/**********************************************************************

Function: print_info

Purpose:  Print out any alerts.

**********************************************************************/

void print_info()

{

    struct pktin *pi;

    struct addrlist *tcplist = NULL, *udplist = NULL, *al;

    struct floodinfo *fi;

    char buf[1024], *eaddr, abuf[32];

    int i;

    strcpy(abuf, anetaddr(Gsi->addr));

    if(Greportlevel == REPORTALL || Greportlevel == REPORTDOS)

    {

        if(Gsi->teardrop.atktime)

        {

        eaddr = ether_ntoa(Gsi->teardrop.eaddr);

        sprintf(buf, "Possible teardrop attack from %s (%s) against %s",

            anetaddr(Gsi->teardrop), eaddr, abuf);

        syslog(LOG_ALERT, buf);

        memset(&Gsi->teardrop, 0, sizeof(struct atk));

        }

        if(Gsi->land.atktime)

        {

        eaddr = ether_ntoa(Gsi->land.eaddr);

        sprintf(buf, "Possible land attack from (%s) against %s",

            eaddr, abuf);

        syslog(LOG_ALERT, buf);

        memset(&Gsi->land, 0, sizeof(struct atk));

        }

        if(Gsi->icmpfrag.atktime)

        {

        eaddr = ether_ntoa(Gsi->icmpfrag.eaddr);

        sprintf(buf, "ICMP fragment detected from %s (%s) against %s",

            anetaddr(Gsi->icmpfrag), eaddr, abuf);

        syslog(LOG_ALERT, buf);

        memset(&Gsi->icmpfrag, 0, sizeof(struct atk));

        }

        if(Gsi->icmpcnt > Gicmplimit)

        {

        sprintf(buf, "ICMP ECHO threshold exceeded, smurfs up.  I saw %d packets\n", Gsi->icmpcnt);

        syslog(LOG_ALERT, buf);

        Gsi->icmpcnt = 0;

        }

    

    }

    for(pi = Gsi->tcpin; pi; pi = pi->next)

    {

    i = 0;

    for(fi = pi->fi; fi; fi = fi->next)

        i++;

        

    if(Greportlevel == REPORTALL || Greportlevel == REPORTDOS)

    {

        if(i > Gsynflood)

        {

            eaddr = ether_ntoa(pi->eaddr);

            sprintf(buf, "Possible SYNFLOOD from %s (%s), against %s.  I saw %d packets\n",

            anetaddr(pi->saddr), eaddr, abuf, i);

            syslog(LOG_ALERT, buf);

        }

    }

    for(al = tcplist; al; al = al->next)

    {

        if(pi->saddr == al->saddr)

        {

        al->cnt++;

        if(pi->sport == 80)

            al->wwwcnt++;

        break;

        }

    }

    if(al == NULL)    /* new address */

    {

        al = (struct addrlist *)malloc(sizeof(struct addrlist));

        if(al == NULL)

        {

        perror("Malloc address list");

        exit(-1);

        }

        memset(al, 0, sizeof(struct addrlist));

        al->saddr = pi->saddr;

        al->cnt = 1;

        if(pi->sport == 80)

        al->wwwcnt = 1;

        al->next = tcplist;

        tcplist = al;

        }

    }

    if(Greportlevel == REPORTALL || Greportlevel == REPORTSCAN)

    {

        for(al = tcplist; al; al = al->next)

        {

        if((al->cnt - al->wwwcnt) > Gportlimit || al->wwwcnt > Gwebcount)

        {

            sprintf(buf, "Possible TCP port scan from %s (%d ports) against %s\n",

            anetaddr(al->saddr), al->cnt, abuf);

            syslog(LOG_ALERT, buf);

        }

        }

        for(pi = Gsi->udpin; pi; pi = pi->next)

        {

        for(al = udplist; al; al = al->next)

        {

            if(pi->saddr == al->saddr)

            {

            al->cnt++;

            break;

            }

        }

        if(al == NULL)    /* new address */

        {

            al = (struct addrlist *)malloc(sizeof(struct addrlist));

            if(al == NULL)

            {

            perror("Malloc address list");

            exit(-1);

            }

            memset(al, 0, sizeof(struct addrlist));

            al->saddr = pi->saddr;

            al->cnt = 1;

            al->next = udplist;

            udplist = al;

        }

        }

        for(al = udplist; al; al = al->next)

        {

        if(al->cnt > Gportlimit)

        {

            sprintf(buf, "Possible UDP port scan from %s (%d ports) against %s\n",

            anetaddr(al->saddr), al->cnt, abuf);

            syslog(LOG_ALERT, buf);

        }

        }

    }

    while(tcplist)

    {

    al = tcplist->next;

    free(tcplist);

    tcplist = al;

    }

    while(udplist)

    {

    al = udplist->next;

    free(udplist);

    udplist = al;

    }

}

/************************************************************************

Function:  anetaddr

Description:

Another version of the intoa function.

************************************************************************/

char *anetaddr(addr)

u_long addr;

{

    u_long naddr;

    static char buf[16];

    u_char b[4];

    int i;

    naddr = ntohl(addr);

    for(i = 3; i >= 0; i--)

    {

        b[i] = (u_char) (naddr & 0xff);

        naddr >>= 8;

    }

    sprintf(buf, "%d.%d.%d.%d", b[0], b[1], b[2], b[3]);

    return(buf);

}

/************************************************************************

Function:  initdevice

Description: Set up the network device so we can read it.

**************************************************************************/

initdevice(fd_flags, dflags)

int fd_flags;

u_long dflags;

{

    struct ifreq ifr;

    int fd, flags = 0;

    if((fd = socket(PF_INET, SOCK_PACKET, htons(0x0003))) < 0)

    {

    perror("Cannot open device socket");

    exit(-1);

    }

    /* Get the existing interface flags */

    strcpy(ifr.ifr_name, Gdevice);

    if(ioctl(fd, SIOCGIFFLAGS, &ifr) < 0)

    {

    perror("Cannot get interface flags");

    exit(-1);

    }

    ifr.ifr_flags |= IFF_PROMISC;

    if(ioctl(fd, SIOCSIFFLAGS,  &ifr) < 0)

    {

    perror("Cannot set interface flags");

    exit(-1);

    }

    

    return(fd);

}

/************************************************************************

Function:  readdevice

Description: Read a packet from the device.

**************************************************************************/

u_char *readdevice(fd, pktlen)

int fd;

int *pktlen;

{

    int cc = 0, from_len, readmore = 1;

    struct sockaddr from;

    static u_char pktbuffer[PKTLEN];

    u_char *cp;

    while(readmore)

    {

    from_len = sizeof(from);

    if((cc = recvfrom(fd, pktbuffer, PKTLEN, 0, &from, &from_len)) < 0)

    {

        if(errno != EWOULDBLOCK)

        return(NULL);

    }

    if(strcmp(Gdevice, from.sa_data) == 0)

        readmore = 0;

    }

    *pktlen = cc;

    return(pktbuffer);

}

/*************************************************************************

Function: ether_ntoa 

Description:

Translates a MAC address into ascii.  This function emulates

the ether_ntoa function that exists on Sun and Solaris, but not on Linux.

It could probably (almost certainly) be more efficent, but it will do.

*************************************************************************/

char *ether_ntoa(etheraddr)

u_char etheraddr[ETH_ALEN];

{

    int i, j;

    static char eout[32];

    char tbuf[10];

    for(i = 0, j = 0; i < 5; i++)

    {

    eout[j++] = etheraddr[i] >> 4;

    eout[j++] = etheraddr[i] & 0xF;

    eout[j++] = ':';

    }

    eout[j++] = etheraddr[i] >> 4;

    eout[j++] = etheraddr[i] & 0xF;

    eout[j++] = '\0';

    for(i = 0; i < 17; i++)

    {

    if(eout[i] < 10)

        eout[i] += 0x30;

    else if(eout[i] < 16)

        eout[i] += 0x57;

    }

    return(eout);

}

/*至少要加入一个linux/sockios.h的头文件――在我的linux box中，我

  还改了netinet/tcp.h ,它才肯跑……:(      *********************/
