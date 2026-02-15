# 预算与支出追踪器 — AI助手财务指挥中心

通过与您的AI助手进行自然对话，您可以追踪每一笔支出、执行预算、识别消费模式并积累财富。

## 工作原理

您可以自然地与助手交流，例如：“我在食品杂货上花了45美元”或“这个月我在食物上的支出是多少？”助手会维护一个本地的JSON账本，执行您的预算设置，并每周/每月为您提供财务分析。

---

## 1. 设置 — 您的财务档案

首次使用时，请在工作区创建 `budget-profile.json` 文件：

```json
{
  "currency": "USD",
  "monthlyIncome": 5000,
  "payDays": [1, 15],
  "fiscalMonthStart": 1,
  "categories": {
    "housing": { "budget": 1500, "essential": true },
    "food": { "budget": 600, "essential": true, "subcategories": ["groceries", "dining", "delivery", "coffee"] },
    "transport": { "budget": 300, "essential": true, "subcategories": ["fuel", "public", "rideshare", "parking"] },
    "utilities": { "budget": 200, "essential": true, "subcategories": ["electric", "water", "internet", "phone"] },
    "health": { "budget": 200, "essential": true, "subcategories": ["gym", "medical", "supplements"] },
    "entertainment": { "budget": 200, "essential": false, "subcategories": ["streaming", "games", "events", "hobbies"] },
    "shopping": { "budget": 300, "essential": false, "subcategories": ["clothes", "electronics", "home", "gifts"] },
    "education": { "budget": 100, "essential": false, "subcategories": ["books", "courses", "subscriptions"] },
    "savings": { "budget": 500, "essential": true, "target": "emergency-fund" },
    "misc": { "budget": 100, "essential": false }
  },
  "alerts": {
    "budgetWarning": 0.75,
    "budgetCritical": 0.90,
    "unusualSpend": 2.0,
    "dailyMax": 200
  },
  "goals": []
}
```

根据您的需求自定义支出类别、预算和子类别。助手会自动适应您定义的结构。

---

## 2. 账本 — 交易格式

所有交易记录存储在 `budget-ledger.json` 文件中：

```json
{
  "transactions": [
    {
      "id": "tx_20260213_001",
      "date": "2026-02-13",
      "type": "expense",
      "amount": 45.67,
      "category": "food",
      "subcategory": "groceries",
      "description": "Weekly shop at Aldi",
      "merchant": "Aldi",
      "paymentMethod": "debit",
      "tags": ["weekly", "essentials"],
      "recurring": false,
      "note": ""
    }
  ],
  "recurringRules": [],
  "metadata": {
    "lastUpdated": "2026-02-13T10:30:00Z",
    "transactionCount": 1,
    "ledgerVersion": "1.0"
  }
}
```

### 交易ID规则
`tx_YYYYMMDD_NNN` — 日期 + 顺序编号。请勿重复使用ID。

---

## 3. 自然语言解析

当用户提到与金钱相关的信息时，系统会将其解析为交易记录：

### 解析规则

| 用户输入 | 解析结果 |
|-----------|-----------|
| “我在食品杂货上花了45美元” | 支出，45美元，食品/杂货 |
| “支付了1500美元的房租” | 支出，1500美元，住房 |
| “收到了2500美元的收入” | 收入，2500美元，工资 |
| “使用Uber花费了12美元” | 支出，12美元，交通/拼车 |
| “每月Netflix费用15.99美元” | 支出，15.99美元，娱乐/流媒体，定期支出 |
| “咖啡5美元” | 支出，5美元，食品/咖啡 |
| “给妈妈转了200美元” | 支出，200美元，其他（询问：是礼物还是借款？） |
| “退回鞋子获得了80美元退款” | 退款，80美元，购物/服装 |

### 异常情况处理
- 如果类别不明确，请做出最佳猜测并确认：“将45美元记录在‘食品/杂货’类别下，正确吗？” |
- 如果金额缺失，询问：“具体是多少？” |
- 如果提到“每月”或“每周”，则创建定期支出规则 |
- “退回”或“退款”视为负支出（收入） |
- “借出”与“借用”需明确区分方向 |

### 定期支出
当用户提到定期支出时，系统会自动创建相应的规则：

```json
{
  "id": "rec_001",
  "description": "Netflix subscription",
  "amount": 15.99,
  "category": "entertainment",
  "subcategory": "streaming",
  "frequency": "monthly",
  "dayOfMonth": 15,
  "active": true,
  "lastApplied": "2026-02-15"
}
```

在每次预算检查时，系统会自动应用这些定期支出规则。

---

## 4. 预算执行引擎

### 实时预算检查

每次记录支出后，系统会立即进行预算检查：

