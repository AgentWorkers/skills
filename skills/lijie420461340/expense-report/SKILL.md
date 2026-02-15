---
name: expense-report
description: 整理、分类并汇总业务支出，以便用于报销和税务申报。
version: 1.0.0
author: Claude Office Skills Contributors
license: MIT
tags: [finance, expenses, accounting]
---

# 费用报告

## 概述

本功能可帮助您将业务支出整理成清晰、分类明确的报告，便于提交报销申请、进行会计处理和税务申报。

**使用场景：**
- 创建费用报销报告
- 整理用于税务申报的收据
- 对业务支出进行分类
- 汇总差旅费用
- 编制月度/季度费用汇总表

## 使用方法

1. 提供您的费用信息（收据、交易记录或费用描述）
2. 指定费用用途（报销、税务申报、预算监控）
3. 告诉我您的费用分类或公司政策
4. 我将为您生成结构化的费用报告

**示例提示：**
- “根据这些收据为我出差的费用生成一份费用报告”
- “对当月的费用进行分类并汇总”
- “将这些费用整理好以备报销”
- “帮我整理自由职业相关的费用以用于税务申报”

## 费用报告模板

### 标准报销报告

```markdown
# Expense Report

**Employee:** [Name]
**Department:** [Department]
**Report Period:** [Start Date] - [End Date]
**Purpose:** [Business trip / Project / General]
**Submission Date:** [Date]

## Summary
| Category | Amount |
|----------|--------|
| Transportation | $XXX.XX |
| Lodging | $XXX.XX |
| Meals | $XXX.XX |
| Other | $XXX.XX |
| **Total** | **$XXX.XX** |

## Expense Details

### Transportation
| Date | Description | Vendor | Amount | Receipt |
|------|-------------|--------|--------|---------|
| [Date] | [Description] | [Vendor] | $XX.XX | ✓ |

### Lodging
| Date | Description | Vendor | Amount | Receipt |
|------|-------------|--------|--------|---------|
| [Date] | [Hotel name] | [Vendor] | $XX.XX | ✓ |

### Meals & Entertainment
| Date | Description | Attendees | Business Purpose | Amount | Receipt |
|------|-------------|-----------|------------------|--------|---------|
| [Date] | [Restaurant] | [Names] | [Purpose] | $XX.XX | ✓ |

### Other Expenses
| Date | Description | Category | Amount | Receipt |
|------|-------------|----------|--------|---------|
| [Date] | [Description] | [Category] | $XX.XX | ✓ |

## Approvals
- [ ] Employee Signature: _____________ Date: _______
- [ ] Manager Approval: _____________ Date: _______
- [ ] Finance Approval: _____________ Date: _______

## Notes
[Any additional context or explanations]
```

### 差旅费用报告

```markdown
# Travel Expense Report

**Traveler:** [Name]
**Trip Dates:** [Start] - [End]
**Destination:** [City, Country]
**Business Purpose:** [Reason for travel]

## Trip Summary
- **Duration:** [X] days
- **Total Expenses:** $X,XXX.XX
- **Per Diem Allowance:** $XXX.XX
- **Variance:** +/- $XX.XX

## Pre-Trip Expenses
| Item | Vendor | Amount | Date Paid |
|------|--------|--------|-----------|
| Flight | [Airline] | $XXX.XX | [Date] |
| Hotel Booking | [Hotel] | $XXX.XX | [Date] |
| Conference Registration | [Event] | $XXX.XX | [Date] |

## Daily Expenses

### Day 1 - [Date]
| Category | Description | Amount |
|----------|-------------|--------|
| Transport | Airport taxi | $XX.XX |
| Meals | Dinner | $XX.XX |
| **Day Total** | | **$XX.XX** |

### Day 2 - [Date]
| Category | Description | Amount |
|----------|-------------|--------|
| Meals | Breakfast/Lunch/Dinner | $XX.XX |
| Transport | Uber to meeting | $XX.XX |
| **Day Total** | | **$XX.XX** |

## Expense by Category
| Category | Amount | % of Total |
|----------|--------|------------|
| Airfare | $XXX.XX | XX% |
| Lodging | $XXX.XX | XX% |
| Ground Transport | $XXX.XX | XX% |
| Meals | $XXX.XX | XX% |
| Other | $XXX.XX | XX% |
| **Total** | **$X,XXX.XX** | 100% |

## Receipt Checklist
- [ ] Flight confirmation/receipt
- [ ] Hotel invoice
- [ ] Ground transportation receipts
- [ ] Meal receipts over $[threshold]
- [ ] Other expense receipts
```

