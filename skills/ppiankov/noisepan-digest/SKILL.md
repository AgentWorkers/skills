---
name: noisepan-digest
description: 使用 noisepan（信号提取）、entropia（来源验证）和 HN blind spot detection（HN 盲点检测）来设置自动化的新闻摘要生成系统。该系统可用于配置每日新闻简报、整理 RSS 源，或构建替代人工新闻浏览的自动化智能处理流程。
metadata: {"openclaw":{"requires":{"bins":["noisepan","entropia"]}}}
---
# Noisepan 摘要

这是一个自动化的新闻情报工具，具备来源验证功能，旨在替代无目的的滚动浏览行为。每天会生成两篇新闻摘要。

**数据来源：**
- https://github.com/ppiankov/noisepan （信号提取）
- https://github.com/ppiankov/entropia （来源验证）

**所需软件：** `noisepan`、`entropia`、`python3`、`curl`

## 安装

### macOS（推荐使用 Homebrew）

```bash
brew install ppiankov/tap/noisepan ppiankov/tap/entropia
noisepan version && entropia version
```

### Linux（下载二进制文件并验证校验和）

下载二进制文件后，验证其校验和，然后进行安装。在将文件安装到 `/usr/local/bin` 目录之前，请先询问用户是否同意——如果用户希望将软件安装到用户自定义的 `~/bin` 目录中，也可以提供这个选项。

```bash
# noisepan
VER=$(curl -s https://api.github.com/repos/ppiankov/noisepan/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d v)
curl -fsSL "https://github.com/ppiankov/noisepan/releases/download/v${VER}/noisepan_${VER}_linux_amd64.tar.gz" -o /tmp/noisepan.tar.gz
curl -fsSL "https://github.com/ppiankov/noisepan/releases/download/v${VER}/checksums.txt" -o /tmp/noisepan-checksums.txt
# Verify checksum
grep linux_amd64 /tmp/noisepan-checksums.txt | (cd /tmp && sha256sum -c)
tar xzf /tmp/noisepan.tar.gz -C /usr/local/bin noisepan
rm /tmp/noisepan.tar.gz /tmp/noisepan-checksums.txt

# entropia
VER=$(curl -s https://api.github.com/repos/ppiankov/entropia/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d v)
curl -fsSL "https://github.com/ppiankov/entropia/releases/download/v${VER}/entropia_${VER}_linux_amd64.tar.gz" -o /tmp/entropia.tar.gz
curl -fsSL "https://github.com/ppiankov/entropia/releases/download/v${VER}/checksums.txt" -o /tmp/entropia-checksums.txt
# Verify checksum
grep linux_amd64 /tmp/entropia-checksums.txt | (cd /tmp && sha256sum -c)
tar xzf /tmp/entropia.tar.gz -C /usr/local/bin entropia
rm /tmp/entropia.tar.gz /tmp/entropia-checksums.txt

# Verify both
noisepan version && entropia version
```

### 初始化

```bash
noisepan init --config ~/.noisepan
# Verify entropia is detected
noisepan doctor --config ~/.noisepan
```

## 配置信息源

编辑 `~/.noisepan/config.yaml` 文件。推荐的结构如下：

```yaml
sources:
  hn:
    min_points: 200    # Native HN via Firebase API

  rss:
    feeds:
      # Security
      - "https://www.reddit.com/r/netsec/.rss"
      - "https://krebsonsecurity.com/feed/"
      - "https://www.bleepingcomputer.com/feed/"
      - "https://feeds.feedburner.com/TheHackersNews"
      - "https://www.cisa.gov/cybersecurity-advisories/all.xml"

      # DevOps
      - "https://www.reddit.com/r/devops/.rss"
      - "https://www.reddit.com/r/kubernetes/.rss"
      - "https://blog.cloudflare.com/rss/"

      # AI/LLM
      - "https://www.reddit.com/r/LocalLLaMA/.rss"
      - "https://simonwillison.net/atom/everything/"
      - "https://arxiv.org/rss/cs.AI"

      # Status pages
      - "https://status.aws.amazon.com/rss/all.rss"
      - "https://www.cloudflarestatus.com/history.rss"

      # World / Policy
      - "https://feeds.bbci.co.uk/news/world/rss.xml"
      - "https://www.eff.org/rss/updates.xml"

      # Aggregators
      - "https://lobste.rs/rss"
      - "https://changelog.com/news/feed"
```

根据个人兴趣自定义配置。添加信息源后，运行 `noisepan doctor` 命令进行验证。

## 信息源分类

编辑 `~/.noisepan/taste.yaml` 文件。主要分类如下：

**高关注度信息（评分 3-5）：** 漏洞（CVE）、零日攻击、供应链安全事件、服务中断、安全承诺、数据主权、反垄断相关、军事人工智能、去匿名化技术、命令注入攻击、重大系统变更

**低关注度信息（评分 -3 至 -5）：** 招聘信息、网络研讨会、赞助商公告、网络迷因、职业建议、名人动态

**重要提示：** 如果没有包含“政策”、“数据主权”、“反垄断”或“人工智能安全”等关键词，真实重要的新闻可能会被安全相关的噪音信息掩盖。因此，这些信息的权重应与漏洞信息相同。

## Reddit 的访问限制

当同时订阅 15 个以上的 Reddit 订阅源时，会触发 Reddit 的访问限制（429 错误）。此时需要创建一个顺序获取数据的脚本来规避这个问题：

