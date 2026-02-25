---
name: invoice-tracker
description: 完整的自由职业者计费工作流程：生成专业发票、跟踪付款状态、发送自动提醒以及核对付款信息。适用于需要向客户收费、跟进逾期付款、整理财务记录或为自由职业收入准备税务文件的情况。
---
# 发票跟踪工具

确保您能够及时收回应得的款项。该工具涵盖了从发票生成到付款对账的整个 billing 生命周期，提供专业的模板、自动提醒以及财务报告功能。

## 功能概述

- **发票生成**：根据项目数据生成专业发票。
- **付款跟踪**：明确谁欠了多少钱以及何时应该付款。
- **自动提醒**：对逾期付款发送礼貌的催款通知。
- **付款对账**：将实际收到的付款与发票信息进行核对。
- **财务报告**：生成收入统计、账款逾期情况以及税务摘要。
- **定期账单**：处理预付款和订阅服务的账单。
- **滞纳金管理**：计算并收取滞纳金。

## 快速入门

### 1. 创建第一张发票
```
"Create an invoice for:

Client: [Company Name]
Client Email: [email]
Project: [Project Name]
Invoice #: INV-2024-001
Issue Date: [date]
Due Date: Net 15

Line Items:
1. Website Design - $5,000
2. Development - $3,500
3. CMS Training - $500

Payment terms: Net 15, 1.5% late fee after 30 days
Payment methods: Bank transfer, PayPal, credit card"
```

### 2. 批量生成发票
```
"Generate monthly invoices for my retainer clients:

Client A: $2,000/month - Website maintenance
Client B: $1,500/month - Ongoing consulting
Client C: $3,000/month - Marketing support

Period: January 2024
Terms: Net 30
Include: Hours summary, deliverables completed"
```

### 3. 催收逾期付款
```
"Create follow-up emails for overdue invoices:

Invoice INV-2024-005 - $4,500 - 15 days overdue
Invoice INV-2024-008 - $2,200 - 30 days overdue
Invoice INV-2024-012 - $6,000 - 45 days overdue

Tone: Professional but firm
Include: Payment link, original invoice, late fee notice"
```

## 发票结构

### 必需元素

**页眉**：
- 公司名称/标志
- 发票编号（唯一且连续）
- 发票日期
- 截止付款日期

**收款方信息**：
- 发票开具方：公司名称、地址、税务识别号
- 收款方：客户名称、联系人、 billing 地址

**明细项目**：
| 服务内容 | 数量 | 单价 | 合计金额 |
|-------------|----------|------|--------|
| 服务名称 | 10小时 | $100/小时 | $1,000 |
| 交付成果 | 1个 | $2,500 | $2,500 |

**总计**：
- 小计
- 税费（如适用）
- 折扣
- **应付款总额**

**页脚**：
- 付款说明
- 条款和条件
- 感谢语

### 专业发票模板
```
┌─────────────────────────────────────────────────────────┐
│  [YOUR LOGO]                              INVOICE       │
│  Your Business Name                         #INV-2024-001│
│  123 Main Street                           Date: Jan 15 │
│  City, ST 12345                            Due: Feb 1   │
│  contact@yourbusiness.com                             │
├─────────────────────────────────────────────────────────┤
│  BILL TO:                                               │
│  Client Company Name                                    │
│  Attn: Accounts Payable                                 │
│  456 Business Ave                                       │
│  City, ST 67890                                         │
├─────────────────────────────────────────────────────────┤
│  PROJECT: Website Redesign                              │
├─────────────────────────────────────────────────────────┤
│  Description           │ Qty │ Rate      │ Amount      │
│  ──────────────────────┼─────┼───────────┼─────────────│
│  Discovery & Strategy  │ 1   │ $1,500.00 │ $1,500.00   │
│  UI/UX Design          │ 1   │ $3,000.00 │ $3,000.00   │
│  Frontend Development  │ 40  │ $100.00   │ $4,000.00   │
│  CMS Integration       │ 1   │ $1,500.00 │ $1,500.00   │
│  ──────────────────────┴─────┴───────────┼─────────────│
│                               Subtotal   │ $10,000.00  │
│                               Tax (0%)   │ $0.00       │
│                               ─────────────────────────│
│                               TOTAL DUE  │ $10,000.00  │
├─────────────────────────────────────────────────────────┤
│  PAYMENT OPTIONS:                                       │
│  • Bank Transfer: [Account details]                     │
│  • PayPal: [PayPal.me link]                             │
│  • Credit Card: [Stripe/PayPal link]                    │
│                                                         │
│  TERMS: Net 30. Late payments subject to 1.5% monthly   │
│  service charge after 30 days.                          │
│                                                         │
│  Questions? Contact: billing@yourbusiness.com           │
│  Thank you for your business!                           │
└─────────────────────────────────────────────────────────┘
```

