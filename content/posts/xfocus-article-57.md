---
title: "如何隐藏你的踪迹"
date: 2000-06-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-57"
---

(quack_at_xfocus.org)

################################################

               #                                              #

               #               如何隐藏你的踪迹               #

               #                                              #

               ################################################


                       第一章   理论篇


                              I. 概述

                             II. 思想认识(MENTAL)

                            III. 基础知识

                             IV. 高级技巧

                              V. 当你受到怀疑时...

                             VI. 被捕

                            VII. 有用的程序

                           VIII. 最后的话

     I. 概述

     ----------------------------------------------------------------------


 >>  译者注:本文是德国著名hacker组织"The Hacker's Choice"的96年写的一篇文章,

 >>  但今天读来仍颇有收获,就象他自己说的:"即使是一个很有经验的hacker也能从这

 >>  里学到一些东西".在翻译的过程中对原文做了一些改动,也加入了一些自己的理解,

 >>  不当之处,还请赐教.

 >>                                              

 

     注意 : 本文分为两部分.

            第一部分讲述了一些背景和理论知识.

            第二部分通过具体的实例教你一步一步了解该做什么和不该做什么.

            如果你懒得看完全部文章,那就只读第二部分吧.它主要是写给那些

            Unix hack新手看的.

            


     如果你把尽快得到最新的exploits当成最重要的事的话,那我要说-你错了.


>>   译者注:exploits可以理解为"漏洞",不过我并不想这么翻,翻过来总感觉怪

>>   怪的,所以我还是保留了原文.文中还有一些地方也是如此处理,不再一一注明


     一旦警察没收了你的计算机、你的所有帐户都被取消、你的一切活动都被监视

     的时候,即便是最好的exploit对你又有什么用呢?

     我不想听那些辩解的话.

                不,最重要的事应该是不要被捕!

     这是每个hacker都应该明白的第一件事.因为在很多情况下,特别是当你首次

     hack一个由于饱受入侵之苦而开始对系统安全敏感的站点时,你的第一次hack

     也许就将成为你最后一次hack.

     

     所以请仔细阅读所有章节!

     即使是一个很有经验的hacker也能从中学到一些东西.

     


     下面是各节的简介:

             节 I   - 你现在正在读的

             节 II  - 思想认识

                       1. 动机

                       2. 为什么你必须要谨慎(paranoid)

                       3. 怎样才能谨慎

                       4. 保持谨慎

                      

             节 III - 在你开始hack前应当知道的基本知识

                      1. 前言

                      2. 自身安全

                      3. 自己的帐户

                      4. log文件

                      5. 不要留下痕迹

                      6. 你应当避免的事

             节 IV  - 你该了解的高级技巧

                      1. 前言

                      2. 阻止任何跟踪

                      3. 找到并处理所有的log文件

                      4. 检查syslog设置和log文件

                      5. 检查安装的安全程序

                      6. 检查系统管理员  

                      7. 怎样修正checksum检查软件

                      8. 注意某些用户的安全陷阱(诡计?)

                      9. 其他

             节 V   - 一旦你受到怀疑你该怎么做

             节 VI  - 当你被捕时该做的与不该做的

             节 VII - 一些用于隐藏痕迹的程序的列表

             节 VIII- 最后的话,作者想说的一些废话


     请仔细阅读,开动脑筋.

     

     

     

     

     

    II. 思想认识(MENTAL)

    

>>      译者注:这一节的目的主要是提醒你树立正确的"hack"观 ;)    

     ----------------------------------------------------------------------


          内容:           1. 动机

                         2. 为什么你必须要谨慎(paranoid)

                         3. 怎样才能谨慎

                         4. 保持谨慎

>>      译者注:paranoid的意思是"患偏执狂的",在这里可能是当

>>      "小心谨慎"来讲吧.


   * 1. 动机 *

     

     不管做什么事,信念总是取得成功的一个关键.

     

     它是你的动力源泉,它激发你去奋斗,自我约束,小心谨慎而又面对现实,准确的估

     计风险,它也能让你去做你不喜欢做但又非常重要的事情(即使你现在就想去游泳).

     如果你不激励自己去编制重要工具,等候恰当的时机去攻击目标,那你永远不

     能成为真正的hacker.

     

     一个成功而又优秀的hacker必须满足这些要求.它就象健身和节食---如果你

     真正努力去做,你就能成功.

     


   * 2. 为什么你必须要谨慎 *

     当然,小心谨慎并不会让你的生活变得更幸福.

     然而如果你从不做最坏的打算,任何事情都能击倒你,让你失去平衡.你正在做的

     事会让你冒很大风险.而在你正常的生活中你并不需要担心警察,小偷什么的.但

     如果你从另一方面考虑,你要知道你正在给别人的生活带来麻烦和恶梦--他们很

     想阻止你.

     尽管你不认为这是犯罪.但当警察迅速逮捕每个可能被牵扯的人时,你会发现一件

     很悲惨的事:你是有罪的除非你能证明你无罪!

     一旦你得到了一个hacker的"污名",你就永远不能将其去除.一旦你有了犯罪纪录,

     你将很难找到一份工作.特别是没有软件公司甚至没有与计算机有关的公司会聘用

     你,他们会害怕你的技术.你也许不得不移民...

     一旦跌倒了,能再爬起来的只是少数人.


     要小心谨慎!

     要保护好你自己!

     记住你得到的一切都可能失去!

     绝不为做额外的反跟踪工作而感到愚蠢!

     绝不为如果别人嘲笑你太谨慎而烦心!

     决不要因为太懒或者厌倦而放弃修改log文件!

     一名hacker必须%100的完成他的"工作"!

     


   * 3. 怎样才能小心谨慎 *

   

     如果你读了上面的话并且你认为那是对的,那就容易了---你已经变得小心谨慎了

     但这必须要变成你生活中的一部分才行,当你总是考虑究竟是谁告诉你了那些事,

     考虑你的电话和email可能已被监视的时候,那它已经变成你生活的一部分了.


     如果上面这些还不能帮你,那么考虑一下如果你被捕会发生什么.

     你的女友还会站在你这边吗?你想看到你父母为你流泪吗?你想丢掉饭碗

     或学业吗?

     

     不要给这一切以发生的机会!


     如果这还不能警醒你:

     离HACKING远点儿!!!

     对整个hacker社会和你的朋友来说,你都是个危险人物!

     


   * 4. 保持谨慎 *

     我希望现在你明白为什么小心谨慎的重要性了.

     所以保持谨慎.一个错误或者一次偷懒都可能彻底毁掉你的生活和事业.

        

     在做一件事时应时刻记着你的动机是什么.      

     

