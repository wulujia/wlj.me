---
title: "了解你的敌人"
date: 2000-07-21T00:00:00+08:00
tags: ["Security", "Translation"]
draft: false
slug: "xfocus-honeynet-enemy"
---

> 本文是 Honeynet Project 的"了解你的敌人"系列文章的中文翻译，原文发布于 [project.honeynet.org](http://project.honeynet.org/)，中文翻译来自 [xfocus.net](http://www.xfocus.net/)。

我的长官经常对我说：在敌人面前好很好的保护自己，你必须先了解敌人先。(孙子兵法：知己知彼，百战百胜)。这句军事用语现在也很好的应用于网络安全领域中了，就象作战一样，你要保护自己的资源，你需要知道谁是你最大的威胁和他们会怎样攻击。在这个系列中的第一篇文章，就是讨论一种很流行很广泛的来自Scritp
Kiddie所使用的工具和方法，如果你或者你的组织有任何资源连接到Internet上，你就有此类的威胁。

Know Your Enemy文章主要是涉及到blackhatck团体使用的工具，策略和动机。而[Know
Your Enemy:II](http://www.xfocus.net/honeynet/papers/enemy2/index.html)主要集中于你怎样能探测这些威胁，判断他们所使用的工具和他们在你系统上寻找什么样的漏洞。[Know
Your Enemy:III](http://www.xfocus.net/honeynet/papers/enemy3/index.html)集中讨论攻击者获得ROOT后在系统上怎样操作，特别是他们是如何掩盖他们的踪迹和他们下一步主要干什么。[Know
Your Enemy: Forensics](http://project.honeynet.org/papers/forensics/index.html) 涉及了你怎样分析一种攻击。[Know
Your Enemy: Motives](http://www.xfocus.net/honeynet/papers/motives/index.html) 通过捕获black-hat团体之间的通信和联系来分析他们的动机和心理状态。[Know
Your Enemy: Worms at War](http://www.xfocus.net/honeynet/papers/worms/index.html) 描述了WORM蠕虫是怎样自动攻击WINDOW系统的。 

**什么叫Script Kiddie **

Script kiddie是一些专门找寻一些容易下手资源的人，他们不专门针对某种特定信息或者目标特定公司，他们的目标是尽可能的用最简单的方法获得ROOT，他们通过搜集一些公开的exploit信息并搜索整个Internet来找寻有这种exploit漏洞的资源，这样，不管怎样，总有某些人会被他们操作。

其中一些高级点的家伙会开发他们自己的工具，并留下一些复杂的后门，另外一些根本就不知道他们做什么，就知道怎样在命令行打"go"的人。忽略他们的技术水平不说，Script
kiddie就是共享一些公共策略，随机搜索某个特殊漏洞并利用这个特殊漏洞的人。

** 他们形成的威胁在哪里？**

由于Script kiddie是随机选择目标，所以存在的威胁是你的系统迟早会被[扫描](http://www.xfocus.net/honeynet/papers/enemy/probed.txt)到，我知道管理员很惊讶他们的系统在设置以后没几天也没有告诉任何人的时候就被扫描到了，其实这一点也不值得惊讶，因为Scritp
kiddie一般是扫描一段网络来操作的。

如果扫描只能限制在几个独立的资源，你可能会很安心，因为Internet上千千万万的机器，扫描到你的机器的几率少之又少。但是，事实不是你想象的这样，目前多数工具能很方面的使用大范围扫描并广泛传播，任何人可以使用他们，使用这些工具的人数增长率呈现惊人的速率。Internet是一个无国界的区域，这种威胁就很快转播到世界各个地方，有这么多人使用这些工具，你被探测就不是问题了。

试图以含糊其词来搪塞你的安全问题会害了你:你或许会认为没有人知道你的系统，你就会安全，或者你认为你的系统没有价值，他们为何要探测你，其实这些系统正是scritp
kiddies搜寻的目标--没有任何保护的系统，非常容易得手的系统。 

** 具体方法讨论**

Scritp kiddie的方法很简单，扫描Internet有特定缺陷的系统，一但查找到，便对它下手，他们用的许多工具会自动操作，不需要很多的交互。你只要打开工具，然后过几天回来看看你的结果就可以了。没有两个工具是相同的就象没有两个漏洞是一样的，但是虽然如此，许多工具的策略是一样的，第一，开发要扫描的IP段，然后扫描这些IP段中特定的漏洞。

例如:我们假定一个用户有一个工具可以利用Linux系统上的imap漏洞，如[imapd_exploit.c](http://www.xfocus.net/honeynet/papers/enemy/imapd_exploit.txt)，开始，他们开发一IP数据库来扫描，一旦IP数据库构建好，用户会想判断系统是否运行LINUX系统。目前许多扫描器可以通过发送不正常的信息包到目标系统并查看他们如果响应便可很方便的判断操作系统，如Fyodor的[nmap](http://www.insecure.org/nmap),然后，工具会判断LINUX系统是否运行着imap服务，最后就是利用imapd_exploit.c程序来进入系统了。

你会想所以这些扫描会有很大的动静，很容易引起注意，但是，很多人没有很好的监视他们的系统，并不认识到他们正被扫描，而且，许多script kiddies在查看他们所要利用的系统时也会保持相当的安静，一旦他们利用这个漏洞进入系统，他们就会使用这个系统作为跳板，并不带任何包袱的扫描整个系统，因为如果这种扫描被抓获，责任是系统管理员而不是那些script-kiddie.

所有这些扫描的结果经常被用来归档或者在其他用户中共享，以便在以后的日子里使用，如用户在最初为了某个漏洞扫描出来的LINUX系统开了那些端口的数据库后，过一点时间，一个新的漏洞被发现以后，用户可以不用重新构建或者扫描新的IP段，他可以很方便的来查看以前归档的数据库并来利用这个新发现的漏洞。其他变相的，用户可以交流或者买卖有漏洞系统的数据库。你可以看[Know
Your Enemy: Motives](http://www.xfocus.net/honeynet/papers/motives/index.html)文章中的例子，这样造成scritp kiddie可以不扫描系统而破坏你的资源。

有些Black-hats会采用木马或者后门来种植在破坏的系统中，后门允许方便的随时的让攻击者来访问你的系统，而木马使入侵者难于被发现，这些技术可以让他们的操作不显示在任何LOG记录，系统进程或者文件结构上，他可以构建一个舒适安全的环境来扫描Internet，跟详细的信息请看:[Know
Your Enemy: III](http://www.xfocus.net/honeynet/papers/enemy3/index.html)。

这些攻击没有限制在一天中的任何时间，许多管理员搜索他们的LOG记录来查询当晚发生了什么，并相信这是攻击者的攻击时间，其实script kiddies在任意时间进行攻击，他们一天24小时的进行扫描，你根本不能考虑到你什么时候会被探测到。而且由于Internet的无边界性，时间也就不确定了，攻击者当地在午夜在攻击，而你这里可能是在当地时间下午一点种。
以上对系统漏洞的扫描可以用于多种用途，近来，一种新的拒绝服务攻击--分布式拒绝服务攻击DDoS，就是攻击者一个人控制了很多台有漏洞的系统，他可以遥控这些控制的系统来共同对目标系统执行拒绝服务攻击。由于多个系统被使用，所以防卫和判断源攻击地也变的非常困难。要控制多个系统，Script
kiddie的策略就变的很有用，有漏洞的系统随机被判断并用来作为DDOS的垫板，越多的系统被控制，DDOS攻击的强度就越大。如[stacheldraht](http://www.xfocus.net/honeynet/papers/enemy/ddos.txt)，要了解关于更多的分布式拒绝服务攻击和怎样保护自己，请查看Paul
Ferguson站上的[Denialinfo](http://www.denialinfo.com/)。

**工具**

这些工具一般使用起来很见大，许多工具一般只是几个选项来完成单个目标，开始工具用来构建IP数据库，这些工具很随机的扫描Internet，如一个工具有一个单一的选项，A，B和C，你可以选择一个字母来决定要扫描的网络大小，这工具然后就选择A，B，C相应的IP网络进行扫描。另一个工具使用域名如z0ne，这个工具通过对域名和子域名的区域传输操作来构造IP数据库，用户通过扫描整个.com或者.edu域来获得2百万或者更多的IP数据库，一旦发现这些IP，它们就被会被工具用户判断版本名字，操作系统，所运行的服务，如果发现系统有漏洞，black-hat就会马上进行攻击。要更好的理解这些工具，请看[Know
Your Enemy: Forensics](http://www.xfocus.net/honeynet/papers/forensics/index.html)。

**怎样防止这类威胁 **

下面的一些步骤你可以比较好的保护你的系统，第一，script kiddie一般找寻容易下手的对象，如一些很公开很容易得手的漏洞系统，保证你的系统和网络不受这些漏洞的影响，[www.cert.org](http://www.cert.org/)
和[www.ciac.org](http://www.ciac.org/)是了解这些漏洞很好的资料库。同样地，[bugtraq](http://www.securityfocus.com/forums/bugtraq/faq.html)
([securityfocus.com](http://www.securityfocus.com/)的一个邮件列表 ) 也是获得这些漏洞信息很好的地方。另一个保护你自己的方法是只运行你需要的服务，如果你不需要某个服务，关掉它，如果你确实要使用某个服务，确保你的服务版本是最新的。要怎样操作，请看这些文章：Armoring
[Solaris](http://www.xfocus.net/honeynet/papers/enemy/armoring.html)
, [Armoring
Linux](http://www.xfocus.net/honeynet/papers/enemy/linux.html) 或者[Armoring
NT](http://www.xfocus.net/honeynet/papers/enemy/nt.html).

上面知道，DNS服务器是经常被用来找寻IP数据库的对象之一，你必须在你的名字服务器上限制区域传送的操作，记录任何未认证的区域传输并跟踪他们。我强烈建议升级BIND到最新的版本，你可以在下面的地址找到：[www.isc.org/bind.html](http://www.isc.org/bind.html).
最后监视你被探测的系统，你可以跟踪这些探测操作获得更多对你网络有威胁的举动。

**总结**

Scritp kiddie会对所有系统有威胁，他们没有任何偏爱，任何系统他们都挑，不计较地点和价值。不管怎样，你迟早会被扫描到。通过了解他们的动机和方法，你可以很好的对付这些威胁而更好的保护你的系统。
