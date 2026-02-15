---
name: microsoft-excel
description: |
  Microsoft Excel API integration with managed OAuth. Read and write Excel workbooks, worksheets, ranges, tables, and charts stored in OneDrive.
  Use this skill when users want to read or modify Excel spreadsheets, manage worksheet data, work with tables, or access cell values.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Microsoft Excel

您可以使用托管的 OAuth 认证来访问 Microsoft Excel API（通过 Microsoft Graph）。您可以读取和写入存储在 OneDrive 或 SharePoint 中的工作簿、工作表、单元格范围、表格和图表。

## 快速入门

```bash
# List worksheets in a workbook
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/microsoft-excel/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Microsoft Graph API 端点路径。该网关会将请求代理到 `graph.microsoft.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 标头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Microsoft Excel OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=microsoft-excel&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'microsoft-excel'}).encode()
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
    "connection_id": "4751ac89-3970-47e1-872c-eacdf4291732",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T00:43:18.565932Z",
    "last_updated_time": "2026-02-07T00:43:29.729782Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "microsoft-excel",
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

如果您有多个 Microsoft Excel 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/microsoft-excel/v1.0/me/drive')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '4751ac89-3970-47e1-872c-eacdf4291732')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## 工作簿访问方式

您可以使用基于 ID 或基于路径的方式访问工作簿：

**通过文件 ID：**
```
/microsoft-excel/v1.0/me/drive/items/{file-id}/workbook/...
```

**通过文件路径：**
```
/microsoft-excel/v1.0/me/drive/root:/{path-to-file}:/workbook/...
```

## API 参考

### 驱动器操作

#### 获取驱动器信息

```bash
GET /microsoft-excel/v1.0/me/drive
```

#### 列出根目录下的文件

```bash
GET /microsoft-excel/v1.0/me/drive/root/children
```

#### 搜索 Excel 文件

```bash
GET /microsoft-excel/v1.0/me/drive/root/search(q='.xlsx')
```

#### 上传 Excel 文件

```bash
PUT /microsoft-excel/v1.0/me/drive/root:/{filename}.xlsx:/content
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

{binary xlsx content}
```

### 会话管理

会话可以提高多次操作的性能。建议用于批量操作。

#### 创建会话

```bash
POST /microsoft-excel/v1.0/me/drive/root:/{path}:/workbook/createSession
Content-Type: application/json

{
  "persistChanges": true
}
```

**响应：**
```json
{
  "persistChanges": true,
  "id": "cluster=PUS7&session=..."
}
```

在后续请求中使用会话 ID：
```
workbook-session-id: {session-id}
```

#### 关闭会话

```bash
POST /microsoft-excel/v1.0/me/drive/root:/{path}:/workbook/closeSession
workbook-session-id: {session-id}
```

### 工作表操作

#### 列出工作表

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets
```

**响应：**
```json
{
  "value": [
    {
      "id": "{00000000-0001-0000-0000-000000000000}",
      "name": "Sheet1",
      "position": 0,
      "visibility": "Visible"
    }
  ]
}
```

#### 获取工作表信息

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')
```

#### 创建工作表

```bash
POST /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets
Content-Type: application/json

{
  "name": "NewSheet"
}
```

#### 更新工作表

```bash
PATCH /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')
Content-Type: application/json

{
  "name": "RenamedSheet",
  "position": 2
}
```

#### 删除工作表

```bash
DELETE /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('{worksheet-id}')
```

成功时返回 204（表示“无内容”）。

### 单元格范围操作

#### 获取单元格范围

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/range(address='A1:B2')
```

**响应：**
```json
{
  "address": "Sheet1!A1:B2",
  "values": [
    ["Hello", "World"],
    [1, 2]
  ],
  "formulas": [
    ["Hello", "World"],
    [1, 2]
  ],
  "text": [
    ["Hello", "World"],
    ["1", "2"]
  ],
  "numberFormat": [
    ["General", "General"],
    ["General", "General"]
  ],
  "rowCount": 2,
  "columnCount": 2
}
```

#### 获取已使用的单元格范围

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/usedRange
```

#### 更新单元格范围

```bash
PATCH /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/range(address='A1:B2')
Content-Type: application/json

{
  "values": [
    ["Updated", "Values"],
    [100, 200]
  ]
}
```

#### 清空单元格范围

```bash
POST /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/range(address='A1:B2')/clear
Content-Type: application/json

{
  "applyTo": "All"
}
```

可选参数：`All`、`Formats`、`Contents`

### 表格操作

#### 列出表格

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/tables
```

#### 从单元格范围创建表格

```bash
POST /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/tables/add
Content-Type: application/json

