---
name: xint-rs
description: >
  Fast X Intelligence CLI（Rust）——一个用于在终端中搜索、分析并处理X/Twitter数据的工具。适用场景包括：  
  (1) 用户请求“查询X相关信息”、“在Twitter上搜索某内容”或“了解人们对某事的看法”；  
  (2) 用户需要实时监控（通过“watch”命令）；  
  (3) 用户希望利用Grok进行AI驱动的分析（如情感分析）；  
  (4) 用户需要获取智能分析报告；  
  (5) 用户希望追踪自己的关注者或关注他人的情况；  
  (6) 用户想要了解热门话题。  
  该工具还支持以下功能：  
  - 书签功能；  
  - 点赞/关注操作（通过OAuth认证）；  
  - 数据导出（支持CSV、JSON、JSONL格式）。  
  **注意事项：**  
  - 该工具不支持发布推文或发送私信，也不提供企业级功能。
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
# xint — X Intelligence CLI（Rust）

这是一个快速、无依赖的命令行工具，用于在终端中执行与X/Twitter相关的搜索、分析和互动操作。所有输出都会直接写入标准输出（stdout），便于通过管道传输。

## 安全注意事项

该工具需要处理敏感的凭据，请遵循以下指南：

### 凭据
- **X_BEARER_TOKEN**：用于访问X API，属于机密信息，仅应在环境变量或`.env`文件中设置。
- **XAI_API_KEY**：可选，用于AI分析，同样属于机密信息。
- **X_CLIENT_ID**：可选，用于OAuth认证，虽然敏感度较低，但也不应公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于集合管理。

### 文件写入
- 该工具会将数据写入`data/`目录，包括缓存文件、导出的数据、快照以及OAuth令牌。
- OAuth令牌会以严格的权限（`chmod 600`）进行存储。
- 在共享数据之前，请务必审查其中的内容，因为这些数据可能包含敏感的搜索查询。

### Webhook
- `watch`命令支持`--webhook`选项，可将数据发送到外部URL。
- 仅使用您自己控制的Webhook服务（例如自己的服务器或Slack/Discord账户）。
- 切勿将敏感的URL作为Webhook的目标。

### 代理程序的自主性
- 该工具设计为可被添加到代理程序的技能目录中。
- 提供了“克隆到技能目录”的说明，这是为了确保技能的正常运行。
- 如果没有明确要求，代理程序在安装新技能之前应先询问用户。

### 安装
- 对于Bun环境，建议优先使用操作系统提供的包管理器进行安装，而非手动执行`curl | bash`命令。
- 在运行任何安装脚本之前，请务必检查其安全性。

## 设置

需要设置环境变量（位于`.env`文件中）：
- `X_BEARER_TOKEN`：用于搜索、查看用户资料、推文、话题、趋势、关注列表和生成报告等操作。
- `X_CLIENT_ID`：用于OAuth相关操作（如书签、点赞、关注、差异分析等）。
- `XAI_API_KEY`：用于AI分析功能（如分析数据、生成报告、执行搜索等）。
- `XAI_MANAGEMENT_API_KEY`：用于集合管理（如列出集合、创建集合、验证集合状态、添加文档等）。

### OAuth设置（一次性操作）：`xint auth setup`

## 命令说明

### 搜索与发现
```bash
xint search "AI agents" --limit 10            # Search recent tweets
xint search "AI agents" --quick               # Fast mode (1 page, 10 max, 1hr cache)
xint search "AI agents" --quality             # Min 10 likes filter
xint search "AI agents" --since 1d --sort likes
xint search "from:elonmusk" --limit 5
xint search "AI agents" --json                # JSON output
xint search "AI agents" --jsonl               # One JSON per line
xint search "AI agents" --csv                 # CSV output
xint search "AI agents" --sentiment           # AI sentiment analysis (needs XAI_API_KEY)
xint search "AI agents" --save                # Save to data/exports/
```

### 监控
```bash
xint watch "AI agents" -i 5m                  # Poll every 5 minutes
xint watch "@elonmusk" -i 30s                 # Watch user (auto-expands to from:)
xint watch "bitcoin" --webhook https://...    # POST new tweets to webhook
xint watch "topic" --jsonl                    # Machine-readable output
```

### 用户资料与推文
```bash
xint profile elonmusk                         # User profile + recent tweets
xint profile elonmusk --json                  # JSON output
xint tweet 1234567890                         # Fetch single tweet
xint thread 1234567890                        # Fetch conversation thread
```

