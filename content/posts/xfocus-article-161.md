---
title: "Avoiding security holes Part 1"
date: 2001-04-18T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-161"
---

(quack_at_xfocus.org)

*Abstract: *


This article is the first one in a series about the main types of security holes in applications. We'll show the ways to avoid them by changing your development habits a little.


### Introduction


It doesn't take more than two weeks before a major application which is part of most Linux distributions presents a security hole allowing, for instance, a local user to become root. Despite the great quality of most of this software, ensuring the security of a program is a hard job : it must not allow a bad guy to benefit illegally from system resources. The availability of application source code is a good thing, much appreciated by programmers, but the smallest defects in software become visible to everyone. Furthermore, the detection of such defects comes at random and the people finding them do not always have good intentions.


From the sysadmin side, daily work consists of reading the lists concerning security problems and immediately updating the involved packages. For a programmer it can be a good lesson to try out such security problems since avoiding security holes from the beginning is the preferred method of fixing them. We'll try to define some "classic" dangerous behaviors and provide solutions to reduce the risks. We won't talk about network security problems since they often stem from configuration mistakes (dangerous cgi-bin scripts, ...) or from system bugs allowing DOS (Denial Of Service) type attacks to prevent a machine from listening to its own clients. These problems concern the sysadmin or the kernel developers. But the application programmer must also protect her code as soon as she takes into account external data. Some versions of pine, acroread, netscape, access,... have allowed elevated access or information leaks under some conditions. As a matter of fact secure programming is everyone's concern.


This set of articles shows methods which can be used to damage a Unix system. We could only have mentioned them or said a few words about them, but we prefer complete explanations to make people understand the risks. Thus, when debugging a program or developing your own, you'll be able to avoid or correct these mistakes. For each discussed hole, we will take the same approach. We'll start detailing the way it works. Next, we will show how to avoid it. For every example we will use security holes still present in wide spread software.


This first article talks about the basics needed for understanding security holes, that is the notion of privileges and the Set-UID or Set-GID bit. Next, we analyse the holes based on the system() function, since they are easier to understand.


We will often use small C programs to illustrate what we are talking about. However, the approaches mentioned in these articles are applicable to other programming languages : perl, java, shell scripts... Some security holes depend on a language, but this is not true for all of them as we will see it with system().


### Privileges


On a Unix system, users are not equals, neither are applications. The access to the file system nodes - and accordingly the machine peripherals - relies on a strict identity control. Some users are allowed to do sensitive operations to maintain the system in good condition. A number called UID (User Identifier) allows the identification. To make things easier, a user name corresponds to this number, the association is done in the /etc/passwd file.


The UID of 0, with default name of root, can access everything in the system. He can create, modify, remove every system node, but he can as well manage the physical configuration of the machine, mounting partitions, activating network interfaces and changing their configuration (IP address), or using system calls such as mlock() to act on physical memory, or sched_setscheduler() to change the order mechanism. In a future article we will study the Posix.1e features which allows limiting the privileges of an application executed as root, but for now, let's assume the super-user can do everything on a machine.


The attacks we will mention are internal ones, that is an authorized user on a machine tries to gain privileges he doesn't have. On the other hand, the network attacks are external ones, coming from people trying to connect to a machine they are not allowed on. 


To use privileges reserved for another user without being able to log in under her identity, one must at least have the opportunity to talk to an application running under the victim's UID. When an application - a process - runs under Linux, it has a well defined identity. First, a program has an attribute called RUID (Real UID) corresponding to the user ID who launched it. This data is managed by the kernel and usually can not change. A second attribute completes this information : the EUID field (Effective UID) corresponding to the identity the kernel takes into account when managing the access rights (opening files, reserved system-calls).


To get the privileges of another user means everything will be done under the UID of that user, and not under the proper UID. Of course, a cracker tries to get the root ID, but many other user accounts are of interest, either because they give access to system information (news, mail, lp...) or because they allow reading private data (mail, personal files, etc) or they can be used to hide illegal activities such as attacks on other sites.


