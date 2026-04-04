---
title: "用自由软件构建中小企业弱点评估系统"
date: 2004-04-24T00:00:00+08:00
tags: ["Tech", "Security"]
draft: false
slug: "enterprise-vul-assessment"
---

吴鲁加 04/24/2004

## 版本控制

```
v0.8 04/18/2004 文档创建
v0.9 04/24/2004 在第三部份中加入分布式扫描和多用户管理的描述
```

## 1. 准备工作

### 1.1 了解你需要什么

在确定要投入精力来配置系统之前，你或许希望了解它能为你带来什么。这么说吧，如果你现在：

- 负责企业内部的企业安全，希望有一套比较适合企业应用的漏洞扫描系统;
- 自己的网络和系统管理水平较好，不需要太多的所谓专家顾问支持;
- 公司在这方面的预算相当有限，你的钱必须花在上级已经定好的几个项目和产品上了。

这里所说的比较适合企业应用，简单说来，我想至少包括下面几点：

- 漏报、误报率较低，或者至少自己能够对报警的真实性进行调整后再统计;
- 对漏洞升级的快速反应，重大事件三天内应该有相应扫描模块升级;
- 能够出具比较美观的报表，对企业内部安全状况进行分析;
- 尽量简单易用，或者配置后就能自动运转，减少系统管理员的维护工作量。

那么，恭喜你，Inprotect具备了上述的所有功能，如果你有一定的编程能力，那么你还可以对它进行定制，使之更适合你的特定网络环境需求。

### 1.2 环境准备

安装配置支持php、mysql和gd的apache服务器，并且顺手将nmap、nessus和nikto这些扫描工具全装齐。

```bash
apt-get install apache php4 php4-gd2 php4-mysql mysql-server mysql-client nmap nessus nessusd nikto
```

配置apache，直接编辑 `/etc/apache/httpd.conf`，将：

```
DirectoryIndex index.html index.htm index.shtml index.cgi
#AddType application/x-httpd-php .php
#AddType application/x-httpd-php-source .phps
AddDefaultCharset on
```

改成：

```
DirectoryIndex index.php index.php3 index.html index.htm index.shtml index.cgi
AddType application/x-httpd-php .php .php3
AddType application/x-httpd-php-source .phps
AddDefaultCharset gb2312
```

运行下面的命令给mysql加上密码：

```bash
mysqladmin password xxxxxx
```

如果希望mysql启动时带上更好的中文支持，则可以编辑 `/etc/init.d/mysql` 文件，把 `/usr/bin/mysqld_safe > /dev/null 2>&1 &` 改成：

```bash
/usr/bin/mysqld_safe --default-character-set=gb2312 /dev/null 2>&1 &
```

编辑 `/etc/php4/apache/php.ini` 文件，找到 `";default_charset = "iso-8859-1""`，替换成：

```
default_charset = "gb2312"
```

## 2. 安装配置

### 2.1 Inprotect的安装

#### 2.1.1 安装perl模块

至少需要以下模块才能够使crontab里面的perl脚本正常运行，可以到CPAN找来安装。

```
MIME::Lite
Parallel::ForkManager
Date::Calc
```

#### 2.1.2 下载Inspect并导入数据库

直接到 http://www.inprotect.com/ 下载Inspect的最新版本。解包后可以仔细阅读INSTALL、console/html/readme.txt这两份文件，里面有较为详细的安装说明。

进入console/sql目录，运行：

```bash
mysql -h localhost --user=root < sql/inprotect.sql
```

如果你下载的是018版本，可能会有错误提示，数据库不会完全导入，原因是inprotect_settings重复，将第二个inprotect_settings的内容注释掉即可。

由于我对MySQL不太熟练，更喜欢通过phpmyadmin进行web管理，这样也方便后期更好地对弱点数据库进行整理。因此，就 `apt-get install phpmyadmin` 安装。phpmyadmin的界面如下：

![Inprotect Phpmyadmin](/images/enterprise-vul-assessment-1.png)

#### 2.1.3 安装并修改配置文件

运行install.sh，可以安装Inprotect程序，但该脚本只是为RedHat准备的，有些地方需要修改。脚本分成安装web文件、安装数据库和安装扫描器三个部份，除了安装文件外，也写入crontab定时运行任务。所有这些内容都可以自行根据脚本内容进行灵活调整。

分别编辑在html目录下的config.php和 `/usr/local/etc/inprotect.cfg`，主要修改数据库相关参数如主机、用户名、口令等。然后创建数据目录 `/usr/data/nessus` 和 `/usr/data/nmap`。

#### 2.1.4 updateplugins.pl

这样Inprotect就可以运行了，但由于nessus的插件还没有入库，因此暂时只是nmap扫描可用，试图运行nessus扫描时，会提示先运行nessus-plugins-update脚本，这个脚本中我们需要注意几个地方：

