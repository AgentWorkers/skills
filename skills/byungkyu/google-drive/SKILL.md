---
name: google-drive
description: **Google Drive API集成与托管式OAuth**：支持列出、搜索、创建和管理文件及文件夹。当用户需要与Google Drive中的文件进行交互时，可使用此功能。对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
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

使用托管的OAuth认证来访问Google Drive API。可以列出、搜索、创建和管理文件及文件夹。

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

## 基本URL

```
https://gateway.maton.ai/google-drive/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Google Drive API端点路径。该网关会将请求代理到 `www.googleapis.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

在 `https://ctrl.maton.ai` 管理您的Google OAuth连接。

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
    "app": "google-drive",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth认证。

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

如果您有多个Google Drive连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-drive/drive/v3/files?pageSize=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 列出文件

```bash
GET /google-drive/drive/v3/files?pageSize=10
```

- 带查询参数的示例：
```bash
GET /google-drive/drive/v3/files?q=name%20contains%20'report'&pageSize=10
```

- 仅列出文件夹的示例：
```bash
GET /google-drive/drive/v3/files?q=mimeType='application/vnd.google-apps.folder'
```

- 列出特定文件夹中的文件的示例：
```bash
GET /google-drive/drive/v3/files?q='FOLDER_ID'+in+parents
```

- 带字段参数的示例：
```bash
GET /google-drive/drive/v3/files?fields=files(id,name,mimeType,createdTime,modifiedTime,size)
```

### 获取文件元数据

```bash
GET /google-drive/drive/v3/files/{fileId}?fields=id,name,mimeType,size,createdTime
```

### 下载文件内容

```bash
GET /google-drive/drive/v3/files/{fileId}?alt=media
```

### 导出Google文档

```bash
GET /google-drive/drive/v3/files/{fileId}/export?mimeType=application/pdf
```

### 创建文件（仅包含元数据）

```bash
POST /google-drive/drive/v3/files
Content-Type: application/json

{
  "name": "New Document",
  "mimeType": "application/vnd.google-apps.document"
}
```

### 创建文件夹

```bash
POST /google-drive/drive/v3/files
Content-Type: application/json

{
  "name": "New Folder",
  "mimeType": "application/vnd.google-apps.folder"
}
```

### 更新文件元数据

```bash
PATCH /google-drive/drive/v3/files/{fileId}
Content-Type: application/json

{
  "name": "Renamed File"
}
```

### 将文件移动到文件夹

```bash
PATCH /google-drive/drive/v3/files/{fileId}?addParents=NEW_FOLDER_ID&removeParents=OLD_FOLDER_ID
```

### 删除文件

```bash
DELETE /google-drive/drive/v3/files/{fileId}
```

### 复制文件

```bash
POST /google-drive/drive/v3/files/{fileId}/copy
Content-Type: application/json

{
  "name": "Copy of File"
}
```

## 文件上传

Google Drive支持三种上传方式，具体取决于文件大小以及是否需要包含元数据：

### 简单上传（媒体文件）

适用于文件大小不超过5MB且不需要设置元数据的情况：

```bash
POST /google-drive/upload/drive/v3/files?uploadType=media
Content-Type: text/plain

<file content>
```

**Python示例：**
```python
import urllib.request, os

file_content = b'Hello, this is file content!'

url = 'https://gateway.maton.ai/google-drive/upload/drive/v3/files?uploadType=media'
req = urllib.request.Request(url, data=file_content, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'text/plain')
response = urllib.request.urlopen(req)
```

### 多部分上传

适用于文件大小不超过5MB且需要包含元数据（如文件名、描述等）的情况：

```bash
POST /google-drive/upload/drive/v3/files?uploadType=multipart
Content-Type: multipart/related; boundary=boundary

--boundary
Content-Type: application/json; charset=UTF-8

{"name": "myfile.txt", "description": "My file"}
--boundary
Content-Type: text/plain

<file content>
--boundary--
```

**Python示例：**
```python
import urllib.request, os, json

boundary = '----Boundary'
metadata = json.dumps({'name': 'myfile.txt', 'description': 'My file'})
file_content = 'File content here'

body = f'''--{boundary}\r
Content-Type: application/json; charset=UTF-8\r
\r
{metadata}\r
--{boundary}\r
Content-Type: text/plain\r
\r
{file_content}\r
--{boundary}--'''.encode()

url = 'https://gateway.maton.ai/google-drive/upload/drive/v3/files?uploadType=multipart'
req = urllib.request.Request(url, data=body, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', f'multipart/related; boundary={boundary}')
response = urllib.request.urlopen(req)
```

### 可恢复上传（大文件）

适用于文件大于5MB的情况。该方法包括以下步骤：
1. 初始化上传会话 - 获取上传URI。
2. 分块上传文件 - 将文件分部分发送。
3. 支持恢复上传 - 如果上传中断，可以从上次中断的位置继续。

**步骤1：初始化上传会话**

```bash
POST /google-drive/upload/drive/v3/files?uploadType=resumable
Content-Type: application/json; charset=UTF-8
X-Upload-Content-Type: application/octet-stream
X-Upload-Content-Length: <file_size>

{"name": "large_file.bin"}
```

响应中会包含包含上传URI的 `Location` 头。

**步骤2：上传文件内容**

```bash
PUT <upload_uri>
Content-Length: <file_size>
Content-Type: application/octet-stream

<file content>
```

