---
title: "我的Linux工作平台配置与展示"
date: 2004-04-17T00:00:00+08:00
tags: ["Tech", "Linux"]
draft: false
slug: "my-linux-desktop"
---

吴鲁加 04/17/2004

曾经多次尝试将工作平台转移到Linux上，但总是以失败告终。最大的原因是需要与大量windows用户进行文档交换，其中有很多Microsoft Office的东西，也包括visio和project。近期工作重心转变，便再次尝试转换工作平台，没有太多的不适应。

先来参观一下我简单实用的Debian吧……

先是我的桌面，或许大多数人会觉得这样的桌面简直让人不知所措……因为简陋得让人无从下手。但如果你知道我按Alt+2就能够切换到第二个虚拟桌面、Alt+F1就能够最大化当前窗口、Alt+9就能打开浏览器上网……我几乎所有应用程序都可以用键盘或者鼠标快速操作，这样的界面，是简陋，还是简洁？

再来看看我的网络应用程序吧，这里是我的浏览器，用的是 Mozilla-firefox；电子邮件客户端则采用一款叫 sylpheed 的软件；对一部份人来说，上网的另一大乐趣是聊天，那么，看看这个叫 gaim 的即时聊天工具吧……

很多人会说：我上班需要用到很多文档处理性质的工作，Linux操作起来很困难……其实，OpenOffice日趋成熟，按我实际使用情况来看，普通的word、excel和ppt文件在OpenOffice下打开问题不大(当然，如果是大型的网络建设方案，里面有大量OLE，或许显示起来会有问题，但，掉个头来想想，Microsoft Office还打不开OpenOffice做的文档呢……)，基本可以满足日常工作要求了。

其它软件呢？有编辑文档的 gvim、有用来看pdf文件的 acroread、有类似金山词霸的翻译软件星际译王、有看chm文件的 xchm、有播放各种影音文件的 mplayer、有不亚于photoshop的作图软件 gimp……

![gimp](/images/my-linux-desktop-1.png)

![mplayer](/images/my-linux-desktop-2.png)

如果实在有些软件Linux上没有，比如我现在偶尔用的SPSS或者MindManager，那么，我还可以用 rdesktop 连接远程windows服务器进行编辑处理 :)

![rdesktop](/images/my-linux-desktop-3.png)

我不认为Linux是万能的，但如果你只要求一个普通的办公平台，除此之外，你还需要什么？

那，我们开始吧。

## 1 安装GNU/Linux系统和软件

GNU/Linux的世界里有太多的选择，Debian、RedHat、SuSE、Gentoo、Slackware等发行版，多数各有其优势和特点。这里我选择的是 Debian。它自由、非商业、高质量的并且结构非常清晰。

### 1.1 下载netinstall光盘安装

由于Debian的apt工具可以非常简捷地安装应用软件，因此通常不需要下载完整的ISO文件。我下载了sarge每天测试性build出的ISO，大概一百多兆，可以直接写在cdrw上，避免浪费资源。

我将系统分成四个分区，采用reiserfs，分别如下：

```
Device Boot      Start         End      Blocks   Id  System        mountpoint  comment
/dev/hda1               1         904     6834208+  83  Linux       /           根分区
/dev/hda2             905        1007      778680   82  Linux swap  swap        swap
/dev/hda3            1008        1653     4883760   83  Linux       /home       存放用户数据
/dev/hda4            1654        5168    26573400   83  Linux       /doc        存放大量文档
```

这样安装的好处是，即使重新安装系统，至少不用管/home和/doc里面的数据，系统重装完，基本上用户配置都完全没有变化。

安装过程非常简单，如果用sarge，在安装时选择简体中文，则系统的locale会自动选择好。

先编辑 `/etc/apt/sources.list`，手工输入一行apt源：

```
deb ftp://mirrors.geekbone.org/debian sarge main non-free contrib
```

通常我习惯先装上ssh server，然后从另一台机器ssh上去，方便安装时的复制粘贴 ;)

```bash
apt-get update
apt-get install ssh
```

### 1.2 安装软件

Debian的优异特性在这时展露无遗，直接一条命令把想装的软件一次性装全吧。安装的速度视你网络速度而定。

```bash
apt-get install x-window-system-core bzip2 unzip gcc g++ autoconf automake make rxvt rxvt-ml debfoster vim vim-gtk fcitx stardict gaim \
fvwm rdesktop lftp sylpheed mozilla-firefox imagemagick scrot gqview  xmms gnupg gpa ethereal nmap nessus nessusd xdm mc xscreensaver \
modconf openoffice.org-l10n-zh-cn xchm dh-make lpr sudo bg5ps lynx gimp libgtk2.0-dev netcat libglade2-dev lsof smbclient smbfs
```

### 1.3 某些非官方软件

加上apt源：

```
deb ftp://debian.ustc.edu.cn/debian-uo/misc/i386 ./
```

然后运行：

```bash
apt-get install acroread-chfonts acroread mplayer-i686
```

## 2 部份与中文相关的处理

传统的中文美化三部曲：复制字体、修改全局配置文件、修改个人配置文件

### 2.1 复制字体

虽然有一些自由或者免费的字体可供使用，但感觉起来更适应simsun，所以将windows下的simsun.ttc复制到Linux下，我直接放在家目录下的.zh_CN。

在 `~/.zh_CN` 下建立文件 fonts.dir，然后复制fonts.dir为 fonts.scale，再创建一个文件叫 encodings.dir，这就是我们的字体目录了。

### 2.2 修改全局配置文件

现在该将字体目录添加进XFree86相关的文件中了，这里就是我的 `/etc/X11/XF86Config-4` 和 `/etc/fonts/fonts.conf`，前者主要增加了字体目录，并且将freetype改为xtt，后者只简单加入字体目录。

