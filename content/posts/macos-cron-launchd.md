---
title: "macOS 的 cron 和 launchd"
date: 2026-04-24T07:08:52+08:00
tags: ["Tech"]
draft: false
slug: "macos-cron-launchd"
---

今天在终端收到一封 cron 发来的邮件，说某个脚本 "Operation not permitted"。查下去才发现，苹果对 cron 越来越不待见——它从十几年前就在劝大家迁到 launchd 了。

## 先看今天这件事

我有三个用 cron 跑的定时任务：每小时 15 分把知识库备份到 git，每小时 20 分刷新知识库的向量索引，每天早 9 点跑一次健康检查。

有一天开始，前两个任务悄无声息失败。打开日志才看见：

```
/bin/bash: .../brain-git-backup.sh: Operation not permitted
/bin/bash: gbrain: command not found
```

第一个是权限拦截——脚本文件在 `~/Library/CloudStorage/Dropbox/` 里，macOS 的隐私系统（TCC）不让 cron 碰 iCloud、Dropbox 这种云端同步目录下的文件。

第二个是 PATH 问题。cron 跑的 bash 是个干净的非交互 shell，`.zshrc` 里配置的 PATH 不会加载，`gbrain` 找不到。

两个问题合起来是一个主题：苹果对 cron 不上心了。

## cron 和 launchd 是什么

两者都是"定时工具"——让系统在指定时间跑一段命令。

cron 是 Unix 时代的老工具，几十年历史，Linux、Mac 都有，写一行配置就能用。

launchd 是苹果自己做的调度系统，2005 年随 macOS 10.4 推出。现在苹果系统里所有后台服务，包括 cron 本身，都归 launchd 管。

## 苹果怎么对待 cron

从 macOS 10.4 起，苹果把 cron 标成 "deprecated"——还能用，但不推荐，以后也不会再优化。这意味着：

- 苹果给系统做的新能力，不会往 cron 上接
- TCC 权限系统，launchd 原生支持"单个任务单独授权"，cron 只能整体授权一次
- 系统日志，launchd 的输出能按服务筛选，cron 只能自己写日志文件

## 每个任务单独授权

这是 cron 和 launchd 差别最直观的地方。

cron 只有一个进程 `/usr/sbin/cron`，所有定时任务都跑在它底下。你要给 cron 开"完全磁盘访问"权限，就等于一次性给**所有** cron 任务都开了。要么全开，要么全关。

launchd 不一样。每个任务是一个独立的 "agent"，放在 `~/Library/LaunchAgents/` 下的一个 plist 文件：

```
~/Library/LaunchAgents/com.luca.brain-backup.plist
~/Library/LaunchAgents/com.luca.brain-sync.plist
~/Library/LaunchAgents/com.luca.brain-health.plist
```

系统把每个 agent 当成独立程序，可以单独授权、单独关、单独看日志。

## plist 大概长什么样

就是一个 XML 文件。比如"每小时 15 分跑一次 brain-git-backup.sh"：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.luca.brain-backup</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/lucawu/Dropbox/Github/Luca/script/brain-git-backup.sh</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Minute</key>
        <integer>15</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/lucawu/.brain-git-backup.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/lucawu/.brain-git-backup.log</string>
</dict>
</plist>
```

写好丢进 `~/Library/LaunchAgents/`，跑一下 `launchctl load <plist 路径>`，就开始工作了。

## launchd 还有几个 cron 做不到的事

- 睡眠期间错过的任务能补跑。cron 直接跳过，launchd 电脑醒来会补一次
- 进程挂了能自动重启，加一行 `KeepAlive` 就行
- 可以监听文件变化触发。比如某个文件夹一有新文件就跑脚本，不一定按时间
- 日志接到系统 log 命令，用 `log show --predicate 'subsystem == "com.luca.brain-backup"'` 能按服务筛

## 那今天我迁走了吗

没有。三个任务用 cron 也能跑好，只要把 PATH 显式写到 crontab 顶部，再给 `/usr/sbin/cron` 加一次完全磁盘访问权限，两个问题都解决。

迁 launchd 是为将来准备的——等到任务多了想分开管、想让睡眠错过的任务补跑、想让某个任务挂掉自动重启，那时候再迁不迟。

今天的教训是一条：macOS 上的 cron 能用，但别指望它和系统新特性无缝配合。遇到坑，多半是因为苹果不打算再给它打补丁了。
