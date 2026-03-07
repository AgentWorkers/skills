---
name: xint
description: >
  **X Intelligence CLI** — 一个用于在终端中搜索、分析并互动X/Twitter内容的工具。适用场景包括：  
  1. 当用户询问“关于X的研究”、“在X上搜索某内容”、“在Twitter上搜索某内容”、“人们都在说什么”、“Twitter上有什么动态”、“检查X的最新情况”等时；  
  2. 当用户正在处理需要X平台最新动态作为背景信息的工作时（例如新库发布、API变更、产品发布、文化事件、行业动态等）；  
  3. 当用户想了解开发者、专家或社区对某个话题的看法时；  
  4. 当用户需要实时监控（如“观看”相关内容）或进行AI驱动的分析（如“情感分析”、“报告分析结果”）时。  
  该工具还支持以下功能：  
  - 添加书签  
  - 给内容点赞  
  - 关注/取消关注（支持读写操作）  
  - 跟踪热门话题  
  - 使用Grok AI进行内容分析  
  - 跟踪相关成本（如数据消耗等）  
  支持的数据导出格式包括：JSON、JSONL（可管道传输）、CSV和Markdown。  
  **注意事项：**  
  - 该工具不适用于发布推文或发送私信（DM）。  
  - 需要OAuth认证才能执行与用户信息相关的操作（如添加书签、点赞、关注、比较数据等）。
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
primary_credential: X_BEARER_TOKEN
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

这是一个通用的代理研究工具，用于在 X/Twitter 上进行搜索和分析。它可以将任何研究问题分解为具体的搜索请求，通过迭代优化搜索策略，跟踪相关话题的讨论线索，深入挖掘链接内容，并将这些信息整合成一份详细的报告。

有关 X API 的详细信息（端点、操作符和响应格式），请参阅 `references/x-api.md`。

## 安全注意事项

使用此工具需要敏感的凭据。请遵循以下指南：

### 凭据
- **X_BEARER_TOKEN**：用于访问 X API。请将其视为机密信息——建议将其设置为环境变量（项目本地 `.env` 文件中的变量）。
- **XAI_API_KEY**：可选，用于 AI 分析。同样属于机密信息。
- **X_CLIENT_ID**：可选，用于 OAuth 认证。虽然敏感度较低，但也不应公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于管理数据集合。

### 文件写入
- 该工具会将数据写入 `data/` 目录：包括缓存文件、导出的数据、快照以及 OAuth 令牌。
- OAuth 令牌的权限设置为 `chmod 600` 以限制访问。
- 在共享数据之前，请务必检查其中是否包含敏感的搜索查询内容。

### Webhook
- `watch` 和 `stream` 功能可以将数据发送到指定的 Webhook 端点。
- 远程 Webhook 端点必须使用 `https://` 协议（`http://` 仅适用于本地或回环测试）。
- 可以配置允许的 Webhook 主机列表：`XINT_WEBHOOK_ALLOWED_HOSTS=hooks.example.com,*.internal.example`。
- 避免将敏感的搜索查询或包含令牌的 URL 发送到第三方服务器。

### 运行时注意事项
- 本文档仅描述了该命令行工具的使用方法和安全控制措施。
- 网络监听功能是可选的（通过 `mcp --sse` 参数启用），默认情况下是禁用的。
- Webhook 功能也是可选的（通过 `--webhook` 参数启用），默认情况下是禁用的。

### 安装
- 如果可能的话，建议使用操作系统的包管理器来安装该工具，而不是通过 `curl | bash` 命令手动安装。
- 在运行任何安装脚本之前，请务必验证其完整性。

### MCP 服务器（可选）
- 使用 `bun run xint.ts mcp` 命令可以启动一个本地的 MCP 服务器，从而提供 xint 命令的接口。
- 默认模式下，数据会直接输出到标准输出（stdout）或本地文件；除非明确启用 `--sse` 参数，否则不会启动外部 Web 服务器。
- 请遵守 `--policy read_only|engagement|moderation` 等配置选项，以控制数据的使用权限。

## 命令行工具（CLI）

所有命令都在项目目录下执行：

