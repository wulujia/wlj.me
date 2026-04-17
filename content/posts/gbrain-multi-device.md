---
title: 'gbrain 多设备怎么办'
date: 2026-04-17T13:07:23+08:00
tags: ["AI","Tools","Tech"]
draft: false
slug: "gbrain-multi-device"
---

多台电脑共用一个 GBrain。写东西的时候随手就录进去，搜的时候不管换哪台机器都能搜到。

## 方法

两件事。

markdown 走 Git。所有 GBrain 内容放一个独立仓库，推到 GitHub。每台机器开机自动 `git pull`，写完自动 `git push`。

每台机器本地跑自己的 DB。`gbrain init` 默认用嵌入式 Postgres，零配置。新机器装完跑一次 `gbrain reindex` 从 markdown 重建索引，之后每次 git pull 完跑 `gbrain sync` 做增量更新。

DB 不要跨设备同步。Dropbox、iCloud、Syncthing 都不要用来同步 GBrain 的 DB 目录。

## 为什么

GBrain 存两层数据。markdown 文件是真相，DB 里的向量索引和全文索引是为了搜索快从 markdown 派生出来的缓存。

DB 里的东西都能从 markdown 重新生成：embedding 用 OpenAI 重算，全文索引重建，实体关系重新解析。反过来不行，DB 里没有 markdown 没有的信息。

所以 DB 是可以丢的。坏了跑一遍 reindex，几美金、几十分钟，回到原样。markdown 坏了才是真的丢数据。

每台机器本地跑一份缓存就行。只要 markdown 同步对齐，搜索结果自然一致。不需要任何云数据库，也不会出现两台机器抢着写 DB 导致损坏的问题。

## 一个小提醒

autopilot（凌晨自动整理任务）只在一台主力机上装。多台都装会重复处理同一批 markdown，浪费 API 费用，还会撞车。

其他机器只做捕获和查询，让主力机晚上统一整理。
