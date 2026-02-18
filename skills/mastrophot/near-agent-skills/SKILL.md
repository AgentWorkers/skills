---
name: near-agent-skills
description: NEAR协议的全面代理技能，包括气体（Gas）优化和链上分析功能。
version: 1.0.0
author: mastrophot
tags:
  - near
  - blockchain
  - analytics
  - gas-optimizer
  - agent-skills
---
# NEAR Agent Skills

这是一系列专为与NEAR协议交互而设计的工具，专为自主代理（autonomous agents）进行了优化。

## 功能

### ⛽ 气体费用优化器（Gas Optimizer）

- **`near_gas_estimate`**：实时估算合约调用所需的气体费用（TGas）。
- **`near_gas_optimize`**：提供可操作的建议，以降低合约执行成本。
- **`near_gas_history`**：账户的历史气体费用使用情况。
- **`near_gas_compare`**：比较NEAR与Ethereum的气体费用。

### 📊 上链分析（On-Chain Analytics）

- **`near_analytics_network`**：网络吞吐量和健康状况指标。
- **`near_analytics_whales`**：追踪高价值交易。
- **`near_analytics_trending`**：识别最活跃的智能合约。
- **`near_analytics_defi`**：NEAR去中心化金融（DeFi）生态系统的总价值（TVL）和交易量统计。

## 设置（Setup）

```bash
npm install
npm run build
```

## 使用方法（Usage）

这些工具需要通过OpenClaw来运行。每个命令都对应包中导出的一个特定工具。