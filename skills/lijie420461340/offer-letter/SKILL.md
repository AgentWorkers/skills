---
name: Offer Letter Generator
description: 创建包含薪酬和条款的正式雇佣邀请函
author: claude-office-skills
version: "1.0"
tags: [hr, recruitment, hiring, employment, legal]
models: [claude-sonnet-4, claude-opus-4]
tools: [text_editor]
---

# 招聘offer生成器

该工具能够生成专业的就业offer信，清晰地说明工作条款和薪酬信息。

## 概述

此功能可生成正式的offer信，具备以下特点：
- 明确说明职位名称和薪酬待遇
- 列出主要的雇佣条款
- 确保符合法律法规要求
- 为候选人提供良好的体验

## 使用方法

请提供以下信息：

### 必填项
1. **候选人姓名**：完整的法定姓名
2. **职位名称**：提供的职位
3. **入职日期**：建议的入职时间
4. **薪酬**：基本工资及支付频率
5. **雇佣类型**：全职、兼职或合同制
6. **上级**：经理的姓名和职位

### 可选项
7. **股权/奖金**：股票期权、签约奖金、年度奖金
8. **福利**：健康保险、401(k)退休计划、带薪休假政策
9. **工作地点**：办公室地址或远程办公
10. **回复截止日期**：offer的有效期限
11. **附加条件**：背景调查、推荐信等

## 输出格式

```
[Company Letterhead]

[Date]

[Candidate Name]
[Address - if known]

Dear [First Name],

RE: Employment Offer - [Job Title]

[Opening paragraph - excitement about offering position]

[Position details paragraph]

[Compensation paragraph]

[Benefits summary paragraph]

[Contingencies paragraph - if applicable]

[Next steps and deadline]

[Closing]

Sincerely,
[Hiring Manager Name]
[Title]

---
ACCEPTANCE

I accept this offer of employment:

Signature: _______________________
Print Name: ______________________
Date: ___________________________
```

## 模板结构

### 开头部分
```
We are pleased to extend this offer of employment for the position of 
[Job Title] at [Company Name]. After our interview process, we believe 
your skills and experience make you an excellent addition to our team.
```

### 职位详情
```
Position: [Job Title]
Department: [Department]
Reports To: [Manager Name], [Manager Title]
Start Date: [Date]
Work Location: [Location/Remote]
Employment Type: [Full-time/Part-time/Contract]
```

### 薪酬信息
```
Base Salary: $[Amount] per [year/month/hour]
Payment Schedule: [Bi-weekly/Monthly]

[If applicable:]
Signing Bonus: $[Amount], payable [timing]
Annual Bonus: Up to [X]% of base salary, based on performance
Equity: [X] stock options, vesting over [Y] years with [Z]-year cliff
```

### 福利概述
```
You will be eligible for our comprehensive benefits package, including:
- Medical, dental, and vision insurance
- 401(k) with [X]% company match
- [X] days paid time off annually
- [Additional benefits]

Full benefits details will be provided during onboarding.
```

### 附加条件
```
This offer is contingent upon:
- Successful completion of a background check
- Verification of your eligibility to work in [Country]
- [Other contingencies]
```

### 接受条款
```
Please indicate your acceptance by signing and returning this letter 
by [Date]. This offer will expire if not accepted by this date.

If you have any questions, please contact [Name] at [Email/Phone].

We look forward to welcoming you to the team!
```

## 示例

### 示例请求
```
Create an offer letter:
- Candidate: Sarah Johnson
- Position: Product Manager
- Start: March 15, 2026
- Salary: $145,000/year
- Bonus: 15% target
- Equity: 10,000 options, 4-year vest
- Manager: Mike Chen, VP Product
- Location: Hybrid (NYC office 2 days/week)
- Deadline: January 31, 2026
```

### 示例输出
```
ACME CORPORATION
123 Innovation Way, New York, NY 10001

January 15, 2026

Sarah Johnson

Dear Sarah,

RE: Employment Offer - Product Manager

We are thrilled to offer you the position of Product Manager at ACME 
Corporation! Your experience in B2B product strategy and your insights 
during our interviews impressed the entire team. We believe you'll make 
significant contributions to our product vision.

POSITION DETAILS
Position: Product Manager
Department: Product
Reports To: Mike Chen, VP of Product
Start Date: March 15, 2026
Work Location: Hybrid - NYC office (Tuesdays & Thursdays), Remote otherwise
Employment Type: Full-time, Exempt

COMPENSATION
Base Salary: $145,000 annually, paid bi-weekly
Annual Bonus: Target of 15% of base salary ($21,750), based on individual 
and company performance
Equity: 10,000 stock options, vesting over 4 years with a 1-year cliff

BENEFITS
You will be eligible for our comprehensive benefits package starting on 
your first day, including:
- Medical, dental, and vision insurance (100% employee coverage)
- 401(k) with 4% company match
- 20 days paid time off + 10 company holidays
- $1,500 annual professional development budget
- Commuter benefits

This offer is contingent upon successful completion of a standard 
background check.

Please indicate your acceptance by signing below and returning this 
letter by January 31, 2026. If you have questions, please reach out 
to me directly at mike.chen@acme.com.

We're excited about the possibility of you joining our team!

Sincerely,

Mike Chen
VP of Product
ACME Corporation

---
ACCEPTANCE

I accept this offer of employment and agree to the terms outlined above.

Signature: _______________________

Print Name: ______________________

Date: ___________________________
```

## 最佳实践

### 应遵循的原则
- 使用清晰、直接的语言
- 包括所有重要条款
- 明确指定截止日期
- 提供咨询联系方式
- 包含签名栏

### 应避免的行为
- 不要做出超出标准条款的承诺
- 不要使用歧视性语言
- 不要遗漏任何重要细节
- 不要使用过于复杂的法律术语

### 法律注意事项
- Offer信通常不属于正式合同（必要时需添加免责声明）
- 在美国，应明确说明雇佣类型为“at-will”（随时可解除的雇佣关系）
- 股权相关条款应参照完整协议
- 发送前需经过法律或人力资源部门的审核

## 限制事项
- 本文档仅为模板指南，不构成法律建议
- 各地区的雇佣法律可能有所不同
- 必须纳入公司的具体政策
- 复杂的股权安排需进行法律审查
- 国际offer信件有额外的要求