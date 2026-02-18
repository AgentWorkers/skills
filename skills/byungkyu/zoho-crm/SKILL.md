---
name: zoho-crm
description: >
  **Zoho CRM API集成与托管式OAuth**  
  该功能允许用户通过OAuth身份验证机制，对Zoho CRM中的潜在客户（leads）、联系人（contacts）、账户（accounts）、交易（deals）及其他CRM记录进行读取、创建、更新或删除操作。同时，用户还可以搜索联系人信息、管理销售流程（sales pipelines）、访问组织设置（organization settings）、管理用户（users），以及获取模块元数据（module metadata）。  
  **适用场景**：  
  当用户需要执行以下操作时，可使用此功能：  
  - 读取或修改Zoho CRM中的数据  
  - 创建新的CRM记录  
  - 更新现有CRM记录  
  - 删除不必要的CRM记录  
  - 搜索特定的联系人  
  - 管理销售流程  
  - 访问组织配置信息  
  - 管理用户账户  
  - 获取模块的相关元数据  
  **注意事项**：  
  - 使用此功能需要具备网络连接权限以及有效的Maton API密钥（valid Maton API key）。  
  - 对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）进行集成。  
  **技术要求**：  
  - 支持OAuth身份验证机制  
  - 需要网络访问权限  
  - 需要有效的Maton API密钥  
  **推荐使用场景**：  
  - 企业级销售管理系统（CRM）集成  
  - 自动化数据同步工具  
  - 客户关系管理（CRM）系统扩展  
  **注意事项**：  
  - 请确保您的应用程序已正确配置OAuth认证参数。  
  - 如遇到授权问题，请检查Maton API密钥的有效性及网络连接状态。
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---
# Zoho CRM

您可以使用受管理的 OAuth 认证来访问 Zoho CRM API。通过完整的 CRUD 操作（包括搜索和批量操作），您可以管理潜在客户（Leads）、联系人（Contacts）、账户（Accounts）、销售机会（Deals）以及其他 CRM 模块。此外，该 API 还支持组织详情、用户管理以及模块元数据的检索。

## 快速入门

```bash
# List leads
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads?fields=First_Name,Last_Name,Email')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-crm/crm/v8/{endpoint}
```

该网关会将请求代理到 `www.zohoapis.com/crm/v8`，并自动插入您的 OAuth 令牌。

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

1. 在 [maton.ai](https://maton.ai) 上登录或创建一个账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Zoho CRM OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-crm&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-crm'}).encode()
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
    "connection_id": "e55c5bac-241a-4cc8-9db5-50d2cad09136",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoho-crm",
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

如果您有多个 Zoho CRM 连接，请使用 `Maton-Connection` 头指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads?fields=First_Name,Last_Name,Email')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'e55c5bac-241a-4cc8-9db5-50d2cad09136')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 模块

Zoho CRM 将数据组织成不同的模块。核心模块包括：

| 模块 | API 名称 | 描述 |
|--------|----------|-------------|
| 潜在客户（Leads） | `Leads` | 潜在客户 |
| 联系人（Contacts） | `Contacts` | 个人信息 |
| 账户（Accounts） | `Accounts` | 组织/公司 |
| 销售机会（Deals） | `Deals` | 销售机会 |
| 营销活动（Campaigns） | `Campaigns` | 营销活动 |
| 任务（Tasks） | `Tasks` | 待办事项 |
| 通话记录（Calls） | `Calls` | 电话通话记录 |
| 活动（Events） | `Events` | 日历约会 |
| 产品（Products） | `Products` | 产品信息 |

### 列出记录

```bash
GET /zoho-crm/crm/v8/{module_api_name}?fields={field1},{field2}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `fields` | 字符串 | **必填。** 以逗号分隔的字段 API 名称（最多 50 个） |
| `page` | 整数 | 页码（默认：1） |
| `per_page` | 整数 | 每页记录数（默认/最大：200） |
| `sort_by` | 字符串 | 排序方式：`id`、`Created_Time` 或 `Modified_Time` |
| `sort_order` | 字符串 | `asc` 或 `desc`（默认） |
| `cvid` | 长整型 | 自定义视图 ID |
| `page_token` | 字符串 | 当记录数超过 2000 时用于分页 |

**示例 - 列出潜在客户：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads?fields=First_Name,Last_Name,Email,Phone,Company')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "First_Name": "Christopher",
      "Email": "christopher-maclead@noemail.invalid",
      "Last_Name": "Maclead (Sample)",
      "Phone": "555-555-5555",
      "Company": "Rangoni Of Florence",
      "id": "7243485000000597000"
    }
  ],
  "info": {
    "per_page": 200,
    "count": 1,
    "page": 1,
    "sort_by": "id",
    "sort_order": "desc",
    "more_records": false,
    "next_page_token": null
  }
}
```

**示例 - 列出联系人：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Contacts?fields=First_Name,Last_Name,Email,Phone')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例 - 列出账户：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Accounts?fields=Account_Name,Website,Phone')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例 - 列出销售机会：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Deals?fields=Deal_Name,Stage,Amount')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取记录

