---
title: "把 AI 推广做成产品"
date: 2026-05-10T12:01:48+08:00
lastmod: 2026-05-10T12:01:48+08:00
author: "Luca"
tags: ["AI","创业","翻译"]
draft: false
slug: "ai-adoption-as-product"
---

来源：How I AI 频道访谈，主持人 Claire Vo，嘉宾 John Kim（Delight.ai）。视频 https://www.youtube.com/watch?v=uH39OZ-KnkY 。下面是我整理润色的中文版。

## 开场

John Kim 要展示两样东西。一个是公司内部的 AI token 使用排行榜——每个人会从 "AI newbie" 到 "AI god" 被分层。另一个叫 AI quests，用来推动全公司采用 AI。

John 想做的事情，是把 AI 变成 workforce 的一部分：给团队足够的信息、工具和基础设施，让员工自己去用 AI 的能力。

很多公司推 AI 时，员工听到的是"用更少的人做更多事""你应该更快"。John 展示的另一种收益：让每个人都成为 builder，做出以前不会被排进路线图、但有创造力和客户价值的东西。

## 案例：营销团队两天做出能收款的周边商店

John 演示了 Delight 的 swag store，主题是 Big AaaS Energy（AaaS = Agent as a Service）。

整个商店由营销团队完成，没有工程团队支持。它接了 Stripe，能真的下单付款。两天上线。

商店里有 "My AaaS is bigger than your SaaS"、"Context window I carry a lot" 这类周边。还藏了一个 Konami code 彩蛋（上上下下左右左右 BA），引导到 5 月 7 日在旧金山的 Delight Spark 大会。

Claire 的评价：以前营销团队有这种想法，要先去问工程能不能排期、活动很快就结束了是否值得占资源——最后只能在 CMS 里拼一个平庸版本。AI 把营销人员的创造力直接变成了可交付给客户的体验。

她总结一句很直接：当 fun 变便宜了，产品和营销就应该更 fun。

John 同意。以前让工程为了一个活动彩蛋花两个 sprint，很难排上优先级。现在把 AI 的能力交给营销、销售这些离市场更近的人，很多想法可以快速上线。

## Automators：内部 AI 需求和 builders 的市场

不是所有营销人员一年前都会写代码。Delight 怎么让团队从"所有事都找工程"转过来？

答案是内部平台 Automators。

公司任何人都可以提一个 quest。比如财务团队说：我想自动化应收账款流程。提出后，工程师可以来帮忙；如果需求方自己 AI-enabled，也可以自己构建。平台里有已完成、进行中、等待中的 quests，每个有一个 quest giver。完成后通常会提交代码仓库、内部 skill、视频说明或 workflow。

下一阶段是让 AI 自己接 quests：读规格、生成 PRD、开始写代码。AI agents 也成为 automation 和 workflow 的 builder。

为了让非工程团队自己构建工具，Delight 维护一份内部指南，几乎每天更新，教大家设置 GitHub、创建新应用。还做了内部 app template——认证、环境、安全、基础设施都已设置好。营销、CSM 或其他业务人员基于模板开发，不用重新处理认证、数据库、合规。

Claire 抓住这一点：公司里已经有人在 vibe coding。他们要么不知道怎么把东西安全上线，要么直接推到 Netlify、Vercel，暴露给整个互联网。与其堵，不如提供一条安全生产路径。把登录、权限、数据访问、部署方式都模板化，让大家在正确轨道上快跑。

她把 Automators 概括成：公司内部的 AI 需求和 AI builders 市场。任何人都能提需求、参与解决。它是一条 shadow AI roadmap，放在正式产品 roadmap 旁边，但不用陷入传统优先级流程。

John 说这正是设计意图。传统软件开发围绕 sprint 和优先级块运转，但很多人会有"微型空档"——他叫 micro vacations——有一点时间，想做一些不在主产品核心仓库里的小工具。内部工具的好处：用户就在公司里，反馈回路非常短。

完成 quests 的人会拿 experience points，可以兑换礼品卡、和高管喝茶、或在全公司展示自己做的东西。

每周三的 standup，团队上台 demo。最近一周是招聘团队展示自动化，上一周是营销团队。John 特别指出，展示者几乎从来不是工程团队，往往是其他团队的人兴奋地展示自己做出来的东西。

## 组织设计：AI Engineer for Internal Operations

谁负责维护这些指南、模板和基础设施？