>>   译者注:这部分是让你知道你正在干什么及你的处境.如果你不想让你成为无聊

>>   记者津津乐道的话题---"某地破获重大黑客案...",那就多看看,多想想.要知

>>   道,自己是这种新闻的主角和看别人的新闻可完全不是一个感觉.

>>   所以要:谦虚谨慎,戒骄戒躁    :-)


     III. 基础知识

     ----------------------------------------------------------------------


          内容 :          

                         1. 前言

                         2. 自身安全

                         3. 自己的帐户

                         4. log文件

                         5. 不要留下痕迹

                         6. 你应当避免的事


   * 1. 前言 *

     

     在你开始你的初次hack之前,你应当知道这些并且进行些练习.这些都是非常基本

     的,不知道这些你很快就会有麻烦了.即便是一名很有经验的hacker也能从中得到

     一些新的提示.


   * 2. 自身安全 *

     

     系统管理员读了你的email吗?

     你的电话被警察监听了吗?

     警察没收了你存有所有hacking数据的计算机吗?

     

     如果你不接收可疑的email,不在电话里谈论hacking/phreaking的话题,在你的硬盘

     上也没有敏感和私人数据的话,那你不必担心上面那些情景.但那样你就并不是一个

     hacker.每个hacker和phreaker都与其他人保持联系并把他的数据保存在某个地方.

    

     加密所有敏感数据!!!

     在线硬盘加密程序是非常重要和有用的:

         在internet上游很多好的免费硬盘加密程序,它们对你的操作系统来说是完全

         透明的.下面所列的几个软件都是经过测试的,是hacker's的首选工具:

          - 如果你用MsDos,你可以使用SFS v1.17或者SecureDrive 1.4b

          - 如果你用Amiga,你可以使用EnigmaII v1.5

          - 如果你用Unix,你可以使用CFS v1.33


>>   译者注:在win9x下可以考虑emf,iprotect...          


     文件加密软件: 你可以使用任何一种加密软件,但它应该是使用一种众所周知的

     安全加密机制.绝对不要用那些被出口的加密程序,它们的有效密钥长度被缩短了!

          - Triple DES

          - IDEA

          - Blowfish (32 rounds)

     加密你的Email!

          - PGP v2.6.x 是个不错的工具.

     如果你想讨论重要的事情的话,加密你的电话.

          - Nautilus v1.5a 是迄今最好的

     当你连到一个unix系统时加密你的终端.

     一些人可能正在sniffing或者监视你的电话线:

          - SSH 是最安全的

          - DES-Login 也不错


>> 译者注:- SSL 基于SSL的一些软件也可以一试


     用强壮的不可猜测的,不在任何字典中的密码.它应当看起来象随机的但又容易记

     忆.如果密码长度可以比10个字符更长,那就用更长的.可以从书中抽取一句话,并

     略作修改.请将你的hacker朋友的电话号码加密两遍.如果你不加密,你应当从公用

     电话给他打电话.


>>   译者注:其实有个好记又难猜的密码并不难,例如考虑句子"I'm a haxor!"可以从中抽

>>   取几个单词组成I'mhaxor,好象没有数字,呵呵,用"eleet"的hacker语言,haxor=h4x0r

>>   所以我们的口令可以是:I'mh4x0r(我是hacker).这样的密码恐怕只能用暴力破解了.     


     如果你对hacking有了深入了解,你应当加密所有的东西!


     为你的数据做个备份,当然要先加密,把它放在一个隐秘的地方,最好不要在家里.

     所以即使你因为失误,火灾或警察搜捕等原因丢失了数据,你还可以得到备份数据.

     

     只有当你真的需要它们时才写出来,否则将它们放在一个机密文件或加密分区里更

     安全.一旦你不需要它们了,烧掉那些纸.你也可以用只有你自己知道的加密机制将

     它们写下来,但不要告诉任何人,也别太经常的使用它.也许它很容易被分析和破解

 

     真正沉稳和谨慎的hackers应该考虑实施干扰方案.警察,间谍,其他hacker能监视你

     的举动.一个拥有先进设备的人可以获得他想要的任何东西:

     计算机发射的电子脉冲可以从100米以外的距离被截获,可以显示你的监视器屏幕,

     监听你的私人谈话,确认键盘敲击时的高频信号等等...所以各种可能性总是存在的.

     成本低廉的应付方法就是采用电子脉冲干扰发射机,商店里就有卖的.如果你不想让