### 搜索（Search）
```bash
# Set your environment variables
export X_BEARER_TOKEN="your-token"
```

**选项：**
- `--sort likes|impressions|retweets|recent` — 排序方式（默认：按点赞数排序）
- `--since 1h|3h|12h|1d|7d` — 时间过滤条件（默认：过去 7 天内的数据）。也支持以分钟（`30m`）或 ISO 时间戳为单位进行过滤。
- `--min-likes N` — 按最低点赞数过滤结果。
- `--min-impressions N` — 按最低浏览量过滤结果。
- `--pages N` — 每页显示的推文数量（默认：1 或 100 条推文/页）。
- `--limit N` — 显示的最大结果数量（默认：15 条）。
- `--quick` — 快速模式：仅显示第 1 页的内容，最多显示 10 条结果，自动过滤无关内容，使用 1 小时的缓存，并提供费用统计信息。
- `--from <username>` — 用于简化查询中的 `from:username` 参数。
- `--quality` — 过滤互动次数较低的推文（至少获得 10 个点赞）。
- `--no-replies` — 不显示回复内容。
- `--sentiment` — 使用 Grok 进行每条推文的 sentiment 分析，并显示分析结果（正面/负面/中性/混合）。
- `--save` — 将搜索结果保存到 `data/exports/` 目录。
- `--json` — 以原始 JSON 格式输出结果。
- `--jsonl` — 每行输出一个 JSON 对象（适用于 Unix 管道操作，例如 `| jq`, `| tee`）。
- `--csv` — 以 CSV 格式输出结果，便于导入电子表格进行分析。
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

### 个人资料（Profile）
```bash
bun run xint.ts profile <username> [--count N] [--replies] [--json]
```

用于获取指定用户的最新推文（默认情况下不显示回复内容）。

### 话题讨论（Thread）
```bash
bun run xint.ts thread <tweet_id> [--pages N]
```

根据根推文的 ID 获取整个讨论话题的完整内容。

### 单条推文（Single Tweet）
```bash
bun run xint.ts tweet <tweet_id> [--json]
```

### 文章内容获取（Article）
```bash
bun run xint.ts article <url> [--json] [--full] [--ai <text>]
```

使用 xAI 的 web_search 工具从任意 URL 获取并提取文章的完整内容（Grok 用于解析页面内容）。返回包含标题、作者、发布日期和字数的信息。需要 `XAI_API_KEY`。

**选项：**
- `--json` — 以结构化 JSON 格式输出文章信息（标题、内容、作者、发布时间、字数）。
- `--full` — 显示完整的文章内容（默认情况下内容会被截断至约 5000 个字符）。
- `--model <name>` — 使用指定的 Grok 模型进行解析（默认使用 grok-4）。
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

**代理使用说明：** 当搜索结果中包含文章链接时，可以使用 `article` 命令来阅读文章的完整内容。搜索结果会显示文章的标题和描述（以 `📰` 标识）。优先选择以下类型的文章：
- 被多条推文引用的文章。
- 来自互动频繁的推文的文章。
- 标题或描述在 API 元数据中具有相关性的文章。

### 收藏夹（Bookmarks）
```bash
bun run xint.ts bookmarks [options]       # List bookmarked tweets
bun run xint.ts bookmark <tweet_id>       # Bookmark a tweet
bun run xint.ts unbookmark <tweet_id>     # Remove a bookmark
```

**收藏夹列表选项：**
- `--limit N` — 显示的最大收藏夹数量（默认：20 个）。
- `--since <dur>` — 按时间过滤收藏夹（1 小时、1 天等）。
- `--query <text>` — 客户端文本过滤条件。
- `--json` — 以原始 JSON 格式输出结果。
- `--markdown` — 以 Markdown 格式输出结果。
- `--save` — 将收藏夹信息保存到 `data/exports/` 目录。
- `--no-cache` — 禁用缓存功能。

使用此功能需要 OAuth 认证。请先运行 `auth setup` 命令进行设置。

