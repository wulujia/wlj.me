---
title: 'OOM 杀死 NetworkManager 事件记录'
date: 2026-04-20T08:47:06+08:00
tags: ["Tech"]
draft: false
slug: "oom-kills-networkmanager"
---

2026 年 4 月 19 日凌晨 00:06，luca-xm（RedmiBook Air 13，16GB 内存，4GB swap）上的 NetworkManager 意外退出，网络断开。

## 时间线

- 4 月 18 日全天，NetworkManager 日志显示 WiFi 连接在 CONNECTED_SITE 和 CONNECTED_GLOBAL 之间反复切换，但均自动恢复，属正常行为
- 4 月 19 日 00:06:13，内核触发 OOM Killer
- OOM Killer 选中 `unattended-upgr`（PID 392258，属于 `apt-daily.service`），该进程占用 13.6GB 匿名内存（anon-rss: 13601484kB）
- 此时 swap 已耗尽（Free swap = 0kB）
- 进程被杀后，D-Bus 连接断裂（`Unexpected error response from GetNameOwner(): Connection terminated`）
- NetworkManager 收到 SIGTERM，正常退出
- 4 月 20 日 08:43，系统重启后 NetworkManager 恢复正常

## 根因

`apt-daily.service` 自动执行系统更新时，`unattended-upgr` 进程内存泄漏或异常膨胀至 13.6GB，耗尽系统全部可用内存和 swap。OOM Killer 介入后引发 D-Bus 连接中断，NetworkManager 作为 D-Bus 依赖方被连带终止。NetworkManager 本身无异常。

## 决策

禁用自动更新定时器，改为手动更新：

```
sudo systemctl disable apt-daily.timer apt-daily-upgrade.timer
sudo systemctl stop apt-daily.timer apt-daily-upgrade.timer
```

后续系统更新手动执行 `sudo apt update && sudo apt upgrade`。