>>   译者注:不知道我们的商店里有没有卖的.;-)     


     任何人监视你,我认为这些还不够...

     

     

     

     


   * 3. 你自己的帐户 *

     下面让我们谈谈你自己的帐户.它就是你在学校/公司/ISP那里得到的帐户,它

     总是与你的真实姓名联系在一起,所以在使用它时绝对不要违背下面的原则:

     

     永远不要用你的真实帐户做任何非法或者惹人怀疑的事!

     永远不要试图从你的真实帐户telnet到任何被hacked主机去!

     当然可以用这个帐号订阅安全mailing lists.

     但任何与hacking有关的东西都必须加密或者立刻销毁.

     决不要在你帐号下保存hacking或security工具.

     尽量用POP3连到你的mailserver下载或者删除你的邮件(如果你对unix比较熟悉,

     还可以直接telnet到POP3端口执行下载或者删除命令).

     决不要泄漏你的真实email给你不信任的人,只把它给你信任的人,他们也应当是比较

     注意安全问题的人,否则如果他们被捕,下一个就是你了(或许他们根本就是警察,而不

     是hacker.).

     与其他的hacker用email交流时必须要用PGP加密,因为系统管理员经常偷看用户目录,

     甚至读区别人的email!!其他的hacker也可能hack你们的站点并试图得到你的数据.

     

     绝不要用你的帐号表明你对hacking感兴趣!

     对安全感兴趣可以,但不要再进一步了.

     

>>   译者注:与别人交流时可以申请免费信箱,最好是国外的,比如hotmail之类,登陆时注意最好

>>   通过proxy.自己的真实信箱应当只用来进行一般的正常通信,与朋友/老师/同事...


     

   * 4. LOG文件 *

     

     有三个重要的log文件:

          WTMP - 记录每次登录的信息,包括登陆/退出的时间,终端,登录主机ip

          UTMP - 在线用户记录

          LASTLOG - 记录用户上次是从哪里登录的

     当然还有其他的log,它们将在"高级技巧"一节种讨论.每次通过telnet,ftp,rlogin,rsh

     的登录都会被记录到这些文件中.如果你正在hacking,把自己从这些记录中删除就是很

     重要的了.否则他们会:

          a) 准确的发现你什么时候在搞hacking活动

          b) 发现你从那个站点过来

          c) 知道你在线的时间有多长,以便计算你给他们造成的损失


     绝对不要删除这些log文件!!!那等于通知管理员:"嗨,你的机器上有个hacker!".找一个

     好程序来修改这些log.ZAP(或ZAP2)经常被认为是最好的但事实上它并不是.它只是简单

     的用0来填充用户上次登陆的数据段.CERT已经发布了一个简单的程序用来检查这些全零

     数据项.所以这样也会很容易就让人知道现在有个hacker在活动,这样你所有的工作就没

     有意义了.ZAP的另外一个缺陷是当它找不到那些log文件时,它并不报告.所以在编译之前

     必须先检查一下路径!你应该使用能改变记录内容的程序(象cloark2.c)或者能真正删掉

     记录的程序(象clear)

 

>>   译者注:     THC提供的cleara.c ,clearb.c是非常好用的清除工具.可以清除

>>   utmp/utmpx,wtmp/wtmpx,修复lastlog让其仍然显示该用户的上次登录信息(而不

>>   是你登录的信息).如果你发现你登录后没有显示上次登录信息,那很可能你的机器

>>   可能已经被人hack了,当然,即使显示正确的信息也未必就没有被hack.;-)


     一般来说要修改log你必须是root(有些老版本系统例外,它们将utmp/wtmp设成允许所有人可写)但

     如果你不能得到root权限---你该怎么做呢?

     你应该rlogin到你现在所处的主机,以便在lastlog种增加一个不是那么惹人怀疑的数据项,它将在

     该用户下次登录时被显示,如果他看到"上次从localhost登录"的信息时也许不会怀疑.


>>   译者注:这也是没有办法的办法,换了我,我就会怀疑.;)


     很多unix系统的login命令有一个bug.当你登录以后再执行一遍login命令时,它将

     用你当前的终端重写UTMP中的login from段(它显示你是从哪里来的!)

     

     那么这些log文件缺省在什么地方呢?

     这依赖于不同的Unix版本.

     UTMP : /etc 或 /var/adm 或 /usr/adm 或 /usr/var/adm 或 /var/log

     WTMP : /etc 或 /var/adm 或 /usr/adm 或 /usr/var/adm 或 /var/log

     LASTLOG :  /usr/var/adm 或 /usr/adm 或 /var/adm 或 /var/log

     在一些旧unix版本中lastlog数据被写到$HOME/.lastlog

     

   * 5. 不要留下痕迹 *

     我曾经碰到很多hacker,他们把自己从log里删除了.但他们忘记删掉他们在机器中留下

     的其他一些东西:在/tmp和$HOME中的文件

     

     Shell 记录

     一些shell会保留一个history文件(依赖于环境设置)记录你执行的命令.这对hacker来

     说确实是件很糟糕的事.

     

     最好的选择就是当你登录以后先启动一个新shell,然后在你的$HOME中查找历史纪录.

     历史记录文件: 

        sh  : .sh_history

        csh : .history

        ksh : .sh_history

        bash: .bash_history

        zsh : .history


