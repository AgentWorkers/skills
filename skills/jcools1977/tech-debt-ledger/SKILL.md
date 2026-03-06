---
name: tech-debt-ledger
version: 1.0.0
description: 将技术债务量化为实际的财务债务——包括本金、利率、最低还款额以及复利增长。这把“我们总有一天会修复这个问题”的模糊说法，转化为具有具体成本、到期日和偿还策略的量化责任。因为无法衡量的债务，永远也偿还不清。
author: J. DeVere Cooley
category: everyday-tools
tags:
  - tech-debt
  - estimation
  - planning
  - project-health
metadata:
  openclaw:
    emoji: "📒"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - planning
---
# 技术债务账本

> “技术债务就像财务债务一样。为了加快开发速度而负债是可以的——只要你知道利率、跟踪债务余额，并有一个偿还计划。问题在于，大多数团队堆积的债务多得连自己都看不懂。”

## 技术债务的作用

你的代码库中存在技术债务。这一点大家都清楚。但没人知道具体有多少债务、这些债务到底花了多少钱，以及何时会变得难以承受。

**技术债务账本**采用**复式记账法**来管理技术债务。每一个捷径、临时解决方案，以及“我们以后再修复”的承诺，都会被记录在账本中，包括以下信息：
- **本金**：立即修复这些债务所需的成本
- **利率**：如果不修复，这些债务会以多快的速度增加
- **利息类型**：利息是呈指数级增长还是线性增长？
- **最低还款额**：为防止系统出问题而需要支付的维护费用
- **到期日**：如果不解决这些问题，何时会引发危机

## 财务模型

### 债务类型

并非所有的技术债务都是一样的。不同类型的债务具有不同的利率：

| 债务类型 | 本金 | 利率 | 利息类型 | 例子 |
|---|---|---|---|
| **谨慎且经过深思熟虑的** | 已知且计划好的 | 低（2-5%） | 简单的 | “先发布代码，后续再自动化” |
| **谨慎但出于疏忽的** | 后来才发现的 | 中等（5-15%） | 简单的 | “现在我们意识到应该使用某种设计模式” |
| **鲁莽但经过深思熟虑的** | 已知但被忽视的 | 高（15-30%） | 利息呈指数级增长 | “我们没有时间进行测试” |
| **鲁莽且出于疏忽的** | 直到危机发生时才意识到问题的存在 | 非常高（30%以上） | 利息呈指数级增长 | “你说没有输入验证是什么意思？” |

### 债务计算公式

```
CURRENT COST = Principal + Accumulated Interest

Where:
  Simple interest:   Accumulated = Principal × Rate × Time
  Compound interest: Accumulated = Principal × (1 + Rate)^Time - Principal

TOTAL DEBT BURDEN = Σ(Current Cost of all entries)

DEBT SERVICE RATIO = Monthly interest payments / Monthly development capacity
  < 0.15  →  Healthy
  0.15-0.30 → Manageable (prioritize payoff)
  0.30-0.50 → Stressed (debt is slowing you down)
  > 0.50   → Crisis (most work is fighting debt, not building features)
```

## 账本条目结构

每个债务条目都是一份完整的财务记录：

