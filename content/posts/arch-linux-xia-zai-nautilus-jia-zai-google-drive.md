---
title: "arch linux 下在 nautilus 加载 Google Drive"
date: 2024-06-15T10:00:00+08:00
tags: ["Linux", "Arch Linux"]
draft: false
slug: "arch-linux-xia-zai-nautilus-jia-zai-google-drive"
---

之前用 ubuntu 里的 gnome，在 Online account 里填上 Google 帐号，打开 File 选项，就可以在 Nautilus 里看见挂载上的 Google Drive，这次用 Endeavour OS，填完 Google 帐号，就像什么都没发生一样。

其实是缺了个 gvfs 的 backend，只需要：

```
yay -S gvfs-google
```

然后：

```
gio mount google-drive://<your gmail user>@gmail.com/
```

就可以了。

```
gio mount -l
```

可以看挂载情况。
