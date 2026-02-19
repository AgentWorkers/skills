---
name: zohobookings
description: >
  **Zoho Bookings API集成与托管式OAuth**  
  该功能支持用户通过OAuth身份验证来管理预约、服务、员工信息以及工作空间。  
  当用户需要在Zoho Bookings中预约服务、查看员工可用性或管理工作空间时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用此功能需要网络连接以及有效的Maton API密钥。
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
# Zoho Bookings

您可以使用托管的 OAuth 认证来访问 Zoho Bookings API。该 API 允许您执行完整的 CRUD 操作（创建、读取、更新和删除），以管理预约、服务、员工和工作空间。

## 快速入门

```bash
# List workspaces
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/workspaces')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-bookings/bookings/v1/json/{endpoint}
```

该网关会将请求代理到 `www.zohoapis.com/bookings/v1/json`，并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 管理您的 Zoho Bookings OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-bookings&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-bookings'}).encode()
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
    "connection_id": "3c358231-7ca7-4a63-8a3c-3a9d21be53ca",
    "status": "ACTIVE",
    "creation_time": "2026-02-18T00:17:23.498742Z",
    "last_updated_time": "2026-02-18T00:18:59.299114Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoho-bookings",
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

如果您有多个 Zoho Bookings 连接，请使用 `Maton-Connection` 头指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/workspaces')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '3c358231-7ca7-4a63-8a3c-3a9d21be53ca')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 工作空间

#### 获取工作空间信息

```bash
GET /zoho-bookings/bookings/v1/json/workspaces
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `workspace_id` | string | 按特定工作空间 ID 过滤 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/workspaces')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "returnvalue": {
      "data": [
        {
          "name": "Main Office",
          "id": "4753814000000048016"
        }
      ]
    },
    "status": "success"
  }
}
```

#### 创建工作空间

```bash
POST /zoho-bookings/bookings/v1/json/createworkspace
Content-Type: application/x-www-form-urlencoded
```

**表单参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `name` | string | 是 | 工作空间名称（2-50 个字符，不含特殊字符） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode
form_data = urlencode({'name': 'New York Office'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/createworkspace', data=form_data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 服务

#### 获取服务信息

```bash
GET /zoho-bookings/bookings/v1/json/services?workspace_id={workspace_id}
```

**查询参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `workspace_id` | string | 是 | 工作空间 ID |
| `service_id` | string | 否 | 按特定服务 ID 过滤 |
| `staff_id` | string | 否 | 按员工 ID 过滤 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/services?workspace_id=4753814000000048016')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "returnvalue": {
      "data": [
        {
          "id": "4753814000000048054",
          "name": "Product Demo",
          "duration": "30 mins",
          "service_type": "APPOINTMENT",
          "price": 0,
          "currency": "USD",
          "assigned_staffs": ["4753814000000048014"],
          "assigned_workspace": "4753814000000048016",
          "embed_url": "https://example.zohobookings.com/portal-embed#/4753814000000048054",
          "let_customer_select_staff": true
        }
      ],
      "next_page_available": false,
      "page": 1
    },
    "status": "success"
  }
}
```

#### 创建服务

```bash
POST /zoho-bookings/bookings/v1/json/createservice
Content-Type: application/x-www-form-urlencoded
```

**表单参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `name` | string | 是 | 服务名称 |
| `workspace_id` | string | 是 | 工作空间 ID |
| `duration` | integer | 否 | 服务持续时间（分钟） |
| `cost` | number | 否 | 服务价格 |
| `pre_buffer` | integer | 否 | 服务前的缓冲时间（分钟） |
| `post_buffer` | integer | 否 | 服务后的缓冲时间（分钟） |
| `description` | string | 否 | 服务描述 |
| `assigned_staffs` | string | 否 | 员工 ID 的 JSON 数组 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode
form_data = urlencode({
    'name': 'Consultation',
    'workspace_id': '4753814000000048016',
    'duration': '60'
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/createservice', data=form_data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 员工

#### 获取员工信息

```bash
GET /zoho-bookings/bookings/v1/json/staffs?workspace_id={workspace_id}
```

**查询参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `workspace_id` | string | 是 | 工作空间 ID |
| `staff_id` | string | 否 | 按特定员工 ID 过滤 |
| `service_id` | string | 否 | 按服务 ID 过滤 |
| `staff_email` | string | 否 | 按电子邮件（部分匹配）过滤 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/staffs?workspace_id=4753814000000048016')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "returnvalue": {
      "data": [
        {
          "id": "4753814000000048014",
          "name": "John Doe",
          "email": "john@example.com",
          "designation": "Consultant",
          "assigned_services": ["4753814000000048054"],
          "assigned_workspaces": ["4753814000000048016"],
          "embed_url": "https://example.zohobookings.com/portal-embed#/4753814000000048014"
        }
      ]
    },
    "status": "success"
  }
}
```

