---
name: agentapi
description: 浏览并搜索 AgentAPI 目录——这是一个专为 AI 代理设计的 API 集成库。在这里可以找到与 MCP 兼容的 API，涵盖搜索、人工智能、通信、数据库、支付等功能。在构建需要外部 API 集成的代理工作流程时，可充分利用这些 API。
author: shipitlucas
version: 1.0.0
tags: [api, mcp, agents, directory, search, integrations]
---
# AgentAPI

这是一个专为AI代理设计的API目录，支持机器读取，并兼容MCP标准。所有API均可被AI代理访问。

**官方网站：** https://agentapihub.com

## 快速搜索

### 按类别分类

| 类别 | API | 示例 |
|----------|------|---------|
| 搜索 | Brave, Serper, Exa, Tavily, Perplexity | 支持AI摘要的网页搜索功能 |
| AI与机器学习 | OpenAI, Claude, Gemini, Groq, Replicate | 用于大语言模型推理和图像生成 |
| 通信 | Resend, Twilio, Slack, Discord, Telegram | 提供电子邮件、短信和消息传递服务 |
| 数据库 | Supabase, Pinecone, Qdrant, Neon, Upstash | 支持SQL操作、向量存储和键值存储 |
| 支付 | Stripe, Lemon Squeezy, PayPal | 提供支付处理服务 |
| 网页抓取 | Firecrawl, Browserbase, Apify | 用于网页抓取和自动化操作 |
| 开发者工具 | GitHub, Vercel, Linear, Sentry | 提供代码托管、部署和问题跟踪功能 |
| 生产力工具 | Notion, Google Calendar, Todoist | 用于任务管理和日程安排 |

### 兼容MCP标准的API

目录中的50多个API均兼容MCP标准。可通过`?mcp=true`进行筛选。

## API访问

### JSON接口

```bash
# Fetch all APIs
curl https://agentapihub.com/api/v1/apis

# Search by capability
curl "https://agentapihub.com/api/v1/apis?q=send+email&mcp=true"

# Filter by category
curl "https://agentapihub.com/api/v1/apis?category=ai"
```

### 响应格式

```json
{
  "id": "resend",
  "name": "Resend",
  "description": "Modern email API for developers",
  "category": "communication",
  "provider": "Resend",
  "docs": "https://resend.com/docs",
  "auth": "api_key",
  "pricing": "freemium",
  "pricingDetails": "3,000 free/mo, then $20/mo",
  "rateLimit": "10 req/sec",
  "mcpCompatible": true,
  "examplePrompt": "Send an email notification using Resend",
  "latency": "fast",
  "reliability": 99.9,
  "tags": ["email", "transactional", "notifications"]
}
```

## 各类别的热门API

### 搜索
- **Brave Search**：注重隐私保护，每月免费使用2000次搜索请求 |
- **Exa**：专为AI代理设计的神经/语义搜索引擎 |
- **Tavily**：专为AI代理量身定制的搜索工具

### AI与机器学习
- **OpenAI**：提供GPT-4、DALL-E、Whisper等模型 |
- **Anthropic Claude**：非常适合用于推理和编码任务 |
- **Groq**：具有最快的推理速度（每秒超过500次请求）

### 通信
- **Resend**：简单的电子邮件发送API，每月免费使用3000次 |
- **Twilio**：提供短信和语音通信服务，属于行业标准 |
- **Slack/Discord/Telegram**：支持团队间的实时消息传递

### 数据库
- **Supabase**：基于Postgres的数据库，支持身份验证和数据存储 |
- **Pinecone/Qdrant**：用于快速检索（RAG）的向量数据库 |
- **Upstash**：基于Redis的无服务器数据库解决方案

## 使用示例

```markdown
# Find an API for sending emails
Search AgentAPI for "email" → Returns Resend, SendGrid, Twilio

# Find vector databases for RAG
Search AgentAPI for "vector embeddings" → Returns Pinecone, Qdrant, Weaviate

# Find fast LLM inference
Search AgentAPI for category "ai" + filter by latency → Returns Groq, Gemini Flash
```

## 贡献方式

如需提交新的API，请访问：https://agentapihub.com （在页面底部找到“提交API”的链接）。

## 开发者信息

由Lucas（[@shipitlucas](https://twitter.com/shipitlucas)）开发。