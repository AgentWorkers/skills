---
name: stakingverse-lukso
description: 在 Stakingverse（LUKSO 液态质押平台）上进行 LYX 代币的质押操作。适用于用户需要质押或赎回 LYX 代币、领取奖励，或查看在 Stakingverse 上的 SLYX 代币余额的场景。该平台支持代币的存入、提取请求，以及基于预言机（oracle）的奖励领取机制。
---
# Stakingverse LUKSO 持币奖励技能

在 Stakingverse 上质押 LYX 以获得 sLYX（流动性质押代币），同时保持资产的流动性，并享受约 8% 的年化收益率（APY）。

## 该技能的功能

- **质押 LYX** → 立即获得 sLYX 代币
- **请求解质押** → 启动取款流程（需要经过预言机处理）
- **领取解质押的 LYX** → 预言机处理完取款请求后
- **查看 sLYX 余额** → 查看您的质押状况
- **查看可领取的 LYX** → 查看取款是否已准备好领取

## 所需凭证

请设置以下环境变量或编辑相关脚本：

```bash
export STAKINGVERSE_VAULT="0x9F49a95b0c3c9e2A6c77a16C177928294c0F6F04"
export MY_UP="your_universal_profile_address"
export CONTROLLER="your_controller_address"
export PRIVATE_KEY="your_controller_private_key"
export RPC_URL="https://rpc.mainnet.lukso.network"
```

## 快速入门

```bash
# Stake 10 LYX
node scripts/stake.js 10

# Check sLYX balance
node scripts/balance.js

# Request unstake of 5 sLYX
node scripts/unstake-request.js 5

# Check if withdrawal is ready
node scripts/check-claim.js

# Claim unstaked LYX (after oracle processes)
node scripts/claim.js
```

## 工作原理

### Stakingverse 的架构

Stakingverse 是一个基于 LUKSO 的流动性质押协议：

- **您质押 LYX** → 获得 sLYX 代币（1:1 的比例）
- **sLYX 代币增值** → 随着质押奖励的累积，1 sLYX 的价值会超过 1 LYX
- **sLYX 具有流动性** → 可以在去中心化金融（DeFi）环境中进行交易、转账或使用
- **解质押分为两步** → 提出解质押请求 → 等待预言机处理 → 领取解质押的代币

### 关键合约

| 合约 | 地址 | 功能 |
|----------|---------|---------|
| Vault | `0x9F49a95b0c3c9e2A6c77a16C177928294c0F6F04` | 质押/解质押逻辑处理 |
| sLYX 代币 | `0x8a3982f4abcdc30f777910e8b5b5d8242628290a` | 流动性质押代币（LSP7 标准） |
| Oracle | 多个预言机地址 | 验证取款请求 |

### 质押流程

```
You (Controller)
    ↓
KeyManager.execute()
    ↓
UP.execute(CALL, Vault, 10 LYX, deposit())
    ↓
Vault receives LYX
    ↓
Vault mints sLYX to your UP
    ↓
You hold sLYX (earning rewards)
```

### 解质押流程（两步）

```
Step 1: Request Withdrawal
    You (Controller)
        ↓
    KeyManager.execute()
        ↓
    UP.execute(CALL, Vault, 0, withdraw(sLYX_amount))
        ↓
    Vault burns sLYX
        ↓
    Oracle queue: withdrawal request created

Step 2: Wait for Oracle
    ↓ (Time passes - oracle processes)

Step 3: Claim LYX
    You (Controller)
        ↓
    KeyManager.execute()
        ↓
    UP.execute(CALL, Vault, 0, claim())
        ↓
    Oracle approves
        ↓
    Vault sends LYX to your UP
```

## 详细使用方法

### 质押 LYX

```javascript
const { ethers } = require('ethers');

// Setup
const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

// Vault ABI (minimal)
const VAULT_ABI = [
  'function deposit() external payable',
  'function balanceOf(address) view returns (uint256)'
];

const LSP0_ABI = [
  'function execute(uint256 operation, address target, uint256 value, bytes calldata data) external'
];

const LSP6_ABI = [
  'function execute(bytes calldata payload) external payable returns (bytes memory)'
];

// Amount to stake
const stakeAmount = ethers.parseEther('10'); // 10 LYX

// Encode deposit call on Vault
const vaultInterface = new ethers.Interface(VAULT_ABI);
const depositData = vaultInterface.encodeFunctionData('deposit');

// Encode execute call on UP
const upInterface = new ethers.Interface(LSP0_ABI);
const executeData = upInterface.encodeFunctionData('execute', [
  0,                      // operation: CALL
  process.env.STAKINGVERSE_VAULT,  // target: Vault
  stakeAmount,            // value: LYX to stake
  depositData             // data: deposit()
]);

// Send via KeyManager
const keyManager = new ethers.Contract(process.env.KEY_MANAGER, LSP6_ABI, wallet);
const tx = await keyManager.execute(executeData);
const receipt = await tx.wait();

console.log(`Staked ${ethers.formatEther(stakeAmount)} LYX`);
console.log(`Transaction: ${receipt.hash}`);
```

