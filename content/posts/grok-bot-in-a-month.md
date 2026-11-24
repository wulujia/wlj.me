---
title: "[翻译]几个人一个月做出 Grok Bot"
date: 2026-09-12T10:05:28+08:00
tags: ["WeChat", "AI", "Translation"]
draft: false
slug: "grok-bot-in-a-month"
---

- 节目：Lenny’s Podcast

- 链接：https://www.lennysnewsletter.com/p/how-we-built-grok-bot-in-a-month

- 嘉宾：Roman Ugarte，Grok Bot 产品负责人，早期加入 Cursor

- 时长：约 1:22:43

- 发布：2026-09-08

- 主题：Grok Bot 如何在一个月内从零做出；AI Agent 应该是什么产品形态；为什么要给 Agent 自己的电脑；如何做产品、组织、增长与 moat。

Roman 对 Grok Bot 的最终愿景非常简单：\*\*每个人都应该拥有一支 AI bot 团队，既帮你工作，也帮你处理生活。\*\*

他认为 Grok Bot 真正改变的并不是模型，而是人与 AI 的关系。今天大部分产品仍然是：

> 人打开一个 AI → 创建一次对话 → 给任务 → 看过程 → 检查结果 → 修改 → 再继续。

Grok Bot 想把它变成：

\*\*“这是一个有自己电脑的同事。我把事情交给它，然后去做别的事。”\*\*

这条主线贯穿整个对谈。

---

## 1. Grok Bot 是怎么开始的：真的从一张白纸开始

### 04:03–08:40

Lenny 问 Grok Bot 最初是怎么来的。

Roman 说，他们很早就意识到 Cursor 在 developer / engineer 场景积累了大量关于 Agent 的经验，但一直有一个问题：

\*\*如果不是 coding，而是普通 knowledge work，一个真正好的 Agent 产品应该是什么样？\*\*

他们没有从 Cursor 里抽一个模块慢慢改，而是建立了一个非常小的内部团队。

只有几个人。

团队被有意地从公司其他部分隔离出去：

- 坐在办公室单独的一块区域；

- 使用 private Slack channels；

- 几乎把自己关进“洞穴”；

- 目标只有一个：做一个面向知识工作的 Agent 产品。

从第一行代码到内部可用版本，大约只用了 \*\*一个月\*\*。

Roman 特别强调，小团队不是偶然。

这个产品每天都要做大量没有先例的“小决定”。如果一开始就几十个人参与，大家不断讨论未来 6～12 个月路线、组织协调、跨团队需求，他们根本不可能一个月做到这个状态。

他的判断是：

\*\*这种探索期需要少数人每天连续做上百个 judgment calls。\*\*

产品做出来以后，他们在 SpaceXAI 内部的 all-hands 上发布。

这里出现了真正让团队确信产品有价值的信号。

内部开发 Grok Bot 的人喜欢它并不能说明什么。开发者天然知道产品怎么用，也知道哪里可以绕过去。

真正的测试是其他员工。

结果发布后的一周内，很多原来每天使用 ChatGPT 或其他聊天式 AI 的员工，开始把大量日常 Agent 工作迁到 Grok Bot。

尤其包括那些并不是开发人员的团队。

Roman 说，这时他们才觉得：

\*\*这不是团队自嗨，它可能真的成立。\*\*

随后整个团队立刻进入“把它发布给全世界”的状态。

---

# 2. 为什么没有把它直接塞进 Cursor

### 08:40–11:18

这是对谈里很重要的一段。

OpenAI、Anthropic 等公司的路径很自然：

coding agent 很强

→ 发现也能做 knowledge work

→ 在现有产品里加新的模式、tab、入口。

Lenny 问 Roman：

为什么不直接给 Cursor 加一个 knowledge-work 模式？

Roman 说，这个决定\*\*一点都不 obvious\*\*，内部讨论了很多次。

Cursor 本身当然也能处理非编程工作，而且 coding agent 在很多普通任务上已经非常强。

问题是产品历史会留下很多东西：

- Cursor 的品牌首先让人想到 coding；

- UI 对非技术用户可能有压力；

- 原有产品的各种设计假设都是围绕 programmer；

- 新功能不断通过新的 tabs、modes、panels 加进去。

Roman 用了一个很有意思的概念：

\*\*shipping your org chart。\*\*

公司内部可能有三支团队、三个产品方向，于是 UI 里正好出现三个 tab。

从组织角度很合理。

用户看到的却是：

“为什么我要理解你公司内部有三个东西？”

最后呈现出来的其实是三个产品哲学被硬塞进同一个窗口。

Grok Bot 团队于是决定：

\*\*重新开始。\*\*

这样他们可以控制每一个 pixel，并围绕“knowledge worker 如何与 AI 同事合作”建立一套完整、一致的产品逻辑。

Roman 并不认为“独立产品”永远是正确答案。他甚至提到 Codex 后来采取了相反方向，把更多东西合并起来。

他的观点只是：

\*\*对于 Grok Bot，当时从零开始给了团队巨大的自由。\*\*

