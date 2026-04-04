---
title: "The Solaris Security FAQ"
date: 2000-08-10T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-67"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

The Solaris Security FAQ 

Answer all your Solaris Security questions here 

Summary

The job of tracking all the security information surrounding Solaris 2 is a difficult one. There's general information about securing Solaris, patches to know about, tools to use, many sources of security information, and specific needs if you're trying to secure a Solaris Web server. Well your job has just been made much easier. The Solaris Security FAQ has all this and more. 


--------------------------------------------------------------------------------


Maintained by Peter Baer Galvin 


The following is a list of questions that are frequently asked about Solaris 2.x Security. You can help make it an even better-quality FAQ by writing a contribution or update and sending it BY E-MAIL ONLY. 


Changes to this document will be indicated in the index by a "+" for new entries and a "*" for changed entries. 


1. GENERAL 

* 1.1) How secure is solaris 2? 

* 1.2) What version of Solaris should I run? 

1.3) Can I just install a machine and ignore it? 


2. How can I configure Solaris to make it more secure? 

2.1) What file permissions should I change? 

2.2) How should I change root user configuration? 

2.3) How should I change startup files? 

2.4) How can I disable network root logins? 

2.5) How do I disable rlogin/rsh access? 

2.6) What accounts are unnecessary? 

* 2.7) How do I protect devices? 

2.8) What permissions should I change in /etc? 

2.9) Why do Solaris machines act as routers? 

2.10) How do I disable automounter? 

2.11) How to I disable NFS service? 

2.12) Do I need to worry about cron jobs? 

2.13) Are there any risks to using dynamic routes? 

2.14) When and how should I use static ARP? 

2.15) Is it unsecure to run rpcbind? 

2.16) What permission bits should be set on /etc/utmp? 

2.17) What programs can be un-suid'ed? 

2.18) What system facilities can I disable? 

2.19) Should I run in.fingerd? 

2.20) Can syslog be made to be more effective? 

2.21) How can the EEPROM make a system more secure? 

2.22) Is my machine being "promiscuous"? 

2.23) If I need to use NFS, how can I make it more secure? 

2.24) How can I secure sendmail 

2.25) Is NIS secure, and how can it be made more secure? 

2.26) What is needed for secure anonymous ftp service? 

2.27) How can X be made more secure? 

2.28) How do I turn on SUN-DES-1 authentication? 

* 2.29) What patches should I install? 

+ 2.30) How can I prevent code from executing in the stack? 

3. What programs should I replace or add? 

3.1) inetd? 

* 3.2) ifstatus? 

* 3.3) xntp 

* 3.4) sendmail? 

3.5) rpcbind? 

* 3.6) Password checking programs? 

3.7) crack? 

3.8) ftp? 

3.9) fix_modes? 

3.10) noshell? 

3.11) bind? 

3.12) netcat? 

4. What other useful resources should I know about? 

4.1) Sun mailing-lists? 

4.2) Sun patches? 

4.3) Other Solaris FAQs? 

4.4) Useful newsgroups? 

4.5) Useful mailing-lists? 

* 4.6) Useful columns? 

* 4.7) Useful Web sites? 

5. How can I make my Solaris Web server more secure? 

5.0) Overview 

5.1) Step 0 - Web server security checklist 

5.1) Step 1 - Hardware Setup 

5.2) Step 2 - Install the OS 

5.3) Step 3 - Strip down the OS 

5.4) Step 4 - Install third-party software 

5.5) Step 5 - Limit network access to the system 

5.6) Step 6 - Configure S/Key 

5.7) Step 7 - Configure wu-ftp 

5.8) Step 8 - Limit access to files and file systems 

5.9) Step 9 - Test the configuration 

5.10) Step 10 - Other suggestions 

6. ACKNOWLEDGEMENTS 

1) General 

1.1) How secure is Solaris 2? 


Solaris 2 is relatively secure, considering that it is a general-purpose, time-sharing, multi-user operating system. Such systems are inherently full of compromises. Solaris 2 is a version of Unix which was not designed for security. However, Sun actively fixes security holes. Additionally, there are facilities that can increase the security of Solaris (see section 3). 


Specifically, Solaris has been designed to meet the TCSEC (Orange Book C2) level for security. According to Sun, Solaris 2.4SE is ITSEC E2/F-C2-certified. Solaris 2.6 is currently undergoing both the ITSEC E3/F-C2 and TCSEC C2 certification processes. Current information can be found at [http://www.sun.com/solaris/2.6/ds-security.html](http://www.sun.com/solaris/2.6/ds-security.html). 


In order to build a system that actually meets the evaluation there are a number of patches that must be installed. A bundle of the exact patches used for the evaluation can be obtained directly from Sun. 


For those that need more security than provided by C2 Sun provides a version of Solaris that meets was designed to meet the TCSEC CMW (Compartmented Mode Workstation) level, which exceeds B1. 


Trusted Solaris 1.2    F-B1/E3        (Based on SunOS 4.1.3_U1)

Trusted Solaris 2.5.1    F-B1/E3        (Based on Solaris 2.5.1 11/97)


1.2) What version of Solaris should I run? 


Where security is concerned? Each subsequent release of Solaris has been an improvement over its predecessor. Solaris 2.7 is currently the latest release, and also the most secure. 


1.3) Can I just install a machine and ignore it? 


Most installed machines suffer from entropy: They lack a current OS release, and up-to-date patches and tools. It's important to install the latest patches, at the least, to be sure that all known security holes are filled. 


2) How can I configure Solaris to make it more secure? 


2.1) What file permissions should I change? 


The program fix-modes runs on Solaris 2.4 and 2.5 and changes system file and directory permissions. The new permissions make it harder for non-root users to become root, and for non-root users to modify system files. 


2.2) How should I change root user configuration? 


Be sure root has a umask setting of 077 or 027. 


Be sure root has a safe search path, as in /usr/bin:/sbin:/usr/sbin 


2.3) How should I change startup files? 


Generally, examine all "S" files in /etc/rc2.d and /etc/rc3.d. Any files that start unneeded facilities should be renamed (be sure the new names don't start with "S"). Test all boot files changes by rebooting, examining /var/adm/messages, and checking for extraneous processes in ps -elf output. 


2.4) How can I disable network root logins? 


Make sure the to enable the "CONSOLE" line in /etc/default/login. To disable use of ftp by root, add "root" to /etc/ftpusers. 


2.5) How do I disable rlogin/rsh access? 


Remove /etc/hosts.equiv, /.rhosts, and all of the "r" commands from /etc/inetd.conf Do a kill -HUP of the inetd process. 


2.6) What accounts are unnecessary? 


