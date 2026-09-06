---
title: "什么是贡献者许可协议（CLA）"
date: 2026-09-06T11:46:59+08:00
lastmod: 2026-09-06T11:46:59+08:00
author: "Luca"
tags: ["Tech"]
draft: false
slug: "what-is-cla"
---

最近我让 AI 给 Slax Reader 加了书签导入功能。代码提交成 PR 后，CLA Assistant 要求我先签一份协议，检查才会通过。我自己也签了一次，顺便弄清楚了 CLA 是什么。

CLA 的全称是 Contributor License Agreement，中文一般叫“贡献者许可协议”。它是代码贡献者和开源项目之间的一份协议，约定项目可以怎样使用贡献者提交的代码、文档和其他内容。

开源许可证规定别人可以怎样使用已经发布的项目。CLA 规定项目可以怎样使用别人提交进来的内容。

## 签 CLA 代表什么

具体权利要看协议文本。常见的 CLA 会要求贡献者确认几件事：

- 这份代码是自己写的，或者自己有权提交。
- 项目可以长期使用、修改和发布这份代码。
- 与这份代码有关的部分专利，也一并授权给项目使用。
- 如果代码受到雇主或第三方协议限制，需要提前说明。

贡献者一般仍然保留自己代码的版权，只是把一组明确的使用权授予项目。Apache 基金会对 CLA 的解释也是这样：贡献者保留原有权利，同时允许项目发布和继续开发这些贡献。

这份记录可以减少以后的争议。比如贡献者离职后，公司声称代码属于公司；或者项目几年后调整许可证，却发现没有权利处理早期贡献。CLA 会事先把这些问题写清楚。

有些 CLA 还允许项目把贡献放进采用其他许可证的产品，包括商业或闭源产品。这类权利适合双重许可的项目，也意味着贡献者给出的授权超过了普通开源许可证。

## 每次提 PR 都要签吗

使用 CLA Assistant 这类工具时，每个 PR 都会检查签署状态。贡献者签过当前版本后，后面的 PR 通常不用重复签。协议内容发生变化时，工具会要求重新签署。

这个步骤仍然会增加贡献门槛。修一个错字或改几行代码，也要先阅读一份法律文件。有些人看到这里就会放弃提交。

另一个轻量做法是 [DCO](https://developercertificate.org/)。贡献者在每次提交里加一行 `Signed-off-by`，确认自己有权提交这份代码。DCO 主要确认代码来源，不额外授予项目广泛的再许可权。

## Slax Reader 怎么用

Slax Reader 采用 Apache 2.0。它的[第 5 条](https://www.apache.org/licenses/LICENSE-2.0.html)已经规定，提交给项目的贡献默认使用同一份许可证，除非双方另有协议。[GitHub 服务条款](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#6-contributions-under-repository-license)也写了同样的规则。

Slax Reader 目前更需要降低参与门槛，让更多人愿意提交小改动。我的建议是先停用所有 PR 强制签 CLA 的规则。普通贡献使用 Apache 2.0 和 GitHub 的默认条款；如果想多留一份代码来源记录，可以使用 DCO。

等到 Slax Reader 确实需要双重许可、商业再授权，或者接收公司贡献的大块代码时，再启用 CLA。正式启用前，请律师检查法律主体、适用法律、专利授权和再许可范围，并给贡献者一份能看懂的说明。

CLA 本身是正常的开源治理工具。对 Slax Reader 来说，什么时候用、要求谁签，比安装一个检查机器人更重要。

参考：[Apache Contributor Agreements](https://www.apache.org/licenses/contributor-agreements.html)、[CLA Assistant](https://github.com/cla-assistant/cla-assistant)。
