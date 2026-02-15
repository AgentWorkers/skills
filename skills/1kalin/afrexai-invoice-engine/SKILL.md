---
name: afrexai-invoice-engine
description: 生成、管理和追踪专业发票，支持支付条款设置、周期性计费功能、逾期提醒自动化处理以及财务报告功能。适用于创建发票、跟踪付款进度、管理客户信息或审核收入情况。
---

# 发票引擎 — 完整的发票处理与应收账款管理

这是一个完全独立的代理技能，支持从报价到付款再到报告的端到端发票处理流程。

## 快速入门

当用户请求“创建发票”或“向[客户]开账单”时：

1. 检查客户是否存在于内存中（详见下面的客户注册表）。
2. 如果是新客户，则执行客户入职流程。
3. 使用发票生成器生成发票。
4. 提交审核并最终确定。
5. 将发票记录在发票账本中。

---

## 1. 客户注册表

在工作区维护一个YAML格式的客户数据库：

```yaml
# clients.yaml
clients:
  - id: "CLI-001"
    name: "Acme Corp"
    contact: "Jane Smith"
    email: "jane@acme.com"
    address:
      line1: "123 Business Ave"
      line2: "Suite 400"
      city: "New York"
      state: "NY"
      zip: "10001"
      country: "US"
    tax_id: "US-EIN-12-3456789"
    payment_terms: "net-30"       # net-15, net-30, net-45, net-60, due-on-receipt, custom
    preferred_currency: "USD"
    default_tax_rate: 0           # 0 for B2B cross-border, local rate for domestic
    notes: "PO required for invoices > $5,000"
    created: "2026-01-15"
    lifetime_revenue: 12500.00
    invoices_sent: 3
    invoices_paid: 2
    avg_days_to_pay: 22
```

### 客户入职检查清单
在添加新客户时，需要收集以下信息：
- [ ] 法定实体名称（与客户记录一致）
- [ ] 账务联系人姓名及电子邮件
- [ ] 账务地址（包括国家）
- [ ] 税务识别号/VAT号码（如适用）
- [ ] 首选付款方式
- [ ] 优先货币
- [ ] 任何采购订单或审批要求
- [ ] 是否免税？（如是，请提供免税证明）

---

## 2. 发票生成器

### 发票编号格式
```
[PREFIX]-[YEAR].[MONTH].[SEQUENCE]
Example: INV-2026.02.001
```

可根据业务类型配置前缀：
- `INV`：标准发票
- `PRO`：报价单
- `REC`：定期发票
- `CN`：贷项通知单

### 发票模板

生成发票时，其结构如下：

```
╔══════════════════════════════════════════════════════════╗
║  [YOUR COMPANY NAME]                                     ║
║  [Address Line 1]                                        ║
║  [City, State ZIP]                                       ║
║  [Country]                                               ║
║  Tax ID: [YOUR TAX ID]                                   ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  INVOICE [NUMBER]                  Date: [ISSUE DATE]    ║
║                                    Due:  [DUE DATE]      ║
║                                                          ║
║  Bill To:                          Payment Terms:        ║
║  [CLIENT NAME]                     [Net-30 / etc.]       ║
║  [Client Address]                                        ║
║  [City, State ZIP]                 PO Number:            ║
║  Tax ID: [CLIENT TAX ID]          [If applicable]        ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  #  │ Description          │ Qty │ Rate    │ Amount     ║
╠═════╪══════════════════════╪═════╪═════════╪════════════╣
║  1  │ [Service/Product]    │  1  │ $X,XXX  │ $X,XXX.XX ║
║  2  │ [Service/Product]    │  3  │ $XXX    │ $X,XXX.XX ║
║  3  │ [Expense passthrough]│  1  │ $XXX    │ $XXX.XX   ║
╠═════╧══════════════════════╧═════╧═════════╧════════════╣
║                              Subtotal:    $XX,XXX.XX     ║
║                              Discount:    -$X,XXX.XX     ║
║                              Tax (X%):    $X,XXX.XX      ║
║                              ─────────────────────────   ║
║                              TOTAL DUE:   $XX,XXX.XX     ║
╠══════════════════════════════════════════════════════════╣
║  Payment Methods:                                        ║
║  • Bank Transfer: [Bank] | Acct: [XXXX] | Routing: [XX] ║
║  • PayPal: [email]                                       ║
║  • Stripe: [payment link]                                ║
║  • Bitcoin: [address] / Lightning: [LNURL]               ║
║                                                          ║
║  Notes: [Custom message / thank you / late fee notice]   ║
╚══════════════════════════════════════════════════════════╝
```

