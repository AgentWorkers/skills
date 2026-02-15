---
name: hyperliquid
version: 1.1.0
description: 通过 ClawdBot API 查询 Hyperliquid DEX 的账户余额、持仓、盈亏（PnL）和保证金数据
author: ClawdBot
category: finance
tags:
  - defi
  - trading
  - perpetuals
  - hyperliquid
  - crypto
  - portfolio
  - positions
  - margin-trading
  - dex
  - derivatives
env:
  - name: TRADING_WALLET_ADDRESS
    description: Default wallet address to query (0x format)
    required: false
keywords:
  - hyperliquid account
  - perp positions
  - unrealized pnl
  - margin usage
  - liquidation price
  - cross margin
  - leverage trading
triggers:
  - hyperliquid
  - my perp positions
  - hyperliquid balance
  - check my HL account
  - show positions on hyperliquid
---

# Hyperliquid DEX 集成

您可以查询 Hyperliquid 永续合约账户的实时余额、未平仓头寸、未实现盈亏（PnL）以及保证金数据。

## ClawdBot 集成

此功能专为 **ClawdBot** 设计，它通过调用 ClawdBot 的内部 API 服务器来向官方 Hyperliquid API（地址：`https://api.hyperliquid.xyz`）发送请求。

**架构：**
```
User → ClawdBot Gateway → ClawdBot API Server → Hyperliquid Public API
                         (Railway)              (api.hyperliquid.xyz)
```

ClawdBot API 服务器负责以下任务：
- 超时保护（15 秒）
- 响应解析与格式化
- 从环境变量中获取默认钱包地址

## 功能特性

- **账户概览**：获取账户总价值、可用抵押品以及保证金使用情况
- **头寸跟踪**：查看所有未平仓的永久合约头寸，包括合约规模、方向和入场价格
- **盈亏监控**：实时显示每个头寸的未实现盈亏及资产回报率
- **风险管理**：提供每个头寸的清算价格和杠杆信息
- **多钱包支持**：可以查询任意钱包地址，或使用配置的交易钱包

## 环境变量

| 变量          | 是否必填 | 说明                          |
|---------------|---------|-------------------------------------------|
| `TRADING_WALLET_ADDRESS` | 否      | 未提供时使用的默认钱包地址（0x 格式）               |

## API 端点

**ClawdBot 内部 API：**
```
POST {CLAWDBOT_API_URL}/api/hyperliquid/account
```

**上游 API（由 ClawdBot 调用）：**
```
POST https://api.hyperliquid.xyz/info
```

### 请求（可选请求体）

```json
{
  "walletAddress": "0x..."
}
```

如果未提供钱包地址，系统将使用环境变量 `TRADING_WALLET_ADDRESS`。

### 响应

```json
{
  "timestamp": "2026-02-10T03:30:00.000Z",
  "walletAddress": "0x...",
  "account": {
    "accountValue": 10523.45,
    "totalPositionNotional": 25000.00,
    "freeCollateral": 5200.00,
    "totalMarginUsed": 5323.45
  },
  "positions": [
    {
      "coin": "ETH",
      "direction": "long",
      "size": 2.5,
      "entryPrice": 2450.00,
      "positionValue": 6250.00,
      "unrealizedPnl": 125.50,
      "returnOnEquity": 0.024,
      "leverage": { "type": "cross", "value": 5 },
      "liquidationPrice": 1850.00,
      "marginUsed": 1250.00
    }
  ],
  "positionCount": 1
}
```

## 安全注意事项

- **仅读权限**：此功能仅用于读取账户数据，不支持交易或签名操作
- **公共 API**：使用 Hyperliquid 的公共信息 API，无需身份验证
- **不涉及私钥**：仅使用钱包地址（公开信息）
- **超时保护**：设置 15 秒的超时机制以防止请求挂起

## 使用示例

### 检查账户余额
```
"What's my Hyperliquid balance?"
"Show my HL account value"
```

### 查看头寸
```
"What positions do I have open on Hyperliquid?"
"Am I in profit on my perps?"
"What's my unrealized PnL?"
```

### 风险评估
```
"What are my liquidation prices on Hyperliquid?"
"How much margin am I using?"
"What leverage am I running?"
```

## 相关资源

- [Hyperliquid 文档](https://hyperliquid.gitbook.io/hyperliquid-docs)
- `ichimoku`：Ichimoku 云交易信号工具
- `wallet-tracker`：跨链监控钱包余额的工具
- `crypto-tracker`：跟踪加密货币价格和投资组合的工具