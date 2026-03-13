---
name: budget-pro
description: >
  **个人预算管理工具：以隐私保护为核心，采用本地存储技术**  
  适用于用户需要设置预算、记录支出、核对费用明细、查看预算执行情况或按类别管理资金的情况。该工具能够实时追踪收入、支出以及各类预算的收支情况，并通过主动提醒帮助用户更好地控制财务。**绝对不会访问银行账户或任何外部金融服务**。
---
# 预算管理工具

这是一个具备主动追踪功能的个人预算管理系统。它私密、简单且高效。

## 高度的隐私与安全性

### 数据存储（至关重要）
- **所有预算数据仅存储在本地**：`memory/budget/`
- **不使用任何外部API来处理财务数据**
- **不连接银行账户**——所有操作均需手动输入
- **不向任何财务应用程序或服务传输数据**
- 用户可完全控制数据的保留和删除

### 安全原则（不可妥协）
- ✅ 通过手动输入按类别记录支出
- ✅ 在预算达到70%、90%或100%时发出警报
- ✅ 生成报告并提供支出分析
- ✅ 提供类别间的资金重新分配建议
- ❌ **绝不连接银行账户**或信用卡
- ❌ **绝不访问任何外部金融服务**
- ❌ **绝不在预算调整之外提供财务建议**
- ❌ **绝不存储敏感的财务信息**

## 快速入门

### 数据存储设置
预算数据存储在您的本地工作目录中：
- `memory/budget/budget.json` – 按类别划分的月度预算限额
- `memory/budget/expenses.json` – 所有已记录的支出
- `memory/budget/income.json` – 收入来源
- `memory/budget/reports/` – 生成的报告和分析结果

请使用 `scripts/` 目录中的脚本进行所有数据操作。

## 核心工作流程

### 设置预算
```
User: "My food budget is $500 per month"
→ Use scripts/set_budget.py --category food --limit 500 --period monthly
→ Store budget limit
```

### 记录支出
```
User: "I spent $45 on groceries"
→ Use scripts/log_expense.py --amount 45 --category food --description "groceries"
→ Check against budget, alert if thresholds crossed
```

### 检查预算状况
```
User: "How is my budget this month?"
→ Use scripts/budget_status.py --period month
→ Show all categories with spent/remaining/status
```

### 查询支出类别
```
User: "What can I still spend on dining?"
→ Use scripts/category_status.py --category dining
→ Show remaining budget for specific category
```

### 处理超出预算的情况
```
User: "I went over on entertainment"
→ Use scripts/overage_analysis.py --category entertainment
→ Show overage amount and suggest recovery options
```

### 生成报告
```
User: "Show me my spending report"
→ Use scripts/generate_report.py --type weekly
→ Generate detailed spending analysis
```

## 模块参考

有关每个模块的详细实现方式，请参阅：
- **预算设置**：[references/budget-setup.md](references/budget-setup.md)
- **支出追踪**：[references/expense-tracking.md](references/expense-tracking.md)
- **警报与阈值**：[references/alerts.md](references/alerts.md)
- **报告与分析**：[references/reports.md](references/reports.md)
- **超出预算的处理**：[references/overage-recovery.md](references/overage-recovery.md)

## 脚本参考

所有数据操作均通过 `scripts/` 目录中的脚本完成：

| 脚本 | 功能 |
|--------|---------|
| `set_budget.py` | 设置或更新预算 |
| `log_expense.py` | 记录支出 |
| `delete_expense.py` | 删除或更正支出记录 |
| `budget_status.py` | 显示整体预算状况 |
| `category_status.py` | 显示特定类别的预算情况 |
| `list_expenses.py` | 查看支出历史 |
| `overage_analysis.py` | 分析超出预算的情况并提供恢复建议 |
| `reallocate_budget.py` | 在不同类别间重新分配预算 |
| `generate_report.py` | 生成支出报告 |
| `export_data.py` | 导出预算数据（CSV/JSON格式）

## 默认预算类别

| 类别 | 典型预算占比 | 常见支出项目 |
|----------|---------------|-----------------|
| 房屋 | 25-35% 的收入 | 租金、房贷、保险 |
| 食物 | 10-15% 的收入 | 食品杂货、外出就餐 |
| 交通 | 10-15% 的收入 | 油费、公共交通费用、车辆维护 |
| 公用事业 | 5-10% 的收入 | 电费、燃气费、互联网费用、电话费 |
| 娱乐 | 5-10% 的收入 | 电影票、爱好相关费用、订阅服务 |
| 健康 | 5-10% 的收入 | 保险费、医疗费用、健身费用 |
| 购物 | 5-10% 的收入 | 服装、家居用品 |
| 储蓄 | 10-20% 的收入 | 应急基金、投资 |

可根据需要添加自定义类别。

## 免责声明

本工具仅提供预算追踪和管理功能，不提供财务建议、投资建议或税务指导。如需进行财务规划，请咨询合格的财务顾问。