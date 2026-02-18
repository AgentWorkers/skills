---
name: google-bigquery
description: >
  **Google BigQuery API集成与托管式OAuth**  
  支持通过OAuth身份验证来访问Google BigQuery服务，从而执行SQL查询、管理数据集和表格，并进行大规模数据分析。  
  当用户需要查询BigQuery数据、创建或管理数据集/表格、运行分析任务或操作BigQuery资源时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
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
# Google BigQuery

您可以使用托管的 OAuth 认证来访问 Google BigQuery API。执行 SQL 查询、管理数据集和表格，并大规模分析数据。

## 快速入门

```bash
# Run a simple query
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'SELECT 1 as test_value', 'useLegacySql': False}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-bigquery/bigquery/v2/projects/{projectId}/queries', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-bigquery/bigquery/v2/{resource-path}
```

请将 `{resource-path}` 替换为实际的 BigQuery API 端点路径。该网关会将请求代理到 `bigquery.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Google BigQuery OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-bigquery&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-bigquery'}).encode()
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
    "connection_id": "c8463a31-e5b4-4e52-9a32-e78dcd7ba7b1",
    "status": "ACTIVE",
    "creation_time": "2026-02-14T09:02:02.780520Z",
    "last_updated_time": "2026-02-14T09:02:19.977436Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-bigquery",
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

如果您有多个 Google BigQuery 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-bigquery/bigquery/v2/projects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'c8463a31-e5b4-4e52-9a32-e78dcd7ba7b1')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 项目

#### 列出项目

列出已认证用户可以访问的所有项目。

```bash
GET /google-bigquery/bigquery/v2/projects
```

**响应：**
```json
{
  "kind": "bigquery#projectList",
  "projects": [
    {
      "id": "my-project-123",
      "numericId": "822245862053",
      "projectReference": {
        "projectId": "my-project-123"
      },
      "friendlyName": "My Project"
    }
  ],
  "totalItems": 1
}
```

### 数据集

#### 列出数据集

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/datasets
```

**查询参数：**
- `maxResults` - 返回的最大结果数量
- `pageToken` - 分页令牌
- `all` - 如果为 `true`，则包含隐藏的数据集

#### 获取数据集

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}
```

#### 创建数据集

```bash
POST /google-bigquery/bigquery/v2/projects/{projectId}/datasets
Content-Type: application/json

{
  "datasetReference": {
    "datasetId": "my_dataset",
    "projectId": "{projectId}"
  },
  "description": "My dataset description",
  "location": "US"
}
```

**响应：**
```json
{
  "kind": "bigquery#dataset",
  "id": "my-project:my_dataset",
  "datasetReference": {
    "datasetId": "my_dataset",
    "projectId": "my-project"
  },
  "location": "US",
  "creationTime": "1771059780773"
}
```

#### 更新数据集（PATCH）

```bash
PATCH /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}
Content-Type: application/json

{
  "description": "Updated description"
}
```

#### 删除数据集

```bash
DELETE /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}
```

**查询参数：**
- `deleteContents` - 如果为 `true`，则删除数据集中的所有表格（默认值：`false`）

### 表格

#### 列出表格

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables
```

**查询参数：**
- `maxResults` - 返回的最大结果数量
- `pageToken` - 分页令牌

#### 获取表格

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}
```

#### 创建表格

```bash
POST /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables
Content-Type: application/json