- nessus-update-plugins命令

```perl
#execute nessus-update-plugins
#system ("nessus-update-plugins") == 0 or die "No new plugins installed";
#If used patch for nessus-update-plugins, we may pass parameter on the command line.
system ("nessus-update-plugins -u $inprotect_url/html/nessus") == 0 or die "No new plugins installed";
```

这里的nessus-update-plugins带了-u参数，是Inprotect的作者修改过的，可以指定url，这里指定了本地url以提高速度。这个脚本在Inprotect软件包console/patch目录下。由于速度对我影响不大，因此我将这行注释了，直接采用不带-u参数的。

- nessus命令参数

```perl
#system("/usr/bin/nessus -qxpS $nessussvr $nessusport $nessususer $nessuspassw > $tempfile");
system("/usr/bin/nessus -qxpS localhost 1241 aa my_password_here > $tempfile");
```

系统中原来是第一行，但变量没有赋值(017之前的版本是在inprotect.cfg文件中赋值的)，懒得改了，直接把自己的nessus用户信息写进程序。

#### 2.1.5 登陆使用

直接连接到web服务器 http://localhost/html/login.php ，以用户名Admin，密码password直接登陆。

是否还算精美？;)

### 2.2 配置使用

建议的使用流程如下：

- **建立个人的profile**：选择"Settings" -> "Nessus Scan Profiles" -> "Create New Profile" -> 填写信息 -> 点击"Save"
- **选择nessusd服务器**：选择"Settings" -> "Nessus Servers" -> "Add new Nessus server" -> 填写信息 -> 点击"Save"
- **建立nessus管理区域**：选择"Settings" -> "Network Zones" -> "Add New Network Zone" -> 填写信息 -> 点击"Add zone" -> 返回 -> Edit Zone -> Zone Details -> Edit Zone Users。提示：这里填写的zone的IP范围要覆盖你希望扫描的网络。如果这里的信息填写有误，则添加扫描任务的时候会无法加入IP地址。
- **建立nessus用户**：选择"Settings" -> "Manage Users" -> 增加或者修改用户信息
- **开始扫描**：这时候可以到Security Scan里尝试一下，如果配置得当，nessus的扫描与nmap的扫描都可以正常使用了。

### 2.3 报告

这里的报告实际上是将Nessus、nmap和nikto的结果综合输出了，报告还是相当精美的，并且能够直接生成pdf。

## 3. 企业应用

### 3.1 Inprotect对企业应用的支持

#### 3.1.1 周期扫描

套用一款商用扫描器的广告词：可以在指定时间自动完成定时扫描任务或周期扫描任务，同时可以在无人值守的情况下自动获取升级信息。

#### 3.1.2 误报分析

在2.3节的报告部份，我们可以看到图片中每一漏洞后都有红色的小勾，如果我们点击该小勾，则将该漏洞表示为"误报"，这对数据入库后的月、季和年度分析的准确性很有帮助。

#### 3.1.3 趋势分析

在报告部份，有漏洞趋势分析、按日期或扫描排序的趋势等，能够对安全问题的趋势、分布进行统筹分析，便于制定安全决策和长远的安全规划。

#### 3.1.4 分布式扫描

部份企业的网络可能由多个远程分支机构组成，甚至可能是同一个内部物理环境中具有多个VLAN或者由防火墙隔离出了不同的区域，这时的扫描如何进行呢？

Inprotect可以管理多台Nessus的服务器，这样你可以从多点扫描，最终数据由Inprotect数据库集中收集和分析。

#### 3.1.5 多用户管理

有时企业中对不同资产的职责划分是不同的，可能网络管理员负责核心交换机、路由器设备，系统管理员负责所有Unix和Windows主机等……这时需要较好地做好职能划分。Inprotect中支持用户管理，可以增加一个网络管理员用户，并指定其管理的IP地址，这时该用户便只能扫描指定范围，扫描结果仍存储到数据库，这种分级分权管理是否更符合你的需求？

### 3.2 怎样用好弱点评估系统

其实漏洞扫描是一种"未雨绸缪"式的安全工作，如果工作到位，能使入侵者的攻击难度极大增加，下面是我工作中的一些小经验，希望有用：

- 将内部网络划分成不同的区域，每个区域有不同安全级别，定义的扫描频度和强度也有所不同。但一定要涵盖全网，不能有遗漏！
- 让机器代替人去做定期重复性的扫描，管理员把精力放在分析扫描报告上。最初几次扫描能够初步了解内部网络信息，后期分析则注重看"区别"。
- 注重问题的解决而非漏洞扫描本身。每次扫描的结果与上次比较，如果漏洞已经通知IT但却长期不补，至少责任能够厘清。
