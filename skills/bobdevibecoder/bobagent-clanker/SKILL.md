---
name: clanker
description: 使用 Clanker SDK 在 Base、Ethereum、Arbitrum 及其他基于 EVM 的区块链上部署 ERC20 代币。该工具适用于用户需要部署新代币、创建表情币（memecoin）、设置代币归属规则、配置空投（airdrops）、管理代币奖励、领取 LP 费用或更新代币元数据等场景。支持 V4 部署模式，具备以下功能：使用安全存储库（vaults）进行代币管理、执行空投操作、允许开发者购买代币、设置自定义的市场上限（market caps）、生成个性化地址（vanity addresses），以及实现跨链部署（multi-chain deployment）。
---

# Clanker SDK

使用官方的Clanker TypeScript SDK，部署具备内置流动性池的、可用于生产环境的ERC20代币。

## 概述

Clanker是一种代币部署协议，它能够通过一次交易同时创建带有Uniswap V4流动性池的ERC20代币。该SDK提供了TypeScript接口，支持具有高级功能的代币部署，例如代币归属（vesting）、空投（airdrops）以及可定制的奖励分配。

## 快速入门

### 安装

```bash
npm install clanker-sdk viem
# or
yarn add clanker-sdk viem
# or
pnpm add clanker-sdk viem
```

### 环境设置

创建一个`.env`文件并配置您的私钥：

```bash
PRIVATE_KEY=0x...your_private_key_here
```

### 基本代币部署

```typescript
import { Clanker } from 'clanker-sdk';
import { createPublicClient, createWalletClient, http, type PublicClient } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const PRIVATE_KEY = process.env.PRIVATE_KEY as `0x${string}`;
const account = privateKeyToAccount(PRIVATE_KEY);

const publicClient = createPublicClient({
  chain: base,
  transport: http(),
}) as PublicClient;

const wallet = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

const clanker = new Clanker({ wallet, publicClient });

const { txHash, waitForTransaction, error } = await clanker.deploy({
  name: 'My Token',
  symbol: 'TKN',
  image: 'ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi',
  tokenAdmin: account.address,
  metadata: {
    description: 'My awesome token',
  },
  context: {
    interface: 'Clanker SDK',
  },
  vanity: true,
});

if (error) throw error;

const { address: tokenAddress } = await waitForTransaction();
console.log('Token deployed at:', tokenAddress);
```

## 核心功能

### 1. 代币部署

您可以完全自定义代币的配置，包括元数据、社交链接和流动性池设置。

**基本部署步骤：**
- 代币名称、符号和图片（存储在IPFS上）
- 代币描述和社交媒体链接
- 生成自定义的代币地址（vanity address）
- 自定义流动性池配置

**参考文档：** [references/deployment.md](references/deployment.md)

### 2. 代币归属（Vesting）

锁定一定比例的代币，并设置锁定期和归属期：

```typescript
vault: {
  percentage: 10,           // 10% of token supply
  lockupDuration: 2592000,  // 30 days cliff (in seconds)
  vestingDuration: 2592000, // 30 days linear vesting
  recipient: account.address,
}
```

**参考文档：** [references/vesting.md](references/vesting.md)

### 3. 空投（Airdrops）

使用Merkle树证明将代币分配给多个地址：

```typescript
import { createAirdrop, registerAirdrop } from 'clanker-sdk/v4/extensions';

const { tree, airdrop } = createAirdrop([
  { account: '0x...', amount: 200_000_000 },
  { account: '0x...', amount: 50_000_000 },
]);

// Include in deployment
airdrop: {
  ...airdrop,
  lockupDuration: 86_400,  // 1 day
  vestingDuration: 86_400, // 1 day
}
```

**参考文档：** [references/airdrops.md](references/airdrops.md)

### 4. 奖励配置

您可以配置交易费用的分配方式：

```typescript
rewards: {
  recipients: [
    {
      recipient: account.address,
      admin: account.address,
      bps: 5000,      // 50% of fees
      token: 'Both',  // Receive both tokens
    },
    {
      recipient: '0x...',
      admin: '0x...',
      bps: 5000,      // 50% of fees
      token: 'Both',
    },
  ],
}
```

#### 代币类型选项

选择每个接收者从交易费用中获得的代币类型：

| 代币类型 | 描述 |
|------------|-------------|
| `'Clanker'` | 仅接收部署的代币 |
| `'Paired'` | 仅接收配对代币（例如WETH） |
| `'Both'` | 同时接收两种代币 |

#### 默认的Bankr接口费用

通过Bankr进行部署时，使用以下默认的奖励配置（接口费用为20%）：

