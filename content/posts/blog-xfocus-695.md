---
title: "Microsoft MN700 无线网卡在 Debian 下的安装"
date: 2005-01-21T00:00:00+08:00
tags: ["Tech"]
draft: false
slug: "blog-xfocus-695"
---

家里的 AP 的无线网卡是找朋友从国外带的 Microsoft MN70的水货，因为是 Microsoft，一直也没想着能在 Debian 下驱动起来，昨天偶然在插着无线网卡的时候运行了 lspci 命令，居然有一条提示是：

0000:03:00.0 Network controller: Broadcom Corporation: Unknown device 4325 (rev 02)

原来微软是 OEM Broadcom 的设备。记起有个 [ndiswrapper](http://ndiswrapper.sf.net/) 项目，可以用 Windows 下的驱动在 linux 下跑某些无线网卡，Broadcom 恰好就是它所支持的一种。

1、安装前准备

需要安装内核的头文件
# apt-get install kernel-headers-2.6.8-1-386

2、安装ndiswrapper

# make
# make install
# ndiswrapper -i /root/mn720.inf <-- 我把windows下的inf文件、驱动都复制到/root目录下了，该命令是安装
# modproe ndiswrapper

# ndiswrapper -l <-- 查看是否安装成功
Installed ndis drivers:
mn720   driver present, hardware present

# dmesg <-- 查看日志，可以看到成功安装的记录
ndiswrapper version 1.0rc2 loaded (preempt=yes,smp=no)
PCI: Enabling device 0000:03:00.0 (0000 -> 0002)
ACPI: PCI interrupt 0000:03:00.0[A] -> GSI 11 (level, low) -> IRQ 11
PCI: Setting latency timer of device 0000:03:00.0 to 64
ndiswrapper: using irq 11
wlan0: ndiswrapper ethernet device 00:0d:3a:27:5f:84 using driver mn720
wlan0: encryption modes supported: WEP, WPA with TKIP, WPA with AES/CCMP
ndiswrapper: driver mn720 (Microsoft,07/07/2003, 3.20.26.0) added

3、安装无线工具并配置开机自启动

# apt-get install wireless-tools kismet airsnort

编辑 auto wlan0
iface wlan0 inet static
        address 192.168.100.222
        wireless-essid WLJHOME
        wireless-key MyWirelessKeyHere
        netmask 255.255.255.0
        gateway 192.168.100.254

在 /etc/modules 最后一行加入 ndiswrapper

安装成功 :)
