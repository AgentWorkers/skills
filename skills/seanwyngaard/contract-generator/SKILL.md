---
name: contract-generator
description: 为客户项目生成专业的自由职业合同、工作范围说明书（SOW）和保密协议（NDAs）。这些文件可用于创建合同、工作范围文档或自由职业服务的法律协议。
argument-hint: "[contract-type] [project-description]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
disable-model-invocation: true
---

# 自由职业合同生成器

本工具可生成适用于自由职业项目的专业合同、工作说明书（SOW）和保密协议（NDA），涵盖项目范围、付款方式、知识产权保护、修改流程及合同终止等相关条款，旨在保护双方的权益。

**免责声明**：这些合同模板仅适用于常见的自由职业合作场景，不构成法律建议。用户在使用前应请具有执业资格的律师根据所在地区的法律法规对合同内容进行审核。

## 使用方法

```
/contract-generator service "Website redesign for Acme Corp, $5,000 fixed, 6 weeks, 2 revision rounds"
/contract-generator sow "Mobile app development, Phase 1: MVP, React Native, $15,000"
/contract-generator nda "Mutual NDA with TechStartup Inc for potential consulting engagement"
/contract-generator retainer "Monthly SEO services for LocalBiz, $1,500/mo, 3 month minimum"
```

- `$ARGUMENTS[0]`：合同类型（`service`、`sow`、`nda`、`retainer`、`hourly`）
- `$ARGUMENTS[1]`：包含关键条款的项目描述

## 合同类型

### `service` — 固定价格服务协议

适用于项目范围明确、价格固定的短期项目。

```markdown
# FREELANCE SERVICE AGREEMENT

**Agreement Date**: [Date]
**Agreement Number**: [SA-YYYY-NNN]

## PARTIES

**Service Provider** ("Contractor"):
[Name/Business Name]
[Address]
[Email]

**Client**:
[Client Name/Business]
[Address]
[Email]

## 1. SCOPE OF WORK

### 1.1 Project Description
[Detailed description of what will be delivered]

### 1.2 Deliverables
| # | Deliverable | Description | Due Date |
|---|------------|-------------|----------|
| 1 | [Item] | [Description] | [Date] |
| 2 | [Item] | [Description] | [Date] |
| 3 | [Item] | [Description] | [Date] |

### 1.3 Out of Scope
The following are explicitly NOT included in this agreement:
- [Item not included]
- [Item not included]
- [Common assumption to clarify]

Any work outside the defined scope requires a separate agreement
or written amendment to this contract with adjusted compensation.

## 2. TIMELINE

- **Project Start**: [Date]
- **Milestone 1**: [Description] — [Date]
- **Milestone 2**: [Description] — [Date]
- **Final Delivery**: [Date]

Timeline assumes timely feedback from Client. Delays in Client
feedback extend the timeline by an equal number of business days.

## 3. COMPENSATION

### 3.1 Total Fee
$[Amount] USD for the complete scope of work defined in Section 1.

### 3.2 Payment Schedule
| Payment | Amount | Due |
|---------|--------|-----|
| Deposit | $[X] (50%) | Upon signing |
| Milestone | $[X] (25%) | Upon [milestone] |
| Final | $[X] (25%) | Upon delivery |

### 3.3 Payment Terms
- Payment due within 14 days of invoice date
- Accepted methods: [Bank transfer / PayPal / Wise / Stripe]
- Late payments accrue interest at 1.5% per month
- Work may be paused if payment is more than 14 days overdue

## 4. REVISIONS

- [X] rounds of revisions are included in the project fee
- Each revision round includes feedback on all deliverables
  submitted to date
- Additional revision rounds are billed at $[X]/hour
- A "revision" is a change to approved work within the original
  scope. New features or scope changes are not revisions.

## 5. INTELLECTUAL PROPERTY

### 5.1 Ownership Transfer
Upon receipt of full payment, all deliverables and associated
intellectual property rights transfer to the Client.

### 5.2 Prior to Full Payment
Contractor retains all rights to the work until final payment
is received in full.

### 5.3 Contractor Tools
Contractor retains rights to any pre-existing tools, frameworks,
libraries, or methodologies used in the project. Client receives
a perpetual, non-exclusive license to use these as part of the
deliverables.

### 5.4 Portfolio Rights
Contractor may display the completed work in their portfolio
and marketing materials unless Client requests otherwise in
writing.

## 6. CONFIDENTIALITY

Both parties agree to keep confidential any proprietary
information shared during this engagement, including but not
limited to business strategies, customer data, technical
specifications, and financial information. This obligation
survives termination of this agreement for a period of 2 years.

## 7. TERMINATION

### 7.1 By Client
Client may terminate this agreement with 7 days written notice.
Client will pay for all work completed to date plus any
non-refundable expenses incurred.

### 7.2 By Contractor
Contractor may terminate with 14 days written notice if Client
fails to provide required feedback, materials, or payment
within the agreed timeframes.

### 7.3 Kill Fee
If Client terminates after work has begun, the deposit is
non-refundable. Additional compensation is due for work
completed beyond the deposit amount.

## 8. WARRANTIES AND LIABILITY

### 8.1 Contractor Warranties
Contractor warrants that:
- The work will be original and not infringe third-party rights
- The work will substantially conform to the agreed specifications
- Contractor has the right to enter this agreement

### 8.2 Limitation of Liability
Contractor's total liability under this agreement shall not
exceed the total fees paid by Client under this agreement.

### 8.3 No Consequential Damages
Neither party shall be liable for indirect, incidental, or
consequential damages.

## 9. GENERAL PROVISIONS

### 9.1 Independent Contractor
Contractor is an independent contractor, not an employee.

### 9.2 Governing Law
This agreement is governed by the laws of [State/Country].

### 9.3 Entire Agreement
This document constitutes the entire agreement. Amendments
must be in writing and signed by both parties.

### 9.4 Force Majeure
Neither party is liable for delays caused by events beyond
reasonable control.

---

**AGREED AND ACCEPTED:**

Contractor: _________________________ Date: ____________

Client:    _________________________ Date: ____________
```