### 月度费用汇总

```markdown
# Monthly Expense Summary

**Period:** [Month Year]
**Prepared by:** [Name]
**Business:** [Business Name]

## Overview
| Metric | Amount |
|--------|--------|
| Total Expenses | $X,XXX.XX |
| vs Last Month | +/-XX% |
| vs Budget | +/-XX% |

## Expenses by Category

### Operating Expenses
| Category | Amount | Budget | Variance |
|----------|--------|--------|----------|
| Rent/Utilities | $XXX.XX | $XXX.XX | $XX.XX |
| Software/Subscriptions | $XXX.XX | $XXX.XX | $XX.XX |
| Office Supplies | $XXX.XX | $XXX.XX | $XX.XX |

### Professional Services
| Category | Amount | Budget | Variance |
|----------|--------|--------|----------|
| Legal | $XXX.XX | $XXX.XX | $XX.XX |
| Accounting | $XXX.XX | $XXX.XX | $XX.XX |
| Consulting | $XXX.XX | $XXX.XX | $XX.XX |

### Marketing & Sales
| Category | Amount | Budget | Variance |
|----------|--------|--------|----------|
| Advertising | $XXX.XX | $XXX.XX | $XX.XX |
| Events | $XXX.XX | $XXX.XX | $XX.XX |
| Travel | $XXX.XX | $XXX.XX | $XX.XX |

## Top 10 Expenses
| Rank | Date | Description | Category | Amount |
|------|------|-------------|----------|--------|
| 1 | [Date] | [Description] | [Category] | $XXX.XX |
| 2 | [Date] | [Description] | [Category] | $XXX.XX |

## Notes & Anomalies
- [Explanation for any unusual expenses]
- [Budget variance explanations]
```

## 费用分类

### 常见业务费用分类

| 分类 | 示例 | 是否可抵扣税款 |
|----------|----------|----------------|
| **差旅** | 飞票、酒店、租车 | 通常可抵扣 |
| **餐饮与娱乐** | 客户聚餐、团队午餐 | 50-100% 可抵扣 |
| **交通** | 出租车、优步、停车费、里程费 | 可抵扣 |
| **办公用品** | 纸张、笔、打印机墨水 | 可抵扣 |
| **软件与订阅服务** | SaaS 工具、应用程序 | 可抵扣 |
| **专业发展** | 课程、书籍、会议 | 通常可抵扣 |
| **通讯** | 电话费用、网络费用 | 部分可抵扣 |
| **专业服务** | 法律服务、会计服务 | 可抵扣 |
| **市场营销** | 广告费用、宣传材料 | 可抵扣 |
| **设备** | 电脑、办公家具 | 可抵扣（需按折旧年限计算） |

### 美国国税局（IRS）费用分类标准

| IRS 分类 | 说明 |
|--------------|-------------|
| 广告 | 市场营销和宣传费用 |
| 车辆费用 | 车辆相关支出 |
| 佣金 | 给承包商的付款 |
| 合同工费用 | 自由职业者的报酬 |
| 折旧 | 资产折旧费用 |
| 保险 | 商业保险费用 |
| 利息 | 商业贷款利息 |
| 法律与专业服务 | 律师费、注册会计师费用 |
| 办公费用 | 一般办公开支 |
| 租金 | 办公场所租金 |
| 维修费用 | 设备维护费用 |
| 用品费用 | 商业用品费用 |
| 税费与许可证 | 商业税费 |
| 差旅费用 | 差旅相关费用 |
| 餐饮费用 | 差旅期间的餐饮费用（50% 可抵扣） |
| 公用事业费 | 商业用水/电费 |