然后修改 `/etc/gtk/gtkrc.zh_CN`，创建 `/etc/gtk-2.0/gtkrc`，分别对gtk1.2和gtk2.0的应用程序全局字体进行定义。

### 2.3 修改个人配置文件

先是X启动时的文件：`~/.xsession`，然后与全局定义类似加入 `~/.gtkrc.zh_CN` 和 `~/.gtkrc-2.0`，设置就基本完成。

## 3 部份应用软件的配置

GNU/Linux下的软件可以称得上是浩如烟海，对于刚准备从Windows转入Linux的朋友来说，可以先看看 The table of equivalents / replacements / analogs of Windows software in Linux 这篇文章，里面提到了绝大多数日常工作中可以用Linux产品替代的Windows软件。

按上述方式装好的系统，已经能够完成我日常99%的工作了，大多数比在Windows下还来得利索。这么一个系统的大小的情况基本如下所示：

```
aa@risker:~$ df -h
Filesystem            容量  已用 可用 已用% 挂载点
/dev/hda1             6.6G  1.1G  5.5G  17% /
tmpfs                 126M     0  126M   0% /dev/shm
/dev/hda3             4.7G  415M  4.3G   9% /home
/dev/hda4              26G  3.9G   22G  16% /doc
```

### 3.1 窗口管理器FVWM

fvwm的强大与灵活，可以说，用得越久，体会越深。对于fvwm的初学者，我推荐到王垠的主页看详细中文介绍。

### 3.2 中文打印的处理

- **安装cupsys**

先是安装软件和确认打印机

```bash
apt-get install cupsys cupsys-bsd cupsys-client foomatic-bin samba smbclient gs-esp a2ps
smbclient -L 192.168.100.4 -U guest
```

通过浏览器直接连接到cupsys的web控制界面：http://localhost:631/

一些配置选项设成：

```
Device:Windows Printer via SAMBA
Device URI:smb://guest@192.168.100.4/HPLaserJ
```

把Output Resolution改成600 DPI了，打印测试页正常。

- **各种程序下的中文打印**

有些程序直接打印就很正常，比如OO，有部份程序，比如gedit之类的可以设置打印字体，但对sylpheed之类的软件，直接发送命令给lpr的，打印总是乱码，这时采用bg5ps这个软件来辅助。

```bash
apt-get install bg5ps
```

调整 `~/.bg5ps.conf`，修改设定至少以下项目：

```
Encoding="gb2312"
chineseFontPath="/home/aa/.zh_CN"
fontName_gb2312="simsun.ttc"
```

运行命令测试：

```bash
bg5ps -if 20040324_DongGuan.txt |lpr
```

打印中文正常。这样就可以在如sylpheed等软件中用类似 `bg5ps -if %s|lpr` 的命令输出中文了。

- **mozilla中文打印**

直接在 `/usr/lib/mozilla-firefox/defaults/pref/unix.js` 打开FreeType2再指定路径就行了，如下：

```
pref("font.FreeType2.enable", true);
pref("font.directory.truetype.1","/home/aa/.zh_CN");
```

- **多页缩印**

```bash
apt-get install mpage
mpage -4 mozilla.ps > out.ps|lpr
```

### 3.3 简捷的日程管理

由于没有装gnome或KDE，无法使用那些大型的日程管理软件，于是动起小巧心思，尝试过mozilla的calendar插件、vim插件、emacs、gdeskcal等，都不是很满意，偶然想起有个命令叫cal，结合calendar命令，也就是简洁漂亮的日程管理工具了。

在calendar命令中，日期可以有多种表达方式，我首先在.xsession中保证calendar变量设置成为我们的calendar文件，该文件的写法就很灵活了……

```
aa@risker:~$ cat .xsession|grep calen
export calendar=/home/aa/.calendar/calendar.all
aa@risker:~$ cat /home/aa/.calendar/calendar.all
25 *        每月工作回顾(每位同事的绩效面谈、售后服务状况、1/2同事共事)
20 *        技术部标准发布内容更新一次
Friday      每周工作回顾(重点项目回顾、文件服务器)
09/18       9-18事变纪念日
June Sun+3  父亲节(6月的第三个星期天)
May Sun+2   母亲节(五月的第三个星期天)
```

使用异常简单：

```
aa@risker:~$ calendar -A 5
 4月 17         完成给xfocus的文档《中小型企业安全评估操作》
 4月 19         确认公司邮件组事宜是否完成
 4月 20*        技术部标准发布内容更新一次
 4月 21         完成给xfocus的文档《弱点评估的工具、模型和方法》
```

### 3.4 其它

- **Samba支持中文共享名**

在samba中要直接连接中文共享名字的文件夹，往往会出错。需要在 `/etc/samba/smb.conf` 中的[global]段加上：

```
display charset = cp936
unix charset = cp936
dos charset = cp936
```

这时再 `mount -t smbfs` 就可以直接使用中文共享名。

- **OpenOffice字体不认simsun**

由于openoffice只认识ttf字体，所以可以将字体做一个链接：

```bash
ln -s /home/aa/.zh_CN/simsun.ttc /usr/share/fonts/truetype/openoffice/simsun.ttf
```

重新打开OpenOffice便正常了。

- **mc乱码**

mc是一款很精巧的字符界面文件管理器，但很奇怪的是它的中文部份显示不正确，反而影响了美观，因此干脆去掉中文的mo和hint。

```bash
rm -fr /usr/share/locale/zh_CN/LC_MESSAGES/mc.mo
rm -fr /usr/share/mc/mc.hint.zh
```
