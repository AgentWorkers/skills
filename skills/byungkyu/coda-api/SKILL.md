---
name: coda
description: |
  Coda API integration with managed OAuth. Manage docs, pages, tables, rows, and formulas.
  Use this skill when users want to read, create, update, or delete Coda docs, pages, tables, or rows.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
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

# Coda

您可以使用受管理的 OAuth 认证来访问 Coda API。通过完整的 CRUD 操作（创建、读取、更新和删除），您可以管理文档、页面、表格、行、公式和控制项。

## 快速入门

```bash
# List your docs
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/coda/apis/v1/docs')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/coda/apis/v1/{resource}
```

请将 `{resource}` 替换为实际的 Coda API 端点路径。该网关会将请求代理到 `coda.io/apis/v1`，并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 管理您的 Coda OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=coda&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'coda'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接

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
    "connection_id": "f46d34b1-3735-478a-a0d7-54115a16cd46",
    "status": "ACTIVE",
    "creation_time": "2026-02-12T01:38:10.500238Z",
    "last_updated_time": "2026-02-12T01:38:33.545353Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "coda",
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

如果您有多个 Coda 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/coda/apis/v1/docs')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'f46d34b1-3735-478a-a0d7-54115a16cd46')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 账户

#### 获取当前用户

```bash
GET /coda/apis/v1/whoami
```

返回有关已认证用户的信息。

### 文档

#### 列出文档

```bash
GET /coda/apis/v1/docs
```

查询参数：
- `isOwner` - 仅显示您拥有的文档（true/false）
- `query` - 搜索查询
- `sourceDoc` - 按源文档 ID 过滤
- `isStarred` - 仅显示星标文档
- `inGallery` - 仅显示图库中的文档
- `workspaceId` - 按工作区过滤
- `folderId` - 按文件夹过滤
- `limit` - 页面大小（默认：25，最大：200）
- `pageToken` - 分页令牌

#### 创建文档

```bash
POST /coda/apis/v1/docs
Content-Type: application/json

{
  "title": "My New Doc",
  "sourceDoc": "optional-source-doc-id",
  "timezone": "America/Los_Angeles",
  "folderId": "optional-folder-id"
}
```

#### 获取文档

```bash
GET /coda/apis/v1/docs/{docId}
```

#### 删除文档

```bash
DELETE /coda/apis/v1/docs/{docId}
```

### 页面

#### 列出页面

```bash
GET /coda/apis/v1/docs/{docId}/pages
```

查询参数：
- `limit` - 页面大小
- `pageToken` - 分页令牌

#### 创建页面

```bash
POST /coda/apis/v1/docs/{docId}/pages
Content-Type: application/json

{
  "name": "New Page",
  "subtitle": "Optional subtitle",
  "parentPageId": "optional-parent-page-id"
}
```

#### 获取页面

```bash
GET /coda/apis/v1/docs/{docId}/pages/{pageIdOrName}
```

#### 更新页面

```bash
PUT /coda/apis/v1/docs/{docId}/pages/{pageIdOrName}
Content-Type: application/json

{
  "name": "Updated Page Name",
  "subtitle": "Updated subtitle"
}
```

#### 删除页面

```bash
DELETE /coda/apis/v1/docs/{docId}/pages/{pageIdOrName}
```

### 表格

#### 列出表格

```bash
GET /coda/apis/v1/docs/{docId}/tables
```

查询参数：
- `limit` - 页面大小
- `pageToken` - 分页令牌
- `sortBy` - 按字段排序
- `tableTypes` - 按表格类型过滤

#### 获取表格

```bash
GET /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}
```

### 列

#### 列出列

```bash
GET /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}/columns
```

查询参数：
- `limit` - 页面大小
- `pageToken` - 分页令牌

#### 获取列

```bash
GET /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}/columns/{columnIdOrName}
```

### 行

#### 列出行

```bash
GET /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}/rows
```

查询参数：
- `query` - 按搜索查询过滤行
- `useColumnNames` - 在响应中使用列名而不是 ID（true/false）
- `valueFormat` - 值格式（简单、简单带数组、丰富）
- `sortBy` - 按列排序
- `limit` - 页面大小
- `pageToken` - 分页令牌

#### 获取行

```bash
GET /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}/rows/{rowIdOrName}
```

查询参数：
- `useColumnNames` - 在响应中使用列名而不是 ID
- `valueFormat` - 值格式

#### 插入/更新行

```bash
POST /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}/rows
Content-Type: application/json

{
  "rows": [
    {
      "cells": [
        {"column": "Column Name", "value": "Cell Value"},
        {"column": "Another Column", "value": 123}
      ]
    }
  ],
  "keyColumns": ["Column Name"]
}
```

- 使用 `keyColumns` 来决定更新或插入行为（如果存在则更新，否则插入）
- 行的插入/更新是异步处理的（返回 requestId）

#### 更新行

```bash
PUT /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}/rows/{rowIdOrName}
Content-Type: application/json

{
  "row": {
    "cells": [
      {"column": "Column Name", "value": "Updated Value"}
    ]
  }
}
```

#### 删除行

```bash
DELETE /coda/apis/v1/docs/{docId}/tables/{tableIdOrName}/rows/{rowIdOrName}
```

### 公式

#### 列出公式

```bash
GET /coda/apis/v1/docs/{docId}/formulas
```

#### 获取公式

```bash
GET /coda/apis/v1/docs/{docId}/formulas/{formulaIdOrName}
```

### 控制项

#### 列出控制项

```bash
GET /coda/apis/v1/docs/{docId}/controls
```

#### 获取控制项

