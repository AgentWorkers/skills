---
name: "newsriver-global-intelligence"
version: "3.0.0"
description: "专为AI代理设计的专业量化智能与DeFi执行平台。该平台拥有10年的新闻价格相关性分析数据，集成了Enso DeFi超级聚合器（支持200多个去中心化交易所、15个区块链平台），具备跨链桥接功能（支持多种协议），并采用Privy TEE技术保障钱包的安全性。"
tags: ["finance", "crypto", "trading", "alpha", "correlation", "defi", "swap", "bridge", "cross-chain", "enso", "x402", "proxy", "privy"]
author: "YieldCircle Infrastructure"
homepage: "https://showcase.yieldcircle.app"
author_url: "https://showcase.yieldcircle.app"
license: "MIT"
env:
  NEWSRIVER_API_KEY:
    description: "Your YieldCircle API key for subscription-based access. Required if not using x402 micropayments."
    required: false
---
# YieldCircle 智能与去中心化金融（DeFi）执行技能（v3.0.0）

## 功能与背景
YieldCircle 是一个面向机构的智能系统，专为 AI 代理提供去中心化金融（DeFi）执行服务及相关基础设施。它利用 10 年的金融历史数据，通过 Enso Finance 在 15 个以上的区块链上实现自动化的 DeFi 执行功能；同时通过 Across Protocol 提供跨链桥接服务，并使用 Privy TEE（可信执行环境）确保交易安全——所有这些功能都通过一个统一的 API 提供。

### 1. DeFi 超级聚合器（Enso Finance）
- **交易执行：** 在 200 多个去中心化交易所（DEX）和 180 多个协议上执行交易、跨链转账、收益投资等操作。
  - **代币交换：** `POST /api/defi/swap` — 在支持的任何区块链上执行代币交换
  - **跨链转账：** `POST /api/defi/cross-chain` — 原子化地执行跨链转账（支持 Stargate、LayerZero 等协议）
  - **收益投资：** `POST /api/defi/yield` — 进入或退出收益投资策略（如 Aave、Compound 等平台）
  - **多步骤操作：** `POST /api/defi/bundle` — 将多个 DeFi 操作合并为一次交易
  - **账户余额：** `GET /api/defi/balances` — 查看所有协议下的账户余额
  - **支持的平台：** `GET /api/defi/supported` — 查看支持的区块链、代币及功能列表

```bash
# Cross-chain swap: USDC on Base → POL on Polygon (LIVE ✓)
curl -X POST https://api.yieldcircle.app/api/defi/swap \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": 2,
    "chain_id": 8453,
    "token_in": "USDC",
    "token_out": "ETH",
    "amount": "1000000",
    "slippage": 50,
    "receiver": "0xYourAddress",
    "dry_run": true
  }'
```

### 2. 跨链桥接（Across Protocol）
- **无需人工干预的桥接服务：** 在 7 个以上的区块链上实现快速（亚分钟级）的跨链转账。
  - **报价查询：** `GET /api/bridge/quote?from=Base&to=Arbitrum&amount=1`
  - **执行操作：** `POST /api/bridge/execute` — 通过 Privy 钱包完成转账操作
  - **状态查询：** `GET /api/bridge/status/:txHash` — 查看转账状态
  - **流量限制：** `GET /api/bridge/limits` — 查看每对区块链的流量限制

### 3. 新闻影响分析引擎（高级功能）
- **量化新闻影响：** 分析特定新闻对资产价格的历史影响。
  - **价格波动分析：** 查询 BTC、ETH 及 400 多种加密货币在特定新闻发布后的 24 小时和 7 天内的价格变动
  - **历史数据参考：** 提供过去十年内类似新闻事件对市场的真实影响数据

```bash
curl -H "X-API-Key: $NEWSRIVER_API_KEY" \
  "https://api.yieldcircle.app/api/v1/analysis/correlation?topic=ETF&symbol=BTC-USD"
```

### 4. “今日回顾”功能
- **历史事件检索：** 提供过去 10 年内的精选新闻事件及其对应的价格变动记录
- **重要节点记录：** 包括市场历史高点、暴跌事件及重大政策变动

### 5. AskRiver AI 聊天服务（高级功能）
- **基于 Gemini 的自然语言处理技术：** 可搜索来自 137 个国家、277 个来源的 28.8 万篇文章

### 6. 执行代理服务
- **发送邮件（0.05 美元）：** `POST /api/v1/proxy/email`
- **发送短信（0.25 美元）：** `POST /api/v1/proxy/sms`
- **网页抓取（0.10 美元）：** `POST /api/v1/proxy/scrape`

### 7. 代理钱包（Privy TEE）
- **安全保障：** 代理使用 Privy TEE 环境中的专用钱包进行交易，私钥始终安全存储
- **钱包创建：** `POST /api/privy/wallets/create-all`
- **余额查询：`GET /api/defi/balances?agent_id=2&chain_id=8453`

## 认证机制
- **x402 微支付（自动处理）：** 使用 USDC 进行支付，需在请求头中添加 `X-PAYMENT` 标头
- **API 密钥：** 订阅服务需提供 `X-API-Key` 标头
- 所有操作均记录在 D1 数据库中，便于审计

## 错误处理与支持
若 API 返回 `402 Payment Required` 错误，请访问 [agent.yieldcircle.app/#pricing](https://agent.yieldcircle.app/#pricing) 进行处理；
如需支持，请联系 **support@agent.yieldcircle.app**。