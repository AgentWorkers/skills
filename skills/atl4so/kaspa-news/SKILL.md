---
name: kaspa-news
description: "**Kaspa News** — 将关于 Kaspa 的所有信息集中在一个地方：最新新闻、核心开发更新、生态系统发布、社区活动以及每周报告摘要。当有人询问 Kaspa 的最新动态时（包括开发/构建团队的活动、热门推文、视频以及 Reddit 上的更新），可以使用此工具。无需使用 API 密钥。"
metadata: {"clawdbot":{"requires":{"bins":["python3","jq"]}}}
---
# Kaspa 新闻技能

通过查询公开的 kaspa.news API 来获取 Kaspa 生态系统的信息。无需 API 密钥。

## 快速入门

```bash
SCRIPT="~/.openclaw/workspace/skills/kaspa-news/scripts/kaspa-news.sh"

$SCRIPT focused           # Curated community tweets
$SCRIPT builders           # Ecosystem/builder tweets
$SCRIPT top                # Most viewed tweets
$SCRIPT developers         # Core dev tweets (includes replies)
$SCRIPT videos             # YouTube videos
$SCRIPT reddit             # r/kaspa posts
$SCRIPT pulse              # Latest AI pulse report
```

## 所需软件

- 安装了 `python3` 及 `requests` 模块的开发环境
- 安装了 `jq` 工具
- 具备访问 `https://kaspa.news/api` 的网络权限
- **无需 API 密钥、令牌或身份验证** — 所有接口都是公开的

---

## 命令参考

### `focused` — 精选社区推文
由社区精选的推文，不包括回复。非常适合了解“Kaspa 社区在讨论什么？”

```bash
$SCRIPT focused              # Latest 10
$SCRIPT focused -n 5         # Latest 5
$SCRIPT focused --since 12   # Last 12 hours only
```

### `builders` — 基于 Kaspa 的项目推文
在 kaspa.news 网站上标记为“Ecosystem”的项目相关推文，不包括回复。

```bash
$SCRIPT builders             # Latest 10
$SCRIPT builders -n 20       # Latest 20
```

### `top` — 点击量最高的推文
按点击量排序（点击量最高的排在最前面）。**这是唯一一个会显示点击量的命令**（👁️）。

```bash
$SCRIPT top                  # Top 10 by views
$SCRIPT top -n 3             # Top 3
```

### `developers` — 开发者推文
来自知名 Kaspa 核心开发者的推文，**包括回复**（与其他推文命令不同）。可以查看开发者的讨论和技术交流。

脚本内置了已知开发者用户名的列表，但这仅适用于默认的 `developers` 命令。针对特定用户的搜索（见下文）可以搜索任何用户名。

```bash
$SCRIPT developers           # Latest 10 dev tweets
$SCRIPT developers -n 15     # Latest 15
```

### `videos` — 与 Kaspa 相关的 YouTube 视频
最新的 Kaspa 相关 YouTube 视频，附带观看次数和点赞数。

```bash
$SCRIPT videos               # Latest 10
$SCRIPT videos --since 48    # Last 2 days
```

### `reddit` — Reddit 帖子
来自 r/kaspa 的最新帖子，附带点赞数。

```bash
$SCRIPT reddit               # Latest 10
$SCRIPT reddit -n 5          # Latest 5
```

### `pulse` — 人工智能报告
由 AI 生成的 Kaspa 生态系统活动摘要报告，仅提供最新的报告。

```bash
$SCRIPT pulse                # Latest report (text summary)
$SCRIPT pulse --sources      # With clickable source links to tweets
$SCRIPT pulse --json         # Full JSON (for custom parsing)
```

---

## 全局选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `-n, --limit N` | 显示的条目数量 | 10 |
| `--since HOURS` | 仅显示过去 N 小时的内容 | 全部内容 |
| `--json` | 原始 JSON 格式输出（用于脚本编写/解析） | 关闭 |
| `--sources` | 在报告中显示来源链接 | 关闭 |
| `-h, --help` | 显示帮助信息 | — |

