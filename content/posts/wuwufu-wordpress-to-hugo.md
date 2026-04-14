---
title: "把父亲的 WordPress.com 博客迁到 Hugo + Cloudflare Pages"
date: 2026-04-14T20:44:10+0800
tags: ["Hugo", "Cloudflare", "WordPress"]
draft: false
slug: "wuwufu-wordpress-to-hugo"
---

父亲从 2005 年开始在 WordPress.com 写博客，到 2025 年一共 786 篇文章、591 条评论、78 段视频。这几天把它整站搬到了 Hugo + Cloudflare Pages，托管在 [wuwufu.com](https://wuwufu.com)。

记录一下工具链和几个要留意的地方。

## 整体方案

- 内容：wp2hugo 从 WordPress 导出的 WXR XML 转 Markdown
- 主题：PaperMod，自定义布局模仿原站 Twenty Seventeen 的头图风格
- 评论：REST API 抓回来，生成静态 HTML 嵌入每篇文章末尾
- 视频：ffmpeg x265 2-pass 压缩，从 10.1GB 压到 587MB
- 托管：Cloudflare Pages，DNS 也搬到 Cloudflare

## 内容转换：wp2hugo

WordPress 后台导出 WXR XML（Tools → Export），然后跑 [wp2hugo](https://github.com/ashishb/wp2hugo)，出来就是 Hugo 友好的目录结构：`content/posts/*.md` + `static/wp-content/uploads/`。

转换后 Markdown 里会有一些残留的 WordPress shortcode（`[gallery]`、`[embed]` 这些），还有空标题、重复文章，写了几个清理脚本扫一遍。

## 评论：自己抓，嵌进去

WordPress.com 因为不是自托管，用不了评论迁移插件。但 20 年下来 591 条评论不能丢。

好在 WordPress.com 开放了 REST API，按文章 ID 翻页抓：

```
https://public-api.wordpress.com/wp/v2/sites/<site-id>/comments?post=<id>
```

抓回来之后生成两份东西：

1. 每篇文章末尾追加一块静态 HTML，显示原评论（头像、昵称、时间、内容）
2. 一个 `/comments/` 汇总页，按时间倒序列出所有评论和出处文章

全部是构建时生成的静态内容，不依赖任何运行时服务。搬到 Hugo 之后新评论功能关掉——这本来就是一个归档站。

## 视频：压到 25MB 以下

**Cloudflare Pages 单文件 25MB 上限**，这是部署到一半才发现的硬约束。父亲拍的 78 段 MP4 原文件大多 100-300MB，总共 10.1GB。

处理流程：

1. 去重：相同哈希的文件只留一份
2. 分析：ffprobe 扫一遍，记下分辨率、码率、时长
3. 压缩：ffmpeg x265 2-pass，按时长反推目标码率——保证压完能进 25MB
4. 补压：第一轮之后还有几个超限的，用更低 CRF 再压一遍
5. 核验：最后扫一遍，确认文件全在限制内、能正常播放

最终 587 MB，全部通过。x265 相比原来的 H.264 省了一个数量级的空间，画质肉眼看没差。

## 分类补全

WordPress 里有 61 篇没分类的文章。写了个脚本按标题关键词归到 11 个既有分类里，人工校对一遍。

## 部署：Cloudflare Pages

和我自己博客一样的套路：

- Framework preset：Hugo
- Build command：`hugo --gc --minify`
- Output directory：`public`
- 环境变量：`HUGO_VERSION=0.155.1`（内置的太旧，不设会挂）

DNS 搬到 Cloudflare 托管，SSL 自动签。

## 几个要留意的点

- **Cloudflare Pages 单文件 25MB、整站 20000 文件上限。** 有视频的站尤其要提前盘算，要么压，要么放 R2/对象存储然后只在站里引用。
- **保留 WordPress 原来的 `/wp-content/uploads/` 路径。** 不要图好看改成 `/images/` 之类的新路径——老链接（搜索引擎收录的、别处引用的）会全部失效。
- **WordPress.com 的评论没有插件迁移路径**，REST API 是唯一选择。做成静态嵌入最省事：永远不会挂，也不用运维。
- **HUGO_VERSION 环境变量必须设。** Cloudflare 内置的 Hugo 版本偏旧，新主题会因为语法不兼容直接构建失败。
- **检查 front matter 的 `date` 字段**。wp2hugo 转出来的时区如果有偏差，会有文章落到"未来时间"，Hugo 默认不发布未来时间的内容，结果就是"丢文章"。

20 年的内容现在不再挂在 WordPress.com 上了，不再按年付费，只要 GitHub 仓库和 Cloudflare 账号在，站就一直在。
