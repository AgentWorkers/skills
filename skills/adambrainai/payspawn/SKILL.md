---
name: payspawn
description: "为任何通过 API 进行支付的 AI 代理添加支出控制功能。支持 x402 自动支付、每日限额、单笔交易限额、地址白名单以及代理群组管理。当您的代理自主调用付费 API 或进行支付时，可以使用此功能。该功能兼容基于 USDC 的 Base 平台。"
requires:
  env:
    - name: PAYSPAWN_CREDENTIAL
      description: "Scoped spending credential issued from payspawn.ai/dashboard. This is NOT a private key — it is a base64-encoded spend permission authorizing the PaySpawn V5 contract to transfer USDC up to the limits you set. The credential encodes: daily cap, per-transaction limit, optional address whitelist, and expiry. Revocable on-chain at any time via dashboard or ps.agent.pause(). Set the lowest limits sufficient for your use case."
      secret: true
      required: false
      lifetime: "Up to 1 year from creation (set at credential creation time). Revocable immediately on-chain — revocation takes effect on the next transaction attempt."
      minPrivilege: "Set daily cap to the minimum USDC needed per day. Use allowedTo address whitelist to restrict payment destinations. Use per-tx cap to limit single-payment exposure."
  install:
    - package: "@payspawn/sdk"
      registry: "npm"
      version: ">=5.3.0"
      source: "https://www.npmjs.com/package/@payspawn/sdk"
      audit: "https://github.com/adambrainai/payspawn"
metadata:
  {
    "openclaw": {
      "emoji": "🔐",
      "color": "#F65B1A"
    }
  }
---
# PaySpawn — 代理支付控制

为能够自主进行支付的AI代理设置消费限额。这些限制是在Base链上的智能合约层面执行的，既不在软件中，也不在服务器端。该合约不可被篡改。

## 安装

```bash
npm install @payspawn/sdk
```

## 凭据设置（仅需一次人工操作）

在代理能够进行支付之前，钱包所有者必须创建一个凭证：

1. 访问 [payspawn.ai/dashboard](https://payspawn.ai/dashboard)
2. 连接您的钱包（MetaMask、Coinbase Wallet或任何支持USDC的Base链钱包）
3. 批准USDC的每日消费上限（一次链上交易，手续费约0.005美元）
4. 设置限额：每日总额上限、单笔交易上限，可选的地址白名单
5. 签署凭证（使用EIP-712签名方式，无需支付手续费，也不会产生交易费用）
6. 复制凭证字符串，并将其设置为环境变量 `PAYSPAWN_CREDENTIAL`

该凭证并非私钥；您的钱包密钥始终由您控制。代理只能在其设定的限额范围内进行支付——智能合约会严格执行这一限制，无法被绕过。

## 使用方法

```typescript
import { PaySpawn } from "@payspawn/sdk";
const ps = new PaySpawn(process.env.PAYSPAWN_CREDENTIAL);

// Auto-pay x402 APIs within your set limits
const res = await ps.fetch("https://api.example.com/endpoint");

// Send a payment
await ps.pay("0xRecipientAddress", 1.00);

// Check balance and remaining daily allowance
const { balance, remaining } = await ps.check();

// Pause all payments instantly (on-chain, immediate effect)
await ps.agent.pause();

// Resume payments
await ps.agent.unpause();
```

## 队列模式

从一个共享的凭证池中为多个代理分配凭证。一个钱包为整个池提供资金；每个代理都会获得自己的凭证以及相应的每日消费限额。

```typescript
// Create a shared budget pool
const pool = await ps.pool.create({ totalBudget: 100, agentDailyLimit: 10 });

// Fund the pool: send USDC to pool.address from your wallet

// Provision credentials for each agent
const fleet = await ps.fleet.provision({ poolAddress: pool.address, count: 10 });
// fleet[0], fleet[1], ... → credential strings, one per agent
```

## 合约执行机制

在USDC资金转移之前，Base链上的PaySpawn V5智能合约会检查以下条件：

- 如果超过每日限额 → 交易将被撤销
- 如果交易金额超过单笔交易限额 → 交易将被撤销
- 如果收款人不在白名单内 → 交易将被撤销

该系统不支持通过API进行任何修改，也没有配置选项。所有计算都会在每次交易前自动执行。

**智能合约地址（Base主网）：** `0xaa8e6815b0E8a3006DEe0c3171Cf9CA165fd862e`  
**USDC地址（Base链）：** `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

## 相关链接：

- [payspawn.ai](https://payspawn.ai)
- [payspawn.ai/dashboard](https://payspawn.ai/dashboard)
- [@payspawn](https://x.com/payspawn)
- [npm: @payspawn/sdk](https://www.npmjs.com/package/@payspawn/sdk)