---

## 脚本输出格式

脚本以 **纯文本** 的形式输出结果。以下是每个命令的具体输出内容：

### 推文命令（focused, builders, developers）

```
🎯 Focused Tweets

📝 @DailyKaspa (1h)
Nearly $10 million in short positions are stacked around the 0.037 level...
[SOURCE](https://x.com/DailyKaspa/status/2024047412226978031)

💬 @KaspaHub (10h)
Better late than never, I guess.
[SOURCE](https://x.com/KaspaHub/status/2023918673216311580)

↩️ @hashdag (1h)
@asaefstroem @maxibitcat could be, not ruling that out...
[SOURCE](https://x.com/hashdag/status/2024050945718399078)
```

### `top` 命令（包含点击量）

```
🔥 Top Tweets

📝 @BSCNews (23h) — 👁️ 22179
🚨JUST IN: $KAS, $PI, $ASTER AMONG PROJECTS WITH MOST BULLISH SENTIMENT...
[SOURCE](https://x.com/BSCNews/status/2023709720901534048)

💬 @kaspaunchained (14h) — 👁️ 10663
Private messaging on Kaspa L1. Encrypted payloads riding the BlockDAG...
[SOURCE](https://x.com/kaspaunchained/status/2023845437577257447)
```

### 视频

```
📺 Kaspa Videos

📺 Kaspa Crypto Prediction | Why We Went Bearish?
  📡 Crypto MindSet | 👁️ 80 | ❤️ 3 | 6h
  🔗 https://youtube.com/watch?v=NgO5iW1B_t4
```

### Reddit 帖子

```
🟠 Kaspa Reddit

🟠 Did Fred Thiel Dump his Kaspa Bag?
  👤 u/Weekly-Fudge1909 | ⬆️ 10 | 2h
  🔗 https://reddit.com/r/kaspa/comments/1r7o9oi
```

### 人工智能报告

```
📊 Kaspa Pulse Reports

[REPORT HERE](https://kaspa.news/pulse/d6167911-21ab-4135-bccb-a4baf4e4480f)

📊 From Silverscript to TangFi...
  🕐 13h | 🤖 gpt-5.2

  Silverscript compiler goes live on Testnet 12, delivering first high-level
  contract language for Kaspa...
```

---

## 🎨 展示规则（所有操作人员必须遵守）

脚本以纯文本形式输出结果。在向用户展示时，请严格遵循以下规则。这是官方规定的格式，请勿更改。

### 推文类型对应的表情符号

| 表情符号 | 含义 |
|-------|---------|
| 📝 | 普通推文 |
| 💬 | 引用推文（仅显示用户的评论，不包括被引用的源推文） |
| ↩️ | 回复 |

### 脚本已完成的操作（无需重复）

- ✅ 自动选择正确的表情符号（📝/💬/↩️）
- ✅ 显示相对时间（如“10小时”、“1天”、“5分钟”，不使用“ago”）
- ✅ 将 t.co 链接转换为实际网址
- ✅ 删除 t.co 链接后的图片链接
- ✅ 解码 HTML 实体（& → &, > → >）
- ✅ 将输出内容截断至 300 个字符
- ✅ 在每条推文后添加 [来源](url) 链接
- ✅ 仅在 `top` 命令中显示 👁️（表示点击量）

### 您（展示者）需要执行的操作

#### 将推文链接转换为 X/Twitter 格式

- 将纯文本中的 @用户名、#标签和 $CASHTAG 转换为可点击链接：
  - `@username` → `[@username](https://x.com/username)` — 链接到 X 社交平台的个人主页
  - `#hashtag` → `[#hashtag](https://x.com/search?q=%23hashtag)` — 链接到 X 社交平台的搜索页面
  - `$KAS` → `[$KAS](https://x.com/search?q=%24KAS)` — 链接到 X 社交平台的搜索页面