Remove, lock, or comment out unnecessary accounts, including "sys", "uucp", "nuucp", and "listen". The cleanest way to shut them down is to put "NP" in the password field of the /etc/shadow file. Also consider using the noshell program to log attempts to use secured accounts. 


2.7) How to I protect devices? 


The file /etc/logindevperm contains configuration information to tell the system the permissions to set on devices associated with login (console, keyboard, etc). Check the values in this file and modify them to give different permissions. 


For removable media the BSM subsystem provides the allocate and deallocate commands that ensure that only a single user can access removable media (such as tapes) at any one time. 


2.8) What permissions should I change in /etc? 


No file in /etc needs to be group writeable. Remove group write permission via the command chmod -R g-w /etc 


2.9) Why do Solaris machines act as routers? 


By default, if a Solaris machine has more than one network interface, Solaris will route packets between the multiple interfaces. This behavior is controlled by /etc/init.d/inetinit. To turn of routing on a Solaris 2.4 (or lesser) machine, add ndd -set /dev/ip ip_forwarding 0 at the end of /etc/init.d/inetinit. For Solaris 2.5, simply touch /etc/notrouter. Be aware that there is a small window of vulnerability during startup when the machine may route, before the routing is turned off. 


2.10) How do I disable automounter? 


Automounter is controlled by the /etc/auto_* configuration files. To disable automounter, remove those files, and/or disable the /etc/rc2.d/S74autofs. 


2.11) How to I disable NFS service? 


NFS exports are controlled by the /etc/dfs/dfstab file. Remove this file. To disable the NFS server daemon, rename /etc/rc3.d/S15nfs.server. To prevent a machine from being an NFS client, rename /etc/rc2.d/S73nfs.client. When renaming startup files, be sure to name them with a starting letter other than "S". 


2.12) Do I need to worry about cron jobs? 


Review all the cron jobs by reading the cron file of every system account in /var/spool/cron/crontabs. Consider logging all cron activities by setting "CRONLOG=yes" in /etc/default/cron. 


2.13) Are there any risks to using dynamic routes? 


Machines using a dynamic route-receiving daemon like in.routed and in.rdisc are vulnerable to receiving incorrect routes. These routes can disable some or all connectivity to other networks. When possible, use static routes (routes added via the route commands in startup files, rather than the routing daemons. 


2.14) When and how should I use static ARP? 


ARP is the protocol used to associate IP and Ethernet addresses. Machines that share a wire (and have no routers between them) know each others ARP addresses. If one machine is replaced with another, the ARP addresses are usually different. By default, Solaris machines dynamically determine ARP addresses. The arp command can be used to statically set ARP table entries and flush all other entries. This facility is best used when there are few, unchanging systems on a network and the machines need to be assured of each other's identities. 


2.15) Is it unsecure to run rpcbind? 


rpcbind is the program that allows rpc callers and rpc service provides to find each other. Unfortunately, standard rpc is unsecure. It uses "AUTH_UNIX" authentication, which means it depends on the remote system's IP address and the remote user's UID for identification. Both of these forms of identification can be easily forged or changed. General-purpose systems usually need rpc running to keep users happy. Special purpose systems (Web servers, ftp servers, mail servers, etc) can usually have rpc disabled. Be sure to test all the facilities that you depend on to be sure they aren't affected if you turn off rpc. To disable rpc, rename /etc/rc2.d/S71RPC. 


2.16) What permission bits should be set on /etc/utmp? 


/etc/utmp can be set to mode 644 without disrupting any service. 


2.17) What programs can be un-suid'ed? 


Many of the setuid and setgid programs on Solaris are used only by root, or by the user or group-id to which they are set. They can have setuid and setgid removed without diminishing user's abilities to get their work done. Consider each of these programs individually as to their use on your system. This is an example list of setuid programs taken from a Solaris 2.6 system: 


# find / -perm -4000 -print

/usr/lib/lp/bin/netpr

/usr/lib/fs/ufs/quota

/usr/lib/fs/ufs/ufsdump

/usr/lib/fs/ufs/ufsrestore

/usr/lib/fs/vxfs/vxdump

/usr/lib/fs/vxfs/vxquota

/usr/lib/fs/vxfs/vxrestore

/usr/lib/exrecover

/usr/lib/pt_chmod

/usr/lib/sendmail

/usr/lib/utmp_update

/usr/lib/acct/accton

/usr/lib/uucp/remote.unknown

/usr/lib/uucp/uucico

/usr/lib/uucp/uusched

/usr/lib/uucp/uuxqt

/usr/lib/sendmail.orig

/usr/openwin/lib/mkcookie

/usr/openwin/bin/xlock

/usr/openwin/bin/ff.core

/usr/openwin/bin/kcms_configure

/usr/openwin/bin/kcms_calibrate

/usr/openwin/bin/sys-suspend

/usr/dt/bin/dtaction

/usr/dt/bin/dtappgather

/usr/dt/bin/sdtcm_convert

/usr/dt/bin/dtprintinfo

/usr/dt/bin/dtsession

/usr/bin/at

/usr/bin/atq

/usr/bin/atrm

/usr/bin/crontab

/usr/bin/eject

/usr/bin/fdformat

/usr/bin/login

/usr/bin/newgrp

/usr/bin/passwd

/usr/bin/ps

/usr/bin/rcp

/usr/bin/rdist

/usr/bin/rlogin

/usr/bin/rsh

/usr/bin/su

/usr/bin/tip

/usr/bin/uptime

/usr/bin/w

/usr/bin/yppasswd

/usr/bin/admintool

/usr/bin/ct

/usr/bin/cu

/usr/bin/uucp

/usr/bin/uuglist

/usr/bin/uuname

/usr/bin/uustat

/usr/bin/uux

/usr/bin/chkey

/usr/bin/nispasswd

/usr/bin/cancel

/usr/bin/lp

/usr/bin/lpset

/usr/bin/lpstat

/usr/bin/volcheck

/usr/bin/volrmmount

/usr/bin/pppconn

/usr/bin/pppdisc

/usr/bin/ppptool

/usr/sbin/allocate

/usr/sbin/mkdevalloc

/usr/sbin/mkdevmaps

/usr/sbin/ping

/usr/sbin/sacadm

/usr/sbin/whodo

/usr/sbin/deallocate

/usr/sbin/list_devices

/usr/sbin/m64config

/usr/sbin/lpmove

/usr/sbin/pmconfig

/usr/sbin/static/rcp

/usr/sbin/vxprint

/usr/sbin/vxmkcdev

/usr/ucb/ps

/usr/vmsys/bin/chkperm

/etc/lp/alerts/printer


