---
name: acuity-scheduling
description: |
  Acuity Scheduling API integration with managed OAuth. Manage appointments, calendars, clients, and availability. Use this skill when users want to schedule, reschedule, or cancel appointments, check availability, or manage clients and calendars. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Acuity Scheduling

您可以使用受管理的 OAuth 认证来访问 Acuity Scheduling API，以管理预约、日历、客户、可用时间等信息。

## 快速入门

```bash
# List appointments
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/acuity-scheduling/api/v1/appointments?max=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/acuity-scheduling/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Acuity API 端点路径。该网关会将请求代理到 `acuityscheduling.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Acuity Scheduling OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=acuity-scheduling&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'acuity-scheduling'}).encode()
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
    "app": "acuity-scheduling",
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

如果您有多个 Acuity Scheduling 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/acuity-scheduling/api/v1/appointments')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 账户信息

#### 获取账户信息

```bash
GET /acuity-scheduling/api/v1/me
```

返回账户信息，包括时区、调度页面 URL 和计划详情。

**响应：**
```json
{
  "id": 12345,
  "email": "user@example.com",
  "timezone": "America/Los_Angeles",
  "name": "My Business",
  "schedulingPage": "https://app.acuityscheduling.com/schedule.php?owner=12345",
  "plan": "Professional",
  "currency": "USD"
}
```

### 预约

#### 列出预约

```bash
GET /acuity-scheduling/api/v1/appointments
```

**查询参数：**
| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `max` | 整数 | 最大结果数量（默认：100） |
| `minDate` | 日期 | 在此日期或之后的预约 |
| `maxDate` | 日期 | 在此日期或之前的预约 |
| `calendarID` | 整数 | 按日历筛选 |
| `appointmentTypeID` | 整数 | 按预约类型筛选 |
| `canceled` | 布尔值 | 是否包含已取消的预约（默认：false） |
| `firstName` | 字符串 | 按客户名字筛选 |
| `lastName` | 字符串 | 按客户姓氏筛选 |
| `email` | 字符串 | 按客户电子邮件筛选 |
| `excludeForms` | 布尔值 | 省略表单以加快响应速度 |
| `direction` | 字符串 | 排序方式：ASC 或 DESC（默认：DESC） |

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/acuity-scheduling/api/v1/appointments?max=10&minDate=2026-02-01')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
[
  {
    "id": 1630290133,
    "firstName": "Jane",
    "lastName": "McTest",
    "phone": "1235550101",
    "email": "jane.mctest@example.com",
    "date": "February 4, 2026",
    "time": "9:30am",
    "endTime": "10:20am",
    "datetime": "2026-02-04T09:30:00-0800",
    "type": "Consultation",
    "appointmentTypeID": 88791369,
    "duration": "50",
    "calendar": "Chris",
    "calendarID": 13499175,
    "canceled": false,
    "confirmationPage": "https://app.acuityscheduling.com/schedule.php?..."
  }
]
```

#### 获取预约详情

```bash
GET /acuity-scheduling/api/v1/appointments/{id}
```

#### 创建预约

```bash
POST /acuity-scheduling/api/v1/appointments
Content-Type: application/json

{
  "datetime": "2026-02-15T09:00",
  "appointmentTypeID": 123,
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phone": "555-123-4567",
  "timezone": "America/New_York"
}
```

**必填字段：**
- `datetime` - 日期和时间（必须能被 PHP 的 `strtotime()` 函数解析）
- `appointmentTypeID` - 预约类型 ID |
- `firstName` - 客户名字 |
- `lastName` - 客户姓氏 |
- `email` - 客户电子邮件 |

**可选字段：**
- `phone` - 客户电话号码 |
- `calendarID` - 特定日历（省略时自动选择） |
- `timezone` - 客户时区 |
- `certificate` - 包或优惠券代码 |
- `notes` - 管理员备注 |
- `addonIDs` - 表单字段 ID 的数组 |
- `fields` - 表单字段值的数组 |

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'datetime': '2026-02-15T09:00',
    'appointmentTypeID': 123,
    'firstName': 'John',
    'lastName': 'Doe',
    'email': 'john.doe@example.com'
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/acuity-scheduling/api/v1/appointments', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新预约

```bash
PUT /acuity-scheduling/api/v1/appointments/{id}
Content-Type: application/json

