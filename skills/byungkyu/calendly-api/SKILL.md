---
name: calendly
description: |
  Calendly API integration with managed OAuth. Access event types, scheduled events, invitees, availability, and manage webhooks. Use this skill when users want to view scheduling data, check availability, book meetings, or integrate with Calendly workflows. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Calendly

您可以使用管理的 OAuth 认证来访问 Calendly API。该 API 允许您检索事件类型、已安排的事件、受邀者信息、可用时间数据，并管理用于自动化日程安排的 Webhook 订阅。

## 快速入门

```bash
# Get current user
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/calendly/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Calendly API 端点路径。Gateway 会将请求代理到 `api.calendly.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 管理您的 Calendly OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=calendly&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'calendly'}).encode()
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
    "app": "calendly",
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

如果您有多个 Calendly 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，Gateway 将使用默认的（最旧的）活动连接。

## API 参考

### 用户

#### 获取当前用户

```bash
GET /calendly/users/me
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "resource": {
    "uri": "https://api.calendly.com/users/AAAAAAAAAAAAAAAA",
    "name": "Alice Johnson",
    "slug": "alice-johnson",
    "email": "alice.johnson@acme.com",
    "scheduling_url": "https://calendly.com/alice-johnson",
    "timezone": "America/New_York",
    "avatar_url": "https://example.com/avatar.png",
    "created_at": "2024-01-15T10:30:00.000000Z",
    "updated_at": "2025-06-20T14:45:00.000000Z",
    "current_organization": "https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB"
  }
}
```

#### 获取用户信息

```bash
GET /calendly/users/{uuid}
```

### 事件类型

#### 列出事件类型

```bash
GET /calendly/event_types
```

查询参数：
- `user` - 用于过滤事件类型的用户 URI
- `organization` - 用于过滤事件类型的组织 URI
- `active` - 按活动状态过滤（true/false）
- `count` - 返回的结果数量（默认 20，最大 100）
- `page_token` - 分页令牌
- `sort` - 排序方式（例如，`name:asc`，`created_at:desc`）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/event_types?user=https://api.calendly.com/users/AAAAAAAAAAAAAAAA&active=true')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "collection": [
    {
      "uri": "https://api.calendly.com/event_types/CCCCCCCCCCCCCCCC",
      "name": "30 Minute Meeting",
      "active": true,
      "slug": "30min",
      "scheduling_url": "https://calendly.com/alice-johnson/30min",
      "duration": 30,
      "kind": "solo",
      "type": "StandardEventType",
      "color": "#0066FF",
      "created_at": "2024-02-01T09:00:00.000000Z",
      "updated_at": "2025-05-15T11:30:00.000000Z",
      "description_plain": "A quick 30-minute catch-up call",
      "description_html": "<p>A quick 30-minute catch-up call</p>",
      "profile": {
        "type": "User",
        "name": "Alice Johnson",
        "owner": "https://api.calendly.com/users/AAAAAAAAAAAAAAAA"
      }
    }
  ],
  "pagination": {
    "count": 1,
    "next_page_token": null
  }
}
```

#### 获取事件类型详细信息

```bash
GET /calendly/event_types/{uuid}
```

### 已安排的事件

#### 列出已安排的事件

```bash
GET /calendly/scheduled_events
```

查询参数：
- `user` - 用于过滤事件的用户 URI
- `organization` - 用于过滤事件的组织 URI
- `invitee_email` - 用于过滤受邀者的电子邮件
- `status` - 按状态过滤（`active`，`canceled`）
- `min_start_time` - 过滤在此时间之后开始的事件（ISO 8601 格式）
- `max_start_time` - 过滤在此时间之前开始的事件（ISO 8601 格式）
- `count` - 返回的结果数量（默认 20，最大 100）
- `page_token` - 分页令牌
- `sort` - 排序方式（例如，`start_time:asc`）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/scheduled_events?user=https://api.calendly.com/users/AAAAAAAAAAAAAAAA&status=active&min_start_time=2025-03-01T00:00:00Z')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "collection": [
    {
      "uri": "https://api.calendly.com/scheduled_events/DDDDDDDDDDDDDDDD",
      "name": "30 Minute Meeting",
      "status": "active",
      "start_time": "2025-03-15T14:00:00.000000Z",
      "end_time": "2025-03-15T14:30:00.000000Z",
      "event_type": "https://api.calendly.com/event_types/CCCCCCCCCCCCCCCC",
      "location": {
        "type": "zoom",
        "join_url": "https://zoom.us/j/123456789"
      },
      "invitees_counter": {
        "total": 1,
        "active": 1,
        "limit": 1
      },
      "created_at": "2025-03-10T09:15:00.000000Z",
      "updated_at": "2025-03-10T09:15:00.000000Z",
      "event_memberships": [
        {
          "user": "https://api.calendly.com/users/AAAAAAAAAAAAAAAA"
        }
      ]
    }
  ],
  "pagination": {
    "count": 1,
    "next_page_token": null
  }
}
```

#### 获取已安排的事件详细信息

```bash
GET /calendly/scheduled_events/{uuid}
```

#### 取消已安排的事件

