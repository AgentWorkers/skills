---
name: scenario-war-room
description: "跨职能的“假设情景建模”适用于涉及多个变量的复杂场景。与基于单一假设的压力测试不同，该方法能够同时模拟所有业务职能所面临的复合性风险。在面对复杂的风险场景、具有重大负面影响的战略决策，或者用户提出“如果X和Y同时发生会怎样？”这类问题时，这种建模方法非常有用。"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: strategic-planning
  updated: 2026-03-05
  python-tools: scenario_modeler.py
  frameworks: scenario-planning
---
# 场景战争室（Scenario War Room）

该工具能够模拟所有业务功能中的连锁性“假设情景”（cascading what-if scenarios），而不仅仅是基于单一假设的压力测试（stress tests）。它能够展示一个问题如何引发另一个问题，从而形成复杂的负面效应。

## 关键词
- 场景规划（Scenario Planning）
- 战争室（War Room）
- 假设分析（What-if Analysis）
- 风险建模（Risk Modeling）
- 连锁效应（Cascading Effects）
- 复合风险（Compound Risk）
- 应急计划（Contingency Planning）
- 压力测试（Stress Test）
- 危机规划（Crisis Planning）
- 多变量情景（Multi-variable Scenarios）
- 事后分析（Post-mortem）

## 快速入门

```bash
python scripts/scenario_modeler.py   # Interactive scenario builder with cascade modeling
```

或者，您可以这样描述一个具体的场景：
```
/war-room "What if we lose our top customer AND miss the Q3 fundraise?"
/war-room "What if 3 engineers quit AND we need to ship by Q3?"
/war-room "What if our market shrinks 30% AND a competitor raises $50M?"
```

## 本工具的用途

- **不是** 单一假设的压力测试（请参考 `/em:stress-test`）。
- **不仅** 用于财务建模**——所有业务功能都会被纳入模型中**。
- **不仅** 仅考虑最坏情况**——模型会涵盖三种不同的严重程度。
- **不会** 因分析而陷入停滞**——会提供具体的应对策略和触发条件。

## 框架：六步连锁模型（6-Step Cascade Model）

### 第一步：定义场景变量（最多3个）
为每个变量明确说明：
- **变化内容**——具体且尽可能量化。
- **发生概率**——您的最佳估计。
- **时间线**——事件发生的时间。

```
Variable A: Top customer (28% ARR) gives 60-day termination notice
  Probability: 15% | Timeline: Within 90 days

Variable B: Series A fundraise delayed 6 months beyond target close
  Probability: 25% | Timeline: Q3

Variable C: Lead engineer resigns
  Probability: 20% | Timeline: Unknown
```

### 第二步：领域影响映射（Domain Impact Mapping）

对于每个变量，相关角色需要评估其影响：

| 领域 | 负责人 | 影响因素 |
|--------|-------|--------|
| 现金流与运营周期 | 财务总监（CFO） | 现金消耗、运营周期变化、临时解决方案 |
| 收入 | 销售总监（CRO） | 年收入（ARR）缺口、客户流失风险、销售渠道 |
| 产品 | 产品总监（CPO） | 产品路线图影响、关键人员风险 |
| 工程技术 | 技术总监（CTO） | 项目进展速度影响、关键人员风险 |
| 人力资源 | 人力资源总监（CHRO） | 人员流失风险、招聘冻结的影响 |
| 运营 | 运营总监（COO） | 生产能力、关键绩效指标（OKR）影响、流程风险 |
| 安全 | 安全总监（CISO） | 合规性风险 |
| 市场 | 市场总监（CMO） | 客户获取成本（CAC）影响、市场竞争风险 |

### 第三步：连锁效应映射（Cascade Effect Mapping）

这是核心步骤。展示变量A如何引发其他领域的后果，进而导致变量B的影响：

```
TRIGGER: Customer churn ($560K ARR)
  ↓
CFO: Runway drops 14 → 8 months
  ↓
CHRO: Hiring freeze; retention risk increases (morale hit)
  ↓
CTO: 3 open engineering reqs frozen; roadmap slips
  ↓
CPO: Q4 feature launch delayed → customer retention risk
  ↓
CRO: NRR drops; existing accounts see reduced velocity → more churn risk
  ↓
CFO: [Secondary cascade — potential death spiral if not interrupted]
```

明确指出这种连锁效应的路径，并指出可能被中断的环节。

### 第四步：严重程度矩阵（Severity Matrix）

模拟三种情景：
| 情景 | 定义 | 应对措施 |
|----------|------------|---------|
| **基础情景** | 仅一个变量受到影响 | 通过计划可以应对 |
| **压力情景** | 两个变量同时受到影响 | 需要重大响应 |
| **严重情景** | 所有变量都受到影响 | 影响企业生存，需要董事会介入 |

对于每种严重程度，评估以下方面：
- 现金流影响
- 年收入（ARR）影响
- 人员数量影响
- 企业陷入不可接受状态的时间线

### 第五步：触发点（Early Warning Signals）

定义在情景确认之前可以检测到的可测量信号：

