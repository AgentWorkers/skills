---
name: x402-direct
description: 通过 `x402.direct` 目录 API 发现并搜索支持 x402 支付方式的服务。当代理需要查找接受 x402 支付的付费 API 服务、浏览 x402 生态系统、查询服务详情、检查信任评分或搜索特定功能（如 AI、图像处理、天气信息、搜索、数据、音频、视频、开发工具、金融、语言服务、存储服务等）时，可以使用该 API。相关触发词包括：“find x402 service”、“x402 directory”、“search x402”、“x402 API”、“paid API search”、“x402.direct”以及“agent-to-agent payments”和“crypto-native API discovery”。
---

# x402.direct – 服务目录

x402.direct API 是一个用于查询支持 x402 支付方式的服务的目录。它索引了能够接受 x402 支付（HTTP 402 + 加密货币）的服务，并提供搜索、浏览和信任评分功能。

**基础 URL:** `https://x402.direct`

## 端点（Endpoints）

### 1. 搜索（需付费 – 每次查询费用 $0.001）

```
GET /api/search?q=<query>
```

可以对所有被索引的服务进行全文搜索。搜索结果根据文本相关性和信任评分进行排序。该功能受到 x402 中间件的保护：首次请求会返回 HTTP 402 错误，需要用户提供支付凭证后才能再次发送请求。

**参数（Parameters）:**

| 参数          | 类型        | 是否必填 | 描述                                      |
|---------------|------------|---------|-----------------------------------------|
| q             | string       | 是        | 搜索查询（最长 500 个字符）                          |
| category       | string       | 否        | 按类别过滤                                   |
| network        | string       | 否        | 按区块链网络过滤                               |
| maxPrice       | string       | 否        | 最高价格（以原子单位计，类型为 bigint）                   |
| minScore       | integer      | 否        | 最低信任评分（0-100）                              |
| limit          | integer      | 否        | 最多显示结果数量（默认 20，最多 50）                        |

**示例（Example）:**

```bash
curl "https://x402.direct/api/search?q=weather+api&minScore=60&limit=5"
```

**响应格式（Response Format）:**

```json
{
  "query": "weather api",
  "count": 3,
  "results": [
    {
      "id": 42,
      "resourceUrl": "https://example.com/api/weather",
      "description": "Real-time weather data for any location",
      "category": "weather",
      "provider": "example.com",
      "network": "base-mainnet",
      "price": "1000",
      "priceUsd": "0.001",
      "scoutScore": 85,
      "scoutVerdict": "safe",
      "relevance": 0.3214,
      "score": 58.11
    }
  ]
}
```

**x402 支付流程:**

1. 向 `/api/search?q=...` 发送 GET 请求，且请求头中不包含支付信息。
2. 服务器返回 HTTP 402 错误，并在响应体中包含支付详情（价格、网络、收款地址、支付中介的 URL）。
3. 使用 Base（通过代理钱包或 Coinbase Agentic Wallet）支付 $0.001 USDC。
4. 重新发送相同的请求，并在请求头中添加 `X-402-Payment: <proof>` 字段。
5. 服务器通过支付中介验证支付信息后，返回搜索结果。

如果使用支持 x402 的 HTTP 客户端（例如 `x402` npm 包），支付过程将自动完成：

```typescript
import { createX402Client } from "x402";
const client = createX402Client({ wallet: agentWallet });
const resp = await client.fetch("https://x402.direct/api/search?q=weather+api");
```

### 2. 浏览服务（免费）

```
GET /api/services
```

提供所有被索引服务的分页列表。无需支付费用。

**参数（Parameters）:**

| 参数          | 类型        | 默认值     | 描述                                      |
|---------------|------------|---------|-----------------------------------------|
| page          | integer      | 1         | 当前页码                                    |
| limit          | integer      | 50        | 每页显示的结果数量（最多 100）                          |
| category       | string       | --        | 按类别过滤                                   |
| network        | string       | --        | 按区块链网络过滤                               |
| sort          | string       | score      | 排序方式：`score`、`newest`、`price`                   |
| minScore       | integer      | --        | 最低信任评分（0-100）                              |

**示例（Example）:**

```bash
# Top-rated AI services
curl "https://x402.direct/api/services?category=ai&sort=score&limit=10"

# Newest services on Base mainnet
curl "https://x402.direct/api/services?network=base-mainnet&sort=newest"

# Only high-trust services
curl "https://x402.direct/api/services?minScore=70&sort=score"
```

**响应格式（Response Format）:**

```json
{
  "services": [
    {
      "id": 1,
      "resourceUrl": "https://example.com/api/generate",
      "type": "x402",
      "description": "AI text generation endpoint",
      "category": "ai",
      "provider": "example.com",
      "network": "base-mainnet",
      "scheme": "exact",
      "price": "5000",
      "priceUsd": "0.005",
      "scoutScore": 92,
      "scoutVerdict": "safe",
      "lastSeen": "2025-05-01T12:00:00.000Z",
      "createdAt": "2025-04-15T08:00:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 127,
    "totalPages": 3
  }
}
```

