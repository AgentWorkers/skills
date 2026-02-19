---
name: one-drive
description: >
  **OneDrive API集成：通过Microsoft Graph实现受管理的OAuth认证**  
  该功能允许用户通过Microsoft Graph管理OneDrive中的文件、文件夹以及文件共享设置。当用户需要上传、下载、整理或共享OneDrive中的文件时，可以使用此技能。  
  对于其他第三方应用程序，建议使用`api-gateway`技能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用此功能需要网络连接以及有效的Maton API密钥。
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---
# OneDrive

通过 Microsoft Graph 和管理的 OAuth 认证来访问 OneDrive API。您可以执行完整的 CRUD 操作（创建、读取、更新和删除）来管理文件、文件夹、驱动器以及文件共享功能。

## 快速入门

```bash
# List files in OneDrive root
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-drive/v1.0/me/drive/root/children')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/one-drive/v1.0/{resource}
```

该网关会将请求代理到 `graph.microsoft.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 OneDrive OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=one-drive&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'one-drive'}).encode()
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
    "connection_id": "3f17fb58-4515-4840-8ef6-2bbf0fa67e2c",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T08:23:30.317909Z",
    "last_updated_time": "2026-02-07T08:24:04.925298Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "one-drive",
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

如果您有多个 OneDrive 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-drive/v1.0/me/drive')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '3f17fb58-4515-4840-8ef6-2bbf0fa67e2c')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最新的）活动连接。

## API 参考

### 驱动器

#### 获取当前用户的驱动器

```bash
GET /one-drive/v1.0/me/drive
```

**响应：**
```json
{
  "id": "b!F3Y7M0VT80OO9iu_D6Z-LA...",
  "driveType": "personal",
  "name": "OneDrive",
  "owner": {
    "user": {
      "displayName": "John Doe",
      "id": "d4648f06c91d9d3d"
    }
  },
  "quota": {
    "total": 5368709120,
    "used": 1234567,
    "remaining": 5367474553
  }
}
```

#### 列出用户的驱动器

```bash
GET /one-drive/v1.0/me/drives
```

#### 通过 ID 获取驱动器

```bash
GET /one-drive/v1.0/drives/{drive-id}
```

### 文件和文件夹

#### 获取驱动器根目录

```bash
GET /one-drive/v1.0/me/drive/root
```

#### 列出根目录下的子文件夹

```bash
GET /one-drive/v1.0/me/drive/root/children
```

**响应：**
```json
{
  "value": [
    {
      "id": "F33B7653325337C3!s88...",
      "name": "Documents",
      "folder": {
        "childCount": 5
      },
      "createdDateTime": "2024-01-15T10:30:00Z",
      "lastModifiedDateTime": "2024-02-01T14:20:00Z"
    },
    {
      "id": "F33B7653325337C3!s3f...",
      "name": "report.pdf",
      "file": {
        "mimeType": "application/pdf",
        "hashes": {
          "sha1Hash": "cf23df2207d99a74fbe169e3eba035e633b65d94"
        }
      },
      "size": 35212
    }
  ]
}
```

#### 通过 ID 获取文件

```bash
GET /one-drive/v1.0/me/drive/items/{item-id}
```

#### 通过路径获取文件

使用冒号（:`）语法通过路径访问文件：

```bash
GET /one-drive/v1.0/me/drive/root:/Documents/report.pdf
```

#### 通过路径列出文件夹下的子文件夹

```bash
GET /one-drive/v1.0/me/drive/root:/Documents:/children
```

#### 获取文件的子文件

```bash
GET /one-drive/v1.0/me/drive/items/{item-id}/children
```

### 特定文件夹

可以通过名称访问已知的文件夹：

```bash
GET /one-drive/v1.0/me/drive/special/documents
GET /one-drive/v1.0/me/drive/special/photos
GET /one-drive/v1.0/me/drive/special/music
GET /one-drive/v1.0/me/drive/special/approot
```

### 最近使用的文件和共享文件

#### 获取最近使用的文件

```bash
GET /one-drive/v1.0/me/drive/recent
```

#### 获取与我共享的文件

```bash
GET /one-drive/v1.0/me/drive/sharedWithMe
```

### 搜索

```bash
GET /one-drive/v1.0/me/drive/root/search(q='{query}')
```

示例：
```bash
GET /one-drive/v1.0/me/drive/root/search(q='budget')
```

### 创建文件夹

```bash
POST /one-drive/v1.0/me/drive/root/children
Content-Type: application/json

{
  "name": "New Folder",
  "folder": {},
  "@microsoft.graph.conflictBehavior": "rename"
}
```

在另一个文件夹内创建文件夹：
```bash
POST /one-drive/v1.0/me/drive/items/{parent-id}/children
Content-Type: application/json

{
  "name": "Subfolder",
  "folder": {}
}
```

### 上传文件（简单 - 最大 4MB）

```bash
PUT /one-drive/v1.0/me/drive/items/{parent-id}:/{filename}:/content
Content-Type: application/octet-stream

{file binary content}
```

示例 - 上传到根目录：
```bash
PUT /one-drive/v1.0/me/drive/root:/document.txt:/content
Content-Type: text/plain

Hello, OneDrive!
```

### 上传文件（大文件 - 可分块上传）

对于超过 4MB 的文件，可以使用分块上传：

**步骤 1：创建上传会话**
```bash
POST /one-drive/v1.0/me/drive/root:/{filename}:/createUploadSession
Content-Type: application/json

{
  "item": {
    "@microsoft.graph.conflictBehavior": "rename"
  }
}
```

**响应：**
```json
{
  "uploadUrl": "https://sn3302.up.1drv.com/up/...",
  "expirationDateTime": "2024-02-08T10:00:00Z"
}
```

