---
title: "1Password"
date: 2023-04-05T13:48:00+08:00
tags: ["Life"]
draft: false
slug: "1password"
---

最近考虑买个 1Password（早些年买过 1Password7，但后来嫌贵，升级时就弃坑，换到一个小众得多的 Enpass 上了）。

早年的 1Password 还允许密码库存放在本地、iCloud，同步、备份其实也很方便。但升级到 1Password8 后，就强制上传到他们的云服务了，这让人多少有点不放心。

在他们官网，有篇 Blog 解释了"为什么安全"，链接在：

[https://blog.1password.com/how-1password-protects-your-data/](https://blog.1password.com/how-1password-protects-your-data/)

大意是：

你的密码数据库是用你的"登录密码"加上"密钥"来加密的。1Password 官方破解不了，黑客攻破了 1Password 的网络也破解不了。

使用了安全远程密码（SRP）加密协议验证登录，密码是安全的。

用了双因素认证和端到端加密。
