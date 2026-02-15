---
name: sendgrid
description: 通过 SendGrid API 发送交易相关的邮件和营销邮件。支持使用模板、附件以及进行邮件分析。
metadata: {"clawdbot":{"emoji":"📧","requires":{"env":["SENDGRID_API_KEY"]}}}
---

# SendGrid

用于大规模发送电子邮件。

## 环境配置

```bash
export SENDGRID_API_KEY="SG.xxxxxxxxxx"
```

## 发送电子邮件

```bash
curl -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{"to": [{"email": "recipient@example.com"}]}],
    "from": {"email": "sender@example.com"},
    "subject": "Hello",
    "content": [{"type": "text/plain", "value": "Hello World!"}]
  }'
```

## 使用模板发送邮件

```bash
curl -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{
      "to": [{"email": "recipient@example.com"}],
      "dynamic_template_data": {"name": "John", "order_id": "12345"}
    }],
    "from": {"email": "sender@example.com"},
    "template_id": "d-xxxxxxxxxxxx"
  }'
```

## 模板列表

```bash
curl "https://api.sendgrid.com/v3/templates?generations=dynamic" \
  -H "Authorization: Bearer $SENDGRID_API_KEY"
```

## 获取邮件统计信息

```bash
curl "https://api.sendgrid.com/v3/stats?start_date=2024-01-01" \
  -H "Authorization: Bearer $SENDGRID_API_KEY"
```

## 链接
- 控制台：https://app.sendgrid.com
- 文档：https://docs.sendgrid.com