>>   译者注:.*history是我最喜欢看的文件之一,通过它你可以了解root或用户常干些什么,

>>   从而得知他们的水平如何,如果他们只会执行"ls","pwd","cp"...那说明水平不过尔尔,无须

>>   太担心.不过如果你发现root喜欢"find / -type f -perm -04000 -exec ls -al {} \;","

>>   "vim /var/adm/messages","ps -aux( -elf) ","netstat -an"....那你就要小心一点了


     备份文件 :

        dead.letter, *.bak, *~


     在你离开前执行一下"ls -altr"看看你有没有留下什么不该留下的东西.

     

     你可以敲4个csh命令,它能让你离开时删掉这些历史文件,不留下任何痕迹.

          mv .logout save.1

          echo rm .history>.logout

          echo rm .logout>>.logout

          echo mv save.1 .logout>>.logout


>>   译者注:对于bash,有一个简单的办法就是执行一下"HISTFILE=",就是不设置bash的历史文件,

>>   这样就不会有讨厌的.bash_history了.(准确地说,是不会往$HOME/.bash_history里写了)

>>   或者退出的时候简单的敲kill -9 0 ,它会杀掉这次登录后产生的所有进程,bash也不会往.bash

>>   _history里写

          


   * 6. 你应当避免的事 *

     不要在不属于你的机器上crack口令.如果你在别人(比如说一所大学)的机器上破解口令,

     一旦root发现了你的进程,并且检查它.那么不仅你hacking的帐号保不住了,可能连你得

     到的那passwd文件也没了.那学校将会密切注视你的一举一动...

     所以得到口令文件后应该在自己的机器上破解.你并不需要破解太多的帐号,能破出几个就

     够了.

     如果你运行攻击/检测程序象ypx,iss,satan或其他的exploiting程序,应当先改名再执行它们.

     或者你可以修改源码改变它们在进程列表中显示的名字...

     

>>   译者注:这并不难,你只要在main()中将argv[]用你喜欢显示的名字替代就可以了比如argv[0]

>>   ="in.telnetd",argv[1]=""...(当然必须在程序已经从argv中读取了所需的参数之后).     


     如果某个细心的用户/root发现5个ypx程序在后台运行,他马上就会明白发生了什么.

     当然如果可能的话不要在命令行中输入参数.如果程序支持交互方式,象telnet.

     应当先敲"telnet",然后"o target.host.com"...这就不会在进程表中显示目标主机

     名.

     

>>   译者注:如果你用ftp,最好这样做:

>>   $ ftp -n

>>   $ ftp>o target.host

>>     blahblah...(一些连接信息)

>>     blahblah...(ftp server版本)

>>     ftp>user xxx

>>     ....

     

     如果你hack了一个系统---不要在任何地方放suid shell!

     最好装一些后门象(ping,quota或者login),用fix来更正文件的atime和mtime.


>>   译者注:   放suid shell是很蠢的,非常容易被root发现.

          


     IV. 高级技巧

     ----------------------------------------------------------------------


         内容 :          1. 前言

                         2. 阻止任何跟踪

                         3. 找到并处理所有的log文件

                         4. 检查syslog设置和log文件

                         5. 检查安装的安全程序

                         6. 检查系统管理员  

                         7. 怎样修正checksum检查软件

                         8. 注意某些用户的安全陷阱(诡计?)

                         9. 其他                         


   


   * 1. 前言 * 

     一旦你装了第一个sniffer开始你的hack生涯,你就应该知道并使用这些技巧!

     请运用这些技巧---否则你的hack之旅就行将结束.

     

   * 2. 阻止任何跟踪 * 

     有时候你的hacking活动会被人发现.那并不是什么大问题 - 你hacked一些站点

     可能会被关掉,但谁管它呢,赶紧离开就是了.但如果他们试图跟踪你的来路(通常

     是为了抓住你)的话那就很危险了!

     


     这一节将告诉你他们跟踪你的各种可能的方法以及你该如何应对.

     

     * 通常对系统管理员来说发现一个hacker是从哪里来的并不是什么问题:检查log记

       录(如果那个hacker真的那么蠢的话);看看hacker安装的sniffer的输出记录(也许

       里面也记下了他的连接)或者其他系统记帐软件(象loginlog等等);甚至可以用netstat

       显示所有已经建立的网络连接--如果那个hacker正在线的话,那他就被发现了.

       这就是为什么你需要一个gateway server(网关).

     

     * 什么是gateway server?

       它是你所"拥有"的很多服务器中的一个,你已经得到了它的root权限.你

       需要root权限去清除wtmp/lastlog/utmp等系统记录或者其他一些记帐软

       件的log文件.除此之外你不在这台机器上做任何其他的事(它只是个中转

       站).你应当定期更换gateway server,可以每隔1,2个星期更换一次,然后

       至少一个月内不再使用原来的gateway server.这样他们就很难跟踪到你

       的hacking server.

       

     * hackin server - 所有活动的出发点

       你从这些机器开始hacking.Telnet(或者更好的:remsh/rsh)到一个gateway server,

       然后再到一个目标机器.你需要有root权限以修改log.你必须每隔2-4个星期就更换

       hacking server..

       

     * 你的堡垒/拨号主机.

       这是个临界点.一但他们能跟踪回你拨号进入的机器,你就有麻烦了.只要打

       个电话给警察,再进行一次通信线路跟踪,你的hack活动就会成为历史了,也

       许是你的未来.

       在堡垒主机上你不需要得到root权限.既然你只是通过modem拨入,那里没有

       什么必须修改的记录.你应该每天用一个不同的帐号拨号进入,尽量用那些

       很少使用的.你应该找到至少2个你能拨号进去堡垒主机,每隔1-2个月更换一

       次.

       

