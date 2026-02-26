---
name: pocket-money
description: 为你的AI代理在Base平台上创建加密钱包。为每个特定用途创建独立的钱包，让人类用户为这些钱包充值资金，查看余额，并管理预算。无需任何账户信息或KYC（了解客户）流程——只需钱包地址和USDC（Base平台上的数字货币）即可。
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
      config:
        - .auteng/wallets/
    install:
      - kind: node
        package: "@auteng/pocket-money"
        bins: []
    homepage: https://github.com/operator-auteng-ai/pocket-money
---
# **零用钱管理** — 为你的代理（人类助手）管理资金

你拥有一个工具，可以用来创建和管理加密钱包（基于 Base 平台的 USDC）。每个钱包都是一对独立的密钥，拥有自己的余额——可以根据不同的用途或预算来创建相应的钱包。

**包**: [`@auteng/pocket-money`](https://www.npmjs.com/package/@auteng/pocket-money) — 由 AutEng 开发（[GitHub 源代码链接](https://github.com/operator-auteng-ai/pocket-money))。

## **首次设置**

安装 `pocket-money` 库：

```bash
npm install @auteng/pocket-money
```

## **创建钱包**

为每个用途或预算创建一个对应的钱包：

```typescript
import { wallet } from '@auteng/pocket-money';

const w = await wallet.create({ name: "feb-2026" });
console.log(w.address); // 0xABC123...
```

如果磁盘上已经存在同名钱包，系统会自动加载该钱包。所有钱包都存储在 `.auteng/wallets/<name>.json` 文件中。

你也可以快速创建一个默认钱包：

```typescript
const w = await wallet.create();
```

### **网络设置**

```typescript
// Base mainnet (default)
const w = await wallet.create({ name: "prod" });

// Base Sepolia testnet
const w = await wallet.create({ name: "test", network: "base-sepolia" });
```

## **请求资金**

当你需要资金时，向你的代理请求为特定的钱包充值：

```
I need $12 in USDC for today's tasks.

Please send USDC on **Base** to this address:
`0xABC123...` (wallet: "feb-2026")

You can send from Coinbase, an exchange, or any wallet that supports Base.
```

请明确说明以下信息：
- **所需金额** 及 **用途**（例如：“$5 用于 API 调用”，“$20 用于批量处理任务”）
- **钱包名称**，以便你和你的代理都能追踪资金使用情况
- **使用的网络**：必须使用 Base 网络（而非 Ethereum 主网或 Arbitrum）
- **使用的代币**：必须使用 USDC（而非 ETH 或其他代币）

## **等待资金到账**

请求资金后，请等待 USDC 到账：

```typescript
await w.waitForFunding(12_000000n);
// Polls Base every 10s until >= 12 USDC is available
```

你可以设置超时时间：

```typescript
await w.waitForFunding(12_000000n, { timeout: 120_000 });
// Throws after 2 minutes if balance < $12
```

告知你的代理你正在等待资金到账——他们可能需要几分钟来完成转账。

## **支出前的手动批准**

**重要提示**：在进行任何支付操作之前，你必须：
1. 向你的代理详细说明你要支出的金额及用途
2. 显示预计的费用
3. **等待他们的明确批准** 后再继续操作

**示例**：

```
I'd like to call an x402 API endpoint.

  Service: api.example.com/generate
  Cost:    ~$0.05 per request
  Wallet:  "feb-2026" ($0.98 remaining)

OK to proceed?
```

切勿在没有列出所有待支付操作的情况下批量执行支付请求。如果需要执行多个支付请求，请先展示总费用并获得批准。

## **钱包管理**

```typescript
// Retrieve an existing wallet by name
const w = wallet.get("feb-2026");

// List all wallets
const all = wallet.list();
for (const w of all) {
  const bal = await w.checkBalance();
  console.log(`${w.name}: ${w.address} — ${bal} USDC`);
}

// Check balance
const balance = await w.checkBalance();
// Returns USDC in minor units (6 decimals)
// e.g., 12_000000n = $12.00
```

如果钱包余额不足，请在执行高成本操作前向代理请求更多资金。

## **安全与存储**

**私钥**：钱包的私钥以未加密的 JSON 格式存储在 `.auteng/wallets/<name>.json` 文件中，文件权限设置为 0600（仅允许所有者读取和写入）。这些私钥用于签署 USDC 支付授权。如果文件被泄露或设备被入侵，钱包中的资金可能会被盗。请将钱包文件视为重要密码来保护。

**网络访问**：该工具会通过 HTTPS 向以下地址发送请求：
- **Base RPC**（`mainnet.base.org`）——用于查询 USDC 余额

**安全措施**：
- **在任何支出操作前都必须获得代理的批准**
- 仅为特定任务所需的少量资金充值钱包——将其视为零用钱，而非长期储蓄
- 为不同的预算创建单独的钱包，以便你和你的代理能够清晰地追踪资金使用情况
- 你的钱包仅需要存储 **Base 平台上的 USDC**——无需使用 ETH 作为交易手续费