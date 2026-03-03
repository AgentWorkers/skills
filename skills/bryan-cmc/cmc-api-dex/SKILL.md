---
name: cmc-api-dex
description: >
  **CoinMarketCap DEX API参考**  
  本文档提供了CoinMarketCap（CMC）去中心化交易所（DEX）相关API的详细说明，涵盖以下功能：  
  - **代币查询**  
  - **流动性池信息**  
  - **交易记录**  
  - **热门代币榜单**  
  - **安全分析**  
  请在以下场景中使用本文档：  
  - 当用户提及DEX API时  
  - 当用户需要查询链上代币数据时  
  - 当用户希望根据合约地址查找代币信息时  
  - 当用户需要进行代币的安全性或风险评估时  
  - 当用户正在开发DEX集成时  
  **相关关键词**：  
  - DEX API  
  - 根据合约地址查询代币  
  - CMC安全API  
  - 流动性池API  
  - `/cmc-api-dex`  
  **使用说明**：  
  - 本文档为CMC DEX API的官方参考资料，涵盖了所有核心功能的详细实现细节。  
  - 请确保在开发或使用相关功能时遵循文档中的规范和限制。  
  **触发词**：  
  - “DEX API”  
  - “根据合约地址查询代币”  
  - “CMC安全API”  
  - “流动性池API”  
  - “/cmc-api-dex”
user-invocable: true
requires-credentials:
  - name: X-CMC_PRO_API_KEY
    description: CoinMarketCap Pro API key for REST API access
    obtain-from: https://pro.coinmarketcap.com/login
    storage: User provides in API request headers
allowed-tools:
  - Bash
  - Read
---
# CoinMarketCap DEX API

本文档介绍了CoinMarketCap的DEX（去中心化交易所）API，用于获取链上代币的相关数据。与CEX（中心化交易所）的接口不同，这些API直接从Uniswap、PancakeSwap、Raydium等区块链DEX获取数据。

## 认证

所有请求都必须在请求头中包含API密钥：

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/platform/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

您可以在以下链接获取API密钥：https://pro.coinmarketcap.com/login

## 基本URL

```
https://pro-api.coinmarketcap.com
```

## POST与GET接口

许多DEX接口使用POST方法来处理带有参数的复杂请求。请务必检查请求方法：
- GET接口通过查询字符串传递参数。
- POST接口需要将参数以JSON格式放在请求体中，并设置`Content-Type: application/json`。

## 常见用例

请参考[use-cases.md](references/use-cases.md)，了解根据具体需求选择合适接口的指导：
1. 通过合约地址获取代币价格。
2. 通过代币名称查找其合约地址。
3. 同时获取多个代币的价格。
4. 在交易前检查代币的安全性。
5. 查找某个代币的流动性池。
6. 查找热门的DEX代币。
7. 查找当日表现最佳的DEX代币。
8. 查找新推出的代币。
9. 检测潜在的“羊毛拔毛”行为（即流动性突然减少的情况）。
10. 获取某个代币的最新交易记录。
11. 获取支持的区块链网络和DEX。
12. 获取表情包代币（meme coins）。

## API概述

| 接口 | 方法 | 描述 | 参考文档 |
|----------|--------|-------------|-----------|
| /v1/dex/token | GET | 根据平台/地址获取代币详情 | [tokens.md](references/tokens.md) |
| /v1/dex/token/price | GET | 获取代币的最新DEX价格 | [tokens.md](references/tokens.md) |
| /v1/dex/token/price/batch | POST | 批量获取代币价格 | [tokens.md](references/tokens.md) |
| /v1/dex/token/pools | GET | 查找某个代币的流动性池 | [tokens.md](references/tokens.md) |
| /v1/dex/token-liquidity/query | GET | 查看代币的流动性变化历史 | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/batch-query | POST | 批量获取代币元数据 | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/transactions | GET | 获取代币的最新交易记录 | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/trending/list | POST | 获取热门的DEX代币列表 | [tokens.md](references/tokens.md) |
| /v4/dex/pairs/quotes/latest | GET | 获取最新的DEX交易对报价 | [pairs.md](references/pairs.md) |
| /v4/dex/spot-pairs/latest | GET | 获取DEX的现货交易对列表 | [pairs.md](references/pairs.md) |
| /v1/dex/platform/list | GET | 获取支持的DEX平台列表 | [platforms.md](references/platforms.md) |
| /v1/dex/platform/detail | GET | 获取平台详情 | [platforms.md](references/platforms.md) |
| /v1/dex/search | GET | 搜索DEX代币/交易对 | [platforms.md](references/platforms.md) |
| /v1/dex/gainer-loser/list | POST | 获取表现最佳的DEX代币（盈利/亏损情况） | [discovery.md](references/discovery.md) |
| /v1/dex/liquidity-change/list | GET | 查找流动性发生变化的代币 | [discovery.md](references/discovery.md) |
| /v1/dex/meme/list | POST | 查找DEX上的表情包代币 | [discovery.md](references/discovery.md) |
| /v1/dex/new/list | POST | 查找新发现的DEX代币 | [discovery.md](references/discovery.md) |
| /v1/dex/security/detail | GET | 获取代币的安全性/风险信息 | [security.md](references/security.md) |

## 常见工作流程

### 获取DEX代币信息
1. 搜索代币：`/v1/dex/search?keyword=PEPE`
2. 获取代币详情：`/v1/dex/token?network_slug=ethereum&contract_address=0x...`
3. 检查代币的安全风险：`/v1/dex/security/detail?network_slug=ethereum&contract_address=0x...`

### 分析代币流动性
1. 获取代币的流动性池：`/v1/dex/token/pools?network_slug=ethereum&contract_address=0x...`
2. 查看代币的流动性历史：`/v1/dex/token-liquidity/query?network_slug=ethereum&contract_address=0x...`

### 查找热门代币
1. 获取热门代币列表：`POST /v1/dex/tokens/trending/list` 并设置相应过滤条件。
2. 获取盈利/亏损代币列表：`POST /v1/dex/gainer-loser/list`
3. 查找新推出的代币：`POST /v1/dex/new/list`

### 监控DEX活动
1. 获取代币的最新交易记录：`/v1/dex/tokens/transactions?network_slug=ethereum&contract_address=0x...`
2. 获取交易对报价：`/v4/dex/pairs/quotes/latest?network_slug=ethereum&contract_address=0x...`

## 关键参数

大多数DEX接口需要以下参数：
- `network_slug` 或 `platform_crypto_id`：用于标识区块链（如ethereum、solana、bsc）。
- `contract_address`：代币的链上合约地址。

请使用`/v1/dex/platform/list`获取有效的区块链名称和平台ID。

## 错误处理

| 错误代码 | 含义 |
|------|---------|
| 400 | 请求无效（参数错误） |
| 401 | 未经授权（API密钥无效或缺失） |
| 403 | 禁止访问（请求的接口不在您的使用范围内） |
| 429 | 超过请求频率限制 |
| 500 | 服务器错误 |

错误响应示例：

```json
{
  "status": {
    "error_code": 400,
    "error_message": "Invalid value for 'contract_address'"
  }
}
```

## 请求频率限制

请求频率限制取决于您的API使用计划。请查看响应头中的以下字段：
- `X-CMC_PRO_API_KEY_CREDITS_REMAINING`：剩余的API使用次数。
- `X-CMC_PRO_API_KEY_CREDITS_RESET`：API密钥重置的时间戳。

## 响应格式

所有响应都遵循以下格式：

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