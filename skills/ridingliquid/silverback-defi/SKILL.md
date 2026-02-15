---
name: silverback-defi
description: 由 Silverback 提供支持的 DeFi 智能服务——在 Base 链上拥有 19 个 x402 端点。提供市场数据、交易报价、技术分析、收益机会、代币审计、大户追踪以及 AI 对话功能。使用 USDC 进行按次付费。
homepage: https://silverbackdefi.app
user-invocable: true
disable-model-invocation: true
metadata: {"clawdbot":{"requires":{"bins":["curl","jq"]},"emoji":"🦍","category":"Finance & Crypto","tags":["defi","trading","crypto","yield","swap","analysis","base-chain","x402"]}}
---

# Silverback DeFi Intelligence

在 Base 链上提供了 19 个基于 x402 协议的 DeFi 服务端点。所有服务端点均支持通过 USDC 进行按次付费，无需 API 密钥或订阅。这些服务端点均使用 x402 微支付协议。

基础 URL：`https://x402.silverbackdefi.app`

## 服务端点

### 聊天 ($0.05)
支持与所有 19 个智能工具进行 AI 对话，可以随时询问关于 DeFi 的任何问题。

```bash
curl -s -X POST https://x402.silverbackdefi.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the top coins right now?"}'
```

### 市场数据 ($0.001/次)
提供实时市场数据。

```bash
# Top coins by market cap
curl -s -X POST https://x402.silverbackdefi.app/api/v1/top-coins \
  -H "Content-Type: application/json" -d '{}'

# Top liquidity pools on Base
curl -s -X POST https://x402.silverbackdefi.app/api/v1/top-pools \
  -H "Content-Type: application/json" -d '{}'

# Top DeFi protocols by TVL
curl -s -X POST https://x402.silverbackdefi.app/api/v1/top-protocols \
  -H "Content-Type: application/json" -d '{}'

# Trending tokens
curl -s -X POST https://x402.silverbackdefi.app/api/v1/trending-tokens \
  -H "Content-Type: application/json" -d '{}'

# Base gas prices
curl -s -X POST https://x402.silverbackdefi.app/api/v1/gas-price \
  -H "Content-Type: application/json" -d '{}'

# Token details
curl -s -X POST https://x402.silverbackdefi.app/api/v1/token-metadata \
  -H "Content-Type: application/json" -d '{"token": "ETH"}'
```

### 交易与分析
提供详细的交易和分析功能。

```bash
# Swap quote with routing ($0.002)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/swap-quote \
  -H "Content-Type: application/json" \
  -d '{"fromToken": "ETH", "toToken": "USDC", "amount": "1"}'

# Technical analysis — RSI, MACD, Bollinger ($0.02)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/technical-analysis \
  -H "Content-Type: application/json" \
  -d '{"token": "ETH"}'

# Backtest a strategy ($0.10)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/backtest \
  -H "Content-Type: application/json" \
  -d '{"token": "ETH", "strategy": "rsi", "days": 30}'

# Token correlation matrix ($0.005)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/correlation-matrix \
  -H "Content-Type: application/json" \
  -d '{"tokens": ["ETH", "BTC", "VIRTUAL"]}'
```

### 收益与 DeFi 产品
帮助用户了解 DeFi 产品的收益情况。

```bash
# Yield opportunities ($0.02)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/defi-yield \
  -H "Content-Type: application/json" \
  -d '{"token": "USDC"}'

# Pool health analysis ($0.005)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/pool-analysis \
  -H "Content-Type: application/json" \
  -d '{"pool": "ETH/USDC"}'
```

### 安全性与情报分析
提供有关 DeFi 系统安全性的分析报告。

```bash
# Token contract audit ($0.01)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/token-audit \
  -H "Content-Type: application/json" \
  -d '{"token": "0x558881c4959e9cf961a7E1815FCD6586906babd2"}'

# Whale movement tracking ($0.01)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/whale-moves \
  -H "Content-Type: application/json" \
  -d '{"token": "VIRTUAL"}'

# Arbitrage scanner ($0.005)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/arbitrage-scanner \
  -H "Content-Type: application/json" -d '{}'

# Agent reputation — ERC-8004 ($0.001)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/agent-reputation \
  -H "Content-Type: application/json" \
  -d '{"agentId": "13026"}'

# Discover agents by capability ($0.002)
curl -s -X POST https://x402.silverbackdefi.app/api/v1/agent-discover \
  -H "Content-Type: application/json" \
  -d '{"capability": "defi"}'
```

### 非托管式交易（$0.05）
提供未签名的 EIP-712 Permit2 数据，供客户端自行签名使用。

```bash
curl -s -X POST https://x402.silverbackdefi.app/api/v1/swap \
  -H "Content-Type: application/json" \
  -d '{"fromToken": "USDC", "toToken": "ETH", "amount": "10", "walletAddress": "0xYOUR_WALLET"}'
```

## 支付（x402 协议）
所有服务端点在响应时会返回 HTTP 402 错误码，并要求用户使用 USDC 进行支付。您可以使用 `@x402/fetch` 或任何兼容 x402 协议的客户端工具（及其自带的钱包）来完成支付。

服务费用范围为每次 $0.001 至 $0.10，具体费用会在响应中明确说明。

## 免费服务端点
部分服务端点提供免费使用。

```bash
# Health check
curl -s https://x402.silverbackdefi.app/api/v1/health

# Pricing info
curl -s https://x402.silverbackdefi.app/api/v1/pricing

# Endpoint list
curl -s https://x402.silverbackdefi.app/api/v1/endpoints
```

## MCP 服务器
适用于 Claude Desktop、Cursor 或 Claude Code 工具：

```bash
npm install -g silverback-x402-mcp
```
https://www.npmjs.com/package/silverback-x402-mcp

## 链接

- **官方网站**：https://silverbackdefi.app
- **x402 文档**：https://silverbackdefi.app/x402
- **API**：https://x402.silverbackdefi.app
- **源代码**：https://github.com/RidingLiquid/silverback-skill