Create a master list of the remaining setuid/setgid programs on your system and check that the list remains static over time. 


2.18) What system facilities can I disable? 


Every network on the system should be inspected to determine if the facility that it provides is appropriate for your environment. If not, disable the facility. Some of these facilities are in the system startup files, as discussed in section 2. Other are started in /etc/inetd.conf. Comment out the unneeded facilities and kill -HUP the inetd daemon. Some common facilities are: 


tftp         systat        rexd    ypupdated    netstat

rstatd         rusersd        sprayd    walld           exec

comsat         rquotad        name    uucp


For a very secure system, replace the standard inetd.conf with one that just includes telnet and ftp (if you need those facilities). 


2.19) Should I run in.fingerd? 


in.fingerd has had some security problems in the past. If you want to provide the finger facility, run it as "nobody", not as "root". 


2.20) Can syslog be made to be more effective? 


By default, syslog provides minimal system logging. Modify the /etc/syslog.conf file to have syslog log more information, and separate to where the information is logged by importance. Anything related to security should be sent to a file that gets encrypted. Unfortunately, syslog must be restarted for it to read the new configuration file. 


More login logging can be enabled by creating the "loginlog" file: 


touch /var/adm/loginlog

chmod 600 /var/adm/loginlog

chgrp sys /var/adm/loginlog


2.21) How can the EEPROM make a system more secure? 


Set the EEPROM security mode to command via "ok setenv security-mode=command" to password-protect all EEPROM commands except "boot" and "continue". Set the EEPROM's password so no one else can change its modes. Unfortunately, this doesn't truly secure the machine. If someone has physical access to the machine, they can open the machine and replace its EEPROM. Replacing the machine's EEPROM also changes its hostid. Recording all the hostids of your machines and checking this list against the machines occasionally to verify that no EEPROMs have been replaced. 


2.22) Is my machine being "promiscuous"? 


Under Solaris, there is no way to determine if a machine's network interfaces are in "promiscuous" mode. Promiscuous mode allows the machine to see all network packets, rather than just those packets destined for the machine. This allows the machine to snoop the network and monitor all traffic. An interface should only be in promiscuous mode if the snoop program, or another network monitor program, is being run. If you aren't running such a program, and your machine's interface is in promiscuous mode, then it's likely that a hacker is monitoring your network. The public domain ifstatus command returns a machine's promiscuous state. (See section 3.) 


2.23) If I need to use NFS, how can I make it more secure ? 


Any filesystems listed in /etc/dfs/dfstab will be exported to the world, by default. Include a list of nfs clients (or a netgroup) with the "-o rw" or "-o ro" options. 

Include the "nosuid" option to disable setuid programs on that mount where applicable 

Don't run nfs mount through rpcbind - the mount daemon will see the request as being local and allow it. This is the source of known rpcbind vulnerabilities as reported by CERT (section 4). Use the rpcbind replacement (section 3) that disables request forwarding, or be sure have installed the latest Sun rpcbind patches which also disable forwarding. 

Use secure-RPC if possible. If not, you're using "AUTH_UNIX" authentication, which simply depends on the IP address of the client for identification. Any machine using the IP address of the ones in your access list can gain access to NFS. 

Disable NFS if possible. NFS traffic flows in clear-text (even when using "AUTH_DES" or "AUTH_KERB" for authentication) so any files transported via NFS are susceptible to snooping. 

Programs can guess the file handle of the root mount point and get any file from an NFS server, regardless of any access rights. Use fsirand to randomize inode numbers on NFS servers. 

2.24) How can I secure sendmail 


With Solaris 2.5, Sun is shipping a much more modern sendmail. Still, there are new bugs reported monthly. How can sendmail be made more secure? 


Consider running the latest version Berkeley sendmail (see section 3) 

Consider using smrsh (section 3) 

Remove "decode" from /etc/aliases 

Set /etc/aliases permissions to 644 

Consider using a proxy-based firewall with SMTP filtering to screen out unnecessary SMTP commands. 

2.25) Is NIS secure, and how can it be made more secure? 


NIS is not a secure distributed name service. NIS+ is more secure when configured properly. NIS will give away all the information in its tables if its domain name is guessable. To close this hole, put trusted host/net addresses to /var/yp/securenets. Also consider using secure RPC or NIS+. Finally, don't include root and other system account information in NIS tables. 


2.26) What is needed for secure anonymous ftp service? 


Solaris 2.5 ftpd(1M) contains a good set of configuration directions, with the following exceptions: 


cp /etc/nsswitch.conf ~ftp/etc 

Make sure that the filesystem containing ~ftp is not mounted with the "nosuid" option 

No files under ~ftp should be owned by "ftp" 

More detailed instructions can be found the anonymous ftp directions (section 4). 

2.27) How can X be made more secure? 


Use the SUN-DES-1 option to use Secure RPC to pass X authentication/authorization information. 

Use xhost +user@host when granting access 

2.28) How do I turn on SUN-DES-1 authentication? 


set DisplayManager*authorize: true 

set DisplayManager._0.authName: SUN-DES-1 

rm ~/.Xauthority 

add access permission for local host via xauth local/unix:0 SUN-DES-1 unix.local@nisdomain and xauth local:0 SUN-DES-1 unix.local@nisdomain 

Start X via xinit -- -auth ~/.Xauthority 

Add yourself and remove all others via xhost +user@ +unix.local@nisdomain -local -localhost 

Now, to give user "foo" permission to access host "node": 


Give "foo" permission on "node" via xhost +foo@ 

Create appropriate xauthority for "foo" via xauth add node:0 SUN-DES-1 unix.node@nisdomain 

"foo" can now connect to "node": xload -display node:0 

2.29) What patches should I install? 


Use showrev -p to list patches installed on the system. Check Sun's patch list (section 4) for current security-related patches for the version you are running. Download and install all pertinent security patches. Recheck the patch list frequently. Not all security patches need be installed on every machine. But protect machines, or those with public access, should be kept up-to-date. The patchdiag program that is available on the SunSolve CD and at the SunSolve Web site will automatically compare the patch level of a host against the current Sun recommended patch set, and display any differences. 


2.30) How can I prevent code from executing in the stack? 


There are a whole category of security holes that depend on one system flaw: the ability to execute code from the stack. These bugs overflow a buffer such that it writes into stack space. In that space they put code that they can then execute. In this way, the bug can execute arbitrary code on the target system. 


To secure your system against stack based buffer overflows, you can add the following to /etc/system: 


set noexec_user_stack=1

set noexec_user_stack_log =1


