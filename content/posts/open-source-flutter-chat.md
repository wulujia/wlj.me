---
title: "开源超轻量的 Flutter 聊天库"
date: 2025-02-26T22:46:45+08:00
tags: ["WeChat"]
draft: false
slug: "open-source-flutter-chat"
---

这两年，大量 AI ChatBot 涌现。不少人在用 Flutter 做跨平台应用时，想加个简单的 AI 聊天，却被一堆 IM 方案搞得头大——我们就是这样。所以同事做了一个超轻量的 Flutter 库：simple_chat。它能让你几行代码就把聊天界面跑起来，通吃 iOS、Android、Web。之所以叫 simple，是因为它真的是主打简洁。你不用拉一大堆依赖或后端配置，几分钟就能搞定。UI 也很好改，如果想要自己定制聊天气泡、字体、颜色，分分钟就能上手。有人会问，能用它干什么？常见的 IM、客服、AI 聊天机器人都能用得上，毕竟它支持消息发送状态、群聊、未读消息指示，还能直接选图、预览图片，算是“麻雀虽小，五脏俱全”。如果你对那些大而全的 Stream、Sendbird 没什么兴趣，只想要个纯前端的简洁方案，simple_chat 或许就是你想要的。同事 Lawrence 还在不断迭代这个项目，未来计划支持更多自定义选项、多媒体消息、实时打字状态等功能。项目开源，如果你也想帮忙或者提想法，不妨去看看：- GitHub https://github.com/Tealseed-Lab/simple_chat- pub.dev https://pub.dev/packages/simple_chatsimple_chat 能让 Flutter 开发者省去很多麻烦，专注业务逻辑，而不是陷在复杂的聊天框架里。再上一个 simple_chat 的小应用案例：EatVenture——觅食历险产品，里面嵌了 simple_chat，如图：我用 EatVenture 解决俩问题：1. 在海外找餐馆2. 在餐厅看不懂菜单拍一下识图推荐EatVenture 更多信息：https://tealseed.com/eatventure/。