```
╔══════════════════════════════════════════════════════════════╗
║  DEBT ENTRY: #TD-2025-047                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  DESCRIPTION: No integration tests for payment flow          ║
║  LOCATION: src/payments/*, src/checkout/*                    ║
║  CATEGORY: Reckless-Deliberate                               ║
║  INCURRED: 2025-01-15 (Sprint 42, "launch deadline")        ║
║                                                              ║
║  PRINCIPAL:          16 dev-hours to write comprehensive     ║
║                      integration test suite                  ║
║                                                              ║
║  INTEREST RATE:      20% per quarter (compound)              ║
║  INTEREST TYPE:      Compound — untested code attracts more  ║
║                      untested code; complexity grows          ║
║                                                              ║
║  CURRENT BALANCE:    23.1 dev-hours (7.1h interest accrued)  ║
║                                                              ║
║  MINIMUM PAYMENT:    2 dev-hours/month                       ║
║                      (manual testing each deploy,            ║
║                       investigating payment bugs)            ║
║                                                              ║
║  MATURITY DATE:      2025-07-01 (EU compliance audit)        ║
║  MATURITY PENALTY:   Compliance failure, potential fine       ║
║                                                              ║
║  INTEREST EXPLANATION:                                       ║
║  Every month without tests, the payment code changes.        ║
║  Each change makes the eventual test suite harder to write.  ║
║  Developers avoid refactoring because there's no safety net. ║
║  Bad patterns calcify. The 16-hour fix today becomes a       ║
║  40-hour fix in 6 months.                                    ║
╚══════════════════════════════════════════════════════════════╝
```

## 债务分类系统

### 按严重程度分类

| 评级 | 债务与开发能力的比率 | 说明 |
|---|---|---|
| **AAA** | < 5% | 债务极少，代码库健康 |
| **AA** | 5-10% | 债务较低，管理得当 |
| **A** | 10-20% | 债务适中，需要制定偿还计划 |
| **BBB** | 20-30% | 债务较多，开发速度放缓 |
| **BB** | 30-40% | 债务较高，功能开发速度下降 |
| **B** | 40-50% | 债务严重，大部分工作都是维护 |
| **CCC** | 50-70% | 代码库状况不佳，正在讨论是否需要重写 |
| **D** | > 70% | 债务过高，代码库几乎无法维护 |

### 按来源分类

```
DEBT HEATMAP:
├── src/payments/    ████████████████████  42h (36% of total debt)
├── src/auth/        ████████████          24h (21%)
├── src/checkout/    ████████              18h (15%)
├── src/api/         ██████                14h (12%)
├── src/utils/       ████                  9h (8%)
└── src/ui/          ████                  9h (8%)
                                    Total: 116 dev-hours
```

## 账本操作

### 1. 债务审计（发现债务）

```
AUTOMATED DISCOVERY:
├── TODO/FIXME/HACK/WORKAROUND comments → convert to ledger entries
├── Code complexity hotspots → potential structural debt
├── Test coverage gaps → testing debt
├── Outdated dependencies → maintenance debt
├── Copy-pasted code → duplication debt
├── Dead code / unused exports → cleanliness debt
├── Missing error handling → reliability debt
└── Hardcoded values → configuration debt

MANUAL DISCOVERY:
├── "We know this is wrong but..." decisions
├── Shortcuts taken for deadlines
├── Deferred refactoring
├── Missing documentation
└── Known security gaps
```

### 2. 债务评估（估算本金）

```
FOR EACH ITEM:
├── Estimate fix time (optimistic, realistic, pessimistic)
│   └── Principal = realistic estimate
├── Estimate interest rate:
│   ├── Does this area change frequently? (high change = high interest)
│   ├── Do bugs cluster here? (high bugs = high interest)
│   ├── Does this block other work? (blocking = high interest)
│   └── Does this have a deadline? (deadline = maturity date)
├── Classify interest type:
│   ├── Simple: cost grows linearly (tech stays the same)
│   └── Compound: cost grows exponentially (complexity breeds complexity)
└── Set minimum payment: ongoing maintenance cost to keep it alive
```

### 3. 偿还策略

| 策略 | 描述 | 适用场景 |
|---|---|---|
| **雪球式偿还** | 先偿还利率最高的债务 | 最大化长期节省 |
| **逐步偿还** | 先偿还本金最少的债务 | 快速取得成果，提升团队士气 |
| **有针对性地偿还** | 先偿还阻碍特定目标的债务 | 有截止日期的项目 |
| **最低还款额策略** | 仅偿还最低还款额 | 当功能开发至关重要时 |
| **再融资** | 用更便宜的债务替换高成本的债务（例如，用更简单的解决方案替代复杂的代码） | 当彻底修复不可行时 |

