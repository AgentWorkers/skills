---
name: "contract-and-proposal-writer"
description: "合同与提案撰写专家"
---
# 合同与提案编写工具

**级别：** 高级  
**类别：** 业务增长  
**领域：** 法律文件、业务发展、客户关系  

---

## 概述  
该工具可生成专业的、符合当地法律要求的商业文件，包括自由职业合同、项目提案、工作说明书（SOW）、保密协议（NDAs）和主服务协议（MSAs）。输出格式为结构化的Markdown，并提供转换为DOCX文件的说明。支持美国（特拉华州）、欧盟（GDPR）、英国和DACH（德国/奥地利/瑞士）地区的法律规范。  

**请注意：** 本工具不能替代专业法律顾问。对于高价值或复杂的业务项目，建议在使用这些模板前咨询律师。  

---

## 核心功能  
- 自由职业开发合同（固定价格/按小时计费）  
- 包含时间表和预算分解的项目提案  
- 带有交付物矩阵的工作说明书（SOW）  
- 双方或单方的保密协议（NDAs）  
- 主服务协议（MSAs）  
- 针对不同司法管辖区的特定条款（美国/欧盟/英国/德国/奥地利/瑞士）  
- 符合GDPR的数据处理附加条款（针对欧盟/德国/奥地利/瑞士地区）  

---

## 关键条款参考  
| 条款 | 选项 |  
|--------|---------|  
| 支付条款 | 净额支付、分阶段付款、按月预付费用 |  
| 知识产权归属 | 雇佣制（美国）、转让（欧盟/英国）、许可返还 |  
| 责任限制 | 合同金额的1倍（标准情况）、3倍（高风险情况） |  
| 合同终止 | 有正当理由时终止（14天通知期）；便利性终止（30/60/90天通知期） |  
| 保密条款 | 保密期限2-5年；商业机密永久保密 |  
| 保修条款 | 按“现状”提供产品；有限期的30/90天保修 |  
| 争议解决 | 仲裁（AAA/ICC）；法院（根据司法管辖区选择） |  

---

## 使用场景  
- 需要快速起草新客户合同  
- 客户要求提供包含价格和时间表的提案  
- 需要主服务协议（MSA）的合作伙伴关系或供应商关系  
- 需要保密协议（NDA）来保护知识产权或机密信息  
- 涉及欧盟/德国/奥地利/瑞士地区的项目，且数据处理需符合GDPR规定  

---

## 工作流程  
### 1. 收集需求  
向用户询问：  
    1. 文件类型（合同/提案/工作说明书/保密协议/主服务协议）  
    2. 所在司法管辖区（美国特拉华州/欧盟/英国/德国/奥地利/瑞士）  
    3. 合同类型（固定价格/按小时计费/按月预付费用）  
    4. 合同各方（名称、角色、企业地址）  
    5. 项目范围（1-3句话概括）  
    6. 总金额或每小时费率  
    7. 合同开始/结束日期或期限  
    7. 特殊要求（知识产权转让、白牌使用、分包商等）  

### 2. 选择模板  
根据文件类型和司法管辖区选择相应的模板：  
| 文件类型 | 司法管辖区 | 模板 |  
|------|-------------|----------|  
| 固定价格的开发合同 | 任意 | 模板A |  
| 咨询服务按月预付合同 | 任意 | 模板B |  
| SaaS合作伙伴协议 | 任意 | 模板C |  
| 双方保密协议（NDA） | 欧盟/英国/德国/奥地利/瑞士 | NDA-M |  
| 单方保密协议（NDA） | 欧盟/英国/德国/奥地利/瑞士 | NDA-OW |  
| 工作说明书（SOW） | 任意 | 模板C |  

### 3. 生成并填写合同内容  
填写所有[方括号内]的占位符内容。缺失的数据请标记为“必需填写”。  

### 4. 转换为DOCX文件  
```bash
# Install pandoc
brew install pandoc        # macOS
apt install pandoc         # Ubuntu

# Basic conversion
pandoc contract.md -o contract.docx \
  --reference-doc=reference.docx \
  -V geometry:margin=1in

# With numbered sections (legal style)
pandoc contract.md -o contract.docx \
  --number-sections \
  -V documentclass=article \
  -V fontsize=11pt

# With custom company template
pandoc contract.md -o contract.docx \
  --reference-doc=company-template.docx
```  

---

## 各司法管辖区的注意事项  
### 美国（特拉华州）  
- 适用特拉华州法律  
- 采用“雇佣制”原则（《版权法》第101条）  
- 仲裁机构：AAA商业仲裁规则  
- 竞业禁止条款：需明确合理范围和时间限制  

### 欧盟（GDPR）  
- 处理个人数据时必须包含数据处理附加条款  
- 在某些成员国，知识产权转让需另行签署书面协议  
- 仲裁机构：国际商会（ICC）或当地仲裁机构  

### 英国（脱欧后）  
- 适用英国法律  
- 知识产权相关法规：《1977年专利法》/《1988年数据保护法》  
- 仲裁机构：伦敦国际仲裁院（LCIA）  
- 数据保护：遵循英国GDPR规定  

