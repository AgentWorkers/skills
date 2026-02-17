---
name: xint
description: >
  **X Intelligence CLI** — 一个用于在终端中搜索、分析并互动的工具，专门针对 X/Twitter 平台。适用场景包括：  
  1. 当用户输入“x research”、“search x for”、“search twitter for”等指令时，用于查询相关信息；  
  2. 当用户需要了解关于某个主题的公众观点（例如新库发布、API 更改、产品发布、文化事件或行业动态）时；  
  3. 当用户希望获取开发者、专家或社区对某个话题的看法时；  
  4. 当用户需要实时监控 Twitter 上的动态时；  
  5. 当用户希望利用 AI 功能进行数据分析（如情感分析、趋势分析或报告生成）。  
  该工具还支持以下功能：  
  - 书签功能  
  - 点赞/关注（读/写操作）  
  - 热门话题追踪  
  - Grok AI 分析  
  - 成本追踪  
  数据输出格式支持 JSON、JSONL（可管道传输）、CSV 或 Markdown。  
  **注意事项：**  
  - 该工具不适用于发布推文或发送私信（DM）。  
  - 需要 OAuth 认证才能执行与用户信息相关的操作（如书签、点赞、关注及数据对比）。
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
# xint — X 智能命令行工具 (X Intelligence CLI)

这是一个通用的代理研究工具，用于在 X/Twitter 上进行信息收集和分析。它可以将任何研究问题分解为多个针对性的搜索请求，通过迭代优化搜索策略、跟踪相关话题、深入分析链接内容，并最终生成一份详细的报告。

有关 X API 的详细信息（端点、操作符和响应格式），请参阅 `references/x-api.md`。

## 安全注意事项

使用本工具需要敏感的认证信息，请遵循以下指南：

### 认证信息
- **X_BEARER_TOKEN**：用于访问 X API，属于机密信息，仅应在环境变量或 `.env` 文件中设置。
- **XAI_API_KEY**：可选，用于 AI 分析，同样属于机密信息。
- **X_CLIENT_ID**：可选，用于 OAuth 认证，虽然敏感度较低，但也不应公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于集合管理。

### 文件写入
- 本工具会将数据写入 `data/` 目录，包括缓存文件、导出结果和 OAuth 令牌。
- OAuth 令牌的权限设置为 `chmod 600` 以限制访问。
- 在共享数据之前，请仔细检查导出的内容，因为其中可能包含敏感的搜索查询。

### Webhook
- `watch` 命令支持 `--webhook` 选项，可将数据发送到外部 URL。
- 仅使用您自己控制的 Webhook（例如自己的服务器或 Slack/Discord 账户）。
- 不要将敏感的 URL 作为 Webhook 的目标。

### 代理自主性
- 本工具设计为可添加到代理技能目录中。
- 提供了 “克隆到技能目录” 的说明，以便于技能功能的实现。
- 代理在安装新技能之前应先询问是否真的需要该技能。

### 安装
- 在使用 Bun 时，建议优先通过操作系统包管理器进行安装，而不是手动执行 `curl | bash` 命令。
- 在运行任何安装脚本之前，请确保其安全性。

## 命令行工具
所有命令都在本工具的目录下执行：

```bash
# Set your environment variables
export X_BEARER_TOKEN="your-token"
```

### 搜索 (Search)
```bash
bun run xint.ts search "<query>" [options]
```

