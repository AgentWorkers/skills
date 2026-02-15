---
name: revnet-modeler
description: |
  Revnet simulation and planning tool for modeling token dynamics. Use when: (1) planning
  revnet parameters before deployment, (2) visualizing treasury/token dynamics over time,
  (3) comparing different scenarios (loans, cash-outs, investments), (4) understanding
  chart outputs, (5) explaining simulation results. Covers stage configuration, event
  sequences, and all chart types.
---

# Revnet Modeler：仿真工具

## 问题

规划revnet参数需要了解不同配置如何影响
资金库动态、代币分配以及参与者的长期收益。该建模工具在部署前会模拟这些动态变化。

## 使用场景/触发条件

- 规划新的revnet部署
- 比较不同的参数配置
- 了解事件（投资、贷款、提现）对系统的影响
- 可视化资金库和代币的动态变化
- 向用户解释图表输出结果

## 解决方案

### 工具位置

```
https://github.com/mejango/rev-sim/index.html
```

在浏览器中打开该工具即可使用交互式建模功能。

### 七个经济调控杠杆（每个阶段均可配置）

每个阶段可以配置以下参数：

| 杠杆 | 描述 | 影响 |
|-------|-------------|--------|
| **阶段开始日期** | 该阶段开始的时间 | 定义阶段之间的转换 |
| **初始发行率** | 每美元发行的代币数量 | 发行率越高，每次支付获得的代币越多 |
| **发行削减百分比** | 每个周期的削减比例 | 随时间增加代币的稀缺性 |
| **发行削减频率** | 削减发生的间隔天数 | 控制削减频率（7天、14天、28天） |
| **分配比例** | 发行代币中用于分配给团队/预留的比例 |
| **提现税率** | 代币的税收（0-100%） | 税率越高，资金库保留的代币越多 |
| **自动发行** | 自动发行代币 | 预定的分配计划 |

### 事件类型

该建模工具支持以下事件类型：

| 事件 | 描述 | 对资金库的影响 |
|-------|-------------|-----------------|
| `investment` | 外部投资 | 增加资金库支持，增加代币供应 |
| `revenue` | 经营收入 | 增加资金库支持，增加代币供应 |
| `loan` | 用代币借款 | 减少资金库支持（扣除费用后） |
| `payback-loan` | 偿还贷款 | 增加资金库支持 |
| `cashout` | 提现代币 | 减少资金库支持，减少代币供应 |

事件会标注发起者（例如：“团队”、“投资者A”、“客户”）。

### 可用的图表

#### 资金库与价值图表

| 图表 | 显示内容 | 关键信息 |
|-------|-------|-------------|
| **资金库支持** | 随时间变化的总支持量 | 资金库的整体健康状况 |
| **提现价值** | 每个代币的赎回价值 | 代币的最低价格动态 |
| **发行价格** | 代币的发行成本 | 包含削减后的最高价格 |
| **现金流** | 每日的资金流入/流出 | 事件对资金库的影响 |

#### 代币图表

| 图表 | 显示内容 | 关键信息 |
|-------|-------|-------------|
| **代币分配** | 持有者持有的代币分布（流动代币+锁定代币） | 谁持有多少代币 |
| **持有比例** | 随时间变化的持有百分比 | 代币稀释情况 |
| **代币估值** | 持有代币的美元价值 | 参与者的财富 |
| **代币表现** | 按参与者计算的ROI百分比 | 投资回报 |

#### 贷款图表

| 图表 | 显示内容 | 关键信息 |
|-------|-------|-------------|
| **贷款潜力** | 持有者可借款的最大金额 | 可用的流动性 |
| **贷款状态** | 未偿还的贷款金额 | 当前债务 |
| **未偿还贷款** | 随时间变化的贷款金额 | 债务走势 |
| **代币作为贷款抵押的比例** | 代币中用于抵押的比例 | 债务风险 |

#### 费用图表

| 图表 | 显示内容 | 关键信息 |
|-------|-------|-------------|
| **费用流向** | 内部费用与外部费用 | 费用的去向分布 |

### 状态机计算

该建模工具使用状态机（`StateMachine.getStateAtDay(day)`来跟踪系统的状态变化：

