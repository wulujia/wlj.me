# wlj.me

Hugo 博客，GitHub Pages 托管，Terminal 主题。

## 发布文章

- date 字段必须先跑 `date '+%Y-%m-%dT%H:%M:%S%z'` 取当前时间，直接使用，不能手动填。Hugo 不发布未来时间的文章。
- slug 必须是英文（kebab-case），不要用中文。中文 slug 经 URL encode 后会 404。
- 发布脚本：`./publish.sh input.md [tag1,tag2,...]`
- publish.sh 从输入文件名取 slug，所以**输入 md 文件名必须是英文**（例如 `ai-writing-workflow.md`，不是 `AI写文章.md`）。
