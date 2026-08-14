---
title: "在手机上用自己电脑里的 AI Agent"
date: 2026-08-14T12:10:00+08:00
lastmod: 2026-08-14T12:10:00+08:00
author: "Luca"
tags: ["Tools","Tech","AI"]
draft: false
slug: "phone-access-local-ai-agent-tailscale"
---

DeepSeek 开源了自己的 agent harness，叫 dsh。装上跑一条命令就能用：

```bash
npx @deepseek-ai/dsh web
```

它没有终端界面，只有浏览器 UI，默认起在 `http://127.0.0.1:3080`。我想在手机上也能用——躺着的时候给它派个活，回到电脑前看结果。

## 不要直接开放到局域网

第一反应是把它绑到 `0.0.0.0`，手机连同一个 wifi 就能访问。dsh 直接拒绝了这个参数，报错写得很直白：

> `--host 0.0.0.0 is intentionally not supported yet for safety: it would expose remote code execution to the network`

这不是没做完，是故意堵死的。这类 agent 能跑 shell、能读写你整个文件系统，而它目前**没有任何用户认证**。裸奔在局域网上，等于把电脑的 shell 交给任何连了你 wifi 的人。

## 用 Tailscale 反代

正确的做法是：程序继续只绑本地回环，前面放一层带认证的代理。Tailscale 正好干这个。

```bash
# 1. 启动，同时声明信任的域名
dsh web --trusted-host 你的机器名.你的tailnet.ts.net

# 2. Tailscale 在前面反代
tailscale serve --bg 3080
```

完事。手机连上 Tailscale，打开 `https://你的机器名.你的tailnet.ts.net/` 就能用，自带 HTTPS 和设备级认证，家里 wifi 上什么都没暴露。

注意别用 `tailscale funnel`——那是把服务放到公网，对这种东西是灾难。`serve` 只在自己的 tailnet 内可见。

## 两个必须知道的坑

**第一，`--trusted-host` 不是可选项。**

dsh 的 API 有一道防 DNS rebinding 的栅栏：每个请求的 `Host` 头必须是本地回环，或者在信任名单里，否则一律 403。这个设计是对的——攻击者能骗你的浏览器发请求，但伪造不了 Host 头。

反代过来的请求 Host 是那个 tailnet 域名，不声明就全被拦。我一开始没加，页面能打开，一交互就报错。

**第二，手机上改不了设置和 API key。**

dsh 把这几个高危操作**永久钉在本地回环**，信任名单也放行不了：

- 读写设置
- 设置和删除 API key
- 调用系统的文件选择器
- 读取和管理 agent 预设

代码注释里的原话是「until a real authentication layer exists」。所以顺序是：**先在电脑上配好 API key 和工作目录，手机再连上去开会话**。日常用没影响——发消息、看结果、审批工具调用都正常。

## 让它常驻

每次手动起太麻烦，写个 launchd 配置放 `~/Library/LaunchAgents/`：

```xml
<key>ProgramArguments</key>
<array>
  <string>/opt/homebrew/bin/node</string>
  <string>/Users/你的用户名/.local/dsh/node_modules/@deepseek-ai/dsh/lib/bin.js</string>
  <string>web</string>
  <string>--trusted-host</string>
  <string>你的机器名.你的tailnet.ts.net</string>
</array>

<key>EnvironmentVariables</key>
<dict>
  <key>PATH</key>
  <string>/Users/你的用户名/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
</dict>

<key>RunAtLoad</key>
<true/>
<key>KeepAlive</key>
<dict><key>SuccessfulExit</key><false/></dict>
```

```bash
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.deepseek.dsh-web.plist
```

两个地方容易翻车：

**必须写 node 的绝对路径。** 脚本开头是 `#!/usr/bin/env node`，而 launchd 的 PATH 是最小集，找不到 node。

**必须显式注入 PATH。** 这条更隐蔽——agent 的 bash 工具继承的就是这个 PATH。不写的话它跑命令时会发现 git、rg、python 全都不存在，症状很怪，排查半天。

Tailscale serve 的配置本身是持久的，重启电脑不用管。

## 这套思路不限于 dsh

任何「只绑本地、没有认证、但你想远程用」的自建服务都适用：本地回环 + Tailscale serve + 声明信任域名。比开端口映射、比公网加密码，都更省事也更安全。