```bash
GET /zoho-crm/crm/v8/{module_api_name}/{record_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads/7243485000000597000')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建记录

```bash
POST /zoho-crm/crm/v8/{module_api_name}
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
| 潜在客户（Leads） | `Last_Name` |
| 联系人（Contacts） | `Last_Name` |
| 账户（Accounts） | `Account_Name` |
| 销售机会（Deals） | `Deal_Name`, `Stage` |
| 任务（Tasks） | `Subject` |
| 通话记录（Calls） | `Subject`, `Call_Type`, `Call_Start_Time`, `Call_Duration` |
| 活动（Events） | `Event_Title`, `Start_DateTime`, `End_DateTime` |

**示例 - 创建潜在客户：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "Last_Name": "Smith",
        "First_Name": "John",
        "Email": "john.smith@example.com",
        "Company": "Acme Corp",
        "Phone": "+1-555-0123"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads', data=data, method='POST')
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
        "Modified_Time": "2026-02-06T01:10:56-08:00",
        "Modified_By": {
          "name": "User Name",
          "id": "7243485000000590001"
        },
        "Created_Time": "2026-02-06T01:10:56-08:00",
        "id": "7243485000000619001",
        "Created_By": {
          "name": "User Name",
          "id": "7243485000000590001"
        }
      },
      "message": "record added",
      "status": "success"
    }
  ]
}
```

**示例 - 创建联系人：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "Last_Name": "Doe",
        "First_Name": "Jane",
        "Email": "jane.doe@example.com",
        "Phone": "+1-555-9876"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Contacts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例 - 创建账户：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "Account_Name": "Acme Corporation",
        "Website": "https://acme.com",
        "Phone": "+1-555-1234"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Accounts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 更新记录

```bash
PUT /zoho-crm/crm/v8/{module_api_name}
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
        "id": "7243485000000619001",
        "Phone": "+1-555-9999",
        "Company": "Updated Company Name"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads', data=data, method='PUT')
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
        "Modified_Time": "2026-02-06T01:11:01-08:00",
        "Modified_By": {
          "name": "User Name",
          "id": "7243485000000590001"
        },
        "Created_Time": "2026-02-06T01:10:56-08:00",
        "id": "7243485000000619001",
        "Created_By": {
          "name": "User Name",
          "id": "7243485000000590001"
        }
      },
      "message": "record updated",
      "status": "success"
    }
  ]
}
```

### 删除记录

```bash
DELETE /zoho-crm/crm/v8/{module_api_name}?ids={record_id1},{record_id2}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `ids` | 字符串 | 以逗号分隔的记录 ID（必填，最多 100 个） |
| `wf_trigger` | 布尔值 | 是否执行工作流（默认：true） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads?ids=7243485000000619001', method='DELETE')
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
        "id": "7243485000000619001"
      },
      "message": "record deleted",
      "status": "success"
    }
  ]
}
```

### 搜索记录

```bash
GET /zoho-crm/crm/v8/{module_api_name}/search
```

**查询参数（至少需要一个）：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `criteria` | 字符串 | 搜索条件（例如：`(Last_Name:equals:Smith)` |
| `email` | 字符串 | 按电子邮件地址搜索 |
| `phone` | 字符串 | 按电话号码搜索 |
| `word` | 字符串 | 全文搜索 |
| `page` | 整数 | 页码 |
| `per_page` | 整数 | 每页记录数（最大 200） |

**条件格式：** `((field_api_name:operator:value) and/or (...))`

**操作符：**
- 文本字段：`equals`, `not_equal`, `starts_with`, `in`
- 日期/数字字段：`equals`, `not_equal`, `greater_than`, `less_than`, `between`, `in`
- 布尔字段：`equals`, `not_equal`

**示例 - 按电子邮件搜索：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/Leads/search?email=christopher-maclead@noemail.invalid')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例 - 根据条件搜索：**

```bash
python <<'EOF'
import urllib.request, os, json
import urllib.parse
criteria = urllib.parse.quote('(Last_Name:starts_with:Smith)')
req = urllib.request.Request(f'https://gateway.maton.ai/zoho-crm/crm/v8/Leads/search?criteria={criteria}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "First_Name": "Christopher",
      "Email": "christopher-maclead@noemail.invalid",
      "Last_Name": "Maclead (Sample)",
      "id": "7243485000000597000"
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

### 组织详情

检索您的 Zoho CRM 组织详情。

```bash
GET /zoho-crm/crm/v8/org
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/org')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "org": [
    {
      "id": "7243485000000020005",
      "company_name": "Acme Corp",
      "domain_name": "org123456789",
      "primary_email": "admin@example.com",
      "phone": "555-555-5555",
      "currency": "US Dollar - USD",
      "currency_symbol": "$",
      "iso_code": "USD",
      "time_zone": "PST",
      "country_code": "US",
      "zgid": "123456789",
      "type": "production",
      "mc_status": false,
      "license_details": {
        "paid": true,
        "paid_type": "enterprise",
        "users_license_purchased": 10,
        "trial_expiry": null
      }
    }
  ]
}
```

### 用户

检索您 Zoho CRM 组织中的用户。

```bash
GET /zoho-crm/crm/v8/users
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `type` | 字符串 | 按用户类型过滤：`AllUsers`, `ActiveUsers`, `DeactiveUsers`, `ConfirmedUsers`, `NotConfirmedUsers`, `DeletedUsers`, `ActiveConfirmedUsers`, `AdminUsers`, `ActiveConfirmedAdmins`, `CurrentUser` |
| `page` | 整数 | 页码（默认：1） |
| `per_page` | 整数 | 每页记录数（默认/最大：200） |
| `ids` | 字符串 | 以逗号分隔的用户 ID（最多 100 个） |

**示例 - 列出所有用户：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/users?type=AllUsers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "users": [
    {
      "id": "7243485000000590001",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "status": "active",
      "confirm": true,
      "role": {
        "name": "CEO",
        "id": "7243485000000026005"
      },
      "profile": {
        "name": "Administrator",
        "id": "7243485000000026011"
      },
      "time_zone": "PST",
      "country": "US",
      "locale": "en_US"
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

**示例 - 获取特定用户：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/users/7243485000000590001')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 模块元数据

检索所有可用 CRM 模块的元数据。

```bash
GET /zoho-crm/crm/v8/settings/modules
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `status` | 字符串 | 按状态过滤：`user_hidden`, `system_hidden`, `scheduled_for_deletion`, `visible` |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/settings/modules')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "modules": [
    {
      "api_name": "Leads",
      "module_name": "Leads",
      "singular_label": "Lead",
      "plural_label": "Leads",
      "api_supported": true,
      "creatable": true,
      "editable": true,
      "deletable": true,
      "viewable": true,
      "status": "visible",
      "generated_type": "default",
      "id": "7243485000000002175",
      "profiles": [
        {"name": "Administrator", "id": "7243485000000026011"}
      ]
    }
  ]
}
```

### 字段元数据

检索特定模块的字段元数据。

```bash
GET /zoho-crm/crm/v8/settings/fields?module={module_api_name}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `module` | 字符串 | **必填。** 模块的 API 名称（例如：`Leads`, `Contacts`） |
| `type` | 字符串 | `all` 表示所有字段；`unused` 表示仅获取未使用的字段 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/settings/fields?module=Leads')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "fields": [
    {
      "api_name": "Last_Name",
      "field_label": "Last Name",
      "data_type": "text",
      "system_mandatory": true,
      "custom_field": false,
      "visible": true,
      "searchable": true,
      "sortable": true,
      "id": "7243485000000002613"
    }
  ]
}
```

### 布局元数据

检索特定模块的布局元数据。

```bash
GET /zoho-crm/crm/v8/settings/layouts?module={module_api_name}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `module` | 字符串 | **必填。** 模块的 API 名称（例如：`Leads`, `Contacts`） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/settings/layouts?module=Leads')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "layouts": [
    {
      "id": "7243485000000091055",
      "name": "Standard",
      "api_name": "Standard",
      "status": "active",
      "visible": true,
      "profiles": [
        {"name": "Administrator", "id": "7243485000000026011"}
      ],
      "sections": [
        {
          "display_label": "Lead Information",
          "api_name": "Lead_Information",
          "sequence_number": 1,
          "fields": [...]
        }
      ]
    }
  ]
}
```

### 角色

检索您 Zoho CRM 组织中的角色。

```bash
GET /zoho-crm/crm/v8/settings/roles
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/settings/roles')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**示例 - 获取特定角色：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/settings/roles/7243485000000026005')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 配置文件（Profiles）

