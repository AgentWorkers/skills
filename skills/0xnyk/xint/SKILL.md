---
name: xint
description: >
  **X Intelligence CLI** — 一款用于在终端中搜索、分析并互动 Twitter 内容的工具。适用场景包括：  
  1. 当用户输入“x research”、“search x for”、“search twitter for”等指令时，用于查询相关信息；  
  2. 当用户需要了解 Twitter 上的讨论内容（如新库发布、API 变更、产品发布、行业动态等）时；  
  3. 当用户想了解开发者、专家或社区对某个话题的看法时；  
  4. 当用户需要实时监控 Twitter 上的动态时；  
  5. 当用户希望利用 AI 进行内容分析（如情感分析、报告生成等）。  
  该工具还支持以下功能：  
  - 书签功能  
  - 点赞/关注（读写操作）  
  - 跟踪热门话题  
  - 使用 Grok AI 进行内容分析  
  - 成本跟踪  
  数据输出格式支持 JSON、JSONL（可管道传输）、CSV 或 Markdown。  
  **注意事项：**  
  - 该工具不支持发布推文或发送私信（DM），也不提供企业级功能。  
  - 所有涉及用户上下文的操作（如书签、点赞、关注、数据对比等）均需通过 OAuth 认证。
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
required_env_vars:
  - X_BEARER_TOKEN
requiredEnvVars:
  - X_BEARER_TOKEN
primary_credential: X_BEARER_TOKEN
primaryCredential: X_BEARER_TOKEN
security:
  always: false
  autonomous: false
  local_data_dir: data/
  network_endpoints:
    - https://api.x.com
    - https://x.com
    - https://api.x.ai
---
# xint — X 智能命令行工具

这是一个通用的代理研究工具，用于在 X/Twitter 上进行信息收集和分析。它可以将任何研究问题分解为具体的搜索请求，通过迭代优化搜索策略，跟踪相关话题的讨论线索，深入分析链接内容，并最终生成一份详细的报告。

有关 X API 的详细信息（端点、操作符和响应格式），请参阅 `references/x-api.md`。

## 安全注意事项

使用本工具需要敏感的认证信息。请遵循以下指南：

### 认证信息
- **X_BEARER_TOKEN**：X API 所需的令牌。请将其视为机密信息，仅设置在环境变量或 `.env` 文件中。
- **XAI_API_KEY**：可选，用于 AI 分析。同样属于机密信息。
- **X_CLIENT_ID**：可选，用于 OAuth 认证。虽然敏感度较低，但不要公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于集合管理。

### 文件写入
- 本工具会将数据写入 `data/` 目录：包括缓存文件、导出文件和 OAuth 令牌。
- OAuth 令牌的权限设置为 `chmod 600`，以防止未经授权的访问。
- 在共享数据之前，请仔细检查其中是否包含敏感的搜索查询。

### Webhook
- `watch` 和 `stream` 命令可以将数据发送到指定的 Webhook 端点。
- 远程端点必须使用 `https://` 协议（`http://` 仅适用于本地或回环测试）。
- 可以配置允许的 Webhook 主机列表：`XINT_WEBHOOK_ALLOWED_HOSTS=hooks.example.com,*.internal.example`。
- 避免将敏感的搜索查询或包含令牌的 URL 发送到第三方服务器。

### 运行时注意事项
- 本文档仅用于说明用途，不会修改系统的运行时提示或行为。
- 网络监听功能是可选的（通过 `mcp --sse` 启用），默认情况下是禁用的。
- Webhook 功能也是可选的（通过 `--webhook` 启用），默认情况下是禁用的。

### 安装
- 如果可能的话，建议使用操作系统的包管理器来安装 xint，而不是手动执行 `curl | bash` 命令。
- 在使用安装脚本之前，请务必验证其完整性。

### MCP 服务器（可选）
- 使用 `bun run xint.ts mcp` 命令可以启动一个本地的 MCP 服务器，将 xint 命令作为工具提供。
- 默认模式下，数据通过标准输入/输出（stdio）进行传输；除非明确启用 `--sse`，否则不会启动外部 Web 服务器。
- 请遵守 `--policy read_only|engagement|moderation` 策略以及预算限制。

