---
title: "Slax Reader · 项目地图与开发指南"
date: 2026-09-06T19:11:47+08:00
lastmod: 2026-09-06T19:11:47+08:00
author: "Luca"
tags: ["Tech","Startup"]
draft: false
slug: "slax-reader-project-guide"
---

Slax Reader / local field guide / 2026-09-03

先看懂，再动手。

这不是一个仓库。Reader 是一组互相配合的产品、服务和基础组件。下面的地图把“我该改哪里、怎么跑、怎么测、怎样提交”放在同一页。

24 个团队仓库 · `~/Github/reader` · 公开代码 + 闭源代码

## 项目地图

产品入口在 Web、移动端和 CLI；主要业务链路是 Web / App → API → 内容解析、搜索、AI 与通知。

### 用户入口

**slax-reader-web**

Nuxt monorepo：Web 应用 + 浏览器扩展；包含共享的 types / utils。

**slax-reader-client**

Kotlin Multiplatform：Android、iOS、Desktop。

### 业务核心

**slax-reader-api**

Cloudflare Worker + TypeScript + Prisma；用户、书签、同步、AI、搜索、通知。

**readability · jieba · liveproxy**

网页正文提取、中文分词、代理与浏览器侧辅助能力。

### 开发体验

**slax-reader-cli**

Node CLI，可保存、浏览和管理书签，也提供 AI Agent skill。

### 闭源 / 生产线

