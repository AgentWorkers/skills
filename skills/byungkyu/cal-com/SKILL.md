---
name: calcom
description: |
  Cal.com API integration with managed OAuth. Create and manage event types, bookings, schedules, and availability.
  Use this skill when users want to manage scheduling, create bookings, configure event types, or check availability.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Cal.com

您可以使用托管的 OAuth 认证来访问 Cal.com API。该 API 支持创建和管理事件类型、预订、日程安排、日历以及 Webhook。

## 快速入门

```bash
# Get your profile
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/cal-com/v2/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/cal-com/v2/{resource}
```

请将 `{resource}` 替换为 Cal.com API 的端点路径。该网关会将请求代理到 `api.cal.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Cal.com OAuth 连接。

### 列出连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=cal-com&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'cal-com'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "4481afaa-03e4-4b2d-a1c6-7daaf4bff512",
    "status": "ACTIVE",
    "creation_time": "2026-02-12T22:52:17.140998Z",
    "last_updated_time": "2026-02-12T22:55:20.376189Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "cal-com",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Cal.com 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/cal-com/v2/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '4481afaa-03e4-4b2d-a1c6-7daaf4bff512')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户资料

#### 获取用户资料

```bash
GET /cal-com/v2/me
```

**响应：**
```json
{
  "status": "success",
  "data": {
    "id": 2152180,
    "email": "user@example.com",
    "name": "User Name",
    "avatarUrl": "https://...",
    "bio": "",
    "timeFormat": 12,
    "defaultScheduleId": null,
    "weekStart": "Sunday",
    "timeZone": "America/New_York"
  }
}
```

#### 更新用户资料

```bash
PATCH /cal-com/v2/me
Content-Type: application/json

{
  "bio": "Updated bio",
  "name": "New Name"
}
```

### 事件类型

#### 列出事件类型

```bash
GET /cal-com/v2/event-types
```

支持按用户名过滤：

```bash
GET /cal-com/v2/event-types?username={username}
```

**响应：**
```json
{
  "status": "success",
  "data": {
    "eventTypeGroups": [
      {
        "teamId": null,
        "bookerUrl": "https://cal.com",
        "profile": {
          "slug": "username",
          "name": "User Name"
        },
        "eventTypes": [
          {
            "id": 4716831,
            "title": "30 min meeting",
            "slug": "30min",
            "length": 30,
            "hidden": false
          }
        ]
      }
    ]
  }
}
```

#### 获取事件类型信息

```bash
GET /cal-com/v2/event-types/{eventTypeId}
```

#### 创建事件类型

```bash
POST /cal-com/v2/event-types
Content-Type: application/json

{
  "title": "Meeting",
  "slug": "meeting",
  "length": 30
}
```

**必填字段：**
- `title` - 事件类型名称
- `slug` - URL 缩写（必须唯一）
- `length` - 事件持续时间（以分钟为单位）

**响应：**
```json
{
  "status": "success",
  "data": {
    "id": 4745911,
    "title": "Meeting",
    "slug": "meeting",
    "length": 30,
    "locations": [{"type": "integrations:daily"}],
    "hidden": false,
    "userId": 2152180
  }
}
```

#### 更新事件类型

```bash
PATCH /cal-com/v2/event-types/{eventTypeId}
Content-Type: application/json

{
  "title": "Updated Meeting Title",
  "description": "Updated description"
}
```

#### 删除事件类型

```bash
DELETE /cal-com/v2/event-types/{eventTypeId}
```

### 事件类型 Webhook

#### 列出 Webhook

```bash
GET /cal-com/v2/event-types/{eventTypeId}/webhooks
```

#### 创建 Webhook

```bash
POST /cal-com/v2/event-types/{eventTypeId}/webhooks
Content-Type: application/json

{
  "subscriberUrl": "https://example.com/webhook",
  "triggers": ["BOOKING_CREATED"],
  "active": true
}
```

**可用的触发器：**
- `BOOKING_created`
- `BOOKING_RESCHEDULED`
- `BOOKING_CANCELLED`
- `BOOKING-confirmED`
- `BOOKING_REJECTED`
- `BOOKING_REQUESTED`
- `BOOKING_payment_INITIATED`
- `BOOKING_NO_SHOW_UPDATED`
- `MEETING_ENDED`
- `MEETING_STARTED`
- `RECORDING_READY`
- `INSTANT_MEETING`
- `RECORDING_TRANSCRIPTION_GENERATED`

#### 获取 Webhook 信息

```bash
GET /cal-com/v2/event-types/{eventTypeId}/webhooks/{webhookId}
```

#### 更新 Webhook

```bash
PATCH /cal-com/v2/event-types/{eventTypeId}/webhooks/{webhookId}
Content-Type: application/json