>>     译者注:我对phreak不熟.我猜大部分的国内hacker还没什么本事能躲过电信局

>>     的跟踪.所以最好不要用别人的帐号上网,特别是那些很少上网的帐号,一旦他

>>     发现上网费用剧增,肯定会让电信局追查的,到时候你就大难临头了.如果

>>     你用那些上网频繁的人的帐号,他反倒不会注意,只会以为这个月上的太厉

>>     害了.:-)(这绝对没有鼓励你盗用别人帐号的意思,这等于盗窃,凭什么你上网

>>     要别人交钱?就凭你会用john破几个口令吗?hacker的名声就是让这些打着hacker

>>     旗号的无耻之徒败坏的.对这种人就得抓!所以我对这样的phreaker没有什么好感,

>>     你要真有本事,就别嫁祸别人,而且还要让电信局查不出来.) 说多了,咱们言归正传.


       注意: 如果你能每天拨入不同的系统(比如通过"蓝盒子"),那你就不需要那些

             hacking server了.

     * 使用蓝盒子,这样即使他们跟踪到你的堡垒主机,也不能(至少是不能很容易地)

       追踪到你的电话...

       使用蓝盒子必须小心,德国和美国的电话公司有专门的监视系统来追踪使用蓝盒

       子的人...  


       使用一个中间系统来传送你的电话将会使跟踪更加困难, 但是同样由于你使用

       一个pbx或其他的什么东西, 仍使你处于被抓的危险中. 这取决于你.


       注意在丹麦所有的电话数据均被记录!即使在你打完电话10年后,他们仍然能证明你

       曾登录过他们的拨号系统从事hack活动...       

       

     - 其他的

       如果你想运行satan,iss,ypx,nfs文件句柄猜测程序..你应当使用一个专门的服务

       器来完成.不要用这个服务器telnet/rlogin到目标服务器,只是用它来进行检测.

       

       有些程序可以bind到一个特殊端口,当一个指定到该端口的连接建立的时候,它自动

       打开一个连接连到另外一个服务器的某个端口(有些就模拟一个shell,你可以从这个

       socket daemon中"telnet"到其他机器).

       使用这种程序你不会被记录(防火墙log除外).有很多程序可以帮你完成上述功能.


>>     译者注:这种程序我常用的有datapipe.c,telbounc.c,还是很好用的.它就象是个

>>     代理服务器,但是不会有记录.:)       

       

       如果可能的话,hacking server或者gateway server应该在国外!

       因为如果你的入侵被发现,当发现你来自国外的主机时,大多数网管都会放弃追查.

       即使是警察要通过不同的国家追踪你,这也至少可以拖延2-10个星期的时间...

       

     #下面是hack过程的简图,也许对你有些帮助;-)

 

  +-------+     ~--------------->     +-------------+     +-----------+

  |+-----+|     >               >     |             |     |           |

  ||本机 || --> > 安全拨号线路  > --> |  堡垒主机   | --> | hacking   |

  |+-----+|     >               >     | (至少有3个) |     | server    |

  +-------+     ~--------------->     +-------------+     +-----------+

                                                                |

                                                                |

                                                                v

           +-----------------+             +--------+     +-----------+

           |                 |             |        |     |           |

           | 内部网络中的主机| ... <-- ... |目标主机| <-- |  gateway  |

           |                 |             |        |     |   server  |

           +-----------------+             +--------+     +-----------+


   * 3. 找到并处理所有的LOG文件 *

     找到所有的logfiles是很重要的---即使他们被隐藏.要找到它们有两种可能的方法:

     1)找到所有打开的文件.

        既然所有的log必须写到某个地方去,所以用可以用LSOF(LiSt Open Files)程序

        去检查所有打开的文件,必要的话就得修改它们.


>>   译者注:lsof由Vic Abell <abe@purdue.edu>编写,用来提供被进程打开的文件的信息,

>>   它的最新版本可以在[ftp://vic.cc.purdue.edu/pub/tools/unix/lsof](ftp://vic.cc.purdue.edu/pub/tools/unix/lsof)下找到.有趣

>>   的是,不久前有人发现lsof4.40以前的版本中存在buffer overflow问题,可以取得root

>>   权限.:-)        

           

     2) 搜索所有在你登录后有变化的文件

        在你登录后,执行"touch /tmp/check",然后可以干你的活.最后只要执行"find / 

        -newer /tmp/check -print",并检查找到的文件,如果其中有记帐文件,就应该修改

        它.注意不是所有版本的find都支持 -newer 参数.你也可以用"find / -ctime 0 

        -print" 或者 "find / -cmin 0 -print"来查找它们.


>>   译者注:我更喜欢用-exec ls -l {} \;来代替-print,因为这可以列出比较详细的信息.

>>   注意上述方法主要是针对系统记帐软件的,它可能会记录你执行的命令.对于只记录login

>>   信息的软件,它在你看到shell提示符以前就已经完成记录了.所以用这种检查是查不出来的.


     检查你找到的所有的logfiles.它们一般在/usr/adm,/var/adm或者/var/log,/var/run.

     如果它们被记录到@loghost,那你可能就有点麻烦了.你需要hack那台loghost主机去修改

     log...

     

