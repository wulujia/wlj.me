---
title: "Caddy 是什么，和 Nginx 有什么区别"
date: 2026-09-10T10:30:00+08:00
tags: ["Tech"]
draft: false
slug: "caddy-web-server"
description: "Caddy 在软件部署中负责什么，它和 Nginx 有什么区别，以及目前的市场占有率。"
---

Caddy 是一个 Web 服务器，也可以做反向代理。它和 Nginx 属于同一类软件。

一套 Web 应用部署到服务器后，通常只监听本机端口，比如：

```text
http://127.0.0.1:3000
```

用户访问的则是：

```text
https://app.example.com
```

Caddy 放在应用前面，接收来自互联网的请求，再把请求转给本机的应用：

```text
用户 → HTTPS → Caddy → HTTP → 应用程序
```

它主要处理几件事：

- 接收 80 和 443 端口的公开流量。
- 根据域名，把请求转给对应的应用。
- 自动申请和更新 HTTPS 证书。
- 把 HTTP 请求跳转到 HTTPS。
- 提供静态文件、压缩、访问日志和负载均衡。

应用程序只管自己的业务。域名、证书和公开流量交给 Caddy。

## 和 Nginx 的区别

Caddy 和 Nginx 能做的事情很接近。Nginx 历史更久，市场更大，文档、模块和运维经验也更多。复杂的流量规则、大规模部署和已有的 Nginx 系统，继续使用 Nginx 很自然。

Caddy 的配置短很多。它默认处理 HTTPS 证书，也会自动续期。一个最简单的反向代理只要几行：

```caddyfile
app.example.com {
    reverse_proxy localhost:3000
}
```

用 Nginx 完成同样的部署，通常还要配置证书，并用 Certbot 或其他工具处理续期。对只有几台服务器、几个域名的小团队，Caddy 可以少维护一套证书流程。

Caddy 也很适合 Docker。服务器只把 80 和 443 端口开放给 Caddy，其他容器留在内部网络里：

```text
互联网
  ↓
Caddy
  ├── Web 容器
  ├── API 容器
  └── Admin 容器
```

GitHub Actions 负责构建和发布，Docker 负责运行应用，Caddy 负责接收 Web 请求。三者解决的是不同环节的问题。

## 市场占有率

W3Techs 在 2026 年 9 月 8 日的数据里，统计了能够识别 Web 服务器的网站：

- Nginx 占 31.3%。
- Caddy 占 0.9%。

只看流量排名前 100 万的网站，Nginx 占 27.6%，Caddy 占 1.0%。Caddy 已经出现在大约 1% 的可识别公开网站上，Nginx 的占有率仍然高出约 30 倍。

这个数字只能用来判断大致规模。Cloudflare 会藏住后面的服务器，有些网站也会删除服务器名称。内网服务和私有 API 不在统计范围内。一条请求还可以依次经过 Cloudflare、Caddy 和应用服务器，公网扫描无法还原这些部署层次。

实际选型可以简单一些。已有成熟的 Nginx 配置就继续使用。新部署只有几台 VPS、Docker 服务和常规反向代理需求，Caddy 能省掉不少配置和证书维护工作。

## 来源

- [Caddy Documentation](https://caddyserver.com/docs/)
- [Automatic HTTPS](https://caddyserver.com/docs/automatic-https)
- [W3Techs：Nginx 与 Caddy 使用情况](https://w3techs.com/technologies/comparison/ws-caddy%2Cws-nginx)
- [W3Techs：Web 服务器历史趋势](https://w3techs.com/technologies/history_overview/web_server)
