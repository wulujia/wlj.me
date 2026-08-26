---
title: "Hyprland 是什么"
date: 2026-08-26T17:18:29+08:00
lastmod: 2026-08-26T17:18:29+08:00
author: "Luca"
tags: ["Tools","Tech"]
draft: false
slug: "hyprland"
---

Linux 上的一个窗口管理器，官网 [hypr.land](https://hypr.land/)。它决定窗口怎么摆、怎么切换、动画长什么样。

## 平铺

一般桌面上窗口是叠在一起的，像桌上摊开的一堆纸，你拖来拖去调整位置和大小。平铺是另一种摆法：窗口不重叠，自动铺满整个屏幕。开第一个窗口占满屏，开第二个屏幕自动一分为二，开第三个再分。

好处是不用手动拖窗口，也不会有窗口被压在下面找不到。切换、移动、调整大小全走键盘快捷键。

Linux 上平铺窗口管理器有很多，i3、dwm、sway 都是。Hyprland 的区别在于它有圆角、模糊、阴影和动画，窗口开关和切换都有过渡效果。

## Wayland

Hyprland 只能在 Wayland 上跑。

Wayland 是 Linux 上画图形界面的一套协议，用来取代 1987 年的 X11。在 X11 时代，窗口管理器和显示服务器是两个程序；到了 Wayland，两者合并成一个，叫合成器（compositor）。所以 Hyprland 既管窗口布局，也管画面合成。

老程序只认 X11 的，通过 XWayland 这个兼容层照样能跑。

## 它不是完整桌面

GNOME、KDE 装完就能用：状态栏、文件管理器、设置面板、通知、锁屏，全都有。Hyprland 只管窗口，其余要自己拼：

- 状态栏：[Waybar](https://github.com/Alexays/Waybar)
- 程序启动器：[wofi](https://hg.sr.ht/~scoopta/wofi) 或 [rofi](https://github.com/davatorium/rofi)
- 通知：[mako](https://github.com/emersion/mako)
- 锁屏：[hyprlock](https://github.com/hyprwm/hyprlock)
- 壁纸：[hyprpaper](https://github.com/hyprwm/hyprpaper)

装完第一次启动是一块黑屏加一个鼠标指针，什么都没有。所有东西都得自己配出来。

## 配置

一个文本文件，`~/.config/hypr/hyprland.conf`。按键绑定、动画、窗口规则都写在里面，存盘立刻生效，不用重启。所有配置项在 [Wiki](https://wiki.hypr.land/) 上。

```
bind = SUPER, Return, exec, ghostty
bind = SUPER, Q, killactive
bind = SUPER, 1, workspace, 1

animations {
    enabled = true
    bezier = smooth, 0.05, 0.9, 0.1, 1.05
}
```

## 现状

滚动发布，两三个月一个版本，最新是 0.56.2（2026 年 8 月）。主力开发者是 Vaxry。版本号还在 0.x。源码和发布记录在 [GitHub](https://github.com/hyprwm/Hyprland)。

## 在 NixOS 上

一行：

```nix
programs.hyprland.enable = true;
```

配合 home-manager，状态栏、快捷键、主题、壁纸全部声明在同一份配置里。换台机器 `nixos-rebuild` 跑一遍，桌面一模一样。

## 谁不需要它

- 用 macOS 或 Windows 的：跑不了，它是 Linux 专属
- 服务器：没有显示器，装了也没用
- 想装完就能用的：它需要花时间拼一套自己的桌面
