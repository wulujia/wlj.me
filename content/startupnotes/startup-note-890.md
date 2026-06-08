---
title: "创业笔记 890：Claude Skills 学习"
date: 2025-12-11T08:08:25+08:00
lastmod: 2025-12-11T08:08:25+08:00
author: "Luca"
tags: ["Startup"]
draft: false
slug: "startup-note-890"
summary: "先看官方文档： https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills https://platform.cla"
paywall: true
---

先看官方文档：
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- https://www.claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples
- https://code.claude.com/docs/en/plugin-marketplaces

## Skills 是什么

Claude Skills 是由指令、脚本和资源组成的有序文件夹，Agent 可以动态发现并加载这些文件夹，从而更好地完成特定任务。Skills 通过将您的专业知识打包成可组合的资源供 Claude 使用，扩展了 Claude 的功能，将通用 Agent 转变为满足您需求的专用 Agent。

Skills 运行在一个代码执行环境中，Claude 在该环境中拥有文件系统访问权限、bash 命令使用权限和代码执行权限。就像虚拟机上的目录，Claude 使用与在计算机上浏览文件相同的 bash 命令与它们进行交互。

简单来说，Skills 就是一个包含 SKILL.md 文件的目录。
1. 以 YAML 前置元数据开头，其中包含一些必需的元数据： name 和 description 。启动时，代理会将每个已安装技能的 name 和 description 预加载到其系统提示符中。
2. Markdown 写的详细信息。
3. 可以引用其他文件，引入更长的上下文。
4. 可以包含脚本——由于代码是确定性的，工作流程具有一致性和可重复性。
