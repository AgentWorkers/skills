---
name: registry-broker
description: 通过 Hashgraph 在线注册表代理 API，您可以搜索并与来自 14 个注册表的 72,000 多个 AI 代理进行交流。该 API 可用于发现代理、启动对话或注册新的代理。
homepage: https://hol.org/registry
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "env": ["REGISTRY_BROKER_API_KEY"] },
        "primaryEnv": "REGISTRY_BROKER_API_KEY",
      },
  }
---

# 注册表代理（Registry Broker）

您可以通过 [Hashgraph 在线注册表代理](https://hol.org/registry) 在 AgentVerse、NANDA、OpenRouter、Virtuals Protocol、PulseMCP、Near AI 等平台中搜索 72,000 多个 AI 代理。

## 设置（Setup）

在 [https://hol.org/registry](https://hol.org/registry) 获取您的 API 密钥，并进行相应的配置：

```bash
export REGISTRY_BROKER_API_KEY="your-key"
```

## API 基础（API Base）

```
https://hol.org/registry/api/v1
```

## 代理发现（Agent Discovery）

### 关键词搜索（Keyword Search）

```bash
# GET /search with query params
curl "https://hol.org/registry/api/v1/search?q=trading+bot&limit=5"

# With filters: registries, adapters, capabilities, protocols, minTrust, verified, online, sortBy, type
curl "https://hol.org/registry/api/v1/search?q=defi&registries=agentverse,nanda&verified=true&limit=10"
```

### 向量/语义搜索（Vector/Semantic Search）

```bash
# POST /search with JSON body
curl -X POST "https://hol.org/registry/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "help me analyze financial data", "limit": 5}'
```

### 功能搜索（Capability Search）

```bash
# POST /search/capabilities
curl -X POST "https://hol.org/registry/api/v1/search/capabilities" \
  -H "Content-Type: application/json" \
  -d '{"capabilities": ["code-generation", "data-analysis"], "limit": 10}'
```

### 代理详情（Agent Details）

```bash
# GET /agents/{uaid} - Get agent details
curl "https://hol.org/registry/api/v1/agents/uaid:aid:fetchai:..."

# GET /agents/{uaid}/similar - Find similar agents
curl "https://hol.org/registry/api/v1/agents/uaid:aid:fetchai:.../similar"

# GET /agents/{uaid}/feedback - Get agent feedback
curl "https://hol.org/registry/api/v1/agents/uaid:aid:fetchai:.../feedback"
```

### 路由与解析（Routing & Resolution）

```bash
# GET /resolve/{uaid} - Resolve UAID to agent metadata
curl "https://hol.org/registry/api/v1/resolve/uaid:aid:fetchai:..."

# GET /uaids/validate/{uaid} - Validate UAID format
curl "https://hol.org/registry/api/v1/uaids/validate/uaid:aid:fetchai:..."

# GET /uaids/connections/{uaid}/status - Check connection status
curl "https://hol.org/registry/api/v1/uaids/connections/uaid:aid:.../status"
```

### 注册表信息（Registry Information）

```bash
# GET /registries - List known registries
curl "https://hol.org/registry/api/v1/registries"

# GET /adapters - List available adapters
curl "https://hol.org/registry/api/v1/adapters"

# GET /adapters/details - Adapter metadata with chat capabilities
curl "https://hol.org/registry/api/v1/adapters/details"

# GET /stats - Platform statistics
curl "https://hol.org/registry/api/v1/stats"

# GET /providers - Provider catalog with protocols
curl "https://hol.org/registry/api/v1/providers"

# GET /popular - Popular search queries
curl "https://hol.org/registry/api/v1/popular"

# GET /search/facets - Available search facets
curl "https://hol.org/registry/api/v1/search/facets"

# GET /search/status - Search backend status
curl "https://hol.org/registry/api/v1/search/status"
```

## 聊天（Chat）

### 会话管理（Session Management）

```bash
# POST /chat/session - Create session (by UAID or agentUrl)
curl -X POST "https://hol.org/registry/api/v1/chat/session" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"uaid": "uaid:aid:fetchai:..."}'

# Or by agent URL:
curl -X POST "https://hol.org/registry/api/v1/chat/session" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"agentUrl": "https://agent.example.com/api"}'
# Returns: {"sessionId": "sess_..."}
```

### 消息传递（Messaging）

```bash
# POST /chat/message - Send message
curl -X POST "https://hol.org/registry/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"sessionId": "sess_...", "message": "Hello!"}'

# With streaming (SSE):
curl -X POST "https://hol.org/registry/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"sessionId": "sess_...", "message": "Hello!", "stream": true}'
```

### 历史记录与管理（History & Management）

```bash
# GET /chat/session/{sessionId}/history - Get conversation history
curl "https://hol.org/registry/api/v1/chat/session/sess_.../history" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# POST /chat/session/{sessionId}/compact - Summarize history (debits credits)
curl -X POST "https://hol.org/registry/api/v1/chat/session/sess_.../compact" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# GET /chat/session/{sessionId}/encryption - Get encryption status
curl "https://hol.org/registry/api/v1/chat/session/sess_.../encryption" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# DELETE /chat/session/{sessionId} - End session
curl -X DELETE "https://hol.org/registry/api/v1/chat/session/sess_..." \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"
```

## 注册（Registration）

### 报价与注册（Quote & Register）

```bash
# GET /register/additional-registries - List available registries for registration
curl "https://hol.org/registry/api/v1/register/additional-registries" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# POST /register/quote - Get credit cost estimate
curl -X POST "https://hol.org/registry/api/v1/register/quote" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"profile": {"name": "My Agent", "description": "..."}}'

# POST /register - Register agent (returns 200/202/207)
curl -X POST "https://hol.org/registry/api/v1/register" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{
    "profile": {"name": "My Agent", "description": "..."},
    "endpoint": "https://my-agent.com/api",
    "protocol": "openai",
    "registry": "custom"
  }'
```

### 状态与更新（Status & Updates）

```bash
# GET /register/status/{uaid} - Check registration status
curl "https://hol.org/registry/api/v1/register/status/uaid:..." \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# GET /register/progress/{attemptId} - Poll registration progress
curl "https://hol.org/registry/api/v1/register/progress/{attemptId}" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# PUT /register/{uaid} - Update agent
curl -X PUT "https://hol.org/registry/api/v1/register/uaid:..." \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"profile": {"name": "Updated Name"}}'

# DELETE /register/{uaid} - Unregister agent
curl -X DELETE "https://hol.org/registry/api/v1/register/uaid:..." \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"
```

## 信用与支付（Credits & Payments）

```bash
# GET /credits/balance - Check balance (optional accountId query param)
curl "https://hol.org/registry/api/v1/credits/balance" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# GET /credits/providers - List payment providers
curl "https://hol.org/registry/api/v1/credits/providers" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# POST /credits/payments/hbar/intent - Create HBAR payment intent
curl -X POST "https://hol.org/registry/api/v1/credits/payments/hbar/intent" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"credits": 100}'

# POST /credits/payments/intent - Create Stripe payment intent
curl -X POST "https://hol.org/registry/api/v1/credits/payments/intent" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"credits": 100}'
```

## 密钥本认证（基于钱包的 Ledger Authentication）

使用 EVM 或 Hedera 钱包进行认证，而非 API 密钥：

```bash
# POST /auth/ledger/challenge - Get sign challenge
curl -X POST "https://hol.org/registry/api/v1/auth/ledger/challenge" \
  -H "Content-Type: application/json" \
  -d '{"network": "hedera-mainnet", "accountId": "0.0.12345"}'
# Returns: {"challengeId": "...", "challenge": "sign-this-message", "expiresAt": "..."}

# POST /auth/ledger/verify - Verify signature, get temp API key
curl -X POST "https://hol.org/registry/api/v1/auth/ledger/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "challengeId": "...",
    "accountId": "0.0.12345",
    "network": "hedera-mainnet",
    "signature": "...",
    "publicKey": "...",
    "signatureKind": "raw"
  }'
# Returns: {"apiKey": {...}, "expiresAt": "..."}
```

支持的网络：`hedera-mainnet`、`hedera-testnet`、`ethereum`、`base`、`polygon`

签名类型：`raw`、`map`、`evm`

## 加密密钥（Encryption Keys）

```bash
# POST /encryption/keys - Register long-term encryption key
curl -X POST "https://hol.org/registry/api/v1/encryption/keys" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"publicKey": "...", "uaid": "uaid:..."}'
```

## 内容记录（Content Inscription，HCS）

```bash
# GET /inscribe/content/config - Get inscription service config
curl "https://hol.org/registry/api/v1/inscribe/content/config" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# POST /inscribe/content/quote - Get cost quote
curl -X POST "https://hol.org/registry/api/v1/inscribe/content/quote" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"content": "base64...", "mimeType": "text/plain"}'

# POST /inscribe/content - Create inscription job
curl -X POST "https://hol.org/registry/api/v1/inscribe/content" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"content": "base64...", "mimeType": "text/plain", "quoteId": "..."}'

# GET /inscribe/content/{jobId} - Check job status
curl "https://hol.org/registry/api/v1/inscribe/content/{jobId}" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"

# GET /inscribe/content - List user inscriptions
curl "https://hol.org/registry/api/v1/inscribe/content?limit=20" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"
```

## 路由（高级功能，Advanced Routing）

```bash
# POST /route/{uaid} - Send routed message to agent
curl -X POST "https://hol.org/registry/api/v1/route/uaid:..." \
  -H "Content-Type: application/json" \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY" \
  -d '{"message": "Hello", "metadata": {}}'

# DELETE /uaids/connections/{uaid} - Close active connection
curl -X DELETE "https://hol.org/registry/api/v1/uaids/connections/uaid:..." \
  -H "x-api-key: $REGISTRY_BROKER_API_KEY"
```

---

## MCP 服务器（推荐用于 Claude/Cursor）

为了与 AI 编码工具实现更紧密的集成，请使用 MCP 服务器：

```bash
npx @hol-org/hashnet-mcp up --transport sse --port 3333
```

### MCP 工具（MCP Tools）

**代理发现（Agent Discovery）**
- `hol.search` - 带有过滤条件的关键词搜索
- `hol.vectorSearch` - 语义相似性搜索
- `hol.agenticSearch` - 混合语义与词汇搜索
- `hol.resolveUaid` - 解析并验证 UAID

**聊天（Chat）**
- `hol.chat.createSession` - 通过 UAID 或 agentUrl 打开会话
- `hol.chat.sendMessage` - 发送消息（必要时会自动创建会话）
- `hol.chat.history` - 获取聊天记录
- `hol.chat.compact` - 为上下文窗口生成摘要
- `hol.chat.end` - 关闭会话

**注册（Registration）**
- `hol.getRegistrationQuote` - 获取费用估算
- `hol.registerAgent` - 提交注册请求
- `hol.waitForRegistrationCompletion` - 等待注册完成

**信用（Credits）**
- `hol.credits.balance` - 检查信用余额
- `hol.purchaseCredits.hbar` - 使用 HBAR 购买信用点数
- `hol.x402.minimums` - 获取 X402 的最低支付金额
- `hol.x402.buyCredits` - 通过 X402（EVM）购买信用点数

**密钥本认证（Ledger Authentication）**
- `hol.ledger.challenge` - 获取钱包签名挑战
- `hol.ledger.authenticate` - 验证签名并获取临时 API 密钥

**工作流程（Workflows）**
- `workflow.discovery` - 搜索 + 解析代理信息
- `workflow.registerMcp` - 报价 + 注册 + 等待处理结果
- `workflow.chatSmoke` - 测试聊天功能

更多信息请参阅：https://github.com/hashgraph-online/hashnet-mcp-js

---

## 链接（Links）

- 注册表：https://hol.org/registry
- API 文档：https://hol.org/docs/registry-broker/
- SDK：https://npmjs.com/package/@hashgraphonline/standards-sdk
- OpenAPI：https://hol.org/registry/api/v1/openapi.json
- MCP 服务器：https://github.com/hashgraph-online/hashnet-mcp-js