### 项目类型
- **按时间计费**：小时数 × 每小时费率（记录工作时间，自动计算）
- **固定费用**：项目里程碑费用、预付款
- **按数量计费**：单位数 × 单价
- **费用转嫁**：按成本或加价百分比计费
- **折扣行**：负金额（表示提前付款、批量购买或忠诚度优惠）
- **定期发票**：根据定期计划自动填充

### 税务处理规则
```
Is client in same country as you?
├── YES → Apply local tax rate
│   ├── Client tax-exempt? → Add exemption reference, 0% tax
│   └── Client NOT exempt → Apply standard rate
└── NO → Usually 0% (reverse charge / export)
    ├── Both in EU? → Reverse charge mechanism (0%, note on invoice)
    ├── US interstate? → Check nexus rules
    └── International → 0% with export reference
```

### 折扣与定价策略
- **提前付款**：10天内付款享受2%折扣
- **批量购买**：数量分级定价（1-10单位 = $X，11-50单位 = $Y，51单位以上 = $Z）
- **忠诚度优惠**：连续开具6张发票后享受5%的持续折扣
- **捆绑服务**：多项服务打包优惠10-15%
- **季节性优惠**：第四季度额外优惠10%，第一季度优惠5%（如适用）

---

## 3. 发票生命周期与状态跟踪

### 状态流转
```
DRAFT → SENT → VIEWED → PARTIALLY_PAID → PAID → CLOSED
                  ↓
              OVERDUE → ESCALATED → WRITTEN_OFF
                  ↓
            DISPUTED → RESOLVED → PAID
```

### 发票账本（YAML格式）

```yaml
# invoices.yaml
invoices:
  - number: "INV-2026.02.001"
    client_id: "CLI-001"
    status: "sent"
    issue_date: "2026-02-13"
    due_date: "2026-03-15"
    currency: "USD"
    subtotal: 5000.00
    discount: 0
    tax: 0
    total: 5000.00
    amount_paid: 0
    balance_due: 5000.00
    payment_terms: "net-30"
    line_items:
      - description: "AI Integration Consulting — February"
        qty: 20
        rate: 250.00
        amount: 5000.00
    payments: []
    notes: ""
    sent_date: "2026-02-13"
    reminders_sent: 0
    created: "2026-02-13T10:30:00Z"
```

### 付款记录
收到付款时：
```yaml
payments:
  - date: "2026-03-10"
    amount: 5000.00
    method: "bank_transfer"    # bank_transfer, stripe, paypal, btc, cash, check
    reference: "TXN-ABC123"
    notes: "Paid in full"
```

更新：`amount_paid`（已付款金额）、`balance_due`（未付余额）、`status`（余额为0则标记为已支付，余额大于0则标记为部分支付）

---

## 4. 定期发票

### 安排计划
```yaml
recurring:
  - id: "REC-001"
    client_id: "CLI-001"
    description: "Monthly Retainer — AI Ops Support"
    frequency: "monthly"          # weekly, biweekly, monthly, quarterly, annually
    day_of_month: 1               # 1-28 (avoid 29-31 for safety)
    line_items:
      - description: "AI Operations Retainer"
        qty: 1
        rate: 3500.00
    auto_send: true               # false = create as draft
    start_date: "2026-01-01"
    end_date: null                # null = indefinite
    next_invoice: "2026-03-01"
    invoices_generated: 2
    active: true
```

### 定期发票处理流程
1. 检查`recurring`记录中`next_invoice`是否小于或等于当前日期且`active`为`true`。
2. 对于符合条件的记录：
   - 从模板生成发票并分配新的发票编号。
   - 如果`auto_send`设置为`true`，则标记为已发送并通知客户。
   - 如果`auto_send`设置为`false`，则将发票保存为草稿并通知用户审核。
   - 更新`next_invoice`为下一次付款日期。
   - 每日更新内存中的记录。

---

## 5. 逾期管理及收款

### 提醒机制
| 逾期天数 | 处理方式 | 通知方式 |
|---|---|---|
| +1天 | 发送友好提醒邮件 | “温馨提醒...” |
| +7天 | 发送附有发票的跟进邮件 | “正在跟进您的订单...” |
| +14天 | 发送正式提醒并提及滞纳金 | “该发票已逾期14天...” |
| +30天 | 发送最终通知 | “最后通知——请尽快付款...” |
| +45天 | 人工介入处理（Kalin/Christina） | 标记为需要人工催收 |
| +60天 | 考虑核销或采取其他收款措施 | 由业务部门决定 |

