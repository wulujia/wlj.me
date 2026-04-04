---
title: "用moinmoin创建多个wiki主页"
date: 2006-09-10T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2067"
---

一时兴起，又想建一个firefox的维基百科，前些日子听人说twiki相当不错，装上试了试，语法和moinmoin不太一样，因为网络安全焦点维基百科已经用了moinmoin，还是遵从自己的习惯，仍然用它吧。

moinmoin允许一套代码运行多个wiki实例，但翻译过来的文档看起来实在难以理解，所以花了不少时间，简单记录一下我的配置过程，免得忘了。

1、复制/usr/share/moin/config/wikifarm/目录下的farmconfig.py和mywiki.py到/usr/share/moin/wiki下；

2、将原有的wikiconfig.py改名为xfocus.py，配置mywiki.py如下：

> from farmconfig import FarmConfig
> 
>   class Config(FarmConfig):
> 
>       sitename = u'中文Firefox应用与推广维基百科'
> 
>       logo_string = u'<img src="/wiki/common/moinmoin.png" alt="MoinMoin Logo">'
> 
>       page_front_page = u"首页"
> 
>       data_dir = '/path/to/data/'
> 
>       from MoinMoin.util.antispam import SecurityPolicy
> 
>       navi_bar = [
> 
>           u'%(page_front_page)s',
> 
>           u'SiteNavigation',
> 
>           u'RecentChanges',
> 
>           u'FindPage',
> 
>           u'HelpContents',
> 
>       ]
> 
>       theme_default = 'classic'
> 
>       language_default = 'zh'
> 
>       tz_offset = '8.0'
> 
>       show_section_numbers = 1
> 
>       show_hosts = 0
3、编辑主配置文件farmconfig.py，我的配置内容很简单：

> wikis = [
> 
>       ("mywiki",    r"^firefox.unnoo.com/.*$"),
> 
>       ("xfocus",    r"^wiki.xfocus.net/.*$"),
> 
>   ]
> 
>   
> 
>   from MoinMoin.multiconfig import DefaultConfig
> 
>   
> 
>   class FarmConfig(DefaultConfig):
> 
>       data_underlay_dir = '../underlay/'
> 
>       url_prefix = '/wiki'
> 
>       page_category_regex = u'^Category[A-Z]'
> 
>       page_dict_regex = u'[a-z]Dict$'
> 
>       page_form_regex = u'[a-z]Form$'
> 
>       page_group_regex = u'[a-z]Group$'
> 
>       page_template_regex = u'[a-z]Template$'
上面的mywiki和xfocus两行，分别代表几个不同的wiki实例。

4、应该已经大功告成。其中需要注意的是：每个单独的维基只需要设定各有不同的设置选项即可(比如logo，数据目录或者ACL设置)。其他的设置都从基本配置类（farmconfig.py）中继承而来。

有些晚了，过几天将陆续添加wiki中的内容，可能会采用域名：[http://firefox.unnoo.com](http://firefox.unnoo.com/)
