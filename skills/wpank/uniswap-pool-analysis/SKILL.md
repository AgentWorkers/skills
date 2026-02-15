---
name: uniswap-pool-analysis
description: 分析 Uniswap 池的数据，包括流动性分布、费用等级、时间间隔（tick ranges）以及总价值锁定（TVL，Total Value Locked）。当用户询问池的指标、流动性分析信息，或希望查询链上池的状态时，可以使用此功能。
---

# Uniswap 池分析

## 概述

本技能介绍如何使用 viem 在链上查询和分析 Uniswap v3/v4 池的状态。

## 关键概念

- **sqrtPriceX96**: Uniswap v3/v4 使用的编码价格格式。转换公式为：`price = (sqrtPriceX96 / 2^96)^2`
- **Ticks**: 定义流动性范围的离散价格点。Tick 之间的间隔取决于费用等级。
- **Liquidity**: 表示当前 Tick 下活跃流动性的数值 `L`。

## 费用等级（v3）

| 费用（bps） | Tick 间隔 | 适用场景                |
| ----------- | ------------ | ------------------- |
| 1 (0.01%)   | 1            | 稳定币对             |
| 5 (0.05%)   | 10           | 相关币对             |
| 30 (0.30%)  | 60           | 标准币对             |
| 100 (1.00%) | 200          | 特殊币对             |

## 查询池状态

使用 Uniswap v3 池的 ABI（Application Binary Interface）来读取链上状态：

```typescript
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.ETHEREUM_RPC_URL),
});

// Read slot0 for current price and tick
const [
  sqrtPriceX96,
  tick,
  observationIndex,
  observationCardinality,
  observationCardinalityNext,
  feeProtocol,
  unlocked,
] = await client.readContract({
  address: poolAddress,
  abi: poolAbi,
  functionName: "slot0",
});

// Read liquidity
const liquidity = await client.readContract({
  address: poolAddress,
  abi: poolAbi,
  functionName: "liquidity",
});
```

## 价格转换

```typescript
function sqrtPriceX96ToPrice(
  sqrtPriceX96: bigint,
  decimals0: number,
  decimals1: number,
): number {
  const price = Number(sqrtPriceX96) / 2 ** 96;
  return (price * price * 10 ** decimals0) / 10 ** decimals1;
}

function tickToPrice(
  tick: number,
  decimals0: number,
  decimals1: number,
): number {
  return (1.0001 ** tick * 10 ** decimals0) / 10 ** decimals1;
}
```

## 流动性分布

要分析各个 Tick 下的流动性分布，请按照以下步骤操作：

1. 查询 `tickBitmap` 以获取已初始化的 Tick。
2. 对于每个已初始化的 Tick，读取 `ticks(tickIndex)` 以获取其对应的 `liquidityNet` 值。
3. 从 `MIN_TICK` 遍历到 `MAX_TICK`，累计每个 Tick 的流动性变化量。
4. 绘制流动性与价格的累积分布图。

## 多链支持

始终需要提供一个 `chainId` 参数。使用 `packages/common/` 中的共享链配置来获取以下信息：

- RPC（Remote Procedure Call）URL
- 池工厂地址
- 报价器地址
- 子图端点（如果可用）