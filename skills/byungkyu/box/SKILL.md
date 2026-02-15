---
name: box
description: |
  Box API integration with managed OAuth. Manage files, folders, collaborations, and cloud storage.
  Use this skill when users want to upload, download, share, or organize files and folders in Box.
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

# Box

使用托管的 OAuth 认证来访问 Box API。您可以管理文件、文件夹、协作内容、共享链接以及云存储资源。

## 快速入门

```bash
# Get current user info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/box/2.0/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/box/2.0/{resource}
```

网关会将请求代理到 `api.box.com/2.0`，并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Box OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=box&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'box'}).encode()
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
    "connection_id": "bd484938-0902-4fc0-9ffb-2549d7d91f1d",
    "status": "ACTIVE",
    "creation_time": "2026-02-08T21:14:41.808115Z",
    "last_updated_time": "2026-02-08T21:16:10.100340Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "box",
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

如果您有多个 Box 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/box/2.0/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'bd484938-0902-4fc0-9ffb-2549d7d91f1d')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户信息

#### 获取当前用户

```bash
GET /box/2.0/users/me
```

**响应：**
```json
{
  "type": "user",
  "id": "48806418054",
  "name": "Chris",
  "login": "chris@example.com",
  "created_at": "2026-02-08T13:12:34-08:00",
  "modified_at": "2026-02-08T13:12:35-08:00",
  "language": "en",
  "timezone": "America/Los_Angeles",
  "space_amount": 10737418240,
  "space_used": 0,
  "max_upload_size": 262144000,
  "status": "active",
  "avatar_url": "https://app.box.com/api/avatar/large/48806418054"
}
```

#### 获取用户信息

```bash
GET /box/2.0/users/{user_id}
```

### 文件夹操作

#### 获取根文件夹

根文件夹的 ID 为 `0`：

```bash
GET /box/2.0/folders/0
```

#### 获取文件夹信息

```bash
GET /box/2.0/folders/{folder_id}
```

**响应：**
```json
{
  "type": "folder",
  "id": "365037181307",
  "name": "My Folder",
  "description": "Folder description",
  "size": 0,
  "path_collection": {
    "total_count": 1,
    "entries": [
      {"type": "folder", "id": "0", "name": "All Files"}
    ]
  },
  "created_by": {"type": "user", "id": "48806418054", "name": "Chris"},
  "owned_by": {"type": "user", "id": "48806418054", "name": "Chris"},
  "item_status": "active"
}
```

#### 列出文件夹内容

```bash
GET /box/2.0/folders/{folder_id}/items
```

查询参数：
- `limit` - 返回的最大项目数量（默认为 100，最大值为 1000）
- `offset` - 分页偏移量
- `fields` - 需要包含的字段列表（用逗号分隔）

**响应：**
```json
{
  "total_count": 1,
  "entries": [
    {
      "type": "folder",
      "id": "365036703666",
      "name": "Subfolder"
    }
  ],
  "offset": 0,
  "limit": 100
}
```

#### 创建文件夹

```bash
POST /box/2.0/folders
Content-Type: application/json

{
  "name": "New Folder",
  "parent": {"id": "0"}
}
```

**响应：**
```json
{
  "type": "folder",
  "id": "365037181307",
  "name": "New Folder",
  "created_at": "2026-02-08T14:56:17-08:00"
}
```

#### 更新文件夹信息

```bash
PUT /box/2.0/folders/{folder_id}
Content-Type: application/json

{
  "name": "Updated Folder Name",
  "description": "Updated description"
}
```

#### 复制文件夹

```bash
POST /box/2.0/folders/{folder_id}/copy
Content-Type: application/json

{
  "name": "Copied Folder",
  "parent": {"id": "0"}
}
```

#### 删除文件夹

```bash
DELETE /box/2.0/folders/{folder_id}
```

查询参数：
- `recursive` - 设置为 `true` 以删除非空文件夹

成功时返回 204（表示“无内容”）。

### 文件操作

#### 获取文件信息

```bash
GET /box/2.0/files/{file_id}
```

#### 下载文件

```bash
GET /box/2.0/files/{file_id}/content
```

返回文件的下载 URL。

#### 上传文件

```bash
POST https://upload.box.com/api/2.0/files/content
Content-Type: multipart/form-data

attributes={"name":"file.txt","parent":{"id":"0"}}
file=<binary data>
```

**注意：** 文件上传使用不同的基础 URL：`upload.box.com`。

#### 更新文件信息

```bash
PUT /box/2.0/files/{file_id}
Content-Type: application/json

{
  "name": "renamed-file.txt",
  "description": "File description"
}
```

#### 复制文件

```bash
POST /box/2.0/files/{file_id}/copy
Content-Type: application/json

{
  "name": "copied-file.txt",
  "parent": {"id": "0"}
}
```

#### 删除文件

```bash
DELETE /box/2.0/files/{file_id}
```

成功时返回 204（表示“无内容”）。

#### 获取文件版本

```bash
GET /box/2.0/files/{file_id}/versions
```

### 共享链接

通过更新文件或文件夹来创建共享链接：

```bash
PUT /box/2.0/folders/{folder_id}
Content-Type: application/json

{
  "shared_link": {
    "access": "open"
  }
}
```

访问权限级别：
- `open` - 任何拥有链接的人都可以访问
- `company` - 仅企业内的用户可以访问
- `collaborators` - 仅协作用户可以访问

**响应包含：**
```json
{
  "shared_link": {
    "url": "https://app.box.com/s/sisarrztrenabyygfwqggbwommf8uucv",
    "access": "open",
    "effective_access": "open",
    "is_password_enabled": false,
    "permissions": {
      "can_preview": true,
      "can_download": true,
      "can_edit": false
    }
  }
}
```

