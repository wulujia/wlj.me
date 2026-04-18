---
title: 'GBrain 双机部署实录'
date: 2026-04-18T20:30:00+08:00
tags: ["AI","Tools","Tech"]
draft: false
slug: "gbrain-multi-device"
---

一台常开的台式 / 常驻机负责跑重活，一台笔记本带在身边随写随记。两台机器共用一个 GBrain，写在哪台都能在另一台搜到。

下面是我把这套装起来的实际过程，包括踩到的坑。环境是两台 Mac：M2（常开）和 M4（日常，有开有关），GitHub 账号 `wulujia`，笔记放 Dropbox。

## 架构

三层，分工明确。

**Brain 仓库** = markdown 文件，源头。放 `~/Dropbox/brain/`，Dropbox 负责实时同步文件，GitHub private repo 负责版本备份。

**gbrain 工具** = 读 markdown、灌进索引的 CLI。每台机器**独立**从 GitHub clone 到**非 Dropbox** 路径，各自 `bun link`。不要让 Dropbox 同步工具源码，`node_modules` 跨机会掐架。

**索引** = PGLite（嵌入式 Postgres），默认引擎，放 `~/.gbrain/`。每台机器一份独立本地索引。markdown 是真相，索引坏了重建。

## M4（日常机）从零装起

### 1. 装 gbrain 工具

```bash
git clone https://github.com/garrytan/gbrain.git
cd gbrain && bun install && bun link
```

### 2. OPENAI_API_KEY

到 platform.openai.com 建个 project key，丢 zshrc：

```bash
echo 'export OPENAI_API_KEY="sk-proj-..."' >> ~/.zshrc
source ~/.zshrc
```

**注意变量名全大写** `OPENAI_API_KEY`。一个字母错了 OpenAI SDK 读不到，跑出来一堆 401。

账户要充 $5 以上。新账户 free quota 不够给 embedding 用，会返 429。

### 3. gbrain init

```bash
gbrain init
```

默认 PGLite，零配置。建库在 `~/.gbrain/brain.pglite/`。

### 4. 建 brain 仓库

```bash
mkdir -p ~/Dropbox/brain/{people,companies,ideas,meetings,originals,concepts}
cd ~/Dropbox/brain
for d in people companies ideas meetings originals concepts; do touch "$d/.gitkeep"; done

# README.md + .gitignore 自己写点内容
git init -b main
```

### 5. **关键**：让 Dropbox 别同步 `.git`

这是多机 git 仓库放 Dropbox 的老坑。Dropbox 如果同步 `.git/objects/`，两台机器并发写就 corrupt。

现代 macOS Dropbox 用 File Provider，要**两个 xattr 都设**，缺一个都不保险：

```bash
xattr -w com.apple.fileprovider.ignore#P 1 ~/Dropbox/brain/.git
xattr -w com.dropbox.ignored 1 ~/Dropbox/brain/.git
```

我第一次只加了老的 `com.dropbox.ignored`，两台机器跑了一会儿 `gbrain sync` 之后，`git fsck` 报 `missing tree` 和 `invalid sha1 pointer`，得从 GitHub 重拉 `.git` 才救回来。别学我。

### 6. 首次 commit + 推到 GitHub

```bash
cd ~/Dropbox/brain
git add .
git commit -m "init brain"
gh repo create wulujia/brain --private --source=. --push
```

### 7. 首次 sync + embed

```bash
gbrain sync --repo ~/Dropbox/brain
gbrain embed --stale
gbrain stats   # 看到 Pages 和 Embedded 数字
```

### 8. 接 Claude Code MCP

```bash
claude mcp add -s user gbrain -- gbrain serve
claude mcp list | grep gbrain   # ✓ Connected
```

`-s user` 是全局作用域，任何目录启动 Claude Code 都能调。

### 9. 装 autopilot

```bash
launchctl setenv OPENAI_API_KEY "$OPENAI_API_KEY"
gbrain autopilot --install --repo ~/Dropbox/brain --interval 1800
```

30 分钟跑一次 sync + extract + embed + backlinks。

第二行 `launchctl setenv` 是把 key 暴露给 launchd，不然 daemon 读不到（launchd 不 source zshrc）。

还要检查 `~/.gbrain/autopilot.err`，如果报 `env: bun: No such file or directory`，说明 launchd 环境里 PATH 没 bun。手动编辑 `~/.gbrain/autopilot-run.sh`，在 `source ~/.zshrc` 前加一行：

```bash
export PATH="/Users/<你>/.bun/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
```

然后 `launchctl unload ... && launchctl load ...` 重载。

## M2（常开机）接上来

M2 上 Dropbox 已经把 `~/Dropbox/brain/` 的 markdown 文件同步过来了，但 `.git` 目录因为 xattr 不会过来。所以 M2 要做的是：把 gbrain 工具装上、重建 `.git`、灌本地索引。

```bash
# 1. gbrain 工具（非 Dropbox 路径）
git clone https://github.com/garrytan/gbrain.git ~/gbrain
cd ~/gbrain && bun install && bun link

# 2. OPENAI_API_KEY — 你如果 zshrc 也走 Dropbox dotfile 同步，这步自动完成，
#    否则手动加一次

# 3. gbrain init
gbrain init

# 4. 给 brain 仓库加回 .git（临时 clone 然后把 .git 挪过来）
git clone git@github.com:wulujia/brain.git /tmp/brain-clone
mv /tmp/brain-clone/.git ~/Dropbox/brain/
rm -rf /tmp/brain-clone
cd ~/Dropbox/brain
xattr -w com.apple.fileprovider.ignore#P 1 .git
xattr -w com.dropbox.ignored 1 .git

# 5. 首次 sync
gbrain sync --repo ~/Dropbox/brain --no-pull
gbrain embed --stale

# 6. MCP
claude mcp add -s user gbrain -- gbrain serve

# 7. autopilot
launchctl setenv OPENAI_API_KEY "$OPENAI_API_KEY"
gbrain autopilot --install --repo ~/Dropbox/brain --interval 1800
```