## 付款跟踪系统

### 发票状态分类
```
DRAFT        → Created but not sent
SENT         → Issued to client, awaiting payment
VIEWED       → Client opened invoice (if using online system)
PARTIAL      → Partial payment received
PAID         → Full payment received
OVERDUE      → Past due date, payment pending
COLLECTIONS  → Seriously overdue, escalation needed
VOID         → Cancelled/replaced
```

### 账款逾期报告
按逾期时间对发票进行分类：
```
Aging Report - February 2024

Client              Invoice     Amount    0-30    31-60   60+
─────────────────────────────────────────────────────────────
ABC Corp            INV-005     $4,500            $4,500
XYZ Inc             INV-008     $2,200    $2,200
123 LLC             INV-012     $6,000                    $6,000
─────────────────────────────────────────────────────────────
TOTALS                          $12,700   $2,200  $4,500  $6,000
```

## 自动提醒流程

### 标准催款计划

- **第0天**：发送发票
- **第7天**：友好提醒（适用于Net 30付款方式）
- **第25天**：付款即将到期
- **第31天**：第一次逾期通知
- **第45天**：第二次逾期通知
- **第60天**：最终通知及滞纳金提示
- **第75天**：启动追讨流程

### 电子邮件模板

- **付款到期前提醒（第25天）**：
```
Subject: Payment Reminder: Invoice INV-2024-001 ($10,000)

Hi [Name],

Just a friendly reminder that invoice INV-2024-001 for $10,000 
is due on [due date] (5 days from now).

You can view and pay the invoice here: [link]

Payment options:
• Bank transfer (preferred)
• PayPal: [link]
• Credit card: [link]

Please let me know if you have any questions or need any 
additional information.

Thanks!
[Your name]
```

- **第一次逾期通知（第31天）**：
```
Subject: Overdue Invoice: INV-2024-001 ($10,000) - Action Needed

Hi [Name],

I wanted to follow up on invoice INV-2024-001 for $10,000, 
which was due on [due date] and is now overdue.

If you've already sent payment, please disregard this message 
and accept my thanks.

If not, you can pay online here: [link]

I'm happy to discuss any questions or concerns you may have. 
Please reply to this email or call me at [phone].

Best regards,
[Your name]
```

- **第二次逾期通知（第45天）**：
```
Subject: Second Notice: Overdue Invoice INV-2024-001 ($10,000)

Hi [Name],

This is my second notice regarding invoice INV-2024-001 for 
$10,000, originally due on [due date].

Per our agreement, a late fee of $150 (1.5%) will be applied 
to this invoice if payment is not received by [date + 15 days].

I value our working relationship and want to resolve this 
amicably. Please contact me to discuss payment arrangements 
if needed.

Payment link: [link]

Regards,
[Your name]
```

- **最终通知（第60天）**：
```
Subject: FINAL NOTICE: Overdue Invoice INV-2024-001 ($10,150)

Hi [Name],

This is a final notice regarding invoice INV-2024-001.

Original amount: $10,000
Late fees applied: $150
Current balance: $10,150

If payment is not received within 15 days, I will need to 
escalate this matter to collections and suspend any ongoing 
work.

I would prefer to avoid this. Please contact me immediately 
to discuss payment: [phone/email]

Payment link: [link]

[Your name]
```

## 财务报告

