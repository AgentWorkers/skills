---
name: x402-client
description: 使用 x402 协议（Coinbase）通过 HTTP 进行 USDC 支付和收款。适用于代理的 Stripe 工具——可用于支付服务费用、销售自己的产品以及查询余额。该功能支持 Base 网络（主网 + 测试网）。
metadata: {"clawdbot":{"requires":{"bins":["node"]}}}
---

# x402 客户端 — 代理支付功能

通过 HTTP 使用 USDC 稳定币支付服务费用或出售自己的服务。

## 快速入门

```bash
# Install + create wallet
cd <skill-dir> && bash scripts/setup.sh

# Buy: access a paid API
node scripts/pay-request.js --url https://api.example.com/paid

# Sell: run your own paywalled service
node scripts/serve-paid.js --port 4021

# Check balance
node scripts/wallet-balance.js
```

---

## 设置

```bash
bash scripts/setup.sh
```

在 `~/.x402/wallet.json` 中创建一个 EVM 钱包，并安装所需的依赖项。此操作是幂等的（即不会覆盖现有的钱包）。

**用 USDC 充值您的钱包**：
- **测试网：** Circle 水龙头 → https://faucet.circle.com （20 USDC，Base Sepolia）
- **主网：** 从 Coinbase、WazirX 或其他代理平台转账 USDC

---

## 支付服务费用（客户端）

### 命令行脚本
```bash
node scripts/pay-request.js \
  --url "https://api.example.com/service" \
  --method GET \
  --network base-sepolia \
  --max-price 0.50 \
  --dry-run          # preview price without paying
```

选项：
| 标志 | 默认值 | 描述 |
|------|---------|-------------|
| `--url` | （必填） | 服务 URL |
| `--method` | GET | HTTP 方法 |
| `--body` | — | POST/PUT 请求的 JSON 请求体 |
| `--network` | base | `base`（主网）或 `base-sepolia`（测试网） |
| `--max-price` | 1.00 | 价格上限（以 USD 计） |
| `--dry-run` | false | 不进行实际支付，仅显示价格 |

### 程序化实现（lib/client.js）
```js
import { createPayClient, getBalance } from 'x402-client/lib/client.js';

// Create a payment-enabled fetch
const payFetch = await createPayClient({ maxPrice: 0.50 });

// Use it like regular fetch — payments happen automatically
const res = await payFetch('https://api.example.com/paid');
const data = await res.json();

// Check wallet balance
const balance = await getBalance(); // { mainnet: "5.23", testnet: "19.99" }
```

---

## 出售服务（服务器端）

### 快速入门
```bash
# Run the template server
node scripts/serve-paid.js --port 4021 --network base-sepolia
```

编辑 `serve-paid.js` 以添加您自己的服务端接口。这是一个模板，您可以自由定制。

### 程序化实现（lib/server.js）
```js
import express from 'express';
import { createPaywall, paymentRequired } from 'x402-client/lib/server.js';

const app = express();

// Option 1: Middleware (simplest)
app.get('/api/audit',
  createPaywall({ price: 0.03, description: 'Skill audit' }),
  (req, res) => {
    res.json({ result: 'your premium content' });
  }
);

// Option 2: Manual 402 response (more control)
app.get('/api/custom', (req, res) => {
  if (!req.header('payment-signature')) {
    return paymentRequired(res, { price: 0.05 });
  }
  res.json({ result: 'paid content' });
});

app.listen(4021);
```

服务器功能：
- `createPaywall(opts)` — Express 中间件，仅在支付完成后允许访问接口 |
- `paymentRequired(res, opts)` — 发送带有正确 x402 v2 标头的 402 错误响应 |
- `buildPaymentRequirements(opts)` — 手动生成支付所需的信息 |
- 无需使用 Coinbase 的实时支付服务（适用于测试网） |
- 从 `~/.x402/wallet.json` 自动读取钱包地址 |

---

## 测试

```bash
# Run full end-to-end test (server + client, automated)
node scripts/test-e2e.js
```

测试流程：发送请求 → 收到 402 错误响应 → 完成签名支付 → 服务内容交付。

---

## 钱包管理

```bash
# Show address (safe to share)
node scripts/wallet-info.js

# Check USDC balance (mainnet + testnet)
node scripts/wallet-balance.js

# Export private key (⚠️ DANGEROUS)
node scripts/wallet-info.js --export-key
```

---

## 安全性

- 私钥加密存储在 `~/.x402/wallet.json` 中（仅所有者可访问） |
- `--max-price` 防止意外超支 |
- 对于不熟悉的服务，务必先使用 `--dry-run` 模式进行测试 |
- 保持最低限度的资金余额，仅保留操作所需的资金 |
- 绝不要分享私钥或 `wallet.json` 文件 |

---

## x402 的工作原理

```
Client → GET /api/service → 402 + PAYMENT-REQUIRED header (base64 JSON)
      → parse requirements → sign USDC payment (EIP-712)
      → retry with PAYMENT-SIGNATURE header → 200 + content
```

- **协议：** x402 v2（基于 Coinbase 的支付协议）——通过 HTTP 标头传递支付所需的信息 |
- **货币：** USDC 稳定币（6 位小数） |
- **网络：** Base（Ethereum L2）——手续费低，结算速度快 |
- **无需 ETH**：支付过程由 Coinbase 在链上处理相关费用 |

---

## 文件结构

```
x402-client/
├── SKILL.md              # This file
├── lib/
│   ├── client.js         # Reusable payment client wrapper
│   └── server.js         # Reusable payment server wrapper
└── scripts/
    ├── setup.sh          # One-command install
    ├── pay-request.js    # CLI: make paid requests
    ├── serve-paid.js     # CLI: run paywalled server (template)
    ├── wallet-create.js  # Generate wallet
    ├── wallet-info.js    # Show/export wallet
    ├── wallet-balance.js # Check USDC balance
    └── test-e2e.js       # End-to-end test
```