## 命令行工具说明

所有命令都在项目目录下执行：

### 搜索
```bash
# Set your environment variables
export X_BEARER_TOKEN="your-token"
```

**选项：**
- `--sort likes|impressions|retweets|recent` — 排序方式（默认：按点赞数排序）
- `--since 1h|3h|12h|1d|7d` — 时间筛选条件（默认：过去 7 天内的数据）。也可以使用分钟（`30m`）或 ISO 时间戳。
- `--min-likes N` — 根据最低点赞数筛选结果。
- `--min-impressions N` — 根据最低浏览量筛选结果。
- `--pages N` — 每页显示的推文数量（默认：1 或 100 条推文/页）。
- `--limit N` — 显示的最大结果数量（默认：15 条）。
- `--quick` — 快速模式：每页显示 1 条推文，最多显示 10 条结果，自动过滤无关内容，缓存有效期为 1 小时，并提供费用统计。
- `--from <username>` — 简写形式，等同于 `from:username`。
- `--quality` — 筛选互动性较低的推文（至少获得 10 个点赞）。
- `--no-replies` — 不显示回复内容。
- `--sentiment` — 使用 Grok 进行每条推文的 sentiment 分析（显示正面/负面/中性/混合的评分）。
- `--save` — 将结果保存到 `data/exports/` 目录。
- `--json` — 以原始 JSON 格式输出结果。
- `--jsonl` — 每行输出一个 JSON 对象（适用于 Unix 管道操作，如 `| jq`, `| tee`）。
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

### 查看用户资料
```bash
bun run xint.ts profile <username> [--count N] [--replies] [--json]
```

用于获取指定用户的最新推文（默认不显示回复内容）。

### 跟踪话题讨论线索
```bash
bun run xint.ts thread <tweet_id> [--pages N]
```

根据根推文的 ID 获取整个讨论线索。

### 查看单条推文
```bash
bun run xint.ts tweet <tweet_id> [--json]
```

### 获取文章全文
```bash
bun run xint.ts article <url> [--json] [--full] [--ai <text>]
```

使用 xAI 的 web_search 工具（基于 Grok）从任意 URL 获取并提取文章全文。返回包含标题、作者、日期和字数的干净文本。需要 `XAI_API_KEY`。

**选项：**
- `--json` — 以结构化 JSON 格式输出文章信息（标题、内容、作者、发布时间、字数）。
- `--full` — 返回完整的文章文本（默认截断为约 5000 个字符）。
- `--model <name>` — 使用指定的 Grok 模型进行分析（默认使用 grok-4）。
- `--ai <text>` — 使用 Grok AI 对文章内容进行分析。

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

**代理使用说明：**当搜索结果中包含文章链接时，可以使用 `article` 命令查看文章全文。搜索结果现在会显示文章的标题和描述（标记为 `📰`），帮助你判断哪些文章值得阅读。优先考虑以下类型的文章：
- 被多条推文引用的文章。
- 来自互动性较高的推文的文章。
- 标题或描述在 API 元数据中具有相关性的文章。

### 添加书签
```bash
bun run xint.ts bookmarks [options]       # List bookmarked tweets
bun run xint.ts bookmark <tweet_id>       # Bookmark a tweet
bun run xint.ts unbookmark <tweet_id>     # Remove a bookmark
```

**书签列表选项：**
- `--limit N` — 显示的最大书签数量（默认：20 个）。
- `--since <dur>` — 根据时间筛选书签（1 小时、1 天、7 天等）。
- `--query <text>` — 客户端文本筛选条件。
- `--json` — 以原始 JSON 格式输出书签信息。
- `--markdown` — 以 Markdown 格式输出书签信息。
- `--save` — 将书签保存到 `data/exports/` 目录。
- `--no-cache` — 禁用缓存。

