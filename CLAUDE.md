# wlj.me

Hugo 博客，GitHub Pages 托管，Terminal 主题。

## 禁止直接写入 content 目录

不要用 Write 或 Edit 在 content/posts/ 或 content/notes/ 下创建文件。日期、frontmatter 由发布工具自动生成，手动填写必然出错。

## 发布文章（posts）

必须通过 publish.sh 发布，流程：

1. 在 /tmp/ 下创建临时 md 文件，文件名为英文 kebab-case（这就是 slug）
2. 文件内容：第一行 `# 标题`，空一行，正文。不写 frontmatter
3. 运行 `./publish.sh /tmp/slug-name.md tag1,tag2`

publish.sh 自动处理：date（取当前时间）、slug（取文件名）、frontmatter、git commit、git push。

规则：
- slug 必须是英文 kebab-case，中文 slug 经 URL encode 后会 404
- tags 必须用英文，优先复用现有标签

## 笔记（notes）

notes 通过 social-poster bot 的 wlj 平台发布，不在 Claude Code 的职责范围内。
