---
name: hubspot
description: |
  HubSpot CRM API integration with managed OAuth. Manage contacts, companies, deals, and associations. Use this skill when users want to create or update CRM records, search contacts, or sync data with HubSpot. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# HubSpot

您可以使用托管的 OAuth 认证来访问 HubSpot CRM API，从而创建和管理联系人、公司、交易及其关联关系。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/hubspot/crm/v3/objects/contacts?limit=10&properties=email,firstname,lastname')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/hubspot/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 HubSpot API 端点路径。该网关会将请求代理到 `api.hubapi.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 管理您的 HubSpot OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=hubspot&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'hubspot'}).encode()
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
    "app": "hubspot",
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

如果您有多个 HubSpot 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/hubspot/crm/v3/objects/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 联系人

#### 列出联系人

```bash
GET /hubspot/crm/v3/objects/contacts?limit=100&properties=email,firstname,lastname,phone
```

支持分页：

```bash
GET /hubspot/crm/v3/objects/contacts?limit=100&properties=email,firstname&after={cursor}
```

#### 获取联系人信息

```bash
GET /hubspot/crm/v3/objects/contacts/{contactId}?properties=email,firstname,lastname
```

#### 创建联系人

```bash
POST /hubspot/crm/v3/objects/contacts
Content-Type: application/json

{
  "properties": {
    "email": "john@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "phone": "+1234567890"
  }
}
```

#### 更新联系人信息

```bash
PATCH /hubspot/crm/v3/objects/contacts/{contactId}
Content-Type: application/json

{
  "properties": {
    "phone": "+0987654321"
  }
}
```

#### 删除联系人

```bash
DELETE /hubspot/crm/v3/objects/contacts/{contactId}
```

#### 搜索联系人

```bash
POST /hubspot/crm/v3/objects/contacts/search
Content-Type: application/json

{
  "filterGroups": [{
    "filters": [{
      "propertyName": "email",
      "operator": "EQ",
      "value": "john@example.com"
    }]
  }],
  "properties": ["email", "firstname", "lastname"]
}
```

### 公司

#### 列出公司

```bash
GET /hubspot/crm/v3/objects/companies?limit=100&properties=name,domain,industry
```

#### 获取公司信息

```bash
GET /hubspot/crm/v3/objects/companies/{companyId}?properties=name,domain,industry
```

#### 创建公司

```bash
POST /hubspot/crm/v3/objects/companies
Content-Type: application/json

{
  "properties": {
    "name": "Acme Corp",
    "domain": "acme.com",
    "industry": "COMPUTER_SOFTWARE"
  }
}
```

**注意：** `industry` 属性需要特定的枚举值（例如 `COMPUTER_SOFTWARE`、`FINANCE`、`HEALTHCARE`）。请使用 `List Properties` 端点获取有效的值。

#### 更新公司信息

```bash
PATCH /hubspot/crm/v3/objects/companies/{companyId}
Content-Type: application/json

{
  "properties": {
    "industry": "COMPUTER_SOFTWARE",
    "numberofemployees": "50"
  }
}
```

#### 删除公司

```bash
DELETE /hubspot/crm/v3/objects/companies/{companyId}
```

#### 搜索公司

```bash
POST /hubspot/crm/v3/objects/companies/search
Content-Type: application/json

{
  "filterGroups": [{
    "filters": [{
      "propertyName": "domain",
      "operator": "CONTAINS_TOKEN",
      "value": "*"
    }]
  }],
  "properties": ["name", "domain"],
  "limit": 10
}
```

### 交易

#### 列出交易

```bash
GET /hubspot/crm/v3/objects/deals?limit=100&properties=dealname,amount,dealstage
```

#### 获取交易信息

```bash
GET /hubspot/crm/v3/objects/deals/{dealId}?properties=dealname,amount,dealstage
```

#### 创建交易

```bash
POST /hubspot/crm/v3/objects/deals
Content-Type: application/json

{
  "properties": {
    "dealname": "New Deal",
    "amount": "10000",
    "dealstage": "appointmentscheduled"
  }
}
```

#### 更新交易信息

```bash
PATCH /hubspot/crm/v3/objects/deals/{dealId}
Content-Type: application/json

{
  "properties": {
    "amount": "15000",
    "dealstage": "qualifiedtobuy"
  }
}
```

#### 删除交易

```bash
DELETE /hubspot/crm/v3/objects/deals/{dealId}
```

### 关联关系（v4 API）

#### 关联对象

```bash
PUT /hubspot/crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/{toObjectType}/{toObjectId}
Content-Type: application/json

[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 279}]
```