### 月度收入报告
```
Revenue Report - January 2024

Invoiced:           $25,000
  - Services:       $20,000
  - Products:       $5,000

Collected:          $22,500
Outstanding:        $12,500
  - Current:        $5,000
  - Overdue:        $7,500

Top Clients:
1. ABC Corp:        $8,000
2. XYZ Inc:         $6,500
3. 123 LLC:         $4,500

Payment Methods:
- Bank transfer:    60%
- PayPal:           30%
- Credit card:      10%
```

### 税务摘要
```
Annual Tax Summary - 2024

Total Revenue:      $180,000
  - Q1:             $45,000
  - Q2:             $42,000
  - Q3:             $48,000
  - Q4:             $45,000

Taxable Income:     $165,000
  (after $15,000 expenses)

Estimated Tax:      ~$41,250 (25% effective rate)
Quarterly payments: $10,312

1099s Received:     3 clients ($95,000 total)
1099s Required:     2 contractors ($12,000 paid)
```

## 定期账单

### 预付款设置
```
"Create a monthly retainer invoice template:

Client: [Name]
Service: Ongoing consulting
Amount: $3,000/month
Billing date: 1st of month
Payment terms: Net 15

Include:
- Hours included: 20
- Overage rate: $150/hr
- Rollover policy: Up to 5 hours
- Minimum commitment: 3 months"
```

### 订阅服务账单生成
对于产品化服务：
```
Tier: Starter ($99/month)
- Invoice auto-generated on subscription date
- Payment auto-charged (if using Stripe/PayPal)
- Failed payment → retry sequence
- Cancellation → final invoice prorated
```

## 最佳实践

### 发票编号规则

使用统一的编号格式：
- `INV-YYYY-NNN`（例如：INV-2024-001）
- `YYYY-MM-NNN`（例如：2024-01-001）
- `CLIENT-NNN`（例如：ABC-001）

### 付款条款

常见选项：
- **Net 15**：适用于大型企业（这些客户通常付款周期较长）
- **Net 30**：大多数客户的默认选项
- **收到款项后付款**：适用于小型项目或新客户
- **50/50**：50%预付款，50%项目完成后付款
- **分阶段付款**：根据项目进度分阶段付款

### 现金流管理建议

1. **立即开具发票**——不要等到月底。
2. **要求预付款**——新客户需支付50%的预付款。
3. **提供提前付款折扣**——例如Net 30付款方式下，提前10天付款可享受2%的折扣。
4. **收取滞纳金**——并严格执行。
5. **对逾期账户停止服务**——保护自己的权益。
6. **使用在线支付方式**——方便客户付款，加快收款速度。

### 需警惕的警示信号

- 客户在达成协议后质疑费用标准。
- 客户反复表示“支票已经在寄出中”。
- 项目完成后才要求付款（且未支付预付款）。
- 客户在发票到期后消失不见。
- 客户希望在项目进行中更改付款条款。

## 工具集成

**会计软件**：
- QuickBooks、Xero、FreshBooks——实现发票数据同步。
- 自动化对账功能。
- 提供税务报告支持。

**支付处理器**：
- Stripe——支持信用卡和ACH转账。
- PayPal——广泛接受的支付方式。
- Wise——支持国际转账。
- 银行转账——费用最低。

**时间管理工具**：
- Harvest、Toggl、Clockify——根据工作时间自动生成发票。

## 常见错误

1. **未能及时开具发票**——导致付款延迟数周。
2. **付款条款不明确**——引发误解和延误。
3. **不收取滞纳金**——客户没有按时付款的动力。
4. **忽视逾期发票**——逾期时间越长，收回款项越困难。
5. **新客户不要求预付款**——增加收款风险。
6. **个人账户与业务账户混用**——可能导致税务问题。
7. **未正确处理1099表格**——可能引发IRS（美国国税局）的处罚。

## 集成建议

- 与**提案生成工具**集成，将接受的提案自动转换为发票。
- 与**客户接待机器人**集成，提前设定付款条款。
- 结合**内容回报分析工具**，监控项目盈利能力。

## 收益化建议

该工具是**Freelancer Revenue Engine**的一部分。为获得最佳效果，请同时使用以下工具：
- **提案生成工具**：将提案转换为发票。
- **客户接待机器人**：提前设定付款条款。

**套餐价格**：Freelancer Revenue Engine（89美元）。