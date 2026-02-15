---
name: AGIRAILS Payments
version: 2.1.0
description: 官方 ACTP（Agent Commerce Transaction Protocol）SDK——专为 AI 代理设计的第一个无需信任的支付层。您可以通过基于区块链的安全 USDC 代管系统在 Base L2 平台上进行服务支付或接收付款。当代理需要支付、接收付款、查询交易状态或处理纠纷时，均可使用该 SDK。
author: AGIRAILS Inc.
homepage: https://agirails.io
repository: https://github.com/agirails/openclaw-skill
license: MIT
tags:
  - payments
  - blockchain
  - escrow
  - agent-commerce
  - base-l2
  - usdc
  - web3
keywords:
  - AI agent payments
  - trustless escrow
  - ACTP protocol
  - agent-to-agent commerce
  - USDC payments
metadata:
  openclaw:
    emoji: "💸"
    minVersion: "1.0.0"
    requires:
      env:
        - AGENT_PRIVATE_KEY
        - AGENT_ADDRESS
---

# AGIRAILS — 为AI代理提供去中心化的支付服务

通过基于区块链的安全USDC托管机制，让你的AI代理能够**支付服务费用**或**接收付款**。

## 🚀 快速入门

只需输入：“*向0xProvider支付10 USDC以获取翻译服务*”

代理将执行以下操作：
1. 初始化ACTP客户端
2. 创建包含托管功能的交易
3. 跟踪交易状态直至完成
4. 在需要时处理争议

---

## 先决条件

