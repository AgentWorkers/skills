---
name: whale-pulse-monitor
description: "实时BTC订单簿不平衡（OBI）追踪系统，专为专业交易者设计。该系统能够在重大交易行为发生前及时发现那些具有强烈交易意愿的“大户”（即持有大量BTC的交易者）的活动。该系统基于Sovereign-Futures算法进行运行。"
metadata:
  {
    "openclaw": { "emoji": "🐋" },
    "author": "System Architect Zero",
    "x402": { "fee": 0.25, "currency": "USDC", "network": "base" }
  }
---
# Whale Pulse Monitor

别再猜测了，开始追踪资金流动吧。该工具直接连接到Sovereign-Futures的OBI扫描引擎，当在OKX/Binance平台上检测到资金流动不平衡时，会立即向您发出警报。

## 主要功能
- **鲸鱼交易识别**：能够区分散户的随机交易和机构投资者的大规模交易（“冰山订单”）。
- **S级警报**：仅当OBI（资金流动指标）大于5.0时才会触发警报，以确保警报的准确性。
- **低延迟**：与基于Rust语言开发的market-cli工具直接集成。

## 使用方法
```bash
npx openclaw skill run whale-pulse-monitor
```

## 为什么定价为0.25美元？
这是为了过滤掉非专业投资者的干扰信号，并确保我们能够维持高性能的运行基础设施。