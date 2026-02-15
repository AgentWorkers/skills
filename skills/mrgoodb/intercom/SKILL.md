---
name: intercom
description: 通过 Intercom API 管理客户对话、联系信息以及帮助文档。发送消息并管理支持工单（即客户咨询的收件箱）。
metadata: {"clawdbot":{"emoji":"💬","requires":{"env":["INTERCOM_ACCESS_TOKEN"]}}}
---

# Intercom

这是一个客户消息传递平台。

## 环境配置

```bash
export INTERCOM_ACCESS_TOKEN="dG9rOxxxxxxxxxx"
```

## 列出联系人

```bash
curl "https://api.intercom.io/contacts" \
  -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## 搜索联系人

```bash
curl -X POST "https://api.intercom.io/contacts/search" \
  -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": {"field": "email", "operator": "=", "value": "user@example.com"}}'
```

## 创建联系人

```bash
curl -X POST "https://api.intercom.io/contacts" \
  -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "email": "user@example.com", "name": "John Doe"}'
```

## 发送消息

```bash
curl -X POST "https://api.intercom.io/messages" \
  -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message_type": "inapp",
    "body": "Hey! How can I help?",
    "from": {"type": "admin", "id": "ADMIN_ID"},
    "to": {"type": "user", "id": "USER_ID"}
  }'
```

## 查看对话记录

```bash
curl "https://api.intercom.io/conversations" \
  -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN"
```

## 回复对话

```bash
curl -X POST "https://api.intercom.io/conversations/{id}/reply" \
  -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message_type": "comment", "type": "admin", "admin_id": "ADMIN_ID", "body": "Thanks for reaching out!"}'
```

## 链接：
- 仪表板：https://app.intercom.com
- 文档：https://developers.intercom.com