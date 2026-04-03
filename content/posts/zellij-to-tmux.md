---
title: "prefix + A 一键开 4 pane 平铺"
date: 2026-04-03T11:29:56+08:00
draft: false
slug: "zellij-to-tmux"
---

从 Zellij 回到 tmux

用了大半年 Zellij，最终还是切回了 tmux。

Zellij 开箱即用，底部状态栏把快捷键直接摆给你看，新手不用查文档。但用久了几个问题越来越明显：偶尔有渲染 bug，某些场景下 CPU 占用偏高，插件生态还太早期。分屏操作不够利索——我经常在大屏幕上同时跑 3-5 个 Agent，需要快速平铺，Zellij 做这件事要反复手动调整。还有就是遇到问题搜解决方案，tmux 的答案永远比 Zellij 多十倍。

核心概念

tmux 就三层：session → window → pane。session 是最外层的容器，断开 SSH 后还活着；window 相当于浏览器的 tab；pane 是一个 window 里的分屏。

默认 prefix 是 Ctrl-b，下面所有快捷键都是先按 prefix 再按对应键。

Session 管理

• tmux new -s work — 创建名为 work 的 session
• tmux ls — 列出所有 session
• tmux a -t work — 重新接入
• d — detach，断开但不关闭
• s — 在 session 之间切换（交互式列表）
• $ — 重命名当前 session

Window（Tab）

• c — 新建 window
• n / p — 下一个 / 上一个
• 0-9 — 直接跳到对应编号
• , — 重命名
• & — 关闭

Pane（分屏）

• % — 左右分
• " — 上下分
• 方向键 — 在 pane 之间移动
• z — 当前 pane 全屏/恢复，临时专注某个 pane 的时候好用
• x — 关闭当前 pane
• Ctrl-b 然后按住方向键 — 调整 pane 大小

复制模式

• [ — 进入复制模式，可以滚动、选文字
• 在 .tmux.conf 里加 setw -g mode-keys vi 就能用 vi 键位选文字
• Space 开始选择，Enter 复制，] 粘贴

多 Agent 快速平铺

大屏幕上同时跑多个 Agent 是我最常见的场景。

prefix + Space 会在五种内置布局之间循环切换：

• even-horizontal — 所有 pane 等宽左右排列
• even-vertical — 所有 pane 等高上下排列
• main-horizontal — 上面一个大 pane，下面几个小的并排
• main-vertical — 左边一个大 pane，右边几个小的叠起来
• tiled — 网格平铺，自动算行列

跑 3-5 个 Agent 的时候，按几次 Space 切到 tiled，所有 pane 自动等分，不用手动调。也可以直接 prefix + Alt+5 跳到 tiled。

不想一个一个手动分屏，可以在 .tmux.conf 里绑个快捷键一步到位：

# prefix + A 一键开 4 pane 平铺
bind A split-window -h \; split-window -v \; select-pane -t 0 \; split-window -v \; select-layout tiled

或者写个 shell 函数，想开几个开几个：

# 加到 .bashrc / .zshrc
agents() {
  local n=${1:-4}
  tmux new-window -n agents
  for ((i=1; i<n; i++)); do
    tmux split-window -t agents
    tmux select-layout -t agents tiled
  done
}

# agents 5 → 开 5 个 pane 自动平铺

关掉某个 pane 后布局会乱，再按一次 prefix + Space 切回 tiled 就重新整齐了。

几个实用的东西

在 ~/.tmux.conf 里加 set -g mouse on，就能用鼠标切 pane、调大小、滚屏。不用纯键盘操作。

SSH 到远程服务器干活，网络断了，tmux session 还活着。重新连上 tmux a 就回来了，进程一个没丢。

prefix + s 列出所有 session 带预览，prefix + w 列出所有 window 带预览。管理多个项目的时候比 tmux ls 再手动 attach 快。

最小配置

# ~/.tmux.conf
set -g mouse on
set -g history-limit 50000
set -g base-index 1
setw -g pane-base-index 1
setw -g mode-keys vi
set -g status-style 'bg=#282c34 fg=#abb2bf'
set -g default-terminal "tmux-256color"

# 一键开 4 pane 跑 Agent
bind A split-window -h \; split-window -v \; select-pane -t 0 \; split-window -v \; select-layout tiled

不需要插件管理器，不需要主题包。以后有需要再加。
