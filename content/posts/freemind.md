---
title: "我用FreeMind"
date: 2004-07-19T00:00:00+08:00
tags: ["Tech", "Tools"]
draft: false
slug: "freemind"
---

吴鲁加 07/19/2004

## 版本控制

```
v0.8 07/19/2004 文档创建
```

## 1. 所谓MindMap

### 1.1 MindMap是什么

MindMap是什么呢？其实是英国人托尼・巴赞创造的一种提出笔记方法，和传统的直线记录方法完全不同，它以直观形象的图示建立起各个概念之间的联系。在国内，MindMap又被称为脑图或思维导图。

思维导图(Mind Mapping)以放射性思考(Radiant Thinking)为基础的收放自如方式，除了提供一个正确而快速的学习方法与工具外，运用在创意的发想与收敛、项目企划、问题解决与分析、会议管理等方面，往往产生令人惊喜的效果。它是一种展现个人智力潜能极至的方法，将可提升思考技巧，大幅增进记忆力、组织力与创造力。它与传统笔记法和学习法有量子跳跃式的差异。

### 1.2 MindMap软件介绍

其实当前MindMap软件相当多，最为流行的应该这三款：

- Mindjet MindManager
- inspiration
- FreeMind

对我来说，FreeMind最合适，原因有二：

- 跨平台，这样无论我在Windows、Debian或者FreeBSD下都可以正常使用；
- 采用xml保存数据，方便读取或者与其它程序转换；

功能简洁，却又恰到好处的够用，因此我就选定它了!

## 2. 我用FreeMind

### 2.1 速读

通过我的读书笔记可以看出，用FreeMind做记录是非常方便的。

采用了FreeMind后，我对一些"快餐书籍"的阅读方式是这样的：

1. 仔细看一遍目录，根据目录先画一张mindmap，基本把握作者的思路；
2. 进入阅读状态，边读边写写画画，圈出重点，读完一章，便在mindmap中完善一章的内容，如此周而复始；
3. 看整张mindmap，从整体回顾，找出重点，标记不同的颜色以便今后重点重读，并且结合自己的感觉，填进mindmap中；
4. 扔开mindmap，闭上眼睛回忆阅读的结果。

### 2.2 小项目管理

FreeMind有个很好的功能是根据目录创建文件，也就是可以根据某个目录下的文件结构来直接生成一个MindMap，这个功能也很诱人，于是我利用它来管理我的小项目。

首先直接生成一幅MindMap，然后进行部份细节调整和分类，再标出生要等级。当项目中有新任务创建时，就做简单记录。这样就能轻松地将企业内部的项目放在一起全盘考虑和分析了。

### 2.3 脑力激荡

一帮朋友在一起讨论某个创业机会时、几个程序员在商量产品功能特点的时候、企业管理人员聚会研究公司发展战略的时候……或者，仅仅是自己想写一篇文章的时候，比如我现在:)

FreeMind是否都能助你一臂之力？

### 2.4 会议记录

会议记录这点似乎乏善可陈，谁都能看出用它做会议记录，相对较能抓住所谈事务的主题，并且容易促进与会者的关联分析。

## 3. 小技巧

### 3.1 快捷键或鼠标

我常用的快捷键有：

```
在下方新增节点 = Enter
新增子节点 = INSERT
在上方新增节点 = Shift+Enter
查找 = Ctrl+F
编辑 = F2
展开或缩起 = Space
```

当然，按F3-F9能够给节点设置不同的颜色等等，也是很常用的。另外还有些组合键，如按住Alt键后用鼠标选中根节点，就是全选。按住Ctrl+Shift后用鼠标连接两个节点，便是在节点间创建连接线……快捷键也可以自定义，但通常无须这样做。

### 3.2 在web上发布

当你精心完成一个MindMap后，是否有希望别人看到的愿望呢？直接通过freemind-browser可以轻松地将Mindmap发表到网站上，并且访问者能够象直接操作程序般对各节点进行展开、关闭等行为。

只要将freemindbrowser.html中的两部份稍做修改，即标题和具体mm文件的位置，并连同freemindbrowser.jar一起复制到你的web服务器上，用户应该就能够正常浏览了。

