---
name: xint-rs
description: >
  Fast X Intelligence CLI（Rust）——通过终端执行在X/Twitter上的搜索、分析和操作。适用场景包括：  
  (1) 用户请求“查询x相关信息”、“在Twitter上搜索x”、“了解人们对x的看法”等；  
  (2) 用户需要实时监控（使用“watch”功能）；  
  (3) 用户需要基于Grok技术的智能分析（如情感分析、内容分类）；  
  (4) 用户需要生成智能报告；  
  (5) 用户希望追踪关注者或关注对象的变化；  
  (6) 用户需要获取热门话题信息。  
  该工具还支持以下功能：  
  - 书签功能；  
  - 点赞/关注操作（通过OAuth认证）；  
  - 数据导出（格式支持CSV、JSON、JSONL）。  
  **注意事项：**  
  - 该工具不支持发布推文或发送私信（DM），也不提供企业级功能。
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
# xint — X Intelligence CLI（Rust）

这是一个快速、无依赖的命令行工具，用于在终端中执行与X/Twitter相关的搜索、分析和互动操作。所有输出都会直接输出到标准输出（stdout），便于通过管道传输。

## 安全注意事项

使用此工具需要处理敏感的凭证信息，请遵循以下指南：

### 凭证信息
- **X_BEARER_TOKEN**：X API所需的凭证。请将其视为机密信息，仅通过环境变量或`.env`文件设置。
- **XAI_API_KEY**：可选，用于AI分析。同样属于机密信息。
- **X_CLIENT_ID**：可选，用于OAuth认证。虽然敏感度较低，但请不要公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于集合管理。

### 文件写入
- 该工具会将数据写入`data/`目录：包括缓存文件、导出文件、快照以及OAuth令牌。
- OAuth令牌会以严格的权限（`chmod 600`）进行存储。
- 在共享数据之前，请仔细检查导出的内容，因为其中可能包含敏感的搜索查询。

### Webhook
- `watch`命令支持`--webhook`选项，可将数据发送到外部URL。
- 仅使用您自己控制的Webhook服务（例如自己的服务器或Slack/Discord账户）。
- 请勿将敏感的URL作为Webhook的目标。

### 代理执行限制
- 本文档仅描述了可执行的命令及相关的安全限制。
- 安装或克隆操作前需要用户的明确授权。
- 请仅使用文档中规定的命令和参数。
- 在启用网络功能（如`mcp --sse`、`watch --webhook`）之前，必须获得用户的明确授权。

### 安装
- 对于所需的工具，尽可能使用操作系统的包管理器进行安装，而非手动执行`curl | bash`命令。
- 在运行任何安装脚本之前，请务必对其进行验证。

### MCP服务器（可选）
- 使用`xint mcp`可以启动一个本地MCP服务器，将xint命令作为工具提供。
- 默认模式下，数据仅通过标准输入/输出（stdio）进行传输；除非明确启用`--sse`选项，否则不会启动外部Web服务器。
- 请遵守`--policy read_only|engagement|moderation`配置选项以及预算限制。

## 设置
需要设置环境变量（位于`.env`文件中或通过其他方式导出）：
- `X_BEARER_TOKEN`：用于搜索、查看用户资料、推文、话题、趋势、关注和生成报告等操作。
- `X_CLIENT_ID`：用于OAuth相关操作（如书签、点赞、关注、比较等）。
- `XAI_API_KEY`：用于AI分析（如分析数据、生成报告、执行搜索等）。
- `XAI_MANAGEMENT_API_KEY`：用于集合管理（如列出集合、创建集合、验证集合内容、添加文档等）。

### OAuth设置（一次性操作）
执行`xint auth setup`命令以完成OAuth配置。

## 命令列表

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
xint watch "bitcoin" --webhook https://example.com/webhook  # POST new tweets to webhook
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
使用xAI的`web_search`工具从任意URL获取并提取文章内容。同时支持从X推文中提取链接的文章。
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
xint analyze "question"                              # Free-form analysis request
```

### 智能报告
```bash
xint report "AI agents"                       # Full report with AI summary
xint report "AI agents" -a @user1,@user2      # Track specific accounts
xint report "AI agents" -s                    # Include sentiment analysis
xint report "AI agents" --save                # Save to data/exports/
```

### 关注者追踪（需要OAuth）
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

### xAI X搜索（无需cookie/GraphQL）
通过xAI提供的`x_search`工具执行搜索。无需使用bearer token或cookie，仅需`XAI_API_KEY`。
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
通过xAI的文件和集合API上传文档、管理集合以及进行语义搜索。
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
大多数命令支持`--json`格式以输出原始JSON数据。搜索命令还支持以下格式：
- `--jsonl`：每行输出一个JSON对象（适合通过管道传输）。
- `--csv`：适合电子表格格式。
- `--markdown`：格式化后的输出，适用于生成报告。

## 数据传输（通过管道）
```bash
xint search "topic" --jsonl | jq '.username'
xint search "topic" --json | xint analyze --pipe "summarize these"
xint search "topic" --csv > export.csv
```

## 成本控制
X API的搜索费用约为每条推文0.005美元。系统设有预算限制，防止费用过高：
- 默认每日预算限制为1.00美元。
- 可通过`xint costs budget <amount>`自定义预算。
- `watch`命令会在达到预算限制时自动停止执行。