他们不用尊重旧产品里的任何假设。

---

# 3. 为什么亲自 onboarding 200～300 个用户

### 11:18–18:41

正式发布前，核心团队大约花了两周时间，亲自 onboarding 了 \*\*200～300 人\*\*。

每个人大概 20 分钟。

Roman 说最早几场其实“相当痛苦”。

比如：

- cloud computer 起不来；

- 用户卡在 onboarding；

- 用户根本不知道下一步怎么办；

- 某个团队以为显而易见的设计，用户完全看不懂。

核心开发者自己坐在那里看一个真人困惑 20 分钟，会产生一种 dashboard 给不了你的压力：

\*\*“这个东西明天必须修掉，因为明天我还要亲自给另一个用户做 onboarding。”\*\*

这种反馈周期非常短。

今天发现问题，明天就要修。

这也是 Roman 认为人工 onboarding 特别有价值的原因之一。

## 一个自然出现的模式：Chief of Staff

内部使用一两周后，人们开始创建 5～10 个 bot。

不同 bot 分别负责：

- 某个领域；

- 某类任务；

- 某条工作线。

随后出现了一个团队完全没有设计出来的行为。

一些员工开始挑出表现最好的 bot，把它“晋升”为：

\*\*Chief of Staff。\*\*

以后用户主要和这个 Chief of Staff 说话。

Chief of Staff 再：

- 分发任务给其他 bots；

- 跟踪工作；

- 汇总结果；

- 管理整个 bot 团队。

甚至有人正式告诉 bot：

“你被升职了。”

bot 还会问：

“那我涨薪了吗？”

“我的 token budget 会增加吗？”

有趣归有趣，Roman 真正关心的是：

\*\*这是内部文化导致的特殊玩法，还是人类面对一组 AI Agent 后自然会形成的组织方式？\*\*

所以做外部 onboarding 时，他们刻意没有告诉用户应该建立 Chief of Staff。

Roman 的原话意思是，他们不想 \*\*lead the witness\*\*，不想诱导实验结果。

结果不少外部用户也自然发展出了类似结构。

这才让团队更有信心，在产品里稍微鼓励这种模式。

但他们仍不希望把它设计成唯一正确的工作方式。

---

# 4. 用户到底需要看到 Agent 的多少内部过程

### 14:30–16:17

Grok Bot 和很多 Agent 产品一个明显区别是：

\*\*它刻意不给用户看太多。\*\*

传统 Agent 产品喜欢显示：

- reasoning；

- chain of thought；

- tool calls；

- browser clicks；

- 当前正在调用什么工具；

- memory；

- 每一步执行过程。

Roman 认为这里可能搞反了。

如果你把任务交给一个真人同事，你一般不会要求：

“每隔两秒告诉我你点了什么按钮。”

“现在打开了什么网页？”

“你的每一步思考是什么？”

那会非常烦。

所以 Grok Bot 的设计更接近 Slack：

你发给 bot 一件事情。

它开始工作。

你看到：

- typing indicator；

- active 状态；

- 必要的时候，它主动给一些 progress update。

但不会看到它每一次 tool call、每一个 click、完整 reasoning stream。

Roman 并不是说用户完全不需要可见性。

早期用户确实提出：

- 我希望看到 bot 大概有哪些待办；

- 我想知道它怎么排 priority；

- 我想知道它现在大概在处理什么。

团队认为这些反馈合理。

但几乎没人真的想看长长的 chain-of-thought 和 tool-call log。

这加强了他们的判断：

\*\*Agent 的内部机制应该越来越被抽象掉。\*\*

你管理的是工作，而不是管理 AI 如何移动鼠标。

---

# 5. 为什么早期用户不能只找 Silicon Valley AI 圈的人

### 16:17–18:41

200～300 个 early users 并不只是所谓 influencers 和 AI power users。

Lenny 自己属于这一类，因为他用过很多 AI 产品，能够快速比较。

但 Grok Bot 团队还故意寻找一些他们平常完全接触不到的人。

Roman 举了一个例子：

\*\*一个咖啡店老板。\*\*

他是公司的朋友的朋友。

有人给他演示了一下 Grok Bot，他变成了非常重度的用户，而且后来成了特别有价值的 bug / feature feedback 来源。

原因很简单。

一个经营咖啡馆的人遇到的问题可能是：

- Shopify integration 某一步不稳定；

- 商品 copy 写得不符合实际需求；

- 小企业运营中的某个流程很别扭。

这些问题，SpaceXAI 自己 dogfood 一辈子也不一定遇得到。

Roman 认为公司存在明显的：

\*\*Silicon Valley AI bubble。\*\*

这个 bubble 有价值，因为里面的人会推动 frontier。

但如果 Grok Bot 真想成为 mainstream user 和普通公司的工作方式，就必须主动逃出这个 bubble。

他甚至认为这种 Agent 对 non-developer 可能比 developer 更重要。

---

# 6. 内测到发布的三周：他们主要做的是“删东西”

### 18:41–21:48

时间线是：

- 约 1 个月：第一行代码 → internal beta；

- 约 3 周：internal beta → public launch；

