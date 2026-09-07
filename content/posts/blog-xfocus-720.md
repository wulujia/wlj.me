---
title: "windows下的vi和sed"
date: 2005-02-02T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-720"
---

为了方便迁移，现在windows上能用开源软件的都尽量用着，比如，装了firefox、thunderbird、openoffice 1.9、gvim、还有gnuwin32下的所有工具。
前几天遇到个问题：
我在gvim下面写完文章，要处理成html的时候，gvim只是简单地加了

标记，于是浏览器看起来就不换行了。但vi里的tw=78这样的设置又把一串中文当成一个单词来处理，不起作用。
简单点说，就是我希望能够指定在文章的某一列加上换行符，但现在搞不定……

想找解决办法……跟watercloud大牛和yiminggong讨论半天，至少现在在windows下是ok了一小半。

C:>cat a
abcdefghijklmnopqrstuvwxy

用sed的方法

C:>sed s/^.{6}/"&"n/g a
abcdef
ghijkl
mnopqr
stuvwx
y

直接在vi里处理则是用：

:%s/...../&r/g

我在_vimrc里面加了一句：

noremap   :%s/.{78}/&r/g

以后按F8就可以直接处理了。但这样又有一个新问题，vi对中英文混排处理上，由于我的encoding用了cp936，于是处理起来，如果一排英文一排中文，会是这样的：

aaaa
我我我我

如果一行里有中文也有英文，那列长又不对齐了，麻烦，难道真得象yiming说的那样，写个脚本来处理？
