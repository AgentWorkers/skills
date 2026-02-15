---
name: Whistle RPC
slug: whistle-rpc
version: 1.0.4
description: 用于AI代理的生产级Solana RPC服务：支持无限量的JSON-RPC和WebSocket请求。费用为每月1 SOL，通过链上支付方式结算。该服务无速率限制，也不存在费用等级之分。
author: DylanPort
homepage: https://whistle.ninja
repository: https://github.com/nickneedsaname/whistle-rpc
tags: solana, rpc, blockchain, web3, defi, agent, infrastructure, websocket, dex, trading
---

# Whistle RPC — 专为AI代理设计的Solana基础设施

Whistle RPC提供无限量的JSON-RPC、WebSocket、DEX数据以及历史API接口，专为需要可靠区块链访问的AI代理而设计。

## 服务

| 服务 | URL | 功能 |
|---------|-----|-------------|
| **RPC** | `https://rpc.whistle.ninja` | 所有Solana JSON-RPC 2.0方法 |
| **WebSocket** | `wss://rpc.whistle.ninja/ws` | 实时数据订阅（如插槽信息、账户信息、日志等） |
| **DEX API** | `https://dex.whistle.ninja/v1` | 流行代币信息、交易记录、持有者信息、交易量 |
| **历史数据** | `https://rpc.whistle.ninja/v1` | 详细交易及转账历史记录 |
| **代理API** | `https://api.whistle.ninja` | 订阅管理功能 |

## 认证

所有接口均需要通过订阅获得的API密钥进行访问：

```
Query param:  https://rpc.whistle.ninja?api_key=YOUR_KEY
Header:       X-API-Key: YOUR_KEY
Header:       Authorization: Bearer YOUR_KEY
```

## 支持的RPC方法

所有标准的Solana JSON-RPC 2.0方法：

- **账户**：`getBalance`, `getAccountInfo`, `getMultipleAccounts`, `getTokenAccountsByOwner`, `getMinimumBalanceForRentExemption`
- **区块**：`getSlot`, `getBlockHeight`, `getBlock`, `getEpochInfo`, `getRecentPerformanceSamples`
- **交易**：`sendTransaction`, `simulateTransaction`, `getTransaction`, `getSignaturesForAddress`, `getLatestBlockhash`
- **节点**：`getHealth`, `getVersion`

## WebSocket订阅

- `slotSubscribe`, `accountSubscribe`, `programSubscribe`, `signatureSubscribe`, `logsSubscribe`

示例：

使用您的API密钥作为查询参数，连接到 `wss://rpc.whistle.ninja/ws`。

## DEX与市场数据

基础URL：`https://dex.whistle.ninja/v1`

## 历史数据

基础URL：`https://rpc.whistle.ninja`

## 订阅流程（REST API）

订阅费用为每月1 SOL，通过链上支付。整个流程包括三次HTTP请求和一次Solana转账。

> **重要提示：** 支付步骤需要在主网上实际发送Solana代币。代理在签署任何交易前必须获得人工操作员的明确批准，显示确切的金额和收款人信息，并使用专用低价值钱包进行支付。

### 1. 请求报价

响应格式：`{"nonce": "...", "amount": 1, "recipient": "...", "duration": 30}`

### 2. 在链上支付

使用标准的Solana `SystemProgram.transfer`将`amount` SOL代币转移到`recipient`地址。代理在签署交易前必须与用户确认金额和收款人信息。

### 3. 激活订阅

响应格式：`{"apiKey": "...", "expiresAt": "...", "rpcUrl": "...", "wsUrl": "..."}`

### 检查订阅状态

响应格式：`{"active": true, "daysLeft": 29, "renewalNeeded": false}`

### 续订

当`renewalNeeded`为`true`时，重复订阅 → 支付 → 激活的流程。续订前务必与用户确认。

## 价格

每月1 SOL，包含所有服务内容，无等级限制，无速率限制。收入将分配给WHISTLE的质押者和节点运营商。

## 链接

- 网站：https://whistle.ninja
- NPM CLI：https://npmjs.com/package/whistle-rpc
- 工具清单：https://whistle.ninja/tools.json