- 录制节目时：public launch 也才约 3 周。

Lenny 问：

这三周里产品变化最大在哪里？

Roman 的第一个回答是：

\*\*We unshipped a lot.\*\*

早期版本里有大量实验性功能。

尤其因为开发团队自己需要 debug，他们把很多内部东西直接做进了产品：

- model thinking；

- stored memories；

- developer-like observability；

- 各种内部状态。

发布前他们开始猛烈删除。

把：

\*\*开发者为了 debug 想看到的东西\*\*

和：

\*\*用户完成任务真正需要看到的东西\*\*

彻底分开。

Roman 认为未来甚至还要继续删。

目标是：

> ruthlessly simplify the product.

另一个主要工作不是加“大 feature”，而是：

\*\*make it just work。\*\*

用户真正想要的其实很朴素：

“这是我的任务。”

然后 AI 去做。

回来时：

- 要么事情已经完成；

- 要么给用户一个可以判断和继续 steering 的结果。

为了做到这一点，团队真正投入时间的是一些后台很不起眼的问题：

- 鼠标能不能准确点击；

- 网站能不能成功登录；

- 浏览器状态能不能正确理解；

- 遇到某个 UI 能不能继续向下跑。

一个功能列表根本体现不了这些东西。

但 Agent 在这里失败一次，整个任务就断了。

---

# 7. Sales 为什么成了 Grok Bot 最疯狂的用户之一

### 21:48–23:45

内部 sales / GTM 团队很快变成非常重度的 Grok Bot 用户。

原因恰恰是他们每天使用的大量企业软件：

\*\*没有好 API，也没有好 MCP。\*\*

传统 AI 工具执行到这里就卡住。

但 Grok Bot 有电脑。

所以可以像真正员工一样：

- 打开 Salesforce；

- 看 dashboard；

- 点击网页；

- 输入；

- 继续完成 workflow。

这暴露了很多底层问题。

比如某个 Salesforce 页面上的控件，Agent 鼠标控制不够精确，就是点不到。

于是核心团队可以拿到极具体的问题：

“Agent 缺少哪一种 screen / browser understanding，使这个真实任务无法完成？”

Roman 很喜欢这种反馈。

因为相比 benchmark 从 73.2 上升到 74.1，它意味着：

\*\*昨天还完全无法完成的一整块真实工作，今天突然能做了。\*\*

而且他们能立刻看到反馈。

修完以后，sales 团队第二天就开始疯狂感谢他们：

“之前连续失败七天的 workflow 终于跑通了。”

Roman 认为 Agent 的进步很大程度就是不断：

\*\*找到下一块尚未解锁的工作 → 解锁它。\*\*

---

# 8. Recruiting 的案例：AI 不只是筛简历

### 23:45–27:00

招聘团队同样是早期重度用户。

Roman 先解释 SpaceXAI 的招聘哲学：

一个人是否正在找工作，不应该成为是否招聘他的前提。

他们更喜欢反过来：

1. 公司目前最大的业务问题是什么？

2. 全世界谁最适合解决它？

3. 找到这些人。

4. 想尽办法接触他们、说服他们加入。

如果你采用这种招聘方法，“AI 帮我读 500 份 résumé 然后排序”的价值其实很有限。

真正有价值的是：

\*\*在整个可能的人才宇宙中主动找人。\*\*

Roman 给出一个具体的 workflow。

假设某个领域最新人才出现在学术会议里，而且论文甚至没有 Google Scholar 页面，只存在 conference website。

Bot 可以每天：

- 去会议网站；

- 下载新的 PDF；

- 提取新论文作者；

- 和已经追踪过的名字去重；

- 把新名字加入 spreadsheet；

- 调查每个人；

- 查看 SpaceXAI 内部谁跟这个人认识；

- 如果有联系，就主动发 Slack 请求 introduction。

然后第二天继续。

过去这是极其手工的 sourcing 工作。

Roman 认为这种持续、重复、大范围的信息搜索其实非常适合 AI。

招聘人员自己于是可以把时间花在：

\*\*和最优秀的人建立关系、说服他们加入。\*\*

而不是拉 list。

---

# 9. 一个很重要的产品语言变化：

# “Grok Bot now has…” → “Grok Bot can now…”

### 27:49–30:20

Roman 说他们内部会问：

\*\*如果这个东西发布，我们的 launch tweet 是什么？\*\*

如果连一条有吸引力的发布内容都写不出来，也许根本不应该做。

但还有一个更重要的语言变化。

传统软件公司描述 feature：

> Grok Bot now has …

后面通常接：

- 一个新 button；

- 一个新 dropdown；

- 一个新 panel；

- 一个新的 integration。

Roman 希望团队改成：

> Grok Bot can now …

也就是：

\*\*Grok Bot 现在能够做什么？\*\*

这强迫产品团队思考的是：

- 给 bot 增加什么 capability？

- 它现在能多完成什么工作？

而不是：

- UI 还能塞进什么东西？

他的说法非常明确：

\*\*Adding things to the product is not the goal.\*\*

