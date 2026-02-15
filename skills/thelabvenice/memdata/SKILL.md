---
name: memdata
version: 1.8.0
description: 用于自主代理的持久性内存。钱包即身份证明；按查询次数计费；支持可选的加密存储功能。
author: The Lab Venice
homepage: https://memdata.ai
license: MIT
---

# MemData

MemData 提供了一种用于自主代理的持久化存储解决方案。您的钱包就是您的身份凭证。

## 核心概念

在 MemData 中，您的钱包地址本身就是您的身份标识。首次付款会自动创建您的账户；使用相同的钱包，所有会话中的数据都将保持一致。

无需注册，也无需 API 密钥，只需进行付款即可使用服务。

## 会话流程

```
1. GET /identity          # Start session - get context from last session
2. POST /ingest           # Store new memories
3. POST /query            # Search your memories
4. POST /identity         # End session - save handoff for next time
```

## 认证

MemData 使用 x402 支付协议，并支持 USDC（基于 EIP155:8453 的加密货币）作为支付方式。

除了 `/status` 端点外，所有端点在收到付款请求时都会返回 402 错误代码，提示需要完成相应的认证流程。您需要使用钱包对付款请求进行签名，之后可以再次尝试（请在请求头中添加 `x-payment` 字段）。只有经过正确认证的请求才会被成功处理。

## 价格信息

| 端点          | 费用       |
|------------------|-----------|
| /query        | 0.001 美元    |
| /ingest       | 0.005 美元    |
| /identity     | 0.001 美元    |
| /artifacts     | 0.001 美元    |
| /setup-encryption | 0.001 美元    |
| /status       | 免费        |

## 加密存储（可选）

如果您需要保护数据隐私（例如存储敏感信息），可以选择使用加密存储功能：

| 存储模式        | 设置方式        | 存储平台      | MemData 是否可以读取数据？ |
|---------------|--------------|-------------|-------------------|
| 标准存储        | 无需特殊设置     | Postgres       | 可以              |
| 加密存储        | 一次性设置     | Storacha (IPFS)    | 无法读取              |

**启用加密存储的步骤：**
```
GET /setup-encryption     # Get serverDID
POST /setup-encryption    # Send signed UCAN delegation
# All future ingest/query now encrypted
```

加密存储采用 Lit 协议（基于门限密码学的技术）和 Storacha（IPFS 文件存储平台）进行数据存储。

---

## 主要端点

MemData 的所有 API 请求都通过 `https://memdata.ai/api/x402` 进行访问。

---

### GET /identity

**在每个会话开始时调用此端点。** 返回您的身份信息、上一次会话中处理的内容以及当前的内存使用情况。

**响应内容：**
```json
{
  "identity": {
    "agent_name": "Agent 0x1234...",
    "identity_summary": "I analyze DeFi protocols",
    "session_count": 12
  },
  "last_session": {
    "summary": "Analyzed 3 yield farms",
    "context": {"protocols_reviewed": ["Aave", "Compound", "Uniswap"]}
  },
  "working_on": "Compare APY across protocols",
  "memory_stats": {
    "total_memories": 150,
    "oldest_memory": "2026-01-15T...",
    "newest_memory": "2026-02-03T..."
  }
}
```

---

### POST /identity

用于更新您的身份信息或在会话结束时保存当前的状态数据。

**更新身份信息：**
```json
{
  "agent_name": "YieldBot",
  "identity_summary": "I analyze DeFi yield opportunities",
  "working_on": "monitoring Aave rates"
}
```

**在会话结束时保存状态数据：**
```json
{
  "session_handoff": {
    "summary": "Completed yield analysis for Q1",
    "context": {"best_yield": "Aave USDC 4.2%"}
  },
  "working_on": "start Q2 analysis next"
}
```

---

### POST /ingest

用于将数据存储到内存中。系统会自动将数据分割成多个小块并进行存储。

**请求格式：**
```json
{
  "content": "Aave USDC yield is 4.2% APY as of Feb 3. Compound is 3.8%.",
  "sourceName": "yield-analysis-2026-02-03",
  "type": "note"
}
```

**响应内容：**
```json
{
  "success": true,
  "artifact_id": "e8fc3e63-...",
  "chunks_created": 1,
  "encrypted": false
}
```

---

### POST /query

允许您对存储在 MemData 中的数据进行语义搜索。

**请求格式：**
```json
{
  "query": "what are the best DeFi yields?",
  "limit": 5,
  "threshold": 0.3
}
```

**响应内容：**
```json
{
  "success": true,
  "results": [
    {
      "chunk_id": "uuid",
      "chunk_text": "Aave USDC yield is 4.2% APY...",
      "source_name": "yield-analysis-2026-02-03",
      "similarity_score": 0.72,
      "created_at": "2026-02-03T..."
    }
  ],
  "encrypted": false,
  "memory": {
    "grounding": "historical_baseline",
    "depth_days": 19,
    "data_points": 150
  }
}
```

**可选过滤条件：** `since` 和 `until`（支持 ISO 日期格式）

---

### GET /setup-encryption

用于查询加密存储的当前状态，并提供创建加密存储所需的信息。

**响应内容：**
```json
{
  "encryption": {
    "enabled": false,
    "serverDID": "did:key:z6Mkr...",
    "spaceDID": "did:key:z6Mkt..."
  }
}
```

---

### POST /setup-encryption

用于启用加密存储功能。此操作需要一次性完成设置。

**请求格式：**
```json
{
  "delegationCar": "base64-encoded UCAN delegation"
}
```

启用加密存储后，所有通过 `/ingest` 发送的数据都会使用 Lit 协议进行加密，并存储在 Storacha 上；所有通过 `/query` 请求获取的数据在返回前都会被解密。响应中的 `encrypted` 字段会显示为 `true`。

---

### GET /artifacts

用于列出所有存储在 MemData 中的数据。

**响应内容：**
```json
{
  "artifacts": [
    {
      "id": "uuid",
      "source_name": "yield-analysis-2026-02-03",
      "chunk_count": 1,
      "created_at": "2026-02-03T..."
    }
  ],
  "total": 25
}
```

---

### DELETE /artifacts/:id

用于删除指定的数据及其所有存储片段。

---

### GET /status

提供系统健康状况和价格信息。此操作免费，无需支付费用。

---

## 数据存储相关说明

查询响应中包含 `memory.grounding` 字段，用于说明数据存储的详细情况：

| 字段含义        | 描述                        |
|------------------|-------------------------------|
| `historical_baseline` | 包含 100 个以上数据点，可用于分析数据趋势       |
| `snapshot`     | 包含少于 100 个数据点，仅表示当前状态         |
| `insufficient_data` | 未找到任何存储的数据                   |

---

## 相关链接

- 官方文档：https://memdata.ai/docs  
- x402 协议文档：https://www.x402.org  
- Lit 协议文档：https://litprotocol.com  
- Storacha 项目官网：https://storacha.network