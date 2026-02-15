---
name: zoho-bigin
description: |
  Zoho Bigin API integration with managed OAuth. Manage contacts, companies, pipelines, and products in Bigin CRM.
  Use this skill when users want to read, create, update, or delete CRM records, search contacts, or manage sales pipelines.
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

# Zoho Bigin

您可以使用管理的 OAuth 认证来访问 Zoho Bigin API。该 API 支持对联系人、公司、销售流程和产品进行完整的创建（Create）、读取（Read）、更新（Update）和删除（Delete, CRUD）操作。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts?fields=First_Name,Last_Name,Email')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-bigin/bigin/v2/{endpoint}
```

该网关会将请求代理到 `www.zohoapis.com/bigin/v2`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Zoho Bigin OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-bigin&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-bigin'}).encode()
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
    "app": "zoho-bigin",
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

如果您有多个 Zoho Bigin 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts?fields=First_Name,Last_Name,Email')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 模块

Zoho Bigin 将数据组织成不同的模块。可用的模块包括：

| 模块 | API 名称 | 描述 |
|--------|----------|-------------|
| 联系人 | `Contacts` | 单个联系人信息 |
| 公司 | `Accounts` | 组织/企业信息 |
| 销售流程 | `Pipelines` | 销售机会/交易信息 |
| 产品 | `Products` | 您销售的产品信息 |
| 任务 | `Tasks` | 待办事项（需要额外的 OAuth 权限） |
| 事件 | `Events` | 日历预约（需要额外的 OAuth 权限） |
| 通话 | `Calls` | 电话通话记录（需要额外的 OAuth 权限） |
| 备注 | `Notes` | 附加到记录的备注（需要额外的 OAuth 权限） |

### 列出记录

```bash
GET /zoho-bigin/bigin/v2/{module_api_name}?fields={field1},{field2}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `fields` | 字符串 | **必填。** 以逗号分隔的字段名称，用于检索数据 |
| `sort_order` | 字符串 | `asc` 或 `desc` | 排序方式 |
| `sort_by` | 字符串 | 排序依据的字段名称 |
| `page` | 整数 | 页码（默认：1） |
| `per_page` | 整数 | 每页显示的记录数（默认：200，最大：200） |
| `cvid` | 字符串 | 过滤结果的自定义视图 ID |

**示例 - 列出联系人：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts?fields=First_Name,Last_Name,Email,Phone')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "First_Name": "Ted",
      "Email": "support@bigin.com",
      "Last_Name": "Watson",
      "id": "7255024000000596045"
    }
  ],
  "info": {
    "per_page": 200,
    "count": 1,
    "page": 1,
    "more_records": false
  }
}
```

**示例 - 列出公司（Accounts）：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Accounts?fields=Account_Name,Website')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取记录信息

```bash
GET /zoho-bigin/bigin/v2/{module_api_name}/{record_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts/7255024000000596045')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建记录

```bash
POST /zoho-bigin/bigin/v2/{module_api_name}
Content-Type: application/json

{
  "data": [
    {
      "field_api_name": "value"
    }
  ]
}
```

**各模块的必填字段：**

| 模块 | 必填字段 |
|--------|-----------------|
| 联系人 | `Last_Name` | 姓氏 |
| 公司 | `Account_Name` | 公司名称 |
| 销售流程 | `Pipeline_Name` | 销售流程名称 |
| 产品 | `Product_Name` | 产品名称 |

**示例 - 创建联系人：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "Last_Name": "Smith",
        "First_Name": "John",
        "Email": "john.smith@example.com",
        "Phone": "+1-555-0123"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "code": "SUCCESS",
      "details": {
        "Modified_Time": "2026-02-06T00:28:53-08:00",
        "Modified_By": {
          "name": "User Name",
          "id": "7255024000000590001"
        },
        "Created_Time": "2026-02-06T00:28:53-08:00",
        "id": "7255024000000605002",
        "Created_By": {
          "name": "User Name",
          "id": "7255024000000590001"
        }
      },
      "message": "record added",
      "status": "success"
    }
  ]
}
```

**示例 - 创建公司（Accounts）：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "Account_Name": "Acme Corporation",
        "Website": "https://acme.com"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Accounts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 更新记录

```bash
PUT /zoho-bigin/bigin/v2/{module_api_name}
Content-Type: application/json

