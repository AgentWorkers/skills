---
name: google-docs
description: |
  Google Docs API integration with managed OAuth. Create documents, insert text, apply formatting, and manage content. Use this skill when users want to interact with Google Docs. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google 文档（Google Docs）

使用托管的 OAuth 认证来访问 Google 文档 API。您可以创建文档、插入和格式化文本以及管理文档内容。

## 快速入门

```bash
# Get document
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-docs/v1/documents/{documentId}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-docs/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google 文档 API 端点路径。该网关会将请求代理到 `docs.googleapis.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-docs&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-docs'}).encode()
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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-docs",
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

如果您有多个 Google 文档连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-docs/v1/documents/{documentId}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 获取文档

```bash
GET /google-docs/v1/documents/{documentId}
```

### 创建文档

```bash
POST /google-docs/v1/documents
Content-Type: application/json

{
  "title": "New Document"
}
```

### 批量更新文档

```bash
POST /google-docs/v1/documents/{documentId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "insertText": {
        "location": {"index": 1},
        "text": "Hello, World!"
      }
    }
  ]
}
```

## 常见的批量更新请求

### 插入文本

```json
{
  "insertText": {
    "location": {"index": 1},
    "text": "Text to insert"
  }
}
```

### 删除内容

```json
{
  "deleteContentRange": {
    "range": {
      "startIndex": 1,
      "endIndex": 10
    }
  }
}
```

### 替换所有文本

```json
{
  "replaceAllText": {
    "containsText": {
      "text": "{{placeholder}}",
      "matchCase": true
    },
    "replaceText": "replacement value"
  }
}
```

### 插入表格

```json
{
  "insertTable": {
    "location": {"index": 1},
    "rows": 3,
    "columns": 3
  }
}
```

### 更新文本样式

```json
{
  "updateTextStyle": {
    "range": {
      "startIndex": 1,
      "endIndex": 10
    },
    "textStyle": {
      "bold": true,
      "fontSize": {"magnitude": 14, "unit": "PT"}
    },
    "fields": "bold,fontSize"
  }
}
```

### 插入分页符

```json
{
  "insertPageBreak": {
    "location": {"index": 1}
  }
}
```

## 代码示例

### JavaScript

```javascript
// Create document
const response = await fetch(
  'https://gateway.maton.ai/google-docs/v1/documents',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({ title: 'New Document' })
  }
);

// Insert text
await fetch(
  `https://gateway.maton.ai/google-docs/v1/documents/${docId}:batchUpdate`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      requests: [{ insertText: { location: { index: 1 }, text: 'Hello!' } }]
    })
  }
);
```

### Python

```python
import os
import requests

# Create document
response = requests.post(
    'https://gateway.maton.ai/google-docs/v1/documents',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'title': 'New Document'}
)
```

## 注意事项

- 索引位置从 1 开始（文档从索引 1 开始）。
- 使用 `endOfSegmentLocation` 在文档末尾添加内容。
- `batchUpdate` 中的多个请求会原子性地执行。
- 需要先获取文档才能找到正确的索引位置来进行更新。
- 在 `styleUpdate` 请求中，`fields` 参数使用字段掩码语法。
- **重要提示：** 当使用 `curl` 命令时，如果 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 以禁用全局解析。
- **重要提示：** 当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中，环境变量（如 `$MATON_API_KEY`）可能无法正确解析，这可能导致“无效的 API 密钥”错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google 文档连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Google 文档 API 的传递错误 |

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

1. 确保您的 URL 路径以 `google-docs` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/google-docs/v1/documents/{documentId}`
- 错误的格式：`https://gateway.maton.ai/docs/v1/documents/{documentId}`

## 资源

- [文档 API 概述](https://developers.google.com/docs/api/how-tos/overview)
- [获取文档](https://developers.google.com/docs/api/reference/rest/v1/documents/get)
- [创建文档](https://developers.google.com/docs/api/reference/rest/v1/documents/create)
- [批量更新](https://developers.google.com/docs/api/reference/rest/v1/documents/batchUpdate)
- [请求类型](https://developers.google.com/docs/api/reference/rest/v1/documents/request)
- [文档结构](https://developers.google.com/docs/api/concepts/structure)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)