---
name: BudgetLy
description: "智能的基于类别的预算管理工具。可按类别（食物、交通、娱乐等）设置每月预算，记录每项支出的详细情况，查看显示预算与实际支出对比的可视化进度条，接收超支警告，并生成包含支出百分比明细的月度报告。非常适合无需使用电子表格的个人预算管理。"
version: "1.0.0"
author: "BytesAgain"
tags: ["budget","finance","money","spending","savings","personal-finance","categories"]
categories: ["Finance", "Personal Management", "Productivity"]
---
# BudgetLy

BudgetLy 是一个基于类别的预算管理工具，帮助您更好地控制自己的支出。您可以为不同的类别设置预算，记录支出情况，并通过直观的进度条查看实际支出与预算之间的差异。

## 为什么选择 BudgetLy？

- **直观的支出追踪**：进度条让您一目了然地了解各类别的预算使用情况。
- **智能提醒**：当支出接近或超过预算时，系统会发出警告。
- **分类管理**：您可以按食物、交通、娱乐等类别来组织支出。
- **月度报告**：查看您的资金流向，并了解各项支出的占比。
- **本地存储**：您的财务数据始终存储在您的设备上，不会被泄露。

## 命令

- `set <类别> <金额>` — 为某个类别设置每月预算。
- `spend <类别> <金额> [备注]` — 记录该类别的支出情况。
- `status` — 查看所有预算的详细信息，包括进度条和警告提示。
- `report` — 生成包含类别明细的月度支出报告。
- `info` — 显示软件的版本信息。
- `help` — 显示可用的命令列表。

## 使用示例

```bash
budgetly set food 500
budgetly set transport 200
budgetly set entertainment 150
budgetly spend food 45.50 groceries
budgetly spend transport 30 uber
budgetly status
budgetly report
```

## 状态显示

`status` 命令会以可视化的方式显示每个类别的预算使用情况：
```
food         $  245.50/$  500.00 [██████░░░░]  49.1%
transport    $  180.00/$  200.00 [█████████░]  90.0% ⚠️
entertainment$   75.00/$  150.00 [█████░░░░░]  50.0%
```

---
💬 意见与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com