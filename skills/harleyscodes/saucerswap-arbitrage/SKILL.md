---
name: saucerswap-arbitrage
description: Execute triangular arbitrage on Hedera via SaucerSwap. Use for: (1) Finding arbitrage opportunities on HBAR DEX, (2) Multi-hop token swaps, (3) Calculating profit across pools, (4) Executing atomic swaps.
---

# SaucerSwap套利

## 概述

SaucerSwap是Hedera平台上的主要去中心化交易所（DEX），支持三角形套利机制：通过利用三种代币之间的价格差异来获利。

## 主网关键合约

- **SaucerSwap V1**: `0xcaec9706a4622D356d2D3aEd8f8D40c51f0C0dF`
- **SaucerSwap V2**: `0xA6F4E11E5D8A3F62A7D4E3E6B1E7F3C9E8F2A1B4`

## 获取报价（V1）

```typescript
const axios = require('axios');

async function getQuote(amountIn, path) {
  const [tokenA, tokenB, tokenC] = path;
  const url = `https://mainnet-api.saucerswap.fi/route?from=${tokenA}&to=${tokenB}&amount=${amountIn}`;
  const response = await axios.get(url);
  return response.data;
}
```

## 代币地址（Hedera）

- **HBAR**: `0.0.1000`（封装形式：EVM格式下的`0x...`）
- **USDC**: `0.0.456719`
- **USDT**: `0.0.456720`
- **ETH**: `0.0.456721`
- **WBTC**: `0.0.456722`
- **SAUCE**: `0.0.456723`

## 套利逻辑

### 1. 检查价格
```typescript
// Get prices for potential paths
const paths = [
  ['USDC', 'HBAR', 'USDC'],
  ['USDC', 'SAUCE', 'USDC'],
  ['HBAR', 'USDC', 'HBAR']
];

for (const path of paths) {
  const out = await getQuote(1000, path);
  const profit = out - 1000;
  console.log(`${path.join(' → ')}: ${profit}`);
}
```

### 2. 执行交易
```typescript
// Via HashPack or direct contract call
const tx = new ContractExecuteTransaction()
  .setContractId(poolAddress)
  .setFunction("swap")
  .setParameters([...]);
```

## 安全性检查

1. **滑点控制**：设定最小输出价值为预期价值的0.97倍
2. **网络费用**：以“tinybars”为单位估算网络手续费
3. **交易池深度**：在进行大额交易前检查交易池的流动性
4. **Hedera网络延迟**：考虑网络延迟对交易的影响

## 与EVM的主要区别

- **不支持EOA（Externally Owned Accounts）签名**：必须使用Hedera原生的签名机制
- **网络费用**：以“tinybars”为单位支付
- **交易类型**：使用HAPI（Hedera Application Programming Interface）而非EVM
- **代币格式**：使用`0.0.xxxxx`表示代币地址，而非`0x...`