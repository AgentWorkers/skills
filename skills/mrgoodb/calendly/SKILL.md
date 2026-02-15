---
name: calendly
description: 管理 Calendly 的日程安排：列出事件、预订信息以及用户的可用时间。能够通过编程方式生成用于日程安排的链接。
metadata: {"clawdbot":{"emoji":"📅","requires":{"env":["CALENDLY_API_TOKEN"]}}}
---

# Calendly

用于实现日程安排的自动化功能。

## 环境配置

```bash
export CALENDLY_API_TOKEN="xxxxxxxxxx"
```

## 获取当前用户信息

```bash
curl "https://api.calendly.com/users/me" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

## 列出事件类型

```bash
curl "https://api.calendly.com/event_types?user=https://api.calendly.com/users/USERID" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

## 列出已安排的事件

```bash
curl "https://api.calendly.com/scheduled_events?user=https://api.calendly.com/users/USERID&status=active" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

## 获取事件详情

```bash
curl "https://api.calendly.com/scheduled_events/{uuid}" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

## 列出受邀参与者

```bash
curl "https://api.calendly.com/scheduled_events/{event_uuid}/invitees" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

## 取消事件

```bash
curl -X POST "https://api.calendly.com/scheduled_events/{uuid}/cancellation" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason": "Scheduling conflict"}'
```

## 链接：
- 仪表盘：https://calendly.com/app/home
- 文档：https://developer.calendly.com