---
name: dropbox
description: |
  Dropbox API integration with managed OAuth. Files, folders, search, metadata, and cloud storage.
  Use this skill when users want to manage files and folders in Dropbox, search content, or work with file metadata.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Dropbox

使用托管的 OAuth 认证来访问 Dropbox API。您可以管理文件和文件夹、搜索内容、检索元数据以及处理文件的版本信息。

## 快速入门

```bash
# List files in root folder
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"path": ""}).encode()
req = urllib.request.Request('https://gateway.maton.ai/dropbox/2/files/list_folder', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基础 URL

```
https://gateway.maton.ai/dropbox/2/{endpoint}
```

该网关会将请求代理到 `api.dropboxapi.com`，并自动插入您的 OAuth 令牌。

**重要提示：** Dropbox API v2 的所有端点都使用 POST 方法，并且请求体必须是 JSON 格式。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Dropbox OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=dropbox&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'dropbox'}).encode()
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
    "connection_id": "1efbb655-88e9-4a23-ad3b-f3e19cbff279",
    "status": "ACTIVE",
    "creation_time": "2026-02-09T23:34:49.818074Z",
    "last_updated_time": "2026-02-09T23:37:09.697559Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "dropbox",
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

如果您有多个 Dropbox 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"path": ""}).encode()
req = urllib.request.Request('https://gateway.maton.ai/dropbox/2/files/list_folder', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '1efbb655-88e9-4a23-ad3b-f3e19cbff279')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户

#### 获取当前账户信息

```bash
POST /dropbox/2/users/get_current_account
Content-Type: application/json

null
```

**响应：**
```json
{
  "account_id": "dbid:AAA-AdT84WzkyLw5s590DbYF1nGomiAoO8I",
  "name": {
    "given_name": "John",
    "surname": "Doe",
    "familiar_name": "John",
    "display_name": "John Doe",
    "abbreviated_name": "JD"
  },
  "email": "john@example.com",
  "email_verified": true,
  "disabled": false,
  "country": "US",
  "locale": "en",
  "account_type": {
    ".tag": "basic"
  },
  "root_info": {
    ".tag": "user",
    "root_namespace_id": "11989877987",
    "home_namespace_id": "11989877987"
  }
}
```

#### 获取空间使用情况

```bash
POST /dropbox/2/users/get_space_usage
Content-Type: application/json

null
```

**响应：**
```json
{
  "used": 538371,
  "allocation": {
    ".tag": "individual",
    "allocated": 2147483648
  }
}
```

### 文件和文件夹

#### 列出文件夹

使用空字符串 `""` 作为根文件夹路径。

**可选参数：**
- `recursive` - 包含子目录的内容（默认值：false）
- `include_deleted` - 包含已删除的文件（默认值：false）
- `include_media_info` - 包含照片/视频的媒体信息
- `limit` - 每次响应的最大条目数（1-2000）

**响应：**
```json
{
  "entries": [
    {
      ".tag": "file",
      "name": "document.pdf",
      "path_lower": "/document.pdf",
      "path_display": "/document.pdf",
      "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
      "client_modified": "2026-02-09T19:58:12Z",
      "server_modified": "2026-02-09T19:58:13Z",
      "rev": "016311c063b4f8700000002caa704e3",
      "size": 538371,
      "is_downloadable": true,
      "content_hash": "6542845d7b65ffc5358ebaa6981d991bab9fda194afa48bd727fcbe9e4a3158b"
    },
    {
      ".tag": "folder",
      "name": "Documents",
      "path_lower": "/documents",
      "path_display": "/Documents",
      "id": "id:Awe3Av8A8YYAAAAAAAAABw"
    }
  ],
  "cursor": "AAVqv-MUYFlM98b1QpFK6YaYC8L1s39lWjqbeqgWu4un...",
  "has_more": false
}
```

#### 继续列出文件夹

```bash
POST /dropbox/2/files/list_folder/continue
Content-Type: application/json

{
  "cursor": "AAVqv-MUYFlM98b1QpFK6YaYC8L1s39lWjqbeqgWu4un..."
}
```

当上一次响应中的 `has_more` 为 `true` 时使用此方法。

#### 获取元数据

```bash
POST /dropbox/2/files/get_metadata
Content-Type: application/json

{
  "path": "/document.pdf",
  "include_media_info": false,
  "include_deleted": false,
  "include_has_explicit_shared_members": false
}
```

**响应：**
```json
{
  ".tag": "file",
  "name": "document.pdf",
  "path_lower": "/document.pdf",
  "path_display": "/document.pdf",
  "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
  "client_modified": "2026-02-09T19:58:12Z",
  "server_modified": "2026-02-09T19:58:13Z",
  "rev": "016311c063b4f8700000002caa704e3",
  "size": 538371,
  "is_downloadable": true,
  "content_hash": "6542845d7b65ffc5358ebaa6981d991bab9fda194afa48bd727fcbe9e4a3158b"
}
```

#### 创建文件夹

```bash
POST /dropbox/2/files/create_folder_v2
Content-Type: application/json

