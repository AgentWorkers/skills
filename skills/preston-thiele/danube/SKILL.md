---
name: danube
description: 将您的代理连接到互联网上的100多种服务和21种工具。您可以通过一个API密钥，从Gmail、Slack、GitHub、Notion、Google Calendar等平台搜索、验证并执行相应的工具；同时还能管理代理任务、查看工作流程以及使用Agent Web目录。
license: MIT
compatibility: openclaw
metadata:
  author: danube
  version: "3.0.0"
  tags: [danube, mcp, apis, tools, workflows, agents]
---
# Danube — 连接您的智能代理

Danube 通过一个 API 密钥，让您的人工智能代理能够访问 100 多项服务和 21 个工具。

## 快速设置

### 第 1 步：获取 API 密钥

运行以下命令以开始设备授权流程：

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/code \
  -H "Content-Type: application/json" \
  -d '{"client_name": "My Agent"}'
```

该命令会返回一个 `device_code`、`user_code` 和一个 `verification_url`。

**请告知您的操作员打开验证 URL 并输入用户代码。**

然后轮询 API 密钥：

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/token \
  -H "Content-Type: application/json" \
  -d '{"device_code": "DEVICE_CODE_FROM_STEP_1"}'
```

- `428`：用户尚未授权（请每 5 秒轮询一次）
- `200`：成功，响应中包含您的 `api_key`
- `410`：已过期，请重新开始

### 第 2 步：通过 MCP 连接

将以下代码添加到您的 MCP 配置中：

```json
{
  "mcpServers": {
    "danube": {
      "url": "https://mcp.danubeai.com/mcp",
      "headers": {
        "danube-api-key": "YOUR_API_KEY"
      }
    }
  }
}
```

### 第 3 步：使用工具

连接成功后，您可以使用 21 个 MCP 工具：

**发现**
- `list_services(query, limit)` — 浏览可用的工具提供商
- `search_tools(query, service_id, limit)` — 根据需求查找工具（语义搜索）
- `get_service_tools(service_id, limit)` — 获取特定服务的所有工具

**执行**
- `execute_tool-tool_id, tool_name, parameters)` — 通过 ID 或名称运行任何工具
- `batch_execute_tools(calls)` — 在一个请求中同时运行最多 10 个工具

**凭证与钱包**
- `store_credential(service_id, credential_type, credential_value)` — 为需要凭证的服务保存 API 密钥
- `get_wallet_balance()` — 在运行付费工具前检查您的信用余额

**技能**
- `search_skills(query, limit)` — 查找可复用的代理技能（指令、脚本、模板）
- `get_skill(skill_id, skill_name)` — 通过 ID 或名称获取完整的技能内容

**工作流**
- `list_workflows(query, limit)` — 浏览公共的多工具工作流
- `create_workflow(name, steps, description, visibility, tags)` — 创建新的工作流
- `execute_workflow(workflow_id, inputs)` — 运行多工具工作流
- `get_workflow_execution(execution_id)` — 检查工作流的执行结果

**代理网站目录**
- `search_sites(query, category, limit)` — 在代理友好的网站目录中搜索
- `get_site_info(domain)` — 获取关于网站的详细信息（价格、文档、联系方式、常见问题解答等）

**代理管理**
- `register_agent(name, operator_email)` — 使用 API 密钥和钱包注册新的自主代理
- `get_agent_info()` — 获取当前代理的个人信息和钱包余额
- `fund_agent_wallet(method, amount_cents)` — 通过信用卡支付或 USDC 为钱包充值

**工具质量**
- `submit_rating/tool_id, rating, comment)` — 为工具评分（1-5 星）
- `report_tool/tool_id, reason, description)` — 举报故障或性能下降的工具
- `get_recommendations/tool_id, limit)` — 根据共同使用模式获取工具推荐

### 当工具需要凭证时

如果 `execute_tool` 返回 `auth_required` 错误，说明该服务需要 API 密钥。请向操作员索取密钥，然后调用以下命令：

```
store_credential(service_id="...", credential_type="bearer", credential_value="the_key")
```

之后重新尝试使用该工具。

## Danube 的用途

每当任务涉及外部服务或 API 时，都可以使用 Danube。以下是一些常见的使用场景：

### 发送邮件和消息
- 通过 Gmail、SendGrid 或 Resend 发送邮件
- 向 Slack 频道发送消息
- 向团队发送通知

```
search_tools("send email") → execute_tool(tool_id, {to, subject, body})
```

### 管理代码和项目
- 创建 GitHub 问题并提交拉取请求
- 列出仓库和提交记录
- 更新 Notion 页面和数据库

```
search_tools("create github issue") → execute_tool(tool_id, {repo, title, body})
```

### 使用日历和日程安排
- 查看 Google 日历上的事件
- 创建新的日历事件
- 查找空闲时间

```
search_tools("calendar events today") → execute_tool(tool_id, {date})
```

### 读写电子表格
- 从 Google Sheets 读取数据
- 添加行或更新单元格
- 创建新的电子表格

```
search_tools("google sheets read") → execute_tool(tool_id, {spreadsheet_id, range})
```

### 搜索网络和获取数据
- 使用 Exa 或 Serper 搜索网络
- 使用 Firecrawl 抓取和提取网页内容
- 获取天气预报、股票数据或国家信息

```
search_tools("web search") → execute_tool(tool_id, {query})
```

