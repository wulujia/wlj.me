---
title: "Firefox安装扩展时无法校验签名"
date: 2006-09-08T00:00:00+08:00
tags: ["Life"]
draft: false
slug: "blog-xfocus-2059"
---

在给办公室电脑上的firefox
2.0安装del.icio.us扩展的时候遇到点小问题，因为这个扩展本身写着只支持1.0-1.5.*版本的firefox，通常情况下我们只要改改
install.rdf里设定的maxVersion就可以了，可这回改完提示我无法安装，原因是无法校验签名。

看了看包里的文件：


发现目录Meta-inf就是用来签名的，直接将它从xpi里删除，再装就OK了。对部份有做签名的扩展，翻译者以及象我这样“强行安装”者，这个小技巧还是有用的。另外，可以看看[Signing an XPI](http://www.mozdevgroup.com/docs/pete/Signing-an-XPI.html)这篇文档了解更多细节。