To run an application with the privileges of an Effective UID different from its Real UID (the user who launched it) the executable file must have a specific bit turned on called Set-UID. This bit is found in the file permission attribute (like user's execute, read, write bits, group members or others) and has the octal value of 4000. The Set-UID bit is represented with an s when displaying the rights with the ls command :


>> ls -l /bin/su

-rwsr-xr-x  1 root  root  14124 Aug 18  1999 /bin/su

>>


The command "find / -type f -perm +4000" displays a list of the system applications having their Set-UID bit set to 1. When the kernel runs an application with the Set-UID bit on, it uses the program owner's identity as EUID for the process. On the other hand, the RUID doesn't change and corresponds to the user who launched the program. For instance, every user can have access to the /bin/su command, but it runs under its owner's identity (root) with every privilege on the system. Needless to say one must be very careful when writing a program with this attribute. 

Each process also has an Effective group ID, EGID, and a real identifier RGID. The Set-GID bit (2000 in octal) in the access rights of an executable file, asks the kernel to use the owner's group of the file as EGID and not the GID of the user who launched the program. A curious combination sometimes appears with the Set-GID set to 1 but without the group execute bit. As a matter of fact, it's a convention having nothing to do with privileges related to applications, but indicating the file can be blocked with the function fcntl(fd, F_SETLK, lock). Usually an application doesn't use the Set-GID bit, but it does happen sometimes. Some games, for instance, use it to save the best scores into a system directory.


### Type of attacks and potential targets


There are various types of attacks against a system. Today we'll study the mechanisms to execute an external command from within and application. This is usually a shell running under the identity of the owner of the application. A second type of attack relies on buffer overflow giving the attacker the ability to run personal code instructions. Last, the third main type of attack is based on race condition - a lapse of time between two instructions in which a system component is changed (usually a file) while the application believes it remains the same.


The two first types of attacks often try to execute a shell with the application owner's privileges, while the third one is targeted instead at getting write access to protected system files. Read access is sometimes considered a system security weakness (personal files, emails, password file /etc/shadow, and pseudo kernel configuration files in /proc).


The targets of security attacks are mostly the programs having a Set-UID (or Set-GID) bit on. However, this also effects every application running under a different ID than the one of its user. The system daemons represent a big part of these programs. A daemon is an application usually started at boot time, running in the background without any control terminal, and doing privileged work for any user. For instance, the lpd daemon allows every user to send documents to the printer, sendmail receives and redirects electronic mail, or apmd asks the Bios for the battery status of a laptop. Some daemons are in charge of communication with external users through the network (Ftp, Http, Telnet... services). A server called inetd manages the connections of many of these services.


We can then conclude that a program can be attacked as soon as it talks - even briefly - to a user different from the one who started it. While developing this type of application you must be careful to keep in mind the risks presented by the functions we will study here.


### Changing privilege levels


When an application runs with an EUID different from its RUID, it's to provide the user with privileges he needs but doesn't have (file access, reserved system calls...). However these privileges are only needed for a very short time, for instance when opening a file, otherwise the application is able to run with its user's privileges. It's possible to temporarily change an application EUID with the system-call :


  int seteuid (uid_t uid);


A process can always change its EUID value giving it the one of its RUID. In that case, the old UID is kept in a saved field called SUID (Saved UID) different from SID (Session ID) used for control terminal management. It's always possible to get the SUID back to use it as EUID. Of course, a program having a null EUID (root) can change at will both its EUID and RUID (it's the way /bin/su works). 

To reduce the risks of attacks, it's suggested to change the EUID and use the RUID of the users instead. When a portion of code needs privileges corresponding to those of the file's owner, it's possible to put the Saved UID into the EUID. Here is an example :


  uid_t e_uid_initial;

  uid_t r_uid;


  int

  main (int argc, char * argv [])

  {

    /* Saves the different UIDs */

    e_uid_initial = geteuid ();

    r_uid = getuid ();


    /* limits access rights to the ones of the

     * user launching the program */

    seteuid (r_uid);

    ...

    privileged_function ();

    ...

  }


  void

  privileged_function (void)

  {

    /* Gets initial privileges back */

    seteuid (e_uid_initial);

    ...

    /* Portion needing privileges */

    ...

    /* Back to the rights of the runner */

    seteuid (r_uid);

  }


This method is much more secure than the unfortunately all to common one consisting of using the initial EUID and then temporarily reducing the privileges just before doing a "risky" operation. However this privilege reduction is useless against buffer-overflow attacks. As we'll see in a next article, these attacks intend to ask the application to execute personal instructions and can contain the system-calls needed to make the privilege level higher. Nevertheless, this approach protects from external commands and from most race conditions.