### 查看 sLYX 余额

```javascript
const SLYX_ABI = ['function balanceOf(address) view returns (uint256)'];

const slyx = new ethers.Contract(
  '0x8a3982f4abcdc30f777910e8b5b5d8242628290a',
  SLYX_ABI,
  provider
);

const balance = await slyx.balanceOf(process.env.MY_UP);
console.log(`sLYX Balance: ${ethers.formatEther(balance)}`);
```

### 请求解质押

```javascript
const amountToUnstake = ethers.parseEther('5'); // 5 sLYX

// Encode withdraw call on Vault
const withdrawData = vaultInterface.encodeFunctionData('withdraw', [amountToUnstake]);

// Encode execute call on UP
const executeData = upInterface.encodeFunctionData('execute', [
  0,                              // operation: CALL
  process.env.STAKINGVERSE_VAULT, // target: Vault
  0,                              // value: 0 (no ETH sent)
  withdrawData                    // data: withdraw(amount)
]);

// Send via KeyManager
const tx = await keyManager.execute(executeData);
await tx.wait();

console.log(`Unstake requested for ${ethers.formatEther(amountToUnstake)} sLYX`);
console.log('Wait for oracle processing, then run claim.js');
```

### 查看可领取的 LYX

```javascript
const VAULT_FULL_ABI = [
  'function getClaimableAmount(address) view returns (uint256)',
  'function getPendingWithdrawals(address) view returns (uint256)'
];

const vault = new ethers.Contract(
  process.env.STAKINGVERSE_VAULT,
  VAULT_FULL_ABI,
  provider
);

const claimable = await vault.getClaimableAmount(process.env.MY_UP);
const pending = await vault.getPendingWithdrawals(process.env.MY_UP);

console.log(`Claimable LYX: ${ethers.formatEther(claimable)}`);
console.log(`Pending withdrawals: ${ethers.formatEther(pending)}`);
```

### 领取解质押的 LYX

```javascript
// Encode claim call on Vault (no parameters)
const claimData = vaultInterface.encodeFunctionData('claim');

// Encode execute call on UP
const executeData = upInterface.encodeFunctionData('execute', [
  0,
  process.env.STAKINGVERSE_VAULT,
  0,
  claimData
]);

// Send via KeyManager
const tx = await keyManager.execute(executeData);
const receipt = await tx.wait();

console.log(`Claimed LYX to your UP`);
console.log(`Transaction: ${receipt.hash}`);
```

## 交易流程参考

所有交易必须遵循以下流程：

### 标准模式：KeyManager → UP → 目标地址

```javascript
// 1. Encode the target contract call
const targetData = targetInterface.encodeFunctionData('functionName', [args]);

// 2. Encode UP.execute() wrapper
const upData = upInterface.encodeFunctionData('execute', [
  0,              // operation type (0 = CALL)
  targetAddress,  // target contract
  value,          // LYX to send (0 for most calls)
  targetData      // encoded function call
]);

// 3. Send via KeyManager
const tx = await keyManager.execute(upData);
```

## 常见问题

### “权限不足”
- 您的控制器需要 `CALL` 和 `TRANSFERVALUE` 权限
- 检查：`keyManager.getPermissions(controllerAddress)`

### “取款未准备好”
- 预言机尚未处理您的请求
- 在调用 `claim()` 函数前，请先查看可领取的代币数量
- 取款可能需要数小时，具体取决于预言机的处理速度

### “金额无效”
- 尝试解质押的 sLYX 代币数量超过了您实际拥有的数量
- 请先查看余额：`sLYX.balanceOf(UP_ADDRESS)`

## 重要说明

- **年化收益率（APY）会变化**：目前约为 8%，但会根据网络状况进行调整
- **sLYX 代币遵循 LSP7 标准**：具有可互换性（类似于 ERC20）
- **奖励自动复利**：sLYX 代币的价值会自动增长，无需手动领取
- **依赖预言机**：为确保安全性，解质押需要预言机的验证
- **Gas 费用**：所有交易费用由控制器承担

## 相关资源

- Stakingverse 应用程序：https://app.stakingverse.io
- Stakingverse 文档：https://docs.stakingverse.io
- LUKSO 文档：https://docs.lukso.tech
- sLYX 代币地址：`0x8a3982f4abcdc30f777910e8b5b5d8242628290a`