**选项：**
- `--sort likes|impressions|retweets|recent` — 排序方式（默认：按点赞数排序）
- `--since 1h|3h|12h|1d|7d` — 时间过滤（默认：过去 7 天内）。也支持以分钟（`30m`）或 ISO 时间戳为单位进行过滤。
- `--min-likes N` — 按最低点赞数过滤
- `--min-impressions N` — 按最低浏览量过滤
- `--pages N` — 每页显示的推文数量（默认：1 或 100 条）
- `--limit N` — 显示的最大结果数量（默认：15 条）
- `--quick` — 快速模式：每页显示 1 条推文，自动过滤无关内容，缓存 1 小时，并提供费用统计。
- `--from <username>` — 用于简化 `from:username` 的输入格式。
- `--quality` — 过滤互动较低的推文（点赞数 >= 10）。
- `--no-replies` — 不包括回复。
- `--sentiment` — 使用 Grok 进行每条推文的 sentiment 分析，并显示结果（正面/负面/中性/混合）。
- `--save` — 将结果保存到 `data/exports/`。
- `--json` — 以原始 JSON 格式输出结果。
- `--jsonl` — 每行输出一个 JSON 对象（适用于 Unix 管道操作，如 `| jq`、`| tee`）。
- `--csv` — 以 CSV 格式输出结果，便于电子表格分析。
- `--markdown` — 以 Markdown 格式输出结果。

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

### 个人资料 (Profile)
```bash
bun run xint.ts profile <username> [--count N] [--replies] [--json]
```

获取指定用户的最新推文（默认不包含回复）。

### 话题讨论 (Thread)
```bash
bun run xint.ts thread <tweet_id> [--pages N]
```

根据根推文的 ID 获取完整的讨论线程。

### 单条推文 (Single Tweet)
```bash
bun run xint.ts tweet <tweet_id> [--json]
```

### 文章内容获取 (Article Content Fetcher)
```bash
bun run xint.ts article <url> [--json] [--full] [--ai <prompt>]
```

使用 xAI 的 web_search 工具从任意 URL 获取并提取文章的全部内容。返回包含标题、作者、日期和字数的干净文本。需要 `XAI_API_KEY`。

该工具还支持 X 推文的链接，可以自动从推文中提取相关文章并获取其内容。

**选项：**
- `--json` — 以结构化 JSON 格式输出（包含标题、内容、作者、发布时间和字数）。
- `--full` — 返回完整的文章文本（默认截断为约 5000 个字符）。
- `--model <name>` — 使用的 Grok 模型（默认：grok-4）。
- `--ai <prompt>` — 使用 Grok AI 分析文章内容。

**示例：**
```bash
# Fetch article from URL
bun run xint.ts article https://example.com/blog/post

# Auto-extract article from X tweet URL and analyze
bun run xint.ts article "https://x.com/user/status/123456789" --ai "Summarize key takeaways"

# Fetch + analyze with AI
bun run xint.ts article https://techcrunch.com/article --ai "What are the main points?"

# Full content without truncation
bun run xint.ts article https://blog.example.com/deep-dive --full
```

**代理使用说明：** 当搜索结果中包含文章链接时，可以使用 `article` 命令查看完整内容。搜索结果现在会显示文章的标题和描述（标记为 `📰`），帮助您判断哪些文章值得阅读。优先考虑以下类型的文章：
- 被多条推文引用的文章。
- 来自互动较高的推文的文章。
- 标题或描述在 API 元数据中具有相关性的文章。

### 收藏夹 (Bookmarks)
```bash
bun run xint.ts bookmarks [options]       # List bookmarked tweets
bun run xint.ts bookmark <tweet_id>       # Bookmark a tweet
bun run xint.ts unbookmark <tweet_id>     # Remove a bookmark
```

**收藏夹列表选项：**
- `--limit N` — 显示的最大收藏夹数量（默认：20 个）。
- `--since <dur>` — 按时间过滤（过去 1 小时、1 天等）。
- `--query <text>` — 客户端文本过滤条件。
- `--json` — 以原始 JSON 格式输出。
- `--markdown` — 以 Markdown 格式输出。
- `--save` — 将结果保存到 `data/exports/`。
- `--no-cache` — 跳过缓存。

使用此功能需要 OAuth 认证。请先运行 `auth setup` 命令。

### 点赞 (Likes)
```bash
bun run xint.ts likes [options]           # List your liked tweets
bun run xint.ts like <tweet_id>           # Like a tweet
bun run xint.ts unlike <tweet_id>         # Unlike a tweet
```