`--no-pull` 这个 flag 很关键。`gbrain sync` 默认会先跑 `git pull --ff-only`，如果 git 没配好 SSH 或 credential helper，会卡在输入密码的提示。加 `--no-pull` 跳过，反正 markdown 走 Dropbox 同步，pull 是多余的。

要彻底修好 pull，把 remote 换成 SSH：
```bash
git remote set-url origin git@github.com:wulujia/brain.git
```

## Git 自动备份

Dropbox 管文件实时同步，但不做版本。每小时一次 cron 自动 commit + push：

```bash
cat > ~/Dropbox/Github/Luca/script/brain-git-backup.sh << 'EOF'
#!/bin/bash
set -u
BRAIN="$HOME/Dropbox/brain"
cd "$BRAIN" || exit 1

git pull --rebase --quiet 2>&1 || true

if [ -z "$(git status --porcelain)" ]; then
  echo "[$(date '+%F %T') $(hostname -s)] clean"
  exit 0
fi

git add .
git commit -m "auto-backup from $(hostname -s) at $(date '+%F %T')" --quiet
git push --quiet 2>&1 || echo "push failed, will retry next hour"
EOF
chmod +x ~/Dropbox/Github/Luca/script/brain-git-backup.sh
```

这个脚本放 Dropbox 同步的脚本目录，两台机器都能用。加 cron 时**错开触发分钟**，避免撞车：

```bash
# M4 crontab
15 * * * * /bin/bash $HOME/Dropbox/Github/Luca/script/brain-git-backup.sh >> $HOME/.brain-git-backup.log 2>&1

# M2 crontab（:45 错开）
45 * * * * /bin/bash $HOME/Dropbox/Github/Luca/script/brain-git-backup.sh >> $HOME/.brain-git-backup.log 2>&1
```

macOS 还要给 cron 开 **Full Disk Access**：System Settings → Privacy & Security → Full Disk Access → 加 `/usr/sbin/cron`。不然访问 Dropbox 下的文件会静默失败。

## 端到端验证

光装好不够，得跑通一次完整链路。

M2 上：
```bash
echo "# test $(date +%s)" > ~/Dropbox/brain/ideas/m2-test.md
cd ~/Dropbox/brain && git add . && git commit -m "m2 test" && git push
```

等 1-2 分钟后，M4 上：
```bash
ls ~/Dropbox/brain/ideas/m2-test.md           # Dropbox 到了吗
gbrain sync --repo ~/Dropbox/brain --no-pull  # 索引更新
gbrain embed --stale                          # embedding 生成
gbrain search "test"                          # 搜得到就通了
```

## 日常用法

写笔记就往 `~/Dropbox/brain/` 下的对应目录扔 markdown。人放 `people/`，公司放 `companies/`，想法放 `ideas/`，这些。

写完不用做任何事：

- Dropbox 把文件秒同步到另一台
- 各机 autopilot 每 30 分钟自动 sync + embed
- Cron 每小时自动 git commit + push

搜笔记在 Claude Code 里直接问"搜一下我关于 XX 的笔记"，或者终端 `gbrain search "XX"` / `gbrain query "XX"`。

## 健康检查脚本

一个小脚本，两台跑一下，7 项绿就说明装对了。放 Dropbox 脚本目录：

```bash
cat > ~/Dropbox/Github/Luca/script/gbrain-health.sh << 'EOF'
#!/bin/bash
source ~/.zshrc 2>/dev/null
echo "=== $(hostname -s)  $(date '+%F %T') ==="
echo "1. CLI:           $(gbrain --version 2>&1 | head -1)"
echo "2. Binary path:   $(which gbrain)"
echo "3. OpenAI key:    ${OPENAI_API_KEY:0:10}... (len ${#OPENAI_API_KEY})"
echo "4. Brain repo:    $([ -d ~/Dropbox/brain/.git ] && echo OK || echo MISSING)"
echo "5. Stats:"
gbrain stats 2>&1 | head -4 | sed 's/^/     /'
echo "6. MCP:           $(claude mcp list 2>&1 | grep gbrain)"
echo "7. Autopilot:     $(gbrain autopilot --status 2>&1 | head -1)"
EOF
chmod +x ~/Dropbox/Github/Luca/script/gbrain-health.sh
```

## 踩过的坑汇总

按出现频率排序：

1. **变量名大小写**。`OPENAI_API_Key` 错的，`OPENAI_API_KEY` 对的。OpenAI SDK 大小写敏感。
2. **Dropbox `.git` 同步**。两个 xattr 一起设，只设老的 `com.dropbox.ignored` 会 corrupt。
3. **OpenAI 429**。新账户免费额度不够，充 $5 就好。Project key 可能还有独立的 project budget 要设。
4. **launchd 找不到 bun**。launchd 环境的 PATH 极简，手动在 autopilot-run.sh 里 export。
5. **`gbrain sync` 卡 auth prompt**。加 `--no-pull`，或者把 remote 改 SSH。
6. **PGLite 锁冲突**。MCP server 和 autopilot 抢同一个数据库锁，等就行，或者迁 Supabase。
7. **cron 静默失败**。macOS 要给 `/usr/sbin/cron` 开 Full Disk Access。

---

这套跑起来后，脑子外挂了一层。写笔记该怎么写怎么写，搜的时候不管在哪台机器、哪个 AI 工具里问，都能翻出来。
