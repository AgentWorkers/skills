---
name: jb-suckers
description: |
  Juicebox V5 sucker contracts for cross-chain token bridging. Use when: (1) implementing bridge
  functionality, (2) understanding prepare/toRemote/claim flow, (3) working with merkle proofs for
  cross-chain claims, (4) querying sucker pairs from registry, (5) handling emergency exits,
  (6) debugging "claimable" vs "pending" states, (7) encoding sucker transaction calldata.
  Covers JBSucker, JBOptimismSucker, JBArbitrumSucker, JBCCIPSucker, and JBSuckerRegistry.
---

# Juicebox V5 Suckers - 跨链代币桥接

## 问题

要在不同区块链之间桥接项目代币，并同时保持它们对应的储备金比例，需要理解一个复杂的三阶段协议，该协议涉及默克尔证明（Merkle proofs）、特定于区块链的地址映射表（AMBs）以及精细的状态管理。

## 使用场景

在以下情况下需要运用这些知识：
- 构建跨链桥接用户界面（UIs）
- 编码 `prepare()`、`toRemote()` 或 `claim()` 交易
- 查询待处理或可领取的桥接交易
- 从 Juicerkle 获取默克尔证明
- 查明桥接为何处于“待处理”状态
- 实现紧急退出机制
- 使用 JBSuckerRegistry 查找桥接路径

## 解决方案

### 什么是 Suckers？

Suckers 是专门的桥接合约，用于**连接不同区块链上的 Juicebox 项目**，并在它们之间传输项目代币及其对应的储备金。

**为什么需要 Suckers？**：项目 ID 在不同区块链上是独立分配的——例如，在以太坊上可能分配到项目 ID #42，在 Optimism 上可能分配到项目 ID #17。Suckers 将这些独立的项目连接起来，使它们能够作为一个统一的“多链项目”进行代币桥接。

与标准代币桥接器不同：
- 代币在源链上通过“现金提取”（cash-out）方式被销毁
- 代币转移时，相应的 ETH/USDC 也会按比例转移
- 接收方会在目标链上收到新生成的代币
- 储备金价值会随代币的转移而变化

### 三阶段桥接流程

```
PHASE 1: PREPARE (Source Chain)
┌─────────────────────────────────────────────────────────────┐
│ User calls: sucker.prepare(                                  │
│   projectTokenCount,  // Amount to bridge                   │
│   beneficiary,        // Recipient on remote chain          │
│   minTokensReclaimed, // Slippage protection                │
│   token               // Terminal token (ETH/USDC address)  │
│ )                                                           │
│                                                             │
│ What happens:                                               │
│ 1. Project tokens transferred from user to sucker           │
│ 2. Sucker calls terminal.cashOutTokensOf()                  │
│ 3. Receives proportional ETH/USDC from treasury             │
│ 4. Creates leaf in outbox merkle tree                       │
│ 5. Emits InsertToOutboxTree event                          │
│                                                             │
│ Status: PENDING                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
PHASE 2: EXECUTE (Cross-Chain Message)
┌─────────────────────────────────────────────────────────────┐
│ User/Relayer calls: sucker.toRemote(token)                  │
│                                                             │
│ What happens:                                               │
│ 1. Computes merkle root of all pending outbox leaves        │
│ 2. Increments nonce                                         │
│ 3. Sends JBMessageRoot via AMB:                             │
│    - OP Stack: IOPMessenger.sendMessage()                   │
│    - Arbitrum: IInbox.unsafeCreateRetryableTicket()         │
│    - CCIP: ICCIPRouter.ccipSend()                          │
│ 4. Transfers ETH/tokens to peer sucker                      │
│ 5. Emits RootToRemote event                                │
│                                                             │
│ Status: CLAIMABLE (on destination)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
PHASE 3: CLAIM (Destination Chain)
┌─────────────────────────────────────────────────────────────┐
│ User calls: peerSucker.claim(claimData)                     │
│                                                             │
│ claimData = {                                               │
│   token: address,                                           │
│   leaf: { index, beneficiary, projectTokenCount,            │
│           terminalTokenAmount },                            │
│   proof: bytes32[32]  // Merkle proof from Juicerkle        │
│ }                                                           │
│                                                             │
│ What happens:                                               │
│ 1. Validates merkle proof against inbox root                │
│ 2. Checks leaf not already executed (prevents double-spend) │
│ 3. Marks leaf as executed in bitmap                         │
│ 4. Mints project tokens to beneficiary                      │
│ 5. Adds terminal tokens to project balance                  │
│ 6. Emits Claimed event                                      │
│                                                             │
│ Status: CLAIMED                                             │
└─────────────────────────────────────────────────────────────┘
```

