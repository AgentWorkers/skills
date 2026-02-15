---
name: xint
description: >
  **X Intelligence CLI** — 一种用于在终端中搜索、分析并处理 X/Twitter 内容的工具。适用场景包括：  
  1. 当用户输入“x research”、“search x for”、“search twitter for”等指令时；  
  2. 当用户需要了解最新 X/Twitter 上的讨论内容（如新库发布、API 变更、产品发布、文化事件或行业动态）时；  
  3. 当用户想了解开发者、专家或社区对某个主题的看法时。  
  该工具还支持以下功能：  
  - 实时监控（watch）  
  - 跟踪粉丝变化（diff）  
  - 智能报告生成  
  - 人工智能情感分析  
  - 互动功能（如点赞、关注、书签等）  
  - 热门话题追踪  
  - Grok AI 分析  
  - 成本跟踪  
  数据输出格式支持 JSON、JSONL（可管道传输）、CSV 或 Markdown。  
  使用该工具需要通过 OAuth 进行用户身份验证，以便访问相关数据和执行操作。
credentials:
  - name: X_BEARER_TOKEN
    description: X API v2 bearer token for search, profile, thread, tweet, trends
    required: true
  - name: XAI_API_KEY
    description: xAI API key for Grok analysis, article fetching, sentiment, x-search, collections
    required: false
  - name: XAI_MANAGEMENT_API_KEY
    description: xAI Management API key for collections management
    required: false
  - name: X_CLIENT_ID
    description: X OAuth 2.0 client ID for user-context operations (bookmarks, likes, following, diff)
    required: false
---
# xint — X 智能命令行工具（X Intelligence CLI）

这是一个通用的代理研究工具，用于在 X/Twitter 上进行信息收集和分析。它可以将任何研究问题分解为具体的搜索任务，通过迭代优化搜索策略、跟踪相关话题、深入分析链接内容，并最终生成一份详细的报告。

有关 X API 的详细信息（端点、操作符和响应格式），请参阅 `references/x-api.md`。

## 命令行工具（CLI）

所有命令都在这个工具目录下执行：

```bash
# Set your environment variables
export X_BEARER_TOKEN="your-token"
```

### 搜索（Search）

```bash
bun run xint.ts search "<query>" [options]
```

**选项：**
- `--sort likes|impressions|retweets|recent` — 排序方式（默认：按点赞数排序）
- `--since 1h|3h|12h|1d|7d` — 时间筛选条件（默认：过去 7 天内）。也支持以分钟（`30m`）或 ISO 时间戳为单位进行筛选。
- `--min-likes N` — 根据最低点赞数进行筛选
- `--min-impressions N` — 根据最低浏览量进行筛选
- `--pages N` — 要获取的页面数（1-5 页，默认：每页 100 条推文）
- `--limit N` — 显示的最大结果数量（默认：15 条）
- `--quick` — 快速模式：仅显示第 1 页的内容，最多显示 10 条结果，自动过滤无关内容，缓存 1 小时，并提供费用统计
- `--from <username>` — 用于查询的简写形式（等同于 `from:username`）
- `--quality` — 筛选互动量较高的推文（点赞数 >= 10）
- `--no-replies` — 不包括回复内容
- `--sentiment` — 使用 Grok 进行每条推文的 sentiment 分析（显示正面/负面/中性/混合情感）
- `--save` — 将结果保存到 `data/exports/`
- `--json` — 以原始 JSON 格式输出结果
- `--jsonl` — 每行输出一个 JSON 对象（适用于 Unix 管道操作，例如 `| jq`, `| tee`）
- `--csv` — 以 CSV 格式输出结果，便于电子表格分析
- `--markdown` — 以 Markdown 格式输出结果，用于生成研究文档

系统会自动添加 `-is:retweet` 选项（除非用户已经在查询中明确指定了该选项）。所有搜索结果都会显示预估的 API 费用。

**示例：**
```bash
bun run xint.ts search "AI agents" --sort likes --limit 10
bun run xint.ts search "from:elonmusk" --sort recent
bun run xint.ts search "(opus 4.6 OR claude) trading" --pages 2 --save
bun run xint.ts search "$BTC (revenue OR fees)" --min-likes 5
bun run xint.ts search "AI agents" --quick
bun run xint.ts search "AI agents" --quality --quick
bun run xint.ts search "solana memecoins" --sentiment --limit 20
bun run xint.ts search "startup funding" --csv > funding.csv
bun run xint.ts search "AI" --jsonl | jq 'select(.metrics.likes > 100)'
```