### 提醒模板
**第1天（友好提醒）**
```
Subject: Friendly reminder — Invoice [NUMBER] due [DATE]

Hi [CONTACT],

Hope all is well! Just a quick reminder that invoice [NUMBER] for [AMOUNT] was due on [DATE].

If you've already sent payment, please disregard this note.

Payment details are on the attached invoice. Let me know if you need anything.

Best,
[YOUR NAME]
```

**第14天（正式提醒）**
```
Subject: Invoice [NUMBER] — 14 days overdue ([AMOUNT])

Hi [CONTACT],

Invoice [NUMBER] for [AMOUNT] is now 14 days past the due date of [DATE].

Per our agreement, a late fee of [X]% may apply to balances outstanding beyond [Y] days.

Could you confirm when we can expect payment? Happy to discuss if there's an issue.

Thanks,
[YOUR NAME]
```

**第30天（最终提醒）**
```
Subject: Final notice — Invoice [NUMBER] overdue ([AMOUNT])

Hi [CONTACT],

This is a final reminder that invoice [NUMBER] for [AMOUNT] remains unpaid, now 30 days past the due date.

Please arrange payment within the next 7 business days to avoid further action.

If there's a dispute or issue with this invoice, please let me know immediately so we can resolve it.

Regards,
[YOUR NAME]
```

### 滞纳金计算
```
Standard: 1.5% per month on overdue balance (18% APR)
Grace period: 5 business days after due date
Compound: Simple interest (not compound)
Cap: 25% of invoice total (or local legal maximum)

Formula: late_fee = balance_due × (monthly_rate / 30) × days_overdue
Example: $5,000 × (0.015 / 30) × 14 = $35.00
```

---

## 6. 财务报告

### 收入仪表盘（每周/每月生成）

```
═══ REVENUE SUMMARY — [MONTH YEAR] ═══

Invoiced This Month:      $XX,XXX.XX  ([N] invoices)
Collected This Month:     $XX,XXX.XX  ([N] payments)
Outstanding (not overdue): $XX,XXX.XX  ([N] invoices)
Overdue:                  $XX,XXX.XX  ([N] invoices, avg [X] days late)
Written Off (YTD):        $XX,XXX.XX

Collection Rate:          XX.X%  (collected / invoiced, trailing 90 days)
Avg Days to Pay:          XX days (trailing 90 days)
Avg Invoice Size:         $X,XXX.XX

═══ TOP CLIENTS (by revenue, YTD) ═══
1. [Client] — $XX,XXX  ([N] invoices, avg [X] days to pay)
2. [Client] — $XX,XXX  ([N] invoices, avg [X] days to pay)
3. [Client] — $XX,XXX  ([N] invoices, avg [X] days to pay)

═══ AGING REPORT ═══
Current (not yet due):     $XX,XXX  ([N] invoices)
1-15 days overdue:         $XX,XXX  ([N] invoices)
16-30 days overdue:        $XX,XXX  ([N] invoices)
31-60 days overdue:        $XX,XXX  ([N] invoices)
60+ days overdue:          $XX,XXX  ([N] invoices) ⚠️

═══ MONTHLY TREND ═══
Jan: $XX,XXX ████████████
Feb: $XX,XXX ████████████████
Mar: $XX,XXX ██████████
...

═══ ACTIONS NEEDED ═══
• [N] invoices need reminder emails
• [N] recurring invoices due for generation
• [Client] has disputed INV-XXXX — needs resolution
```

### 需要跟踪的关键指标
- **收款率**：实际收款金额占发票金额的百分比（目标：>95%）
- **DSO（应收账款周转天数）**：从发票生成到付款的平均天数（目标：<30天）
- **逾期比例**：逾期余额占总未付金额的比例（目标：<10%）
- **收入集中度**：来自最大客户的收入占比（占比超过40%则标记为风险）
- **定期发票收入**：定期发票的总收入

---

## 7. 贷项通知单与调整

当需要退款或调整时：

```yaml
credit_note:
  number: "CN-2026.02.001"
  original_invoice: "INV-2026.01.003"
  client_id: "CLI-001"
  reason: "Partial refund — service hours overcharged"
  line_items:
    - description: "Correction: 5 hours overcharged"
      qty: -5
      rate: 250.00
      amount: -1250.00
  total: -1250.00
  issued: "2026-02-13"
```

应用贷项通知单来：
- 减少原发票的余额。
- 用于未来的发票（作为账户抵扣）。
- 直接退款（记录退款方式和参考信息）。

---

## 8. 多货币支持

