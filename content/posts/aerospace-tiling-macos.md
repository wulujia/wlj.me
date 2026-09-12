---
title: "用 AeroSpace 给 Mac 加上 Omarchy 式的平铺和快捷键"
date: 2026-09-13T07:55:18+08:00
lastmod: 2026-09-13T07:55:18+08:00
author: "Luca"
tags: ["Tech","Tools"]
draft: false
slug: "aerospace-tiling-macos"
---

在 Omarchy 上习惯了 Super+Return 开终端，新窗口自动排在当前窗口旁边。回到 Mac 上想要同样的东西，发现缺两块：macOS 不会自动平铺新窗口，Alacritty 也没有分屏。

AeroSpace 一个工具补上两块。它是 i3 风格的平铺窗口管理器，不用关 SIP，自带全局快捷键，所以 yabai 和 skhd 都不用装。

```
brew install --cask nikitabobko/tap/aerospace
```

配置是一个 toml 文件，放在 `~/.config/aerospace/aerospace.toml`。我配的键：

- Cmd+Return：新开一个 Alacritty 窗口，自动平铺到当前窗口旁边
- Cmd+Shift+Return：开浏览器
- Cmd+Shift+F：开 Finder
- Alt+H/J/K/L：切焦点，加 Shift 移动窗口
- Alt+1 到 9：切工作区，加 Shift 把窗口送过去
- Alt+F 全屏，Alt+R 进 resize 模式

开终端那一条走的是 `alacritty msg create-window`，在已经跑着的 Alacritty 进程里开新窗口，没在跑就用 `open -a` 拉起：

```toml
[mode.main.binding]
cmd-enter = 'exec-and-forget /Applications/Alacritty.app/Contents/MacOS/alacritty msg create-window || open -a Alacritty'
cmd-shift-enter = 'exec-and-forget open -a "Brave Origin"'
cmd-shift-f = 'exec-and-forget open -a Finder'
```

系统设置、Raycast 和 Finder 的复制进度窗设成浮动，其余全部平铺。首次启动要给 Accessibility 权限，给了才能动窗口。

## 两个代价

全局键会抢走应用自己的键。Cmd+Shift+F 在 VS Code 是全文搜索，在 Chrome 是全屏，装了之后这两处都到不了应用。嫌冲突就换 Ctrl+Cmd 这类没人用的组合。

工作区我留在 Alt 上，没换成 Cmd。Mac 上 Cmd+1 到 9 是所有应用的切 tab 键，浏览器、终端、Finder 都占着，换过去就全丢了。Omarchy 能用 Super 是因为 Linux 上没别的应用抢它。