### 预约

#### 预订服务

```bash
POST /zoho-bookings/bookings/v1/json/appointment
Content-Type: application/x-www-form-urlencoded
```

**表单参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `service_id` | string | 是 | 服务 ID |
| `staff_id` | string | 是* | 员工 ID（*或 resource_id/group_id） |
| `from_time` | string | 是 | 开始时间：`dd-MMM-yyyy HH:mm:ss`（24 小时制） |
| `timezone` | string | 否 | 时区（例如：`America/Los_Angeles`） |
| `customer_details` | string | 是 | 包含 `name`、`email`、`phone_number` 的 JSON 字符串 |
| `notes` | string | 否 | 预约备注 |
| `additional_fields` | string | 否 | 包含自定义字段的 JSON 字符串 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode
form_data = urlencode({
    'service_id': '4753814000000048054',
    'staff_id': '4753814000000048014',
    'from_time': '20-Feb-2026 10:00:00',
    'timezone': 'America/Los_Angeles',
    'customer_details': json.dumps({
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'phone_number': '+15551234567'
    })
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/appointment', data=form_data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "returnvalue": {
      "booking_id": "#NU-00001",
      "service_name": "Product Demo",
      "staff_name": "John Doe",
      "start_time": "20-Feb-2026 10:00:00",
      "end_time": "20-Feb-2026 10:30:00",
      "duration": "30 mins",
      "customer_name": "Jane Smith",
      "customer_email": "jane@example.com",
      "status": "upcoming",
      "time_zone": "America/Los_Angeles"
    },
    "status": "success"
  }
}
```

#### 获取预约信息

```bash
GET /zoho-bookings/bookings/v1/json/getappointment?booking_id={booking_id}
```

**查询参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `booking_id` | string | 是 | 预约 ID（URL 编码格式，例如：`%23NU-00001`） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/getappointment?booking_id=%23NU-00001')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取所有预约信息

```bash
POST /zoho-bookings/bookings/v1/json/fetchappointment
Content-Type: application/x-www-form-urlencoded
```

**表单参数：**

将参数作为 JSON 数据发送：

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `from_time` | string | 开始日期：`dd-MMM-yyyy HH:mm:ss` |
| `to_time` | string | 结束日期：`dd-MMM-yyyy HH:mm:ss` |
| `status` | string | `UPCOMING`、`CANCEL`、`COMPLETED`、`NO_SHOW`、`PENDING` |
| `service_id` | string | 按服务过滤 |
| `staff_id` | string | 按员工过滤 |
| `customer_name` | string | 按客户名称（部分匹配）过滤 |
| `customer_email` | string | 按电子邮件（部分匹配）过滤 |
| `page` | integer | 页码 |
| `per_page` | integer | 每页显示的结果数量（最多 100 条） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode
form_data = urlencode({
    'data': json.dumps({
        'from_time': '17-Feb-2026 00:00:00',
        'to_time': '20-Feb-2026 23:59:59'
    })
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/fetchappointment', data=form_data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "returnvalue": {
      "response": [
        {
          "booking_id": "#NU-00001",
          "service_name": "Product Demo",
          "staff_name": "John Doe",
          "start_time": "20-Feb-2026 10:00:00",
          "customer_name": "Jane Smith",
          "status": "upcoming"
        }
      ],
      "next_page_available": false,
      "page": 1
    },
    "status": "success"
  }
}
```