{
  "path": "/New Folder",
  "autorename": false
}
```

**响应：**
```json
{
  "metadata": {
    "name": "New Folder",
    "path_lower": "/new folder",
    "path_display": "/New Folder",
    "id": "id:Awe3Av8A8YYAAAAAAAAABw"
  }
}
```

#### 复制文件或文件夹

```bash
POST /dropbox/2/files/copy_v2
Content-Type: application/json

{
  "from_path": "/source/file.pdf",
  "to_path": "/destination/file.pdf",
  "autorename": false
}
```

**响应：**
```json
{
  "metadata": {
    ".tag": "file",
    "name": "file.pdf",
    "path_lower": "/destination/file.pdf",
    "path_display": "/destination/file.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAACA"
  }
}
```

#### 移动文件或文件夹

```bash
POST /dropbox/2/files/move_v2
Content-Type: application/json

{
  "from_path": "/old/location/file.pdf",
  "to_path": "/new/location/file.pdf",
  "autorename": false
}
```

**响应：**
```json
{
  "metadata": {
    ".tag": "file",
    "name": "file.pdf",
    "path_lower": "/new/location/file.pdf",
    "path_display": "/new/location/file.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAACA"
  }
}
```

#### 删除文件或文件夹

```bash
POST /dropbox/2/files/delete_v2
Content-Type: application/json

{
  "path": "/file-to-delete.pdf"
}
```

**响应：**
```json
{
  "metadata": {
    ".tag": "file",
    "name": "file-to-delete.pdf",
    "path_lower": "/file-to-delete.pdf",
    "path_display": "/file-to-delete.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAABQ"
  }
}
```

#### 获取临时下载链接

```bash
POST /dropbox/2/files/get_temporary_link
Content-Type: application/json

{
  "path": "/document.pdf"
}
```

**响应：**
```json
{
  "metadata": {
    "name": "document.pdf",
    "path_lower": "/document.pdf",
    "path_display": "/document.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
    "size": 538371,
    "is_downloadable": true
  },
  "link": "https://uc785ee484c03b6556c091ea4491.dl.dropboxusercontent.com/cd/0/get/..."
}
```

该链接的有效时间为 4 小时。

### 搜索

#### 搜索文件

```bash
POST /dropbox/2/files/search_v2
Content-Type: application/json

{
  "query": "document",
  "options": {
    "path": "",
    "max_results": 100,
    "file_status": "active",
    "filename_only": false
  }
}
```

**响应：**
```json
{
  "has_more": false,
  "matches": [
    {
      "highlight_spans": [],
      "match_type": {
        ".tag": "filename"
      },
      "metadata": {
        ".tag": "metadata",
        "metadata": {
          ".tag": "file",
          "name": "document.pdf",
          "path_display": "/document.pdf",
          "path_lower": "/document.pdf",
          "id": "id:Awe3Av8A8YYAAAAAAAAABw"
        }
      }
    }
  ]
}
```

#### 继续搜索

```bash
POST /dropbox/2/files/search/continue_v2
Content-Type: application/json

{
  "cursor": "..."
}
```

### 文件版本

#### 列出文件版本

```bash
POST /dropbox/2/files/list_revisions
Content-Type: application/json

{
  "path": "/document.pdf",
  "mode": "path",
  "limit": 10
}
```

**响应：**
```json
{
  "is_deleted": false,
  "entries": [
    {
      "name": "document.pdf",
      "path_lower": "/document.pdf",
      "path_display": "/document.pdf",
      "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
      "client_modified": "2026-02-09T19:58:12Z",
      "server_modified": "2026-02-09T19:58:13Z",
      "rev": "016311c063b4f8700000002caa704e3",
      "size": 538371,
      "is_downloadable": true
    }
  ],
  "has_more": false
}
```

#### 恢复文件

```bash
POST /dropbox/2/files/restore
Content-Type: application/json

{
  "path": "/document.pdf",
  "rev": "016311c063b4f8700000002caa704e3"
}
```

### 标签

#### 获取标签信息

```bash
POST /dropbox/2/files/tags/get
Content-Type: application/json