真正目标是让 bot 在后台：

\*\*reliably do impactful work。\*\*

因此很多“feature”其实根本不需要 pixels。

能变成 bot 自己控制的能力，就应该把对应 UI 删除。

---

# 10. Automation：为什么不应该有 automation builder

### 29:00–30:20

传统 automation 产品通常是：

1. 打开 sidebar；

2. 点 +；

3. 选择 trigger；

4. 选择 action；

5. 配置参数；

6. 可能再写 natural-language instruction。

Roman 觉得很笨重。

结果就是普通用户根本不会建立很多 automation。

Grok Bot 采用另一种方式。

直接对 bot 说：

“每天早上 8 点提醒我做这件事情。”

结束。

用户甚至不应该意识到背后创建了一个 automation object。

Roman 说当时平台上大约 \*\*99% 的 automations 都是通过自然语言创建的\*\*。

这就是他所说的：

\*\*capability 不一定需要 UI。\*\*

---

# 11. Grok Bot 最关键的两个早期决定

### 30:20–35:17

Lenny 提了一个很尖锐的问题。

理论上 Codex、Cowork 等也能完成很多类似事情。

那为什么 Grok Bot 给人的感觉如此不同？

Roman 认为有两个决定最关键。

## 决定一：所有东西默认在 cloud

用户根本不应该考虑：

- 我的电脑是不是开着？

- 手机发任务时家里的 Mac 要不要在线？

- 这个任务是在 local 还是 cloud？

- 我能不能合盖？

- runtime 到底在哪里？

这些都是 implementation detail。

Grok Bot 从很早开始就决定：

\*\*全部 cloud-native。\*\*

这样 bot 是一个持续存在的 entity。

你可以：

- 手机发任务；

- 电脑继续看；

- 未来甚至直接打电话给它；

- 你的设备关掉，任务仍然运行。

Bot 的存在不依附于你当前正在使用哪台设备。

## 决定二：每一个 bot 都拥有自己的 computer

Roman 认为这件事甚至更关键。

首先是现实原因。

大量工作没有 API，也没有 MCP。

人类自己也不是通过 API 完成工作的。

我们：

- 看屏幕；

- 点 pixels；

- 在 textbox 里输入。

那么 AI 至少也应该拥有这些基本能力。

但 Roman 接下来给了一个更有意思的类比。

想象公司来了一个新员工。

你对他说：

“欢迎入职。”

“我们不会给你 laptop。”

“以后你永远坐我旁边。”

“我们两个共享这一台电脑。”

“你的账号和密码我都可以看到，我的账号和密码你也可以看到。”

“而且我们俩还得轮流抢鼠标。”

人类听到马上会觉得：

\*\*这显然疯狂。\*\*

但今天很多 AI 产品的 computer use 恰好就是这样。

AI 和用户抢同一台电脑。

Roman 认为未来回头看这一阶段，会觉得非常奇怪。

既然你把 AI 当新的 colleague onboarding：

\*\*它就应该有自己的电脑。\*\*

---

# 12. 为什么竞争对手没有直接这么做

Roman 不认为这是他们有什么天才洞察。

很多 primitives 其实市场已经证明过了。

尤其是 \*\*OpenClaw\*\*。

Roman 认为 OpenClaw 做对了两个非常重要的事情。

### 1. 给 AI 真正的工具

模型已经够聪明。

很多大家认为“AI 还是很笨”的案例，其实问题不是 intelligence。

问题是：

\*\*你没给它完成工作的工具。\*\*

如果：

- 给它真实 tools；

- 给它自己的 computer；

- 给它你日常工作的环境；

当前模型能够做的事情立刻增加很多。

### 2. 把 AI 当成一个 colleague / helper entity

OpenClaw 改变了很多人的 mental model。

不再只是：

“这里有个 chatbox。”

而是：

“我生活里有一个持续存在、能接触各种东西的 helper。”

Grok Bot 做的事情更多是 \*\*productize\*\* 这套模式。

OpenClaw 的问题是：

- Mac mini；

- VPN；

- 自己部署；

- 技术配置；

- skills；

- slash commands；

- 大量 AI power-user 才懂的概念。

Roman 认为这种方式不可能服务 millions of mainstream users，更不可能成为普通企业标准工作方式。

所以 Grok Bot 的创新重点之一不是发明这些 primitives，而是：

\*\*把 rough edges 全部磨掉。\*\*

比如用户甚至不应该知道“skill”这个概念。

Bot 需要 skill，就在后台创建、使用。

普通用户没有义务每天研究 AI frontier 才能把产品用好。

---

# 13. “Colleague-pilled”：产品设计的 North Star

### 39:21–42:19

Roman 再次描述最终愿景：

你拥有一个 AI team。

这些 AI：

- autonomous；

- 可以被 steering；

- 不需要 micromanage；

- 拥有完成复杂工作需要的工具。

团队内部有一个半开玩笑的词：

\*\*colleague-pilled。\*\*

当两个产品方案看起来都有道理，大家争不出结果时，他们会换一个问题：

\*\*“如果这是真人同事，我希望他怎么做？”\*\*

