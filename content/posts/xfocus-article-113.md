---
title: "揭开木马的神秘面纱"
date: 2001-03-03T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-113"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

前言

　　在网上，大家最关心的事情之一就是木马：最近出了新的木马吗？木马究竟能实现

哪些功能？木马如何防治？木马究竟是如何工作的？本文试图以我国最著名的木马之

 - 冰河为例，向大家剖析木马的基本原理，为大家揭开木马的神秘面纱。

　　木马冰河是用C++Builder写的，为了便于大家理解，我将用相对比较简单的VB来说

明它，其中涉及到一些WinSock编程和Windows API的知识，如果你不是很了解的话，请

去查阅相关的资料。


一、基础篇（揭开木马的神秘面纱）

　　无论大家把木马看得多神秘，也无论木马能实现多么强大的功能，木马，其实质只

是一个网络客户/服务程序。那么，就让我们从网络客户/服务程序的编写开始。

　　1.基本概念:

　　　网络客户/服务模式的原理是一台主机提供服务(服务器)，另一台主机接受服务

(客户机)。作为服务器的主机一般会打开一个默认的端口并进行监听(Listen), 如果有

客户机向服务器的这一端口提出连接请求(Connect Request), 服务器上的相应程序就

会自动运行，来应答客户机的请求，这个程序我们称为守护进程(UNIX的术语,不过已经

被移植到了MS系统上)。对于冰河，被控制端就成为一台服务器，控制端则是一台客户

