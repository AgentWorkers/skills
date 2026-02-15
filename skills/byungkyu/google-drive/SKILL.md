---
name: google-drive
description: |
  Google Drive API integration with managed OAuth. List, search, create, and manage files and folders. Use this skill when users want to interact with Google Drive files. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Drive

通过管理的 OAuth 认证来访问 Google Drive API。可以列出、搜索、创建和管理文件及文件夹。

## 快速入门

```bash
# List files
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-drive/drive/v3/files?pageSize=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-drive/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google Drive API 端点路径。该网关会将请求代理到 `www.googleapis.com` 并自动插入您的 OAuth 令牌。

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

在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-drive&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-drive'}).encode()
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
    "app": "google-drive",
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

如果您有多个 Google Drive 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-drive/drive/v3/files?pageSize=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 列出文件

```bash
GET /google-drive/drive/v3/files?pageSize=10
```

- 带查询参数：
  - `name = '确切的文件名'`
  - `name contains '部分名称'`
  - `mimeType = 'application/pdf'`
  - `'folderId' in parents`
  - `trashed = false`
  - `modifiedTime > '2024-01-01T00:00:00'`

- 使用 `and` 进行组合查询：
  ```
name contains 'report' and mimeType = 'application/pdf'
```

## 常见 MIME 类型

- `application/vnd.google-apps.document` - Google 文档
- `application/vnd.google-apps.spreadsheet` - Google 表格
- `application/vnd.google-apps.presentation` - Google 幻灯片
- `application/vnd.google-apps.folder` - 文件夹
- `application/pdf` - PDF 文件

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/google-drive/drive/v3/files?pageSize=10',
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
    'https://gateway.maton.ai/google-drive/drive/v3/files',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'pageSize': 10}
)
```

## 注意事项

- 使用 `fields` 参数来限制响应数据。
- 分页功能使用上一次响应中的 `nextPageToken`。
- 导出功能仅适用于 Google Workspace 文件。
- 重要提示：当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 命令可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致“无效 API 密钥”的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Google Drive 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Google Drive API 的传递错误 |

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

1. 确保您的 URL 路径以 `google-drive` 开头。例如：
  - 正确的路径：`https://gateway.maton.ai/google-drive/drive/v3/files`
  - 错误的路径：`https://gateway.maton.ai/drive/v3/files`

## 资源

- [Drive API 概述](https://developers.google.com/drive/api/reference/rest/v3)
- [列出文件](https://developers.google.com/drive/api/reference/rest/v3/files/list)
- [获取文件](https://developers.google.com/drive/api/reference/rest/v3/files/get)
- [创建文件](https://developers.google.com/drive/api/reference/rest/v3/files/create)
- [更新文件](https://developers.google.com/drive/api/reference/rest/v3/files/update)
- [删除文件](https://developers.google.com/drive/api/reference/rest/v3/files/delete)
- [导出文件](https://developers.google.com/drive/api/reference/rest/v3/files/export)
- [搜索查询语法](https://developers.google.com/drive/api/guides/search-files)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)