---
name: uniswap-swap-simulation
description: 模拟并分析 Uniswap 交易，包括价格影响、滑点、最优路由选择以及交易费用（gas）的估算。当用户询问交易执行、路由策略、价格变动或最大经济价值（Maximum Economic Value, MEV）相关问题时，可使用此功能。
---

# Uniswap 交易模拟

## 概述

本技能涵盖 Uniswap 交易的模拟、价格影响的计算以及路由决策的分析。

## 关键概念

- **价格影响**：交易导致的池内价格变动。交易金额越大，价格影响越大。
- **滑点**：预期价格与实际执行价格之间的差异，包括提交交易到执行交易之间的价格波动。
- **路由**：在多个池和协议中寻找最佳的执行路径。

## 模拟交易

使用 Quoter 合约来模拟交易（无需实际执行交易）：

```typescript
import { createPublicClient, http, encodeFunctionData } from "viem";

// QuoterV2 for v3 pools
const quote = await client.readContract({
  address: quoterV2Address,
  abi: quoterV2Abi,
  functionName: "quoteExactInputSingle",
  args: [
    {
      tokenIn,
      tokenOut,
      amountIn,
      fee,
      sqrtPriceLimitX96: 0n,
    },
  ],
});

// Returns: [amountOut, sqrtPriceX96After, initializedTicksCrossed, gasEstimate]
```

## 价格影响计算

```typescript
function calculatePriceImpact(
  amountIn: bigint,
  amountOut: bigint,
  marketPrice: number, // token1/token0
  decimals0: number,
  decimals1: number,
): number {
  const executionPrice =
    Number(amountOut) / 10 ** decimals1 / (Number(amountIn) / 10 ** decimals0);
  return Math.abs(1 - executionPrice / marketPrice);
}
```

## 滑点容忍度

- **稳定币对**：0.01% - 0.05%
- **主要币对**（如 ETH/USDC）：0.1% - 0.5%
- **高波动性币对**：0.5% - 1.0%
- **流动性较低的交易**：1% - 5%

计算最小交易金额：

```typescript
const minAmountOut = (amountOut * (10000n - BigInt(slippageBps))) / 10000n;
```

## 多跳路由

对于没有直接交易池的代币，需要通过中间代币进行路由：

```typescript
// ETH -> USDC -> DAI (two hops)
const path = encodePacked(
  ["address", "uint24", "address", "uint24", "address"],
  [WETH, 3000, USDC, 100, DAI],
);

const quote = await client.readContract({
  address: quoterV2Address,
  abi: quoterV2Abi,
  functionName: "quoteExactInput",
  args: [path, amountIn],
});
```

## 交易手续费估算

根据交易复杂度，典型的手续费成本如下：

- 单跳交易：约 130,000 gas
- 两跳交易：约 200,000 gas
- 三跳交易：约 270,000 gas

在手续费估算中始终保留 15-20% 的缓冲空间。

## MEV（最大经济价值）考虑

在开发交易模拟工具时：

- 建议对大额交易使用私有的 RPC（如 Flashbots Protect）进行保护
- 对于影响较大的交易，提醒用户注意“三明治攻击”风险
- 建议使用截止时间参数来限制交易风险