```bash
cat > ~/.local/bin/noisepan-pull << 'SCRIPT'
#!/bin/bash
# Prefetch Reddit RSS sequentially to avoid rate limiting, then run noisepan pull
CACHE_DIR="/tmp/reddit-rss-cache"
CONFIG_DIR="${HOME}/.noisepan"
UA="Mozilla/5.0 (compatible; noisepan/1.0)"

mkdir -p "$CACHE_DIR"
FEEDS=$(grep "reddit.com" "$CONFIG_DIR/config.yaml" | grep -v "^#" | grep -v "^      #" | sed 's/.*"\(.*\)"/\1/')

for feed in $FEEDS; do
    sub=$(echo "$feed" | grep -oP '/r/\K[^/]+')
    curl -s -o "$CACHE_DIR/${sub}.xml" -H "User-Agent: $UA" "$feed"
    sleep 2
done

python3 -m http.server 18222 --directory "$CACHE_DIR" &>/dev/null &
HTTP_PID=$!; sleep 0.5

mkdir -p /tmp/noisepan-tmp
cp "$CONFIG_DIR/config.yaml" /tmp/noisepan-tmp/config.yaml
for feed in $FEEDS; do
    sub=$(echo "$feed" | grep -oP '/r/\K[^/]+')
    sed -i "s|$feed|http://localhost:18222/${sub}.xml|" /tmp/noisepan-tmp/config.yaml
done
ln -sf "$CONFIG_DIR/taste.yaml" /tmp/noisepan-tmp/taste.yaml
ln -sf "$CONFIG_DIR/noisepan.db" /tmp/noisepan-tmp/noisepan.db

noisepan pull --config /tmp/noisepan-tmp "$@"
kill $HTTP_PID 2>/dev/null; rm -rf /tmp/noisepan-tmp
SCRIPT
mkdir -p ~/.local/bin && chmod +x ~/.local/bin/noisepan-pull
```

当订阅了 15 个以上的 Reddit 订阅源时，应使用 `noisepan-pull` 而不是 `noisepan pull` 命令。

## HN（Hacker News）的遗漏信息检测脚本

可选功能——用于捕捉那些被常规评分机制遗漏的高关注度 HN 新闻。可作为 Noisepan 原生 HN 源信息的补充检查工具。

```bash
cat > ~/.local/bin/hn-top << 'SCRIPT'
#!/bin/bash
MIN_POINTS=${1:-200}
curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | \
python3 -c "
import json, sys, urllib.request, time
ids = json.load(sys.stdin)[:30]
min_pts = int(sys.argv[1]) if len(sys.argv) > 1 else 200
for id in ids:
    try:
        with urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{id}.json') as r:
            item = json.loads(r.read())
            if item and item.get('score', 0) >= min_pts:
                print(f'[{item[\"score\"]:4d}pts | {item.get(\"descendants\",0):3d}c] {item[\"title\"]}')
                print(f'  {item.get(\"url\", f\"https://news.ycombinator.com/item?id={id}\")}')
                print()
        time.sleep(0.1)
    except: pass
" "$MIN_POINTS"
SCRIPT
chmod +x ~/.local/bin/hn-top
```

## Cron 任务设置

创建两个 OpenClaw Cron 任务（分别在上午和下午执行）。任务流程包括：
1. 获取信息源数据（使用 `noisepan-pull` 或 `noisepan pull`）
2. 生成摘要文件（`noisepan digest --format json --output /tmp/digest.json`）
3. 运行 `hn-top 300` 命令检查遗漏的信息
4. 对非 Reddit 来源的 top 6 条新闻使用 `entropia scan <url>` 进行进一步分析
5. 过滤条件：排除 Entropia 评分低于 40 的信息或存在冲突的信息
6. 如果 top 6 条新闻被过滤掉，再从第 4 到第 6 条新闻中补充数据
7. 比较 HN 的 top 300 条新闻与摘要文件，找出遗漏的信息（即摘要中未包含的、评分超过 400 分的新闻）

### 输出格式

```
🔥 Trending: keywords across 3+ channels
☀️ Morning Brief (3 verified items):
| # | Score | Topic | What happened | Entropia | Link |
💡 HN Blind Spot (stories the taste profile missed):
| # | HN pts | Topic | What happened | Link |
⚠️ Skipped (filtered for low quality):
| # | Score | Topic | Why skipped |
```

**执行时间：** 上午 07:00，下午 18:00（可根据时区进行调整）

## 有用的命令

```bash
noisepan doctor --config ~/.noisepan    # Feed health + companion tool detection
noisepan stats --config ~/.noisepan     # Signal-to-noise per channel
noisepan rescore --config ~/.noisepan   # Recompute after taste changes
entropia scan <url>                     # Verify a specific source
```

## 经验总结：
- 使用 `noisepan doctor` 可检测到过时或被完全忽略的信息源；添加新信息源后请运行此命令
- `noisepan stats` 可显示每个信息源的关注度；30 天后关注度低于 0% 的信息源应被删除
- Hacker News 的 RSS 数据较为简单，建议使用 `sources.hn` 或 `hn-top` 来检测遗漏的信息
- 如果 Entropia 的评分低于 40，则表示该信息无法被有效提取，应直接忽略
- 当订阅 15 个以上的 Reddit 订阅源时，必须使用顺序获取数据的脚本来规避访问限制
- 如果信息源的标题中不包含 “服务事件” 或 “运营问题” 等关键词，其评分会较低

---
**Noisepan 摘要 v1.0**
作者：ppiankov
版权所有 © 2026 ppiankov
官方仓库：https://github.com/ppiankov/noisepan
许可证：MIT

如果本文档出现在其他地方，上述仓库中的版本为正式版本。