---
name: x402
description: 使用 x402 协议进行基于 HTTP 的加密支付。当 Clawdbot 需要为 API 支付费用、访问付费资源或处理“402 Payment Required”（需要支付）的响应时，请使用该协议。该协议支持通过 x402 标准在 Base、Ethereum 及其他 EVM 链上进行 USDC（Uniswap 标准的美元稳定币）支付。
metadata: {"clawdbot":{"emoji":"💸","requires":{"anyBins":["node","npx"]},"env":["WALLET_PRIVATE_KEY"]}}
---

# x402 支付协议

x402 支付协议允许通过 HTTP 直接进行即时稳定的加密货币支付，它利用了 402 “Payment Required” 状态码来实现这一功能。该协议非常适合 AI 代理为 API 服务、数据或按需计算服务付费。

## 快速入门

### 安装 SDK
```bash
npm install x402
# or
pnpm add x402
```

### 环境配置
```bash
# Store wallet private key securely
export WALLET_PRIVATE_KEY="0x..."

# Optional: specify network RPC
export BASE_RPC_URL="https://mainnet.base.org"
```

## x402 的工作原理

1. **请求** → 客户端调用需要付费的 API。
2. **402 响应** → 服务器在 `PAYMENT-REQUIRED` 标头中返回支付详情。
3. **支付并重试** → 客户端完成支付操作，并在请求头中添加 `PAYMENT-SIGNATURE` 标头来尝试再次请求。
4. **访问资源** → 服务器验证支付信息后，释放资源并返回给客户端。

## 使用 x402 客户端

### TypeScript/Node.js
```typescript
import { x402Client } from 'x402';

const client = x402Client({
  privateKey: process.env.WALLET_PRIVATE_KEY,
  network: 'base', // or 'ethereum', 'arbitrum', etc.
});

// Automatic 402 handling
const response = await client.fetch('https://api.example.com/paid-endpoint');
const data = await response.json();
```

### 使用 fetch 库进行调用
```typescript
import { wrapFetch } from 'x402';

const fetch402 = wrapFetch(fetch, {
  privateKey: process.env.WALLET_PRIVATE_KEY,
});

// Use like normal fetch - 402s handled automatically
const res = await fetch402('https://paid-api.com/data');
```

## 手动操作流程（使用 curl）

### 第 1 步：获取支付要求
```bash
curl -i https://api.example.com/paid-resource
# Returns 402 with PAYMENT-REQUIRED header (base64 JSON)
```

### 第 2 步：解码支付详情
```bash
# The PAYMENT-REQUIRED header contains base64-encoded JSON:
# {
#   "amount": "1000000",      # 1 USDC (6 decimals)
#   "currency": "USDC",
#   "network": "base",
#   "recipient": "0x...",
#   "scheme": "exact"
# }
```

### 第 3 步：签名并完成支付
```bash
# Use x402 CLI or SDK to create payment signature
npx x402 pay \
  --amount 1000000 \
  --recipient 0x... \
  --network base
```

### 第 4 步：提供支付凭证后重试请求
```bash
curl -H "PAYMENT-SIGNATURE: <base64_payload>" \
  https://api.example.com/paid-resource
```

## 常见应用场景

- **为 API 调用付费**
- **为 AI 模型推理服务付费**
- **支付前检查账户余额**

## 支持的网络

| 网络 | 链路 ID | 支持状态 |
|---------|----------|--------|
| Base | 8453 | ✅ 主要网络 |
| Ethereum | 1 | ✅ 支持 |
| Arbitrum | 42161 | ✅ 支持 |
| Optimism | 10 | ✅ 支持 |
| Polygon | 137 | ✅ 支持 |

## 支付方式

- **固定金额支付**：每次 API 调用支付固定费用（例如：0.01 美元）。
- **按使用量计费**：根据实际使用情况支付最高限额（例如：LLM 代币）。
- **订阅模式**：基于钱包的访问方式（V2 版本）。

## 错误处理
```typescript
try {
  const res = await client.fetch(url);
} catch (err) {
  if (err.code === 'INSUFFICIENT_BALANCE') {
    // Need to fund wallet
  } else if (err.code === 'PAYMENT_FAILED') {
    // Transaction failed on-chain
  } else if (err.code === 'INVALID_PAYMENT_REQUIREMENTS') {
    // Server sent malformed 402 response
  }
}
```

## 安全注意事项

- **切勿在日志或聊天记录中泄露私钥**。
- **使用环境变量来存储钱包凭证**。
- **推荐使用 `op run` 或类似工具来注入敏感信息**。
- **在确认大额交易前仔细核对支付金额**。

## V2 版本（2025 年 12 月发布）

- **基于钱包的身份验证**：通过会话机制，避免每次调用时都需要重新支付。
- **自动检测**：API 会在 `/.well-known/x402` 路径下提供支付元数据。
- **多支付处理商选择**：用户可以自由选择支付服务提供商。
- **CAIP 标准**：统一的链路/资产标识符。

## 相关资源

- **技术规范**：https://github.com/coinbase/x402
- **官方文档**：https://docs.cdp.coinbase.com/x402
- **演示 API**：https://www.x402.org