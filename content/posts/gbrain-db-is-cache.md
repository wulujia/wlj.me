---
title: 'markdown 是真相，数据库是缓存'
date: 2026-04-17T13:07:23+08:00
tags: ["AI","Tools","Tech"]
draft: false
slug: "gbrain-db-is-cache"
---

传统系统里数据库是最重要的东西，坏了就丢数据。

GBrain 反过来。

## 两层

GBrain 存两层。markdown 文件，人可读的文本。DB 里的向量索引和全文索引。

DB 里的东西都能从 markdown 重新生成：embedding 用 OpenAI 重算，全文索引重建，实体关系重新解析。反过来不行，DB 里没有 markdown 没有的信息。

## 谁重要

DB 坏了，跑一遍 `gbrain reindex`，几美金 embedding，几十分钟，回到原样。

markdown 坏了才是真的丢数据。

## 一个推论

多设备方案变简单：markdown 走 Git 同步，每台机器本地跑自己的 DB，不用共享数据库。新机器第一次索引，之后 git pull 增量更新。没有云依赖，没有同步冲突。

备份策略也倒过来：markdown 多份备份，Git + GitHub + 偶尔离线。DB 不用备份。