### 关键合约

| 合约 | 功能 |
|----------|---------|
| `JBSucker` | 包含核心桥接逻辑的抽象基类 |
| `JBOptimismSucker` | 用于 Optimism 和 Base 链路的桥接 |
| `JBArbitrumSucker` | 用于 Arbitrum 链路的消息传递 |
| `JBCCIPSucker` | 用于 L2 链路之间的跨链通信（CCIP） |
| `JBSuckerRegistry` | 负责部署和跟踪桥接对（bridge pairs） |

### 查询桥接对信息

```javascript
// Get all bridge destinations for a project
const pairs = await publicClient.readContract({
  address: JB_SUCKER_REGISTRY,
  abi: [{
    name: 'suckerPairsOf',
    type: 'function',
    inputs: [{ name: 'projectId', type: 'uint256' }],
    outputs: [{
      name: 'pairs',
      type: 'tuple[]',
      components: [
        { name: 'local', type: 'address' },
        { name: 'remote', type: 'address' },
        { name: 'remoteChainId', type: 'uint256' }
      ]
    }],
    stateMutability: 'view'
  }],
  functionName: 'suckerPairsOf',
  args: [projectId]
});

// pairs = [
//   { local: '0x...', remote: '0x...', remoteChainId: 10n },
//   { local: '0x...', remote: '0x...', remoteChainId: 8453n }
// ]
```

### 编码交易

**准备阶段（Step 1）：**
```javascript
import { encodeFunctionData } from 'viem';

const prepareData = encodeFunctionData({
  abi: [{
    name: 'prepare',
    type: 'function',
    inputs: [
      { name: 'projectTokenCount', type: 'uint256' },
      { name: 'beneficiary', type: 'address' },
      { name: 'minTokensReclaimed', type: 'uint256' },
      { name: 'token', type: 'address' }
    ],
    outputs: [],
    stateMutability: 'nonpayable'
  }],
  functionName: 'prepare',
  args: [
    parseUnits('100', 18),     // 100 project tokens
    beneficiaryAddress,
    parseUnits('0.9', 18),     // 10% slippage allowed
    NATIVE_TOKEN               // 0xEEEE...EEEe for ETH
  ]
});

// Send transaction
await walletClient.sendTransaction({
  to: suckerAddress,
  data: prepareData
});
```

**执行阶段（Step 2）：**
```javascript
// Estimate fee via simulation (binary search)
async function estimateBridgeFee(sucker, token) {
  let low = 0n;
  let high = parseUnits('0.04', 18);

  for (let i = 0; i < 10; i++) {
    const mid = (low + high) / 2n;
    try {
      await publicClient.simulateContract({
        address: sucker,
        abi: SUCKER_ABI,
        functionName: 'toRemote',
        args: [token],
        value: mid
      });
      high = mid; // Success - try lower
    } catch {
      low = mid;  // Failed - try higher
    }
  }
  return (high * 110n) / 100n; // Add 10% buffer
}

const fee = await estimateBridgeFee(suckerAddress, NATIVE_TOKEN);

const toRemoteData = encodeFunctionData({
  abi: [{
    name: 'toRemote',
    type: 'function',
    inputs: [{ name: 'token', type: 'address' }],
    outputs: [],
    stateMutability: 'payable'
  }],
  functionName: 'toRemote',
  args: [NATIVE_TOKEN]
});

await walletClient.sendTransaction({
  to: suckerAddress,
  data: toRemoteData,
  value: fee
});
```

