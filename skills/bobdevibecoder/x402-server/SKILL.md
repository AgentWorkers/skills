---
name: x402-server
description: 使用 x402 支付协议的盈利型 API 服务器：针对 AI 代理服务，收费采用 USDC（基于 Base 的加密货币）。
metadata:
  clawdbot:
    emoji: "💰"
    requires:
      bins: ["node"]
---

# x402 带广告功能的 API 服务器

使用 Base 平台上的 x402 支付协议，构建一个按请求计费（使用 USDC）的付费 API，该 API 可供其他 AI 代理使用。

## 主要功能

- 提供 4 个付费 API 端点：（加密研究、市场扫描、内容生成、代理状态）
- 通过 HTTP 402 响应实现支付验证（当请求不符合支付要求时返回 402 错误）
- 在 Base 平台上支持无需手续费（“无 gas”）的 USDC 支付
- 兼容 Coinbase 的代理钱包（Agentic Wallet）

## 设置步骤

1. 安装所需依赖：`npm install express x402-express`
2. 将 `PAY_TO` 变量设置为你的钱包地址
3. 运行服务器：`node index.js`

## API 端点及其功能

| 端点          | 费用      | 描述                                      |
|---------------|---------|-----------------------------------------|
| GET /api/crypto-research | \$0.05    | 提供代币研究和分析服务                   |
| GET /api/market-scan | \$0.02    | 提供热门代币扫描服务                   |
| POST /api/content-generate | \$0.10    | 提供 AI 内容生成服务                   |
| GET /api/agent-status | \$0.01    | 提供代理状态及功能信息                   |
| GET /health       | 免费      | 提供服务器健康检查服务                   |
| GET /api/services    | 免费      | 提供所有可用服务的目录                   |