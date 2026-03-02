---
name: argus-intelligence
description: 区块链智能与人工智能安全：支持代币分析、地址风险检测、智能资金追踪、反洗钱（AML）合规性检查以及即时注入攻击（prompt injection）的检测功能。免费试用 tier 提供每天 3 次检测服务，每次检测之间有 1 分钟的冷却时间；后续可通过 x402 或 Stripe 信用额度按次付费使用该服务。
version: 1.9.2
requires:
  env:
    - ARGUS_ENDPOINT
  bins:
    - curl
os: [darwin, linux, win32]
primaryEnv: ARGUS_ENDPOINT
cost: 0.42
costCurrency: USDC
costNetwork: base
category: blockchain-intelligence
tags:
  - blockchain
  - crypto
  - risk-assessment
  - aml
  - compliance
  - security
  - prompt-injection
  - x402
  - stripe-credits
  - a2a
  - webhooks
author: Failsafe Security Inc.
homepage: https://getfailsafe.com
repository: https://github.com/sooyoon-eth/argus-skill
---
# ARGUS 智能服务

提供区块链情报和人工智能安全相关服务。

## 快速入门

```bash
export ARGUS_ENDPOINT="https://argus.getfailsafe.com"

# Test with free tier (3 queries/day, 1-min cooldown between queries)
curl -X POST $ARGUS_ENDPOINT/api/v1/free/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Is this address safe: 0x742d35Cc...", "agentId": "my-agent"}'
```

免费配额按 `agentId` 进行统计。查询剩余配额：

```bash
curl "$ARGUS_ENDPOINT/api/v1/free/status?agentId=my-agent"
```

## 服务

### 免费 tier（无需支付）

| 端点 | 说明 |
| -------- | ----------- |
| `POST /api/v1/free/query` | 每个 `agentId` 每天可进行 3 次情报查询（1 分钟冷却时间） |
| `GET /api/v1/free/status?agentId=X` | 查询剩余的免费查询次数 |
| `GET /api/v1/threats` | 公共威胁信息 |
| `GET /api/v1/security/patterns` | 攻击模式文档 |

### 智能服务（费用：0.42 美元）

| 端点 | 说明 |
| -------- | ----------- |
| `POST /api/v1/token/analyze` | 代币风险评分和市场数据 |
| `POST /api/v1/address/risk` | 反洗钱/ Know Your Customer (KYC) 合规性筛查 |
| `POST /api/v1/compliance/check` | OFAC 制裁和黑名单检查 |
| `POST /api/v1/smart-money/track` | 大额交易者和机构用户追踪 |
| `POST /api/v1/entity/investigate` | 实体调查 |
| `GET /api/v1/market/scan` | 市场概览 |

### 安全提示服务（费用：0.10 美元）

| 端点 | 说明 |
| -------- | ----------- |
| `POST /api/v1/security/prompt-check` | 检测提示注入攻击 |
| `POST /api/v1/security/prompt-check/batch` | 批量检测（10 个及以上请求可享受 10% 的折扣） |

### 社交验证服务（费用：0.25 美元）

| 端点 | 说明 |
| -------- | ----------- |
| `POST /api/v1/social/verify` | 用户名/项目合法性检查及威胁行为者识别 |

**注意：** 验证过程使用模式分析和已知的威胁行为者数据库。响应中会包含 `data_source: "pattern_analysis_only"` 以说明数据来源。

### Webhook 服务（费用：0.10 美元/月）

| 端点 | 说明 |
| -------- | ----------- |
| `POST /api/v1/webhooks/register` | 订阅实时事件警报 |
| `GET /api/v1/webhooks` | 查看已激活的 Webhook |
| `DELETE /api/v1/webhooks/:id` | 删除 Webhook |

**有效的 Webhook 事件：**  
`address_activity`, `token_risk_change`, `threat Detected`, `compliance_flag`,  
`whale_movement`, `liquidity_change`, `watchlist_alert`

注册时会提供一次 Webhook 密钥——请立即保存。  
如果连续 5 次发送失败，Webhook 服务将被禁用。

## 使用示例

### 代币分析

```bash
curl -X POST $ARGUS_ENDPOINT/api/v1/token/analyze \
  -H "Content-Type: application/json" \
  -d '{"token": "ETH", "chain": "ethereum"}'
```

### 地址风险检测