**点赞列表选项：** 与收藏夹选项相同。

使用 OAuth 认证，需要 `like.read` 和 `like.write` 权限。

### 关注 (Following)
```bash
bun run xint.ts following [username] [--limit N] [--json]
```

列出您（或其他用户）关注的用户。默认显示当前登录用户的关注列表。

使用 OAuth 认证，需要 `follows.read` 权限。

### 热门话题 (Trends)
```bash
bun run xint.ts trends [location] [options]
```

获取热门话题。首先尝试使用 X 官方 API 的趋势端点；如果该端点不可用，则使用基于搜索的标签频率估算方法。

**选项：**
- `[location]` — 地点名称或 WOEID 编号（默认：全球范围）。
- `--limit N` — 显示的热门话题数量（默认：20 个）。
- `--json` — 以原始 JSON 格式输出。
- `--no-cache` — 跳过 15 分钟的缓存。
- `--locations` — 列出所有已知的位置名称。

**示例：**
```bash
bun run xint.ts trends                    # Worldwide
bun run xint.ts trends us --limit 10      # US top 10
bun run xint.ts trends japan --json       # Japan, JSON output
bun run xint.ts trends --locations        # List all locations
```

### 分析 (Grok AI)
```bash
bun run xint.ts analyze "<query>"                              # Ask Grok a question
bun run xint.ts analyze --tweets <file>                        # Analyze tweets from JSON file
bun run xint.ts search "topic" --json | bun run xint.ts analyze --pipe  # Pipe search results
```

使用 xAI 的 Grok API（兼容 OpenAI）。需要 `XAI_API_KEY`。

**选项：**
- `--model <name>` — 使用的 Grok 模型（默认：grok-3、grok-3-mini 或 grok-2）。
- `--system <prompt>` — 自定义系统提示。
- `--tweets <file>` — 包含推文的 JSON 文件路径。
- `--pipe` — 从标准输入读取推文 JSON 数据。

**示例：**
```bash
bun run xint.ts analyze "What are the top AI agent frameworks right now?"
bun run xint.ts search "AI agents" --json | bun run xint.ts analyze --pipe "Which show product launches?"
bun run xint.ts analyze --model grok-3 "Deep analysis of crypto market sentiment"
```

## xAI X 搜索（无需 Cookie/GraphQL）
如果您想在不使用 Cookie/GraphQL 的情况下获取“最新情感分析”或“X 的最新动态”，可以使用 xAI 的 `x_search` 工具。

**示例脚本：**
```bash
python3 /home/openclaw/.openclaw/skills/xint/scripts/xai_x_search_scan.py --help
```

Jarv cron 工具会在 `workspace-jarv/x-signals/x-search-queries.json` 文件中配置相关查询。

## xAI 集合知识库 (Collections)
```bash
python3 /home/openclaw/.openclaw/skills/xint/scripts/xai_collections.py --help
```

将第一方生成的文件（报告、日志等）存储在 xAI 集合中，并支持后续的语义搜索。

**示例脚本：**
```bash
python3 /home/openclaw/.openclaw/skills/xint/scripts/xai_collections.py --help
```

**环境变量：**
- `XAI_API_KEY`（api.x.ai）：用于文件上传和搜索。
- `XAI_MANAGEMENT_API_KEY`（management-api.x.ai）：用于集合管理和文档附加。

**注意事项：**
- 请勿直接打印环境变量中的密钥。
- 在配置新的定时任务时，建议使用 `--dry-run` 选项进行测试。

### 实时监控 (Watch)
```bash
bun run xint.ts watch "<query>" [options]
```

定期查询搜索结果，仅显示新的推文。适用于监控热门话题、跟踪提及情况或向下游工具推送实时数据。

