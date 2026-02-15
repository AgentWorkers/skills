---
name: expense-tracker-pro
description: 通过自然语言记录支出，获取支出汇总信息，并设置预算。
author: clawd-team
version: 1.0.0
triggers:
  - "log expense"
  - "track spending"
  - "what did I spend"
  - "budget check"
  - "expense report"
---

# Expense Tracker Pro

通过自然语言轻松记录您的支出。无需使用任何应用程序或电子表格——只需告诉Clawd您花费了多少钱即可。

## 功能介绍

- 从自然语言中记录支出（例如：“我在食品杂货上花费了45美元”）。
- 自动对支出进行分类，并与预算进行对比。
- 根据需要提供支出汇总。
- 所有数据会保存在您的本地Clawd内存中。

## 使用方法

**记录支出：**
```
"Spent $23.50 on lunch"
"$150 for electricity bill"
"Coffee $4.75"
```

**查看支出情况：**
```
"What did I spend this week?"
"Show my food expenses this month"
"Am I over budget on entertainment?"
```

**设置预算：**
```
"Set grocery budget to $400/month"
"Budget $100 for entertainment"
```

**生成报告：**
```
"Monthly expense breakdown"
"Compare spending to last month"
"Export expenses to CSV"
```

## 支出类别

系统会根据上下文自动识别以下类别：
- 食品与餐饮
- 交通费用
- 公共事业费用
- 娱乐开支
- 购物费用
- 健康相关支出
- 订阅服务
- 其他

您也可以手动指定支出类别，例如：“我在[商品名称]上花费了50美元，类别为[具体类别]”。

## 使用技巧

- 请详细说明支出金额，以确保记录的准确性。
- 对于订阅服务，请使用“recurring”（例如：“Netflix订阅费用为每月15美元”）。
- 可以查询“支出趋势”以了解长期支出情况。
- 所有数据都保存在您的本地设备上。