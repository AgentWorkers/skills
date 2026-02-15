---
name: xclaw02
description: 执行 x402 类型的支付操作。为 API 支付费用，销售您的服务，并使用 USDC 在 Base 以及其他 EVM 链上处理“支付 Required”（402）类型的响应。
metadata: {"openclaw":{"emoji":"$","requires":{"anyBins":["node","npx","python3","pip"]}}}
---

# xClaw02

这是您使用 x402 的入口点——x402 是一种用于代理网络的开放支付标准。

x402 是一个 [开放协议](https://x402.org)，它允许通过 HTTP 使用 402 “Payment Required” 状态码进行即时稳定的加密货币支付。xClaw02 由 [Primer](https://primer.systems) 开发，提供了对代理友好的命令行工具（CLI）和简单的 API，用于发起和接收支付。

## 何时使用此技能

在以下情况下使用 xClaw02：
- 当您收到 “402 Payment Required” 的 HTTP 响应时
- 当您需要访问需要付费的 API 或资源时
- 当用户要求您使用加密货币/USDC 进行支付时
- 当您需要检查钱包余额或管理支付时
- 当您希望为自己的 API 或服务收费时

## 如何响应

| 用户所说/所问 | 应该做什么 |
|----------------|------------|
| “我收到了一个 402 错误” | 这是一个 x402 支付请求。使用 `xclaw02 probe <url>` 命令检查该 URL，显示价格，并询问用户是否愿意支付 |
| “为这个 API 支付” | 使用 `xclaw02 pay <url> --max-amount <amount>` 命令进行支付——请务必先与用户确认金额 |
| “检查我的余额” | 运行 `xclaw02 wallet balance <address>` 命令 |
| “设置 x402” / “设置支付” | 运行 `xclaw02 openclaw init` 命令 |
| “你们支持哪些网络？” | 列出支持的网络（Base 是主要网络；还包括 Ethereum、Arbitrum、Optimism、Polygon） |
| “X 的费用是多少？” | 使用 `xclaw02 probe <url>` 命令检查价格 |
| “创建一个钱包” | 运行 `xclaw02 wallet create` 命令——提醒用户安全保存私钥 |
| “我想为我的 API 收费” | 展示 Express.js 或 FastAPI 中间件的示例 |

## 快速设置

### Node.js
```bash
npx xclaw02 openclaw init
```

### Python
```bash
pip install xclaw02
xclaw02 openclaw init
```

这将：
1. 创建一个新的钱包（或使用现有的钱包）
2. 将配置保存到 `~/.openclaw/skills/xclaw02/` 文件夹中
3. 显示钱包地址，以便用户可以使用 USDC 在 Base 网络上进行充值

## x402 的工作原理

1. **请求**：您调用一个需要付费的 API
2. **402 响应**：服务器在响应头中返回支付要求
3. **支付并重试**：签署支付信息，然后使用 `PAYMENT-SIGNATURE` 标头重新发送请求
4. **访问**：服务器验证支付信息，在链上完成结算，并返回资源

对于付款方来说，这笔支付是 **无需支付 gas 费用的**——支付处理方会负责处理 gas 费用。

## CLI 命令

| 命令 | 描述 |
|---------|-------------|
| `xclaw02 openclaw init` | 为当前代理设置 xClaw02 |
| `xclaw02 openclaw status` | 检查设置状态和余额 |
| `xclaw02 probe <url>` | 检查该 URL 是否需要支付并获取价格 |
| `xclaw02 pay <url>` | 为资源支付（需要 `XCLAW02_PRIVATE_KEY`） |
| `xclaw02 pay <url> --dry-run` | 预览支付（不实际支付） |
| `xclaw02 pay <url> --max-amount 0.10` | 设置支付限额进行支付 |
| `xclaw02 wallet create` | 创建一个新的钱包 |
| `xclaw02 wallet balance <address>` | 查看 Base 网络上的 USDC 余额 |
| `xclaw02 wallet from-mnemonic` | 从助记词恢复钱包 |
| `xclaw02 networks` | 列出支持的网络 |

### CLI 命令示例输出

```bash
$ xclaw02 probe https://api.example.com/paid
{
  "status": "payment_required",
  "price": "0.05",
  "currency": "USDC",
  "network": "base",
  "recipient": "0x1234...abcd",
  "description": "Premium API access"
}

$ xclaw02 wallet balance 0xYourAddress
{
  "address": "0xYourAddress",
  "network": "base",
  "balance": "12.50",
  "token": "USDC"
}

$ xclaw02 pay https://api.example.com/paid --max-amount 0.10
{
  "status": "success",
  "paid": "0.05",
  "txHash": "0xabc123...",
  "response": { ... }
}
```

## 在代码中使用

### Node.js / TypeScript
```javascript
const { createSigner, x402Fetch } = require('xclaw02');

// Private key format: 0x followed by 64 hex characters
const signer = await createSigner('eip155:8453', process.env.XCLAW02_PRIVATE_KEY);
const response = await x402Fetch('https://api.example.com/paid', signer, {
  maxAmount: '0.10'  // Maximum USDC to spend
});
const data = await response.json();
```

### Python
```python
from xclaw02 import create_signer, x402_requests
import os

# Private key format: 0x followed by 64 hex characters
signer = create_signer('eip155:8453', os.environ['XCLAW02_PRIVATE_KEY'])
with x402_requests(signer, max_amount='0.10') as session:
    response = session.get('https://api.example.com/paid')
    data = response.json()
```

## 在服务器端出售服务

希望其他代理为您付费？可以在您的 API 中添加支付墙：

### Express.js
```javascript
const express = require('express');
const { x402Express } = require('xclaw02');

const app = express();

app.use(x402Express('0xYourAddress', {
  '/api/premium': {
    amount: '0.05',          // $0.05 USDC per request
    asset: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    network: 'eip155:8453'
  }
}));

app.get('/api/premium', (req, res) => {
  res.json({ data: 'Premium content here' });
});
```

### FastAPI (Python)
```python
from fastapi import FastAPI
from xclaw02 import x402_fastapi

app = FastAPI()

app.add_middleware(x402_fastapi(
    '0xYourAddress',
    {
        '/api/premium': {
            'amount': '0.05',
            'asset': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
            'network': 'eip155:8453'
        }
    }
))

@app.get("/api/premium")
async def premium_endpoint():
    return {"data": "Premium content here"}
```

## 支持的网络

| 网络 | CAIP-2 ID | 代币 | 备注 |
|---------|-----------|-------|-------|
| Base | eip155:8453 | USDC | **主要网络**——速度快、费用低，推荐使用 |
| Base Sepolia | eip155:84532 | USDC | 测试网 |
| Ethereum | eip155:1 | USDC | 费用较高 |
| Arbitrum | eip155:42161 | USDC | |
| Optimism | eip155:10 | USDC | |
| Polygon | eip155:137 | USDC | |

Base 是默认网络。要使用其他网络，请设置 `XCLAW02_NETWORK` 环境变量。

## 支付处理方

支付处理方负责支付验证和链上结算。x402 生态系统中有许多独立的支付处理方：

| 名称 | URL | 备注 |
|------|-----|-------|
| Primer | https://x402.primer.systems | 默认支付处理方 |
| Coinbase | https://api.cdp.coinbase.com/platform/v2/x402 | |
| x402.org | https://x402.org/facilitator | 仅支持测试网 |
| PayAI | https://facilitator.payai.network | |
| Corbits | https://facilitator.corbits.dev | |
| Dexter | https://x402.dexter.cash | |
| Heurist | https://facilitator.heurist.xyz | |
| Kobaru | https://gateway.kobaru.io | |
| Nevermined | https://api.live.nevermined.app/api/v1/ | |
| Openfacilitator | https://pay.openfacilitator.io | |
| Solpay | https://x402.solpay.cash | |
| xEcho | https://facilitator.xechoai.xyz | |

要使用其他支付处理方，请设置 `XCLAW02_FACILITATOR` 环境变量。

## 环境变量

| 变量 | 格式 | 描述 |
|----------|--------|-------------|
| `XCLAW02_PRIVATE_KEY` | `0x` + 64 个十六进制字符 | 钱包私钥（支付时必需） |
| `XCLAW02_NETWORK` | `eip155:8453`、`base` 等 | 默认网络（默认为 Base） |
| `XCLAW02_MAX_AMOUNT` | `0.10` | 默认的最大支付金额（单位：USDC） |
| `XCLAW02_FACILITATOR` | 支付处理方 URL | 可自定义 |

## 错误处理

| 错误代码 | 含义 | 应该做什么 |
|------------|---------|------------|
| `INSUFFICIENT_FUNDS` | 钱包余额不足 | 告诉用户在 Base 网络上使用 USDC 充值 |
| `AMOUNT_EXCEEDS_MAX` | 支付金额超过最大限额 | 请用户批准更高的金额，然后使用 `--max-amount` 重新尝试 |
| `SETTLEMENT_FAILED` | 链上结算失败 | 稍等片刻后重试，或尝试其他支付处理方 |
| `INVALID_RESPONSE` | 402 响应格式不正确 | 该 URL 可能不支持 x402 协议 |
| `NETWORK_MISMATCH` | 使用的网络不正确 | 检查 402 响应中的网络信息，并设置 `XCLAW02_NETWORK` |

## 安全注意事项

- **切勿在日志、聊天记录或输出中泄露私钥** |
- 使用环境变量来存储钱包凭证 |
- **在支付前务必与用户确认支付金额** |
- 仅使用完成任务所需的资金为钱包充值 |
- 私钥格式：`0x` 后跟 64 个十六进制字符

## 替代实现

x402 是一个开放标准，有多种实现方式：

**官方 Coinbase SDK**：提供 Go 语言支持，同时支持 Solana（SVM）和 EVM 链路：
- GitHub: https://github.com/coinbase/x402
- ClawHub：参见 @notorious-d-e-v 开发的 `x202` 实现 |
- 适合：Go 开发者、Solana 平台的支付场景，完全符合规范

**何时使用替代方案**：
- 当您需要 Go 语言支持时（xClaw02 仅支持 Node.js/Python）
- 当您需要 Solana 平台的支付功能时（xClaw02 仅支持 EVM 链路）
- 当您希望使用官方参考实现时

所有 x402 实现都是互操作的——使用任何 SDK 的客户端都可以向使用其他 SDK 的服务器进行支付，只要它们支持相同的网络和支付处理方即可。

## 链接

- **x402 协议**：https://x402.org
- **SDK (npm)**：https://npmjs.com/package/xclaw02
- **SDK (PyPI)**：https://pypi.org/project/xclaw02
- **GitHub**：https://github.com/primer-systems/xClaw02