**选项：**
- `--interval <dur>` / `-i` — 查询间隔（30 秒、1 分钟、5 分钟、15 分钟，默认：5 分钟）。
- `--webhook <url>` — 将新推文作为 JSON 数据发送到此 URL（例如 Slack、Discord 等）。
- `--jsonl` — 以 JSONL 格式输出（便于通过管道传输到 `tee`、`jq` 等工具）。
- `--quiet` — 不显示每次查询的头部信息，仅显示推文内容。
- `--limit N` — 每次查询显示的最大推文数量。
- `--sort likes|impressions|retweets|recent` — 排序方式。

按 `Ctrl+C` 停止监控。该命令会显示会话统计信息（持续时间、总查询次数、新发现的推文数量和总费用）。

**示例：**
```bash
bun run xint.ts watch "solana memecoins" --interval 5m
bun run xint.ts watch "@vitalikbuterin" --interval 1m
bun run xint.ts watch "AI agents" -i 30s --webhook https://hooks.slack.com/...
bun run xint.ts watch "breaking news" --jsonl | tee -a feed.jsonl
```

**代理使用说明：** 当需要持续监控某个话题时，使用 `watch` 命令。如需一次性检查，可以使用 `search` 命令。如果超出每日预算，`watch` 命令会自动停止。

### 关注者变化跟踪 (Diff)
```bash
bun run xint.ts diff <@username> [options]
```

使用本地缓存数据跟踪用户随时间的关注者变化情况。首次运行会生成基准数据，后续运行会显示自上次检查以来的关注/取消关注操作。

**选项：**
- `--following` — 跟踪用户关注的用户（而非用户的关注者）。
- `--history` — 查看该用户的所有保存的缓存数据。
- `--json` — 以结构化 JSON 格式输出。
- `--pages N` — 每页显示的关注者数量（默认：5 个，每页 1000 个）。

使用 OAuth 认证（请先运行 `auth setup` 命令）。缓存数据存储在 `data/snapshots/` 目录中。

**示例：**
```bash
bun run xint.ts diff @vitalikbuterin          # First run: create snapshot
bun run xint.ts diff @vitalikbuterin          # Later: show changes
bun run xint.ts diff @0xNyk --following       # Track who you follow
bun run xint.ts diff @solana --history        # View snapshot history
```

**代理使用说明：** 使用 `diff` 命令检测目标账户的关注者变化。结合 `watch` 命令可进行全面的账户监控。建议定期（例如每天）运行此命令以记录关注者变化的历史。

### 智能报告 (Report)
```bash
bun run xint.ts report "<topic>" [options]
```

生成包含搜索结果、可选的情感分析以及通过 Grok 进行的 AI 摘要的 Markdown 报告。

**选项：**
- `--sentiment` — 包含每条推文的情感分析结果。
- `--accounts @user1,@user2` — 包含指定账户的活动信息。
- `--model <name>` — 用于生成 AI 摘要的 Grok 模型（默认：grok-3-mini）。
- `--pages N` — 获取的搜索页面数量（默认：2 页）。
- `--save` — 将报告保存到 `data/exports/`。

**示例：**
```bash
bun run xint.ts report "AI agents"
bun run xint.ts report "solana" --sentiment --accounts @aaboronkov,@rajgokal --save
bun run xint.ts report "crypto market" --model grok-3 --sentiment --save
```

**代理使用说明：** 当用户需要关于某个话题的详细报告时，使用 `report` 命令。该命令会一次性执行搜索、情感分析和摘要生成，生成结构化的 Markdown 报告。如需快速查看结果，可以使用 `search --quick` 命令。

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

跟踪每次 API 调用的费用，并提供每日费用汇总和可配置的预算限制。

### 关注列表 (Watchlist)
```bash
bun run xint.ts watchlist                       # Show all
bun run xint.ts watchlist add <user> [note]     # Add account
bun run xint.ts watchlist remove <user>         # Remove account
bun run xint.ts watchlist check                 # Check recent from all
```

