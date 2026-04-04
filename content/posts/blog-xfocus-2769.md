---
title: "映像劫持（IFEO）及其修复"
date: 2007-07-13T00:00:00+08:00
tags: ["Startup"]
draft: false
slug: "blog-xfocus-2769"
---

现在只要跟技术相关的事儿，我基本不闻不问（主要是闻了问了，也未必能搞得明白），由此也被killer着实鄙视了几回。比如[超级巡警](http://www.google.cn/search?q=%E8%B6%85%E7%BA%A7%E5%B7%A1%E8%AD%A6&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:unofficial&client=firefox-a)3.x已经具备的映像劫持（IFEO）修复工具，我就一直没明白是咋回事，今天比较有空，找了找资料，总结了一下：
1、什么是映像劫持

如果你明明双击执行了程序A，但运行起来的却是程序B（比如，明明运行QQ，但QQ没起来，反而跳出个Foxmail），那么恭喜你，你应该中了某类采用了IFEO技术的病毒了。
所谓IFEO，其实是Image File Execution
Option的缩写，其实就是个注册表项：
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
NT\CurrentVersion\Image File Execution Options
近期被很多病毒都利用该技术来：

> a,
> 阻止杀毒软件和专杀工具的运行；
> 
> b,
> 重定向一些常用程序到病毒体，一旦运行这些程序，病毒再度死灰复燃；

2、有哪些实际的病毒例子这么瞎折腾的吗？

[separator]

当然有，比如前段时间的AV终结者病毒，就是这么轰轰烈烈地玩了一把，它的技术细节可以从超级巡警的主页上看到。

这个病毒的主要目的是盗号，附送的功能就是杀杀毒软件和破环安全模式（中了之后，用户就进不了安全模式了）。
3、怎么用超级巡警对付这些玩意儿？

运行超级巡警（ast.exe）或者超级巡警加载工具（ToolsLoader），切换到“安全优化”标签，点击左侧的“系统修复”图标，勾选“修复映像劫持”和“修复安全模式启动”这两项，然后点击“修复”按钮。

![](https://web.archive.org/web/20071014204939im_/http://www.i170.com/Attach/4AEF4A8B-1B3F-4B4E-A6DB-EB1902C32D4C)

重启系统，怎么样，世界清静了吧？
4、参考资料

> http://www.fzpchome.com/Article/bdcc/200706/445.html
> 
> http://dswlab.com/vir/v20070611.html

顺便提一句，[超级巡警4.0](http://www.baidu.com/s?wd=%B3%AC%BC%B6%D1%B2%BE%AF&cl=3)虽然还在beta阶段，但从界面到功能都做了些调整，欢迎大伙儿帮忙测试。另外，3.5版目前暂停升级，会在4.0版本稳定之后，再直接在线升级到最新。