### 协作内容

#### 列出文件夹的协作关系

```bash
GET /box/2.0/folders/{folder_id}/collaborations
```

#### 创建协作关系

```bash
POST /box/2.0/collaborations
Content-Type: application/json

{
  "item": {"type": "folder", "id": "365037181307"},
  "accessible_by": {"type": "user", "login": "user@example.com"},
  "role": "editor"
}
```

角色：`editor`（编辑者）、`viewer`（查看者）、`previewer`（预览者）、`uploader`（上传者）、`previewer_uploader`（预览者上传者）、`viewer_uploader`（查看者上传者）、`co-owner`（共同所有者）

#### 更新协作关系

```bash
PUT /box/2.0/collaborations/{collaboration_id}
Content-Type: application/json

{
  "role": "viewer"
}
```

#### 删除协作关系

```bash
DELETE /box/2.0/collaborations/{collaboration_id}
```

### 搜索

```bash
GET /box/2.0/search?query=document
```

查询参数：
- `query` - 搜索查询
- `type` - 按类型过滤：`file`（文件）、`folder`（文件夹）、`web_link`（共享链接）
- `file_extensions` - 用逗号分隔的文件扩展名
- `ancestor_folder_ids` - 限制在特定文件夹内搜索
- `limit` - 最大结果数量（默认为 30）
- `offset` - 分页偏移量

**响应：**
```json
{
  "total_count": 5,
  "entries": [...],
  "limit": 30,
  "offset": 0,
  "type": "search_results_items"
}
```

### 事件

```bash
GET /box/2.0/events
```

查询参数：
- `stream_type` - `all`（所有事件）、`changes`（变更事件）、`sync`（同步事件）、`admin_logs`（管理员日志）
- `stream_position` - 开始搜索的位置
- `limit` - 返回的最大事件数量

**响应：**
```json
{
  "chunk_size": 4,
  "next_stream_position": "30401068076164269",
  "entries": [...]
}
```

### 回收站

#### 列出回收站中的项目

```bash
GET /box/2.0/folders/trash/items
```

#### 获取回收站中的项目

```bash
GET /box/2.0/files/{file_id}/trash
GET /box/2.0/folders/{folder_id}/trash
```

#### 恢复回收站中的项目

```bash
POST /box/2.0/files/{file_id}
POST /box/2.0/folders/{folder_id}
```

#### 永久删除项目

```bash
DELETE /box/2.0/files/{file_id}/trash
DELETE /box/2.0/folders/{folder_id}/trash
```

### 收藏夹（收藏项目）

#### 列出收藏夹

```bash
GET /box/2.0/collections
```

**响应：**
```json
{
  "total_count": 1,
  "entries": [
    {
      "type": "collection",
      "name": "Favorites",
      "collection_type": "favorites",
      "id": "35223030868"
    }
  ]
}
```

#### 获取收藏夹中的项目

```bash
GET /box/2.0/collections/{collection_id}/items
```

### 最新项目

```bash
GET /box/2.0/recent_items
```

### Webhook

#### 列出 Webhook

```bash
GET /box/2.0/webhooks
```

#### 创建 Webhook

```bash
POST /box/2.0/webhooks
Content-Type: application/json

{
  "target": {"id": "365037181307", "type": "folder"},
  "address": "https://example.com/webhook",
  "triggers": ["FILE.UPLOADED", "FILE.DOWNLOADED"]
}
```

**注意：** 创建 Webhook 可能需要企业管理员权限。

#### 删除 Webhook

```bash
DELETE /box/2.0/webhooks/{webhook_id}
```

## 分页

Box 使用基于偏移量的分页机制：

```bash
GET /box/2.0/folders/0/items?limit=100&offset=0
GET /box/2.0/folders/0/items?limit=100&offset=100
```

某些端点使用基于标记的分页机制，需要 `marker` 参数。

**响应：**
```json
{
  "total_count": 250,
  "entries": [...],
  "offset": 0,
  "limit": 100
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/box/2.0/folders/0/items',
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
    'https://gateway.maton.ai/box/2.0/folders/0/items',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### Python（创建文件夹）

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/box/2.0/folders',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'name': 'New Folder',
        'parent': {'id': '0'}
    }
)
folder = response.json()
print(f"Created folder: {folder['id']}")
```

## 注意事项

- 根文件夹的 ID 为 `0`。
- 文件上传使用 `upload.box.com`，而不是 `api.box.com`。
- 删除操作成功时返回 204（表示“无内容”）。
- 使用 `fields` 参数可以请求特定的字段，从而减少响应大小。
- 共享链接可以设置密码保护和过期日期。
- 某些操作（如列出用户、创建 Webhook）需要企业管理员权限。
- 可以使用 ETags 通过 `If-Match` 头部进行条件性更新。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中，环境变量（如 `$MATON_API_KEY`）可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Box 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 操作权限不足 |
| 404 | 资源未找到 |
| 409 | 冲突（例如，存在同名项目） |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Box API 的传递错误 |

Box 的错误会包含详细的错误信息：
```json
{
  "type": "error",
  "status": 409,
  "code": "item_name_in_use",
  "message": "Item with the same name already exists"
}
```

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

1. 确保您的 URL 路径以 `box` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/box/2.0/users/me`
- 错误的路径：`https://gateway.maton.ai/2.0/users/me`

## 资源

- [Box API 参考](https://developer.box.com/reference)
- [Box 开发者文档](https://developer.box.com/guides)
- [认证指南](https://developer.box.com/guides/authentication)
- [Box SDKs](https://developer.box.com/sdks-and-tools)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)