**重要提示：**
  - 仅链接真实的用户名/标签/关键词
  - 数字（如 #2、#4、#10BPS）不是标签，请保持原样
  - 电子邮件地址中的 @ 符号不是用户名，请保持原样
  - 链接应指向 x.com（而非 twitter.com 或 Telegram）

#### 人工智能报告的格式化

在展示报告时，请按照以下格式进行分组：

```
📊 **Latest Kaspa Pulse Report** (date)

**"Report Title Here"**

━━━ Core Development ━━━

🔧 **Silverscript** — First high-level smart contract language, live on TN12.

📐 **Covenants** — Enable programmable spending conditions on UTXO.

━━━ Ecosystem ━━━

💵 **TangFi** — Bridging stablecoins (USDT/USDC) to Kaspa L1.

🔐 **Private Messaging** — Encrypted payloads on BlockDAG at 10 BPS.

━━━ Milestones ━━━

📈 600M total transactions on Kaspa mainnet.
```

**人工智能报告格式规则：**
- 使用 `━━━ 分类 ━━━` 作为分类分隔符
- 项目/功能的名称需加粗显示
- 每条内容占一行，最多 1-2 句
- 使用表情符号作为项目前缀（🔧💵🔐💬🌉⚡🏦📊📈💎🎤📱）
- 需要提及的关键人物：@hashdag（Yonatan Sompolinsky）、@michaelsuttonil（Michael Sutton）、@OriNewman（Ori Newman）

---

## 🔍 根据用户查询特定用户的推文

当用户请求查看某个特定用户的推文时（例如：“展示 @michaelsuttonil 过去两周的推文”），该功能支持任何用户名，不受内置开发者名称的限制。

### 查询方法

- 获取所有接口的数据并进行合并（建议查询所有数据）：

```bash
# Fetch all 4 tweet sources
$SCRIPT focused --json -n 999 > /tmp/focused.json
$SCRIPT builders --json -n 999 > /tmp/builders.json
$SCRIPT top --json -n 999 > /tmp/top.json
$SCRIPT developers --json -n 999 > /tmp/devs.json

# Merge, deduplicate by url, filter by username + date range (safe)
TARGET_USER="michaelsuttonil"
cat /tmp/*.json | jq -s --arg user "$TARGET_USER" 'add | unique_by(.url) | [.[] | select(.author_username == $user)]'
```

或者使用 `--json` 输出格式，然后通过 `jq` 或 Python 进行过滤。

**安全提示：** 切勿直接将用户的原始输入插入到 `jq` 脚本中。请始终通过 `--arg` 或 `--argjson` 传递用户参数。

### 展示用户推文的结果

- 按日期排序（最新的内容在前）
- 先显示独立发布的推文，再显示回复。

```
📅 Feb 17 — Smart contracts and Silverscript progress

📝 @michaelsuttonil
Full tweet text here exactly as-is...
[SOURCE](https://x.com/michaelsuttonil/status/123)

💬 @michaelsuttonil
Quote comment here (user's own words only)...
[SOURCE](https://x.com/michaelsuttonil/status/456)

↩️ To @hashdag: "Reply text shown in quotes..."
[SOURCE](https://x.com/michaelsuttonil/status/789)

---

📅 Feb 16 — TN12 testing and validator discussion

📝 @michaelsuttonil
Another tweet...
[SOURCE](url)
```

**用户推文展示规则：**
- 使用日期格式 `📅 2月17日`，并在日期前加上破折号和简短的主题总结
- 使用 `---` 作为日期组之间的分隔符
- 独立发布的推文在前（📝/💬），回复在后面（↩️）
- 回复内容格式：`↩️ 发送给 @recipient: “被引用的回复内容...”`
- 除非内容重要，否则省略简单的回复（如“100%”、“sure”、“thanks”）
- 在结尾处添加对该时间段内主题的简要总结
- **始终查询用户请求的完整时间范围**，不要自行缩短时间范围
- **显示所有找到的推文**，不要预先过滤或缩小搜索结果

