---
title: "OpenBSD Loadable Kernel Modules"
date: 2001-08-16T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-251"
---

(quack_at_xfocus.org)


### OpenBSD Loadable Kernel Modules


comments to [peter_a_werner@yahoo.com](mailto:peter_a_werner@yahoo.com)


[http://www.deadly.org/article.php3?sid=20010812210650](http://www.deadly.org/article.php3?sid=20010812210650)


Introduction 


From lkm(4): "Loadable kernel modules allow the system administrator to dynamically add and remove functionality from a running system. This ability also helps software developers to develop new parts of the kernel without constantly rebooting to test their changes." 


The module framework used on OpenBSD was written by Terrence R. Lambert, with a design aim of providing similar functionality to the loadable kernel module implementation from SunOS 4.1.3. A quick visit to [www.netbsd.org](http://www.netbsd.org/) indicates that most of the information here should apply to systems running NetBSD as well. 


A caveat of loadable modules is the security risk they present. They open a wide range of possibilities to a malicious superuser, and can be very hard to detect. As such, modules cannot be loaded or unloaded at a securelevel greater than 0. If you are a system administrator and wish to have a module loaded, you can add an entry to /etc/rc.securelevel to load the module before the securelevel rises. If you are working on the development of a module, you will probably want to run at securelevel -1, again, this can be set by editing /etc/rc.securelevel 


Overview 


The interaction with /dev/lkm is done via a series of ioctl(2) calls. These are mainly used by the modload(8), modunload(8) and modstat(8) tools to get your module in and our of the kernel. The lkm interface defines five different types of modules: 


System Call Modules 

Virtual File System modules 

Device Drive modules 

Execution Interpreter modules 

Miscellaneous modules 

A generic module has three main sections: 

1) A handler for kernel entry and exit (ie, when the module is being loaded, unloaded or queried once loaded). 


2) An external entry point, used when the module is being loaded with modload(8) 


3) The bulk of the module, containing the functional code. 


For the miscellaneous type of module, it is up to the module writer to provide sanity checks and to restore the previous state of the kernel when the module is unloaded. For the other types, this is handled by the lkm device. 


Module support must be compiled into the kernel using 'option LKM' in the kernel configuration file. Support for modules is enabled by default in the GENERIC OpenBSD 2.9 kernel. Generally, space in the kernel data structures is provided for module operations. As an example there are slots in bdevsw[] and cdevsw[] for lkm devices. 


For each type of module there is a macro used for initialisation of an internal data structure. This is where things like the name of the module and its position in the kernel data structure can be specified, along with module specific data such as a struct sysent for system call modules. 


Lets have a look at some examples. 


System Call modules. 


Here we will add a new system call that printf()'s its integer and string arguments. Its prototype looks like this: 


int syscall(int, char *)


The definition of the internal lkm structure for a syscall looks like this: 

struct lkm_syscall {

        MODTYPE lkm_type;

        int     lkm_ver;

        char    *lkm_name;

        u_long  lkm_offset;             /* save/assign area */

        struct sysent   *lkm_sysent;

        struct sysent   lkm_oldent;     /*save area for unload */

};


Briefly, we have the type of module (in this case it will be LM_SYSCALL), the version of the lkm interface, the name of the module, its offset which in the case of a system call is its position in the system call table. Finally we have a pointer to the struct sysent for this system call and space for a copy of whatever was in the slot it takes before the module was loaded. 

It will be initialised using the MOD_SYSCALL macro: 


MOD_SYSCALL("ourcall", -1, &newcallent)


This sets its name to "ourcall", used for querying the module and as displayed when using modstat(8). The -1 is the slot where the syscall should be placed, in this case -1 means we don't care where it is placed, it should just be allocated the next available one. Finally the newcallent is a struct sysent containing the relevant data for our system call. 

