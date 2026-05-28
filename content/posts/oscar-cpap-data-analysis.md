---
title: "OSCAR：看 CPAP 真实在做什么"
date: 2026-05-28T09:57:44+08:00
lastmod: 2026-05-28T09:57:44+08:00
author: "Luca"
tags: ["Life","AI","Tools"]
draft: false
slug: "oscar-cpap-data-analysis"
---

之前那篇 Apple Watch 数据分析说过，Apple Watch 推断的"夜间呼吸异常事件"不准。要看 CPAP 真实效果只能看机器本身的 SD 卡——那里有每一晚每两秒采样的数据。

把 SD 卡从呼吸机里拔出来插到电脑上，里面有个 DATALOG 文件夹，按日期一晚一个子目录。导出来扔给 Claude 跑脚本，14 晚的数据 30 秒就出来了。

下面分开说：CPAP 是什么、OSCAR 是什么、SD 卡里有什么文件、这些数据能算出什么、我自己最近两周的情况。

---

## CPAP 是什么

Continuous Positive Airway Pressure，持续气道正压通气。一台小机器，靠管子和面罩把空气持续吹进鼻腔，用正压撑开睡觉时容易塌掉的上气道。专门治阻塞性睡眠呼吸暂停（OSA，Obstructive Sleep Apnea）。

OSA 的机制：睡着后喉咙后面的软组织松弛塌下来，把气道堵住，呼吸短暂停。停几秒大脑缺氧自动惊醒一下，气道打开，又睡着，几分钟后再来一次。一晚循环几十上百次，自己感觉不到。

CPAP 不吃药、不开刀，靠空气压力机械上不让气道塌。

我用的是 ResMed AirSense 10，自动调压（AutoSet）模式——机器实时检测气道塌陷的程度，自动在 5-15 cmH₂O 范围内调整压力。

---

## OSCAR 是什么

Open Source CPAP Analysis Reporter。开源软件，Mac/Windows/Linux 都能装。专门解析 ResMed、Philips DreamStation、Fisher & Paykel 这几家主流厂商 CPAP 机器 SD 卡的数据。

呼吸机厂商通常有自家 App（ResMed 的 myAir、Philips 的 DreamMapper），但只给摘要：昨晚 AHI 多少、漏气是否合格、星星几颗。

OSCAR 直接读底层 EDF 文件，能看到每一晚每两秒的漏气、压力、流量限制、潮气量、呼吸频率，以及每一个被检测出来的呼吸暂停或低通气事件。还能画图，把 5 个小时的数据铺成一张大图。

想自己看清楚 CPAP 在替你做什么，OSCAR 是唯一选择。

---

## SD 卡里有什么文件

我这台 ResMed AirSense 10 的 SD 卡，DATALOG 文件夹按日期分子目录，比如 `20260513/`、`20260514/`。每一晚的文件夹里有 5 个 EDF 文件（European Data Format，医学数据通用格式）：

- **CSL.edf** — Compliance Session List。当晚开机/关机时间戳。
- **EVE.edf** — Events。呼吸事件：Apnea（完全暂停）、Hypopnea（低通气）、FlowLimit（流量限制）、RERA（呼吸努力相关觉醒）。每个事件带时间戳和持续时长。
- **BRP.edf** — Breath-Rate Pressure。25Hz 高频采样，气流和压力波形。文件最大，单晚 2-3 MB。
- **PLD.edf** — Per Lap Data，按 2 秒间隔采样的关键指标：
  - MaskPress（面罩实际压力）
  - Press（设定压力）
  - EprPress（EPR 调整后压力）
  - Leak（漏气量，L/s 单位）
  - RespRate（呼吸频率）
  - TidVol（潮气量）
  - MinVent（每分钟通气量）
  - Snore（鼾声强度）
  - FlowLim（流量限制指数）
- **SAD.edf** — Summary And Data。如果接了外置血氧模块，里面有 SpO2 和脉搏。我没接，所以全是 -1。

每个 EDF 还有一个同名 .crc 校验文件，保证数据没在 SD 卡上损坏。

---

## 这些数据能算出什么

核心指标是 AHI（Apnea-Hypopnea Index，呼吸暂停低通气指数）。每小时睡眠里发生多少次：

- Apnea：气流完全停止 ≥ 10 秒
- Hypopnea：气流减少 ≥ 30% 同时血氧下降 ≥ 3%

OSCAR 数 EVE.edf 里的事件总数，除以使用时长。

- AHI ≥ 5 是 OSA 诊断阈值
- AHI < 5 是治疗成功
- AHI < 1 是极优

第二重要的是漏气：

- 取 PLD.edf 的 Leak 通道（L/s）× 60 → L/min
- 计算 95% 分位数（P95）
- ResMed 警戒线 24 L/min
- P95 漏气太高 = 面罩没戴好，治疗压力会被泄掉，AHI 会随之上升

还能看：

- 治疗压力的均值和 95% 分位（你的机器实际跑到多高）
- 鼾声指数（低通气前的预警）
- 流量限制指数（气道开始变窄但还没塌）
- 使用时长是否够（≥ 4h/晚算"合规"）

---

## 我自己的两周

5/13 启用 CPAP，到现在戴了两周多。14 个夜分成三类：

**完整戴的 10 晚**（≥ 5h）：5/13-16、5/19-22、5/25-26
**开机即摘 2 晚**：5/18 戴了 4.97 分钟，5/24 戴了 3 分钟（疫苗那天）
**完全没戴 2 晚**：5/17、5/23

10 个完整夜的关键数据：

| 指标 | 我的值 | 临床目标 |
|---|---:|---|
| AHI | **0.10** | < 5 优，< 1 极优 |
| 使用时长 | 7.15h/晚 | ≥ 4h |
| 漏气 P95 | 21 L/min | < 24 |
| 治疗压力均值 | 9.98 cmH₂O | < 15（我设的上限）|

AHI 0.10 接近零，相当于平均每 10 小时才有 1 个事件。机器把我的 OSA 基本消除掉了。

治疗压力只跑到 9.98 cmH₂O（最高 11.88），离我设的上限 15 还很远。我的 OSA 严重度本身不重——气道塌得不深，10 cmH₂O 就撑得住。

一个孤立高值：5/19 那晚漏气 P95 飙到 36 L/min，远超 24 警戒线。其他 9 晚都 < 26。但那晚 AHI 仍是 0——单晚漏气偏高没毁掉治疗效果。

---

## OSCAR 比 Apple Watch 准多少

用 Apple Watch 数据做了次对照实验：戴 CPAP 的 8 晚 vs 同一周没戴 CPAP 的 3 晚（控制组），Apple Watch 推断的"呼吸异常事件"两组数字几乎一样——1.38 vs 1.39 次/小时。它不知道我戴了 CPAP 没。

而 CPAP 自己记的 AHI，戴的夜是 0.10，没戴的夜按之前估算在 5+。差 50 倍。

判断 CPAP 治疗效果，看 OSCAR，不是 Apple Watch。

---

## 下一步

- 把 EPR 从 3 降到 2，看主观舒适度有没有改善
- 6/8 满 4 周再跑一次完整对比
