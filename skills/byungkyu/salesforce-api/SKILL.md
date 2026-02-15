---
name: salesforce
description: |
  Salesforce CRM API integration with managed OAuth. Query records with SOQL, manage sObjects (Contacts, Accounts, Leads, Opportunities), and perform batch operations. Use this skill when users want to interact with Salesforce data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Salesforce

您可以使用托管的 OAuth 认证来访问 Salesforce REST API。通过 SOQL 查询记录、管理 sObjects，并对 Salesforce 数据执行创建（Create）、读取（Read）、更新（Update）和删除（Delete，简称 CRUD）操作。

## 快速入门

```bash
# Query contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/salesforce/services/data/v59.0/query?q=SELECT+Id,Name,Email+FROM+Contact+LIMIT+10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/salesforce/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Salesforce REST API 端点路径。该网关会将请求代理到 `{instance}.salesforce.com`（会根据您的连接配置自动替换），并插入您的访问令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Salesforce OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=salesforce&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'salesforce'}).encode()
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
    "app": "salesforce",
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

如果您有多个 Salesforce 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/salesforce/services/data/v59.0/sobjects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### SOQL 查询

```bash
GET /salesforce/services/data/v59.0/query?q=SELECT+Id,Name+FROM+Contact+LIMIT+10
```

复杂查询示例：

```bash
GET /salesforce/services/data/v59.0/query?q=SELECT+Id,Name,Email+FROM+Contact+WHERE+Email+LIKE+'%example.com'+ORDER+BY+CreatedDate+DESC
```

### 获取对象信息

```bash
GET /salesforce/services/data/v59.0/sobjects/{objectType}/{recordId}
```

示例：

```bash
GET /salesforce/services/data/v59.0/sobjects/Contact/003XXXXXXXXXXXXXXX
```

### 创建对象

```bash
POST /salesforce/services/data/v59.0/sobjects/{objectType}
Content-Type: application/json

{
  "FirstName": "John",
  "LastName": "Doe",
  "Email": "john@example.com"
}
```

### 更新对象

```bash
PATCH /salesforce/services/data/v59.0/sobjects/{objectType}/{recordId}
Content-Type: application/json

{
  "Phone": "+1234567890"
}
```

### 删除对象

```bash
DELETE /salesforce/services/data/v59.0/sobjects/{objectType}/{recordId}
```

### 描述对象（获取对象结构）

```bash
GET /salesforce/services/data/v59.0/sobjects/{objectType}/describe
```

### 列出对象

```bash
GET /salesforce/services/data/v59.0/sobjects
```

### 搜索（SOSL）

```bash
GET /salesforce/services/data/v59.0/search?q=FIND+{searchTerm}+IN+ALL+FIELDS+RETURNING+Contact(Id,Name)
```

### 组合请求（批量执行多个操作）

```bash
POST /salesforce/services/data/v59.0/composite
Content-Type: application/json

{
  "compositeRequest": [
    {
      "method": "GET",
      "url": "/services/data/v59.0/sobjects/Contact/003XXXXXXX",
      "referenceId": "contact1"
    },
    {
      "method": "GET",
      "url": "/services/data/v59.0/sobjects/Account/001XXXXXXX",
      "referenceId": "account1"
    }
  ]
}
```

### 组合批量请求

```bash
POST /salesforce/services/data/v59.0/composite/batch
Content-Type: application/json

{
  "batchRequests": [
    {"method": "GET", "url": "v59.0/sobjects/Contact/003XXXXXXX"},
    {"method": "GET", "url": "v59.0/sobjects/Account/001XXXXXXX"}
  ]
}
```

### 创建 sObject 集合（批量创建）

```bash
POST /salesforce/services/data/v59.0/composite/sobjects
Content-Type: application/json

{
  "allOrNone": true,
  "records": [
    {"attributes": {"type": "Contact"}, "FirstName": "John", "LastName": "Doe"},
    {"attributes": {"type": "Contact"}, "FirstName": "Jane", "LastName": "Smith"}
  ]
}
```

### 删除 sObject 集合（批量删除）

```bash
DELETE /salesforce/services/data/v59.0/composite/sobjects?ids=003XXXXX,003YYYYY&allOrNone=true
```

### 获取已更新的记录

```bash
GET /salesforce/services/data/v59.0/sobjects/{objectType}/updated/?start=2026-01-30T00:00:00Z&end=2026-02-01T00:00:00Z
```

### 获取已删除的记录

```bash
GET /salesforce/services/data/v59.0/sobjects/{objectType}/deleted/?start=2026-01-30T00:00:00Z&end=2026-02-01T00:00:00Z
```

### 获取 API 限制

```bash
GET /salesforce/services/data/v59.0/limits
```

### 列出 API 版本

```bash
GET /salesforce/services/data/
```

## 常见对象

- `Account` - 公司/组织
- `Contact` - 与账户关联的人员
- `Lead` - 潜在客户
- `Opportunity` - 销售机会
- `Case` - 支持案例
- `Task` - 待办事项
- `Event` - 日历事件

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/salesforce/services/data/v59.0/query?q=SELECT+Id,Name+FROM+Contact+LIMIT+5',
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
    'https://gateway.maton.ai/salesforce/services/data/v59.0/query',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'q': 'SELECT Id,Name FROM Contact LIMIT 5'}
)
```

## 注意事项

- 对 SOQL 查询使用 URL 编码（空格会转换为 `+`）。
- 记录 ID 是 15 或 18 个字符的字母数字字符串。
- API 版本（v59.0）可以调整；最新版本为 v65.0。
- 创建和删除操作成功时会返回 HTTP 204（无内容）状态码。
- 更新/删除操作的日期使用 ISO 8601 格式：`YYYY-MM-DDTHH:MM:SSZ`。
- 在批量操作中使用 `allOrNone: true` 以确保原子性交易。
- 重要提示：当 URL 包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Salesforce 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Salesforce API 的传递错误 |

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

1. 确保您的 URL 路径以 `salesforce` 开头。例如：
- 正确：`https://gateway.maton.ai/salesforce/services/data/v59.0/query`
- 错误：`https://gateway.maton.ai/services/data/v59.0/query`

## 资源

- [REST API 开发者指南](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/intro_rest.htm)
- [列出 sObjects](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/resources_describeGlobal.htm)
- [描述 sObject](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/resources_sobject_describe.htm)
- [获取记录](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/resources_sobject_retrieve_get.htm)
- [创建记录](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/dome_sobject_create.htm)
- [更新记录](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/dome_update_fields.htm)
- [删除记录](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/dome_delete_record.htm)
- [查询记录（SOQL）](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/resources_query.htm)
- [组合请求](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/resources_composite_composite_post.htm)
- [sObject 集合](https://developer.salesforce.com/docs/atlas.en-us.api/rest.meta/api_rest/resources_composite_sobjects_collections_create.htm)
- [SOQL 参考](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm)
- [SOSL 参考](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_sosl.htm)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)