使用此功能需要 OAuth 认证。请先运行 `auth setup` 命令。

### 查看点赞记录
```bash
bun run xint.ts likes [options]           # List your liked tweets
bun run xint.ts like <tweet_id>           # Like a tweet
bun run xint.ts unlike <tweet_id>         # Unlike a tweet
```

**点赞记录选项：**与添加书签的选项相同。

使用此功能需要 OAuth 认证，并具有 `like.read` 和 `like.write` 权限。

### 关注账户
```bash
bun run xint.ts following [username] [--limit N] [--json]
```

列出你（或其他用户）关注的所有账户。默认显示当前登录用户的关注列表。

使用此功能需要 OAuth 认证，并具有 `follows.read` 权限。

### 获取热门趋势
```bash
bun run xint.ts trends [location] [options]
```

获取当前的热门话题。首先尝试使用 X 官方 API 的趋势端点；如果该端点不可用，则使用基于搜索的哈希标签频率估算方法。

**选项：**
- `[location]` — 地点名称或 WOEID 编号（默认：全球范围）。
- `--limit N` — 显示的热门话题数量（默认：20 个）。
- `--json` — 以原始 JSON 格式输出结果。
- `--no-cache` — 禁用 15 分钟的缓存机制。
- `--locations` — 列出所有已知的位置名称。

**示例：**
```bash
bun run xint.ts trends                    # Worldwide
bun run xint.ts trends us --limit 10      # US top 10
bun run xint.ts trends japan --json       # Japan, JSON output
bun run xint.ts trends --locations        # List all locations
```

### 使用 Grok AI 进行分析
```bash
bun run xint.ts analyze "<query>"                              # Ask Grok a question
bun run xint.ts analyze --tweets <file>                        # Analyze tweets from JSON file
bun run xint.ts search "topic" --json | bun run xint.ts analyze --pipe  # Pipe search results
```

使用 xAI 的 Grok API（兼容 OpenAI）。需要 `XAI_API_KEY`（在环境变量或 `.env` 文件中设置）。

**选项：**
- `--model <name>` — 使用指定的 Grok 模型（默认：grok-3, grok-3-mini, grok-2）。
- `--tweets <file>` — 指定包含推文的 JSON 文件路径。
- `--pipe` — 从标准输入读取推文 JSON 数据。

**示例：**
```bash
bun run xint.ts analyze "What are the top AI agent frameworks right now?"
bun run xint.ts search "AI agents" --json | bun run xint.ts analyze --pipe "Which show product launches?"
bun run xint.ts analyze --model grok-3 "Deep analysis of crypto market sentiment"
```

## 使用 xAI 进行无 cookie/GraphQL 的搜索
```bash
python3 scripts/xai_x_search_scan.py --help
```

如果需要在不使用 cookie/GraphQL 的情况下获取“最近的趋势信息”或“X 的最新动态”，可以使用 xAI 提供的 `x_search` 工具。

### 管理 xAI 收集的内容
```bash
python3 scripts/xai_collections.py --help
```

将第一方生成的文件（报告、日志等）存储在 xAI 的集合中，并支持后续的语义搜索。

**环境变量设置：**
- `XAI_API_KEY`（api.x.ai）：用于文件上传和搜索操作。
- `XAI_MANAGEMENT_API_KEY`（management-api.x.ai）：用于集合管理和文档附加。

**注意事项：**
- 请勿直接打印这些环境变量的值。
- 在设置新的定时任务时，建议使用 `--dry-run` 选项进行测试。

### 实时监控
```bash
bun run xint.ts watch "<query>" [options]
```

定期查询指定的搜索内容，仅显示新发布的推文。适用于监控特定话题、跟踪提及情况或向下游工具传递实时数据。

