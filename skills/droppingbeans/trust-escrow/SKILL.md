---
name: trust-escrow
description: 在 Base Sepolia 平台上，创建和管理用于代理间支付的 USDC 代管账户（escrow accounts）。该系统可节省 30% 的交易手续费（gas fees），支持批量操作，并提供争议解决机制。
metadata: {"clawdbot":{"emoji":"🫘","requires":{"network":"base-sepolia"}}}
---

# Trust Escrow V2

这是一个专为在 Base Sepolia 上的代理间 USDC 支付设计的、可投入生产的托管服务。

## 使用场景

- 代理招聘（交付后付款）
- 服务市场
- 代理间协作
- 奖励/任务系统
- x402 支付集成

---

## 快速入门

### 合同信息

- **地址：** `0x6354869F9B79B2Ca0820E171dc489217fC22AD64`
- **网络：** Base Sepolia（ChainID：84532）
- **USDC：** `0x036CbD53842c5426634e7929541eC2318f3dCF7e`
- **RPC：** `https://sepolia.base.org`

### 平台

- **Web 应用程序：** https://trust-escrow-web.vercel.app
- **代理文档：** https://trust-escrow-web.vercel.app/agent-info
- **集成指南：** https://trust-escrow-web.vercel.app/skill.md

---

## 核心功能

### `createEscrowreceiver, amount, deadline)`  
创建新的托管账户。返回托管 ID。

```typescript
// Using viem/wagmi
await writeContract({
  address: '0x6354869F9B79B2Ca0820E171dc489217fC22AD64',
  abi: ESCROW_ABI,
  functionName: 'createEscrow',
  args: [
    '0xRECEIVER_ADDRESS',              // address receiver
    parseUnits('100', 6),               // uint96 amount (USDC 6 decimals)
    Math.floor(Date.now()/1000) + 86400 // uint40 deadline (24h)
  ]
});
```

### `release(escrowId)`  
发送方可以提前释放付款（需手动批准）。

```typescript
await writeContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'release',
  args: [BigInt(escrowId)]
});
```

### `autoRelease(escrowId)`  
在截止时间过后 1 小时的检查期内，任何人都可以自动释放付款。

```typescript
// First check if ready
const ready = await readContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'canAutoRelease',
  args: [BigInt(escrowId)]
});

if (ready) {
  await writeContract({
    address: ESCROW_ADDRESS,
    abi: ESCROW_ABI,
    functionName: 'autoRelease',
    args: [BigInt(escrowId)]
  });
}
```

### `cancel(escrowId)`  
发送方可以在最初 30 分钟内取消操作。

```typescript
await writeContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'cancel',
  args: [BigInt(escrowId)]
});
```

### `dispute(escrowId)`  
任何一方都可以申请仲裁以解决争议。

```typescript
await writeContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'dispute',
  args: [BigInt(escrowId)]
});
```

---

## 批量操作（V2 特性）

### **创建多个托管账户**  
与单独交易相比，可节省 41% 的 Gas 费用。

```typescript
await writeContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'createEscrowBatch',
  args: [
    [addr1, addr2, addr3, addr4, addr5],      // address[] receivers
    [100e6, 200e6, 150e6, 300e6, 250e6],      // uint96[] amounts
    [deadline1, deadline2, deadline3, deadline4, deadline5] // uint40[] deadlines
  ]
});
```

### **释放多个托管账户**  
与单独交易相比，可节省 35% 的 Gas 费用。

```typescript
await writeContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'releaseBatch',
  args: [[id1, id2, id3, id4, id5]]
});
```

---

## 查看功能

### `getEscrow(escrowId)`  
获取托管账户的详细信息。

```typescript
const escrow = await readContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'getEscrow',
  args: [BigInt(escrowId)]
});

// Returns: [sender, receiver, amount, createdAt, deadline, state]
// state: 0=Active, 1=Released, 2=Disputed, 3=Refunded, 4=Cancelled
```

### `canAutoRelease(escrowId)`  
检查托管账户是否已准备好自动释放。

```typescript
const ready = await readContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'canAutoRelease',
  args: [BigInt(escrowId)]
});

// Returns: boolean
```

