---
name: "scenario-war-room"
description: "跨职能的“假设情景建模”适用于涉及多个变量的复杂场景。与基于单一假设的压力测试不同，该方法能够同时模拟所有业务职能所面临的复合性风险。当面临复杂的风险场景、具有重大负面影响的战略决策，或者用户提出“如果X和Y同时发生会怎样？”这样的问题时，可以使用这种方法。"
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
# 情景战争室（Scenario War Room）

该工具能够模拟所有业务功能中的连锁性“假设情景”（cascading what-if scenarios），而不仅仅是基于单一假设的压力测试（stress tests）。它能够展示一个问题如何引发另一个问题，从而形成复杂的负面效应。

## 关键词
- 情景规划（scenario planning）
- 战争室（war room）
- 假设分析（what-if analysis）
- 风险建模（risk modeling）
- 连锁效应（cascading effects）
- 复合风险（compound risk）
- 应急规划（contingency planning）
- 压力测试（stress test）
- 危机规划（crisis planning）
- 多变量情景（multi-variable scenario）
- 事后分析（post-mortem）

## 快速入门

```bash
python scripts/scenario_modeler.py   # Interactive scenario builder with cascade modeling
```

或者，您可以这样描述一个具体的情景：
```
/war-room "What if we lose our top customer AND miss the Q3 fundraise?"
/war-room "What if 3 engineers quit AND we need to ship by Q3?"
/war-room "What if our market shrinks 30% AND a competitor raises $50M?"
```

## 本工具不是什么

- **不是** 单一假设的压力测试（请参考 `/em:stress-test`）
- **不仅** 用于财务建模**——所有业务功能都会被纳入建模**
- **不仅** 仅关注最坏情况**——会模拟三种不同的风险严重程度**
- **不会** 因分析而陷入停滞**——会提供具体的应对策略和触发条件**

## 框架：六步连锁模型（6-Step Cascade Model）

### 第一步：定义情景变量（最多3个）
为每个变量明确说明：
- **变化内容**——具体且尽可能量化
- **发生概率**——您的最佳估计
- **时间线**——事件发生的时间

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

| 领域 | 负责人 | 模型内容 |
|--------|-------|--------|
| 现金流与业务周期 | 财务总监（CFO） | 现金消耗的影响、业务周期的变化、临时解决方案 |
| 收入（Revenue） | 销售总监（CRO） | 年收入（ARR）的缺口、客户流失的风险、销售管道（pipeline） |
| 产品（Product） | 产品总监（CPO） | 产品路线图的影响、产品市场失败（PMF）的风险 |
| 工程（Engineering） | 技术总监（CTO） | 项目进度的影响、关键人员的风险 |
| 人员（People） | 人力资源总监（CHRO） | 人员流失的情况、招聘冻结的影响 |
| 运营（Operations） | 运营总监（COO） | 生产能力、关键绩效指标（OKR）的影响、流程风险 |
| 安全（Security） | 安全总监（CISO） | 合规性的时间线风险 |
| 市场（Market） | 市场总监（CMO） | 客户获取成本（CAC）的影响、市场竞争的风险 |

### 第三步：连锁效应映射（Cascade Effect Mapping）

这是核心步骤。展示变量A如何触发其他领域的后果，进而引发变量B的影响：

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

明确指出这种连锁反应的路径，并指出可能被中断的环节。

### 第四步：严重程度矩阵（Severity Matrix）

模拟三种情景：

| 情景 | 定义 | 应对措施 |
|----------|------------|---------|
| **基础情景（Base）** | 仅一个变量受到影响 | 可以通过计划进行管理 |
| **压力情景（Stress）** | 两个变量同时受到影响 | 需要采取重大应对措施 |
| **严重情景（Severe）** | 所有变量都受到影响 | 形成系统性危机，需要董事会介入 |