Roman 说这个问题往往能瞬间澄清争论。

因为 SaaS 产品应该如何工作，大家可能意见不同。

但“一个优秀同事在这种情况下应该怎么做”，通常大家的答案非常接近。

于是问题变成：

\*\*那我们能不能把 AI 做成那样？\*\*

Roman 认为很多 AI 产品问题其实不需要特别天才的 product insight。

人类已经有几百年合作经验。

关键是问：

\*\*human teammate 在这里是什么行为？\*\*

然后尽量复制这种 interaction model。

---

# 14. Voice 的例子：为什么 AI 协作还缺一个重要形态

Roman 用真人工作举例。

很多时候你和同事在 Slack 打字。

打到一半发现：

“这件事五分钟讲清楚更快。”

于是：

- 开一个 huddle；

- 聊五分钟；

- share screen；

- 双方解释 context；

- 结束 huddle；

- 回到 asynchronous work。

这在人类协作里非常自然。

但 AI 产品目前通常被割裂成：

- chat；

- voice mode；

- screen share；

- agent execution。

Roman 认为真正的 AI colleague 应该把这些状态自然连起来。

你可能本来在异步给 bot 任务。

某一刻直接：

“我们聊五分钟。”

给它看屏幕。

讨论完以后它继续自己干活。

这才更接近 teammate。

---

# 15. Work 与 personal：一个产品还是两个？

Lenny 问，未来我们会不会：

一个 AI assistant 管工作；

一个 AI assistant 管个人生活？

Roman 认为确实会存在数据和身份隔离。

很多人本身就希望 work / personal 分开。

企业安全也要求隔离。

但他认为：

\*\*解决这两个问题的产品 form factor 本质上非常相似。\*\*

工作里你想把：

- low-leverage tasks；

- repetitive work；

- information processing

交给 bot。

生活里也是一样。

所以 Roman 的 instinct 是：

\*\*最终一个产品应该可以覆盖两边。\*\*

里面可能是不同 bots、不同权限和 context boundaries，但 interaction model 是同一套。

---

# 16. 下一代“power tool”可能看起来反而很简单

Roman 对“专业软件”还有一个很有意思的判断。

过去的 power tool 很像 Photoshop。

强大意味着：

- 很多 buttons；

- 很多 panels；

- 很多 knobs；

- 用户必须变成 cockpit pilot；

- 熟练掌握软件本身是一种专业能力。

AI 时代可能恰好相反。

新的 power tool 主要需要用户做两件事：

\*\*表达 intent + steering。\*\*

剩下的复杂性应该被 AI 吞掉。

UI 只有在用户确实需要精细控制时才出现。

所以一个非常强大的专业工作工具，未来看起来可能像：

\*\*聊天软件。\*\*

Roman 甚至说他走过同事桌边时，有时候第一眼会觉得对方正在 messaging。

其实那个人正在 Grok Bot 里完成主要工作。

---

# 17. Under the hood：不要把 Grok Bot 理解成 VM 产品

### 47:15–51:05

Lenny 问具体 architecture：

是不是每个 bot 一台 VM？

Roman 没有把重点放在 infrastructure implementation。

他还是回到 colleague analogy。

如果我和你是同事，你应该几乎永远不需要：

“接管我的电脑。”

然后说：

“你点错了，让我来。”

所以随着 computer-use 能力越来越强，Roman 认为：

\*\*computer 最终应该完全从用户的 mental model 中消失。\*\*

今天“bot 有自己的电脑”是重要概念。

未来用户甚至不用意识到电脑的存在。

Roman 认为更正确的 mental model 是：

\*\*这是一支 bot team。\*\*

这些 bots 有两个核心属性。

### Long-lived

它们不是 disposable chat sessions。

传统 chat：

- 新任务；

- new thread；

- context 又从头开始；

- 用户不断复制贴上一次 conversation 内容。

Roman 很讨厌这个模式。

真人团队是按照角色和工作领域长期合作。

AI 也应该这样。

一个 bot 长期负责某个 lane。

它记住：

- 过去 interaction；

- 工作 context；

- 用户习惯；

- 经验。

然后随着时间变得更好。

### 拥有真人员工会拥有的工具

包括：

- API；

- MCP；

- SaaS；

- computer。

也就是既可以走机器接口，也可以在没有机器接口时直接操作 computer。

---

# 18. Grok Bot inside Grok Bot：QA Bot

### 49:44–51:05

Lenny 在 meetup 看到一个很疯狂的 demo：

\*\*让一个 Grok Bot 的 computer 运行 Grok Bot。\*\*

也就是 bot 操作另一个 bot。

Roman 说自己真的每天在这么用。

他有一个：

\*\*QA tester bot。\*\*

做法是：

- 给这个 bot 安装 Grok Bot；

- 每次有新 desktop build；

- 给它一组大约十个 workflows；

- 自动测试；

- 把结果写进 Notion；

- Notion 中保存过去每个版本的历史测试；

- 自动比较 regression。

这个例子强化了 Roman 的 mental model：

不要想“AI chat 能连接哪些 app”。