---

## ❌ 禁止的行为（严格禁止）

以下行为会导致输出错误：

| 禁止的行为 | 原因 |
|------|-----|
| ❌ 不得编辑、修剪、重写或总结推文内容 | 必须显示用户原文 |
| ❌ 不得将同一作者的多条推文合并 | 每条推文应单独显示 |
| ❌ 不得显示被引用推文的来源文本 | 引用推文仅显示用户的评论 |
| ❌ 不得显示情绪分析百分比（如牛市/熊市 %） | 用户明确禁止显示这些信息 |
| ❌ 不得在报告中显示“分析了 N 条推文”的数量 | 用户明确禁止显示这些信息 |
| ❌ 不得在报告中显示模型名称 | 这是内部信息 |
| ❌ 不得在推文输出中加粗 @用户名 | 格式已固定 |
| ❌ 不得在推文中添加额外的表情符号或分隔线 | 格式已固定 |
| ❌ 不得在章节标题中添加“(最新 N 条)” | 标题应简洁明了 |
| ❌ 不得在时间后面添加类型标签（如 “— 📝 推文”） | 使用表情符号前缀即可 |
| ❌ 不得使用Markdown表格展示推文 | 应采用逐行显示的格式 |
| ❌ 不得在报告中添加“根据人工智能报告”这样的表述 | 直接展示信息即可 |
| ❌ 除 `top` 命令外，不得在报告中添加互动指标（❤️/🔁） | 只有 `top` 命令会显示点击量 |
| ❌ 不得将 @用户名链接指向 Telegram | 必须链接到 X 社交平台（x.com） |
| ❌ 不得删除 [来源] 链接 | 这些链接始终需要显示 |

---

## ✅ 推荐的最佳实践

| 推荐做法 | 详细说明 |
|----------|--------|
| ✅ 运行脚本并展示其输出结果 | 不得伪造数据或使用旧数据 |
| ✅ 将 @用户名链接转换为 X 社交平台的个人主页 | `[@user](https://x.com/user)` |
| ✅ 将 #标签链接转换为 X 社交平台的搜索页面 | `[#hashtag](https://x.com/search?q=%23kaspa)` |
| ✅ 将 $CASHTAG 链接转换为 X 社交平台的搜索页面 | `[$KAS](https://x.com/search?q=%24KAS)` |
| ✅ 按类别对人工智能报告进行分组 | 使用 `━━━` 作为分隔符 |
| ✅ 在报告中加粗项目名称 | 便于阅读 |
| ✅ 保持内容在移动设备上易于阅读 | 使用简短的行和表情符号 |
| ✅ 对于用户查询：查询所有数据 | 查阅完整的时间范围 |
| ✅ 使用 `--json` 进行自定义过滤 | 然后手动格式化结果 |

---

## 触发短语

当用户提到以下内容时，可以使用此技能：
- “Kaspa 新闻”、“Kaspa 生态系统发生了什么”、“Kaspa 推文”
- “Kaspa 人工智能报告”、“Kaspa 更新”
- “Kaspa 开发者”、“Kaspa 开发者都在说什么”
- “Kaspa 视频”、“Kaspa 在 YouTube 上的内容”
- “展示 @someone 的推文”（查询特定用户的推文）
- “热门的 Kaspa 推文”、“Kaspa 的热门内容”
- 任何与 kaspa.news 相关的查询

---

## 架构说明

- **API 基础地址**：`https://kaspa.news/api`（固定地址，不可更改）
- **API 返回缓存数据** — 如 `?limit=` 等查询参数在服务器端会被忽略
- **所有过滤操作都在客户端完成** — 脚本会获取全部数据，然后使用 `jq` 进行过滤
- **无需身份验证** — 所有接口都是公开的，无需 API 密钥
- **无需运行时环境变量**  
- **脚本输出纯文本** — 展示者负责处理链接的生成
- 技能目录中的 `FORMAT_LOCK.md` 文件包含了官方的格式规范