{
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jane.smith@example.com"
}
```

#### 取消预约

```bash
PUT /acuity-scheduling/api/v1/appointments/{id}/cancel
```

返回的响应中，`canceled` 为 `true` 表示预约已被取消。

#### 重新安排预约

```bash
PUT /acuity-scheduling/api/v1/appointments/{id}/reschedule
Content-Type: application/json

{
  "datetime": "2026-02-20T10:00"
}
```

**注意：** 新的日期和时间必须是一个可用的时间段。

### 日历

#### 列出日历

```bash
GET /acuity-scheduling/api/v1/calendars
```

**响应：**
```json
[
  {
    "id": 13499175,
    "name": "Chris",
    "email": "",
    "replyTo": "chris@example.com",
    "description": "",
    "location": "",
    "timezone": "America/Los_Angeles"
  }
]
```

### 预约类型

#### 列出预约类型

```bash
GET /acuity-scheduling/api/v1/appointment-types
```

**查询参数：**
- `includeDeleted` (布尔值) - 是否包含已删除的预约类型

**响应：**
```json
[
  {
    "id": 88791369,
    "name": "Consultation",
    "active": true,
    "description": "",
    "duration": 50,
    "price": "45.00",
    "category": "",
    "color": "#ED7087",
    "private": false,
    "type": "service",
    "calendarIDs": [13499175],
    "schedulingUrl": "https://app.acuityscheduling.com/schedule.php?..."
  }
]
```

### 可用时间

#### 获取可用日期

```bash
GET /acuity-scheduling/api/v1/availability/dates?month=2026-02&appointmentTypeID=123
```

**必填参数：**
- `month` - 要检查的月份（例如：“2026-02”）
- `appointmentTypeID` - 预约类型 ID |

**可选参数：**
- `calendarID` - 特定日历 |
- `timezone` - 结果的时区（例如：“America/New_York”）

**响应：**
```json
[
  {"date": "2026-02-09"},
  {"date": "2026-02-10"},
  {"date": "2026-02-11"}
]
```

#### 获取可用时间段

```bash
GET /acuity-scheduling/api/v1/availability/times?date=2026-02-10&appointmentTypeID=123
```

**必填参数：**
- `date` - 要检查的日期 |
- `appointmentTypeID` - 预约类型 ID |

**可选参数：**
- `calendarID` - 特定日历 |
- `timezone` - 结果的时区

**响应：**
```json
[
  {"time": "2026-02-10T09:00:00-0800", "slotsAvailable": 1},
  {"time": "2026-02-10T09:50:00-0800", "slotsAvailable": 1},
  {"time": "2026-02-10T10:40:00-0800", "slotsAvailable": 1}
]
```

### 客户

#### 列出客户

```bash
GET /acuity-scheduling/api/v1/clients
```

**查询参数：**
- `search` - 按名字、姓氏或电话号码筛选

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/acuity-scheduling/api/v1/clients?search=John')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
[
  {
    "firstName": "Jane",
    "lastName": "McTest",
    "email": "jane.mctest@example.com",
    "phone": "(123) 555-0101",
    "notes": ""
  }
]
```

#### 创建客户

```bash
POST /acuity-scheduling/api/v1/clients
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "555-123-4567"
}
```

#### 更新客户

```bash
PUT /acuity-scheduling/api/v1/clients
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.updated@example.com"
}
```

**注意：** 更新/删除客户仅适用于已有预约的客户。

#### 删除客户

```bash
DELETE /acuity-scheduling/api/v1/clients
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe"
}
```

### 时间段

#### 列出时间段

```bash
GET /acuity-scheduling/api/v1/blocks
```

