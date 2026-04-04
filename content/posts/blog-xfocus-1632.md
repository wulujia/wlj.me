---
title: "MODx CMS 烦人的输出"
date: 2006-02-20T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1632"
---

最近有资格去应聘网页设计师了……又折腾开了 CMS，这回找了个叫 MODxCMS 的，号称什么 AJAX、Web 2.0啥啥的，其实，象我这么缺乏审美观念的人，也就看上了它的模板功能，剥别人的网页风格那叫一个方便啊……这不，刚做好的网站，连黄董这样比我还缺乏审美观的人，都说我进步了……

可是，这玩意儿很让我心烦的是，它把所有人都当成了好人……这不，炽天使同学的职业习惯，就往 url 后面加料要玩注入……压根不用使劲造，MODxCMS 倒是有错误处理机制，可它全告诉你了，我岂不是很危险……

« MODx Parse Error »
MODx encountered the following error while attempting to parse the requested resource:
« Execution of a query to the database failed - Unknown column '6l' in 'where clause' »
SQL: SELECT sc.parent FROM `modx`.modx_site_content sc LEFT JOIN `modx`.modx_document_groups dg on dg.document = sc.id WHERE (sc.id=6l ) AND (sc.privateweb=0) LIMIT 1

找到manager/includes/document.parser.class.inc.php，将其中的：

$this->documentContent = $parsedMessageString;

随便换成什么 $this->documentContent = "xxx"; 世界就清静了。

当然，包子同学提供的防注入工具也是功不可没的，今后要上什么 CMS 之类的东西，再不用审代码了 ;)

btw：小鼻涕也在为开源软件做贡献，开始做 MODxCMS 的汉化工作啦 :)