{
  "active": false
}
```

#### 删除 Webhook

```bash
DELETE /cal-com/v2/event-types/{eventTypeId}/webhooks/{webhookId}
```

### 预订

#### 列出预订信息

```bash
GET /cal-com/v2/bookings
```

支持过滤：

```bash
GET /cal-com/v2/bookings?status=upcoming
GET /cal-com/v2/bookings?status=past
GET /cal-com/v2/bookings?status=cancelled
GET /cal-com/v2/bookings?status=accepted
GET /cal-com/v2/bookings?take=10
```

**响应：**
```json
{
  "status": "success",
  "data": {
    "bookings": [
      {
        "id": 15893969,
        "uid": "gZJNR7FQG2qLsBqnFdxAPE",
        "title": "30 min meeting between User and Guest",
        "startTime": "2026-02-13T17:00:00.000Z",
        "endTime": "2026-02-13T17:30:00.000Z",
        "status": "ACCEPTED"
      }
    ],
    "totalCount": 1,
    "nextCursor": null
  }
}
```

#### 获取预订信息

```bash
GET /cal-com/v2/bookings/{bookingUid}
```

#### 创建预订

```bash
POST /cal-com/v2/bookings
Content-Type: application/json

{
  "eventTypeId": 4716831,
  "start": "2026-02-13T17:00:00Z",
  "timeZone": "America/New_York",
  "language": "en",
  "responses": {
    "name": "Guest Name",
    "email": "guest@example.com"
  },
  "metadata": {}
}
```

**必填字段：**
- `eventTypeId` - 事件类型的 ID
- `start` - 开始时间（ISO 8601 格式，必须是可用的时间段）
- `timeZone` - 有效的 IANA 时区
- `language` - 语言代码（例如：“en”）
- `responses.name` - 参与者的姓名
- `responses.email` - 参与者的电子邮件

**响应：**
```json
{
  "status": "success",
  "data": {
    "id": 15893969,
    "uid": "gZJNR7FQG2qLsBqnFdxAPE",
    "title": "30 min meeting between User and Guest Name",
    "startTime": "2026-02-13T17:00:00.000Z",
    "endTime": "2026-02-13T17:30:00.000Z",
    "status": "ACCEPTED",
    "location": "integrations:daily"
  }
}
```

#### 取消预订

```bash
POST /cal-com/v2/bookings/{bookingUid}/cancel
Content-Type: application/json

{
  "cancellationReason": "Reason for cancellation"
}
```

### 日程安排

#### 获取默认日程安排

```bash
GET /cal-com/v2/schedules/default
```

#### 获取具体日程安排

```bash
GET /cal-com/v2/schedules/{scheduleId}
```

#### 创建日程安排

```bash
POST /cal-com/v2/schedules
Content-Type: application/json

{
  "name": "Work Hours",
  "timeZone": "America/New_York",
  "isDefault": false
}
```

**响应：**
```json
{
  "status": "success",
  "data": {
    "id": 1243030,
    "name": "Work Hours",
    "isManaged": false,
    "workingHours": [
      {
        "days": [1, 2, 3, 4, 5],
        "startTime": 540,
        "endTime": 1020
      }
    ]
  }
}
```

#### 更新日程安排

```bash
PATCH /cal-com/v2/schedules/{scheduleId}
Content-Type: application/json

{
  "name": "Updated Schedule Name"
}
```

#### 删除日程安排

```bash
DELETE /cal-com/v2/schedules/{scheduleId}
```

### 可用时间段

#### 获取可用时间段

```bash
GET /cal-com/v2/slots/available?eventTypeId={eventTypeId}&startTime={startTime}&endTime={endTime}
```

**参数：**
- `eventTypeId` - 必填。事件类型的 ID
- `startTime` - 范围的开始时间（ISO 8601 格式）
- `endTime` - 范围的结束时间（ISO 8601 格式）

**响应：**
```json
{
  "status": "success",
  "data": {
    "slots": {
      "2026-02-13": [
        {"time": "2026-02-13T17:00:00.000Z"},
        {"time": "2026-02-13T17:30:00.000Z"},
        {"time": "2026-02-13T18:00:00.000Z"}
      ],
      "2026-02-14": [
        {"time": "2026-02-14T14:00:00.000Z"}
      ]
    }
  }
}
```

#### 预订时间段

```bash
POST /cal-com/v2/slots/reserve
Content-Type: application/json