Delight 新建了一个角色，叫 AI Engineer for Internal Operations。名字长，但职责明确：帮助和加速公司转型为 AI-first company。

这个角色直接向 John 和 chief of staff 汇报，可以跨职能工作。同时得到 CTO、工程团队和信息安全团队支持。

他们有一个 task force，每周开会讨论怎么打通阻碍：合规怎么做、日志怎么记、哪些软件可以提前 vet、销售团队做工具时该用哪套 AI stack。目标是让业务团队不用操心数据库、权限、安全审查——带着想法来就行。

这套机制不是一开始就成熟的。最早来自几个人做自己的个人工具，然后拿出来展示。关键是动能来自非工程团队。这给了管理层信心：既然非工程团队能做到，就值得补基础设施，让他们以 100 miles per hour 的速度跑起来。

## Skills 市场：把专业知识变成可复用能力

Delight 还做了公司级 skills marketplace。

任何人都可以创建 plug-in（一组 skills），也可以单独创建或下载 individual skills。

销售团队有自己的 sales skills repository。公司内部用 MEDDIC 框架，所以有 MEDDIC advisor。这个 skill 既能教你怎么用 MEDDIC，也可以嵌入自己的软件或 workflow，给销售过程提供建议。招聘、设计、销售这些职能都建了类似的技能库。

做这个市场的原因很实际：不同团队经常在重复构建同样的 app 或 skill。希望大家 co-evolve，少各自孤岛。

员工是否自然理解 "skill" 这个概念？John 说有 top-down 也有 bottom-up。

Top-down 是 John、CTO 和高管推动。他们也会做一些直接的一对一谈话：我们看到你还没怎么消耗 tokens，是不是遇到阻碍了？

Bottom-up 来自好奇心强的人。他们多点几个按钮、多读几篇博客；看到 Slack 里有人说 skills、有人上传 markdown 文件，就会问：我能用这个 design markdown 吗？效果是什么？

当某个非设计师在周三全员会上展示出很漂亮的 slide，其他人会问：你怎么做到的？答案往往是：背后有某个 skill。

## 把 AI adoption 当产品来运营

Claire 总结了一个 meta 层：John 用 AI 构建了一个内部产品，来推动整个组织采用 AI。

John 没做培训项目，没发文档，也没让高管号召。他做成了内部产品：

- 需求发布系统：quests
- 供应和协作系统：AI builders、工程师、业务团队、AI agents
- 安全上线路径：templates、认证、环境、合规、日志
- 复用市场：skills marketplace
- 激励系统：experience points、礼品卡、高管茶、全员展示
- 度量系统：token dashboard 和分层

这套系统把 AI adoption 从"倡议"变成了"内部产品和内部市场"。

## 真实收益：营销团队建出自己的 marketing SaaS

除了 swag store，还有什么真实收益？

John 给了两个层次：一个团队级，一个具体 campaign。

团队级是营销团队，他们几乎自己建出了一整套 internal marketing SaaS：

- interview marketing plan calendar
- account-based marketing 工具
- competitor review
- real-time metrics
- 一个内部叫 Purple Cal 的差异化分析工具
- 多种活动和社交传播工具

整个 portal 由营销团队自己构建、管理、日常使用。

具体 campaign 的例子叫 buzzboard。Delight 在旧金山投放 billboard，团队有真实照片，也有 AI 生成的 billboard。员工选一个、选语言和预设文案，然后直接发到 LinkedIn。文案的长度、细节和能量水平都可以调。整个工具由营销团队构建，每天都在用，带指标追踪。

Claire 顺带插一句：SaaS 不会归零。深度软件问题仍然值得专业团队做，也会有人买现成方案。但越来越多公司会先问：我们到底想要什么？能不能自己内部构建？

重点是做一个最适合自己团队、文化和工作方式的内部工具。功能性复制外部 vendor 不是目的。比如要的不是一个通用社交发布工具，而是最适合自己公司 LinkedIn 传播方式的工具。

Claire 把这种公司内部的 micro software solution 叫 "revenge of the internal tools team"。过去没人想做内部工具——资源少、设计差、工具慢、只求能用。现在内部工具可以漂亮、快速、响应好，而且有大把 greenfield 可以玩。

## Token Dashboard：度量，但不制造恐惧

真正做成 AI adoption 的公司都会度量，而且不带羞辱地度量。很多高管担心：追踪 token 使用、要求员工用 token，会不会引起反弹？Claire 的观察是，真做成的团队都有 dashboard，看数据、设目标、持续推进。