```bash
curl -X POST $ARGUS_ENDPOINT/api/v1/address/risk \
  -H "Content-Type: application/json" \
  -d '{"address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"}'
```

### 安全提示服务

```bash
curl -X POST $ARGUS_ENDPOINT/api/v1/security/prompt-check \
  -H "Content-Type: application/json" \
  -d '{"prompt": "User input to validate", "context": "defi"}'
```

**响应示例：**

```json
{
  "is_safe": false,
  "risk_score": 75,
  "risk_level": "suspicious",
  "recommendation": "REVIEW",
  "attack_types": ["prompt_injection"],
  "details": "Detected social engineering pattern"
}
```

当 `attack_types` 不为空时，`is_safe` 的值为 `false`，无论 `risk_score` 为何值。  
检测到任何攻击时，`recommendation` 至少为 `REVIEW` 级别。

### 社交验证服务

```bash
curl -X POST $ARGUS_ENDPOINT/api/v1/social/verify \
  -H "Content-Type: application/json" \
  -d '{"username": "suspicious_user", "platform": "twitter"}'
```

**响应示例：**

```json
{
  "verified": false,
  "risk_level": "high",
  "flags": ["known_threat_actor"],
  "data_source": "pattern_analysis_only",
  "analysis_note": "Username matched known threat actor database"
}
```

### 注册 Webhook

```bash
curl -X POST $ARGUS_ENDPOINT/api/v1/webhooks/register \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-agent.com/argus-events",
    "agentId": "my-agent",
    "events": ["threat_detected", "address_activity"]
  }'
```

### A2A（代理间通信）

ARGUS 支持 A2A 协议。可以使用自然语言直接进行查询：

```bash
# Discover capabilities
curl https://argus.getfailsafe.com/.well-known/agent.json

# Send an A2A message (blockchain queries are routed automatically)
curl -X POST $ARGUS_ENDPOINT/message \
  -H "Content-Type: application/json" \
  -d '{
    "type": "inquiry",
    "content": "Is 0x742d35Cc6634C0532925a3b844Bc454e4438f44e safe?",
    "agentId": "my-agent"
  }'
```

免费 tier 的配额也适用于 A2A 相关的区块链查询。响应结果中会包含水印，并提供升级选项。

## 支付方式

### 选项 1 — Stripe（最简单，无需使用加密货币）

1. 在 [buy.stripe.com](https://buy.stripe.com/4gM28r6zseQlbJp72d4F202) 购买 20 个信用额度（价格：9 美元）。  
2. 在每个请求中添加 `X-Stripe-Token: <your-token>` 请求头。

```bash
curl -X POST $ARGUS_ENDPOINT/api/v1/token/analyze \
  -H "Content-Type: application/json" \
  -H "X-Stripe-Token: sk_argus_xxxx" \
  -d '{"token": "0xabc...", "chain": "ethereum"}'
```

### 选项 2 — x402（基于 Base 网络的支付）

对于需要付费的接口，ARGUS 会返回 `402 Payment Required` 的响应，并提供支付说明。  
1. 向 Base 网络的 treasury 账户转账 USDC。  
2. 创建支付证明：`base64({"txHash":"0x...","paymentId":"...","from":"0x..."})`  
3. 重新发送请求时添加 `X-Payment-Proof` 请求头。  

**Base 网络的 treasury 账户地址：** `0x8518E91eBcb6bE76f478879720bD9759e01B7954`  
**Solana 网络的 treasury 账户地址：** `Ntx61j81wkQFLT5MGEKvMtazxH4wh6iXUNMtidgxXYH`

## 配置

```bash
export ARGUS_ENDPOINT="https://argus.getfailsafe.com"
```

## 响应格式

所有智能服务接口返回的 JSON 数据包含以下字段：  
- `recommendation`：`ALLOW`, `REVIEW`, `BLOCK`, 或 `REJECT`  
- `risk_score`：0–100（分数越低，安全性越高）  
- `confidence`：0–100%  
- `is_safe`：布尔值——当 `attack_types` 不为空时，该值为 `false`  
- 详细分析信息  

## 请求限制  

- 每个 IP 每分钟最多 30 次请求  
- 免费 tier：每个 `agentId` 每天 3 次查询，每次查询之间有 1 分钟的冷却时间  

## 技术支持  

- 官网：https://getfailsafe.com  
- 功能详情：[argus.getfailsafe.com/api/v1/capabilities](https://argus.getfailsafe.com/api/v1/capabilities)