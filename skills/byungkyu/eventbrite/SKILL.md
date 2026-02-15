---
name: eventbrite
description: |
  Eventbrite API integration with managed OAuth. Manage events, venues, ticket classes, orders, and attendees.
  Use this skill when users want to create and manage events, check orders, view attendees, or access event categories.
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

# Eventbrite

通过管理的OAuth认证来访问Eventbrite API。您可以管理事件、场地、票类、订单、参与者等信息。

## 快速入门

```bash
# Get current user
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/eventbrite/v3/users/me/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/eventbrite/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Eventbrite API端点路径。该网关会将请求代理到 `www.eventbriteapi.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Eventbrite OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=eventbrite&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'eventbrite'}).encode()
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
    "connection_id": "a2dd9063-64b4-4fe2-b4c5-8dd711648244",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T09:11:20.516013Z",
    "last_updated_time": "2026-02-07T09:14:35.273822Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "eventbrite",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth认证。

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

如果您有多个Eventbrite连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/eventbrite/v3/users/me/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'a2dd9063-64b4-4fe2-b4c5-8dd711648244')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 用户操作

#### 获取当前用户

```bash
GET /eventbrite/v3/users/me/
```

**响应：**
```json
{
  "emails": [{"email": "user@example.com", "verified": true, "primary": true}],
  "id": "1234567890",
  "name": "John Doe",
  "first_name": "John",
  "last_name": "Doe",
  "is_public": false,
  "image_id": null
}
```

#### 列出用户所属的组织

```bash
GET /eventbrite/v3/users/me/organizations/
```

#### 列出用户的订单

```bash
GET /eventbrite/v3/users/me/orders/
```

### 组织操作

#### 列出组织事件

```bash
GET /eventbrite/v3/organizations/{organization_id}/events/
```

查询参数：
- `status` - 按状态过滤：`draft`、`live`、`started`、`ended`、`completed`、`canceled`
- `order_by` - 排序方式：`start_asc`、`start_desc`、`created_asc`、`created_desc`
- `time_filter` - 按时间过滤：`current_future`、`past`

#### 列出组织场地

```bash
GET /eventbrite/v3/organizations/{organization_id}/venues/
```

#### 创建场地

```bash
POST /eventbrite/v3/organizations/{organization_id}/venues/
Content-Type: application/json

{
  "venue": {
    "name": "Conference Center",
    "address": {
      "address_1": "123 Main St",
      "city": "San Francisco",
      "region": "CA",
      "postal_code": "94105",
      "country": "US"
    }
  }
}
```

### 事件操作

#### 获取事件信息

```bash
GET /eventbrite/v3/events/{event_id}/
```

#### 创建事件

事件必须在一个组织下创建：

```bash
POST /eventbrite/v3/organizations/{organization_id}/events/
Content-Type: application/json

{
  "event": {
    "name": {"html": "My Event"},
    "description": {"html": "<p>Event description</p>"},
    "start": {
      "timezone": "America/Los_Angeles",
      "utc": "2026-03-01T19:00:00Z"
    },
    "end": {
      "timezone": "America/Los_Angeles",
      "utc": "2026-03-01T22:00:00Z"
    },
    "currency": "USD",
    "online_event": false,
    "listed": true,
    "shareable": true,
    "capacity": 100,
    "category_id": "103",
    "format_id": "1"
  }
}
```

#### 更新事件

```bash
POST /eventbrite/v3/events/{event_id}/
Content-Type: application/json

{
  "event": {
    "name": {"html": "Updated Event Name"},
    "capacity": 200
  }
}
```

#### 发布事件

```bash
POST /eventbrite/v3/events/{event_id}/publish/
```

#### 取消事件

```bash
POST /eventbrite/v3/events/{event_id}/unpublish/
```

#### 删除事件

```bash
DELETE /eventbrite/v3/events/{event_id}/
```

### 票类操作

#### 列出票类

```bash
GET /eventbrite/v3/events/{event_id}/ticket_classes/
```

#### 创建票类

```bash
POST /eventbrite/v3/events/{event_id}/ticket_classes/
Content-Type: application/json

{
  "ticket_class": {
    "name": "General Admission",
    "description": "Standard entry ticket",
    "quantity_total": 100,
    "cost": "USD,2500",
    "sales_start": "2026-01-01T00:00:00Z",
    "sales_end": "2026-02-28T23:59:59Z",
    "minimum_quantity": 1,
    "maximum_quantity": 10
  }
}
```

对于免费票，请省略 `cost` 字段或设置 `free: true`。

#### 更新票类

```bash
POST /eventbrite/v3/events/{event_id}/ticket_classes/{ticket_class_id}/
Content-Type: application/json

{
  "ticket_class": {
    "quantity_total": 150
  }
}
```

#### 删除票类

```bash
DELETE /eventbrite/v3/events/{event_id}/ticket_classes/{ticket_class_id}/
```

### 参与者操作

#### 列出事件参与者

```bash
GET /eventbrite/v3/events/{event_id}/attendees/
```

