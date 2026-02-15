---
name: contract-template
description: 使用 Accord Project 生成智能合约模板——这些模板具有法律约束力且可被机器读取。
author: claude-office-skills
version: "1.0"
tags: [contract, legal, template, accord, smart-contracts]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: accord-project
  url: https://github.com/accordproject
  stars: 322
---

# 合同模板技能

## 概述

该技能允许使用 **Accord Project**（一个开源框架）来创建智能合约模板。Accord Project 支持创建具有法律约束力且可被机器读取的合约，并支持在模板中嵌入逻辑以实现合约执行的自动化。

## 使用方法

1. 描述合约的类型和条款；
2. 指定变量和逻辑规则；
3. Accord Project 会自动生成相应的合约模板。

**示例提示：**
- “创建一个包含可变条款的保密协议（NDA）模板”；
- “制定包含付款节点的服务协议模板”；
- “生成租赁协议模板”；
- “设计包含终止条款的咨询合同模板”。

## 相关领域知识

### 模板结构

```
contract-template/
├── package.json           # Metadata
├── grammar/
│   └── template.tem.md    # Natural language template
├── model/
│   └── model.cto          # Data model
├── logic/
│   └── logic.ergo         # Business logic
└── text/
    └── sample.md          # Sample contract
```

### 模板语法（TemplateMark）

```markdown
# Service Agreement

This Agreement is made between [{supplier}] ("Supplier") 
and [{buyer}] ("Buyer").

## Services
The Supplier agrees to provide [{serviceDescription}].

## Payment
The Buyer shall pay [{paymentAmount}] within 
[{paymentDays}] days of invoice.

## Term
This Agreement begins on [{startDate as "MMMM DD, YYYY"}] 
and continues for [{termMonths}] months.

{{#if latePenalty}}
## Late Payment
A penalty of [{penaltyPercent}]% applies to late payments.
{{/if}}
```

### 数据模型（Concerto）

```cto
namespace org.example.service

import org.accordproject.time.*

asset ServiceAgreement extends Contract {
  o String supplier
  o String buyer
  o String serviceDescription
  o Double paymentAmount
  o Integer paymentDays
  o DateTime startDate
  o Integer termMonths
  o Boolean latePenalty optional
  o Double penaltyPercent optional
}

transaction PaymentRequest {
  o Double amount
  o DateTime dueDate
}

transaction PaymentResponse {
  o Double amount
  o Double penalty
  o DateTime paymentDue
}
```

### 业务逻辑（Ergo）

```ergo
namespace org.example.service

import org.accordproject.time.*

contract ServiceContract over ServiceAgreement {
  
  clause payment(request : PaymentRequest) : PaymentResponse {
    let dueDate = addDuration(request.dueDate, 
                              Duration{ amount: contract.paymentDays, unit: ~org.accordproject.time.TemporalUnit.days });
    
    let penalty = 
      if contract.latePenalty
      then request.amount * contract.penaltyPercent / 100.0
      else 0.0;
    
    return PaymentResponse{
      amount: request.amount,
      penalty: penalty,
      paymentDue: dueDate
    }
  }
}
```

### 使用 Cicero CLI

```bash
# Install
npm install -g @accordproject/cicero-cli

# Parse contract
cicero parse --template ./contract-template --sample ./text/sample.md

# Execute logic
cicero trigger --template ./contract-template \
  --sample ./text/sample.md \
  --request ./request.json

# Draft new contract
cicero draft --template ./contract-template --data ./data.json
```

## 示例：保密协议（NDA）模板

### template.tem.md
```markdown
# Non-Disclosure Agreement

This Non-Disclosure Agreement ("Agreement") is entered into 
as of [{effectiveDate as "MMMM DD, YYYY"}] by and between:

**Disclosing Party:** [{disclosingParty}]
**Receiving Party:** [{receivingParty}]

## 1. Confidential Information

"Confidential Information" means all non-public information 
disclosed by the Disclosing Party, including but not limited to:
[{confidentialScope}].

## 2. Obligations

The Receiving Party agrees to:
- Maintain confidentiality for [{termYears}] years
- Use information only for [{permittedPurpose}]
- Not disclose to third parties without written consent

## 3. Exclusions

This Agreement does not apply to information that:
{{#if hasExclusions}}
[{exclusions}]
{{else}}
- Is or becomes publicly available
- Was known prior to disclosure
- Is independently developed
{{/if}}

## 4. Return of Materials

Upon termination, the Receiving Party shall return or destroy 
all Confidential Information within [{returnDays}] days.

## 5. Remedies

{{#if monetaryPenalty}}
Breach of this Agreement shall result in liquidated damages 
of [{penaltyAmount}].
{{else}}
The Disclosing Party shall be entitled to seek injunctive relief.
{{/if}}

**SIGNATURES**

Disclosing Party: ____________________
Date: ____________________

Receiving Party: ____________________
Date: ____________________
```

### data.json
```json
{
  "effectiveDate": "2024-01-15",
  "disclosingParty": "Tech Corp",
  "receivingParty": "Consultant LLC",
  "confidentialScope": "trade secrets, customer lists, and technical specifications",
  "termYears": 3,
  "permittedPurpose": "evaluating a potential business relationship",
  "hasExclusions": false,
  "returnDays": 30,
  "monetaryPenalty": true,
  "penaltyAmount": "$50,000"
}
```

## 资源

- [Accord Project](https://accordproject.org/)
- [GitHub 组织页面](https://github.com/accordproject)
- [模板库](https://templates.accordproject.org/)