### 认证 (Auth)
```bash
bun run xint.ts auth setup [--manual]    # Set up OAuth 2.0 (PKCE)
bun run xint.ts auth status              # Check token status
bun run xint.ts auth refresh             # Manually refresh tokens
```

所需权限：`bookmark.read`、`bookmark.write`、`tweet.read`、`users.read`、`like.read`、`like.write`、`follows.read`、`offline.access`。

### 缓存 (Cache)
```bash
bun run xint.ts cache clear    # Clear all cached results
```

缓存有效期为 15 分钟，避免重复请求相同的数据。

## 研究流程（代理使用）
在进行深入研究时（而不仅仅是简单搜索），请按照以下步骤操作：

### 1. 将问题分解为多个查询
将研究问题转化为 3-5 个关键词查询：
- **核心查询**：与主题直接相关的关键词。
- **专家观点**：特定专家的推文。
- **问题点**：如 `(broken OR bug OR issue OR migration)` 等关键词。
- **正面信号**：如 `(shipped OR love OR fast OR benchmark)` 等关键词。
- **链接**：如 `url:github.com` 或特定域名的链接。
- **减少无关内容**：使用 `-is:retweet`（默认添加），如有需要可添加 `-is:reply`。

### 2. 进行搜索并提取结果
通过 CLI 执行每个查询。每次查询后，评估：
- 这些结果是相关内容还是无关信息？根据需要调整查询条件。
- 哪些专家的观点值得进一步研究？
- 哪些讨论线程值得跟踪？
- 哪些链接的资源值得深入分析？

### 3. 跟踪讨论线程
当某条推文的互动较高或是一个讨论的起点时：

### 4. 深入分析链接内容
搜索结果会包含来自 X API 的文章标题和描述（在输出中标记为 `📰`）。根据这些信息判断哪些链接值得阅读，然后使用 `xint article` 命令获取相关文章内容：

**示例：**
```bash
bun run xint.ts article <url>               # terminal display
bun run xint.ts article <url> --json         # structured output
bun run xint.ts article <url> --full         # no truncation
```

优先考虑以下类型的链接：
- 被多条推文引用的链接。
- 来自互动较高的推文的链接。
- 标题或描述具有深度信息的链接（而不仅仅是链接聚合器提供的内容）。
- 直接指向与问题相关的技术资源的链接。

### 5. 使用 Grok 进行分析
对于复杂的研究，将搜索结果传递给 Grok 进行进一步分析：

### 6. 合并分析结果
按主题对分析结果进行分类：

### 7. 保存结果
使用 `--save` 选项将结果保存到 `data/exports/`。

## 费用控制
所有 API 调用都会被记录在 `data/api-costs.json` 文件中。系统会在接近预算限制时发出警告，但不会阻止调用。

**X API v2 的按使用计费规则：**
- 推文读取（搜索、收藏夹、点赞、个人资料查看）：约 0.005 美元/条。
- 完整档案搜索：约 0.01 美元/条。
- 操作（点赞、取消点赞、添加/删除收藏夹）：约 0.01 美元/次。
- 个人资料查询：约 0.005 美元/次。
- 关注者/被关注者查询：约 0.01 美元/条。
- 热门话题查询：约 0.10 美元/次。
- Grok AI 服务（情感分析/报告）：按 xAI 的单独费率计费。

**默认每日预算：$1.00**（可通过 `costs budget set <N>` 进行调整）。

## 优化建议：
- **内容过多？** 添加 `-is:reply`，使用 `--sort likes` 选项缩小搜索范围。
- **结果太少？** 使用 `OR` 扩大搜索范围，移除过于具体的查询条件。
- **垃圾信息过多？** 添加 `-airdrop`、`-giveaway`、`-whitelist` 等过滤条件。
- **只关注专家观点？** 使用 `from:` 或 `--min-likes 50` 限制。
- **注重实质内容而非表面现象？** 使用 `has:links` 进行搜索。

## 文件结构
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