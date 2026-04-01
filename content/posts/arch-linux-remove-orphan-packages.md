---
title: "Arch Linux 清除孤立软件包"
date: 2024-06-25T10:00:00+08:00
tags: ["Linux", "Arch Linux"]
draft: false
slug: "arch-linux-remove-orphan-packages"
---

```
sudo pacman -Qqdt | sudo pacman -Rs -
```
