---
name: Named Immortal
description: 该功能为AI代理提供了评估加密资产健康状况的能力。它通过调用Majestify API（crypto-health-hub）来计算夏普比率（Sharpe Ratio）、索蒂诺比率（Sortino Ratio）、风险价值（VaR）、条件风险价值（CVaR）以及资产回撤率（Drawdown）等风险指标，并据此将资产分类为“永生”（IMMORTAL）、“ mortal”（MORTAL）或“危急”（CRITICAL）状态。该工具完全不依赖任何本地资源，只要有互联网连接，便可在任何地方使用。
license: MIT
compatibility:
  os: [windows, macos, linux]
  python: ">=3.10"
metadata:
  openclaw:
    emoji: 🛡️
    version: 1.0.0
    tags:
      - crypto-risk
      - resource-management
      - vitality-assessment
      - agent-intelligence
      - majestify
    requires:
      bins: []
      packages: []          # httpx is optional; falls back to stdlib
---
# 名称：Immortal：代理资源智能（Agent Resource Intelligence）

> “要在这场无休止的‘游戏’中生存下来，人们不仅要了解价格，还要了解‘生命力’——即生存的数学概率。”

## 该技能的功能

该技能使代理能够通过调用实时运行的[Majestify](https://majestify.io) API来**评估加密货币资产的财务健康状况**。它计算机构级别的风险指标，并将每种资产分为三个生命力等级：

| 等级 | 判断标准 | 代理建议 |
|:---|:---|:---|
| 🛡️ **Immortal** | 夏普比率（Sharpe Ratio）> 1.2，回撤率（Drawdown）< 60% | 作为现金储备或长期持有 |
| ⚠️ **Mortal** | 中等风险水平 | 需要主动管理或寻求资产增长 |
| ☠️ **Critical** | 回撤率> 80% 或夏普比率< -1.0 | 应避免投资或进行对冲 |

## 计算的指标

所有指标均由Crypto Health Hub后端（`services.py`）提供：

- **夏普比率（Sharpe Ratio）**：风险调整后的回报率与无风险利率的比率 |
- **索蒂诺比率（Sortino Ratio）**：仅针对下行风险的风险调整指标 |
- **VaR/CVaR（95%）**：最坏情况下的损失概率 |
- **Cornish-Fisher VaR**：考虑了数据分布的偏度（skewness）和峰度（kurtosis）的VaR |
- **最大回撤率（Max Drawdown）**：资产价格从最高点到最低点的最大跌幅 |
- **年化回报率（Annualized Return）**：指定时间窗口内的复合年增长率（CAGR） |
- **偏度/峰度（Skewness/Kurtosis）**：描述数据分布形态的统计量 |

## 使用方法

### 基本用法（默认设置：比特币（BTC）和以太坊（ETH），时间窗口为365天）
```bash
python .agent/skills/immortal/scripts/assess_vitality.py
```

### 自定义资产
```bash
python .agent/skills/immortal/scripts/assess_vitality.py --coins bitcoin ethereum solana
```

### 自定义API端点
```bash
python .agent/skills/immortal/scripts/assess_vitality.py --api https://crypto-health-hub.onrender.com
```

### 自定义时间窗口
```bash
python .agent/skills/immortal/scripts/assess_vitality.py --coins bitcoin --days 90
```

## 输出结果

- **人类可读的**输出结果会显示在`stdout`中；
- **机器可读的JSON格式**输出会发送到`stderr`，以便代理进行后续处理：
```bash
# 代理可以通过以下方式捕获JSON输出：
python assess_vitality.py --coins bitcoin 2>results.json
```

## 所需依赖库

- **Python 3.10及以上版本**（支持无`match`关键字的语法，兼容3.10及更高版本）
- **httpx**（可选）：如果已安装，用于异步HTTP请求；否则会使用标准库中的`urllib`。
- **网络连接**：需要能够访问Majestify API（地址：`crypto-health-hub.onrender.com`）

## 相关技能

- [immortal-api](file:///.agent/skills/immortal-api/SKILL.md)：提供全面计算预算管理功能的API，包括账本（ledger）、优化器（optimizer）、策略引擎（policy engine）和断路器（circuit breakers）。
- [financial_analysis](file:///.agent/skills/financial_analysis/SKILL.md)：编码规范和指标比较指南。