{
  "eventTypeId": 4716831,
  "slotUtcStartDate": "2026-02-20T14:00:00Z",
  "slotUtcEndDate": "2026-02-20T14:30:00Z"
}
```

**响应：**
```json
{
  "status": "success",
  "data": "968ed924-83fb-4da7-969e-eaa621643535"
}
```

### 日历

#### 列出关联的日历

```bash
GET /cal-com/v2/calendars
```

**响应：**
```json
{
  "status": "success",
  "data": {
    "connectedCalendars": [
      {
        "integration": {
          "name": "Google Calendar",
          "type": "google_calendar"
        },
        "calendars": [...]
      }
    ]
  }
}
```

### 会议

#### 列出可用的会议应用程序

```bash
GET /cal-com/v2/conferencing
```

**响应：**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1769268,
      "type": "google_video",
      "appId": "google-meet"
    }
  ]
}
```

#### 获取默认会议应用程序

```bash
GET /cal-com/v2/conferencing/default
```

### Webhook（用户级别）

#### 列出 Webhook

```bash
GET /cal-com/v2/webhooks
```

#### 创建 Webhook

```bash
POST /cal-com/v2/webhooks
Content-Type: application/json

{
  "subscriberUrl": "https://example.com/webhook",
  "triggers": ["BOOKING_CREATED"],
  "active": true
}
```

#### 获取 Webhook 信息

```bash
GET /cal-com/v2/webhooks/{webhookId}
```

#### 更新 Webhook

```bash
PATCH /cal-com/v2/webhooks/{webhookId}
Content-Type: application/json

{
  "active": false
}
```

#### 删除 Webhook

```bash
DELETE /cal-com/v2/webhooks/{webhookId}
```

### 团队

#### 列出团队信息

```bash
GET /cal-com/v2/teams
```

### 验证过的资源

#### 列出已验证的电子邮件地址

```bash
GET /cal-com/v2/verified-resources/emails
```

## 分页

预订信息支持基于游标的分页，使用 `take` 和 `nextCursor`：

```bash
GET /cal-com/v2/bookings?take=10
```

响应中包含分页信息：

```json
{
  "data": {
    "bookings": [...],
    "totalCount": 25,
    "nextCursor": "abc123"
  }
}
```

要查看下一页：

```bash
GET /cal-com/v2/bookings?take=10&cursor=abc123
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/cal-com/v2/event-types',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/cal-com/v2/event-types',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 除非指定了时区，否则所有时间均以 UTC 为准。
- 事件类型中的 `length` 字段以分钟为单位。
- 创建预订前需要检查是否有可用的时间段（请先调用 `/v2/slots/available`）。
- 日程安排的工作时间从午夜开始计算（例如：540 表示上午 9:00，1020 表示下午 5:00）。
- 日程安排中的天数：0 表示星期日，1 表示星期一，依此类推。
- `GET /v2/schedules` 端点可能会返回 500 错误；请改用 `GET /v2/schedules/{id}`。
- 重要提示：当使用 curl 命令时，如果 URL 中包含括号，请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 curl 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立与 Cal.com 的连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 409 | 资源冲突（重复的资源） |
| 429 | 使用频率受限 |
| 500 | Cal.com API 出现错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `cal-com` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/cal-com/v2/me`
- 错误的格式：`https://gateway.maton.ai/v2/me`

### 故障排除：创建预订失败

1. 在创建预订前检查是否有可用的时间段：
```bash
GET /cal-com/v2/slots/available?eventTypeId={id}&startTime=...&endTime=...
```

2. 确保提供了所有必填字段：
   - `eventTypeId`
   - `start`（必须与可用的时间段匹配）
   - `timeZone`
   - `language`
   - `responses.name`
   - `responses.email`

## 资源

- [Cal.com API 文档](https://cal.com/docs/api-reference/v2/introduction)
- [Cal.com API 参考](https://cal.com/docs/api-reference/v2)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)