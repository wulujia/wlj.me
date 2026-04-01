---
title: "Mac 下 neovim 里自动 esc 切换输入法"
date: 2025-01-01T00:00:00+08:00
tags: ["neovim", "mac", "Input Method"]
draft: false
slug: "neovim-auto-switch-input-on-esc"
---

## 1. 安装 macism

[https://github.com/laishulu/macism](https://github.com/laishulu/macism)

```bash
brew tap laishulu/homebrew
brew install macism
```

## 2. nvim 插件里加一个 im-select.lua

`~/.config/nvim/lua/plugins/im-select.lua`

```lua
return {
  "keaising/im-select.nvim",
  config = function()
    require("im_select").setup({
      -- 在普通模式下，默认使用的英文输入法
      -- 请将下面的值替换为您在上一步中获取到的英文输入法标识符
      default_im_select = "com.apple.keylayout.ABC", -- macOS 示例
      -- default_im_select = "1033", -- Windows 示例
      -- default_im_select = "keyboard-us", -- Linux (Fcitx5) 示例

      -- 设置触发切换的事件
      set_default_events = { "InsertLeave", "CmdlineLeave" },
      set_previous_events = { "InsertEnter" },

      -- 保持安静，当找不到依赖的命令行工具时不发出警告
      keep_quiet_on_no_binary = false,

      -- 异步切换输入法，避免卡顿
      async_switch_im = true
    })
  end,
}
```
