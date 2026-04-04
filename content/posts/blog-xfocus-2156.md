---
title: "漏洞扫描中fping的作用"
date: 2006-10-19T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2156"
---

这几天又复习起[安全评估](http://www.i170.com/user/wlj/Article_24274)了，重新操刀在一家运营商为几个业务系统进行安全评估工作，今天漏洞扫描时，记起一个小工具，共享一下。因为以往在进行漏洞扫描时，很偶然的情况下（虽说很偶然，但几个久经阵仗的老手都栽过跟头，我当然也不例外，这里面的血泪史，说起来，都是经验啊……![](https://web.archive.org/web/20071014204849im_/http://www.i170.com/htmledit/editor/images/smiley/msn/cry_smile.gif)），可能会有些脆弱的应用导致系统负载过高而当机。

监控的办法有很多，电信、移动或金融行业许多都有自身的监控平台，一旦业务异常便会有告警，这是一种形式。但有时无法实时查看告警平台时，就只能用土办法了，比如，持续地ping被扫描的服务器。

[fping](http://www.kwakkelflap.com/)在这里能够起到很好的作用，我主要看中它的几个功能：

> 1、能够从文件导入一批IP地址或直接设置一个网段，同时ping；
> 
>   2、回应timeout的时候，可以有声音提示；
> 
>   3、可以设定间隔多长时间ping一次；
它的命令参数有：

> Usage:
> 
>   fping <host(-list)> [-s data_size] [-S size1/size2] [-c] [-t time] [-w timeout]
> 
>          [-n count] [-h TTL] [-v TOS] [-r routes] [-R min/max] [-a] [-f]
> 
>          [-b(-)] [-i] [-l] [-T] [-D] [-d ping_data] [-g host1/host2]
> 
>          [-H filename] [-L filename]
> 
>   
> 
>   Options:
> 
>           -s : data_size in bytes up to 65500
> 
>           -S : size sweep. Ping with size1, size1 + 1, ..., size 2 datalength
> 
>           -c : continuous ping (higher priority than -n)
> 
>                to see statistics and continue - type Control-Break;
> 
>                to stop - type Control-C.
> 
>           -t : time between 2 pings in ms up to 1000000
> 
>           -w : timeout in ms to wait for each reply
> 
>           -n : number of echo requests to send
> 
>           -h : number of hops (TTL: 1 to 128)
> 
>           -v : Type Of Service (0 to 255)
> 
>           -r : record route (1 to 9 routes)
> 
>           -R : random length between min and max (disabled when using -S)
> 
>           -a : resolve addresses to hostnames
> 
>           -f : set Don't Fragment flag in packet
> 
>           -b : beep on every successful reply (- to beep on timeout)
> 
>           -i : use ICMP dll instead of raw socket (disables -r)
> 
>           -l : limit the output to ping results and errors
> 
>           -T : print timestamp with each reply
> 
>           -D : print datestamp and timestamp with each reply
> 
>           -d : ping with specified data (disabled when using -R)
> 
>           -g : ping IP range from host1 to host2
> 
>           -H : get hosts from filename (comma delimited, filename with full path)
> 
>           -L : logging to a text file
在评估报告中的“风险规避”这部份，把这张图贴进去，好歹也是种负责任的态度吧 ;)

![](https://web.archive.org/web/20071014204849im_/http://www.i170.com/attach/99D87A24-3BF1-42F2-B1C4-081FFE665346)
