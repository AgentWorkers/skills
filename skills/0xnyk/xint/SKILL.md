---
name: xint
description: >
  **X Intelligence CLI** — 一个用于在终端中搜索、分析并互动X/Twitter内容的工具。适用场景包括：  
  (1) 用户执行“x research”、“search x for”、“search twitter for”等命令时；  
  (2) 当用户正在处理需要X平台最新动态作为背景信息的工作时（例如新库发布、API变更、产品发布、文化事件或行业动态）；  
  (3) 用户希望了解开发者、专家或社区对某个话题的看法；  
  (4) 用户需要实时监控（“watch”）X平台上的动态；  
  (5) 用户希望利用人工智能进行内容分析（如情感分析、趋势报告等）。  
  该工具还支持以下功能：  
  - 书签功能  
  - 点赞/关注操作（读写）  
  - 跟踪热门话题  
  - Grok AI分析  
  - 成本跟踪  
  数据输出格式支持：JSON、JSONL（可管道传输）、CSV或Markdown。  
  **注意事项：**  
  - 该工具不适用于发布推文或发送私信（DM）。  
  - 需要OAuth认证才能执行与用户信息相关的操作（如书签、点赞、关注、数据对比等）。
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

xint 是一个通用的代理研究工具，用于在 X（Twitter）上进行数据挖掘和分析。它可以将任何研究问题分解为具体的搜索任务，通过迭代优化搜索策略、跟踪相关话题、深入分析链接内容，并最终生成一份详细的报告。

## X API 详细信息（端点、操作符、响应格式）：请参阅 `references/x-api.md`。

### 安全注意事项

使用该工具需要敏感的凭据。请遵循以下指南：

#### 凭据
- **X_BEARER_TOKEN**：X API 的必备凭据，应视为机密信息，仅应在环境变量或 `.env` 文件中设置。
- **XAI_API_KEY**：可选，用于 AI 分析，同样属于机密信息。
- **X_CLIENT_ID**：可选，用于 OAuth 认证，虽然敏感度较低，但也不应公开。
- **XAI_MANAGEMENT_API_KEY**：可选，用于集合管理。

#### 文件写入
- 该工具会将数据写入 `data/` 目录（包括缓存、导出文件和 OAuth 令牌）。
- OAuth 令牌的权限设置为 `chmod 600` 以限制访问。
- 在共享数据之前，请务必审查其中包含的搜索查询内容，因为这些信息可能包含敏感信息。

#### Webhook
- `watch` 命令支持 `--webhook` 选项，可将数据发送到外部 URL。
- 仅使用受控的 Webhook（例如您自己的服务器或 Slack/Discord 服务器）。
- 不要将敏感 URL 作为 Webhook 的目标。

#### 代理执行限制
- 本文档仅记录了可使用的命令及其安全限制。
- 安装或克隆操作前需要用户的明确授权。
- 仅使用文档中规定的命令和参数。
- 在启用网络功能（如 `mcp --sse`、`watch --webhook`）前，必须获得用户的明确授权。

### 安装
- 在 Bun 环境中，建议优先使用操作系统包管理器进行安装，而非手动执行 `curl | bash` 命令。
- 在使用任何安装脚本之前，请务必验证其安全性。

### MCP 服务器（可选）
- 使用 `bun run xint.ts mcp` 可以启动一个本地 MCP 服务器，从而提供 xint 命令的访问接口。
- 默认模式下，数据通过标准输入/输出（stdio/local）传输；除非明确启用 `--sse`，否则不会启动外部 Web 服务器。
- 请遵守 `--policy read_only|engagement|moderation` 策略以及预算限制。

## 命令行工具说明
所有命令均需在项目目录下执行。

### 搜索
（命令及选项详细信息见相应的代码块）

### 分析特定用户的信息
（命令及选项详细信息见相应的代码块）

### 获取特定用户的最新推文（默认不包含回复）

### 获取由特定推文发起的完整对话链

### 获取单条推文的内容

### 获取文章的全文
（命令及选项详细信息见相应的代码块）

### 使用 xAI 的 WebSearch 工具获取文章内容
（命令及选项详细信息见相应的代码块）

### 书签功能
（命令及选项详细信息见相应的代码块）

### 点赞功能
（命令及选项详细信息见相应的代码块）

### 关注功能
（命令及选项详细信息见相应的代码块）

### 跟踪趋势
（命令及选项详细信息见相应的代码块）

### 分析数据（使用 Grok AI）
（命令及选项详细信息见相应的代码块）

### 使用 xAI 的 `x_search` 工具（无需 Cookie/GraphQL）
（命令及选项详细信息见相应的代码块）

### 管理集合
（命令及选项详细信息见相应的代码块）

### 实时监控
（命令及选项详细信息见相应的代码块）

### 监控账户的关注者变化
（命令及选项详细信息见相应的代码块）

### 生成智能报告
（命令及选项详细信息见相应的代码块）

### 成本管理
（命令及选项详细信息见相应的代码块）

### 缓存策略
（命令及选项详细信息见相应的代码块）

### 研究流程
在进行深入研究时，请遵循以下步骤：

1. **将问题分解为多个查询**：
   - 使用 X 的搜索操作符将研究问题转化为 3-5 个关键词查询。

2. **执行搜索并提取结果**：
   - 分析每个查询的结果，根据需要调整搜索策略。

3. **跟踪相关话题**：
   - 确定哪些话题值得进一步深入研究。

4. **分析链接内容**：
   - 根据分析结果，选择值得阅读的链接。

5. **综合分析结果**：
   - 按主题对分析结果进行分类。

6. **保存数据**：
   - 使用 `--save` 选项将结果保存到指定目录。

### 成本控制
所有 API 调用都会被记录在 `data/api-costs.json` 文件中。系统会在接近预算限制时发出警告，但不会阻止调用。

## 额度设置
默认每日预算为 $1.00（可通过 `costs budget set <N>` 进行调整）。

## 优化建议：
- 如发现过多无关信息，可添加 `-is:reply` 选项或使用 `--sort likes` 来过滤结果。
- 如果结果较少，可使用 `OR` 来扩展查询范围。
- 如需排除特定类型的推文，可使用相应的过滤条件。

## 文件结构
（文件结构说明见相应的代码块）