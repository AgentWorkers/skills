---
name: elizacloud
description: **管理 elizaOS Cloud**  
- 部署 AI 代理（AI agents）  
- 提供聊天辅助功能（chat completions）  
- 支持图像/视频生成（image/video generation）  
- 实现语音克隆（voice cloning）  
- 管理知识库（knowledge base）  
- 支持容器技术（containers）  
- 提供市场服务（marketplace）  

**使用说明：**  
该工具用于与 elizaOS Cloud 或 elizacloud.ai 进行交互，部署 AI 代理，或管理托管在云端的 AI 代理。**需要**设置 `ELIZACLOUD_API_KEY` 环境变量才能正常使用。
metadata:
  openclaw:
    requires:
      env: [ELIZACLOUD_API_KEY]
---

# elizaOS Cloud

elizaOS Cloud 是一个用于构建、部署和扩展智能 AI 代理的平台。该平台提供了完整的 elizaOS Cloud API，支持代理管理、内容生成以及 AI 驱动的应用程序开发。

## 快速入门

将您的 API 密钥设置为环境变量：

```bash
export ELIZACLOUD_API_KEY="your_api_key_here"
```

使用随附的 bash 客户端执行常见操作：

```bash
./scripts/elizacloud-client.sh status
./scripts/elizacloud-client.sh agents list
./scripts/elizacloud-client.sh chat agent-id "Hello!"
```

## API 配置

- **基础 URL**：`https://elizacloud.ai/api/v1`
- **认证**：
  - `Authorization: Bearer $ELIZACLOUD_API_KEY`
  - `X-API-Key: $ELIZACLOUD_API_KEY`
- **Content-Type**：`application/json`

## 核心端点

### 聊天补全（兼容 OpenAI）

```bash
curl https://elizacloud.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-agent-id",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

**特性**：流式处理、函数调用、结构化输出

### 代理管理

- **列出代理**  
```bash
GET /api/my-agents/characters
```

- **创建代理**  
```bash
POST /api/v1/app/agents
{
  "name": "My Assistant",
  "bio": "A helpful AI assistant"
}
```

- **获取代理**  
```bash
GET /api/my-agents/characters/{id}
```

- **删除代理**  
```bash
DELETE /api/my-agents/characters/{id}
```

### 图像生成

```bash
POST /api/v1/images/generate
{
  "prompt": "A futuristic city at sunset",
  "model": "flux-pro",
  "width": 1024,
  "height": 1024
}
```

**模型**：FLUX Pro、FLUX Dev、Stable Diffusion

### 视频生成

```bash
POST /api/v1/video/generate
{
  "prompt": "A peaceful lake with mountains in the background",
  "duration": 5,
  "model": "minimax-01"
}
```

**模型**：MiniMax、Runway

### 语音克隆（ElevenLabs）

```bash
POST /api/v1/voice/clone
{
  "text": "Hello, this is a test of voice cloning",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "model": "eleven_turbo_v2"
}
```

### 知识库

- **上传文档**  
```bash
POST /api/v1/knowledge/upload
```

- **查询知识**  
```bash
POST /api/v1/knowledge/query
{
  "query": "How do I deploy an agent?",
  "limit": 5
}
```

### 容器

- **部署容器**  
```bash
POST /api/v1/containers
{
  "name": "my-app",
  "image": "nginx:latest",
  "ports": [{"containerPort": 80}]
}
```

### A2A 协议（代理间通信）

- **发现代理**  
```bash
GET /api/v1/discovery
```

- **发送任务**  
```bash
POST /api/a2a
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "params": {
    "id": "task_123",
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "Analyze this data"}]
    }
  },
  "id": 1
}
```

## API 密钥

**创建 API 密钥**
```bash
POST /api/v1/api-keys
{
  "name": "Production Key",
  "permissions": ["chat", "agents", "images"]
}
```

**可用权限**：`chat`、`embeddings`、`images`、`video`、`voice`、`knowledge`、`agents`、`apps`

## 错误处理

所有错误均遵循以下格式：

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request body is invalid",
    "details": "Field 'model' is required"
  }
}
```

**常见错误代码**：
- `UNAUTHORIZED` (401)：无效或缺失的认证信息
- `FORBIDDEN` (403)：权限不足
- `NOT_FOUND` (404)：资源未找到
- `RATE_LIMITED` (429)：请求次数过多
- `INSUFFICIENT_CREDITS` (402)：信用点数不足

## 请求速率限制

| 端点           | 速率限制      |
|------------------|-------------|
| 聊天补全       | 60 次/分钟     |
| 图像生成       | 100 次/分钟     |
| 视频生成       | 5 次/分钟     |

