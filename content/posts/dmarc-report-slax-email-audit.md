---
title: "一封 DMARC 报告，挖出 slax.com 邮件配置的三处问题"
date: 2026-05-09T23:18:56+08:00
lastmod: 2026-05-09T23:18:56+08:00
author: "Luca"
tags: ["Email","Security","Ops"]
draft: false
slug: "dmarc-report-slax-email-audit"
---

slax.com 的客服邮箱每天会收到几封 DMARC Aggregate Report，发件人是 `dmarcreport@microsoft.com`，附件是几百字节的 zip，里面是 XML。我之前从来不开。今天问了 Nix 一下这是什么，顺着查下去，挖出三处问题。

## DMARC 是什么

DMARC 是配在 DNS 里的邮件认证规则。它告诉收件方"声称从这个域名发出的邮件，应该满足 SPF 或 DKIM 验证，不满足的怎么处理"。DMARC 记录里有一个 `rua=mailto:...` 标签，等于公开说"请把每天替我做的验证统计发到这个地址"。Microsoft、Google、Yahoo 这些大邮件服务商按这个标签每天发一封报告。

收到报告本身正常。问题是 slax.com 的 DMARC 把这个地址写成了客服邮箱，所以这些 XML 报告天天堆在客服信箱里。

## 用 dig 拉现状

让 Nix 用 dig 查了一遍：

```bash
dig +short TXT slax.com
# v=spf1 +include:_netblocks.m.feishu.cn -all

dig +short TXT _dmarc.slax.com
# v=DMARC1; p=quarantine; pct=100; ruf=mailto:hi@...; rua=mailto:hi@...

dig +short MX slax.com
# 1 mx1.feishu.cn.
# 5 mx2.feishu.cn.
# 10 mx3.feishu.cn.
```

DKIM 试了 `s1`、`s2`、`default`、`mail`、`selector1`、`larksuite` 等十几个常见 selector，全部空。

## 三处问题

### 1. 报告地址指向客服邮箱

DMARC 有两个报告标签。`rua` 是聚合统计，每天一封。`ruf` 是失败样本，里面带完整的失败邮件副本，包括邮件头、收件人，甚至正文片段。

`ruf` 指到客服邮箱意味着任何发往 slax.com 失败的邮件碎片会落到客服那里读。这是隐私风险。

### 2. DKIM 没配

只配了 SPF。SPF 记的是"哪些 IP 可以替我发邮件"。

SPF 不抗转发。客户把我的邮件转发到 Gmail 时，源 IP 变成转发服务器，SPF 失败。DKIM 给每封邮件加密签名，签名跟着邮件走，被转发也不掉。

只有 SPF 没 DKIM，意味着所有被转发的邮件在收件方那里都过不了 DMARC 检查。每天的报告其实就在告诉我这件事，我之前没看。

### 3. DMARC 标签不全

现在的记录：

```text
v=DMARC1; p=quarantine; pct=100; ruf=mailto:hi@...; rua=mailto:hi@...
```

`p=quarantine` 是失败丢垃圾箱，`pct=100` 全量执行，这两个没问题。缺三个：

- 没有 `sp=`：`p` 只覆盖主域。子域 `notify.slax.com`、`support.slax.com` 没策略
- 没有 `adkim=` / `aspf=`：默认 relaxed，允许子域代主域过 DMARC。改 `s` 严格对齐
- 没有 `fo=`：默认是 SPF 和 DKIM 都失败才报告。`fo=1` 任一失败就报告

## 修复

待办（让同事处理）：

1. 飞书管理后台开 DKIM，把生成的 TXT 记录加到 DNS
2. 新建一个专用的 dmarc 收件地址，不混在客服邮箱
3. 把 DMARC 改成：

```text
v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@...; sp=quarantine; adkim=s; aspf=s; fo=1
```

去掉 `ruf`。多数收件方已经不发它了，留着是隐私风险。

## 自查命令

任何域名都可以用这四条命令查现状：

```bash
dig +short TXT yourdomain.com
dig +short TXT _dmarc.yourdomain.com
dig +short MX yourdomain.com
dig +short TXT default._domainkey.yourdomain.com
```

如果 DMARC 不存在，或者 `rua` 指向有人在读的地址，就有得改。
