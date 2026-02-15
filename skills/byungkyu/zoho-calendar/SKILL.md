---
name: zoho-calendar
description: |
  Zoho Calendar API integration with managed OAuth. Manage calendars and events with full scheduling capabilities.
  Use this skill when users want to read, create, update, or delete calendar events, manage calendars, or schedule meetings.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Zoho 日历

通过管理的 OAuth 认证来访问 Zoho 日历 API。您可以执行完整的 CRUD 操作（创建、读取、更新和删除）来管理日历和事件，包括重复事件和参与者管理。

## 快速入门

```bash
# List calendars
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-calendar/api/v1/calendars')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-calendar/api/v1/{endpoint}
```

该网关会将请求代理到 `calendar.zoho.com/api/v1`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Zoho 日历 OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-calendar&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-calendar'}).encode()
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
    "app": "zoho-calendar",
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

如果您有多个 Zoho 日历连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-calendar/api/v1/calendars')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 日历

#### 列出日历

```bash
GET /zoho-calendar/api/v1/calendars
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-calendar/api/v1/calendars')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "calendars": [
    {
      "uid": "fda9b0b4ad834257b622cb3dc3555727",
      "name": "My Calendar",
      "color": "#8cbf40",
      "textcolor": "#FFFFFF",
      "timezone": "PST",
      "isdefault": true,
      "category": "own",
      "privilege": "owner"
    }
  ]
}
```

#### 获取日历详情

```bash
GET /zoho-calendar/api/v1/calendars/{calendar_uid}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-calendar/api/v1/calendars/fda9b0b4ad834257b622cb3dc3555727')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建日历

```bash
POST /zoho-calendar/api/v1/calendars?calendarData={json}
```

**必填字段：**
- `name` - 日历名称（最多 50 个字符）
- `color` - 十六进制颜色代码（例如：`#FF5733`）

**可选字段：**
- `textcolor` - 文本颜色十六进制代码
- `description` - 日历描述（最多 1000 个字符）
- `timezone` - 日历时区
- `include_infreebusy` - 是否显示为忙碌/空闲（布尔值）
- `public` - 可见性级别（`disable`、`freebusy` 或 `view`）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json, urllib.parse

calendarData = {
    "name": "Work Calendar",
    "color": "#FF5733",
    "textcolor": "#FFFFFF",
    "description": "My work calendar"
}

url = f'https://gateway.maton.ai/zoho-calendar/api/v1/calendars?calendarData={urllib.parse.quote(json.dumps(calendarData))}'
req = urllib.request.Request(url, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "calendars": [
    {
      "uid": "86fb9745076e4672ae4324f05e1f5393",
      "name": "Work Calendar",
      "color": "#FF5733",
      "textcolor": "#FFFFFF"
    }
  ]
}
```

#### 删除日历

```bash
DELETE /zoho-calendar/api/v1/calendars/{calendar_uid}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-calendar/api/v1/calendars/86fb9745076e4672ae4324f05e1f5393', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "calendars": [
    {
      "uid": "86fb9745076e4672ae4324f05e1f5393",
      "calstatus": "deleted"
    }
  ]
}
```

### 事件

#### 列出事件

```bash
GET /zoho-calendar/api/v1/calendars/{calendar_uid}/events?range={json}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `range` | JSON 对象 | **必填。** 开始和结束日期，格式为 `{"start":"yyyyMMdd","end":"yyyyMMdd"`。最多支持 31 天的时间范围。 |
| `byinstance` | 布尔值 | 如果为 `true`，则重复事件会分别返回 |
| `timezone` | 字符串 | 日期时间的时区 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json, urllib.parse
from datetime import datetime, timedelta

today = datetime.now()
end_date = today + timedelta(days=7)
range_param = json.dumps({
    "start": today.strftime("%Y%m%d"),
    "end": end_date.strftime("%Y%m%d")
})

