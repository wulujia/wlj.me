---
title: "铁卷透明支持Adobe PageMaker"
date: 2006-10-26T00:00:00+08:00
tags: ["Startup"]
draft: false
slug: "blog-xfocus-2166"
---

PageMaker是出版业的首选工具之一，很多人用它来排版说明书、教材。前些天耿先生提出了，在他所处的教材制作行业中，有这样的需求，并且希望试
用，于是对PageMaker
6.5和7.0两个版本进行测试。结果出乎意料的顺利，不需要开发人员在代码上做任何调整，目前的[铁卷电子文档安全系统3.0](http://www.unnoo.com/)版本就能够透明支持
PageMaker :)

需要做的仅仅是导入我们制作的规则文件AdobePageMaker.igr，然后在创建Agent的高级选项中勾选Adobe PageMaker，如下图所示：

> ![](https://web.archive.org/web/20071014204849im_/http://www.i170.com/attach/49E067E9-8ACC-432A-84F2-3A3E8939809A)
这样用户安装铁卷agent之后，由PageMaker创建的所有文件（包括pdf、html等），都会被透明地加密，只有授
权用户能够打开。当然，如果需要发送明文文件给客户，也能够轻松地通过“申请解密”功能提交解密申请，管理员可以在查看文件内容敏感程度后决定允许或拒
绝，这就一定程度上解决了安全性与易用性之间的矛盾，希望用户会喜欢![](https://web.archive.org/web/20071014204849im_/http://www.i170.com/htmledit/editor/images/smiley/msn/teeth_smile.gif)
