# wlj.me

Hugo 博客，GitHub Pages 托管，Terminal 主题。

## 写文章前必读（强制）

下笔前必须先读 `~/Dropbox/context/core/WRITING.md`，按里面的规则写。特别是：

- 只写用户交代过的事实。没发生的过程别编，没说过的感受别加
- 不做价值评估。用户没评的好坏、意义、聪明、适合谁，一律不写
- 不写"为什么这个方案聪明 / 本质上是 / 核心想法"这类提炼升华
- 不加对比（Remotion vs Slidev、和传统剪辑比）除非用户说过
- 不补充实现细节（缓存策略、具体选型建议）除非用户说过

写完自检一遍：每一段有没有用户没给的信息？有就删。

## 禁止直接写入 content 目录（强制）

不要用 Write 或 Edit 在 content/posts/ 或 content/notes/ 下创建文件，也不要手写 frontmatter。日期、frontmatter 由 publish.sh 自动生成，手动填写必然出错。

典型事故：手填 `date` 时间比 build 时间晚（比如 build 在 07:43，date 写成 10:30），Hugo 默认不发布未来时间的文章，文章不会出现在网站上。这种问题排查起来很费时间。

唯一允许的人为路径：通过 publish.sh，按下面流程走。

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