**unnoo/***

前端 fork、后端 fork、App、研究 demo、beta 与内部工具。先确认任务和权限，再动手。

两个前端要分清：`slax-lab/slax-reader-web` 是公开基础版；`unnoo/slax_reader_frontend` 和 `frontend_beta` 是 fork + upstream layer，内部版本的增量主要在 fork 层，`upstream/` 是只读子模块。

## 从哪里开始

先做一条最短、可验证的链路，不要一上来读完 24 个仓库。

### 先读公开总览

打开 [slax-lab/slax-reader](https://github.com/slax-lab/slax-reader) 的 README，再读 [Web 开发文档](https://github.com/slax-lab/slax-reader-web/blob/main/public/DEVELOPMENT-DOCUMENT-EN.md)。它们说明产品边界和 monorepo 结构。

### 按任务选仓库

页面、交互、扩展 → `slax-reader-web`；接口、数据、AI、搜索 → `slax-reader-api`；移动端 → `slax-reader-client`；命令行 → `slax-reader-cli`；正文提取 → `readability` / `slax_readability`。

### 先跑一项检查

Web 先跑 `pnpm install` 和 `pnpm run test:dweb`；API 先跑 `pnpm install`、`pnpm test`；其他仓库按下方矩阵。

### 用一个小问题建立上下文

推荐从一个 `good first issue`、一个已有测试的 bug，或一处文档修正开始。改动范围小，能完整走一遍分支、检查、PR。

## 环境怎么搭

不要把所有仓库一次装完。按要改的层安装工具；密钥放在本地 env 文件或密码管理器里。

### slax-reader-web

要求 Node.js `^22.22.2` / `^24.15.0` / `>=26`，pnpm `>=9`。

```bash
cd ~/Github/reader/slax-lab/slax-reader-web
pnpm install
pnpm run dev:dweb
```

浏览器扩展用 `pnpm run dev:extensions`。内部 fork 还需要初始化 `upstream/` 子模块；其 README 的 `postinstall` 会自动处理。

### slax-reader-api

Node + pnpm + Wrangler + Prisma。本地 API 默认由 Wrangler 提供。

```bash
cd ~/Github/reader/slax-lab/slax-reader-api
pnpm install
pnpm init:pgsql
pnpm migration:local
pnpm dev
```

需要本地配置文件和服务凭证时，先看 `public/` 部署文档。

### slax-reader-client

Kotlin Multiplatform，目标是 Android / iOS / Desktop。入口在 `composeApp`，iOS 壳在 `iosApp`。

```bash
cd ~/Github/reader/slax-lab/slax-reader-client
./gradlew tasks
# 用 Android Studio / Xcode 选择目标运行
```

### slax-reader-cli

Node.js `>=18`。源码在 `src/`，构建用 tsup。

```bash
cd ~/Github/reader/slax-lab/slax-reader-cli
npm install
npm run typecheck
npm run build
```

### readability · jieba

Readability 是 Node + Mocha；jieba 相关仓库混合 Node、Rust、WASM。

```bash
cd ~/Github/reader/slax-lab/readability
npm install
npm test
npm run lint
```

### slax-home

Astro 站点。Node + pnpm，质量检查使用 Biome。

```bash
cd ~/Github/reader/slax-lab/slax-home
pnpm install
pnpm dev
```

环境变量原则：Web 通过 zod 校验 `PUBLIC_BASE_URL`、`DWEB_API_BASE_URL`、`COOKIE_*`、OAuth 和 Turnstile 等变量；API 还涉及 Cloudflare、数据库和 AI 服务。复制仓库里的 example，使用 `.env.*.local`，不要提交真实值。

## 如何提交代码

公开仓库走 GitHub fork + PR；闭源仓库先确认组织权限和目标仓库，不把内部代码带到公开仓库。

### 公开仓库

标准 PR 路径：

```bash
cd ~/Github/reader/slax-lab/slax-reader-web
git switch -c fix/short-description
# edit
git diff
git status
pnpm run lint
pnpm run test:dweb
git add path/to/files
git commit -m "🐛 fix short description"
git push -u origin fix/short-description
```

仓库指南要求从 fork 建分支，完成本地测试后发 PR。提交信息使用“emoji + 简短描述”，如需要关联 issue，再加 `emoji issue: #xxx`。

### 闭源仓库

内部变更路径：

```bash
cd ~/Github/reader/unnoo/slax_reader_frontend
git switch -c feat/short-description
# edit and test
git diff --check
git status
git add path/to/files
git commit -m "✨ add short description"
git push -u origin feat/short-description
```

先确认团队约定、review 人和部署影响。内部 fork 的 `upstream/` 是只读来源；公共能力优先回到公开仓库，再由 fork 同步。

PR 前自查：改动是否只属于一个仓库？是否有测试或可复现步骤？是否误提交 `.env`、密钥、构建产物？是否改变 API / 数据库迁移 / 客户端协议？若是，PR 描述里写清兼容性和回滚办法。公开 API 仓库的首个 PR 还会触发 CLA Assistant，未签署不能合并。

## 开发与测试矩阵

先执行与改动最接近的检查，再跑完整套件。命令来自各仓库当前的 package scripts / README。

### slax-lab/slax-reader-web

Node 22+ · pnpm 9+

- 开发：`pnpm run dev:dweb` / `pnpm run dev:extensions`
- 测试：`pnpm run test:dweb`；覆盖率：`pnpm run test:dweb:coverage`
- 质量：`pnpm run lint`、`pnpm run format:check`；内部 fork 再跑 `pnpm run audit:deps`

### slax-lab/slax-reader-api

Cloudflare Worker

- 开发：`pnpm dev`；类型：`pnpm types`
- 测试：`pnpm test`（Vitest）；质量：`pnpm lint`
- 数据库：先看迁移状态，再用 `pnpm migration:local`；不要直接碰线上数据

### slax-lab/slax-reader-client

KMP

- 结构：`composeApp/src/commonMain` 放共享代码；平台实现放 `androidMain` / `iosMain` / `jvmMain`
- 验证：用 Gradle task 列表和目标 IDE 编译；iOS 变更在 Xcode 检查
- 先确认本机 Android SDK、JDK、Xcode 与 CocoaPods 版本

### slax-lab/slax-reader-cli

Node 18+

- 开发：`npm run dev`（tsup watch）
- 检查：`npm run typecheck`；构建：`npm run build`
- 发布前会执行 `prepublishOnly` 构建

### slax-lab/readability / unnoo/slax_readability

- 测试：`npm test`（Mocha）；质量：`npm run lint`
- 新增解析规则时，优先加最小 HTML testcase，再改解析器

### slax-lab/slax-reader-web-bridge

Rollup + Jest

- 开发：`npm run dev`；构建：`npm run build`
- 测试：`npm run test`；类型：`npm run typecheck`

### slax-lab/slax-home

Astro

- 开发：`pnpm dev`；构建：`pnpm build`；预览：`pnpm preview`
- 质量：`pnpm lint`；完整检查：`pnpm check:all`

### unnoo/slax_jieba / unnoo/slax_jieba_rs

- 先读各自 README 和 `Cargo.toml`；构建链路包含 Cargo、WASM 和 bundler
- `slax_jieba` 的默认 `test` 目前会返回失败占位，不要把它当成通过标准

### unnoo/*

闭源

- 优先读取仓库自己的 README、AGENTS.md、CLAUDE.md 和 Makefile
- 后端 fork 的常用命令：`pnpm dev`、`pnpm test`、`pnpm lint`
- Go 服务有 Docker Compose；Flutter App 的 README 记录了 CocoaPods 更新方式

## 本地仓库索引

统一目录：`~/Github/reader/{slax-lab,unnoo}/<repo>`。同名项目用组织目录区分。

### slax-lab / public

先看这 8 个：`slax-reader` · `slax-reader-web` · `slax-reader-api` · `slax-reader-client` · `slax-reader-cli` · `readability` · `liveproxy-service-worker` · `slax-home`

[GitHub 总览](https://github.com/slax-lab/slax-reader) · [Web 开发文档](https://github.com/slax-lab/slax-reader-web/blob/main/public/DEVELOPMENT-DOCUMENT-EN.md) · [API 贡献指南](https://github.com/slax-lab/slax-reader-api/blob/main/public/HOW-TO-CONTRIBUTION-EN.md)

### unnoo / private

内部仓库：`SlaxReader` · `slax_reader_frontend` · `slax_reader_frontend_dev` · `slax_reader_frontend_beta` · `slax_reader_backend` · `slax_reader_client` · `slax_reader_app` · `slax_reader_golang_backend` · `slax-home-dev` · `slax-reader-design-prototypes` · `slax_reader_research_demos` · `readability` · `slax_readability` · `slax_jieba` · `slax_jieba_rs` · `AITools`

注意：索引中的闭源仓库清单以团队权限为准。贡献前确认 GitHub remote 指向正确组织，尤其是名字相近的 `slax-reader-web` / `slax_reader_frontend` 和 `readability`。

这页根据本地 `~/Github/reader` 在 2026-09-03 的 README、贡献指南、package scripts、Makefile 和项目结构整理。命令与环境会随仓库变化；动手前先看目标仓库最近的文档和 CI。