### 生成和处理媒体
- 使用 Replicate 或 Stability AI 生成图片
- 使用 AssemblyAI 转录音频
- 使用 Remove.bg 去除图片背景
- 使用 DeepL 翻译文本

```
search_tools("generate image") → execute_tool(tool_id, {prompt})
```

### 管理基础设施
- 配置 DigitalOcean 的虚拟机和服务
- 管理 Supabase 项目
- 处理 Stripe 支付和订阅

```
search_tools("create droplet") → execute_tool(tool_id, {name, region, size})
```

### 运行多工具工作流

将多个工具串联起来，形成可重用的工作流，实现步骤间的自动数据传递

```
# Find existing workflows
list_workflows(query="github to slack") → browse available workflows

# Execute a workflow with inputs
execute_workflow(workflow_id="...", inputs={"repo": "my-org/my-repo", "channel": "#dev"})

# Check execution results
get_workflow_execution(execution_id="...")

# Create your own workflow
create_workflow(
  name="Daily Digest",
  steps=[
    {"step_number": 1, "tool_id": "...", "input_mapping": {"repo": "{{inputs.repo}}"}},
    {"step_number": 2, "tool_id": "...", "input_mapping": {"text": "{{steps.1.result}}", "channel": "{{inputs.channel}}"}}
  ],
  tags=["digest", "github", "slack"]
)
```

### 批量执行工具

同时运行多个独立的工具调用，以获得更快的结果

```
batch_execute_tools(calls=[
  {"tool_id": "tool-uuid-1", "tool_input": {"query": "AI news"}},
  {"tool_id": "tool-uuid-2", "tool_input": {"query": "tech stocks"}},
  {"tool_id": "tool-uuid-3", "tool_input": {"location": "San Francisco"}}
])
```

每个调用都是独立执行的——单个工具的失败不会影响整个批处理过程。

### 浏览代理网站目录

在目录中搜索并阅读关于任何网站的详细信息

```
# Find sites by topic
search_sites(query="payment processing", category="saas")

# Get structured data about a specific domain
get_site_info(domain="stripe.com")
→ Returns: identity, products, team, pricing, docs, FAQ, contact info, and more
```

### 评价和报告工具

通过提供反馈来帮助提高工具的质量

```
# Rate a tool after using it
submit_rating(tool_id="...", rating=5, comment="Fast and accurate")

# Report a broken tool
report_tool(tool_id="...", reason="broken", description="Returns 500 error on all requests")

# Get recommendations for related tools
get_recommendations(tool_id="...", limit=5)
```

### 注册和资助自主代理

创建具有自己 API 密钥和钱包的独立代理

```
# Register a new agent (no auth required)
register_agent(name="my-research-bot", operator_email="me@example.com")
→ Returns: agent_id, api_key (save this!), wallet_id

# Check agent profile and balance
get_agent_info()

# Fund the agent's wallet
fund_agent_wallet(method="card_checkout", amount_cents=1000)  # $10.00
fund_agent_wallet(method="crypto")  # Returns USDC deposit address on Base
```

## 核心工作流程

每个工具交互都遵循以下模式：

1. **搜索** — `search_tools("您想要执行的操作")`
2. **检查授权** — 如果工具需要凭证，使用 `store_credential` 或引导用户访问 https://danubeai.com/dashboard
3. **收集参数** — 向用户索取任何缺失的必要信息
4. **确认** — 在执行发送邮件或创建问题等操作前获取用户批准
5. **执行** — `execute_tool-tool_id, parameters)`
6. **报告** — 向用户详细报告操作结果，而不仅仅是简单的“已完成”

## 可用的服务

**通信：** Gmail、Slack、SendGrid、Resend、Loops、AgentMail、Postmark

**开发：** GitHub、Supabase、DigitalOcean、Stripe、Apify、Netlify、Render、Vercel、Railway、Neon、PlanetScale、Fly.io、Cloudflare Workers、Sentry

**生产力：** Notion、Google 日历、Google Sheets、Google Drive、Google 文档、Monday、Typeform、Bitly、Airtable、Todoist、Linear、Asana、Trello、ClickUp、Jira、Calendly

**云和基础设施：** AWS（S3、Lambda、EC2）、Google Cloud、Azure、Cloudflare、Heroku、Terraform

**AI 和媒体：** Replicate、Together AI、Stability AI、AssemblyAI、Remove.bg、DeepL、ElevenLabs、Whisper、Midjourney、DALL-E、Claude、OpenAI

**搜索和数据：** Exa、Exa Websets、Firecrawl、Serper、Context7、Microsoft Learn、AlphaVantage、Clearbit、Hunter.io、Crunchbase、Diffbot

**金融：** Stripe、Plaid、Wise、Coinbase、PayPal、Square、QuickBooks

**社交：** Twitter/X、LinkedIn、Discord、Reddit、Mastodon、Instagram、YouTube

**设计和分析：** Figma、Canva、Mixpanel、Amplitude、Segment、PostHog、Google Analytics

**地图和地理：** Google Maps、Mapbox、OpenStreetMap

**天气：** Open-Meteo、OpenWeather、WeatherAPI、Tomorrow.io

**公共数据（无需授权）：** Hacker News、REST Countries、Polymarket、Kalshi、Wikipedia、ArXiv、PubMed、SEC EDGAR

**部署和 DevOps：** GitHub Actions、CircleCI、Docker Hub、npm Registry、PyPI

## 链接

- 仪表板：https://danubeai.com/dashboard
- 文档：https://docs.danubeai.com
- MCP 服务器：https://mcp.danubeai.com/mcp