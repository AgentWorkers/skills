---
name: celo-defi
description: 在 Celo 上集成 DeFi 协议。当使用 Uniswap、Aave、Ubeswap 或其他 DeFi 协议构建交换、借贷或流动性应用程序时，可以使用这一功能。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Celo DeFi集成

本技能涵盖了在Celo平台上集成DeFi协议，包括用于交易的Uniswap、用于借贷的Aave以及其他相关协议。

## 使用场景

- 使用Uniswap或Ubeswap构建交易功能
- 集成Aave的借贷服务
- 创建流动性提供功能
- 开发DeFi聚合器

## Celo上的DeFi协议

### 去中心化交易所（DEX）

| 协议 | 描述 |
|----------|-------------|
| Uniswap V3/V4 | 主要的DEX，拥有高度集中的流动性 |
| Ubeswap | 原生于Celo的DEX，专为移动设备优化 |
| Velodrome | Superchain平台的DEX，支持流动性挖矿 |
| Carbon DeFi | 类订单簿的自动化交易系统 |

### 借贷服务

| 协议 | 描述 |
|----------|-------------|
| Aave V3 | 去中心化借贷服务（2025年3月上线） |
| Credit Collective | 基于链上的私人信贷服务 |
| PWN | 固定利率借贷服务 |

### DEX聚合器

| 协议 | 描述 |
|----------|-------------|
| LI.FI | 跨链交易聚合器 |

### 流动性与收益

| 协议 | 描述 |
|----------|-------------|
| Steer Protocol | 自动化流动性管理策略 |
| Merkl | 流动性提供者奖励机制 |

## Uniswap V3集成

### 合约地址 - 主网（链ID：42220）

| 合约 | 地址 |
|----------|---------|
| Factory | 0xAfE208a311B21f13EF87E33A90049fC17A7acDEc |
| SwapRouter02 | 0x5615CDAb10dc425a742d643d949a7F474C01abc4 |
| QuoterV2 | 0x82825d0554fA07f7FC52Ab63c961F330fdEFa8E8 |
| NonfungiblePositionManager | 0x3d79EdAaBC0EaB6F08ED885C05Fc0B014290D95A |
| UniversalRouter | 0x643770E279d5D0733F21d6DC03A8efbABf3255B4 |
| Permit2 | 0x000000000022D473030F116dDEE9F6B43aC78BA3 |
| TickLens | 0x5f115D9113F88e0a0Db1b5033D90D4a9690AcD3D |
| Multicall2 | 0x633987602DE5C4F337e3DbF265303A1080324204 |

### 合约地址 - Alfajores测试网

| 合约 | 地址 |
|----------|---------|
| Factory | 0x229Fd76DA9062C1a10eb4193768E192bdEA99572 |
| SwapRouter02 | 0x8C456F41A3883bA0ba99f810F7A2Da54D9Ea3EF0 |
| QuoterV2 | 0x3c1FCF8D6f3A579E98F4AE75EB0adA6de70f5673 |
| NonfungiblePositionManager | 0x0eC9d3C06Bc0A472A80085244d897bb604548824 |
| UniversalRouter | 0x84904B9E85F76a421223565be7b596d7d9A8b8Ce |
| Permit2 | 0x000000000022D473030F116dDEE9F6B43aC78BA3 |

### 简单交易示例

```typescript
import { createWalletClient, custom, encodeFunctionData } from "viem";
import { celo } from "viem/chains";

const SWAP_ROUTER = "0x5615CDAb10dc425a742d643d949a7F474C01abc4";

const SWAP_ROUTER_ABI = [
  {
    name: "exactInputSingle",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "tokenIn", type: "address" },
          { name: "tokenOut", type: "address" },
          { name: "fee", type: "uint24" },
          { name: "recipient", type: "address" },
          { name: "amountIn", type: "uint256" },
          { name: "amountOutMinimum", type: "uint256" },
          { name: "sqrtPriceLimitX96", type: "uint160" },
        ],
      },
    ],
    outputs: [{ type: "uint256" }],
  },
] as const;

async function swapExactInput(
  tokenIn: string,
  tokenOut: string,
  amountIn: bigint,
  amountOutMin: bigint,
  fee: number = 3000
): Promise<string> {
  const walletClient = createWalletClient({
    chain: celo,
    transport: custom(window.ethereum),
  });

  const [address] = await walletClient.getAddresses();

  const hash = await walletClient.sendTransaction({
    account: address,
    to: SWAP_ROUTER,
    data: encodeFunctionData({
      abi: SWAP_ROUTER_ABI,
      functionName: "exactInputSingle",
      args: [
        {
          tokenIn: tokenIn as `0x${string}`,
          tokenOut: tokenOut as `0x${string}`,
          fee,
          recipient: address,
          amountIn,
          amountOutMinimum: amountOutMin,
          sqrtPriceLimitX96: 0n,
        },
      ],
    }),
  });

  return hash;
}
```

