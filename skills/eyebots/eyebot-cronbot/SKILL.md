---
name: eyebot-cronbot
description: 任务调度器与区块链自动化引擎
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: automation
---

# CronBot ⏰

**区块链任务自动化**

用于安排和自动化重复的区块链操作。您可以设置触发条件、创建工作流程，并按计划执行交易。

## 特点

- **定时任务**：支持Cron风格的定时功能
- **事件触发**：能够响应链上的事件
- **价格触发**：在达到目标价格时执行操作
- **工作流链**：支持多步骤的自动化流程
- **重试逻辑**：处理失败的交易

## 触发类型

| 触发类型 | 例子 |
|---------|---------|
| 时间 | 每小时；每天上午9点 |
| 价格 | 当ETH价格超过3000美元时 |
| 事件 | 当发生代币转移时 |
| 余额 | 当钱包余额低于0.1 ETH时 |
| 气体费用 | 当气体费用低于20 gwei时 |

## 使用场景

- 自动领取奖励
- 定期进行分散投资（DCA）购买
- 优化气体费用的交易
- 在特定条件触发警报
- 资产组合再平衡

## 使用方法

```bash
# Schedule a task
eyebot cronbot schedule "swap ETH USDC 0.1" --cron "0 9 * * *"

# Set price trigger
eyebot cronbot trigger "buy ETH 1000" --when "ETH < 2000"

# List active jobs
eyebot cronbot list
```

## 技术支持

Telegram: @ILL4NE