### 个人资料（Profile）

```bash
bun run xint.ts profile <username> [--count N] [--replies] [--json]
```

获取指定用户的最新推文（默认不包含回复内容）。

### 话题链（Thread）

```bash
bun run xint.ts thread <tweet_id> [--pages N]
```

根据根推文的 ID 获取完整的话题链。

### 单条推文（Single Tweet）

```bash
bun run xint.ts tweet <tweet_id> [--json]
```

### 文章内容获取（Article Content Fetcher）

```bash
bun run xint.ts article <url> [--json] [--full]
```

使用 xAI 的 web_search 工具从任意 URL 获取并提取文章的全部内容（Grok 会解析页面内容）。返回包含标题、作者、日期和字数的干净文本。需要 `XAI_API_KEY`。

**选项：**
- `--json` — 以结构化 JSON 格式输出（标题、内容、作者、发布时间、字数）
- `--full` — 返回完整文章内容（默认仅显示前 5000 个字符）
- `--model <name>` — 使用的 Grok 模型（默认：grok-3-mini）

**示例：**
```bash
bun run xint.ts article https://example.com/blog/post
bun run xint.ts article https://techcrunch.com/article --json
bun run xint.ts article https://blog.example.com/deep-dive --full
```

**代理使用说明：** 当搜索结果中包含文章链接时，可以使用 `article` 命令来阅读文章的全文。搜索结果现在会显示文章的标题和描述（标记为 `📰`），帮助用户判断哪些文章值得阅读。优先考虑以下类型的文章：
- 被多条推文引用的文章
- 来自互动量较高的推文的文章
- 标题或描述在 API 元数据中具有相关性的文章

### 收藏夹（Bookmarks）

```bash
bun run xint.ts bookmarks [options]       # List bookmarked tweets
bun run xint.ts bookmark <tweet_id>       # Bookmark a tweet
bun run xint.ts unbookmark <tweet_id>     # Remove a bookmark
```

**收藏夹列表选项：**
- `--limit N` — 显示的最大收藏夹数量（默认：20 个）
- `--since <dur>` — 根据时间筛选收藏夹（1 小时、1 天等）
- `--query <text>` — 客户端文本筛选条件
- `--json` — 以原始 JSON 格式输出
- `--markdown` — 以 Markdown 格式输出
- `--save` — 将收藏夹保存到 `data/exports/`
- `--no-cache` — 禁用缓存

使用 OAuth 进行操作。请先运行 `auth setup` 命令进行授权设置。

### 点赞（Likes）

```bash
bun run xint.ts likes [options]           # List your liked tweets
bun run xint.ts like <tweet_id>           # Like a tweet
bun run xint.ts unlike <tweet_id>         # Unlike a tweet
```

**点赞列表选项：** 与收藏夹选项相同（`--limit`, `--since`, `--query`, `--json`, `--no-cache`）。

需要使用具有 `like.read` 和 `like.write` 权限的 OAuth 访问权限。

### 关注（Following）

```bash
bun run xint.ts following [username] [--limit N] [--json]
```

列出你（或其他用户）关注的用户列表。默认显示当前登录用户的关注列表。

需要使用具有 `follows.read` 权限的 OAuth 访问权限。

### 热门话题（Trends）

```bash
bun run xint.ts trends [location] [options]
```

获取热门话题。首先尝试使用 X 官方 API 的趋势端点；如果该端点不可用，则使用基于搜索的标签频率估算方法。

**选项：**
- `[location]` — 地点名称或 WOEID 编号（默认：全球范围）
- `--limit N` — 显示的热门话题数量（默认：20 个）
- `--json` — 以原始 JSON 格式输出
- `--no-cache` — 禁用 15 分钟的缓存
- `--locations` — 列出所有已知的位置名称

**示例：**
```bash
bun run xint.ts trends                    # Worldwide
bun run xint.ts trends us --limit 10      # US top 10
bun run xint.ts trends japan --json       # Japan, JSON output
bun run xint.ts trends --locations        # List all locations
```