### 点赞（Likes）
```bash
bun run xint.ts likes [options]           # List your liked tweets
bun run xint.ts like <tweet_id>           # Like a tweet
bun run xint.ts unlike <tweet_id>         # Unlike a tweet
```

**点赞列表选项：** 与收藏夹选项相同（`--limit`, `--since`, `--query`, `--json`, `--no-cache`）。

使用此功能需要 `like.read` 和 `like.write` 权限。

### 关注（Following）
```bash
bun run xint.ts following [username] [--limit N] [--json]
```

列出你（或其他用户）关注的用户列表。默认显示当前登录用户的关注列表。

使用此功能需要 `follows.read` 权限。

### 热门话题（Trends）
```bash
bun run xint.ts trends [location] [options]
```

获取热门话题的信息。首先尝试使用 X 官方的趋势端点；如果该端点不可用，则会使用基于搜索的哈希标签频率估计方法来获取热门话题。

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

### 分析（Grok AI）
```bash
bun run xint.ts analyze "<query>"                              # Ask Grok a question
bun run xint.ts analyze --tweets <file>                        # Analyze tweets from JSON file
bun run xint.ts search "topic" --json | bun run xint.ts analyze --pipe  # Pipe search results
```

使用 xAI 的 Grok API（兼容 OpenAI）。需要 `XAI_API_KEY`。

**选项：**
- `--model <name>` — 使用指定的 Grok 模型进行解析（默认使用 grok-3 或 grok-3-mini）。
- `--tweets <file>` — 指定包含推文的 JSON 文件路径。
- `--pipe` — 从标准输入（stdin）读取推文数据。

**示例：**
```bash
bun run xint.ts analyze "What are the top AI agent frameworks right now?"
bun run xint.ts search "AI agents" --json | bun run xint.ts analyze --pipe "Which show product launches?"
bun run xint.ts analyze --model grok-3 "Deep analysis of crypto market sentiment"
```

## xAI X 搜索（无需 Cookie/GraphQL）**

如果你想在不使用 Cookie 或 GraphQL 的情况下获取“最新趋势”或“X 的最新动态”，可以使用 xAI 提供的 `x_search` 工具。

**示例脚本：**
```bash
python3 scripts/xai_x_search_scan.py --help
```

## xAI 数据集合管理（Files + Collections）
```bash
python3 scripts/xai_collections.py --help
```

将第一方生成的文件（如报告、日志等）存储在 xAI 的数据集合中，并允许后续进行语义搜索。

**示例脚本：**
```bash
python3 scripts/xai_collections.py --help
```

**环境变量设置：**
- `XAI_API_KEY`（api.x.ai）：用于文件上传和搜索操作。
- `XAI_MANAGEMENT_API_KEY`（management-api.x.ai）：用于数据集合管理和文件上传。

**注意事项：**
- 请勿直接打印这些环境变量的值。
- 在设置新的定时任务时，建议使用 `--dry-run` 选项进行测试。

### 实时监控（Watch）
```bash
bun run xint.ts watch "<query>" [options]
```

定期查询指定的搜索内容，仅显示新的推文。适用于监控热点话题、跟踪提及情况或向下游工具传递实时数据。

**选项：**
- `--interval <dur>` / `-i` — 查询间隔（30 秒、1 分钟、5 分钟、15 分钟，默认：5 分钟）。
- `--webhook <url>` — 将新推文作为 JSON 数据发送到指定的 URL（远程主机需要使用 `https://` 协议）。
- `--jsonl` — 以 JSONL 格式输出结果（便于通过管道传输到 `tee`, `jq` 等工具）。
- `--quiet` — 禁止显示每次查询的头部信息，仅显示推文内容。
- `--limit N` — 每次查询显示的最大推文数量。
- `--sort likes|impressions|retweets|recent` — 排序方式。

按 `Ctrl+C` 停止监控操作——系统会显示监控期间的统计信息（持续时间、总查询次数、新发现的推文数量、总费用）。

**示例：**
```bash
bun run xint.ts watch "solana memecoins" --interval 5m
bun run xint.ts watch "@vitalikbuterin" --interval 1m
bun run xint.ts watch "AI agents" -i 30s --webhook https://hooks.example.com/ingest
bun run xint.ts watch "breaking news" --jsonl | tee -a feed.jsonl
```