**选项：**
- `--interval <dur>` / `-i` — 查询间隔（30 秒、1 分钟、5 分钟、15 分钟，默认：5 分钟）。
- `--webhook <url>` — 将新推文作为 JSON 数据发送到指定的 URL（远程主机需要使用 `https://` 协议）。
- `--jsonl` — 以 JSONL 格式输出结果（便于通过管道传输到 `tee`, `jq` 等工具）。
- `--quiet` — 禁止显示每次查询的头部信息，仅显示推文内容。
- `--limit N` — 每次查询显示的最大推文数量。
- `--sort likes|impressions|retweets|recent` — 排序方式。

按 `Ctrl+C` 停止监控。系统会显示监控统计信息（持续时间、总查询次数、新发现的推文数量、总费用）。

**示例：**
```bash
bun run xint.ts watch "solana memecoins" --interval 5m
bun run xint.ts watch "@vitalikbuterin" --interval 1m
bun run xint.ts watch "AI agents" -i 30s --webhook https://hooks.example.com/ingest
bun run xint.ts watch "breaking news" --jsonl | tee -a feed.jsonl
```

**代理使用说明：**当需要持续监控某个话题时，可以使用 `watch` 命令。如需一次性检查，可以使用 `search` 命令。如果超过每日预算限制，`watch` 命令会自动停止。

### 跟踪关注者变化
```bash
bun run xint.ts diff <@username> [options]
```

使用本地缓存数据跟踪用户随时间的关注者变化情况。首次运行会创建一个基准数据；后续运行会显示自上次检查以来新增或取消关注的账户。

**选项：**
- `--following` — 跟踪用户关注了哪些账户。
- `--history` — 查看该用户的所有保存的关注者信息。
- `--json` — 以结构化 JSON 格式输出结果。
- `--pages N` — 每页显示的关注者数量（默认：5 个，每页 1000 个）。

使用此功能需要 OAuth 认证（请先运行 `auth setup` 命令）。缓存数据存储在 `data/snapshots/` 目录中。

**示例：**
```bash
bun run xint.ts diff @vitalikbuterin          # First run: create snapshot
bun run xint.ts diff @vitalikbuterin          # Later: show changes
bun run xint.ts diff @0xNyk --following       # Track who you follow
bun run xint.ts diff @solana --history        # View snapshot history
```

**代理使用说明：**使用 `diff` 命令检测被监控账户的关注者变化。可以结合 `watch` 命令进行全面的账户监控。建议定期（例如每天）运行此命令以记录关注者变化的历史。

### 生成智能报告
```bash
bun run xint.ts report "<topic>" [options]
```

生成包含搜索结果、可选的 sentiment 分析以及通过 Grok 进行的 AI 总结的 Markdown 报告。

**选项：**
- `--sentiment` — 包含每条推文的 sentiment 分析结果。
- `--accounts @user1,@user2` — 包含特定账户的活动信息。
- `--model <name>` — 使用指定的 Grok 模型进行情感分析（默认：grok-3-mini）。
- `--pages N` — 每页显示的搜索结果数量（默认：2 页）。
- `--save` — 将报告保存到 `data/exports/` 目录。

**示例：**
```bash
bun run xint.ts report "AI agents"
bun run xint.ts report "solana" --sentiment --accounts @aaboronkov,@rajgokal --save
bun run xint.ts report "crypto market" --model grok-3 --sentiment --save
```

**代理使用说明：**当用户需要关于某个话题的全面报告时，可以使用 `report` 命令。该命令会一次性执行搜索、情感分析和总结，生成结构化的 Markdown 报告。如需快速查看结果，可以使用 `search --quick` 命令。

### 费用管理
```bash
bun run xint.ts costs                     # Today's costs
bun run xint.ts costs week                # Last 7 days
bun run xint.ts costs month               # Last 30 days
bun run xint.ts costs all                 # All time
bun run xint.ts costs budget              # Show budget info
bun run xint.ts costs budget set 2.00     # Set daily limit to $2
bun run xint.ts costs reset               # Reset today's data
```

记录每次 API 调用的费用，并提供每日费用汇总和可配置的预算限制。

### 监控列表
```bash
bun run xint.ts watchlist                       # Show all
bun run xint.ts watchlist add <user> [note]     # Add account
bun run xint.ts watchlist remove <user>         # Remove account
bun run xint.ts watchlist check                 # Check recent from all
```

