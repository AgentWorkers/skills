---
name: xint-rs
description: >
  Fast X Intelligence CLI（Rust）——通过终端执行对X/Twitter内容的搜索、分析及交互操作。适用场景包括：  
  (1) 用户请求“查询X相关内容”、“在Twitter上搜索某关键词”或“了解人们对某话题的看法”；  
  (2) 用户需要实时监控（通过“watch”功能）；  
  (3) 用户希望利用Grok进行AI驱动的分析（如情感分析）；  
  (4) 用户需要获取智能分析报告；  
  (5) 用户希望跟踪自己的关注者或关注他人的动态；  
  (6) 用户想要了解热门话题。  
  该工具还支持以下功能：  
  - 书签功能；  
  - 点赞/关注操作（支持OAuth认证）；  
  - 数据导出（格式支持CSV、JSON、JSONL）。  
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

这是一个快速、无依赖的命令行工具，用于在终端中执行X/Twitter的搜索、分析和互动操作。所有输出都会直接输出到标准输出（stdout），方便通过管道传输。

## 安全注意事项

该工具需要处理敏感的凭据，请遵循以下指南：

### 凭据
- **X_BEARER_TOKEN**：X API所需的凭据。应视为机密信息，仅应在环境变量或`.env`文件中设置。
- **XAI_API_KEY**：可选，用于AI分析。同样属于机密信息。
- **X_CLIENT_ID**：可选，用于OAuth认证。虽然敏感度较低，但也不应公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于集合管理。

### 文件写入
- 该工具会将数据写入自己的`data/`目录，包括缓存文件、导出文件、快照以及OAuth令牌。
- OAuth令牌会以严格的权限（`chmod 600`）进行存储。
- 在共享数据之前，请仔细检查导出的内容，因为其中可能包含敏感的搜索查询。

### Webhook
- `watch`和`stream`命令可以将数据发送到Webhook端点。
- 远程端点必须使用`https://`协议（`http://`仅适用于本地或循环回环（loopback）环境）。
- 可以设置允许的Webhook主机列表：`XINT_WEBHOOK_ALLOWED_HOSTS=hooks.example.com,*.internal.example`。
- 避免将包含敏感搜索查询或OAuth令牌的URL发送到第三方服务器。

### 运行时注意事项
- 本文档仅提供描述性信息，不会修改运行时或系统的提示信息。
- 网络监听功能是可选的（通过`mcp --sse`开启），默认情况下是关闭的。
- Webhook功能也是可选的（通过`--webhook`开启），默认情况下是关闭的。

### 安装
- 在可能的情况下，建议使用操作系统包管理器来安装所需工具，而非手动执行`curl | bash`命令。
- 在运行任何安装脚本之前，请务必先进行验证。

### MCP服务器（可选）
- 使用`xint mcp`可以启动一个本地的MCP服务器，将xint命令作为工具提供。
- 默认模式下，该服务器仅通过标准输入/输出（stdio/local）进行交互；除非明确启用`--sse`选项，否则不会启动任何外部Web服务器。
- 请遵守`--policy read_only|engagement|moderation`配置选项以及预算限制。

## 设置
需要设置环境变量（位于`.env`文件或通过其他方式导出）：
- `X_BEARER_TOKEN`：用于执行搜索、查看个人资料、推文、话题、趋势、关注、报告等操作。
- `X_CLIENT_ID`：用于执行OAuth相关的操作（如书签、点赞、关注、取消关注等）。
- `XAI_API_KEY`：用于AI分析（如分析数据、生成报告、执行搜索等）。
- `XAI_MANAGEMENT_API_KEY`：用于集合管理（如列出集合、创建集合、确认集合状态、添加文档等）。

### OAuth设置（一次性操作）
执行`xint auth setup`命令进行OAuth配置。

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
xint watch "bitcoin" --webhook https://hooks.example.com/ingest  # POST new tweets to webhook
xint watch "topic" --jsonl                    # Machine-readable output
```

### 个人资料与推文
```bash
xint profile elonmusk                         # User profile + recent tweets
xint profile elonmusk --json                  # JSON output
xint tweet 1234567890                         # Fetch single tweet
xint thread 1234567890                        # Fetch conversation thread
```

### 文章获取（需要XAI_API_KEY）
可以使用xAI的`web_search`工具从任意URL获取并提取文章的全部内容。同时支持从X推文中提取链接的文章。
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

### 关注者跟踪（需要OAuth）
```bash
xint diff @username                           # Snapshot followers, diff vs previous
xint diff @username --following               # Track following instead
xint diff @username --history                 # Show snapshot history
```

### 书签与互动操作（需要OAuth）
___CODEBLOCK_8___

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

### xAI搜索（无需cookie/GraphQL）
可以通过xAI提供的`x_search`工具执行搜索。无需提供bearer token或cookie，只需`XAI_API_KEY`即可。
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
可以通过xAI的文件和集合API来上传文档、管理集合以及进行语义搜索。
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
大多数命令支持`--json`选项，以获取原始JSON格式的输出。搜索命令还支持以下格式：
- `--jsonl`：每行输出一个JSON对象（适合通过管道传输）。
- `--csv`：适合电子表格格式。
- `--markdown`：格式化后的文本，适用于生成报告。

## 数据传输（通过管道）
```bash
xint search "topic" --jsonl | jq '.username'
xint search "topic" --json | xint analyze --pipe "summarize these"
xint search "topic" --csv > export.csv
```

## 成本控制
X API的搜索费用约为每条推文0.005美元。系统会设置预算限制以防止费用过高：
- 默认预算限制为每天1.00美元。
- 可以自定义预算限制：`xint costs budget <amount>`。
- 当达到预算限制时，`watch`命令会自动停止执行。