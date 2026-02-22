---
name: stakingverse-ethereum
description: 在StakeWise上进行ETH质押（Ethereum的流动性质押服务）。适用于用户需要质押ETH、解质押ETH或查看在StakeWise V3保管库中质押的资产情况的情况。该服务支持通过“keeper”进行状态更新，并能从子图（subgraph）中获取质押收益的证明（harvest proofs）。
---
# StakeWise以太坊质押技巧

在StakeWise V3平台上质押ETH，以获得osETH（一种流动性质押代币），同时保持您的ETH的流动性，并赚取质押奖励。

## 该技巧的功能

- **质押ETH** → 获得osETH代币（自动处理状态更新）
- **解质押ETH** → 将osETH兑换回ETH
- **查看质押情况** → 查看您的质押份额及获得的奖励
- **监控质押状态** → 检查是否需要更新保管者状态
- **查询收获证明** → 从Subgraph获取存款的Merkle证明

## 所需凭证

请设置以下环境变量或编辑相关脚本：

```bash
export STAKEWISE_VAULT="0x8A93A876912c9F03F88Bc9114847cf5b63c89f56"
export KEEPER="0x6B5815467da09DaA7DC83Db21c9239d98Bb487b5"
export PRIVATE_KEY="your_private_key"
export MY_ADDRESS="your_address"
export RPC_URL="https://ethereum-rpc.publicnode.com"
```

## 快速入门

```bash
# Stake 0.1 ETH (auto-handles state updates)
node scripts/stake.mjs 0.1

# Check staked position
node scripts/position.js

# Unstake 0.05 osETH
node scripts/unstake.js 0.05

# Check if state update required
node scripts/check-state.js
```

## StakeWise V3的工作原理

### 架构概述

StakeWise V3采用**保管者-预言机（Keeper-Oracle）模式**来进行状态更新：

```
User (EOA/UP)
    ↓
Vault Contract
    ↓
Keeper (Oracle) - Validates and processes rewards
    ↓
osETH Token - Liquid staking token
```

### 关键组件

| 组件 | 地址 | 功能 |
|-----------|---------|---------|
| 存储库（Vault） | `0x8A93A876912c9F03F88Bc9114847cf5b63c89f56` | 质押/解质押逻辑 |
| 保管者（Keeper） | `0x6B5815467da09DaA7DC83Db21c9239d98Bb487b5` | 负责状态更新的预言机 |
| osETH代币 | 每个存储库独立管理 | 流动性质押代币 |
| Subgraph | `https://graphs.stakewise.io/mainnet-a/subgraphs/name/stakewise/prod` | 用于获取收获证明和数据 |

### 状态更新机制

**为什么需要状态更新？**
- StakeWise通过验证者离线积累奖励
- 保管者定期将奖励“收获”并上传到链上
- 用户只能在状态更新后进行存款

**何时需要状态更新？**
```javascript
const vault = new ethers.Contract(vaultAddress, vaultAbi, provider);
const needsUpdate = await vault.isStateUpdateRequired();
// true = must update state before depositing
```

### 质押流程（包含状态更新）

```
Step 1: Check State
    User
      ↓
    vault.isStateUpdateRequired()
      ↓
    Returns: true (update needed)

Step 2: Query Subgraph for Harvest Params
    User
      ↓
    POST to StakeWise subgraph
      ↓
    Returns: rewardsRoot, reward, unlockedMevReward, proof[]

Step 3: Update State and Deposit
    User
      ↓
    vault.updateStateAndDeposit(harvestParams, receiver, referrer)
      ↓
    Keeper validates harvest
      ↓
    Vault mints osETH to receiver
      ↓
    User receives osETH
```

## 详细使用方法

### 质押ETH（包含状态更新的完整流程）

```javascript
import { ethers } from 'ethers';
import fetch from 'node-fetch';

// Setup
const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

// Vault ABI (minimal)
const VAULT_ABI = [
  'function isStateUpdateRequired() view returns (bool)',
  'function updateStateAndDeposit(tuple(bytes32 rewardsRoot, uint256 reward, uint256 unlockedMevReward, bytes32[] proof) harvestParams, address receiver, address referrer) external payable',
  'function deposit(address receiver, address referrer) external payable'
];

const vault = new ethers.Contract(
  process.env.STAKEWISE_VAULT,
  VAULT_ABI,
  wallet
);

// Amount to stake
const stakeAmount = ethers.parseEther('0.1'); // 0.1 ETH

// Step 1: Check if state update required
const needsUpdate = await vault.isStateUpdateRequired();
console.log('State update required:', needsUpdate);

if (needsUpdate) {
  // Step 2: Query subgraph for harvest params
  const subgraphQuery = {
    query: `
      query getHarvestProofs($vault: String!) {
        harvestProofs(
          where: { vault: $vault }
          orderBy: blockNumber
          orderDirection: desc
          first: 1
        ) {
          rewardsRoot
          reward
          unlockedMevReward
          proof
        }
      }
    `,
    variables: {
      vault: process.env.STAKEWISE_VAULT.toLowerCase()
    }
  };

  const response = await fetch('https://graphs.stakewise.io/mainnet-a/subgraphs/name/stakewise/prod', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subgraphQuery)
  });

  const data = await response.json();
  const harvestProof = data.data.harvestProofs[0];

  // Step 3: Call updateStateAndDeposit
  const harvestParams = {
    rewardsRoot: harvestProof.rewardsRoot,
    reward: BigInt(harvestProof.reward),
    unlockedMevReward: BigInt(harvestProof.unlockedMevReward),
    proof: harvestProof.proof
  };

  const tx = await vault.updateStateAndDeposit(
    harvestParams,
    process.env.MY_ADDRESS,  // receiver
    ethers.ZeroAddress,       // referrer (optional)
    { value: stakeAmount }
  );

  const receipt = await tx.wait();
  console.log(`Staked ${ethers.formatEther(stakeAmount)} ETH with state update`);
  console.log(`Transaction: ${receipt.hash}`);
} else {
  // Simple deposit (no state update needed)
  const tx = await vault.deposit(
    process.env.MY_ADDRESS,
    ethers.ZeroAddress,
    { value: stakeAmount }
  );

  const receipt = await tx.wait();
  console.log(`Staked ${ethers.formatEther(stakeAmount)} ETH`);
  console.log(`Transaction: ${receipt.hash}`);
}
```

