---
title: "英文版 Debian 安装 ibus-libpinyin"
date: 2024-01-28T09:09:00+08:00
tags: ["Tech"]
draft: false
slug: "debian-install-ibus-pinyin"
---

安装拼音输入法

```
apt-get install ibus-libpinyin
```

设置中文 locales

```
dpkg-reconfigure locales
```

然后到 Keyboard 里看看，应该有 Chinese 选项了。在退出重新登录后，Win + Space 应该就可以切换输入法了。