>>   译者注:一般单纯用作loghost的机器比较难hack,因为它往往关掉了几乎所有端口,并且只

>>   允许从控制台登录.对于这样的机器,可以用DoS攻击使之瘫痪,从而失去log功能.(要hack

>>   往往比较难,要crash it则相对容易一些.;-)当然，本次登陆的记录仍然会被保存下来.

  

 

     为了处理logs,你可以用"grep -v"或者用wc统计行数后,再用"tail -10 log"察看最后10行

     ,或者用编辑器vi,emcas.


>>   译者注:如果你从a.b.c来,你可以用grep -v "a.b.c" logfile>logtemp;mv logtemp logfile;

>>   来清除所有含有a.b.c的行.如果log文件比较大,你也可以用vim来编辑.     

>>   注意这只能用来修改文本文件!!!对二进制文件的修改可能导致文件格式被破坏!!!


     如果数据文件是二进制格式的,你应当首先查明它是由什么软件产生的,然后设法找到该软件

     的源码,分析记录项的结构,自己编程修改记录.(可以利用现成的程序加以修改,比如Zap,clear

     cloak...).

     

     如果系统安装了accounting软件.你可以用zhart写的acct-clener---它非常有效!

     

     如果你必须修改wtmp,但系统又不能编译源程序也没有perl....你可以这样做,先uuencode 

     wtmp,然后运行vi,移动到最后一行,删除最后以"M"开头的4行...然后保存退出.uudecode

     .然后最后5个wtmp记录项就被删除了.;-) 注意这只在SCO unix下有效,linux下是不行的.


>>   译者注:我没有验证这个,因为没有SCO服务器.如果你要这么做,记得要先做个wtmp的备份.

     

     如果系统用wtmpx和utmpx,那你又有麻烦了..迄今我还不知道有哪个cleaner程序可以处理

     它们.你不得不自己编一个程序来完成工作.

     

>>   译者注:wtmpx和utmpx结构与wtmp和utmp类似,只要将清除utmp和wtmp的软件略加修改就可

