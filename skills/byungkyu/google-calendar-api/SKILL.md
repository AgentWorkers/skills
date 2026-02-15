---
name: google-calendar
description: |
  Google Calendar API integration with managed OAuth. Create events, list calendars, check availability, and manage schedules. Use this skill when users want to interact with Google Calendar. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Google 日历

通过管理的 OAuth 认证来访问 Google 日历 API。您可以创建和管理事件、列出日历以及查看日程安排。

## 快速入门

```bash
# List upcoming events
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events?maxResults=10&orderBy=startTime&singleEvents=true')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-calendar/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google 日历 API 端点路径。该网关会将请求代理到 `www.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-calendar&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-calendar'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-calendar",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Google 日历连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 列出日历

```bash
GET /google-calendar/calendar/v3/users/me/calendarList
```

### 获取日历信息

```bash
GET /google-calendar/calendar/v3/calendars/{calendarId}
```

使用 `primary` 代表用户的默认日历。

### 列出事件

```bash
GET /google-calendar/calendar/v3/calendars/primary/events?maxResults=10&orderBy=startTime&singleEvents=true
```

可以指定时间范围：

```bash
GET /google-calendar/calendar/v3/calendars/primary/events?timeMin=2024-01-01T00:00:00Z&timeMax=2024-12-31T23:59:59Z&singleEvents=true&orderBy=startTime
```

### 获取事件信息

```bash
GET /google-calendar/calendar/v3/calendars/primary/events/{eventId}
```

### 创建事件

```bash
POST /google-calendar/calendar/v3/calendars/primary/events
Content-Type: application/json

{
  "summary": "Team Meeting",
  "description": "Weekly sync",
  "start": {
    "dateTime": "2024-01-15T10:00:00",
    "timeZone": "America/Los_Angeles"
  },
  "end": {
    "dateTime": "2024-01-15T11:00:00",
    "timeZone": "America/Los_Angeles"
  },
  "attendees": [
    {"email": "attendee@example.com"}
  ]
}
```

### 创建全天事件

```bash
POST /google-calendar/calendar/v3/calendars/primary/events
Content-Type: application/json

{
  "summary": "All Day Event",
  "start": {"date": "2024-01-15"},
  "end": {"date": "2024-01-16"}
}
```

### 更新事件

```bash
PUT /google-calendar/calendar/v3/calendars/primary/events/{eventId}
Content-Type: application/json

{
  "summary": "Updated Meeting Title",
  "start": {"dateTime": "2024-01-15T10:00:00Z"},
  "end": {"dateTime": "2024-01-15T11:00:00Z"}
}
```

### 部分更新事件（Patch）

```bash
PATCH /google-calendar/calendar/v3/calendars/primary/events/{eventId}
Content-Type: application/json

{
  "summary": "New Title Only"
}
```

### 删除事件

```bash
DELETE /google-calendar/calendar/v3/calendars/primary/events/{eventId}
```

### 快速添加事件（使用自然语言）

```bash
POST /google-calendar/calendar/v3/calendars/primary/events/quickAdd?text=Meeting+with+John+tomorrow+at+3pm
```

### 查询日程安排（空闲/忙碌）

```bash
POST /google-calendar/calendar/v3/freeBusy
Content-Type: application/json

{
  "timeMin": "2024-01-15T00:00:00Z",
  "timeMax": "2024-01-16T00:00:00Z",
  "items": [{"id": "primary"}]
}
```

## 代码示例

### JavaScript

```javascript
// List events
const response = await fetch(
  'https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events?maxResults=10&singleEvents=true',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

// Create event
await fetch(
  'https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      summary: 'Meeting',
      start: { dateTime: '2024-01-15T10:00:00Z' },
      end: { dateTime: '2024-01-15T11:00:00Z' }
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# List events
events = requests.get(
    'https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events',
    headers=headers,
    params={'maxResults': 10, 'singleEvents': 'true'}
).json()

# Create event
response = requests.post(
    'https://gateway.maton.ai/google-calendar/calendar/v3/calendars/primary/events',
    headers=headers,
    json={
        'summary': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z'},
        'end': {'dateTime': '2024-01-15T11:00:00Z'}
    }
)
```

## 注意事项

- 使用 `primary` 作为用户主日历的标识符（calendarId）。
- 时间必须遵循 RFC3339 格式（例如：`2024-01-15T10:00:00Z`）。
- 对于重复事件，请使用 `singleEvents=true` 以获取所有实例。
- 当使用 `orderBy=startTime` 时，必须设置 `singleEvents=true`。
- 重要提示：在使用 `curl` 命令时，如果 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 以避免全局解析问题。
- 重要提示：在将 `curl` 的输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google 日历连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（10 次/秒） |
| 4xx/5xx | 来自 Google 日历 API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `google-calendar` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/google-calendar/calendars/primary/events`
- 错误的路径：`https://gateway.maton.ai/calendars/primary/events`

## 资源

- [Google 日历 API 概述](https://developers.google.com/calendar/api/v3/reference)
- [列出日历](https://developers.google.com/workspace/calendar/api/v3/reference/calendarList/list)
- [列出事件](https://developers.google.com/workspace/calendar/api/v3/reference/events/list)
- [获取事件信息](https://developers.google.com/workspace/calendar/api/v3/reference/events/get)
- [插入事件](https://developers.google.com/workspace/calendar/api/v3/reference/events/insert)
- [更新事件](https://developers.google.com/workspace/calendar/api/v3/reference/events/update)
- [删除事件](https://developers.google.com/workspace/calendar/api/v3/reference/events/delete)
- [快速添加事件](https://developers.google.com/workspace/calendar/api/v3/reference/events/quickAdd)
- [查询日程安排（空闲/忙碌）](https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)