**查询参数：**
- `max` - 最大结果数量（默认：100） |
- `minDate` - 在此日期或之后的时间段 |
- `maxDate` - 在此日期或之前的时间段 |
- `calendarID` - 按日历筛选 |

#### 获取时间段详情

```bash
GET /acuity-scheduling/api/v1/blocks/{id}
```

#### 创建时间段

```bash
POST /acuity-scheduling/api/v1/blocks
Content-Type: application/json

{
  "start": "2026-02-15T12:00",
  "end": "2026-02-15T13:00",
  "calendarID": 1234,
  "notes": "Lunch break"
}
```

**响应：**
```json
{
  "id": 9589304654,
  "calendarID": 13499175,
  "start": "2026-02-15T12:00:00-0800",
  "end": "2026-02-15T13:00:00-0800",
  "notes": "Lunch break",
  "description": "Sunday, February 15, 2026 12:00pm - 1:00pm"
}
```

#### 删除时间段

```bash
DELETE /acuity-scheduling/api/v1/blocks/{id}
```

成功时返回 204（表示“无内容”）。

### 表单

#### 列出表单

```bash
GET /acuity-scheduling/api/v1/forms
```

**响应：**
```json
[
  {
    "id": 123,
    "name": "Client Intake Form",
    "appointmentTypeIDs": [456, 789],
    "fields": [
      {
        "id": 1,
        "name": "How did you hear about us?",
        "type": "dropdown",
        "options": ["Google", "Friend", "Social Media"],
        "required": true
      }
    ]
  }
]
```

### 标签

#### 列出标签

```bash
GET /acuity-scheduling/api/v1/labels
```

**响应：**
```json
[
  {"id": 23116714, "name": "Checked In", "color": "green"},
  {"id": 23116715, "name": "Completed", "color": "pink"},
  {"id": 23116713, "name": "Confirmed", "color": "yellow"}
]
```

## 分页

Acuity Scheduling 使用 `max` 参数来限制结果数量。您可以使用 `minDate` 和 `maxDate` 来在日期范围内进行分页：

```bash
# First page
GET /acuity-scheduling/api/v1/appointments?max=100&minDate=2026-01-01&maxDate=2026-01-31

# Next page
GET /acuity-scheduling/api/v1/appointments?max=100&minDate=2026-02-01&maxDate=2026-02-28
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/acuity-scheduling/api/v1/appointments?max=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const appointments = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/acuity-scheduling/api/v1/appointments',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'max': 10}
)
appointments = response.json()
```

## 注意事项：

- 日期时间值必须能被 PHP 的 `strtotime()` 函数解析。
- 时区使用 IANA 格式（例如：“America/New_York”, “America/Los_Angeles”）。
- 更新/删除客户操作仅适用于已有预约的客户。
- 重新安排预约时，新的日期和时间必须是一个可用的时间段。
- 使用 `excludeForms=true` 可以加快预约列表的响应速度。
- **重要提示：** 当 URL 中包含括号时，使用 `curl -g` 可以防止全局解析。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析，可能会导致“无效 API 密钥”错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求无效（例如：时间不可用、客户未找到） |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 使用频率限制 |
| 4xx/5xx | 来自 Acuity API 的传递错误 |

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

### 故障排除：无效的应用程序名称

1. 确保您的 URL 路径以 `acuity-scheduling` 开头。例如：
- 正确：`https://gateway.maton.ai/acuity-scheduling/api/v1/appointments`
- 错误：`https://gateway.maton.ai/api/v1/appointments`

## 资源

- [Acuity Scheduling API 快速入门](https://developers.acuityscheduling.com/reference/quick-start)
- [预约 API](https://developers.acuityscheduling.com/reference/get-appointments)
- [可用时间 API](https://developers.acuityscheduling.com/reference/get-availability-dates)
- [日历 API](https://developers.acuityscheduling.com/reference/get-calendars)
- [客户 API](https://developers.acuityscheduling.com/reference/clients)
- [OAuth2 文档](https://developers.acuityscheduling.com/docs/oauth2)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)