We also provide a handler for the load and unload function, in this case we just say 'hi' and 'bye' when the module is loaded and unloaded. Handlers can be provided for the load, unload and stat functions, which can be useful for debugging. The handler can be the same function or individual functions, the action being performed is passed to the handler allowing inspection and decision based on that. If no handler is desired, lkm_nofunc() should be specified which is simply a stub returning 0. 


The external entry point for our module is ourcall() which makes use of the macro DISPATCH: 


int

ourcall(lkmtp, cmd, ver)

        struct lkm_table *lkmtp;

        int     cmd;

        int     ver;

{

        DISPATCH(lkmtp, cmd, ver, ourcall_handler, ourcall_handler, lkm_nofunc)

}


This handles the loading, unloading and querying of the module. The fourth argument is the handler for the load action, the fifth argument the handler for the unload action and the sixth argument the handler for the stat function (which is not used in the case of system calls). 

This is the complete code for the system call module (syscall.c): 


#include <sys/param.h>

#include <sys/systm.h>

#include <sys/ioctl.h>

#include <sys/cdefs.h>

#include <sys/conf.h>

#include <sys/mount.h>

#include <sys/exec.h>

#include <sys/lkm.h>

#include <sys/proc.h>

#include <sys/syscallargs.h>


/* our system call prototype */

int     newcall __P((struct proc *p, void *uap, int *retval));


/*

 * All system calls are passed three arguments: a pointer to the 

 * struct proc that is calling it, a void pointer to its arguments

 * and an integer pointer to its return value. Here we define a 

 * structure for the arguments. If you only have one argument, 

 * create your structure with just one entry.

 */


struct newcall_args{

        syscallarg(int) value;

        syscallarg(char *) msg;

};


/* 

 * This structure defines our system call. The first argument is the 

 * number of arguments, the second argument is the size of the 

 * arguments and the third argument the function that contains the 

 * actual code for the system call.

 */


static struct sysent newcallent = {

        2, sizeof(struct newcall_args), newcall 

};


/* 

 * Initialise an internal structure for our syscall. 

 * Argument 1 is the name of the syscall used for (among other things)

 * lookups in the ioctl() call. Argument 2 is the slot for the system 

 * call function pointer should be placed. You can either pass the 

 * number you want, or -1 which indicates the next available slot 

 * should be used. Argument 3 is a pointer to a struct sysent for the 

 * call.

 */     


MOD_SYSCALL("ourcall", -1, &newcallent);


/*

 * This function will be used when our module is being "wired in".

 * It is passed a pointer to a struct lkm_table and the command or 

 * action that is being performed. Checking the value of the command 

 * as we do below allows a generic "handler" if desired. When adding

 * a system call via a module, there is no special handling performed

 * for the stat action.

 */


static int

ourcall_handler(lkmtp, cmd)

        struct lkm_table *lkmtp;

        int     cmd;

{

        if (cmd == LKM_E_LOAD) 

                printf("hi!n");

        else if (cmd == LKM_E_UNLOAD)

                printf("bye!n");


        return(0);

}


/* 

 * This is the external entry point for our module.  As above we are

 * passed a command describe the action being performed allowing generic

 * handlers. We are also passed a version number to allow one module to

 * contain the source for future versions of the lkm interface. 

 *

 * The macro DISPATCH is additionally passed three arguments specifying

 * the code that will be called for the actions load, unload and stat.

 * For load and unload we share the function ourcall_handler(). For stat 

 * (which is unused when adding system calls) we use lkm_nofunc() which

 * is simply a stub that returns 0.

 */


int

ourcall(lkmtp, cmd, ver)

        struct lkm_table *lkmtp;

        int     cmd;

        int     ver;

{

        DISPATCH(lkmtp, cmd, ver, ourcall_handler, ourcall_handler, lkm_nofunc)

}


/* 

 * Finally we have the code for our actual new system call. The arguments

 * passed to it are at the void pointer.

 */


int

newcall(p, v, retval)

        struct proc *p;

        void *v;

        int *retval;

