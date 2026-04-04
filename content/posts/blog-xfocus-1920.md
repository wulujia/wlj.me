---
title: "/etc/hotplug/blacklist"
date: 2006-07-15T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-1920"
---

新装的 debian 服务器在启动时出现这样的错误：
pciehp: acpi_pciehprm:_SB_.PCI0 _HPP fail=0x5
pciehp: acpi_pciehprm:_SB_.PCI0 OSHP fails=0x5
pciehp: acpi_pciehprm:   Slot sun(1) at s:b:d:f=0x00:00:08:ffff
shpchp: acpi_shpchprm:_SB_.PCI0 _HPP fail=0x5
shpchp: acpi_pciehprm:_SB_.PCI0 OSHP fails=0x5
shpchp: acpi_shpchprm:   Slot sun(1) at s:b:d:f=0x00:00:08:ffff

现在懒了，凡事不求甚解，反正不影响使用，直接在 /etc/hotplug/blacklist 的末尾加上两行：

pciehp
shpchp

再 dmesg 看看，凑合了，只要看不到错误信息，就行啦。