### 3. 服务详情（免费）

```
GET /api/services/:id
```

提供单个服务的详细信息，包括支付选项、原始元数据和支付中介信息。

**示例（Example）:**

```bash
curl "https://x402.direct/api/services/42"
```

**响应格式（Response Format）:**

```json
{
  "id": 42,
  "resourceUrl": "https://example.com/api/weather",
  "type": "x402",
  "x402Version": "1",
  "description": "Real-time weather data for any location",
  "mimeType": "application/json",
  "category": "weather",
  "provider": "example.com",
  "network": "base-mainnet",
  "scheme": "exact",
  "price": "1000",
  "priceUsd": "0.001",
  "payTo": "0xAbC123...",
  "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "scoutScore": 85,
  "scoutVerdict": "safe",
  "accepts": [{"scheme": "exact", "network": "base-mainnet", "maxAmountRequired": "1000", "asset": "..."}],
  "metadata": {"description": "...", "mimeType": "application/json"},
  "lastSeen": "2025-05-01T12:00:00.000Z",
  "lastUpdated": "2025-05-01T12:00:00.000Z",
  "createdAt": "2025-04-15T08:00:00.000Z",
  "facilitator": {
    "name": "x402.org",
    "url": "https://x402.org/facilitator",
    "facilitatorId": "x402-org-mainnet"
  }
}
```

### 4. 生态系统统计（免费）

```
GET /api/stats
```

提供生态系统的高层次统计信息，便于查看整体情况。

**示例（Example）:**

```bash
curl "https://x402.direct/api/stats"
```

**响应格式（Response Format）:**

```json
{
  "services": 247,
  "providers": 38,
  "categories": 12,
  "facilitators": 3,
  "avgScoutScore": 62,
  "networks": [
    { "network": "base-mainnet", "count": 180 },
    { "network": "base-sepolia", "count": 45 },
    { "network": "polygon", "count": 15 },
    { "network": "solana", "count": 7 }
  ]
}
```

## 过滤条件（Filter Values）

**类别（Categories）:** `ai`, `image`, `weather`, `search`, `data`, `audio`, `video`, `developer`, `finance`, `language`, `storage`, `other`

**区块链网络（Networks）:** `base-mainnet`, `base-sepolia`, `polygon`, `solana`（随着生态系统的发展，可能还会增加更多网络）

**排序方式（Sort Options）:** `score`（默认：信任评分）、`newest`（创建时间）、`price`（价格从低到高）

## 信任评分（ScoutScore）

每个服务的信任评分范围为 0-100，评分依据包括：

- HTTPS 安全性
- 服务是否部署在主网（mainnet）或测试网（testnet）
- 域名的唯一性及服务提供商的声誉
- 服务描述的完整性和文档质量
- 价格是否合理
- 是否使用自定义域名（而非通用托管服务）

**评分说明：**

| 评分范围        | 评分结果    | 含义                                      |
|-----------------|-----------|----------------------------------------|
| 70-100         | `安全`      | 服务文档齐全，部署在主网，使用自定义域名                |
| 40-69         | `谨慎使用`    | 缺少部分信任评分依据                        |
| 0-39         | `避免使用`    | 缺少关键信任评分依据                        |

**建议：**在搜索适用于生产环境的服务时，建议设置 `minScore` 为 60 或更高；仅在探索或调试时使用 `minScore=0`。

## 使用场景（Usage Patterns）

- **查找特定任务所需的服务：**  
  ```bash
# Agent needs image generation
curl "https://x402.direct/api/services?category=image&sort=score&minScore=60&limit=5"
```

- **根据特定功能进行搜索（需付费）：**  
  ```bash
curl "https://x402.direct/api/search?q=text+to+speech&minScore=70" \
  -H "X-402-Payment: <proof>"
```

- **在调用服务前获取详细信息：**  
  ```bash
# Found service ID 42 from browse/search, now get payment details
curl "https://x402.direct/api/services/42"
# Use the payTo, asset, network, and price fields to construct the x402 payment
```

- **检查生态系统健康状况：**  
  ```bash
curl "https://x402.direct/api/stats"
```

## 决策指南（Decision Guide）

| 目标                          | 对应端点        | 费用        |
|-----------------------------------|-------------------|------------|
| 按类别/网络浏览服务        | `/api/services`   | 免费        |
| 获取服务支付详情        | `/api/services/:id` | 免费        |
| 使用自然语言搜索        | `/api/search`     | 每次查询 $0.001    |
| 查看生态系统概览      | `/api/stats`      | 免费        |

**建议：**  
- 当已知服务类别时，优先使用 `/api/services` 并设置相应过滤条件；  
- 当需要根据服务描述和提供商进行语义匹配时，使用 `/api/search`。