```typescript
// Bankr interface fee recipient
const BANKR_INTERFACE_ADDRESS = '0xF60633D02690e2A15A54AB919925F3d038Df163e';

rewards: {
  recipients: [
    {
      recipient: account.address,           // Creator
      admin: account.address,
      bps: 8000,                            // 80% to creator
      token: 'Paired',                      // Receive paired token (WETH)
    },
    {
      recipient: BANKR_INTERFACE_ADDRESS,   // Bankr interface
      admin: BANKR_INTERFACE_ADDRESS,
      bps: 2000,                            // 20% to Bankr
      token: 'Paired',                      // Receive paired token (WETH)
    },
  ],
}
```

**参考文档：** [references/rewards.md](references/rewards.md)

### 5. 开发者购买（Dev Buy）

在部署过程中包含初始的代币购买操作：

```typescript
devBuy: {
  ethAmount: 0.1,           // Buy with 0.1 ETH
  recipient: account.address,
}
```

### 6. 自定义市值

设置代币的初始价格和市值：

```typescript
import { getTickFromMarketCap } from 'clanker-sdk';

const customPool = getTickFromMarketCap(5); // 5 ETH market cap

pool: {
  ...customPool,
  positions: [
    {
      tickLower: customPool.tickIfToken0IsClanker,
      tickUpper: -120000,
      positionBps: 10_000,
    },
  ],
}
```

**参考文档：** [references/pool-config.md](references/pool-config.md)

### 7. 防止恶意交易（Anti-Sniper Protection）

配置费用衰减机制，以防止恶意交易行为：

```typescript
sniperFees: {
  startingFee: 666_777,    // 66.6777% starting fee
  endingFee: 41_673,       // 4.1673% ending fee
  secondsToDecay: 15,      // 15 seconds decay
}
```

## 合同限制与常量

| 参数 | 值 | 说明 |
|-----------|-------|-------|
| 代币总量 | 1000亿 | 固定为100,000,000,000个，保留18位小数 |
| 最大扩展比例 | 90% | 最大分配给扩展方的代币比例，最低10%分配给流动性提供者（LP） |
| 最大扩展数量 | 10 | 每次部署的最大扩展数量 |
| 流动性提供者最低锁定期限 | 7天 | 流动性提供者的最低锁定期限 |
| 空投最低锁定期限 | 1天 | 空投的最低锁定期限 |
| 最高流动性提供者费用 | 10% | 流动性提供者的最高交易费用 |
| 最高恶意交易费用 | 80% | 防止恶意交易的最高费用 |
| 恶意交易费用衰减时间 | 最长2分钟 | 恶意交易费用的衰减时间 |
| 最大奖励接收者数量 | 7 | 最多的奖励接收者数量 |
| 最大流动性提供者数量 | 7 | 最多的流动性提供者数量 |

## 支持的区块链

| 区块链 | 区块链ID | 原生代币 | 支持情况 |
|-------|----------|--------------|--------|
| Base | 8453 | ETH | ✅ 完全支持 |
| Ethereum | 1 | ETH | ✅ 完全支持 |
| Arbitrum | 42161 | ETH | ✅ 完全支持 |
| Unichain | - | ETH | ✅ 完全支持 |
| Monad | - | MON | ✅ 仅支持静态费用 |

## 部署后的操作

### 提取锁定代币

```typescript
const claimable = await clanker.getVaultClaimableAmount({ token: TOKEN_ADDRESS });

if (claimable > 0n) {
  const { txHash } = await clanker.claimVaultedTokens({ token: TOKEN_ADDRESS });
}
```

### 收集交易奖励

```typescript
// Check available rewards
const availableFees = await clanker.availableRewards({
  token: TOKEN_ADDRESS,
  rewardRecipient: FEE_OWNER_ADDRESS,
});

// Claim rewards
const { txHash } = await clanker.claimRewards({
  token: TOKEN_ADDRESS,
  rewardRecipient: FEE_OWNER_ADDRESS,
});
```

### 更新代币元数据

```typescript
const metadata = JSON.stringify({
  description: 'Updated description',
  socialMediaUrls: [
    { platform: 'twitter', url: 'https://twitter.com/mytoken' },
    { platform: 'telegram', url: 'https://t.me/mytoken' },
  ],
});

const { txHash } = await clanker.updateMetadata({
  token: TOKEN_ADDRESS,
  metadata,
});
```

### 更新代币图片

```typescript
const { txHash } = await clanker.updateImage({
  token: TOKEN_ADDRESS,
  image: 'ipfs://new_image_hash',
});
```

