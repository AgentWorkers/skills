# 客户入职自动化工具

自动化整个客户入职流程——从最初的咨询到项目启动。包括处理客户信息表单、生成合同、收集付款信息、发送欢迎邮件以及设置项目相关内容。

## 该工具的功能

1. **客户信息收集**：从电子邮件或表单提交中获取新客户的详细信息。
2. **合同生成**：根据模板创建服务协议。
3. **付款处理**：自动发送Stripe支付链接。
4. **欢迎流程**：按时间顺序发送入职邮件（第0天、第1天、第3天、第7天）。
5. **项目设置**：为新客户创建文件夹、任务列表和待办事项清单。
6. **客户关系管理（CRM）更新**：将客户信息记录到您的跟踪系统中。

## 触发条件

当收到新的咨询时（通过匹配的电子邮件模式、表单Webhook或手动触发）：

```
New client: [name] | [email] | [service] | [budget]
```

## 工作流程

### 第1步：信息收集
解析收到的咨询信息，并提取以下内容：
- 客户名称和电子邮件地址
- 所请求的服务
- 选择的预算/套餐
- 项目时间安排
- 特殊要求

### 第2步：自动回复（立即执行）
发送一封个性化的确认邮件：
```
Subject: Thanks for reaching out, [Name]! Here's what happens next

Hi [Name],

Thanks for your interest in [service]. I've received your inquiry and here's what to expect:

1. I'll review your requirements (within 2 hours)
2. You'll receive a proposal with pricing
3. Once approved, we kick off immediately

In the meantime, here's a quick questionnaire to help me prepare:
[Link to intake form]

Best,
[Your name]
```

### 第3步：制定提案
创建一份提案文件，内容包括：
- 服务范围（根据所选服务确定）
- 价格（根据您的定价表）
- 项目时间表
- 合同条款

### 第4步：合同生成与付款
提案被接受后：
- 根据模板生成合同
- 为约定的付款金额创建Stripe支付链接
- 将合同和支付链接发送给客户

### 第5步：欢迎流程
付款完成后：
- **第0天**：发送欢迎邮件及访问凭证 + 项目启动问卷
- **第1天**：发送“入门指南” + 项目启动电话的日历链接
- **第3天**：进行项目进度确认 + 提供首个交付成果的预览
- **第7天**：更新项目进度 + 请求客户反馈

### 第6步：项目设置
- 在工作区中为新客户创建项目文件夹
- 根据服务类型生成任务清单
- 设置定期项目进度提醒

## 配置要求

- 需要使用ResendGrid、SendGrid或SMTP来发送电子邮件
- 需要使用Stripe来处理付款
- 需要配置OpenClaw的电子邮件/Webhook通道

## 所需工具/服务
- OpenClaw（用于处理Webhook和自动化流程）
- Stripe（用于处理支付）
- SendGrid或SMTP（用于发送电子邮件）