---
title: "BlackBerry 8700g 使用两天的一些心得"
date: 2007-05-24T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2655"
---

**Q：怎样刷机？**

A：大家所说的刷机，实际上就是升级BB的ROM，步骤如下：

> 1、到黑莓网站下载blackberry desktop
> manager的最新版本并安装到PC上；
> 
> 2、下载对应的ROM安装程序，也安装到PC上；
> 
> 3、删除c:\Program Files\Common Files\Research In
> Motion\AppLoader\Vendor.xml；
> 
> 4、运行desktop
> manager，此时dm会提示有新版本，按照提示一步步确认即可；

刷机的过程可能会耗费20分钟左右，在这个过程中，不要断开USB连接线，否则有可能导致手机不可用。

另外，可能有时会有最新的英文版ROM已经发布，但没有中文版的情况，这时可以将旧版本中的chinese.alx和java\zh_cn相关内容复制到c:\Program
Files\Common Files\Research In
Motion\Shared下相应的目录中，即可实现所谓的“混刷”。

BB的官方下载地址在：https://www.blackberry.com/Downloads/entry.do?code=E1E32E235EEE1F970470A3A6658DFDD5。

**Q：有什么好的五笔输入法？**

A：bb自带的拼音输入法就不错，但如果热衷于五笔输入，可以参考以下贴子，经测试黑莓五笔输入法可以在8700g上使用，但该输入法严格来说，只是一个应用程序，使用起来较不方便，需要在程序间切换和粘贴，因此只适合大量输入的情况：

http://www.hi-pda.com/forum/viewthread.php?tid=322440&extra=page%3D1&page=1

另外，网上通过autotext（即bb中的智能替换）改造的输入法，我个人不太喜欢，原因一是词库量大，可能导致系统缓慢；原因二是输入英文反而不方便。

**Q：BB是不是可以和我的outlook同步？**

A：当然可以，BlackBerry和Outlook同步支持做得很好，至少能确认Outlook
2003、Outlook 2007可以非常顺利地同步进来。

**Q：我从XX手机迁移到BlackBerry，要怎样把电话本也导过来？**

A：可以有两种方法：一种是将电话本先全部存入SIM卡（中国移动的SIM卡根据时间不同，能存储的号码数量也不一样，应该普遍是150-300个的），
卡放进BB后，再全部复制到电话中；第二种是，将电话本导出成表格后，导入回outlook，再通过outlook同步功能，直接导进BB中。

**Q：我新入手的BB后盖有些松动，感觉很不爽怎么办？**

A：直接在后盖内侧贴几张双面胶，就可以让后盖完全紧贴了。

**Q：怎样上网浏览网页和用gmail收发邮件？**

A：很多人写的GPRS上网步骤，令人看起来头大如斗，其实，只要是ROM的版本在4.1.351之后，要上网都非常简单，步骤如下：

> 1、确认你的手机号码已经开通GPRS服务；
> 
> 2、确认选项->网络->数据服务中的设置是“打开”；
> 
> 3、确认选项->高级选项->TCP中的APN设置为CMNET，用户名与口令均留空；
> 
> 
> 4、到http://www.operamini.com/下载并安装OperaMini软件并安装；
> 
> 5、接入你希望注意的网页，例如浏览你的gmail邮件：http://m.gmail.com

**Q：在Blackberry上能不能用即时通讯软件，比如gtalk？**

A：在BlackBerry上可以很好地使用qq、msn、gtalk、Yahoo
Messenger、ICQ等软件进行交流，详细情况可以参考《BlackBerry Instant
Messaging FAQ》一文，链接是：

http://www.blackberryforums.com/aftermarket-software/2973-blackberry-instant-messaging-faq-msn-aim-icq-yahoo-chat.html。

我在BlackBerry上并不喜欢用IM，因此只测试了GoogleTalk，采用的是testa客户端，效果相当不错，软件下载及详细信息可以参见以下链接：

http://www.maxpda.com/thread-35697-1-1.html

**Q：用什么软件阅读电子书比较好？**

A：下载Mobipocket Reader的PC端，并通过它安装Mobipocket
reader到手机上，同时也可以用该阅读器的PC端制作和传输电子书到bb上，下载地址为：

http://www.mobipocket.com/en/DownloadSoft/application.asp?device=Blackberry

**Q：怎样为你的VIP设置独特的铃声与头像？**

A：在通讯薄里选定你的VIP用户，单击滚轮，可以看到“添加自定义电话铃音”和“添加图片”。8700g支持mp3铃音，因此你也可以自己录制mp3文件并通过DM上传，就象[“喜洋洋”同学的铃音](http://www.i170.com/Attach/5D63838C-03E2-4AEA-BDED-F835EE4DEEAF)。

**Q：我想将屏幕上的图像截下来和朋友们分享，该怎么做？**

A：可以采用由mincwolf写的BBScreen软件，连接USB线后，就可以在PC上操作，直接截屏。程序的下载地址：http://www.cnvanke.com/ShowArticle.asp?ArticleID=51。

**Q：我能否给手机加个密码，这样别人就没办法乱动我的电话了？**

A：在选项->安全选项->一般设置->密码中，将设置改为“已启用”，关机或锁屏后要使用手机，就必须输入密码（但该功能需要慎用，
因为默认设置输错10次密码后，会清除手机中的数据，如果有朋友“暴力猜测”你的密码，有可能会导致手机内的数据完全丢失）。

**Q：有哪些BlackBerry的资源吗？**

A：英文网站：http://www.blackberryforums.com/

   中文网站：http://www.maxpda.com/
