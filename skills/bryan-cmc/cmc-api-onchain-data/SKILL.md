---
name: cmc-api-dex
description: >
  **CoinMarketCap DEX API参考**  
  本文档提供了CoinMarketCap（CMC）DEX（去中心化交易所）相关端点的API参考，涵盖了token查询、流动性池管理、交易记录、市场趋势分析以及安全性评估等功能。  
  **适用场景**：  
  - 当用户提及DEX API时  
  - 当用户需要查询链上token的数据时  
  - 当用户希望根据合约地址查找特定token时  
  - 当用户需要进行token的安全性或风险评估时  
  - 当用户正在开发DEX集成时  
  **主要功能**：  
  - **Token查询**：允许用户根据token名称或合约地址获取相关信息。  
  - **流动性池管理**：提供关于token在各个流动性池中的分布情况。  
  - **交易记录**：展示token的交易历史和交易量。  
  - **市场趋势分析**：提供token的市场表现数据（如价格、交易量等）。  
  - **安全性评估**：提供token的安全性相关指标（如交易活跃度、风险等级等）。  
  **相关关键词**：  
  - DEX API  
  - token by contract address  
  - CMC security API  
  - liquidity pool API  
  - /cmc-api-dex  
  **使用提示**：  
  请在需要使用这些API功能时参考本文档，以确保正确地调用相应的接口并处理返回的数据。
user-invocable: true
allowed-tools:
  - Bash
  - Read
---
# CoinMarketCap DEX API

本文档介绍了 CoinMarketCap 的去中心化交易所（DEX）API，用于获取链上代币的相关数据。与中心化交易所（CEX）的接口不同，这些 API 直接从 Uniswap、PancakeSwap、Raydium 等区块链 DEX 中获取数据。

## 认证

所有请求都必须在请求头中包含 API 密钥：

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/platform/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

您可以在以下链接获取 API 密钥：https://pro.coinmarketcap.com/login

## 基本 URL

```
https://pro-api.coinmarketcap.com
```

## POST 与 GET 请求方式

许多 DEX 接口使用 POST 方法来处理带有请求体参数的复杂查询。请务必检查请求方法：
- GET 请求将参数作为查询字符串传递。
- POST 请求需要将参数以 JSON 格式放在请求体中，并设置 `Content-Type: application/json`。

## 常见使用场景

请参阅 [use-cases.md](references/use-cases.md)，以了解根据具体需求选择相应接口的指导：
1. 通过合约地址获取 DEX 代币价格。
2. 通过代币名称查找其合约地址。
3. 同时获取多个代币的价格。
4. 在交易前检查代币的安全性。
5. 查找代币的流动性池。
6. 查找热门的 DEX 代币。
7. 查找当日表现最佳的 DEX 代币。
8. 查找新推出的代币。
9. 检测潜在的“拉盘”行为（即突然减少流动性）。
10. 获取代币的最新交易记录。
11. 获取支持的区块链网络及 DEX。
12. 获取表情包代币（meme coins）。

## API 概述

| 接口 | 方法 | 描述 | 参考文档 |
|----------|--------|-------------|-----------|
| /v1/dex/token | GET | 根据平台/地址获取代币详情 | [tokens.md](references/tokens.md) |
| /v1/dex/token/price | GET | 获取代币的最新 DEX 价格 | [tokens.md](references/tokens.md) |
| /v1/dex/token/price/batch | POST | 批量获取代币价格 | [tokens.md](references/tokens.md) |
| /v1/dex/token/pools | GET | 获取代币的流动性池信息 | [tokens.md](references/tokens.md) |
| /v1/dex/token-liquidity/query | GET | 查看代币的流动性变化历史 | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/batch-query | POST | 批量获取代币元数据 | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/transactions | GET | 获取代币的最新交易记录 | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/trending/list | POST | 获取热门的 DEX 代币列表 | [tokens.md](references/tokens.md) |
| /v4/dex/pairs/quotes/latest | GET | 获取最新的 DEX 对交易报价 | [pairs.md](references/pairs.md) |
| /v4/dex/spot-pairs/latest | GET | 获取 DEX 现货交易对列表 | [pairs.md](references/pairs.md) |
| /v1/dex/platform/list | GET | 获取支持的 DEX 平台列表 | [platforms.md](references/platforms.md) |
| /v1/dex/platform/detail | GET | 获取平台详情 | [platforms.md](references/platforms.md) |
| /v1/dex/search | GET | 搜索 DEX 代币/交易对 | [platforms.md](references/platforms.md) |
| /v1/dex/gainer-loser/list | POST | 获取表现最佳的 DEX 代币（盈利/亏损情况） | [discovery.md](references/discovery.md) |
| /v1/dex/liquidity-change/list | GET | 获取流动性发生变化的代币 | [discovery.md](references/discovery.md) |
| /v1/dex/meme/list | POST | 获取 DEX 上的表情包代币信息 | [discovery.md](references/discovery.md) |
| /v1/dex/new/list | POST | 获取新发现的 DEX 代币信息 | [discovery.md](references/discovery.md) |
| /v1/dex/security/detail | GET | 获取代币的安全性/风险信号 | [security.md](references/security.md) |

## 常见工作流程

### 获取 DEX 代币信息
1. 搜索代币：`/v1/dex/search?keyword=PEPE`
2. 获取代币详情：`/v1/dex/token?network_slug=ethereum&contract_address=0x...`
3. 检查代币的安全风险：`/v1/dex/security/detail?network_slug=ethereum&contract_address=0x...`

### 分析代币流动性
1. 获取代币的流动性池信息：`/v1/dex/token/pools?network_slug=ethereum&contract_address=0x...`
2. 查看代币的流动性历史：`/v1/dex/token-liquidity/query?network_slug=ethereum&contract_address=0x...`

### 查找热门代币
1. 获取热门代币：`POST /v1/dex/tokens/trending/list` 并设置相关过滤条件。
2. 获取表现最佳的/最差的代币：`POST /v1/dex/gainer-loser/list`
3. 查找新推出的代币：`POST /v1/dex/new/list`

### 监控 DEX 活动
1. 获取代币的最新交易记录：`/v1/dex/tokens/transactions?network_slug=ethereum&contract_address=0x...`
2. 获取交易对报价：`/v4/dex/pairs/quotes/latest?network_slug=ethereum&contract_address=0x...`

## 关键参数

大多数 DEX 接口需要以下参数：
- `network_slug` 或 `platform_crypto_id`：用于标识区块链（如 Ethereum、Solana、BSC）。
- `contract_address`：代币的链上合约地址。

请使用 `/v1/dex/platform/list` 获取有效的区块链名称和平台 ID。

## 错误处理

| 错误代码 | 含义 |
|------|---------|
| 400 | 请求无效（参数错误） |
| 401 | 未经授权（API 密钥无效或缺失） |
| 403 | 禁止访问（请求的接口不在您的使用计划内） |
| 429 | 超过请求频率限制 |
| 500 | 服务器错误 |

示例错误响应：

```json
{
  "status": {
    "error_code": 400,
    "error_message": "Invalid value for 'contract_address'"
  }
}
```

## 请求频率限制

请求频率限制取决于您的 API 计划。请查看响应头中的以下字段：
- `X-CMC_PRO_API_KEY_CREDITS_REMAINING`：剩余的 API 信用额度。
- `X-CMC_PRO_API_KEY_CREDITS_RESET`：信用额度重置时间。

## 响应格式

所有响应均遵循以下格式：

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null
  },
  "data": { ... }
}
```