{

        struct newcall_args *uap = v;


        printf("%d %sn", SCARG(uap, value), SCARG(uap, msg));

        return(0);

}


Compiling and Installing: 

# cc -D_KERNEL -I/sys -c syscall.c

# modload -o ourcall.o -eourcall syscall.o

Module loaded as ID 0

#


The -o option specifies the output file, the -e option is the external entry point and the last argument is the input file. Checking with modstat: 

# modstat

Type     Id Off Loadaddr Size Info     Rev Module Name

SYSCALL   0 210 e0b92000 0002 e0b93008   2 ourcall

#


Of note is the 'Off' entry, which is the system calls position in the system call table. We use this when we want to make use of the system call. We can also see our 'hi' in the dmesg when the module was loaded: 

# dmesg | tail -2

hi!

DDB symbols added: 150060 bytes

#


Let's have a look at a sample program to use our new call (calltest.c): 

#include <stdio.h>

#include <unistd.h>

#include <stdlib.h>

#include <fcntl.h>

#include <err.h>

#include <sys/lkm.h>

#include <sys/ioctl.h>

#include <sys/syscall.h>


int 

main(argc, argv)

        int argc;

        char **argv;

{

        int error, fd;

        struct lmc_stat modstat;


        if (argc != 3)

                errx(1, "%s  ", argv[0]);


        modstat.name = "ourcall";

        

        fd = open("/dev/lkm", O_RDONLY);

        if (fd == -1)

                err(1, "open");


        error = ioctl(fd, LMSTAT, &modstat);

        if (error == -1)

                err(1, "ioctl");


        printf("syscall no: %lun", modstat.offset);    


        error = syscall(modstat.offset, atoi(argv[1]), argv[2]);

        if (error == -1)

                err(1, "syscall");

        

        exit(0);

}


Notice how we query the status of the module using ioctl() to get its offset. Generally the permissions on /dev/lkm don't allow unprivileged users to do this, but it can perhaps be used for custom installation programs when installing new devices. It can also be obtained from modstat(8) as shown above. 

So our program takes an integer and string argument and uses our new system call. Lets take it for a run: 


# cc -o calltest calltest.c

# ./calltest 4 beers

syscall no: 210

# dmesg | tail -1

4 beers

#


To unload the module, it is generally best to use modunload(8): 

# modunload -n ourcall

#


You can also unload modules by their id, as appears in modstat. Lets check our module unloaded ok: 

# dmesg | tail -1

bye!

#


Now lets have a look at devices. 

Device Driver Modules 


Device modules have a lot of similarity with system call modules. They have an external entry point, a handler if desired, along with module specific code. In this case the module specific code will be the operations vector for our device. In this example we will look at a simple character device that only supports the open, close, read and ioctl operations. Before we get into its internals, lets have a look at how the lkm treats devices. 


This is the definition for a loadable device driver: 


struct lkm_dev {

        MODTYPE lkm_type;

        int     lkm_ver;

        char    *lkm_name;

        u_long  lkm_offset;

        DEVTYPE lkm_devtype;

        union {

                void    *anon;

                struct bdevsw   *bdev;

                struct cdevsw   *cdev;

        } lkm_dev;

        union

        {

                struct bdevsw bdev;

                struct cdevsw cdev;

        } lkm_olddev;

};


First we have the module type (in this case it will be LM_DEV), then the version number of the lkm implementation, then its name and its position in the cdevsw[] or bdevsw[] table. Next comes the device type, either a character device or block device specified by LM_DT_CHAR or LM_DT_BLOCK respectively. Then comes our new set of operations for the device and space to store the old operations vector (if any) when the module is loaded. This structure is initialised by the macro MOD_DEV: 

MOD_DEV("ourdev", LM_DT_CHAR, -1, &cdev_ourdev)