### 3.3 聪明的复制与粘贴

FreeMind比其它软件优势的一个地方还在于它智能的复制方式，例如，我可以通过一个有缩进层次关系的txt、html或其它文件复制成很漂亮的MindMap，也能将MindMap直接复制进word、excel甚至outlook中，并保持良好的缩进和层次关系。

### 3.4 修改配置文件

在一份user.properties的文件中，保存着许多可配置的选项，其中仅有几项是通过Edit->Preference可以设定的。这份文件通常在你的~目录下，在windows 2k、xp和2003下，应该在 `c:\Documents and Settings\(your user name)\freemind\user.properties`，如果是Win9x下则在 `C:\WINDOWS\freemind\user.properties`，要判断你的HOME目录，可以直接在cmd窗口输入：`echo %HOMEPATH%`

里面的部份格式如下：

```
## Experimental features, "true" / "false"
#experimental_file_locking_on = false
##If dnd is enabled. "true" or "false"
#draganddrop = true
#
##The Modes which Freemind will load on startup, full Class names separated by a comma.
#modes = freemind.modes.browsemode.BrowseMode,freemind.modes.mindmapmode.MindMapMode,freemind.modes.filemode.FileMode
##The initial mode that is loaded on startup
#initial_mode = MindMap
```

并不难理解，就不多做说明了。

### 3.5 MindManager数据导出到FreeMind

身边有很多朋友使用的Mind Map工具是MindManager X5，这毫无疑问是一款杰出的商用软件，但与FreeMind之间的格式却是不相通用的，好在两者都采用xml格式来保存数据，因此数据转换并不困难。

先用解压缩工具打开MindManager的 `*.mmap` 文件——该格式实际上就是将相关信息打包压缩。我们可以看到里面有一个Document.xml的文件，这就是MindManager的主文件了。

采用特定的xslt，比如 mm2fm.xslt，再配合 xsltproc 软件，将Document.xml解压后直接进行处理，便能够轻松地将该xml顺利转成Freemind所能理解的mm格式：

```
c:\xsltproc>xsltproc.exe -o ssp2p.mm mm2fm.xslt Document.xml
c:\xsltproc>
```

### 3.6 FreeMind数据保存到MindManager

因为成功地游说了几个朋友转移到FreeMind上来，因此一般我自己没有这个需求，偶尔要做这种转换时，就投机取巧了一把：

- 选择File->Export to HTML，将mm导出为html；
- 用MS Word打开该html文件，并另存为Word的doc格式；
- 打开MindManager，采用File->Open->Microsoft word document(*.doc,*.dot)，选定刚才保存的文件后打开。

### 3.7 添加自己的插件

一个程序如果可定制程度高，当然能让人觉得更加自由。MindManager可以使用vb编写宏，并且直接载入菜单，这方面FreeMind做得如何呢？

答案是：相当出色，事实上你可以用java或者jython编写插件并加载。

在windows下，到 `C:\Program Files\FreeMind\accessories\plugins` 下创建文件Pyhello.py如下：

```python
from freemind.extensions import NodeHookAdapter
import javax.swing as swing

class Pyhello(NodeHookAdapter):
    def __init__(win):
	win = swing.JFrame("HelloWorld")
	win.size = (200, 200)
	win.show()

instance=Pyhello()
```

这是插件程序本身，唯一的功能就是显示Hello World :)

创建Pyhello.properties如下：

```
documentation=This is a simple Jython script that tests the node hook possibilites
#
# the script returns an object of this type:
base=freemind.extensions.NodeHookAdapter
script=Pyhello.py
modes=freemind.modes.mindmapmode
documentation=<html>welcome to risker.org</html>
icon=accessories/plugins/icons/kcmsystem.png
```

这里定义了上面那个程序的位置、运行模式、说明及图标，重新载入FreeMind时，我们可以看到在工具栏上多出一个图标，点击弹出helloworld。

### 3.8 数据导出

当前的最新测试版本是v 0.72，在这个版本中新增了将MindMap导出为图片或xslt文件的插件，不用费劲心机地截屏或者打印了，直接存成图片发送好了。