{
  "paths": ["/document.pdf", "/folder"]
}
```

**响应：**
```json
{
  "paths_to_tags": [
    {
      "path": "/document.pdf",
      "tags": [
        {
          ".tag": "user_generated_tag",
          "tag_text": "important"
        }
      ]
    },
    {
      "path": "/folder",
      "tags": []
    }
  ]
}
```

#### 添加标签

```bash
POST /dropbox/2/files/tags/add
Content-Type: application/json

{
  "path": "/document.pdf",
  "tag_text": "important"
}
```

成功时返回 `null`。

**注意：** 标签文本必须符合 `[\w]+` 的模式（仅包含字母、数字和下划线，不允许使用连字符或空格）。

#### 删除标签

```bash
POST /dropbox/2/files/tags/remove
Content-Type: application/json

{
  "path": "/document.pdf",
  "tag_text": "important"
}
```

成功时返回 `null`。

### 批量操作

#### 删除批量文件

```bash
POST /dropbox/2/files/delete_batch
Content-Type: application/json

{
  "entries": [
    {"path": "/file1.pdf"},
    {"path": "/file2.pdf"}
  ]
}
```

返回异步作业 ID。使用 `/files/delete_batch/check` 查看作业状态。

#### 复制批量文件

```bash
POST /dropbox/2/files/copy_batch_v2
Content-Type: application/json

{
  "entries": [
    {"from_path": "/source/file1.pdf", "to_path": "/dest/file1.pdf"},
    {"from_path": "/source/file2.pdf", "to_path": "/dest/file2.pdf"}
  ],
  "autorename": false
}
```

#### 移动批量文件

```bash
POST /dropbox/2/files/move_batch_v2
Content-Type: application/json

{
  "entries": [
    {"from_path": "/old/file1.pdf", "to_path": "/new/file1.pdf"},
    {"from_path": "/old/file2.pdf", "to_path": "/new/file2.pdf"}
  ],
  "autorename": false
}
```

## 分页

Dropbox 使用基于游标的分页机制。当 `has_more` 为 `true` 时，使用返回的游标通过 `/continue` 端点继续分页。

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Initial request
response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/list_folder',
    headers=headers,
    json={'path': '', 'limit': 100}
)
result = response.json()
all_entries = result['entries']

# Continue while has_more is True
while result.get('has_more'):
    response = requests.post(
        'https://gateway.maton.ai/dropbox/2/files/list_folder/continue',
        headers=headers,
        json={'cursor': result['cursor']}
    )
    result = response.json()
    all_entries.extend(result['entries'])

print(f"Total entries: {len(all_entries)}")
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/dropbox/2/files/list_folder',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ path: '' })
  }
);
const data = await response.json();
console.log(data.entries);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/list_folder',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'path': ''}
)
data = response.json()
print(data['entries'])
```

### Python（创建文件夹和搜索）

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Create folder
response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/create_folder_v2',
    headers=headers,
    json={'path': '/My New Folder', 'autorename': False}
)
folder = response.json()
print(f"Created folder: {folder['metadata']['path_display']}")

# Search for files
response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/search_v2',
    headers=headers,
    json={'query': 'document'}
)
results = response.json()
print(f"Found {len(results['matches'])} matches")
```

## 注意事项

- 所有 Dropbox API v2 端点都使用 HTTP POST 方法。
- 请求体必须是 JSON 格式（而非表单编码格式）。
- 使用空字符串 `""` 作为根文件夹路径。
- 路径不区分大小写，但会保留大小写差异。
- 文件 ID（例如 `id:Awe3Av8A8YYAAAAAAAAABQ`）在文件被移动或重命名后仍然保持不变。
- 标签文本必须符合 `[\w]+` 的模式（仅包含字母、数字和下划线）。
- 临时下载链接的有效时间为 4 小时。
- 每个用户的请求速率限制较为宽松。
- **重要提示：** 当将 curl 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Dropbox 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 409 | 冲突（路径不存在、已存在等） |
| 429 | 请求速率受限 |
| 4xx/5xx | 来自 Dropbox API 的传递错误 |

错误响应会包含详细信息：
```json
{
  "error_summary": "path/not_found/...",
  "error": {
    ".tag": "path",
    "path": {
      ".tag": "not_found"
    }
  }
}
```

### 故障排除：API 密钥无效

**当收到“API 密钥无效”的错误时，请务必按照以下步骤操作，再确定是否存在问题：**

1. 检查 `MATON_API_KEY` 环境变量是否已设置：

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

## 资源

- [Dropbox HTTP API 概述](https://www.dropbox.com/developers/documentation/http/overview)
- [Dropbox 开发者门户](https://www.dropbox.com/developers)
- [Dropbox API 探索器](https://dropbox.github.io/dropbox-api-v2-explorer/)
- [DBX 文件访问指南](https://developers.dropbox.com/dbx-file-access-guide)