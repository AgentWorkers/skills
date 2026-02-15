---
name: Invoice Organizer
description: 组织、分类并跟踪发票和收据
author: claude-office-skills
version: "1.0"
tags: [finance, invoices, receipts, organization, accounting, expense]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, file_operations]
---

# 发票管理工具

用于整理、分类和追踪发票及收据，以提升财务管理效率。

## 概述

该工具可帮助您：
- 从发票中提取关键数据
- 自动分类各项支出
- 跟踪付款状态
- 保持文件的一致性
- 为税务/审计工作做好准备

## 使用方法

### 处理发票
```
"Extract data from this invoice"
"Categorize this receipt"
"Add this invoice to my tracking"
```

### 整理文件
```
"Organize my invoice folder"
"Create a filing system for receipts"
"Sort invoices by vendor and date"
```

### 生成报告
```
"Summarize invoices by category"
"Show unpaid invoices"
"Generate expense report for Q1"
```

## 数据提取

### 发票数据字段
```markdown
## Invoice Data Extraction

### Extracted Information
| Field | Value | Confidence |
|-------|-------|------------|
| **Vendor** | Acme Corp | 98% |
| **Invoice #** | INV-2026-0042 | 99% |
| **Invoice Date** | 2026-01-15 | 99% |
| **Due Date** | 2026-02-14 | 99% |
| **Subtotal** | $1,250.00 | 98% |
| **Tax** | $100.00 | 98% |
| **Total** | $1,350.00 | 99% |
| **Currency** | USD | 99% |

### Line Items
| Description | Qty | Unit Price | Total |
|-------------|-----|------------|-------|
| Consulting Services | 10 hrs | $100.00 | $1,000.00 |
| Software License | 1 | $250.00 | $250.00 |

### Vendor Details
- **Company**: Acme Corp
- **Address**: 123 Business St, NY 10001
- **Tax ID**: 12-3456789
- **Contact**: billing@acme.com

### Payment Information
- **Terms**: Net 30
- **Method**: Bank Transfer
- **Account**: XXXX-1234
```

## 分类系统

### 支出类别
```markdown
## Expense Category System

### Standard Categories
| Category | Subcategory | Examples |
|----------|-------------|----------|
| **Office** | Supplies | Paper, pens, toner |
| | Equipment | Computers, furniture |
| | Services | Cleaning, maintenance |
| **Travel** | Transportation | Flights, trains, taxis |
| | Accommodation | Hotels, Airbnb |
| | Meals | Client dinners, per diem |
| **Software** | Subscriptions | SaaS, cloud services |
| | Licenses | One-time purchases |
| **Professional** | Legal | Attorney fees |
| | Accounting | CPA, bookkeeping |
| | Consulting | Advisors, contractors |
| **Marketing** | Advertising | Ads, sponsorships |
| | Events | Conferences, booths |
| | Content | Design, copywriting |
| **Utilities** | Phone/Internet | Telecom services |
| | Cloud/Hosting | AWS, servers |

### Auto-Categorization Rules
| Vendor Contains | → Category |
|-----------------|------------|
| Amazon Web Services | Software > Cloud |
| Office Depot | Office > Supplies |
| United Airlines | Travel > Transportation |
| Marriott, Hilton | Travel > Accommodation |
| Adobe, Microsoft | Software > Subscriptions |
```

## 文件归档系统

### 文件夹结构
```markdown
## Invoice Filing System

### By Year and Category
```
📁 发票/
├── 📁 2026/
│   ├── 📁 办公费用/
│   │   └── 2026-01-15_办公用品_125.50_INV001.pdf
│   ├── 📁 软件费用/
│   │   └── 2026-01-20_Adobe软件_54.99_INV002.pdf
│   ├── 差旅费用/
│   │   └── 2026-01-22_差旅费用_450.00_INV003.pdf
│   ├── 专业服务/
│   └── 其他费用/
├── 📁 2025/
│   └── ...
└── 📁 归档/
```

### Naming Convention
```
YYYY-MM-DD_供应商名称_发票编号.pdf
```

**Examples**:
- 2026-01-15_AcmeCorp_1350.00_INV-2026-0042.pdf
- 2026-01-20_Adobe_54.99_Monthly.pdf
- 2026-01-22_DeltaAirlines_425.00_CONF123456.pdf
```

## 跟踪系统