检索您 Zoho CRM 组织中的配置文件（权限设置）。

```bash
GET /zoho-crm/crm/v8/settings/profiles
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/settings/profiles')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "profiles": [
    {
      "id": "7243485000000026011",
      "name": "Administrator",
      "display_label": "Administrator",
      "type": "normal_profile",
      "custom": false,
      "description": null
    },
    {
      "id": "7243485000000026014",
      "name": "Standard",
      "display_label": "Standard",
      "type": "normal_profile",
      "custom": false,
      "description": null
    }
  ]
}
```

**示例 - 获取特定配置文件：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-crm/crm/v8/settings/profiles/7243485000000026011')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 分页

Zoho CRM 使用基于页面的分页机制，对于大型数据集提供了可选的页码令牌：

```bash
GET /zoho-crm/crm/v8/{module_api_name}?fields=First_Name,Last_Name&page=1&per_page=50
```

响应中包含分页信息：

```json
{
  "data": [...],
  "info": {
    "per_page": 50,
    "count": 50,
    "page": 1,
    "sort_by": "id",
    "sort_order": "desc",
    "more_records": true,
    "next_page_token": "token_value",
    "page_token_expiry": "2026-02-07T01:10:56-08:00"
  }
}
```

- 对于最多 2,000 条记录：使用 `page` 参数（每次请求递增页码）
- 对于超过 2,000 条记录：使用上一次响应中的 `page_token`
- 页码令牌在 24 小时后失效

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-crm/crm/v8/Leads?fields=First_Name,Last_Name,Email',
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
    'https://gateway.maton.ai/zoho-crm/crm/v8/Leads',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'fields': 'First_Name,Last_Name,Email'}
)
data = response.json()
```

## 注意事项

- `fields` 参数在列表操作中是 **必填的**（最多 50 个字段）
- 模块的 API 名称区分大小写（例如：`Leads`，而不是 `leads`）
- 创建/更新请求每次最多处理 100 条记录
- 删除请求每次最多处理 100 条记录
- 获取请求每次最多返回 200 条记录
- 不使用页码令牌时最多返回 2,000 条记录；使用页码令牌时最多返回 100,000 条记录
- 在请求中使用字段的 API 名称（而不是显示名称）
- 如果收到范围错误，请联系 Maton 支持团队（support@maton.ai），并提供具体的操作、API 和使用场景
- 空数据集会返回 HTTP 204（No Content）状态码且内容为空
- **重要提示：** 当 URL 包含括号时，使用 `curl -g` 选项来禁用全局解析
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少 Zoho CRM 连接、缺少必填参数或请求无效 |
| 401 | Maton API 密钥无效或缺失，或者 OAuth 范围不匹配 |
| 404 | 资源未找到 |
| 429 | 请求次数限制 |
| 4xx/5xx | 来自 Zoho CRM API 的传递错误 |

### 常见错误代码

| 代码 | 描述 |
|------|-------------|
| `OAUTH_SCOPE_MISMATCH` | OAuth 令牌缺乏访问该端点的所需权限 |
| `MANDATORY_NOT_FOUND` | 必填字段缺失 |
| `INVALID_DATA` | 数据类型不匹配或格式错误 |
| `DUPLICATE_DATA` | 记录违反了唯一性字段约束 |
| `RECORD_NOT_FOUND` | 指定的记录 ID 不存在 |

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

1. 确保您的 URL 路径以 `zoho-crm` 开头。例如：

- 正确：`https://gateway.maton.ai/zoho-crm/crm/v8/Leads`
- 错误：`https://gateway.maton.ai/crm/v8/Leads`

## 资源

- [Zoho CRM API v8 文档](https://www.zoho.com/crm/developer/docs/api/v8/)
- [获取记录 API](https://www.zoho.com/crm/developer/docs/api/v8/get-records.html)
- [插入记录 API](https://www.zoho.com/crm/developer/docs/api/v8/insert-records.html)
- [更新记录 API](https://www.zoho.com/crm/developer/docs/api/v8/update-records.html)
- [删除记录 API](https://www.zoho.com/crm/developer/docs/api/v8/delete-records.html)
- [搜索记录 API](https://www.zoho.com/crm/developer/docs/api/v8/search-records.html)
- [组织 API](https://www.zoho.com/crm/developer/docs/api/v8/get-org-data.html)
- [用户 API](https://www.zoho.com/crm/developer/docs/api/v8/get-users.html)
- [模块 API](https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
- [字段 API](https://www.zoho.com/crm/developer/docs/api/v8/field-meta.html)
- [布局 API](https://www.zoho.com/crm/developer/docs/api/v8layouts-meta.html)
- [角色 API](https://www.zoho.com/crm/developer/docs/api/v8/get-roles.html)
- [配置文件 API](https://www.zoho.com/crm/developer/docs/api/v8/get-profiles.html)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)