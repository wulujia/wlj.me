---
title: "在 Endeavour OS 安装 fcitx"
date: 2024-06-10T10:00:00+08:00
tags: ["AI", "Tech"]
draft: false
slug: "endeavouros-install-fcitx"
---

## 1. 安装需要的包

```
sudo pacman -S fcitx5 fcitx5-gtk fcitx5-qt fcitx5-configtool fcitx5-rime
```

## 2. 安装 GNOME 扩展用于面板显示

安装 `gnome-browser-connector` 以在 GNOME 系统托盘中显示 fcitx：

```
sudo pacman -Sy gnome-browser-connector
```

然后安装 KimPanel GNOME 扩展：https://extensions.gnome.org/extension/261/kimpanel/

## 3. 安装雾凇拼音词库

参考：https://github.com/iDvel/rime-ice?tab=readme-ov-file

使用 AUR 助手安装 `rime-ice-git` 包：

```
# paru 默认会重新评估 pkgver，有新提交时自动更新
# yay 需要手动启用：yay -Y --devel --save

paru -S rime-ice-git
# yay -S rime-ice-git
```

推荐使用 patch 方法。编辑输入框架目录中的 `default.custom.yaml` 文件：

- iBus：`$HOME/.config/ibus/rime/`
- Fcitx5：`$HOME/.local/share/fcitx5/rime/`

**default.custom.yaml：**

```yaml
patch:
  __include: rime_ice_suggestion:/
  __patch:
    key_binder/bindings/+:
      - { when: paging, accept: comma, send: Page_Up }
      - { when: has_menu, accept: period, send: Page_Down }
```

## 4. 其他配置

使用 `fcitx5-configtool` 进行进一步自定义。
