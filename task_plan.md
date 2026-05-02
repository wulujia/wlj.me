# wlj.me SEO / GEO 完整改造计划

日期：2026-05-02

## 目标

根据 `20260502-technical-seo-checklist.md` 和 `20260502-geo-best-practices.md`，把 wlj.me 从基础 Hugo 博客升级为可持续维护的 SEO / GEO 友好站点。

## 阶段

- [x] Phase 1: 读取现有配置、模板、文档和线上表现
- [x] Phase 2: 落地抓取、索引和 GEO 入口
- [x] Phase 3: 落地结构化数据、作者、时间戳和页面结构
- [x] Phase 4: 落地索引收敛、sitemap 收敛和内容质量保护
- [x] Phase 5: 写入 CHANGELOG、CLAUDE.md、AGENTS.md
- [x] Phase 6: 构建验证和输出结果

## 决策

- 站点是个人长期博客，不把每条短 note 都当作 SEO 页面。
- 核心文章、关于页、归档页保留索引；短 notes、tag/category/list pagination 等低价值页面默认 `noindex,follow`。
- GEO 不依赖人工维护静态清单，尽量让 Hugo 自动生成 `llms.txt` 和 `llms-full.txt`。

## 错误记录

| 时间 | 错误 | 处理 |
|---|---|---|
| 2026-05-02 | Google PageSpeed API 返回 429 quota exceeded | 不重复调用，保留为外部验证项 |
| 2026-05-02 | `llms.txt` 仍有少量 Hugo 实体转义 | 已改用 plain text 输出格式和显式 LLMS 模板；剩余实体来自 Hugo 内容摘要渲染，不影响抓取 |
