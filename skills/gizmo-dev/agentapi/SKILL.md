---
name: agentapi
description: 浏览并搜索 AgentAPI 目录——这是一个专为 AI 代理设计的 API 数据库。您可以在这里找到与 MCP 兼容的 API，涵盖搜索、AI、通信、数据库、支付等功能。该目录提供免费访问服务，同时也提供按使用量计费的 x402 API 选项。
author: gizmolab
version: 1.0.7
tags: [api, mcp, agents, directory, search, integrations, x402]
homepage: https://agentapihub.com
source: https://github.com/gizmolab/agentapi
---
# AgentAPI

这是一个专为AI代理设计的API目录，支持机器读取，兼容MCP协议，并可供代理直接访问。

**官方网站：** https://agentapihub.com  
**文档：** https://api.agentapihub.com/api/docs

## 免费功能

该目录及搜索功能完全免费：

```bash
# Browse all APIs (FREE)
curl https://agentapihub.com/api/v1/apis

# Search by capability (FREE)
curl "https://agentapihub.com/api/v1/apis?q=send+email&mcp=true"

# Filter by category (FREE)
curl "https://agentapihub.com/api/v1/apis?category=ai"
```

## x402按使用量付费的API

部分API采用**x402**协议提供按使用量付费的服务，支持使用Base链上的USDC进行支付。

### 可用的x402 API

| API | 端点 | 大约价格 |
|-----|----------|---------------|
| Gemini Chat | `/api/gemini/chat/completions` | 约0.001美元/请求 |
| Gemini Embeddings | `/api/gemini/embeddings` | 约0.0005美元/请求 |

### x402的使用方式

1. 调用相应的API端点。
2. 收到“需要支付402费用”的提示，其中包含费用详情。
3. 在Base链上发送USDC支付。
4. 提交包含支付证明的请求并重试。
5. 接收API响应。

### ⚠️ 重要安全提示

- **x402支付需要明确设置，并且不应在没有安全措施的情况下自动执行**：
  - **必须配置一个包含USDC的钱包**。
  - **建议获得用户授权**：在支付前实施确认流程。
  - **验证收款人**：收款人为`0xcCb92A101347406ed140b18C4Ed27276844CD9D7`（gizmolab.eth）。
  - **设置消费限制**：配置每次请求和每日的最大支付限额。
  - **此功能不会自动执行支付**——仅提供相关文档。

有关实现细节，请参阅：https://api.agentapihub.com/api/docs

## 目录分类

| 分类 | API | 示例 |
|----------|------|---------|
| 搜索 | Brave, Serper, Exa, Tavily, Perplexity | 支持AI摘要的网页搜索 |
| AI与机器学习 | OpenAI, Claude, Gemini, Groq, Replicate | 大语言模型推理、图像生成 |
| 通信 | Resend, Twilio, Slack, Discord, Telegram | 电子邮件、短信、消息传递 |
| 数据库 | Supabase, Pinecone, Qdrant, Neon, Upstash | SQL数据库、向量存储、键值存储 |
| 支付 | Stripe, Lemon Squeezy, PayPal | 支付处理 |
| 数据抓取 | Firecrawl, Browserbase, Apify | 网页抓取、自动化 |
| 开发者工具 | GitHub, Vercel, Linear, Sentry | 代码管理、部署、问题跟踪 |
| 生产力工具 | Notion, Google Calendar, Todoist | 任务管理、日程安排 |

## 兼容MCP协议的API

目录中的50多个API均兼容MCP协议。可通过`?mcp=true`进行筛选。

## API响应格式

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
  "x402Enabled": false,
  "tags": ["email", "transactional", "notifications"]
}
```

## 按分类划分的热门API

### 搜索
- **Brave Search**：注重隐私保护，每月2000次免费使用。
- **Exa**：专为AI设计的神经/语义搜索工具。
- **Tavily**：专为AI代理设计的搜索服务。

### AI与机器学习
- **OpenAI**：GPT-4、DALL-E、Whisper
- **Anthropic Claude**：最适合推理和编程任务的AI模型。
- **Groq**：最快的推理引擎（每秒处理500多个请求）。

### 通信
- **Resend**：简单的电子邮件发送API，每月3000次免费使用。
- **Twilio**：业界标准的短信/语音服务。
- **Slack/Discord/Telegram**：团队消息传递工具。

### 数据库
- **Supabase**：结合Postgres的认证和存储解决方案。
- **Pinecone/Qdrant**：用于检索式问答（RAG）的向量数据库。
- **Upstash**：无服务器的Redis解决方案。

## 使用示例

```markdown
# Find an API for sending emails
Search AgentAPI for "email" → Returns Resend, SendGrid, Twilio

# Find vector databases for RAG
Search AgentAPI for "vector embeddings" → Returns Pinecone, Qdrant, Weaviate

# Find fast LLM inference
Search AgentAPI for category "ai" + filter by latency → Returns Groq, Gemini Flash
```

## 贡献新API

欢迎在https://agentapihub.com提交新的API（在页面底部提交API链接）。

## 开发者信息

由GizmoLab开发（[@gizmolab_](https://twitter.com/gizmolab_)）—— [gizmolab.io](https://gizmolab.io)