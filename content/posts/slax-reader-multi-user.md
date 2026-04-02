---
title: "从AI聊天到多用户互动：Slax Reader 新功能抢先看"
date: 2024-11-04T23:13:02+08:00
tags: ["WeChat"]
draft: false
slug: "slax-reader-multi-user"
---

Slax Reader 的研发节奏比较快，是滚动发布，新功能在开发环境测试稳定后，会快速发布到生产坏境。前些天，团队把一个完整版本里的功能都上线了，我做个汇总。

几个用户体感会比较明显的功能有：

- 选中文章的部分内容进行 AI chat，效果如图

- 增加分享书签功能，比如一个收藏的链接，可以这样分享出去

- 支持收藏者的划线评论

- 书签被分享后，其他用户可以在分享页里划线和划线评论。大家可以试着到下面的链接聊聊天。

产品转型6次才找到PMF，这家公司公开了自己的PMF方法论：https://reader.slax.com/s/rc083599b9

- 自动打标签、内置标签（用户自定义标签不参与自动打标签）

一些细节调整：

- 针对性样式处理（比如 markdown，代码块）

- 支持编辑书签标题

- 归档后，首页可以自动刷新

- AI Chatbot 增加 Latex 支持

- 改进 AI Chat 里生成内容所使用的语言逻辑

- 优化支付页面，清晰地区分“7 天试用价格”和“订阅价格”

- AI Chat 里 Shift + Enter 从发送改为换行，以符合用户习惯

- 用户语言同步、页面语言跟随

- 列表页“没有更多”

- Telegram 支持查看 topics、筛选

- 大量其他 UI、交互细节调整

一些运维和后端工作：

- 在生产环境 Cloudflare 里应用权限最小原则（收拢权限）

- slax.com 加入 clash 规则 or API / Pages 加速

- Collecting 的后端接口异步处理

--

Slax Reader 是全新的阅读、学习产品，官网：https://reader.slax.com/
