---
title: "让 Mac 保持清醒：caffeinate"
date: 2026-07-15T10:54:00+08:00
lastmod: 2026-07-15T10:54:00+08:00
author: "Luca"
tags: ["Tools","Tech"]
draft: false
slug: "caffeinate-keep-mac-awake"
---

macOS 自带一个命令，caffeinate，给机器灌咖啡，不让它睡。跑长任务、下载大文件的时候用，不用去系统设置里改电源选项。

```bash
caffeinate
```

运行后 Mac 不睡眠。Ctrl+C 退出，恢复正常。

## 常用参数

屏幕常亮：

```bash
caffeinate -d
```

默认只防系统睡眠，屏幕照样熄。加 `-d`，屏幕也一起保持。

限时，单位是秒：

```bash
caffeinate -t 7200
```

两小时后自动失效，不用手动关。

跟着任务走：

```bash
caffeinate -i ./backup.sh
```

任务跑多久，机器醒多久。任务结束，自动恢复。

## 合盖

管不了。caffeinate 挡的是空闲睡眠，合盖触发的是另一套强制睡眠，合上照样睡。

接了外接屏、电源和键鼠，macOS 本身就支持合盖运行，不用任何命令，这是官方的 clamshell 模式。

没有外接屏，还想合盖继续跑：

```bash
sudo pmset -a disablesleep 1
```

设置重启后还在。用完改回 0，否则 Mac 塞进包里也不睡，发热耗电。

怕忘关，套一层自动恢复：

```bash
sudo sh -c 'pmset -a disablesleep 1; trap "pmset -a disablesleep 0" INT TERM EXIT; sleep 28800'
```

合盖不睡 8 小时。到点、Ctrl+C、关终端，都会自动恢复睡眠。把 `sleep 28800` 换成任务本身，就是合盖版的 `caffeinate -i`。

查当前状态：

```bash
pmset -g | grep SleepDisabled
```

1 是不睡，0 是正常。