First we pass the name we want to reference our module with and the type of the device, in this case it is a character device. Next comes the slot in cdevsw[] where we want its vector placed, as with the system call example, -1 means we are unfussed and for lkm to place it in the next available slot. If there are no free slots, ENFILE ("Too many open files in system") will be returned. Finally we pass the initialised struct cdevsw of our operations for the device. 

Our character device will support four operations, open, close, read and ioctl. It isn't a device that does anything of much use, it will store a string and a number which can be set and retrieved using ioctl() and the string can also be retrieved using read(). Internally we use a structure defined as this: 


#define MAXMSGLEN 100


struct ourdev_io {

        int value;

        char msg[MAXMSGLEN];

};


When the module is first loaded, we initialise our value to 13 and creatively use "hello world!" as our string. This is done in the handler, and only done on load. We also define two simple ioctl()'s for setting and getting the current value of the internal structure. These both take a struct ourdev_io as an argument, and perform the appropriate action depending on the ioctl used. 

In the entry point to our module, again we use the DISPATCH macro but this time only providing a function for actions on load. In the handler we also print out the modules name. Being able to access the structure that lkm has can be useful for debugging, for example when what seems to be a correctly written module refuses to load. 


This is the complete code for our device (chardev.c): 


#include <sys/param.h>

#include <sys/fcntl.h>

#include <sys/systm.h> 

#include <sys/ioctl.h>

#include <sys/exec.h>

#include <sys/conf.h>

#include <sys/lkm.h>


#include "common.h"


/* 

 * prototypes for our supported operations, namely open, close, read and ioctl 

 */


int     ourdevopen __P((dev_t dev, int oflags, int devtype, struct proc *p));

int     ourdevclose __P((dev_t dev, int fflag, int devtype, struct proc *p));

int     ourdevread __P((dev_t dev, struct uio *uio, int ioflag));

int     ourdevioctl __P((dev_t dev, u_long cmd, caddr_t data, int fflag, 

                        struct proc *p));

int     ourdev_handler __P((struct lkm_table *lkmtp, int cmd));


/* 

 * struct ourdev_io is defined in common.h, our device will use the ioctl call

 * to get and set its values, along with the read operation on the device.

 */


static struct ourdev_io dio;


/* 

 * here we initialise the operations vector for our device 

 */


cdev_decl(ourdev);

static struct cdevsw cdev_ourdev = cdev_ourdev_init(1, ourdev);


/* 

 * Initialise an internal structure for the lkm interface. The first argument

 * is the name of the module, which will appear when viewed with modstat, the

 * second is the type of the device, in this case LM_DT_CHAR for a character 

 * device. Thirdly we have the position in the cdevsw[] table we want our 

 * operations structure stored. As with the system call, the value -1 means we

 * dont mind where it is and the next available slot should be allocated. 

 * Finally we pass our initialised struct cdevsw

 */


MOD_DEV("ourdev", LM_DT_CHAR, -1, &cdev_ourdev)


/*

 * The actions for when the device is opened, in this case just say hello 

 */


int

ourdevopen(dev, oflags, devtype, p)

        dev_t dev;

        int oflags, devtype;

        struct proc *p;

{

        printf("device opened, hi!n");

        return(0);

}


/*

 * Actions for when the device is closed, again just print a small message 

 */


int

ourdevclose(dev, fflag, devtype, p)

        dev_t dev;

        int fflag, devtype;

        struct proc *p;

{

        printf("device closed! bye!n");

        return(0);

}


/*

 * Actions for the read operation on the device, here we copy out the current

 * value of the string stored in our internal struct ourdev_io. 

 */


int

ourdevread(dev, uio, ioflag)

        dev_t dev;

        struct uio *uio;

        int     ioflag;

{

        int resid = MAXMSGLEN;

        int error = 0;


        do {

                if (uio->uio_resid < resid)

                        resid = uio->uio_resid;


                error = uiomove(dio.msg, resid, uio);   


        } while (resid > 0 && error == 0);


        return(error);

}


