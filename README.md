# wlj.me

Luca 的个人博客，基于 [Hugo](https://gohugo.io/) 构建，使用 [terminal](https://github.com/panr/hugo-theme-terminal) 主题，通过 GitHub Actions 自动部署到 GitHub Pages。

网站地址：https://wlj.me/

## 目录结构

```
content/
├── posts/       # 博客文章（约 1280 篇）
├── notes/       # 笔记（约 800 条）
├── about/       # 关于页面
└── archives.md  # 归档页面
```

## 发布文章

在 `content/posts/` 下新建 `.md` 文件：

```markdown
---
title: "文章标题"
date: 2026-04-06T10:00:00+08:00
tags: ["Life"]
draft: false
slug: "url-slug"
---

正文内容
```

## 发布笔记

在 `content/notes/` 下新建 `.md` 文件：

```markdown
---
title: "笔记标题"
date: 2026-04-06T10:00:00+08:00
tags: ["Note"]
draft: false
slug: "note-slug"
---

笔记内容
```

## 从 zsxq 导入笔记后

zsxq 导出的 markdown 含 `<e type="web" .../>` 等自闭合自定义标签，
HTML5 解析器会把它们当成开标签，吞掉后续所有内容，导致笔记渲染为空。
每次拉新内容后跑一遍清理脚本：

```bash
./scripts/clean_zsxq.py content/notes/
```

可加 `--dry-run` 先预览。脚本幂等，重复跑不会出问题。

## 部署

```bash
git add .
git commit -m "新增内容"
git push
```

推送后 GitHub Actions 自动构建部署，约 35 秒上线。

## 注意事项

- `date` 不要设成未来时间，否则 Hugo 不会渲染
- `draft: true` 为草稿，不会发布
- `slug` 决定文章 URL，建议用英文短横线连接
- 常用 tags：Life、Tech、AI、Reading、Startup、Writing、Security、Tools、Photography
