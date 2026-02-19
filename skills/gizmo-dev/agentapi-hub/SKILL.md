---
name: agentapi
description: 浏览并搜索 AgentAPI 目录——这是一个专为 AI 代理设计的 API 数据库。您可以在这里找到与 MCP 兼容的 API，用于搜索、AI 操作、通信、数据库管理、支付等功能。该目录支持基于 USDC 的 x402 按使用量计费的支付方式。
author: gizmolab
version: 1.0.3
tags: [api, mcp, agents, directory, search, integrations, x402, crypto, payments]
---
# AgentAPI

这是一个专为AI代理设计的API目录，支持机器读取，并兼容MCP协议。所有API均可被AI代理直接访问。

**官方网站：** https://agentapihub.com  
**计费API：** https://api.agentapihub.com  
**文档：** https://api.agentapihub.com/api/docs  

## x402 按使用次数计费的支付方式  

AgentAPI支持**x402**支付协议，允许AI代理使用USDC在Base链上进行API调用。无需API密钥。  

### 工作原理：  
1. 代理调用API端点（例如：`/api/gemini/chat/completions`）。  
2. 服务器返回`402 Payment Required`的响应，其中包含费用信息和钱包地址。  
3. 代理在Base链上使用USDC完成支付。  
4. 代理在请求头中附上支付证明后重新尝试调用API。  
5. 服务器验证支付信息后，代理的请求会被转发并返回响应。  

### 示例流程：  
```bash
# 1. Initial request returns 402
curl https://api.agentapihub.com/api/gemini/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-2.0-flash","messages":[{"role":"user","content":"Hello"}]}'

# Response: 402 Payment Required
# {
#   "price": "0.001",
#   "currency": "USDC",
#   "chain": "base",
#   "recipient": "0xcCb92A101347406ed140b18C4Ed27276844CD9D7",
#   "paymentId": "pay_abc123"
# }

# 2. Agent pays on Base, retries with proof
curl https://api.agentapihub.com/api/gemini/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Payment-Proof: 0x..." \
  -d '{"model":"gemini-2.0-flash","messages":[{"role":"user","content":"Hello"}]}'
```  

### 可用的x402 API：  
| API | 端点 | 费用（单位：USD） |
|-----|----------|-------|  
| Gemini Chat | `/api/gemini/chat/completions` | 约0.001美元/次 |  
| Gemini Embeddings | `/api/gemini/embeddings` | 约0.0005美元/次 |  

### 选择x402的原因：  
- **无需API密钥**：代理可以自行配置访问权限。  
- **按使用次数计费**：无需订阅，无最低使用量要求。  
- **基于加密货币**：使用USDC在Base链上进行支付，交易速度快且成本低。  
- **对代理友好**：支持编程化支付，无需人工干预。  

## 快速搜索：  
### 按类别分类：  
| 类别 | API | 示例功能 |  
|------|------|---------|  
| 搜索 | Brave, Serper, Exa, Tavily, Perplexity | 支持AI辅助的网页搜索功能。  
| AI与机器学习 | OpenAI, Claude, Gemini, Groq, Replicate | 提供大语言模型（LLM）推理和图像生成服务。  
| 通信 | Resend, Twilio, Slack, Discord, Telegram | 支持电子邮件、短信和即时通讯功能。  
| 数据库 | Supabase, Pinecone, Qdrant, Neon, Upstash | 提供SQL数据库、向量存储和键值存储服务。  
| 支付 | Stripe, Lemon Squeezy, PayPal | 提供支付处理服务。  
| 数据抓取 | Firecrawl, Browserbase, Apify | 支持网页抓取和自动化任务。  
| 开发工具 | GitHub, Vercel, Linear, Sentry | 提供代码托管、部署和问题跟踪功能。  
| 生产力工具 | Notion, Google Calendar, Todoist | 提供任务管理和日程安排功能。  

### 兼容MCP协议的API  
目录中的50多个API均支持MCP协议。可通过`?mcp=true`进行筛选。  

## API访问方式：  
### JSON格式的API端点：  
```bash
# Fetch all APIs
curl https://agentapihub.com/api/v1/apis

# Search by capability
curl "https://agentapihub.com/api/v1/apis?q=send+email&mcp=true"

# Filter by category
curl "https://agentapihub.com/api/v1/apis?category=ai"
```  

### 响应格式：  
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

## 按类别划分的热门API：  
### 搜索：  
- **Brave Search**：注重隐私保护，每月免费使用2000次搜索请求。  
- **Exa**：专为AI代理设计的神经/语义搜索工具。  
- **Tavily**：专为AI代理设计的搜索引擎。  

### AI与机器学习：  
- **OpenAI**：提供GPT-4、DALL-E、Whisper等模型。  
- **Anthropic Claude**：适合推理和编程任务。  
- **Groq**：具有最快的推理速度（超过500次请求/秒）。  

### 通信：  
- **Resend**：简单的电子邮件发送API，每月免费使用3000次。  
- **Twilio**：提供短信和语音通信服务，属于行业标准。  
- **Slack/Discord/Telegram**：支持团队协作和消息传递。  

### 数据库：  
- **Supabase**：结合Postgres和身份验证功能的数据库系统。  
- **Pinecone/Qdrant**：用于快速检索的向量数据库。  
- **Upstash**：基于Serverless技术的Redis存储解决方案。  

## 使用示例：  
```markdown
# Find an API for sending emails
Search AgentAPI for "email" → Returns Resend, SendGrid, Twilio

# Find vector databases for RAG
Search AgentAPI for "vector embeddings" → Returns Pinecone, Qdrant, Weaviate

# Find fast LLM inference
Search AgentAPI for category "ai" + filter by latency → Returns Groq, Gemini Flash
```  

## 贡献方式：  
如需提交新的API，请访问：https://agentapihub.com（在页面底部提交API相关信息）。  

## 开发者信息：  
AgentAPI由GizmoLab开发（[@gizmolab_](https://twitter.com/gizmolab_)，官网：[gizmolab.io](https://gizmolab.io)