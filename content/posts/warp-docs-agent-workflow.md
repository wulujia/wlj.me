---
title: "Warp 文档站的 agent 工作流"
date: 2026-05-10T21:05:01+08:00
lastmod: 2026-05-10T21:05:01+08:00
author: "Luca"
tags: ["AI","Docs","Tools"]
draft: false
slug: "warp-docs-agent-workflow"
---

Warp 是从终端起家的 AI 开发环境。2026 年 5 月，它把产品文档站 docs.warp.dev 的源代码开源了，仓库地址 [github.com/warpdotdev/docs](https://github.com/warpdotdev/docs)。这个仓库除了文档内容本身，还配了一整套用 AI agent 维护文档的工作流。

文档站基于 Astro 6 + Starlight，内容用 MDX 写在 `src/content/docs/` 下。Node.js 22 起步，`npm install` 后 `npm run dev` 启动本地预览，端口 4321。"Ask AI" 按钮和 "Was this helpful?" 反馈是可选功能，需要在 `.env` 里填公开值。

下面分四块说明仓库里 agent 相关的结构。

## `.agents/` 目录

[.agents/](https://github.com/warpdotdev/docs/tree/main/.agents) 分四个子目录：

- **`skills/`** — [25 个 skill](https://github.com/warpdotdev/docs/tree/main/.agents/skills)。每个 skill 是一个子目录，里面至少有一个 `SKILL.md` 描述用途和执行步骤，部分含有 `references/`、`scripts/`。
- **`rules/`** — 通用规则，当前只有一个 [`oz-style-guidelines.md`](https://github.com/warpdotdev/docs/blob/main/.agents/rules/oz-style-guidelines.md)。
- **`templates/`** — 不同类型文档页面的模板（quickstart、guide、procedural 等）。
- **`references/`** — 词汇表等参考资料。

25 个 skill 按用途分四类：

**草稿生成（10 个）**：`draft_quickstart`、`draft_guide`、`draft_procedural`、`draft_conceptual`、`draft_reference`、`draft_faq`、`draft_troubleshooting`、`draft_feature_doc`、`draft_docs`、`missing_docs`。从空白页起一篇新文档时使用。

**审查质检（5 个）**：[`review-docs-pr`](https://github.com/warpdotdev/docs/blob/main/.agents/skills/review-docs-pr/SKILL.md)、`style_lint`、`check_for_broken_links`、`docs-seo-audit`、`validate_ui_refs`。

**同步类（4 个）**：`sync-error-docs`、`sync-openapi-spec`、`sync_terminology`、[`update-changelog`](https://github.com/warpdotdev/docs/blob/main/.agents/skills/update-changelog/SKILL.md)。`update-changelog` 从 `channel_versions.json` 拉每周 release，按模板生成 changelog 条目并开 PR；要求生成内容与源数据一字不差。

**辅助类**：`answer_question`、`create_pr`、`afdocs-audit`、`afdocs-fix`。

## `AGENTS.md`

仓库根目录的 [`AGENTS.md`](https://github.com/warpdotdev/docs/blob/main/AGENTS.md) 是文档站的写作风格指南。文件分两段，前一段写作规范（Warp Documentation Style Guide），后一段仓库说明（Warp Docs Repository Guide）。

写作规范覆盖：

- Voice & tone：第二人称、动作导向、不堆行话
- Language：主动语态、消除模糊动词（may / might / should）、避免代词指代不清、避免修饰语堆叠、避免名词化
- Punctuation：强制 serial comma；指令性文本里不用 em dash
- Tense / Person：一般现在时；指令用 imperative；面向读者用第二人称
- Inclusive language：性别中立代词、避免 ableist 用词、不靠颜色单独传达信息
- 写给 agent 看（AEO）：描述性 header、明确上下文、frontmatter description 当成搜索摘要写、术语统一
- Content structure：必填 frontmatter description、sentence case headers、文件名 lowercase + 连字符
- Formatting：列表里 bold 关键词 + 破折号 + 解释；代码块必须带语言标识；图片 alt 描述具体内容；caption 不超过 10 词

这份文档既是写作者的规范，也是 `review-docs-pr` 评审 PR 时的参考依据。

## `.github/workflows/`

[三个 workflow](https://github.com/warpdotdev/docs/tree/main/.github/workflows)。

### [`ci.yml`](https://github.com/warpdotdev/docs/blob/main/.github/workflows/ci.yml)

触发：每个 PR 和 push 到 main。

步骤：checkout → 装 Node.js 22 + Python 3.12 → `npm ci` → `npm run typecheck` → `npm run build` → 调用 `.agents/skills/check_for_broken_links/check_links.py --internal-only` → `npm audit --omit=dev --audit-level=high`（暂用 `|| true` 不阻塞）。

### [`review-pr.yml`](https://github.com/warpdotdev/docs/blob/main/.github/workflows/review-pr.yml)

触发：PR opened 或 ready_for_review，且来源在同仓库内。

主步骤：调用 `warpdotdev/oz-agent-action@v1`，传入 `skill: review-docs-pr`。agent 跑完输出 `review.json`，结构如下：

```json
{
  "summary": "...",
  "comments": [
    { "path": "...", "line": 42, "side": "RIGHT", "body": "..." }
  ]
}
```

接下来一段 JavaScript（用 `actions/github-script@v7` 跑）做后处理：

1. 读 `review.json`，解析失败时清掉控制字符再试一次
2. 调 GitHub API 拉 PR 改动文件清单和 diff hunks
3. 解析每个文件的 diff，建出"哪些行号在 LEFT/RIGHT 侧出现"的集合
4. 遍历 agent 输出的 comments：路径正常化、丢弃路径不在 PR 内的、丢弃行号非法的、丢弃行号不在 diff 范围内的（这些不丢失，挪到 summary 末尾的 "Additional comments"）
5. 用 `pulls.createReview` 一次性提交 summary + inline comments

`review-docs-pr` skill 要求每条 comment 开头打严重度标签：🚨 [CRITICAL]、⚠️ [IMPORTANT]、💡 [SUGGESTION]、🧹 [NIT]，并尽量使用 GitHub Suggestion 语法让作者一键应用。

### [`respond-to-comment.yml`](https://github.com/warpdotdev/docs/blob/main/.github/workflows/respond-to-comment.yml)

触发：PR 评论或 review comment 内容里出现 `@oz-agent`。

主要步骤：

1. **权限校验**：用 `repos.getCollaboratorPermissionLevel` 检查评论作者，只允许 admin 或 write 权限的人触发
2. **加 👀 反应**：通过 reactions API 给评论加 `eyes`，告知用户已收到
3. **checkout PR**：`gh pr checkout`
4. **构造 prompt**：抓 PR 标题、描述、改动文件清单、评论内容、评论作者；如果是 review comment，再带上文件路径、行号、diff hunk
5. **跑 agent**：`warpdotdev/oz-agent-action@v1`，传入构造好的 prompt
6. **commit 改动**：以 `Oz Agent <agent@warp.dev>` 的身份 git add / commit / push（如果有改动）
7. **回复评论**：解析 agent 的 JSONL 输出，取最后一条 `type: agent` 的 `text`，作为 reply 贴回评论
8. **失败处理**：agent 步骤失败时，回复一条带 workflow logs 链接的错误提示

---

仓库链接汇总：

- 主仓库：[github.com/warpdotdev/docs](https://github.com/warpdotdev/docs)
- `.agents/`：[/.agents](https://github.com/warpdotdev/docs/tree/main/.agents)
- `AGENTS.md`：[/AGENTS.md](https://github.com/warpdotdev/docs/blob/main/AGENTS.md)
- `.github/workflows/`：[/.github/workflows](https://github.com/warpdotdev/docs/tree/main/.github/workflows)
