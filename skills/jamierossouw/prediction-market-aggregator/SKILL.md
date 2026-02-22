---
name: prediction-market-aggregator
version: 1.0.0
description: 跨市场预测市场数据聚合器。支持 Polymarket、Manifold、Metaculus 和 Kalshi 等平台，能够发现市场间的套利机会、追踪共识变化、比较隐含概率，并识别潜在的交易机会。作为 DomeAPI 的开源替代方案，适用于需要跨市场预测市场数据、套利分析、共识对比或统一预测市场信号的场景。
author: JamieRossouw
tags: [prediction-markets, polymarket, manifold, metaculus, arbitrage, domeapi-alternative]
---
# 预测市场聚合器（Prediction Market Aggregator）

这是一个跨市场预测数据、边缘检测及套利扫描工具，是DomeAPI的开源替代方案。

## 支持的市场

| 市场        | 资产        | API            | 认证方式     |
|-------------|------------|-----------------|-----------|
| **Polymarket**   | BTC、ETH、SOL、XRP（每小时数据）及主要事件 | CLOB REST       | API密钥 + EIP-712   |
| **Manifold Markets** | 数千个社区交易市场 | REST           | API密钥（免费）     |
| **Metaculus**   | 长期预测结果、汇总的共识数据 | REST           | 无需认证（公开访问） |
| **Kalshi**     | 美国监管的二元期权合约   | REST           | API密钥       |

## 核心功能

### 1. 跨市场套利扫描器（Cross-Market Arbitrage Scanner）
- 查找在不同市场上价格存在差异的相同预测结果：
```
BTC >$70k by March? 
  Polymarket: 62% 
  Manifold: 71%  ← 9% gap → sell Manifold, buy Polymarket
  Metaculus: 58%
```

### 2. 共识趋势检测（Consensus Drift Detection）
- 监测市场共识随时间的变化：
  - 当市场在30分钟内波动超过10%时发出警报
  - 识别机构投资者与散户资金流动的差异
  - 标记Metaculus（顶级预测者）与Polymarket预测结果相差超过15%的市场

### 3. Polymarket数据集成（Polymarket CLOB Integration）
- 完全兼容py-clob-client库：
  - 每小时扫描BTC/ETH/SOL/XRP市场数据
  - 计算实际价格与技术分析预测之间的概率差异（Argus策略）
  - 检测与市场共识相悖的情况（L023规则：当市场单边走势超过70%且技术分析预测相反时，视为套利机会）

### 4. 统一的API响应格式（Unified API Response Format）
```json
{
  "question": "BTC up by 1pm ET?",
  "markets": {
    "polymarket": { "yes": 0.62, "volume": 455000, "url": "..." },
    "manifold": { "yes": 0.71, "traders": 142, "url": "..." }
  },
  "arbitrage": { "detected": true, "gap": 0.09, "direction": "buy_poly_sell_manifold" },
  "consensus": { "weighted_avg": 0.65, "superforecaster_avg": 0.58 }
}
```

## 使用方法

- 询问：“Polymarket和Manifold对BTC价格的预测是否存在套利机会？”
- 询问：“当前哪些市场的共识差距最大？”
- 询问：“利用跨市场共识数据，找到Polymarket中具有最高套利潜力的交易机会。”

## 从DomeAPI迁移指南（DomeAPI Migration Guide）

如果您之前使用DomeAPI获取跨市场数据，请按照以下步骤进行迁移：
- `/v1/markets` → 使用Polymarket的CLOB接口 `/markets`、Manifold的 `/v0/markets` 以及Metaculus的 `/questions`
- `/v1/arbitrage` → 使用本工具的跨市场套利扫描功能
- `/v1/consensus` → 使用Metaculus提供的社区预测结果作为共识基准

## 与Argus策略的集成（Integration with Argus Strategy）

本工具可直接与Argus边缘检测策略结合使用：
1. 从`argus-edge`技能获取技术分析评分
2. 将该评分与本工具提供的跨市场共识数据进行比较
3. 如果技术分析预测与市场共识均与Polymarket价格不符，即可进行最大置信度的投注操作