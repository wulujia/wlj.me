---
title: "METR：经费、团队与非营利研究机构是什么意思"
date: 2026-09-14T16:06:29+08:00
lastmod: 2026-09-14T16:06:29+08:00
author: "Luca"
tags: ["AI","Reading"]
draft: false
slug: "metr-nonprofit-funding-team"
---

METR（Model Evaluation & Threat Research，读作 meter）是一家评估前沿 AI 模型能力与灾难性风险的美国非营利研究机构。本页回答三件事：它说的 “nonprofit research institute” 在法律上是什么意思、钱从哪来、谁在做。

取样截至 2026-09-14主要来源：metr.org About / 博客地点：Berkeley, CA

先说结论

METR 是美国联邦税法下的 501(c)(3) 免税慈善机构，法人名 Model Evaluation and Threat Research，EIN 99-1219864；没有私人股东，盈余留在使命内。 生存主要靠捐赠：2024 年 10 月 The Audacious Project 促成的 Canary 合作里，约 3800 万美元总额中约 1700 万美元支持 METR；2026 年 8 月 14 日自报过去 6 个月获得约 7100 万美元承诺。 创始人兼 CEO 是 Beth Barnes（2022 年离开 OpenAI，先在 Alignment Research Center 下做 ARC Evals，2023 年 12 月独立并改名 METR）；领导层还有 President Chris Painter、Chief Scientist Hjalmar Wijk、CTO Nate Rush。

## 非营利研究机构是什么意思

METR 自称 nonprofit research institute。落到美国法律上，对应的是 501(c)(3) 免税慈善组织：为公共利益做研究与教育，向 IRS 登记后，合格捐赠人在美国税法下可申请抵扣。

### 501(c)(3) 在说什么

- 没有私人股东，也不能把利润分给“所有人”。

- 若有盈余，继续用于章程写明的公益使命（对 METR 来说是评估方法与风险评估研究）。

- 组织本身在符合条件时免缴联邦所得税；捐赠人是否能抵税，取决于美国税法与捐赠人身份，本页不展开各国税制。

About 页写明其定位是独立第三方：用可公开的方法评估前沿系统的自主能力与相关风险，并在可能时公开发表。

### 容易混淆的几种说法

      METR 是什么、不是什么
      说法是否适用依据

        美国政府机构否独立 501(c)(3)；可与 NIST、欧盟 AI 办公室等合作，本身不是行政当局
        营利初创公司（暂不分红）否无股权结构、无利润分配；捐赠为主，不是 VC 轮次融资
        前沿实验室的子公司或评估部门否自报未接受 AI 公司资金；合作方提供评测用 token 与试点评估入口
        公益研究 / 教育慈善机构是IRS 免税登记；使命写在 About 与 2023 年独立公告

### METR 的法人登记

    法人名Model Evaluation and Threat Research
    EIN99-1219864
    免税起始ProPublica Nonprofit Explorer 标注自 2024 年 3 月起免税
    驻地Berkeley, California（Wikipedia）
    读音 / 全称METR，读作 meter；Model Evaluation & Threat Research，名字呼应计量学（metrology）

  待确认GuideStar / Candid 档案页需登录才能看完整 Form 990 明细；本页 EIN 以 ProPublica Nonprofit Explorer 公开页为准，不编造 2025/2026 年报收入行。

## 生存模式与经费

About 页第一句写：METR is funded by donations。 下面按规模与时间拆开。

### 主要靠捐赠

日常运转依赖机构与个人捐赠。另有一小笔合同收入：向欧洲 AI 办公室（European AI Office）提供失控风险（loss of control）评估方法的技术援助。 这笔合同在 About 里被写成 “a small part of our income”，不是主渠道。

### Audacious 约 1700 万美元

2024 年 10 月 9 日，METR 发文称 The Audacious Project（设于 TED 的协作资助计划）促成约 3800 万美元给 Canary——METR 与 RAND 的合作项目，用于开发和部署危险能力评估。其中约 1700 万美元支持 METR 的工作。 About 页把这笔钱称作 METR 的 “first institutional-scale funding”。

    ~$38MCanary 总额（Audacious 促成）
    ~$17M其中支持 METR（2024-10）
    ~$71M近 6 个月承诺（截至 2026-08）

  说明以上三笔均为 METR / Audacious 侧自报的 “approximately / around” 数字，不是经审计后的到账明细。

### 2026 年约 7100 万美元承诺

2026 年 8 月 14 日博客 Funding update：过去 6 个月获得约 7100 万美元 commitments（承诺），用于自主能力、递归自我改进追踪、监控系统评估、风险评估、AI 事件调查等。

  待确认“commitments” 是否已全部到账、分几年拨付、与 Audacious 旧承诺是否有重叠，公开文未拆开；完整 Form 990 行项需登录 GuideStar，本页不估算年收入。

### 具名支持者

About 页列出的支持者类别与名字（2026-09 取样）：

- The Audacious Project（TED 旗下资助倡议）

- 来自 Jane Street 的个人

- 基金会：Sijbrandij Foundation、The Pew Charitable Trusts、Schmidt Sciences、Packard Foundation、LaCentra-Sumerlin Foundation、Astralis Foundation、Expa.org

- AI Security Institute

- 汇集基金：Longview Philanthropy、Effektiv Spenden

- Survival and Flourishing Fund 的推荐

- 个人：David Farhi、Geoff Ralston、Dylan Field、Steve Newman

### 接受与拒绝什么钱

- 未接受 AI 公司的资金（has not accepted funding from AI companies）。

- 拒绝由前沿 AI 公司员工本人或按其指示作出的捐赠。