/* 

 * Code for the ioctl operation. We define two possible operations, one for 

 * reading the current values of the internal struct ourdev_io, and one for

 * setting the values. We default to returning the error "Inappropriate ioctl 

 * for device".

 */


int

ourdevioctl(dev, cmd, data, fflag, p)

        dev_t dev;

        u_long cmd;

        caddr_t data;

        int fflag;

        struct proc *p;

{

        struct ourdev_io *d;

        int error = 0;


        switch(cmd) {

        case ODREAD:


                d = (struct ourdev_io *)data;

                d->value = dio.value;

                error = copyoutstr(&dio.msg, d->msg, MAXMSGLEN - 1, NULL);


                break;


        case ODWRITE:


                if ((fflag & FWRITE) == 0)

                        return(EPERM);


                d = (struct ourdev_io *)data;

                dio.value = d->value;

                bzero(&dio.msg, MAXMSGLEN);

                error = copyinstr(d->msg, &dio.msg, MAXMSGLEN - 1, NULL);


                break;


        default:

                error = ENOTTY;

                break;

        }

        

        return(error);

}


/*

 * Our external entry point. Much like the system call example, we have a 

 * handler for when the module is loaded, but unlike the system call we take

 * no special action when the module is unloaded.

 */


int

ourdev(lkmtp, cmd, ver)

        struct lkm_table *lkmtp;

        int cmd;

        int ver;

{

        DISPATCH(lkmtp, cmd, ver, ourdev_handler, lkm_nofunc, lkm_nofunc)

}


/*

 * Our handler for when the module is loaded. We set up our internal structure

 * with some initial values, which can later be changed using ioctl(2). This 

 * will only be used when the module is loaded, but we check the action anyway.

 */


int

ourdev_handler(lkmtp, cmd)

        struct lkm_table *lkmtp;

        int cmd;

{

        struct lkm_dev *args = lkmtp->private.lkm_dev;

        

        if (cmd == LKM_E_LOAD) {

                dio.value = 13;

                strncpy(dio.msg,"hello world!n", MAXMSGLEN - 1);

                printf("loading module %sn", args->lkm_name);

        }


        return 0;

}


This time when installing we will use the -p option to modload(8), which enables us to specify a shell script to be run if the module was installed successfully. In this case, we will use a rather quick and dirty shell script to create a device in /dev using mknod(8), called '/dev/ourdev'. If a post install program is specified, it is always passed the module id as the first argument and the module type as the second argument. If the module is a system call it is passed its system call number in the third argument, in the case of a device module it is passed its major number. 

This is the shell script (dev-install.sh): 


#!/bin/sh

MAJOR=`modstat -n ourdev | tail -1 | awk '{print $3}'`

mknod -m 644 /dev/ourdev c $MAJOR 0

echo "created device /dev/ourdev, major number $MAJOR"

ls -l /dev/ourdev


Compile: 

# cc -D_KERNEL -I/sys -c chardev.c

#


And install: 

# modload -o ourdev.o -eourdev -p ./dev-install.sh chardev.o

Module loaded as ID 0

created device /dev/ourdev, major number 29

crw-r--r--  1 root  wheel   29,   0 Jul 10 05:16 /dev/ourdev

#


Checking our dmesg: 

# dmesg | tail -2

loading module ourdev

DDB symbols added: 140232 bytes

#


We can now read directly from the device, to do this we'll use dd(1): 

# dd if=/dev/ourdev of=/dev/fd/1 count=1 bs=100

hello world!

1+0 records in

1+0 records out

100 bytes transferred in 1 secs (100 bytes/sec)

#


Now we can check that our ioctl()'s work as expected with a test program. First here's the include that both the module code and our sample code uses (common.h): 

#define MAXMSGLEN 100


struct ourdev_io {

        int value;

        char msg[MAXMSGLEN];

};


