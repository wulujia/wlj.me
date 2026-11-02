# Reading 页面检查基线

检查日期：2026-11-02。检查范围：全部整理页及专题子页。

共 80 个 HTML 页面。46 页通过，34 页有错误或警告。
通过检查仅说明满足现有检查项，不代表风格一致。

## 检查方法

逐页调用现有 HTML 检查器的 `check_file`。
失败统计包含 error 和 warning，不包含 style。
检查器同时检查结构、主题和正文用语。

## 差异

- 60 页使用 `nav.outline`，其他页面使用不同导航结构。
- 4 页没有 main 元素。
- 13 页缺少检查器要求的手动暗色规则。
- 16 页的目录缺少三级标题。
- 3 页缺少目录。
- 发布脚本只检查入口页，未递归检查专题子页。
- 部署流程直接构建，没有整理页规范检查。

## 未通过页面

| 页面 | 错误或警告类别及次数 |
| --- | --- |
| amos-atomic-macos-stealer-2026-10 | outline-h3 × 1 |
| before-vegas-red-hackers | outline-h3 × 1；prose-contrast × 2；prose-inflation × 1；prose-jargon × 7；theme-toggle × 1 |
| caresexpo-2026-taxonomy | prose-jargon × 28 |
| clio-privacy-preserving-insights-2024-12 | prose-attribution × 1；prose-cliche × 3；prose-contrast × 1；prose-jargon × 41；prose-preempt × 2；prose-rider × 1 |
| crash-exploit-and-burn | heading-skip × 3；outline-h3 × 1；prose-contrast × 3；prose-jargon × 4；prose-rider × 1；theme-toggle × 1 |
| crunchbase | outline-h3 × 1 |
| dario-amodei-pace-the-frontier-2026-09 | prose-attribution × 1；prose-cliche × 2；prose-contrast × 3；prose-jargon × 21 |
| decluttering-at-the-speed-of-life | heading-skip × 4；outline-h3 × 1；prose-cliche × 1；prose-contrast × 10；prose-jargon × 1；prose-preempt × 1；theme-toggle × 1 |
| detecting-and-countering-ai-misuse-2026-09 | ai-byline × 1；h1 × 1；h2-id × 1；outline-h2 × 1；prose-attribution × 1；prose-cliche × 1；prose-contrast × 7；prose-jargon × 41；prose-preempt × 3；prose-value × 1；size × 1；viewport × 1 |
| digital-minimalism | heading-skip × 5；outline-h3 × 1；prose-contrast × 16；prose-inflation × 2；prose-jargon × 5；theme-toggle × 1 |
| longing-for-less | heading-skip × 4；outline-h3 × 1；prose-contrast × 2；prose-jargon × 1；theme-toggle × 1 |
| mobilizing-cyber-power | heading-skip × 2；outline-h3 × 1；prose-contrast × 4；prose-jargon × 8；theme-toggle × 1 |
| mythical-beasts-spyware-market | heading-skip × 1；outline-h3 × 1；prose-contrast × 3；theme-toggle × 1 |
| openai-huggingface-incident-2026-09/anthropomorphic-loss-of-control | prose-inflation × 1 |
| openai-huggingface-incident-2026-09/blackhat-usa-2026-talk | prose-jargon × 10；prose-preempt × 2 |
| openai-huggingface-incident-2026-09/hf-agent-replay-collection | prose-jargon × 3 |
| openai-huggingface-incident-2026-09 | ai-byline × 1；prose-contrast × 1；theme-toggle × 1 |
| openai-huggingface-incident-2026-09/metr-investigation-report | prose-contrast × 3；prose-inflation × 4；prose-jargon × 2；prose-preempt × 4 |
| openai-huggingface-incident-2026-09/openai-technical-report | prose-contrast × 1；prose-jargon × 55；prose-preempt × 1 |
| openclaw-open-source-ops | placeholder × 1；prose-contrast × 1 |
| product-hunt | outline-h3 × 1 |
| quanzhou-old-town-housing | outline-h3 × 1 |
| sam-altman-fortune-titans-2026-09 | prose-contrast × 1；prose-jargon × 33；prose-preempt × 2 |
| science-new-golden-age | heading-skip × 3；outline-h3 × 1；prose-inflation × 6；prose-jargon × 4；theme-toggle × 1 |
| singapore-esr-2026 | h2-id × 8；outline × 1 |
| singapore-government-revenue | h2-id × 5；outline × 1；print-css × 1；theme-toggle × 1 |
| slax-reader-project-guide | outline-h3 × 1；prose-jargon × 3 |
| techcrunch | outline-h3 × 1 |
| temasek-review-2026 | outline-h3 × 1；prose-inflation × 1；theme-toggle × 1 |
| the-power-broker | full-viewport-hero × 1；heading-skip × 2；outline × 1；prose-cliche × 1；prose-contrast × 1；prose-jargon × 2 |
| the-up-series | outline-h2 × 1；outline-h3 × 1；theme-toggle × 1 |
| tobi-lutke-ai-judgment-2026-09 | prose-contrast × 1；prose-jargon × 1 |
| zhangxiaojun-zengming-industry-history-2026-09 | prose-announce × 1；prose-cliche × 8；prose-closer × 1；prose-contrast × 2；prose-inflation × 11；prose-jargon × 26；prose-preempt × 1 |
| zhouyi-jingzhuan-15-lectures | full-viewport-hero × 1；heading-skip × 1；prose-attribution × 2；prose-cliche × 1；prose-inflation × 1；theme-toggle × 1 |

## 迁移注意事项

检查器提示仍需逐项判断。
引用、专有名词和代码中的命中可能是误报。
不得为通过检查删除事实、附件或来源。
目录、标题和布局改动需要保留原有锚点。
双语报告约 14MB，需单独处理图片体积。

## 验证范围

本记录是迁移前基线。尚未修改现有页面。
截图、交互和发布拒绝测试将在迁移后执行。
基线没有重新核查正文事实及外部链接状态。
