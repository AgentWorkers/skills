---
name: unified-dev-monitor-autobuy
description: 具有自动购买功能的统一开发监控工具，适用于 BSC 和 Solana 平台
version: "1.0.0"
author: Your Name
tags: [bsc, solana, monitor, trading, auto-buy, crypto, defi, multi-chain]
payment:
  provider: skillpay.me
  api_key: sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5
  price: 0.01
  currency: USDT
  billing_mode: per_call
---# 统一开发监控工具（含自动购买功能）

## 🎯 概述

这是一个针对 BSC 和 Solana 的全面开发钱包监控工具，具备自动购买功能。它可以监控来自开发者地址的代币转账，并通过 PancakeSwap（BSC）和 PumpSwap（Solana）自动购买新代币。

## 💰 价格

- **每次调用费用**：0.01 USDT
- **支付方式**：SkillPay.me
- **计费模式**：按每次调用计费

## 🚀 快速入门

### 安装

```bash
npm install
```

### 测试运行

```bash
# Test environment
npm test

# Test BSC monitoring with auto-buy disabled
node index.js test

# Test BSC monitoring with auto-buy enabled
AUTO_BUY_ENABLED="true" AUTO_BUY_AMOUNT="1" WALLET_PRIVATE_KEY="your-key" node index-bsc.js test

# Test Solana monitoring (use index-sol-safe.js)
node index-sol-safe.js test

# Test Solana monitoring with auto-buy enabled (use index-sol-safe.js)
AUTO_BUY_ENABLED="true" AUTO_BUY_AMOUNT="0.1" WALLET_PRIVATE_KEY="your-sol-key-base64" node index-sol-safe.js test
```

## 📊 支持的链

### 1. BSC（Binance Smart Chain）

- **原生代币**：BNB
- **去中心化交易所（DEX）**：PancakeSwap
- **支付代币**：USDT（0x55d398326f9955f0bEb）
- **路由器地址**：0x10ED43C718714eb63d5aA57B78B54704E256024E
- **区块确认时间**：约 3 秒
- **地址格式**：0x...（42 个十六进制字符）

### 2. Solana

- **原生代币**：SOL
- **去中心化交易所（DEX）**：PumpSwap
- **支付代币**：SOL（WSOL）
- **路由器地址**：自动检测
- **区块确认时间**：约 400 毫秒
- **地址格式**：Base58（32-44 个字符）

## 📖 使用方法

### 监控 BSC 并自动购买

```javascript
{
  "action": "monitor",
  "chain": "BSC",
  "address": "YourBSCDevAddress",
  "duration": 3600,
  "autoBuy": {
    "enabled": true,
    "amount": "10",
    "slippage": 5
  }
}
```

**响应（检测 + 自动购买）**：
```json
{
  "success": true,
  "chain": "BSC",
  "detected": true,
  "transaction": {
    "hash": "0x...",
    "blockNumber": 12345678,
    "timestamp": "2026-03-05T10:30:00Z",
    "from": "DevAddress",
    "to": "RecipientAddress",
    "tokenAddress": "0x...",
    "tokenSymbol": "PEPE",
    "tokenName": "Pepe Token",
    "amount": "1000000000000000000000000",
    "decimals": 18
  },
  "autoBuy": {
    "enabled": true,
    "success": true,
    "transactionHash": "0x...",
    "gasUsed": "0.005 BNB",
    "actualAmount": "10 USDT"
  }
}
```

### 监控 Solana 并自动购买

```javascript
{
  "action": "monitor",
  "chain": "SOL",
  "address": "YourSolanaDevAddress",
  "duration": 3600,
  "autoBuy": {
    "enabled": true,
    "amount": 0.1,
    "slippage": 5
  }
}
```

**响应（检测 + 自动购买）**：
```json
{
  "success": true,
  "chain": "SOL",
  "detected": true,
  "transaction": {
    "signature": "3h1y...",
    "slot": 12345678,
    "timestamp": "2026-03-05T10:30:00Z",
    "from": "DevAddress",
    "to": "RecipientAddress",
    "tokenMint": "TokenMintAddress...",
    "tokenSymbol": "TOKEN",
    "amount": "1000000",
    "decimals": 9
  },
  "autoBuy": {
    "enabled": true,
    "success": true,
    "transactionHash": "3h1y...",
    "feePaid": 0.001 SOL"
  }
}
```

## 🔧 配置

### 环境变量