### 德国/奥地利/瑞士（DACH地区）  
- 合同受《德国民法典》（BGB）管辖  
- 某些条款需以书面形式体现（BGB第126条）  
- 知识产权：作者保留精神权利；需明确转让使用权  
- 竞业禁止条款：最长2年，需支付补偿  
- 争议解决：德国法院或DIS仲裁  
- 个人数据处理需遵守《德国数据保护法》（DSGVO）  

---

## 模板示例  
- **模板A：Web开发固定价格合同**  
```markdown
# SOFTWARE DEVELOPMENT AGREEMENT

**Effective Date:** [DATE]
**Client:** [CLIENT LEGAL NAME], [ADDRESS] ("Client")
**Developer:** [YOUR LEGAL NAME / COMPANY], [ADDRESS] ("Developer")

---

## 1. SERVICES

Developer agrees to design, develop, and deliver:

**Project:** [PROJECT NAME]
**Description:** [1-3 sentence scope]

**Deliverables:**
- [Deliverable 1] due [DATE]
- [Deliverable 2] due [DATE]
- [Deliverable 3] due [DATE]

## 2. PAYMENT

**Total Fee:** [CURRENCY] [AMOUNT]

| Milestone | Amount | Due |
|-----------|--------|-----|
| Contract signing | 50% | Upon execution |
| Beta delivery | 25% | [DATE] |
| Final acceptance | 25% | Within 5 days of acceptance |

Late payments accrue interest at 1.5% per month.
Client has [10] business days to accept or reject deliverables in writing.

## 3. INTELLECTUAL PROPERTY

Upon receipt of full payment, Developer assigns all right, title, and interest in the
Work Product to Client as a work made for hire (US) / by assignment of future copyright (EU/UK).

Developer retains the right to display Work Product in portfolio unless Client
requests confidentiality in writing within [30] days of delivery.

Pre-existing IP (tools, libraries, frameworks) remains Developer's property.
Developer grants Client a perpetual, royalty-free license to use pre-existing IP
as embedded in the Work Product.

## 4. CONFIDENTIALITY

Each party keeps confidential all non-public information received from the other.
This obligation survives termination for [3] years.

## 5. WARRANTIES

Developer warrants Work Product will substantially conform to specifications for
[90] days post-delivery. Developer will fix material defects at no charge during
this period. EXCEPT AS STATED, WORK PRODUCT IS PROVIDED "AS IS."

## 6. LIABILITY

Developer's total liability shall not exceed total fees paid under this Agreement.
Neither party liable for indirect, incidental, or consequential damages.

## 7. TERMINATION

For Cause: Either party may terminate if the other materially breaches and fails
to cure within [14] days of written notice.

For Convenience: Client may terminate with [30] days written notice and pay for
all work completed plus [10%] of remaining contract value.

## 8. DISPUTE RESOLUTION

US: Binding arbitration under AAA Commercial Rules, [CITY], Delaware law.
EU/DACH: ICC / DIS arbitration, [CITY]. German / English law.
UK: LCIA Rules, London. English law.

## 9. GENERAL

- Entire Agreement: Supersedes all prior discussions.
- Amendments: Must be in writing, signed by both parties.
- Independent Contractor: Developer is not an employee of Client.

---

CLIENT: _________________________ Date: _________
[CLIENT NAME], [TITLE]

DEVELOPER: _________________________ Date: _________
[YOUR NAME], [TITLE]
```  

- **模板B：按月咨询服务预付合同**  
```markdown
# CONSULTING RETAINER AGREEMENT

**Effective Date:** [DATE]
**Client:** [CLIENT LEGAL NAME] ("Client")
**Consultant:** [YOUR NAME / COMPANY] ("Consultant")

---

## 1. SERVICES

Consultant provides [DOMAIN, e.g., "CTO advisory and technical architecture"] services.

**Monthly Hours:** Up to [X] hours/month
**Rollover:** Unused hours [do / do not] roll over (max [X] hours banked)
**Overflow Rate:** [CURRENCY] [RATE]/hr for hours exceeding retainer

## 2. FEES

**Monthly Retainer:** [CURRENCY] [AMOUNT], due on the 1st of each month.
**Payment Method:** Bank transfer / Stripe / SEPA direct debit
**Late Payment:** 2% monthly interest after [10]-day grace period.

## 3. TERM AND TERMINATION

**Initial Term:** [3] months starting [DATE]
**Renewal:** Auto-renews monthly unless either party gives [30] days written notice.
**Immediate termination:** For material breach uncured after [7] days notice.

On termination, Consultant delivers all work in progress within [5] business days.

## 4. INTELLECTUAL PROPERTY

Work product created under this Agreement belongs to [Client / Consultant / jointly].
Advisory output (recommendations, analyses) are Client property upon full payment.

## 5. EXCLUSIVITY

[OPTION A - Non-exclusive:]
This Agreement is non-exclusive. Consultant may work with other clients.

[OPTION B - Partial exclusivity:]
Consultant will not work with direct competitors of Client during the term
and [90] days thereafter.

## 6. CONFIDENTIALITY AND DATA PROTECTION

EU/DACH: If Consultant processes personal data on behalf of Client, the parties
shall execute a Data Processing Agreement (DPA) per Art. 28 GDPR.

## 7. LIABILITY

Consultant's aggregate liability is capped at [3x] the fees paid in the [3] months
preceding the claim.

---

Signatures as above.
```  

