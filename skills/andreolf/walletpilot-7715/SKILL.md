---
name: WalletPilot-7715
description: 使用用户授予的权限在链上执行交易。基于 MetaMask 和 ERC-7715 标准开发。无需私钥，具备全面的安全防护机制。
tags:
  - crypto
  - wallet
  - ethereum
  - defi
  - web3
  - blockchain
  - metamask
  - transactions
  - agent
  - automation
---

# WalletPilot-7715

通过 MetaMask 的 ERC-7715 权限，为您的 AI 代理赋予加密技术的超级能力。

## 概述

WalletPilot 允许 AI 代理使用 MetaMask 的 ERC-7715 权限标准在链上执行交易。用户只需一次性授予代理相应的权限（如消费限额、链限制等），之后代理便可以在这些限制范围内自由操作。

**主要特性：**
- **无需共享私钥**：用户仍可完全控制自己的 MetaMask 账户。
- **可配置的安全机制**：支持设置消费限额和允许使用的链。
- **多链支持**：支持 Ethereum、Polygon、Arbitrum 和 Base 等链。
- **基于 MetaMask 官方智能账户框架开发**。

## 设置

1. 在 [walletpilot.xyz](https://walletpilot.xyz) 获取 API 密钥。
2. 安装 SDK：`npm install @walletpilot/sdk`

## 可用的操作

### connect

向用户请求钱包权限。

```typescript
import { WalletPilot, PermissionBuilder } from '@walletpilot/sdk';

const pilot = new WalletPilot({ apiKey: 'wp_...' });

const permission = new PermissionBuilder()
  .spend('USDC', '100', 'day')   // Max $100 USDC per day
  .spend('ETH', '0.1', 'day')    // Max 0.1 ETH per day
  .chains([1, 137, 42161])       // Ethereum, Polygon, Arbitrum
  .expiry('30d')                 // Valid for 30 days
  .build();

const { deepLink } = await pilot.requestPermission(permission);
console.log('User should open:', deepLink);
```

### execute

使用已授予的权限执行交易。

```typescript
const result = await pilot.execute({
  to: '0x1234...',        // Target contract
  data: '0xabcd...',      // Calldata (e.g., swap)
  value: '0',             // ETH value (optional)
  chainId: 1,             // Chain ID
});

console.log('Transaction hash:', result.hash);
```

### balance

查询代币余额（使用标准 RPC 请求，无需权限）。

```typescript
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

const client = createPublicClient({
  chain: mainnet,
  transport: http(),
});

const balance = await client.getBalance({ address: '0x...' });
```

### swap

通过 DEX 代理器执行代币交换。

```typescript
// Get swap quote from 1inch, 0x, or similar
const quote = await fetch('https://api.1inch.io/v5.0/1/swap?...');
const { tx } = await quote.json();

// Execute via WalletPilot
await pilot.execute({
  to: tx.to,
  data: tx.data,
  value: tx.value,
  chainId: 1,
});
```

### send

将代币发送到指定地址。

```typescript
import { encodeFunctionData, erc20Abi } from 'viem';

// Encode ERC20 transfer
const data = encodeFunctionData({
  abi: erc20Abi,
  functionName: 'transfer',
  args: ['0xRecipient...', 1000000n], // 1 USDC (6 decimals)
});

await pilot.execute({
  to: '0xUSDC_ADDRESS...',
  data,
  chainId: 1,
});
```

### history

获取交易历史记录。

```typescript
const state = pilot.getState();
console.log('Active permissions:', state.permissions);

// Or via API
const response = await fetch('https://api.walletpilot.xyz/v1/tx/history/PERMISSION_ID', {
  headers: { 'Authorization': 'Bearer wp_...' },
});
const { data } = await response.json();
console.log('Recent transactions:', data);
```

## 权限类型

| 权限类型 | 示例 | 说明 |
|---------|------|-----------|
| `spend` | `{ token: 'USDC', limit: '100', period: 'day' }` | 每个周期内的最大代币消费限额 |
| `chains` | `[1, 137, 42161]` | 允许使用的链 ID 列表 |
| `contracts` | `['0x...']` | 允许使用的合约地址 |
| `expiry` | `'30d'` | 权限的有效期限 |

## 支持的链

| 链      | ID     | 名称       |
|---------|--------|-----------|
| Ethereum | 1      | mainnet     |
| Polygon | 137      | polygon     |
| Arbitrum | 42161    | arbitrum     |
| Optimism | 10      | optimism    |
| Base     | 8453    | base       |

## 安全性

- **无需共享私钥**：用户通过 MetaMask 保持对账户的完全控制权。
- **权限范围限制**：代理只能在授权的范围内操作。
- **权限自动过期**：权限具有时效性。
- **可撤销**：用户可随时撤销权限。
- **交易透明化**：所有交易记录均会被记录并公开。

## API 参考

**基础 URL：** `https://api.walletpilot.xyz`

| 端点        | 方法        | 说明                |
|-------------|-----------|-------------------|
| `/v1/permissions/request` | POST       | 请求新的权限            |
| `/v1/permissions/:id` | GET       | 获取权限详情            |
| `/v1/tx/execute` | POST       | 执行交易              |
| `/v1/tx/:hash` | GET       | 获取交易状态            |

## 示例：DeFi 代理的应用场景

```typescript
import { WalletPilot, PermissionBuilder } from '@walletpilot/sdk';

async function defiAgent() {
  const pilot = new WalletPilot({ apiKey: process.env.WALLETPILOT_KEY });

  // Check if we have active permissions
  const state = pilot.getState();
  
  if (!state.connected) {
    // Request permission
    const permission = new PermissionBuilder()
      .spend('USDC', '500', 'day')
      .chains([1, 42161])
      .expiry('7d')
      .description('DeFi trading agent')
      .build();
    
    const { deepLink } = await pilot.requestPermission(permission);
    console.log('Approve in MetaMask:', deepLink);
    return;
  }

  // Execute trades
  const swapData = await getSwapQuote('USDC', 'ETH', '100');
  
  await pilot.execute({
    to: swapData.to,
    data: swapData.data,
    chainId: 1,
  });
  
  console.log('Swap executed!');
}
```

## 链接

- [文档](https://docs.walletpilot.xyz)
- [GitHub 仓库](https://github.com/andreolf/walletpilot)
- [API 参考文档](https://api.walletpilot.xyz)