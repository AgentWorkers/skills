---
name: tax
description: 个人及企业税务管理工具，具备本地文档管理功能。适用于用户需要处理税务申报、税务文件、税收减免、纳税申报、美国国税局（IRS）通知或预估税款支付等场景。该工具可全年跟踪税务相关文件，识别可抵扣项，协助用户准备税务专业会议，并管理税务截止日期。但请注意：本工具绝不提供税务咨询服务，也无法替代持证税务专业人士的职责。
---
# 税务管理

这是一个税务文件管理系统，支持全年税务文件的整理与申报，让您轻松完成税务申报工作。

## 高度重视隐私与安全

### 数据存储（至关重要）
- **所有税务数据仅存储在本地**：`memory/tax/`
- **不使用任何外部API来存储税务数据**
- **不与IRS（美国国税局）或其他税务机构系统连接**
- **不上传任何文件到云端**，所有数据均存储在本地
- 用户可完全控制数据的保留和删除

### 安全准则（不可商讨）
- ✅ 整理税务文件和收据
- ✅ 全年跟踪可抵扣费用
- ✅ 计算预估税款
- ✅ 为与税务专业人士的会议做准备
- ❌ **绝不允许提供税务咨询或申报建议**
- ❌ **绝不允许计算最终的税务责任**（具体取决于所在司法管辖区）
- ❌ **绝不允许替代持证税务专业人士的工作**
- ❌ **绝不允许解释税法或相关法规**

### 法律免责声明
税法因司法管辖区而异，且经常发生变化，具体内容需根据个人情况而定。本工具仅提供税务文件的整理和准备支持。在处理税务申报或复杂问题时，请务必咨询持证税务专业人士。

## 快速入门

### 数据存储设置
税务记录存储在您的本地工作区中：
- `memory/tax/documents.json` – 税务文件清单
- `memory/tax/expenses.json` – 可抵扣费用记录
- `memory/tax/estimated_payments.json` – 季度税款支付记录
- `memory/tax/meetings.json` – 与税务专业人士会议的准备资料
- `memory/tax/deadlines.json` – 税务截止日期和提醒

请使用`scripts/`目录中的脚本进行所有数据操作。

## 核心工作流程

### 添加税务文件
```
User: "I received a 1099 from my client"
→ Use scripts/add_document.py --type "1099" --issuer "Client Name" --amount 5000
→ Log document and categorize
```

### 跟踪可抵扣费用
```
User: "$200 business meal today"
→ Use scripts/track_expense.py --amount 200 --category "business-meal" --date 2024-03-01
→ Track for deduction, check documentation requirements
```

### 计算预估税款
```
User: "How much estimated tax should I pay this quarter?"
→ Use scripts/calculate_estimate.py --quarter Q1 --income 15000
→ Calculate based on income to date and safe harbor rules
```

### 为税务会议做准备
```
User: "Prep me for my accountant meeting"
→ Use scripts/prep_meeting.py --year 2024
→ Generate organized summary of all documents and expenses
```

### 检查截止日期
```
User: "When is my estimated tax due?"
→ Use scripts/check_deadlines.py
→ Show upcoming tax deadlines
```

## 模块参考

如需详细实现指南：
- **文件管理**：请参阅 [references/document-system.md](references/document-system.md)
- **可抵扣费用管理**：请参阅 [references/deductions.md](references/deductions.md)
- **预估税款计算**：请参阅 [references/estimated-taxes.md](references/estimated-taxes.md)
- **税务会议准备**：请参阅 [references/meeting-prep.md](references/meeting-prep.md)
- **IRS通知**：请参阅 [references/irs-notices.md](references/irs-notices.md)
- **年末规划**：请参阅 [references/year-end.md](references/year-end.md)

## 脚本参考

| 脚本 | 功能 |
|--------|---------|
| `add_document.py` | 记录税务文件的接收情况 |
| `track_expense.py` | 跟踪可抵扣费用 |
| `calculate_estimate.py` | 计算预估税款 |
| `check_deadlines.py` | 显示即将到期的税务截止日期 |
| `prep_meeting.py` | 为与税务专业人士的会议做准备 |
| `generate_summary.py` | 生成税务年度总结 |
| `log_irs_notice.py` | 记录并跟踪IRS的通信信息 |
| `set_reminder.py` | 设置税务截止日期提醒 |

## 免责声明

本工具仅提供税务文件的整理和准备支持。税法因司法管辖区而异，且经常发生变化。在处理税务申报或复杂问题时，请务必咨询持证税务专业人士。