```yaml
currencies:
  primary: "USD"
  accepted: ["USD", "GBP", "EUR", "BTC"]
  exchange_rates:  # Update weekly or use live rates
    GBP_USD: 1.27
    EUR_USD: 1.08
    BTC_USD: 97500
  conversion_note: "Converted at rate on invoice date. Payment accepted in invoiced currency only."
```

规则：
- 始终使用客户首选的货币开具发票。
- 以实际收到的货币记录付款。
- 将付款金额转换为报告使用的主货币（使用付款当天的汇率）。
- 如果涉及跨货币交易，请在发票上注明汇率。
- 对于BTC/Lightning等数字货币，同时显示sat和法币等值金额。

---

## 9. 从报价到发票的流程

### 报价单模板
与发票模板相同，但：
- 前缀为`PRO-`而非`INV-`
- 标题为“QUOTATION”而非“INVOICE”
- 添加“有效期至：[日期]”（通常为30天）
- 添加“此发票不用于税务申报”

### 流程
```
QUOTE → ACCEPTED → INVOICE → PAID
  ↓
EXPIRED (auto-expire after validity period)
  ↓
REVISED (new version with changes)
```

报价单被接受后：
1. 将其转换为发票（更改前缀，删除有效期说明）。
2. 根据客户信息设置付款条款。
3. 发送发票。
4. 将报价单归档为“已转换”状态。

---

## 10. 特殊情况与规则

### 部分付款
- 每次付款都单独记录，并附上参考编号。
- 每次付款后更新未付余额。
- 最后一次付款后，将状态标记为“已支付”。
- 如果部分付款且存在逾期，仅追讨剩余未付金额。

### 有争议的发票
- 将状态标记为“DISPUTED”（有争议）。
- 记录争议原因和日期。
- 在争议期间暂停提醒。
- 跟进争议解决情况（调整、发放贷项通知单或确认无误）。
- 解决争议后恢复计费。

### 发票作废与贷项通知单
- **发票作废**：发票发送错误，实际上不应存在 → 标记为VOIDED，并从报告中排除。
- **贷项通知单**：服务已提供但需要调整 → 发放贷项通知单，并计入报告。

### 各地区的税务发票要求
- **美国**：没有严格格式要求，但需提供EIN（企业识别号）。
- **英国/欧盟**：必须包含VAT号码和VAT金额；如适用，需注明“反向收费”。
- **澳大利亚**：必须标注“Tax Invoice”并包含ABN（澳大利亚商业编号）和GST金额。
- **加拿大**：必须包含GST/HST号码，并遵守特定省份的规则。

### 四舍五入
- 所有项目金额四舍五入到小数点后两位。
- 对小计金额征税（而不是每项单独征税），以避免金额差异。
- 在金额前显示货币符号：$1,234.56

### 发票编号规则
- 绝不要重复使用或跳过编号（符合税务审计要求）。
- 在同一前缀下按顺序编号。
- 如果发票被作废，保留编号，仅更改状态。

---

## 11. 自动化机会

设置定时任务或心跳检查，用于：
- [ ] 按计划生成定期发票。
- [ ] 按上述计划发送逾期提醒。
- [ ] 每周向负责人发送收入仪表盘。
- [ ] 每月生成账龄报告。
- [ ] 自动标记逾期超过45天的客户。
- [ ] 每季度更新汇率和价格信息。

---

## 12. 导出格式

当用户需要导出数据时：
- **CSV**：适用于电子表格或会计导入。
  ```
  invoice_number,client,date,due_date,total,status,amount_paid,balance
  ```
- **JSON**：用于API集成或备份。
- **Markdown表格**：便于在聊天中快速查看。
- **PDF格式文本**：格式化后的文本，可直接用于PDF生成。

---

## 命令参考

| 命令 | 功能 |
|---|---|
| "Invoice [客户] for [金额/描述]" | 创建新发票 |
| "Quote [客户] for [服务]" | 创建报价单 |
| "Show outstanding invoices" | 列出未付发票 |
| "What's overdue?" | 显示逾期发票列表 |
| "Revenue this month" | 显示本月收入 |
| "Send reminder for [发票]" | 生成付款提醒邮件 |
| "Record payment [发票] [金额]" | 记录付款信息 |
| "Recurring: [客户] [金额] [频率]" | 设置定期发票 |
| "Credit note for [发票]" | 发放贷项通知单/进行调整 |
| "Client report [名称]" | 显示客户的完整付款历史 |
| "Export invoices [格式]" | 以CSV/JSON/Markdown格式导出发票 |
| "Void [发票]" | 作废发票 |
| "Update rates" | 更新汇率 |