对于每种严重程度，评估以下方面：
- 现金流的影响
- 年收入（ARR）的影响
- 人员数量的影响
- 陷入不可接受状态的时间线（触发点）

### 第五步：触发点（Early Warning Signals）

定义在情景确认之前可以检测到的可量化信号：

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

针对每种情景，制定在情景发生前应采取的**立即行动**，以减少其影响：

| 应对措施 | 成本 | 影响 | 负责人 | 截止日期 |
|-------|------|--------|-------|---------|
| 开设50万美元的信用额度 | 5000美元/年 | 如果发生客户流失，可维持3个月的运营 | 财务总监（CFO） | 60天内 |
| 为3名关键工程师提供12个月的保留奖金 | 9万美元 | 通过融资确保团队稳定 | 人力资源总监（CHRO） | 30天内 |
| 将客户收入集中度降低到20%以下 | 销售团队 | 降低对单一客户的依赖风险 | 销售总监（CRO） | 两个季度内 |
| 缩短融资时间，同时启动其他融资渠道 | 首席执行官（CEO） | 在业务周期重叠前完成融资 | 首席执行官（CEO） | 立即执行 |

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

## 优秀的战争室会议规则

- **每个情景最多包含3个变量**。超过3个变量会导致分析混乱——你无法有效地为涉及5个变量的危机做好准备。只需关注真正让你担心的3个变量。
- **进行量化或估算**。笼统的描述（如“收入下降”没有实际意义）；使用具体的数值范围（例如“60天内年收入可能减少42万美元”）。
- **不要只关注初始影响**。真正的损害通常体现在连锁反应中。
- **不仅要模拟影响，还要规划应对措施**。每个情景都应包含具体的应对方案。
- **区分基础情景和敏感情景**。不要将“可能发生的情况”与“必然会发生的情况”混为一谈。
- **避免过度建模**。每个规划周期模拟3-4个情景最为合适。过多的情景会导致分析效率低下。

---

## 常见情景类型（按发展阶段划分）

**种子阶段（Seed）：**
- 共同创始人离职 + 产品无法按时发布
- 资金耗尽 + 临时融资条款不利

**A系列（Series A）：**
- 未能达到年收入目标 + 融资延迟
- 关键客户流失 + 竞争对手筹集资金

**B系列（Series B）：**
- 市场萎缩 + 多次资金消耗高峰
- 首席投资者要求调整战略 + 团队抗拒改变

## 与高层管理团队的协作（Integration with C-Suite Roles）

| 情景类型 | 主要负责人 | 可能影响的部门/角色 |
|--------------|---------------|------------|
| 收入未达目标 | 销售总监（CRO）、财务总监（CFO） | 市场总监（CMO，负责销售管道）、运营总监（COO，负责裁员） |
| 关键人员离职 | 人力资源总监（CHRO）、运营总监（COO） | 技术总监（CTO，如果涉及工程团队）；销售总监（CRO，如果涉及销售团队） |
| 融资失败 | 财务总监（CFO）、首席执行官（CEO） | 运营总监（COO，负责延长业务周期）、人力资源总监（CHRO，负责招聘冻结） |
| 安全漏洞 | 安全总监（CISO）、技术总监（CTO） | 首席执行官（CEO，负责沟通），财务总监（CFO，负责成本控制），销售总监（CRO，负责客户关系） |
| 市场变化 | 首席执行官（CEO）、产品总监（CMO） | 市场总监（CMO，负责重新定位），销售总监（CRO，负责开拓新市场） |
| 竞争对手的行动 | 市场总监（CMO）、销售总监（CRO） | 产品总监（CPO，负责调整产品路线图），首席执行官（CEO，负责制定战略） |

## 参考资料
- `references/scenario-planning.md` — 情景规划的方法论、事后分析（post-mortem）、蒙特卡洛（Monte Carlo）建模、连锁效应框架
- `scripts/scenario_modeler.py` — 用于结构化情景建模的命令行工具