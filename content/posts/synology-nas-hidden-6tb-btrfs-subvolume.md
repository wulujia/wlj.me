---
title: "群晖 NAS：6.5 TB 空间被占用，所有界面都找不到"
date: 2026-11-03T22:00:23+08:00
lastmod: 2026-11-03T22:00:23+08:00
author: "Luca"
tags: ["Tech","Ops"]
draft: false
slug: "synology-nas-hidden-6tb-btrfs-subvolume"
---

日期：2026-11-01

## 现象

- Storage Manager 显示 Volume 1 已用 10.4 TB，剩余 60 GB，状态 Warning。
- Storage Analyzer 显示共享文件夹合计只有 4.45 TB：Downloads 3.83 TB，homes 622 GB，docker 0。
- 差了约 6 TB。重启无效。
- 回收站为空。没有安装 Snapshot Replication，快照数为 0。

## 排查过程

DSM 界面上没有任何地方能看到这 6 TB。只能开 SSH。

第一轮用 `du` 太慢，10 TB 要扫几小时。改用 Btrfs 自己的账本，几秒出结果：

```bash
sudo btrfs filesystem df /volume1          # 数据 vs 元数据，排除元数据膨胀
sudo btrfs subvolume list -s /volume1 | wc -l   # 快照数量，结果 0
sudo btrfs qgroup show -pcre --human-readable /volume1   # 每个子卷的大小
sudo btrfs subvolume list /volume1         # 子卷 ID 对应的路径
```

qgroup 显示子卷 `0/258` 占 6.50 TiB。subvolume list 显示 ID 258 是 `/volume1/@synologydrive`。

这是 Synology Drive Server 的版本历史目录。这个套件早就卸载了，但卸载时没有选"删除数据"，6.5 TB 留在原地。它是一个 Btrfs 子卷，不在任何共享文件夹里，所以 Storage Analyzer 和 File Station 都看不到。

## 处理

```bash
synopkg list | grep -i drive                        # 确认 SynologyDrive 套件不在列表
sudo btrfs subvolume show /volume1/@synologydrive   # 确认就是 ID 258
sudo btrfs subvolume delete /volume1/@synologydrive # 一秒返回
df -h /volume1                                      # 后台释放，10–30 分钟
```

不要用 `rm -rf`。删 6.5 TB 的子卷用 `rm` 要几小时，`btrfs subvolume delete` 一秒。