```bash
POST /calendly/scheduled_events/{uuid}/cancellation
Content-Type: application/json

{
  "reason": "Meeting rescheduled"
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'reason': 'Meeting rescheduled'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/calendly/scheduled_events/DDDDDDDDDDDDDDDD/cancellation', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 邀请者

#### 列出事件受邀者

```bash
GET /calendly/scheduled_events/{event_uuid}/invitees
```

查询参数：
- `status` - 按状态过滤（`active`，`canceled`）
- `email` - 用于过滤受邀者的电子邮件
- `count` - 返回的结果数量（默认 20，最大 100）
- `page_token` - 分页令牌
- `sort` - 排序方式（例如，`created_at:asc`）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/scheduled_events/DDDDDDDDDDDDDDDD/invitees')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "collection": [
    {
      "uri": "https://api.calendly.com/scheduled_events/DDDDDDDDDDDDDDDD/invitees/EEEEEEEEEEEEEEEE",
      "email": "bob.smith@example.com",
      "name": "Bob Smith",
      "status": "active",
      "timezone": "America/Los_Angeles",
      "event": "https://api.calendly.com/scheduled_events/DDDDDDDDDDDDDDDD",
      "created_at": "2025-03-10T09:15:00.000000Z",
      "updated_at": "2025-03-10T09:15:00.000000Z",
      "questions_and_answers": [
        {
          "question": "What would you like to discuss?",
          "answer": "Project timeline review",
          "position": 0
        }
      ],
      "tracking": {
        "utm_source": null,
        "utm_medium": null,
        "utm_campaign": null
      },
      "cancel_url": "https://calendly.com/cancellations/EEEEEEEEEEEEEEEE",
      "reschedule_url": "https://calendly.com/reschedulings/EEEEEEEEEEEEEEEE"
    }
  ],
  "pagination": {
    "count": 1,
    "next_page_token": null
  }
}
```

#### 获取受邀者信息

```bash
GET /calendly/scheduled_events/{event_uuid}/invitees/{invitee_uuid}
```

#### 创建事件受邀者（日程安排 API）

通过创建受邀者来程序化地安排会议。这需要使用付费的 Calendly 计划。

```bash
POST /calendly/event_types/{event_type_uuid}/invitees
Content-Type: application/json

{
  "start_time": "2025-03-20T15:00:00Z",
  "email": "bob.smith@example.com",
  "name": "Bob Smith",
  "timezone": "America/Los_Angeles",
  "location": {
    "kind": "zoom"
  },
  "questions_and_answers": [
    {
      "question_uuid": "QQQQQQQQQQQQQQQ",
      "answer": "Project timeline review"
    }
  ]
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'start_time': '2025-03-20T15:00:00Z', 'email': 'bob.smith@example.com', 'name': 'Bob Smith'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/calendly/event_types/CCCCCCCCCCCCCCCC/invitees', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**注意：** `start_time` 必须对应一个有效的可用时间段。请使用 `/event_type_available_times` 端点来查找可用时间。

### 可用性

#### 获取事件类型的可用时间

```bash
GET /calendly/event_type_available_times
```

查询参数：
- `event_type` - 事件类型 URI（必需）
- `start_time` - 时间范围的开始时间（ISO 8601 格式，必需）
- `end_time` - 时间范围的结束时间（ISO 8601 格式，最长为开始后的 7 天）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/event_type_available_times?event_type=https://api.calendly.com/event_types/CCCCCCCCCCCCCCCC&start_time=2025-03-15T00:00:00Z&end_time=2025-03-22T00:00:00Z')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "collection": [
    {
      "status": "available",
      "invitees_remaining": 1,
      "start_time": "2025-03-17T14:00:00.000000Z",
      "scheduling_url": "https://calendly.com/alice-johnson/30min/2025-03-17T14:00:00Z"
    },
    {
      "status": "available",
      "invitees_remaining": 1,
      "start_time": "2025-03-17T14:30:00.000000Z",
      "scheduling_url": "https://calendly.com/alice-johnson/30min/2025-03-17T14:30:00Z"
    }
  ]
}
```

#### 获取用户的忙碌时间

```bash
GET /calendly/user_busy_times
```

