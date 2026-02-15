---
name: zendesk
description: 通过 Zendesk API 管理支持工单、用户和帮助中心。可以编程方式创建、更新和搜索工单。
metadata: {"clawdbot":{"emoji":"🎫","requires":{"env":["ZENDESK_SUBDOMAIN","ZENDESK_EMAIL","ZENDESK_API_TOKEN"]}}}
---

# Zendesk

客户支持工单管理。

## 环境配置

```bash
export ZENDESK_SUBDOMAIN="yourcompany"
export ZENDESK_EMAIL="admin@company.com"
export ZENDESK_API_TOKEN="xxxxxxxxxx"
```

## 列出工单

```bash
curl "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN"
```

## 创建工单

```bash
curl -X POST "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": {
      "subject": "Help needed",
      "comment": {"body": "I need assistance with..."},
      "priority": "normal",
      "requester": {"name": "John", "email": "john@example.com"}
    }
  }'
```

## 更新工单

```bash
curl -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/{id}.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ticket": {"status": "solved", "comment": {"body": "Issue resolved!"}}}'
```

## 搜索工单

```bash
curl "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/search.json?query=status:open" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN"
```

## 链接
- 管理员入口：https://yourcompany.zendesk.com/admin
- 文档中心：https://developer.zendesk.com/api-reference