机，G_server.exe是守护进程, G_client是客户端应用程序。(这一点经常有人混淆，

而且往往会给自己种了木马!甚至还有人跟我争得面红耳赤，昏倒!!）

　　　

　　2.程序实现:

　　　在VB中,可以使用Winsock控件来编写网络客户/服务程序, 实现方法如下:

　　　(其中,G_Server和G_Client均为Winsock控件)

　　　服务端:

　　　G_Server.LocalPort=7626(冰河的默认端口,可以改为别的值)

　　　G_Server.Listen(等待连接)

　　　

　　　客户端:

　　　G_Client.RemoteHost=ServerIP(设远端地址为服务器地址)

　　　G_Client.RemotePort=7626　　(设远程端口为冰河的默认端口,呵呵,知道吗?这

是冰河的生日哦)

　　　(在这里可以分配一个本地端口给G_Client, 如果不分配, 计算机将会自动分配

一个, 建议让计算机自动分配)

　　　G_Client.Connect　　　　　　(调用Winsock控件的连接方法)

　　　

　　　一旦服务端接到客户端的连接请求ConnectionRequest,就接受连接

　　　Private Sub G_Server_ConnectionRequest(ByVal requestID As Long)

　　　　　　　G_Server.Accept requestID

　　　End Sub

　　　

　　　客户机端用G_Client.SendData发送命令,而服务器在G_Server_DateArrive事件

中接受并执行命令(几乎所有的木马功能都在这个事件处理程序中实现)


　　　如果客户断开连接,则关闭连接并重新监听端口　　　

　　　Private Sub G_Server_Close()

　　　　　　　G_Server.Close　 (关闭连接)

　　　　　　　G_Server.Listen　(再次监听)

　　　End Sub


　　　其他的部分可以用命令传递来进行，客户端上传一个命令，服务端解释并执行命

令......

　　　　


二、控制篇（木马控制了这个世界！）

　　由于Win98开放了所有的权限给用户，因此，以用户权限运行的木马程序几乎可以

控制一切，让我们来看看冰河究竟能做些什么(看了后,你会认同我的观点:称冰河为木

马是不恰当的,冰河实现的功能之多,足以成为一个成功的远程控制软件)

　　因为冰河实现的功能实在太多,我不可能在这里一一详细地说明,所以下面仅对冰河

的主要功能进行简单的概述, 主要是使用Windows API函数, 如果你想知道这些函数的

具体定义和参数, 请查询WinAPI手册。

　　1.远程监控(控制对方鼠标、键盘，并监视对方屏幕)

　　　keybd_event　模拟一个键盘动作(这个函数支持屏幕截图哦)。

　　　mouse_event　模拟一次鼠标事件(这个函数的参数太复杂,我要全写在这里会被

编辑骂死的,只能写一点主要的,其他的自己查WinAPI吧)

　　　mouse_event(dwFlags,dx,dy,cButtons,dwExtraInfo)


dwFlags:　

　　　MOUSEEVENTF_ABSOLUTE 指定鼠标坐标系统中的一个绝对位置。

　　　MOUSEEVENTF_MOVE 移动鼠标

　　　MOUSEEVENTF_LEFTDOWN 模拟鼠标左键按下

　　　MOUSEEVENTF_LEFTUP 模拟鼠标左键抬起

　　　MOUSEEVENTF_RIGHTDOWN 模拟鼠标右键按下

　　　MOUSEEVENTF_RIGHTUP 模拟鼠标右键按下

　　　MOUSEEVENTF_MIDDLEDOWN 模拟鼠标中键按下

　　　MOUSEEVENTF_MIDDLEUP 模拟鼠标中键按下

dx,dy:

　　　MOUSEEVENTF_ABSOLUTE中的鼠标坐标


　　　

2.记录各种口令信息(出于安全角度考虑,本文不探讨这方面的问题,也请不要给我来信

询问)


　　3.获取系统信息

　　　a.取得计算机名　 GetComputerName

　　　b.更改计算机名　 SetComputerName

　　　c.当前用户　　　 GetUserName函数

　　　d.系统路径　

　　　　　Set FileSystem0bject = CreateObject("Scripting.FileSystemObject")

　　　　　 (建立文件系统对象)

　　　　　Set SystemDir = FileSystem0bject.getspecialfolder(1)

　　　　　(取系统目录)

　　　　　Set SystemDir = FileSystem0bject.getspecialfolder(0)

　　　　　(取Windows安装目录)

　　　　　

　　　　　(友情提醒: FileSystemObject是一个很有用的对象,你可以用它来完成很多

有用的文件操作)


　　　e.取得系统版本　 GetVersionEx(还有一个GetVersion,不过在32位windows下可

能会有问题,所以建议用GetVersionEx


　　　f.当前显示分辨率

　　　Width = screen.Width　\ screen.TwipsPerPixelX

　　　Height= screen.Height \ screen.TwipsPerPixelY


　　　其实如果不用Windows API我们也能很容易的取到系统的各类信息,那就是

Winodws的"垃圾站"-注册表

　　　比如计算机名和计算机标识吧:

HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\VxD\VNETSUP

中的Comment,ComputerName和WorkGroup

　　　注册公司和用户名:

HKEY_USERS\.DEFAULT\Software\Microsoft\MS Setup (ACME)\UserInfo

至于如何取得注册表键值请看第6部分


　　4.限制系统功能

　　　a.远程关机或重启计算机,使用WinAPI中的如下函数可以实现:

　　　　ExitWindowsEx(ByVal uFlags,0)

　　　　当uFlags=0 EWX_LOGOFF 中止进程，然后注销

　　　　　　　=1 EWX_SHUTDOWN 关掉系统电源

　　　　　　　=2 EWX_REBOOT　 重新引导系统

　　　　　　　=4 EWX_FORCE　　强迫中止没有响应的进程

　　　

　　　b.锁定鼠标

　　　　ClipCursor(lpRect As RECT)可以将指针限制到指定区域,或者用

ShowCursor(FALSE)把鼠标隐藏起来也可以

　　　　

　　　　注:RECT是一个矩形,定义如下:

　　　　Type RECT

　　　　　　 Left As Long

　　　　　　 Top As Long

　　　　　　 Right As Long

　　　　　　 Bottom As Long

　　　　End Type


　　　c.锁定系统　这个有太多的办法了,嘿嘿,想Windows不死机都困难呀,比如,搞个

死循环吧,当然,要想系统彻底崩溃还需要一点技巧,比如设备漏洞或者耗尽资源什么的

.......


　　　d.让对方掉线 RasHangUp......


　　　e.终止进程　 ExitProcess......


　　　f.关闭窗口　利用FindWindow函数找到窗口并利用SendMessage函数关闭窗口


　　　


　　5.远程文件操作

　　　无论在哪种编程语言里, 文件操作功能都是比较简单的, 在此就不赘述了,你也

可以用上面提到的FileSystemObject对象来实现


　　6.注册表操作

　　　在VB中只要Set RegEdit=CreateObject（"WScript.Shell")

　　　就可以使用以下的注册表功能:

　　　删除键值:RegEdit.RegDelete RegKey

　　　增加键值:RegEdit.Write　　 RegKey,RegValue

　　　获取键值:RegEdit.RegRead　 (Value)

　　　记住,注册表的键值要写全路径,否则会出错的。


　　7.发送信息

　　　很简单,只是一个弹出式消息框而已,VB中用MsgBox("")就可以实现,其他程序也

不太难的。


　　8.点对点通讯

　　　呵呵,这个嘛随便去看看什么聊天软件就行了

　　　(因为比较简单但是比较烦,所以我就不写了,呵呵。又:我始终没有搞懂冰河为什

么要在木马里搞这个东东，困惑......)


　　9.换墙纸

　　　Call SystemParametersInfo(20,0,"BMP路径名称",&H1)

　　　值得注意的是,如果使用了Active Desktop,换墙纸有可能会失败，遇到这种问

题，请不要找冰河和我，去找比尔盖子吧。


三、潜行篇（Windows，一个捉迷藏的大森林）

　　木马并不是合法的网络服务程序(即使你是把木马装在女朋友的机子上,也是不合法

的,当然,这种行为我可以理解，呵呵)，因此，它必须想尽一切办法隐藏自己，好在，

Windows是一个捉迷藏的大森林!

　　1、在任务栏中隐藏自己：

　　　这是最基本的了,如果连这个都做不到......（想象一下，如果Windows的任务栏

里出现一个国际象棋中木马的图标...@#$%!#@$...也太嚣张了吧!)

　　　在VB中，只要把form的Visible属性设为False, ShowInTaskBar设为False, 程序

就不会出现在任务栏中了。


　　2、在任务管理器中隐形：（就是按下Ctrl+Alt+Del时看不见那个名字叫做“木

马”的进程）

　　　这个有点难度，不过还是难不倒我们，将程序设为“系统服务”可以很轻松的伪

装成比尔盖子的嫡系部队(Windows,我们和你是一家的,不要告诉别人我藏在哪儿...)。

　　　在VB中如下的代码可以实现这一功能：

　　　Public Declare Function RegisterServiceProcess Lib "kernel32" (ByVal

ProcessID As Long, ByVal ServiceFlags As Long) As Long

　　　Public Declare Function GetCurrentProcessId Lib "kernel32" () As Long

　　　(以上为声明)

　　　Private Sub Form_Load()

　　　　　 RegisterServiceProcess GetCurrentProcessId, 1 (注册系统服务)

　　　End Sub

　　　Private Sub Form_Unload()

　　　　　RegisterServiceProcess GetCurrentProcessId, 0 (取消系统服务)

　　　End Sub


　　3、如何悄没声息地启动：

　　　你当然不会指望用户每次启动后点击木马图标来运行服务端，木马要做到的第二

重要的事就是如何在每次用户启动时自动装载服务端（第一重要的是如何让对方中木

马，嘿嘿，这部分的内容将在后面提到）

　　　Windows支持多种在系统启动时自动加载应用程序的方法(简直就像是为木马特别

定做的)启动组、win.ini、system.ini、注册表等等都是木马藏身的好地方。冰河采用

了多种方法确保你不能摆脱它(怎么听起来有点死缠烂打呀....哎呦,谁呀谁呀,那什么

黄鑫,不要拿鸡蛋扔我!)首先,冰河会在注册表的

HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run和RUNSERVICE

键值中加上了<system>\kernl32.exe(<system>是系统目录), 其次如果你删除了这个键

值,自以为得意地喝著茶的时候,冰河又阴魂不散地出现了...怎么回事?原来冰河的服务

端会在c:\windows(这个会随你windows的安装目录变化而变化）下生成一个叫

sysexplr.exe文件（太象超级解霸了，好毒呀，冰河！）,这个文件是与文本文件相关

联的,只要你打开文本(哪天不打开几次文本?), sysexplr.exe文件就会重新生成

krnel32.exe, 然后你还是被冰河控制著。（冰河就是这样长期霸占著穷苦劳动人民宝

贵的系统资源的，555555）

　

　　4、端口

　　木马都会很注意自己的端口(你呢?你关心你的6万多个端口吗?),如果你留意的话,

你就会发现,木马端口一般都在1000以上,而且呈越来越大的趋势(netspy是1243....)这

是因为,1000以下的端口是常用端口,占用这些端口可能会造成系统不正常,这样木马就

会很容易暴露; 而由于端口扫描是需要时间的(一个很快的端口扫描器在远程也需要大

约二十分钟才能扫完所有的端口),故而使用诸如54321的端口会让你很难发现它。在文

章的末尾我给大家转贴了一个常见木马的端口表,你就对著这个表去查吧(不过,值得提

醒的是,冰河及很多比较新的木马都提供端口修改功能,所以,实际上木马能以任意端口

出现)

　　

　　5.最新的隐身技术

　　目前,除了冰河使用的隐身技术外,更新、更隐蔽的方法已经出现，那就是-驱动程

序及动态链接库技术（冰河3.0会采用这种方法吗?）。

　　驱动程序及动态链接库技术和一般的木马不同，它基本上摆脱了原有的木马模式-

监听端口，而采用替代系统功能的方法（改写驱动程序或动态链接库）。这样做的结果

是：系统中没有增加新的文件（所以不能用扫描的方法查杀）、不需要打开新的端口

（所以不能用端口监视的方法查杀）、没有新的进程（所以使用进程查看的方法发现不

了它，也不能用kill进程的方法终止它的运行）。在正常运行时木马几乎没有任何的症

状,而一旦木马的控制端向被控端发出特定的信息后,隐藏的程序就立即开始运作......

　　事实上，我已经看到过几个这样类型的木马，其中就有通过改写vxd文件建立隐藏

共享的木马...(江湖上又将掀起新的波浪)


四、破解篇（魔高一尺、道高一丈）

　　本文主要是探讨木马的基本原理, 木马的破解并非是本文的重点(也不是我的长

处),具体的破解请大家期待yagami的《特洛伊木马看过来》（我都期待一年了，大家和

我一起继续期待吧，嘿嘿），本文只是对通用的木马防御、卸载方法做一个小小的总结

：

　　1.端口扫描

　　端口扫描是检查远程机器有无木马的最好办法, 端口扫描的原理非常简单, 扫描程

序尝试连接某个端口, 如果成功, 则说明端口开放, 如果失败或超过某个特定的时间

(超时), 则说明端口关闭。（关于端口扫描，Oliver有一篇关于“半连接扫描”的文

章，很精彩，那种扫描的原理不太一样，不过不在本文讨论的范围之中）


　　但是值得说明的是, 对于驱动程序/动态链接木马, 扫描端口是不起作用的。


　　2.查看连接

　　查看连接和端口扫描的原理基本相同，不过是在本地机上通过netstat -a（或某个

第三方的程序）查看所有的TCP/UDP连接，查看连接要比端口扫描快，缺点同样是无法

查出驱动程序/动态链接木马,而且仅仅能在本地使用。


　　3.检查注册表

　　上面在讨论木马的启动方式时已经提到，木马可以通过注册表启动（好像现在大部

分的木马都是通过注册表启动的，至少也把注册表作为一个自我保护的方式），那么，

我们同样可以通过检查注册表来发现"马蹄印",冰河在注册表里留下的痕迹请参照《潜

行篇》。


　　4.查找文件

　　查找木马特定的文件也是一个常用的方法（这个我知道,冰河的特征文件是

G_Server.exe吧? 笨蛋!哪会这么简单,冰河是狡猾狡猾的......）冰河的一个特征文件

是kernl32.exe(靠,伪装成Windows的内核呀),另一个更隐蔽,是sysexlpr.exe(什么什么

,不是超级解霸吗?)对！冰河之所以给这两个文件取这样的名字就是为了更好的伪装自

己, 只要删除了这两个文件,冰河就已经不起作用了。其他的木马也是一样（废话，

Server端程序都没了，还能干嘛？）

　　黄鑫:"咳咳,不是那么简单哦......"(狡猾地笑)

　　是的, 如果你只是删除了sysexlpr.exe而没有做扫尾工作的话,可能会遇到一些麻

烦-就是你的文本文件打不开了,因为前面说了,sysexplr.exe是和文本文件关联的,你还

必须把文本文件跟notepad关联上,方法有三种:

　　a.更改注册表(我就不说了,有能力自己改的想来也不要我说,否则还是不要乱动的

好)

　　b.在<我的电脑>-查看-文件夹选项-文件类型中编辑

　　c.按住SHIFT键的同时鼠标右击任何一个TXT文件,选择打开方式,选中<始终用该程

序打开......>,然后找到notepad,点一下就OK了。（这个最简单，推荐使用）

　　黄鑫："我...我笑不起来了 :( "

　　提醒一下，对于木马这种狡猾的东西，一定要小心又小心，冰河是和txt文件关联

的，txt打不开没什么大不了，如果木马是和exe文件关联而你贸然地删了它......你苦

了！连regedit都不能运行了！


　　5.杀病毒软件

　　之所以把杀病毒软件放在最后是因为它实在没有太大的用,包括一些号称专杀木马

的软件也同样是如此, 不过对于过时的木马以及菜鸟安装的木马(没有配置服务端)还是

有点用处的, 值得一提的是最近新出来的ip armor在这一方面可以称得上是比较领先的

,它采用了监视动态链接库的技术,可以监视所有调用Winsock的程序，并可以动态杀除

进程，是一个个人防御的好工具（虽然我对传说中“该软件可以查杀未来十年木马”的

说法表示怀疑，嘿嘿，两年后的事都说不清，谁知道十年后木马会“进化”到什么程度

？甚至十年后的操作系统是什么样的我都想象不出来）


　　另外，对于驱动程序/动态链接库木马，有一种方法可以试试，使用Windows的"系

统文件检查器"，通过"开始菜单"-"程序"-"附件"-"系统工具"-"系统信息"-"工具"可以

运行"系统文件检查器"(这么详细,不会找不到吧? 什么,你找不到! 吐血! 找一张98安

装盘补装一下吧), 用“系统文件检查器”可检测操作系统文件的完整性，如果这些文

件损坏，检查器可以将其还原，检查器还可以从安装盘中解压缩已压缩的文件（如驱动

程序）。如果你的驱动程序或动态链接库在你没有升级它们的情况下被改动了,就有可

能是木马(或者损坏了),提取改动过的文件可以保证你的系统安全和稳定。(注意,这个

操作需要熟悉系统的操作者完成,由于安装某些程序可能会自动升级驱动程序或动态链

接库,在这种情况下恢复"损坏的"文件可能会导致系统崩溃或程序不可用！)


五、狡诈篇（只要你的一点点疏忽......)

　　只要你有一点点的疏忽，就有可能被人安装了木马，知道一些给人种植木马的常见

伎俩对于保证自己的安全不无裨益。

1.网上“帮”人种植木马的伎俩主要有以下的几条

　　　a.软哄硬骗法；

　　　这个方法很多啦, 而且跟技术无关的, 有的是装成大虾, 有的是装成PLMM, 有的

态度谦恭, 有的......反正目的都一样,就是让你去运行一个木马的服务端。

　　　b.组装合成法

　　　就是所谓的221(Two To One二合一)把一个合法的程序和一个木马绑定,合法程序

的功能不受影响,但当你运行合法程序时,木马就自动加载了,同时,由于绑定后程序的代

码发生了变化,根据特征码扫描的杀毒软件很难查找出来。

　　　c.改名换姓法

　　　这个方法出现的比较晚,不过现在很流行,对于不熟练的windows操作者，很容易

上当。具体方法是把可执行文件伪装成图片或文本----在程序中把图标改成Windows的

默认图片图标, 再把文件名改为*.jpg.exe, 由于Win98默认设置是"不显示已知的文件

后缀名",文件将会显示为*.jpg, 不注意的人一点这个图标就中木马了(如果你在程序中

嵌一张图片就更完美了)

