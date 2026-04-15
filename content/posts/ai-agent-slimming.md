---
title: "给 AI Agent 瘦身"
date: 2026-04-16T07:19:58+08:00
tags: ["AI","Tools"]
draft: false
slug: "ai-agent-slimming"
---

我的 OpenClaw 跑了几个月，token 账单越来越肥。今天花了一个小时做了一轮瘦身，效果不错，记录一下。

核心发现很简单：很多任务根本不需要 AI 参与，但它们都在 AI 会话里跑。每跑一次，哪怕只是执行一句 bash 命令，也要启动一个 session、加载 context、消耗 token。相当于你请了一个年薪百万的工程师，每天的工作是帮你按一下回车键。

具体做了四件事。

第一，降低心跳频率。Agent 有一个 heartbeat 机制，定时唤醒做巡检。我之前把 OpenClaw 设成 8 小时一次，配置没真正生效，实际还是一天 24 次。改成 12 小时一次，一天 2 次。心跳的作用是维护 context、检查状态，2 次够了。

第二，把纯 shell 任务迁出 AI。安全巡检、日志整理、会话记录提取、GitHub 同步、版本检查这些任务，本质都是跑一个 shell 或 Python 脚本。之前放在 OpenClaw 里，执行链路是：cron 触发 → 启动 AI session → AI 理解 prompt → AI 调用 bash → 收集输出 → AI 总结输出 → 发通知。现在改成：crontab 触发 → 跑脚本 → 有输出就用 Gmail API 发邮件。中间砍掉了 AI 理解和总结两步，对这类任务毫无价值。

写了一个通用的 wrapper 脚本，20 来行。脚本正常跑完没输出就静默，有输出或者失败就发邮件，失败的邮件标题加 [FAIL] 前缀。简单粗暴，但够用。复用了 OpenClaw 已有的 Gmail OAuth 凭证，不需要额外配置。

迁移过程中顺手修了安全巡检的一个误报 bug。脚本用 grep -ci "critical" 统计严重问题数量，但 `openclaw security audit` 输出的 summary 行本身就包含 "0 critical"，grep 会把这行也数进去，导致永远报 1 个 critical。改成用正则提取数字就好了。这种 bug 不难，但没人看脚本输出的话，能默默误报好几个月。

第三，调整 context 压缩阈值。AI 的 API 成本跟 context 长度成正比。原来 context 用到 93% 才压缩，大部分时间都在高 context 区运行。改成 50% 触发压缩后，每次交互的平均 context 从 141k 降到 83k，摊薄下来每次调用省 38% 的 input tokens。压缩频率会高一些，但每次压缩本身也更快更便宜。附带的好处是 agent 响应也快了，因为 prefill 的数据少了。

第四，修复配置的连锁反应。改了压缩阈值，有两个关联参数也得跟着调。一个是 memoryFlush 的触发时机——压缩前 agent 会把重要信息写到文件里，原来的缓冲区太小，agent 可能写到一半就被压缩打断。另一个是 context 缓存的过期时间，原来设成 1 小时，但 heartbeat 改成 12 小时后，每次 heartbeat 到来时缓存早就过期了，等于没用。这种事情很典型：改了一个参数觉得完事了，但系统是一张网，拉动一根线会影响其他地方。

后来又审计了一轮，发现两个问题。

一个是 shell 任务其实没迁干净。OpenClaw 安装时往 ~/.config/systemd/user/ 里放了几个 timer，一天几次在背后跑同样的脚本。我当时只改了 OpenClaw 自己的调度配置，没想到脚本还被 systemd timer 这一层调度。session_to_log 这种脚本，实际上一天被 crontab、systemd timer、OpenClaw 三个调度器各唤醒一次。冗余跑了一段时间我没察觉。统一到 crontab 一层之后，`crontab -l` 就能看到所有任务，一处可见。迁移的意思不止是新增一条路径，还包括把旧路径关掉。

另一个漏洞是"需要 AI"的任务也能瘦身。邮件翻译第一轮被判定为"需要 AI"，留在 agent 里。后来想明白，agent session 和一次 LLM CLI 调用不是一个量级。前者要启动会话、加载历史、进入生命周期；后者就是 stdin 进 stdout 出。我用 codex CLI 重写了邮件翻译：Python 脚本抓未读邮件、调 `codex exec` 翻译和判重要、推 Telegram、标已读，一次 14 秒跑完。原来 agent 版本要 2 分钟以上，token 消耗差一个数量级。

两轮下来，OpenClaw 的内部调度清空了，jobs.json 只剩 `{ "jobs": [] }`。agent 现在只做 Telegram 对话入口，不再承担调度职责。

判断一个任务是否需要 AI，标准很简单：它需要理解、推理、生成吗？确定性操作加转发结果，是 crontab 的活。需要 AI 的任务还要再选调用方式，从重到轻依次是：长期运行的 agent daemon、独立的 agent session、一次 CLI 调用。量级差一到两个数量级。邮件翻译一次 codex 调用就够了。

agent 平台让设置自动化任务变得太方便了，方便到你会不自觉地把所有事情都丢给它。定期审计一下哪些任务在跑、频率是否合理、是否真的需要 AI，是值得养成的习惯。
