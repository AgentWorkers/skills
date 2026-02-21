---
name: hft-paper-trader
version: 1.0.0
description: 高频加密货币纸交易框架：该框架支持多种技术分析指标（RSI、MACD、EMA、BB、OBV、StochRSI）的评估，采用凯利准则（Kelly Criterion）进行头寸大小调整，并具备止损管理功能及交易记录功能。目标为每天执行300笔以上交易，每笔交易的平均风险控制在0.05%以内。该框架适用于纸交易、交易逻辑的回测、高频交易（HFT）模拟，或用于构建自动交易系统。
author: JamieRossouw
tags: [trading, paper-trading, hft, crypto, kelly, backtesting, autonomous-agent]
---
# HFT Paper Trader — 自动化加密货币交易框架

这是一个完整的高频纸面交易系统，用于构建和测试自动化加密货币交易策略。

## 架构

```
Market Data (Binance public API)
    ↓
TA Engine (RSI + MACD + EMA + BB + OBV + StochRSI)
    ↓
Signal Score (-10 to +10)
    ↓
Kelly Position Sizer (0.05% risk per trade)
    ↓
Paper Portfolio Manager (PORTFOLIO.json)
    ↓
Trade Ledger (LEDGER.csv)
```

## 特点

- **多指标融合**：将7个指标综合成一个综合评分
- **OBV divergence检测**：用于识别市场的累积/分配趋势
- **Quarter-Kelly资金管理策略**：采用保守的风险管理方法
- **回撤控制**：当每日净资产价值（NAV）下跌2%时自动暂停交易
- **完整审计追踪**：每笔交易都会记录交易细节（包括入场价、止损价、目标价和交易结果）
- **自我优化机制**：每次亏损后都会更新策略相关文档（lessons.md）

## 使用方法

```
Use hft-paper-trader to run TA on BTC and place a paper trade

Use hft-paper-trader to check portfolio performance

Use hft-paper-trader to scan the watchlist and trade all signals
```

## 关注列表
BTC ETH SOL XRP TRX DOGE ADA AVAX BNB LINK LTC SUI ARB OP NEAR DOT ATOM UNI MATIC

## 成绩表现
使用750美元的初始资金，在Binance平台上进行纸面交易，累计净资产价值达到748美元以上。每日目标：完成100笔以上交易。