## 常见工作流程

### 简单的纪念币发布（Simple Memecoin Launch）

1. 准备代币图片（上传到IPFS）
2. 使用基本配置进行部署（名称、符号、图片）
3. 为代币地址生成易于记忆的格式
4. 分享合约地址

### 带有空投功能的社区代币（Community Token with Airdrop）

1. 编制空投接收者列表
2. 使用`createAirdrop()`方法创建Merkle树
3. 带有空投功能的代币部署
4. 在Clanker服务中注册空投
5. 分享领取说明

### 带有归属功能的创建者代币（Creator Token with Vesting）

1. 使用锁定配置进行部署
2. 设置锁定期
3. 设置归属期限
4. 在代币归属时进行领取

## 完整的部署配置

```typescript
// Bankr interface fee recipient (20%)
const BANKR_INTERFACE_ADDRESS = '0xF60633D02690e2A15A54AB919925F3d038Df163e';

const tokenConfig = {
  chainId: 8453,                    // Base
  name: 'My Token',
  symbol: 'TKN',
  image: 'ipfs://...',
  tokenAdmin: account.address,
  
  metadata: {
    description: 'Token description',
    socialMediaUrls: [
      { platform: 'twitter', url: '...' },
      { platform: 'telegram', url: '...' },
    ],
  },
  
  context: {
    interface: 'Bankr',
    platform: 'farcaster',
    messageId: '',
    id: '',
  },
  
  vault: {
    percentage: 10,
    lockupDuration: 2592000,
    vestingDuration: 2592000,
    recipient: account.address,
  },
  
  devBuy: {
    ethAmount: 0,
    recipient: account.address,
  },
  
  // Default: 80% creator, 20% Bankr interface (all in paired token)
  rewards: {
    recipients: [
      { 
        recipient: account.address,
        admin: account.address,
        bps: 8000,  // 80% to creator
        token: 'Paired',  // Receive paired token (WETH)
      },
      { 
        recipient: BANKR_INTERFACE_ADDRESS,
        admin: BANKR_INTERFACE_ADDRESS,
        bps: 2000,  // 20% to Bankr
        token: 'Paired',  // Receive paired token (WETH)
      },
    ],
  },
  
  pool: {
    pairedToken: '0x4200000000000000000000000000000000000006', // WETH
    positions: 'Standard',
  },
  
  fees: 'StaticBasic',
  vanity: true,
  
  sniperFees: {
    startingFee: 666_777,
    endingFee: 41_673,
    secondsToDecay: 15,
  },
};
```

## 最佳实践

### 安全性

1. **切勿泄露私钥** - 使用环境变量来存储私钥
2. **先在测试网进行测试** - 在主网上部署前验证配置
3. **模拟交易** - 在执行前使用模拟方法
4. **仔细检查地址** - 双重核对所有接收者地址

### 代币设计

1. **选择有意义的名称** - 代币名称应清晰易记
2. **使用高质量的图片** - 使用高分辨率、适合IPFS存储的图片
3. **合理配置归属机制** - 根据项目进度来设定归属规则

### 优化交易费用

1. **选择Base或Arbitrum** - 这些区块链的交易费用较低
2. **批量操作** - 尽可能合并多个操作
3. **监控交易费用** - 在交易量较低的时候进行部署

## 故障排除

### 常见问题

- **“缺少私钥（Missing PRIVATE_KEY）”** - 确保已设置环境变量
- **“余额不足”** - 用原生代币充值钱包
- **“交易被撤销（Transaction reverted）”** - 检查参数并先进行模拟
- **“图片无效”** - 确保IPFS图片链接有效

### 调试步骤

1. 检查钱包余额
2. 验证区块链配置
3. 使用模拟工具进行测试
4. 在区块浏览器中查看交易详情
5. 查看错误信息

## 资源

- **GitHub仓库**：[github.com/clanker-devco/clanker-sdk](https://github.com/clanker-devco/clanker-sdk)
- **NPM包**：[npmjs.com/package/clanker-sdk](https://www.npmjs.com/package/clanker-sdk)
- **示例代码**：[github.com/clanker-devco/clanker-sdk/tree/main/examples/v4](https://github.com/clanker-devco/clanker-sdk/tree/main/examples/v4)

---

**💡 提示**：始终使用`vanity: true`选项来生成易于记忆的合约地址。

**⚠️ 安全提示**：切勿直接提交私钥。请使用`.env`文件，并将其添加到`.gitignore`文件中。

**🚀 快速上手建议**：从简单的部署示例开始，根据需要逐步添加代币归属和奖励等功能。