#define ODREAD  _IOR('O', 0, struct ourdev_io)

#define ODWRITE _IOW('O', 1, struct ourdev_io)


#ifdef _KERNEL


/* open, close, read, ioctl */

#define cdev_ourdev_init(c,n) { 

        dev_init(c,n,open), dev_init(c,n,close), dev_init(c,n,read), 

        (dev_type_write((*))) lkmenodev, dev_init(c,n,ioctl), 

        (dev_type_stop((*))) lkmenodev, 0, (dev_type_select((*))) lkmenodev, 

        (dev_type_mmap((*))) lkmenodev }


#endif /* _KERNEL */


Now this is the program we'll use to test (chardevtest.c): 

#include <sys/types.h>

#include <sys/ioctl.h>


#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <fcntl.h>

#include <unistd.h>

#include <err.h>


#include "common.h"


int 

main(void)

{

        struct ourdev_io a;

        int error, fd;


        fd = open("/dev/ourdev", O_WRONLY);

        if (fd == -1)

                err(1, "open");


        error = ioctl(fd, ODREAD, &a);

        if (error == -1)

                err(1, "ioctl");


        printf("%d %s", a.value, a.msg);

        

        bzero(a.msg, MAXMSGLEN);


        strlcpy(a.msg, "cowsn", sizeof(a.msg));

        a.value = 42;


        error = ioctl(fd, ODWRITE, &a);

        if (error == -1)

                err(1, "ioctl");


        bzero(&a, sizeof(struct ourdev_io));            


        error = ioctl(fd, ODREAD, &a);

        if (error == -1)

                err(1, "ioctl");


        printf("%d %s", a.value, a.msg);

        

        close(fd);

        

        exit(0);

}


First it reads the existing values, then replaces them with its own. Finally it reads the new values and prints them out, just to make sure they were replaced ok. 

Compile: 


# cc -o chardevtest chardevtest.c

#


And run: 

# ./chardevtest

13 hello world!

42 cows

#


Checking with dd(1) again shows the internal string is now 'cows'. 

Virtual File System Modules 


Adding a virtual file system is very easy. If you're developing a new file system or writing support for an existing file system you just have to write an entrypoint for the module. Similarly if you are debugging an existing file system, all that is needed is an entrypoint. You do have to make sure your kernel is compiled without the target file system support. 


The structure used for vfs modules is defined as this: 


struct lkm_vfs {

                MODTYPE lkm_type;

                int     lkm_ver;

                char    *lkm_name;

                u_long  lkm_offset;

                struct vfsconf  *lkm_vfsconf;

};


As with the above examples we have a module type (LM_VFS), a version number, a name and an offset. In the case of vfs modules, the offset will be un-used. Finally we have a pointer to a vfsconf structure which will contain the virtual file system's operations vector, among other things (struct vfsconf is defined in /usr/include/sys/mount.h). 

This structure is initialised with the MOD_VFS macro like this: 


MOD_VFS("nullfs", -1, &nullfs_vfsconf)


The first argument is the name of our module, the second is the offset it will use, and in the case of vfs modules it doesn't matter. The final argument is the initialised vfsconf structure for our file system. 

In the entry point for your module, you must call vfs_opv_init_explicit and vfs_opv_init_default to allocate and initialise the operations vector and to set a default operation for the vector. For file systems compiled into the kernel, this is done at boot if they have an entry in vfs_opv_desc[] defined in /usr/src/sys/kern/vfs_conf.c. When the file system is loaded, it will be added to the kernel's linked list of vfsconf structures and have its _init operation called. 


An important note when using more than one source file is that when linking with ld to create the object file for modload(8), you must use the '-r' flag to create a relocatable object file. This is because modload(8) will use ld(1) when linking your module with the kernel. You can use the '-d' flag to modload(8) to see arguments passed to internal ld(1) run. 


Here is the complete source for a module using nullfs (nullmod.c): 


#include <sys/param.h>

