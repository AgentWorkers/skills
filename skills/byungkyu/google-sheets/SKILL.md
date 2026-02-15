---
name: google-sheets
description: |
  Google Sheets API integration with managed OAuth. Read and write spreadsheet data, create sheets, apply formatting, and manage ranges. Use this skill when users want to read from or write to Google Sheets. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Sheets

使用托管的 OAuth 认证来访问 Google Sheets API。您可以读取和写入电子表格的数据，创建新的电子表格，应用格式设置，并执行批量操作。

## 快速入门

```bash
# Read values from a spreadsheet (note: range is URL-encoded)
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-sheets/v4/spreadsheets/SPREADSHEET_ID/values/Sheet1%21A1%3AD10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-sheets/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google Sheets API 端点路径。该网关会将请求代理到 `sheets.googleapis.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-sheets&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-sheets'}).encode()
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
    "app": "google-sheets",
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

如果您连接了多个 Google 账户，请使用 `Maton-Connection` 头部指定要使用的账户：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-sheets/v4/spreadsheets/SPREADSHEET_ID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 获取电子表格元数据

```bash
GET /google-sheets/v4/spreadsheets/{spreadsheetId}
```

### 获取电子表格中的数据

```bash
GET /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}
```

示例：

```bash
GET /google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1%21A1%3AD10
```

### 获取多个范围的数据

```bash
GET /google-sheets/v4/spreadsheets/{spreadsheetId}/values:batchGet?ranges=Sheet1%21A1%3AB10&ranges=Sheet2%21A1%3AC5
```

### 更新电子表格中的数据

```bash
PUT /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}?valueInputOption=USER_ENTERED
Content-Type: application/json

{
  "values": [
    ["A1", "B1", "C1"],
    ["A2", "B2", "C2"]
  ]
}
```

### 向电子表格中追加数据

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}:append?valueInputOption=USER_ENTERED
Content-Type: application/json

{
  "values": [
    ["New Row 1", "Data", "More Data"],
    ["New Row 2", "Data", "More Data"]
  ]
}
```

### 批量更新电子表格中的数据

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}/values:batchUpdate
Content-Type: application/json

{
  "valueInputOption": "USER_ENTERED",
  "data": [
    {"range": "Sheet1!A1:B2", "values": [["A1", "B1"], ["A2", "B2"]]},
    {"range": "Sheet1!D1:E2", "values": [["D1", "E1"], ["D2", "E2"]]}
  ]
}
```

### 清空电子表格中的数据

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}:clear
```

### 创建电子表格

```bash
POST /google-sheets/v4/spreadsheets
Content-Type: application/json

{
  "properties": {"title": "New Spreadsheet"},
  "sheets": [{"properties": {"title": "Sheet1"}}]
}
```

### 批量更新（包括格式设置、添加电子表格等）

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {"addSheet": {"properties": {"title": "New Sheet"}}}
  ]
}
```

## 常见的批量更新请求

### 带格式设置更新单元格

```json
{
  "updateCells": {
    "rows": [
      {"values": [{"userEnteredValue": {"stringValue": "Name"}}, {"userEnteredValue": {"numberValue": 100}}]}
    ],
    "fields": "userEnteredValue",
    "start": {"sheetId": 0, "rowIndex": 0, "columnIndex": 0}
  }
}
```

### 格式化标题行（加粗 + 背景颜色）

```json
{
  "repeatCell": {
    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 3},
    "cell": {
      "userEnteredFormat": {
        "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
        "textFormat": {"bold": true}
      }
    },
    "fields": "userEnteredFormat(backgroundColor,textFormat)"
  }
}
```

### 自动调整列宽

```json
{
  "autoResizeDimensions": {
    "dimensions": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 3}
  }
}
```

### 重命名电子表格

```json
{
  "updateSheetProperties": {
    "properties": {"sheetId": 0, "title": "NewName"},
    "fields": "title"
  }
}
```

### 插入行/列

```json
{
  "insertDimension": {
    "range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 1, "endIndex": 3},
    "inheritFromBefore": true
  }
}
```

### 对范围进行排序

```json
{
  "sortRange": {
    "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 10, "startColumnIndex": 0, "endColumnIndex": 3},
    "sortSpecs": [{"dimensionIndex": 1, "sortOrder": "DESCENDING"}]
  }
}
```

### 添加过滤器

```json
{
  "setBasicFilter": {
    "filter": {
      "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 100, "startColumnIndex": 0, "endColumnIndex": 5}
    }
  }
}
```

### 删除电子表格

```json
{
  "deleteSheet": {"sheetId": 123456789}
}
```

## 数据输入选项

- `RAW` - 数据以原始形式存储。
- `USER_ENTERED` - 数据会被解析为用户在用户界面中输入的内容（公式会被执行，数字会被解析）。

## 范围表示法

- `Sheet1!A1:D10` - 指定范围。
- `Sheet1!A:D` - A 到 D 列的所有单元格。
- `Sheet1!1:10` - 1 到 10 行的所有单元格。
- `Sheet1` - 整个电子表格。
- `A1:D10` - 第一个电子表格中的范围。

## 代码示例

### JavaScript

```javascript
// Read values
const response = await fetch(
  'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:D10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

// Write values
await fetch(
  'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:B2?valueInputOption=USER_ENTERED',
  {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      values: [['A1', 'B1'], ['A2', 'B2']]
    })
  }
);
```

### Python

```python
import os
import requests

# Read values
response = requests.get(
    'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:D10',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)

# Write values
response = requests.put(
    'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:B2',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'valueInputOption': 'USER_ENTERED'},
    json={'values': [['A1', 'B1'], ['A2', 'B2']]}
)
```

## 注意事项

- 使用 `curl` 时，URL 路径中的范围需要使用 URL 编码（`!` -> `%21`，`:` -> `%3A`）。JavaScript 的 `fetch` 和 Python 的请求会自动处理编码。
- 使用 `valueInputOption=USER_ENTERED` 可以解析公式和数字。
- 请通过 Google Drive API 而不是 Sheets API 来删除电子表格。
- 电子表格的 ID 是数字格式的，可以在电子表格的元数据中找到。
- **重要提示：** 当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- **重要提示：** 当将 `curl` 的输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Google Sheets 连接。 |
| 401 | Maton API 密钥无效或缺失。 |
| 429 | 每个账户的请求速率限制为 10 次/秒。 |
| 4xx/5xx | 来自 Google Sheets API 的传递错误。 |

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

1. 确保您的 URL 路径以 `google-sheets` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/google-sheets/v4/spreadsheets/SPREADSHEET_ID`
- 错误的格式：`https://gateway.maton.ai/v4/spreadsheets/SPREADSHEET_ID`

## 资源

- [Sheets API 概述](https://developers.google.com/workspace/sheets/api/reference/rest)
- [获取电子表格信息](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/get)
- [创建电子表格](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/create)
- [批量更新电子表格](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate)
- [批量更新请求类型](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/request)
- [获取电子表格数据](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/get)
- [更新电子表格数据](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/update)
- [向电子表格中追加数据](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append)
- [批量获取电子表格数据](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/batchGet)
- [批量更新电子表格数据](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)