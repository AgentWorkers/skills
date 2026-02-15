---
name: kyberswap-arbitrage
description: Execute triangular arbitrage on Base network via KyberSwap. Use for: (1) Finding arbitrage opportunities between token pairs, (2) Calculating optimal swap paths, (3) Executing multi-hop trades, (4) Managing gas and slippage.
---

# KyberSwap套利

## 概述

**三角形套利**：通过三种代币之间的价格差异获利（例如：USDC → ETH → USDT → USDC）

## 主网核心合约

- **Router**：`0x6131B5fae19EA4f9D964eAc0408E4408b2a37dD8`
- **Factory**：`0x5F1dddbf348aC2BEbe18559BF0eDE9D3fE6ce35f`

## 核心逻辑

### 1. 获取报价
```typescript
const router = new ethers.Contract(routerAddr, routerABI, provider);

// Get amounts out for exact input
const [amountOut] = await router.getAmountsOut(
  amountIn,      // Wei amount
  [tokenA, tokenB, tokenC] // Path
);
```

### 2. 计算利润
```
profit = finalAmount - initialAmount - gasCosts
```

### 3. 执行交易
```typescript
const tx = await router.swapExactTokensForTokens(
  amountIn,
  amountOutMin,
  path,
  recipient,
  deadline
);
```

## 代币地址（主网）

- **USDC**：`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **USDT**：`0xfde4C96c85940E8F44A6D8d5e4fD4f4C4f9D8E8`
- **ETH**：`0x4200000000000000000000000000000000000006`
- **WETH**：`0x4200000000000000000000000000000000000006`

## 套利路径（主网）

常见的三角形套利路径：
- USDC → ETH → USDC
- USDC → WETH → USDT → USDC
- USDT → ETH → USDC → USDT

## 安全检查

1. **滑点**：设置 `amountOutMin` = 输出金额 × (1 - 滑点百分比)
2. **Gas费用**：估算Gas费用，确保利润大于Gas费用
3. **最大价格波动**：在进行大额交易前检查交易池的储备情况
4. **已放弃所有权的代币**：仅交易那些所有权已被放弃的代币

## 风险等级

- **风险较高**，但需先进行审计
- 跳过所有所有权未被放弃的代币
- 注意是否存在“陷阱代币”（即可能被用于欺诈的代币）