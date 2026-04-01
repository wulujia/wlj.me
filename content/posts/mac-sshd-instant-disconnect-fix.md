---
title: "Mac 下开启 sshd 登录后马上断开连接的一种可能"
date: 2025-01-01T00:00:00+08:00
tags: ["mac", "ssh"]
draft: false
slug: "mac-sshd-instant-disconnect-fix"
---

如果"共享 → 远程登录"里选择了"只允许这些用户…"，系统会用 **`com.apple.access_ssh`** 做白名单。**不在组里就会被 PAM 拒绝**。

```
# 查看是否在白名单组
dseditgroup -o checkmember -m "$USER" com.apple.access_ssh

# 不在的话加入（需要管理员密码）
sudo dseditgroup -o edit -a "$USER" -t user com.apple.access_ssh

# 也可放开给所有用户（图形界面改：系统设置 → 通用 → 共享 → 远程登录，选"所有用户"）
```

改完重启 sshd：

```
sudo launchctl kickstart -k system/com.openssh.sshd
```
