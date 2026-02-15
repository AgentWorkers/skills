---
name: freshdesk
description: 通过 Freshdesk API 管理支持工单、联系人和知识库。创建、更新并解决客户问题。
metadata: {"clawdbot":{"emoji":"🎧","requires":{"env":["FRESHDESK_DOMAIN","FRESHDESK_API_KEY"]}}}
---

# Freshdesk

这是一个客户支持平台。

## 环境配置

```bash
export FRESHDESK_DOMAIN="yourcompany"  # yourcompany.freshdesk.com
export FRESHDESK_API_KEY="xxxxxxxxxx"
```

## 列出工单

```bash
curl "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets" \
  -u "$FRESHDESK_API_KEY:X"
```

## 获取工单

```bash
curl "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets/{id}" \
  -u "$FRESHDESK_API_KEY:X"
```

## 创建工单

```bash
curl -X POST "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets" \
  -u "$FRESHDESK_API_KEY:X" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Support needed",
    "description": "I need help with...",
    "email": "customer@example.com",
    "priority": 2,
    "status": 2
  }'
```

## 更新工单

```bash
curl -X PUT "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets/{id}" \
  -u "$FRESHDESK_API_KEY:X" \
  -H "Content-Type: application/json" \
  -d '{"status": 4, "priority": 3}'
```

## 回复工单

```bash
curl -X POST "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets/{id}/reply" \
  -u "$FRESHDESK_API_KEY:X" \
  -H "Content-Type: application/json" \
  -d '{"body": "Thanks for reaching out! Here is your solution..."}'
```

## 列出联系人

```bash
curl "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/contacts" \
  -u "$FRESHDESK_API_KEY:X"
```

## 搜索工单

```bash
curl "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/search/tickets?query=\"status:2\"" \
  -u "$FRESHDESK_API_KEY:X"
```

## 优先级/状态值
- 优先级：1=低，2=中等，3=高，4=紧急
- 状态：2=未解决，3=待处理，4=已解决，5=已关闭

## 链接
- 仪表板：https://yourcompany.freshdesk.com
- 文档：https://developers.freshdesk.com