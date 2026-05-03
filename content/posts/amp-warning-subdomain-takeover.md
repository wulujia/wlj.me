---
title: "一个 AMP 报警，挖出一个子域名接管"
date: 2026-05-03T21:41:01+08:00
lastmod: 2026-05-03T21:41:01+08:00
author: "Luca"
tags: ["SEO","Security","Ops"]
draft: false
slug: "amp-warning-subdomain-takeover"
---

今天收到 Google Search Console 的一封邮件：

> AMP issues detected in wulujia.com
>
> To the owner of wulujia.com:
>
> Search Console has identified that your site is affected by 1 AMP issue(s). The following issues were found on your site.
>
> Top non-critical issues
>
> AMP page domain mismatch
>
> Non-critical issues are suggestions for improvement, but don't prevent the page or feature from appearing on Google. Some of these issues could be reclassified as critical in the future, and critical issues can affect your site's appearance on Search.
>
> We recommend that you fix these issues when possible to enable the best experience and coverage in Google Search.

第一反应是奇怪。我这个老站没做 AMP。源码里搜了一遍，也没有 `rel="amphtml"`。

继续查 Search Console 里的示例 URL，看到一个 Cloudflare Pages 域名，形如：

```text
https://<some-project>.pages.dev/
```

打开之后是一个真正的 AMP 页面，内容是印尼博彩。它的 canonical 指向我的一个子域名：

```html
<link rel="canonical" href="https://<some-subdomain>.wulujia.com/">
```

再打开这个子域名，也是同一套博彩页面。页面里还有：

```html
<link rel="amphtml" href="https://<some-project>.pages.dev/" />
```

这就解释了 Google 的邮件。canonical 页在 `wulujia.com` 的某个子域名，AMP 页在 `pages.dev`，两个域名不一致，所以 Search Console 报 `AMP page domain mismatch`。

真正的问题在 DNS。

Cloudflare DNS 里有两条历史遗留记录：

```text
A    *    185.199.111.153
A    *    185.199.108.153
```

`*` 是 wildcard。意思是所有没有明确配置的子域名，都会解析过去。那两个 IP 是 GitHub Pages 的 IP。

所以链路变成了：

```text
<some-subdomain>.wulujia.com
-> 命中 *.wulujia.com
-> 解析到 GitHub Pages
-> 被别人用这个子域名挂了垃圾页
```

我犯的错误是把 wildcard 当成方便的兜底配置。老站、旧博客、GitHub Pages、Cloudflare 之间迁来迁去，DNS 里留下了这个东西。我以为没主动使用的子域名就没有风险，实际不是这样。DNS 只负责把名字指过去，不管那里是不是我自己的内容。

[GitHub Pages 文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)里也明确提醒，不要用 wildcard DNS 指向 GitHub Pages，这会带来 domain takeover 风险。

修复方式很简单：

1. 在 Cloudflare DNS 删除 `*.wulujia.com` 的 wildcard A 记录。
2. 只保留明确需要的子域名，比如 `www`、`blog`。
3. 用 `dig <some-subdomain>.wulujia.com A` 确认异常子域名不再解析。
4. 用 `curl -I https://<some-subdomain>.wulujia.com/` 确认博彩页消失。
5. 在 Search Console 的 Removals 里提交 `https://<some-subdomain>.wulujia.com/` 前缀移除。
6. 在 AMP 报告里点 Validate Fix。
7. 向 Cloudflare 举报那个 `pages.dev` 垃圾页。

另一个顺手修的点是 `www`。它不是这次事故的主因，因为 `www` 是明确子域名，不会被别人随便接管。但它还指向一个很旧的 GitHub Pages IP，访问时会多跳一次 HTTP。这个应该改成 Cloudflare Redirect Rule：

```text
https://www.wulujia.com/* -> https://wulujia.com/$1
```

然后把旧的 `www` A 记录清掉。

这事有意思的地方在于，入口只是一封看起来不严重的 AMP 提醒。[Google 的说明](https://support.google.com/webmasters/answer/7478053?hl=en)里也写了，这个 issue 不影响索引和排名。可顺着它往下查，看到的是 DNS 里一个很多年前留下来的坑。

小站也会有基础设施债。尤其是个人域名用得久，GitHub Pages、Cloudflare Pages、Vercel、Netlify 都试过，DNS 最容易变成旧配置博物馆。

这次记下来，主要是提醒自己：

不要把 wildcard DNS 指向任何托管平台，除非非常确定每一级子域都被自己控制。更好的习惯是，需要哪个子域就配哪个子域。