**领取阶段（Step 3）：**
```javascript
// Fetch proof from Juicerkle
const JUICERKLE_API = 'https://juicerkle-production.up.railway.app';

// NOTE: Addresses must be lowercase for Juicerkle API
const proofResponse = await fetch(`${JUICERKLE_API}/claims`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    chainId: destinationChainId,
    sucker: peerSuckerAddress.toLowerCase(),
    token: NATIVE_TOKEN.toLowerCase(),
    beneficiary: userAddress.toLowerCase()
  })
});

// Response uses PascalCase
// interface JuicerkleClaim {
//   Token: string;
//   Leaf: { Index, Beneficiary, ProjectTokenCount, TerminalTokenAmount };
//   Proof: number[][]; // Array of 32-byte arrays
// }
const proofs = await proofResponse.json();
const claim = proofs[0];

// Convert Proof from number[][] to bytes32[]
const proofBytes = claim.Proof.map(arr => {
  const hex = arr.map(b => b.toString(16).padStart(2, '0')).join('');
  return `0x${hex}`;
});

const claimData = encodeFunctionData({
  abi: [{
    name: 'claim',
    type: 'function',
    inputs: [{
      name: 'claimData',
      type: 'tuple',
      components: [
        { name: 'token', type: 'address' },
        { name: 'leaf', type: 'tuple', components: [
          { name: 'index', type: 'uint256' },
          { name: 'beneficiary', type: 'address' },
          { name: 'projectTokenCount', type: 'uint256' },
          { name: 'terminalTokenAmount', type: 'uint256' }
        ]},
        { name: 'proof', type: 'bytes32[32]' }
      ]
    }],
    outputs: [],
    stateMutability: 'nonpayable'
  }],
  functionName: 'claim',
  args: [{
    token: claim.Token,
    leaf: {
      index: BigInt(claim.Leaf.Index),
      beneficiary: claim.Leaf.Beneficiary,
      projectTokenCount: BigInt(claim.Leaf.ProjectTokenCount),
      terminalTokenAmount: BigInt(claim.Leaf.TerminalTokenAmount)
    },
    proof: proofBytes
  }]
});

await walletClient.sendTransaction({
  to: peerSuckerAddress,
  data: claimData
});
```

### 查询桥接状态（Bendystraw）

```graphql
query SuckerTransactions($suckerGroupId: String!, $status: suckerTransactionStatus) {
  suckerTransactions(
    where: { suckerGroupId: $suckerGroupId, status: $status }
    orderBy: "createdAt"
    orderDirection: "desc"
  ) {
    items {
      id
      chainId
      peerChainId
      sucker
      peer
      beneficiary
      projectTokenCount
      terminalTokenAmount
      token
      status        # "pending" | "claimable" | "claimed"
      index
      root
      createdAt
    }
  }
}
```

### 状态转换

| 状态 | 含义 | 下一步操作 |
|--------|---------|-------------|
| `pending` | 准备完成但尚未发送 | 调用 `toRemote()` 方法 |
| `claimable` | 根节点已到达，等待领取 | 提供证明后调用 `claim()` 方法 |
| `claimed` | 桥接完成 | 无需进一步操作 |

### 紧急退出机制

如果桥接系统出现故障：

