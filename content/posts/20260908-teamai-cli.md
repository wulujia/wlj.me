---
title: "TeamAI：给 AI 编程工具加一层团队协作"
date: 2026-09-08T12:36:25+08:00
lastmod: 2026-09-08T12:36:25+08:00
author: "Luca"
tags: ["AI","Tools","Team"]
draft: false
slug: "20260908-teamai-cli"
---

TeamAI 是腾讯开源的命令行工具。它把 Claude Code、Cursor、Codex、CodeBuddy 等 Agent 的 skills、rules、hooks、MCP 和团队知识放进一个共享 Git 仓库，通过评审后同步到成员本机。

资料日期：2026-09-08。功能与命令来自项目文档；Stars、Forks、Issue 数量是当天快照，未实际安装验证。

| 协议 | 快照 | 版本 | 技术栈 |
| --- | --- | --- | --- |
| MIT | 约 1.7k Stars、121 Forks | 0.22.0 | TypeScript / Node.js |

## 它解决什么问题

个人 Agent 已经能做很多事，但一次踩坑、一个有效的 skill，常常只留在某个人的电脑上。不同工具的配置路径不一致，MCP 和 hooks 也难统一管理。

TeamAI 把这层团队工作方式放进 Git：团队维护 Harness（skills、rules、agents、hooks、MCP、env 等）和 learnings；成员通过 `pull` 获取更新；新增内容经 Merge Request 评审后再分发。它也会收集摩擦信号，支持回顾、周报和看板。

它不提供模型推理，也不是 Cursor、Claude Code 或 Codex 的替代品。它运行在这些工具旁边。

## 三层能力

| 层 | 要解决的问题 | 命令或功能 |
| --- | --- | --- |
| Team Execution | 让每个 Agent 使用团队约定 | `init`、`pull`、`push`；skills、rules、agents、hooks、MCP、env、packages |
| Team Context | 让 Agent 理解团队背景 | recall、learnings、代码库图谱、teamwiki、`culture.md` |
| Team Improvement | 把执行中的经验带回团队 | 摩擦信号、session save、digest、dashboard、KB Health |

分发与管理还包括 Roles、Tags、Sources、Packages 和 skill exclude。

知识库部分，Stop hook 会按摩擦评分提示分享 learnings；`teamai recall` 使用 BM25 和图谱，默认关闭；`teamai import` 用 AST 和规则建立图谱。Claude、Codex、Cursor、CodeBuddy、Qoder 的支持较完整，缺少 hook 的工具需要手动 `pull`。

## 工作方式

```text
teamai push -> Merge Request -> merge
SessionStart hook -> teamai pull -> 本地 AI 工具
```

初始化时完成 OAuth、关联仓库和 hooks 注入。成员在分支上提交，评审者合并；新 session 启动后，SessionStart hook 自动同步团队配置。

默认是 project scope，也可用 `--scope user`。单仓模式用 `teamai init .`；HTTP 只读模式用 `teamai init --http`。

## 安装与上手

前置条件是 Node.js 18 或更高版本以及 Git。TGit 需另装 `gf`，CNB 需另装 `cnb`。

公开 README 的安装方式：

```bash
npm install -g teamai-cli
teamai --version
```

腾讯内网文档使用另一个包名和 registry：

```bash
npm install -g @tencent/teamai-cli --registry=http://r.tnpm.oa.com
```

公开环境以 README 的 `teamai-cli` 为准。

```bash
# 默认：项目范围
cd /path/to/my-project
teamai init https://github.com/yourorg/yourrepo

# 用户范围
teamai init https://github.com/yourorg/yourrepo --scope user

# 单仓模式
teamai init .
teamai init . --agent claude,codex

teamai pull
teamai push
teamai status
teamai doctor
teamai recall enable
teamai recall "port conflict"
teamai digest
teamai dashboard
teamai uninstall --dry-run
```

## 适用范围

适合已经使用 Claude Code、Cursor、Codex 或 CodeBuddy，需要统一 skills、rules、MCP 的团队；也适合想经 MR 评审后再发布团队规范、把 session 经验做成可检索知识，或在 TGit、CNB、私有 Git 和多业务仓之间共享规范的团队。

单人随手使用、无意维护团队仓库时，维护成本未必划算。它也不会让模型本身变强。对 hooks 或本机配置改动有严格限制的环境，需要先评估。

## 和相近工具的边界

| 对象 | 关系 |
| --- | --- |
| Claude Code / Cursor / Codex | TeamAI 的目标运行时 |
| CodeBuddy / WorkBuddy | 腾讯生态 Agent，适配较深 |
| 手工同步 skills | TeamAI 增加 MR、角色和标签、SessionStart 自动同步 |
| 通用 RAG / 知识库 SaaS | recall 是 Git 仓内的 BM25 和图谱，不是托管向量库 |
| teamai-hub | 模板组织，可从模板仓初始化 |

上表按产品文档描述的边界整理，没有官方竞品对比页。

## 成熟度快照

| 指标 | 2026-09-08 的观测 |
| --- | --- |
| License | MIT（Tencent 2026） |
| Stars / Forks | 约 1.7k / 121 |
| Open issues | 约 19 |
| 版本 | `teamai-cli` 0.22.0 |
| 技术栈 | TypeScript ESM、tsup、vitest |
| 维护 | 项目 2026 年 3 月开始维护，当天有 commit |
| 版本记录 | 已标记的版本约为 0.14.x，与发布包 0.22.0 不一致 |

## 风险与注意事项

- **MCP 密钥：**`${VAR}` 会解析成明文并写入工具配置（权限为 0600）。项目级 MCP 文件必须加入 `.gitignore`。
- **Hooks：**团队 `hooks.yaml` 可以分发命令。用 `autoApply`、`requireTeamScripts`、`TEAMAI_HOOKS_DISABLED` 管理执行范围。
- **网络：**依赖 Git 托管服务；TGit、CNB 需要额外 CLI；内网 tnpm 无法在外网使用。
- **隐私：**digest 和 dashboard 以计数为主，sessions 和 stats 仍会进入团队仓库。
- **本机改动：**会修改 AI 工具 settings，也会修改 shell profile。卸载前可先运行 `teamai uninstall --dry-run`。
- **Codex：**写入 hooks 后需要手动信任。
- **自动更新：**Stop hook 可以更新 CLI，可用 `autoUpdate` 和 `updatePolicy` 控制。

## 资料与局限

- [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli)
- [README 中文版](https://github.com/Tencent/teamai-cli/blob/main/README.zh-CN.md)
- [使用指南](https://github.com/Tencent/teamai-cli/blob/main/docs/usage-guide.zh-CN.md)
- [CHANGELOG](https://github.com/Tencent/teamai-cli/blob/main/CHANGELOG.md)
- [npm：teamai-cli](https://www.npmjs.com/package/teamai-cli)
- [teamai-hub 模板](https://github.com/teamai-hub)

定位、三层架构、安装命令、主要命令、MCP、hooks、recall、MIT、公开包名、0.22.0 版本和 Agent 支持矩阵均以文档为依据。Stars、Forks 和 Issue 数量来自 Shields 快照；GitHub API 当时限流，Releases 页面超时，未取得月下载量，也没有实际安装测试。