{
  "tableReference": {
    "projectId": "{projectId}",
    "datasetId": "{datasetId}",
    "tableId": "my_table"
  },
  "schema": {
    "fields": [
      {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
      {"name": "name", "type": "STRING", "mode": "NULLABLE"},
      {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"}
    ]
  }
}
```

**响应：**
```json
{
  "kind": "bigquery#table",
  "id": "my-project:my_dataset.my_table",
  "tableReference": {
    "projectId": "my-project",
    "datasetId": "my_dataset",
    "tableId": "my_table"
  },
  "schema": {
    "fields": [
      {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
      {"name": "name", "type": "STRING", "mode": "NULLABLE"},
      {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"}
    ]
  },
  "numRows": "0",
  "type": "TABLE"
}
```

#### 更新表格（PATCH）

```bash
PATCH /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}
Content-Type: application/json

{
  "description": "Updated table description"
}
```

#### 删除表格

```bash
DELETE /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}
```

### 表格数据

#### 列出表格数据

从表格中检索行。

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/data
```

**查询参数：**
- `maxResults` - 返回的最大结果数量
- `pageToken` - 分页令牌
- `startIndex` - 开始行的基于零的索引

**响应：**
```json
{
  "kind": "bigquery#tableDataList",
  "totalRows": "100",
  "rows": [
    {
      "f": [
        {"v": "1"},
        {"v": "Alice"},
        {"v": "1.7710597807E9"}
      ]
    }
  ],
  "pageToken": "..."
}
```

#### 插入表格数据（流式插入）

使用流式插入将行插入表格。注意：需要 BigQuery 的付费版本。

```bash
POST /google-bigquery/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/insertAll
Content-Type: application/json

{
  "rows": [
    {"json": {"id": 1, "name": "Alice"}},
    {"json": {"id": 2, "name": "Bob"}}
  ]
}
```

### 作业和查询

#### 运行查询（同步）

执行 SQL 查询并直接返回结果。

```bash
POST /google-bigquery/bigquery/v2/projects/{projectId}/queries
Content-Type: application/json

{
  "query": "SELECT * FROM `my_dataset.my_table` LIMIT 10",
  "useLegacySql": false,
  "maxResults": 100
}
```

**响应：**
```json
{
  "kind": "bigquery#queryResponse",
  "schema": {
    "fields": [
      {"name": "id", "type": "INTEGER"},
      {"name": "name", "type": "STRING"}
    ]
  },
  "jobReference": {
    "projectId": "my-project",
    "jobId": "job_abc123",
    "location": "US"
  },
  "totalRows": "2",
  "rows": [
    {"f": [{"v": "1"}, {"v": "Alice"}]},
    {"f": [{"v": "2"}, {"v": "Bob"}]}
  ],
  "jobComplete": true,
  "totalBytesProcessed": "1024"
}
```

**查询参数：**
- `useLegacySql` - 使用旧版 SQL 语法（对于 GoogleSQL，默认值为 `false`）
- `maxResults` - 每页的最大结果数量
- `timeoutMs` - 查询超时时间（以毫秒为单位）

#### 创建作业（异步）

提交作业以进行异步执行。

```bash
POST /google-bigquery/bigquery/v2/projects/{projectId}/jobs
Content-Type: application/json

{
  "configuration": {
    "query": {
      "query": "SELECT * FROM `my_dataset.my_table`",
      "useLegacySql": false,
      "destinationTable": {
        "projectId": "{projectId}",
        "datasetId": "{datasetId}",
        "tableId": "results_table"
      },
      "writeDisposition": "WRITE_TRUNCATE"
    }
  }
}
```

#### 列出作业

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/jobs
```

**查询参数：**
- `maxResults` - 返回的最大结果数量
- `pageToken` - 分页令牌
- `stateFilter` - 按作业状态过滤：`done`、`pending`、`running`
- `projection` - `full` 或 `minimal`

**响应：**
```json
{
  "kind": "bigquery#jobList",
  "jobs": [
    {
      "id": "my-project:US.job_abc123",
      "jobReference": {
        "projectId": "my-project",
        "jobId": "job_abc123",
        "location": "US"
      },
      "state": "DONE",
      "statistics": {
        "creationTime": "1771059781456",
        "startTime": "1771059782203",
        "endTime": "1771059782324"
      }
    }
  ]
}
```

#### 获取作业

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/jobs/{jobId}
```

**查询参数：**
- `location` - 作业位置（例如：“US”、“EU”）

#### 获取查询结果

从已完成的查询作业中检索结果。

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/queries/{jobId}
```

**查询参数：**
- `location` - 作业位置
- `maxResults` - 每页的最大结果数量
- `pageToken` - 分页令牌
- `startIndex` - 基于零的起始行

#### 取消作业

```bash
POST /google-bigquery/bigquery/v2/projects/{projectId}/jobs/{jobId}/cancel
```

**查询参数：**
- `location` - 作业位置

## 分页

BigQuery 使用基于令牌的分页。当存在更多结果时，列表响应中会包含 `pageToken`：

```bash
GET /google-bigquery/bigquery/v2/projects/{projectId}/datasets?maxResults=10&pageToken={token}
```

**响应：**
```json
{
  "datasets": [...],
  "nextPageToken": "eyJvZmZzZXQiOjEwfQ=="
}
```

在后续请求中将 `nextPageToken` 值作为 `pageToken` 使用。

## 代码示例

### JavaScript

```javascript
// Run a query
const response = await fetch(
  'https://gateway.maton.ai/google-bigquery/bigquery/v2/projects/my-project/queries',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: 'SELECT * FROM `my_dataset.my_table` LIMIT 10',
      useLegacySql: false
    })
  }
);
const data = await response.json();
console.log(data.rows);
```

### Python

```python
import os
import requests