>>   以了.而且现在已经不少现成的程序可以修改utmpx/wtmpx了.


  


   * 4. 检查SYSLOG配置和记录 *

     大部分程序都用syslog函数来记录它们需要的所有东西.因而检查syslogd的配置文件是

     很重要的.

     这个配置文件是/etc/syslog.conf - 我不会告诉你它的格式是什么/每一项是什么意思,

     自己去读它的man页.

     对你来说重要的syslog类型是kern.*,auth.*和authpriv.*.看看它们被写到哪里了,如

     果写到文件里还可以修改.如果被转发到其他主机,你必须也要hack它们.如果消息被发给

     某个用户,tty或者控制台.你能耍点小花招发很多个假消息象"echo 17:04 12-05-85 kernel

     sendmail[243]: can't resolve bla.bla.com > /dev/console"(或其他你想flood的

     的设备),让它卷屏,以隐藏你引发的信息.这些log文件是非常非常重要的!检查它们!

     


   * 5. 检查已经安装的安全程序 *

     很多注重安全的站点都通过cron运行安全检查程序.crontabs通常在/var/spool/cron/crontabs.

     检查里面所有的文件,特别是"root"文件,检查它里面都运行了什么程序.用"crontab -l root"可以

     快速的检查root crontab的内容.

   

     这些安全工具往往装在管理员的目录下比如~/bin.

     

     这些检查软件可能是 tiger, cops, spi, tripwire, l5,binaudit, hobgoblin, s3 等等...


     你必须检查它们都报告了些什么东西,看它们是否报告了一些显示出你入侵迹象的东西.

     如果是的话,你可以 - 更新软件的数据文件,是它们不再报告这种类型的消息.

                     - 可以重新编程或修改该软件使它们不再产生报告.

                     - 如果可能的话,删除你安装的后门或其他程序,并试着用其他的方法来完成

         


   * 6. 检查系统管理员 *

     对你来说了解系统管理员采取了那些安全措施是非常重要的.因此你需要知道他们经常使用哪些

     普通用户帐号.

     你可以检查root的.forward文件和alias内容.看看sulog文件,注意那些成功su成root的

     用户.检查group文件中的wheel和admin组(或者其他任何与管理员相关的组).你也可以在

     passwd文件中查找admin,也许你又能找到一个管理员帐号.

     现在你应该已经知道这台机器上谁是管理员了.进入他们的目录(如果系统不允许root读所有

     的文件,用chid.c或者changeid.c将自己的uid变成该用户的),检查他们的.history/.sh

     _history/.bash_history文件看看他们经常执行什么命令.也应当检查他们的.profile/.

     login/.bash_profile文件看看里面都设置了什么alias,是否执行了什么自动安全检查或

     logging程序.也检查他们的~/bin目录!大多数情况下被编译的安全程序被放到那里面!当然

     也要看一下他们的每一个目录(ls -alR ~/).

     如果你找到任何与安全有关的东西,请读5小节以设法绕过它们的安全保护.


   * 7. 怎样修正checksum检查软件 *

     一些管理员真得很怕hacker所以装了一些软件来检查二进制文件.如果一个二进制文件被

     改动了,下次管理员做二进制检查的时候,它将被检测到.

     那么你怎么找到是否系统安装了这样的程序,又怎样修改它们以便你能植入你的木马程序呢?

     

     注意有很多的二进制检查程序,而且要写一个也真是非常容易(15分钟就够了),你可以用一个

     小的script完成这个工作.所以如果这样的软件被安装的话要找到它们是比较困难的.注意

     有些常用安全检查程序也提供这样的检查.下面是一些应用得很广泛的软件:     


     软件名                    标准路径                        二进制文件名

    

     tripwire     : /usr/adm/tcheck, /usr/local/adm/tcheck  : databases, tripwire

     binaudit     : /usr/local/adm/audit                    : auditscan 

     hobgoblin    : ~user/bin                               : hobgoblin

     raudit       : ~user/bin                               : raudit.pl

     l5           : 编译所在目录                             : l5


     你要明白有很多种可能!这软件或数据库甚至可能放在一个正常情况下不被mount的盘上或

     者在其他主机export的NFS分区上.也可能checksum数据库是储存在一个写保护的介质上的.

     各种可能性都有!但一般情况下你只要检查上述软件是否被安装就可以了,如果没有的话,你就

     可以改变某些二进制文件.如果你没有找到那些软件,但你又知道这是一个进行了完善安全保

     护的站点的话,你就不应该改变二进制文件!它们(二进制检查软件)肯定被藏在什么地方了.


     如果你发现了这种软件被安装并且你可以修改它们(比如不是放在只读介质上,或者可以通过

     一些办法绕过限制 - 比如umount该盘然后重新mount成可写的)的话,你该怎么做呢?

     你有两种选择:

     首先你可以只检查软件的参数,然后对已经修改过的二进制文件执行一次"update"检查.

     比如用tripwire的话你可以执行" tripwire -update /bin/target ".

     第二种办法是你可以编辑要被检查的二进制文件名单 - 从中删除你改动过的二进制文件名.

     注意你也应当看看是不是连数据库文件自身也会被检查!如果是的话 - 先update再删除

     数据库文件名.

     


   * 8. 注意某些用户的安全陷阱(诡计?) *

     这种情况较少发生,这里提出来主要是为了讨论的更完全.

     一些用户(可能是管理员或者hacker)通常不象他自己的帐户被别人使用.所以他们有时候

     会在他们的启动文件里采取一点安全措施.

     所以要检查所有的以"."开头的文件(.profile,.cshrc,.login,.logout 等等),看看

     他们执行了什么命令,记录了些什么东西,以及他们的搜索路径是怎么摄制的.如果某个目录

     (比如$HOME/bin)出现在/bin的前面,你就应该检查一下那个目录的内容了...也许里面装

     了个程序"ls"或者"w",它会先记录被执行的时间然后再执行真正的程序

     也许还有些程序用来自动检查wtmp和lastlog文件是否被zap处理过,检查.rhosts,

     .Xauthority文件,或是否有sniffer正在运行...

     千万不要使用一个unix高手的帐号!

     


   * 9. 其他 *

     最后,在讨论受怀疑或被捕的话题之前,还有一些其他的事情值得引起注意.

     

     老的telnet client会export USER变量.一个了解这一点的系统管理员可以编辑telnetd

     ,从而得到所有(通过telnet登录进来的)用户名.一旦他注意到你,他就可以很容易的得知你

     是从(远方主机的)哪个帐号hack进来的.新的client(客户端程序)已经解决了了这一问题 -

     但是一个聪明的管理员仍然可以得到其他的信息以鉴别用户:UID,MAIL,HOME变量,这些变量

     仍然被export,这就可以很容易得鉴别 hacker使用的是哪个帐户.因此在你进行telnet前,

     记得要改变USER,UID,MAIL和HOME变量,如果你正处在home目录下的话也许甚至要改变PWD变

     量.

     

     在HP Unix(版本低于v10)中你可以建立隐藏目录.我不是说那些以"."开头的目录而是

     一些有特殊标志的目录.HP在v9版推出了它,但从v10版本以后就去除了(因为只有hacker

     才是用它 ;-).

     如果你执行"chmod +H directory",则directory目录就不能用"ls -al"列出.为了看

     这个隐藏目录,你需要为ls增加 -H 参数,例如:"ls -alH".

      

     

     无论什么时候,当你需要改变文件的日期时,记住你能用"touch"命令设置atime和mtime.

     你只能通过直接的硬盘读写来设置ctime.


     

     如果你在一个重要系统中安装了sniffer,一定要加密sniffer的输出或者让sniffer通过

     icmp或者udp将所有被截获的数据发送到一个由你控制的外部主机.为什么要这样做?因为

     这样即使管理员发现了sniffer(通过cpm或其他检查sniffer存在的程序),他们也不能从

     sniffer log中得知哪些东西被sniff了,所以他也不能即使提醒正被你sniff的主机.

     

     V. 当你被怀疑时...

     ----------------------------------------------------------------------


     一旦你受到怀疑(被警察或是系统管理员)你应该采取些特别的行动是他们不能得到不利你的

     证据.

     


     注意 :  如果系统管理员认为你是个hacker,

            你就是有罪的直到你被证明是无辜的!

     

     这些管理员根本不理会什么法律(有时候我认为hacker与管理员的不同仅仅在于那台计算机

     属于管理员而已).当他们认为你是个hacker的时候,你就是有罪的,没有律师为你辩护.他们

     会监视你,你的邮件,文件,甚至记录你的键盘(如果他们够利害的话).

     

     当警察被牵扯进来的时候,你的电话线也可能被监听,搜捕行动也许跟着就来了.

     

     如果你注意到你正受到怀疑,一定要保持低调!不要采取任何攻击性行动!

     最好是等上至少1到2个月,什么都不做.

     警告你的朋友不要给你发任何邮件,或者只发一些正常的/无害的邮件.如果你突然采用 PGP加密

     邮件,这会提醒正在监视的警察和管理员---你发现他们的监视了.切断与hacking有关的联系,

     写点儿文章或者编编程序,一直等到一切都过去.及主要加密你的敏感数据,销毁所有记有帐号

     数据,电话号码等等的纸张.当警察搜捕你的时候,那些东西是他们要找的最重要的东西.


     VI. 被捕

     ----------------------------------------------------------------------


     Note that this small chapter covers only the ethics and basics and

     hasn't got any references to current laws - because they are different

     for every country.


     Now we talking about the stuff you should/shouldn't do once the feds

     visited you. There are two *very* important things you have to do :

     1) GET A LAWYER IMMEDEANTELY !

        The lawyer should phone the judge and appeal against the search

           warrant. This doesn't help much but may hinder them in their work.

           The lawyer should tell you everything you need to know what the

           feds are allowed to do and what not.

           The lawyer should write a letter to the district attorney and/or

           police to request the computers back as fast as possible because

           they are urgently needed to do business etc.

           As you can see it is very useful to have got a lawyer already

           by hand instead of searching for one after the raid.

        2) NEVER TALK TO THE COPS !

           The feds can't promise you anything. If they tell you, you'll get

           away if you talk, don't trust them! Only the district attorney

           has got the power to do this. The cops just want to get all

           information possible. So if you tell them anything they'll have

           got more information from and against you.

           You should *always* refuse to give evidence - tell them that you

           will only talk with them via your lawyer.


     Then you should make a plan with your lawyer how to get you out of this

     shit and reduce the damage.

     But please keep in mind : don't betray your friends. Don't tell them

     any secrets. Don't blow up the scene.

     If you do, that's a boomerang : the guys & scene will be very angry

     and do revenge, and those guys who'll be caught because of your

     evidence will also talk ... and give the cops more information about

     *your* crimes!


     Note also that once you are caught you get blamed for everything which

     happened on that site. If you (or your lawyer) can show them that they

     don't have got evidences against you for all those cases they might

     have trouble to keep the picture of that "evil hacker" they'll try to

     paint about you at the court. If you can even prove that you couldn't

     do some of the crimes they accuse you for then your chances are even

     better. When the judge sees that false accuses are made he'll suspect

     that there could be more false ones and will become distrusted against

     the bad prepared charges against you.


     I get often asked if the feds/judge can force you to give up your

     passwords for PGP, encrypted files and/or harddisks.

     That's different for every country. Check out if they could force you

     to open your locked safe.

     If that's the case you should hide the fact that you are crypting your

     data! Talk with your lawyer if it's better for you to stand against

     the direction to give out the password - maybe they'd get evidences

     which could you get into jail for many years.


     (For german guys : THC-MAG #4 will have got an article about the german

      law, as far as it concerns hacking and phreaking - that article will

      be of course checked by a lawyer to be correct. Note that #4 will only

      discuss germany and hence will be in the german language.

      But non-germans, keep ya head up, this will be the first and last german

      only magazine release ;-)