应该想：

\*\*如果这是一个拥有电脑的人，我可以叫他做什么？\*\*

一旦把问题改成这样，可委托任务范围会大很多。

---

# 19. Roman 自己最重要的用法之一：Infovore

### 51:05–53:37

Roman 认为非常有潜力的一类 Agent 是：

\*\*information eater / infovore。\*\*

也就是让 AI 吞掉巨大数量的信息，把用户从 information overload 中释放出来。

最简单的 V1 是：

给 Grok Bot：

- Slack；

- email。

然后告诉它：

- 我的角色是什么；

- 我在意什么；

- 哪些情况马上通知我；

- 哪些东西不要打扰我；

- 哪些放进每天 digest。

Roman 自己已经做到更复杂的版本。

他的 bot 可以读：

\*\*X 上几乎所有关于 Grok Bot 的 mention。\*\*

然后：

- 和内部 context 交叉；

- 如果是 bug，交给 QA bot 尝试 reproduce；

- 根据情况联系用户；

- 有必要时通知 Roman。

所以 AI 不再等 Roman 去 query。

它变成 always-on 的 Chief of Staff：

\*\*外面的 information firehose 一直冲进来，但 Roman 自己不用一直看。\*\*

Bot 决定什么值得他的 attention。

甚至已经有人让 Grok Bot 拥有 \*\*page 自己的权限\*\*。

例如用户出去喝咖啡，如果发生真正紧急的事情，bot 可以 page 他。

当然这需要极高 trust，因为 false positive 会非常烦人。

Roman 认为未来 AI 一个重要变化就是：

\*\*从 reactive 变成 proactive。\*\*

今天是：

人 → AI。

未来越来越多会是：

AI → 人。

---

# 20. Go-to-market：从个人 early adopter 进入公司

### 53:37–57:57

Lenny 注意到 Grok Bot 团队现在：

- 大量给免费账号；

- 鼓励各种 use cases；

- templates；

- 用户在 X 分享奇怪玩法；

- 很明显想迅速扩大 adoption。

Roman 说，他们在 coding AI 上已经经历过一次类似路径。

大约 2023 年：

开发者在公司里还用传统 IDE。

晚上回家做 side project 时：

开始用 Cursor 和最新 AI coding tools。

突然感觉生产力完全不同。

第二天去公司，他们开始觉得：

“为什么公司还让我这样写代码？”

于是员工反过来要求企业采购 AI tools。

Roman 认为 knowledge work 也会发生类似事情。

用户可能最先因为很个人、很好玩的事情产生 aha moment，例如：

- 控制家里的 robot；

- robot vacuum；

- 帮忙处理 Tesla charger negotiation；

- 各种个人事务。

随后他们会把这种体验带回工作。

最终 Roman 认为 Grok Bot 并不是单纯 consumer toy。

他的目标明确指向：

\*\*transform businesses / transform teams。\*\*

Bot 最终要进入公司并产生真正有经济价值的工作。

接下来要解决的问题就从：

“我和一个 bot 怎么协作？”

变成：

- bot 如何进入一个真实团队？

- 如何理解公司大量历史 context？

- organization-level memory 应该是什么？

- 不同员工和 bots 如何协作？

Roman 明确说这里仍有很多 unanswered questions。

---

# 21. SpaceXAI 当时的三个 AI 产品支柱

### 58:43–1:00:43

Roman 把 SpaceXAI 当时的方向分成三块。

### Coding

Cursor + Grok Build。

他仍然非常相信：

专业 programmer 最终需要一个每个 pixel 都针对 engineering 优化的专业 surface。

Grok Bot 可以：

- kick off cloud agents；

- merge PR；

- QA；

- engineering-adjacent tasks。

但真正 shipping production software，仍然需要 developer-specific product。

### General knowledge work

这就是 Grok Bot。

目标是不断扩大可委托工作的范围，使它更像真正 teammate。

尤其是进入 businesses 和 teams。

### Models

训练更强的 general models。

Roman 把 SpaceXAI 的模型目标描述成相当 practical：

\*\*useful AI。\*\*

他的表述是，他们的重点没有那么偏向抽象地追求某个“superintelligence”概念，而更偏向把模型能力落实为实际可用产品。

这和团队里很多人的 applied engineering 背景有关。

---

# 22. “完成 90%”和“完成 100%”不是数量区别

### 1:00:43–1:03:27

这是整期我认为最重要的一段之一。

Roman 有一条 tweet，大意是：

\*\*能够完成 100% 工作的 AI，与只能做到 90% 的 AI，是完全不同类别的产品体验。\*\*

为什么？

假设你把工作交给一个只能信任 90% 的同事。

你知道：

- 他可能做不好；

- 你中途可能得 intervention；

- 结果回来你还需要检查；

- 有些地方肯定还要自己补。

那么任务虽然理论上完成了 90%，实际上它一直留在你的脑子里。

你没有真正卸载它。

Roman 认为：

\*\*这不是真正的 delegation。\*\*

真正 delegation 更像篮球里的 \*\*no-look pass\*\*。

