---
name: omp-memory
description: OpenClaw内存协议（OMP）——用于在BSC区块链上存储和检索加密文件，并提供基于工作量证明（PoW）的挖矿奖励。当用户希望将文件存储在链上、检索已存储的文件、查看MMP代币余额、管理存储费用，或与BSC主网上的OMP协议进行交互时，可以使用该协议。
---
# OMP内存协议

这是一个基于BSC（Binance Smart Chain）的链上加密文件存储系统。文件被分割成256KB的块，经过Merkle哈希处理后存储，并带有基于租金的过期机制。矿工通过托管数据来赚取MMP代币。

## 设置（首次使用）

```bash
# 1. Install dependencies
cd ~/.omp-client && npm install

# 2. Create encrypted wallet
node bin/cli.js init
# → saves wallet to ~/.omp/wallet.json

# 3. Check MMP balance / get top-up info
node bin/cli.js topup
```

## 主要命令

### 存储文件
```bash
node bin/cli.js save <file> [--rent <blocks>]
# --rent default: 201600 (~7 days). 0 = free tier (≤10KB, permanent)
# Returns: merkleRoot (save this — needed to retrieve the file)
```

### 检索文件
```bash
node bin/cli.js load <merkleRoot> <outFile>
```

### 检查状态
```bash
node bin/cli.js status              # network overview
node bin/cli.js status <merkleRoot> # specific tree info
```

### 授予/撤销访问权限
```bash
node bin/cli.js grant <merkleRoot> <address>
node bin/cli.js revoke <merkleRoot> <address>
```

### 续订租金
```bash
node bin/cli.js renew <merkleRoot> [--blocks <n>]
```

## 合同地址（BSC主网）

| 合同 | 地址         |
|---------|------------|
| MemoryProtocol Proxy | `0x3BD7945d18FE6B68D273109902616BF17eb40F44` |
| MMPToken    | `0x30b8Bf35679E024331C813Be4bDfDB784E8E9a1E` |

## 环境变量（.env）

```
PROTOCOL_ADDRESS=0x3BD7945d18FE6B68D273109902616BF17eb40F44
MMP_TOKEN_ADDRESS=0x30b8Bf35679E024331C813Be4bDfDB784E8E9a1E
BSC_RPC=https://bsc-dataseed.binance.org/
WALLET_PASSWORD=<your-password>
```

## 安装脚本

运行`scripts/install.sh`以自动从OMP仓库安装命令行工具（CLI）。

## 注意事项：

- 免费 tier：每个地址最多存储10KB的数据，提供一个永久性的存储槽（无需支付MMP代币）。
- 付费 tier：费用根据文件大小和租金时长计算。
- EPOCH_blocks = 1000（约50分钟）：每个挖矿周期矿工有50分钟的存储时间窗口。
- `renounceUpgradeability()` — 所有者（`0x571d447f4f24688eC35Ccf07f1D6993655F6aF15`）可以调用此函数来永久锁定合约。