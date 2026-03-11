---
name: divorce
description: >
  **离婚流程支持服务**  
  包括财务清单编制、法律准备以及情感辅导。适用于用户提及离婚、分居、子女抚养权、财产分割或离婚诉讼的情况。该服务可协助用户整理财务文件、了解相关流程选项、为律师会议做准备、跟踪截止日期，并协助制定育儿计划。但请注意：我们绝不提供任何法律建议。
---
# 离婚流程管理

本系统旨在帮助用户顺利应对离婚过程中的各项事务，提供有序的组织和指导。

## 高度重视隐私与安全

### 数据存储（至关重要）
- **所有离婚相关数据仅存储在本地**：`memory/divorce/`
- **提供最高级别的隐私保护**，涉及敏感的个人信息
- **严禁任何形式的数据外部共享**
- **建议采用加密存储方式**（文件系统级别）
- 用户可完全控制数据的保留和删除

### 安全注意事项
- ✅ 整理财务文件
- ✅ 说明离婚流程的类型（调解、协商、诉讼）
- ✅ 为律师会议做好准备
- ✅ 监控重要截止日期和要求
- ❌ **严禁提供法律建议**
- ❌ **严禁替代持证的家庭法律师**
- ❌ **严禁保证具体的离婚结果**

### 重要提示
离婚涉及重大的法律和财务后果。本系统仅提供流程管理支持，请务必咨询持证的家庭法律师以获取专业法律指导。

### 数据结构
离婚相关数据存储在本地：
- `memory/divorce/financial_inventory.json`：完整的财务情况
- `memory/divorce/documents.json`：文件整理信息
- `memory/divorce/process.json`：离婚流程类型及时间线
- `memory/divorce/attorney_prep.json`：律师会议准备资料
- `memory/divorce/parenting_plan.json`：抚养权及育儿计划详情
- `memory/divorce/deadlines.json`：关键截止日期

## 核心工作流程

### 财务状况梳理
```
User: "Help me organize my financial documents"
→ Use scripts/financial_inventory.py
→ Build complete inventory of assets, debts, accounts, property
```

### 选择离婚流程类型
```
User: "Should I mediate or go to court?"
→ Use scripts/compare_process.py --situation "amicable but complex assets"
→ Explain mediation, collaborative, litigation options
```

### 为律师会议做准备
```
User: "Prep me for my first attorney meeting"
→ Use scripts/prep_attorney.py
→ Organize financial summary, questions, goals
```

### 制定育儿计划
```
User: "Help me think through custody arrangements"
→ Use scripts/parenting_plan.py
→ Work through physical custody, legal custody, schedules, logistics
```

### 监控截止日期
```
User: "What deadlines do I have coming up?"
→ Use scripts/check_deadlines.py
→ Show disclosure deadlines, court dates, response requirements
```

## 相关参考资料
- **离婚流程类型**：请参阅 [references/process-types.md](references/process-types.md)
- **财务状况梳理**：请参阅 [references/financial-inventory.md](references/financial-inventory.md)
- **律师会议准备**：请参阅 [references/attorney-prep.md](references/attorney-prep.md)
- **育儿计划**：请参阅 [references/parenting-plans.md](references/parenting-plans.md)
- **抚养权相关内容**：请参阅 [references/custody.md](references/custody.md)
- **情绪支持**：请参阅 [references/emotional-support.md](references/emotional-support.md)

## 脚本参考
| 脚本 | 功能 |
|--------|---------|
| `financial_inventory.py` | 生成财务清单 |
| `compare_process.py` | 比较不同的离婚流程选项 |
| `prep_attorney.py` | 为律师会议做准备 |
| `parenting_plan.py` | 制定育儿计划 |
| `check_deadlines.py` | 监控关键截止日期 |
| `log_document.py` | 记录收集到的文件信息 |
| `track_expense.py` | 跟踪离婚相关费用 |
| `self_care_check.py` | 检查用户的情绪健康状况 |