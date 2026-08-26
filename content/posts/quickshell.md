---
title: "Quickshell 是什么"
date: 2026-08-26T17:43:46+08:00
lastmod: 2026-08-26T17:43:46+08:00
author: "Luca"
tags: ["Tools","Tech"]
draft: false
slug: "quickshell"
---

Linux 上做桌面部件的工具箱，官网 [quickshell.org](https://quickshell.org/)。状态栏、通知弹窗、锁屏、音量面板、壁纸切换器，这些东西用它来写。

## 它解决什么

[上一篇](/posts/hyprland/)讲 Hyprland 时提过，那种窗口管理器只管窗口怎么摆，状态栏、通知、锁屏都要另外找程序拼。常见的拼法是 Waybar 加 mako 加 hyprlock，各是各的程序，各有各的配置格式，样式对不齐，之间也不通消息。

Quickshell 换一个思路：这些部件全都自己写，用同一种语言，跑在同一个进程里。状态栏上的音量图标和按音量键弹出的那个提示，可以共用一份状态。

## 用什么写

QML，Qt 的界面语言。长这样：

```qml
import Quickshell
import QtQuick

PanelWindow {
  anchors {
    top: true
    left: true
    right: true
  }
  implicitHeight: 30
  Text {
    anchors.centerIn: parent
    text: "hello world"
  }
}
```

这段就是屏幕顶部一条 30 像素高的栏，中间写着一行字。`anchors` 指定贴哪几条边，贴住之后 Quickshell 会自动向窗口管理器申请这块空间，其他窗口不会被它盖住。

QML 是声明式的：你写界面长什么样、数据变了界面怎么跟着变，不用自己写"收到消息 → 找到那个控件 → 改它的文字"这种流程。

## 存盘就生效

配置放在 `~/.config/quickshell/`，每个子目录里有一个 `shell.qml` 就算一套配置。跑起来之后编辑文件，存盘界面立刻变，不用重启。改一个像素挪一下位置，改完扭头就能看见。

## 自带的接口

写桌面部件要拿系统数据。Quickshell 内置了这些：

- PipeWire：音量、当前播放设备
- MPRIS：正在放什么歌，暂停下一首
- 系统托盘：那些图标
- PAM：验证密码，锁屏要用
- 蓝牙
- Hyprland 和 i3/Sway：当前工作区、窗口标题这类窗口管理器内部状态

官方只内置了 Hyprland 和 i3 两家的接口。用别的窗口管理器，得自己通过 socket 或者调命令去拿。

## 代价

- 得会写代码。Waybar 改个配置文件就能用，Quickshell 是让你自己写一个状态栏出来
- 从空白开始。它是工具箱不是成品，装完什么都没有
- API 还在变。官方明说后续版本会有破坏性改动，升级时要照迁移指南改配置

## 现状

LGPL 3 开源，主力开发者 outfoxxed。源码在 [GitHub](https://github.com/quickshell-mirror/quickshell)，文档在 [quickshell.org/docs](https://quickshell.org/docs/)。Wayland 和 X11 都支持。

社区里有人把整套配置开源出来，可以直接拿来用或者当参考，GitHub 上搜 quickshell 能找到不少。