#include <sys/ioctl.h>

#include <sys/systm.h>

#include <sys/conf.h>

#include <sys/mount.h>

#include <sys/exec.h>

#include <sys/lkm.h>

#include <sys/file.h>

#include <sys/errno.h>


/* 

 * Structures for the operations of the file system

 * referenced from /usr/src/sys/miscfs/nullfs/

 */


extern struct vfsops null_vfsops;

extern struct vnodeopv_desc null_vnodeop_opv_desc;


struct vfsconf nullfs_vfsconf = {

        &null_vfsops, MOUNT_NULL, 9, 0, 0, NULL, NULL

};


/* 

 * Declare our module structure, passing a name, offset (irrelevant for vfs

 * modules) and the initialised vfsconf structure for our file system.

 */

 

MOD_VFS("nullfs", -1, &nullfs_vfsconf)


/*

 * Our external entry point. We just initialise the file system and use

 * the DISPATCH macro, in this case not using a handler at all.

 */ 


int

nullfsmod(lkmtp, cmd, ver)

        struct lkm_table *lkmtp;

        int cmd;

        int ver;

{

        vfs_opv_init_explicit(&null_vnodeop_opv_desc);

        vfs_opv_init_default(&null_vnodeop_opv_desc);


        DISPATCH(lkmtp, cmd, ver, lkm_nofunc, lkm_nofunc, lkm_nofunc)

}


Compiling and Installing: 

(additional source taken from /usr/src/sys/miscfs/nullfs) 


# cc -D_KERNEL -I/sys -c null_subr.c

# cc -D_KERNEL -I/sys -c null_vfsops.c

# cc -D_KERNEL -I/sys -c null_vnops.c

# cc -D_KERNEL -I/sys -c nullmod.c

# ld -r -o nullfs.o null_vfsops.o null_vnops.o null_subr.o nullmod.o

# modload -o nullfsmod -enullfsmod nullfs.o

# modstat

Type     Id Off Loadaddr Size Info     Rev Module Name

VFS       0  -1 e0b84000 0003 e0b860d0   2 nullfs

#


And we're done. 

Miscellaneous Modules 


These modules can be used when writing something that doesn't fit into the predefined categories. In this example we will add some verboseness to the networking stack, printing out some information on incoming TCP packets. 


When writing a misc module, it is up to us to make sure sanity checking takes place, for example, not trying to load the module more than once. Also, it is up to us to "wire in" the module to the kernel. This is done in the handler function we specify for when the module is being loaded or unloaded. 


The structure representing a miscellaneous module is defined as this: 


struct lkm_misc {

        MODTYPE lkm_type;

        int     lkm_ver;

        char    *lkm_name;

        u_long  lkm_offset;

};


We have the module type first (in this case LM_MISC), the the version of lkm being used, the name of the module and its offset value. In the example shown here the offset value will be unused, but in the example provided in /usr/share/lkm/misc (adding a system call) the offset is used to mark the new system calls position in the system call table. It is up to the module writer to make use of the offset field, if need be. 

This structure is initialised using the MOD_MISC macro: 


MOD_MISC("tcpinfo")


It is passed only one argument, specifying the modules name. 

When our module is loaded, we change a pointer to the tcp_input function to point to our specified new_input function. This will print out some information if the mbuf it is passed represents a packet header, then call the original tcp_input function. Before we do this we provide some sanity checking by making sure the module has not already been loaded. 


A few notes on this module: First off its probably not a good idea to load this on a system that is doing a lot of TCP traffic, the printf()'s could possibly slow things up quite a bit. Hopefully you're not using a production environment for development :). Secondly, this is loosely based on a FreeBSD module by pigpen@s0ftpj.org. 


This is the complete module (tcpmod.c): 


#include <sys/param.h>

#include <sys/systm.h>

#include <sys/mbuf.h>

#include <sys/exec.h>

#include <sys/conf.h>

