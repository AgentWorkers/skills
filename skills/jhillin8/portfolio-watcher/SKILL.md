---
name: portfolio-watcher
description: 监控股票/加密货币持仓情况，接收价格警报，追踪投资组合表现
author: clawd-team
version: 1.0.0
triggers:
  - "check portfolio"
  - "stock price"
  - "crypto price"
  - "set price alert"
  - "portfolio performance"
---

# 投资组合监控器

通过自然语言对话来监控您的投资情况。提供实时价格、警报和绩效跟踪功能。

## 功能介绍

- 跟踪您的股票和加密货币持仓；
- 获取实时价格；
- 在达到预设目标时发送警报；
- 计算投资组合的绩效；
- 无需连接任何经纪商服务——只需告诉Clawd您持有的资产即可。

## 使用方法

**添加持仓：**
```
"I own 50 shares of AAPL at $150"
"Add 0.5 BTC bought at $40,000"
"Track NVDA, bought 20 shares at $280"
```

**查看价格：**
```
"What's TSLA at?"
"Bitcoin price"
"Check all my stocks"
```

**设置警报：**
```
"Alert me if AAPL hits $200"
"Notify when ETH drops below $2000"
"Remove MSFT alert"
```

**查看投资组合概览：**
```
"How's my portfolio doing?"
"Total gains/losses"
"Best and worst performers"
```

## 支持的资产类型

- 美国股票（纽约证券交易所、纳斯达克）
- 主要加密货币
- ETFs（交易型开放式指数基金）
- 国际股票（支持范围有限）

## 使用技巧

- 为准确计算收益/损失，请提供购买价格；
- 使用命令“update [股票代码] to [持股数量] at [价格]”来修改持仓；
- 输入“portfolio allocation”可查看投资组合的分配情况（以饼图形式显示）；
- 价格更新频率为几分钟一次（非实时流式显示）；
- 本工具仅提供信息参考，不提供财务建议。