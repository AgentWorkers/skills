---
name: payspawn
description: "在不共享私钥的情况下，为链上的任何AI代理设置 spending limits（支出限制）。适用场景包括：  
(1) 代理需要支付 x402 API 的费用（如网络爬虫、搜索服务、AI 服务等）；  
(2) 为代理钱包设置每日/每笔交易的 USDC 支出上限；  
(3) 列出代理可以支付的合约；  
(4) 立即暂停恶意代理的支出行为；  
(5) 为代理团队配置访问凭据。  
该功能适用于基于 Base 主网的系统，并支持使用 USDC 进行支付。  
**不适用的场景**：  
- 法定货币支付；  
- 非 Base 主链系统；  
- 资金托管服务。"
metadata:
  {
    "openclaw": {
      "emoji": "🔐",
      "color": "#F65B1A"
    }
  }
---
# PaySpawn — 为 AI 代理设置链上消费限制

**PaySpawn** 为 OpenClaw 代理提供的是一个凭证（credential），而非原始的私钥。消费限制、白名单以及“停止支付”的功能都由基于 Base 的智能合约来执行——这一切都依赖于数学逻辑，而非代码实现。

## 快速入门

安装 SDK：

```bash
npm install @payspawn/sdk
```

将你的凭证设置为环境变量：

```
PAYSPAWN_CREDENTIAL=your_credential_from_dashboard
```

在 [payspawn.ai/dashboard](https://payspawn.ai/dashboard) 获取你的凭证：连接钱包、设置消费限制，然后复制凭证字符串。无需使用私钥。

---

## 基本用法

```typescript
import { PaySpawn } from "@payspawn/sdk";

const ps = new PaySpawn(process.env.PAYSPAWN_CREDENTIAL);

// Pay an x402 API automatically
const res = await ps.fetch("https://api.example.com/data");
const data = await res.json();

// Direct USDC payment
await ps.pay("recipient-wallet-address", 1.00);

// Check remaining balance
const { balance, remaining } = await ps.check();

// Kill switch — stops all spending instantly
await ps.agent.pause();
```

---

## 功能说明

- **每日消费上限**：代理每天可以花费的最大 USDC 数量。
- **单笔交易限额**：单次支付的最大金额。
- **地址白名单**：只有允许的对手方才能接收支付。
- **交易频率限制**：每小时允许的最大交易次数。
- **停止支付功能**：通过一次调用即可立即暂停所有支付操作。

---

## x402 自动支付功能

`ps.fetch()` 会自动处理 HTTP 402 错误（表示支付请求被拒绝）。代理调用相应的 API，PaySpawn 会在凭证规定的范围内完成支付，并返回结果：

```typescript
// Works with any x402-compatible API
const result = await ps.fetch("https://paid-api.example.com/endpoint", {
  method: "POST",
  body: JSON.stringify({ task: "do something" })
});
```

---

## 代理舰队（Agent Fleets）

你可以从一个共享的预算池中为多个代理配置资源：

```typescript
// Create a pool for multiple agents
const pool = await ps.pool.create({ totalBudget: 100, agentDailyLimit: 10 });

// Provision 10 agent credentials in one call
const fleet = await ps.fleet.provision({ poolAddress: pool.address, count: 10 });
```

使用同一个 API 调用，每个代理都会获得自己的凭证和每日消费限额。所有代理都从同一个共享预算池中取款。

---

## 为何选择使用 PaySpawn

使用原始私钥的代理具有无限访问权限；一旦出现错误或环境变量泄露，钱包中的资金可能会被耗尽。而 PaySpawn 提供的凭证具有以下优势：
- 消费限制由智能合约强制执行，而非软件本身。
- 即使凭证泄露，也无法超出每日消费上限。
- 如果尝试向未知地址支付，白名单会阻止该操作。
- 通过一次调用即可立即停止所有支付操作。

---

## 链接

- 控制台：[payspawn.ai/dashboard](https://payspawn.ai/dashboard)
- 文档：[payspawn.ai](https://payspawn.ai)
- X 社交媒体账号：[@payspawn](https://x.com/payspawn)