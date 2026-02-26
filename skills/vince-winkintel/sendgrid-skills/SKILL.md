---
name: sendgrid
description: SendGrid 是一个用于发送和接收电子邮件的平台。该平台提供了相应的子技能（sub-skills），用于处理出站交易性邮件（send-email）以及通过 Inbound Parse Webhook 接收邮件（sendgrid-inbound）。当用户提到 SendGrid、交易性邮件（transactional email）、电子邮件 API（email API）、电子邮件解析（email parsing）或电子邮件 Webhook（email webhook）时，应使用相关功能。相关的触发事件包括：SendGrid 的操作、发送邮件（send email）、接收邮件（receive email）、电子邮件 Webhook（email webhook）、Inbound Parse（Inbound Parse），以及交易性邮件（transactional email）。
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
metadata:
  openclaw:
    requires:
      env:
        - SENDGRID_API_KEY
      bins:
        - curl
        - jq
        - node
    notes: |
      Scripts operate on user-provided file paths (send-html-email.sh) and network endpoints (verify-inbound-setup.sh). Review scripts before executing. Use a SendGrid API key scoped to Mail Send only.
---
# SendGrid

## 概述

SendGrid 是一个专为开发者设计的电子邮件平台。本技能会引导您了解与该平台相关的具体功能。

## 子技能

| 功能 | 技能名称 | 使用场景 |
|---------|-------|----------|
| **发送电子邮件** | `send-email` | 用于发送交易型电子邮件、通知邮件、简单邮件以及使用动态模板 |
| **接收电子邮件** | `sendgrid-inbound` | 处理入站邮件、设置 MX 记录以及解析接收到的电子邮件 |

## 常见设置

### API 密钥

将 API 密钥存储在环境变量中：
```bash
export SENDGRID_API_KEY=SG.xxxxxxxxx
```

### SDK 安装

有关安装说明，请参阅 `send-email` 技能文档（涵盖所有支持的语言）。

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