url = f'https://gateway.maton.ai/zoho-calendar/api/v1/calendars/fda9b0b4ad834257b622cb3dc3555727/events?range={urllib.parse.quote(range_param)}'
req = urllib.request.Request(url)
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "events": [
    {
      "uid": "c63e8b9fcb3e48c2a00b16729932d636@zoho.com",
      "title": "Team Meeting",
      "dateandtime": {
        "timezone": "America/Los_Angeles",
        "start": "20260206T100000-0800",
        "end": "20260206T110000-0800"
      },
      "isallday": false,
      "etag": "1770368451507",
      "organizer": "user@example.com"
    }
  ]
}
```

#### 获取事件详情

```bash
GET /zoho-calendar/api/v1/calendars/{calendar_uid}/events/{event_uid}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-calendar/api/v1/calendars/fda9b0b4ad834257b622cb3dc3555727/events/c63e8b9fcb3e48c2a00b16729932d636@zoho.com')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建事件

```bash
POST /zoho-calendar/api/v1/calendars/{calendar_uid}/events?eventdata={json}
```

**必填字段（在 eventdata 中）：**
- `dateandtime` - 包含 `start`、`end` 的对象，可选 `timezone`：
  - 对于定时事件，格式为 `yyyyMMdd'T'HHmmss'Z'`（GMT）。
  - 对于全天事件，格式为 `yyyyMMdd`。

**可选字段：**
- `title` - 事件名称
- `description` - 事件详情（最多 10,000 个字符）
- `location` - 事件地点（最多 255 个字符）
- `isallday` - 全天事件的布尔值
- `isprivate` - 是否向非参与者隐藏详情的布尔值
- `color` - 十六进制颜色代码
- `attendees` - 参与者对象数组
- `reminders` - 提醒对象数组
- `rrule` - 重复规则字符串（例如：`FREQ=DAILY;COUNT=5`）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json, urllib.parse
from datetime import datetime, timedelta

start_time = datetime.utcnow() + timedelta(hours=1)
end_time = start_time + timedelta(hours=1)

eventdata = {
    "title": "Team Meeting",
    "dateandtime": {
        "timezone": "America/Los_Angeles",
        "start": start_time.strftime("%Y%m%dT%H%M%SZ"),
        "end": end_time.strftime("%Y%m%dT%H%M%SZ")
    },
    "description": "Weekly team sync",
    "location": "Conference Room A"
}

url = f'https://gateway.maton.ai/zoho-calendar/api/v1/calendars/fda9b0b4ad834257b622cb3dc3555727/events?eventdata={urllib.parse.quote(json.dumps(eventdata))}'
req = urllib.request.Request(url, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "events": [
    {
      "uid": "c63e8b9fcb3e48c2a00b16729932d636@zoho.com",
      "title": "Team Meeting",
      "dateandtime": {
        "timezone": "America/Los_Angeles",
        "start": "20260206T100000-0800",
        "end": "20260206T110000-0800"
      },
      "etag": "1770368451507",
      "estatus": "added"
    }
  ]
}
```

#### 更新事件

```bash
PUT /zoho-calendar/api/v1/calendars/{calendar_uid}/events/{event_uid}?eventdata={json}
```

**必填字段：**
- `dateandtime` - 开始和结束时间
- `etag` - 事件的当前 etag 值（来自获取事件详情）

**可选字段：** 与创建事件相同

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json, urllib.parse
from datetime import datetime, timedelta

start_time = datetime.utcnow() + timedelta(hours=2)
end_time = start_time + timedelta(hours=1)

eventdata = {
    "title": "Updated Team Meeting",
    "dateandtime": {
        "timezone": "America/Los_Angeles",
        "start": start_time.strftime("%Y%m%dT%H%M%SZ"),
        "end": end_time.strftime("%Y%m%dT%H%M%SZ")
    },
    "etag": 1770368451507
}

url = f'https://gateway.maton.ai/zoho-calendar/api/v1/calendars/fda9b0b4ad834257b622cb3dc3555727/events/c63e8b9fcb3e48c2a00b16729932d636@zoho.com?eventdata={urllib.parse.quote(json.dumps(eventdata))}'
req = urllib.request.Request(url, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 删除事件

```bash
DELETE /zoho-calendar/api/v1/calendars/{calendar_uid}/events/{event_uid}
```

**必填头部：**
- `etag` - 事件的当前 etag 值

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json

req = urllib.request.Request('https://gateway.maton.ai/zoho-calendar/api/v1/calendars/fda9b0b4ad834257b622cb3dc3555727/events/c63e8b9fcb3e48c2a00b16729932d636@zoho.com', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('etag', '1770368451507')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "events": [
    {
      "uid": "c63e8b9fcb3e48c2a00b16729932d636@zoho.com",
      "estatus": "deleted",
      "caluid": "fda9b0b4ad834257b622cb3dc3555727"
    }
  ]
}
```

