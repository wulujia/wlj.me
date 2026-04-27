---
title: "Bitwarden CLI npm 包被投毒，AI 编码工具凭证成新目标"
date: 2026-04-27T12:10:42+08:00
tags: ["AI","Security","Tech"]
draft: false
slug: "bitwarden-cli-supply-chain-attack"
---

The Hacker News 报道了一起 npm 供应链攻击：Bitwarden CLI 的 npm 包（@bitwarden/cli）2026.4.0 版本被植入恶意代码，藏在包内的 bw1.js 文件里。

感染窗口从 4 月 22 日 ET 时间下午 5:57 到 7:30，约 1.5 小时，估计 334 次下载。被怀疑是更大规模 Checkmarx 供应链攻击的一部分，归因到 "Shai-Hulud: The Third Coming" 这一波。

## 攻击路径

攻击者拿下了 Bitwarden CI/CD 流水线里一个被入侵的 GitHub Action（checkmarx/ast-github-action），通过 preinstall 钩子在用户 npm install 时执行恶意代码。

据安全研究员 Adnan Khan 说，这可能是首次使用 npm Trusted Publishing 的包遭到入侵。

## 恶意代码偷什么

- 本地开发凭证：GitHub / npm tokens、.ssh 密钥、.env 文件、shell 历史
- 云端密钥：GitHub Actions 环境变量、CI/CD secrets、多云凭证
- AI 编码工具配置：Claude、Kiro、Cursor、Codex CLI、Aider 的认证配置
- 自传播：偷到 GitHub token 后注入恶意 Actions workflow，用偷到的 npm 凭证向下游包发布恶意版本，蠕虫式扩散
- 数据外泄走 AES-256-GCM 加密发到伪装域名 audit.checkmarx[.]cx，失败后以 GitHub commit 作为 fallback

有一个细节：如果系统 locale 是俄罗斯，恶意代码自动退出。这一行为与原始 Checkmarx 攻击不一致。

## 对开发者的影响

以前担心的是 SSH 私钥和云服务 key，这次攻击者把 Claude、Cursor、Codex CLI 这些 AI 工具的凭证写进了目标列表。Anthropic 和 OpenAI 的 API key 也是高价值目标了。

## 中招了怎么办

如果在 4 月 22 日那 1.5 小时窗口里 npm install @bitwarden/cli 装到了 2026.4.0，按 Bitwarden 官方流程：卸载 2026.4.0，清理 npm 缓存，临时禁用 npm install 脚本，检查 IoC，轮换所有可能暴露的密钥，审计 GitHub 活动和 CI workflow，最后安装 2026.4.1（即 2026.3.0 的重新发布版）。

重点要轮换的密钥：

- AI 工具的 API key：Claude API key、Cursor 配置、Codex CLI 凭证
- GitHub Personal Access Token 和 CI 用的 token
- npm 发布凭证
- .env 里的云服务密钥
- 没设 passphrase 的 SSH 私钥

## 防御加固

- 给 npm install 默认加 --ignore-scripts，或者 pnpm 设 enable-pre-post-scripts=false
- 重要项目用 npm install --frozen-lockfile 锁版本
- AI 工具的凭证用专门的 secret manager，不要直接放 .env
- GitHub token 加最小权限和短过期时间

Bitwarden 官方说没证据表明用户密码库被访问或泄露——这次被针对的是开发者，不是 Bitwarden 的最终用户。