#include <sys/lkm.h>

#include <sys/socket.h>

#include <sys/protosw.h>

#include <net/route.h>

#include <net/if.h>

#include <netinet/in.h>

#include <netinet/in_systm.h>

#include <netinet/ip.h>

#include <netinet/in_pcb.h>


/*

 * We will modify the entry for TCP in this structure.

 */


extern struct protosw   inetsw[];


/* 

 * Our prototypes 

 */


extern int        lkmexists __P((struct lkm_table *));

extern char      *inet_ntoa __P((struct in_addr));


static void       new_input __P((struct mbuf *, ...)); 

static void     (*old_tcp_input) __P((struct mbuf *, ...));


/*

 * Declare and initialise our module structure

 */


MOD_MISC("tcpinfo")


/*

 * Our handler function, used for load and unload.

 */


int

tcpmod_handler(lkmtp, cmd)

        struct lkm_table *lkmtp;

        int cmd;

{

        int s;


        switch(cmd) {


        case LKM_E_LOAD:

                

                /*

                 * Provide some sanity checking, making sure the module

                 * will not be loaded more than once.

                 */


                if (lkmexists(lkmtp))           

                        return(EEXIST);

                

                /*

                 * Block network protocol processing while we modify

                 * the structure. We are changing the pointer to the

                 * function tcp_input to our own wrapper function.

                 */ 


                s = splnet();

                old_tcp_input = inetsw[2].pr_input;

                inetsw[2].pr_input = new_input;

                splx(s);        


                break;


        case LKM_E_UNLOAD:


                /*

                 * Restore the structure back to normal when we 

                 * are unloaded. 

                 */


                s = splnet();

                inetsw[2].pr_input = old_tcp_input;

                splx(s);

                

                break;

        }


        return(0);

}


/*

 * Our external entry point, nothing to do but use DISPATCH

 */


int

tcpinfo(lkmtp, cmd, ver)

        struct lkm_table *lkmtp;

        int cmd;

        int ver;

{

        DISPATCH(lkmtp, cmd, ver, tcpmod_handler, tcpmod_handler, lkm_nofunc)

}


/*

 * Our tcp_input wrapper. If the mbuf represents a packet header, print

 * out the total length of the packet, the interface it was received on

 * and its source address. Then continue on with the original tcp_input.

 */


static void

new_input(struct mbuf *m, ...)

{

        va_list ap;

        int iphlen;

        struct ifnet *ifnp;

        struct ip *ip;


        va_start(ap, m);

        iphlen = va_arg(ap, int);

        va_end(ap);

        

        if (m->m_flags & M_PKTHDR) {

                ifnp = m->m_pkthdr.rcvif;

                ip = mtod(m, struct ip *);

                printf("incoming packet: %d bytes ", m->m_pkthdr.len);

                printf("on %s from %sn", ifnp->if_xname, inet_ntoa(ip->ip_src));

                 

        }

                

        (*old_tcp_input)(m, iphlen);


        return;

}


Compile and Install: 

# cc -D_KERNEL -I/sys -c tcpmod.c

# modload -o tcpinfo.o -etcpinfo tcpmod.o


Generate some tcp traffic and check your dmesg: 

# dmesg | tail -3

incoming packet: 1500 bytes on ne3 from 129.128.5.191

incoming packet: 1205 bytes on ne3 from 129.128.5.191

incoming packet: 52 bytes on ne3 from 129.128.5.191

#


And we're done. 

Conclusion 


Hopefully you will have enough knowledge to develop you own modules, whether using them for debugging existing code or developing new code from scratch. Modules can speed the development process considerably by cutting down on time spent re-compiling new kernels and rebooting. 


Remember to restore your securelevel once development has finished. 


References 

lkm(4), modload(8), modstat(8), modunload(8) 

/usr/src/sys/kern/kern_lkm.c 

/usr/src/sys/sys/lkm.h 

/usr/share/lkm
