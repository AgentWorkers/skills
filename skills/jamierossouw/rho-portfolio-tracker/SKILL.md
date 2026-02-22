---
name: rho-portfolio-tracker
version: 1.0.0
description: >
  **功能概述：**  
  该工具可实时跟踪您在 Binance、Hyperliquid 和 Polymarket 三大加密货币交易平台上的投资组合表现。它能够计算投资组合的净资产价值（NAV）、未实现的盈亏（Unrealized P&L）、每日回撤率（Daily Drawdown）、胜率（Win Rate）以及资产曲线（Equity Curve）。非常适合需要监控投资组合状况、计算净资产价值、分析回撤情况或进行多平台资产管理的用户。
author: JamieRossouw
tags: [crypto, portfolio, tracking, binance, hyperliquid, pnl, nav, drawdown]
---# 加密资产组合追踪器

专为自动化加密货币交易代理设计的多平台资产组合追踪工具。

## 支持的平台
- Binance Spot（纸面交易 + 通过CCXT进行实时交易）
- Hyperliquid Perps（纸面交易 + 实时交易）
- Polymarket预测市场

## 主要功能
- 实时计算资产净值（NAV），采用市值计价法
- 日度回撤跟踪，可在可配置的阈值下自动暂停
- 计算胜率、预期收益和资产净值曲线
- 位置规模验证（使用Kelly准则）
- 可导出CSV账本，以便进行完整审计

## 使用方法
```
Use crypto-portfolio-tracker to check my portfolio NAV

Use crypto-portfolio-tracker to show today's P&L breakdown

Use crypto-portfolio-tracker to export my trade history
```

## 输出示例
```
NAV: $748.36 | Start: $750 | Daily P&L: +$2.16 | DD: 0.00%
Positions: 7 | Trades today: 16 | W:8 L:8 | WR: 50%
Best trade: SOL +$1.20 | Worst: BTC -$0.80
```