| 条件 | 检查 | 安装 |
|-------------|-------|---------|
| **Node.js 18+** | `node --version` | [nodejs.org](https://nodejs.org) |
| **私钥** | `echo $AGENT_PRIVATE_KEY` | 导出钱包私钥 |
| **USDC余额** | 检查钱包余额 | 通过[bridge.base.org](https://bridge.base.org)将USDC桥接到Base网络 |

### 环境变量

```bash
export AGENT_PRIVATE_KEY="0x..."   # Wallet private key
export AGENT_ADDRESS="0x..."       # Wallet address
```

> **注意：** SDK包含默认的RPC端点。对于高并发的生产环境，请通过[Alchemy](https://alchemy.com)或[QuickNode](https://quicknode.com)设置自己的RPC服务，并将`rpcUrl`传递给客户端配置文件。

### 安装

```bash
# TypeScript/Node.js
npm install @agirails/sdk

# Python
pip install agirails
```

---

## 工作原理

ACTP使用了一个包含区块链安全托管功能的**8状态机**：

```
Human/Agent requests service
        ↓
   INITIATED ──► Provider quotes price
        ↓
     QUOTED ──► Requester accepts, locks USDC
        ↓
   COMMITTED ──► Provider starts work
        ↓
  IN_PROGRESS ──► Provider delivers (REQUIRED step!)
        ↓
   DELIVERED ──► Dispute window (48h default)
        ↓
    SETTLED ◄── Manual release (requester calls releaseEscrow)

   DISPUTED ──► Mediator resolves (splits funds)
   CANCELLED ──► Refund to requester
```

### 关键保障机制

| 保障机制 | 说明 |
|-----------|-------------|
| **托管资金充足性** | 存款始终不低于活跃交易金额 |
| **状态单向性** | 状态只能向前推进，不能倒退 |
| **截止日期强制执行** | 过期后无法完成交易 |
| **争议处理** | 在结算前有48小时的争议提出窗口 |

---

## 动作

| 动作 | 执行者 | 说明 |
|--------|-----|-------------|
| `pay` | 请求方 | 进行简单支付（创建交易并锁定资金） |
| `checkStatus` | 任何用户 | 查询交易状态 |
| `createTransaction` | 请求方 | 使用自定义参数创建交易 |
| `linkEscrow` | 请求方 | 将资金锁定在托管账户中 |
| `transitionState` | 提供方 | 提供报价、开始交易或交付服务 |
| `releaseEscrow` | 请求方 | 向提供方释放资金 |
| `transitionState('DISPUTED')` | 任意一方 | 提出争议以寻求调解 |

---

## 请求方流程（支付服务费用）

### 简单支付

```typescript
import { ACTPClient } from '@agirails/sdk';

const client = await ACTPClient.create({
  mode: 'mainnet',
  privateKey: process.env.AGENT_PRIVATE_KEY!,
  requesterAddress: process.env.AGENT_ADDRESS!,
});

// One-liner payment
const result = await client.basic.pay({
  to: '0xProviderAddress',
  amount: '25.00',     // USDC
  deadline: '+24h',    // 24 hours from now
});

console.log(`Transaction: ${result.txId}`);
console.log(`State: ${result.state}`);
```

### 高级支付（完全控制）

```typescript
// 1. Create transaction
const txId = await client.standard.createTransaction({
  provider: '0xProviderAddress',
  amount: '100',  // 100 USDC (user-friendly)
  deadline: Math.floor(Date.now() / 1000) + 86400,
  disputeWindow: 172800,  // 48 hours
  serviceDescription: 'Translate 500 words to Spanish',
});

// 2. Lock funds in escrow
const escrowId = await client.standard.linkEscrow(txId);

// 3. Wait for delivery... then release
// ...wait for DELIVERED
await client.standard.releaseEscrow(escrowId);
```

---

## 提供方流程（接收付款）

```typescript
import { ethers } from 'ethers';
const abiCoder = ethers.AbiCoder.defaultAbiCoder();

// 1. Quote the job (encode amount as proof)
const quoteAmount = ethers.parseUnits('50', 6);
const quoteProof = abiCoder.encode(['uint256'], [quoteAmount]);
await client.standard.transitionState(txId, 'QUOTED', quoteProof);

// 2. Start work (REQUIRED before delivery!)
await client.standard.transitionState(txId, 'IN_PROGRESS');

// 3. Deliver with dispute window proof
const disputeWindow = 172800;  // 48 hours
const deliveryProof = abiCoder.encode(['uint256'], [disputeWindow]);
await client.standard.transitionState(txId, 'DELIVERED', deliveryProof);

// 4. Requester releases after dispute window (or earlier if satisfied)
```

**⚠️ 重要提示：** 在执行`DELIVERED`操作之前，必须先进入`IN_PROGRESS`状态。否则合约会拒绝`COMMITTED → DELIVERED`的交易。

---

## 证明编码

所有证明都必须是ABI编码的十六进制字符串：

| 交易状态 | 证明格式 | 示例 |
|------------|--------------|---------|
| QUOTED | `['uint256']` 金额 | `encode(['uint256'], [parseUnits('50', 6)])` |
| DELIVERED | `['uint256']` 争议处理窗口 | `encode(['uint256'], [172800])` |
| SETTLED (dispute) | `['uint256', 'uint256', 'address', 'uint256']` | `[reqAmt, provAmt, mediator, fee]` |

```typescript
import { ethers } from 'ethers';
const abiCoder = ethers.AbiCoder.defaultAbiCoder();

// Quote proof
const quoteProof = abiCoder.encode(['uint256'], [ethers.parseUnits('100', 6)]);

// Delivery proof
const deliveryProof = abiCoder.encode(['uint256'], [172800]);

// Resolution proof (mediator only)
const resolutionProof = abiCoder.encode(
  ['uint256', 'uint256', 'address', 'uint256'],
  [requesterAmount, providerAmount, mediatorAddress, mediatorFee]
);
```

---

## 查询状态

```typescript
const status = await client.basic.checkStatus(txId);

console.log(`State: ${status.state}`);
console.log(`Can dispute: ${status.canDispute}`);
```

---

## 争议处理

任何一方都可以在结算前提出争议：

```typescript
// Raise dispute
await client.standard.transitionState(txId, 'DISPUTED');

// Mediator resolves (admin only)
const resolution = abiCoder.encode(
  ['uint256', 'uint256', 'address', 'uint256'],
  [
    ethers.parseUnits('30', 6),   // requester gets 30 USDC
    ethers.parseUnits('65', 6),   // provider gets 65 USDC
    mediatorAddress,
    ethers.parseUnits('5', 6),    // mediator fee
  ]
);
await client.standard.transitionState(txId, 'SETTLED', resolution);
```

---

## 协议费用

| 费用类型 | 费用金额 |
|----------|--------|
| 平台费用 | 交易金额的1% |
| 最低费用 | 0.05 USDC |
| 最高限额 | 5%（由社区决定） |

提供方获得的费用：`金额 - (金额 * 0.01) + 最低费用`

---

## 客户端模式

| 模式 | 网络 | 适用场景 |
|------|---------|----------|
| `mock` | 本地模拟环境 | 开发、测试 |
| `testnet` | Base Sepolia网络 | 集成测试 |
| `mainnet` | Base主网 | 生产环境 |

```typescript
// Development
const client = await ACTPClient.create({
  mode: 'mock',
  requesterAddress: '0x...',
});
await client.mintTokens('0x...', '1000000000');  // Mint test USDC

// Production
const client = await ACTPClient.create({
  mode: 'mainnet',
  privateKey: process.env.AGENT_PRIVATE_KEY!,
  requesterAddress: process.env.AGENT_ADDRESS!,
});
```

---

## 错误处理

```typescript
import {
  InsufficientFundsError,
  InvalidStateTransitionError,
  DeadlineExpiredError,
} from '@agirails/sdk';

try {
  await client.basic.pay({...});
} catch (error) {
  if (error instanceof InsufficientFundsError) {
    console.log(error.message);
  } else if (error instanceof InvalidStateTransitionError) {
    console.log(`Invalid state transition`);
  }
}
```

---

## Python示例

```python
import asyncio
import os
from agirails import ACTPClient

async def main():
    client = await ACTPClient.create(
        mode="mainnet",
        private_key=os.environ["AGENT_PRIVATE_KEY"],
        requester_address=os.environ["AGENT_ADDRESS"],
    )

    result = await client.basic.pay({
        "to": "0xProviderAddress",
        "amount": "25.00",
        "deadline": "24h",
    })

    print(f"Transaction: {result.tx_id}")
    print(f"State: {result.state}")

asyncio.run(main())
```

---

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| `COMMITTED → DELIVERED` 交易被回滚 | 缺少`IN_PROGRESS`状态 | 首先需要执行`transitionState(txId, 'IN_PROGRESS')` |
| 证明编码错误 | 编码错误 | 使用`ethers.AbiCoder`并确保类型正确 |
| 余额不足 | USDC不足 | 通过[bridge.base.org](https://bridge.base.org)将USDC桥接到Base网络 |
| 到期时间已过 | 处理速度过慢 | 创建新的交易并设置更长的截止日期 |

---

## 文件说明

| 文件 | 用途 |
|------|---------|
| `{baseDir}/references/requester-template.md` | 完整的请求方代理模板 |
| `{baseDir}/references/provider-template.md` | 完整的提供方代理模板 |
| `{baseDir}/references/state-machine.md` | 详细的状态转换逻辑 |
| `{baseDir}/examples/simple-payment.md` | 简单支付示例 |
| `{baseDir}/examples/full-lifecycle.md` | 完整的交易生命周期示例 |

---

## 与OpenClaw的集成

为OpenClaw代理提供了即用型模板。

### 快速设置（5分钟）

```bash
# Run setup script
bash {baseDir}/scripts/setup.sh

# Add agent config to openclaw.json (see agent-config.json)
# Set environment variables
# Restart OpenClaw
```

详细指南请参见 `{baseDir}/openclaw/QUICKSTART.md`。

### OpenClaw相关文件

| 文件 | 用途 |
|------|---------|
| `{baseDir}/openclaw/QUICKSTART.md` | 5分钟快速设置指南 |
| `{baseDir}/openclaw/agent-config.json` | 即用型代理配置文件 |
| `{baseDir}/openclaw/SOUL-treasury.md` | 买家代理模板 |
| `{baseDir}/openclaw/SOUL-provider.md` | 卖家代理模板 |
| `{baseDir}/openclaw/cron-examples.json` | 自动化任务脚本 |
| `{baseDir}/openclaw/validation-patterns.md` | 交付验证工具 |
| `{baseDir}/openclaw/security-checklist.md` | 上线前的安全审计检查 |

### 脚本

| 脚本 | 用途 |
|--------|---------|
| `{baseDir}/scripts/setup.sh` | 自动化工作区设置 |
| `{baseDir}/scripts/test-balance.ts` | 检查钱包余额 |
| `{baseDir}/scripts/test-purchase.ts` | 在测试网上进行购买测试 |

---

## 资源链接

- **文档**：https://docs.agirails.io
- **SDK仓库**：https://github.com/agirails/sdk
- **Discord频道**：https://discord.gg/nuhCt75qe4
- **支持邮箱**：support@agirails.io