**Python示例（完整代码）：**
```python
import urllib.request, os, json

file_path = '/path/to/large_file.bin'
file_size = os.path.getsize(file_path)

# Step 1: Initiate resumable upload session
url = 'https://gateway.maton.ai/google-drive/upload/drive/v3/files?uploadType=resumable'
metadata = json.dumps({'name': 'large_file.bin'}).encode()

req = urllib.request.Request(url, data=metadata, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json; charset=UTF-8')
req.add_header('X-Upload-Content-Type', 'application/octet-stream')
req.add_header('X-Upload-Content-Length', str(file_size))

response = urllib.request.urlopen(req)
upload_uri = response.headers['Location']

# Step 2: Upload file in chunks (e.g., 5MB chunks)
chunk_size = 5 * 1024 * 1024
with open(file_path, 'rb') as f:
    offset = 0
    while offset < file_size:
        chunk = f.read(chunk_size)
        end = offset + len(chunk) - 1

        req = urllib.request.Request(upload_uri, data=chunk, method='PUT')
        req.add_header('Content-Length', str(len(chunk)))
        req.add_header('Content-Range', f'bytes {offset}-{end}/{file_size}')

        response = urllib.request.urlopen(req)
        offset += len(chunk)

result = json.load(response)
print(f"Uploaded: {result['id']}")
```

**恢复中断的上传：**

如果上传中断，可以查询上传URI以获取当前状态：

```python
req = urllib.request.Request(upload_uri, method='PUT')
req.add_header('Content-Length', '0')
req.add_header('Content-Range', 'bytes */*')
response = urllib.request.urlopen(req)
# Check Range header in response to get current offset
```

### 更新文件内容

要更新现有文件的内容：

```bash
PATCH /google-drive/upload/drive/v3/files/{fileId}?uploadType=media
Content-Type: text/plain

<new file content>
```

**Python示例：**
```python
import urllib.request, os

file_id = 'YOUR_FILE_ID'
new_content = b'Updated file content!'

url = f'https://gateway.maton.ai/google-drive/upload/drive/v3/files/{file_id}?uploadType=media'
req = urllib.request.Request(url, data=new_content, method='PATCH')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'text/plain')
response = urllib.request.urlopen(req)
```

### 上传到特定文件夹

在元数据中包含文件夹ID：

```python
metadata = json.dumps({
    'name': 'myfile.txt',
    'parents': ['FOLDER_ID']
})
```

### 共享文件

```bash
POST /google-drive/drive/v3/files/{fileId}/permissions
Content-Type: application/json

{
  "role": "reader",
  "type": "user",
  "emailAddress": "user@example.com"
}
```

## 查询操作符

在 `q` 参数中使用以下操作符：
- `name = '确切的文件名'`
- `name contains '部分名称'`
- `mimeType = 'application/pdf'`
- `'folderId' in parents`
- `trashed = false`
- `modifiedTime > '2024-01-01T00:00:00'`

可以使用 `and` 进行组合查询：

```
name contains 'report' and mimeType = 'application/pdf'
```

## 常见MIME类型

- `application/vnd.google-apps.document` - Google文档
- `application/vnd.google-apps.spreadsheet` - Google表格
- `application/vnd.google-apps.presentation` - Google幻灯片
- `application/vnd.google-apps.folder` - 文件夹
- `application/pdf` - PDF

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

- 使用 `fields` 参数来限制响应数据量。
- 分页使用上一次响应中的 `nextPageToken`。
- 导出功能仅适用于Google Workspace文件。
- **上传类型**：
  - `uploadType=media`：用于简单上传（文件大小不超过5MB）。
  - `uploadType=multipart`：用于需要包含元数据的上传（文件大小不超过5MB）。
  - `uploadType=resumable`：用于大文件（推荐用于文件大小大于5MB的情况）。
- **上传端点**：文件上传使用 `/upload/drive/v3/files`（注意前缀 `/upload`）。
- **可恢复上传**：对于大文件，使用分块传输的方式进行上传（最小块大小为256KB，建议使用5MB的块大小）。
- **最大文件大小**：Google Drive支持最大5TB的文件。
- **重要提示**：当URL包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免glob解析问题。
- **重要提示**：在将curl输出传递给 `jq` 或其他命令时，某些shell环境中环境变量 `$MATON_API_KEY` 可能无法正确解析，可能会导致“无效API密钥”的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Google Drive连接 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（10次/秒） |
| 4xx/5xx | 来自Google Drive API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的URL路径以 `google-drive` 开头。例如：
  - 正确的路径：`https://gateway.maton.ai/google-drive/drive/v3/files`
  - 错误的路径：`https://gateway.maton.ai/drive/v3/files`

## 资源

- [Drive API概述](https://developers.google.com/drive/api/reference/rest/v3)
- [列出文件](https://developers.google.com/drive/api/reference/rest/v3/files/list)
- [获取文件](https://developers.google.com/drive/api/reference/rest/v3/files/get)
- [创建文件](https://developers.google.com/drive/api/reference/rest/v3/files/create)
- [更新文件](https://developers.google.com/drive/api/reference/rest/v3/files/update)
- [删除文件](https://developers.google.com/drive/api/reference/rest/v3/files/delete)
- [导出文件](https://developers.google.com/drive/api/reference/rest/v3/files/export)
- [上传文件](https://developers.google.com/drive/api/guides/manage-uploads)
- [可恢复上传](https://developers.google.com/drive/api/guides/manage-uploads#resumable)
- [搜索查询语法](https://developers.google.com/drive/api/guides/search-files)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)