---
title: "顺着一封 DMARC 报告，学一下邮件认证三件套"
date: 2026-05-09T23:18:56+08:00
lastmod: 2026-05-10T11:58:47+08:00
author: "Luca"
tags: ["Email","Security","Ops"]
draft: false
slug: "dmarc-report-slax-email-audit"
---

slax.com 的客服邮箱每天会收到几封 DMARC Aggregate Report，发件人是 `dmarcreport@microsoft.com`，附件是几百字节的 zip，里面是 XML。我之前从来不开。今天问了 Nix 一下这是什么，顺着学了一遍邮件认证三件套：SPF、DKIM、DMARC。

## SPF

SPF（Sender Policy Framework）配在 DNS 里，告诉收件方"这些 IP 才允许替我发邮件"。比如域名用飞书邮箱，SPF 记录会写：

```text
v=spf1 +include:_netblocks.m.feishu.cn -all
```

意思是飞书的发送服务器 IP 都允许，其他一律拒绝。

SPF 的弱点是不抗转发。客户把我的邮件转发到 Gmail 时，源 IP 变成转发服务器，原来的 SPF 检查就失败了。

## DKIM

DKIM（DomainKeys Identified Mail）给每封外发邮件加密签名。私钥在邮件服务器那边，公钥发布在 DNS 里。收件方拿公钥验签，确认这封邮件是我发的、内容没被篡改。

签名跟着邮件走，被转发也不掉。所以 SPF 失败的转发场景，DKIM 还能过。

DKIM 的 selector 名因服务商而异，飞书是 `feishu` 加一串时间戳，比如 `feishu2605101150._domainkey.yourdomain.com`。要查 DKIM 是否配置，得知道精确的 selector 名。我一开始拿常见的 `s1`、`default`、`larksuite` 去 dig，全部空，以为是没配。后来登录飞书后台才看到真实的 selector，DKIM 其实早就启用了。

## DMARC

DMARC（Domain-based Message Authentication, Reporting & Conformance）是上面两件的协调层。它告诉收件方"如果 SPF 和 DKIM 都对不上我可见的 `From:` 地址，按这个策略处理（none / quarantine / reject），并把每天的统计发到这里"。

一个典型的 DMARC 记录：

```text
v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@yourdomain.com
```

- `p=quarantine` 失败丢垃圾箱（也可以 `none` 只观察、`reject` 直接拒收）
- `pct=100` 全量执行
- `rua=mailto:...` 收每天的聚合报告

每天来的那一封 DMARC 报告，就是各家邮件服务商按这个 `rua` 标签生成的：告诉我有谁声称是我，谁通过了，谁失败了。

## 自查命令

任何域名都可以用这几条查现状：

```bash
dig +short TXT yourdomain.com           # SPF
dig +short TXT _dmarc.yourdomain.com    # DMARC
dig +short MX yourdomain.com            # 邮件服务商
```

DKIM 要知道 selector 才能查。飞书的可以登录管理后台 → 邮箱 → 域名设置 → DKIM 看到 selector 名。