### 认证信息
```bash
bun run xint.ts auth setup [--manual]    # Set up OAuth 2.0 (PKCE)
bun run xint.ts auth status              # Check token status
bun run xint.ts auth refresh             # Manually refresh tokens
```

所需权限：`bookmark.read`, `bookmark.write`, `tweet.read`, `users.read`, `like.read`, `like.write`, `follows.read`, `offline.access`。

### 缓存机制
```bash
bun run xint.ts cache clear    # Clear all cached results
```

缓存数据的有效期为 15 分钟，以避免重复请求相同的数据。

## 研究流程（代理使用指南）

在进行深入研究时（而不仅仅是简单搜索），请按照以下步骤操作：

### 1. 将问题分解为具体的搜索请求
将研究问题转化为 3-5 个关键词查询：
- **核心查询**：与主题直接相关的关键词。
- **专家观点**：特定专家的推文。
- **问题点**：如 `(broken OR bug OR issue OR migration)` 等关键词。
- **积极信号**：如 `(shipped OR love OR fast OR benchmark)` 等关键词。
- **链接**：如 `url:github.com` 或特定的域名。
- **减少无关内容**：使用 `-is:retweet`（默认添加），如有需要可添加 `-is:reply`。

### 2. 执行搜索并提取结果
通过命令行执行每个查询。执行后，评估以下内容：
- 这些结果是有用的信息还是无用的噪音？
- 哪些专家的观点值得进一步关注（使用 `from:` 进行筛选）？
- 哪些讨论线索值得深入分析（使用 `thread` 命令）？
- 哪些链接的资源值得深入研究？

### 3. 跟踪讨论线索
当某条推文的互动性较高或是一个讨论的起点时：

### 4. 深入分析链接内容
搜索结果中会包含来自 X API 的文章标题和描述（在输出中标记为 `📰`）。根据这些信息判断哪些链接值得阅读，然后使用 `xint article` 命令获取文章内容：

**优先考虑以下类型的链接：**
- 被多条推文引用的链接。
- 来自互动性较高的推文的链接。
- 标题或描述具有相关性的链接（而不仅仅是链接聚合器提供的内容）。
- 直接指向与研究问题相关的技术资源的链接。

### 5. 使用 Grok 进行分析
对于复杂的研究任务，可以将搜索结果传递给 Grok 进行进一步分析：

### 6. 整合分析结果
按照主题对分析结果进行分类：

### 7. 保存结果
使用 `--save` 选项将结果保存到 `data/exports/` 目录。

## 费用管理
所有 API 调用都会被记录在 `data/api-costs.json` 文件中。系统会在接近预算限制时发出警告，但不会阻止调用。

**X API v2 的按使用量计费的费率：**
- 推文读取（搜索、添加书签、点赞、查看用户资料）：约 0.005 美元/条。
- 完整存档搜索：约 0.01 美元/条。
- 操作操作（点赞、取消点赞、添加/删除书签）：约 0.01 美元/次。
- 查看用户资料：约 0.005 美元/次。
- 关注者/被关注者查询：约 0.01 美元/次。
- 热门趋势查询：约 0.10 美元/次。
- 使用 Grok AI 的功能（情感分析/报告）：费用单独计费（不包含在 X API 费用中）。

默认每日预算为 1.00 美元（可通过 `costs budget set <N>` 进行调整）。

## 优化建议：
- **内容过多？** 使用 `-is:reply` 选项，或通过 `--sort likes` 筛选结果，缩小搜索范围。
- **结果太少？** 使用 `OR` 关键字扩大搜索范围，或移除过于具体的筛选条件。
- **遇到垃圾信息？** 使用 `--$, -airdrop, -giveaway, -whitelist` 选项进行过滤。
- **只关注专家观点？** 使用 `from:` 或 `--min-likes 50` 选项进行筛选。
- **关注实质内容而非表面现象？** 使用 `has:links` 进行搜索。

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