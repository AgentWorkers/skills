---
name: telegram-alerts
version: 1.0.0
description: 通过 Telegram 发送格式化的交易警报、投资组合更新和市场信号。支持价格警报、止损通知、盈亏报告以及定时生成的汇总信息。当您需要通过 Telegram 收到交易通知、价格警报、投资组合更新或自动化交易报告时，可以使用该工具。
author: JamieRossouw
tags: [telegram, alerts, trading, notifications, crypto, automation, bots]
---# Telegram 警报 — 交易通知系统

通过 Telegram 发送丰富的交易警报，以通知您任何加密货币事件或投资组合的更新。

## 警报类型
- **交易警报**：包含盈亏（P&L）、入场价格、止损价格和目标价格的交易信息
- **价格警报**：当资产价格达到预设阈值时触发
- **投资组合概览**：资产净值（NAV）、每日盈亏、持仓情况
- **止损警告**：当资金回撤接近预设限制时发出警报
- **连胜/连败记录**：用于庆祝连胜或防止情绪化交易
- **定期报告**：每日 18:00、每周一发送

## 使用方法
```
Use telegram-alerts to send a trade entry notification for BTC LONG at $68,000

Use telegram-alerts to send my daily portfolio summary

Use telegram-alerts to alert me when SOL breaks $90
```

## 格式示例
```
🟢 TRADE OPENED
Asset: BTC/USDT | LONG
Entry: $68,247 | Stop: $67,200 | Target: $70,000
Risk: $0.38 (0.05% NAV) | R:R = 1:2.6
```

## 设置要求
需要在您的 `.env` 文件中配置 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAMCHAT_ID`。