---
title: "Debian下的ATAPI光盘刻录"
date: 2004-11-02T00:00:00+08:00
tags: ["Life"]
draft: false
slug: "blog-xfocus-552"
---

apt-get install cdrecord后，由于使用非SCSI的刻录机，看了看/usr/share/doc/cdrecord/README.ATAPI.setup，是一篇名为Howto setup an ATAPI CD-RW/DVD+-RW recorder on Debian的文档，我是2.6的内核，因此：

1、运行命令cdrecord dev=ATA: -scanbus

得到的结果输出中有：

scsibus1:

        1,0,0   100) 'HL-DT-ST' 'CD-RW GCE-8525B ' '1.03' Removable CD-ROM

        1,1,0   101) 'ATAPI   ' 'DVD-ROM 16XMax  ' '1.12' Removable CD-ROM

2、可以编辑/etc/default/cdrecord，将步骤1中扫描到的你的CD-RW参数加进去。或者直接在命令行中指定：

cdrecord -v speed=52 dev=ATA:1,0,0 -data myiso.iso
