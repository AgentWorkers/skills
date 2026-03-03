---
name: cmc-api-exchange
description: >
  CoinMarketCap（CMC）交易所端点的API参考，包括交易所信息、交易量、市场交易对以及资产数据。  
  每当用户提及交易所API、询问交易所交易量、需要交易对数据、要求查看储备金证明信息，或正在开发交易所集成时，请使用此文档作为权威参考。  
  相关关键词：`exchange API`、`CMC exchange data`、`trading pairs API`、`exchange volume API`、`/cmc-api-exchange`
homepage: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
source: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
user-invocable: true
allowed-tools:
  - Bash
  - Read
---
# CoinMarketCap交易所API技能

本技能涵盖了CoinMarketCap提供的API，用于查询中心化加密货币交易所（如Binance、Coinbase、Kraken等）的相关信息。通过这些API端点，您可以获取交易所的元数据、交易量、市场交易对以及交易所持有的资产信息。

## 认证

所有请求都需要在请求头中包含API密钥。

1. 请访问[https://pro.coinmarketcap.com/login]获取您的API密钥。
2. 在所有请求中添加请求头`X-CMC_PRO_API_KEY: your-api-key`。

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/map" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

## 基础URL

```
https://pro-api.coinmarketcap.com
```

## 常见用例

请参阅[use-cases.md](references/use-cases.md)，以获取关于使用哪个API端点的指导：

1. 通过交易所名称获取交易所信息。
2. 查找交易所的CMC ID。
3. 按交易量排序获取排名靠前的交易所。
4. 仅获取现货交易所（或仅获取衍生品交易所）的信息。
5. 获取特定交易所的当前交易量。
6. 比较多个交易所的交易量。
7. 获取交易所的历史交易量数据。
8. 获取交易所的所有交易对。
9. 查找交易所支持的BTC交易对。
10. 获取交易所支持的永续合约/期货交易对。
11. 检查交易所的储备情况（储备证明）。
12. 查找支持特定加密货币的交易所。

## API概述

| API端点 | 描述 | 参考文档 |
|----------|-------------|-----------|
| GET /v1/exchange/map | 将交易所名称转换为CMC ID | [references/info.md](references/info.md) |
| GET /v1/exchange/info | 交易所元数据（徽标、网址、描述） | [references/info.md](references/info.md) |
| GET /v1/exchange/listings/latest | 列出所有带有市场数据的交易所 | [references/listings.md](references/listings.md) |
| GET /v1/exchange/quotes/latest | 最新的交易所交易量和指标 | [references/quotes.md](references/quotes.md) |
| GET /v1/exchange/quotes/historical | 交易所的历史交易量数据 | [references/quotes.md](references/quotes.md) |
| GET /v1/exchange/market-pairs/latest | 交易所的交易对信息 | [references/market-pairs.md](references/market-pairs.md) |
| GET /v1/exchange/assets | 交易所持有的资产信息 | [references/assets.md](references/assets.md) |

## 常见工作流程

### 获取交易所信息

**原因：**大多数API端点需要使用CMC交易所的ID，而非名称。`/v1/exchange/map`端点可以将人类可读的交易所名称转换为ID。

1. 调用`/v1/exchange/map`并传入`slug=binance`以获取交易所ID。
2. 使用该ID调用`/v1/exchange/info`以获取完整的交易所元数据。

### 比较交易所交易量

**原因：**交易量反映了交易所的流动性和可靠性。交易量越大，价格执行越稳定，滑点越低。

1. 调用`/v1/exchange/listings/latest`以获取按交易量排序的所有交易所列表。
2. 使用`sort=volume_24h`和`sort_dir=desc`参数进行降序排序。

### 分析交易对

**原因：**了解可用的交易对有助于用户确定交易特定资产的位置，并比较不同交易所的流动性。

1. 从`/v1/exchange/map`获取交易所ID。
2. 使用该ID调用`/v1/exchange/market-pairs/latest`。
3. 根据需要使用`category=spot`或`category=derivatives`进行筛选。

### 跟踪交易量历史

**原因：**历史交易量数据可以揭示市场趋势。交易量下降可能表明用户流失，而交易量激增可能意味着洗盘行为或新闻事件的发生。

1. 从`/v1/exchange/map`获取交易所ID。
2. 使用日期范围参数调用`/v1/exchange/quotes/historical`。

## 查询参数

大多数API端点支持以下参数：

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| id | string | CMC交易所ID（多个ID用逗号分隔） |
| slug | string | 交易所名称（例如：“binance”） |
| convert | string | 价格转换的货币（默认：USD） |
| aux | string | 响应中需要包含的附加字段 |

## 错误处理

所有响应都会包含一个`status`对象：

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": { }
}
```

### 常见错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 请求成功 |
| 400 | 请求错误（参数无效） |
| 401 | 未经授权（API密钥无效） |
| 403 | 禁止访问（超出计划使用限制） |
| 429 | 超过请求频率限制 |
| 500 | 服务器内部错误 |

## 请求频率限制

请求频率限制取决于您的订阅计划。请通过响应中的`credit_count`字段来监控API信用使用情况。每个请求都必须包含`X-CMC_PRO_API_KEY`请求头。

## 响应格式

所有响应都以JSON格式返回，结构如下：

```json
{
  "status": { },
  "data": { }
}
```

`data`字段根据API端点的不同，可能包含一个对象（单个数据项）或一个数组（多个数据项）。