### Running external commands


An application often needs to call an external system service. A well known example concerns the mail command to manage an electronic mail (running report, alarm, statistics, etc) without requiring a complex dialog with the mail system. The easiest solution is to use the library function :


  int system (const char * command)


### Dangers of the system() function


This function is rather dangerous : it calls the shell to execute the command given as an argument. The shell behavior depends on the choice of the user. A typical example comes from the PATH environment variable. Let's look at an application calling the mail function. For instance, the following program sends its source code to the user who launched it :


/* system1.c */


#include <stdio.h>

#include <stdlib.h>


int

main (void)

{

  if (system ("mail $USER < system1.c") != 0)

    perror ("system");

  return (0);

}


Let's say this program is Set-UID root : 

>> cc system1.c -o system1

>> su

Password:

[root] chown root.root system1

[root] chmod +s system1

[root] exit

>> ls -l system1

-rwsrwsr-x  1 root  root  11831  Oct 16  17:25 system1

>>


To execute this program, the system runs a shell (with /bin/sh) and with the -c option, it tells it the instruction to invoke. Then the shell goes through the directory hierarchy according to the PATH environment variable to find an executable called mail. To compromise the program, the user only has to change this variable's content before running the application. For example : 

  >> export PATH=.

  >> ./system1


looks for the mail command only within the current directory. One need merely create an executable file (for instance, a script running a new shell) and name it mail and the program will then be executed with the main application owner's EUID! Here, our script runs /bin/sh. However, since it's executed with a redirected standard input (like the initial mail command), we must get it back in the terminal. We then create the script : 

#! /bin/sh

# "mail" script running a shell

# getting its standard input back.

/bin/sh < /dev/tty


Here is the result : 

>> export PATH="."

>> ./system1

bash# /usr/bin/whoami

  root

bash#


Of course, the first solution consists in giving the full path of the program, for instance /bin/mail. Then a new problem appears : the application relies on the system installation. If /bin/mail is usually available on every system, where is GhostScript, for instance? (is it in /usr/bin, /usr/share/bin, /usr/local/bin ?). On the other hand, another type of attack becomes possible with some old shells : the use of the environment variable IFS. The shell uses it to parse the words in the command line. This variable holds the separators. The defaults are the space, the tab and the return. If the user adds the slash /, the command "/bin/mail" is understood by the shell as "bin mail". An executable file called bin in the current directory can be executed just by setting PATH, as we have seen before, and allows to run this program with the application EUID.


Under Linux, the IFS environment variable is not a problem anymore since bash and pdksh both complete it with the default characters on startup. But keeping application portability in mind you must be aware that some systems might be less secure regarding this variable.


Some other environment variables may cause unexpected problems. For instance, the mail application allows the user to run a command while composing a message using an escape sequence "~!". If the user writes the string "~!command" at the beginning of the line, the command is run. The program /usr/bin/suidperl used to make perl scripts work with a Set-UID bit calls /bin/mail to send a message to root when it detects a problem. Since /bin/mail is Set-UID root, the call to /bin/mail is done with root's privileges and contains the name of the faulty file. A user can then create a file whose name contains a carriage return followed by a ~!command sequence and another carriage return. If a perl script calling suidperl fails on a low-level problem related to this file, a message is sent under the root identity, containing the escape sequence from the mail application, and the command in the file name is executed with root's privileges.


This problem shouldn't exist since the mail program is not supposed to accept escape sequences when run automatically (not from a terminal). Unfortunately, an undocumented feature of this application (probably left from debugging), allows the escape sequences as soon as the environment variable interactive is set. The result? A security hole easily exploitable (and widely exploited) in an application supposed to improve system security. The blame is shared. First, /bin/mail holds an undocumented option especially dangerous since it allows code execution only checking the data sent, what should be a priori suspicious for a mail utility. Second, even if the /usr/bin/suidperl developers were not aware of the interactive variable, they shouldn't have left the execution environment as it was when calling an external command, especially when writing this program Set-UID root.