你把球传出去以后就开始跑下一个位置。

因为你相信队友会处理好。

不需要继续回头盯。

这就是 Roman 认为 Grok Bot 第一次在 non-coding work 中让他感受到的东西：

“我把任务交出去。”

“我不用继续想着。”

“回来以后它已经做好了。”

工程师过去一年多已经越来越习惯这种体验，因为 coding agent 大幅改变了 programming。

但大部分普通 knowledge worker 使用 AI 的方式其实仍跟两年前差不多：

- new chat；

- prompt；

- 等结果；

- 看结果；

- 改；

- 继续 prompt。

Roman 认为真正的 Agent 应该结束这种模式。

---

# 23. 公司为什么还能这么快

### 1:03:27–1:08:02

Lenny 说他很震惊于团队速度。

在 Slack 里有人说：

“明天做这个。”

然后第二天真的有了。

或者：

“我们两天后 launch template marketplace。”

然后真的两天。

Roman 把原因主要归到 culture。

他加入 Cursor 时公司大约 \*\*15 人\*\*。

后来增长到 \*\*1,000+\*\*，之后又进入更大的 SpaceXAI。

但他认为有一种东西一直没有完全消失：

\*\*startup feeling。\*\*

他的定义不是：

- 人数少；

- Seed round；

- 没多少钱。

真正的 startup 特征是一种：

\*\*scramble energy。\*\*

看起来可能：

- chaotic；

- disorganized；

- 对某些人来说甚至不是舒服的工作环境。

但是它有一个巨大好处：

一个人可以在极短时间里对某个方向产生巨大影响。

Roman 认为大公司常常嘴上会说：

“我们仍然像 startup 一样快。”

但所有人都知道已经不是了。

他觉得 SpaceXAI/Cursor 至今仍较强地保留这种 impulse。

其中很重要的一点是：

\*\*大家高度信任别人会把自己那部分事情做好。\*\*

所以不需要所有事情层层协调。

---

# 24. Cursor 为什么能一直活下来

Lenny 提出：

从外面看，Cursor 本来“应该死掉”。

因为它面临：

- OpenAI；

- Anthropic；

- Microsoft；

- 大量 AI startups。

而且 Cursor 本身还大量依赖 foundation-model providers。

但 Cursor 从：

autocomplete

→ chat

→ agents

→ cloud agents

→ Grok Bot

不断变化。

Roman 同意，并认为这里最核心的是：

\*\*从来没有觉得自己赢了。\*\*

AI capability 一直变化。

因此“正确产品”本身也一定变化。

两年前正确的 AI 产品，不可能仍然完全适合今天。

Roman 给了一个非常激进的标准：

\*\*如果公司不能大约每六个月彻底重新发明一次自己，就会输。\*\*

甚至最近六个月都嫌太长。

这个重新发明包括：

- priorities；

- core product；

- user experience；

- 对未来的 beliefs。

Roman 认为过去很多 AI coding competitors 消失，并不一定因为他们缺资源或者做了某一个明显错误决定。

更深层问题是：

\*\*组织文化无法随着 reality 足够快地改变。\*\*

---

# 25. 两个内部价值观

### 1:10:11

Roman 提到两个自己经常重复的 values。

## Delete the product

模型能力不断增强以后，很多以前必须靠 product scaffolding 才能实现的东西会变得多余。

因此产品进步并不等于：

不断增加东西。

反而需要不断：

\*\*删除过去为了弥补模型能力而建立的结构。\*\*

即使：

- 一小部分用户喜欢；

- 公司内部有人舍不得；

也要敢删除。

因为最终目标是：

\*\*simple + powerful。\*\*

这也是为什么 Grok Bot 从 prototype 到发布主要做的是 unshipping。

## Just do the thing

如果你看到一件事情需要发生：

不要先寻找许可。

去做。

需要什么资源，自己把人拉进来。

Roman 说这不是：

\*\*ask-for-permission culture。\*\*

公司里每个人都对最终结果拥有 agency。

---

# 26. 对 AI startup moat 的看法

### 1:11:44–1:15:14

Lenny 问了一个现在创业者特别常问的问题：

AI 变化这么快，到底怎样建立 moat？

Roman 对这个问题相当不迷信。

他理解为什么 founder 会想：

- 12 个月以后怎样？

- 24 个月以后模型会怎样？

- 我的 defensibility 在哪？

但 24 个月在 AI 世界几乎像永远。

如果早期 Cursor 是从：

“我们需要建立某个 moat，所以倒推产品”

开始，Roman 不认为它会变成今天这样。

Cursor 真正做的事情是：

\*\*obsess over building something useful today。\*\*

同时观察：

三个月、六个月后模型大概率能做到什么？

然后问：

\*\*有没有办法通过 engineering 和 product，把那种未来能力提前到今天？\*\*

哪怕需要：

- 大量 glue code；

- 特殊 UI；

- 特殊 infra；

- 很复杂的 scaffolding。

先让用户今天就能拥有未来三个月的体验。

三个月后模型自己已经会做了？

很好。

