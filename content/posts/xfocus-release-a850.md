---
title: "通用弱点评价体系（CVSS）简介"
date: 2006-02-08T00:00:00+08:00
tags: ["Security"]
draft: false
slug: "xfocus-release-a850"
---

[http://www.xfocus.net](http://www.xfocus.net/)

一、综述

弱点（vulnerabilities）是网络安全中的一个重要因素，在多种安全产品（如漏洞扫描、入侵检测、防病毒、补丁管理等）中涉及到对弱点及其可能造成的影响的评价。但目前业界并没有通用统一的评价体系标准。通用弱点评价体系（CVSS）是由NIAC开发、FIRST维护的一个开放并且能够被产品厂商免费采用的标准。利用该标准，可以对弱点进行评分，进而帮助我们判断修复不同弱点的优先等级。

二、通用弱点评价体系（CVSS）

2.1 CVSS的要素

通过下图可以看出通用弱点评价体系（CVSS）包含的要素及它们之间的相互关系：

[CVSS-model-detailed-8.0.jpg](/web/20121011103602/http://xfocus.net/articles/200602/CVSS-model-detailed-8.0.jpg)

通用弱点评价体系（CVSS）的所有要素及其取值范围如下表所示：

[CVSS-metric.jpg](/web/20121011103602/http://xfocus.net/articles/200602/CVSS-metric.jpg)

有些需要说明的要素如下：

1、如果漏洞既可远程利用，又可以本地利用，取值应该为远程利用的分值。

2、攻击复杂度的分值由原先的低/高变为低/中/高，参见：[http://www.first.org/cvss/draft/accepted/060103.html](http://www.first.org/cvss/draft/accepted/060103.html)

3、需要认证的例子，如需要预先有Email、FTP帐号等。

有些有用的参考资源如下：

CVSS评分计算器：[http://nvd.nist.gov/cvss.cfm?calculator](http://nvd.nist.gov/cvss.cfm?calculator)

CVSS的最近更新：[http://www.first.org/cvss/draft/](http://www.first.org/cvss/draft/)

一些文档及胶片：[http://www.first.org/cvss/links.html](http://www.first.org/cvss/links.html)

2.2 CVSS评分方法

2.2.1 基本评价

基本评价指的是该漏洞本身固有的一些特点及这些特点可能造成的影响的评价分值，该分值取值如下：

AccessVector     = case AccessVector of

                        local:            0.7 

                        remote:           1.0

                         

AccessComplexity = case AccessComplexity of

                        high:             0.6

                        medium:           0.8

                        low:              1.0

                             

Authentication   = case Authentication of

                        required:         0.6

                        not-required:     1.0

                             

ConfImpact       = case ConfidentialityImpact of

                        none:             0

                        partial:          0.7

                        complete:         1.0

                             

ConfImpactBias   = case ImpactBias of

                        normal:           0.333

                        confidentiality:  0.5

                        integrity:        0.25

                        availability:     0.25

                             

IntegImpact      = case IntegrityImpact of

                        none:             0

                        partial:          0.7

                        complete:         1.0

                             

IntegImpactBias  = case ImpactBias of

                        normal:           0.333

                        confidentiality:  0.25

                        integrity:        0.5

                        availability:     0.25

                             

AvailImpact      = case AvailabilityImpact of

                        none:             0

                        partial:          0.7

                        complete:         1.0

                             

AvailImpactBias  = case ImpactBias of

                        normal:           0.333

                        confidentiality:  0.25

                        integrity:        0.25

                        availability:     0.5

BaseScore = round_to_1_decimal(10 * AccessVector

                                  * AccessComplexity

                                  * Authentication

                                  * ((ConfImpact * ConfImpactBias)

                                  + (IntegImpact * IntegImpactBias)

                                  + (AvailImpact * AvailImpactBias)))

2.2.2 生命周期评价

因为漏洞往往同时间是有紧密关联的，因此这里也列举出三个与时间紧密关联的要素如下：

Exploitability   = case Exploitability of

                        unproven:             0.85

                        proof-of-concept:     0.9

                        functional:           0.95

                        high:                 1.00

                        

RemediationLevel = case RemediationLevel of

                        official-fix:         0.87

                        temporary-fix:        0.90

                        workaround:           0.95

                        unavailable:          1.00

                        

ReportConfidence = case ReportConfidence of

                        unconfirmed:          0.90

                        uncorroborated:       0.95      

                        confirmed:            1.00

TemporalScore = round_to_1_decimal(BaseScore * Exploitability

                                             * RemediationLevel

                                             * ReportConfidence)

2.2.3 环境评价

每个漏洞会造成的影响大小都与用户自身的实际环境密不可分，因此可选项中也包括了环境评价，这可以由用户自评。

CollateralDamagePotential = case CollateralDamagePotential of

                                 none:            0

                                 low:             0.1

                                 medium:          0.3   

                                 high:            0.5      

                                 

TargetDistribution        = case TargetDistribution of

                                 none:            0

                                 low:             0.25

                                 medium:          0.75

                                 high:            1.00

EnvironmentalScore = round_to_1_decimal((TemporalScore + ((10 - TemporalScore)

                                         * CollateralDamagePotential))

                                         * TargetDistribution)

三、示例

3.1 一个漏洞的评分实例

这个例子是Apache Web Server分块编码远程溢出漏洞，该漏洞的描述为（参考[http://www.nsfocus.net/vulndb/2975](http://www.nsfocus.net/vulndb/2975)）：

Apache在处理以分块(chunked)方式传输数据的HTTP请求时存在设计漏洞，远程攻击者可能利用此漏洞在某些Apache服务器上以Web服务器进程的权限执行任意指令或进行拒绝服务攻击。

分块编码(chunked encoding)传输方式是HTTP 1.1协议中定义的Web用户向服务器提交数据的一种方法，当服务器收到chunked编码方式的数据时会分配一个缓冲区存放之，如果提交的数据大小未知，客户端会以一个协商好的分块大小向服务器提交数据。

Apache服务器缺省也提供了对分块编码(chunked encoding)支持。Apache使用了一个有符号变量储存分块长度，同时分配了一个固定大小的堆栈缓冲区来储存分块数据。出于安全考虑，在将分块数据拷贝到缓冲区之前，Apache会对分块长度进行检查，如果分块长度大于缓冲区长度，Apache将最多只拷贝缓冲区长度的数据，否则，则根据分块长度进行数据拷贝。然而在进行上述检查时，没有将分块长度转换为无符号型进行比较，因此，如果攻击者将分块长度设置成一个负值，就会绕过上述安全检查， Apache会将一个超长(至少>0x80000000字节)的分块数据拷贝到缓冲区中，这会造成一个缓冲区溢出。

对于1.3到1.3.24(含1.3.24)版本的Apache，现在已经证实在Win32系统下, 远程攻击者可能利用这一漏洞执行任意代码。在UNIX系统下，也已经证实至少在OpenBSD系统下可以利用这一漏洞执行代码。据报告称下列系统也可以成功的利用：

*      Sun Solaris 6-8 (sparc/x86)

*      FreeBSD 4.3-4.5 (x86)

*      OpenBSD 2.6-3.1 (x86)

*      Linux (GNU) 2.4 (x86)

对于Apache 2.0到2.0.36(含2.0.36)，尽管存在同样的问题代码，但它会检测错误出现的条件并使子进程退出。

根据不同因素，包括受影响系统支持的线程模式的影响，本漏洞可导致各种操作系统下运行的Apache Web服务器拒绝服务。

在CVSS评价中，它的示例如下：

        ----------------------------------------------------

        BASE METRIC                 EVALUATION         SCORE

        ----------------------------------------------------

        Access Vector               [Remote]          (1.00)

        Access Complexity           [Low]             (1.00)

        Authentication              [Not-Required]    (1.00)

        Confidentiality Impact      [Partial]         (0.70)

        Integrity Impact            [Partial]         (0.70)

        Availability Impact         [Complete]        (1.00)

        Impact Bias                 [Availability]    (0.25)

        ----------------------------------------------------

        BASE FORMULA                              BASE SCORE

        ----------------------------------------------------

        round(10 * 1.0 * 1.0 * 1.0 * (0.7 * 0.25) + 

             (0.7 * 0.25) + (1.0 * 0.5)) ==           (8.50)

        ----------------------------------------------------

 

        ----------------------------------------------------

        TEMPORAL METRIC             EVALUATION         SCORE

        ----------------------------------------------------

        Exploitability              [Functional]      (0.95)

        Remediation Level           [Official-Fix]    (0.90)

        Report Confidence           [Confirmed]       (1.00)

        ----------------------------------------------------

        TEMPORAL FORMULA                      TEMPORAL SCORE

        ----------------------------------------------------

        round(8.50 * 0.95 * 0.90 * 1.00) ==           (7.00)

        ----------------------------------------------------

        ----------------------------------------------------

        ENVIRONMENTAL METRIC        EVALUATION         SCORE

        ----------------------------------------------------

        Collateral Damage Potential [None - High]  {0 - 0.5}

        Target Distribution         [None - High]  {0 - 1.0}

        ----------------------------------------------------

        ENVIRONMENTAL FORMULA            ENVIRONMENTAL SCORE

        ----------------------------------------------------

        round((7.0 + ((10 - 7.0) * {0 - 0.5})) * 

             {0 - 1.00}) ==                    (0.00 - 8.50)

        ----------------------------------------------------

3.2 漏洞评分表图例

这里是一个CVSS表格的例子：

[CVSS-sample.jpg](/web/20121011103602/http://xfocus.net/articles/200602/CVSS-sample.jpg)

该例可以从以下地址下载：

样例：[http://www.unnoo.com/files/uploadfile/research/cvss-sample-1.1draft1.xls](http://www.unnoo.com/files/uploadfile/research/cvss-sample-1.1draft1.xls)

空白表格：[http://www.unnoo.com/files/uploadfile/research/cvss-blank-scoring-1.1draft1.xls](http://www.unnoo.com/files/uploadfile/research/cvss-blank-scoring-1.1draft1.xls)

四、应用实例

4.1 Nessus中的应用

在比较流行的免费漏洞扫描工具Nessus中，已经部份地将CVSS中的基本评价（Base Score）用于进行漏洞评价，取代了原先的“Risk factor”取值，举例而言：

ASP-DEv XM Forum IMG Tag Script Injection Vulnerability的Risk factor现在描述如下：

Medium / CVSS Base Score : 5

(AV:R/AC:L/Au:NR/C:P/A:N/I:P/B:N)";

这段话的含义为：该漏洞的影响为中，CVSS基本评价分值为5分，其中分项取值表格

        ----------------------------------------------------

        BASE METRIC                 EVALUATION         SCORE

        ----------------------------------------------------

        Access Vector               [Remote]          (1.00)

        Access Complexity           [Low]             (1.00)

        Authentication              [Not-Required]    (1.00)

        Confidentiality Impact      [Partial]         (0.70)

        Integrity Impact            [Partial]         (0.70)

        Availability Impact         [None]            (0.00)

        Impact Bias                 [Normal]          (0.333)

        ----------------------------------------------------

        BASE FORMULA                              BASE SCORE

        ----------------------------------------------------

        round(10 * 1.0 * 1.0 * 1.0 * (0.7 * 0.333) + 

        (0.7 * 0.333) + (1.0 * 0.333)) ==           (4.66)

4.2 推荐使用甚至CVSS的补丁策略

一个可选的CVSS补丁策略可以是将补丁的优先权分为Patch Level 1-4，每个等级有不同的应对方式：

CVSS分值　　优先级别　　补丁SLA

  0           P4        可以自由决定

 1-3          P3        3-6个月

 4-6          P2        最多4周

 7-10         P1        最多2周

五、参照：微软威胁评价体系介绍

在微软的漏洞威胁评价体系中，包括以下几方面的要素：

Microsoft Product Vulnerability:Yes/No/Patch Not Available

Vectors of Attack

New Vector of Attack:Yes/No

Distribution Potential:High/Medium/Low

Unique Data Destruction:Yes/No

Significant Service Disruption:Yes/No

微软在补丁发布时会有漏洞危急程度的描述，如：CRITICAL、MODERATE等等，都是基于以上要素进行分析的结果，例如CRTTICAL级别漏洞，各要素的取值范畴为：

[Microsoft-score.jpg](/web/20121011103602/http://xfocus.net/articles/200602/Microsoft-score.jpg)

当然，作为商业评价体系，微软的漏洞评价方法公开部份有限，因此仅能作为参考。

六、参考资料

1. A Complete Guide to the Common Vulnerability Scoring System(CVSS)

2. PSS Security Team - Security Alert Severity Matrix

3. The Common Vulnerability Scoring System

4. CVSS FAQ

5. CERT Vulnerability Scoring

6. Example of CVSS base patching policy

欢迎交流讨论，联系方式：

wulujia@unnoo.com

[http://www.unnoo.com](http://www.unnoo.com/)
