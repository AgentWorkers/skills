---
name: priceforagent
description: 获取加密货币、股票和商品的实时价格。当用户询问资产价格、市场数据，或需要查看比特币、以太坊、股票（如NVDA/AAPL）或商品（如黄金/白银）的价值时，可以使用该功能。支持自然语言查询（例如：“比特币的价格是多少？”）以及直接查询。
---

# 代理服务价格

我们提供适用于大语言模型（LLM）的加密货币、股票和商品价格查询服务。

**基础URL：** `https://p4ai.bitharga.com`

## 快速入门

### 1. 注册API密钥

```bash
curl -X POST https://p4ai.bitharga.com/v1/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent"}'
```

**响应：**
```json
{"api_key": "pfa_xxx...", "message": "API key generated successfully"}
```

### 2. 查询价格

**自然语言查询：**
```bash
curl -X POST https://p4ai.bitharga.com/v1/query \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of Bitcoin and Ethereum?"}'
```

**直接查询：**
```bash
curl -H "X-API-Key: YOUR_KEY" https://p4ai.bitharga.com/v1/price/bitcoin
```

**批量查询：**
```bash
curl -X POST https://p4ai.bitharga.com/v1/batch \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pairs": ["BTC", "ETH", "NVDA"]}'
```

## 支持的资产

| 类型 | 示例 |
|------|----------|
| 加密货币 | BTC, ETH, SOL, DOGE, XRP, BNB |
| 股票 | NVDA, AAPL, TSLA, GOOGL |
| 商品 | GOLD, SILVER, OIL |

## 速率限制

- 每个API密钥每秒最多2次请求
- 全局请求限制：1000万次
- 使用情况可通过 `/v1/usage` 查看

## 函数调用

```bash
curl https://p4ai.bitharga.com/v1/function-schema
```

## OpenAPI规范

```bash
curl https://p4ai.bitharga.com/v1/openapi.yaml
```

## 响应格式

```json
{
  "pair": "BTC",
  "price": 70494.63,
  "ask": 70565.13,
  "bid": 70424.14,
  "currency": "USDT",
  "market": "open",
  "timestamp": 1770433814
}
```