{
  "address": "A1:C4",
  "hasHeaders": true
}
```

**响应：**
```json
{
  "id": "{6D182180-5F5F-448B-9E9C-377A5251CFC5}",
  "name": "Table1",
  "showHeaders": true,
  "showTotals": false,
  "style": "TableStyleMedium2"
}
```

#### 获取表格信息

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/tables('Table1')
```

#### 更新表格

```bash
PATCH /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/tables('Table1')
Content-Type: application/json

{
  "name": "PeopleTable",
  "showTotals": true
}
```

#### 获取表格行

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/tables('Table1')/rows
```

**响应：**
```json
{
  "value": [
    {
      "index": 0,
      "values": [["Alice", 30, "NYC"]]
    },
    {
      "index": 1,
      "values": [["Bob", 25, "LA"]]
    }
  ]
}
```

#### 添加表格行

```bash
POST /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/tables('Table1')/rows
Content-Type: application/json

{
  "values": [["Carol", 35, "Chicago"]]
}
```

#### 删除表格行

```bash
DELETE /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/tables('Table1')/rows/itemAt(index=0)
```

成功时返回 204（表示“无内容”）。

#### 获取表格列

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/tables('Table1')/columns
```

#### 添加表格列

```bash
POST /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/tables('Table1')/columns
Content-Type: application/json

{
  "values": [["Email"], ["alice@example.com"], ["bob@example.com"]]
}
```

### 命名项目

#### 列出命名项目

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/names
```

### 图表

#### 列出图表

```bash
GET /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/charts
```

#### 添加图表

```bash
POST /microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets('Sheet1')/charts/add
Content-Type: application/json

{
  "type": "ColumnClustered",
  "sourceData": "A1:C4",
  "seriesBy": "Auto"
}
```

## 代码示例

### JavaScript

```javascript
// Get range values
const response = await fetch(
  "https://gateway.maton.ai/microsoft-excel/v1.0/me/drive/root:/data.xlsx:/workbook/worksheets('Sheet1')/range(address='A1:B10')",
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.values);
```

### Python

```python
import os
import requests

# Update range values
response = requests.patch(
    "https://gateway.maton.ai/microsoft-excel/v1.0/me/drive/root:/data.xlsx:/workbook/worksheets('Sheet1')/range(address='A1:B2')",
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'values': [['Name', 'Age'], ['Alice', 30]]}
)
print(response.json())
```

## 注意事项

- 仅支持 `.xlsx` 格式的工作簿（不支持旧的 `.xls` 格式）。
- 包含特殊字符的工作表名称需要进行 URL 编码。
- 包含 `{` 和 `}` 的表格和工作表 ID 必须进行 URL 编码（使用 `%7B` 和 `%7D`）。
- 会话在大约 5 分钟无活动（持久会话）或 7 分钟后过期（非持久会话）。
- 在值数组中使用 `null` 可以跳过更新特定单元格。
- 空单元格应使用 `""`（空字符串）表示。
- 单元格范围地址使用 A1 标记法（例如：`A1:C10`、`Sheet1!A1:B5`）。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 可以防止全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Microsoft Excel 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 项目未找到或会话已过期 |
| 429 | 请求频率受限 |
| 4xx/5xx | 来自 Microsoft Graph API 的传递错误 |

### 常见错误代码

| 代码 | 描述 |
|------|-------------|
| `ItemNotFound` | 文件或资源不存在 |
| `ItemAlreadyExists` | 已存在同名的工作表或表格 |
| `InvalidArgument` | 参数无效或缺少必需字段 |
| `SessionNotFound` | 会话已过期或不存在 |

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

1. 确保您的 URL 路径以 `microsoft-excel` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/microsoft-excel/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets`
- 错误的格式：`https://gateway.maton.ai/v1.0/me/drive/root:/workbook.xlsx:/workbook/worksheets`

## 资源

- [Microsoft Graph Excel API 概述](https://learn.microsoft.com/en-us/graph/api/resources/excel)
- [在 Microsoft Graph 中使用 Excel](https://learn.microsoft.com/en-us/graph/excel-concept-overview)
- [Excel 工作簿资源](https://learn.microsoft.com/en-us/graph/api/resources/workbook)
- [Excel 工作表资源](https://learn.microsoft.com/en-us/graph/api/resources/worksheet)
- [Excel 单元格范围资源](https://learn.microsoft.com/en-us/graph/api/resources/range)
- [Excel 表格资源](https://learn.microsoft.com/en-us/graph/api/resources/table)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)