---
title: "把 Hugo 博客从 GitHub Pages 迁移到 Cloudflare Pages"
date: 2026-04-13T20:00:00+08:00
tags: ["Hugo", "Cloudflare"]
draft: false
slug: "hugo-github-pages-to-cloudflare"
---

这个博客之前用 GitHub Pages 托管，通过 GitHub Actions 构建 Hugo，推到 main 分支就自动部署。用了一段时间，没什么大问题，但 Cloudflare Pages 有几个吸引我的地方：构建速度更快，自带 CDN 和 DDoS 防护，DNS 和托管在同一个面板管理。

迁移很简单，整个过程不到二十分钟。

## Cloudflare Pages 创建项目

登录 Cloudflare Dashboard，进 Workers & Pages，点 Create，选 Pages，连接 GitHub 仓库。

构建配置：

- Framework preset：Hugo
- Build command：`hugo --gc --minify`
- Build output directory：`public`

环境变量加一条：`HUGO_VERSION` = `0.159.2`（和原来 GitHub Actions 里保持一致）。Cloudflare 内置的 Hugo 版本比较旧，不设这个大概率构建失败。

设好之后 Cloudflare 会立即触发一次构建，几十秒就能完成。构建成功后会分配一个 `xxx.pages.dev` 的临时域名，可以先打开看看效果对不对。

## DNS 迁移

在 Cloudflare 添加域名，它会给你两个 nameserver，类似 `alice.ns.cloudflare.com` 和 `bob.ns.cloudflare.com`。

去域名注册商（或者原来用的 DNS 服务商，比如 DNSPod）把 nameserver 改成 Cloudflare 给的这两个。改完之后等 DNS 传播，通常几分钟到几小时。

Cloudflare 会自动扫描你现有的 DNS 记录并导入，检查一下有没有遗漏就行。

## 绑定自定义域名

Pages 项目设置里，Custom domains，添加 `wlj.me`。Cloudflare 会自动创建对应的 CNAME 记录，SSL 证书也自动签发，不用操心。

## 旧配置要不要删

GitHub Actions 的 workflow 文件和 GitHub Pages 的配置可以不删。DNS 指向 Cloudflare 之后，GitHub Pages 那边的站点没人访问，只是每次 push 会白跑一次构建。留着也算一个备份，哪天 Cloudflare 出问题，把 DNS 切回去就能恢复。

想省 GitHub Actions 的构建时间，删掉 `.github/workflows/hugo.yml` 就行，也可以在 GitHub repo 的 Settings → Pages 里关掉。

## Hugo 版本升级

以后想升级 Hugo 版本，去 Cloudflare Dashboard 改一下 `HUGO_VERSION` 环境变量就行，不用动代码。