As a matter of fact, Linux ignores the Set-UID and Set-GID bit when executing scripts (read /usr/src/linux/fs/binfmt_script.c and /usr/src/linux/fs/exec.c). But some tricks allow you to bypass this rule, like Perl does with its own scripts using /usr/bin/suidperl to take these bit into account.


### Solutions


It isn't always easy to find a replacement for the system() function. The first variant is to use system-calls such as execl() or execle(). However, it'll be quite different since the external program is no longer called as a subroutine, instead the invoked command replaces the current process. You must fork the process and parse the command line arguments. Thus the program :


  if (system ("/bin/lpr -Plisting stats.txt") != 0) {

    perror ("Printing");

    return (-1);

  }


becomes : 

pid_t pid;

int   status;


if ((pid = fork()) < 0) {

  perror("fork");

  return (-1);

}

if (pid == 0) {

  /* child process */

  execl ("/bin/lpr", "lpr", "-Plisting", "stats.txt", NULL);

  perror ("execl");

  exit (-1);

}

/* father process */

waitpid (pid, & status, 0);

if ((! WIFEXITED (status)) || (WEXITSTATUS (status) != 0)) {

  perror ("Printing");

  return (-1);

}


Obviously, the code gets heavier! In some situations, it becomes quite complex, for instance, when you must redirect the application standard input such as in : 

system ("mail root < stat.txt");


That is, the redirection defined by < is done from the shell. You can do the same, using a complicated sequence such as fork(), open(), dup2(), execl(), etc. In that case, an acceptable solution would be using the system() function, but configuring the whole environment. 

Under Linux, the environment variables are stored in the form of a pointer to a table of characters : char ** environ. This table ends with NULL. The strings are of the form "NAME=value".


We start removing the environment using the Gnu extension :


    int clearenv (void);


or forcing the pointer 

    extern char ** environ;


to take the NULL value. Next the important environment variables are initialized, using controlled values, with the functions : 

    int setenv (const char * name, const char * value, int remove)

    int putenv(const char *string)


before calling the system() function. For example : 

    clearenv ();

    setenv ("PATH", "/bin:/usr/bin:/usr/local/bin", 1);

    setenv ("IFS", " \t\n", 1);

    system ("mail root < /tmp/msg.txt");


If needed, you can save the content of some useful variables before removing the environment (HOME, LANG, TERM, TZ,etc.). The content, the form, the size of these variables must be strictly checked. It is important that you remove the whole environment before redefining the needed variables. The suidperl security hole wouldn't have appeared if the environment were properly removed. 

Analogues, protecting a machine on a network first implies denying every connection. Next, a sysadmin activates the required or useful services . In the same way, when programming a Set-UID application the environment must be cleared and then filled with required variables.


Verifying a parameter format is done by comparing the expected value to the allowed formats. If the comparison succeeds the parameter is validated. Otherwise, it is rejected. If you run the test using a list of invalid format values, the risk of leaving a malformed value increases and that can be a disaster for the system.


We must understand what is dangerous with system() is also dangerous for some derived functions such as popen(), or with system-calls such as execlp() or execvp() taking into account the PATH variable.


### Indirect execution of commands


To improve a programs usability, it's easy to leave the user the ability to configure most of the software behavior using macros, for instance. To manage variables or generic patterns as the shell does, there is a powerful function called wordexp(). You must be very careful with it, since sending a string like $(command) allows executing the mentioned external command. Giving it the string "$(/bin/sh)" creates a Set-UID shell. To avoid this, wordexp() has an attribute called WRDE_NOCMD that deactivates the interpretation of the $( ) sequence .


When invoking external commands you must be careful to not call a utility providing an escape mechanism to a shell (like the vi :!command sequence). It's difficult to list them all, some applications are obvious (text editors, file managers...) others are harder to detect (as we have seen with /bin/mail) or have dangerous debugging modes.


### Conclusion


This article illustrates various aspects :


Everything external to a Set-UID root program must be validated! This means the environment variables as well as the parameters given to the program (command line, configuration file...); 

Privileges have to be reduced as soon as the program starts and should only be increased very briefly and only when absolutely necessary; 

The "depth of security" is essential : every protection decision programs make helps reduce the number of people who can compromise them. 

The next article will talk about memory, its organization, and function calls before reaching the buffer overflows. We also will see how to build a shellcode.