　　　d.愿者上钩法

　　　木马的主人在网页上放置恶意代码，引诱用户点击，用户点击的结果不言而喻：

开门揖盗;奉劝：不要随便点击网页上的链接，除非你了解它，信任它，为它死了也愿

意...（什么乱七八糟呀）　　


2． 几点注意（一些陈词滥调）

　　a．不要随便从网站上下载软件,要下也要到比较有名、比较有信誉的站点，这些站

点一般都有专人杀马杀毒；

　　b．不要过于相信别人，不能随便运行别人给的软件；

（特别是认识的，不要以为认识了就安全了，就是认识的人才会给你装木马,哈哈,挑拨

离间......）

　　c．经常检查自己的系统文件、注册表、端口什么的，经常去安全站点查看最新的

木马公告；

　　d.改掉windows关于隐藏文件后缀名的默认设置(我是只有看见文件的后缀名才会放

心地点它的)

　　e．如果上网时发现莫名奇妙地硬盘乱响或猫上的数据灯乱闪，要小心；

　（我常常会突然关掉所有连接，然后盯著我的猫，你也可以试试，要是这时数据传送

灯还在拼命闪，恭喜，你中木马了，快逃吧！）


六、后记

　　这篇文章的问世首先要感谢冰河的作者-黄鑫，我对他说：“我要写篇关于冰河的