#### 更新预约

```bash
POST /zoho-bookings/bookings/v1/json/updateappointment
Content-Type: application/x-www-form-urlencoded
```

**表单参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `booking_id` | string | 是 | 预约 ID |
| `action` | string | 是 | `completed`、`cancel` 或 `noshow` |

**示例 - 取消预约：**

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode
form_data = urlencode({
    'booking_id': '#NU-00001',
    'action': 'cancel'
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/updateappointment', data=form_data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 分页

预约信息支持基于页码的分页：

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode
form_data = urlencode({
    'data': json.dumps({
        'from_time': '01-Feb-2026 00:00:00',
        'to_time': '28-Feb-2026 23:59:59',
        'page': 1,
        'per_page': 50
    })
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bookings/bookings/v1/json/fetchappointment', data=form_data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

响应中包含分页信息：

```json
{
  "response": {
    "returnvalue": {
      "response": [...],
      "next_page_available": true,
      "page": 1
    },
    "status": "success"
  }
}
```

## 代码示例

### JavaScript

```javascript
// Fetch workspaces
const response = await fetch(
  'https://gateway.maton.ai/zoho-bookings/bookings/v1/json/workspaces',
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

# Fetch services
response = requests.get(
    'https://gateway.maton.ai/zoho-bookings/bookings/v1/json/services',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'workspace_id': '4753814000000048016'}
)
data = response.json()
```

## 注意事项

- 日期/时间格式：`dd-MMM-yyyy HH:mm:ss`（例如：`20-Feb-2026 10:00:00`）
- 预约 ID 以 `#` 为前缀（URL 编码为 `%23`）
- `customer_details` 必须是 JSON 字符串，不能是对象
- `fetchappointment` 请求中的参数需要用 `data` 字段作为 JSON 数据发送
- 其他 POST 请求端点使用常规表单字段
- 服务类型：`APPOINTMENT`、`RESOURCE`、`CLASS`、`COLLECTIVE`
- 状态值：`UPCOMING`、`CANCEL`、`ONGOING`、`PENDING`、`COMPLETED`、`NO_SHOW`
- 默认分页数量：每页 50 条预约（最多 100 条）
- 如果收到范围错误，请联系 Maton 支持团队（support@maton.ai），并提供具体的操作、API 和使用场景
- 重要提示：当 URL 包含括号时，使用 `curl -g` 选项来禁用全局解析
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 可能无法正确解析

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Zoho Bookings 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 日限达到 |
| 4xx/5xx | 来自 Zoho Bookings API 的传递错误 |

### 日限

| 计划 | 每日限制 |
|------|-------------|
| 免费 | 每用户 250 次调用 |
| 基础版 | 每用户 1,000 次调用 |
| 高级版 | 每用户 3,000 次调用 |
| Zoho One | 每用户 3,000 次调用 |

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

### 故障排除：无效的应用名称

1. 确保您的 URL 路径以 `zoho-bookings` 开头。例如：

- 正确：`https://gateway.maton.ai/zoho-bookings/bookings/v1/json/workspaces`
- 错误：`https://gateway.maton.ai/bookings/v1/json/workspaces`

## 资源

- [Zoho Bookings API 文档](https://www.zoho.com/bookings/help/api/v1/oauthauthentication.html)
- [预订服务 API](https://www.zoho.com/bookings/help/api/v1/book-appointment.html)
- [获取预约信息 API](https://www.zoho.com/bookings/help/api/v1/fetch-appointment.html)
- [获取服务信息 API](https://www.zoho.com/bookings/help/api/v1/fetch-services.html)
- [获取员工信息 API](https://www.zoho.com/bookings/help/api/v1/fetch-staff.html)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)