The first line will prevent execution on a stack. Care must be taken though, because there are some programs which legitimately try to run code off the stack. Those programs will crash if you implement this option. Generally, if the system is single purpose and needs to be secure (i.e. a Web server), you should use this option. The second line adds logging when someone does try to run an exploit. 


3) What programs should I replace or add? 


3.1) inetd? 


inetd can be replaced with [ftp://qiclab.scn.rain.com/pub/security/xinetd](ftp://qiclab.scn.rain.com/pub/security/xinetd)* to add logging facilities. (This program apparently has not been ported to Solaris.) 


3.2) ifstatus? 


ifstatus can determine if your network interfaces are in promiscuous mode. Apparently this program does not work on Solaris, however, because Solaris does not record the promiscuous state of its interfaces. 


3.3) xntp? 


xntp is a more secure version of ntp, the network time protocol. 


As from Solaris 2.6, Sun ships xntpd with the operating system. 


3.4) sendmail? 


The most recent (and usually most secure) version of sendmail is always available from Berkeley. Included in the sendmail package is smrsh, the "sendmail restricted shell" which can be used to control any programs invoked by sendmail. 


Warning: there are Sun specific modifcations that will be lost if you move to a plain Berkeley sendmail. Also, Sun sendmail patches have a tendency to replace Berkeley sendmail with Sun's sendmail. After installing patches, check that the sendmail version that you want to run is still in place. 


Sun is now shipping sendmail 8.9.1b with Solaris 7. 


3.5) rpcbind? 


rpcbind can be used to replace the standard rpcbind on Solaris machines. This version includes tcpwrapper-like functionality and disables forwarding of NFS requests through rpcbind. Sun's latest patches to rpcbind also solve this problem. 


3.6) Password checking programs? 


Unfortunately, passwd+ and npasswd are not yet released on Solaris. They are replacements for passwd that disallow "stupid" passwords from being used on Unix systems. 


A program similar to npasswd but for NIS only is available: [ftp://autoinst.acs.uci.edu/pub/uci-yppasswd](ftp://autoinst.acs.uci.edu/pub/uci-yppasswd) According to the author (Dan Stromberg), the code for checking for bad passwords is small, and would be easy to copy into other programs. 


From Solaris 2.6 onwards it is possible to augment or replace the authentication mechanism used by Solaris using the PAM facility. For more information see [http://www.sun.com/solaris/pam/](http://www.sun.com/solaris/pam/), [http://www.sun.com/software/events/presentations/ENP2.Lai/ENP2.Lai.html](http://www.sun.com/software/events/presentations/ENP2.Lai/ENP2.Lai.html), and Pete's Wicked World. 


It is easy to implement a PAM module to ensure that users do not use dictionary words, or to implement your other local rules. 


Using PAM there is no need to replace any components of the OS including passwd,login etc. 


3.7) crack? 


The crack program can be used to break "guessable" passwords in your /etc/shadow file. It uses a lot of compute cycles, but will generally tell you the passwords of 10% of your accounts the first time it is run. 


3.8) ftp? 


wu-ftp is a replacement for the standard ftpd daemon. It provides extensive logging and access control. 


3.9) fix_modes? 


fix-modes is a shell script that makes extensive changes to the file and directory permissions on standard Solaris machines. 


3.10) noshell? 


noshell is a program that can be used as the shell on accounts that are never supposed to be logged into. It logs the event (and prevents the login). (This program apparently has not been ported to Solaris.) 


3.11) bind? 


The standard bind on Solaris has known security problems (See CERT in section 4). This problems are patched over time, but the Solaris bind is generally behind the curve on patches. The current standard bind release is always available at ISC. 


3.12) netcat? 


NetCat is a tool that is useful for security managers and crackers alike. It is a flexible network connection creator, allowing for probes of arbitrary ports between arbitrary systems. 


4) What other useful resources should I know about? 


4.1) Sun mailing-list? 


Sun provides a security bulletin service via an e-mail list to subscribe send e-mail to mailto:security-alert@sun.com with a subject of "subscribe CWS your-mail-address". Old bulletins are available at [ftp://ftp.uu.net/systems/sun/sun-dist](ftp://ftp.uu.net/systems/sun/sun-dist). Phone: (415) 688-9081 


4.2) Sun patches? 


Sun security patches are available in two locations: [http://sunsolve1.sun.com/](http://sunsolve1.sun.com/) (for people with Sun contracts) `ftp://ftp.uu.net/systems/sun/sun-dist` (for people without Sun contracts) Or for an http interface use [http://sunsolve.Sun.COM/pub-cgi/patchpage.pl](http://sunsolve.sun.com/pub-cgi/patchpage.pl) 


4.3) Other Solaris FAQs? 


The excellent Solaris FAQ: [http://www.wins.uva.nl/pub/solaris/solaris2/](http://www.wins.uva.nl/pub/solaris/solaris2/) 


4.4) Useful newsgroups? 


All of the USENET newsgroups with "sun" in their name :-) 


comp.security.announce 


4.5) Useful mailing-lists? 


Sun maintains a "patch club" mailing list that includes details of Sun patch releases. Summaries are mailed weekly. The list also receives "EarlyNotifier Alerts" that contain important patch information. To change, add, or delete your e-mail address to the list send mail to: SunSolve-EarlyNotifier@Sun.COM 


If you want to be on one security mailing list, consider the best-of-security mailing list. Send subscription requests to best-of-security-request@suburbia.net, or for a digest form to best-of-security-d-request@suburbia.net. 


Many security problems are due to bugs in the operating system or applications. To keep up-to-date on bug happenings, subscribe to the Bugtraq mailing list. Bugtraq is a full-disclosure UNIX security mailing list, started by Scott Chasin . To subscribe to bugtraq, mailto:listserv@netspace.org containing the message body "subscribe bugtraq". An archive of the mailing list is available at [http://www.geek-girl.com/bugtraq/index.html](http://www.geek-girl.com/bugtraq/index.html). 


The Florida SunFlash is a "closed" mailing list for Sun owners. It contains mostly press releases from Sun and third-party vendors. To find out about a mail point in your area, or for other information send mail to infosunflash@Sun.COM Subscription requests should be sent to sunflash-request@Sun.COM Archives are on solar.nova.edu, ftp.uu.net, sunsite.unc.edu, src.doc.ic.ac.uk and ftp.adelaide.edu.au 


The Sun Managers list is an unmoderated mailing list for emergency-only requests. Subscribe and listen for a while, and read the regularly-posted Policy statement BEFORE sending mail to it. Write to sun-managers@sunmanagers.ececs.uc.edu 


The "Sneakers" mailing list is for discussion of LEGAL evaluations and experiments in testing various Internet "firewalls" and other TCP/IP network security products. 


You can join CIAC's mailing lists by filling out a form at the CIAC Web site. 


The firewall mailing list is obviously for discussion of firewall-related issues. 


For more mailing list information, check out the Security Mailing Lists FAQ at ISS. Here you'll find an annotated list of many security-related mailing lists and directions on how to join them. Exercise prudence, however, or your mailbox will be more full than President Clinton's hair. 


4.6) Useful columns? 