文章”，他说：“写呗”，然后就有了这篇文章的初稿（黄鑫：“不是吧，你答应要用

稿费请我吃饭的，不要赖哦”），随后，黄鑫给我提了很多建议并提供了不少资料,谢

谢冰河。

　　其次是西祠的yagami，他是公认的木马专家，在我写作期间，他不仅在木马的检

测、杀除方面提出了不少自己的看法，还给我找来了几个木马的源代码作为参考，不过

这个家伙实在太忙，所以想看《特洛伊木马看过来》的朋友就只有耐心地等待了。

　　第三个值得一提的家伙是武汉人，我的初稿一出来，他就忙不迭地贴出去了，当时

我很狼狈，只能加紧写，争取早日完成，赶快把漏洞百出的初稿换下来，要不然，嘿

嘿，估计大家也要等个一年半载的才能看到这篇文章了。

　　这篇文章的初稿出来以后，有很多朋友问：为什么不用C++，而要用VB来写木马的

源码说明呢？呵呵，其一是我很懒，VB比 VC要容易多了,还不会把windows搞死机(我用

VC写程序曾经把系统搞崩溃过的:P);其二,本文中能用API的,我基本上都用了,VB只是很

小的一块, WINAPI嘛,移植起来是很容易的;其三,正如我前面强调的,本文只是对木马的

结构和原理进行一番讨论,并非教人如何编写木马程序,要知道,公安部已经正式下文:在

他人计算机内下毒的要处以刑事处分。相比而言，VB代码的危害性要小很多的（如果完

全用VB做一个冰河，大概要一兆多，还不连那些控件和动态链接库文件，呵呵，这么庞

大的程序，能悄 悄 地在别人的机子里捣鬼吗？）

　　最后，作为冰河的朋友，我希望大家能抱著学术的态度来看这篇文章，同样能抱著