## 示例工作流程

### 部署客户支持代理

```bash
# 1. Create agent
curl -X POST https://elizacloud.ai/api/v1/app/agents \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"name": "Support Bot", "bio": "Customer support specialist"}'

# 2. Chat with agent
curl https://elizacloud.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"model": "agent-id", "messages": [{"role": "user", "content": "Help me"}]}'
```

### 生成营销素材

```bash
# 1. Generate image
curl -X POST https://elizacloud.ai/api/v1/images/generate \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"prompt": "Modern tech startup logo", "model": "flux-pro"}'

# 2. Generate video
curl -X POST https://elizacloud.ai/api/v1/video/generate \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"prompt": "Product demo animation", "duration": 10}'
```

### 使用 A2A 协议构建代理网络

```bash
# 1. Discover available agents
curl https://elizacloud.ai/api/v1/discovery \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY"

# 2. Delegate task to specialist agent
curl -X POST https://elizacloud.ai/api/a2a \
  -H "Authorization: Bearer $ELIZACLOUD_API_KEY" \
  -d '{"jsonrpc": "2.0", "method": "tasks/send", "params": {"message": {"role": "user", "parts": [{"type": "text", "text": "Analyze financial data"}]}}}'
```

## 入门指南

### 注册
在 [elizacloud.ai/login](https://elizacloud.ai/login) 注册（需要浏览器登录）。新账户可免费获得 **1,000 个信用点数**，足以测试聊天、图像生成等功能。

### 获取 API 密钥
```bash
# After signing up, create a key at Dashboard → API Keys
# Or via API (once authenticated):
POST /api/v1/api-keys
{
  "name": "My OpenClaw Agent",
  "permissions": ["chat", "agents", "images", "video", "voice", "knowledge"]
}
```

### 安装 CLI（可选）
```bash
bun add -g @elizaos/cli
elizaos login
```

## 支付与信用点数

### 查看余额
```bash
GET /api/v1/credits/balance
```

### 购买信用点数（Stripe）
```bash
POST /api/v1/credits/checkout
{ "amount": 5000 }
# Returns a Stripe checkout URL — redirect to complete payment
```

### 使用 x402 加密货币支付（USDC）
支持按请求使用加密货币支付——无需预先购买信用点数：
```bash
# Include x402 payment header with any API request
curl -X POST "https://elizacloud.ai/api/v1/chat/completions" \
  -H "X-PAYMENT: <x402-payment-header>" \
  -H "Content-Type: application/json" \
  -d '{"model": "agent-id", "messages": [{"role": "user", "content": "Hello"}]}'
```

### 自动充值
```bash
PUT /api/v1/billing/settings
{
  "autoTopUp": true,
  "threshold": 100,
  "amount": 1000
}
```

### 信用点数交易
```bash
GET /api/credits/transactions?limit=50
```

### 使用情况总结
```bash
GET /api/v1/credits/summary
# Returns: org balance, agent budgets, app earnings, redeemable earnings
```

## 钱包与加密货币 RPC 请求

### 创建加密货币支付请求
```bash
POST /api/crypto/payments
```

### 查看支付状态
```bash
GET /api/crypto/status
```

### 认证方法
| 方法            | 头部字段       | 使用场景       |
|------------------|--------------|-------------------------|
| API Key         | `Authorization: Bearer ek_xxx` | 服务器间通信       |
| X-API-Key        | `X-API-Key: ek_xxx`     | 替代头部字段       |
| x402            | `X-PAYMENT: <header>` | 按请求使用 USDC 支付    |
| Session          | 基于 Cookie 的认证   | 浏览器应用程序       |

## 额外资源

- **完整 API 文档**：请参阅 `references/api-reference.md` 以获取完整的端点详情
- **仪表板**：https://elizacloud.ai/dashboard 用于可视化管理
- **OpenAPI 规范**：https://elizacloud.ai/api/openapi.json
- **SDK**：提供 TypeScript 和 Python 客户端
- **社区**：Discord 社区：https://discord.gg/elizaos

## 环境变量

- `ELIZACLOUD_API_KEY`：您的 elizaOS Cloud API 密钥（必需）
- `ELIZACLOUD_BASE_URL`：API 基础 URL（默认：https://elizacloud.ai/api/v1）

## 安全注意事项

- **切勿将 API 密钥提交到版本控制系统中**
- **为开发环境和生产环境使用不同的密钥**
- **定期轮换密钥**
- **将权限限制在最低必要范围内**
- **通过仪表板监控使用情况，及时发现异常**