```
1. Calculate total spent in category this month
2. Compare to budget limit
3. Calculate percentage used
4. Check days remaining in month
5. Calculate daily budget remaining
6. Trigger alerts if needed
```

### 警报级别

| 级别 | 触发条件 | 反应 |
|-------|---------|----------|
| 🟢 在预算范围内 | 预算使用率低于75%，与当月进度相符 | 无声提示（仅记录） |
| 🟡 警告 | 预算使用率为75%-90% | “注意：您已经使用了600美元食品预算的78%，还剩18天。每天剩余3.67美元。” |
| 🔴 危险 | 预算使用率超过90% | “⚠️ 食品预算使用率为92%（552美元/600美元），还剩12天。每天仅剩4美元。” |
| 🚨 超出预算 | 预算使用率超过100% | “🚨 您的食品预算超出了600美元，实际支出为647美元。这会影响您的储蓄目标。” |
| ⚡ 异常支出 | 单笔支出超过该类别的平均水平 | “这次89美元的咖啡支出似乎不寻常——您的平均支出是5.20美元。金额正确吗？” |

### 支出节奏追踪（智能预算分析）

不仅仅是追踪总金额，还要关注支出节奏：

```
Days elapsed this month: 13
Days remaining: 15
Budget: $600
Spent so far: $380
Daily pace: $29.23/day (spending)
Sustainable pace: $21.43/day (budget / total days)
Remaining pace: $14.67/day (remaining budget / remaining days)

Verdict: Spending 37% faster than sustainable. Will exceed budget by ~$160 at current pace.
```

这比单纯显示“您在某类别上花费了X美元”更有用，因为它能预测未来的支出趋势。

---

## 5. 储蓄目标

### 目标设置

```json
{
  "id": "goal_001",
  "name": "Emergency Fund",
  "targetAmount": 10000,
  "currentAmount": 3500,
  "deadline": "2026-12-31",
  "priority": "high",
  "contributions": [
    { "date": "2026-02-01", "amount": 500, "note": "Monthly auto-save" }
  ],
  "autoContribute": {
    "enabled": true,
    "amount": 500,
    "frequency": "monthly",
    "dayOfMonth": 1
  }
}
```

### 目标分析

在检查储蓄目标时，系统会计算：
- **是否按计划进行？** 比较当前的储蓄率与目标储蓄率 |
- **预计完成时间：** 按当前储蓄率计算，目标何时能实现？ |
- **加速建议：** “如果您每月多存100美元，可以提前两个月达成目标” |
- **剩余资金分配：** 如果本月预算有结余，建议将多余资金用于储蓄目标 |

---

## 6. 报告与分析

### 每周总结（每周日或按需生成）

```
📊 Week of Feb 7-13, 2026

💸 Spent: $487.23
💰 Income: $2,500.00
📈 Net: +$2,012.77

Top categories:
  🏠 Housing: $375 (rent proration)
  🍔 Food: $112.23 (18.7% of budget used, on track)

⚡ Unusual: $0 flagged
🎯 Goals: Emergency Fund 35% → 40% (+$500)
💡 Insight: Food spending down 12% vs last week. Nice work.
```

### 每月报告（每月1日生成）

```
📊 January 2026 — Full Report

INCOME:         $5,000.00
EXPENSES:       $3,847.23
NET SAVINGS:    $1,152.77 (23.1% savings rate)

BUDGET PERFORMANCE:
  ✅ Housing:      $1,500 / $1,500 (100%) — on budget
  ✅ Food:         $534 / $600 (89%) — $66 under
  ✅ Transport:    $187 / $300 (62%) — $113 under
  ⚠️ Shopping:     $342 / $300 (114%) — $42 OVER
  ✅ Entertainment: $156 / $200 (78%) — $44 under

CATEGORY TRENDS (vs last month):
  📈 Food: +8% ($534 vs $495)
  📉 Transport: -23% ($187 vs $243) — nice!
  📈 Shopping: +37% ($342 vs $250) — watch this

SAVINGS GOALS:
  🎯 Emergency Fund: $4,000 / $10,000 (40%) — on track for Aug completion
  🎯 Vacation: $800 / $2,000 (40%) — on track

TOP MERCHANTS:
  1. Aldi — $178 (12 visits)
  2. Amazon — $156 (8 orders)
  3. Shell — $89 (6 fills)

💡 INSIGHTS:
  • Shopping was 14% over budget — 3 Amazon orders on Feb 8 totaled $120
  • You saved $113 on transport (worked from home more?)
  • At current savings rate ($1,153/mo), emergency fund complete by August
  • Consider moving $66 food surplus → vacation goal
```

### 年度总结（按需生成）