Back issues of Peter Baer Galvin's SunWorld Solaris Security column (plug :-), known as Pete's Wicked World. 


Carole Fennelly's Wizard's Guide to Security column in SunWorld. 


4.7) Useful Web sites? 


Perhaps the best single source of information, programs, and pointers to other security sites is found at COAST. 


ISS sells security scanning software, and also provides useful information on their Web site. Especially useful is the Security FAQs Web page. 


The Computer Security Institute publishes surveys which track usage of current technology and products by security professionals. 


The Qualix Group publishes a useful Firewall-1 FAQ 


Memco sells software to increase the security of individual and groups of machines. 


The University of Houston has its Information Security Manual online. It makes for interesting reading, especially if you're writing a policy manual for your site. 


If you're interested in Web site security, you must read the WWW Security FAQ. Also of interest is the Security Issues in WWW page. 


Bellcore sells several security programs. 


Trusted Systems does security consulting and training. 


V-One sells products that provide two-way authenticated, encrypted communication. 


Here's A plethora of PGP information. 


The best all-around information on security bugs and their patches is available at CERT. You can also ftp patches. 


The NIH provides a very useful Computer Security Information site, with an especially useful list of security programs. 


Raptor sells a Proxy Gateway firewall for Unix and NT, and has some whitepapers on general firewall technology. 


The Unix Guru Universe is an all-around useful site, and has a selection of security pointers. 


CIAC is the U.S. Department of Energy's Computer Incident Advisory Capability. Established to provide computer security services to employees and contractors of the United States Department of Energy. It's also useful for the rest of us. 


RSA maintains a very useful cryptography FAQ that explains many of the confusing aspects of cryptography. 


Learn from the hackers and crackers by reading the Phrack Newsletter 


