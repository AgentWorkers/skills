---
name: form-builder
description: 使用 `docassemble` 构建交互式文档表单和问卷  

**简介**  
`docassemble` 是一个功能强大的工具，允许您轻松创建具有交互功能的文档和问卷。它支持多种格式（如 HTML、PDF 等），并提供了丰富的模板和自定义选项，以满足您的需求。通过 `docassemble`，您可以轻松设计出美观且易于使用的表单和问卷，从而提高用户填写的效率和体验。  

**主要特性**  
1. **丰富的模板库**：`docassemble` 提供了大量的预定义模板，涵盖了各种类型的文档和问卷格式（如调查问卷、申请表、反馈表等）。  
2. **交互式元素**：支持添加表单验证、下拉菜单、复选框、单选框、日期选择器等交互式元素，使表单更加生动有趣。  
3. **自定义样式**：允许您自定义表单和问卷的样式，以匹配您的品牌形象。  
4. **多语言支持**：支持多种语言版本，方便国际化应用。  
5. **集成 API**：提供 API，方便与其他系统或应用程序进行集成。  
6. **易于使用**：具有直观的界面和详细的文档，即使是没有编程经验的用户也能快速上手。  

**使用步骤**  
1. **安装 docassemble**：根据您的操作系统和编程语言，从 [官方网站](https://docs.assemble.com/) 下载并安装 `docassemble`。  
2. **创建新文档**：使用 `docassemble` 的命令行工具或图形界面创建一个新的文档项目。  
3. **设计表单/问卷**：选择合适的模板，然后根据需要添加和修改元素。  
4. **生成输出文件**：生成所需的文档或问卷格式（如 HTML、PDF 等）。  
5. **部署和测试**：将生成的文件部署到目标平台上，并进行测试，确保其正常运行。  

**示例**  
以下是一个简单的示例，展示了如何使用 `docassemble` 创建一个简单的调查问卷：  

```bash
assemble --template="survey问卷模板" --output="survey问卷.html"
```

通过 `docassemble`，您可以轻松实现各种复杂的交互式表单和问卷功能，提升文档和用户交互的体验。更多详细信息，请访问 [官方网站](https://docs.assemble.com/)。
author: claude-office-skills
version: "1.0"
tags: [forms, questionnaire, docassemble, automation, legal]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: docassemble
  url: https://github.com/jhpyle/docassemble
  stars: 919
---

# 表单构建技能

## 概述

该技能利用 **docassemble** 平台来创建智能文档表单。**docassemble** 是一个用于引导式访谈并自动生成文档的工具，能够根据用户的回答动态调整问卷内容。

## 使用方法

1. 描述您需要的表单或文档的用途。
2. 指定条件逻辑的要求（即表单中的某些字段应根据用户的回答而显示或隐藏）。
3. 我将为您生成相应的 **docassemble** 问卷配置文件（格式为 YAML）。

**示例提示：**
- “为新客户创建一个信息收集表单。”
- “为法律文件生成一个基于用户选择的条件式问卷。”
- “创建一个多步骤的合同生成表单。”
- “设计一个交互式的文档组装表单。”

## 相关领域知识

### 采访结构（Interview Structure）
```yaml
metadata:
  title: Client Intake Form
  short title: Intake

---
question: |
  What is your name?
fields:
  - First Name: first_name
  - Last Name: last_name

---
question: |
  What type of service do you need?
field: service_type
choices:
  - Contract Review
  - Document Drafting
  - Consultation

---
mandatory: True
question: |
  Thank you, ${ first_name }!
subquestion: |
  We will contact you about your ${ service_type } request.
```

### 条件逻辑（Conditional Logic）
```yaml
---
question: |
  Are you a business or individual?
field: client_type
choices:
  - Business
  - Individual

---
if: client_type == "Business"
question: |
  What is your company name?
fields:
  - Company: company_name
  - EIN: ein
    required: False

---
if: client_type == "Individual"
question: |
  What is your date of birth?
fields:
  - Birthdate: birthdate
    datatype: date
```

### 字段类型（Field Types）
```yaml
fields:
  # Text
  - Name: name
  
  # Email
  - Email: email
    datatype: email
  
  # Number
  - Age: age
    datatype: integer
  
  # Currency
  - Amount: amount
    datatype: currency
  
  # Date
  - Start Date: start_date
    datatype: date
  
  # Yes/No
  - Agree to terms?: agrees
    datatype: yesno
  
  # Multiple choice
  - Color: color
    choices:
      - Red
      - Blue
      - Green
  
  # Checkboxes
  - Select options: options
    datatype: checkboxes
    choices:
      - Option A
      - Option B
  
  # File upload
  - Upload document: document
    datatype: file
```

### 文档生成（Document Generation）
```yaml
---
mandatory: True
question: |
  Your document is ready.
attachment:
  name: Contract
  filename: contract
  content: |
    # Service Agreement
    
    This agreement is between **${ client_name }**
    and **Service Provider**.
    
    ## Services
    ${ service_description }
    
    ## Payment
    Total amount: ${ currency(amount) }
    
    Date: ${ today() }
```

## 示例：客户信息收集表单（Example: Client Information Collection Form）
```yaml
metadata:
  title: Legal Client Intake
  short title: Intake

---
objects:
  - client: Individual

---
question: |
  Welcome to our intake form.
subquestion: |
  Please answer the following questions.
continue button field: intro_screen

---
question: |
  What is your name?
fields:
  - First Name: client.name.first
  - Last Name: client.name.last
  - Email: client.email
    datatype: email
  - Phone: client.phone
    required: False

---
question: |
  What type of matter is this?
field: matter_type
choices:
  - Contract: contract
  - Dispute: dispute
  - Advisory: advisory

---
if: matter_type == "contract"
question: |
  Contract Details
fields:
  - Contract Type: contract_type
    choices:
      - Employment
      - Service Agreement
      - NDA
  - Other Party: other_party
  - Estimated Value: contract_value
    datatype: currency

---
mandatory: True
question: |
  Thank you, ${ client.name.first }!
subquestion: |
  **Summary:**
  
  - Name: ${ client.name }
  - Email: ${ client.email }
  - Matter: ${ matter_type }
  
  We will contact you within 24 hours.
```

## 资源（Resources）

- [docassemble 文档](https://docassemble.org/docs.html)
- [GitHub 仓库](https://github.com/jhpyle/docassemble)