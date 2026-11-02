# Reading 统一验收

验收日期：2026-11-02。
部署提交：`3594afa`。
迁移主提交：`3cd0487`。

## 目标核对

| 目标 | 结果 | 证据 |
| --- | --- | --- |
| 统一现有阅读界面 | 达成 | 样式检查 80/80 通过。 |
| 手机、主题和打印可读 | 达成 | 各批截图及浏览器记录见迁移日志。 |
| 保留正文、来源和附件 | 达成 | 各批迁移比较通过，文案调整单独记录。 |
| 无脚本阅读 | 达成 | 索引和图表数据保留静态内容；公开邮箱不依赖脚本。 |
| 后续发布遵守规范 | 达成 | AGENTS.md、CLAUDE.md 和统一模板已提交。 |
| 发布检查覆盖子页 | 达成 | 子页失败、目录重叠和检查器失败测试通过。 |
| 部署拒绝不合规页面 | 达成 | GitHub Actions 在构建前执行测试、标签和样式检查。 |
| 使用文章主题标签 | 达成 | 74/74 条目通过，线上筛选与分页通过。 |
| 完成上线验收 | 达成 | 80 页及 61 张图片共 141 个文件匹配。 |

## 检查输出

```text
python3 -m unittest discover -s tests -p 'test_reading*.py'
Ran 22 tests
OK

python3 scripts/reading_tags.py check
Reading tags: 74/74 entries passed

python3 scripts/reading_style.py static/reading
Reading style: 80/80 pages passed

check_html.py 逐页检查
HTML checks: 80 / 80 passed

hugo --destination /tmp/wlj-check --minify
Pages: 3497
Static files: 493

线上文件比较
Live file verification: 141 / 141 matched
Mismatches: []

Live robots.txt PASS
Live llms.txt PASS
Live llms-full.txt PASS
Live sitemap.xml PASS
Live BlogPosting JSON-LD: PASS
```

线上比较只排除 `email_off` 控制注释。
Cloudflare 消耗该注释，但保留邮箱正文。
其余内容按 SHA-256 比较。

## 浏览器检查

线上标签筛选、分页和刷新恢复均通过。
320、500、1280 像素宽度没有整页横向溢出。
关闭脚本时，列表显示全部 74 条资料。

线上抽查《权力掮客》、AI 滥用报告及《周易》。
三页的主题、目录、打印及无脚本检查通过。
此前全部页面已完成本地截图与功能检查。
各批结果见 `20261102-reading-progress.md`。

## 部署证据

- 首次部署：[41429122477](https://github.com/wulujia/wlj.me/actions/runs/41429122477)，成功。
- 邮箱修复：[41429736047](https://github.com/wulujia/wlj.me/actions/runs/41429736047)，成功。
- 入口：[wlj.me/reading](https://wlj.me/reading/)。

## 限制与后续执行

AI 滥用报告的 61 张图片使用本站路径。
这些图片与页面一起发布，原始字节未变。
离线完整浏览该报告需要本地静态服务。
单独复制 HTML 不包含这些图片。

本次保留原有材料的事实和判断。
本次没有重新研究或核实原作中的所有主张。
文案检查的逐行核对见独立记录。

新页面从 `templates/reading/index.html` 开始。
发布使用 `publish.sh reading`。
主题标签沿用文章已有英文标签，每条 1–5 个。
批量标签更新使用 `publish.sh reading-tags`。

## 本次发现

- 原有脚本生成的数据影响无脚本阅读。
  将可读内容写入 HTML，再保留筛选交互。
- 本机测试曾依赖已安装的检查器。
  测试现已隔离；生产发布仍要求完整检查器。
- Cloudflare 会改写公开邮箱。
  线上验收需检查 CDN 转换后的正文。
