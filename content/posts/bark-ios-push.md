---
title: "Bark 是什么：给 iPhone 推自定义通知的极简通道"
date: 2026-09-08T11:37:53+08:00
lastmod: 2026-09-08T11:37:53+08:00
author: "Luca"
tags: ["Tech","Tools","AI"]
draft: false
slug: "bark-ios-push"
---

开源 App + 可选自建后端，用一条 HTTP 请求把消息打到系统通知栏。对「AI agent 跑完任务提醒我」这种场景，往往比钉钉/飞书/Telegram 机器人更短、更贴锁屏。

| iOS only | HTTP → APNs | 开源 + 免费 |
| --- | --- | --- |
| 接收端是 Bark App（系统推送） | 你发请求，后端转苹果推送 | App 与 bark-server 均开源；公共服长期维护承诺 |

## 一句话

**Bark**（[Finb/Bark](https://github.com/Finb/Bark)）是一款 iOS App：装好后你会得到一个设备 `key`，之后任何脚本/服务器/Agent 只要访问类似 `https://api.day.app/你的key/标题/内容` 的 URL（或 POST JSON），消息就会以**系统推送**出现在 iPhone 上——App 不必一直在前台跑。

它解决的不是「团队 IM」，而是「把事件打到我自己的手机锁屏」。所以你说适合 AI agent 任务完成推送，方向是对的。

## 它怎么工作

| 步骤 | 内容 |
| --- | --- |
| 1 · APP | App Store 装 Bark，打开拿到 device key（也可扫码/复制推送 URL）。 |
| 2 · 请求 | 脚本对公共服 `api.day.app` 或自建 bark-server 发 GET/POST。 |
| 3 · 转发 | bark-server 把消息交给 Apple APNs（系统推送通道）。 |
| 4 · 到达 | iOS 弹出通知；可分组、点按跳 URL、归档历史等。 |

相对「自己接 APNs」：你不用管苹果开发者证书、HTTP/2、token 刷新。公共 Bark 把这些藏在 App/官方后端里；自建时多数人仍可继续用官方 App 的 APNs 能力（按项目文档部署 bark-server）。

## 是不是「现在 iOS 推送最简单的方式」？

**对「推给我自己这部 iPhone」——基本是的，尤其在个人自动化/Agent 场景。**对比常见替代：

| 方案 | 简单度 | 到达形态 | 代价/限制 |
| --- | --- | --- | --- |
| **Bark** | 极高：一条 URL/curl | 系统通知栏 | 几乎只服务 iOS；key 泄露=别人能刷你通知 |
| 钉钉 / 飞书机器人 | 中高（建群+Webhook） | IM 会话 | 要打开对应 App；偏团队协作噪音；接口与安全策略更重 |
| Telegram Bot | 中高 | IM | 需 Bot Token + chat_id；海外网络；不是锁屏级「系统推送」体验（取决于客户端） |
| 自建 APNs / FCM | 低 | 系统推送 | 证书、包名、设备 token，工程量大 |
| 邮件 / 短信 | 中 | 邮箱/短信 | 延迟与打扰形态不同；短信有成本 |
| ntfy / Gotify 等 | 高 | 多端 | Android 友好；iOS 往往不如 Bark「开箱 APNs」顺 |

**边界：**若你要 Android + iOS 统一、或必须进团队群可检索历史，钉钉/飞书/Telegram 仍更合适。Bark 赢在「个人、iOS、系统推送、一行 HTTP」。

## 为什么特别适合 AI Agent

- **完成即推：**长任务（训练、爬虫、cloud agent、本机脚本）结束时 `curl` 一下，手机震动，不必盯终端。
- **无会话负担：**不用维护群聊机器人权限、不用 @机器人格式。
- **可分级：**`level=timeSensitive` / `critical` 等，重要失败可更强硬提醒（具体能力随 iOS 版本与权限）。
- **可分组：**`group=agent` / `group=deploy`，通知中心不搅成一团。
- **可带跳转：**`url=` 点开直达日志页、PR、监控面板。

## 最小用法（回头可抄）

App 里复制你的 key 后：

```bash
# 最简 GET（路径里带标题/正文，注意 URL 编码）
curl "https://api.day.app/YOUR_KEY/Agent完成/报表已生成"

# 推荐：POST JSON（正文含中文/换行更稳）
curl -X POST "https://api.day.app/push" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "device_key": "YOUR_KEY",
    "title": "Agent 完成",
    "body": "Care Expo 报告已写入 Dropbox/misc",
    "group": "agent",
    "url": "https://wlj.me/"
  }'
```

也支持 `/:key/:body`、`/:key/:title/:body`、`/:key/:title/:subtitle/:body` 等路径形态；完整参数见官方 tutorial / bark-server API V2（title、subtitle、body、group、sound、icon、level、copy、badge、url…）。

## 公共服 vs 自建

- **公共** `https://api.day.app`：零运维，个人低频完全够用。官网表述：2018 年上线，维护至少到 2031；维护期内 App 无广告收费承诺（以官网为准）。
- **自建 bark-server**（[Finb/bark-server](https://github.com/Finb/bark-server)）：流量大、要加密推送、或不想依赖公共入口时用。文档称低配也能扛很高 QPS；个人 Agent 场景通常用公共服即可。
- **隐私：**可走加密推送等能力（见官方「隐私与安全」说明）；自建可减少中间环节可见明文的路径，但仍要保护好 device key。

## 和钉钉/飞书/Telegram：怎么选（实用）

| 你的目标 | 更合适 |
| --- | --- |
| Agent/脚本结束「戳一下我」 | Bark |
| 要和同事同步、可搜索聊天记录 | 钉钉 / 飞书 / Telegram |
| 需要卡片按钮、审批流 | 飞书/钉钉 |
| Android 为主或多端统一 | Telegram / ntfy / 飞书 |
| 锁屏强提醒、系统级体验 | Bark（iOS） |

很多人最终是**组合**：Bark 给自己；飞书/Telegram 给团队。不是非此即彼。

## 使用注意

- **Key = 权限：**泄露后他人可向你狂推。放环境变量，别写进公开仓库；可定期在 App 重置。
- **仅 iOS 接收端：**家人安卓机收不到 Bark 系统推送。
- **不是聊天软件：**弱于会话、表情、多人讨论。
- **网络：**推送链路依赖能访问你选的 bark-server / api.day.app，以及设备能连上 APNs。

## 延伸阅读

- [github.com/Finb/Bark](https://github.com/Finb/Bark) — iOS App
- [github.com/Finb/bark-server](https://github.com/Finb/bark-server) — 后端
- [bark.day.app](https://bark.day.app/) — 官网/文档
- API：仓库内 `docs/en-us/tutorial.md`、`bark-server/docs/API_V2.md`

生成时间 2026-09-07 17:10（UTC+8）· 学习笔记 · 星标/承诺以官方仓库与 bark.day.app 为准