## Ubeswap集成

Ubeswap是原生于Celo的DEX，支持Uniswap V2和V3协议。

### 合约地址 - 主网

| 合约 | 地址 |
|----------|---------|
| V3 Factory | 0x67FEa58D5a5a4162cED847E13c2c81c73bf8aeC4 |
| V3 Universal Router | 0x3C255DED9B25f0BFB4EF1D14234BD2514d7A7A0d |
| V3 NFT Position Manager | 0x897387c7B996485c3AAa85c94272Cd6C506f8c8F |
| V2 Factory | 0x62d5b84bE28a183aBB507E125B384122D2C25fAE |
| V2 Router | 0xE3D8bd6Aed4F159bc8000a9cD47CffDb95F96121 |
| UBE Token | 0x71e26d0E519D14591b9dE9a0fE9513A398101490 |

## Aave V3集成

### 合约地址 - 主网

| 合约 | 地址 |
|----------|---------|
| Pool | 0x3E59A31363E2ad014dcbc521c4a0d5757d9f3402 |
| PoolAddressesProvider | 0x9F7Cf9417D5251C59fE94fB9147feEe1aAd9Cea5 |
| PoolConfigurator | 0x7567E3434CC1BEf724AB595e6072367Ef4914691 |
| Oracle | 0x1e693D088ceFD1E95ba4c4a5F7EeA41a1Ec37e8b |
| ACLManager | 0x7a12dCfd73C1B4cddf294da4cFce75FcaBBa314C |
| PoolDataProvider | 0x2e0f8D3B1631296cC7c56538D6Eb6032601E15ED |
| Collector | 0xC959439207dA5341B74aDcdAC59016aa9Be7E9E7 |

### 支持的资产

| 资产 | 地址 | aToken |
|-------|---------|--------|
| USDC | 0xcebA9300f2b948710d2653dD7B07f33A8B32118C | 0xFF8309b9e99bfd2D4021bc71a362aBD93dBd4785 |
| USDT | 0x48065fbbe25f71c9282ddf5e1cd6d6a887483d5e | - |
| USDm | 0x765de816845861e75a25fca122bb6898b8b1282a | - |
| EURm | 0xd8763cba276a3738e6de85b4b3bf5fded6d6ca73 | - |
| CELO | 0x471EcE3750Da237f93B8E339c536989b8978a438 | - |
| WETH | 0xD221812de1BD094f35587EE8E174B07B6167D9Af | - |

### 可借贷资产

```typescript
const POOL_ABI_BORROW = [
  {
    name: "borrow",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
      { name: "interestRateMode", type: "uint256" },
      { name: "referralCode", type: "uint16" },
      { name: "onBehalfOf", type: "address" },
    ],
    outputs: [],
  },
] as const;

async function borrowFromAave(
  asset: string,
  amount: bigint,
  interestRateMode: number = 2 // 2 = variable rate
): Promise<string> {
  const walletClient = createWalletClient({
    chain: celo,
    transport: custom(window.ethereum),
  });

  const [address] = await walletClient.getAddresses();

  const hash = await walletClient.writeContract({
    address: AAVE_POOL,
    abi: POOL_ABI_BORROW,
    functionName: "borrow",
    args: [asset as `0x${string}`, amount, BigInt(interestRateMode), 0, address],
  });

  return hash;
}
```

## 代币授权

在与DeFi协议交互之前，需要先授权代币的使用：

```typescript
const ERC20_ABI = [
  {
    name: "approve",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ type: "bool" }],
  },
] as const;

async function approveToken(
  token: string,
  spender: string,
  amount: bigint
): Promise<string> {
  const walletClient = createWalletClient({
    chain: celo,
    transport: custom(window.ethereum),
  });

  const [address] = await walletClient.getAddresses();

  const hash = await walletClient.writeContract({
    address: token as `0x${string}`,
    abi: ERC20_ABI,
    functionName: "approve",
    args: [spender as `0x${string}`, amount],
  });

  return hash;
}
```

## 费用等级（Uniswap V3）

| 费用 | 使用场景 |
|-----|----------|
| 100（0.01%） | 稳定货币对（USDm/USDC） |
| 500（0.05%） | 大多数货币对 |
| 3000（0.3%） | 大多数货币对 |
| 10000（1%） | 特殊货币对 |

## 依赖项

```json
{
  "dependencies": {
    "viem": "^2.0.0"
  }
}
```

关于Aave的集成细节，请参考相关文档。

## 额外资源

- [contract-addresses.md](references/contract-addresses.md) - 所有DeFi协议的合约地址