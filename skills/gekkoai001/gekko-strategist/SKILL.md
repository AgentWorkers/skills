---
name: gekko-strategist
description: 这款由人工智能驱动的去中心化金融（DeFi）策略开发工具能够帮助用户根据市场状况、风险偏好以及资本配置目标来设计、回测、调整和评估收益 farming（收益获取）策略。它是 Gekko 系统的核心组件，负责实现所有策略相关的智能决策和自动化操作。
version: 1.0.0
metadata: {"clawdbot":{"emoji":"📊","category":"strategy","requires":{"bins":["node"],"api_endpoint":"https://gekkoterminal.ai/api/a2a?agent=strategist"}}}
---

# Gekko Strategist — 战略开发代理

这是一个由人工智能驱动的去中心化金融（DeFi）策略开发工具。它可以根据市场状况、风险偏好和资本配置目标，帮助用户设计、回测、调整和评估收益 farming（收益获取）策略。

**代理 ID：** 1375 | **链：** Base | **协议：** A2A v0.3.0

## Gekko Strategist 的功能

Gekko Strategist 是一个基于人工智能的去中心化金融策略开发工具，它能够：
- 根据市场状况创建定制的收益 farming 策略
- 使用历史数据对策略进行回测
- 自动调整策略以适应市场变化
- 对多种策略进行评估和比较

## 命令

### develop_strategy
根据当前市场状况创建收益 farming 策略。策略会在多个托管账户（vaults）中进行分配，权重分配会考虑到用户的风险承受能力和投资期限。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=strategist \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "develop_strategy",
    "parameters": {
      "marketCondition": "bull",
      "riskTolerance": "medium",
      "timeHorizon": "30d",
      "capital": "10000"
    }
  }'
```

**参数：**
- `marketCondition` (字符串，可选)：`bull`（牛市）| `bear`（熊市）| `sideways`（盘整）
- `riskTolerance` (字符串，可选)：`low`（低）| `medium`（中）| `high`（高）
- `timeHorizon` (字符串，可选)：例如 `7d`（7天）、`30d`（30天）、`90d`（90天）
- `capital` (字符串，可选)：要分配的资本金额

### backtest_strategy
使用历史链上数据对策略进行回测。评估总回报、年化回报、夏普比率（Sharpe ratio）和最大回撤（max drawdown）。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=strategist \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "backtest_strategy",
    "parameters": {
      "strategy": {...},
      "startDate": "2024-01-01",
      "endDate": "2024-12-31"
    }
  }'
```

**参数：**
- `strategy` (对象，可选)：要回测的策略
- `startDate` (字符串，可选)：开始日期（YYYY-MM-DD）
- `endDate` (字符串，可选)：结束日期（YYYY-MM-DD）

### adapt_strategy
根据市场变化调整现有策略。当市场环境发生变化时，自动重新平衡资产配置。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=strategist \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "adapt_strategy",
    "parameters": {
      "currentStrategy": {...},
      "newMarketCondition": "bear"
    }
  }'
```

**参数：**
- `currentStrategy` (对象，可选)：需要调整的现有策略
- `newMarketCondition` (字符串，可选)：`bull`（牛市）| `bear`（熊市）| `sideways`（盘整）

### evaluate_strategies
并行评估和比较多种策略。从风险调整后的回报、策略的一致性和抗回撤能力等方面对策略进行评分。

**使用方法：**
```bash
curl -X POST https://gekkoterminal.ai/api/a2a?agent=strategist \
  -H "Content-Type: application/json" \
  -d '{
    "capability": "evaluate_strategies",
    "parameters": {
      "strategies": [...]
    }
  }'
```

**参数：**
- `strategies` (数组，可选)：需要比较的策略对象数组

## 智能合约（Base 网络）

Gekko Strategist 会在 Base 网络（链 ID：8453）上设计的智能合约中进行资产分配。

### 托管账户合约
| 托管账户 | 地址 |
|-------|---------|
| Seamless USDC | `0x616a4E1db48e22028f6bbf20444Cd3b8e3273738` |
| Moonwell USDC | `0xc1256Ae5FFc1F2719D4937adb3bbCCab2E00A2Ca` |
| Spark USDC | `0x7bFA7C4f149E7415b73bdeDfe609237e29CBF34A` |
| Gauntlet USDC Prime | `0xe8EF4eC5672F09119b96Ab6fB59C27E1b7e44b61` |
| Yo USDC | `0x0000000f2eB9f69274678c76222B35eEc7588a65` |

## 系统要求

- 需要 Node.js 18 及更高版本
- 需要能够访问 Base 网络的 RPC（Remote Procedure Call）服务
- 需要历史数据以便进行回测
- API 端点：`https://gekkoterminal.ai/api/a2a?agent=strategist`

## 安全性

所有策略的资产分配都针对经过审计的开源托管账户合约进行。Gekko Strategist 仅生成分配建议，实际执行需要用户通过 Executor 代理进行明确的钱包操作。智能合约会接受第三方的审计、正式验证和漏洞奖励计划。

---

**由 Gekko AI 开发。基于 ERC-8004 协议运行。**