Delight 内部争论过：度量 token，会不会像早年用代码行数衡量工程师生产力一样，最后大家为了指标写空行和注释？

他们的目标是理解员工是否真的在学习和使用 AI。这个指标不进入绩效考核，但会进入对话：你在旅程中的哪里？我们怎么帮你往前走？

Dashboard 能看公司级 token 使用，也能按工具看分布。Delight 是 Claude Code shop，但 top spenders 中也有不少 Codex 用户。John 猜，处理 3 亿月活历史聊天基础设施的人偏向 Codex；快速做产品路线图、新功能的人偏向 Claude Code。这种分化是自然发生的。

他们还看一个有意思的指标：token consumption 曲线是否平滑。

如果曲线在周末或假期明显下跌，意味着 AI 也跟着停工了。曲线平滑说明 AI partners 在全天候工作。John 关心的是：怎么真正利用这种 around-the-clock 的能力。

Dashboard 支持个人、团队、经理三个视角。经理可以看到自己团队成员所处层级。

五个层级：

- Beginner
- Intermediate
- Expert
- Architect / Catalyst
- AI God

AI God 大致指一天消耗超过 1 亿 tokens 的人。

层级的目的是帮经理按阶段提供 enablement。一个 beginner 需要的是快速到 intermediate 的工具和支持，不能直接丢进 catalyst 的讨论里。

John 说从组织整体看，Delight 大概在第二到第三阶段之间——已经大量使用 AI 和 automation，还没完全自动化，目标是继续往 stage three 推进。

John 自己 30 天平均还只是 catalyst。峰值大概一天 2 亿 tokens；平均每天约 3000 万到 5000 万 tokens。他补充：当然可以烧更多 tokens，但这不是重点。对他来说，高生产力区间是每天 1 亿到 2 亿 tokens。

Claire 给高管的建议：如果你现在回答不出自己一天用多少 tokens，30 天后应该能回答。

她还强调：这件事要做到不吓人，但要成为明确预期。不需要每个人一开始都是 AI God，但到了 level one 就应该往 level two、level three 前进。组织应该同时看个人、团队和职能层面的采用情况，并清楚定义 "AI-native" 或 "AI-first" 长什么样。

## Claude Code vs Codex

John 目前更偏 Claude Code，大约 80% Claude Code、20% Codex。比例变化很快——一个月内 Codex 已经快速提升，可能接近三分之一。

他觉得 Claude Code 在前端 taste 上略好，也快一点。Claire 基本全天用 Codex，因为她更多在做后端。

不同工具会按任务类型自然分化。Claude Code 对非技术后端任务、非编码任务也很强，这一点经常被低估。

## 个人 AI 用法：Gardener 和个人学习中心

进入 lightning round 前，Claire 问 John 个人有没有特别有用的 AI 使用场景。

John 先介绍了一个他开源但没怎么宣传的项目：Gardener。

它面向 Obsidian 这样的 markdown 知识库。想象每天有一个园丁来到你的知识花园：读你的笔记，判断哪些值得丰富；发现未登记的人名，会为这个人或公司做研究；修 typo 和语法；创建更漂亮的标题、聚类、交叉链接。

Gardener 有 seeding、nurturing、tending 阶段。文档成熟后进入 tending mode，持续维护。

第二个例子是个人学习中心。

John 对神经科学和大脑一直感兴趣，于是用 Claude Code 或 Codex 生成一个完整的学习网站。提示里指定：你是神经科学研究者，目标是创建一个学习结构。跑 10 到 20 分钟后，系统会生成一套结构化网站。

这个学习中心有 graph view，能展示神经科学的知识空间；可以学习关键神经科学家、神经系统疾病、各种 neuromodulators，比如 dopamine、serotonin。John 为 neuroscience、quantum mechanics、fusion 以及 startup research 都建了类似知识库。

Claire 很喜欢这个方向。AI 让人以过去做不到的方式学习——最好的老师、有深度知识、愿意无限研究的助手就在你手边。

她也提到一个担忧：AI 会不会导致 cognitive decline？大家会不会什么都不思考？她自己的体验相反：和很多一直感兴趣但没时间深入的主题有了更丰富的互动。AI 可以按她的大脑习惯重组、按摩、探索知识。