{
  "data": [
    {
      "id": "record_id",
      "field_api_name": "updated_value"
    }
  ]
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "id": "7255024000000605002",
        "Phone": "+1-555-9999"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts', data=data, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "code": "SUCCESS",
      "details": {
        "Modified_Time": "2026-02-06T00:29:07-08:00",
        "id": "7255024000000605002"
      },
      "message": "record updated",
      "status": "success"
    }
  ]
}
```

### 删除记录

```bash
DELETE /zoho-bigin/bigin/v2/{module_api_name}?ids={record_id1},{record_id2}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `ids` | 字符串 | 以逗号分隔的记录 ID（最多 100 个） |
| `wf_trigger` | 布尔值 | 是否执行工作流（默认：true） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts?ids=7255024000000605002', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "code": "SUCCESS",
      "details": {
        "id": "7255024000000605002"
      },
      "message": "record deleted",
      "status": "success"
    }
  ]
}
```

### 搜索记录

```bash
GET /zoho-bigin/bigin/v2/{module_api_name}/search
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `criteria` | 字符串 | 搜索条件（例如：`(Last_Name:equals:Smith)` |
| `email` | 字符串 | 按电子邮件地址搜索 |
| `phone` | 字符串 | 按电话号码搜索 |
| `word` | 字符串 | 全文搜索 |
| `page` | 整数 | 页码 |
| `per_page` | 整数 | 每页显示的记录数（最大：200） |

**搜索条件格式：** `((field_api_name:operator:value)and/or(...))`

**操作符：** `equals`, `starts_with`

**示例 - 按电子邮件搜索：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts/search?email=support@bigin.com')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例 - 根据条件搜索：**

```bash
python <<'EOF'
import urllib.request, os, json
import urllib.parse
criteria = urllib.parse.quote('(Last_Name:equals:Watson)')
req = urllib.request.Request(f'https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts/search?criteria={criteria}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 元数据 API

#### 获取模块信息

```bash
GET /zoho-bigin/bigin/v2/settings/modules
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/settings/modules')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取用户信息

```bash
GET /zoho-bigin/bigin/v2/users
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `type` | 字符串 | `AllUsers`, `ActiveUsers`, `AdminUsers`, `CurrentUser` |
| `page` | 整数 | 页码 |
| `per_page` | 整数 | 每页显示的用户数（最大：200） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-bigin/bigin/v2/users?type=ActiveUsers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 分页

Zoho Bigin 使用 `page` 和 `per_page` 参数进行分页：

```bash
GET /zoho-bigin/bigin/v2/{module_api_name}?fields=First_Name,Last_Name&page=1&per_page=50
```

响应中包含分页信息：

```json
{
  "data": [...],
  "info": {
    "per_page": 50,
    "count": 50,
    "page": 1,
    "more_records": true
  }
}
```

当 `more_records` 为 `true` 时，继续获取更多记录，并每次迭代时增加 `page` 的值。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts?fields=First_Name,Last_Name,Email',
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
    'https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'fields': 'First_Name,Last_Name,Email'}
)
data = response.json()
```

## 注意事项：

- `fields` 参数是列表操作所必需的。
- 模块的 API 名称区分大小写（例如，使用 `Contacts` 而不是 `contacts`）。
- 公司信息通过 `Accounts` 模块的 API 访问。
- 销售机会信息通过 `Pipelines` 模块访问。
- 每次创建/更新请求最多允许 100 条记录。
- 每次删除请求最多允许 100 条记录。
- 每次 GET 请求最多返回 200 条记录。
- 在请求中使用字段的 API 名称（而不是显示名称）。
- 一些模块（如任务、事件、通话、备注）需要额外的 OAuth 权限。如果遇到权限问题，请联系 Maton 支持团队（support@maton.ai），并提供具体的操作、API 和使用场景。
- **重要提示：** 当 URL 中包含括号时，使用 `curl -g` 以避免全局解析问题。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Zoho Bigin 连接，缺少必需参数，或请求无效 |
| 401 | Maton API 密钥无效或缺失，或 OAuth 权限不匹配 |
| 404 | URL 格式无效或资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Zoho Bigin API 的传递错误 |

### 常见错误代码

| 代码 | 描述 |
|------|-------------|
| `REQUIRED_PARAM_MISSING` | 必需参数（如 `fields`）缺失 |
| `INVALID_URL_PATTERN` | API 端点路径无效 |
| `INVALID_MODULE` | 模块不存在或不受 API 支持 |
| `OAUTH_SCOPE_MISMATCH` | OAuth 令牌缺乏访问该端点所需的权限 |
| `NO_PERMISSION` | 操作权限不足 |
| `MANDATORY_NOT_FOUND` | 必需字段缺失 |
| `INVALID_DATA` | 数据类型不匹配或格式错误 |
| `DUPLICATE_DATA` | 记录违反了唯一性约束 |

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

### 故障排除：应用程序名称错误

1. 确保您的 URL 路径以 `zoho-bigin` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/zoho-bigin/bigin/v2/Contacts`
- 错误的路径：`https://gateway.maton.ai/bigin/v2/Contacts`

## 资源

- [Bigin API 概述](https://www.bigin.com/developer/docs/apis/v2/)
- [Bigin REST API 文档](https://www.bigin.com/developer/docs/apis/)
- [模块 API](https://www.bigin.com/developer/docs/apis/modules-api.html)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)