- 接受前沿实验室提供的大量免费 token，用于评测、研究与工程。

- 独立资金被写成选择研究方向、设定证据标准的前提。

## 创始人与领导层

Beth Barnes 是创始人兼 CEO。她 2022 年离开 OpenAI，加入 Paul Christiano 创办的 Alignment Research Center（ARC），在其下孵化评估团队 ARC Evals。

2023 年 9 月，ARC Evals 宣布从 ARC 分拆；同年 12 月 4 日正式改为独立 501(c)(3)，并更名为 METR。原计划请 Paul Christiano 任董事与顾问，他因出任美国 AI Safety Institute 的 Head of Safety 而拒绝。

      领导层（About，约 2026-09）
      姓名职位

        Beth BarnesFounder, CEO
        Chris PainterPresident
        Hjalmar WijkChief Scientist
        Nate RushCTO

  说明“Partners” 在 About 里指合作做试点评估的实验室与机构，没有股权合伙含义。创始人只有公开材料里的 Beth Barnes；Paul Christiano 是孵化期所在机构 ARC 的负责人，不是 METR 的联合创始人或现任董事。

## 团队结构

以下人数按 2026-09-14 抓取的 About 名册清点。页面可能滞后于实际招聘；2026 年 8 月融资更新写明团队在显著扩编。

      About 名册分组清点（取样日 2026-09-14）
      分组人数备注

        Leadership4上表
        Technical Staff21另有 1 名 Research Contractor
        Operations Staff7含 Director of Operations
        Policy Staff4—
        名册合计（不含顾问）374+21+1+7+4；顾问、合作者另计

### 技术与研究

Technical Staff 约 21 人，另有 Research Contractor Khalid Mahamud。公开名单中较常被提到的名字包括 Ajeya Cotra、Tom Cunningham、Megan Kinniment、David Rein、Bruce Lee 等。 完整名单见 About 页 “Technical Staff” 一节。

### 运营与政策

运营由 Stephanie Palla（Director of Operations）带队，另有约 6 名运营职员。政策组四人：Charles Foster、Jasmine Dhaliwal、Kit Harris、Rox Heston。

### 顾问

Advisors：Adam Gleave、Alec Radford、Marco Mascorro、Rajiv Dattani、Yoshua Bengio。另有 Research Collaborator Alexander Barry、Specialist Partner Kai Nguyen。

## 与 AI 公司的关系

关系拆成两层：评测合作与免费 token，以及资金上的隔离。

### 合作评估方

About 写：此前与 OpenAI、Anthropic、Google DeepMind、Meta、Amazon 合作试点前沿风险评估；这些公司也提供访问权限与 token，用于评测、研究与工程。 他们是合作评估方，不是股权合伙人或母公司。

- 资金：不收 AI 公司捐款，也不收其员工按公司指示的捐赠。

- 算力 / API：接受大量免费 token。

- 工作内容：试点评估、系统卡相关评测等（具体项目见各模型发布材料与 METR 博客）。

### 政府与标准机构

- NIST AI Safety Institute Consortium 成员

- California Cybersecurity Task Force

- 与 AI Security Institute 合作

- 向欧洲 AI 办公室提供技术援助（失控风险评估方法）

## 时间线

- 2022Beth Barnes 离开 OpenAI，加入 ARC，孵化 ARC Evals。

- 2023-09ARC Evals 宣布从 ARC 分拆；Beth 领导新实体，Paul 留任 ARC。

- 2023-12独立 501(c)(3)，更名 METR；Paul Christiano 因美国 AISI 职务拒绝入董事会。

- 2024-03ProPublica 标注免税起始（EIN 99-1219864）。

- 2024-10Audacious / Canary：约 3800 万美元合作总额，约 1700 万美元支持 METR。

- 2026-08Funding update：过去 6 个月约 7100 万美元 commitments。

## 方法与来源

事实以 METR 官网 About 与博客为主；法人 EIN 用 ProPublica Nonprofit Explorer 公开页；驻地与早期履历对照 Wikipedia。取样日 2026-09-14。未拿到：GuideStar 登录后的完整 Form 990 行项、承诺款到账节奏、精确在职人数的人事系统口径。Audacious 约 1700 万美元与约 7100 万美元承诺均按机构自报文记录，标为自报。

- ProPublica Nonprofit Explorer，《Model Evaluation And Threat Research》，EIN 99-1219864，projects.propublica.org/nonprofits/organizations/991219864（https://projects.propublica.org/nonprofits/organizations/991219864）

- METR，《New Support Through The Audacious Project》，2024-10-09，metr.org/blog/2024-10-09-new-support-through-the-audacious-project（https://metr.org/blog/2024-10-09-new-support-through-the-audacious-project/）

- METR，《Funding update》，2026-08-14，metr.org/blog/2026-08-14-funding-update（https://metr.org/blog/2026-08-14-funding-update/）

- METR，《About METR》，取样 2026-09-14，metr.org/about（https://metr.org/about/）

- Wikipedia，《METR》，驻地 Berkeley, CA；Beth Barnes / ARC Evals 简述，en.wikipedia.org/wiki/METR（https://en.wikipedia.org/wiki/METR）

- METR，《ARC Evals is now METR》，2023-12-04，metr.org/blog/2023-12-04-metr-announcement（https://metr.org/blog/2023-12-04-metr-announcement/）

- METR / Beth Barnes，《ARC Evals is spinning out from ARC》，2023-09-19，metr.org/blog/2023-09-19-spin-out-announcement（https://metr.org/blog/2023-09-19-spin-out-announcement/）