### 参与者

在创建或更新事件时，需要包含参与者信息：

```json
{
  "attendees": [
    {
      "email": "user@example.com",
      "permission": 1,
      "attendance": 1
    }
  ]
}
```

**权限级别：** 0（访客）、1（查看）、2（邀请）、3（编辑）
**出席情况：** 0（非参与者）、1（必填）、2（可选）

### 提醒

```json
{
  "reminders": [
    {
      "action": "popup",
      "minutes": 30
    },
    {
      "action": "email",
      "minutes": 60
    }
  ]
}
```

**操作：** `email`、`popup`、`notification`

### 重复事件

使用 iCalendar 的 RRULE 格式设置 `rrule` 字段：

```json
{
  "rrule": "FREQ=DAILY;COUNT=5;INTERVAL=1"
}
```

**示例：**
- 每天重复 5 次：`FREQ=DAILY;COUNT=5;INTERVAL=1`
- 每周一/周二重复：`FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU;UNTIL=20250817T064600Z`
- 每月最后一个周二重复：`FREQ=MONTHLY;INTERVAL=1;BYDAY=TU;BYSETPOS=-1;COUNT=2`

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-calendar/api/v1/calendars',
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
    'https://gateway.maton.ai/zoho-calendar/api/v1/calendars',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 事件和日历数据以 JSON 格式通过 `eventdata` 或 `calendarData` 查询参数传递。
- 事件的日期/时间格式为 `yyyyMMdd'T'HHmmss'Z'`（GMT）或全天事件的 `yyyyMMdd`。
- 列出事件的 `range` 参数不能超过 31 天。
- 更新和删除操作需要 `etag` — 在修改之前务必获取最新的 etag 值。
- 对于删除操作，`etag` 必须作为头部参数传递，而不是查询参数。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 以禁用全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少 Zoho 日历连接、缺少必填参数或请求无效 |
| 401 | Maton API 密钥无效或缺失，或者 OAuth 范围不匹配 |
| 404 | 资源未找到 |
| 429 | 请求速率限制 |
| 4xx/5xx | 来自 Zoho 日历 API 的传递错误 |

### 常见错误

| 错误 | 描述 |
|-------|-------------|
| `ETAG_MISSING` | 删除操作需要 `etag` 头部 |
| `EXTRA_PARAM_FOUND` | 请求中包含无效参数 |
| `INVALID_DATA` | 请求数据格式错误 |

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

1. 确保您的 URL 路径以 `zoho-calendar` 开头。例如：
- 正确：`https://gateway.maton.ai/zoho-calendar/api/v1/calendars`
- 错误：`https://gateway.maton.ai/api/v1/calendars`

## 资源

- [Zoho 日历 API 介绍](https://www.zoho.com/calendar/help/api/introduction.html)
- [Zoho 日历事件 API](https://www.zoho.com/calendar/help/api/events-api.html)
- [Zoho 日历日历 API](https://www.zoho.com/calendar/help/api/calendars-api.html)
- [创建事件](https://www.zoho.com/calendar/help/api/post-create-event.html)
- [获取事件列表](https://www.zoho.com/calendar/help/api/get-events-list.html)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)