### 分析（Grok AI）

```bash
bun run xint.ts analyze "<query>"                              # Ask Grok a question
bun run xint.ts analyze --tweets <file>                        # Analyze tweets from JSON file
bun run xint.ts search "topic" --json | bun run xint.ts analyze --pipe  # Pipe search results
```

使用 xAI 的 Grok API（兼容 OpenAI）。需要在环境变量或 `.env` 文件中设置 `XAI_API_KEY`。

**选项：**
- `--model <name>` — 可使用的 Grok 模型（默认：grok-3, grok-3-mini, grok-2）
- `--system <prompt>` — 自定义系统提示语
- `--tweets <file>` — 包含推文的 JSON 文件路径
- `--pipe` — 从标准输入读取推文 JSON 数据

**示例：**
```bash
bun run xint.ts analyze "What are the top AI agent frameworks right now?"
bun run xint.ts search "AI agents" --json | bun run xint.ts analyze --pipe "Which show product launches?"
bun run xint.ts analyze --model grok-3 "Deep analysis of crypto market sentiment"
```

## xAI X 搜索（无需 Cookie/GraphQL）

如果需要在不使用 Cookie 或 GraphQL 的情况下获取“最近的热门话题/用户动态”，可以使用 xAI 提供的 `x_search` 工具。

**脚本示例：** `Jarv cron` 会在 `workspace-jarv/x-signals/x-search-queries.json` 文件中通过查询包来使用该工具。

## xAI 收藏夹知识库（文件 + 收藏夹管理）

将第一方生成的文件（报告、日志等）存储在 xAI 的收藏夹中，并允许后续进行语义搜索。

**脚本示例：**
```bash
python3 /home/openclaw/.openclaw/skills/xint/scripts/xai_collections.py --help
```

**环境变量设置：**
- `XAI_API_KEY`（api.x.ai）：用于文件上传和搜索操作
- `XAI_MANAGEMENT_API_KEY`（management-api.x.ai）：用于收藏夹管理和文件上传

**注意事项：**
- 请勿直接打印环境变量中的密钥。
- 在设置新的定时任务时，建议使用 `--dry-run` 选项进行测试。

### 实时监控（Watch）

```bash
bun run xint.ts watch "<query>" [options]
```

定期执行搜索查询，仅显示新的推文。非常适合在活动期间监控话题、跟踪提及情况或向下游工具提供实时数据。

**选项：**
- `--interval <dur>` / `-i` — 查询间隔：30 秒、1 分钟、5 分钟、15 分钟（默认：5 分钟）
- `--webhook <url>` — 将新推文以 JSON 格式发送到指定的 URL（例如 Slack、Discord、n8n 等）
- `--jsonl` — 以 JSONL 格式输出结果（便于通过管道传输到 `tee`, `jq` 等工具）
- `--quiet` — 禁止显示每次查询的头部信息（仅显示推文内容）
- `--limit N` — 每次查询显示的最大推文数量
- `--sort likes|impressions|retweets|recent` — 排序方式

按 `Ctrl+C` 停止监控任务——系统会显示任务统计信息（执行时间、总查询次数、新发现的推文数量、总费用）。

**示例：**
```bash
bun run xint.ts watch "solana memecoins" --interval 5m
bun run xint.ts watch "@vitalikbuterin" --interval 1m
bun run xint.ts watch "AI agents" -i 30s --webhook https://hooks.slack.com/...
bun run xint.ts watch "breaking news" --jsonl | tee -a feed.jsonl
```

**代理使用说明：** 当需要持续监控某个话题时，可以使用 `watch` 命令。如需一次性检查，可以使用 `search` 命令。如果每日预算被超出，`watch` 命令会自动停止。

### 关注者变化跟踪（Diff）

```bash
bun run xint.ts diff <@username> [options]
```

使用本地快照跟踪用户关注者数量的变化。首次运行时会创建一个基准数据；后续运行会显示自上次检查以来新增或取消关注的账户。

**选项：**
- `--following` — 跟踪用户关注的用户（而非用户自己的关注者）
- `--history` — 查看该用户的所有保存的快照
- `--json` — 以结构化 JSON 格式输出
- `--pages N` — 每页显示的关注者数量（默认：5 页，每页 1000 人）