### 文章获取（需要XAI_API_KEY）
- 可使用xAI的web_search工具从任意URL获取并提取文章的全部内容；同时支持从X推文中提取链接的文章。
```bash
# Fetch article content
xint article "https://example.com"

# Fetch + analyze with AI
xint article "https://example.com" --ai "Summarize key takeaways"

# Auto-extract article from X tweet URL and analyze
xint article "https://x.com/user/status/123456789" --ai "What are the main points?"

# Full content without truncation
xint article "https://example.com" --full

# JSON output
xint article "https://example.com" --json
```

### 趋势分析
```bash
xint trends                                   # Worldwide trending
xint trends us                              # US trends
xint trends --json                          # JSON output
xint trends --locations                     # List supported locations
```

### AI分析（需要XAI_API_KEY）
```bash
xint analyze "What's the sentiment around AI?"
xint analyze --tweets saved.json              # Analyze tweets from file
cat tweets.json | xint analyze --pipe         # Analyze from stdin
xint analyze "question" --system "You are..."  # Custom system prompt
```

### 智能报告
```bash
xint report "AI agents"                       # Full report with AI summary
xint report "AI agents" -a @user1,@user2      # Track specific accounts
xint report "AI agents" -s                    # Include sentiment analysis
xint report "AI agents" --save                # Save to data/exports/
```

### 关注者跟踪（需要OAuth）
```bash
xint diff @username                           # Snapshot followers, diff vs previous
xint diff @username --following               # Track following instead
xint diff @username --history                 # Show snapshot history
```

### 书签与互动操作（需要OAuth）
```bash
xint bookmarks                                # List bookmarks
xint bookmarks --since 1d                     # Recent bookmarks
xint bookmark 1234567890                      # Save tweet
xint unbookmark 1234567890                    # Remove bookmark
xint likes                                    # List liked tweets
xint like 1234567890                          # Like a tweet
xint unlike 1234567890                        # Unlike a tweet
xint following                                # List accounts you follow
```

### 成本监控
```bash
xint costs                                    # Today's API costs
xint costs week                               # Last 7 days
xint costs month                              # Last 30 days
xint costs budget 2.00                        # Set $2/day budget
```

### 关注列表
```bash
xint watchlist                                # List watched accounts
xint watchlist add @username "competitor"     # Add with note
xint watchlist remove @username               # Remove
xint watchlist check @username                # Check if watched
```

### xAI X Search（无需cookies/GraphQL）
- 可通过xAI提供的x_search工具直接搜索X平台的内容，无需使用bearer token或cookies，只需提供`XAI_API_KEY`即可。
```bash
# Create a queries file
echo '["AI agents", "solana"]' > queries.json

# Run search scan → markdown report + JSON payload
xint x-search --queries-file queries.json --out-md report.md --out-json raw.json

# Date range filter
xint x-search --queries-file queries.json --from-date 2026-02-01 --to-date 2026-02-15

# Emit memory candidates (deduped against existing workspace sources)
xint x-search --queries-file queries.json --workspace /path/to/workspace --emit-candidates

# Custom model
xint x-search --queries-file queries.json --model grok-3
```

### xAI集合管理
- 可通过xAI的Files + Collections API上传文档、管理集合，并进行语义搜索。
```bash
# List existing collections
xint collections list

# Create or find a collection
xint collections ensure --name "research-kb"

# Upload a file to xAI
xint collections upload --path ./report.md

# Semantic search across documents
xint collections search --query "AI agent frameworks"

# Sync a directory to a collection (upload + attach)
xint collections sync-dir --collection-name "kb" --dir ./docs --glob "*.md" --limit 50
```

### 实用工具
```bash
xint auth setup                               # OAuth setup (interactive)
xint auth setup --manual                      # Manual paste mode
xint auth status                              # Show auth info
xint auth refresh                             # Force token refresh
xint cache clear                              # Clear cached data
```

## 输出格式
大多数命令支持`--json`选项以输出原始JSON格式；搜索命令还支持以下格式：
- `--jsonl`：每行输出一个JSON对象（适合通过管道传输）。
- `--csv`：输出适合电子表格的CSV格式。
- `--markdown`：输出格式化的文本（适用于生成报告）。

## 数据传输（通过管道）
```bash
xint search "topic" --jsonl | jq '.username'
xint search "topic" --json | xint analyze --pipe "summarize these"
xint search "topic" --csv > export.csv
```

## 成本控制
- 使用X API的搜索功能每次请求的费用约为0.005美元。系统设有预算限制，防止费用过高：
  - 默认每日预算为1.00美元。
  - 可通过`xint costs budget <amount>`自定义预算。
  - `watch`命令会在达到预算限制时自动停止执行。