```javascript
{
  day: number,
  revnetBacking: number,      // Treasury balance
  totalSupply: number,        // Total token supply
  tokensByLabel: {            // Tokens held by each participant
    "Team": 1000,
    "Investor A": 500,
    ...
  },
  dayLabeledInvestorLoans: {  // Outstanding loan amounts by participant
    "Team": 50000,
    ...
  },
  loanHistory: {              // Detailed loan records
    "Team": [
      { amount: 50000, remainingTokens: 100, ... }
    ]
  }
}
```

### 关键公式

#### 提现价值（债券曲线）

```javascript
calculateCashOutValueForEvent(tokensToCash, totalSupply, backing, cashOutTax) {
  const proportionalShare = backing * tokensToCash / totalSupply
  const taxMultiplier = (1 - cashOutTax) + (tokensToCash * cashOutTax / totalSupply)
  return proportionalShare * taxMultiplier
}
```

#### 贷款费用

```javascript
// Internal fee (to treasury)
const internalFee = loanAmount * 0.025  // 2.5%

// External fee (to protocol)
const externalFee = loanAmount * 0.035  // 3.5%

// Interest (after grace period)
const annualInterest = 0.05  // 5% after 6-month grace period
```

### 预置场景

该建模工具包含以下预设场景：

| 场景 | 描述 |
|----------|-------------|
| `conservative-growth` | 稳定投资，逐步扩张 |
| `hypergrowth` | 快速投资，高波动性 |
| `bootstrap-scale` | 从小规模开始，然后逐步扩大 |
| `vc-fueled` | 初始大量投资，随后依靠收入增长 |
| `community-driven` | 多次小额投资 |
| `boom-bust` | 先增长后出现大量提现 |

每个场景都有不同的变体：`-with-loans`（包含贷款情况）和`-with-exits`（包含退出情况）。

### 解释结果

#### 资金库健康状况
- **健康**：资金库支持随时间增长，最低价格上升 |
- **警告**：资金库支持停滞或下降，出现大量提现 |
- **危急**：大量贷款违约，资金库状况恶化

#### 代币分配
- **平衡**：没有单一持有者持有超过50%的代币 |
- **集中**：少数持有者控制大部分代币 |
- **稀释**：早期持有者的代币被大幅稀释

#### 贷款风险
- **安全**：用于抵押的代币比例低于20% |
- **中等**：20-50%的代币用于抵押 |
- **高风险**：超过50%的代币用于抵押（系统风险较高）

### 使用方法

1. 设置与您的融资/增长计划相匹配的阶段 |
2. 添加代表预期投资、收入和退出事件的事件 |
3. 运行模拟并查看图表 |
4. 逐步调整参数，直到模拟结果符合目标 |
5. 比较多个场景以进行压力测试

## 验证

1. 确认提现计算结果符合债券曲线公式 |
2. 检查贷款费用总和是否达到预期百分比 |
3. 验证代币分配是否计入总供应量 |
4. 确认资金库余额等于资金流入量减去流出量

## 示例

规划一个包含团队分配和投资者参与的revnet项目：

```
Stage 1 (Days 0-90):
  - Issuance: 1,000,000 tokens/$
  - Split: 30% to Team
  - Cash-out tax: 10%

Events:
  Day 1: Team invests $10,000
  Day 30: Investor A invests $50,000
  Day 60: Revenue $20,000
  Day 90: Team takes loan (50% of tokens)

Run simulation → Review:
  - Token Distribution: Team 30%, Investor A 50%, Revenue recipients 20%
  - Team's loan potential and actual loan
  - Treasury backing trajectory
  - Cash-out value for each participant
```

## 注意事项

- 该建模工具使用简化的费用模型（可能与实际合同实现有所不同） |
- 在输入相同的情况下，模拟结果是确定性的 |
- 参数变化时图表会自动更新 |
- 可导出场景以供比较和记录 |
- 该工具完全在客户端运行（不会向外发送数据）

## 参考资料

- 工具：`https://github.com/mejango/rev-sim/index.html`
- 状态机：`https://github.com/mejango/rev-sim/js/state.js`
- 图表组件：`https://github.com/mejango/rev-sim/js/chartManager.js`
- 学术验证：`/revnet-economics`技能相关资料