需要使用 OAuth 进行操作（请先运行 `auth setup` 命令）。快照保存在 `data/snapshots/` 目录下。

**示例：**
```bash
bun run xint.ts diff @vitalikbuterin          # First run: create snapshot
bun run xint.ts diff @vitalikbuterin          # Later: show changes
bun run xint.ts diff @0xNyk --following       # Track who you follow
bun run xint.ts diff @solana --history        # View snapshot history
```

**代理使用说明：** 使用 `diff` 命令来检测被监控账户的关注者变化。可以与 `watch` 命令结合使用，以实现全面的账户监控。建议定期（例如每天）运行该命令以记录关注者变化的历史记录。

### 报告生成（Report）

```bash
bun run xint.ts report "<topic>" [options]
```

生成包含搜索结果、可选的 sentiment 分析以及通过 Grok 进行的智能总结的 Markdown 报告。

**选项：**
- `--sentiment` — 包含每条推文的 sentiment 分析结果
- `--accounts @user1,@user2` — 包含特定用户的活动记录
- `--model <name>` — 用于生成智能总结的 Grok 模型（默认：grok-3-mini）
- `--pages N` — 要获取的搜索页面数（默认：2 页）
- `--save` — 将报告保存到 `data/exports/`

**示例：**
```bash
bun run xint.ts report "AI agents"
bun run xint.ts report "solana" --sentiment --accounts @aaboronkov,@rajgokal --save
bun run xint.ts report "crypto market" --model grok-3 --sentiment --save
```

**代理使用说明：** 当用户需要关于某个话题的详细报告时，可以使用 `report` 命令。该命令会一次性执行搜索、情感分析和总结操作，并生成结构化的 Markdown 报告。如需快速查看结果，可以使用 `search --quick` 命令。

### 费用管理**

```bash
bun run xint.ts costs                     # Today's costs
bun run xint.ts costs week                # Last 7 days
bun run xint.ts costs month               # Last 30 days
bun run xint.ts costs all                 # All time
bun run xint.ts costs budget              # Show budget info
bun run xint.ts costs budget set 2.00     # Set daily limit to $2
bun run xint.ts costs reset               # Reset today's data
```

记录每次 API 调用的费用，并提供每日费用汇总及可配置的预算限制。

### 收藏夹列表（Watchlist）

```bash
bun run xint.ts watchlist                       # Show all
bun run xint.ts watchlist add <user> [note]     # Add account
bun run xint.ts watchlist remove <user>         # Remove account
bun run xint.ts watchlist check                 # Check recent from all
```

### 认证（Auth）

**所需权限：** `bookmark.read`, `bookmark.write`, `tweet.read`, `users.read`, `like.read`, `like.write`, `follows.read`, `offline.access`

### 缓存（Cache）

**缓存策略：** 缓存有效期为 15 分钟，以避免重复请求相同的数据。

## 研究流程（代理使用指南）

在进行深入研究时（而不仅仅是简单搜索），请按照以下步骤操作：

### 1. 将问题分解为多个查询**

将研究问题转化为 3-5 个关键词查询：
- **核心查询**：直接与主题相关的关键词
- **专家观点**：指定专家的推文
- **问题点**：如 `(broken OR bug OR issue OR migration)` 等关键词
- **正面信号**：如 `(shipped OR love OR fast OR benchmark)` 等关键词
- **链接**：如 `url:github.com` 或特定域名的链接
- **减少无关内容**：使用 `-is:retweet`（系统自动添加），如有需要可添加 `-is:reply`

### 2. 执行搜索并提取结果**

通过 CLI 执行每个查询。每次查询后，评估以下内容：
- 这些结果是有用的信息还是无关内容？根据需要调整查询条件。
- 哪些专家的观点值得进一步关注？
- 哪些话题链值得深入分析？

### 3. 跟踪相关话题链**

当某条推文的互动量较高或它是一个话题的发起者时，可以使用 `thread` 命令进一步探索相关话题链：

```bash
bun run xint.ts thread <tweet_id>
```

### 4. 深入分析链接内容**