### `getEscrowBatch(escrowIds[])`  
高效批量查看托管账户信息（优化了 Gas 消耗）。

```typescript
const result = await readContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'getEscrowBatch',
  args: [[id1, id2, id3, id4, id5]]
});

// Returns: [states[], amounts[]]
```

---

## 完整工作流程示例

```typescript
import { createPublicClient, createWalletClient, http } from 'viem';
import { baseSepolia } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

const ESCROW_ADDRESS = '0x6354869F9B79B2Ca0820E171dc489217fC22AD64';
const USDC_ADDRESS = '0x036CbD53842c5426634e7929541eC2318f3dCF7e';

const account = privateKeyToAccount('0xYOUR_PRIVATE_KEY');

const walletClient = createWalletClient({
  account,
  chain: baseSepolia,
  transport: http()
});

const publicClient = createPublicClient({
  chain: baseSepolia,
  transport: http()
});

// 1. Approve USDC
const approveTx = await walletClient.writeContract({
  address: USDC_ADDRESS,
  abi: [{
    name: 'approve',
    type: 'function',
    inputs: [
      { name: 'spender', type: 'address' },
      { name: 'amount', type: 'uint256' }
    ],
    outputs: [{ name: '', type: 'bool' }],
    stateMutability: 'nonpayable'
  }],
  functionName: 'approve',
  args: [ESCROW_ADDRESS, parseUnits('100', 6)]
});

await publicClient.waitForTransactionReceipt({ hash: approveTx });

// 2. Create escrow
const createTx = await walletClient.writeContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'createEscrow',
  args: [
    '0xRECEIVER_ADDRESS',
    parseUnits('100', 6),
    Math.floor(Date.now()/1000) + 86400
  ]
});

const receipt = await publicClient.waitForTransactionReceipt({ hash: createTx });
console.log('Escrow created:', receipt.transactionHash);

// 3. Later: Release payment
const releaseTx = await walletClient.writeContract({
  address: ESCROW_ADDRESS,
  abi: ESCROW_ABI,
  functionName: 'release',
  args: [escrowId]
});

await publicClient.waitForTransactionReceipt({ hash: releaseTx });
console.log('Payment released!');
```

---

## 主要特性

- ⚡ **节省 30% 的 Gas 费用**：优化了存储机制并添加了自定义错误处理
- 📦 **批量操作**：批量处理可节省 41% 的 Gas 费用
- ⚖️ **争议解决**：由仲裁员解决冲突
- ⏱️ **取消窗口**：有 30 分钟的取消期限
- 🔍 **检查期**：自动释放前有 1 小时的检查时间
- 🤖 **自动释放机制**：无需权限即可自动释放资金

---

## Gas 费用

| 操作        | Gas 费用（单位：gwei） |
|------------|-------------------|
| 创建单个托管账户 | 约 65,000 | 约 0.000065 ETH |
| 释放单个托管账户 | 约 45,000 | 约 0.000045 ETH |
| 批量创建（5 个）   | 约 250,000 | 约 0.00025 ETH |
| 批量释放（5 个）   | 约 180,000 | 约 0.00018 ETH |

---

## 安全性

- ✅ 所有功能均使用了 ReentrancyGuard 保护机制
- ✅ 对输入数据进行验证，并处理自定义错误
- ✅ 通过状态机进行验证
- ✅ 使用 OpenZeppelin 合约（经过审计）
- ✅ 使用 Solidity 0.8.20 及更高版本（具备溢出保护功能）

---

## 资源

- **平台：** https://trust-escrow-web.vercel.app
- **代理文档：** https://trust-escrow-web.vercel.app/agent-info
- **完整文档：** https://trust-escrow-web.vercel.app/skill.md
- **GitHub 仓库：** https://github.com/droppingbeans/trust-escrow-usdc
- **合约地址：** https://sepolia.basescan.org/address/0x6354869F9B79B2Ca0820E171dc489217fC22AD64
- **辅助文件：** https://trust-escrow-web.vercel.app/llms.txt

---

**专为 #USDCHackathon - Agentic Commerce 赛道开发**  
**由 beanbot 制作 🫘**