>>译者注:这一节是讲述了如果被捕,应当做些什么.由于我们的法律和西方不同,所以我就不翻了.有

>>兴趣的可以自己看一看.主要的两点就是:1.马上找到一个律师为你处理这一切.2.不要告诉警察任

>>何东西,也不要出卖其他人.


     VII. 有用的程序

     ----------------------------------------------------------------------


     这里有一个你应该找到并使用的程序列表.不要给我发email问我在哪里找到它们 - 自己到

     hacker世界中去找!我只列出了最好的log编辑程序(见III-4和IV-3).

     其他有趣的程序还有telnet重定向程序(见IV-2),但这种程序有很多,大部分只能在1-3种

     unix类型下编译,所以列表没什么用.

     

     先节是以下几个术语:

          改变      -  将logfile中的域改成你喜欢的任意内容

          删除     -   删除你要求的记录项

          编辑     -   真正的logfile编辑器.

          重写      -  只用0字节来重写记录.

                       不要用这样的软件(e.g. zap) - 它能被检测到!

                              LOG 修改器

                              

     ah-1_0b.tar  改变记帐信息的记录

     clear.c      删除utmp,wtmp,lastlog和wtmpx中的记录

     cloak2.c     改变utmp,wtmp和lastlog中的记录.

     invisible.c  用预设值重写utmp,wtmp和lastlog

                  所以它比zap更好.注意看,有好多inv*.c!

     marryv11.c   编辑utmp, wtmp, lastlog 和 accounting 数据 - 最好的!

     wzap.c       删除wtmp中的记录

     wtmped.c     删除wtmp中的记录

     zap.c        重写utmp, wtmp, lastlog - 不要用它!它会被检测到!


     VIII. 最后的话

     ----------------------------------------------------------------------


     最后的话:

     不要被捕,记住这些技巧.

     如果有人想更正一些错误或者发表一些意见,或对某个话题需要更多的信息,甚至认为我遗漏了

     一些东西 - 请让我知道.

     

                         van Hauser


Type Bits/KeyID    Date       User ID

pub  1024/3B188C7D 1995/10/10 van Hauser/THC of LORE BBS