```
Trigger for Customer Churn Risk:
  - Sponsor goes dark for >3 weeks
  - Usage drops >25% MoM
  - No Q1 QBR confirmed by Dec 1

Trigger for Fundraise Delay:
  - <3 term sheets after 60 days of process
  - Lead investor requests >30-day extension on DD
  - Competitor raises at lower valuation (market signal)

Trigger for Engineering Attrition:
  - Glassdoor activity from engineering team
  - 2+ referral interview requests from engineers
  - Above-market offer counter-required in last 3 months
```

### 第六步：应对策略（Hedging Strategies）

针对每种情景，制定**现在**（在情景发生之前）应采取的措施，以减少其影响：

| 应对策略 | 成本 | 影响 | 负责人 | 截止日期 |
|-------|------|--------|-------|---------|
| 设立50万美元的信用额度 | 5000美元/年 | 如果发生客户流失，可维持3个月运营 | 财务总监（CFO） | 60天内 |
| 为3名关键工程师提供12个月的留任奖金 | 9万美元 | 通过融资确保团队稳定 | 人力资源总监（CHRO） | 30天内 |
| 将客户收入集中度降低到20%以下 | 销售团队 | 降低单一客户的风险 | 销售总监（CRO） | 两个季度内 |
| 缩短融资时间，同时启动其他融资渠道 | 首席执行官（CEO） | 在资金链断裂前完成融资 | 首席执行官（CEO） | 立即执行 |

---

## 输出格式

每次战争室会议都会生成以下内容：

```
SCENARIO: [Name]
Variables: [A, B, C]
Most likely path: [which combination actually plays out, with probability]

SEVERITY LEVELS
Base (A only): [runway/ARR impact] — recovery: [X actions]
Stress (A+B): [runway/ARR impact] — recovery: [X actions]
Severe (A+B+C): [runway/ARR impact] — existential risk: [yes/no]

CASCADE MAP
[A → domain impact → B trigger → domain impact → end state]

EARLY WARNING SIGNALS
- [Signal 1 → which scenario it indicates]
- [Signal 2 → which scenario it indicates]
- [Signal 3 → which scenario it indicates]

HEDGES (take these actions now)
1. [Action] — cost: $X — impact: [what it buys] — owner: [role] — deadline: [date]
2. [Action] — cost: $X — impact: [what it buys] — owner: [role] — deadline: [date]
3. [Action] — cost: $X — impact: [what it buys] — owner: [role] — deadline: [date]

RECOMMENDED DECISION
[One paragraph. What to do, in what order, and why.]
```

---

## 优秀战争室会议的规则

- **每个场景最多包含3个变量**。超过3个变量会导致分析混乱——你无法有效地为涉及5个变量的复杂情况做好准备。只需关注真正令人担忧的3个变量。
- **进行量化或估算**。“收入下降”这样的描述不够具体。“60天内年收入可能减少42万美元”则更有参考价值。如果不确定，可以使用范围来表示。
- **不要仅停留在初步影响上**。真正的损害通常体现在连锁反应中，而不仅仅是最初的冲击。
- **不仅要模拟影响，还要规划应对措施**。每个情景都应包含明确的应对方案。
- **区分基础情景和敏感性分析**。不要将“可能发生的情况”与“必然发生的情况”混为一谈。
- **不要过度建模**。每个规划周期模拟3-4个情景即可。过多的情景会导致分析效率低下。

---

## 常见情景类型

**种子情景（Seed Scenarios）：**
- 共同创始人离职 + 产品发布失败
- 资金耗尽 + 临时融资条款不利

**A系列情景（Series A Scenarios）：**
- 年收入目标未达成 + 融资延迟
- 关键客户流失 + 竞争对手筹集资金

**B系列情景（Series B Scenarios）：**
- 市场萎缩 + 多次资金消耗高峰
- 首席投资者要求业务调整 + 团队抗拒改变

## 与高管团队的协作（Integration with C-Suite Roles）

| 情景类型 | 主要负责人 | 可能波及的部门 |
|--------------|---------------|------------|
| 收入未达标 | 销售总监（CRO）、财务总监（CFO） | 市场总监（CMO，负责销售渠道）、运营总监（COO，负责裁员） |
| 关键人员离职 | 人力资源总监（CHRO）、运营总监（COO） | 技术总监（CTO，如果涉及工程技术部门）；销售总监（CRO，如果涉及销售部门） |
| 融资失败 | 财务总监（CFO）、首席执行官（CEO） | 运营总监（COO，负责延长运营周期）；人力资源总监（CHRO，负责招聘冻结） |
| 安全漏洞 | 安全总监（CISO）、技术总监（CTO） | 首席执行官（CEO，负责沟通）；财务总监（CFO，负责成本控制）；销售总监（CRO，负责客户关系） |
| 市场变化 | 首席执行官（CEO）、产品总监（CMO） | 市场总监（CMO，负责调整市场策略）；销售总监（CRO，负责开拓新市场） |
| 竞争对手行动 | 市场总监（CMO）、销售总监（CRO） | 产品总监（CPO，负责调整产品路线图）；首席执行官（CEO，负责制定战略） |

## 参考资料
- `references/scenario-planning.md` — 场景规划方法论、事后分析（post-mortem）方法、蒙特卡洛（Monte Carlo）模拟、连锁效应模型框架
- `scripts/scenario_modeler.py` — 用于结构化场景建模的命令行工具