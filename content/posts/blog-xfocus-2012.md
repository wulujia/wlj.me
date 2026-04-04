---
title: "backup-manager的两个小问题"
date: 2006-08-16T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2012"
---

这两个问题都是出在用FTP备份文件的时候：

 

1、如果FTP的密码中含有特殊字符，需要用""进行转义，否则认证无法通过。例如密码“[abcd@def](https://web.archive.org/web/20071014204839/mailto:%C2%A1%C2%B0abcd@def)”，就需要写成“abcd@def”

2、默认情况下它用ascii形式传文件，会导致备份文件出错，需要改脚本/usr/bin/backup-manager-upload，加入（标红者为插入语句）：

 

if ($ftp->login($user, $passwd) and

        $ftp->cwd($repository) and $ftp->binary){
