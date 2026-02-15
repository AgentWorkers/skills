---
name: airtable
description: |
  Airtable API integration with managed OAuth. Manage bases, tables, and records. Use this skill when users want to read, create, update, or delete Airtable records, or query data with filter formulas. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Airtable

通过管理的 OAuth 认证来访问 Airtable API。您可以执行完整的 CRUD 操作（创建、读取、更新和删除）来管理数据库、表格和记录。

## 快速入门

```bash
# List records from a table
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/airtable/v0/{baseId}/{tableIdOrName}?maxRecords=100')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基础 URL

```
https://gateway.maton.ai/airtable/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Airtable API 端点路径。该网关会将请求代理到 `api.airtable.com` 并自动插入您的 OAuth 令牌。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Airtable OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=airtable&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'airtable'}).encode()
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
    "app": "airtable",
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

如果您有多个 Airtable 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/airtable/v0/appXXXXX/TableName')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 列出数据库

```bash
GET /airtable/v0/meta/bases
```

### 获取数据库架构

```bash
GET /airtable/v0/meta/bases/{baseId}/tables
```

### 列出记录

```bash
GET /airtable/v0/{baseId}/{tableIdOrName}?maxRecords=100
```

- 带视图：```bash
GET /airtable/v0/{baseId}/{tableIdOrName}?view=Grid%20view&maxRecords=100
```

- 带过滤公式：```bash
GET /airtable/v0/{baseId}/{tableIdOrName}?filterByFormula={Status}='Active'
```

- 带字段选择：```bash
GET /airtable/v0/{baseId}/{tableIdOrName}?fields[]=Name&fields[]=Status&fields[]=Email
```

- 带排序：```bash
GET /airtable/v0/{baseId}/{tableIdOrName}?sort[0][field]=Created&sort[0][direction]=desc
```

### 获取记录

```bash
GET /airtable/v0/{baseId}/{tableIdOrName}/{recordId}
```

### 创建记录

```bash
POST /airtable/v0/{baseId}/{tableIdOrName}
Content-Type: application/json

{
  "records": [
    {
      "fields": {
        "Name": "New Record",
        "Status": "Active",
        "Email": "test@example.com"
      }
    }
  ]
}
```

### 更新记录（PATCH - 部分更新）

```bash
PATCH /airtable/v0/{baseId}/{tableIdOrName}
Content-Type: application/json

{
  "records": [
    {
      "id": "recXXXXXXXXXXXXXX",
      "fields": {
        "Status": "Completed"
      }
    }
  ]
}
```

### 更新记录（PUT - 完整替换）

```bash
PUT /airtable/v0/{baseId}/{tableIdOrName}
Content-Type: application/json

{
  "records": [
    {
      "id": "recXXXXXXXXXXXXXX",
      "fields": {
        "Name": "Updated Name",
        "Status": "Active"
      }
    }
  ]
}
```

### 删除记录

```bash
DELETE /airtable/v0/{baseId}/{tableIdOrName}?records[]=recXXXXX&records[]=recYYYYY
```

## 分页

使用 `pageSize` 和 `offset` 进行分页：

```bash
GET /airtable/v0/{baseId}/{tableIdOrName}?pageSize=50&offset=itrXXXXXXXXXXX
```

当存在更多记录时，响应中会包含 `offset`：

```json
{
  "records": [...],
  "offset": "itrXXXXXXXXXXX"
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/airtable/v0/appXXXXX/TableName?maxRecords=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/airtable/v0/appXXXXX/TableName',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'maxRecords': 10}
)
```

## 注意事项

- 数据库 ID 以 `app` 开头。
- 表格 ID 以 `tbl` 开头（也可以使用表格名称）。
- 记录 ID 以 `rec` 开头。
- 每次创建/更新请求最多允许 100 条记录。
- 每次删除请求最多允许 10 条记录。
- 过滤公式使用 Airtable 的公式语法。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开，这可能导致 “无效的 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Airtable 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Airtable API 的传递错误 |

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

1. 确保您的 URL 路径以 `airtable` 开头。例如：
  - 正确的格式：`https://gateway.maton.ai/airtable/v0/{baseId}/{tableIdOrName}`
  - 错误的格式：`https://gateway.maton.ai/v0/{baseId}/{tableIdOrName}`

## 资源

- [Airtable API 概述](https://airtable.com/developers/web/api/introduction)
- [列出记录](https://airtable.com/developers/web/api/list-records)
- [创建记录](https://airtable.com/developers/web/api/create-records)
- [更新记录](https://airtable.com/developers/web/api/update-record)
- [删除记录](https://airtable.com/developers/web/api/delete-record)
- [公式参考](https://support.airtable.com/docs/formula-field-reference)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)