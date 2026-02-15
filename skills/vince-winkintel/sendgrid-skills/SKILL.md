---
name: sendgrid
description: SendGrid电子邮件平台集成用于发送和接收电子邮件。相关功能被分配到不同的子技能中：  
- `send-email`：用于发送交易性电子邮件；  
- `sendgrid-inbound`：用于通过Inbound Parse Webhook接收电子邮件。  
当用户提及SendGrid、交易性电子邮件、电子邮件API、电子邮件解析或电子邮件Webhook时，应使用此功能。  
触发条件包括：SendGrid事件、发送电子邮件、接收电子邮件、电子邮件Webhook、Inbound Parse以及交易性电子邮件处理。
requirements:
  env:
    - SENDGRID_API_KEY
  env_optional:
    - SENDGRID_FROM
  binaries:
    - curl
    - jq
    - node
  binaries_optional:
    - dig
    - nslookup
---

# SendGrid

## 概述

SendGrid 是一个专为开发者设计的电子邮件平台。本技能会引导您了解与该平台相关的具体功能及子技能。

## 子技能

| 功能          | 技能名称       | 使用场景                |
|--------------|--------------|----------------------|
| **发送电子邮件**    | `send-email`    | 发送交易型邮件、通知邮件、简单邮件以及使用动态模板 |
| **接收电子邮件**    | `sendgrid-inbound` | 设置入站解析 Webhook、配置 MX 记录、解析接收到的电子邮件 |

## 常见设置

### API 密钥

将 API 密钥存储在环境变量中：
```bash
export SENDGRID_API_KEY=SG.xxxxxxxxx
```

### SDK 安装

请参阅 `send-email` 技能中的安装说明，了解各语言版本的安装步骤。

## 何时选择 SendGrid 而非其他服务

```
What's your use case?
├─ Transactional emails (receipts, notifications, password resets)
│  └─ SendGrid (send-email) ✅
├─ Marketing campaigns / bulk email
│  └─ Consider SendGrid Marketing Campaigns (outside this skill)
├─ Receiving emails programmatically
│  └─ SendGrid Inbound Parse (sendgrid-inbound) ✅
└─ Simple SMTP relay
   └─ SendGrid SMTP (outside this skill)
```

## 资源

- [SendGrid 文档](https://docs.sendgrid.com)
- [SendGrid Node.js SDK](https://github.com/sendgrid/sendgrid-nodejs)
- [Email API v3 参考文档](https://docs.sendgrid.com/api-reference/mail-send/mail-send)