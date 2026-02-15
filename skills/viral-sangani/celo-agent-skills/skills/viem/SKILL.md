---
name: viem
description: 使用 viem 进行 Celo 开发。该工具支持费用货币的处理、交易签名以及 Celo 特定的配置设置。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Viem for Celo

Viem 是一个轻量级的 TypeScript 库，提供了对 Celo 的全面支持。它被用于 wagmi 和 RainbowKit 等项目的开发。

来源：https://viem.sh/docs/chains/celo

## 使用场景

- 构建与 Celo 交互的去中心化应用（dApps）
- 使用替代性费用货币发送交易
- 读取合约状态和区块链数据
- 签署消息和交易

## 安装

```bash
npm install viem
```

## 链路配置

来源：https://github.com/wevm/viem (chain definitions)

### 主网（Mainnet）

```typescript
import { celo } from "viem/chains";

// Chain ID: 42220
// RPC: https://forno.celo.org
// Explorer: https://celoscan.io
```

### 测试网（Celo Sepolia）

```typescript
import { celoSepolia } from "viem/chains";

// Chain ID: 11142220
// RPC: https://forno.celo-sepolia.celo-testnet.org
// Explorer: https://celo-sepolia.blockscout.com
```

### 使用自定义配置的自定义链（Custom Chain with Celo Config）

```typescript
import { defineChain } from "viem";
import { chainConfig } from "viem/celo";

export const customCeloChain = defineChain({
  ...chainConfig,
  id: 42220,
  name: "Custom Celo",
  // ...
});
```

## 客户端设置

### 公共客户端（仅支持读取操作）

```typescript
import { createPublicClient, http } from "viem";
import { celo } from "viem/chains";

const publicClient = createPublicClient({
  chain: celo,
  transport: http(),
});

// Read contract state
const balance = await publicClient.getBalance({
  address: "0x...",
});
```

### 钱包客户端（支持读写操作）

```typescript
import { createWalletClient, custom } from "viem";
import { celo } from "viem/chains";

const walletClient = createWalletClient({
  chain: celo,
  transport: custom(window.ethereum),
});

const [address] = await walletClient.getAddresses();
```

## 费用货币支持

Celo 允许使用除 CELO 以外的代币来支付交易手续费。请使用经过白名单审核的费用货币适配器。

来源：https://viem.sh/docs/chains/celo

### 主网的费用货币地址

| 代币 | 适配器地址 |
|-------|-----------------|
| USDC | 0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B |
| USDT | 0x0e2a3e05bc9a16f5292a6170456a710cb89c6f72 |

### Celo Sepolia 的费用货币地址

| 代币 | 适配器地址 |
|-------|-----------------|
| USDC | 0x4822e58de6f5e485eF90df51C41CE01721331dC0 |

### 使用费用货币序列化交易数据

```typescript
import { serializeTransaction } from "viem/celo";
import { parseGwei, parseEther } from "viem";

const serialized = serializeTransaction({
  chainId: 42220,
  gas: 21001n,
  feeCurrency: "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B", // USDC adapter
  maxFeePerGas: parseGwei("20"),
  maxPriorityFeePerGas: parseGwei("2"),
  nonce: 69,
  to: "0x1234512345123451234512345123451234512345",
  value: parseEther("0.01"),
});
```

### 使用费用货币发送交易

```typescript
import { createWalletClient, custom, parseEther } from "viem";
import { celo } from "viem/chains";

const USDC_ADAPTER = "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B";

const walletClient = createWalletClient({
  chain: celo,
  transport: custom(window.ethereum),
});

const [address] = await walletClient.getAddresses();

// Send transaction paying gas in USDC
const hash = await walletClient.sendTransaction({
  account: address,
  to: "0x...",
  value: parseEther("1"),
  feeCurrency: USDC_ADAPTER,
});
```

### 使用费用货币调用合约

```typescript
const hash = await walletClient.writeContract({
  address: CONTRACT_ADDRESS,
  abi: CONTRACT_ABI,
  functionName: "transfer",
  args: [recipient, amount],
  feeCurrency: USDC_ADAPTER,
});
```

## Celo 相关工具

### 解析交易数据

```typescript
import { parseTransaction } from "viem/celo";

// Supports CIP-64, EIP-1559, EIP-2930, and Legacy transactions
const transaction = parseTransaction("0x7cf846...");
```

### 序列化交易数据

```typescript
import { serializeTransaction } from "viem/celo";

const serialized = serializeTransaction({
  chainId: 42220,
  feeCurrency: "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B",
  // ... other params
});
```

## 读取合约数据

```typescript
import { createPublicClient, http } from "viem";
import { celo } from "viem/chains";

const publicClient = createPublicClient({
  chain: celo,
  transport: http(),
});

const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ type: "uint256" }],
  },
] as const;

const balance = await publicClient.readContract({
  address: "0x765de816845861e75a25fca122bb6898b8b1282a", // USDm
  abi: ERC20_ABI,
  functionName: "balanceOf",
  args: ["0x..."],
});
```

## 多次调用（Multicall）

高效地批量执行多次读取操作：

```typescript
const results = await publicClient.multicall({
  contracts: [
    {
      address: TOKEN_ADDRESS,
      abi: ERC20_ABI,
      functionName: "balanceOf",
      args: [userAddress],
    },
    {
      address: TOKEN_ADDRESS,
      abi: ERC20_ABI,
      functionName: "totalSupply",
    },
  ],
});
```

## 重要说明

- Viem 是开发 Celo 应用程序的推荐库（ethers.js 和 web3.js 不支持 `feeCurrency` 参数）
- 使用费用货币的交易会使用 `0x7b` 类型的交易数据格式（CIP-64 标准）
- 使用费用货币的交易会产生约 50,000 单位的额外手续费
- 如果未指定 `feeCurrency`，系统将默认使用 CELO 作为支付货币
- 使用 `viem/celo` 模块来处理 Celo 特有的功能（如解析交易数据、序列化交易数据）

## 依赖项

```json
{
  "dependencies": {
    "viem": "^2.0.0"
  }
}
```

## 额外资源

- [fee-currencies.md](references/fee-currencies.md) - 完整的费用货币参考文档