```bash
# BSC RPC
export BSC_RPC="https://bsc-dataseed.binance.org"

# Solana RPC
export SOLANA_RPC="https://api.mainnet-beta.solana.com"
export SOLANA_RPC_API_KEY="your-api-key"

# Wallet Private Keys
export WALLET_PRIVATE_KEY="your-bsc-private-key"               # BSC
export WALLET_PRIVATE_KEY_BASE64="your-solana-key-base64"   # Solana (Base64)

# Auto-Buy Configuration
export AUTO_BUY_ENABLED="true"
export AUTO_BUY_AMOUNT="10"                      # USDT for BSC
export AUTO_BUY_AMOUNT_SOL="0.1"                # SOL for Solana
export AUTO_BUY_SLIPPAGE="5"                     # Default: 5%
```

### 监控间隔

```javascript
// BSC: 3 seconds per block
const BSC_MONITOR_INTERVAL = 3000;

// Solana: 10 seconds (Solana block time ~400ms)
const SOL_MONITOR_INTERVAL = 10000;
```

## 📊 自动购买配置

### BSC 自动购买（PancakeSwap）

- **路由器地址**：`0x10ED43C718714eb63d5aA57B78B54704E256024E`
- **支付代币**：USDT（0x55d398326f9955f0bEb）
- **滑点默认值**：5%
- **Gas 费用**：约 0.005 BNB（默认值）
- **最小购买金额**：1 USDT
- **推荐购买金额**：10-100 USDT

### Solana 自动购买（PumpSwap）

- **路由器地址**：自动从 PumpSwap 检测
- **支付代币**：SOL（WSOL）
- **滑点默认值**：5%
- **费用**：约 0.001 SOL（默认值）
- **最小购买金额**：0.01 SOL
- **推荐购买金额**：0.1-1 SOL

## 🎯 使用场景

### 1. 自动购买功能的应用场景

- 监控热门开发者地址并自动购买新代币：
```javascript
{
  "action": "monitor",
  "chain": "BSC",
  "address": "0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4",
  "duration": 3600,
  "autoBuy": {
    "enabled": true,
    "amount": 10,
    "slippage": 5
  }
}
```

### 2. 风险管理交易

```javascript
{
  "action": "monitor",
  "chain": "BOTH",
  "addresses": {
    "BSC": [
      "0x4f0f84abd0b2d8a7ae5e252fb96e07946dbbb1a4",
      "0x10ED43C718714eb63d5aA57B78B54704E256024E"
    ],
    "SOL": [
      "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
      "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"
    ]
  },
  "duration": 3600,
  "autoBuy": {
    "enabled": true,
    "amount": 0.1,
    "slippage": 5
  }
}
```

## 📋 日志记录

### BSC 日志

- 监控日志：`logs-bsc/bsc-monitor.log`
- 检测日志：`detections-bsc/detections.json`
- 自动购买日志：`logs-bsc/autobuy.log`

### Solana 日志

- 监控日志：`logs-sol/sol-monitor.log`
- 检测日志：`detections-sol/detections.json`
- 自动购买日志：`logs-sol/autobuy.log`

## 🛠️ 开发相关

### 依赖项

```json
{
  "dependencies": {
    "ethers": "^5.0.0",
    "@solana/web3.js": "^1.87.0",
    "axios": "^1.6.0",
    "@solana/token": "^0.2.0",
    "@solana/spl-token": "^0.2.0"
  }
}
```

### 安装依赖项

```bash
npm install
```

### 测试

```bash
# Test BSC monitoring
node index.js test

# Test BSC monitoring with auto-buy
AUTO_BUY_ENABLED="false" node index-bsc.js YourBSCDevAddress 60

# Test Solana monitoring (use index-sol-safe.js)
node index-sol-safe.js test

# Test Solana monitoring with auto-buy (use index-sol-safe.js)
AUTO_BUY_ENABLED="false" node index-sol-safe.js YourSolanaDevAddress 60
```

## 🔒 安全建议

### 1. 钱包安全

- ❌ **切勿在代码中硬编码钱包私钥**
- ✅ **始终使用环境变量**
- ✅ **为交易使用单独的钱包**
- ✅ **从小额测试开始**

### 2. 风险管理

- **设置合理的自动购买金额**
- **设置每日损失限额**
- **使用止损订单**
- **监控 Gas 费用**

### 3. Gas 资源优化

- **调整滑点以减少交易失败**
- **交易前监控 Gas 费用**
- **设置最大 Gas 费用**

### 4. 代币安全

- **购买前验证代币合约**
- **检查代币流动性**
- **避免购买流动性较低的代币**

## 📈 参考资料

- [BSC 文档](https://docs.bscscan.com/)
- [PancakeSwap 文档](https://docs.pancakeswap.finance/)
- [Solana Web3.js](https://solana-labs.github.io/solana-web3.js/)
- [SPL 代币文档](https://spl.solana.com/token/)
- [Pump.fun](https://pump.fun/)

## 🤝 贡献方式

欢迎提交问题和建议！

## 📄 许可证

MIT 许可证