Another useful cracker site is [http://www.geocities.com/Area51/5537/](http://www.geocities.com/Area51/5537/). It's an archive of information useful to crackers. 


A nice firewall-comparison checklist is available in free and commercial form. An interesting collection of security links: [http://www.fish.com/security/](http://www.fish.com/security/). 


5) How do I make my Solaris Web server more secure? 


There are several steps to installing a "secure" Web server. But what is meant by "secure"? Any machine that is publically accessible is necessarily unsecure. By putting it directly on the Internet you've already opened the front door and allowed anyone to come in and have a look. It is possible to guard the door and be sure the visitors hang out in only one room though. By installing the operating system carefully, adding tools, and adding monitoring software, your Web server can be much safer than one that uses a default installation. 


A previous version of this information was published as a two-part column by Peter Galvin and Hal Pomeranz in SunWorld, April 1996 and SunWorld, May 1996 


How secure does a Web server have to be? The answer is, "very secure." There have been several embarrassing incidents of graffitti on very public Web sites, and worse. Any number of toolkits exist that allow total amateurs to become holy terrors. The good news is that if you can beat the popular intrusion toolkits, 90 percent of the bad guys will go bother somebody else who's less secure. 


While the following techniques can make a Solaris-based system very secure, they have to be combined with a strong network architecture utilizing firewalls or filtering routers (there's no point in controlling access by IP address if crackers can send you packets with spoofed addresses). Such a strong architecture can only truly exist when combined with a comprehensive security policy covering your entire organization. 


Furthermore, no system is ever perfectly secure. The extra services (Web servers and anonymous FTP) that you run on the machine will always impact the overall security of the system. Don't be tempted to install other software not listed in these instructions. This machine is supposed to be secure, not convenient to administer. 


5.0) Web server security checklist 


Use this checklist to be sure your server is installed as securely as possible. Feel free to add to the checklist for site-specific steps, or to share your additions with us if they are general-purpose. 


Keep the system disconnected from the network until all is ready. 

Install just the core operating system, adding only necessary packages. 

Install recommended and security patches. 

Strip down the OS by removing startup files (carefully!). 

Disable IP forwarding in /etc/init.d/inetinit. 

Add a script to system startup to fix /tmp permissions (except on Solaris 2.5). 

Verify that few processes are running via ps. 

Invoke sendmail from cron to process queued mail occasionally. 

Install and configure tcp_wrappers, S/Key, wu-ftp, and tripwire as appropriate to your environment. 

Remove all but wu-ftp and telnet from /etc/inetd.conf, and edit /etc/hosts.allow to limit the machines that can use these daemons. 

Enable logging of all telnet access to the system via syslog . 

Mount filesystems read-only and no-suid as appropriate. 

Make /noshell the default shell for all accounts except root and access. 

Remove /etc/auto_*, /etc/dfs/dfstab, p/var/spool/cron/crontabs/* (except root). 

Use static routing. 

Test your system thoroughly, including allowed access and denied access, and event logging. 

Consider replacing sendmail, syslog, bind, and crontab with more secure versions. 

Install xntp for accurate time stamping. 

Consider enabling system accounting. 

Keep monitoring and testing the Web server. 

Even if you only implement some of these security steps, your Web server will be much more secure than a standard server installed with a standard Unix configuration. But to be safe, go whole-hog and lock that server down with all of these tools and techniques. 


5.1) Hardware setup 


Don't connect the system to a network before it is installed and secured. Theoretically, some cracker could get in and drop back doors onto your system while you are in the process of securing it. There are documented cases of people trying to break into machines within five minutes of the machine being connected to the Internet. 


You will need a CD-ROM drive to do the install and a tape or floppy drive for loading binaries and other files you created on other machines. These instructions are appropriate for Solaris 2.5. If you use a different OS version, the security of the resulting system may vary widely. 


5.2) Install the OS 


Start with the latest, solid version of Solaris 2.X. Each version of Solaris has been more secure than its predecessor. 


Solaris is quite flexible and contains many conveniences that make your work easier. Unfortunately, all of this extra functionality also makes it easier for potential crackers to gain access to your system. When attempting to create a secure system, the best plan is to start with the simplest OS you can and then add packages one-by-one on an "as-needed" basis. A limited OS configuration also boots and runs faster and is less prone to crashing than a feature-rich version. 


Under the Solaris install program, the most limited version of the OS you can select is the Core SPARC installation cluster. In fact, even this cluster has too many features. This cluster is what you should first install on your secure server. After you have selected Core SPARC in the Sun installation screens, you will want to select Customize and add the Terminal Information cluster which gives you support for commonly used terminal emulators (such as xterm and others). 


One of the advantages of the Core SPARC cluster is that it requires much less disk space than most types of Solaris installs. The following partition table is appropriate for machines loaded with the Core SPARC cluster: 


s0:    /         256 megabytes

s1:    swap        256 megabytes

s2:    overlap

s3:

s4:    

s5:    

s6:    /local        ??? megabytes (rest of the drive)

s7:


/var is large to allow for keeping extra logging and auditing information. Size swap as appropriate for your hardware, but extra swap helps prevent "denial of service" type attacks. 


Now, using some other machine, ftp to sunsolve.sun.com:/pub/patches and download the latest "recommended" (read: mandatory) patch cluster for Solaris 2.X (2.X_Recommended.tar.Z). Put this tarfile on a tape, move it over to your secure server, and install the patches. Some patches will not be installed because the software they fix is not included in the Core SPARC cluster. 


5.3) Strip down the OS 


Under Solaris, you control what processes are started at boot time by adding and removing files in /etc/rc[S0-3].d (the files in /etc/rc[S0-3].d being hard links to files in /etc/init.d). Many of these startup scripts run processes that you absolutely do not want running on your secure server: NFS is a prime example. 


Consider removing all extraneous startup files from /etc/rc2.d. We also recommend removing everything from /etc/init.d except the following files: 


K15rrcd         S05RMTMPFILES   K15solved       S20sysetup

S72inetsvc      S99audit        S21perf         

S99dtlogin      K25snmpd        S30sysid.net    S99netconfig

K50pop3         S74syslog       S75cron         S92rtvc-config 

K60nfs.server   K65nfs.client   S69inet                     

K92volmgt       README          S95SUNWmd.sync

S01MOUNTFSYS    S71sysid.sys    S88utmpd        S95rrcd


This list will be larger or smaller depending on if you have a graphics card in the machine, are using Solstice DiskSuite, and so on. Remove the files in /etc/rc3.d. 


For Solaris 2.4, edit /etc/init.d/inetinit and add the following lines near the end of the file: 


ndd -set /dev/ip ip_forward_directed_broadcasts 0

ndd -set /dev/ip ip_forward_src_routed 0

ndd -set /dev/ip ip_forwarding 0


These lines turn off a feature called IP forwarding. Nearly any machine that uses IP-based networking is capable of being a router, which means the bad guys could route packets through your machine to machines on your internal network or other secure machines that might trust the machine you are building. Turning off IP forwarding disables this feature. ``` 


Also consider setting the "ip_strict_dst_multihoming" kernel variable via ndd -set /dev/ip ip_strict_dst_multihoming 1 


The solaris machine will then drop packets coming in through one interface that are destined for another interface. This can prevent host spoofing. 


* Under Solaris 2.5, creating a file called /etc/notrouter will turn off IP forwarding. To allow routing again, simply remove /etc/notrouter and reboot. It's important to note that there is a small time window between when this file is created and when routing is disabled, theoretically allowing some routing to take place. 


Under Solaris 2.4, add a new script called /etc/init.d/tmpfix: 


#!/bin/sh

#ident  "@(#)tmpfix 1.0    95/08/14"


if [ -d /tmp ]

then

    /usr/bin/chmod 1777 /tmp

    /usr/bin/chgrp sys /tmp

    /usr/bin/chown root /tmp


and then ln /etc/init.d/tmpfix /etc/rc2.d/S79tmpfix so the script is invoked at boot time. This script prevents an attack that would allow a system cracker to get superuser access on your machine. It is not necessary under Solaris 2.5 (See "Re-tooling" SunWorld October 1995.) 


Some good advice from Casper Dik. Make sure that all of the startup routes run with the proper umask, so the files they create and not group or world writeable. Here's an easy method to insure this: 


     umask 022  # make sure umask.sh gets created with the proper mode

     echo "umask 022" > /etc/init.d/umask.sh

     for d in /etc/rc?.d

     do

         ln /etc/init.d/umask.sh $d/S00umask.sh

     done


Note: the trailing ".sh" of the scriptname is important, if you don't specify it, the script will be executed in a sub-shell, not in the main shell that executes all other scripts. 


Remove /etc/auto_*. Removing /etc/init.d/autofs should have prevented the automounter from starting up, but there's no reason to keep these files around either. 


Remove /etc/dfs/dfstab. Again, purging /etc/init.d should prevent the machine from ever becoming an NFS server, but best to get rid of this file anyway. 


Remove crontab files. You should remove all files from /var/spool/cron/crontabs except the root file. 


Use static routing. Create an /etc/defaultrouter file instead of relying on information from routed (which can be spoofed). If you need to route through different gateways, consider adding /usr/bin/route commands to /etc/init.d/inetinit instead of running routed. 


When you are done, reboot your machine. Always test boot file changes thoroughly. When the machine comes back up, the output of ps -ef should look like this: 


     UID   PID  PPID  C    STIME TTY      TIME COMD

    root     0     0 55   Mar 04 ?        0:01 sched

    root     1     0 80   Mar 04 ?       22:44 /etc/init -

    root     2     0 80   Mar 04 ?        0:01 pageout

    root     3     0 80   Mar 04 ?       33:18 fsflush

    root  9104     1 17   Mar 13 console  0:00 /usr/lib/saf/ttymon -g -h -p myhost console login:  -T sun -d /dev/console -l co

    root    92     1 80   Mar 04 ?        5:15 /usr/sbin/inetd -s

    root   104     1 80   Mar 04 ?       21:53 /usr/sbin/syslogd

    root   114     1 80   Mar 04 ?        0:11 /usr/sbin/cron

    root   134     1 80   Mar 04 ?        0:01 /usr/lib/utmpd

    root   198     1 25   Mar 04 ?        0:00 /usr/lib/saf/sac -t 300

    root   201   198 33   Mar 04 ?        0:00 /usr/lib/saf/ttymon

    root  6915  6844  8 13:03:32 console  0:00 ps -ef

    root  6844  6842 39 13:02:04 console  0:00 -sh


You will note that the /usr/lib/sendmail daemon is not running on the system: this is a feature. Processes that need to send mail off the system can and will invoke sendmail directly (possibly via some other mail user agent such as mailx), but you do not have to run a sendmail daemon that listens on port 25 and processes the mail queue immediately. You should add the following to root's crontab file: 


0 * * * * /usr/lib/sendmail -q > /var/adm/sendmail.log 2>&1


This entry will invoke sendmail every hour to process any queued mail. 


5.4) Install third-party software 

You will need three pieces of software to help secure your system and allow you to do safe administration of the machine over the network. Because there should be no compiler on your secure server, you will have to build these packages on some other machine and bring them onto the new machine you are building via a tape or floppy disk. 


The first package is the TCP Wrappers package written by Wietse Venema. Wietse's source code produces a small binary called tcpd that can be used to control access to services (such as telnet and ftp) that are started out of /etc/inetd.conf. Access control can be performed on IP address, domain name, and a raft of other parameters, and tcpd can raise alarms via syslog or e-mail if unauthorized connection attempts are made. 


Next, configure S/Key for remote secure access. See Q5.6 for S/Key configuration details. 


If you plan to allow ftp access to your secure server (whether anonymous or for administrative access), you need to get a copy of the WU-Archive ftp daemon. You must get version 2.4 or later since previous versions have major security holes. If you are going to grant administrative ftp access (as opposed to only anonymous ftp), you must hack S/Key support into the ftp daemon binary. In the Crimelabs S/Key distribution you will find an skey/misc/ftpd.c file that demonstrates how to make a previous version of the WU-Archive ftp daemon support S/Key. You will have to make the analogous changes to the v2.4 wu-ftpd source. You may also want to read the wu-ftp FAQ 


Compile and install the binaries (tcpd, wu-ftpd, and keyinit, keysu, and keysh from the S/Key software) in /usr/local/bin. When compiling wu-ftpd you will have to specify configuration and logging directories: we recommend you put the configuration directory somewhere under /etc and the logfiles under /var (so they have plenty of room to grow). See Q5.7 for detailed wu-ftp configuration. 


Use /noshell for all non-login accounts. Make /noshell be the login shell for all users except root and access. This shell disallows the login, while logging that a login attempt occurred. Crackers will never be able to get access through these accounts. 


5.5) Limit network access to the system 


When your secure machine eventually gets into position on the network, you will probably want to be able to use telnet and ftp to access the machine. Note that you do not have to enable these services on your machine, making your machine that much more secure, but that means you will always have to log in on the console and move files on and off the machine using tape or floppy disk. 


The telnet and ftp daemons are started by the inetd process. inetd's configuration file, /etc/inet/inetd.conf, contains many other services besides telnet and ftp, so it is best to simply remove this file and create a new one containing only the following lines: 


ftp stream tcp nowait root /usr/local/bin/tcpd /usr/local/bin/wu-ftpd

telnet stream tcp nowait root /usr/local/bin/tcpd /usr/sbin/in.telnetd


Note that we are using tcpd to control access to both of these services and are using the wu-ftpd binary instead of the ftp server that comes with Solaris. If you do not want to allow anybody to telnet or ftp to you system, then simply remove the appropriate line from inetd.conf, or remove the file altogether and inetd will not even be started at boot time. 


Access control for tcpd is configured using the /etc/hosts.allow and /etc/hosts.deny files. tcpd looks at hosts.allow first, so you can permit a few machines to have telnet or ftp access and then deny access to everybody else in hosts.deny (this is often called a "default deny" policy). Here is a sample hosts.allow file: 


ALL: 172.16.3.0/255.255.255.0


This would allow any user on any host on the 172.16.3.0 network to have access to all of the services (telnet and ftp) on your machine. That user will still have to supply the appropriate password or S/Key response (see below). Always use IP addresses in the hosts.allow file, because hostname information can be spoofed (if you are using the Internet Domain Name Service, or some other name service such as NIS). 


Now we want to disallow access for everybody else. Put the following line into /etc/hosts.deny: 


ALL: ALL: /usr/bin/mailx -s "%d: connection attempt from %c" root@mydomain.com


Not only does this deny access to all services from all hosts, it causes tcpd to send an alarm via e-mail that somebody is trying to get access to the machine. Substitute the e-mail address of somebody who reads e-mail regularly for root@mydomain.com in the above line. 


Now you want tcpd to log all accesses via syslog. Put the following line in /etc/syslog.conf: 


auth.auth.notice;auth.info           /var/log/authlog


The white-space on the line above must be tabs, or syslog will be unable to properly parse the file and no logging will happen. Note that the logging facility is a configurable parameter when building tcpd, but we recommend using AUTH, as opposed to any LOCAL* facilities. 


Other files in /etc/init.d. Casper reiterates that the choice of which scripts to take out of /etc/init.d is highly dependent upon which version of Solaris you are using. The list of files we presented in our article was based on a Solaris 2.4 machine, so make sure you know what you're doing if you try out the directions on a Solaris 2.5 machine. 


Sendmail. Instead of invoking sendmail from cron you can also run the daemon without the -bd option. This will cause the daemon to be a queue-watcher only. We prefer not to have the daemon running (one less process to worry about on the system), but your mileage may vary. 


/etc/syslog.conf. There was a typo and an error in our instructions for configuring /etc/syslog.conf for tcpd. The correct line is 


auth.info        /var/log/authlog


which will log all auth events with severity info and higher to /var/log/authlog. Don't forget that the whitespace in this entry must be tabs. 


5.6) Configure S/Key 


You will need the S/Key package for remote, secure access. (Part of the logdaemon toolset). S/Key is a one-time-only password mechanism. Instead of typing in your password over the network, the S/Key software will send you a challenge string, and you will compute a response on your local machine using the challenge and a secret password that you have memorized. If you send the proper response back, the S/Key software gives you access to the machine but the response you gave will never again be valid for getting access to the machine. This means that if somebody is using a packet sniffer, they cannot capture the response and use it to break into your machine. The S/Key software also comes with a version of the su command that uses S/Key challenge/response to grant superuser access safely over the network. 


To begin using S/Key, create an account that uses /usr/local/bin/keysh as its login shell. You will login as this user with some reusable password of your choosing and then keysh will force you to respond to an S/Key challenge before giving you a shell prompt. 


You should put 


access:x:100:100:Access Account:/tmp:/usr/local/bin/keysh


at the end of /etc/passwd and 


access:NP:6445::::::


at the end of /etc/shadow. Then use the passwd access command to set the password for user access. The password you choose here doesn't have to be a very good password, since you will be relying on keysh to provide the security for this account. 


Since /usr/local/bin/keysh is not a standard shell, you have to create an /etc/shells file with these lines in it: 


/sbin/sh

/usr/local/bin/keysh


Only users whose login shell is one of these two shells are allowed to access the machine. 


Now create an codepty /etc/skeykeys file and make it mode 600 and owned by root: 


touch /etc/skeykeys

chmod 600 /etc/skeykeys

chown root /etc/skeykeys

chgrp root /etc/skeykeys


Use the keyinit access command to initialize the S/Key secret for user access. You have completed the S/Key setup for user access. 


You now want to allow the user access to use the keysu command to become superuser. First change the entry for group root in /etc/group: 


root::0:root,access


Only users listed in this entry are allowed to become superuser using keysu. Now you have to use the keyinit root command to initialize the S/Key secret for the superuser. I recommend using a different secret word than you used for user access. 


At this point you may be tcodepted to simply remove /bin/su so that users are forced to use keysu. Unfortunately, many scripts use /bin/su to start processes that do not require full superuser access. You should, however, chmod 500 /bin/su so that only the superuser can run this program. 


Note the implicit assumption that access is a group account shared by several administrators. You may feel more comfortable giving each administrator a separate account with a different S/Key secret so that you have a better audit trail. The downside to this approach is it creates more accounts that can have bad passwords on them and allow crackers to gain access. Decide what makes sense for your organization. 


5.7) Configure wu-ftp 


Configuring wu-ftpd is tricky, even for experts. When you compiled wu-ftpd, you specified a directory where the daemon will look for its configuration files. This configuration directory will contain a pid directory and three files. The ftpconversions file should be empty but it must exist. The ftpusers file should contain a list of all users in the machine's password file who should not be allowed to ftp into the system. This file should contain every user in the password file: we will add a user later who is allowed to ftp into the system. Most especially, root should always be in the ftpusers file. 


The last file in the configuration directory is the ftpaccess file. Rather than go into full detail, here is a file that you can use if you do not want to allow anonymous ftp into your system, but do want some users to be able to upload files to the machine: 


class users real 172.16.3.*


log commands real

log transfers real inbound,outbound


This allows users to ftp from any host on network 172.16.3.0 and from nowhere else (which is redundant if you are already using tcpd, but security in depth is a Good Thing). All commands and file transfers will be logged to the log file you specified when you compiled the daemon (which is why we recommended you put it in /var where it has plenty of space to grow). 


Configuring anonymous ftp is beyond the scope of this FAQ, but be warned to be very careful, because it is easy to make a mistake and give away access to your system. Review the documentation that comes with wu-ftpd for information and pointers to other documents on anonymous ftp. 


5.8) Limit access to files and file systems 


Download and use fix-modes. The programs in this package clean up unsecure group permissions on some system files and directories. This script has recently been updated to support Solaris 2.5 systems. 


One way to thwart potential system crackers is to prevent them from running setuid programs on your machine. The steps you have already taken make it unlikely that anybody is going to get an unauthorized setuid program onto your machine, but a little paranoia never hurt anybody in the security business. 


Use the nosuid option in /etc/vfstab to prevent setuid programs from being executed on any of your UFS filesystems: 


/proc               -       /proc      proc    -   no   -

fd                  -       /dev/fd    fd      -   no   -

swap                -       /tmp       tmpfs   -   yes  -

/dev/dsk/c0t3d0s1       -       -          swap    -   no   -


/dev/dsk/c0t3d0s0 /dev/rdsk/c0t3d0s0  /       ufs  1   no   remount,nosuid

/dev/dsk/c0t3d0s4 /dev/rdsk/c0t3d0s4  /usr    ufs  1   no   ro

/dev/dsk/c0t3d0s5 /dev/rdsk/c0t3d0s5  /var    ufs  1   no   nosuid

/dev/dsk/c0t3d0s6 /dev/rdsk/c0t3d0s6  /local  ufs  2   yes  nosuid


Note that /usr contains some setuid executables (not the least of which are the S/Key binaries in /usr/local/bin), so we mount it read-only instead of nosuid. The root filesystem is mounted by the boot PROM, so it has to be remounted for the nosuid directive to take effect. 


You must not apply the nosuid directive to the special filesystems. Note that TMPFS type filesystems (such as /tmp) are automatically nosuid in recent releases of Solaris. 


5.9) Test the configuration 


Reboot your system one last time and plug it into the network. Confirm that the following are true: 


You should be able to telnet and ftp to your secure server from the machines you configured tcpd to allow. 


Trying to access the machine from any other machine should result in a denial of access and an e-mail to the appropriate party. 


You should be able to login via telnet and ftp as user access, but not as root or any other user. 


User access should be able to /usr/local/bin/keysu to become superuser. 


ps -ef should show very few processes; in particular, sendmail and the various NFS processes should not be running. 


touch /usr/FOO should fail with an indication that the filesystem is read-only. 


As the superuser, copy the ps command to /, making sure to preserve the setuid bit. access should not be able to get a process listing with /ps -ef. Remove the /ps binary when you are done. 

Congratulations! You have just created a very secure machine. 


5.10) Step 10: Other suggestions 


There are a number of freely available replacements for common system programs that are significantly more secure than the versions provided with Solaris. Consider replacing sendmail with the latest version. Replace the resolver library with the latest version of bind. Replace syslog and crontab (check your local Archie server). 


Your logging information is only as good as the timestamps in your files. Consider running XNTP to keep your system clock in synch with accurate clock sources from the Internet and with other machines on your networks. If somebody breaks in to your network, you may have to correlate logs between dozens of systems, so their clocks had better be in synch. 


Before your system goes live on the network, get a copy of tripwire and make a database of MD5 checksums for all files on your secure server. Put this database on removable media (tape or floppy disk) so that somebody who breaks into your system can't modify the data. Run tripwire at random (but frequent) intervals to make sure nobody is tampering with your files. 


Consider running process accounting so that you have a record of every command executed on your system. You will pay a performance penalty (10 to 20%) if you turn on process accounting. See man acct for more information. 


Change your S/Key secrets regularly (every 30 days if you can stand it) and choose good secret words (use non-alphanumeric characters and long secret words). Change the secret words on the system console or use keyinit -s to change the secret over the network. Do not use the same secret word for both the access and root accounts. 


6) Acknowledgements? 


The following people contributed to the contents of this FAQ: 


Casper Dik (throughout) 

Hal Pomeranz (extensively in section 5) 

Michele Crabb (extensively in sections 1 and 2) 

Dan Stromberg (added information about password-checking programs) 

Darren J Moffat (Solaris 2.6 and 7 updates) 

Jan Koum (Q 2.30) 

About the author

Peter Baer Galvin is the Chief Technologist for Corporate Technologies, a systems integrator and VAR. Before that, Peter was the Systems Manager for Brown University's Computer Science Department. He has written articles for Byte and other magazines and previously wrote Pete's Wicked World, the security column for SunWorld. Peter is co-author of the Operating Systems Concepts texbook. As a consultant and trainer, Peter has taught tutorials on security and system administration and given talks at many conferences and institutions.
