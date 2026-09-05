---
title: "Omarchy 触摸板滚动加速"
date: 2026-09-05T16:41:38+08:00
lastmod: 2026-09-05T16:41:38+08:00
author: "Luca"
tags: ["Tech","Tools"]
draft: false
slug: "omarchy-touchpad-scroll-acceleration"
---

在 ThinkPad 上跑 Omarchy，触摸板滚动一直比 Mac 慢而平：手指快慢不同，页面走的距离都差不多。今天让 AI 查了一下，原因和改法都很短。

## 原因

Hyprland 把触摸板交给 libinput 处理。libinput 默认只给鼠标指针做加速，双指滚动是线性的，手指走多少页面走多少。Omarchy 在这之上还乘了一个 0.4 的系数（`input.touchpad.scroll_factor`），所以整体又慢了一截。Mac 的手感来自两样东西：一条按手速变化的加速曲线，加上抬手后的惯性滑动。

## 改法

libinput 有一个“custom”配置，可以给滚动单独画一条曲线。Hyprland 通过 `accel_profile` 和 `scroll_points` 两个选项把它暴露出来，Omarchy 的 Lua 配置里用 `hl.device` 可以只对触摸板生效，不影响小红点和外接鼠标。

在 `~/.config/hypr/input.lua` 末尾加了这一段：

```lua
hl.device({
  name = "elan06b6:00-04f3:335a-touchpad",
  accel_profile = "custom 0.5 0 0.5 1.05 1.7 2.5 3.4 4.4 5.5",
  scroll_points = "0.5 0 0.4 0.9 1.5 2.3 3.3 4.5 6.0 7.8 10",
})
```

两行曲线的格式一样：第一个数是步长，后面是各个采样点的输出值。横轴是手指速度，纵轴是页面速度。慢慢滑的时候接近一比一，甩得快的时候往上翘。

设备名用 `hyprctl devices` 查。保存后 Hyprland 自动重载，`hyprctl configerrors` 为空就是生效了。

## 两个注意点

- 换成 custom 之后，触摸板的指针加速也一起换掉了，所以 `accel_profile` 后面必须同时给一条指针曲线，不然指针会变成没有加速。
- 曲线上的数字是起点，要靠手感调。想让快甩更猛就调大 `scroll_points` 后面几个数；想让慢滑更细就调小前面几个。整体都嫌慢的话，第二个旋钮是 Omarchy 默认的 `scroll_factor = 0.4`，改到 0.6 试试。

惯性滑动改不了。那是每个应用自己决定的，GTK 应用和 Chromium 有，其他不一定有，合成器这层没有开关。

回退的话把这段删掉就行，旧文件有 `.bak` 备份在同一目录。
