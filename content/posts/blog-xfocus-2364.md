---
title: "MPlayer中的电影文件合并功能"
date: 2006-12-24T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-2364"
---

在MPlayer中有一个mencoder.exe，可以用来合并多个影片，今天拍下的几个片子，就用上了，命令行如下（记着备忘，省得将来再查）：

mencoder -oac pcm -ovc copy -idx -o output.mov 1.mov 2.mov 3.mov
