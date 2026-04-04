---
title: "从规则集看IDS网络探测器的检测能力"
date: 2003-03-01T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-486"
---

文章提交：[stardust](http://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=20) (bugmail_at_telekbird.com.cn)

随着企业和组织对网络安全的日益重视，网络IDS产品以其强大的检测攻击的能力已经成为必要的防火墙、防病毒产品后又一个安全组件设备。从检测方式看IDS产品可分为基于规则（基于误用）和基于异常。基于规则的IDS技术相对成熟，检测准确性可以做的很高，但致命弱点是和反病毒产品一样只能检测已知攻击。基于异常的检测技术还不太成熟，检测准确性不太高，但其最大的优势是通过分析异常检测某些未知攻击，是当前理论界和工业界的研究热点[1]，随着研究的深入在不久的将来很可能逐步取得突破（实际上以协议分析技术为基础协议异常分析已经相当成熟了）。

从IDS检测引擎的实现上主要有两种，一种是简单的ngrep类型的引擎，这种检测引擎对数据包作基本的IP/TCP/UDP/ICMP等三、四层协议解码后就结合数据包数据区的内容匹配来检测攻击，这种实现方式的优点是实现简单，加入规则容易，在规则总数较少的情况下效率较高。ngrep类型的引擎缺点也非常明显，由于只对数据包内容做生硬的匹配无法抵抗多种的变形攻击，非常容易受到愚弄而被绕过，也因为数据匹配的范围很大，在规则总数大量增加的情况下引擎的效率会极剧下降。为了减少ngrep类检测引擎与生俱来的缺陷，当今主流IDS网络探测器普遍使用了高层协议分析技术，也就是加入了对第七层应用层协议的解码和状态分析，这样做虽然很大程度上加大了检测引擎的复杂性，但极大的提高了检测的准确性并能检测检测到某些协议异常的未知攻击，由于匹配区间的减小，在大量加载规则的情况下也不会造成性能太大下降，因此基于协议分析的引擎比单纯的ngrep类型的检测要高级的多。

目前市面上充斥了大量的IDS产品，都号称自己是优秀的产品，拥有强大的检测能力，是否真如厂商所称的那样呢？当然你可以读各种各样的厂商或第三方的产品测试报告来试图了解个大概，但IDS产品的测试非常复杂，涉及到各种技术和环境的影响，因为IDS技术从整体上还不成熟，所以应该说当前大多数的IDS评测也是极不完善的，从测试方法上就存在很多先天的缺陷，其结果并不能真实反映产品实际环境下的能力，有时候评测结果甚至完全是误导性的。

现在主流的IDS产品是采用完全基于规则的或者基于规则与基于异常结合的检测方式。如果厂商允许用户查看或定制IDS的规则集，那么我们可以从此侧面大致了解清楚IDS探测器的实际能力，因为IDS规则的描述方式及提供的检测选项直接反映了IDS探测器对检测内容及方法的支持能力。

下面我们来分析几个公开了规则集的IDS产品（Snort 1.8.6、Dragon IDS 6.0、NFR NID-100、天阗IDS 5.31）的规则定义，由此来从一定程度上评价IDS探测器的检测能力。

Snort

=====

Snort是最出名的开放源码的IDS系统，它的规则集[2]是一些大致以应用层协议分类的.rules文本文件，比如dos.rules文件存放拒绝服务攻击类的规则；ftp.rules文件存放FTP服务相关的规则；telnet.rules文件存放FTP服务相关的规则。规则文件中每行定义一种攻击检测，例子如下：

alert tcp $EXTERNAL_NET any -> $HOME_NET 21 (msg:"FTP SITE CPWD overflow attempt"; flow:established,to_server; content:"SITE "; nocase; content:" CPWD "; nocase; content:!"|0a|"; within:100; reference:bugtraq,5427; reference:cve,CAN-2002-0826; classtype:misc-attack; sid:1888; rev:3;)

一条Snort规则可以分为前后两个部分，规则头和后面的选项部分。规则头包含有匹配后的动作命令、协议类型、以及选择流量的四元组（源目的IP及源目的端口）。规则的选项部分是由一个或几个选项的符合，所有主要选项之间是与的关系。选项之间可能有一定的依赖关系，选项主要可以分为四类，第一类是数据包相关各种特征的描述选项，比如：content、flags、dsize、ttl等；第二类是规则本身相关一些说明选项，比如：reference、sid、classtype、priority等；第三类是规则匹配后的动作选项，比如：msg、resp、react、session、logto、tag等；第四类是选项是对某些选项的修饰，比如从属于content的nocase、offset、depth、regex等。

总的来说，Snort的规则相当有特色，简单高效，体现在规则选项概念清楚明确，选项之间没什么从属关系，规则所提供了丰富的选项用以匹配各种包特征，通过对选项加以组合基本上就能清楚地描述出基于单包的攻击，绝大多数规则只需要一行代码就行。

Snort设计之初是一个ngrep类型的IDS，合适检测基于单包的攻击，是在基本TCP/IP解码的基础上对数据包的数据区进行匹配，对规则选项也不允许复杂的逻辑组合，这种粗糙的检测方式存在很高的漏报误报而且极容易受到反IDS手段（比如变形shellcode）的愚弄。新的高层协议分析技术可以很大程度地避免此类问题，提高检测准确率。Snort逐渐加入一些高层协议（当前支持最常用的HTTP和TELNET）的部分解码，比如在下面的规则使用了较新版的Snort引擎提供的uricontent选项用来匹配HTTP URI请求中的文件名。

alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (msg:"WEB-CGI HyperSeek hsx.cgi directory traversal attempt"; uricontent:"/hsx.cgi"; content:"../../"; content:"%00"; flow:to_server,established; reference:bugtraq,2314; reference:cve,CAN-2001-0253; classtype:web-application-attack; sid:803;  rev:6;)

以上规则检测HTTP请求的URI中是否包含“hsx.cgi”文件名，并检查数据区是否包含“../../”字串，如果攻击者企图利用hsx.cgi脚本的目录遍历漏洞，应该会在同个数据包的数据区搜索到“../../”这个表示遍历上级目录的字串序列。

Snort在全世界志愿者的努力支持开发下，一直在不停地改进中，基本每个新版都会增强一定的引擎的检测能力，同时在规则集中也加入了新的选项。但从总体看由于Snort初始的框架设计限制，其技术水平与主流的商业IDS产品相比还是越拉越大，相对越来越落后。

Dragon IDS

==========

Dragon IDS是Enterasys Networks公司开发的入侵检测系统，它获得了不少的奖项，包括Network Computing杂志的2003年度产品奖。作为一个完整的IDS产品，Dragon现在拥有网络探测器和主机探测器，网络探测器部分它开放了全部的规则集并提供了详细的文档说明如何解释和设置检测规则。

Dragon IDS网络探测器的规则集一般存放在名为dragon.sigs的文本文件中，文件中每行一条规则，示例如下：

[root@ /usr/dragon/sensor/conf]> head dragon.sigs

# Copyright 2000 Network Security Wizards

# Wed Nov 29 12:13:52 2000

U D A B  10  20     H BACK-ORIFICE:DIR     /ce/63/d1/d2/16/e7/13/cf/3c/a5/a5/86

U D A B  10  20     H BACK-ORIFICE:INFO    /ce/63/d1/d2/16/e7/13/cf/39/a5/a5/86

U D A B  10  20     H BACK-ORIFICE:SCAN    /ce/63/d1/d2/16/e7/13/cf/38/a5/a5/86

T S A B 100  20  5600 BLADE-RUNNER         Blade/20Runnner/20

T D A S  50  40     W CARBO:COMMAND        /2fcarbo.dll/3ficatcommand

T D A B  15   2  7161 CISCO:5000-DOS       /0a

T S A B   5   6  1999 CISCO:IDENT-SCAN     cisco

每条规则一般由多个或单个的空格相隔的九个字段构成，对每个字段含义解释如下（整理自Dragon提供的手册）：

T D A S 10 20 80 WEB:CGI-PHF get/20/2fcgi-bin/2fphf

| | | |  |  |  |      |               |

| | | |  |  |  |      |               匹配的字串（/开头的为十六进制值）

| | | |  |  |  |      事件名

| | | |  |  |  端口（TCP或UDP包的端口）

| | | |  |  |

| | | |  |  比较的字节数（数据包数据区的前多少字节，也就是比较深度）

| | | |  |

| | | |  动态记录包数（给后续规则处理的数据包数）

| | | |

| | | 二进制或文本（S:匹配文本，匹配时大小写不敏感，要匹配的字串必须全部小写形

| | |               式; B:匹配二进制串，匹配过程大小写敏感）

| | |

| | 针对的网络流量（A:所有流量; T:去往受保护网络的流量; F:去往受保护网络的流量;

| |                 I:受保护网络内部的流量; X:受保护网络外的流量; D:先前规则处

| |                 理的后续流量）

| |

| 方向（A:匹配源目的中的任意一个端口; B:两者都匹配; D:匹配目的端口; S:匹配源端口）

|

协议（T:TCP; U:UDP; I:ICMP; 其他IP协议:数字）

可以看到Dragon规则是很简单的，基本上就是几个数据包特性选项的与关系组合，匹配特定网络流量的特定数据特征。规则只提供了储如数据包网络层协议、端口、方向及数据区的字串匹配选项给用户，很明显这些特征对于描述日益复杂的网络攻击是远远不够的。比如用户无法指定一些如包数据区大小、包的标志位及TTL等细节特征，对于数据区的匹配指示也非常的弱，只能指定匹配数据区的前多少字节，而无法指定具体匹配数据区的哪几个字节，同样也无法组合数据区的多个特征进行综合判断。这样差劲的数据包描述能力必然会带来很大的漏报和误报，比如Whisker CGI扫描器[3]的一种流行的变形方式（GET /长随机字串/../vulnerable.cgi）可以很轻松的躲过上例规则的检测，而且很多的攻击根本就无法描述，因为规则描述能力上的限制可以肯定的说Dragon IDS攻击检测能力上连Snort都不如。从规则集的整体来看，因为没有深入分析到高层协议，可以很有把握的判断Dragon IDS网络探测器基本上是一种ngrep类型的检测引擎，这种简单粗放的检测引擎已经是处于淘汰行列的技术。

NFR

===

NFR（Network Flight Recorder）是一个老牌的商业网络IDS产品，在很多的评测中表现出色，最近的版本增加了主机探测器，该产品现在由NFR Security公司维护。NFR最初由Firewall的牛人Marcus J. Ranum创建，是作为一个通用的网络流量分析和记录软件来实现的[4]，为了最大限度地发挥分析工具的灵活性，NFR提供了完善强大的N-Code脚本语言，NFR的检测引擎如何动作完全由N-Code来决定。NFR的网络探测器其实只是提供了一个网络流量分析底层框架，把N-Code[5]作为接口提供给用户，引擎部分完成基本的IP/TCP/UDP等协议的解码，重组IP分片和TCP分段，并按N-Code的编程作进一步的分析。N-Code是一个完整的编程语言，包括流控制、过程、变量及各种数据类型，利用它可以完成相当复杂细致的数据包分析工作，这种能力在检测复杂的攻击，减少漏报和误报方面比只使用简单规则描述的IDS产品有着无可比拟的优势。NFR完全开放了所有其用于检测的N-Code代码并提供了开发和编辑N-Code代码的文档和工具，用户可以方便地开发自己的监控和统计网络流量检测代码，几乎具有无限的灵活性，因此NFR可以说是最可定制的IDS系统。NFR早期版本是开放源码的，当时的l0pht组织为其写了大量检测网络攻击的N-Code，后来出于商业运作的需要NFR在98年底的2.02研究版后封闭了源码。

NFR用于检测攻击的N-Code被层次化地组织起来，多个功能相近的共享某些代码的N-Code被组织成一个Backend，多个相关服务相近或功能相近的Backend被组织成一个Package，形成一个树状结构。这样一个结构能比较好地保证代码的简洁，但更新维护上也相对会麻烦的多，这是脚本语言的特点，很难两全。

下面是一个早期检测Web CGI攻击的N-Code例子，作些注释以了解N-Code的工作方式。最新检测Web攻击的N-Code已经是基于协议解码的代码，有很高的准确性，完全不是这个样子了，只是代码太长无法作为例子贴出来，有兴趣的可以自己找来看看。

---------------------------------------------------------------------------

# 下行定义记录数据的方式、参数

badweb_schema = library_schema:new( 1, ["time", "int", 

                                        "ip", "ip", "str"], scope());

# list of web servers to watch.  List IP address of servers or a netmask 

# that matches all. use 0.0.0.0:0.0.0.0 to match any server

da_web_servers = [ 0.0.0.0:0.0.0.0 ] ; # 定义Web服务器的IP地址范围

query_list = [ "/cgi-bin/nph-test-cgi?",

               "/cgi-bin/test-cgi?", 

               "/cgi-bin/perl.exe?", 

               "/cgi-bin/phf?" 

                ] ;  # 待检测的有漏洞的CGI程序名列表

filter bweb tcp ( client, dport: 80 ) # 从TCP数据流中选取从客户端到服务器端80端口的流量对其操作

{

        if (! ( tcp.connDst inside da_web_servers) )

                return;  # 如果连接为内部Web服务器之间的则不检测

        declare $blob inside tcp.connSym; # 声明$blob变量与一个TCP连接关联，每个TCP会话都有自己的$blob变量

        if ($blob == null)

                $blob = tcp.blob; # $blob变量内容为空，则把tcp包的数据区内容赋给它

        else

                $blob = cat ( $blob, tcp.blob ); # $blob变量有内容则把tcp包的数据区内容加在其后

        while (1 == 1) { 

          $x = index( $blob, "\n" );  # 定位$blob串中的换行符，返回换行符在串中的位移到$x变量

          if ($x < 0)           # 如果没有找到换行符则跳出循环

            break;

          $t=substr($blob,$x-1,1);      # 查找换行符前有无回车符

          if ($t == '\r')

            $t=substr($blob,0,$x-1);    # 取回车换行符的字串到$t

          else

            $t=substr($blob,0,$x);

          $counter=0; # 记数器变量置0

          foreach $y inside (query_list) { # 依次在串中搜索有漏洞CGI脚本名列表

            $z = index( $blob, $y ); 

            if ( $z >= 0) {

              $counter=1;

              # save the time, the connection hash, the client,

              # the server, and the command to a histogram

              record system.time, tcp.connHash, tcp.connSrc, tcp.connDst, $t to badweb_hist;

              # 记录数据

            }

          }

          if ($counter)

            break;

        }

        # keep us from getting flooded if there is no newline in the data

        if (strlen($blob) > 4096)

                $blob = ""; # 如果$blob串过长，可能是有问题，清空

        # save the blob for next pass

        $blob = substr($blob, $x + 1); # $blob值由回车换行符的串值代替，准备下一次检测

}

badweb_hist = recorder ("bin/histogram packages/test/badweb.cfg",

        "badweb_schema" ); # 定义记录的格式

--------------------------------------------------------------------------------- 

总而言之，NFR基于N-Code脚本语言的检测方式是相当灵活的，最新检测代码对很多常用协议进行了应用层协议的解码，可以实现非常精确的检测，只要脚本编写周全基本上没有误报的可能。但相对其他IDS产品来说，N-Code还是相当复杂的，要熟练地使用N-Code，不仅要了解其语法，更重要的是对TCP/IP及应用层的协议集有相当深入的认识，不然不可能编写出简洁高效的检测代码，对代码的测试和使用也有一定的难度，不利于对攻击的快速响应。所以NFR更适合那些希望定制系统的高级用户。

天阗

====

天阗IDS是启明星辰公司的主要安全产品，是国内比较出名的IDS产品。最新的5.5版本集成了网络探测器和主机探测器，下面分析的是5.31版IDS网络探测器的规则集，5.5版的规则集文本被编了码，所以无法了解具体内容，可能有很大改进也可能差不多。

天阗IDS对于攻击的描述语言（也就是规则）分类两种，1次事件描述语言和2次事件描述语言： 

1次事件描述语言：基于资料模式的网络事件（启明星辰公司自己的定义）。

1次事件规则文件一般为位于探测器conf/目录下的dt1_event.dat文件，此文件为一文本文件，和很多IDS产品一样每行定义一个待检测的事件。

下面是规则文本中的行规则定义

--------------------------------------------------------------------------------------------------

IP_协议不可识别    IP    28111106    ip_type~1,2,6,8,17    C    类型=ip_type

非IPV4版本    IP    28111107    ip_version~4    C    版本=ip_version

IP_头长度错误    IP    28111105    ip_hlength<20    C    长度=ip_hlength

HTTP_缓冲区溢出    HTTP    263A3A31    http_cmd_length>500&http_url^host    C    长度=http_cm

d_length

HTTP_Unix_Password访问    HTTP    263A3A36    http_url^/etc/passwd    Q    URL名称=http_url_s

tr

HTTP_执行命令    HTTP    263A3A35    http_url^.bat,.cmd    Q    URL名称=http_url_str

HTTP_点点命令    HTTP    263A3A34    http_url^/..    C    URL名称=http_url_str

FINGER_Cybercop查询    FINGER    27368006    [ustr.0]^%0A%20%20%20%20%20    Q    用户名称=fin

ger_user

--------------------------------------------------------------------------------------------------

可以看到每行规则文本是由TAB隔开的几个字段组成，第一个字段是规则名，第二个是涉及到的协议类型，第三个是规则的ID号（好象有一定的生成算法），第四个是最重要的检测事件定义，第五个是事件之间的关系（此字段到底起什么作用还未搞清楚），第六个字段定义了探测器检测到事件后需要向控制台发送的附加数据。

从上面的例子来看，启明IDS一次事件的定义特别是检测事件的定义还是比较简单的，对于检测事件的定义基本上就是引擎所提供的选项是否满足条件的判断之间的逻辑（与和或的关系）组合，对于选项是否满足条件的判断，IDS引擎提供如下几种操作符：

操作符：

= 等于

~ 不等于

> 大于

< 小于

! 倒序匹配

^ 包含

` 不包含

从现有最新规则集来看“!”和“`”操作符还被没有用到。知道了这些，可以很容易地了解事件匹配的含义，对于上面例子的第一条，所有ip_type不等于1,2,6,8,17的事件都被认定为“IP_协议不可识别”事件。上面规则第四条把所有HTTP请求命令长度大于500字节而且HTTP请求的文件名中包含“host”字串的请求都识别为“HTTP_缓冲区溢出”事件。

通过整体分析天阗5.31版网络探测器的1次事件定义，可以看到启明的IDS引擎基本上一个相对比较高级的应用层协议分析引擎，除了对ETHER、IP、ARP、ICMP、TCP、UDP、IGMP这7种基本的网络层、运输层协议解码以外，还对FTP、TFTP、TELNET、RLOGIN、FINGER、AUTH、WHO、SNMP、HTTP、NNTP、IRC、DNS、SMTP、POP3、IMAP、NFS、PMAP、RIP、NETBIOS、ECHO、CHARGEN、WHOIS、NTALK、MSSQL、SUNRPC等应用层协议做了或深或浅的解码（可以从引擎提供的相关可匹配选项来确定）。但对于字符串匹配只能定义开始匹配的位移点，而不能很精确地指定匹配的范围，对于匹配功能的支持上并不如Snort规则那样灵活，可能是天阗IDS引擎的协议解码能力削弱了对这方面能力的需求。然而有时候能灵活地指定匹配范围是非常有用的，检测很多溢出攻击并不需要应用层协议的解码，最近的例子就是几乎把整个Internet彻底搞垮Slammer蠕虫：检测此蠕虫利用的SQL服务器的那个溢出漏洞其实很简单，只要检测到发往UDP/1434端口的数据包数据区的第一个字节为0x04并且数据区长度大于一个阀值就可以完全认定是一个溢出攻击[6]，此攻击连Snort也可以编写规则从原理上检测出来，可

是从天阗IDS提供规则描述语言来看则无法从原理特征上描述。蠕虫出来以后，天阗加入检测规则，但只是匹配蠕虫数据包中的一个特征串，这并没有从原理上解决问题，攻击者只要对数据包内容稍做修改就能躲避检测。

2次事件描述语言：基于统计的行为分析事件（启明星辰公司自己的定义）。 

2次事件是对1次事件进行基于时间统计的再分析基础上产生的事件，事件定义文件条目的例子如下：

--------------------------------------------------------------------------------------------------

TCP_SYNFLOOD_拒绝服务    TCP_SYN    4B228425    Num(event,dip,dport)>500.1    M 

UDP_端口扫描    UDP_不可识别    48248007    num(event,sip,dip,^dport)>50.1    M 

UDP_碎片洪流    UDP_碎片    48248406    num(event,sip,dip,dport)>50.1    M 

FTP_口令弱    FTP_注册成功    49313114    pass(event=FTP_口令,sip,dip,sport,dport)>1.1&

pass(event=FTP_用户名称,sip,dip,sport,dport)>1.1    M 

RLOGIN_口令弱    RLOGIN_口令    49353501    Pass(event=RLOGIN_用户名称,sip,dip,sport,dp

ort)>1.1|pass(event,sip,dip,sport,dport)>1.1    M 

--------------------------------------------------------------------------------------------------

2次事件规则文件一般为位于探测器conf/目录下的dt2_event.dat文件，此文件为一文本文件，结构与1次事件的定义文件相似，也是每行一个定义条目，由TAB隔开的几个字段组成。第一个字段是2次事件名，第二个字段是触发的1次事件名，第三个字段是此2次事件的ID号，第四个字段为对事件的统计定义（每多少秒出现多少次），第五个字段据说是返回参数，如何使用未知。

2次事件的定义是天阗IDS有别于其他IDS产品的又一个地方，看起来天阗IDS对统计类型的事件分析做了一个统一的实现，这有其它的好处，接口简单实现容易，但这样实现也是有一定问题的，比如对检测端口扫描这样比较重要的攻击无法做深入使用比较智能的算法，另外效率也可能会个问题。

相关链接：

[1]

Protocol Anomaly Detection for Network-based Intrusion Detection

[http://www.sans.org/rr/intrusion/anomaly.php](http://www.sans.org/rr/intrusion/anomaly.php)

[2]

Snort Users Manual

[http://www.snort.org/docs/writing_rules/](http://www.snort.org/docs/writing_rules/)

[3]

A look at whisker's anti-IDS tactics

[http://www.wiretrip.net/rfp/pages/whitepapers/whiskerids.html](http://www.wiretrip.net/rfp/pages/whitepapers/whiskerids.html)

[4]

Implementing a Generalized Tool for Network Monitoring

[http://citeseer.nj.nec.com/rd/71310588%2C198878%2C1%2C0.25%2CDownload/http://citeseer.nj.nec.com/cache/papers/cs/8783/http:zSzzSzstaff.washington.eduzSzdittrichzSzpaperszSznetmonitor.pdf/ranum97implementing.pdf](http://citeseer.nj.nec.com/rd/71310588%2C198878%2C1%2C0.25%2CDownload/http://citeseer.nj.nec.com/cache/papers/cs/8783/http:zSzzSzstaff.washington.eduzSzdittrichzSzpaperszSznetmonitor.pdf/ranum97implementing.pdf)

[5]

Customizing NFR NID Using N-Code

[https://support.nfr.com/nid-v3/nde/docs/Customizing_NFR_NID_Sensor_Using_N-Code.pdf](http://support.nfr.com/nid-v3/nde/docs/Customizing_NFR_NID_Sensor_Using_N-Code.pdf)

[6]

Re: Protocol Anomaly Detection IDS 

[http://archives.neohapsis.com/archives/sf/ids/2003-q1/0249.html](http://archives.neohapsis.com/archives/sf/ids/2003-q1/0249.html)