常见的关联类型 ID：
- `279` - 联系人与公司之间的关联
- `3` - 交易与联系人之间的关联
- `341` - 交易与公司之间的关联

#### 列出关联关系

```bash
GET /hubspot/crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}
```

### 批量操作

#### 批量读取

```bash
POST /hubspot/crm/v3/objects/{objectType}/batch/read
Content-Type: application/json

{
  "properties": ["email", "firstname"],
  "inputs": [{"id": "123"}, {"id": "456"}]
}
```

#### 批量创建

```bash
POST /hubspot/crm/v3/objects/{objectType}/batch/create
Content-Type: application/json

{
  "inputs": [
    {"properties": {"email": "one@example.com", "firstname": "One"}},
    {"properties": {"email": "two@example.com", "firstname": "Two"}}
  ]
}
```

#### 批量更新

```bash
POST /hubspot/crm/v3/objects/{objectType}/batch/update
Content-Type: application/json

{
  "inputs": [
    {"id": "123", "properties": {"firstname": "Updated"}},
    {"id": "456", "properties": {"firstname": "Also Updated"}}
  ]
}
```

#### 批量归档

```bash
POST /hubspot/crm/v3/objects/{objectType}/batch/archive
Content-Type: application/json

{
  "inputs": [{"id": "123"}, {"id": "456"}]
}
```

### 属性

#### 列出属性

```bash
GET /hubspot/crm/v3/properties/{objectType}
```

## 搜索操作符

- `EQ` - 等于
- `NEQ` - 不等于
- `LT` / `LTE` - 小于 / 小于或等于
- `GT` / `GTE` - 大于 / 大于或等于
- `CONTAINS_TOKEN` - 包含指定字符串
- `NOT_CONTAINS_TOKEN` - 不包含指定字符串

## 分页

列表端点会返回一个 `paging.next.after` 值，用于获取下一页数据：

```json
{
  "results": [...],
  "paging": {
    "next": {
      "after": "12345"
    }
  }
}
```

使用 `after` 查询参数来获取下一页数据：

```bash
GET /hubspot/crm/v3/objects/contacts?limit=100&after=12345
```

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/hubspot/crm/v3/objects/contacts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({
    properties: { email: 'john@example.com', firstname: 'John' }
  })
});
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/hubspot/crm/v3/objects/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'properties': {'email': 'john@example.com', 'firstname': 'John'}}
)
```

## 注意事项

- 每次请求最多支持 100 条记录的批量操作。
- 归档/删除操作属于“软删除”操作——记录可以在 90 天内恢复。
- 删除操作成功时返回 HTTP 204（无内容）状态码。
- 公司的 `industry` 属性需要特定的枚举值。
- **重要提示：** 当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 参数来禁用全局解析。
- **重要提示：** 在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致“无效 API 密钥”错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 HubSpot 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次请求） |
| 4xx/5xx | 来自 HubSpot API 的传递错误 |

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

1. 确保您的 URL 路径以 `hubspot` 开头。例如：
  - 正确的路径：`https://gateway.maton.ai/hubspot/crm/v3/objects/contacts`
  - 错误的路径：`https://gateway.maton.ai/crm/v3/objects/contacts`

## 资源

- [HubSpot API 概述](https://developers.hubspot.com/docs/api/overview)
- [列出联系人](https://developers.hubspot.com/docs/api-reference/crm-contacts-v3/basic/get-crm-v3-objects-contacts.md)
- [创建联系人](https://developers.hubspot.com/docs/api-reference/crm-contacts-v3/basic/post-crm-v3-objects-contacts.md)
- [搜索联系人](https://developers.hubspot.com/docs/api-reference/crm-contacts-v3/search/post-crm-v3-objects-contacts-search.md)
- [列出公司](https://developers.hubspot.com/docs/api-reference/crm-companies-v3/basic/get-crm-v3-objects-companies.md)
- [创建公司](https://developers.hubspot.com/docs/api-reference/crm-companies-v3/basic/post-crm-v3-objects-companies.md)
- [列出交易](https://developers.hubspot.com/docs/api-reference/crm-deals-v3/basic/get-crm-v3-objects-0-3.md)
- [创建交易](https://developers.hubspot.com/docs/api-reference/crm-deals-v3/basic/post-crm-v3-objects-0-3.md)
- [关联关系 API](https://developers.hubspot.com/docs/api-reference/crm-associations-v4/basic/get-crm-v4-objects-objectType-objectId-associations-toObjectType.md)
- [属性 API](https://developers.hubspot.com/docs/api-reference/crm-properties-v3/core/get-crm-v3-properties-objectType.md)
- [搜索参考](https://developers.hubspot.com/docs/api/crm/search)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)