### 发票登记
```markdown
## Invoice Tracking Register

### Open Invoices
| Invoice # | Vendor | Date | Due | Amount | Status | Days |
|-----------|--------|------|-----|--------|--------|------|
| INV-042 | Acme | 01/15 | 02/14 | $1,350 | ⏳ Pending | 14 |
| INV-045 | Beta | 01/18 | 02/17 | $890 | ⏳ Pending | 11 |
| INV-048 | Gamma | 01/22 | 01/29 | $500 | 🔴 Overdue | -1 |

### Recently Paid
| Invoice # | Vendor | Paid Date | Amount | Method |
|-----------|--------|-----------|--------|--------|
| INV-038 | Delta | 01/25 | $720 | ACH |
| INV-035 | Epsilon | 01/22 | $1,200 | Check |

### Summary
| Status | Count | Total |
|--------|-------|-------|
| Pending | 2 | $2,240 |
| Overdue | 1 | $500 |
| Paid (Jan) | 2 | $1,920 |
```

### 付款状态追踪
```markdown
## Invoice Payment Tracker

### Invoice: INV-2026-0042 (Acme Corp)

| Date | Event | Notes |
|------|-------|-------|
| 01/15 | Received | Via email |
| 01/16 | Reviewed | Approved by Manager |
| 01/20 | Scheduled | Payment batch 01/25 |
| 01/25 | Paid | ACH Ref: 789456 |
| 01/25 | Filed | /2026/Professional/ |

### Payment Details
- **Method**: ACH Transfer
- **Reference**: 789456
- **Bank**: Chase Business
- **Confirmation**: Sent to vendor
```

## 报告功能

### 月度汇总
```markdown
## Invoice Summary: January 2026

### Overview
| Metric | Value |
|--------|-------|
| Total Invoices | 28 |
| Total Amount | $12,450.00 |
| Avg per Invoice | $444.64 |
| Paid | 22 ($9,800) |
| Pending | 4 ($2,150) |
| Overdue | 2 ($500) |

### By Category
| Category | Count | Amount | % of Total |
|----------|-------|--------|------------|
| Software | 8 | $4,200 | 33.7% |
| Professional | 5 | $3,500 | 28.1% |
| Office | 6 | $2,100 | 16.9% |
| Travel | 4 | $1,650 | 13.3% |
| Utilities | 3 | $600 | 4.8% |
| Other | 2 | $400 | 3.2% |

### By Vendor
| Vendor | Invoices | Total |
|--------|----------|-------|
| Adobe | 2 | $1,200 |
| AWS | 1 | $2,800 |
| Acme Corp | 3 | $3,200 |
| ... | ... | ... |

### Trends
- Software expenses up 15% from December
- Travel expenses down 20% (seasonal)
- New vendor added: Gamma Inc.
```

### 税务准备
```markdown
## Tax-Ready Invoice Report: 2025

### Annual Summary
| Category | Total | Tax Deductible |
|----------|-------|----------------|
| Office Supplies | $4,500 | ✅ Yes |
| Software | $18,000 | ✅ Yes |
| Travel - Business | $8,200 | ✅ Yes |
| Travel - Meals (50%) | $1,200 | ⚠️ Partial |
| Professional Services | $12,000 | ✅ Yes |
| **Total Deductible** | **$43,900** | |

### Required Documentation
| Expense Over $75 | Count | Status |
|------------------|-------|--------|
| With receipt | 45 | ✅ |
| Missing receipt | 3 | ⚠️ |

### Missing Receipts
| Date | Vendor | Amount | Action |
|------|--------|--------|--------|
| 03/15 | Hotel ABC | $189 | Request from vendor |
| 07/22 | Uber | $85 | Download from app |
| 11/08 | Restaurant | $95 | Use bank statement |

### Vendor 1099 Review
| Vendor | Total Paid | 1099 Required |
|--------|------------|---------------|
| Consultant A | $8,500 | ✅ Yes (>$600) |
| Consultant B | $450 | ❌ No |
```

## 自动化规则

### 自动处理流程
```markdown
## Invoice Automation Rules

### Email Processing
| Trigger | Action |
|---------|--------|
| From: *@vendor1.com | Auto-categorize: Software |
| Subject: "Invoice" | Add to review queue |
| Attachment: PDF | Extract data |

### Auto-Categorization
| Condition | Category | Confidence |
|-----------|----------|------------|
| Vendor = Adobe | Software > Subscriptions | High |
| Contains "flight" | Travel > Transportation | High |
| Amount < $50 | Office > Supplies | Medium |

### Alerts
| Condition | Alert |
|-----------|-------|
| Due in 3 days | Email reminder |
| Overdue | Daily notification |
| Large invoice (>$1000) | Manager approval required |
```

## 限制事项

- 该工具无法直接执行文件操作
- OCR（光学字符识别）的质量会影响数据提取的准确性
- 部分分类可能需要手动调整
- 无法直接与会计软件集成
- 汇率数据需要外部验证
- 税务相关建议应咨询专业人士