---
name: messari-crypto
description: >
  Crypto market intelligence powered by Messari's REST API. Provides real-time access to
  Messari AI (chat completions over 30TB+ crypto data), Signal (sentiment, mindshare, trending
  narratives), Metrics (prices, volumes, fundamentals for 34,000+ assets across 210+ exchanges),
  News, Research, Stablecoins, Exchanges, Networks, Protocols, Token Unlocks, Fundraising, Intel,
  Topics, and X-Users data.
  Use when the user asks about crypto markets, token analysis, sentiment, protocol metrics, asset
  research, trending narratives, stablecoin flows, token unlock schedules, fundraising rounds,
  governance events, or any blockchain/crypto data question.
  Requires a Messari API key and Messari AI credits.
metadata:
  openclaw:
    env:
      - name: MESSARI_API_KEY
        description: Messari API key from messari.io/api
        required: true
---

# Messari Crypto Intelligence

通过Messari的REST API获取实时的加密货币市场情报——利用AI技术进行分析，提供链上数据指标、市场情绪分析、新闻以及机构级别的研究报告，无需自行构建数据管道。

## 前提条件

- **Messari API密钥**：请在 [messari.io/api](https://messari.io/api) 获取
- **Messari AI信用点**：使用AI功能时需要这些信用点

## REST API概述

**基础URL：** `https://api.messari.io`

**身份验证：** 在每个请求中都必须包含您的API密钥：

```
x-messari-api-key: <YOUR_API_KEY>
```

所有端点都支持并返回JSON格式的数据。POST请求时请设置 `Content-Type: application/json`。

## 服务路由表

| 服务 | 基础路径 | 使用场景 |
|---|---|---|
| **AI** | `/ai/` | 通用加密货币问题解答，跨数据源的综合分析 |
| **Signal** | `/signal/v1/` | 市场情绪分析、趋势分析 |
| **Metrics** | `/metrics/v2/` | 价格、交易量、市值、基本数据 |
| **News** | `/news/v1/` | 实时加密货币新闻、突发事件 |
| **Research** | `/research/v1/** | 机构研究报告、协议深度分析 |
| **Stablecoins** | `/stablecoins/v2/` | 稳定币供应量、链上数据 |
| **Exchanges** | `/exchanges/v2/` | 交易所交易量、指标数据 |
| **Networks** | `/networks/v2/` | 第一/第二层网络指标数据 |
| **Protocols** | `/protocols/v2/** | DeFi协议指标（去中心化交易所、借贷、质押等） |
| **Token Unlocks** | `/token-unlocks/v1/** | 代币解锁计划、解锁事件 |
| **Fundraising** | `/fundraising/v1/** | 融资轮次、投资者信息、并购动态 |
| **Intel** | `/intel/v1/** | 治理事件、协议更新 |
| **Topics** | `/topics/v1/** | 热门话题分类、每日数据趋势 |
| **X-Users** | `/signal/v1/x-users/** | 加密货币领域Twitter用户数据分析 |

有关详细端点文档，请参阅 [references/api_services.md](references/api_services.md)。

## 示例请求

### AI聊天辅助

```bash
curl -X POST "https://api.messari.io/ai/v1/chat/completions" \
  -H "x-messari-api-key: $MESSARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is the bull case for ETH right now?"}
    ]
  }'
```

### 资产指标查询

```bash
curl "https://api.messari.io/metrics/v2/assets?assetSlugs=bitcoin,ethereum" \
  -H "x-messari-api-key: $MESSARI_API_KEY"
```

### 市场情绪分析

```bash
curl "https://api.messari.io/signal/v1/assets/gainers-losers?type=mindshare&limit=10" \
  -H "x-messari-api-key: $MESSARI_API_KEY"
```

### 新闻推送

```bash
curl "https://api.messari.io/news/v1/news/feed?limit=20" \
  -H "x-messari-api-key: $MESSARI_API_KEY"
```

## 路由指南

- **通用加密货币问题**：首先通过 **AI** 端点查询，以获取最全面的信息，该端点会整合市场数据、研究报告和新闻内容。
- **定量分析**：使用 **Metrics** 端点查询价格、交易量和基本数据；使用 **Exchanges** 端点查询交易所级别的数据；使用 **Networks** 端点查询第一/第二层网络指标；使用 **Protocols** 端点查询DeFi相关数据。
- **市场情绪与趋势分析**：使用 **Signal** 端点获取市场情绪和趋势分析；使用 **Topics** 端点获取热门话题信息；使用 **X-Users** 端点获取影响者级别的数据。
- **特定资产类别**：使用 **Stablecoins** 端点查询稳定币的供应量和流动情况；使用 **Token Unlocks** 端点查询代币的解锁计划。
- **研究报告与新闻**：使用 **Research** 端点获取深入分析和报告；使用 **News** 端点获取实时事件；使用 **Intel** 端点获取治理信息和协议更新；使用 **Fundraising** 端点获取融资轮次和并购动态。
- **多服务联合查询**：结合多个服务以获得更全面的信息。例如：“SOL是否被高估了？”：
  1. 使用 **Metrics** 端点查询当前价格、交易量和基本数据；
  2. 使用 **Signal** 端点查询市场情绪和趋势；
  3. 使用 **Token Unlocks** 端点查询即将到来的供应压力；
  4. 使用 **AI** 端点整合所有数据生成综合分析结果。