\*\*把 scaffolding 全删掉。\*\*

然后再次看未来三个月，把下一个“不可能”的东西提前。

Roman 认为 Cursor 一直重复这个 cycle。

长期以后自然产生：

- 用户 trust；

- distribution；

- data advantages；

- 产品使用习惯。

这些后来可以成为 moat。

但 moat 是过程中发现和积累的。

它不是创业第一天在 strategy diagram 上画出来的。

Roman 给 founder 的建议基本是：

\*\*找到今天还不可能、但非常有价值的事情。想办法让它今天就可能。\*\*

用户会为了这个能力来。

然后带他们继续去下一个 frontier。

Lenny 把它总结为一句更简单的话：

\*\*moats are often discovered, not planned。\*\*

这是 Lenny 的归纳，不是 Roman 的原话立场，需要区分。

---

# 27. Roman 建议 Grok Bot 新用户怎么开始

### 1:15:14–1:17:49

Roman 很刻意地不愿意分享所谓“高级 prompt hacks”。

因为如果产品真的需要几十个 hacks 才好用，在他们看来就是产品没有做好。

他的建议反而非常简单。

### 给它 context

就像 onboarding 新员工。

如果员工工作需要：

- Slack；

- email；

- company records；

那 bot 也应该能访问这些 context。

### 然后不要自己猜它能做什么

直接问：

\*\*“根据你现在能看到的 Slack、email 等信息，找五件你可以从我手上完全接过去做的事情，并告诉我需要怎样做。”\*\*

Roman 自己最早就是这么做的。

Bot 推荐了五件。

其中两件非常好。

Roman 直接创建两个 bots 去负责。

关键是这些建议并不是：

“帮你 draft 一封邮件。”

而是：

\*\*一整块 work。\*\*

这成为他自己的 aha moment。

---

# 28. Power user：给所有 bot 一个统一 output store

Roman 目前越来越关注 bots 之间的 cooperation。

与此同时，他发现另一个实际问题：

如果十几个 bots 一直生产信息，输出会散落得到处都是。

所以他建立了一些 scaffolding：

让 bots 把 artifacts / digests 写进一个统一、对人很易读的地方。

比如：

- 每日 digest；

- database；

- 一个稳定的信息 store。

这样用户不需要去十个 bot conversation 里找东西。

Roman 给 advanced users 的建议就是：

\*\*认真设计 bot 输出最终应该落在哪里。\*\*

一群 autonomous agents 如果没有统一的信息出口，很快也会制造另一种 information chaos。

---

# 29. Lightning round

Roman 推荐两本书：

- Kurt Vonnegut 的 \*\*Cat’s Cradle\*\*

- Steven Pressfield 的 \*\*The War of Art\*\*

他会每年重看一次 \*\*Casablanca\*\*，其中恰巧有一个角色也叫 Ugarte。

他也会看老剧 \*\*Monk\*\*，部分原因是喜欢剧中 1990s～2000s 初 San Francisco 的样子。

除 Grok Bot 外，他很喜欢 semantic search 产品。

特别提到 \*\*Exa\*\*，以前叫 Metaphor。

Roman 很喜欢把 semantic search 用在奇怪的数据集上，比如艺术馆 image collection，而不只是搜索网页。

他长期放在门上的一段文字是 \*\*Desiderata\*\*。从十几岁开始，每次搬家都会把它贴到门上，觉得反复读仍能得到新的东西。

---

# 这次对谈真正完整的思想链

如果把整期对谈保持原有逻辑串起来，Roman 的思想其实是下面这一条连续链条：

\*\*模型已经越来越聪明 → 限制 AI 的越来越多不是 intelligence，而是 harness、tools 和 product form → 所以应该给 Agent 真实工具和自己的电脑 → 一旦它能持续存在并真正完成工作，就不应该再被理解成 chat session → 它应该成为长期存在的 colleague → 既然是 colleague，产品设计就可以大量借鉴人与同事的协作方式 → 用户不需要看它每一步 reasoning，也不需要和它共享鼠标 → 用户真正需要的是 delegation 和 trust → 真正的 delegation 要求 AI 接近端到端完成工作 → 90% 完成并没有消除人的 cognitive load → 当 AI 能完成整块工作，它就从“提高效率的软件”变成了“增加团队 capacity 的成员”。\*\*

而 Grok Bot 的很多具体产品决定，其实全部是这条逻辑的后果：

- cloud-first；

- one computer per bot；

- persistent bots；

- long memory；

- 给 bot 名字和职责；

- Chief of Staff 模式；

- 隐藏 tool calls；

- natural-language automation；

- 删除传统 UI；

- proactive notifications；

- bot-to-bot delegation；

- unified artifact store；

- 从 personal early adopters 向企业扩散。

这里最值得注意的地方可能是：Roman 并没有把 Grok Bot 的突破归因于某个新模型。

他反复在说的，其实是：

\*\*同样越来越强的模型，如果你换掉产品的基本假设，用户感受到的是完全不同的东西。\*\*

这也是为什么他们选择从零做一个新产品，而没有继续往 Cursor 里加 tab。