**步骤 2：将文件字节上传到 uploadUrl**

### 下载文件

获取文件元数据以获取下载 URL：

```bash
GET /one-drive/v1.0/me/drive/items/{item-id}
```

响应中包含 `@microsoft.graph.downloadUrl`——这是一个预授权的 URL，有效期较短：

```json
{
  "id": "...",
  "name": "document.pdf",
  "@microsoft.graph.downloadUrl": "https://public-sn3302.files.1drv.com/..."
}
```

直接使用此 URL 下载文件内容（无需认证头）。

### 更新文件（重命名/移动）

```bash
PATCH /one-drive/v1.0/me/drive/items/{item-id}
Content-Type: application/json

{
  "name": "new-name.txt"
}
```

将文件移动到其他文件夹：
```bash
PATCH /one-drive/v1.0/me/drive/items/{item-id}
Content-Type: application/json

{
  "parentReference": {
    "id": "{new-parent-id}"
  }
}
```

### 复制文件

```bash
POST /one-drive/v1.0/me/drive/items/{item-id}/copy
Content-Type: application/json

{
  "parentReference": {
    "id": "{destination-folder-id}"
  },
  "name": "copied-file.txt"
}
```

响应会返回 `202 Accepted` 和 `Location` 头，以便监控复制操作。

### 删除文件

```bash
DELETE /one-drive/v1.0/me/drive/items/{item-id}
```

成功时返回 `204 No Content`。

### 文件共享

#### 创建共享链接

```bash
POST /one-drive/v1.0/me/drive/items/{item-id}/createLink
Content-Type: application/json

{
  "type": "view",
  "scope": "anonymous"
}
```

链接类型：
- `view` - 只读访问
- `edit` - 读写访问
- `embed` - 可嵌入的链接

权限范围：
- `anonymous` - 任何拥有链接的人
- `organization` - 您组织中的任何人

**响应：**
```json
{
  "id": "...",
  "link": {
    "type": "view",
    "scope": "anonymous",
    "webUrl": "https://1drv.ms/b/..."
  }
}
```

#### 邀请用户（与特定人员共享）

```bash
POST /one-drive/v1.0/me/drive/items/{item-id}/invite
Content-Type: application/json

{
  "recipients": [
    {"email": "user@example.com"}
  ],
  "roles": ["read"],
  "sendInvitation": true,
  "message": "Check out this file!"
}
```

## 查询参数

使用 OData 查询参数来自定义响应：

- `$select` - 选择特定属性：`?$select=id,name,size`
- `$expand` - 包含相关资源：`?$expand=children`
- `$filter` - 过滤结果：`?$filter=file ne null`（仅限文件）
- `$orderby` - 对结果进行排序：`?$orderby=name`
- `$top` - 限制结果数量：`?$top=10`

示例：
```bash
GET /one-drive/v1.0/me/drive/root/children?$select=id,name,size&$top=20&$orderby=name
```

## 分页

结果会分页显示。响应中包含 `@odata.nextLink`，用于获取下一页：

```json
{
  "value": [...],
  "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/drive/root/children?$skiptoken=..."
}
```

使用 `@odata.nextLink` 中的完整 URL（不包括网关前缀）来获取下一页。

## 代码示例

### JavaScript

```javascript
// List files in root
const response = await fetch(
  'https://gateway.maton.ai/one-drive/v1.0/me/drive/root/children',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();

// Upload a file
const uploadResponse = await fetch(
  'https://gateway.maton.ai/one-drive/v1.0/me/drive/root:/myfile.txt:/content',
  {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'text/plain'
    },
    body: 'Hello, OneDrive!'
  }
);
```

### Python

```python
import os
import requests

# List files in root
response = requests.get(
    'https://gateway.maton.ai/one-drive/v1.0/me/drive/root/children',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
files = response.json()

# Upload a file
upload_response = requests.put(
    'https://gateway.maton.ai/one-drive/v1.0/me/drive/root:/myfile.txt:/content',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'text/plain'
    },
    data='Hello, OneDrive!'
)
```

## 注意事项

- OneDrive 使用 Microsoft Graph API (`graph.microsoft.com`)。
- 文件 ID 在驱动器内是唯一的。
- 使用冒号（:`）语法进行基于路径的访问：`/root:/path/to/file`。
- 简单上传的最大文件大小为 4MB；对于较大文件，请使用分块上传。
- 从 `@microsoft.graph.downloadUrl` 下载的文件 URL 是预授权的且临时的。
- 冲突处理选项：`fail`、`replace`、`rename`。
- 重要提示：当使用 curl 命令时，如果 URL 中包含括号，请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 OneDrive 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足 |
| 404 | 文件未找到 |
| 409 | 冲突（例如，文件已存在） |
| 429 | 请求速率限制（请检查 `Retry-After` 头） |
| 4xx/5xx | 来自 Microsoft Graph API 的传递错误 |

### 错误响应格式

```json
{
  "error": {
    "code": "itemNotFound",
    "message": "The resource could not be found."
  }
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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `one-drive` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/one-drive/v1.0/me/drive/root/children`
- 错误的路径：`https://gateway.maton.ai/v1.0/me/drive/root/children`

## 资源

- [OneDrive 开发者文档](https://learn.microsoft.com/en-us/onedrive/developer/)
- [Microsoft Graph API 参考](https://learn.microsoft.com/en-us/graph/api/overview)
- [DriveItem 资源](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [Drive 资源](https://learn.microsoft.com/en-us/graph/api/resources/drive)
- [共享和权限](https://learn.microsoft.com/en-us/onedrive/developer/rest-api/concepts/sharing)
- [大文件上传](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)