查询参数：
- `status` - 按状态过滤：`attending`、`not_attending`、`unpaid`
- `changed_since` - ISO 8601时间戳，用于获取之后更改的参与者

#### 获取参与者信息

```bash
GET /eventbrite/v3/events/{event_id}/attendees/{attendee_id}/
```

### 订单操作

#### 列出事件订单

```bash
GET /eventbrite/v3/events/{event_id}/orders/
```

查询参数：
- `status` - 按状态过滤：`active`、`inactive`、`all`
- `changed_since` - ISO 8601时间戳

#### 获取订单信息

```bash
GET /eventbrite/v3/orders/{order_id}/
```

### 场地操作

#### 获取场地信息

```bash
GET /eventbrite/v3/venues/{venue_id}/
```

#### 更新场地信息

```bash
POST /eventbrite/v3/venues/{venue_id}/
Content-Type: application/json

{
  "venue": {
    "name": "Updated Venue Name"
  }
}
```

### 参考数据

#### 列出类别

```bash
GET /eventbrite/v3/categories/
```

**响应：**
```json
{
  "locale": "en_US",
  "pagination": {"object_count": 21, "page_number": 1, "page_size": 50},
  "categories": [
    {"id": "103", "name": "Music", "short_name": "Music"},
    {"id": "101", "name": "Business & Professional", "short_name": "Business"},
    {"id": "110", "name": "Food & Drink", "short_name": "Food & Drink"}
  ]
}
```

#### 获取类别信息

```bash
GET /eventbrite/v3/categories/{category_id}/
```

#### 列出子类别

```bash
GET /eventbrite/v3/subcategories/
```

#### 列出格式

```bash
GET /eventbrite/v3/formats/
```

**常见格式：**
- `1` - 会议
- `2` - 研讨会或演讲
- `5` - 节日或展览
- `6` - 音乐会或表演
- `9` - 课程、培训或工作坊
- `10` - 会议或社交活动
- `11` - 派对或社交聚会

#### 列出国家

```bash
GET /eventbrite/v3/system/countries/
```

#### 列出地区

```bash
GET /eventbrite/v3/system/regions/
```

## 分页

Eventbrite使用基于页面和基于延续的分页方式：

```bash
GET /eventbrite/v3/organizations/{org_id}/events/?page_size=50
```

**响应：**
```json
{
  "pagination": {
    "object_count": 150,
    "page_number": 1,
    "page_size": 50,
    "page_count": 3,
    "has_more_items": true,
    "continuation": "eyJwYWdlIjogMn0"
  },
  "events": [...]
}
```

对于后续页面，请使用 `continuation` 令牌：

```bash
GET /eventbrite/v3/organizations/{org_id}/events/?continuation=eyJwYWdlIjogMn0
```

## 扩展数据

通过使用 `expand` 参数来包含相关数据：

```bash
GET /eventbrite/v3/events/{event_id}/?expand=venue,ticket_classes,category
```

常见扩展数据：
- `venue` - 包含场地详细信息
- `ticket_classes` - 包含票类信息
- `category` - 包含类别详细信息
- `subcategory` - 包含子类别详细信息
- `format` - 包含格式详细信息
- `organizer` - 包含组织者信息

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/eventbrite/v3/users/me/',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const user = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/eventbrite/v3/users/me/',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
user = response.json()
```

## 注意事项

- 所有端点路径应以斜杠 `/` 结尾。
- 创建事件需要一个组织——请使用基于组织的端点。
- 旧的基于用户的事件端点已弃用；请使用基于组织的端点。
- 时间戳采用ISO 8601格式（UTC）。
- 货币金额以小单位表示（例如，“USD,2500”表示$25.00）。
- 调用限制：每小时1,000次，每天48,000次。
- 事件搜索API已不再公开提供（2020年2月弃用）。
- 重要提示：当URL包含括号时，使用 `curl -g` 以禁用全局解析。
- 重要提示：当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少Eventbrite连接或参数无效 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 未授权（请检查权限范围或使用基于组织的端点） |
| 404 | 资源未找到 |
| 429 | 调用次数受限 |
| 4xx/5xx | 来自Eventbrite API的传递错误 |

### 常见错误

**使用旧的用户端点时出现“NOT_AUTHORIZED”：**
```json
{"status_code": 403, "error": "NOT_AUTHORIZED", "error_description": "This user is not able to use legacy user endpoints, please use the organization equivalent."}
```
解决方案：使用 `/organizations/{org_id}/events/` 而不是 `/users/me/owned_events/`。

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的URL路径以 `eventbrite` 开头。例如：
- 正确：`https://gateway.maton.ai/eventbrite/v3/users/me/`
- 错误：`https://gateway.maton.ai/v3/users/me/`

## 资源

- [Eventbrite API文档](https://www.eventbrite.com/platform/api)
- [API基础知识](https://www.eventbrite.com/platform/docs/api-basics)
- [API浏览器](https://www.eventbrite.com/platform/docs/api-explorer)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)