## 处理指南

### 收据要求
- 保留所有超过 $25（美国）或当地规定金额的收据
- 必需的信息：日期、供应商、金额、支付方式
- 餐饮费用：需注明参与人员及费用用途
- 如果缺少收据，请在报告中说明原因

### 货币转换
- 使用费用发生当日的汇率进行转换
- 记录汇率来源（银行、XE.com 等）
- 保留原始货币金额及转换后的金额

### 里程费计算
- 当前 IRS 里程费标准：$0.67/英里（请核实最新标准）
- 记录相关信息：日期、目的地、用途、行驶里程
- 可使用里程表读数或地图应用记录里程

## 输出格式

```markdown
# Expense Report

**Period:** [Dates]
**Total:** $X,XXX.XX

## Summary by Category
[Category breakdown table]

## Detailed Expenses
[Line items with all required info]

## Missing/Notes
[Any issues to address]
```

## 限制事项
- 无法直接扫描或识别收据图片
- 税务相关建议请咨询专业人士
- 请核实汇率的准确性
- 公司政策可能有特殊要求
- 无法将报告直接提交至您的费用管理系统

## 示例

### 快速费用整理示例

**输入：**
```
uber to airport $45
flight to NYC $380
hotel 2 nights $420
dinner with client john from acme $125
coffee and breakfast $35
uber to meetings $28
lunch meeting $65
return flight $395
uber home $42
```

**输出：**

# 差旅费用报告

**出差地点：** 纽约市，客户拜访
**日期：** [根据实际情况填写日期]
**用途：** 与 Acme 公司的商务会议

## 费用汇总
| 分类 | 金额 |
|----------|--------|
| 飞行费 | $775.00 |
| 住宿费 | $420.00 |
| 地面交通费 | $115.00 |
| 餐饮与娱乐费 | $225.00 |
| **总计：** $1,535.00 |

## 详细费用明细

### 飞行费
| 日期 | 详情 | 金额 | 收据 |
|------|-------------|--------|---------|
| [第1天] | 纽约往返航班 | $380.00 | 必需提供 |
| [第3天] | 返回航班 | $395.00 | 必需提供 |
| **小计：** | $775.00 |

### 住宿费
| 日期 | 详情 | 金额 | 收据 |
|------|-------------|--------|---------|
| [第1-2天] | 酒店（2晚） | $420.00 | 必需提供 |

### 地面交通费
| 日期 | 详情 | 金额 | 收据 |
|------|-------------|--------|---------|
| [第1天] | 机场接送 | $45.00 | 通过优步支付 |
| [第2天] | 会议接送 | $28.00 | 通过优步支付 |
| [第3天] | 回家接送 | $42.00 | 通过优步支付 |
| **小计：** | $115.00 |

### 餐饮与娱乐费
| 日期 | 详情 | 参与人员 | 用途 | 金额 | 收据 |
|------|-------------|-----------|---------|--------|---------|
| [第1天] | 客户聚餐 | John (Acme) | 客户会议 | $125.00 | 必需提供 |
| [第2天] | 早餐/咖啡 | 个人消费 | 工作餐 | $35.00 | 可选 |
| [第2天] | 午餐会议 | [待确认] | [会议目的] | $65.00 | 必需提供 |
| **小计：** | | | $225.00 |

## 需要执行的操作：
- [ ] 收集航班确认邮件
- [ ] 获取酒店发票
- [ ] 保存超过 $25 的餐饮费用收据
- [ ] 记录客户聚餐的详细用途
- [ ] 确认午餐会议的参与人员