**代理使用说明：** 当你需要持续监控某个话题时，可以使用 `watch` 命令。对于一次性检查，可以使用 `search` 命令。如果超过每日预算限制，`watch` 命令会自动停止。

### 关注者变化跟踪（Diff）
```bash
bun run xint.ts diff <@username> [options]
```

使用本地快照记录用户关注者数量的变化情况。首次运行时会创建一个基准数据；后续运行会显示自上次检查以来新增或取消关注的账户。

**选项：**
- `--following` — 显示用户关注的用户列表。
- `--history` — 查看该用户的所有保存的快照记录。
- `--json` — 以结构化 JSON 格式输出结果。
- `--pages N` — 每页显示的关注者数量（默认：5 个，每页 1000 个）。

使用此功能需要 OAuth 认证。请先运行 `auth setup` 命令进行设置。快照数据保存在 `data/snapshots/` 目录中。

**示例：**
```bash
bun run xint.ts diff @vitalikbuterin          # First run: create snapshot
bun run xint.ts diff @vitalikbuterin          # Later: show changes
bun run xint.ts diff @0xNyk --following       # Track who you follow
bun run xint.ts diff @solana --history        # View snapshot history
```

**代理使用说明：** 使用 `diff` 命令来检测目标账户的关注者变化情况。可以结合 `watch` 命令进行全面的账户监控。建议定期（例如每天）运行此命令以记录关注者变化的历史记录。

### 智能报告（Report）
```bash
bun run xint.ts report "<topic>" [options]
```

生成包含搜索结果、可选的 sentiment 分析以及通过 Grok 进行的分析结果的 Markdown 报告。

**选项：**
- `--sentiment` — 包括每条推文的 sentiment 分析结果。
- `--accounts @user1,@user2` — 包括指定用户的活动记录。
- `--model <name>` — 用于分析的 Grok 模型（默认使用 grok-3-mini）。
- `--pages N` — 每页显示的搜索结果数量（默认：2 页）。
- `--save` — 将报告保存到 `data/exports/` 目录。

**示例：**
```bash
bun run xint.ts report "AI agents"
bun run xint.ts report "solana" --sentiment --accounts @aaboronkov,@rajgokal --save
bun run xint.ts report "crypto market" --model grok-3 --sentiment --save
```

**代理使用说明：** 当用户需要关于某个话题的详细报告时，可以使用 `report` 命令。该命令会一次性执行搜索、情感分析和分析，并生成结构化的 Markdown 报告。对于快速查看结果，可以使用 `search --quick` 命令。

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

记录每次 API 调用的费用，并提供每日费用统计信息。系统会在接近预算限制时发出警告，但不会直接阻止请求。

**X API v2 的按使用量计费的费率：**
- 推文读取（搜索、收藏夹、点赞、个人资料查询）：约 0.005 美元/条。
- 完整文章搜索：约 0.01 美元/条。
- 操作（点赞、取消点赞、添加/删除收藏夹）：约 0.01 美元/次。
- 个人资料查询：约 0.005 美元/次。
- 关注者/被关注者查询：约 0.01 美元/条。
- 热门话题查询：约 0.10 美元/次。
- 使用 Grok AI 的功能（情感分析/报告）：费用由 xAI 单独收取。

默认每日预算为 1.00 美元（可通过 `costs budget set <N>` 进行调整）。

## 优化建议：
- 如果搜索结果中包含大量无关内容，可以添加 `-is:reply` 选项，并使用 `--sort likes` 参数进行筛选。
- 如果搜索结果太少，可以使用 `OR` 关键字扩大搜索范围，或移除过于具体的查询条件。
- 如果遇到与主题无关的广告内容，可以添加 `-airdrop`、`-giveaway` 或 `--whitelist` 选项来过滤结果。
- 如果只对专家的观点感兴趣，可以使用 `from:` 参数或 `--min-likes 50` 选项进行筛选。
- 如果希望获取有深度的内容，可以使用 `has:links` 参数进行搜索。

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

