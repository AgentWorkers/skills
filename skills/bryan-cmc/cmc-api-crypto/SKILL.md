---
name: cmc-api-crypto
description: >
  **CoinMarketCap加密货币API参考**  
  本文档提供了CoinMarketCap（CMC）提供的各种加密货币相关端点的详细信息，包括价格报价、市场列表、历史价格数据（OHLCV）、市场趋势数据以及加密货币分类等。  
  **适用场景：**  
  - 当用户提及“CMC API”时  
  - 当用户询问如何通过编程方式获取加密货币数据时  
  - 当用户希望构建与加密货币价格相关的应用程序时  
  - 当用户需要了解CMC提供的REST API的详细信息时  
  **主要功能：**  
  - 获取实时加密货币价格  
  - 查看加密货币的市场列表  
  - 查看加密货币的历史价格数据（Open outcry, High, Low, Close）  
  - 分析加密货币的市场趋势  
  - 筛选和查询特定类别的加密货币  
  **使用建议：**  
  - 在需要获取加密货币数据或开发相关应用程序时，请参考本文档。  
  - 本文档是解答所有关于CMC加密货币API问题的权威参考资料。  
  **触发词：**  
  - CMC API  
  - coinmarketcap api  
  - crypto price API  
  - get bitcoin price via API  
  - /cmc-api-crypto
homepage: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
source: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
user-invocable: true
allowed-tools:
  - Bash
  - Read
---
# CoinMarketCap加密货币API

本技能涵盖了CoinMarketCap的加密货币API端点，用于检索价格数据、市场列表、历史报价、热门加密货币以及代币元数据。

## 认证

所有请求都需要在请求头中包含API密钥。

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

您可以在以下链接获取API密钥：https://pro.coinmarketcap.com/login

## 基础URL

```
https://pro-api.coinmarketcap.com
```

## 常见用例

请参阅[use-cases.md](references/use-cases.md)，以获取关于使用哪个端点的指导：

1. 获取代币的当前价格
2. 通过符号或名称查找代币的CMC ID
3. 通过合约地址获取代币信息
4. 获取市值排名前100的加密货币
5. 查找价格范围内的加密货币
6. 获取特定日期的历史价格
7. 绘制价格图表（OHLCV数据）
8. 查找加密货币的交易平台
9. 获取历史最高价及距离最高价（ATH）的距离
10. 查找今日涨幅最大的加密货币
11. 发现新上市的加密货币
12. 获取某个类别（例如DeFi）中的所有代币

## API概述

| 端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v1/cryptocurrency/categories | 列出所有带有市场指标的类别 | [categories.md](references/categories.md) |
| GET /v1/cryptocurrency/category | 单个类别详情 | [categories.md](references/categories.md) |
| GET /v1/cryptocurrency/listings/historical | 历史交易记录快照 | [listings.md](references/listings.md) |
| GET /v1/cryptocurrency/listings/latest | 带有市场数据的当前交易记录 | [listings.md](references/listings.md) |
| GET /v1/cryptocurrency/listings/new | 新添加的加密货币 | [listings.md](references/listings.md) |
| GET /v1/cryptocurrency/map | 将名称/符号映射到CMC ID | [map.md](references/map.md) |
| GET /v1/cryptocurrency/trending/gainers-losers | 表现最佳的加密货币（涨幅/跌幅最大的） | [trending.md](references/trending.md) |
| GET /v1/cryptocurrency/trending/latest | 当前热门的加密货币 | [trending.md](references/trending.md) |
| GET /v1/cryptocurrency/trending/most-visited | 在CMC上访问量最大的加密货币 | [trending.md](references/trending.md) |
| GET /v2/cryptocurrency/info | 静态元数据（徽标、描述、URL） | [info.md](references/info.md) |
| GET /v2/cryptocurrency/market-pairs/latest | 某种加密货币的交易对 | [market-pairs.md](references/market-pairs.md) |
| GET /v2/cryptocurrency/ohlcv/historical | 历史OHLCV数据 | [ohlcv.md](references/ohlcv.md) |
| GET /v2/cryptocurrency/ohlcv/latest | 最新的OHLCV数据 | [ohlcv.md](references/ohlcv.md) |
| GET /v2/cryptocurrency/price-performance-stats/latest | 价格表现统计 | [price-performance.md](references/price-performance.md) |
| GET /v2/cryptocurrency/quotes/latest | 最新价格报价 | [quotes.md](references/quotes.md) |
| GET /v3/cryptocurrency/quotes/historical | 历史价格报价 | [quotes.md](references/quotes.md) |

## 常见工作流程

### 通过符号获取代币价格

1. 首先使用 `/v1/cryptocurrency/map` 将符号映射到CMC ID。
2. 然后使用 `/v2/cryptocurrency/quotes/latest` 获取价格。

```bash
# Step 1: Get CMC ID for ETH
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?symbol=ETH" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Step 2: Get price quote (using id=1027 for ETH)
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?id=1027" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### 获取市值排名前100的加密货币

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=100&sort=market_cap" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### 获取历史价格数据

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/cryptocurrency/quotes/historical?id=1&time_start=2024-01-01&time_end=2024-01-31&interval=daily" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### 获取代币元数据

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?id=1,1027" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

## 错误处理

### HTTP状态码

| 代码 | 含义 |
|------|---------|
| 200 | 成功 |
| 400 | 请求错误（参数无效） |
| 401 | 未经授权（API密钥无效） |
| 403 | 禁止访问（您的订阅计划中不支持该端点） |
| 429 | 超过请求限制 |
| 500 | 服务器错误 |

## 请求限制

请求限制取决于您的订阅计划。响应头中包含以下信息：

1. `X-CMC_PRO_API_KEY_CREDITS_used` – 本次请求使用的信用额度 |
2. `X-CMC_PRO_API_KEY_CREDITS_LEFT` – 剩余的信用额度 |

## 常见错误

- **无效ID**：确保使用来自 `/map` 端点的有效CMC ID。符号查询可能返回多个匹配结果。
- **缺少必需参数**：某些端点至少需要一个标识符（id、slug或symbol）。
- **计划限制**：历史数据端点及某些功能需要付费订阅。请检查您的订阅计划限制。

## 错误响应格式

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 400,
    "error_message": "Invalid value for 'id'",
    "credit_count": 0
  }
}
```

## 响应格式

所有响应都遵循以下结构：

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": { ... }
}
```

## 参考文档

请参阅`references/`目录，以获取每个端点的完整参数和响应文档。