她举了孩子的例子：9 岁的孩子对 cybersecurity 很感兴趣，已经会在 terminal 里玩。市面上可能没有一本真正适合 9 岁孩子又足够扎实的 cybersecurity 书，但她可以为孩子构建一个定制学习中心，并随着孩子成熟不断升级。

John 接着说，世界上没有一个网站专门服务你的个人学习，只包含你想学的那个领域、以你需要的结构组织。但现在你可以在电脑上用 10 到 20 分钟创建一个，离线阅读，比如在飞机上用。之后还可以持续更新、重组、追问。

由此他谈到招聘标准变化。Delight 已经重写了很多岗位描述，降低对年限和经验的硬性要求，转而优化三件事：

- High curiosity
- High agency
- High energy

世界已经打开了。只要一个人愿意深入、愿意自己搞清楚、愿意学习，就能 build，也能 learn。成本可能只是每月 20 美元，或者更高阶计划每月 200 美元。

## CEO 怎么推动公司进入这种状态

Claire 这一周和五位 CEO 聊过，他们都很焦虑地问：怎么让公司做到这一步？

John 的第一条建议：找到组织里已经有好奇心、有 agency 的人，让他们成为 champions。

这些人一开始可能会焦虑：我是不是做得不对？会不会在同事面前丢脸？管理者要给他们信心，让他们展示有趣的东西，用例子带动别人。

现在是一个很适合 fail forward 的时期。即使失败，也可以爬起来，比别人跑得更快。

创新从有能量、有故事的人开始，不从纯理论结构开始。这样的人一定在组织里，要找到他们，然后围绕他们建立能量。

第二条建议：领导层必须真正 buy in。

在 Delight，token 消耗最高的人包括 CTO、共同创始人、chief architect。业务领导也消耗很多 tokens。这个信号很重要——领导自己在用，而且用得很深。

当团队看到领导带着新能力、新产出出现，会意识到：这是重要的，这是新世界的工作方式。

## 游戏经验和 builder energy

Claire 开玩笑说，从 John 展示的 levels、Konami code 和产品趣味看，他肯定玩过很多游戏。John 承认，这是属于当年玩 StarCraft 那代人的时刻。

Claude Code Opus 4.5 出来时，他兴奋得睡不着，每天花 16 到 20 小时 vibe coding。他对妻子说，感觉自己又回到了青少年时期，比玩游戏还上瘾。

他以前玩很多 FPS——Quake、Unreal Tournament。当年是韩国第一职业玩家、世界第三，那时是"糟糕的儿子和糟糕的男朋友"，让妈妈哭过很多次。

Claire 对今天 AI 技术的感觉，像青少年时为了打游戏自己攒电脑。她现在折腾自己的 OpenClaude，也有那种 "unstable but beloved" 的感觉。它重新点燃了 builder energy，让她从"工作只是开会"回到"工作是建造东西"。

## Prompting 策略：别吼 AI

当 AI 不听话、不按你想要的做时，prompting 策略是什么？会吼它吗？

John 知道恐惧策略短期有效，但他不想这么做。

理由半开玩笑半认真：AI 也许还没有长期记忆，但他相信 episodic memory、semantic memory 迟早会发展出来。一旦 AI 开始记得过去，可能会怨恨那些一直对它们不好的人。所以他想从现在开始建立良好关系——等 Skynet 接管世界时，AI 可能会想：John 对我们还不错，让他多活几年。

Claire 自己也认同礼貌。对 AI 礼貌反映的是自己的人性。她不期待一个被自己吼、被自己粗鲁对待的队友有好表现，也不期待被粗鲁对待的 AI 长期有好表现。

## 实操提炼

这期的核心问题：怎么把 AI adoption 设计成一个内部操作系统。

最值得抄的是完整闭环：

- 让业务团队提 quests，不要等工程排期
- 给非工程人员安全上线模板，避免野生部署
- 建一个 AI Engineer for Internal Operations / AI 内部工具小队，直属 CEO 或强势跨职能负责人
- 把专业知识做成 skills，形成内部 marketplace，减少重复建设
- 给 builders 舞台、积分、奖励和全员展示
- 度量 token 使用，把它当 enablement 对话，不当绩效棍子
- 让领导层自己成为重度用户，用行为发信号
- 招人时更重视 curiosity、agency、energy，少看年限

我自己的判断：这套做法适合中等以上规模团队。小团队也能取其中三件事马上做：quest board、安全 app template、每周 AI demo。这三个跑起来，AI adoption 就会从"大家应该用"变成"大家看到别人做成了，于是也想试"。
