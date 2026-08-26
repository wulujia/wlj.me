---
title: "备份公司邮箱的三种办法"
date: 2026-08-26T17:09:23+08:00
lastmod: 2026-08-26T17:09:23+08:00
author: "Luca"
tags: ["Tools","Ops"]
draft: false
slug: "backup-work-email"
---

企业微信邮箱、腾讯企业邮箱，网页端和客户端都只能一封一封另存，没有批量导出。想把几年的邮件整个拿到手，得走 IMAP。

三条路：Mac 自带的邮件 App 导出、imapsync 搬到 Gmail、自己写脚本存本地。共同前提是先开 IMAP。

## 先开 IMAP

网页登录企业邮箱：

1. 设置 → 收发信设置 → 开启 IMAP/SMTP 服务
2. 设置 → 邮箱绑定 → 看"安全登录"开没开。开了就生成一个客户端专用密码，下面三种办法都用它，不用邮箱密码
3. 服务器 `imap.exmail.qq.com`，端口 993，SSL

账号被公司回收之后什么都拿不了，要备份趁还能登录。

## 一、Mac 邮件 App 导出

邮件 → 添加账户 → 其他邮件账户，填地址和客户端专用密码，服务器手填上面那个。等它把邮件同步完，几万封要一两个小时。

然后选中左边的邮箱，菜单 邮箱 → 导出邮箱，选一个文件夹。每个邮箱导出成一个 `.mbox`。

- 好处：不用装东西，附件都在里面
- 坏处：`.mbox` 是一个大文件，几年邮件轻松上 GB，搜索只能靠再导回某个邮件客户端。Apple 的导入功能对超过 2 GB 的 mbox 会出问题，导出时按邮箱分开导，别一次全选

适合：一次性存档，存完基本不再翻。

## 二、imapsync 搬到另一个邮箱

不落地本地文件，直接把邮件复制到 Gmail 或 Fastmail。

```bash
brew install imapsync

imapsync --host1 imap.exmail.qq.com --user1 you@company.com --password1 '客户端专用密码' \
         --host2 imap.gmail.com   --user2 you@gmail.com   --password2 '应用专用密码' \
         --gmail2
```

默认全量：所有文件夹所有邮件，保留时间和已读状态。再跑一遍是增量的，按 Message-ID 跳过搬过的。不加 `--delete1` / `--delete2` 它不删任何东西，源邮箱后来删掉的邮件目标那边还留着。

第一次跑前先 `--dry` 空跑一遍看文件夹怎么映射。

Gmail 那边要先开两步验证再生成应用专用密码，普通密码登不了 IMAP。Gmail 的 IMAP 每天限上传 500 MB，几 GB 的邮箱要跑好几天，`--gmail2` 会自动限速避开配额，顺便把"已发送"映射到 `[Gmail]/Sent Mail`。Fastmail 没有每日配额，也不需要这个开关。

- 好处：一条命令，搜索直接用 Gmail 的
- 坏处：邮件还在别人服务器上。Gmail 账号出问题就一起没了

适合：日常还要查、要用手机看。

## 三、自己写脚本存本地

让 AI 写了一个：[exmail-backup](https://github.com/wulujia/exmail-backup)，纯 Python 标准库，一个文件，跑在 macOS 自带的 Python 3 上。

它做两件事：把每封邮件按原样存成 `.eml` 文件，同时建一个 SQLite 全文索引。

```
~/Mail/exmail/
├── INBOX/1234.eml
├── 已发送/88.eml
└── index.sqlite
```

用法：

```bash
python3 exmail_backup.py set-password        # 密码进钥匙串
python3 exmail_backup.py sync -v             # 增量拉

python3 exmail_backup.py search 发票
python3 exmail_backup.py search "合同 附件" --since 2025-01-01
python3 exmail_backup.py search --from alice --attachment
python3 exmail_backup.py show 1234           # 正文和附件名
python3 exmail_backup.py open 1234           # 用邮件 App 打开，附件在里面
```

几个设计上的取舍：

**只读。** 只读 SELECT 加 `BODY.PEEK`，不改已读状态，不删任何东西。服务器上删了的本地照样留着——这是备份该有的样子。

**一封一个文件。** 不用 mbox 那种大文件，坏一个不影响其他。索引坏了 `reindex` 从文件重建。

**中文能搜。** SQLite 的 FTS5 不认中文分词，所以建索引时把每个汉字之间插空格，查询时整个词当短语匹配。结果是"发票"能搜到，"票发"搜不到，单字也能搜。

**能中断。** 每个文件夹记到哪个 UID 了，每 100 封提交一次。Ctrl-C 之后再跑接着来。

定时的话 crontab 加一行：

```
0 */6 * * * /usr/bin/python3 ~/path/to/exmail_backup.py sync >> ~/Mail/exmail/sync.log 2>&1
```

- 好处：文件在自己硬盘上，能 grep，能进 Time Machine，格式是标准的 `.eml` 任何邮件客户端都能打开
- 坏处：得自己跑，出问题得自己修。索引和检索那部分有测试覆盖，连真实邮箱拉数据那段还没实跑过，第一次用建议先 `--folder INBOX` 只拉一个文件夹看看

适合：当保险箱，几年后还要能翻出来。

## 怎么选

存档一次就完的，用 Mac 邮件 App。日常还要查的，imapsync 搬 Gmail。要留一份自己完全掌控的，用脚本。

三个不冲突，同一个邮箱可以同时用两种。

## 管理员的补充

如果你是企业邮箱管理员，管理后台 → 工具箱 → 邮件备份，可以设规则把指定成员的邮件自动抄一份到备份邮箱。注意它只管开启之后的新邮件，历史邮件一封不备份。存量还是得走上面三条路之一。