# Run a query
response = requests.post(
    'https://gateway.maton.ai/google-bigquery/bigquery/v2/projects/my-project/queries',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'query': 'SELECT * FROM `my_dataset.my_table` LIMIT 10',
        'useLegacySql': False
    }
)
data = response.json()
for row in data.get('rows', []):
    print([field['v'] for field in row['f']])
```

## 数据库模式字段类型

BigQuery 表格模式的常见数据类型：

| 类型 | 描述 |
|------|-------------|
| `STRING` | 可变长度的字符数据 |
| `INTEGER` | 64 位有符号整数 |
| `FLOAT` | 64 位 IEEE 浮点数 |
| `BOOLEAN` | 真或假 |
| `TIMESTAMP` | 绝对时间点 |
| `DATE` | 日历日期 |
| `TIME` | 一天中的时间 |
| `DATETIME` | 日期和时间 |
| `BYTES` | 可变长度的二进制数据 |
| `NUMERIC` | 具有 38 位精度的精确数值 |
| `BIGNUMERIC` | 具有 76 位以上精度的精确数值 |
| `GEOGRAPHY` | 地理数据 |
| `JSON` | JSON 数据 |
| `RECORD` | 嵌套字段（也称为 STRUCT） |

**字段模式：**
- `NULLABLE` - 字段可以为 null（默认值）
- `REQUIRED` - 字段不能为 null
- `REPEATED` - 字段是一个数组

## 注意事项

- 项目 ID 通常采用 `project-name` 或 `project-name-12345` 的格式。
- 数据集 ID 遵循命名规则：字母、数字、下划线（最多 1024 个字符）。
- 表格 ID 遵循与数据集相同的命名规则。
- 作业 ID 由 BigQuery 生成，并包含位置前缀。
- 查询结果使用 `f`（字段）和 `v`（值）结构。
- 流式插入需要 BigQuery 的付费版本（免费版本不可用）。
- 对于 GoogleSQL（标准 SQL）语法，请使用 `useLegacySql: false`。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 来禁用全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少 Google BigQuery 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 访问被拒绝（权限不足或超出配额） |
| 404 | 资源未找到（项目、数据集、表格或作业） |
| 409 | 资源已存在 |
| 429 | 速率限制 |
| 4xx/5xx | 来自 BigQuery API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥的有效性：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `google-bigquery` 开头。例如：

- 正确：`https://gateway.maton.ai/google-bigquery/bigquery/v2/projects`
- 错误：`https://gateway.maton.ai/bigquery/v2/projects`

## 资源

- [BigQuery API 概述](https://cloud.google.com/bigquery/docs/reference/rest)
- [数据集](https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets)
- [表格](https://cloud.google.com/bigquery/docs/reference/rest/v2/tables)
- [作业](https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs)
- [表格数据](https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata)
- [标准 SQL 参考](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)