### 查看质押情况

```javascript
const OSETH_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function convertToAssets(uint256 shares) view returns (uint256)'
];

// Get osETH token address from vault
const osEthAddress = await vault.osToken();
const osEth = new ethers.Contract(osEthAddress, OSETH_ABI, provider);

const osEthBalance = await osEth.balanceOf(process.env.MY_ADDRESS);
const underlyingEth = await osEth.convertToAssets(osEthBalance);

console.log(`osETH Balance: ${ethers.formatEther(osEthBalance)}`);
console.log(`Equivalent ETH: ${ethers.formatEther(underlyingEth)}`);
```

### 解质押ETH

```javascript
const VAULT_FULL_ABI = [
  'function redeem(uint256 shares, address receiver, address owner) returns (uint256 assets)',
  'function maxRedeem(address owner) view returns (uint256)'
];

const vaultFull = new ethers.Contract(
  process.env.STAKEWISE_VAULT,
  VAULT_FULL_ABI,
  wallet
);

// Check max redeemable
const maxShares = await vaultFull.maxRedeem(process.env.MY_ADDRESS);
console.log(`Max redeemable: ${ethers.formatEther(maxShares)} osETH`);

// Redeem shares for ETH
const sharesToRedeem = ethers.parseEther('0.05');
const tx = await vaultFull.redeem(
  sharesToRedeem,
  process.env.MY_ADDRESS,  // receiver
  process.env.MY_ADDRESS   // owner
);

const receipt = await tx.wait();
console.log(`Redeemed ${ethers.formatEther(sharesToRedeem)} osETH for ETH`);
console.log(`Transaction: ${receipt.hash}`);
```

## Subgraph查询

### 获取最新的收获证明

```javascript
const query = {
  query: `
    query {
      harvestProofs(
        orderBy: blockNumber
        orderDirection: desc
        first: 1
      ) {
        id
        vault
        rewardsRoot
        reward
        unlockedMevReward
        proof
        blockNumber
      }
    }
  `
};

const response = await fetch('https://graphs.stakewise.io/mainnet-a/subgraphs/name/stakewise/prod', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(query)
});

const data = await response.json();
console.log(data.data.harvestProofs[0]);
```

### 获取存储库状态

```javascript
const query = {
  query: `
    query {
      vaults(first: 1) {
        id
        address
        totalAssets
        totalShares
        apr
      }
    }
  `
};
```

## 常见问题

### “需要状态更新”
- 保管者尚未发布最近的奖励
- 从Subgraph查询最新的收获证明
- 使用`updateStateAndDeposit()`代替`deposit()`

### “收获证明无效”
- 证明可能已过期
- 在存款前务必立即查询Subgraph
- 证明是特定区块的

### “质押份额不足”
- 尝试兑换超过您实际拥有的osETH数量
- 检查余额：`osETH.balanceOf(yourAddress)`

### “存储库暂停”
- 可能处于紧急暂停状态
- 检查：`vault.paused()`
- 等待StakeWise团队解除暂停

## 重要说明

- **年化收益率（APY）**：根据以太坊验证者的奖励情况而定，通常为3-5%
- **osETH的重新基数调整**：随着奖励的积累，余额会自动增加
- **对保管者的依赖**：存款需要有效的状态（保管者必须处于活跃状态）
- **Gas费用**：状态更新所需的Gas费用高于普通存款
- **MEV奖励**：收获奖励中包含MEV提取奖励

## 相关资源

- StakeWise应用程序：https://app.stakewise.io
- StakeWise文档：https://docs.stakewise.io
- Subgraph：https://graphs.stakewise.io/mainnet-a/subgraphs/name/stakewise/prod
- 存储库（Vault）：`0x8A93A876912c9F03F88Bc9114847cf5b63c89f56`
- 保管者（Keeper）：`0x6B5815467da09DaA7DC83Db21c9239d98Bb487b5`