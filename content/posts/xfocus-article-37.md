---
title: "MySQL安全性指南"
date: 2000-05-06T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-article-37"
---

[quack](https://www.xfocus.net/bbs/index.php?lang=cn&act=Profile&do=03&MID=5) (quack_at_xfocus.org)

MySQL安全性指南 

作 者： 晏子


作为一个MySQL的系统管理员，你有责任维护你的MySQL数据库系统的数据安全性和完整性。本文主要主要介绍如何建立一个安全的MySQL系统，从系统内部和外部网络两个角度，为你提供一个指南。 


本文主要考虑下列安全性有关的问题： 


为什么安全性很重要，你应该防范那些攻击？ 

服务器面临的风险（内部安全性），如何处理？ 

连接服务器的客户端风险（外部安全性），如何处理？ 

MySQL管理员有责任保证数据库内容的安全性，使得这些数据记录只能被那些正确授权的用户访问，这涉及到数据库系统的内部安全性和外部安全性。 

内部安全性关心的是文件系统级的问题，即，防止MySQL数据目录（DATADIR）被在服务器主机有账号的人（合法或窃取的）进行攻击。如果数据目录内容的权限过分授予，使得每个人均能简单地替代对应于那些数据库表的文件，那么确保控制客户通过网络访问的授权表设置正确，对此毫无意义。 


外部安全性关心的是从外部通过网络连接服务器的客户的问题，即，保护MySQL服务器免受来自通过网络对服务器的连接的攻击。你必须设置MySQL授权表（grant table），使得他们不允许访问服务器管理的数据库内容，除非提供有效的用户名和口令。 


下面就详细介绍如何设置文件系统和授权表mysql，实现MySQL的两级安全性。 


一、内部安全性-保证数据目录访问的安全

MySQL服务器通过在MySQL数据库中的授权表提供了一个灵活的权限系统。你可以设置这些表的内容，允许或拒绝客户对数据库的访问，这提供了你防止未授权的网络访问对你数据库攻击的安全手段，然而如果主机上其他用户能直接访问数据目录内容，建立对通过网络访问数据库的良好安全性对你毫无帮助，除非你知道你是登录MySQL服务器运行主机的唯一用户，否则你需要关心在这台机器上的其他用户获得对数据目录的访问的可能性。


以下是你应该保护的内容：


数据库文件。很明显，你要维护服务器管理的数据库的私用性。数据库拥有者通常并且应该考虑数据库内容的安全性，即使他们不想，也应该考虑时数据库内容公开化，而不是通过糟糕的数据目录的安全性来暴露这些内容。 

日志文件。一般和更新日志必须保证安全，因为他们包含查询文本。对日志文件有访问权限的任何人可以监视数据库进行过的操作。

更要重点考虑的日志文件安全性是诸如GRANT和SET PASSWORD等的查询也被记载了，一般和更新日志包含有敏感查询的文本，包括口令（MySQL使用口令加密，但它在已经完成设置后才运用于以后的连接建立。设置一个口令的过程设计象GRANT或SET PASSWORD等查询，并且这些查询以普通文本形式记载在日志文件中）。如果一个攻击者犹如日文件的读权限，只需在日志文件上运行grep寻找诸如GRANT和PASSWORD等词来发现敏感信息。 

显然，你不想让服务器主机上的其他用户有数据库目录文件的写权限，因为他们可以重写你的状态文件或数据库表文件，但是读权限也很危险。如果一个数据库表文件能被读取，偷取文件并得到MySQL本身，以普通文本显示表的内容也很麻烦，为什么？因为你要做下列事情：


在服务器主机上安装你自己“特制”的MySQL服务器，但是有一个不同于官方服务器版本的端口、套接字和数据目录。 

运行mysql_install_db初始化你的数据目录，这赋予你作为MySQL root用户访问你的服务器的权限，所以你有对服务器访问机制的完全控制，它也建立一个test数据库。 

将对应于你想偷取得表文件拷贝到你服务器的数据库目录下的test目录。 

启动你的服务器。你可以随意访问数据库表，SHOW TABLES FROM test显示你有一个偷来的表的拷贝，SELECT *显示它们任何一个的全部内容。 

如果你确实很恶毒，将权限公开给你服务器的任何匿名用户，这样任何人能从任何地方连接服务器访问你的test数据库。你现在将偷来的数据库表公布于众了。 

在考虑一下，从相反的角度，你想让别人对你这样吗？当然不！你可以通过在数据库录下执行ls -l命令确定你的数据库是否包含不安全的文件和目录。查找有“组”和“其他用户”权限设置的文件和目录。下面是一个不安全数据目录的一部分列出：


　

% ls -l

total 10148

drwxrwxr-x  11  mysqladm wheel    1024 May  8 12:20 .

drwxr-xr-x  22  root     wheel     512 May  8 13:31 ..

drwx------   2  mysqladm mysqlgrp  512 Apr 16 15:57 menagerie

drwxrwxr-x   2  mysqladm wheel     512 Jan 25 20:40 mysql

drwxrwxr-x   7  mysqladm wheel     512 Aug 31  1998 sql-bench

drwxrwxr-x   2  mysqladm wheel    1536 May  6 06:11 test

drwx------   2  mysqladm mysqlgrp 1024 May  8 18:43 tmp

....

 


正如你看到的，有些数据库有正确的权限，而其他不是。本例的情形是经过一段时间后的结果。较少限制的权限由在权限设置方面比更新版本更不严格的较早版本服务器设置的（注意更具限制的目录menageria和tmp都有较近日期）。MySQL当前版本确保这些文件只能由运行服务器的用户读取。


让我们来修正这些权限，使得只用服务器用户可访问它们。你的主要保护工具来自于由UNIX文件系统本身提供的设置文件和目录属主和模式的工具。下面是我们要做的：


进入该目录

% cd DATADIR


设置所有在数据目录下的文件属主为由用于运行服务器的账号拥有（你必须以root执行这步）。在本文使用mysqladm和mysqlgrp作为该账号的用户名和组名。你可以使用下列命令之一改变属主：

# chown mysqladm.mysqlgrp .


# find . -follow -type d -print | xargs chown mysqladm.mysqlgrp


设置你的数据目录和数据库目录的模式使得他们只能由mysqladm读取，这阻止其他用户访问你数据库目录的内容。你可以用下列命令之一以root或mysqladm身份运行。

% chmod -R go-rwx  .


% find . -follow -type d -print | xargs chmod go-rwx


数据目录内容的属主和模式为mysqladm设置。现在你应该保证你总是以mysqladm用户运行服务器，因为现在这是唯一由访问数据库目录权限的用户（除root）。 

在完成这些设置后，你最终应该得到下面的数据目录权限：


% ls -l

total 10148

drwxrwx---  11  mysqladm mysqlgrp 1024 May  8 12:20 .

drwxr-xr-x  22  root     wheel     512 May  8 13:31 ..

drwx------   2  mysqladm mysqlgrp  512 Apr 16 15:57 menagerie

drwx------   2  mysqladm mysqlgrp  512 Jan 25 20:40 mysql

drwx------   7  mysqladm mysqlgrp  512 Aug 31  1998 sql-bench

drwx------   2  mysqladm mysqlgrp 1536 May  6 06:11 test

drwx------   2  mysqladm mysqlgrp 1024 May  8 18:43 tmp

....

 


二、外部安全性-保证网络访问的安全

MySQL的安全系统是很灵活的，它允许你以多种不同方式设置用户权限。一般地，你可使用标准的SQL语句GRANT和REVOKE语句做，他们为你修改控制客户访问的授权表，然而，你可能由一个不支持这些语句的老版本的MySQL（在3.22.11之前这些语句不起作用），或者你发觉用户权限看起来不是以你想要的方式工作。对于这种情况，了解MySQL授权表的结构和服务器如何利用它们决定访问权限是有帮助的，这样的了解允许你通过直接修改授权表增加、删除或修改用户权限，它也允许你在检查这些表时诊断权限问题。


关于如何管理用户账号，见《MySQL的用户管理》。而对GRANT和REVOKE语句详细描述，见《MySQL参考手册》。


2.1 MySQL授权表的结构和内容

通过网络连接服务器的客户对MySQL数据库的访问由授权表内容来控制。这些表位于mysql数据库中，并在第一次安装MySQL的过程中初始化（运行mysql_install_db脚本）。授权表共有5个表：user、db、host、tables_priv和columns_priv。


表1 user、db和host授权表结构 

访问范围列

 

user db host 

Host Host Host 

User Db Db 

Password User  

数据库/表权限列 

Alter_priv Alter_priv Alter_priv 

Create_priv Create_priv Create_priv 

Delete_priv Delete_priv Delete_priv 

Drop_priv Drop_priv Drop_priv 

Index_priv Index_priv Index_priv 

Insert_priv Insert_priv Insert_priv 

References_priv References_priv References_priv 

Select_priv Select_priv Select_priv 

Update_priv Update_priv Update_priv 

File_priv Grant_priv Grant_priv 

Grant_priv   

Process_priv   

Reload_priv   

Shutdown_priv   

　 

表2 tables_priv和columns_priv属权表结构

 

访问范围列 

tables_priv  columns_priv 

Host  Host 

Db  Db 

User  User 

Table_name  Table_name 

Column_name   

权限列 

Table_priv  Column_priv 


授权表的内容有如下用途：


user表

user表列出可以连接服务器的用户及其口令，并且它指定他们有哪种全局（超级用户）权限。在user表启用的任何权限均是全局权限，并适用于所有数据库。例如，如果你启用了DELETE权限，在这里列出的用户可以从任何表中删除记录，所以在你这样做之前要认真考虑。 

db表

db表列出数据库，而用户有权限访问它们。在这里指定的权限适用于一个数据库中的所有表。 

host表

host表与db表结合使用在一个较好层次上控制特定主机对数据库的访问权限，这可能比单独使用db好些。这个表不受GRANT和REVOKE语句的影响，所以，你可能发觉你根本不是用它。 

tables_priv表

tables_priv表指定表级权限，在这里指定的一个权限适用于一个表的所有列。 

columns_priv表

columns_priv表指定列级权限。这里指定的权限适用于一个表的特定列。 

在“不用GRANT设置用户”一节里，我们再讨论GRANT语句如何对修改这些表起作用，和你怎样能通过直接修改授权表达到同样的效果。


tables_priv和columns_priv表在MySQL 3.22.11版引进（与GRANT语句同时）。如果你有较早版本的MySQL，你的mysql数据库将只有user、db和host表。如果你从老版本升级到3.22.11或更新，而没有tables_priv和columns_priv表，运行mysql_fix_privileges_tables脚本创建它们。


MySQL没有rows_priv表，因为它不提供记录级权限，例如，你不能限制用户于表中包含特定列值的行。如果你确实需要这种能力，你必须用应用编程来提供。如果你想执行建议的记录级锁定，你可用GET_LOCK()函数做到。


授权表包含两种列：决定一个权限何时运用的范围列和决定授予哪种权限的权限列。


2.1.1 授权表范围列

授权表范围列指定表中的权限何时运用。每个授权表条目包含User和Host列来指定权限何时运用于一个给定用户从给定主机的连接。其他表包含附加的范围列，如db表包含一个Db列指出权限运用于哪个数据库。类似地，tables_priv和columns_priv表包含范围字段，缩小范围到一个数据库中的特定表或一个表的特定列。


2.1.2 授权表权限列

授权表还包含权限列，他们指出在范围列中指定的用户拥有何种权限。由MySQL支持的权限如下表所示。该表使用GRANT语句的权限名称。对于绝大多数在user、db和host表中的权限列的名称与GRANT语句中有明显的联系。如Select_priv对应于SELECT权限。


2.1.3 数据库和表权限

下列权限运用于数据库和表上的操作。


ALTER

允许你使用ALTER TABLE语句，这其实是一个简单的第一级权限，你必须由其他权限，这看你想对数据库实施什么操作。 

CREATE

允许你创建数据库和表，但不允许创建索引。 

DELETE

允许你从表中删除现有记录。 

DROP

允许你删除（抛弃）数据库和表，但不允许删除索引。 

INDEX

允许你创建并删除索引。 

REFERENCES

目前不用。 

SELECT

允许你使用SELECT语句从表中检索数据。对不涉及表的SELECT语句就不必要，如SELECT NOW()或SELECT 4/2。 

UPDATE

允许你修改表中的已有的记录。 

2.1.4 管理权限

下列权限运用于控制服务器或用户授权能力的操作的管理性操作。


FILE

允许你告诉服务器读或写服务器主机上的文件。该权限不应该随便授予，它很危险，见“回避授权表风险”。服务器确实较谨慎地保持在一定范围内使用该权限。你只能读任何人都能读的文件。你正在写的文件必须不是现存的文件，这防止你迫使服务器重写重要文件，如/etc/passwd或属于别人的数据库的数据目录。

如果你授权FILE权限，确保你不以UNIX的root用户运行服务器，因为root可在文件系统的任何地方创建新文件。如果你以一个非特权用户运行服务器，服务器只能在给用户能访问的目录中创建文件。


GRANT

允许你将你自己的权限授予别人，包括GRANT。 

PROCESS

允许你通过使用SHOW PROCESS语句或mysqladmin process命令查看服务器内正在运行的线程（进程）的信息。这个权限也允许你用KILL语句或mysqladmin kill命令杀死线程。

你总是能看到或杀死你自己的线程。PROCESS权限赋予你对任何线程做这些事情的能力。


RELOAD

允许你执行大量的服务器管理操作。你可以发出FLUSH语句，你也能指性mysqladmin的reload、refresh、flush-hosts、flush-logs、flush-privileges和flush-tables等命令。 

SHUTDOWN

允许你用mysqladmin shutdown关闭服务器。 

在user、db和host表中，每一个权限以一个单独的列指定。这些列全部声明为一个ENUM("N","Y")类型，所以每个权的缺省值是“N”。在tables_priv和columns_priv中的权限以一个SET表示，它允许权限用一个单个列以任何组合指定。这两个表比其他三个表更新，这就是为什么它们使用更有效的表示方式的原因。（有可能在未来，user、db和host表也用一个SET类型表示。）


在tables_priv表中的Table_priv列被定义成：


SET('Select','Insert','Update','Delete','Create','Drop','Grant','References','Index','Alter')

在coloums_priv表中的Column_priv列被定义成：　 


SET('Select','Insert','Update','References')

列权限比表权限少，因为列级较少的权限有意义。例如你能创建一个表，但你不能创建一个孤立的列。


user表包含某些在其他授权表不存在的权限的列：File_priv、Process_priv、Reload_priv和Shutdown_priv。这些权限运用于你让服务器执行的与任何特定数据库或表不相关的操作。如允许一个用户根据当前数据库是什么来关闭数据库是毫无意义的。


2.2 服务器如何控制客户访问

在你使用MySQL时，客户访问控制有两个阶段。第一阶段发生在你试图连接服务器时。服务器查找user表看它是否能找到一个条目匹配你的名字、你正在从那儿连接的主机和你提供的口令。如果没有匹配，你就不能连接。如果有一个匹配，建立连接并继续第二阶段。在这个阶段，对于每一个你发出的查询，服务器检查授权表看你是否有足够的权限执行查询，第二阶段持续到你与服务器对话的结束。


本小节详细介绍MySQL服务器用于将授权表条目匹配到来的连接请求或查询的原则，这包括在授权表范围列中合法的值的类型、结合授权表中的权限信息的方式和表中条目被检查的次序。


2.2.1 范围列内容

一些范围列要求文字值，但它们大多数允许通配符或其他特殊值。


Host 

一个Host列值可以是一个主机名或一个IP地址。值localhost意味着本地主机，但它只在你用一个localhost主机名时才匹配，而不是你在使用主机名时。假如你的本地主机名是pit.snake.net并且在user表中有对你的两条记录，一个有一个Host值或localhost，而另一个有pit.snake.net，有localhost的记录将只当你连接localhost时匹配，其他在只在连接pit.snake.net时才匹配。如果你想让客户能以两种方式连接，你需要在user表中有两条记录。


你也可以用通配符指定Host值。可以使用SQL的模式字符“%”和“_”并具有当你在一个查询中使用LIKE算符同样的含义（不允许regex算符）。 SQL模式字符都能用于主机名和IP地址。如%wisc.edu匹配任何wisc.edu域内的主机，而%.edu匹配任何教育学院的主机。类似地，192.168.%匹配任何在192.168 B类子网的主机，而192.168.3.%匹配任何在192.168.3 C类子网的主机。


%值匹配所有主机，并可用于允许一个用户从任何地方连接。一个空白的Host值等同于%。（例外：在db表中，一个空白Host值含义是“进一步检查host表”，该过程在“查询访问验证”中介绍。）


从MySQL 3.23起，你也可以指定带一个表明那些为用于网络地址的网络掩码的IP地址，如192.168.128.0/17指定一个17位网络地址并匹配其IP地址是192.168.128前17位的任何主机。


User 

用户名必须是文字的或空白。一个空白值匹配任何用户。%作为一个User值不意味着空白，相反它匹配一个字面上的%名字，这可能不是你想要的。


当一个到来的连接通过user表被验证而匹配的记录包含一个空白的User值，客户被认为是一个匿名用户。 


Password 

口令值可以是空或非空，不允许用通配符。一个空口令不意味着匹配任何口令，它意味着用户必须不指定口令。


口令以一个加密过的值存储，不是一个字面上的文本。如果你在Password列中存储一个照字面上的口令，用户将不能连接！GRANT语句和mysqladmin password命令为你自动加密口令，但是如果你用诸如INSERT、REPLACE、UPDATE或SET PASSWORD等命令，一定要用PASSWORD("new_password")而不是简单的"new_password"来指定口令。 


Db

在columns_priv和tables_priv表中，Db值必须是真正的数据库名（照字面上），不允许模式和空白。在db和host中，Db值可以以字面意义指定或使用SQL模式字符'%'或'_'指定一个通配符。一个'%'或空白匹配任何数据库。 

Table_name，Column_name

这些列中的值必须是照字面意思的表或列名，不允许模式和空白。

某些范围列被服务器视为大小写敏感的，其余不是。这些原则总结在下表中。特别注意Table_name值总是被看作大小写敏感的，即使在查询中的表名的大小写敏感性对待视服务器运行的主机的文件系统而定（UNIX下是大小写敏感，而Windows不是）。


表3 授权表范围列的大小写敏感性 

列

Host

User

Password

Db

Table_name

Column_name

 大小写敏感性

No

Yes

Yes

Yes

Yes

No

 


2.2.2 查询访问验证

每次你发出一个查询，服务器检查你是否有足够的权限执行它，它以user、db、tables_priv和columns_priv的顺序检查，知道它确定你有适当的访问权限或已搜索所有表而一无所获。更具体的说：


服务器检查user表匹配你开始连接的记录以查看你有什么全局权限。如果你有并且它们对查询足够了，服务器则执行它。 

如果你的全局权限不够，服务器为你在db表中寻找并将该记录中的权限加到你的全局权限中。如果结果对查询足够，服务器执行它。 

如果你的全局和数据库级组合的权限不够，服务器继续查找，首先在tables_priv表，然后columns_priv表。 

如果你在检查了所有表之后仍无权限，服务器拒绝你执行查询的企图。 

用布尔运算的术语，授权表中的权限被服务器这样使用：


user OR tables_priv OR columns_priv


你可能疑惑为什么前面的描述只引用4个授权表，而实际上有5个。实际上服务器是这样检查访问权限：


user OR (db AND host) OR tables_priv OR columns_priv


第一个较简单的表达式是因为host表不受GRANT和REVOKE语句影响。如果你总是用GRANT和REVOKE管理用户权限，你绝不需要考虑host表。但是其工作原理你用该知道：


当服务器检查数据库级权限时，它对于客户查找db表。如果Host列是空的，它意味着“检查host表以找出哪一个主机能访问数据库”。 

服务器在host表中查找有与来自db表的记录相同的Db列值。如果没有host记录匹配客户主机，则没有授予数据库级权限。如果这些记录的任何一个的确有一个匹配连接的客户主机的Host列值，db表记录和host表记录结合产生客户的数据库级权限。

然而，权限用一个逻辑AND（与）结合起来，这意味着除非一个给定的权限在两个表中都有，否则客户就不具备该权限。以这种方式，你可以在db表中授予一个基本的权限集，然后使用host表对特定的主机有选择地禁用它们。如你可以允许从你的域中的所有主机访问数据库，但关闭了那些在较不安全区域的主机的数据库权限。


前面的描述毫无疑问使访问检查听起来一个相当复杂的过程，特别是你以为服务器对你发出的每个查询进行权限检查，然而此过程是很快的，因为服务器其实不从授权表对每个查询查找信息，相反，它在启动时将表的内容读入内存，然后验证查询用的是内存中的副本。这大大提高了访问检查操作的性能。但有一个非常明显的副作用。如果你直接修改授权表的内容，服务器将不知道权限的改变。


例如，如果你用一条INSERT语句向user表加入一个新记录来增加一个新用户，命名在记录中的用户将不能连接服务器。这对管理员新手（有时对有经验的老手）是很困惑的事情，当时解决方法很简单：在你改变了它们之后告诉服务器重载授权表内容，你可以发一条FLUSH PRIVILEGES或执行mysqladmin flush-privileges（或如果你有一个不支持flush-privileges的老版本，用mysqladmin reload。）。


2.2.3 范围列匹配顺序

MySQL服务器按一种特定方式排序符授权表中的记录，然后通过按序浏览记录匹配到来的连接。找到的第一个匹配决定了被使用的记录。理解MySQL使用的排序顺序很重要，特别是对user表。


当服务器读取user表内容时，它根据在Host和User列中的值排序记录，Host值起决定作用（相同的Host值排在一起，然后再根据User值排序）。然而，排序不是典序（按词排序），它只是部分是。要牢记的是字面上的词优先于模式。这意味着如果你正从client.your.net连接服务器而Host有client.your.net和%.your.net两个值，则第一个先选。类似地，%.your.net优先于%.net，然后是%。IP地址的匹配也是这样的。


总之一句话，越具体越优先。可以参见本文附录的实例。


2.3 避免授权表风险

本届介绍一些在你授权时的一些预防措施，以及不明值的选择带来的风险。一般地，你要很“吝啬”地授予超级用户权限，即不要启用user表中条目中的权限，而使用其它授权表，以将用户权限限制于数据库、表、或列。在user表中的权限允许于影响到你的服务器操作或能访问任何数据库中的任何表。


不要授予对mysql数据库的权限。一个拥有包含授权表数据库权限的用户可能会修改表以获取对其他任何数据库的权限。授予允许一个用户修改mysql数据库表的权限也实际上给了用户以一个全局GRANT权限。如果用户能直接修改表，这也等价于能够发出任何你能想象的任何GRANT语句。


FILE权限尤其危险，不要轻易授权它。以下是一个拥有FILE权限的人能干除的事情：


    CREATE TABLE etc_passwd (pwd_entry TEXT);

    LOAD DATA INFILE "/etc/passwd" into TABLE etc_passwd;

    SELECT * FROM etc_passwd;


在发出这些语句后，用户已经拥有了你的口令文件的内容了。实际上，服务器上任何公开可读文件的内容都可被拥有FILE权限的用户通过网络访问。


FILE权限也能被利用来危害没有设置足够权限制的文件权限的系统上的数据库。这就是你为什么应该设置数据目录只能由服务器读取的原因。如果对应于数据库表的文件可被任何人读取，不只是用户服务器账号的用户可读，任何有FILE权限的用户也可通过网络连接并读取它们。下面演示这个过程：


创建一个有一个LONGBLOB列的表： 

USER test;

CREATE TABLE tmp (b LONGBLOB);


使用该表读取每个对应于你想偷取的数据库表文件的内容，然后将表内容写入你自己数据库的一个文件中：


LOAD DATA INFILE "./other_db/x.frm" INTO TABLE tmp

     FIELDS ESCAPED BY "" LINES TERMINATED BY "";

SELECT * FROM tmp INTO OUTFILE "y.frm"

     FIELDS ESCAPED BY "" LINES TERMINATED BY "";

DELETE FROM tmp;

LOAD DATA INFILE "./other_db/x.ISD" INTO TABLE tmp

     FIELDS ESCAPED BY "" LINES TERMINATED BY "";

SELECT * FROM tmp INTO OUTFILE "y.ISD"

     FIELDS ESCAPED BY "" LINES TERMINATED BY "";

DELETE FROM tmp;

LOAD DATA INFILE "./other_db/x.ISM" INTO TABLE tmp

     FIELDS ESCAPED BY "" LINES TERMINATED BY "";

SELECT * FROM tmp INTO OUTFILE "y.ISM"

现在你拥有了一个新表y，它包含other_db.x的内容并且你有全权访问它。 

为避免让人以同样的方式攻击，根据“第一部分 内部安全性-保护你的数据目录”中的指令设置你的数据目录上的权限。你也可以在你启动服务器时使用--skip-show-database选项限制用户对于他们没用访问权限的数据库使用SHOW DATABASES和SHOW TABLES。这有助于防止用户找到关于它们不能访问的数据库和表的信息。


ALTER权限能以不希望的方式使用。假定你想让user1可以访问table1但不能访问tables2。一个拥有ALTER权限的用户可以通过使用ALTER TABLE将table2改名为table1来偷梁换柱。


当心GRANT权限。两个由不同权限但都有GRANT权限的用户可以使彼此的权利更强大。


2.4 不用GRANT设置用户

如果你有一个早于3.22.11的MySQL版本，你不能使用GRANT（或REVOKE）语句设置用户及其访问权限，但你可以直接修改授权表的内容。如果你理解GRANT语句如何修改授权表，这很容易。那么你通过手工发出INSERT语句就能自己做同样的事情。


当你发出一条GRANT语句时，你指定一个用户名和主机名，可能还有口令。对该用户生成一个user表记录，并且这些值记录在User、Host和Password列中。如果你在GRANT语句中指定全局权限，这些权限记录在记录的权限列中。其中要留神的是GRANT语句为你加密口令，而INSERT不是，你需要在INSERT中使用PASSWORD()函数加密口令。


如果你指定数据库级权限，用户名和主机名被记录在db表的User和Host列。你为其授权的数据库记录在Db列中，你授予的权限记录在权限列中。


对于表级和列级权限，效果是类似的。在tables_priv和columns_priv表中创建记录以记录用户名、主机名和数据库，还有相关的表和列。授予的权限记录在权限列中。


如果你还记得前面的介绍，你应该能即使不用GRANT语句也能做GRANT做的事情。记住在你直接修改授权表时，你将通知服务器重载授权表，否则他不知道你的改变。你可以执行一个mysqladmin flush-privileges或mysqladmin reload命令强迫一个重载。如果你忘记做这个，你会疑惑为什么服务器不做你想做的事情。


下列GRANT语句创建一个拥有所有权的超级用户。包括授权给别人的能力：


GRANT ALL ON *.* TO anyname@localhost IDENTIFIED BY "passwd"

    WITH GRANT OPTION

该语句将在user表中为anyname@localhost创建一个记录，打开所有权限，因为这里是超级用户（全局）权限存储的地方，要用INSERT语句做同样的事情，语句是： 


INSERT INTO user  VALUES("localhost","anyname",PASSWORD("passwd"),

    "Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y")

你可能发现它不工作，这要看你的MySQL版本。授权表的结构已经改变而且你在你的user表可能没有14个权限列。用SHOW COLUMNS找出你的授权表包含的每个权限列，相应地调整你的INSERT语句。 下列GRANT语句也创建一个拥有超级用户身份的用户，但是只有一个单个的权限： 


GRANT RELOAD ON *.* TO flush@localhost IDENTIFIED BY "flushpass"

本例的INSERT语句比前一个简单，它很容易列出列名并只指定一个权限列。所有其它列将设置为缺省的"N"： 


INSERT INTO user (Host,Password,Reload) VALUES("localhost","flush",PASSWORD("flushpass"),"Y")

数据库级权限用一个ON db_name.*子句而不是ON *.*进行授权： 


GRANT ALL ON sample.* TO boris@localhost IDENTIFIED BY "ruby"

这些权限不是全局的，所以它们不存储在user表中，我们仍然需要在user表中创建一条记录（使得用户能连接），但我们也需要创建一个db表记录记录数据库集权限： 


INSERT INTO user (Host,User,Password) VALUES("localhost","boris",PASSWORD("ruby")) 


INSERT INTO db VALUES("localhost","sample_db","boris","Y","Y","Y","Y","Y","Y","N","Y","Y","Y")


"N"列是为GRANT权限；对末尾的一个数据库级具有WITH GRANT OPTION的GRANT语句，你要设置该列为"Y"。


要设置表级或列级权限，你对tables_priv或columns_priv使用INSERT语句。当然，如果你没有GRANT语句，你将没有这些表，因为它们在MySQL中同时出现。如果你确实有这些表并且为了某些原因想要手工操作它们，要知道你不能用单独的列启用权限。


你设置tables_priv.Table_priv或columns_priv.Column_priv列来设置包含你想启用的权限值。例如，要对一个表启用SELECT和INSERT权限，你要在相关的tables_priv的记录中设置Table_priv为"Select,Insert"。 


如果你想对一个拥有MySQL账号的用户修改权限，使用UPDATE而不是INSERT，不管你增加或撤销权限都是这样。要完全删除一个用户，从用户使用的每个表中删除记录。 


如果你愿意避免发一个查询来直接修改全权表，你可以看一下MySQL自带的mysqlaccess和mysql_setpermissions脚本。 


附录1 小测验

在你刚刚新安装了一个MySQL服务器，在你增加了一个允许连接MySQL的用户，用下列语句：


GRANT ALL ON samp_db.* TO fred@*.snake.net IDENTIFIED "cocoa"


而fred碰巧在服务器主机上有个账号，所以他试图连接服务器：


%mysql -u fred -pcocoa samp_db

ERROR 1045: Access denied for user: 'fred@localhost' (Using password: YES)


为什么？


原因是： 


先考虑一下mysql_install_db如何建立初始权限表和服务器如何使用user表记录匹配客户连接。在你用mysql_install_db初始化你的数据库时，它创建类似这样的user表：


Host User 

localhost

pit.snake.net

localhost

pit.snake.net root

root


 


头两个记录允许root指定localhost或主机名连接本地服务器，后两个允许匿名用户从本地连接。当增加fred用户后，


Host User 

localhost

pit.snake.net

localhost

pit.snake.net

%.snake.net root

root


fred 


在服务器启动时，它读取记录并排序它们（首先按主机，然后按主机上的用户），越具体越排在前面：


Host User 

localhost

localhost

pit.snake.net

pit.snake.net

%.snake.net root


root


fred 


有localhost的两个记录排在一起，而对root的记录排在第一，因为它比空值更具体。pit.snake.net的记录也类似。所有这些均是没有任何通配符的字面上的Host值，所以它们排在对fred记录的前面，特别是匿名用户排在fred之前。


结果是在fred试图从localhost连接时，Host列中的一个空用户名的记录在包含%.snake.net的记录前匹配。该记录的口令是空的，因为缺省的匿名用户没有口令。因为在fred连接时指定了一个口令，由一个错配且连接失败。


这里要记住的是，虽然用通配符指定用户可以从其连接的主机是很方便。但你从本地主机连接时会有问题，只要你在table表中保留匿名用户记录。


一般地，建议你删除匿名用户记录：


mysql> DELETE FROM user WHERE User="";


更进一步，同时删除其他授权表中的任何匿名用户，有User列的表有db、tables_priv和columns_priv。


附录2 使一个新的MySQL安装更安全

在你自己安装了一个新的MySQL服务器后，你需要为MySQL的root用户指定一个目录（缺省无口令），否则如果你忘记这点，你将你的MySQL处于极不安全的状态（至少在一段时间内）。


在Unix（Linux）上，在按照手册的指令安装好MySQL后，你必须运行mysql_install_db脚本建立包含授权表的mysql数据库和初始权限。在Windows上，运行分发中的Setup程序初始化数据目录和mysql数据库。假定服务器也在运行。


当你第一次在机器上安装MySQL时，mysql数据库中的授权表是这样初始化的：


你可以从本地主机（localhost）上以root连接而不指定口令。root用户拥有所有权限（包括管理权限）并可做任何事情。（顺便说明，MySQL超级用户与Unix超级用户有相同的名字，他们彼此毫无关系。） 

匿名访问被授予用户可从本地连接名为test和任何名字以test_开始的数据库。匿名用户可对数据库做任何事情，但无管理权限。 

从本地主机多服务器的连接是允许的，不管连接的用户使用一个localhost主机名或真实主机名。如：


% mysql -h localhost test


% mysql -h pit.snake.net test


你以root连接MySQL甚至不指定口令的事实只是意味着初始安装不安全，所以作为管理员的你首先要做的应该是设置root口令，然后根据你设置口令使用的方法，你也可以告诉服务器重载授权表是它知道这个改变。（在服务器启动时，它重载表到内存中而可能不知道你已经修改了它们。）


对MySQL 3.22和以上版本，你可以用mysqladmin设置口令：


% mysqladmin -u root password yourpassword


对于MySQL的任何版本，你可以用mysql程序并直接修改mysql数据库中的user授权表：


% mysql -u root mysql

mysql>UPDATE user SET password=PASSWORD("yourpassword") WHERE User="root";


如果你有MySQL的老版本，使用mysql和UPDATE。


在你设置完口令后，通过运行下列命令检查你是否需要告诉服务器重载授权表：


% mysqladmin -u root status


如果服务器仍然让你以root而不指定口令而连接服务器，重载授权表：


% mysqladmin -u root reload


在你设置了root的口令后（并且如果需要重载了授权表），你将需要在任何时候以root连接服务器时指定口令。


――摘自：晏子工作室
