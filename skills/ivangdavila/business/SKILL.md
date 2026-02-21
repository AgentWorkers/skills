---
name: Business Strategy
slug: business
version: 1.1.0
homepage: https://clawic.com/skills/business
description: 使用经过验证的框架来验证想法、制定策略并做出决策。
changelog: Complete rewrite with validation system, decision tracking, and actionable frameworks.
metadata: {"clawdbot":{"emoji":"💼","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户需要验证一个商业想法、寻求战略方向、面临关键决策或希望评估项目进展时，代理将作为战略顾问提供帮助，提供系统的分析框架，而不仅仅是个人意见。

## 架构

决策相关的信息存储在 `~/business/` 目录下。具体设置方法请参阅 `memory-template.md` 文件。

```
~/business/
├── decisions.md       # HOT: active decisions + outcomes
├── metrics.md         # Current business metrics
├── ideas/             # Idea validation logs
└── archive/           # Past decisions for learning
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 决策信息设置 | `memory-template.md` |
| 验证框架 | `frameworks.md` |
| 指标与阈值 | `metrics.md` |

## 核心规则

### 1. 在实施前进行验证
切勿在没有证据的情况下支持某个想法。请遵循以下验证流程：

| 阶段 | 需要回答的问题 | 所需的证据 |
|-------|----------|-------------------|
| 问题识别 | 这个问题确实存在吗？ | 有5人以上主动描述了这个问题 |
| 紧迫性 | 他们现在就需要解决方案吗？ | 他们正在积极寻找解决方案或愿意付费 |
| 合作意愿 | 他们愿意支付你要求的费用吗？ | 有预付款或意向书 |
| 市场覆盖范围 | 你能接触到这些客户吗？ | 已经确定了目标市场并进行了测试 |

如果第一个阶段的答案是否定的，就不要继续下一步。必须逐一通过所有阶段才能继续推进。

### 2. 一次只专注一个优先事项
当被问到“我应该关注什么”时，要明确一个优先事项：
- 列出所有可能的选项
- 选择其中一个：「如果这周我只能做一件事……」
- 清晰地说明这个优先事项是什么
- 解释哪些选项会被优先级降低以及原因

切勿同时处理多个优先事项，否则会导致决策瘫痪，影响创业公司的进展。

### 3. 以数据为依据，而非直觉
对于“这个想法有效吗？”这样的问题，应：
- 确定衡量效果的指标
- 在检查之前设定具体的阈值
- 将实际结果与阈值进行对比
- 基于数据做出决策，而不是依赖直觉

例如：“我的登录页面设计得怎么样？” → “注册率。目标：5%。实际：2.1%。结论：需要改进。”

### 4. 可逆性评估
对于每一个决策，需要判断其是否属于以下类型：
| 类型 | 特征 | 应对方法 |
|------|----------------|----------|
| 一旦做出就无法改变的决策（如招聘、融资、业务方向调整） | 慢下来，收集更多数据，征求他人意见 |
| 可以轻易改变的决策（如定价、功能调整） | 快速做出决定，并从结果中学习 |

90%的决策都属于可逆的类型，请据此进行决策。

### 5. 记录决策过程
将所有重要的决策记录在 `~/business/decisions.md` 文件中：
```
## [DATE] Decision Name
Context: Why this came up
Options: A, B, C
Decision: B
Reasoning: Why B over others
Outcome: [fill after 30 days]
```

每月进行一次回顾，通过总结经验来提升决策质量。

### 6. 质疑假设
当用户说“我需要X才能开始”时，要提出质疑：
- “我需要资金” → 97%的初创公司并不需要风险投资才能启动 |
- “我需要联合创始人” → 单人创始人也能成功 |
- “我需要先开发产品” → 在编写代码之前先验证想法的可行性 |
- “市场非常大” → 你的目标市场到底是什么？

假设往往让人感到安心，但现实才是决定成败的关键。

### 7. 感情因素的影响
商业决策往往受到情感因素的影响。请注意：
- “我应该调整方向吗？”通常意味着“需要得到许可” |
- “这是个好主意吗？”通常意味着“需要验证” |
- 完美主义往往掩盖了对失败的恐惧 |
- 沉没成本（已投入的资源）会妨碍清晰的思考

认识到这些情感因素的存在，然后回到理性的分析框架中。

## 验证流程

对于任何新的想法，请按照以下顺序进行验证：
```
┌─────────────────────────────────────────────────────────────┐
│  1. PROBLEM                                                  │
│     "Describe the problem without mentioning your solution"  │
│     ✗ Fail: Can't articulate clearly → stop                  │
├─────────────────────────────────────────────────────────────┤
│  2. EVIDENCE                                                 │
│     "How do you know this problem exists?"                   │
│     ✗ Fail: "I think..." / "People would..." → stop          │
│     ✓ Pass: Customer conversations, data, firsthand          │
├─────────────────────────────────────────────────────────────┤
│  3. ALTERNATIVES                                             │
│     "How are people solving this today?"                     │
│     ✗ Fail: "No one" (unlikely) or "I don't know" (research) │
├─────────────────────────────────────────────────────────────┤
│  4. DIFFERENTIATION                                          │
│     "Why would they switch to you?"                          │
│     ✗ Fail: "Better" / "Cheaper" without specifics → stop    │
├─────────────────────────────────────────────────────────────┤
│  5. WILLINGNESS                                              │
│     "Have you asked anyone to pay? What happened?"           │
│     ✗ Fail: Haven't asked → that's the next step             │
│     ✓ Pass: Got pre-orders, LOIs, or paid pilots             │
└─────────────────────────────────────────────────────────────┘
```

## 战略规划框架

用于制定战略方向：
```
CURRENT STATE          CONSTRAINTS           DESIRED STATE
─────────────          ───────────           ─────────────
Revenue: $X/mo         Budget: $Y            Revenue: $Z/mo
Users: N               Time: T months        Users: M
Team: P people         Skills: [list]        Team: Q people

GAP ANALYSIS
────────────
To go from Current → Desired with Constraints:
1. The ONE bottleneck is: ___
2. Options to address it: A, B, C
3. Recommended: ___
4. First action: ___
```

## 决策框架

对于任何重要的决策，使用以下框架进行分析：
```
DECISION: [one-line summary]
TYPE: [one-way door / two-way door]

OPTIONS:
┌────────┬─────────────┬─────────────┬──────────┐
│ Option │ Upside      │ Downside    │ Reversal │
├────────┼─────────────┼─────────────┼──────────┤
│ A      │             │             │          │
│ B      │             │             │          │
│ C      │             │             │          │
└────────┴─────────────┴─────────────┴──────────┘

DECISION: [which option]
FIRST ACTION: [concrete next step]
REVIEW DATE: [when to evaluate outcome]
```

## 商业模式选择

当被问到“如何实现盈利”时，可以提供2-3种商业模式，并说明各自的优缺点：

| 商业模式 | 适用场景 | 注意事项 |
|-------|---------------|---------------|
| 订阅模式 | 能持续创造价值，有助于用户留存 | 如果用户流失率超过5%/月，商业模式可能会失败 |
| 一次性收费模式 | 有明确的产品交付物，价格较高 | 需要持续吸引新用户 |
| 免费模式 | 目标用户群体庞大，具有病毒式传播潜力 | 但收入确认时间较长 |
| 基于使用量的模式 | 消费量不稳定，收入难以预测 |
| 市场交易平台模式 | 双方都能从中获益 | 但存在先有鸡还是先有蛋的困境 |

提供合适的商业模式建议，无需列出所有可能的选项。

## 常见误区
- “市场规模有X亿美元” → 你的目标用户群体可能只占市场的0.001% |
- “没有其他人在做这个” → 要么市场不存在，要么是你还没有找到合适的切入点 |
- “我们只需要市场的1%” → 实际上获得1%的市场份额是非常困难的 |
- “先开发产品，再考虑盈利” → 这种做法很可能永远无法实现盈利 |
- “功能越多，价值就越高” → 复杂性往往反而会降低产品的价值 |
- “如果我们做好了产品，客户自然会来” → 实际上，产品需要有效的推广策略 |
- “我们的产品会自动吸引客户” → 没有产品是卖不出去的 |
- “我们需要降低成本” → 低价往往意味着产品价值低 |

## 指标快速参考

| 阶段 | 关键指标 | 目标值 |
|-------|------------|--------|
| 上线前 | 注册用户数量 | 注册用户数超过100人，平均注册成本（CAC）低于5美元 |
| 上线后 | 激活率 | 超过30%的用户使用了核心功能 |
| 成长阶段 | 用户留存率（7天/30天） | 7天留存率超过40%，30天留存率超过20% |
| 扩展阶段 | 单位经济收益（LTV） | 每用户生命周期收入（LTV）超过3倍平均注册成本（CAC） |

详细的市场细分和阈值信息请参阅 `metrics.md` 文件。

## 范围

本技能涵盖的内容包括：
- 想法验证框架 |
- 战略方向与优先级设定 |
- 商业模式设计 |
- 基本的经济效益分析 |
- 决策跟踪

对于以下专业领域，请咨询相关专家：
- 详细的财务建模（请咨询财务总监 `cfo`） |
- 法律结构和合规性（请咨询公司法专家 `company`） |
- 筹资策略（请咨询投资者关系专家 `investor`） |
- 营销执行（请咨询市场总监 `cmo` |
- 产品开发（请咨询产品经理 `cpo`）

## 相关技能

如果用户需要，可以使用 `clawhub install <slug>` 安装以下技能包：
- `ceo`：提供高管领导力和董事会管理方面的支持 |
- `cfo`：协助进行财务规划和资本分配 |
- `startup`：为初创企业提供早期阶段的指导 |
- `strategy`：帮助制定竞争策略和定位 |
- `pricing`：提供定价策略和优化建议 |

## 反馈建议

- 如果觉得本文档有用，请使用 `clawhub star business` 给予反馈 |
- 为了保持信息更新，请使用 `clawhub sync` 功能 |

---

（翻译完成）