## 包管理 API（Package Management API）
该 API 用于管理代理程序的数据包：

| 工具 | 功能 | 所需权限 |
|------|---------|------|
| `xint_package_create` | 根据主题创建数据包 | XINT_PACKAGE_API_KEY |
| `xint_package_status` | 获取数据包的元数据和更新状态 | XINT_PACKAGE_API_KEY |
| `xint_package_query` | 查询数据包信息并返回引用来源 | XINT_PACKAGE_API_KEY |
| `xint_package_refresh` | 触发数据包的重新获取 | XINT_PACKAGE_API_KEY |
| `xint_package_search` | 在数据包目录中搜索相关内容 | XINT_PACKAGE_API_KEY |
| `xint_package_publish` | 将数据包发布到共享目录 | XINT_PACKAGE_API_KEY |

**工作流程：**
1. `xint_package_create`：根据主题创建数据包并指定数据来源。
2. `xint_package_status`：定期检查数据包的状态，直到状态变为“准备就绪”。
3. `xint_package_query`：查询数据包信息并获取引用来源。
4. `xint_package_refresh`：在数据包内容过旧时触发重新获取。
5. `xint_package_publish`：将数据包发布到共享目录。

## 代理使用技巧：
- 使用 `--quick` 参数进行初步探索（仅显示第 1 页的内容，使用 1 小时的缓存，并自动过滤无关内容）。
- 使用 `xint_search` 命令时，设置 `limit: 5` 以减少响应数据量。
- 在执行耗时较重的操作前，使用 `xint_costs` 命令检查当前预算是否充足。

### 批量操作：
- 搜索和个人资料查询应依次进行，避免同时执行（每次请求之间的间隔时间限制为 350 毫秒）。
- 使用 `xint_watch` 命令进行定期查询，避免重复搜索。
- 使用 `xint_report` 命令整合多个搜索结果，以获得更全面的信息。

### 数据上下文管理：
- `xint_search` 命令（限制为 15 条推文）：响应大小约为 3KB。
- `xint_profile` 命令（查询 20 条推文）：响应大小约为 4KB。
- `xint_article` 命令（根据文章长度不同，响应大小在 1-10KB 之间）。
- `xint_trends` 命令：响应大小约为 2KB。
- 使用 `--fields` 参数仅输出所需的信息字段。

## 错误处理机制：
| 错误代码 | 是否可重试 | 代理应采取的措施 | 示例 |
|-----------|-----------|-------------|---------|
| `RATE_LIMITED` | 可重试 | 等待 `retry_after_ms` 毫秒后重试 | X API 返回的错误代码 429 |
| `AUTH_FAILED` | 不可重试 | 停止操作并报告缺失的凭据 | 未提供 `X_BEARER_TOKEN` |
| `NOT_FOUND` | 不可重试 | 跳过该资源，尝试其他方法 | 推文已被删除 |
| `BUDGET_DENIED` | 不可重试 | 停止操作并设置预算限制 `xint costs budget set N` | 超过每日预算限制 |
| `POLICY_DENIED` | 不可重试 | 停止操作并通知用户 | 需要设置 `--policy=engagement` |
| `VALIDATION_ERROR` | 可重试 | 更正参数后重试 | 推文 ID 格式无效 |
| `TIMEOUT` | 可重试 | 等待 5 秒后重试 | 网络超时 |
| `API_ERROR` | 如果返回 5xx 状态码 | 对于 5xx 类错误，等待 30 秒后重试；对于 4xx 类错误，直接停止操作 | X API 出现故障 |

## 备用方案：
当某个工具失败时，可以尝试以下替代方案：
1. `xint_search`（X API v2，快速响应，实时处理）。
2. `xint_xsearch`（使用 xAI 的 Grok 技术进行搜索，需要 `XAI_API_KEY`）。
3. 使用之前的搜索结果（缓存时间：15 分钟）。

**文章内容获取：**
- `xint_article` 命令（通过推文 URL 获取文章内容）。
- `xint_article` 命令（直接从网页获取文章内容）。
- `xint_search` 命令（根据指定主题搜索推文）。