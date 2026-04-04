---
title: "MAC新手使用记录"
date: 2007-06-23T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2721"
---

**一、更好地使用MAC的小技巧**

1、锁定屏幕

打开系统预置->帐户->点按锁按钮以进行更改->登陆选项->启用快速用户切换，之后在屏幕右上角，就会有你的登陆帐号，点击该帐号->登陆窗口，屏幕就会切换回登陆界面。

2、善用expose

打开系统预置->Dashboard与Expose，设置左上角为全部窗口，右上角为应用程序窗口，左下角为Dashboard，右下角为桌面。这样设置之后，切换窗口可以不用Command+Tab，而是直接将鼠标移到屏幕的左上角……的确很方便。

3、让终端支持中文显示与输入

打开终端(Terminal.App)

编辑个人目录下的.profile，添加

> alias ls='ls -a -w -G'
> 
> LANG="zh_CN.UTF-8"
> 
> export LANG

编辑个人目录下的.inputrc(默认不存在)

> set convert-meta off
> 
> set input-meta on
> 
> set output-meta on

打开终端菜单上的终端->窗口设置->仿真，去掉忽略非ASCII字符

终端->窗口设置->显示，选上宽字形，设置UTF-8为默认字符集，并将设置用作预设即可。

这些小技巧都是[silence](http://wuhongsheng.com/)教我的，多谢 ;)

**二、快捷键**

在Finder里点击Command +
K：可以方便地打开SMB连接，服务器地址填入smb://server/

Command + Option + H：隐藏其它应用程序，突出显示当前程序

Command + A：全选

Command + C：拷贝

Command + O：打开（类似鼠标双击）

Command + V：粘贴

Command + N：建立新文件夹

Command + X：拷贝并删除

Command + W：关闭窗口

Command + P：打印

Command + Option + W：关闭所有窗口

Command + S：文件存盘

Command + Q：退出软件

Command + M：建立替身

Command + Y：弹出所选磁盘

Command + Z：恢复上一步状态

Command + I：查看所选对象信息

Command + Delete：把所选对象移进垃圾桶

Command + R：显示原身

**三、我安装的免费应用软件**

快捷启动：[Quicksilver](http://www.quiksilver.com/)

输入法：[FunInputToy](http://fit.coollittlethings.com/)

网页浏览：[Firefox](http://www.mozilla.com/)，可以作为safari的替代，safari对部份网页的支持还不够完善。

FTP：[cyberduck](http://cyberduck.ch/)

文字处理：[CotEdit](http://www.aynimac.com/p_blog/)，中文支持相当好，也支持语法高亮，普通应用足够了。

即时通讯：[Skype](http://www.skype.com/)，[Microsoft
Messenger](http://www.microsoft.com/mac/downloads.aspx#Messenger)，[LumaQQ](http://lumaqq.linuxsir.org/)

视频播放：[MovieTime](http://www.sansworks.com/)，[RealPlayer](http://forms.real.com/real/realone/mac.html)，[MPlayer
OSX](http://www.mplayerhq.hu/)，[Flip4Mac](http://www.flip4mac.com/wmv_download.htm)

解压缩：[Stufflt
Expander](http://www.stuffit.com/detect_expander.html)

看图：[Xee](http://www.macupdate.com/info.php/id/19978)

察看电池状态：[coconutBattery](http://www.coconut-flavour.com/coconutbattery/index.html)

地图：[Google Earth](http://earth.google.com/)

思维导图：[FreeMind](http://freemind.sf.net/)

局域网通讯：[IPMessenger](http://wulujia.com/Article_70830)

无线网络挖掘：[iStumbler](http://www.istumbler.net/)

终端服务连接：[Remote
Desktop Connection](http://www.microsoft.com/mac/downloads.aspx?pid=download&location=/mac/download/misc/rdc_update_103.xml&secid=80&ssid=10&flgnosysreq=True)

网络音乐：[Last.fm](http://last.fm/)

**四、商业软件**

流程图绘制：[OmniGraffle
Professional](http://www.omnigroup.com/applications/omnigraffle/)，MAC下面的流程图，画出来果然更漂亮

项目管理：[OmniPlan](http://www.omnigroup.com/applications/omniplan/)，类似于微软的Project

虚拟机：[Parallels
Desktop](http://www.parallels.com/)

软件下载：[Speed
Download](http://www.yazsoft.com/)

思维导图：[Mindjet
MindManager](http://www.mindjet.com/)，还是有不少人喜欢用它，虽然freemind能打开MM，但MM不能打开FREEMIND，还是装上

办公套件：[Office
2004](http://www.microsoft.com/mac/products/office2004/office2004.aspx?pid=office2004)、[iWork06](http://www.apple.com/iwork/)

程序编辑：[TextMate](http://macromates.com/)

**五、Widget**

系统状态：[iStat
Pro](http://www.apple.com/downloads/dashboard/status/istatpro.html)

字典：[WikiPedia](http://www.apple.com/downloads/dashboard/reference/wikipedia.html)

日历：[ChinaCalendar](http://www.apple.com/downloads/dashboard/status/chinacalendar.html)

各位用MAC的朋友们要是有什么好的软件，或者好的使用习惯推荐，麻烦跟个贴告诉我吧，让我的这个转换历程更短更顺利一些
:)
