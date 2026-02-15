---
name: cal-com
description: 管理 Cal.com 的日程安排功能：可以查看预订信息、事件类型以及可用时间。当您需要查看日程表、管理预订链接，或通过 Cal.com 的 API 自动安排会议时，请使用此功能。
---

# Cal.com API

通过 Cal.com API 管理日程安排和预订。

## 设置

1. 获取 API 密钥：访问 Cal.com → 设置 → 开发者 → API 密钥
2. 存储密钥：
```bash
mkdir -p ~/.config/calcom
echo "cal_live_XXXXX" > ~/.config/calcom/api_key
```

## API 基础知识

```bash
CAL_KEY=$(cat ~/.config/calcom/api_key)
CAL_URL="https://api.cal.com/v1"  # or self-hosted URL

curl -s "${CAL_URL}/me?apiKey=${CAL_KEY}" | jq
```

## 列出事件类型

```bash
curl -s "${CAL_URL}/event-types?apiKey=${CAL_KEY}" | jq '.event_types[] | {id, title, slug, length}'
```

## 获取事件类型

```bash
EVENT_TYPE_ID="123"

curl -s "${CAL_URL}/event-types/${EVENT_TYPE_ID}?apiKey=${CAL_KEY}" | jq
```

## 列出预订信息

```bash
curl -s "${CAL_URL}/bookings?apiKey=${CAL_KEY}" | jq '.bookings[] | {id, title, startTime, endTime, status}'
```

## 获取预订详情

```bash
BOOKING_ID="123"

curl -s "${CAL_URL}/bookings/${BOOKING_ID}?apiKey=${CAL_KEY}" | jq
```

## 按状态筛选预订

```bash
# upcoming, past, cancelled, recurring
curl -s "${CAL_URL}/bookings?apiKey=${CAL_KEY}&status=upcoming" | jq '.bookings'
```

## 创建预订

```bash
curl -s -X POST "${CAL_URL}/bookings?apiKey=${CAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "eventTypeId": 123,
    "start": "2024-01-15T10:00:00.000Z",
    "end": "2024-01-15T10:30:00.000Z",
    "responses": {
      "name": "John Doe",
      "email": "john@example.com",
      "notes": "Looking forward to our meeting"
    },
    "timeZone": "Europe/Paris",
    "language": "en"
  }' | jq
```

## 取消预订

```bash
curl -s -X DELETE "${CAL_URL}/bookings/${BOOKING_ID}?apiKey=${CAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"cancellationReason": "Schedule conflict"}' | jq
```

## 重新安排预订

```bash
curl -s -X PATCH "${CAL_URL}/bookings/${BOOKING_ID}?apiKey=${CAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "start": "2024-01-16T14:00:00.000Z",
    "end": "2024-01-16T14:30:00.000Z"
  }' | jq
```

## 列出可用时间

```bash
curl -s "${CAL_URL}/availability?apiKey=${CAL_KEY}&eventTypeId=123&dateFrom=2024-01-15&dateTo=2024-01-22" | jq
```

## 获取可用时间段

```bash
curl -s "${CAL_URL}/slots?apiKey=${CAL_KEY}&eventTypeId=123&startTime=2024-01-15&endTime=2024-01-22&timeZone=Europe/Paris" | jq '.slots'
```

## 列出日程安排

```bash
curl -s "${CAL_URL}/schedules?apiKey=${CAL_KEY}" | jq '.schedules[] | {id, name, timeZone}'
```

## Webhook

- **列出 Webhook 事件**：
```bash
curl -s "${CAL_URL}/webhooks?apiKey=${CAL_KEY}" | jq
```

- **创建 Webhook**：
```bash
curl -s -X POST "${CAL_URL}/webhooks?apiKey=${CAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "subscriberUrl": "https://example.com/webhook",
    "eventTriggers": ["BOOKING_CREATED", "BOOKING_CANCELLED"],
    "active": true
  }' | jq
```

## 事件触发器

- `BOOKING CREATED`（预订创建）
- `BOOKING_CANCELLED`（预订取消）
- `BOOKING_RESCHEDULED`（预订重新安排）
- `BOOKING_CONFIRMED`（预订确认）
- `BOOKING_REJECTED`（预订被拒绝）

## 自托管环境

对于自托管的 Cal.com 系统，需要更改基础 URL：
```bash
CAL_URL="https://your-cal-instance.com/api/v1"
```

## 速率限制

- **默认设置**：无公开的速率限制（请合理使用 API）
- **自托管环境**：具体限制取决于您的基础设施配置