### 4. 债务预算

```
QUARTERLY DEBT BUDGET:
├── Total development capacity: 480 dev-hours
├── Feature work allocation: 384 dev-hours (80%)
├── Debt payoff allocation: 96 dev-hours (20%)
│
├── PAYOFF PLAN (Avalanche strategy):
│   ├── #TD-2025-047: Payment tests (16h principal, 20% interest) → PAY IN FULL
│   ├── #TD-2025-023: Auth refactor (24h principal, 15% interest) → PAY IN FULL
│   ├── #TD-2025-031: API versioning (18h principal, 10% interest) → PAY IN FULL
│   └── #TD-2024-089: Legacy utils (38h principal, 8% interest) → PARTIAL (38h remaining)
│
├── PROJECTED BALANCE AFTER QUARTER:
│   ├── Before: 116 dev-hours
│   ├── Paid off: 58 dev-hours
│   ├── New interest on remaining: 4.2 dev-hours
│   └── After: 62.2 dev-hours
│
└── DEBT RATING CHANGE: BBB → A (improvement)
```

## 输出格式

```
╔══════════════════════════════════════════════════════════════╗
║                   TECH DEBT LEDGER                          ║
║              Balance Sheet — Q1 2025                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  TOTAL DEBT BALANCE: 116 dev-hours                           ║
║  DEBT RATING: BBB (Significant)                              ║
║  DEBT SERVICE RATIO: 0.23 (Manageable)                       ║
║  MONTHLY INTEREST ACCRUAL: 8.4 dev-hours                     ║
║  MONTHLY MINIMUM PAYMENT: 12 dev-hours                       ║
║                                                              ║
║  TOP 5 DEBTS BY INTEREST COST:                               ║
║  #  | Description              | Balance | Rate | Monthly $  ║
║  ───┼──────────────────────────┼─────────┼──────┼──────────  ║
║  1  | No payment tests         | 23.1h   | 20%  | 1.5h/mo   ║
║  2  | Auth module no types     | 28.8h   | 15%  | 1.1h/mo   ║
║  3  | Hardcoded config values  | 12.0h   | 12%  | 0.5h/mo   ║
║  4  | No API versioning        | 21.6h   | 10%  | 0.7h/mo   ║
║  5  | Legacy utility functions | 42.0h   | 8%   | 1.1h/mo   ║
║                                                              ║
║  TREND:                                                      ║
║  ├── Last quarter: 94h → This quarter: 116h (+23%)           ║
║  ├── New debt incurred: 31h                                   ║
║  ├── Debt paid off: 17h                                       ║
║  └── Interest accrued: 8.4h                                   ║
║                                                              ║
║  ⚠ ALERT: Debt is growing faster than payoff.                ║
║  At current rate, balance reaches 180h in 6 months.          ║
║  Recommend: Increase payoff allocation from 15% to 25%.      ║
╚══════════════════════════════════════════════════════════════╝
```

## 适用场景

- **冲刺计划** — 在安排功能开发工作时，同时规划债务偿还时间
- **新增债务时** — 立即记录下来，以免遗忘
- **季度评审** — 评估债务状况，调整偿还策略
- **在讨论代码重写之前** — 量化重写是否具有经济可行性
- **当开发速度下降时** — 检查债务偿还是否占用了过多的开发资源

## 重要性

那些将技术债务仅仅视为“需要修复的问题”的团队，永远无法真正解决这些问题。而那些将其视为**量化财务义务**的团队，则能够做出合理的决策，知道何时偿还、偿还多少，以及哪些债务是可以接受的。

目标不是将债务降为零。目标是在清楚了解自身债务状况的基础上进行管理——确切知道自己欠了多少钱、这些债务的成本是多少，并有一个明确的偿还计划。

零外部依赖。零API调用。仅进行估算和跟踪。