学术的态度来看待冰河木马，不要用冰河做坏事，我替黄鑫先谢谢你了！(监视自己的

女朋友不算，不过冰河不会对因为使用冰河导致和女友吵架直至分手负任何责任）


附录：常见的一些木马的端口（转）

port 21 - Back Construction, Blade Runner, Doly Trojan, Fore, FTP trojan,

Invisible FTP, Larva,WebEx, WinCrash

port 23 - Tiny Telnet Server (= TTS)

port 25 - Ajan, Antigen, Email Password Sender, Haebu Coceda (= Naebi),

Happy 99, Kuang2, ProMail trojan, Shtrilitz, Stealth, Tapiras, Terminator,

WinPC, WinSpy

port 31 - Agent 31, Hackers Paradise, Masters Paradise

port 41 - DeepThroat

port 59 - DMSetup

port 79 - Firehotcker

port 80 - Executor, RingZero

port 99 - Hidden Port

port 110 - ProMail trojan

port 113 - Kazimas

port 119 - Happy 99

port 121 - JammerKillah

port 421 - TCP Wrappers

port 456 - Hackers Paradise

port 531 - Rasmin

port 555 - Ini-Killer, NeTAdmin, Phase Zero, Stealth Spy

port 666 - Attack FTP, Back Construction, Cain & Abel, Satanz Backdoor,

ServeU, Shadow Phyre

port 911 - Dark Shadow

port 999 - DeepThroat, WinSatan

port 1001 - Silencer, WebEx

port 1010 - Doly Trojan

port 1011 - Doly Trojan

port 1012 - Doly Trojan

port 1015 - Doly Trojan

port 1024 - NetSpy

port 1042 - Bla

port 1045 - Rasmin

port 1090 - Xtreme

port 1170 - Psyber Stream Server, Streaming Audio trojan, Voice

port 1234 - Ultors Trojan

port 1243 - SubSeven

port 1245 - VooDoo Doll

port 1269 - Mavericks Matrix

port 1349 (UDP) - BO DLL

port 1492 - FTP99CMP

port 1509 - Psyber Streaming Server

port 1600 - Shivka-Burka

port 1807 - SpySender

port 1981 - Shockrave

port 1999 - BackDoor

port 1999 - TransScout

port 2000 - TransScout

port 2001 - TransScout

port 2001 - Trojan Cow

port 2002 - TransScout

port 2003 - TransScout

port 2004 - TransScout

port 2005 - TransScout

port 2023 - Ripper

port 2115 - Bugs

port 2140 - Deep Throat, The Invasor

port 2155 - Illusion Mailer

port 2283 - HVL Rat5

port 2565 - Striker

port 2583 - WinCrash

port 2600 - Digital RootBeer

port 2801 - Phineas Phucker

port 2989 (UDP) - RAT

port 3024 - WinCrash

port 3128 - RingZero

port 3129 - Masters Paradise

port 3150 - Deep Throat, The Invasor

port 3459 - Eclipse 2000

port 3700 - Portal of Doom

port 3791 - Eclypse

port 3801 (UDP) - Eclypse

port 4092 - WinCrash

port 4321 - BoBo

port 4567 - File Nail

port 4590 - ICQTrojan

port 5000 - Bubbel, Back Door Setup, Sockets de Troie

port 5001 - Back Door Setup, Sockets de Troie

port 5011 - One of the Last Trojans (OOTLT)

port 5031 - NetMetro

port 5321 - Firehotcker

port 5400 - Blade Runner, Back Construction

port 5401 - Blade Runner, Back Construction

port 5402 - Blade Runner, Back Construction

port 5550 - Xtcp

port 5512 - Illusion Mailer

port 5555 - ServeMe

port 5556 - BO Facil

port 5557 - BO Facil

port 5569 - Robo-Hack

port 5742 - WinCrash

port 6400 - The Thing

port 6669 - Vampyre

port 6670 - DeepThroat

port 6771 - DeepThroat

port 6776 - BackDoor-G, SubSeven

port 6912 - Shit Heep (not port 69123!)

port 6939 - Indoctrination

port 6969 - GateCrasher, Priority, IRC 3

port 6970 - GateCrasher

port 7000 - Remote Grab, Kazimas

port 7300 - NetMonitor

port 7301 - NetMonitor

port 7306 - NetMonitor

port 7307 - NetMonitor

port 7308 - NetMonitor

port 7789 - Back Door Setup, ICKiller

port 8080 - RingZero

port 9400 - InCommand

port 9872 - Portal of Doom

port 9873 - Portal of Doom

port 9874 - Portal of Doom

port 9875 - Portal of Doom

port 9876 - Cyber Attacker

port 9878 - TransScout

port 9989 - iNi-Killer

port 10067 (UDP) - Portal of Doom

port 10101 - BrainSpy

port 10167 (UDP) - Portal of Doom

port 10520 - Acid Shivers

port 10607 - Coma

port 11000 - Senna Spy

port 11223 - Progenic trojan

port 12076 - Gjamer

port 12223 - Hack?9 KeyLogger

port 12345 - GabanBus, NetBus, Pie Bill Gates, X-bill

port 12346 - GabanBus, NetBus, X-bill

port 12361 - Whack-a-mole

port 12362 - Whack-a-mole

port 12631 - WhackJob

port 13000 - Senna Spy

port 16969 - Priority

port 17300 - Kuang2 The Virus

port 20000 - Millennium

port 20001 - Millennium

port 20034 - NetBus 2 Pro

port 20203 - Logged

port 21544 - GirlFriend

port 22222 - Prosiak

port 23456 - Evil FTP, Ugly FTP, Whack Job

port 23476 - Donald Dick

port 23477 - Donald Dick

port 26274 (UDP) - Delta Source

port 29891 (UDP) - The Unexplained

port 30029 - AOL Trojan

port 30100 - NetSphere

port 30101 - NetSphere

port 30102 - NetSphere

port 30303 - Sockets de Troi

port 30999 - Kuang2

port 31336 - Bo Whack

port 31337 - Baron Night, BO client, BO2, Bo Facil

port 31337 (UDP) - BackFire, Back Orifice, DeepBO

port 31338 - NetSpy DK

port 31338 (UDP) - Back Orifice, DeepBO

port 31339 - NetSpy DK

port 31666 - BOWhack

port 31785 - Hack'a'tack

port 31787 - Hack'a'tack

port 31788 - Hack'a'tack

port 31789 (UDP) - Hack'a'tack

port 31791 (UDP) - Hack'a'tack

port 31792 - Hack'a'tack

port 33333 - Prosiak

port 33911 - Spirit 2001a

port 34324 - BigGluck, TN

port 40412 - The Spy

port 40421 - Agent 40421, Masters Paradise

port 40422 - Masters Paradise

port 40423 - Masters Paradise

port 40426 - Masters Paradise

port 47262 (UDP) - Delta Source

port 50505 - Sockets de Troie

port 50766 - Fore, Schwindler

port 53001 - Remote Windows Shutdown

port 54320 - Back Orifice 2000

port 54321 - School Bus

port 54321 (UDP) - Back Orifice 2000

port 60000 - Deep Throat

port 61466 - Telecommando

port 65000 - Devil

　　注：开了上面的端口未必就是中了木马，有的端口本来就是正常的端口，只是被木

马利用了，有的防火墙也会打开一些端口来监控（很无聊的做法），判断木马是一门较

深的学问，如果你有什么疑问和建议，请和我联系


揭开木马的神秘面纱（二）

作者：shotgun


 前言

　　 离冰河二的问世已经快一年了，大家对于木马这种远程控制软件也有了一定的认

识，比如：他会改注册表，他会监听端口等等，和一年前几乎没有人懂得木马是什么东

西相比，这是一个质的飞跃。但是，在这个连“菜鸟”都会用NETSTAT看端口，用

LOCKDOWN保护注册表的今天，难道木马就停步不前，等待我们的“杀戮”么？回答显然

是否定的。木马在这一年当中，同样也不断进步，不断发展，他们变得更加隐蔽，更加

灵活。本文试图通过分析近一年以来木马软件的发展，向大家介绍木马的最新攻防技

巧，从而使大家能够更加安全地畅游在Internet上。（本文中默认的操作系统为

Win2000，默认的编程环境是VC++6.0）


 在过去的一年当中，出过很多有名的木马，SUB7,BO2000,冰河等等，他们都有几个共

同的特点，比如：开TCP端口监听，写注册表等等，因此，针对这些特点，也涌现出了

不少查杀木马的工具，比如LockDown2000, Clean等，这些工具一般都是利用检查注册

表和端口来寻找木马（也有利用特征码来查找的，那种原始的思路我们就不说了，谁都

知道，只要源码稍微改改，特征码查询就毫无用处）甚至还出了一些号称能防范未来多

少年木马的软件。而在大家的不断宣传下，以下的木马法则已经妇孺皆知：

 1、 不要随便从不知名的网站上下载可执行文件，不要随便运行别人给的软件；

 2、不要过于相信别人，不要随便打开邮件的附件；

 3、经常检查自己的系统文件、注册表、端口、进程；

 4、经常去查看最新的木马公告，更新自己防火墙的木马库；

 　　这样看来，第一代木马的特性大家都已经耳熟能详，在这种情况下，作为一个地

下工作者，木马的日子会非常难过。那么，木马就这样甘受屠戮，坐以待毙么？人类就

这样灭绝了木马这个种族么？不是！木马为了生存，也在不断进化，在我们放松警惕，

庆祝胜利的时候，木马已经经历了几次质的突变，现在的木马比起他们的前辈要更加隐

蔽，更加巧妙，更难以发现，功能更强大。

　　 实际上在我们总结了老一辈木马的特征，并把它们写进杀马软件、编入防马教

程、挂在各个安全网站的首页的时候，木马们就意识到了自己的危险，为了自身的安

全，为了种族的延续，木马们认真地审视了自己的不足（没准也看了很多教程）觉得：

要想更好、更安全的发展下去，只有化缺点为优点，改短处为长处，否则只有死路一

条。于是，他们针对自己的不足，采取了以下的升级方案：

　　 一、关端口

 祸从口出，同样，端口也是木马的最大漏洞，经过大家的不断宣传，现在连一个刚刚

上网没有多久的“菜鸟”也知道用NETSTAT查看端口，木马的端口越做越高，越做越象

系统端口，被发现的概率却越来越大。但是端口是木马的生命之源，没有端口木马是无

法和外界进行通讯的，更不要说进行远程控制了。为了解决这个矛盾，木马们深入研究

了Richard Stevens的TCP/IP协议详解，决定：放弃原来他们赖以生存的端口，转而进

入地下。放弃了端口后木马怎么和控制端联络呢？对于这个问题，不同的木马采用了不

同的方法，大致分为以下两种方法：寄生、潜伏。

 1、 寄生就是找一个已经打开的端口，寄生其上，平时只是监听，遇到特殊的指令就

进行解释执行；因为木马实际上是寄生在已有的系统服务之上的，因此，你在扫描或查

看系统端口的时候是没有任何异常的。据我所知，在98下进行这样的操作是比较简单

的，但是对于Win2000 相对要麻烦得多。由于作者对这种技术没有很深的研究，在这里

就不赘述了，感兴趣的朋友可以去[http://www.ahjmw.gov.cn/cit/](http://www.ahjmw.gov.cn/cit/)或者西祠胡同的

WinSock版查看相关的资料。

 2、 潜伏是说使用IP协议族中的其它协议而非TCP/UDP来进行通讯，从而瞒过Netstat

和端口扫描软件。一种比较常见的潜伏手段是使用ICMP协议，ICMP（Internet控制报

文）是IP协议的附属协议，它是由内核或进程直接处理而不需要通过端口，一个最常见

的ICMP协议就是Ping，它利用了ICMP的回显请求和回显应答报文。一个普通的ICMP木马

会监听ICMP报文，当出现特殊的报文时（比如特殊大小的包、特殊的报文结构等）它会

打开TCP端口等待控制端的连接，这种木马在没有激活时是不可见的，但是一旦连接上

了控制端就和普通木马一样，本地可以看到状态为Established的链接（如果端口的最

大连接数设为1，在远程使用Connect方法进行端口扫描还是没有办法发现的）；而一个

真正意义上的ICMP木马则会严格地使用ICMP协议来进行数据和控制命令的传递（数据放

在ICMP的报文中），在整个过程中，它都是不可见的。（除非使用嗅探软件分析网络流

量）

 3、 除了寄生和潜伏之外，木马还有其他更好的方法进行隐藏，比如直接针对网卡或

Modem进行底层的编程，这涉及到更高的编程技巧。


　　 二、隐藏进程。

　　 在win9x时代，简单的注册为系统进程就可以从任务栏中消失，可是在Window2000

盛行的今天，这种方法遭到了惨败，注册为系统进程不仅仅能在任务栏中看到，而且可

以直接在Services中直接控制停止、运行（太搞笑了，木马被客户端控制）。使用隐藏

窗体或控制台的方法也不能欺骗无所不见的ADMIN大人（要知道，在NT下，

Administrator是可以看见所有进程的）。在研究了其它软件的长处之后，木马发现，

Windows下的中文汉化软件采用的陷阱技术非常适合木马的使用。

　　 DLL陷阱技术是一种针对DLL（动态链接库）的高级编程技术，编程者用特洛伊DLL

替换已知的系统DLL，并对所有的函数调用进行过滤，对于正常的调用，使用函数转发

器直接转发给被替换的系统DLL,对于一些事先约定好的特殊情况，DLL会执行一些相对

应的操作，一个比较简单的方法是起一个进程，虽然所有的操作都在DLL中完成会更加

隐蔽，但是这大大增加了程序编写的难度，实际上这样的木马大多数只是使用DLL进行

监听，一旦发现控制端的连接请求就激活自身，起一个绑端口的进程进行正常的木马操

作。操作结束后关掉进程，继续进入休眠状况。

　　 因为大量特洛伊DLL的使用实际上已经危害到了Windows操作系统的安全和稳定

性，据说微软的下一代操作系统Window2001（海王星）已经使用了DLL数字签名、校验

技术，因此，特洛伊DLL的时代很快会结束。取代它的将会是强行嵌入代码技术（插入

DLL，挂接API，进程的动态替换等等），但是这种技术对于编写者的汇编功底要求很

高，涉及大量硬编码的机器指令，并不是一般的木马编写者可以涉足。（晕，我是门都

找不到，哪位高手可以指点我一下？）


　　 三、争夺系统控制权

 木马们并不甘于老是处于防守的地位，他们也会进攻，也会主动出击。WINNT下的溢出

型木马就是这样的积极者，他们不仅仅简单的加载、守候、完成命令，而是利用种种系

统的漏洞设法使自己成为系统的拥有者-ADMIN，甚至系统的控制者-System。那么，木

马利用什么方法能一改过去到处逃亡的面目，从而成为系统的主宰呢？

 首当其冲的显然是注册表：多年驰骋注册表的历史使得木马非常熟悉注册表的构造和

特点（你呢，你能比木马更熟悉注册表么）Windows2000有几个注册表的权限漏洞，允

许非授权用户改写ADMIN的设置，从而强迫ADMIN执行木马程序，这个方法实现起来比较

容易，但是会被大多数的防火墙发现。

 其次是利用系统的权限漏洞，改写ADMIN的文件、配置等等，在ADMIN允许Active

Desktop的情况下这个方法非常好用，但是对于一个有经验的管理员，这个方法不是太

有效；

 第三个选择是系统的本地溢出漏洞，由于木马是在本地运行的，它可以通过本地溢出

的漏洞（比如IIS的本地溢出漏洞等），直接取得system的权限。这部分内容在袁哥和

很多汇编高手的文章中都有介绍，我就不再赘述了。（偷偷告诉你，其实是我说不出

来，我要是能写出那样的溢出程序我还用在这里......）


　　 四、防火墙攻防战

　　 现在，在个人防火墙如此之流行的今天，也许有人会说：我装个防火墙，不管你

用什么木马，在我系统上搞什么，防火墙设了只出不进，反正你没法连进来。同样，对

于局域网内的机器，原先的木马也不能有效的进行控制（难道指望网关会给你做NAT么

？）但是，城墙从来就挡不住木马：在古希腊的特洛伊战争中，人们是推倒了城墙来恭

迎木马的，而在这个互联网的时代，木马仍然以其隐蔽性和欺诈性使得防火墙被从内部

攻破。其中反弹端口型的木马非常清晰的体现了这一思路。

 反弹端口型木马分析了防火墙的特性后发现：防火墙对于连入的链接往往会进行非常

严格的过滤，但是对于连出的链接却疏于防范。于是，与一般的木马相反，反弹端口型

木马的服务端（被控制端）使用主动端口，客户端（控制端）使用被动端口，木马定时

监测控制端的存在，发现控制端上线立即弹出端口主动连结控制端打开的被动端口，为

了隐蔽起见，控制端的被动端口一般开在80，这样，即使用户使用端口扫描软件检查自

己的端口，发现的也是类似 TCP　UserIP:1026　ControllerIP:80 ESTABLISHED的情

况，稍微疏忽一点你就会以为是自己在浏览网页。（防火墙也会这么认为的，我想大概

没有哪个防火墙会不给用户向外连接80端口吧，嘿嘿）看到这里，有人会问：那服务端

怎么能知道控制端的IP地址呢？难道控制端只能使用固定的IP地址？哈哈，那不是自己

找死么？一查就查到了。实际上，这种反弹端口的木马常常会采用固定IP的第三方存储

设备来进行IP地址的传递。举一个简单的例子：事先约定好一个个人主页的空间，在其

中放置一个文本文件，木马每分钟去GET一次这个文件，如果文件内容为空，就什么都

不做，如果有内容就按照文本文件中的数据计算出控制端的IP和端口，反弹一个TCP链

接回去，这样每次控制者上线只需要FTP一个INI文件就可以告诉木马自己的位置，为了

保险起见，这个IP地址甚至可以经过一定的加密，除了服务和控制端，其他的人就算拿

到了也没有任何的意义。对于一些能够分析报文、过滤TCP/UDP的防火墙，反弹端口型

木马同样有办法对付，简单的来说，控制端使用80端口的木马完全可以真的使用HTTP协

议，将传送的数据包含在HTTP的报文中，难道防火墙真的精明到可以分辨通过HTTP协议

传送的究竟是网页还是控制命令和数据？


　　 五、更加隐蔽的加载方式：

　　 记得一年前，大家觉得通过所谓图片传播的木马非常神秘，其实现在几乎人人都

知道那只是一个后缀名的小把戏，而绑定EXE文件的木马也随着“不要轻易执行可执行

文件”的警告变得越来越不可行，和过去不同是，现在木马的入侵方式更加的隐蔽，在

揉合了宏病毒的特性后，木马已经不仅仅通过欺骗来传播了，随着网站互动化进程的不

断进步,越来越多的东西可以成为木马传播的介质，JavaScript，VBScript, ActiveX,

XML......几乎WWW每一个新出来的功能都会导致木马的快速进化，曾几何时，邮件木马

从附件走向了正文，简单的浏览也会中毒，而一个Guest用户也可以很容易的通过修改

管理员的文件夹设置给管理员吃上一点耗子药。当我们小心翼翼地穿行在互联网森林中

的时候，也许正有无数双木马的眼睛在黑暗中窥视，他们在等待你的一次疏忽，一个小

小的疏忽，这将给他们一个完美的机会......


　　 一点点感想：

 入侵高手可能会对于木马的编写和防御不屑一顾，但是，许多入侵事件多多少少会有

木马的参与（这个时候，木马程序往往被叫做后门）在最近的微软被黑事件中，入侵者

使用的就是一种叫QAZ的木马，实际上，这种木马并不非常高级，甚至不能算是第二代

木马（只是一种通过共享传播的蠕虫木马），而正是一只小小的木马，让强大的微软丢

尽了脸。要知道：入侵者和黑客不同，对于入侵者来说，入侵是最终的目的，任何手

段，只要能最快最简单的进入，就是最好的手段，由于被入侵的用户大多数并不是专业

人员，所以木马往往是一个很好的选择。

 在撰写本文的过程中，曾经有朋友和我戏言：危言耸听。其实，事实并非如此，在本

文中描述的木马，虽然看起来匪夷所思，但是在互联网上大多已经有了样品出现，而

且，我相信，一定还有技术含量远远超过上述木马的软件正在开发中。


　　 编后说明：

 本文的撰写，并不是为了发展木马技术，扰乱互联网，而是为了能深入探讨木马的攻

击和防御技术，引起人们对木马的关注，尽量减小木马传播可能造成的危害。

 本文的撰写得到了Lion Hook、无影猫、李逍遥、Yagami、 Quack以及Glacier的指导

和帮助，在此向他们表示感谢。


在揭开木马的神秘面纱（二）发表后，有很多朋友来信询问新型木马的详细情况，本文会详细的分析Win2000下一种新型木马的内部构造和防御方法。（本文默认的操作系统为Win2000，开发环境为VC++6.0。）

　　大家知道，一般的"古典"型木马都是通过建立TCP连接来进行命令和数据的传递的，但是这种方法有一个致命的漏洞，就是木马在等待和运行的过程中，始终有一个和外界联系的端口打开着，这是木马的阿喀琉斯之踵（参看希腊神话《特洛伊战纪》），也是高手们查找木马的杀手锏之一（Netstat大法）。所谓道高一尺，魔高一丈，木马也是在斗争中不断进步不断成长的，其中一种ICMP木马就彻底摆脱了端口的束缚，成为黑客入侵后门工具中的佼佼者。

　　什么是ICMP呢？ICMP全称是Internet Control Message Protocol（互联网控制报文协议）它是IP协议的附属协议，用来传递差错报文以及其他需要注意的消息报文，这个协议常常为TCP或UDP协议服务，但是也可以单独使用，例如著名的工具Ping（向Mike 

Muuss致敬），就是通过发送接收ICMP_ECHO和ICMP_ECHOREPLY报文来进行网络诊断的。

　　实际上，ICMP木马的出现正是得到了Ping程序的启发，由于ICMP报文是由系统内核或进程直接处理而不是通过端口，这就给木马一个摆脱端口的绝好机会，木马将自己伪装成一个Ping的进程，系统就会将ICMP_ECHOREPLY（Ping的回包）的监听、处理权交给木马进程，一旦事先约定好的ICMP_ECHOREPLY包出现（可以判断包大小、ICMP_SEQ等特征），木马就会接受、分析并从报文中解码出命令和数据。

　　ICMP_ECHOREPLY包还有对于防火墙和网关的穿透能力。对于防火墙来说，ICMP报文是被列为危险的一类：从Ping of Death到ICMP风暴到ICMP碎片攻击，构造ICMP报文一向是攻击主机的最好方法之一，因此一般的防火墙都会对ICMP报文进行过滤；但是ICMP_ECHOREPLY报文却往往不会在过滤策略中出现，这是因为一旦不允许ICMP_ECHOREPLY报文通过就意味着主机没有办法对外进行Ping的操作，这样对于用户是极其不友好的。如果设置正确，ICMP_ECHOREPLY报文也能穿过网关，进入局域网。

为了实现发送/监听ICMP报文，必须建立SOCK_RAW（原始套接口），首先，我们需要定义一个IP首部： 


typedef struct iphdr {


　unsigned int version:4; // IP版本号，4表示IPV4


　unsigned int h_len:4; // 4位首部长度


　unsigned char tos; // 8位服务类型TOS


　unsigned short total_len; // 16位总长度（字节） 


　unsigned short ident; file://16位标识


　unsigned short frag_and_flags; // 3位标志位


　unsigned char ttl; file://8位生存时间 TTL


　unsigned char proto; // 8位协议 (TCP, UDP 或其他)


　unsigned short checksum; // 16位IP首部校验和


　unsigned int sourceIP; file://32位源IP地址


　unsigned int destIP; file://32位目的IP地址


}IpHeader; 


　　然后定义一个ICMP首部：


typedef struct _ihdr {


　BYTE i_type; file://8位类型


　BYTE i_code; file://8位代码


　USHORT i_cksum; file://16位校验和 


　USHORT i_id; file://识别号（一般用进程号作为识别号）


　USHORT i_seq; file://报文序列号 


　ULONG timestamp; file://时间戳


}IcmpHeader; 


　　这时可以同过WSASocket建立一个原始套接口：


SockRaw=WSASocket(


　　　　　　　　　　AF_INET, file://协议族 


　　　　　　　　　　SOCK_RAW, file://协议类型，SOCK_RAW表示是原始套接口 


　　　　　　　　　　IPPROTO_ICMP, file://协议，IPPROTO_ICMP表示ICMP数据报


　　　　　　　　　　NULL, file://WSAPROTOCOL_INFO置空


　　　　　　　　　　0, file://保留字，永远置为0


　　　　　　　　　　WSA_FLAG_OVERLAPPED file://标志位


　　　　　　　　　　);


　　注：为了使用发送接收超时设置（设置SO_RCVTIMEO, SO_SNDTIMEO），必须将标志位置为WSA_FLAG_OVERLAPPED 

随后你可以使用fill_icmp_data子程序填充ICMP报文段：


fill_icmp_data函数：


void fill_icmp_data(char * icmp_data, int datasize)


{


　IcmpHeader *icmp_hdr;


　char *datapart;


　icmp_hdr = (IcmpHeader*)icmp_data;


　icmp_hdr->i_type = ICMP_ECHOREPLY; file://类型为ICMP_ECHOREPLY


　icmp_hdr->i_code = 0;


　icmp_hdr->i_id = (USHORT)GetCurrentProcessId(); file://识别号为进程号 


　icmp_hdr->i_cksum = 0; file://校验和初始化


　icmp_hdr->i_seq = 0; file://序列号初始化


　datapart = icmp_data + sizeof(IcmpHeader); file://数据端的地址为icmp报文


　　　　　　　　　　　　　　　　　　　　　　　　地址加上ICMP的首部长度


　memset(datapart,"A", datasize - sizeof(IcmpHeader)); file://这里我填充的数据


　　　　　　　　　　　　　　　　全部为"A"，你可以填充任何代码和数据，实际上


　　　　　　　　　　　　　　　　木马和控制端之间就是通过数据段传递数据的。


} 


　　再使用CheckSum子程序计算ICMP校验和：


　　调用方法：


((IcmpHeader*)icmp_data)->i_cksum 

= checksum((USHORT*)icmp_data, datasize);


CheckSum函数：


USHORT CheckSum (USHORT *buffer, int size) 


{


　unsigned long cksum=0;


　while(size >1) 


　　{ 


　　　　cksum+=*buffer++;


　　　　size -=sizeof(USHORT);


　　}


　　if(size ) cksum += *(UCHAR*)buffer;


　　cksum = (cksum >> 16) + (cksum & 0xffff);


　　cksum += (cksum >>16);


　　return (USHORT)(~cksum);


}// CheckSum函数是标准的校验和函数，你也可以用优化过的任何校验和函数来代替它


　　随后，就可以通过sendto函数发送ICMP_ECHOREPLY报文：


　　sendto(sockRaw,icmp_data,datasize,0,(struct sockaddr*)&dest,sizeof(dest));


　　作为服务端的监听程序，基本的操作相同，只是需要使用recvfrm函数接收ICMP_ECHOREPLY报文并用decoder函数将接收来的报文解码为数据和命令:


recv_icmp=recvfrom(sockRaw,recvbuf,MAX_PACKET,0,(struct 

sockaddr*)&from,&fromlen);


decode_resp(recvbuf,recv_icmp,&from);


decoder函数：


void decoder(char *buf, int bytes,struct sockaddr_in *from) 


{


　IpHeader *iphdr;


　IcmpHeader *icmphdr;


　unsigned short iphdrlen;


　iphdr = (IpHeader *)buf; file://IP首部的地址就等于buf的地址


　iphdrlen = iphdr->h_len * 4 ; // 因为h_len是32位word，要转换成bytes必须*4


　icmphdr = (IcmpHeader*)(buf + iphdrlen); file://ICMP首部的地址等于IP首部长度加buf


　printf("%d bytes from %s:",bytes, inet_ntoa(from->sin_addr)); 

file://取出源地址


　printf(" icmp_id=%d. ",icmphdr->i_id); file://取出进程号


　printf(" icmp_seq=%d. ",icmphdr->i_seq); file://取出序列号


　printf(" icmp_type=%d",icmphdr->i_type); file://取出类型


　printf(" icmp_code=%d",icmphdr->i_code); file://取出代码


　for(i=0;ifile://取出数据段


}


　　注：在WIN2000下使用SOCK_RAW需要管理员的权限。

　　对于ICMP木马，除非你使用嗅探器或者监视windows的SockAPI调用，否则从网络上是很难发现木马的行踪的（关于进程的隐藏及破解会在下一篇文章中进行讨论），那么，有什么可以补救的方法呢？有的，就是过滤ICMP报文，对于win2000可以使用系统自带的路由功能对ICMP协议进行过滤，win2000的Routing 

& Remote Access功能十分强大，其中之一就是建立一个TCP/IP协议过滤器：打开Routing & Remote Access，选中机器名，在IP路由->General->网卡属性中有两个过滤器-输入过滤和输出过滤，只要在这里将你想过滤的协议制定为策略，ICMP木马就英雄无用武之地了；不过值得注意的是，一旦在输入过滤器中禁止了ICMP_ECHOREPLY报文，你就别想再用Ping这个工具了；如果过滤了所有的ICMP报文，你就收不到任何错误报文，当你使用IE访问一个并不存在的网站时，往往要花数倍的时间才能知道结果（嘿嘿，网络不可达、主机不可达、端口不可达报文你一个都收不到），而且基于ICMP协议的tracert工具也会失效，这也是方便和安全之间的矛盾统一了吧。

　　本文的撰写是为了深入地研究Win2000的入侵和防御技术，探讨TCP/IP协议和Windows编程技巧，请不要将文中的内容用于任何违法的目的，文中所附为试验性的ICMP通讯程序，仅仅提供通过ICMP_ECHOREPLY进行通讯交换数据的功能以供研究；如果你对本文中的内容或代码有疑问，请Mail 

to:Shotgun@xici.net，但是出于网络安全的考虑，本人不会提供任何木马软件及代码。
