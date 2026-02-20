---
name: xint
description: >
  **X Intelligence CLI** — 一个用于在终端中搜索、分析并处理 X/Twitter 内容的工具。适用场景包括：  
  1. 当用户执行以下命令时：`x research`、`search x for`、`search twitter for`、`what are people saying about`、`what’s twitter saying`、`check x for`、`x search`、`find tweets about`、`monitor x for`、`track followers`；  
  2. 当用户正在处理需要了解最新 X 社区动态的项目时（例如新库发布、API 变更、产品发布、文化事件或行业动态）；  
  3. 当用户希望了解开发者、专家或社区对某个主题的看法时；  
  4. 当用户需要实时监控（如“watch”功能）或高级分析（如“analyze”、“sentiment”、“report”）时。  
  该工具还支持以下功能：  
  - 书签（bookmarking）、点赞（liking）、关注（following，支持读写操作）；  
  - 热门话题（trending topics）；  
  - Grok AI 分析；  
  - 成本跟踪（cost tracking）。  
  数据输出格式支持：JSON、JSONL（可管道传输）、CSV 或 Markdown。  
  **注意事项：**  
  - 该工具不支持发布推文（posting tweets）或发送私信（DMs），也不提供企业级功能（enterprise features）。  
  - 使用书签、点赞、关注等操作需要通过 OAuth 进行身份验证。
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
# xint — X 智能命令行工具（X Intelligence CLI）

这是一个通用型代理研究工具，用于在 X/Twitter 上进行数据挖掘和分析。它可以将任何研究问题分解为多个针对性的搜索请求，通过迭代优化搜索策略、跟踪相关话题、深入分析链接内容，并最终生成一份详细的报告。

## X API 详情（端点、操作符、响应格式）：请参阅 `references/x-api.md`。

### 安全注意事项

使用本工具需要敏感的认证凭据。请遵循以下指南：

#### 凭据
- **X_BEARER_TOKEN**：X API 的必备凭据，应视为机密信息（建议将其设置为环境变量 `env` 中的本地变量）。
- **XAI_API_KEY**：可选，用于 AI 分析，同样属于机密信息。
- **X_CLIENT_ID**：可选，用于 OAuth 认证，虽然敏感度较低，但也不应公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于集合管理。

#### 文件写入
- 该工具会将数据写入 `data/` 目录（包括缓存文件、导出结果、快照以及 OAuth 令牌）。
- OAuth 令牌的权限设置为 `chmod 600` 以限制访问。
- 在共享数据之前，请仔细检查其中是否包含敏感的搜索查询内容。

#### Webhook
- `watch` 和 `stream` 命令可以将数据发送到指定的 Webhook 端点。
- 远程 Webhook 必须使用 `https://` 协议（`http://` 仅适用于本地或循环测试环境）。
- 可以通过 `XINT_WEBHOOK_ALLOWED_HOSTS=hooks.example.com,*.internal.example` 配置允许访问的域名列表。
- 避免将敏感的搜索查询或包含令牌的 URL 发送到第三方服务器。

#### 运行时注意事项
- 本文档仅描述了该命令行工具的使用方法和安全控制措施。
- 网络监听功能（`mcp --sse`）是可选的，默认处于关闭状态。
- Webhook 功能（`--webhook`）也是可选的，默认处于关闭状态。

### 安装
- 在使用 Bun 时，建议优先通过操作系统包管理器进行安装，而非手动执行 `curl | bash` 命令。
- 在运行任何安装脚本之前，请务必先验证其安全性。

### MCP 服务器（可选）
- 使用 `bun run xint.ts mcp` 命令可以启动一个本地 MCP 服务器，从而提供 xint 命令的访问接口。
- 默认模式下，数据仅通过标准输入/输出（stdio）传输；除非明确启用 `--sse` 选项，否则不会启动外部 Web 服务器。
- 请遵守 `--policy read_only|engagement|moderation` 等配置选项以控制数据访问权限。

### 命令行工具说明
所有命令都在项目目录下执行。

### 搜索功能
（命令及选项详细信息见相应的代码块）

### 个人资料（Profile）
（命令及选项详细信息见相应的代码块）

### 主题讨论（Thread）
（命令及选项详细信息见相应的代码块）

### 单条推文（Single Tweet）
（命令及选项详细信息见相应的代码块）

### 文章内容获取（Article）
（命令及选项详细信息见相应的代码块）

### 书签功能（Bookmark）
（命令及选项详细信息见相应的代码块）

### 点赞功能（Likes）
（命令及选项详细信息见相应的代码块）

### 关注功能（Following）
（命令及选项详细信息见相应的代码块）

### 热门趋势（Trends）
（命令及选项详细信息见相应的代码块）

### 分析功能（Analyze）
（命令及选项详细信息见相应的代码块）

### xAI 搜索（xAI Search）
（命令及选项详细信息见相应的代码块）

### xAI 集合管理（xAI Collections）
（命令及选项详细信息见相应的代码块）

### 监控功能（Watch/Stream）
（命令及选项详细信息见相应的代码块）

### 成本管理（Cost Management）
（命令及选项详细信息见相应的代码块）

### 研究流程（Research Loop）
（命令及选项详细信息见相应的代码块）

### 预算管理（Budget Management）
（命令及选项详细信息见相应的代码块）

### 其他注意事项
- 请确保已正确配置 OAuth 认证。
- 部分功能可能需要额外的权限（如 `like.read`、`follows.read` 等）。

请注意：上述文档为技术性说明，具体使用方法可能因环境或版本的不同而有所调整。如有需要，请参考官方文档或联系技术支持团队。