```
📊 2026 YTD (Jan-Feb)

Total Income:    $10,000
Total Expenses:  $7,694
Total Saved:     $2,306 (23.1% rate)
Goal Progress:   Emergency Fund 40%, Vacation 40%

Best month: January (24.2% savings rate)
Worst category: Shopping (avg 107% of budget)
Most improved: Transport (-15% trend)
```

---

## 7. 智能洞察功能

除了基本追踪外，系统还提供可操作的财务建议：

### 消费模式分析
- **周末消费较高**：“您周末的支出比工作日高出40%。周六平均支出为67美元，工作日为23美元。” |
- **商家忠诚度分析**：“您本月去了18次Starbucks。如果在家自己煮咖啡，3周内就能回本。” |
- **支出趋势**：“过去3个月，购物支出每月增加15%。预计下个月将达到450美元。”

### 优化建议
- **订阅服务审核**：“您有6项流媒体服务（每月78美元）。其中Netflix使用了20次，Disney+仅使用了一次。可以考虑取消Disney+。” |
- **预算调整**：“您连续3个月的交通支出低于预算。可以考虑将预算调整为200美元，并将100美元用于储蓄。” |
- **现金流管理**：“您的最大支出集中在每月1日至5日。可以考虑将部分支出调整到下一次发薪日。” |

### 财务健康评分（0-100分）

系统每月计算评分：

| 评分因素 | 权重 | 分数 |
|--------|--------|---------|
| 储蓄率 | 30% | 20%及以上 = 100分，10%-20% = 70分，5%-10% = 40分，低于5% = 10分 |
| 预算遵守情况 | 25% | 预算完全遵守 = 100分，超出预算1% = 80分，超出2%-3% = 50分，超出4% = 20分 |
| 目标达成情况 | 20% | 按计划进行 = 100分，略落后 = 60分，严重落后 = 20分 |
| 支出稳定性 | 15% | 支出波动小 = 100分，中等 = 60分，波动大 = 20分 |
| 无债务支出 | 10% | 无债务 = 100分，有债务 = 50分 |

评分解读：
- 90-100分：💪 表现优秀，适合财富积累 |
- 70-89分：👍 需进行小幅度优化 |
- 50-69分：⚠️ 需关注某些方面 |
- 低于50分：🚨 需立即采取措施 |

---

## 8. 命令参考

| 命令 | 功能 |
|---------|-------------|
| “我在Y项目上花费了X美元” | 记录支出 |
| “收到了X美元的收入” | 记录收入 |
| “预算检查” | 显示所有预算与实际支出情况 |
| “每周总结” | 生成本周报告 |
| “每月报告” | 生成本月完整分析 |
| “食物支出是多少？” | 详细查看食物类别的支出情况 |
| “将食物预算设置为500美元” | 更新预算 |
| “设定目标：6月前存2000美元用于度假” | 创建储蓄目标 |
| “为度假存200美元” | 记录储蓄进度 |
| “查看财务健康状况” | 计算财务健康评分 |
| “有异常支出吗？” | 标出异常支出 |
| “订阅服务审核” | 列出所有定期支出和服务使用情况 |
| “与上月对比” | 显示月度支出趋势 |
| “导出CSV” | 将账本数据导出为CSV文件 |
| “撤销上一次操作” | 删除最后一次交易记录 |

---

## 9. 数据管理

### 文件位置
- `budget-profile.json` — 您的财务档案和预算设置 |
- `budget-ledger.json` — 所有交易记录 |
- `budget-goals.json` | 储蓄目标和进度 |
- `budget-recurring.json` | 定期支出规则 |

### CSV导出格式
当用户请求导出数据时：

```csv
Date,Type,Amount,Category,Subcategory,Description,Merchant,Tags
2026-02-13,expense,45.67,food,groceries,Weekly shop,Aldi,"weekly,essentials"
```

### 数据备份
定期提醒用户备份账本数据。如果工作区是代码仓库，可以建议用户将数据提交到Git。

### 隐私保护
所有数据仅存储在本地，不使用外部API，也不进行云同步。您的财务数据不会离开您的设备。

---

## 10. 特殊情况处理

- **分摊支出**：“晚餐花费80美元，与朋友平摊” → 记录您应承担的40美元 |
- **外币支出**：“在巴黎花费了50欧元” → 按当前汇率转换，并标注原始货币 |
- **返现/奖励**：将其记录为“返现”类别的收入 |
- **账户间转账**：不计入支出或收入，记录为“转账”类型 |
- **共同支出**：标注为“共同支出”，并记录各自应承担的金额 |
- **可抵扣税项**：标注为“可抵扣税项”，以便年末统计 |
- **同月内的退款**：在相应类别中抵消支出 |
- **收入波动**：如果收入不稳定，使用3个月的平均值进行预算计算 |

---

---

这个AI助手通过自然语言交互，帮助您全面管理财务，实现预算控制、储蓄目标设定和财务健康评估。