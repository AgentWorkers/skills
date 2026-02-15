---
name: mailchimp
description: 通过 Mailchimp API 管理电子邮件营销活动、受众群体以及自动化流程。
metadata: {"clawdbot":{"emoji":"🐵","requires":{"env":["MAILCHIMP_API_KEY","MAILCHIMP_SERVER"]}}}
---

# Mailchimp

电子邮件营销自动化工具。

## 环境配置

```bash
export MAILCHIMP_API_KEY="xxxxxxxxxx-us1"
export MAILCHIMP_SERVER="us1"  # From API key suffix
```

## 列表管理（List Audiences）

```bash
curl "https://$MAILCHIMP_SERVER.api.mailchimp.com/3.0/lists" \
  -u "anystring:$MAILCHIMP_API_KEY"
```

## 添加订阅者（Add Subscriber）

```bash
curl -X POST "https://$MAILCHIMP_SERVER.api.mailchimp.com/3.0/lists/{list_id}/members" \
  -u "anystring:$MAILCHIMP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email_address": "user@example.com",
    "status": "subscribed",
    "merge_fields": {"FNAME": "John", "LNAME": "Doe"}
  }'
```

## 创建营销活动（Create Campaigns）

```bash
curl "https://$MAILCHIMP_SERVER.api.mailchimp.com/3.0/campaigns" \
  -u "anystring:$MAILCHIMP_API_KEY"
```

## 查看营销活动统计（Get Campaign Stats）

```bash
curl "https://$MAILCHIMP_SERVER.api.mailchimp.com/3.0/reports/{campaign_id}" \
  -u "anystring:$MAILCHIMP_API_KEY"
```

## 发送营销邮件（Send Campaign）

```bash
curl -X POST "https://$MAILCHIMP_SERVER.api.mailchimp.com/3.0/campaigns/{campaign_id}/actions/send" \
  -u "anystring:$MAILCHIMP_API_KEY"
```

## 链接：
- 仪表板：https://mailchimp.com
- 文档：https://mailchimp.com/developer/