### `sow` — 工作说明书（Statement of Work）

类似于固定价格服务协议，但更侧重于大型项目的详细工作范围，内容包括：
- 分阶段的详细需求
- 每个交付成果的验收标准
- 变更请求流程
- 沟通计划（每周会议、使用的工具、联系人信息）
- 项目假设及依赖关系

### `nda` — 保密协议（Non-Disclosure Agreement）

标准的保密协议，适用于双方或单方保密需求，内容包括：
- 保密信息的定义
- 接收方的保密义务
- 保密信息的例外情况（公开信息、独立开发的内容等）
- 保密协议的有效期限（通常为2年）
- 材料的归还或销毁要求
- 违反协议的补救措施

### `retainer` — 月度固定费用协议

适用于长期合作项目，内容包括：
- 每月固定的工作小时数（例如20小时/月）
- 未使用工作小时的处理方式（过期或顺延至下个月）
- 超时费用计算规则（超出固定费用部分的小时按小时费率计费）
- 服务范围（涵盖的工作类型）
- 月度报告要求
- 最低合作期限
- 解约通知期限（通常为30天）
- 月度账单生成频率

### `hourly` — 按小时计费协议

适用于按工作时间和材料计费的项目，内容包括：
- 按小时计费的费率
- 最小计费单位（15分钟或30分钟）
- 预计工作小时数（非强制性）
- 每周/每月的工作小时数上限
- 时间记录与报告方法
- 账单生成频率（每周或每两周一次）

## 输出结果

合同文件将保存在 `output/contracts/` 目录下：

```
output/contracts/
  [contract-type]-[client-name]-[date].md    # Markdown version
  [contract-type]-[client-name]-[date].html  # Print-ready HTML
```

生成的HTML版本具备以下特点：
- 适合打印的专业格式
- 清晰的章节编号
- 用于签署的空白行
- 便于打印的分页提示
- 每页均包含协议编号的页眉

## 重要提示：

1. 本工具提供的合同模板需根据具体项目情况进行定制。
2. 必须明确约定项目的具体交付成果；模糊的项目范围是引发纠纷的主要原因。
3. 必须包含“超出项目范围”的条款，以防止项目范围扩大。
4. 付款安排应与项目交付成果挂钩，以保护双方权益。
5. 知识产权保护条款应符合项目实际情况；部分客户可能需要包含“工作成果归委托方所有”的条款。
6. 建议双方通过电子签名工具（如DocuSign、HelloSign）进行签署，以便记录保存。