---
name: noisepan-digest
description: 使用 noisepan（信号提取）、entropia（来源验证）和 HN 盲点检测功能来设置自动化的新闻摘要系统。该系统可用于配置每日新闻简报、整理 RSS 源，或构建替代人工新闻浏览的自动化智能处理流程。
metadata: {"openclaw":{"requires":{"bins":["noisepan","entropia"]}}}
---
# Noisepan 摘要

这是一个自动化的新闻情报工具，具备来源验证功能，旨在替代无意义的刷屏行为，每天提供两次新闻摘要。

**数据来源：**
- https://github.com/ppiankov/noisepan （信号提取）
- https://github.com/ppiankov/entropia （来源验证）

**所需软件：** `noisepan`, `entropia`, `python3`, `curl`

## 安装

### macOS（推荐使用 Homebrew）

```bash
brew install ppiankov/tap/noisepan ppiankov/tap/entropia
noisepan version && entropia version
```

### Linux（二进制文件 + 校验 checksum）

下载文件后，验证 checksum，然后进行安装。在将文件安装到 `/usr/local/bin` 目录之前，请先询问用户是否同意——如果用户希望将软件安装到用户自定义的目录（如 `~/bin`），可以提供该选项。

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

根据个人兴趣进行自定义配置。添加信息源后，运行 `noisepan doctor` 命令进行检测。

## 信息源分类

编辑 `~/.noisepan/taste.yaml` 文件。主要分类如下：

**高关注度信息（评分 3-5）：** 漏洞（CVE）、零日攻击、供应链安全事件、服务中断、安全承诺、数据主权、反垄断、军事人工智能、去匿名化技术、命令注入、重大系统变更

**低关注度信息（评分 -3 至 -5）：** 招聘信息、网络研讨会、赞助活动、新闻通讯、网络迷因、职业建议、名人动态

**重要提示：** 如果信息中不包含与政策、数据主权、反垄断或人工智能安全相关的关键词，这些真实事件可能会被安全相关的噪音信息掩盖。因此，这些信息的权重应与漏洞信息相同。

## Reddit 的访问限制

当同时订阅 15 个以上的 Reddit 论坛时，会触发 429 错误（请求过多）。此时需要使用顺序获取数据的脚本来避免这个问题：

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

当订阅了 15 个以上的 Reddit 论坛时，应使用 `noisepan-pull` 而不是 `noisepan pull` 命令。

## HN（Hacker News）的遗漏信息检测脚本

可选功能——用于捕捉那些被信息源评分系统遗漏的高关注度 HN 新闻。可作为 noisepan 的补充工具使用。

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
1. 下载信息源数据（使用 `noisepan-pull` 或 `noisepan pull`）
2. 生成摘要文件（`noisepan digest --format json --output /tmp/digest.json`）
3. 使用 `hn-top 300` 命令检查遗漏的信息
4. 对非 Reddit 来源的链接执行 `entropia scan <url>` 检查
5. 过滤掉 Entropia 评分低于 40 的信息或存在冲突的信息
6. 如果前 6 项被过滤掉，再从第 4 至 6 项中补充信息
7. 比较 HN 的高关注度信息与摘要文件，找出遗漏的内容（评分超过 400 分但未被收录的新闻）

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

**执行时间：** 上午 07:00，下午 18:00（可根据时区进行调整）。

## 有用的命令

```bash
noisepan doctor --config ~/.noisepan    # Feed health + companion tool detection
noisepan stats --config ~/.noisepan     # Signal-to-noise per channel
noisepan rescore --config ~/.noisepan   # Recompute after taste changes
entropia scan <url>                     # Verify a specific source
```

## 经验总结：
- 使用 `noisepan doctor` 可检测到过时或被忽略的信息源；添加新信息源后请运行此命令。
- `noisepan stats` 可显示每个信息源的关注度；30 天后关注度为 0% 的信息源应被删除。
- Hacker News 的 RSS 数据更新频率较低，建议使用 `sources.hn` 或 `hn-top` 来获取遗漏的信息。
- 如果 Entropia 的评分低于 40，则表示该信息无法被提取；应跳过此类信息。
- 当订阅 15 个以上的 Reddit 论坛时，必须使用顺序获取数据的脚本以避免请求错误。
- 如果信息源的描述中不包含 “服务事件” 或 “运营问题” 等关键词，其评分会较低。

---
版权所有 © 2026 ppiankov。根据 MIT 许可证发布。官方源代码地址：https://github.com/ppiankov/openclaw-skills