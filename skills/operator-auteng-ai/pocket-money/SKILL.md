---
name: pocket-money
description: 将你的AI代理分配加密钱包，以便其能够支付x402服务的相关费用。为每个特定用途创建独立的钱包，让你的工作人员为每个钱包充值资金，然后在使用前必须获得人类的批准，通过x402协议进行交易。无需任何账户或KYC（了解客户）流程——只需提供钱包地址以及存储在Base平台上的USDC（美元稳定币）即可。
---
# 零用钱 — 为代理的钱包充值

您可以使用一个工具来创建加密钱包（基于 Base 的 USDC），并用这些钱包来支付支持 x402 协议的服务（如 AutEng Compute）。每个钱包都是一对独立的密钥，拥有自己的余额——请根据不同的用途或预算创建相应的钱包。

**软件包**: [`@auteng/agent-utils`](https://www.npmjs.com/package/@auteng/agent-utils) — 由 AutEng 发布（[GitHub 源代码](https://github.com/operator-auteng-ai/agent-utils)）。

## 设置（仅首次使用）

安装 `agent-utils` 库：

```bash
npm install @auteng/agent-utils
```

## 创建钱包

为不同的用途或预算创建相应的钱包：

```typescript
import { wallet } from '@auteng/agent-utils';

const w = await wallet.create({ name: "feb-2026-compute" });
console.log(w.address); // 0xABC123...
```

如果磁盘上已经存在同名钱包，系统会自动加载该钱包。每个钱包的文件存储在 `.auteng/wallets/<name>.json` 文件中。

您也可以快速创建一个默认钱包：

```typescript
const w = await wallet.create();
```

## 请求资金

当您需要资金时，请让相关人员为指定的钱包充值：

```
I need $12 in USDC for today's compute tasks.

Please send USDC on **Base** to this address:
`0xABC123...` (wallet: "feb-2026-compute")

You can send from Coinbase, an exchange, or any wallet that supports Base.
```

请明确说明以下信息：
- **所需金额** 及 **用途**（例如：“$5 用于 API 调用”，“$20 用于批量处理任务”）
- **钱包名称**，以便您和相关人员都能追踪预算情况
- **网络**：始终使用 Base 网络（而非 Ethereum 主网或 Arbitrum）
- **使用的代币**：USDC（而非 ETH 或其他代币）

## 等待资金到账

提交请求后，请等待 USDC 资金到账：

```typescript
await w.waitForFunding(12_000000n);
// Polls Base every 10s until >= 12 USDC is available
```

告知相关人员您正在等待资金到账——他们可能需要几分钟时间完成转账。

## 支出前的手动审批

**重要提示**：在进行任何支付或运行计算任务之前，您必须：
1. 向相关人员详细说明您的支出目的及原因
2. 显示预计费用（使用 `compute.pricing()` 函数查询价格）
3. **等待明确的批准** 后再继续操作

**示例**：

```
I'd like to run a Python script on sandboxed compute.

  Size:  small (2 vCPU, 1GB RAM)
  Cost:  ~$0.002 (base) + runtime
  Wallet: "feb-2026-compute" ($0.98 remaining)

OK to proceed?
```

切勿在没有列出所有待支付操作的情况下批量执行它们。如果需要执行多个付费操作，请先展示总预估费用并获得批准。

## 运行计算任务

在获得资金并得到相关人员批准后，将钱包信息传递给计算服务：

```typescript
import { compute } from '@auteng/agent-utils';

const result = await compute.run({
  code: 'print("hello world")',
  stack: 'python',
  size: 'small',
  wallet: w,
});
console.log(result.stdout);  // "hello world\n"
```

支付过程由 x402 协议自动处理。支持的开发语言/框架包括 `python` 和 `node`；任务规模分为 `small`、`med`、`large` 三种。

## 通过 x402 协议进行支付（适用于任何支持 x402 的服务）

对于任何支持 x402 协议的服务，可以直接使用钱包的 `fetch()` 方法进行支付：

```typescript
const res = await w.fetch('https://x402.auteng.ai/api/x402/compute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'print("hello world")',
    stack: 'python',
    size: 'small',
  }),
});
```

如果服务返回 “402 Payment Required” 的提示，库会自动生成支付授权信息并重新尝试支付。无需进行区块链交易——支付过程在服务器端完成。

## 管理多个钱包

```typescript
// Retrieve an existing wallet by name
const w = wallet.get("feb-2026-compute");

// List all wallets
const all = wallet.list();
for (const w of all) {
  const bal = await w.checkBalance();
  console.log(`${w.name}: ${w.address} — ${bal} USDC`);
}
```

## 查看钱包余额

```typescript
const balance = await w.checkBalance();
// Returns USDC in minor units (6 decimals)
// e.g., 12_000000n = $12.00
```

如果钱包余额不足，请在执行高成本操作前向相关人员请求更多资金。

## 重要注意事项：
- 在进行任何涉及资金支出的操作之前，务必获得相关人员的批准。
- 您的钱包仅支持存储 Base 网络上的 USDC——无需使用 ETH 作为交易手续费。
- 钱包的私钥存储在本地文件 `.auteng/wallets/<name>.json` 中，权限设置为 0600（仅限读取）。如果私钥丢失，资金将无法恢复。
- 为每个预算创建单独的钱包，以便您和相关人员能够清晰地追踪支出情况。
- 在支出前请先查看费用信息：使用 `compute.pricing()` 函数查询价格。