- **模板C：SaaS合作伙伴协议**  
```markdown
# SAAS PARTNERSHIP AGREEMENT

**Effective Date:** [DATE]
**Provider:** [NAME], [ADDRESS]
**Partner:** [NAME], [ADDRESS]

---

## 1. PURPOSE

Provider grants Partner [reseller / referral / white-label / integration] rights to
Provider's [PRODUCT NAME] ("Software") subject to this Agreement.

## 2. PARTNERSHIP TYPE

[ ] Referral: Partner refers customers; earns [X%] of first-year ARR per referral.
[ ] Reseller: Partner resells licenses; earns [X%] discount off list price.
[ ] White-label: Partner rebrands Software; pays [AMOUNT]/month platform fee.
[ ] Integration: Partner integrates Software via API; terms in Exhibit A.

## 3. REVENUE SHARE

| Tier | Monthly ARR Referred | Commission |
|------|---------------------|------------|
| Bronze | < $10,000 | [X]% |
| Silver | $10,000-$50,000 | [X]% |
| Gold | > $50,000 | [X]% |

Payout: Net-30 after month close, minimum $[500] threshold.

## 4. INTELLECTUAL PROPERTY

Each party retains all IP in its own products. No implied licenses.
Partner may use Provider's marks per Provider's Brand Guidelines (Exhibit B).

## 5. DATA AND PRIVACY

Each party is an independent data controller for its own customers.
Joint processing requires a separate DPA (Exhibit C - EU/DACH projects).

## 6. TERM

Initial: [12] months. Renews annually unless [90]-day written notice given.
Termination for Cause: [30]-day cure period for material breach.

## 7. LIMITATION OF LIABILITY

Each party's liability capped at [1x] fees paid/received in prior [12] months.
Mutual indemnification for IP infringement claims from own products.

---

Signatures, exhibits, and governing law per applicable jurisdiction.
```  

- **GDPR数据处理附加条款（欧盟/德国/奥地利/瑞士地区）**  
```markdown
## DATA PROCESSING ADDENDUM (Art. 28 GDPR)

Controller: [CLIENT NAME]
Processor: [CONTRACTOR NAME]

### Subject Matter
Processor processes personal data on behalf of Controller solely to perform services
under the main Agreement.

### Categories of Data Subjects
[e.g., end users, employees, customers]

### Categories of Personal Data
[e.g., names, email addresses, usage data]

### Processing Duration
For the term of the main Agreement; deletion within [30] days of termination.

### Processor Obligations
- Process data only on Controller's documented instructions
- Ensure persons authorized to process have committed to confidentiality
- Implement technical and organizational measures per Art. 32 GDPR
- Assist Controller with data subject rights requests
- Not engage sub-processors without prior written consent
- Delete or return all personal data upon termination

### Sub-processors (current as of Effective Date)
| Sub-processor | Location | Purpose |
|--------------|----------|---------|
| [AWS / GCP / Azure] | [Region] | Cloud hosting |
| [Other] | [Location] | [Purpose] |

### Cross-border Transfers
Data transfers outside EEA covered by: [ ] SCCs  [ ] Adequacy Decision  [ ] BCRs
```  

---

## 常见问题  
1. **知识产权转让条款缺失**：在欧盟，仅规定“雇佣制”是不够的；在德国/奥地利/瑞士地区需明确转让使用权。  
2. **验收标准不明确**：需明确“接受”的定义（书面确认、X天内拒绝）。  
3. **缺乏变更流程**：项目范围超出预期可能导致合同问题；应添加超出范围工作的处理条款。  
4. **司法管辖区选择不当**：为仅针对德国的项目选择特拉华州法律可能导致执行困难。  
5. **责任限制条款缺失**：若无责任限制，一个小错误可能导致巨额赔偿。  
6. **口头修改**：口头修改的合同难以执行；所有修改均需书面形式。  

## 最佳实践  
- 对于金额超过1万美元的项目，建议采用分阶段付款方式（而非净额支付），以降低现金流风险。  
- 对于欧盟/德国/奥地利/瑞士地区的项目，务必确认是否需要数据处理附加条款（涉及个人数据时）。  
- 在德国/奥地利/瑞士地区，务必加入书面形式条款。  
- 对于超过3个月的项目，加入不可抗力条款。  
- 对于按月预付费用的服务，明确回复时间（例如紧急情况4小时内响应，常规情况24小时内响应）。  
- 将模板放入版本控制系统中，并使用`git diff`跟踪修改记录。  
- 每年审查合同内容，因为法律会更新（尤其是GDPR相关法规）。  
- 对于保密协议，明确约定合同终止后的保密材料处理方式（归还或销毁）。