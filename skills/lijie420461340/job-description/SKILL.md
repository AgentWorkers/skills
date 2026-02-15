---
name: Job Description Generator
description: 创建引人注目的职位招聘信息，明确列出职位要求、职责以及应聘者的资格条件。
author: claude-office-skills
version: "1.0"
tags: [hr, recruitment, hiring, job-posting]
models: [claude-sonnet-4, claude-opus-4]
tools: [text_editor]
---

# 职位描述生成器

本工具可帮助您生成专业且具有包容性的职位描述，从而吸引符合条件的候选人。

## 概述

该技能专为人力资源专业人士和招聘经理设计，旨在帮助他们创建完善的职位公告：
- 清晰传达职位要求
- 使用包容性、无偏见的语言
- 遵循行业最佳实践
- 吸引多元化的、具备资格的候选人

## 使用方法

请提供以下信息：
1. **职位名称**：职位的名称
2. **部门**：所属的团队或部门
3. **职位级别**：初级、中级、高级、主管、总监等
4. **就业类型**：全职、兼职、合同制
5. **工作地点**：现场办公、远程办公、混合办公
6. **主要职责**：职位的具体工作内容
7. **必备要求**：必须具备的资格条件
8. **优先考虑的资格**：推荐具备的资格条件
9. **公司信息**：公司简介（可选）

## 输出格式

```markdown
# [Job Title]

## About [Company]
[Brief company description]

## About the Role
[2-3 sentences describing the position and its impact]

## What You'll Do
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]
...

## What We're Looking For

### Required
- [Requirement 1]
- [Requirement 2]
...

### Nice to Have
- [Preferred qualification 1]
- [Preferred qualification 2]
...

## What We Offer
- [Benefit 1]
- [Benefit 2]
...

## How to Apply
[Application instructions]
```

## 最佳实践

### 语言指南
- 使用“您”而非“理想的候选人”
- 避免使用性别歧视性的语言（如“他/她”）
- 去除不必要的行话
- 明确区分必备要求和优先考虑的条件
- 如有可能，请提供薪资范围（这能提高申请率30%）

### 应避免的错误表述
- 使用“超级明星”/“高手”/“专家”等夸张词汇，改用“专家”或“资深人士”
- 对于工作节奏的描述，应具体说明工作量
- 必备要求过多，建议控制在5-7项以内
- 职责描述模糊不清，应使用可衡量的成果来描述工作内容

### 包容性语言示例
| 应避免的表述 | 可替换的表述 |
|------------|-------------------|
| “年轻且充满活力” | “积极进取、热情高涨” |
| “英语母语者” | “英语流利” |
| “文化契合度” | “价值观一致” |
| “数字原住民” | “熟练使用数字工具” |

## 示例

### 示例请求
```
Create a job description for:
- Title: Senior Frontend Developer
- Department: Engineering
- Level: Senior (5+ years)
- Type: Full-time, Remote
- Tech stack: React, TypeScript, GraphQL
- Team size: 8 engineers
- Company: B2B SaaS startup, Series B
```

### 示例输出
```markdown
# Senior Frontend Developer

## About Us
We're a Series B B2B SaaS startup transforming how enterprises manage their workflows. Our engineering team of 40+ builds products used by Fortune 500 companies.

## About the Role
Join our 8-person frontend team to architect and build the next generation of our platform. You'll have significant impact on technical decisions and mentor junior developers.

## What You'll Do
- Design and implement complex UI features using React and TypeScript
- Collaborate with designers to create intuitive user experiences
- Optimize application performance and accessibility
- Contribute to our GraphQL API design
- Mentor junior developers through code reviews and pairing
- Participate in technical planning and architecture discussions

## What We're Looking For

### Required
- 5+ years of frontend development experience
- Strong proficiency in React and TypeScript
- Experience with GraphQL or similar query languages
- Track record of building accessible, performant web applications
- Excellent communication skills

### Nice to Have
- Experience with design systems
- Contributions to open source projects
- Experience at B2B SaaS companies
- Familiarity with testing frameworks (Jest, Cypress)

## What We Offer
- Competitive salary: $150,000 - $190,000
- Equity package
- Fully remote with flexible hours
- Health, dental, and vision insurance
- $2,000 annual learning budget
- Home office stipend

## How to Apply
Send your resume and a brief note about why you're interested to careers@company.com
```

## 领域知识

### 职位级别（常见划分）
| 职位级别 | 工作经验年限 | 职责范围 |
|---------|-----------------|-------------------|
| 初级/初级员工 | 0-2年 | 执行具体任务 |
| 中级员工 | 2-5年 | 独立完成项目 |
| 高级员工 | 5-8年 | 提供技术指导 |
| 主管/团队负责人 | 8-12年 | 对团队产生直接影响 |
| 总监/负责人 | 12年以上 | 负责整个团队的管理工作 |

### 常见的福利项目
- 医疗保险
- 退休计划（401(k)计划、养老金）
- 休假政策
- 远程办公选项
- 专业发展机会
- 亲子假
- 工作设备/补贴

## 限制事项
- 无法保证内容的合法性（需由人力资源部门或法律顾问审核）
- 薪资标准可能不反映当地市场行情
- 行业特定要求需依据行业知识来确定
- 无法验证所提供的公司信息