查询参数：
- `user` - 用户 URI（必需）
- `start_time` - 时间范围的开始时间（ISO 8601 格式，必需）
- `end_time` - 时间范围的结束时间（ISO 8601 格式，最长为开始后的 7 天）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/user_busy_times?user=https://api.calendly.com/users/AAAAAAAAAAAAAAAA&start_time=2025-03-15T00:00:00Z&end_time=2025-03-22T00:00:00Z')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "collection": [
    {
      "type": "calendly",
      "start_time": "2025-03-17T10:00:00.000000Z",
      "end_time": "2025-03-17T11:00:00.000000Z"
    },
    {
      "type": "external",
      "start_time": "2025-03-18T14:00:00.000000Z",
      "end_time": "2025-03-18T15:00:00.000000Z"
    }
  ]
}
```

#### 获取用户的可用时间表

```bash
GET /calendly/user_availability_schedules
```

查询参数：
- `user` - 用户 URI（必需）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/user_availability_schedules?user=https://api.calendly.com/users/AAAAAAAAAAAAAAAA')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 组织

#### 列出组织成员

```bash
GET /calendly/organization_memberships
```

查询参数：
- `organization` - 组织 URI（必需）
- `user` - 用于过滤的用户 URI
- `email` - 用于过滤的电子邮件
- `count` - 返回的结果数量（默认 20，最大 100）
- `page_token` - 分页令牌

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/organization_memberships?organization=https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "collection": [
    {
      "uri": "https://api.calendly.com/organization_memberships/FFFFFFFFFFFFFFFF",
      "role": "admin",
      "user": {
        "uri": "https://api.calendly.com/users/AAAAAAAAAAAAAAAA",
        "name": "Alice Johnson",
        "email": "alice.johnson@acme.com"
      },
      "organization": "https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB",
      "created_at": "2024-01-15T10:30:00.000000Z",
      "updated_at": "2025-06-20T14:45:00.000000Z"
    }
  ],
  "pagination": {
    "count": 1,
    "next_page_token": null
  }
}
```

### Webhook

Webhook 需要使用付费的 Calendly 计划（Standard、Teams 或 Enterprise）。

#### 列出 Webhook 订阅

```bash
GET /calendly/webhook_subscriptions
```

查询参数：
- `organization` - 组织 URI（必需）
- `scope` - 按范围过滤（`user`，`organization`）
- `user` - 用于过滤的用户 URI（当 scope 为 `user` 时）
- `count` - 返回的结果数量（默认 20，最大 100）
- `page_token` - 分页令牌

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/webhook_subscriptions?organization=https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB&scope=organization')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建 Webhook 订阅

```bash
POST /calendly/webhook_subscriptions
Content-Type: application/json

{
  "url": "https://example.com/webhook",
  "events": ["invitee.created", "invitee.canceled"],
  "organization": "https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB",
  "scope": "organization",
  "signing_key": "your-secret-key"
}
```

可用事件：
- `invitee.created` - 当受邀者安排事件时触发
- `invitee.canceled` - 当受邀者取消事件时触发
- `routing_form_submission.created` - 当路由表单提交时触发

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'url': 'https://example.com/webhook', 'events': ['invitee.created', 'invitee.canceled'], 'organization': 'https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB', 'scope': 'organization'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/calendly/webhook_subscriptions', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "resource": {
    "uri": "https://api.calendly.com/webhook_subscriptions/GGGGGGGGGGGGGGGG",
    "callback_url": "https://example.com/webhook",
    "created_at": "2025-03-01T12:00:00.000000Z",
    "updated_at": "2025-03-01T12:00:00.000000Z",
    "retry_started_at": null,
    "state": "active",
    "events": ["invitee.created", "invitee.canceled"],
    "scope": "organization",
    "organization": "https://api.calendly.com/organizations/BBBBBBBBBBBBBBBB",
    "user": null,
    "creator": "https://api.calendly.com/users/AAAAAAAAAAAAAAAA"
  }
}
```

#### 获取 Webhook 订阅信息

```bash
GET /calendly/webhook_subscriptions/{uuid}
```

#### 删除 Webhook 订阅

```bash
DELETE /calendly/webhook_subscriptions/{uuid}
```

**示例：**

**成功时返回 `204 No Content`。**

## 分页

使用 `page_token` 进行分页。如果存在更多结果，响应中会包含 `pagination.next_page_token`：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/calendly/scheduled_events?user=USER_URI&page_token=NEXT_PAGE_TOKEN')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/calendly/scheduled_events?user=https://api.calendly.com/users/AAAAAAAAAAAAAAAA&status=active',
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
    'https://gateway.maton.ai/calendly/scheduled_events',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={
        'user': 'https://api.calendly.com/users/AAAAAAAAAAAAAAAA',
        'status': 'active'
    }
)
data = response.json()
```

## 注意事项

- 资源标识符是 URI（例如，`https://api.calendly.com/users/AAAAAAAAAAAAAAAA`）
- 时间戳采用 ISO 8601 格式
- 日程安排 API（创建事件受邀者）需要使用付费的 Calendly 计划
- Calendly 的免费计划不支持 Webhook
- 可用性端点的每次请求的最大时间范围为 7 天，且 `start_time` 必须在未来
- 该 API 不支持程序化地创建或管理事件类型
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确展开。这可能会导致“无效 API 密钥”错误。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求错误或缺少 Calendly 连接 |
| 401 | 无效或缺少 Maton API 密钥 |
| 403 | 禁止访问 - 权限不足或计划限制 |
| 404 | 资源未找到 |
| 424 | 外部日历错误（Calendly 侧的问题） |
| 429 | 请求速率限制 |
| 4xx/5xx | 来自 Calendly API 的传递错误 |

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

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `calendly` 开头。例如：
- 正确：`https://gateway.maton.ai/calendly/users/me`
- 错误：`https://gateway.maton.ai/users/me`

## 资源

- [Calendly 开发者门户](https://developer.calendly.com/)
- [API 参考](https://developer.calendly.com/api-docs)
- [API 使用案例](https://developer.calendly.com/api-use-cases)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)