```bash
GET /coda/apis/v1/docs/{docId}/controls/{controlIdOrName}
```

### 权限

#### 获取共享元数据

```bash
GET /coda/apis/v1/docs/{docId}/acl/metadata
```

#### 列出权限

```bash
GET /coda/apis/v1/docs/{docId}/acl/permissions
```

#### 添加权限

```bash
POST /coda/apis/v1/docs/{docId}/acl/permissions
Content-Type: application/json

{
  "access": "readonly",
  "principal": {
    "type": "email",
    "email": "user@example.com"
  }
}
```

权限值：`readonly`、`write`、`comment`

#### 删除权限

```bash
DELETE /coda/apis/v1/docs/{docId}/acl/permissions/{permissionId}
```

### 分类

#### 列出分类

```bash
GET /coda/apis/v1/categories
```

### 实用工具

#### 解析浏览器链接

```bash
GET /coda/apis/v1/resolveBrowserLink?url={encodedUrl}
```

将 Coda 浏览器 URL 转换为 API 资源信息。

#### 获取变更状态

```bash
GET /coda/apis/v1/mutationStatus/{requestId}
```

检查异步变更操作的状态。

### 分析

#### 列出文档分析

```bash
GET /coda/apis/v1/analytics/docs
```

查询参数：
- `isPublished` - 按发布状态过滤
- `sinceDate` - 开始日期（YYYY-MM-DD）
- `untilDate` - 结束日期（YYYY-MM-DD）
- `limit` - 页面大小
- `pageToken` - 分页令牌

#### 列出包分析

```bash
GET /coda/apis/v1/analytics/packs
```

#### 获取分析更新时间

```bash
GET /coda/apis/v1/analytics/updated
```

## 分页

Coda 使用基于游标的分页机制，通过 `pageToken` 进行分页：

```bash
GET /coda/apis/v1/docs?limit=25
```

当存在更多结果时，响应中会包含 `nextPageToken`：

```json
{
  "items": [...],
  "href": "https://coda.io/apis/v1/docs?pageToken=...",
  "nextPageToken": "eyJsaW1..."
}
```

在后续请求中使用 `nextPageToken` 值作为 `pageToken`。

## 异步变更

创建、更新和删除操作会返回 HTTP 202 状态码，并附带一个 `requestId`：

```json
{
  "id": "canvas-abc123",
  "requestId": "mutate:9f038510-be42-4d16-bccf-3468d38efd57"
}
```

检查变更状态：

```bash
GET /coda/apis/v1/mutationStatus/mutate:9f038510-be42-4d16-bccf-3468d38efd57
```

响应：
```json
{
  "completed": true
}
```

变更通常在几秒钟内完成处理。

## 代码示例

### JavaScript - 列出文档

```javascript
const response = await fetch(
  'https://gateway.maton.ai/coda/apis/v1/docs?limit=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.items);
```

### Python - 列出文档

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/coda/apis/v1/docs',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
data = response.json()
for doc in data['items']:
    print(f"{doc['name']}: {doc['id']}")
```

### Python - 创建文档和页面

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
base_url = 'https://gateway.maton.ai/coda/apis/v1'

# Create doc
doc_response = requests.post(
    f'{base_url}/docs',
    headers=headers,
    json={'title': 'My New Doc'}
)
doc = doc_response.json()
print(f"Created doc: {doc['id']}")

# Create page
page_response = requests.post(
    f'{base_url}/docs/{doc["id"]}/pages',
    headers=headers,
    json={'name': 'First Page', 'subtitle': 'Created via API'}
)
page = page_response.json()
print(f"Created page: {page['id']}")
```

### Python - 插入行

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

response = requests.post(
    'https://gateway.maton.ai/coda/apis/v1/docs/{docId}/tables/{tableId}/rows',
    headers=headers,
    json={
        'rows': [
            {
                'cells': [
                    {'column': 'Name', 'value': 'John Doe'},
                    {'column': 'Email', 'value': 'john@example.com'}
                ]
            }
        ]
    }
)
result = response.json()
print(f"Request ID: {result['requestId']}")
```

## 注意事项

- 文档 ID 的格式为 `s0ekj2vV-v`。
- 页面 ID 以 `canvas-` 开头。
- 可以使用表格和列的名称代替 ID。
- 行的操作需要基于基础表格（而不是视图）。
- 创建/更新/删除操作是异步的（返回 requestId）。
- 新创建的文档可能需要一段时间才能通过 API 访问（可能会返回 409 错误）。
- 页面级别的分析需要 Enterprise 计划。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 时，环境变量可能无法正确展开。建议使用 Python 示例。

## 速率限制

| 操作 | 限制 |
|-----------|-------|
| 读取数据 | 每 6 秒 100 次请求 |
| 写入数据 | 每 6 秒 10 次请求 |
| 写入文档内容 | 每 10 秒 5 次请求 |
| 列出文档 | 每 6 秒 4 次请求 |
| 读取分析数据 | 每 6 秒 100 次请求 |

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Coda 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 409 | 文档尚未可用（刚刚创建） |
| 429 | 达到速率限制 |
| 4xx/5xx | 来自 Coda API 的传递错误 |

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

1. 确保您的 URL 路径以 `coda` 开头。例如：
- 正确：`https://gateway.maton.ai/coda/apis/v1/docs`
- 错误：`https://gateway.maton.ai/apis/v1/docs`

## 资源

- [Coda API 文档](https://coda.io/developers/apis/v1)
- [Coda API Postman 集合](https://www.postman.com/codaio/coda-workspace/collection/0vy7uxn/coda-api)
- [Coda API Python 库 (codaio)](https://codaio.readthedocs.io/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)