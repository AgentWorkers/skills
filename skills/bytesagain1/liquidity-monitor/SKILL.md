---
name: Liquidity Monitor
version: 1.0.0
description: 监控 dex（去中心化交易所）的流动性池深度，追踪流动性变化，计算 LP（锁定池）的收益，并估算非永久性损失（即因市场波动导致的资产损失）。
runtime: python3
---
# 流动性监控器 💧

实时监控去中心化交易所（DEX）的流动性池，提供永久性损失（Impermanent Loss, IL）的计算以及流动性提供者（LP）的收益估算功能。

## 功能列表

### 🔍 流动性池发现与监控
- 可在各大DEX中按代币对搜索流动性池
- 实时监控流动性池的总价值锁定（Total Value Locked, TVL）
- 跟踪流动性池的深度变化
- 当流动性低于阈值时发出警报

### 📊 永久性损失计算器
- 计算任何价格变动情景下的永久性损失
- 比较永久性损失与持有代币的收益
- 对不同价格区间内的永久性损失进行建模（针对流动性集中的情况）
- 提供现有头寸的历史永久性损失分析

### 💰 流动性提供者收益计算器
- 根据交易费用估算年化收益率（APR/APY）
- 将 farming 奖励纳入收益计算
- 可预测自定义时间范围内的收益
- 比较不同流动性池和DEX的收益

### ⚠️ 警报系统
- 流动性流失警报（检测资金抽逃行为）
- 大额交易对流动性池的影响警告
- 流动性池比例失衡通知
- TVL下降百分比触发警报

### 📈 分析与报告
- 流动性池健康评分（0-100分）
- 交易量与流动性比率分析
- 最主要流动性提供者追踪
- 生成HTML仪表盘

## 使用方法

### 监控流动性池

```bash
bash scripts/liquidity-monitor.sh monitor \
  --dex uniswap-v2 \
  --pair "ETH/USDC" \
  --chain ethereum
```

### 计算永久性损失

```bash
bash scripts/liquidity-monitor.sh impermanent-loss \
  --token-a ETH \
  --token-b USDC \
  --entry-price 3000 \
  --current-price 4500
```

### 估算流动性提供者收益

```bash
bash scripts/liquidity-monitor.sh yield \
  --pool-address "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc" \
  --amount 10000 \
  --period 30
```

### 检查流动性池健康状况

```bash
bash scripts/liquidity-monitor.sh health \
  --dex raydium \
  --pair "SOL/USDC" \
  --chain solana
```

### 生成仪表盘

```bash
bash scripts/liquidity-monitor.sh dashboard \
  --pools-file my-pools.json \
  --output liquidity-dashboard.html
```

## 支持的DEX

**EVM链：**
- Uniswap V2 / V3（以太坊、Polygon、Arbitrum、Optimism、Base）
- SushiSwap（多链支持）
- PancakeSwap（BSC、以太坊）
- Curve Finance（以太坊、Polygon、Arbitrum）

**Solana：**
- Raydium（AMM及CLMM）
- Orca（Whirlpools）
- Meteora

## 永久性损失参考表

| 价格变动百分比 | 永久性损失（50/50分配的流动性池） | 相当损失（每1,000美元） |
|-------------|-----------------|-----------------|
| ±25% | 0.6% | 6美元 |
| ±50% | 2.0% | 20美元 |
| ±75% | 3.8% | 38美元 |
| ±100%（2倍价格变动） | 5.7% | 57美元 |
| ±200%（3倍价格变动） | 13.4% | 134美元 |
| ±400%（5倍价格变动） | 25.5% | 255美元 |

## 流动性池健康评分标准

| 评分因素 | 权重 | 说明 |
|--------|--------|-------------|
| TVL稳定性 | 25% | 7天内TVL的稳定性 |
| 交易量与TVL比率 | 20% | 比率越高，费用生成能力越强 |
| 流动性提供者数量 | 15% | 流动性提供者越多，集中度风险越低 |
| 流动性池年龄 | 15% | 年龄越长的池子通常更安全 |
| 最大流动性提供者占比 | 15% | 流动性提供者集中度越低越好 |
| 智能合约审计情况 | 10% | 经过审计的DEX协议得分更高 |