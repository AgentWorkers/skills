---
name: postmark
description: 通过 Postmark API 发送具有高送达率的交易性电子邮件。管理邮件模板、跟踪邮件退回情况，并查看分析数据。
metadata: {"clawdbot":{"emoji":"📮","requires":{"env":["POSTMARK_SERVER_TOKEN"]}}}
---

# Postmark

用于发送事务性（即需要确认收件人已阅读的）电子邮件。

## 环境配置

```bash
export POSTMARK_SERVER_TOKEN="xxxxxxxxxx"
```

## 发送电子邮件

```bash
curl -X POST "https://api.postmarkapp.com/email" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "From": "sender@example.com",
    "To": "recipient@example.com",
    "Subject": "Hello",
    "TextBody": "Hello from Postmark!",
    "HtmlBody": "<p>Hello from Postmark!</p>"
  }'
```

## 使用模板发送邮件

```bash
curl -X POST "https://api.postmarkapp.com/email/withTemplate" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "From": "sender@example.com",
    "To": "recipient@example.com",
    "TemplateId": 12345,
    "TemplateModel": {"name": "John", "product": "Widget"}
  }'
```

## 批量发送邮件

```bash
curl -X POST "https://api.postmarkapp.com/email/batch" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {"From": "sender@example.com", "To": "user1@example.com", "Subject": "Hi", "TextBody": "Hello 1"},
    {"From": "sender@example.com", "To": "user2@example.com", "Subject": "Hi", "TextBody": "Hello 2"}
  ]'
```

## 模板列表

```bash
curl "https://api.postmarkapp.com/templates" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN"
```

## 获取邮件退回统计信息

```bash
curl "https://api.postmarkapp.com/bounces" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN"
```

## 获取邮件发送统计信息

```bash
curl "https://api.postmarkapp.com/deliverystats" \
  -H "X-Postmark-Server-Token: $POSTMARK_SERVER_TOKEN"
```

## 链接：
- 仪表板：https://account.postmarkapp.com
- 文档：https://postmarkapp.com/developer