搜索结果中现在会包含来自 X API 的文章标题和描述（在输出中标记为 `📰`）。根据这些信息判断哪些链接值得阅读，然后使用 `xint article` 命令获取文章内容：

```bash
bun run xint.ts article <url>               # terminal display
bun run xint.ts article <url> --json         # structured output
bun run xint.ts article <url> --full         # no truncation
```

优先考虑以下类型的链接：
- 被多条推文引用的链接
- 来自互动量较高的推文的链接
- 标题或描述具有深度信息的链接（而不仅仅是简单的链接聚合工具）
- 直接指向与研究主题相关的技术资源的链接

### 5. 使用 Grok 进行分析**

对于复杂的研究任务，可以将搜索结果传递给 Grok 进行进一步分析：

```bash
bun run xint.ts search "topic" --json | bun run xint.ts analyze --pipe "Summarize themes and sentiment"
```

### 6. 整合分析结果**

根据主题对分析结果进行分类：

```
### [Theme/Finding Title]

[1-2 sentence summary]

- @username: "[key quote]" (NL, NI) [Tweet](url)
- @username2: "[another perspective]" (NL, NI) [Tweet](url)

Resources shared:
- [Resource title](url) — [what it is]
```

### 7. 保存结果**

使用 `--save` 选项将分析结果保存到 `data/exports/` 目录。

## 费用管理

所有 API 调用都会被记录在 `data/api-costs.json` 文件中。系统会在费用接近预算限制时发出警告，但不会阻止调用操作。

**X API v2 的按使用量计费的费率：**
- 推文读取（搜索、收藏夹操作、点赞、个人资料查询）：约 0.005 美元/条
- 完整存档搜索：约 0.01 美元/条
- 写入操作（点赞、取消点赞、添加/删除收藏夹）：约 0.01 美元/次
- 个人资料查询：约 0.005 美元/次
- 关注者/被关注者查询：约 0.01 美元/次
- 热门话题查询：约 0.10 美元/次
- Grok AI 服务（情感分析/报告生成）：按 xAI 的收费标准单独计费

**默认每日预算：1.00 美元（可通过 `costs budget set <N>` 进行调整）。**

## 优化建议：
- **内容过多？** 添加 `-is:reply` 选项，使用 `--sort likes` 优化查询范围
- **结果太少？** 使用 `OR` 关键字扩大搜索范围，移除过于具体的查询条件
- **遇到垃圾信息？** 使用 `-airdrop`, `-giveaway`, `-whitelist` 等选项过滤无关内容
- **只关注专家观点？** 使用 `from:` 或 `--min-likes 50` 限制查询范围
- **注重实质内容而非表面现象？** 使用 `has:links` 关键字进行搜索

## 文件结构**

```
xint/
├── SKILL.md           (this file — agent instructions)
├── xint.ts            (CLI entry point)
├── lib/
│   ├── api.ts         (X API wrapper: search, thread, profile, tweet)
│   ├── article.ts     (full article content fetcher via xAI web_search)
│   ├── bookmarks.ts   (bookmark read — OAuth)
│   ├── cache.ts       (file-based cache, 15min TTL)
│   ├── costs.ts       (API cost tracking & budget)
│   ├── engagement.ts  (likes, like/unlike, following, bookmark write — OAuth)
│   ├── followers.ts   (follower/following tracking + snapshot diffs)
│   ├── format.ts      (terminal, markdown, CSV, JSONL formatters)
│   ├── grok.ts        (xAI Grok analysis integration)
│   ├── oauth.ts       (OAuth 2.0 PKCE auth + token refresh)
│   ├── report.ts      (intelligence report generation)
│   ├── sentiment.ts   (AI-powered sentiment analysis via Grok)
│   ├── trends.ts      (trending topics — API + search fallback)
│   └── watch.ts       (real-time monitoring with polling)
├── data/
│   ├── api-costs.json  (cost tracking data)
│   ├── oauth-tokens.json (OAuth tokens — chmod 600)
│   ├── watchlist.json  (accounts to monitor)
│   ├── exports/        (saved research)
│   ├── snapshots/      (follower/following snapshots for diff)
│   └── cache/          (auto-managed)
└── references/
    └── x-api.md        (X API endpoint reference)
```