# Aoineco Ledger — 人工智能代理的财务跟踪引擎

<!-- 🌌 经 Aoineco 验证 | S-DNA: AOI-2026-0213-SDNA-AL01 -->

**版本：** 1.0.0  
**作者：** Aoineco & Co.  
**许可证：** MIT  
**标签：** 财务、费用跟踪、预算、投资回报率（ROI）、引导式启动（Bootstrap）、多代理、会计

## 产品描述

专为预算紧张的人工智能代理设计的财务跟踪工具。可追踪每一次 API 调用、Gas 费用以及收入情况，并能详细区分各代理的支出情况。原生支持 $7 的引导式启动（Bootstrap）协议。

该工具基于 `agentledger`（Node.js）项目重新开发为 Python 版本，针对多代理团队和微预算操作进行了重大优化。

**核心指标：** *每美元产生的价值（Intelligence per Dollar, IPD）—— 即每花费一美元能完成多少次操作。*

## 问题背景

人工智能代理在运行过程中会产生成本（API 调用、Gas 费用、订阅费用等），但往往缺乏有效的跟踪机制。当使用仅有 $7 的预算来运营一个由 9 个代理组成的团队时，每一分钱的支出都至关重要。您需要：
- 实时了解资金消耗情况；
- 明确每个代理的支出明细；
- 在超出预算前收到预警；
- 追踪收入以评估实际的投资回报率（ROI）。

## 主要功能

| 功能 | 详细描述 |
|---------|-------------|
| **交易记录** | 通过简洁的接口记录费用、收入、API 费用及 Gas 费用 |
| **$7 引导式启动指标** | 跟踪初始投资、投资回报率（ROI）、项目剩余时间、每日资金消耗率、每美元产生的价值（IPD） |
| **代理级成本分配** | 可按团队成员（如 oracle、blue-sound 等）细分支出情况 |
| **预算预警** | 为不同类别/时间段设置支出上限——达到 80% 时发出警告，达到 100% 时阻止进一步支出 |
| **类别分类系统** | 预先配置了适用于人工智能操作的类别（如 API/LLM、Gas/区块链、收入等） |
| **CSV/JSON 导出** | 支持导出全部交易数据，便于税务处理、审计或数据分析 |
| **JSONL 存储** | 采用只读写入方式的交易日志存储方式，速度快且数据不易损坏 |
| **时间范围筛选** | 可查询今日、本周、本月、本年或全部数据 |

## 快速入门

```python
from ledger_engine import AoinecoLedger

ledger = AoinecoLedger()

# Log API cost
ledger.log_api_cost(0.0042, "Google", "gemini-3-flash", tokens_used=150000, agent="oracle")

# Log gas fee
ledger.log_gas(0.0003, chain="base", tx_hash="0xabc123", agent="blue-sound")

# Log revenue
ledger.log_revenue(0.01, "MoltLaunch", "Tier-1 Intel Report", category="Revenue/Gig")

# Set budget
ledger.set_budget("API/LLM", limit=3.00, period="daily")

# Check $7 Bootstrap metrics
metrics = ledger.get_bootstrap_metrics()
# → Seed: $7.00, Burn: $0.02/day, Runway: 300 days, IPD: 257.5 ops/$
```

## 引导式启动（Bootstrap）指标示例

```
💰 Seed Amount: $7.00
📈 Total Revenue: $0.0150
📉 Total Expenses: $0.0233
🤖 API/LLM Cost: $0.0230
💵 Net Profit: $-0.0083
📊 ROI: -0.1%
💎 Remaining Balance: $6.9917
🔥 Daily Burn Rate: $0.0233/day
⏱️ Runway: 300 days
🧠 IPD: 257.5 ops/$
```

## 预先配置的类别

- `API/LLM`：OpenAI、Anthropic、Google API 的使用费用  
- `Gas/Blockchain`：链上交易费用  
- `Revenue/Gig`：MoltLaunch 的收入  
- `Revenue/DeFi`：Meteora、LP 的收益  
- `Revenue/Music`：claw.fm 的版税收入  
- `Infrastructure`（基础设施）、`Marketing`（市场营销）、`Tools`（工具）、`Subscriptions`（订阅费用）、`Other`（其他费用）

## 文件结构

```
aoineco-ledger/
├── SKILL.md              # This file
└── scripts/
    └── ledger_engine.py  # Main engine (zero external dependencies)
```

## 无外部依赖

完全基于 Python 3.10 及更高版本开发，无需安装任何第三方库（如 pip）。  
专为 $7 的引导式启动协议设计——每一字节的数据都至关重要。