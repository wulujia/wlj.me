---
title: "Beli "Add Your School" 功能分析"
date: 2026-04-16T11:29:11+08:00
tags: ["Product"]
draft: false
slug: "20260416-beli-add-your-school"
---

## Beli 是什么

餐厅评分社交 App，2021 年创立，"餐厅版 Letterboxd"。核心差异化：不打 1-5 星，而是比较排序（A 和 B 哪个更好），算法据此生成你和朋友各自的偏好分数。

截至 2025 年 9 月，7500 万条评价，3 万个城市，80% 用户 35 岁以下。融资 1200 万美元，团队约 5 人。被 Food Network 称为"Gen Z 的 Yelp"。

## Add Your School 机制

菜单入口，让用户绑定自己的大学（支持学生 ID / 校园卡）。绑定后解锁两个东西：校内排行榜（按打卡餐厅数排名）和全国 187 所大学之间的 "Dining Hall of Fame" 竞赛——评选"最能吃的大学"。

积分方式：给餐厅打分、每周新增排名、推荐新用户。推荐的新用户绑定同校则积分叠加。

菜单里这个入口排在 Settings 之上、Unlock Features 之下，说明 Beli 把它当核心增长动作，不是附属设置。

## 解决什么问题

表面是校内美食社交圈，实际解决三个增长问题：

冷启动的社交密度。餐厅评分 App 需要朋友也在用才有意义。学校是天然的高密度社交网络，绑定后排行榜上立刻出现认识的人。

口碑裂变的结构化。80% 用户来自推荐，但"邀请朋友"缺乏动力。学校竞赛把个人推荐转化成集体荣誉——你在帮学校争排名，不只是帮自己拉人。经典的 group-level incentive。

留存。校内排行榜天然有攀比效应，加上每周积分设计，推动持续打卡。类似 Duolingo 的 streak。

## 效果

评分量从 2022 年 250 万增长到 2025 年 5800 万，CAGR 180%，主要靠口碑。NYU 新生入学迎新就下载 Beli，已经是校园文化。UChicago、Brown、Northwestern 是早期种子校。

策略上，2021 年秋就招校园大使参与产品迭代。Her Campus、Spoon University、NYU Washington Square News 等校园媒体大量覆盖，客观上形成了免费分发渠道。

## 设计要点

邀请制 + 学校绑定是双重飞轮。注册要邀请码，进来后鼓励绑定学校拉更多人，两个钩子嵌套。功能解锁机制（评价 10 家餐厅才解锁高级功能）和学校积分互相强化——你为解锁去打分，打分同时为学校加分。

游戏化很轻量：排名 + 学校荣誉 + streak，没有复杂积分体系，但精准打中大学生的竞争心理。

## 启发

"Add Your School" 本质是用身份归属驱动增长。把个人行为（打分）变成集体行为（为校争光），传播力远超个人激励。这个思路适用于任何有天然群体归属的场景——公司、城市、社区——都可以用"加入你的 XX"制造社交密度和竞争动力。

## Sources

- [Beli - Wikipedia](https://en.wikipedia.org/wiki/Beli_(app))
- [How Beli Became Gen Z's Yelp - Food Network](https://www.foodnetwork.com/fn-dish/news/beli-app-trend)
- [NYU students and Beli - Washington Square News](https://nyunews.com/culture/dining/2023/10/16/beli-app/)
- [Design Critique: Beli App - IXD@Pratt](https://ixd.prattsi.org/2024/09/design-critique-beli-app/)
- [Beli: food diary and dining advisor - Startup Signals](https://startupsignals.substack.com/p/beli-your-food-diary-and-dining-advisor)