```javascript
// 1. Project owner enables emergency hatch
await ownerClient.writeContract({
  address: suckerAddress,
  abi: SUCKER_ABI,
  functionName: 'enableEmergencyHatchFor',
  args: [token]
});

// 2. Users can exit locally (no bridging)
// Retrieves funds from outbox without crossing chains
await userClient.writeContract({
  address: suckerAddress,
  abi: SUCKER_ABI,
  functionName: 'exitThroughEmergencyHatch',
  args: [claimData] // Same structure as claim()
});
```

### 代币映射

项目需要明确指定哪些代币可以进行桥接：

```javascript
const mapping = {
  localToken: USDC_MAINNET,
  remoteToken: USDC_OPTIMISM,
  minGas: 300000,        // Minimum gas for cross-chain call
  minBridgeAmount: 10e6  // Minimum 10 USDC to bridge
};

await ownerClient.writeContract({
  address: suckerAddress,
  abi: SUCKER_ABI,
  functionName: 'mapToken',
  args: [mapping]
});
```

### 特定链路的注意事项

**OP Stack（Optimism, Base）：**
- 使用原生的 OP Messenger 协议
- 费用最低（约 0.0005-0.002 ETH）
- 交易最终确认速度快

**Arbitrum：**
- 使用可重试的提交机制（Retryable Tickets）
- 动态计算交易费用（gas pricing）
- 需要计算 `maxSubmissionCost`

**CCIP（L2↔L2）：**
- 费用最高，但灵活性最高
- 支持任意支持 CCIP 的区块链之间的通信
- 适用于 Optimism ↔ Arbitrum、Base ↔ Arbitrum 之间的桥接

### Suckers 的退役计划

```
ENABLED → DEPRECATION_PENDING → SENDING_DISABLED → DEPRECATED
```

- `DEPRECATION_PENDING`：警告状态，仍可正常使用
- `SENDING_DISABLED`：无法创建新的桥接，但仍可领取代币
- `DEPRECATED`：仅允许使用紧急退出机制

## 验证步骤

1. 在桥接前检查 Sucker 的状态：`sucker.state()`
2. 验证代币是否已正确映射：`sucker.remoteTokenFor(localToken)`
3. 检查接收方的代币余额：`sucker.outboxOf(token).balance`
4. 在提交交易前通过 Juicerkle 验证领取证明

## 示例

**使用 React 完整实现桥接流程：**

```typescript
async function bridgeTokens({
  sourceChainId,
  destChainId,
  suckerAddress,
  amount,
  beneficiary
}: BridgeParams) {
  // 1. Approve project token
  await writeContract({
    address: projectToken,
    abi: erc20Abi,
    functionName: 'approve',
    args: [suckerAddress, amount]
  });

  // 2. Prepare
  await writeContract({
    address: suckerAddress,
    abi: suckerAbi,
    functionName: 'prepare',
    args: [amount, beneficiary, 0n, NATIVE_TOKEN]
  });

  // 3. Execute (can be batched with others)
  const fee = await estimateBridgeFee(suckerAddress, NATIVE_TOKEN);
  await writeContract({
    address: suckerAddress,
    abi: suckerAbi,
    functionName: 'toRemote',
    args: [NATIVE_TOKEN],
    value: fee
  });

  // 4. Wait for root to arrive (check Bendystraw)
  // 5. Claim on destination (separate transaction)
}
```

## 其他注意事项：

- 默克尔树的深度为 32，证明数据始终为 `bytes32[32]` 格式
- 随机数（nonces）是单调递增的，以防止重放攻击
- 每种代币都有独立的发送/接收树结构
- `addToBalanceMode` 可设置为 `MANUAL` 或 `ON_CLAIM`
- 通过执行叶子节点的位图（leaf bitmap）来防止双重支付
- 紧急退出机制使用独立的执行命名空间（execution namespace）

## 相关技能

- `/jb-omnichain-ui`：使用 Relayr 和 Bendystraw 构建多链 UI
- `/jb-v5-currency-types`：处理跨链项目的货币相关逻辑
- `/jb-bendystraw`：用于查询跨链数据