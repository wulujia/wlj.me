# wlj.me SEO / GEO 改造进度

日期：2026-05-02

## 日志

- 读取用户提供的技术 SEO 和 GEO 最佳实践。
- 审计现有 Hugo 配置、模板、关于页、线上 robots / sitemap / 页面 HTML。
- 确认本次直接实施完整改造，并把规范写入 CHANGELOG、CLAUDE.md、AGENTS.md。
- 新增 robots、sitemap、llms、llms-full、JSON-LD、SEO head partial。
- 调整索引策略：notes、tags、categories、分页页 noindex 并排除出 sitemap。
- 更新文章页作者和更新时间显示，更新 publish.sh 自动写入 `author` 和 `lastmod`。
- 新增 CHANGELOG.md 和 AGENTS.md，扩展 CLAUDE.md。
- 验证 `hugo --destination /tmp/wlj-final-check` 成功，构建无 warning / error。
- 验证 `hugo --gc --minify --destination /tmp/wlj-final-minify` 成功，和 CI 构建方式一致。
- 验证 sitemap 共 1320 个 URL，notes/tags/categories 均为 0。
- 验证文章页 JSON-LD 可解析，包含 `Person`、`WebSite`、`BlogPosting`、`BreadcrumbList`。
- 验证构建产物中多 H1 页面数量为 0。
