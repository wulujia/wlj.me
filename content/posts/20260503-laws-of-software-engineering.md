---
title: "软件工程定律网站采集"
date: 2026-05-03T10:00:00+08:00
tags: ["软件工程","Reference"]
draft: false
slug: "laws-of-software-engineering"
---

[lawsofsoftwareengineering.com](https://lawsofsoftwareengineering.com/) 这个站做得很漂亮，配色、卡片排版都挺花心思。

首页每张卡片一句话，点进去详情页约 1300 字，含定义 / Takeaways / 例子 / 出处 / 推荐阅读 / 相关定律。

内容都是 Wikipedia 上能查到的经典概念，没有原创理论。它的价值是集中收纳、视觉好看、结构化重述，不是新见解。当 reference 用足够，当 insight 没什么。

学习一些名词也挺好。下面给中英对照，中文是严格按英文翻译的，不扩写。

| # | 名称 | 英文描述 | 中文描述 |
|---|------|---------|---------|
| 1 | Conway's Law<br>康威定律 | Organizations design systems that mirror their own communication structure. | 组织设计的系统会反映其自身的沟通结构。 |
| 2 | Premature Optimization<br>过早优化 | Premature optimization is the root of all evil. | 过早优化是万恶之源。 |
| 3 | Hyrum's Law<br>海勒姆定律 | With a sufficient number of API users, all observable behaviors of your system will be depended on by somebody. | 当 API 用户数量足够多时，系统所有可观察到的行为都会被某人依赖。 |
| 4 | The Boy Scout Rule<br>童子军规则 | Leave the code better than you found it. | 让代码比你来时更好。 |
| 5 | YAGNI<br>你不会用到的 | Don't add functionality until it is necessary. | 在功能必要之前不要添加它。 |
| 6 | Brooks's Law<br>布鲁克斯定律 | Adding manpower to a late software project makes it later. | 给延期的软件项目增加人手会让它更晚。 |
| 7 | Gall's Law<br>盖尔定律 | A complex system that works is invariably found to have evolved from a simple system that worked. | 能运转的复杂系统，无一例外是从能运转的简单系统演化而来的。 |
| 8 | The Law of Leaky Abstractions<br>抽象漏洞定律 | All non-trivial abstractions, to some degree, are leaky. | 所有非平凡的抽象，都在某种程度上有漏洞。 |
| 9 | Tesler's Law<br>泰斯勒定律 | Every application has an inherent amount of irreducible complexity that can only be shifted, not eliminated. | 每个应用都有一定量不可削减的固有复杂度，只能转移，不能消除。 |
| 10 | CAP Theorem<br>CAP 定理 | A distributed system can guarantee only two of: consistency, availability, and partition tolerance. | 分布式系统只能在一致性、可用性、分区容忍性中保证两项。 |
| 11 | Second-System Effect<br>第二系统效应 | Small, successful systems tend to be followed by overengineered, bloated replacements. | 小而成功的系统之后，往往跟着过度工程、臃肿的替代品。 |
| 12 | Fallacies of Distributed Computing<br>分布式计算谬误 | A set of eight false assumptions that new distributed system designers often make. | 分布式系统新手常犯的八条错误假设。 |
| 13 | Law of Unintended Consequences<br>意外后果定律 | Whenever you change a complex system, expect surprise. | 每当你改动一个复杂系统，都要预期会有意外。 |
| 14 | Zawinski's Law<br>扎文斯基定律 | Every program attempts to expand until it can read mail. | 每个程序都会扩张到能收发邮件为止。 |
| 15 | Dunbar's Number<br>邓巴数 | There is a cognitive limit of about 150 stable relationships one person can maintain. | 一个人能维持的稳定关系存在约 150 人的认知上限。 |
| 16 | The Ringelmann Effect<br>林格尔曼效应 | Individual productivity decreases as group size increases. | 群体规模增大时，个人生产力下降。 |
| 17 | Price's Law<br>普赖斯定律 | The square root of the total number of participants does 50% of the work. | 参与者总数的平方根的人，完成 50% 的工作。 |
| 18 | Putt's Law<br>普特定律 | Those who understand technology don't manage it, and those who manage it don't understand it. | 懂技术的人不管理技术，管理技术的人不懂技术。 |
| 19 | Peter Principle<br>彼得原理 | In a hierarchy, every employee tends to rise to their level of incompetence. | 在层级体系中，每个员工都倾向于上升到其不胜任的层级。 |
| 20 | Bus Factor<br>巴士因子 | The minimum number of team members whose loss would put the project in serious trouble. | 失去之后会让项目陷入严重麻烦的最少团队成员数。 |
| 21 | Dilbert Principle<br>呆伯特原理 | Companies tend to promote incompetent employees to management to limit the damage they can do. | 公司倾向于把不胜任的员工提到管理岗，以限制他们能造成的损害。 |
| 22 | Parkinson's Law<br>帕金森定律 | Work expands to fill the time available for its completion. | 工作会扩张到填满可用于完成它的时间。 |
| 23 | The Ninety-Ninety Rule<br>九十-九十法则 | The first 90% of the code accounts for the first 90% of development time; the remaining 10% accounts for the other 90%. | 前 90% 的代码占前 90% 的开发时间；剩下 10% 的代码占另外 90% 的开发时间。 |
| 24 | Hofstadter's Law<br>侯世达定律 | It always takes longer than you expect, even when you take into account Hofstadter's Law. | 它总是比你预期的更久，即使你已经把侯世达定律考虑进去。 |
| 25 | Goodhart's Law<br>古德哈特定律 | When a measure becomes a target, it ceases to be a good measure. | 当一个衡量指标成为目标时，它就不再是一个好指标。 |
| 26 | Gilb's Law<br>吉尔布定律 | Anything you need to quantify can be measured in some way better than not measuring it. | 任何你需要量化的东西，都能以某种比不衡量更好的方式被衡量。 |
| 27 | Murphy's Law / Sod's Law<br>墨菲定律 | Anything that can go wrong will go wrong. | 任何可能出错的事都会出错。 |
| 28 | Postel's Law<br>波斯特尔定律 | Be conservative in what you do, be liberal in what you accept from others. | 自己发出的要保守，接受别人的要宽容。 |
| 29 | Broken Windows Theory<br>破窗理论 | Don't leave broken windows (bad designs, wrong decisions, or poor code) unrepaired. | 不要让破窗（糟糕的设计、错误的决策或差的代码）放着不修。 |
| 30 | Technical Debt<br>技术债 | Technical Debt is everything that slows us down when developing software. | 技术债就是开发软件时一切让我们变慢的东西。 |
| 31 | Linus's Law<br>林纳斯定律 | Given enough eyeballs, all bugs are shallow. | 只要有足够多的眼睛，所有 bug 都是浅显的。 |
| 32 | Kernighan's Law<br>柯尼汉定律 | Debugging is twice as hard as writing the code in the first place. | 调试的难度是最初写代码难度的两倍。 |
| 33 | Testing Pyramid<br>测试金字塔 | A project should have many fast unit tests, fewer integration tests, and only a small number of UI tests. | 一个项目应该有大量快速的单元测试、较少的集成测试，以及只有少量的 UI 测试。 |
| 34 | Pesticide Paradox<br>农药悖论 | Repeatedly running the same tests becomes less effective over time. | 反复运行相同的测试，随着时间推移会越来越无效。 |
| 35 | Lehman's Laws of Software Evolution<br>莱曼软件演化定律 | Software that reflects the real world must evolve, and that evolution has predictable limits. | 反映真实世界的软件必须演化，而这种演化有可预测的极限。 |
| 36 | Sturgeon's Law<br>斯特金定律 | 90% of everything is crap. | 任何东西的 90% 都是垃圾。 |
| 37 | Amdahl's Law<br>阿姆达尔定律 | The speedup from parallelization is limited by the fraction of work that cannot be parallelized. | 并行化带来的加速比，受限于无法并行的那部分工作的比例。 |
| 38 | Gustafson's Law<br>古斯塔夫森定律 | It is possible to achieve significant speedup in parallel processing by increasing the problem size. | 通过增大问题规模，并行处理可以获得显著的加速。 |
| 39 | Metcalfe's Law<br>梅特卡夫定律 | The value of a network is proportional to the square of the number of users. | 网络的价值与用户数量的平方成正比。 |
| 40 | DRY<br>不要重复 | Every piece of knowledge must have a single, unambiguous, authoritative representation. | 每一项知识都必须有单一、明确、权威的表达。 |
| 41 | KISS<br>保持简单 | Designs and systems should be as simple as possible. | 设计和系统应该尽可能简单。 |
| 42 | SOLID Principles<br>SOLID 原则 | Five main guidelines that enhance software design, making code more maintainable and scalable. | 五条提升软件设计的主要准则，让代码更易维护和扩展。 |
| 43 | Law of Demeter<br>迪米特法则 | An object should only interact with its immediate friends, not strangers. | 一个对象应只与其直接的朋友交互，不与陌生人交互。 |
| 44 | Principle of Least Astonishment<br>最小惊讶原则 | Software and interfaces should behave in a way that least surprises users and other developers. | 软件和界面的行为方式，应当让用户和其他开发者最不感到惊讶。 |
| 45 | Dunning-Kruger Effect<br>邓宁-克鲁格效应 | The less you know about something, the more confident you tend to be. | 你对某件事知道得越少，就越倾向于自信。 |
| 46 | Hanlon's Razor<br>汉隆剃刀 | Never attribute to malice that which is adequately explained by stupidity or carelessness. | 凡能用愚蠢或粗心充分解释的事，绝不归咎于恶意。 |
| 47 | Occam's Razor<br>奥卡姆剃刀 | The simplest explanation is often the most accurate one. | 最简单的解释通常是最准确的。 |
| 48 | Sunk Cost Fallacy<br>沉没成本谬误 | Sticking with a choice because you've invested time or energy in it, even when walking away helps you. | 因为已经投入了时间或精力而坚持某个选择，即使放弃才对你有益。 |
| 49 | The Map Is Not the Territory<br>地图不是疆域 | Our representations of reality are not the same as reality itself. | 我们对现实的表征并不等同于现实本身。 |
| 50 | Confirmation Bias<br>确认偏误 | A tendency to favor information that supports our existing beliefs or ideas. | 一种偏爱支持我们既有信念或观点的信息的倾向。 |
| 51 | The Hype Cycle & Amara's Law<br>炒作周期与阿玛拉定律 | We tend to overestimate the effect of a technology in the short run and underestimate the impact in the long run. | 我们倾向于高估一项技术的短期效果，低估其长期影响。 |
| 52 | The Lindy Effect<br>林迪效应 | The longer something has been in use, the more likely it is to continue being used. | 一件东西被使用的时间越长，就越有可能继续被使用。 |
| 53 | First Principles Thinking<br>第一性原理 | Breaking a complex problem into its most basic blocks and then building up from there. | 把一个复杂问题拆解为最基本的模块，再从那里向上构建。 |
| 54 | Inversion<br>反转思维 | Solving a problem by considering the opposite outcome and working backward from it. | 通过考虑相反的结果并从中逆推，来解决问题。 |
| 55 | Pareto Principle<br>帕累托原则 | 80% of the problems result from 20% of the causes. | 80% 的问题来自 20% 的原因。 |
| 56 | Cunningham's Law<br>坎宁安定律 | The best way to get the correct answer on the Internet is not to ask a question, it's to post the wrong answer. | 在互联网上得到正确答案的最佳方式不是提问，而是发一个错误答案。 |
